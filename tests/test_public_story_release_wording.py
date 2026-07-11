from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
RELEASE_NOTES = ROOT / 'docs' / 'releases' / 'v0.1.0.md'
OFFICIALIZATION_NOTES = ROOT / 'docs' / 'releases' / 'v0.1.0-officialization-notes.md'
ROADMAP = ROOT / 'docs' / 'roadmap.md'
TECHNICAL_ARTICLE = ROOT / 'docs' / 'articles' / '02-technical-lumi-layered-memory-nuances-presence.md'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def test_readme_states_private_review_gated_v010_and_v02_demo_boundary():
    text = read(README)

    required = [
        'private, review-gated `v0.1.0` preview release',
        '`v0.2` is a demo-evidence path, not a live automation claim',
        'Native Telegram reactions are not claimed until verified by a real host-runtime run',
        '[v0.1.0 release notes](docs/releases/v0.1.0.md)',
    ]
    missing = [phrase for phrase in required if phrase not in text]
    assert not missing, missing


def test_release_notes_keep_preview_release_and_no_live_runtime_claims_clear():
    text = read(RELEASE_NOTES)

    required = [
        'private, review-gated preview release',
        'not a live autonomous Lumi service',
        'not live automation proof',
        'Native Telegram reactions are not claimed by this release.',
        'canonical_writes: 0',
        'runtime_actions: []',
        'requires_human_review: true',
    ]
    missing = [phrase for phrase in required if phrase not in text]
    assert not missing, missing


def test_officialization_notes_are_not_sprint_transcript_first():
    text = read(OFFICIALIZATION_NOTES)

    assert 'private, review-gated preview release' in text
    assert 'not proof of a live autonomous Lumi service' in text
    assert 'Product-readiness contribution' not in text
    assert 'Sprint 1' not in text
    assert 'Sprint 6' not in text
    assert '| Capability | Public-readiness contribution |' in text


def test_article_source_uses_current_review_gated_live_surface_boundary():
    text = read(TECHNICAL_ARTICLE)

    required = [
        'The system remains review-gated and fail-closed',
        'tested Live Surface contracts and natural-language controls',
        'Natural-language controls are semantic intent families, not magic keyword commands',
        'already-warmed safe context should add no user-visible wait',
        'refresh pressure is kept separate from permission to surface proactively',
        'without overstating live automation',
    ]
    forbidden = [
        '0.3.0',
        'v0.3.0',
    ]
    missing = [phrase for phrase in required if phrase not in text]
    present_forbidden = [phrase for phrase in forbidden if phrase in text]
    assert not missing, missing
    assert not present_forbidden, present_forbidden


def test_roadmap_marks_public_story_cleanup_done():
    text = read(ROADMAP)

    assert '- [x] Update README, release notes, and article sources to state that `v0.1.0` exists as a private, review-gated preview release.' in text
