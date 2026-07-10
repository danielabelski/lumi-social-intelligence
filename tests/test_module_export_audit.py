import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'audit_module_export.py'


def _run_audit(tmp_path: Path, module: str, source: Path) -> subprocess.CompletedProcess[str]:
    report = tmp_path / 'audit-report.json'
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            '--module',
            module,
            '--source',
            str(source),
            '--report',
            str(report),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_audit_accepts_allowlisted_candidate_without_copying_files(tmp_path):
    source = tmp_path / 'candidate'
    source.mkdir()
    (source / 'README.md').write_text('# Lumi Layered Memory\n', encoding='utf-8')
    (source / 'pyproject.toml').write_text('[project]\nname = "lumi-layered-memory"\n', encoding='utf-8')
    src = source / 'src' / 'lumi_layered_memory'
    src.mkdir(parents=True)
    (src / '__init__.py').write_text('__all__ = []\n', encoding='utf-8')
    tests = source / 'tests'
    tests.mkdir()
    (tests / 'test_smoke.py').write_text('def test_smoke():\n    assert True\n', encoding='utf-8')

    result = _run_audit(tmp_path, 'Lumi Layered Memory', source)

    assert result.returncode == 0, result.stderr
    report = json.loads((tmp_path / 'audit-report.json').read_text(encoding='utf-8'))
    assert report['module'] == 'Lumi Layered Memory'
    assert report['package_name'] == 'lumi-layered-memory'
    assert report['status'] == 'pass'
    assert report['would_copy'] is False
    assert report['allowed_files'] == [
        'README.md',
        'pyproject.toml',
        'src/lumi_layered_memory/__init__.py',
        'tests/test_smoke.py',
    ]
    assert report['blocked_files'] == []


def test_audit_blocks_private_runtime_and_raw_runs(tmp_path):
    source = tmp_path / 'candidate'
    source.mkdir()
    (source / 'README.md').write_text('# Presence\n', encoding='utf-8')
    runs = source / 'runs'
    runs.mkdir()
    (runs / 'overnight.jsonl').write_text('{"private": true}\n', encoding='utf-8')
    hermes = source / '.hermes'
    hermes.mkdir()
    (hermes / 'config.yaml').write_text('token: nope\n', encoding='utf-8')

    result = _run_audit(tmp_path, 'Presence', source)

    assert result.returncode == 1
    report = json.loads((tmp_path / 'audit-report.json').read_text(encoding='utf-8'))
    assert report['status'] == 'blocked'
    blocked = {entry['path']: entry['reason'] for entry in report['blocked_files']}
    assert blocked['runs/overnight.jsonl'] == 'raw run artifact is forbidden'
    assert blocked['.hermes/config.yaml'] == 'private runtime artifact is forbidden'
    assert 'blocked files found' in result.stderr
