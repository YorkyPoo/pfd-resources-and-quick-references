#!/usr/bin/env bash
# Gate runner for card t_e787ab8d — homepage -> on-scene dashboard.
# Writes the log to audit/gates/<branch>-<sha>.log (acceptance item 6).
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=homepage-dashboard
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/${BRANCH}-${SHA}.log"
export PATH=/root/pfd-ssg-env/bin:$PATH
mkdir -p audit/gates
{
echo "# gate log — branch ${BRANCH}, content commit ${SHA}"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_homepage.sh (card t_e787ab8d)"
echo "# gates run on the content commit ${SHA}; site gates after the strict build"
echo
run() {
  local name="$1"; shift
  echo "## gate: ${name}"
  echo "cmd: $*"
  "$@" > /tmp/home_gate_out.txt 2>&1
  local rc=$?
  tail -n 25 /tmp/home_gate_out.txt
  echo "EXIT=${rc}"
  echo
  if [ "$rc" -ne 0 ]; then FAILED="${FAILED} ${name}=${rc}"; fi
}
FAILED=""
run gen_resource_pages python3 scripts/gen_resource_pages.py --check
run pip_mapper python3 scripts/test_pip_strip_mapper.py
run verify_pems_canonical python3 scripts/verify_pems_canonical.py --check
run level_rule python3 scripts/level_rule.py --check
run mc_wording python3 scripts/mc_wording.py --check
run agency_names python3 scripts/agency_names.py --check
run build_outstanding python3 scripts/build_outstanding_decisions.py --check
run internal_artifacts python3 scripts/internal_artifacts.py --check
run mkdocs_strict mkdocs build --strict
run verify_pip_strip python3 scripts/verify_pip_strip.py --base site --archive audit/archive/tables-2026-11-20
run link_sweep python3 scripts/link_sweep.py site
run internal_artifacts_site python3 scripts/internal_artifacts.py --check --site site
echo "## summary"
if [ -z "$FAILED" ]; then echo "ALL GATES EXIT=0 (12 of 12)"; else echo "FAILED:${FAILED}"; fi
} 2>&1 | tee "${LOG}"
