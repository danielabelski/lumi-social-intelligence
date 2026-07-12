from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "release.yml"


def test_release_workflow_builds_artifacts_for_tag_version():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "VERSION=${GITHUB_REF_NAME#v}" in text
    assert "--version \"$VERSION\"" in text
    assert "python3 scripts/build_release_artifacts.py --output-dir dist/release" not in text
