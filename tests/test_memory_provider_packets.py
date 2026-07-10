from copy import deepcopy
import json
from pathlib import Path

import pytest

from lumi_social_intelligence.memory_provider import (
    CompatibilityPacketError,
    build_compatibility_packet,
    decide_presence_from_packet,
)


FIXTURES = Path(__file__).resolve().parents[1] / 'examples' / 'synthetic-memory-pack'


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding='utf-8'))


def test_obsidian_and_hermes_sources_feed_same_presence_path_without_mutation():
    obsidian_source = _fixture('obsidian_context.json')
    hermes_source = _fixture('hermes_memory_context.json')
    originals = (deepcopy(obsidian_source), deepcopy(hermes_source))

    obsidian_packet = build_compatibility_packet(obsidian_source)
    hermes_packet = build_compatibility_packet(hermes_source)

    assert obsidian_source == originals[0]
    assert hermes_source == originals[1]
    assert obsidian_packet['compatibility_view']['normalized_summary'] == hermes_packet['compatibility_view']['normalized_summary']
    assert decide_presence_from_packet(obsidian_packet)['decision'] == 'review_proposal'
    assert decide_presence_from_packet(hermes_packet)['decision'] == 'review_proposal'


def test_missing_provider_data_fails_closed():
    with pytest.raises(CompatibilityPacketError, match='provider'):
        build_compatibility_packet({
            'source_id': 'vault://missing-provider',
            'text': 'A source without provider metadata should not be trusted.',
        })


def test_conflicting_provider_context_preserves_ambiguity_without_merged_fact():
    packet = build_compatibility_packet({
        'provider': 'mixed-review-bundle',
        'source_id': 'review://conflict/communication-style',
        'text': 'One source says concise replies; another says expansive coaching.',
        'confidence': 0.72,
        'conflicts': [
            {'provider': 'obsidian', 'claim': 'prefers concise replies'},
            {'provider': 'hermes-memory', 'claim': 'prefers expansive coaching'},
        ],
    })

    decision = decide_presence_from_packet(packet)

    assert packet['compatibility_view']['ambiguity'] == 'preserved'
    assert packet['compatibility_view']['merged_fact'] is None
    assert decision['decision'] == 'ask_or_wait'
    assert 'do not invent a merged fact' in decision['reason']


def test_blocked_write_attempt_returns_receipt_not_provider_mutation():
    source = {
        'provider': 'obsidian',
        'source_id': 'vault://lumi/public-safe-note',
        'text': 'Possible new preference: more diagrams.',
        'confidence': 0.8,
        'requested_effect': 'write',
        'write_mode': 'none',
    }

    packet = build_compatibility_packet(source)
    decision = decide_presence_from_packet(packet)

    assert decision['decision'] == 'blocked'
    assert decision['provider_mutation'] is False
    assert decision['receipt']['effect'] == 'no_write'
    assert decision['proposal'] is None
