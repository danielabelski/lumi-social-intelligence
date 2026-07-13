import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_v050_cache_backed_fast_lane_is_authorized_local_and_bounded():
    from lumi_social_intelligence.care_release import build_cache_backed_fast_lane_plan

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

    assert plan["schema"] == "lumi.v050.cache_backed_fast_lane.v1"
    assert plan["version"] == "0.5.0"
    assert plan["status"] == "ready_for_host_reply"
    assert plan["direct_reply_allowed"] is True
    assert plan["eligibility"] == {
        "authorized_sender_required": True,
        "platform_scope": "telegram_direct_message",
        "supported_intent_scope": "weather_or_scooter_departure",
        "fresh_valid_cache_required": True,
    }
    assert plan["cache_contract"] == {
        "cache_read_location": "host_local_state_only",
        "network_io_allowed": False,
        "max_age_seconds": 43200,
        "raw_cache_content_exported": False,
    }
    assert plan["dispatch_contract"] == {
        "authorization_precedes_direct_reply": True,
        "agent_session_or_compression_allowed": False,
        "agent_tool_calls_allowed": 0,
        "reply_char_limit": 4096,
        "normal_delivery_adapter_required": True,
    }
    assert plan["fallback_contract"]["on_unauthorized_sender"] == "normal_auth_or_pairing_flow"
    assert plan["fallback_contract"]["on_unsupported_or_missing_intent"] == "normal_full_dispatch"
    assert plan["fallback_contract"]["on_missing_invalid_or_stale_cache"] == "normal_full_dispatch"
    assert plan["side_effects"] == {
        "telegram_messages_sent_by_public_repo": 0,
        "telegram_reactions_sent_by_public_repo": 0,
        "private_runtime_reads_by_public_repo": 0,
        "runtime_mutations_by_public_repo": 0,
    }


def test_v050_fast_lane_falls_through_when_any_eligibility_condition_is_missing():
    from lumi_social_intelligence.care_release import build_cache_backed_fast_lane_plan

    for context, reason, fallback in [
        ({"authorized_sender": False, "is_direct_message": True, "supported_intent": "weather_or_scooter_departure", "cache_fresh": True, "cache_valid": True}, "unauthorized_sender", "normal_auth_or_pairing_flow"),
        ({"authorized_sender": True, "is_direct_message": False, "supported_intent": "weather_or_scooter_departure", "cache_fresh": True, "cache_valid": True}, "unsupported_platform_or_non_direct_message", "normal_full_dispatch"),
        ({"authorized_sender": True, "is_direct_message": True, "supported_intent": "other", "cache_fresh": True, "cache_valid": True}, "unsupported_or_missing_intent", "normal_full_dispatch"),
        ({"authorized_sender": True, "is_direct_message": True, "supported_intent": "weather_or_scooter_departure", "cache_fresh": False, "cache_valid": True}, "missing_invalid_or_stale_cache", "normal_full_dispatch"),
        ({"authorized_sender": True, "is_direct_message": True, "supported_intent": "weather_or_scooter_departure", "cache_fresh": True, "cache_valid": False}, "missing_invalid_or_stale_cache", "normal_full_dispatch"),
    ]:
        plan = build_cache_backed_fast_lane_plan(
            now="2026-07-13T16:00:00+07:00",
            source="telegram",
            context=context,
        )
        assert plan["status"] == "fallback_full_dispatch"
        assert plan["direct_reply_allowed"] is False
        assert plan["fallback_reason"] == reason
        assert plan["fallback_action"] == fallback


def test_v050_evidence_builder_and_artifacts_are_public_safe(tmp_path):
    evidence = tmp_path / "v0.5.0-cache-fast-lane-evidence.json"
    markdown = tmp_path / "v0.5.0-cache-fast-lane-evidence.md"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_v050_cache_fast_lane_evidence.py",
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
    assert report["version"] == "0.5.0"
    assert receipt["schema"] == "lumi.v050.cache_fast_lane_evidence.v1"
    assert receipt["fast_lane_contract"]["dispatch_contract"]["authorization_precedes_direct_reply"] is True
    assert receipt["fast_lane_contract"]["cache_contract"]["network_io_allowed"] is False
    assert receipt["public_boundary"]["ships_private_hermes_adapter"] is False
    assert receipt["public_boundary"]["raw_private_runtime_state"] is False
    assert receipt["side_effects"]["telegram_messages_sent_by_public_repo"] == 0
    assert "Falls through normally" in md
    assert "12-hour cache freshness ceiling" in md

    artifact_dir = tmp_path / "artifacts"
    artifact_result = subprocess.run(
        [sys.executable, "scripts/build_release_artifacts.py", "--version", "0.5.0", "--output-dir", str(artifact_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    artifact_report = json.loads(artifact_result.stdout)
    manifest = json.loads((artifact_dir / "release-manifest.json").read_text(encoding="utf-8"))
    archive = artifact_dir / "lumi-social-intelligence-0.5.0.zip"

    assert artifact_report["version"] == "0.5.0"
    assert manifest["cache_fast_lane_evidence"]["status"] == "verified"
    assert "docs/releases/v0.5.0.md" in manifest["archive_members"]
    assert "docs/evidence/v0.5.0-cache-fast-lane-evidence.json" in manifest["archive_members"]
    assert "docs/evidence/v0.5.0-cache-fast-lane-evidence.md" in manifest["archive_members"]
    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())
    assert "docs/releases/v0.5.0.md" in names
    assert "docs/evidence/v0.5.0-cache-fast-lane-evidence.json" in names
    assert "docs/evidence/v0.5.0-cache-fast-lane-evidence.md" in names


def test_v050_release_notes_state_the_contract_and_public_boundary():
    text = (ROOT / "docs/releases/v0.5.0.md").read_text(encoding="utf-8")

    assert "# Lumi Social Intelligence v0.5.0" in text
    assert "cache-backed fast lane" in text
    assert "authorization precedes direct reply" in text
    assert "Falls through normally" in text
    assert "12-hour cache freshness ceiling" in text
    assert "does **not** ship the private Hermes runtime adapter" in text
    assert "canonical_writes: 0" in text
    assert "private_runtime_reads_by_public_repo: 0" in text
