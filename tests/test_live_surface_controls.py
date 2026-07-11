from lumi_social_intelligence.live_surface_controls import (
    SIDE_EFFECTS_ZERO,
    apply_control_shadow,
    build_control_state,
    parse_control_intent,
    render_control_ack,
)


def test_safe_keep_fresh_control_is_local_reversible_and_quiet():
    card = apply_control_shadow(
        "keep this ready for when I leave",
        now="2026-07-11T17:00:00+07:00",
        source="host_shadow_surface",
    )

    state = card["state"]
    assert state["intent"] == "keep_fresh"
    assert state["scope"] == "session"
    assert state["status"] == "active"
    assert state["review_status"] == "not_required"
    assert state["reversible"] is True
    assert state["raw_user_text_stored"] is False
    assert state["raw_user_text_hash"].startswith("sha256:")
    assert state["refresh_policy"] == "safe_readiness_only"
    assert state["surfacing_policy"] == "presence_gated"
    assert card["ack"] == "Got it — I’ll keep it warm quietly."
    assert card["side_effects"] == SIDE_EFFECTS_ZERO


def test_calendar_free_busy_request_requires_surface_review_and_no_read():
    card = apply_control_shadow(
        "check my calendar and keep plans fresh",
        now="2026-07-11T17:00:00+07:00",
        source="host_shadow_surface",
    )

    state = card["state"]
    assert state["intent"] == "add_surface"
    assert state["scope"] == "review_required"
    assert state["status"] == "pending_review"
    assert state["needs_confirmation"] is True
    assert "personal_data_surface" in state["safety_flags"]
    assert "personal_data_read_blocked" in state["safety_flags"]
    assert state["target"]["surface_membership_required"] == ["explicit_user_approval"]
    assert state["side_effects"]["calendar_reads_without_surface"] == 0
    assert state["side_effects"]["personal_data_reads"] == 0
    assert card["ack"] == "I can add that, but Calendar needs your explicit okay first."


def test_acknowledgements_do_not_expose_runtime_plumbing():
    forbidden = ("ctrl_", "queue", "cron", "job_id", "scheduler", "json", "schema", "config", "runtime")
    samples = [
        "what are you keeping warm",
        "only bring this up if I ask",
        "send them a message if this changes",
        "make it less like that",
    ]

    for sample in samples:
        ack = render_control_ack(build_control_state(sample, now="2026-07-11T17:00:00+07:00", source="host_shadow_surface"))
        assert not any(token in ack.lower() for token in forbidden)


def test_external_send_scheduler_and_durable_memory_are_review_gated():
    cases = [
        ("send them a message if this changes", "external_send_blocked"),
        ("schedule a daily job for this", "scheduler_mutation_blocked"),
        ("remember forever that I always want this", "durable_memory_review_required"),
    ]

    for text, flag in cases:
        parsed = parse_control_intent(text)
        assert parsed["needs_confirmation"] is True
        assert parsed["scope"] == "review_required"
        assert flag in parsed["safety_flags"]


def test_shadow_card_never_claims_runtime_promotion_or_side_effects():
    card = apply_control_shadow("park this for later", now="2026-07-11T17:00:00+07:00")
    assert card["promotion_scope"] == "local_shadow_evidence_only_no_runtime_apply"
    assert all(value == 0 for value in card["side_effects"].values())
    assert card["ack"] == "Got it — captured now, I’ll enrich it later quietly."
