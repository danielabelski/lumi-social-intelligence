#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TMP_ROOT="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT

python3 scripts/build_release_artifacts.py --version 0.4.1 --output-dir "$TMP_ROOT/artifacts" >/tmp/lumi-release-build-report.json

test -f "$TMP_ROOT/artifacts/lumi-social-intelligence-0.4.1.zip"
test -f "$TMP_ROOT/artifacts/release-manifest.json"
test -f "$TMP_ROOT/artifacts/SHA256SUMS"

python3 - "$TMP_ROOT/artifacts" <<'PY'
import hashlib
import json
import sys
import zipfile
from pathlib import Path

artifact_dir = Path(sys.argv[1])
manifest = json.loads((artifact_dir / 'release-manifest.json').read_text(encoding='utf-8'))
assert manifest['private_material_findings'] == []
assert manifest['canonical_writes'] == 0
assert manifest['version'] == '0.4.1'
assert manifest['v02_demo_verification']['status'] == 'verified'
assert manifest['v04_real_controls_evidence']['status'] == 'verified'
assert manifest['v04_real_controls_evidence']['shadow_only'] is False
assert 'installers/lumi-for-hermes/preview.py' in manifest['archive_members']
assert 'docs/releases/v0.4.1.md' in manifest['archive_members']
assert 'docs/evidence/v0.4.1-native-reaction-evidence.json' in manifest['archive_members']
assert manifest['native_telegram_reaction_evidence']['status'] == 'verified'
assert 'docs/demos/v0.2-demo-side-by-side.md' in manifest['archive_members']

archive = artifact_dir / manifest['archive']
with zipfile.ZipFile(archive) as zf:
    names = set(zf.namelist())
assert 'README.md' in names
assert 'scripts/release_check.sh' in names
assert all(not name.startswith(('.git/', '.hermes/', 'runs/', 'logs/')) for name in names)

checksums = {}
for line in (artifact_dir / 'SHA256SUMS').read_text(encoding='utf-8').splitlines():
    digest, name = line.split('  ', 1)
    checksums[name] = digest
for name, digest in checksums.items():
    assert hashlib.sha256((artifact_dir / name).read_bytes()).hexdigest() == digest
PY

echo "clean checkout smoke passed"
