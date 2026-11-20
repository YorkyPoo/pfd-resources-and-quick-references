#!/usr/bin/env bash
# Gate runner for card t_7a22b040 — reviewer round 1 fix (CPAP Pearls bullet). Writes to audit/gates/.
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=peep-final
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/${BRANCH}-${SHA}.log"
MKDOCS=/root/pfd-ssg-env/bin/mkdocs
{
echo "# gate log — ${BRANCH}, commit ${SHA}"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_peep_final_pearls.sh (card t_7a22b040)"
echo "# re-run after the reviewer's blocking item: docs/procedures/CPAP.md Pearls bullet qualified to the owner ruling"
echo
FAILED=""
run() {
  local name="$1"; shift
  echo "## gate: ${name}"
  echo "cmd: $*"
  "$@" > /tmp/gate_out.txt 2>&1
  local rc=$?
  tail -n 40 /tmp/gate_out.txt
  echo "EXIT=${rc}"
  echo
  if [ "$rc" -ne 0 ]; then FAILED="${FAILED} ${name}=${rc}"; fi
}
run verify_pems_canonical python3 scripts/verify_pems_canonical.py
run level_rule python3 scripts/level_rule.py --check
run mc_wording python3 scripts/mc_wording.py --check
run build_outstanding python3 scripts/build_outstanding_decisions.py --check
run mkdocs_strict "$MKDOCS" build --strict
echo "## summary"
if [ -z "$FAILED" ]; then echo "ALL GATES EXIT=0 (5 of 5)"; else echo "FAILED:${FAILED}"; fi
} 2>&1 | tee "${LOG}"
