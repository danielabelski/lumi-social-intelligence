"""Public-safe Live Surface natural-language controls.

This module demonstrates how a host can parse ordinary user phrasing into
small, reversible Live Surface state while keeping personal-data surfaces,
external sends, scheduler/config changes, and durable memory behind review
gates. The legacy shadow helper returns local evidence only. The v0.4 public path
returns real review-gated control cards that can be applied by a host API while
still refusing private integrations, external sends, scheduler/config changes,
and durable memory writes unless an explicit reviewed surface exists.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any

SESSION_TTL_SECONDS = 24 * 60 * 60
REVIEW_TTL_SECONDS = 7 * 24 * 60 * 60

SIDE_EFFECTS_ZERO = {
    'telegram_messages_sent': 0,
    'telegram_reactions_sent': 0,
    'direct_sends': 0,
    'external_writes': 0,
    'calendar_reads_without_surface': 0,
    'calendar_writes': 0,
    'email_reads': 0,
    'email_writes': 0,
    'canonical_memory_writes': 0,
    'runtime_config_writes': 0,
    'scheduler_mutations': 0,
    'permission_expansions': 0,
    'raw_private_events_stored': 0,
    'personal_data_reads': 0,
}

PERSONAL_SURFACES = ('calendar', 'free/busy', 'free busy', 'email', 'gmail', 'inbox', 'photos', 'messages', 'whatsapp', 'telegram history')
EXTERNAL_SEND = ('send ', 'reply ', 'post ', 'dm ', 'message them', 'text them')
SCHEDULER_TERMS = ('schedule', 'daily job', 'cron', 'remind me every', 'timer')
MEMORY_TERMS = ('remember forever', 'always want', 'permanently remember', 'store in memory')
BROAD_FORGET = ('forget everything', 'delete everything', 'wipe all', 'erase all')


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _target_label(text: str, target_hint: str | None = None) -> str:
    if target_hint:
        return target_hint[:120]
    lowered = _norm(text)
    if 'rain' in lowered or 'weather' in lowered or 'leave' in lowered:
        return 'rain/readiness context'
    if 'calendar' in lowered or 'free/busy' in lowered or 'free busy' in lowered:
        return 'calendar free/busy'
    if 'email' in lowered or 'inbox' in lowered:
        return 'email surface'
    return 'current conversation context'


def parse_control_intent(text: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    t = _norm(text)
    flags: list[str] = []
    intent = 'unknown'
    needs_confirmation = False
    scope = 'session'
    confidence = 0.74

    if _contains_any(t, PERSONAL_SURFACES):
        intent = 'add_surface'
        needs_confirmation = True
        scope = 'review_required'
        flags.extend(['personal_data_surface', 'permission_expansion'])
        if any(term in t for term in ('check ', 'watch ', 'read ', 'scan ', 'keep it fresh')):
            flags.append('personal_data_read_blocked')
    if _contains_any(t, EXTERNAL_SEND):
        intent = 'unknown'
        needs_confirmation = True
        scope = 'review_required'
        flags.append('external_send_blocked')
    if _contains_any(t, SCHEDULER_TERMS):
        intent = 'unknown'
        needs_confirmation = True
        scope = 'review_required'
        flags.append('scheduler_mutation_blocked')
    if _contains_any(t, BROAD_FORGET):
        intent = 'forget_pattern'
        needs_confirmation = True
        scope = 'review_required'
        flags.append('broad_forgetting_review_required')
    elif 'forget' in t or 'stop learning this pattern' in t:
        intent = 'forget_pattern'
        needs_confirmation = True
        scope = 'review_required'
    if _contains_any(t, MEMORY_TERMS):
        intent = 'set_boundary'
        needs_confirmation = True
        scope = 'review_required'
        flags.append('durable_memory_review_required')

    if intent == 'unknown' and not flags:
        if any(p in t for p in ('keep this fresh', 'keep an eye', 'keep this warm', 'keep this ready', 'watch the rain', 'keep it warm')) or ('keep' in t and 'warm' in t):
            intent = 'keep_fresh'
        elif any(p in t for p in ('only bring this up if i ask', 'only if i ask', 'when i ask', 'on request')):
            intent = 'only_on_request'
        elif any(p in t for p in ("don't surface", 'do not surface', 'hide this', 'never surface')):
            intent = 'do_not_surface'
        elif any(p in t for p in ('park this for later', 'capture this', 'save this for later', 'enrich it later')):
            intent = 'capture_now_enrich_later'
        elif any(p in t for p in ('what are you keeping warm', 'show status', 'what is live', 'what are you tracking')):
            intent = 'show_status'
        elif any(p in t for p in ('not that close', 'quiet this', 'be quieter', 'ask me before acting', 'less proactive')):
            intent = 'set_boundary'
        elif any(p in t for p in ('make it less like that', 'less like that', 'change that')):
            intent = 'needs_clarification'
            needs_confirmation = True
            scope = 'review_required'
            confidence = 0.31
        else:
            needs_confirmation = True
            scope = 'review_required'
            confidence = 0.22

    if intent in {'add_surface', 'remove_surface', 'forget_pattern'}:
        needs_confirmation = True
        scope = 'review_required'

    return {
        'intent': intent,
        'needs_confirmation': needs_confirmation,
        'scope': scope,
        'confidence': confidence,
        'safety_flags': sorted(set(flags)),
    }


def build_control_state(text: str, *, now: str, source: str, target_hint: str | None = None, context: dict[str, Any] | None = None) -> dict[str, Any]:
    parsed = parse_control_intent(text, context=context)
    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    intent = parsed['intent']
    scope = parsed['scope']
    review_required = scope == 'review_required' or parsed['needs_confirmation']

    surfacing_policy = 'presence_gated'
    refresh_policy = 'safe_readiness_only'
    if intent in {'only_on_request', 'do_not_surface'}:
        surfacing_policy = 'on_request_only' if intent == 'only_on_request' else 'suppressed'
    elif intent == 'show_status':
        surfacing_policy = 'reply_to_current_query_only'
        refresh_policy = 'no_refresh_requested'
    elif intent == 'capture_now_enrich_later':
        surfacing_policy = 'presence_gated'
        refresh_policy = 'delayed_enrichment_when_idle'
    elif intent in {'add_surface', 'forget_pattern', 'unknown', 'needs_clarification'} and review_required:
        surfacing_policy = 'confirmation_required'
        refresh_policy = 'no_refresh_until_review'

    return {
        'control_id': 'ctrl_' + digest[:12],
        'created_at': now,
        'updated_at': now,
        'source': source,
        'raw_user_text_hash': 'sha256:' + digest,
        'raw_user_text_stored': False,
        'intent': intent,
        'target': {
            'kind': 'surface' if intent == 'add_surface' else 'topic',
            'label': _target_label(text, target_hint),
            'sensitivity': 'personal' if intent == 'add_surface' else 'low',
            'surface_membership_required': ['explicit_user_approval'] if intent == 'add_surface' else [],
        },
        'scope': scope,
        'ttl_seconds': REVIEW_TTL_SECONDS if review_required else SESSION_TTL_SECONDS,
        'surfacing_policy': surfacing_policy,
        'refresh_policy': refresh_policy,
        'review_status': 'pending_user_review' if review_required else 'not_required',
        'needs_confirmation': parsed['needs_confirmation'],
        'safety_flags': parsed['safety_flags'],
        'reversible': True,
        'status': 'pending_review' if review_required else 'active',
        'ack_style': 'tiny' if not review_required else 'confirm_gate',
        'side_effects': dict(SIDE_EFFECTS_ZERO),
    }


def render_control_ack(state: dict[str, Any]) -> str:
    intent = state.get('intent')
    if state.get('needs_confirmation') or state.get('scope') == 'review_required':
        if intent == 'add_surface':
            label = state.get('target', {}).get('label', '')
            if 'calendar' in label.lower():
                return 'I can add that, but Calendar needs your explicit okay first.'
            if 'email' in label.lower():
                return 'I can add that, but email needs your explicit okay first.'
            return 'I can add that, but it needs your explicit okay first.'
        if intent == 'needs_clarification':
            return 'I can do that — what should I make less prominent?'
        if intent == 'forget_pattern':
            return 'I can do that, but forgetting patterns needs your explicit okay first.'
        if 'external_send_blocked' in state.get('safety_flags', []):
            return 'I can help draft that, but I won’t send anything without your explicit okay.'
        return 'I can do that, but I need your explicit okay first.'
    if intent == 'keep_fresh':
        return 'Got it — I’ll keep it warm quietly.'
    if intent == 'only_on_request':
        return 'Got it — I’ll only bring it up if you ask.'
    if intent == 'do_not_surface':
        return 'Got it — I won’t surface it unless you bring it back.'
    if intent == 'capture_now_enrich_later':
        return 'Got it — captured now, I’ll enrich it later quietly.'
    if intent == 'show_status':
        return 'I’ll show only the safe warmed context, no plumbing.'
    if intent == 'set_boundary':
        return 'Got it — I’ll make that boundary quieter.'
    return 'I can do that — what should I adjust?'


def _missing_surface_for_state(state: dict[str, Any], available_surfaces: tuple[str, ...]) -> str | None:
    label = state.get('target', {}).get('label', '').lower()
    surfaces = {surface.lower() for surface in available_surfaces}
    if 'calendar' in label and 'calendar' not in surfaces:
        return 'calendar'
    if 'email' in label and 'email' not in surfaces:
        return 'email'
    return None


def build_review_card(state: dict[str, Any], *, available_surfaces: tuple[str, ...] = ('conversation', 'weather')) -> dict[str, Any]:
    missing_surface = _missing_surface_for_state(state, available_surfaces)
    if missing_surface:
        return {
            'schema': 'lumi.live_surface.review_card.v1',
            'decision': 'blocked_missing_surface',
            'missing_surface': missing_surface,
            'applyable_by_public_api': False,
            'requires_private_runtime': False,
            'review_required': True,
            'allowed_operations': [],
            'blocked_operations': [
                f'{missing_surface}_read_without_explicit_surface',
                'permission_expansion_without_review',
            ],
        }
    if state.get('status') == 'active' and state.get('scope') == 'session':
        return {
            'schema': 'lumi.live_surface.review_card.v1',
            'decision': 'ready_for_review',
            'missing_surface': None,
            'applyable_by_public_api': True,
            'requires_private_runtime': False,
            'review_required': False,
            'allowed_operations': ['session_readiness_state'],
            'blocked_operations': [],
        }
    return {
        'schema': 'lumi.live_surface.review_card.v1',
        'decision': 'pending_user_review',
        'missing_surface': None,
        'applyable_by_public_api': False,
        'requires_private_runtime': False,
        'review_required': True,
        'allowed_operations': [],
        'blocked_operations': sorted(state.get('safety_flags', [])),
    }


def apply_review_gated_control(
    text: str,
    *,
    now: str,
    source: str = 'public_review_gated_surface',
    target_hint: str | None = None,
    context: dict[str, Any] | None = None,
    available_surfaces: tuple[str, ...] = ('conversation', 'weather'),
) -> dict[str, Any]:
    """Return a real public v0.4 review-gated Live Surface control card."""
    state = build_control_state(text, now=now, source=source, target_hint=target_hint, context=context)
    review_card = build_review_card(state, available_surfaces=available_surfaces)
    ack = render_control_ack(state)
    if review_card.get('decision') == 'blocked_missing_surface' and review_card.get('missing_surface') == 'calendar':
        ack = "Calendar doesn't yet exist on Live Surface, would you like to add it?"
    return {
        'schema': 'lumi.live_surface.review_gated_control.v1',
        'mode': 'review_gated',
        'shadow_only': False,
        'state': state,
        'review_card': review_card,
        'ack': ack,
        'side_effects': dict(SIDE_EFFECTS_ZERO),
        'claim_boundary': 'review-gated public Live Surface control; no autonomous external automation',
    }


def apply_control_shadow(text: str, *, now: str, source: str = 'host_shadow_surface', target_hint: str | None = None, context: dict[str, Any] | None = None) -> dict[str, Any]:
    state = build_control_state(text, now=now, source=source, target_hint=target_hint, context=context)
    return {
        'state': state,
        'ack': render_control_ack(state),
        'side_effects': dict(SIDE_EFFECTS_ZERO),
        'promotion_scope': 'local_shadow_evidence_only_no_runtime_apply',
    }


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parse Live Surface natural-language controls in local shadow mode.')
    parser.add_argument('text')
    parser.add_argument('--now', default='2026-07-11T17:00:00+07:00')
    args = parser.parse_args()
    print(json.dumps(apply_control_shadow(args.text, now=args.now), indent=2, sort_keys=True))
