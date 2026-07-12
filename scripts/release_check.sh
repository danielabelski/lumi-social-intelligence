#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== Lumi Social Intelligence release check =="

python3 -m compileall -q scripts tests

if command -v pytest >/dev/null 2>&1 && [ -d tests ]; then
  pytest -q
else
  echo "pytest not available or no tests yet; skipping test runner"
fi

python3 scripts/public_secret_scan.py
python3 scripts/validate_module_release_gates.py
python3 -m pytest -q tests/test_release_candidate.py
python3 scripts/verify_v02_demo_package.py >/tmp/lumi-v02-demo-verification.json
python3 scripts/build_v04_real_controls_evidence.py --evidence /tmp/lumi-v04-real-controls-evidence.json --markdown /tmp/lumi-v04-real-controls-evidence.md >/tmp/lumi-v04-real-controls-build.json
python3 scripts/build_v041_native_reaction_evidence.py --evidence /tmp/lumi-v041-native-reaction-evidence.json --markdown /tmp/lumi-v041-native-reaction-evidence.md >/tmp/lumi-v041-native-reaction-build.json
python3 scripts/public_readiness_audit.py --artifact-dir /tmp/lumi-public-readiness-artifacts --report /tmp/lumi-public-readiness-report.json
./scripts/clean_checkout_smoke.sh

git diff --check

echo "release check passed"
