import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / 'docs' / 'module-release-gates.json'
EXPECTED_MODULES = {
    'Lumi Layered Memory': ('lumi-layered-memory', 'core/layered-memory'),
    'Nuances': ('lumi-nuances', 'core/nuances'),
    'Presence': ('lumi-presence', 'core/presence'),
}


def _gates() -> list[dict]:
    return json.loads(GATES.read_text(encoding='utf-8'))['modules']


def test_module_release_gate_manifest_names_every_public_module():
    modules = _gates()
    by_name = {module['product_name']: module for module in modules}

    assert set(by_name) == set(EXPECTED_MODULES)
    for product_name, (package_name, release_surface) in EXPECTED_MODULES.items():
        module = by_name[product_name]
        assert module['package_name'] == package_name
        assert module['release_surface'] == release_surface
        assert (ROOT / release_surface).is_dir()


def test_module_release_gates_are_fail_closed_and_public_safe():
    for module in _gates():
        assert module['promotion_status'] == 'blocked_until_gate_passes'
        assert module['gate_command']
        assert module['public_safe_fixtures_only'] is True
        assert module['raw_runs_allowed'] is False
        assert module['private_runtime_allowed'] is False
        assert module['credentials_allowed'] is False
        assert module['export_allowlist']
        assert 'runs/' not in module['export_allowlist']
        assert '.hermes/' not in module['export_allowlist']


def test_release_gate_validator_accepts_current_manifest():
    from scripts.validate_module_release_gates import validate_manifest

    validate_manifest(GATES)
