import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'public_readiness_audit.py'


def load_audit_module():
    spec = importlib.util.spec_from_file_location('public_readiness_audit', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_public_readiness_audit_script_exists_and_documents_sprint_6_scope():
    assert SCRIPT.exists()
    text = SCRIPT.read_text(encoding='utf-8')
    for phrase in [
        'tracked_files',
        'ignored_local_artifacts',
        'naming_scan',
        'host_claim_scan',
        'license_notice_scan',
        'release_archive_scan',
        'lumi_for_hermes_preview_scan',
    ]:
        assert phrase in text


def test_public_readiness_audit_report_passes_for_current_repo(tmp_path):
    module = load_audit_module()
    artifact_dir = tmp_path / 'artifacts'
    report = module.build_report(artifact_dir)

    assert report['schema'] == 'lumi.public_readiness_audit.v1'
    assert report['status'] == 'pass'
    assert report['canonical_writes'] == 0
    assert report['private_material_findings'] == []

    checks = {check['name']: check for check in report['checks']}
    for required in [
        'tracked_files',
        'ignored_local_artifacts',
        'secret_privacy_scan',
        'naming_scan',
        'host_claim_scan',
        'openclaw_deferred_scan',
        'license_notice_scan',
        'github_metadata_recommendation',
        'release_archive_scan',
        'lumi_for_hermes_preview_scan',
    ]:
        assert checks[required]['status'] == 'pass'

    archive = checks['release_archive_scan']['details']
    assert archive['version'] == '0.4.1'
    assert archive['private_material_findings'] == []
    assert archive['canonical_writes'] == 0
    assert archive['v02_demo_verification']['status'] == 'verified'
    assert archive['v04_real_controls_evidence']['status'] == 'verified'
    assert archive['v04_real_controls_evidence']['shadow_only'] is False
    assert 'installers/lumi-for-hermes/preview.py' in archive['archive_members']
    assert 'docs/releases/v0.4.1.md' in archive['archive_members']
    assert archive['native_telegram_reaction_evidence']['status'] == 'verified'


def test_public_readiness_audit_cli_writes_json_report(tmp_path):
    import subprocess

    report_path = tmp_path / 'public-readiness-audit.json'
    artifact_dir = tmp_path / 'artifacts'
    result = subprocess.run(
        [
            'python3',
            str(SCRIPT),
            '--artifact-dir',
            str(artifact_dir),
            '--report',
            str(report_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    stdout_report = json.loads(result.stdout)
    file_report = json.loads(report_path.read_text(encoding='utf-8'))
    assert stdout_report == file_report
    assert file_report['status'] == 'pass'
    assert file_report['canonical_writes'] == 0


def test_public_readiness_audit_fails_closed_for_openclaw_adapter(monkeypatch, tmp_path):
    module = load_audit_module()

    monkeypatch.setattr(
        module,
        '_tracked_files',
        lambda: ['README.md', 'adapters/openclaw/README.md'],
    )
    report = module.build_report(tmp_path / 'artifacts')

    openclaw = next(check for check in report['checks'] if check['name'] == 'openclaw_deferred_scan')
    assert report['status'] == 'fail'
    assert openclaw['status'] == 'fail'
    assert openclaw['findings']
