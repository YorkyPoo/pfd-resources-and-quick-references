#!/bin/bash
# run_gates.sh — the six acceptance gates for the PEMS p.55 sedation pass.
# Usage: bash audit/level-scan/logs/sedation-p55/run_gates.sh
# Writes one log per gate plus gates.txt (command, EXIT code) into this directory.
set -u
OUT="$(dirname "$0")"
run() {
  name="$1"; shift
  "$@" > "$OUT/$name.log" 2>&1
  rc=$?
  echo "cmd:  $*" >> "$OUT/gates.txt"
  echo "EXIT=$rc" >> "$OUT/gates.txt"
  echo "log:  audit/level-scan/logs/sedation-p55/$name.log" >> "$OUT/gates.txt"
  echo "-----" >> "$OUT/gates.txt"
  echo "$name EXIT=$rc"
}
rm -f "$OUT/gates.txt"
{
  echo "gate tree: $(git rev-parse HEAD)  ($(git log -1 --format='%s'))"
  echo "docs/ tree clean before run: $(test -z "$(git status --porcelain -- docs)" && echo yes || echo NO)"
  echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "======"
} >> "$OUT/gates.txt"
run verify_pems_canonical python3 scripts/verify_pems_canonical.py
run level_rule           python3 scripts/level_rule.py --check
run mc_wording           python3 scripts/mc_wording.py --check
run agency_names         python3 scripts/agency_names.py --check
run internal_artifacts   python3 scripts/internal_artifacts.py --check
run mkdocs               /root/pfd-ssg-env/bin/mkdocs build --strict
echo "=====" >> "$OUT/gates.txt"
echo "gates exit 0: $(grep -c '^EXIT=0$' "$OUT/gates.txt") of 6" >> "$OUT/gates.txt"
