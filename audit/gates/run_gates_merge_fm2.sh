#!/usr/bin/env bash
# Gate runner for card t_51e5ae18 — merge of front-matter-2 into main.
# Same shape as audit/gates/run_gates.sh: every EXIT= in the log is the
# subprocess's real return code, never typed by hand.
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=integrate-fm2
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/${BRANCH}-${SHA}.log"
MKDOCS=/root/pfd-ssg-env/bin/mkdocs
{
echo "# gate log — merge of front-matter-2 into main, merge commit ${SHA}"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_merge_fm2.sh (card t_51e5ae18)"
echo "# gates run on the merge commit ${SHA} (site gates after the strict build)"
echo "# ancestry gate: git merge-base --is-ancestor origin/main front-matter-2 (branch tip 2f9d814)"
echo
run() {
  local name="$1"; shift
  echo "## gate: ${name}"
  echo "cmd: $*"
  "$@" > /tmp/gate_out_fm2_merge.txt 2>&1
  local rc=$?
  tail -n 40 /tmp/gate_out_fm2_merge.txt
  echo "EXIT=${rc}"
  echo
  FAILED=${FAILED:-}
  if [ "$rc" -ne 0 ]; then FAILED="${FAILED} ${name}=${rc}"; fi
}
FAILED=""
run verify_pems_canonical python3 scripts/verify_pems_canonical.py
run level_rule python3 scripts/level_rule.py --check
run mc_wording python3 scripts/mc_wording.py --check
run agency_names python3 scripts/agency_names.py --check
run build_outstanding python3 scripts/build_outstanding_decisions.py --check
run internal_artifacts python3 scripts/internal_artifacts.py --check
run mkdocs_strict "$MKDOCS" build --strict
run link_sweep python3 scripts/link_sweep.py site
run internal_artifacts_site python3 scripts/internal_artifacts.py --check --site site
echo "## summary"
if [ -z "$FAILED" ]; then echo "ALL GATES EXIT=0 (9 of 9)"; else echo "FAILED:${FAILED}"; fi
} 2>&1 | tee "${LOG}"
grep -q "ALL GATES EXIT=0" "${LOG}"
