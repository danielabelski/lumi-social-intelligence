import json
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_live_surface_reaction_intent_is_instant_deterministic_and_no_tool_spelunking():
    from lumi_social_intelligence.care_release import build_care_action_plan

    plan = build_care_action_plan(
        "Add emoji to my last message",
        now="2026-07-12T09:00:00+07:00",
        source="telegram",
        context={"last_user_message_ref": "platform:last_user_message", "default_emoji": "❤️"},
    )

    assert plan["schema"] == "lumi.v042.care_action_plan.v1"
    assert plan["version"] == "0.4.2"
    assert plan["intent"] == "react_to_last_user_message"
    assert plan["emoji"] == "❤️"
    assert plan["target"]["kind"] == "last_user_message"
    assert plan["target"]["resolution"] == "host_envelope_required"
    assert plan["execution_lane"] == "instant_control_plane"
    assert plan["agent_tool_calls_allowed"] == 0
    assert plan["visible_latency_budget"] == "instant"
    assert plan["db_archaeology_allowed"] is False
    assert plan["tool_discovery_allowed"] is False
    assert plan["llm_planning_required"] is False
    assert plan["side_effects"] == {
        "telegram_messages_sent_by_public_repo": 0,
        "telegram_reactions_sent_by_public_repo": 0,
        "private_runtime_reads_by_public_repo": 0,
        "runtime_mutations_by_public_repo": 0,
    }


def test_next_step_care_narrates_before_action_and_confirm_after():
    from lumi_social_intelligence.care_release import build_care_action_plan

    plan = build_care_action_plan(
        "React with 😂 to my last message",
        now="2026-07-12T09:00:00+07:00",
        source="telegram",
        context={"last_user_message_ref": "platform:last_user_message"},
    )

    narration = plan["next_step_care"]
    assert narration["principle"] == "reduce_uncertainty_before_task_time"
    assert narration["before_action"] == "I’m going to react with 😂 to your latest Telegram message."
    assert narration["after_success"] == "Done 😂"
    assert narration["fail_closed"] == "I can’t safely find the last message id, so I won’t guess."
    assert narration["tone"] == "tiny_predictable_caring_not_infantilizing"
    assert narration["must_precede_side_effect"] is True


def test_missing_last_message_ref_fails_closed_without_guessing():
    from lumi_social_intelligence.care_release import build_care_action_plan

    plan = build_care_action_plan(
        "Add emoji to my last message",
        now="2026-07-12T09:00:00+07:00",
        source="telegram",
        context={},
    )

    assert plan["status"] == "blocked_missing_target"
    assert plan["actionable"] is False
    assert plan["target"]["available"] is False
    assert plan["next_step_care"]["before_action"] == "I can’t safely find the last message id, so I won’t guess."
    assert plan["agent_tool_calls_allowed"] == 0
    assert plan["db_archaeology_allowed"] is False


def test_v042_evidence_builder_documents_care_release_contract(tmp_path):
    evidence = tmp_path / "v0.4.2-care-release-evidence.json"
    markdown = tmp_path / "v0.4.2-care-release-evidence.md"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_v042_care_release_evidence.py",
            "--evidence",
            str(evidence),
            "--markdown",
            str(markdown),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    report = json.loads(result.stdout)
    receipt = json.loads(evidence.read_text(encoding="utf-8"))
    md = markdown.read_text(encoding="utf-8")

    assert report["status"] == "verified"
    assert report["version"] == "0.4.2"
    assert receipt["schema"] == "lumi.v042.care_release_evidence.v1"
    assert receipt["status"] == "verified"
    assert receipt["release_principle"] == "Live Surface reduces uncertainty before it reduces task time"
    assert receipt["instant_reaction_contract"]["agent_tool_calls_allowed"] == 0
    assert receipt["instant_reaction_contract"]["tool_discovery_allowed"] is False
    assert receipt["instant_reaction_contract"]["db_archaeology_allowed"] is False
    assert receipt["next_step_care_contract"]["must_precede_side_effect"] is True
    assert receipt["public_boundary"]["sends_telegram_reactions"] is False
    assert receipt["public_boundary"]["ships_private_hermes_adapter"] is False
    assert receipt["side_effects"]["telegram_reactions_sent_by_public_repo"] == 0
    assert "Next-Step Care" in md
    assert "0 tool calls" in md
    assert "I can’t safely find the last message id" in md


def test_v042_release_artifacts_include_care_release_evidence(tmp_path):
    result = subprocess.run(
        [sys.executable, "scripts/build_release_artifacts.py", "--version", "0.4.2", "--output-dir", str(tmp_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    report = json.loads(result.stdout)
    manifest = json.loads((tmp_path / "release-manifest.json").read_text(encoding="utf-8"))
    archive = tmp_path / "lumi-social-intelligence-0.4.2.zip"

    assert report["version"] == "0.4.2"
    assert report["artifacts"] == ["lumi-social-intelligence-0.4.2.zip", "release-manifest.json", "SHA256SUMS"]
    assert manifest["version"] == "0.4.2"
    assert manifest["care_release_evidence"]["status"] == "verified"
    assert manifest["care_release_evidence"]["instant_reaction_contract"]["agent_tool_calls_allowed"] == 0
    assert "docs/releases/v0.4.2.md" in manifest["archive_members"]
    assert "docs/evidence/v0.4.2-care-release-evidence.json" in manifest["archive_members"]
    assert "docs/evidence/v0.4.2-care-release-evidence.md" in manifest["archive_members"]

    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())
    assert "docs/releases/v0.4.2.md" in names
    assert "docs/evidence/v0.4.2-care-release-evidence.json" in names
    assert "docs/evidence/v0.4.2-care-release-evidence.md" in names


def test_v042_release_notes_name_the_missed_care_requirement():
    text = (ROOT / "docs/releases/v0.4.2.md").read_text(encoding="utf-8")

    assert "# Lumi Social Intelligence v0.4.2" in text
    assert "care release" in text.lower()
    assert "Next-Step Care" in text
    assert "neurodivergent" in text
    assert "0 tool calls" in text
    assert "not guess" in text
    assert "canonical_writes: 0" in text
    assert "telegram_reactions_sent_by_public_repo: 0" in text
