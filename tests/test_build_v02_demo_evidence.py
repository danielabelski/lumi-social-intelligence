import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'build_v02_demo_evidence.py'


def load_demo_module():
    spec = importlib.util.spec_from_file_location('build_v02_demo_evidence', SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_build_v02_demo_evidence_script_documents_sprint_8_scope():
    assert SCRIPT.exists()
    text = SCRIPT.read_text(encoding='utf-8')
    for phrase in [
        'v0.2 demo evidence receipt',
        'synthetic-v02-live-proof-001',
        'native outbound emoji reaction delivery',
        'shadow_only',
    ]:
        assert phrase in text


def test_build_v02_demo_evidence_report_is_public_safe():
    module = load_demo_module()
    report = module.build_report()

    assert report['schema'] == 'lumi.v02.demo_receipt.v1'
    assert report['status'] == 'valid_v02_demo_receipt'
    assert report['claims']['safe_to_claim_live_native_reaction_delivery'] is False
    assert report['evidence']['observed'] == ['review card generated from synthetic context']
    assert report['evidence']['shadow_only'] == ['native outbound emoji reaction delivery']
    assert report['safety']['canonical_writes'] == 0
    assert report['safety']['runtime_actions'] == []
    assert report['safety']['telegram_messages_sent'] == 0
    assert report['safety']['telegram_reactions_sent'] == 0


def test_build_v02_demo_side_by_side_report_is_public_safe():
    module = load_demo_module()
    report = module.build_side_by_side_report()

    assert report['schema'] == 'lumi.v02.demo_side_by_side_report.v1'
    assert report['status'] == 'ready_for_demo'
    assert report['columns'][0]['items'] == ['review card generated from synthetic context']
    assert report['columns'][1]['items'] == ['native outbound emoji reaction delivery']
    assert report['live_claims']['native_outbound_reaction_delivery'] == 'not_claimed'
    assert report['safety']['canonical_writes'] == 0
    assert report['safety']['telegram_reactions_sent'] == 0


def test_build_v02_demo_side_by_side_markdown_is_public_safe():
    module = load_demo_module()
    markdown = module.build_side_by_side_markdown()

    assert markdown.startswith('# v0.2 Demo Side-by-Side Evidence')
    assert '| Observed in this repo | Shadow-only / not yet claimed live |' in markdown
    assert '| review card generated from synthetic context | native outbound emoji reaction delivery |' in markdown
    assert '**Native outbound reaction delivery:** `not_claimed`' in markdown
    assert 'Canonical writes: `0`' in markdown
    assert 'Telegram reactions sent: `0`' in markdown


def test_build_v02_demo_evidence_cli_writes_json_report(tmp_path):
    report_path = tmp_path / 'v02-demo-evidence.json'
    side_by_side_path = tmp_path / 'v02-demo-side-by-side.json'
    markdown_path = tmp_path / 'v02-demo-side-by-side.md'
    result = subprocess.run(
        [
            'python3',
            str(SCRIPT),
            '--report',
            str(report_path),
            '--side-by-side-report',
            str(side_by_side_path),
            '--side-by-side-markdown',
            str(markdown_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    stdout_report = json.loads(result.stdout)
    file_report = json.loads(report_path.read_text(encoding='utf-8'))
    side_by_side_report = json.loads(side_by_side_path.read_text(encoding='utf-8'))
    markdown = markdown_path.read_text(encoding='utf-8')
    assert stdout_report == file_report
    assert file_report['status'] == 'valid_v02_demo_receipt'
    assert side_by_side_report['status'] == 'ready_for_demo'
    assert side_by_side_report['live_claims']['native_outbound_reaction_delivery'] == 'not_claimed'
    assert markdown.startswith('# v0.2 Demo Side-by-Side Evidence')
    assert '| review card generated from synthetic context | native outbound emoji reaction delivery |' in markdown
