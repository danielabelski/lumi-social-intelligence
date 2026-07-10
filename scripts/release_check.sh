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

git diff --check

echo "release check passed"
