import hashlib
import importlib.util
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_builder_module():
    spec = importlib.util.spec_from_file_location(
        'build_release_artifacts', ROOT / 'scripts' / 'build_release_artifacts.py'
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_builder(out_dir: Path) -> dict:
    result = subprocess.run(
        [sys.executable, 'scripts/build_release_artifacts.py', '--output-dir', str(out_dir)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(result.stdout)


def test_release_artifact_builder_creates_archive_manifest_and_checksums(tmp_path):
    report = run_builder(tmp_path)

    assert report['schema'] == 'lumi.release_artifacts.v1'
    assert report['status'] == 'built'
    assert report['canonical_writes'] == 0
    assert report['output_dir'] == str(tmp_path)

    archive = tmp_path / 'lumi-social-intelligence-0.4.0.zip'
    manifest = tmp_path / 'release-manifest.json'
    checksums = tmp_path / 'SHA256SUMS'

    assert archive.exists()
    assert manifest.exists()
    assert checksums.exists()

    manifest_data = json.loads(manifest.read_text(encoding='utf-8'))
    assert manifest_data['version'] == '0.4.0'
    assert manifest_data['private_material_findings'] == []
    assert manifest_data['v02_demo_verification']['status'] == 'verified'
    assert manifest_data['v04_real_controls_evidence']['status'] == 'verified'
    assert manifest_data['v04_real_controls_evidence']['shadow_only'] is False
    assert 'installers/lumi-for-hermes/preview.py' in manifest_data['archive_members']
    assert 'adapters/hermes/lumi_for_hermes.py' in manifest_data['archive_members']
    assert 'docs/releases/v0.4.0.md' in manifest_data['archive_members']
    assert 'docs/demos/v0.2-demo-side-by-side.md' in manifest_data['archive_members']

    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())
    assert 'README.md' in names
    assert 'scripts/release_check.sh' in names
    assert 'installers/lumi-for-hermes/preview.py' in names
    assert all(not name.startswith(('.git/', '.hermes/', 'runs/', 'logs/')) for name in names)
    assert all('__pycache__' not in name and '.pytest_cache' not in name for name in names)

    checksum_lines = checksums.read_text(encoding='utf-8').strip().splitlines()
    checksum_by_name = {line.split('  ', 1)[1]: line.split('  ', 1)[0] for line in checksum_lines}
    assert checksum_by_name[archive.name] == hashlib.sha256(archive.read_bytes()).hexdigest()
    assert checksum_by_name[manifest.name] == hashlib.sha256(manifest.read_bytes()).hexdigest()


def test_release_builder_blocks_tracked_private_material(monkeypatch, tmp_path):
    builder = load_builder_module()
    monkeypatch.setattr(
        builder,
        '_run_git_ls_files',
        lambda: [
            'README.md',
            'LICENSE',
            'LICENSE-DOCS.md',
            'NOTICE.md',
            'scripts/release_check.sh',
            'scripts/public_secret_scan.py',
            'scripts/build_release_artifacts.py',
            'adapters/hermes/lumi_for_hermes.py',
            'adapters/hermes/README.md',
            'installers/lumi-for-hermes/preview.py',
            'installers/lumi-for-hermes/README.md',
            'core/presence/pyproject.toml',
            'runs/private.jsonl',
        ],
    )

    try:
        builder.build(tmp_path)
    except SystemExit as exc:
        assert 'private material findings' in str(exc)
        assert 'runs/private.jsonl' in str(exc)
    else:
        raise AssertionError('private tracked material was not blocked')


def test_clean_checkout_smoke_script_exists_and_checks_artifact_contract():
    smoke = ROOT / 'scripts' / 'clean_checkout_smoke.sh'
    assert smoke.exists()
    text = smoke.read_text(encoding='utf-8')
    assert 'build_release_artifacts.py' in text
    assert 'release-manifest.json' in text
    assert 'SHA256SUMS' in text
    assert '--version 0.4.1' in text
    assert 'native_telegram_reaction_evidence' in text


def test_github_release_workflow_runs_release_gate_and_uploads_artifacts():
    workflow = ROOT / '.github' / 'workflows' / 'release.yml'
    assert workflow.exists()
    text = workflow.read_text(encoding='utf-8')
    assert './scripts/release_check.sh' in text
    assert 'scripts/build_release_artifacts.py' in text
    assert 'actions/upload-artifact' in text
    assert 'softprops/action-gh-release' in text
    assert 'v*' in text
