from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / 'docs' / 'roadmap.md'


def _roadmap_section(heading: str, next_heading: str) -> str:
    text = ROADMAP.read_text(encoding='utf-8')
    start = text.index(heading)
    end = text.index(next_heading, start)
    return text[start:end]


def test_presprint_article_foundation_is_marked_complete_after_article_pack_commit():
    section = _roadmap_section(
        '## Pre-sprint — NotebookLM article foundation',
        '## Sprint 0 — Release doorway foundation',
    )

    unchecked = [line for line in section.splitlines() if line.startswith('- [ ]')]
    assert not unchecked, unchecked


def test_sprint_1_memory_provider_boundary_is_marked_complete_after_compatibility_commit():
    section = _roadmap_section(
        '## Sprint 1 — Memory-provider compatibility boundary',
        '## Sprint 2 — Module release gates and package names',
    )

    unchecked = [line for line in section.splitlines() if line.startswith('- [ ]')]
    assert not unchecked, unchecked
    assert '**Status:** Complete.' in section
