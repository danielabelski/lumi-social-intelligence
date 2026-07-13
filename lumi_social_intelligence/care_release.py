"""v0.4.2 care-release contracts for Live Surface instant reactions.

This module is public-safe. It does not send Telegram reactions, read private
runtime state, or mutate Hermes. It defines the host contract: safe tiny actions
must be resolved from already-warmed host envelope context, not by visible tool
spelunking.
"""
from __future__ import annotations

import re
from typing import Any

VERSION = "0.4.2"
VERSION_043 = "0.4.3"
VERSION_050 = "0.5.0"

SIDE_EFFECTS_ZERO = {
    "telegram_messages_sent_by_public_repo": 0,
    "telegram_reactions_sent_by_public_repo": 0,
    "private_runtime_reads_by_public_repo": 0,
    "runtime_mutations_by_public_repo": 0,
}

DEFAULT_EMOJI = "❤️"
_EMOJI_RE = re.compile(
    "["
    "\U0001F1E6-\U0001F1FF"
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FAFF"
    "\u2600-\u27BF"
    "]"
)


def _extract_emoji(text: str, context: dict[str, Any]) -> str:
    match = _EMOJI_RE.search(text)
    if match:
        emoji = match.group(0)
        if emoji == "❤" and "❤️" in text:
            return "❤️"
        return emoji
    return str(context.get("default_emoji") or DEFAULT_EMOJI)


def _is_reaction_request(text: str) -> bool:
    t = " ".join(text.lower().split())
    return (
        ("emoji" in t or "react" in t or "reaction" in t)
        and ("last message" in t or "latest message" in t or "previous message" in t)
    )


def _next_step_care(emoji: str, *, available: bool) -> dict[str, Any]:
    fail = "I can’t safely find the last message id, so I won’t guess."
    return {
        "principle": "reduce_uncertainty_before_task_time",
        "before_action": f"I’m going to react with {emoji} to your latest Telegram message." if available else fail,
        "after_success": f"Done {emoji}",
        "fail_closed": fail,
        "tone": "tiny_predictable_caring_not_infantilizing",
        "must_precede_side_effect": True,
    }


