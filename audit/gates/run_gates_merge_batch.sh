#!/usr/bin/env bash
# Gate runner for card t_b734b27a — merge batch light-colour-r2 + station-legend
# + level-rule-ledger into main. Every EXIT= in the log is the subprocess's real
# return code, never typed by hand.
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=merge-batch-2026-11-21
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/${BRANCH}-${SHA}.log"
MKDOCS=/root/pfd-ssg-env/bin/mkdocs
OUT=$(mktemp /dev/shm/gate_out_batch.XXXXXX)
{
echo "# gate log — merge batch (light-colour-r2, station-legend, level-rule-ledger) into main"
echo "# merge commit ${SHA} on branch $(git rev-parse --abbrev-ref HEAD)"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_merge_batch.sh (card t_b734b27a)"
echo "# site gates run after the strict build"
echo
run() {
  local name="$1"; shift
  echo "## gate: ${name}"
  echo "cmd: $*"
  "$@" > "$OUT" 2>&1
  local rc=$?
  tail -n 40 "$OUT"
  echo "EXIT=${rc}"
  echo
  if [ "$rc" -ne 0 ]; then FAILED="${FAILED} ${name}=${rc}"; fi
}
FAILED=""
run verify_pems_canonical python3 scripts/verify_pems_canonical.py
run level_rule python3 scripts/level_rule.py --check
run pip_legend_unique python3 scripts/check_pip_legend_unique.py
run mc_wording python3 scripts/mc_wording.py --check
run agency_names python3 scripts/agency_names.py --check
run build_outstanding python3 scripts/build_outstanding_decisions.py --check
run internal_artifacts python3 scripts/internal_artifacts.py --check
run mkdocs_strict "$MKDOCS" build --strict
run link_sweep python3 scripts/link_sweep.py site
run internal_artifacts_site python3 scripts/internal_artifacts.py --check --site site
echo "## summary"
if [ -z "$FAILED" ]; then echo "ALL GATES EXIT=0 (10 of 10)"; else echo "FAILED:${FAILED}"; fi
} 2>&1 | tee "${LOG}"
rm -f "$OUT"
grep -q "ALL GATES EXIT=0" "${LOG}"
