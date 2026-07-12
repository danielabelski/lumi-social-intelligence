#!/usr/bin/env python3
"""Build a public-readiness audit report for Lumi Social Intelligence.

Sprint 6 is a release-candidate hardening pass. This script is intentionally
read-only except for optional report/artifact output paths supplied by the
caller. It checks public safety, naming consistency, host claims, license files,
release archive contents, and the Lumi for Hermes clean inspection path.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_TRACKED_PARTS = {
    '.hermes',
    'runs',
    'logs',
    'cron',
    'state',
    'secrets',
    'private',
    '.env',
}
PRIVATE_TEXT_PATTERNS = (
    (re.compile(r'(?i)chat[_-]?id\s*[:=]'), 'chat id assignment'),
    (re.compile(r'(?i)job[_-]?id\s*[:=]'), 'job id assignment'),
    (re.compile(r'(?i)scheduler[_-]?id\s*[:=]'), 'scheduler id assignment'),
    (re.compile(r'(?i)(password|secret|api[_-]?key|token)\s*[:=]'), 'secret assignment'),
    (re.compile(r'\b\d{1,3}\.\d{5,},\s*\d{1,3}\.\d{5,}\b'), 'coordinate-like value'),
)
REQUIRED_PRODUCT_NAMES = ('Lumi Social Intelligence', 'Lumi Layered Memory', 'Nuances', 'Presence')
REQUIRED_HERMES_PREVIEW_CLAIMS = (
    "Hermes' selected memory provider remains authoritative",
    'Lumi reads selected context only through explicit host configuration',
    'Lumi emits proposals and receipts before any durable write',
    'Default preview mode is read-only plus reviewable proposal/receipt output',
)
GITHUB_ABOUT_RECOMMENDATION = {
    'description': 'Social-intelligence layer for agents: careful memory, contextual appraisal, and governed initiative.',
    'homepage': '',
    'topics': [
        'ai-agents',
        'agent-memory',
        'human-ai-interaction',
        'social-intelligence',
        'hermes-agent',
        'presence',
    ],
}


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, check=True, text=True, capture_output=True)


def _tracked_files() -> list[str]:
    return sorted(line for line in _run(['git', 'ls-files']).stdout.splitlines() if line)


def _ignored_local_artifacts() -> list[str]:
    result = _run(['git', 'ls-files', '--others', '--ignored', '--exclude-standard'])
    return sorted(line for line in result.stdout.splitlines() if line)


def _text_for(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def _check(name: str, findings: list[str] | None = None, details: dict[str, Any] | None = None) -> dict[str, Any]:
    findings = findings or []
    return {
        'name': name,
        'status': 'fail' if findings else 'pass',
        'findings': findings,
        'details': details or {},
    }


def tracked_files_check(tracked: list[str]) -> dict[str, Any]:
    findings = []
    for path in tracked:
        parts = set(Path(path).parts)
        if parts & FORBIDDEN_TRACKED_PARTS:
            findings.append(path)
    return _check('tracked_files', findings, {'count': len(tracked)})


def ignored_local_artifacts_check(ignored: list[str]) -> dict[str, Any]:
    sensitive = [path for path in ignored if any(part in FORBIDDEN_TRACKED_PARTS for part in Path(path).parts)]
    return _check('ignored_local_artifacts', [], {'ignored_count': len(ignored), 'sensitive_ignored_examples': sensitive[:20]})


def secret_privacy_scan_check(tracked: list[str]) -> dict[str, Any]:
    findings = []
    for path in tracked:
        if Path(path).suffix not in {'.md', '.py', '.sh', '.txt', '.toml', '.yaml', '.yml', '.json'} and Path(path).name not in {'LICENSE', 'NOTICE.md'}:
            continue
        if not (ROOT / path).is_file():
            findings.append(f'{path}: tracked path is not readable')
            continue
        if path.startswith('scripts/') or path.startswith('tests/'):
            continue
        try:
            text = _text_for(path)
        except UnicodeDecodeError:
            continue
        for pattern, label in PRIVATE_TEXT_PATTERNS:
            if pattern.search(text):
                findings.append(f'{path}: {label}')
    return _check('secret_privacy_scan', findings)


def naming_scan_check(tracked: list[str]) -> dict[str, Any]:
    docs = [path for path in tracked if path.endswith('.md') and not path.startswith('docs/articles/')]
    missing = []
    for path in ('README.md', 'docs/README.md', 'docs/product-brief.md', 'docs/architecture.md'):
        text = _text_for(path)
        absent = [name for name in REQUIRED_PRODUCT_NAMES if name not in text]
        if absent:
            missing.append(f'{path}: missing {absent}')
    bad_lowercase = []
    for path in docs:
        if not (ROOT / path).is_file():
            continue
        text = _text_for(path)
        if 'lumi layered memory' in text.lower() and 'Lumi Layered Memory' not in text:
            bad_lowercase.append(path)
    return _check('naming_scan', missing + bad_lowercase, {'docs_scanned': len(docs)})


def host_claim_scan_check() -> dict[str, Any]:
    adapter_text = _text_for('adapters/hermes/README.md')
    missing = [claim for claim in REQUIRED_HERMES_PREVIEW_CLAIMS if claim not in adapter_text]
    broad_claims = []
    for path in ('README.md', 'docs/host-compatibility.md', 'installers/lumi-for-hermes/README.md'):
        text = _text_for(path).lower()
        if 'production ready' in text or 'fully supports' in text or 'drop-in replacement' in text:
            broad_claims.append(path)
    return _check('host_claim_scan', missing + broad_claims)


def openclaw_deferred_scan_check(tracked: list[str]) -> dict[str, Any]:
    findings = [path for path in tracked if path.startswith(('adapters/openclaw/', 'installers/lumi-for-openclaw/'))]
    return _check('openclaw_deferred_scan', findings, {'deferred': True})


def license_notice_scan_check() -> dict[str, Any]:
    findings = []
    if 'MIT License' not in _text_for('LICENSE'):
        findings.append('LICENSE must be MIT')
    if 'Creative Commons Attribution 4.0 International License' not in _text_for('LICENSE-DOCS.md'):
        findings.append('LICENSE-DOCS.md must be CC BY 4.0')
    notice = _text_for('NOTICE.md')
    if 'split license model' not in notice or 'Project names, logos, and branding are reserved' not in notice:
        findings.append('NOTICE.md must document split license and reserved branding')
    return _check('license_notice_scan', findings)


def github_metadata_recommendation_check() -> dict[str, Any]:
    return _check('github_metadata_recommendation', [], GITHUB_ABOUT_RECOMMENDATION)


def _load_release_builder():
    script = ROOT / 'scripts' / 'build_release_artifacts.py'
    spec = importlib.util.spec_from_file_location('build_release_artifacts', script)
    if spec is None or spec.loader is None:
        raise RuntimeError('could not load build_release_artifacts.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def release_archive_scan_check(artifact_dir: Path) -> dict[str, Any]:
    builder = _load_release_builder()
    build_report = builder.build(artifact_dir, version='0.4.1')
    manifest_path = artifact_dir / 'release-manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    archive_path = artifact_dir / manifest['archive']
    with zipfile.ZipFile(archive_path) as zf:
        archive_members = sorted(zf.namelist())
    findings = []
    if manifest['private_material_findings']:
        findings.append('manifest contains private material findings')
    if manifest['canonical_writes'] != 0:
        findings.append('release build must report canonical_writes=0')
    if 'installers/lumi-for-hermes/preview.py' not in archive_members:
        findings.append('archive missing Lumi for Hermes preview')
    details = {
        'version': manifest['version'],
        'artifact_report': build_report,
        'archive': manifest['archive'],
        'archive_member_count': len(archive_members),
        'archive_members': archive_members,
        'private_material_findings': manifest['private_material_findings'],
        'canonical_writes': manifest['canonical_writes'],
        'v02_demo_verification': manifest.get('v02_demo_verification', {}),
        'v04_real_controls_evidence': manifest.get('v04_real_controls_evidence', {}),
        'native_telegram_reaction_evidence': manifest.get('native_telegram_reaction_evidence', {}),
        'package_artifacts': manifest['package_artifacts'],
    }
    return _check('release_archive_scan', findings, details)


def lumi_for_hermes_preview_scan_check() -> dict[str, Any]:
    result = _run(['python3', 'installers/lumi-for-hermes/preview.py', '--dry-run', '--root', '/tmp/lumi-hermes-preview'])
    payload = json.loads(result.stdout)
    safety = payload.get('safety', {})
    findings = []
    if payload.get('canonical_writes') != 0:
        findings.append('preview must report canonical_writes=0')
    if payload.get('would_write') != []:
        findings.append('preview must report no would_write paths')
    safety_text = ' '.join(safety if isinstance(safety, list) else [])
    if 'does not read Hermes private runtime state' not in safety_text:
        findings.append('preview must document no Hermes runtime reads')
    if 'does not write config, memory, scheduler, queues, or chat metadata' not in safety_text:
        findings.append('preview must document no runtime writes')
    if 'review-card output only' not in safety_text:
        findings.append('preview must remain review-card output only')
    return _check('lumi_for_hermes_preview_scan', findings, payload)


def build_report(artifact_dir: Path) -> dict[str, Any]:
    tracked = _tracked_files()
    ignored = _ignored_local_artifacts()
    checks = [
        tracked_files_check(tracked),
        ignored_local_artifacts_check(ignored),
        secret_privacy_scan_check(tracked),
        naming_scan_check(tracked),
        host_claim_scan_check(),
        openclaw_deferred_scan_check(tracked),
        license_notice_scan_check(),
        github_metadata_recommendation_check(),
        release_archive_scan_check(artifact_dir),
        lumi_for_hermes_preview_scan_check(),
    ]
    private_findings = [finding for check in checks for finding in check['findings']]
    return {
        'schema': 'lumi.public_readiness_audit.v1',
        'status': 'fail' if private_findings else 'pass',
        'canonical_writes': 0,
        'checks': checks,
        'private_material_findings': private_findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Build Lumi Social Intelligence public-readiness audit report.')
    parser.add_argument('--artifact-dir', type=Path, default=ROOT / 'dist' / 'public-readiness-audit')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args(argv)

    report = build_report(args.artifact_dir)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
