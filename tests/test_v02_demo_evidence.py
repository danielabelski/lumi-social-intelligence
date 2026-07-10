from lumi_social_intelligence.v02_demo_evidence import (
    build_v02_demo_receipt,
    build_v02_demo_side_by_side_markdown,
    build_v02_demo_side_by_side_report,
    validate_v02_demo_receipt,
)


def test_v02_demo_receipt_connects_context_to_presence_with_shadow_boundaries():
    receipt = build_v02_demo_receipt({
        'schema': 'lumi.v02.demo_fixture_input.v1',
        'demo_id': 'synthetic-v02-live-proof-001',
        'observed_at': '2026-07-10T12:00:00+07:00',
        'memory_context': {
            'provider': 'hermes-memory',
            'source_id': 'synthetic://demo/memory/short-replies',
            'text': 'Marko prefers short replies for reaction-aware presence moments.',
            'confidence': 0.92,
        },
        'nuance_appraisal': {
            'why_now': 'a warm reaction signal is better answered with a tiny presence gesture than a paragraph',
            'grounded': True,
            'confidence': 0.87,
        },
        'reaction_input': {
            'reaction': '❤️',
            'source_message_role': 'assistant',
            'previous_reaction_ack_turns_ago': 10,
        },
        'outbound_emoji_input': {
            'candidate_reaction': '❤️',
            'target_message_role': 'user',
            'why_now': 'warm moment where an emoji reaction is less intrusive than text',
            'previous_outbound_reaction_turns_ago': 10,
        },
        'live_observations': [
            {
                'surface': 'telegram',
                'behavior': 'review card generated from synthetic context',
                'status': 'observed',
                'evidence': 'pytest fixture receipt',
            },
            {
                'surface': 'telegram',
                'behavior': 'native outbound emoji reaction delivery',
                'status': 'shadow_only',
                'evidence': 'live adapter delivery not yet observed',
            },
        ],
    })

    assert receipt['schema'] == 'lumi.v02.demo_receipt.v1'
    assert receipt['demo_id'] == 'synthetic-v02-live-proof-001'
    assert receipt['flow']['memory']['source']['source_id'] == 'synthetic://demo/memory/short-replies'
    assert receipt['flow']['nuance']['why_now'].startswith('a warm reaction signal')
    assert receipt['flow']['presence_decision']['move'] == 'speak'
    assert receipt['reaction_aware_presence']['presence_decision']['reply'] == '❤️'
    assert receipt['outbound_emoji_presence']['emoji_choice']['emoji'] == '❤️'
    assert receipt['evidence']['observed'] == ['review card generated from synthetic context']
    assert receipt['evidence']['shadow_only'] == ['native outbound emoji reaction delivery']
    assert receipt['claims']['safe_to_claim_live_native_reaction_delivery'] is False
    assert receipt['claims']['observed_behavior_is_separated_from_shadow_behavior'] is True
    assert receipt['safety']['canonical_writes'] == 0
    assert receipt['safety']['runtime_actions'] == []
    assert receipt['safety']['telegram_messages_sent'] == 0
    assert receipt['safety']['telegram_reactions_sent'] == 0
    assert validate_v02_demo_receipt(receipt) == []


def test_v02_demo_side_by_side_report_keeps_observed_and_shadow_claims_apart():
    receipt = build_v02_demo_receipt({
        'schema': 'lumi.v02.demo_fixture_input.v1',
        'demo_id': 'synthetic-v02-live-proof-001',
        'observed_at': '2026-07-10T12:00:00+07:00',
        'memory_context': {
            'provider': 'hermes-memory',
            'source_id': 'synthetic://demo/memory/short-replies',
            'text': 'Marko prefers short replies for reaction-aware presence moments.',
            'confidence': 0.92,
        },
        'nuance_appraisal': {
            'why_now': 'a warm reaction signal is better answered with a tiny presence gesture than a paragraph',
            'grounded': True,
            'confidence': 0.87,
        },
        'reaction_input': {'reaction': '❤️', 'source_message_role': 'assistant'},
        'outbound_emoji_input': {
            'candidate_reaction': '❤️',
            'target_message_role': 'user',
            'why_now': 'warm moment where an emoji reaction is less intrusive than text',
            'previous_outbound_reaction_turns_ago': 10,
        },
        'live_observations': [
            {
                'surface': 'telegram',
                'behavior': 'review card generated from synthetic context',
                'status': 'observed',
                'evidence': 'pytest fixture receipt',
            },
            {
                'surface': 'telegram',
                'behavior': 'native outbound emoji reaction delivery',
                'status': 'shadow_only',
                'evidence': 'live adapter delivery not yet observed',
            },
        ],
    })

    report = build_v02_demo_side_by_side_report(receipt)

    assert report['schema'] == 'lumi.v02.demo_side_by_side_report.v1'
    assert report['status'] == 'ready_for_demo'
    assert report['demo_id'] == 'synthetic-v02-live-proof-001'
    assert report['columns'][0]['label'] == 'Observed in this repo'
    assert report['columns'][0]['items'] == ['review card generated from synthetic context']
    assert report['columns'][1]['label'] == 'Shadow-only / not yet claimed live'
    assert report['columns'][1]['items'] == ['native outbound emoji reaction delivery']
    assert report['live_claims']['native_outbound_reaction_delivery'] == 'not_claimed'
    assert report['headline'] == 'Observed demo receipt is separate from shadow-only Telegram delivery.'
    assert report['safety']['canonical_writes'] == 0
    assert report['safety']['telegram_reactions_sent'] == 0


