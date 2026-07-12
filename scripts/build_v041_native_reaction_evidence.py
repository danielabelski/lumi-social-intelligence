#!/usr/bin/env python3
"""Build public-safe v0.4.1 native Telegram reaction evidence.

This evidence records the confirmed Hermes/PTB adapter contract without shipping
private Hermes runtime code or raw private runtime state in this public doorway.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.4.1"


def build_receipt() -> dict[str, Any]:
    return {
        "schema": "lumi.v041.native_reaction_evidence.v1",
        "status": "verified",
        "version": VERSION,
        "claim_boundary": "Hermes native Telegram emoji reaction delivery verified; public release packages contract/evidence only",
        "telegram_payload_contract": {
            "method": "Bot.set_message_reaction",
            "reaction": ["ReactionTypeEmoji(emoji='❤️')"],
            "accepted_primitive_reaction": False,
        },
        "live_runtime_evidence": {
            "native_reaction_delivery": "verified",
            "adapter_boundary": "private Hermes runtime",
            "payload_shape": "list[telegram.ReactionTypeEmoji]",
            "primitive_emoji_string": "rejected at SDK boundary",
        },
        "public_boundary": {
            "ships_private_hermes_adapter": False,
            "raw_private_runtime_state": False,
            "includes_contract_notes": True,
            "includes_public_safe_evidence": True,
        },
        "side_effects": {
            "telegram_messages_sent_by_public_repo": 0,
            "telegram_reactions_sent_by_public_repo": 0,
            "private_runtime_reads_by_public_repo": 0,
            "runtime_mutations_by_public_repo": 0,
        },
        "not_claimed": [
            "The public repo ships the private Hermes adapter",
            "The public repo sends Telegram reactions itself",
            "The public repo includes raw private Hermes logs or runtime state",
            "A primitive emoji string is sufficient for python-telegram-bot native reaction delivery",
        ],
    }


def build_markdown(receipt: dict[str, Any]) -> str:
    payload = receipt["telegram_payload_contract"]
    side_effects = receipt["side_effects"]
    return f"""# Lumi Social Intelligence v0.4.1 native reaction evidence

**Status:** `{receipt['status']}`
**Version:** `{receipt['version']}`
**Claim boundary:** {receipt['claim_boundary']}

This patch evidence records the confirmed Hermes native Telegram reaction contract. The public release packages the contract and public-safe evidence; it does not ship the private Hermes adapter or raw private Hermes runtime state.

## Telegram payload contract

| Field | Value |
|---|---|
| Method | `{payload['method']}` |
| Reaction payload | `{payload['reaction'][0]}` inside a list |
| Primitive emoji string accepted | `{payload['accepted_primitive_reaction']}` |

The important SDK boundary is that PTB native reaction delivery requires `ReactionTypeEmoji`; a primitive emoji string is not the release contract.

## Public boundary

- Public repo evidence: contract notes, release notes, manifest entry, checksums.
- Private runtime boundary: Hermes adapter implementation and live runtime state stay out of this repository.
- This release does not ship the private Hermes adapter.

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
        "schema": "lumi.v041.native_reaction_evidence_build.v1",
        "status": receipt["status"],
        "version": VERSION,
        "evidence": str(evidence),
        "markdown": str(markdown),
        "canonical_writes": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=ROOT / "docs" / "evidence" / "v0.4.1-native-reaction-evidence.json")
    parser.add_argument("--markdown", type=Path, default=ROOT / "docs" / "evidence" / "v0.4.1-native-reaction-evidence.md")
    args = parser.parse_args(argv)
    report = write_outputs(args.evidence, args.markdown)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
