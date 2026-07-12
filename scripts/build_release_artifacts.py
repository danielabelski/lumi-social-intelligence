#!/usr/bin/env python3
"""Build deterministic Lumi Social Intelligence release artifacts.

Sprint 5 keeps release building local and inspectable: the script packages only
tracked public doorway files, writes artifacts to the requested output directory,
scans the archive member list for private/runtime material, and emits checksums.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.verify_v02_demo_package import verify as verify_v02_demo_package
from scripts.build_v04_real_controls_evidence import build_receipt as build_v04_receipt
from scripts.build_v041_native_reaction_evidence import build_receipt as build_v041_receipt
from scripts.build_v042_care_release_evidence import build_receipt as build_v042_receipt

DEFAULT_VERSION = '0.4.0'
FORBIDDEN_MEMBER_PATTERNS = (
    '.git/*',
    '.hermes/*',
    'runs/*',
    'logs/*',
    'cron/*',
    'state/*',
    'secrets/*',
    'private/*',
    '*__pycache__*',
    '*.pyc',
    '.pytest_cache/*',
    'dist/*',
    'build/*',
    '*.egg-info/*',
)
BASE_REQUIRED_RELEASE_MEMBERS = (
    'README.md',
    'LICENSE',
    'LICENSE-DOCS.md',
    'NOTICE.md',
    'docs/releases/v0.1.0.md',
    'docs/releases/v0.2.0.md',
    'docs/releases/v0.3.0.md',
    'docs/demos/v0.2-demo-evidence.json',
    'docs/demos/v0.2-demo-side-by-side.json',
    'docs/demos/v0.2-demo-side-by-side.md',
    'docs/demos/v0.2-demo-index.md',
    'docs/demos/v0.2-demo-script.md',
    'scripts/release_check.sh',
    'scripts/public_secret_scan.py',
    'scripts/public_readiness_audit.py',
    'scripts/prepare_release_candidate.py',
    'scripts/build_release_artifacts.py',
    'scripts/verify_v02_demo_package.py',
    'adapters/hermes/lumi_for_hermes.py',
    'adapters/hermes/README.md',
    'installers/lumi-for-hermes/preview.py',
    'installers/lumi-for-hermes/README.md',
    'core/presence/pyproject.toml',
)
VERSION_REQUIRED_RELEASE_MEMBERS = {
    '0.4.0': (
        'docs/releases/v0.4.0.md',
        'docs/evidence/v0.4.0-real-controls-evidence.json',
        'docs/evidence/v0.4.0-real-controls-evidence.md',
    ),
    '0.4.1': (
        'docs/releases/v0.4.1.md',
        'docs/evidence/v0.4.1-native-reaction-evidence.json',
        'docs/evidence/v0.4.1-native-reaction-evidence.md',
        'scripts/build_v041_native_reaction_evidence.py',
    ),
    '0.4.2': (
        'docs/releases/v0.4.2.md',
        'docs/evidence/v0.4.2-care-release-evidence.json',
        'docs/evidence/v0.4.2-care-release-evidence.md',
        'scripts/build_v042_care_release_evidence.py',
        'lumi_social_intelligence/care_release.py',
    ),
}


def _run_git_ls_files() -> list[str]:
    result = subprocess.run(
        ['git', 'ls-files'],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return sorted(line for line in result.stdout.splitlines() if line)


def _is_forbidden(member: str) -> bool:
    return any(fnmatch.fnmatch(member, pattern) for pattern in FORBIDDEN_MEMBER_PATTERNS)


def _private_material_findings(members: Iterable[str]) -> list[dict[str, str]]:
    findings = []
    for member in members:
        if _is_forbidden(member):
            findings.append({'path': member, 'reason': 'forbidden release archive member'})
    return findings


def _write_zip(archive_path: Path, members: list[str]) -> None:
    with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for member in members:
            source = ROOT / member
            if not source.is_file():
                continue
            info = zipfile.ZipInfo(member)
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if os.access(source, os.X_OK) else 0o644) << 16
            zf.writestr(info, source.read_bytes())


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _write_checksums(output_dir: Path, artifact_paths: list[Path]) -> Path:
    checksum_path = output_dir / 'SHA256SUMS'
    lines = [f'{_sha256(path)}  {path.name}' for path in sorted(artifact_paths, key=lambda p: p.name)]
    checksum_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return checksum_path


def _package_artifacts(members: list[str]) -> list[dict[str, str]]:
    packages = []
    for product, package_name, surface in (
        ('Lumi Layered Memory', 'lumi-layered-memory', 'core/layered-memory'),
        ('Nuances', 'lumi-nuances', 'core/nuances'),
        ('Presence', 'lumi-presence', 'core/presence'),
    ):
        has_pyproject = f'{surface}/pyproject.toml' in members
        packages.append({
            'product_name': product,
            'package_name': package_name,
            'release_surface': surface,
            'artifact_status': 'source_included' if has_pyproject else 'blocked_until_promoted',
        })
    return packages


def _archive_name(version: str) -> str:
    return f'lumi-social-intelligence-{version}.zip'


def _required_release_members(version: str) -> tuple[str, ...]:
    if version not in VERSION_REQUIRED_RELEASE_MEMBERS:
        raise SystemExit(f'unsupported release version: {version}')
    return BASE_REQUIRED_RELEASE_MEMBERS + VERSION_REQUIRED_RELEASE_MEMBERS[version]


def build(output_dir: Path, version: str = DEFAULT_VERSION) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    tracked_members = _run_git_ls_files()
    findings = _private_material_findings(tracked_members)
    if findings:
        raise SystemExit(f'private material findings: {findings}')

    v02_demo_verification = verify_v02_demo_package()
    if v02_demo_verification['status'] != 'verified':
        raise SystemExit(f'v0.2 demo verification failed: {v02_demo_verification["findings"]}')
    v04_real_controls_evidence = build_v04_receipt()
    if v04_real_controls_evidence['status'] != 'verified':
        raise SystemExit('v0.4 real controls evidence failed verification')
    if v04_real_controls_evidence['shadow_only'] is not False:
        raise SystemExit('v0.4 real controls evidence must not be shadow-only')
    native_telegram_reaction_evidence = None
    if version in {'0.4.1', '0.4.2'}:
        native_telegram_reaction_evidence = build_v041_receipt()
        if native_telegram_reaction_evidence['status'] != 'verified':
            raise SystemExit('v0.4.1 native reaction evidence failed verification')
    care_release_evidence = None
    if version == '0.4.2':
        care_release_evidence = build_v042_receipt()
        if care_release_evidence['status'] != 'verified':
            raise SystemExit('v0.4.2 care release evidence failed verification')

    members = tracked_members
    missing_required = [member for member in _required_release_members(version) if member not in members]
    if missing_required:
        raise SystemExit(f'missing required release members: {missing_required}')

    archive_name = _archive_name(version)
    archive_path = output_dir / archive_name
    _write_zip(archive_path, members)

    manifest = {
        'schema': 'lumi.release_manifest.v1',
        'version': version,
        'archive': archive_name,
        'archive_members': members,
        'package_artifacts': _package_artifacts(members),
        'lumi_for_hermes_preview': {
            'adapter': 'adapters/hermes/lumi_for_hermes.py',
            'installer_preview': 'installers/lumi-for-hermes/preview.py',
            'mode': 'dry_run_review_card_only',
        },
        'private_material_findings': findings,
        'v02_demo_verification': {
            'status': v02_demo_verification['status'],
            'canonical_writes': v02_demo_verification['canonical_writes'],
            'markdown_matches_json': v02_demo_verification['markdown_matches_json'],
            'native_outbound_reaction_delivery': v02_demo_verification['live_claim_boundary']['native_outbound_reaction_delivery'],
        },
        'v04_real_controls_evidence': {
            'status': v04_real_controls_evidence['status'],
            'mode': v04_real_controls_evidence['mode'],
            'shadow_only': v04_real_controls_evidence['shadow_only'],
            'canonical_writes': v04_real_controls_evidence['canonical_writes'],
            'external_writes': v04_real_controls_evidence['external_writes'],
            'private_runtime_reads': v04_real_controls_evidence['private_runtime_reads'],
            'scheduler_mutations': v04_real_controls_evidence['scheduler_mutations'],
            'claim_boundary': v04_real_controls_evidence['claim_boundary'],
        },
        'canonical_writes': 0,
    }
    if native_telegram_reaction_evidence is not None:
        manifest['native_telegram_reaction_evidence'] = {
            'status': native_telegram_reaction_evidence['status'],
            'claim_boundary': native_telegram_reaction_evidence['claim_boundary'],
            'telegram_payload_contract': native_telegram_reaction_evidence['telegram_payload_contract'],
            'public_boundary': native_telegram_reaction_evidence['public_boundary'],
            'side_effects': native_telegram_reaction_evidence['side_effects'],
        }
    if care_release_evidence is not None:
        manifest['care_release_evidence'] = {
            'status': care_release_evidence['status'],
            'release_principle': care_release_evidence['release_principle'],
            'instant_reaction_contract': care_release_evidence['instant_reaction_contract'],
            'next_step_care_contract': care_release_evidence['next_step_care_contract'],
            'public_boundary': care_release_evidence['public_boundary'],
            'side_effects': care_release_evidence['side_effects'],
        }
    manifest_path = output_dir / 'release-manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    checksums_path = _write_checksums(output_dir, [archive_path, manifest_path])

    return {
        'schema': 'lumi.release_artifacts.v1',
        'status': 'built',
        'version': version,
        'output_dir': str(output_dir),
        'artifacts': [archive_path.name, manifest_path.name, checksums_path.name],
        'private_material_findings': findings,
        'canonical_writes': 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Build Lumi Social Intelligence release artifacts.')
    parser.add_argument('--version', default=DEFAULT_VERSION, choices=sorted(VERSION_REQUIRED_RELEASE_MEMBERS))
    parser.add_argument('--output-dir', type=Path, default=None)
    args = parser.parse_args(argv)
    output_dir = args.output_dir or ROOT / 'dist' / args.version
    report = build(output_dir, version=args.version)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
