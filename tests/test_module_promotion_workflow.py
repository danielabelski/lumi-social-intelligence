import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_SCRIPT = ROOT / 'scripts' / 'audit_module_export.py'
PLAN_SCRIPT = ROOT / 'scripts' / 'plan_module_export.py'
APPLY_SCRIPT = ROOT / 'scripts' / 'apply_module_export.py'
WORKFLOW_DOC = ROOT / 'docs' / 'module-promotion-workflow.md'
DOCS_README = ROOT / 'docs' / 'README.md'


def test_module_promotion_workflow_doc_is_linked_and_names_the_airlock_steps():
    docs_readme = DOCS_README.read_text(encoding='utf-8')
    workflow = WORKFLOW_DOC.read_text(encoding='utf-8')

    assert '[Module promotion workflow](module-promotion-workflow.md)' in docs_readme
    assert 'Private candidate' in workflow
    assert 'read-only audit' in workflow
    assert 'review-only copy plan' in workflow
    assert 'explicit reviewed apply' in workflow
    assert 'No private candidate is exported by this document alone.' in workflow


def test_synthetic_module_promotion_chain_runs_end_to_end_without_private_sources(tmp_path):
    candidate = tmp_path / 'synthetic-presence-candidate'
    candidate.mkdir()
    (candidate / 'README.md').write_text('# Presence\n\nSynthetic public-safe candidate.\n', encoding='utf-8')
    src = candidate / 'src' / 'lumi_presence'
    src.mkdir(parents=True)
    (src / '__init__.py').write_text('__all__ = []\n', encoding='utf-8')
    tests = candidate / 'tests'
    tests.mkdir()
    (tests / 'test_smoke.py').write_text('def test_smoke():\n    assert True\n', encoding='utf-8')

    report = tmp_path / 'presence-audit.json'
    plan = tmp_path / 'presence-plan.json'
    export_root = tmp_path / 'export-root'

    audit = subprocess.run(
        [
            sys.executable,
            str(AUDIT_SCRIPT),
            '--module',
            'Presence',
            '--source',
            str(candidate),
            '--report',
            str(report),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert audit.returncode == 0, audit.stderr
    audit_report = json.loads(report.read_text(encoding='utf-8'))
    assert audit_report['status'] == 'pass'
    assert audit_report['would_copy'] is False

    planned = subprocess.run(
        [
            sys.executable,
            str(PLAN_SCRIPT),
            '--audit-report',
            str(report),
            '--plan',
            str(plan),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert planned.returncode == 0, planned.stderr
    copy_plan = json.loads(plan.read_text(encoding='utf-8'))
    assert copy_plan['status'] == 'ready_for_review'
    assert copy_plan['would_copy'] is False
    assert copy_plan['requires_human_review'] is True

    # Keep the end-to-end fixture public-safe and isolated: redirect the reviewed
    # plan into pytest's temp directory instead of mutating repository core/.
    for operation in copy_plan['copy_operations']:
        repo_destination = Path(operation['destination'])
        relative = repo_destination.relative_to(ROOT / copy_plan['release_surface'])
        operation['destination'] = str(export_root / relative)
    plan.write_text(json.dumps(copy_plan, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    applied = subprocess.run(
        [
            sys.executable,
            str(APPLY_SCRIPT),
            '--plan',
            str(plan),
            '--apply-reviewed-plan',
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert applied.returncode == 0, applied.stderr
    assert (export_root / 'README.md').read_text(encoding='utf-8').startswith('# Presence')
    manifest = json.loads((export_root / '.lumi-export-manifest.json').read_text(encoding='utf-8'))
    assert manifest['module'] == 'Presence'
    assert manifest['package_name'] == 'lumi-presence'
    assert manifest['status'] == 'applied_reviewed_plan'
    assert manifest['copied_files'] == ['README.md', 'src/lumi_presence/__init__.py', 'tests/test_smoke.py']

    repo_presence_init = ROOT / 'core/presence/src/lumi_presence/__init__.py'
    if repo_presence_init.exists():
        assert repo_presence_init.read_text(encoding='utf-8') != "__all__ = []\n"
