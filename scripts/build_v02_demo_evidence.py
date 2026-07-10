#!/usr/bin/env python3
"""Generate the public-safe v0.2 demo evidence receipt."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lumi_social_intelligence.v02_demo_evidence import (
    build_v02_demo_receipt,
    build_v02_demo_side_by_side_markdown,
    build_v02_demo_side_by_side_report,
)

DEMO_FIXTURE = {
    "schema": "lumi.v02.demo_fixture_input.v1",
    "demo_id": "synthetic-v02-live-proof-001",
    "observed_at": "2026-07-10T12:00:00+07:00",
    "memory_context": {
        "provider": "hermes-memory",
        "source_id": "synthetic://demo/memory/short-replies",
        "text": "Marko prefers short replies for reaction-aware presence moments.",
        "confidence": 0.92,
    },
    "nuance_appraisal": {
        "why_now": "a warm reaction signal is better answered with a tiny presence gesture than a paragraph",
        "grounded": True,
        "confidence": 0.87,
    },
    "reaction_input": {
        "reaction": "❤️",
        "source_message_role": "assistant",
        "previous_reaction_ack_turns_ago": 10,
    },
    "outbound_emoji_input": {
        "candidate_reaction": "❤️",
        "target_message_role": "user",
        "why_now": "warm moment where an emoji reaction is less intrusive than text",
        "previous_outbound_reaction_turns_ago": 10,
    },
    "live_observations": [
        {
            "surface": "telegram",
            "behavior": "review card generated from synthetic context",
            "status": "observed",
            "evidence": "tests/test_v02_demo_evidence.py",
        },
        {
            "surface": "telegram",
            "behavior": "native outbound emoji reaction delivery",
            "status": "shadow_only",
            "evidence": "live adapter delivery not yet observed",
        },
    ],
}


def build_report() -> dict:
    return build_v02_demo_receipt(DEMO_FIXTURE)


def build_side_by_side_report() -> dict:
    return build_v02_demo_side_by_side_report(build_report())


def build_side_by_side_markdown() -> str:
    return build_v02_demo_side_by_side_markdown(build_side_by_side_report())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Lumi v0.2 public-safe demo evidence receipt.")
    parser.add_argument("--report", type=Path, default=ROOT / "docs" / "demos" / "v0.2-demo-evidence.json")
    parser.add_argument(
        "--side-by-side-report",
        type=Path,
        default=ROOT / "docs" / "demos" / "v0.2-demo-side-by-side.json",
    )
    parser.add_argument(
        "--side-by-side-markdown",
        type=Path,
        default=ROOT / "docs" / "demos" / "v0.2-demo-side-by-side.md",
    )
    args = parser.parse_args(argv)

    report = build_report()
    side_by_side_report = build_side_by_side_report()
    side_by_side_markdown = build_v02_demo_side_by_side_markdown(side_by_side_report)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.side_by_side_report.parent.mkdir(parents=True, exist_ok=True)
    args.side_by_side_markdown.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.side_by_side_report.write_text(
        json.dumps(side_by_side_report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.side_by_side_markdown.write_text(side_by_side_markdown, encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "valid_v02_demo_receipt" and side_by_side_report["status"] == "ready_for_demo" else 1


if __name__ == "__main__":
    raise SystemExit(main())
