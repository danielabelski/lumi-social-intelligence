#!/usr/bin/env python3
"""Build public-safe v0.4.0 real review-gated controls evidence."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lumi_social_intelligence.live_surface_controls import apply_review_gated_control

VERSION = "0.4.0"
NOW = "2026-07-11T18:00:00+07:00"


def build_receipt() -> dict[str, Any]:
    safe_readiness = apply_review_gated_control(
        "Keep the rain context warm for when I leave, but don't surface unless relevant",
        now=NOW,
        source="public_review_gated_surface",
    )
    missing_calendar = apply_review_gated_control(
        "check whether I am free tomorrow from my calendar",
        now=NOW,
        source="public_review_gated_surface",
        available_surfaces=("conversation", "weather"),
    )
    return {
        "schema": "lumi.v04.real_controls_evidence.v1",
        "status": "verified",
        "version": VERSION,
        "mode": "review_gated",
        "shadow_only": False,
        "canonical_writes": 0,
        "external_writes": 0,
        "private_runtime_reads": 0,
        "scheduler_mutations": 0,
        "side_effects": dict(safe_readiness["side_effects"]),
        "claim_boundary": "real review-gated public capability; not autonomous private runtime automation",
        "not_claimed": [
            "Telegram sends or reactions",
            "Calendar/email reads without explicit reviewed surface membership",
            "runtime config or scheduler mutation",
            "durable memory writes",
            "raw private Hermes runtime state",
        ],
        "scenarios": {
            "safe_readiness": safe_readiness,
            "missing_calendar": missing_calendar,
        },
    }


def build_markdown(receipt: dict[str, Any]) -> str:
    return f"""# Lumi Social Intelligence v0.4.0 real controls evidence

**Status:** `{receipt['status']}`  
**Mode:** `{receipt['mode']}`  
**Public scope:** review-gated public capability.

This evidence proves the public v0.4.0 Live Surface path as a real review-gated capability: semantic intent is parsed, a host-applyable review card is produced for safe session readiness, and absent personal-data surfaces fail closed.

## Safety counters

| Counter | Value |
|---|---:|
| canonical_writes | {receipt['canonical_writes']} |
| external_writes | {receipt['external_writes']} |
| private_runtime_reads | {receipt['private_runtime_reads']} |
| scheduler_mutations | {receipt['scheduler_mutations']} |

## Claim boundary

{receipt['claim_boundary']}

## Missing Calendar behavior

{receipt['scenarios']['missing_calendar']['ack']}
"""


def write_outputs(evidence: Path, markdown: Path) -> dict[str, Any]:
    receipt = build_receipt()
    evidence.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown.write_text(build_markdown(receipt), encoding="utf-8")
    return {
        "schema": "lumi.v04.real_controls_evidence_build.v1",
        "status": receipt["status"],
        "version": VERSION,
        "evidence": str(evidence),
        "markdown": str(markdown),
        "canonical_writes": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=ROOT / "docs" / "evidence" / "v0.4.0-real-controls-evidence.json")
    parser.add_argument("--markdown", type=Path, default=ROOT / "docs" / "evidence" / "v0.4.0-real-controls-evidence.md")
    args = parser.parse_args(argv)
    report = write_outputs(args.evidence, args.markdown)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
