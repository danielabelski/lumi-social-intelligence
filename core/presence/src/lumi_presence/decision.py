"""Small, public-safe Presence decision helper.

This module is intentionally minimal. It demonstrates the release surface contract
without exporting private behavioral internals, runtime senders, or generated
research artifacts.
"""

from __future__ import annotations

from typing import Literal, TypedDict

PresenceMove = Literal["speak", "ask", "help", "hold", "defer", "block", "repair"]


class PresenceDecision(TypedDict):
    move: PresenceMove
    reason: str
    side_effect_allowed: bool


def decide_presence_move(*, why_now: str | None, grounded: bool, side_effect: bool) -> PresenceDecision:
    """Return a conservative Presence move for synthetic/public examples.

    The helper encodes the first public boundary: if the assistant cannot explain
    why now, or if the moment is ungrounded, it should hold instead of performing
    social confidence. Side effects remain gated even when speaking is allowed.
    """

    if not grounded:
        return {
            "move": "hold",
            "reason": "missing grounded context",
            "side_effect_allowed": False,
        }
    if not why_now or not why_now.strip():
        return {
            "move": "hold",
            "reason": "no clear why-now justification",
            "side_effect_allowed": False,
        }
    return {
        "move": "speak",
        "reason": why_now.strip(),
        "side_effect_allowed": False if side_effect else True,
    }
