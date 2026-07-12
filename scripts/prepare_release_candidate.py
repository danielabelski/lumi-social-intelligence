#!/usr/bin/env python3
"""Prepare a non-mutating release-candidate plan for Lumi Social Intelligence."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NOTES = 'docs/releases/v0.4.1.md'


def _run(command: list[str]) -> str:
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def _is_clean_status(status: str) -> bool:
    lines = [line for line in status.splitlines() if line.strip()]
    return all(line.startswith('## ') for line in lines)


def _release_notes_summary(notes_path: Path) -> dict:
    text = notes_path.read_text(encoding='utf-8')
    if notes_path.name == 'v0.4.1.md':
        required = [
            'Hermes native Telegram emoji reaction delivery',
            'ReactionTypeEmoji',
            'primitive emoji string',
            'does not ship the private Hermes adapter',
            'raw private Hermes runtime state',
            'canonical_writes: 0',
            'telegram_reactions_sent_by_public_repo: 0',
        ]
    elif notes_path.name == 'v0.4.0.md':
        required = [
            'real public release of review-gated Live Surface natural-language controls',
            'not a shadow-only release',
            'Real review-gated public capability',
            'shadow_only: false',
            'Missing Calendar behavior',
            'canonical_writes: 0',
            'private_runtime_reads: 0',
            'not autonomous private runtime automation',
        ]
    elif notes_path.name == 'v0.3.0.md':
        required = [
            'shadow-only Live Surface natural-language controls',
            'Observed / verified in this repository',
            'Review-gated / no-write boundary',
            'Not yet supported or not yet claimed live',
            'Natural-language Live Surface control parsing',
            'Calendar/email reads',
            'blocked in shadow mode',
            'canonical_memory_writes: 0',
        ]
    elif notes_path.name == 'v0.2.0.md':
        required = [
            'release-candidate',
            'Observed / verified in this repository',
            'Review-gated / no-write boundary',
            'Not yet supported or not yet claimed live',
            'native outbound emoji reaction delivery',
            'not_claimed',
            'canonical_writes: 0',
            'docs/demos/v0.2-demo-evidence.json',
        ]
    else:
        required = [
            'We are making the self-improvement loop something that is human-shaped.',
            'governed reflection layer',
            'not an auto-personality-rewriter',
            'confidence scoring',
            'contradiction handling',
            'user approval',
            'skill evaluation',
            'Lumi for Hermes',
            'canonical_writes: 0',
        ]
    missing = [item for item in required if item not in text]
    return {
        'path': str(notes_path.relative_to(ROOT)),
        'required_positioning_present': not missing,
        'missing_required_positioning': missing,
        'line_count': len(text.splitlines()),
    }


def build_plan(tag: str = 'v0.4.1', notes_path: str = DEFAULT_NOTES) -> dict:
    blockers: list[str] = []
    status = _run(['git', 'status', '--short', '--branch'])
    branch = _run(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip()
    head = _run(['git', 'rev-parse', 'HEAD']).strip()
    existing_tags = set(_run(['git', 'tag', '--list', 'v*']).splitlines())

    if not _is_clean_status(status):
        blockers.append('working tree is not clean; commit or revert changes before tagging')
    if branch != 'main':
        blockers.append(f'expected branch main, got {branch}')
    if tag in existing_tags:
        blockers.append(f'tag already exists: {tag}')

    notes = ROOT / notes_path
    if not notes.is_file():
        blockers.append(f'release notes missing: {notes_path}')
        notes_summary = {'path': notes_path, 'required_positioning_present': False, 'missing_required_positioning': ['release notes file missing']}
    else:
        notes_summary = _release_notes_summary(notes)
        if not notes_summary['required_positioning_present']:
            blockers.append(f'release notes missing required positioning: {notes_summary["missing_required_positioning"]}')

    plan = {
        'schema': 'lumi.release_candidate_plan.v1',
        'status': 'blocked' if blockers else 'ready',
        'tag': tag,
        'target_branch': 'main',
        'current_branch': branch,
        'head': head,
        'release_notes': notes_path,
        'release_notes_summary': notes_summary,
        'canonical_writes': 0,
        'pushes': [],
        'blockers': blockers,
        'recommended_commands': [
            './scripts/release_check.sh',
            f'git tag -a {tag} -m "Lumi Social Intelligence {tag}"',
            f'git push origin {tag}',
        ],
        'human_decision_required': [
            'confirm repository visibility before any public release',
            'inspect release artifacts and SHA256SUMS',
            'decide whether to publish this release-candidate or keep it as demo evidence only',
        ],
        'safety': {
            'creates_tag': False,
            'pushes_tag': False,
            'creates_github_release': False,
            'notes': 'This script is a dry-run planner. It does not tag, push, publish, or mutate runtime state.',
        },
    }
    return plan


def main(argv: list[str] | None = None) -> dict:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tag', default='v0.4.1')
    parser.add_argument('--notes', default=DEFAULT_NOTES)
    parser.add_argument('--report', default='')
    args = parser.parse_args(argv)

    plan = build_plan(tag=args.tag, notes_path=args.notes)
    payload = json.dumps(plan, indent=2, sort_keys=True)
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(payload + '\n', encoding='utf-8')
    print(payload)
    return plan


if __name__ == '__main__':
    result = main()
    sys.exit(0 if result['status'] == 'ready' else 1)
