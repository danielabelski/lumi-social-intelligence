#!/usr/bin/env python3
"""Build public-safe v0.5.0 cache-backed fast-lane evidence.

This release artifact documents a host contract only. It neither reads private
cache data nor sends a Telegram reply; a private host adapter must implement and
validate the fast lane before using it.
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

from lumi_social_intelligence.care_release import build_cache_backed_fast_lane_plan

VERSION = "0.5.0"


def build_receipt() -> dict[str, Any]:
    plan = build_cache_backed_fast_lane_plan(
        now="2026-07-13T16:00:00+07:00",
        source="telegram",
        context={
            "authorized_sender": True,
            "is_direct_message": True,
            "supported_intent": "weather_or_scooter_departure",
            "cache_fresh": True,
            "cache_valid": True,
        },
    )
    if plan["status"] != "ready_for_host_reply":
        raise RuntimeError("v0.5.0 fast-lane release contract did not become ready")
    return {
        "schema": "lumi.v050.cache_fast_lane_evidence.v1",
        "status": "verified",
        "version": VERSION,
        "release_principle": "A narrow, authorized local-cache reply may skip agent work; every uncertainty falls through normally",
        "claim_boundary": "Public-safe contract/evidence only; no private adapter, cache contents, identifiers, Telegram sends, or runtime promotion",
        "fast_lane_contract": plan,
        "verified_invariants": {
            "authorization_precedes_direct_reply": plan["dispatch_contract"]["authorization_precedes_direct_reply"],
            "network_io_allowed": plan["cache_contract"]["network_io_allowed"],
            "agent_session_or_compression_allowed": plan["dispatch_contract"]["agent_session_or_compression_allowed"],
            "agent_tool_calls_allowed": plan["dispatch_contract"]["agent_tool_calls_allowed"],
            "reply_char_limit": plan["dispatch_contract"]["reply_char_limit"],
            "cache_max_age_seconds": plan["cache_contract"]["max_age_seconds"],
            "fresh_valid_cache_required": plan["eligibility"]["fresh_valid_cache_required"],
        },
        "public_boundary": {
            "sends_telegram_messages": False,
            "sends_telegram_reactions": False,
            "ships_private_hermes_adapter": False,
            "raw_private_runtime_state": False,
            "private_identifiers": False,
            "includes_public_safe_contract": True,
        },
        "side_effects": dict(plan["side_effects"]),
        "not_claimed": [
            "The public repository reads a host cache or private runtime state",
            "The public repository sends a Telegram reply",
            "A fast lane is available to group chats, unauthorized users, or unrelated intents",
            "A stale, invalid, or missing cache entry may be used for an instant reply",
        ],
    }


def build_markdown(receipt: dict[str, Any]) -> str:
    plan = receipt["fast_lane_contract"]
    eligibility = plan["eligibility"]
    cache = plan["cache_contract"]
    dispatch = plan["dispatch_contract"]
    fallback = plan["fallback_contract"]
    side = receipt["side_effects"]
    return f"""# Lumi Social Intelligence v0.5.0 cache-backed fast-lane evidence

**Status:** `{receipt['status']}`<br>
**Version:** `{receipt['version']}`<br>
**Principle:** {receipt['release_principle']}<br>
**Claim boundary:** {receipt['claim_boundary']}

v0.5.0 defines a deliberately narrow fast lane for a private host adapter. It may use a previously refreshed local weather/departure cache to reply immediately only after authorization and only for the bounded Telegram DM intent. The public repository does not ship that adapter or the cache.

## Eligibility and cache boundary

| Field | Value |
|---|---|
| Authorized sender required | `{eligibility['authorized_sender_required']}` |
| Platform scope | `{eligibility['platform_scope']}` |
| Supported intent scope | `{eligibility['supported_intent_scope']}` |
| Fresh + valid cache required | `{eligibility['fresh_valid_cache_required']}` |
| Cache location | `{cache['cache_read_location']}` |
| Network I/O allowed | `{cache['network_io_allowed']}` |
| Cache ceiling | `{cache['max_age_seconds'] // 3600}-hour cache freshness ceiling` |
| Raw cache content exported | `{cache['raw_cache_content_exported']}` |

## Dispatch boundary

- Authorization precedes direct reply: `{dispatch['authorization_precedes_direct_reply']}`.
- Agent session/compression allowed: `{dispatch['agent_session_or_compression_allowed']}`.
- Agent tool calls allowed: `{dispatch['agent_tool_calls_allowed']}`.
- Reply character limit: `{dispatch['reply_char_limit']}`.
- Delivery still uses the host's normal adapter: `{dispatch['normal_delivery_adapter_required']}`.

## Fail closed

**Falls through normally** when the sender is unauthorized, the platform is not a Telegram DM, the intent is unsupported, or the local cache is missing, invalid, or stale.

| Condition | Required host action |
|---|---|
| Unauthorized sender | `{fallback['on_unauthorized_sender']}` |
| Non-DM / unsupported platform | `{fallback['on_unsupported_platform_or_non_direct_message']}` |
| Unsupported or missing intent | `{fallback['on_unsupported_or_missing_intent']}` |
| Missing, invalid, or stale cache | `{fallback['on_missing_invalid_or_stale_cache']}` |

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
        "schema": "lumi.v050.cache_fast_lane_evidence_build.v1",
        "status": receipt["status"],
        "version": VERSION,
        "evidence": str(evidence),
        "markdown": str(markdown),
        "canonical_writes": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=ROOT / "docs" / "evidence" / "v0.5.0-cache-fast-lane-evidence.json")
    parser.add_argument("--markdown", type=Path, default=ROOT / "docs" / "evidence" / "v0.5.0-cache-fast-lane-evidence.md")
    args = parser.parse_args(argv)
    report = write_outputs(args.evidence, args.markdown)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