def build_care_action_plan(
    text: str,
    *,
    now: str,
    source: str,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a public-safe v0.4.2 care action plan.

    A host runtime may use this contract to route tiny safe actions, but this
    public package only emits a deterministic plan. The target must come from the
    inbound host envelope/session context. If it is absent, the plan fails closed
    instead of guessing or searching private databases.
    """
    ctx = dict(context or {})
    emoji = _extract_emoji(text, ctx)
    last_ref = ctx.get("last_user_message_ref")
    target_available = bool(last_ref)
    reaction_request = _is_reaction_request(text)
    status = "ready" if reaction_request and target_available else "blocked_missing_target"

    return {
        "schema": "lumi.v042.care_action_plan.v1",
        "version": VERSION,
        "created_at": now,
        "source": source,
        "status": status,
        "actionable": status == "ready",
        "intent": "react_to_last_user_message" if reaction_request else "unknown",
        "emoji": emoji,
        "target": {
            "kind": "last_user_message",
            "available": target_available,
            "resolution": "host_envelope_required",
            "ref_stored_publicly": False,
        },
        "execution_lane": "instant_control_plane",
        "visible_latency_budget": "instant",
        "agent_tool_calls_allowed": 0,
        "db_archaeology_allowed": False,
        "tool_discovery_allowed": False,
        "llm_planning_required": False,
        "next_step_care": _next_step_care(emoji, available=target_available),
        "review_gate": {
            "host_must_already_have_target": True,
            "must_not_guess_message_id": True,
            "private_runtime_state_not_exported": True,
        },
        "side_effects": dict(SIDE_EFFECTS_ZERO),
    }


def build_live_surface_autoresearch_readiness_plan(
    *,
    now: str,
    source: str,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the public-safe v0.4.3 Live Surface AutoResearch readiness plan.

    This is a contract artifact, not a runtime bridge. It documents that small
    research/concepting routes must be warm at Gateway start and must acknowledge
    before any longer tool path, while keeping permission and side effects gated.
    """
    ctx = dict(context or {})
    warmed = bool(ctx.get("autoresearch_small_investigation_ready", True))
    return {
        "schema": "lumi.v043.live_surface_autoresearch_readiness.v1",
        "version": VERSION_043,
        "created_at": now,
        "source": source,
        "status": "ready" if warmed else "blocked_not_warmed",
        "gateway_startup_readiness": {
            "contract": "all_live_surface_tools_ready_after_gateway_start",
            "first_user_need_warmup_allowed": False,
            "autoresearch_small_investigation_ready": warmed,
            "startup_phase": "gateway_start",
            "host_prefill_messages_file_required": True,
            "host_prefill_messages_file_config_key": "prefill_messages_file",
            "host_prefill_messages_file_default": "~/.hermes/state/live_surface_prefill_messages.json",
            "host_prefill_messages_file_purpose": "prime public-safe Live Surface behaviour before the first user need",
        },
        "pre_tool_acknowledgement": {
            "simple_familiar_check": {
                "required_before_tool": True,
                "example": "Sure, let’s check.",
                "tone": "warm_brief_human_handoff",
                "avoid": "over_explaining_read_only_or_bounded_mechanics_unless_safety_or_scope_needs_it",
                "emoji_reaction_allowed": False,
            },
            "longer_tool_path": {
                "required_before_tool": True,
                "required_medium": "text_reply",
                "example": "I’m checking the small AutoResearch route now, then I’ll give you the concrete next step — no silent long wait.",
                "visible_latency_contract": "no_silent_long_wait",
                "emoji_reaction_allowed": False,
                "emoji_reaction_is_not_acknowledgement": True,
                "switch_from_reaction_to_writing_when_tool_call_is_expensive": True,
            },
        },
        "emoji_reaction_policy": {
            "instant_reaction_intent_only": True,
            "allowed_lane": "instant_control_plane",
            "allowed_when_agent_tool_calls_allowed": 0,
            "for_longer_or_expensive_tool_paths": "write_a_brief_text_acknowledgement_instead",
            "must_not_mask_tool_latency": True,
        },
        "review_gate": {
            "readiness_is_not_permission": True,
            "permission_expansion_allowed": False,
            "durable_memory_write_allowed": False,
            "runtime_promotion_allowed_by_public_repo": False,
        },
        "side_effects": dict(SIDE_EFFECTS_ZERO),
    }


def build_cache_backed_fast_lane_plan(
    *,
    now: str,
    source: str,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the public-safe v0.5.0 cache-backed fast-lane contract.

    The public package deliberately receives only host-verified booleans and an
    intent label. It never opens a cache, resolves a chat, sends a reply, or
    invokes a network/tool path. A host may use the ready result only after it
    has authorized the sender and validated a local, fresh cache entry.
    """
    ctx = dict(context or {})
    direct_message = source == "telegram" and bool(ctx.get("is_direct_message"))
    authorized = bool(ctx.get("authorized_sender"))
    supported_intent = ctx.get("supported_intent") == "weather_or_scooter_departure"
    cache_ready = bool(ctx.get("cache_fresh")) and bool(ctx.get("cache_valid"))

    if not authorized:
        status = "fallback_full_dispatch"
        fallback_reason = "unauthorized_sender"
        fallback_action = "normal_auth_or_pairing_flow"
    elif not direct_message:
        status = "fallback_full_dispatch"
        fallback_reason = "unsupported_platform_or_non_direct_message"
        fallback_action = "normal_full_dispatch"
    elif not supported_intent:
        status = "fallback_full_dispatch"
        fallback_reason = "unsupported_or_missing_intent"
        fallback_action = "normal_full_dispatch"
    elif not cache_ready:
        status = "fallback_full_dispatch"
        fallback_reason = "missing_invalid_or_stale_cache"
        fallback_action = "normal_full_dispatch"
    else:
        status = "ready_for_host_reply"
        fallback_reason = None
        fallback_action = None

    return {
        "schema": "lumi.v050.cache_backed_fast_lane.v1",
        "version": VERSION_050,
        "created_at": now,
        "source": source,
        "status": status,
        "direct_reply_allowed": status == "ready_for_host_reply",
        "eligibility": {
            "authorized_sender_required": True,
            "platform_scope": "telegram_direct_message",
            "supported_intent_scope": "weather_or_scooter_departure",
            "fresh_valid_cache_required": True,
        },
        "cache_contract": {
            "cache_read_location": "host_local_state_only",
            "network_io_allowed": False,
            "max_age_seconds": 43200,
            "raw_cache_content_exported": False,
        },
        "dispatch_contract": {
            "authorization_precedes_direct_reply": True,
            "agent_session_or_compression_allowed": False,
            "agent_tool_calls_allowed": 0,
            "reply_char_limit": 4096,
            "normal_delivery_adapter_required": True,
        },
        "fallback_contract": {
            "on_unauthorized_sender": "normal_auth_or_pairing_flow",
            "on_unsupported_platform_or_non_direct_message": "normal_full_dispatch",
            "on_unsupported_or_missing_intent": "normal_full_dispatch",
            "on_missing_invalid_or_stale_cache": "normal_full_dispatch",
        },
        "fallback_reason": fallback_reason,
        "fallback_action": fallback_action,
        "review_gate": {
            "host_authorization_required": True,
            "private_identifiers_exported": False,
            "private_cache_content_exported": False,
            "runtime_promotion_allowed_by_public_repo": False,
        },
        "side_effects": dict(SIDE_EFFECTS_ZERO),
    }
