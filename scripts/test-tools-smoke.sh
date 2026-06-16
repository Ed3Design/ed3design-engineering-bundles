#!/usr/bin/env bash
# test-tools-smoke.sh — behavioral smoke-test for the helper tools.
#
# `--help`-only checks are insufficient (they miss runtime errors on the
# documented happy path). This test invokes each tool against a real fixture
# and verifies the produced artifact, then runs a negative case to confirm
# bad input is rejected with a non-zero exit.
#
# Wired into CI as a fast feedback gate.

set -u

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$REPO_ROOT/cad-design/tools/generate_fusion360_parameters.py"

PASS=0
FAIL=0

ok()   { PASS=$((PASS + 1)); echo "  ✅ $1"; }
bad()  { FAIL=$((FAIL + 1)); echo "  ❌ $1"; }

echo "── generate_fusion360_parameters.py ──"

# Pre-flight: executable + shebang
[ -x "$TOOL" ] || bad "tool not executable"
head -1 "$TOOL" | grep -q "^#!" || bad "tool missing shebang"

# --help exits 0
if "$TOOL" --help > /dev/null 2>&1; then ok "--help exits 0"; else bad "--help failed"; fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Happy path: documented top-level-list format → valid add-in
cat > "$TMP/params.json" <<'JSON'
[
  {"name": "outerDiameter", "value": 80,  "unit": "mm", "comment": "Housing OD"},
  {"name": "wallThickness", "value": 2.5, "unit": "mm", "comment": "Default wall"}
]
JSON
if "$TOOL" "$TMP/params.json" "$TMP/out.py" > /dev/null 2>&1; then
    if [ -s "$TMP/out.py" ] && python3 -m py_compile "$TMP/out.py" 2>/dev/null; then
        ok "happy path produces a compilable add-in"
    else
        bad "happy path output missing or does not compile"
    fi
else
    bad "happy path invocation failed (exit non-zero)"
fi

# Negative case: malformed input (object instead of list) must be rejected
cat > "$TMP/bad.json" <<'JSON'
{"parameters": [{"name": "x", "value": 1}]}
JSON
if "$TOOL" "$TMP/bad.json" "$TMP/bad_out.py" > /dev/null 2>&1; then
    bad "malformed input was accepted (should reject with non-zero exit)"
else
    ok "malformed input rejected with non-zero exit"
fi

echo ""
echo "  PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -gt 0 ] && exit 1
exit 0
