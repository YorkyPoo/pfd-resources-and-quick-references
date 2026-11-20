#!/usr/bin/env bash
# Gate runner for card t_432b2e79 — merge of peep-final (d92dfbc) into main.
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=peep-final
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/${BRANCH}-${SHA}.log"
MKDOCS=/root/pfd-ssg-env/bin/mkdocs
TMPOUT=/root/.hermes/profiles/developer/cache/scratch/gate_out_peepfinal.txt
{
echo "# gate log — merge of ${BRANCH} into main, merge commit ${SHA}"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_merge_peepfinal.sh (card t_432b2e79)"
echo "# parents: main 9995acd + ${BRANCH} d92dfbc"
echo "# ancestry precondition: git merge-base --is-ancestor origin/main peep-final -> exit 0 (main had not moved)"
echo
FAILED=""
run() {
  local name="$1"; shift
  echo "## gate: ${name}"
  echo "cmd: $*"
  "$@" > "$TMPOUT" 2>&1
  local rc=$?
  tail -n 40 "$TMPOUT"
  echo "EXIT=${rc}"
  echo
  if [ "$rc" -ne 0 ]; then FAILED="${FAILED} ${name}=${rc}"; fi
}
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