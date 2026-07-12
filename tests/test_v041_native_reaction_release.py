import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_v041_native_reaction_evidence_documents_ptb_payload_contract(tmp_path):
    evidence = tmp_path / "v0.4.1-native-reaction-evidence.json"
    markdown = tmp_path / "v0.4.1-native-reaction-evidence.md"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_v041_native_reaction_evidence.py",
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
    assert report["version"] == "0.4.1"
    assert receipt["schema"] == "lumi.v041.native_reaction_evidence.v1"
    assert receipt["version"] == "0.4.1"
    assert receipt["status"] == "verified"
    assert receipt["claim_boundary"] == "Hermes native Telegram emoji reaction delivery verified; public release packages contract/evidence only"
    assert receipt["telegram_payload_contract"] == {
        "method": "Bot.set_message_reaction",
        "reaction": ["ReactionTypeEmoji(emoji='❤️')"],
        "accepted_primitive_reaction": False,
    }
    assert receipt["live_runtime_evidence"]["native_reaction_delivery"] == "verified"
    assert receipt["public_boundary"]["ships_private_hermes_adapter"] is False
    assert receipt["public_boundary"]["raw_private_runtime_state"] is False
    assert receipt["side_effects"] == {
        "telegram_messages_sent_by_public_repo": 0,
        "telegram_reactions_sent_by_public_repo": 0,
        "private_runtime_reads_by_public_repo": 0,
        "runtime_mutations_by_public_repo": 0,
    }
    assert "ReactionTypeEmoji" in md
    assert "does not ship the private Hermes adapter" in md
    assert "primitive emoji string" in md


def test_v041_release_artifacts_include_native_reaction_evidence(tmp_path):
    result = subprocess.run(
        [sys.executable, "scripts/build_release_artifacts.py", "--version", "0.4.1", "--output-dir", str(tmp_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    report = json.loads(result.stdout)
    manifest = json.loads((tmp_path / "release-manifest.json").read_text(encoding="utf-8"))
    archive = tmp_path / "lumi-social-intelligence-0.4.1.zip"

    assert report["version"] == "0.4.1"
    assert report["artifacts"] == ["lumi-social-intelligence-0.4.1.zip", "release-manifest.json", "SHA256SUMS"]
    assert manifest["version"] == "0.4.1"
    assert manifest["native_telegram_reaction_evidence"]["status"] == "verified"
    assert manifest["native_telegram_reaction_evidence"]["telegram_payload_contract"]["method"] == "Bot.set_message_reaction"
    assert "docs/releases/v0.4.1.md" in manifest["archive_members"]
    assert "docs/evidence/v0.4.1-native-reaction-evidence.json" in manifest["archive_members"]
    assert "docs/evidence/v0.4.1-native-reaction-evidence.md" in manifest["archive_members"]

    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())
    assert "docs/releases/v0.4.1.md" in names
    assert "docs/evidence/v0.4.1-native-reaction-evidence.json" in names
    assert "docs/evidence/v0.4.1-native-reaction-evidence.md" in names


def test_v041_release_notes_have_public_boundary_and_payload_contract():
    text = (ROOT / "docs/releases/v0.4.1.md").read_text(encoding="utf-8")

    assert "# Lumi Social Intelligence v0.4.1" in text
    assert "ReactionTypeEmoji" in text
    assert "primitive emoji string" in text
    assert "does not ship the private Hermes adapter" in text
    assert "raw private Hermes runtime state" in text
    assert "canonical_writes: 0" in text
    assert "telegram_reactions_sent_by_public_repo: 0" in text