def test_v02_demo_side_by_side_markdown_renders_copy_pastable_table():
    report = {
        'schema': 'lumi.v02.demo_side_by_side_report.v1',
        'demo_id': 'synthetic-v02-live-proof-001',
        'status': 'ready_for_demo',
        'headline': 'Observed demo receipt is separate from shadow-only Telegram delivery.',
        'columns': [
            {'label': 'Observed in this repo', 'items': ['review card generated from synthetic context']},
            {'label': 'Shadow-only / not yet claimed live', 'items': ['native outbound emoji reaction delivery']},
        ],
        'live_claims': {'native_outbound_reaction_delivery': 'not_claimed'},
        'safety': {'canonical_writes': 0, 'telegram_reactions_sent': 0},
        'blocked_reasons': [],
    }

    markdown = build_v02_demo_side_by_side_markdown(report)

    assert markdown.startswith('# v0.2 Demo Side-by-Side Evidence')
    assert '| Observed in this repo | Shadow-only / not yet claimed live |' in markdown
    assert '| review card generated from synthetic context | native outbound emoji reaction delivery |' in markdown
    assert '**Native outbound reaction delivery:** `not_claimed`' in markdown
    assert 'Canonical writes: `0`' in markdown
    assert 'Telegram reactions sent: `0`' in markdown
    assert 'blocked' not in markdown.lower()


def test_v02_demo_side_by_side_markdown_escapes_table_pipes():
    report = {
        'schema': 'lumi.v02.demo_side_by_side_report.v1',
        'demo_id': 'pipe-safe',
        'status': 'ready_for_demo',
        'headline': 'Pipe safety.',
        'columns': [
            {'label': 'Observed | repo', 'items': ['review | card']},
            {'label': 'Shadow | only', 'items': ['native | reaction']},
        ],
        'live_claims': {'native_outbound_reaction_delivery': 'not_claimed'},
        'safety': {'canonical_writes': 0, 'telegram_reactions_sent': 0},
        'blocked_reasons': [],
    }

    markdown = build_v02_demo_side_by_side_markdown(report)

    assert 'Observed \\| repo' in markdown
    assert 'review \\| card' in markdown


def test_v02_demo_receipt_fails_closed_when_live_claim_has_no_observation():
    receipt = build_v02_demo_receipt({
        'schema': 'lumi.v02.demo_fixture_input.v1',
        'demo_id': 'synthetic-v02-bad-live-claim',
        'observed_at': '2026-07-10T12:00:00+07:00',
        'memory_context': {
            'provider': 'hermes-memory',
            'source_id': 'synthetic://demo/memory/low',
            'text': 'Safe fixture.',
            'confidence': 0.91,
        },
        'nuance_appraisal': {
            'why_now': 'safe fixture with enough grounding',
            'grounded': True,
            'confidence': 0.86,
        },
        'reaction_input': {'reaction': '👍'},
        'outbound_emoji_input': {
            'candidate_reaction': '👍',
            'target_message_role': 'user',
            'why_now': 'safe fixture',
            'previous_outbound_reaction_turns_ago': 10,
            'platform_delivery_verified': True,
        },
        'live_observations': [],
    })

    assert receipt['status'] == 'fail_closed'
    assert receipt['claims']['safe_to_claim_live_native_reaction_delivery'] is False
    assert 'cannot claim live native reaction delivery without observed evidence' in receipt['safety']['blocked_reasons']
    assert receipt['safety']['telegram_reactions_sent'] == 0


def test_v02_demo_receipt_rejects_private_runtime_fields():
    try:
        build_v02_demo_receipt({
            'schema': 'lumi.v02.demo_fixture_input.v1',
            'demo_id': 'unsafe',
            'memory_context': {
                'provider': 'hermes-memory',
                'source_id': 'synthetic://demo/memory/unsafe',
                'text': 'Safe fixture.',
                'confidence': 0.9,
            },
            'nuance_appraisal': {
                'why_now': 'safe fixture',
                'grounded': True,
                'confidence': 0.9,
            },
            'reaction_input': {'reaction': '❤️'},
            'outbound_emoji_input': {'candidate_reaction': '❤️', 'chat_id': 'do-not-export'},
            'live_observations': [],
        })
    except ValueError as exc:
        assert 'chat_id' in str(exc)
    else:
        raise AssertionError('expected forbidden field rejection')
