#!/usr/bin/env python3
"""Build public-safe v0.4.3 Live Surface readiness evidence.

The evidence records Gateway-start readiness, written pre-tool acknowledgement,
and explicit emoji-reaction suppression for longer/expensive tool paths. It does
not send Telegram messages/reactions or include private Hermes runtime state.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lumi_social_intelligence.care_release import build_live_surface_autoresearch_readiness_plan

VERSION = "0.4.3"


def build_receipt() -> dict[str, Any]:
    plan = build_live_surface_autoresearch_readiness_plan(
        now="2026-07-12T09:00:00+07:00",
        source="public_release_evidence",
        context={"autoresearch_small_investigation_ready": True},
    )
    ack = plan["pre_tool_acknowledgement"]
    emoji_policy = plan["emoji_reaction_policy"]
    return {
        "schema": "lumi.v043.live_surface_readiness_evidence.v1",
        "status": "verified",
        "version": VERSION,
        "release_principle": "Live Surface must be ready before user need and write before visible expensive tool waits",
        "claim_boundary": "Public-safe readiness contract/evidence; no public repo Telegram sends, reactions, private runtime reads, or runtime promotion",
        "readiness_plan": plan,
        "gateway_startup_contract": plan["gateway_startup_readiness"],
        "pre_tool_acknowledgement_contract": ack,
        "emoji_reaction_policy": emoji_policy,
        "verified_invariants": {
            "first_user_need_warmup_allowed": plan["gateway_startup_readiness"]["first_user_need_warmup_allowed"],
            "longer_tool_path_ack_required": ack["longer_tool_path"]["required_before_tool"],
            "longer_tool_path_ack_medium": ack["longer_tool_path"]["required_medium"],
            "emoji_reaction_not_acknowledgement": ack["longer_tool_path"]["emoji_reaction_is_not_acknowledgement"],
            "expensive_tool_path_switches_to_writing": ack["longer_tool_path"]["switch_from_reaction_to_writing_when_tool_call_is_expensive"],
            "reactions_only_for_instant_zero_tool_call_lane": emoji_policy["instant_reaction_intent_only"] and emoji_policy["allowed_when_agent_tool_calls_allowed"] == 0,
        },
        "public_boundary": {
            "sends_telegram_messages": False,
            "sends_telegram_reactions": False,
            "ships_private_hermes_adapter": False,
            "raw_private_runtime_state": False,
            "promotes_runtime_surface": False,
            "includes_public_safe_contract": True,
        },
        "side_effects": dict(plan["side_effects"]),
        "not_claimed": [
            "The public repository sends Telegram messages or reactions itself",
            "The public repository promotes Live Surface tools in a private Hermes runtime",
            "Emoji reactions are acceptable acknowledgements for longer or expensive tool calls",
            "First-use warmup in the user path is acceptable for Live Surface tools",
        ],
    }


def build_markdown(receipt: dict[str, Any]) -> str:
    gateway = receipt["gateway_startup_contract"]
    ack = receipt["pre_tool_acknowledgement_contract"]
    longer = ack["longer_tool_path"]
    simple = ack["simple_familiar_check"]
    emoji = receipt["emoji_reaction_policy"]
    side = receipt["side_effects"]
    return f"""# Lumi Social Intelligence v0.4.3 Live Surface readiness evidence

**Status:** `{receipt['status']}`<br>
**Version:** `{receipt['version']}`<br>
**Principle:** {receipt['release_principle']}<br>
**Claim boundary:** {receipt['claim_boundary']}

v0.4.3 closes the preview gap between instant reactions and expensive tool paths. Instant emoji reactions remain an instant, zero-tool-call lane only. When a tool path is longer or expensive, the assistant must write a brief text acknowledgement before opening the machine room; an emoji reaction is not enough and must not mask latency.

## Gateway-start readiness

| Field | Value |
|---|---|
| Contract | `{gateway['contract']}` |
| Startup phase | `{gateway['startup_phase']}` |
| First-use warmup allowed | `{gateway['first_user_need_warmup_allowed']}` |
| AutoResearch small investigation ready | `{gateway['autoresearch_small_investigation_ready']}` |

## Pre-tool acknowledgement

| Path | Required medium | Example | Emoji reaction allowed |
|---|---|---|---|
| Simple familiar check | text reply | “{simple['example']}” | `{simple['emoji_reaction_allowed']}` |
| Longer/expensive tool path | `{longer['required_medium']}` | “{longer['example']}” | `{longer['emoji_reaction_allowed']}` |

Longer path invariant: `emoji_reaction_is_not_acknowledgement = {longer['emoji_reaction_is_not_acknowledgement']}` and `switch_from_reaction_to_writing_when_tool_call_is_expensive = {longer['switch_from_reaction_to_writing_when_tool_call_is_expensive']}`.

## Emoji reaction policy

- Instant reaction intent only: `{emoji['instant_reaction_intent_only']}`
- Allowed lane: `{emoji['allowed_lane']}`
- Allowed when agent tool calls allowed: `{emoji['allowed_when_agent_tool_calls_allowed']}`
- Longer/expensive paths: `{emoji['for_longer_or_expensive_tool_paths']}`
- Must not mask tool latency: `{emoji['must_not_mask_tool_latency']}`

## Side-effect counters

| Counter | Value |
|---|---:|
| telegram_messages_sent_by_public_repo | {side['telegram_messages_sent_by_public_repo']} |
| telegram_reactions_sent_by_public_repo | {side['telegram_reactions_sent_by_public_repo']} |
| private_runtime_reads_by_public_repo | {side['private_runtime_reads_by_public_repo']} |
| runtime_mutations_by_public_repo | {side['runtime_mutations_by_public_repo']} |
"""


def write_outputs(evidence: Path, markdown: Path) -> dict[str, Any]:
    receipt = build_receipt()
    evidence.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown.write_text(build_markdown(receipt), encoding="utf-8")
    return {
        "schema": "lumi.v043.live_surface_readiness_evidence_build.v1",
        "status": receipt["status"],
        "version": VERSION,
        "evidence": str(evidence),
        "markdown": str(markdown),
        "canonical_writes": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=ROOT / "docs" / "evidence" / "v0.4.3-live-surface-readiness-evidence.json")
    parser.add_argument("--markdown", type=Path, default=ROOT / "docs" / "evidence" / "v0.4.3-live-surface-readiness-evidence.md")
    args = parser.parse_args(argv)
    report = write_outputs(args.evidence, args.markdown)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
