#!/usr/bin/env python3
"""Validate public-safe Lumi module release gates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / 'docs' / 'module-release-gates.json'
EXPECTED_PRODUCTS = {
    'Lumi Layered Memory': ('lumi-layered-memory', 'core/layered-memory'),
    'Nuances': ('lumi-nuances', 'core/nuances'),
    'Presence': ('lumi-presence', 'core/presence'),
}
FORBIDDEN_ALLOWLIST_ENTRIES = {'runs/', '.hermes/', 'logs/', 'secrets/'}
REQUIRED_FALSE_FLAGS = (
    'raw_runs_allowed',
    'private_runtime_allowed',
    'credentials_allowed',
)


class ModuleReleaseGateError(ValueError):
    """Raised when the module release gate manifest is unsafe or incomplete."""


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        raise ModuleReleaseGateError(f'{path}: invalid JSON: {exc}') from exc


def _validate_module(module: dict[str, Any]) -> None:
    product = module.get('product_name')
    if product not in EXPECTED_PRODUCTS:
        raise ModuleReleaseGateError(f'unexpected product_name: {product!r}')

    expected_package, expected_surface = EXPECTED_PRODUCTS[product]
    if module.get('package_name') != expected_package:
        raise ModuleReleaseGateError(f'{product}: package_name must be {expected_package!r}')
    if module.get('release_surface') != expected_surface:
        raise ModuleReleaseGateError(f'{product}: release_surface must be {expected_surface!r}')
    if not (ROOT / expected_surface).is_dir():
        raise ModuleReleaseGateError(f'{product}: missing release surface directory {expected_surface}')

    if module.get('promotion_status') != 'blocked_until_gate_passes':
        raise ModuleReleaseGateError(f'{product}: promotion must fail closed')
    if not module.get('gate_command'):
        raise ModuleReleaseGateError(f'{product}: gate_command is required')
    if module.get('public_safe_fixtures_only') is not True:
        raise ModuleReleaseGateError(f'{product}: public_safe_fixtures_only must be true')

    for flag in REQUIRED_FALSE_FLAGS:
        if module.get(flag) is not False:
            raise ModuleReleaseGateError(f'{product}: {flag} must be false')

    allowlist = module.get('export_allowlist')
    if not isinstance(allowlist, list) or not allowlist:
        raise ModuleReleaseGateError(f'{product}: export_allowlist is required')
    forbidden = sorted(FORBIDDEN_ALLOWLIST_ENTRIES.intersection(allowlist))
    if forbidden:
        raise ModuleReleaseGateError(f'{product}: forbidden allowlist entries: {forbidden}')


def validate_manifest(path: Path = DEFAULT_MANIFEST) -> None:
    manifest = _load_manifest(path)
    modules = manifest.get('modules')
    if not isinstance(modules, list):
        raise ModuleReleaseGateError('manifest.modules must be a list')

    seen = {module.get('product_name') for module in modules}
    if seen != set(EXPECTED_PRODUCTS):
        raise ModuleReleaseGateError(f'module set mismatch: {sorted(seen)!r}')

    for module in modules:
        _validate_module(module)


def main() -> int:
    validate_manifest()
    print('module release gates valid')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
