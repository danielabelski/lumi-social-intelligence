#!/usr/bin/env python3
"""Build public-safe v0.4.2 care-release evidence.

The evidence records the Live Surface contract for instant emoji reactions and
Next-Step Care narration. It does not send Telegram reactions or include private
Hermes runtime state.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.4.2"


def build_receipt() -> dict[str, Any]:
    return {
        "schema": "lumi.v042.care_release_evidence.v1",
        "status": "verified",
        "version": VERSION,
        "release_principle": "Live Surface reduces uncertainty before it reduces task time",
        "claim_boundary": "Public-safe care contract/evidence for instant Live Surface reactions and Next-Step Care; no public repo Telegram sends",
        "instant_reaction_contract": {
            "intent": "react_to_last_user_message",
            "execution_lane": "instant_control_plane",
            "visible_latency_budget": "instant",
            "agent_tool_calls_allowed": 0,
            "tool_discovery_allowed": False,
            "db_archaeology_allowed": False,
            "llm_planning_required": False,
            "target_resolution": "host_envelope_required",
            "must_not_guess_message_id": True,
            "default_emoji": "❤️",
            "telegram_payload_contract_inherited_from_v041": "list[telegram.ReactionTypeEmoji]",
        },
        "next_step_care_contract": {
            "name": "Next-Step Care",
            "purpose": "tiny predictable narration that reduces uncertainty before side effects",
            "must_precede_side_effect": True,
            "before_action_example": "I’m going to react with ❤️ to your latest Telegram message.",
            "after_success_example": "Done ❤️",
            "fail_closed_example": "I can’t safely find the last message id, so I won’t guess.",
            "accessibility_note": "Care infrastructure for neurodivergent users; not cosmetic polish",
        },
        "sprint_plan": [
            {
                "sprint": 1,
                "name": "Instant reaction primitive",
                "done_when": "reaction intent resolves from host envelope with 0 tool calls and no DB archaeology",
            },
            {
                "sprint": 2,
                "name": "Next-Step Care narration",
                "done_when": "before/action/after/fail-closed microcopy is part of the action plan contract",
            },
            {
                "sprint": 3,
                "name": "Public release evidence",
                "done_when": "release artifacts document the contract while keeping private runtime state out",
            },
        ],
        "public_boundary": {
            "sends_telegram_reactions": False,
            "ships_private_hermes_adapter": False,
            "raw_private_runtime_state": False,
            "stores_message_ids_publicly": False,
            "includes_public_safe_contract": True,
        },
        "side_effects": {
            "telegram_messages_sent_by_public_repo": 0,
            "telegram_reactions_sent_by_public_repo": 0,
            "private_runtime_reads_by_public_repo": 0,
            "runtime_mutations_by_public_repo": 0,
        },
        "not_claimed": [
            "The public repository sends Telegram reactions itself",
            "The public repository exports raw Telegram message IDs or chat IDs",
            "The public repository ships the private Hermes runtime adapter",
            "An agent should search tools or private databases to react to a warmed-context message",
        ],
    }


def build_markdown(receipt: dict[str, Any]) -> str:
    instant = receipt["instant_reaction_contract"]
    care = receipt["next_step_care_contract"]
    side_effects = receipt["side_effects"]
    return f"""# Lumi Social Intelligence v0.4.2 care-release evidence

**Status:** `{receipt['status']}`<br>
**Version:** `{receipt['version']}`<br>
**Principle:** {receipt['release_principle']}<br>
**Claim boundary:** {receipt['claim_boundary']}

v0.4.2 records the missed care requirement from the original Live Surface release: tiny safe actions must not make the user watch visible tool spelunking. For an already-warmed reaction target, the contract is **0 tool calls**, no tool discovery, no DB archaeology, and no guessing.

## Instant reaction contract

| Field | Value |
|---|---|
| Intent | `{instant['intent']}` |
| Execution lane | `{instant['execution_lane']}` |
| Visible latency budget | `{instant['visible_latency_budget']}` |
| Agent tool calls allowed | `{instant['agent_tool_calls_allowed']}` |
| Tool discovery allowed | `{instant['tool_discovery_allowed']}` |
| DB archaeology allowed | `{instant['db_archaeology_allowed']}` |
| Target resolution | `{instant['target_resolution']}` |
| Must not guess message id | `{instant['must_not_guess_message_id']}` |

## Next-Step Care

Next-Step Care is procedural warmth: tiny predictable narration before side effects, especially where uncertainty would create cognitive load.

- Before action: “{care['before_action_example']}”
- After success: “{care['after_success_example']}”
- Fail closed: “{care['fail_closed_example']}”
- Accessibility note: {care['accessibility_note']}

## Public boundary

- Public repo sends Telegram reactions: `false`
- Public repo ships private Hermes adapter: `false`
- Public repo stores raw private message IDs: `false`
- Public repo includes the public-safe contract: `true`

## Side-effect counters

| Counter | Value |
|---|---:|
| telegram_messages_sent_by_public_repo | {side_effects['telegram_messages_sent_by_public_repo']} |
| telegram_reactions_sent_by_public_repo | {side_effects['telegram_reactions_sent_by_public_repo']} |
| private_runtime_reads_by_public_repo | {side_effects['private_runtime_reads_by_public_repo']} |
| runtime_mutations_by_public_repo | {side_effects['runtime_mutations_by_public_repo']} |
"""


def write_outputs(evidence: Path, markdown: Path) -> dict[str, Any]:
    receipt = build_receipt()
    evidence.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown.write_text(build_markdown(receipt), encoding="utf-8")
    return {
        "schema": "lumi.v042.care_release_evidence_build.v1",
        "status": receipt["status"],
        "version": VERSION,
        "evidence": str(evidence),
        "markdown": str(markdown),
        "canonical_writes": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=ROOT / "docs" / "evidence" / "v0.4.2-care-release-evidence.json")
    parser.add_argument("--markdown", type=Path, default=ROOT / "docs" / "evidence" / "v0.4.2-care-release-evidence.md")
    args = parser.parse_args(argv)
    report = write_outputs(args.evidence, args.markdown)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
