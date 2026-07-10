import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from lumi_presence import decide_presence_move


def test_presence_holds_without_grounded_context():
    decision = decide_presence_move(why_now="maybe say something", grounded=False, side_effect=False)

    assert decision == {
        "move": "hold",
        "reason": "missing grounded context",
        "side_effect_allowed": False,
    }


def test_presence_speaks_only_with_why_now_and_no_side_effect():
    decision = decide_presence_move(
        why_now="User is leaving and practical timing help is useful",
        grounded=True,
        side_effect=False,
    )

    assert decision["move"] == "speak"
    assert decision["side_effect_allowed"] is True


def test_presence_keeps_side_effects_gated():
    decision = decide_presence_move(
        why_now="A reviewed suggestion card is useful",
        grounded=True,
        side_effect=True,
    )

    assert decision["move"] == "speak"
    assert decision["side_effect_allowed"] is False
