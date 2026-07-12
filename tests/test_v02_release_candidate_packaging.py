import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO_DIR = ROOT / 'docs' / 'demos'


def run_demo_verifier() -> dict:
    result = subprocess.run(
        [sys.executable, 'scripts/verify_v02_demo_package.py'],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(result.stdout)


def run_release_builder(out_dir: Path) -> dict:
    result = subprocess.run(
        [sys.executable, 'scripts/build_release_artifacts.py', '--output-dir', str(out_dir)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(result.stdout)


def test_v02_demo_verifier_proves_public_safe_contract():
    report = run_demo_verifier()

    assert report['schema'] == 'lumi.v02.demo_package_verification.v1'
    assert report['status'] == 'verified'
    assert report['canonical_writes'] == 0
    assert report['required_artifacts_present'] is True
    assert report['safety']['canonical_writes'] == 0
    assert report['safety']['telegram_reactions_sent'] == 0
    assert report['live_claim_boundary']['native_outbound_reaction_delivery'] == 'not_claimed'
    assert report['markdown_matches_json'] is True
    assert report['forbidden_live_claims'] == []
    assert report['blocked_action_explanations_present'] is True
    assert report['findings'] == []


def test_v02_demo_verifier_script_is_wired_into_release_check():
    release_check = (ROOT / 'scripts' / 'release_check.sh').read_text(encoding='utf-8')
    assert 'scripts/verify_v02_demo_package.py' in release_check


def test_v02_release_notes_define_rc_boundary_and_demo_evidence():
    notes = ROOT / 'docs' / 'releases' / 'v0.2.0.md'
    text = notes.read_text(encoding='utf-8')

    assert '# Lumi Social Intelligence v0.2.0' in text
    assert 'release-candidate' in text
    assert 'Observed / verified in this repository' in text
    assert 'Review-gated / no-write boundary' in text
    assert 'Not yet supported or not yet claimed live' in text
    assert 'canonical_writes: 0' in text
    assert 'native outbound emoji reaction delivery' in text
    assert 'not_claimed' in text
    assert 'docs/demos/v0.2-demo-evidence.json' in text
    assert 'docs/demos/v0.2-demo-side-by-side.md' in text


def test_v02_release_artifacts_package_tracked_demo_and_notes(tmp_path):
    report = run_release_builder(tmp_path)

    assert report['version'] == '0.4.0'
    assert report['canonical_writes'] == 0
    archive = tmp_path / 'lumi-social-intelligence-0.4.0.zip'
    manifest = tmp_path / 'release-manifest.json'
    checksums = tmp_path / 'SHA256SUMS'
    assert archive.exists()
    assert manifest.exists()
    assert checksums.exists()

    manifest_data = json.loads(manifest.read_text(encoding='utf-8'))
    assert manifest_data['schema'] == 'lumi.release_manifest.v1'
    assert manifest_data['version'] == '0.4.0'
    assert manifest_data['private_material_findings'] == []
    assert manifest_data['canonical_writes'] == 0
    assert manifest_data['v02_demo_verification']['status'] == 'verified'
    assert manifest_data['v02_demo_verification']['canonical_writes'] == 0
    assert manifest_data['v04_real_controls_evidence']['status'] == 'verified'
    assert manifest_data['v04_real_controls_evidence']['shadow_only'] is False

    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())
    for required in [
        'docs/releases/v0.2.0.md',
        'docs/releases/v0.4.0.md',
        'docs/evidence/v0.4.0-real-controls-evidence.json',
        'scripts/verify_v02_demo_package.py',
        'docs/demos/v0.2-demo-evidence.json',
        'docs/demos/v0.2-demo-side-by-side.json',
        'docs/demos/v0.2-demo-side-by-side.md',
        'docs/demos/v0.2-demo-index.md',
        'docs/demos/v0.2-demo-script.md',
    ]:
        assert required in names

    checksum_by_name = {
        line.split('  ', 1)[1]: line.split('  ', 1)[0]
        for line in checksums.read_text(encoding='utf-8').strip().splitlines()
    }
    assert checksum_by_name[archive.name] == hashlib.sha256(archive.read_bytes()).hexdigest()
    assert checksum_by_name[manifest.name] == hashlib.sha256(manifest.read_bytes()).hexdigest()


def test_release_candidate_planner_defaults_to_v041():
    script = (ROOT / 'scripts' / 'prepare_release_candidate.py').read_text(encoding='utf-8')
    assert "default='v0.4.1'" in script
    assert "docs/releases/v0.4.1.md" in script
    assert "ReactionTypeEmoji" in script
