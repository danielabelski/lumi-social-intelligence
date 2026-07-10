from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_README = ROOT / 'adapters' / 'hermes' / 'README.md'
ROADMAP = ROOT / 'docs' / 'roadmap.md'


def test_hermes_adapter_readme_names_live_shadow_and_blocked_scope():
    text = ADAPTER_README.read_text(encoding='utf-8')

    required_sections = [
        '## Current public scope',
        '## Live-demo scope',
        '## Shadow-only scope',
        '## Blocked side effects',
        '## Operator rule',
    ]
    missing_sections = [section for section in required_sections if section not in text]
    assert not missing_sections, missing_sections

    required_phrases = [
        'dry-run/review-gated preview surface',
        'explicit synthetic or host-selected input',
        'review card or receipt output',
        'reaction-aware Presence records are shadow-only',
        'outbound emoji Presence records are shadow-only',
        'no Telegram API reads',
        'no Telegram sends or reactions',
        'no canonical writes',
        'no durable memory promotion',
        'Native outbound reaction delivery is not claimed live',
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in text]
    assert not missing_phrases, missing_phrases


def test_hermes_adapter_readme_avoids_sprint_transcript_language():
    text = ADAPTER_README.read_text(encoding='utf-8')

    forbidden_public_process_terms = [
        'Sprint 4',
        'Sprint 8',
        'Sprint 9',
        'sprint transcript',
    ]
    leaked = [term for term in forbidden_public_process_terms if term in text]
    assert not leaked, leaked


def test_roadmap_marks_adapter_doc_cleanup_done():
    roadmap = ROADMAP.read_text(encoding='utf-8')

    assert '- [x] Update adapter docs so live-demo scope, shadow-only scope, and blocked side effects are easy to understand.' in roadmap
