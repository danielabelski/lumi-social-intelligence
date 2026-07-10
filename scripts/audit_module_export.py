#!/usr/bin/env python3
"""Audit a candidate Lumi module export before anything is copied.

This is intentionally read-only: it walks a candidate source tree, compares files
against the public release-gate allowlist, flags private/runtime artifacts, and
writes a JSON report for human review.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_module_release_gates import DEFAULT_MANIFEST, ModuleReleaseGateError  # noqa: E402

FORBIDDEN_PREFIX_REASONS = {
    'runs/': 'raw run artifact is forbidden',
    '.hermes/': 'private runtime artifact is forbidden',
    'logs/': 'log artifact is forbidden',
    'secrets/': 'secret directory is forbidden',
}
FORBIDDEN_FILENAMES = {
    '.env': 'environment/credential file is forbidden',
    '.env.local': 'environment/credential file is forbidden',
}


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        raise ModuleReleaseGateError(f'{path}: invalid JSON: {exc}') from exc


def _module_gate(manifest_path: Path, module_name: str) -> dict[str, Any]:
    manifest = _load_manifest(manifest_path)
    for module in manifest.get('modules', []):
        if module.get('product_name') == module_name:
            return module
    raise ModuleReleaseGateError(f'unknown module: {module_name!r}')


def _relative_files(source: Path) -> list[str]:
    files: list[str] = []
    for path in source.rglob('*'):
        if path.is_file():
            files.append(path.relative_to(source).as_posix())
    return sorted(files)


def _matches_allowlist(path: str, patterns: list[str]) -> bool:
    posix = PurePosixPath(path)
    for pattern in patterns:
        if pattern.endswith('/**'):
            prefix = pattern[:-3]
            if path.startswith(f'{prefix}/'):
                return True
        elif '*' in pattern:
            if posix.match(pattern):
                return True
        elif path == pattern:
            return True
    return False


def _blocked_reason(path: str, allowlist: list[str]) -> str | None:
    for prefix, reason in FORBIDDEN_PREFIX_REASONS.items():
        if path.startswith(prefix):
            return reason
    name = PurePosixPath(path).name
    if name in FORBIDDEN_FILENAMES:
        return FORBIDDEN_FILENAMES[name]
    if not _matches_allowlist(path, allowlist):
        return 'not included in export allowlist'
    return None


def audit_candidate(module_name: str, source: Path, manifest_path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    if not source.is_dir():
        raise ModuleReleaseGateError(f'source directory does not exist: {source}')

    gate = _module_gate(manifest_path, module_name)
    allowlist = gate.get('export_allowlist')
    if not isinstance(allowlist, list) or not allowlist:
        raise ModuleReleaseGateError(f'{module_name}: export_allowlist is required')

    allowed_files: list[str] = []
    blocked_files: list[dict[str, str]] = []
    for relative in _relative_files(source):
        reason = _blocked_reason(relative, allowlist)
        if reason:
            blocked_files.append({'path': relative, 'reason': reason})
        else:
            allowed_files.append(relative)

    return {
        'module': gate['product_name'],
        'package_name': gate['package_name'],
        'release_surface': gate['release_surface'],
        'source': str(source),
        'manifest': str(manifest_path),
        'status': 'blocked' if blocked_files else 'pass',
        'would_copy': False,
        'allowed_files': allowed_files,
        'blocked_files': blocked_files,
    }


def _write_report(report: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Audit a Lumi module candidate export without copying files.')
    parser.add_argument('--module', required=True, help='Public module/product name from docs/module-release-gates.json')
    parser.add_argument('--source', required=True, type=Path, help='Candidate module source directory to audit')
    parser.add_argument('--report', required=True, type=Path, help='JSON report path to write')
    parser.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST, help='Release-gate manifest path')
    args = parser.parse_args(argv)

    try:
        report = audit_candidate(args.module, args.source, args.manifest)
        _write_report(report, args.report)
    except ModuleReleaseGateError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if report['blocked_files']:
        print(f"blocked files found; report written to {args.report}", file=sys.stderr)
        return 1

    print(f"module export audit passed; report written to {args.report}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
