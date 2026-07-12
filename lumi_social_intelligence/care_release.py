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
