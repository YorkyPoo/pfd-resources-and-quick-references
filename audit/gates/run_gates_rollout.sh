#!/usr/bin/env bash
# Gate runner for the pip-strip rollout (card t_a3480fb0).
# Writes the log to audit/gates/<branch>-<sha>.log. Every gate prints EXIT=n.
set -uo pipefail
cd "$(dirname "$0")/.."
BRANCH=pipstrip-rollout
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/${BRANCH}-${SHA}.log"
MKDOCS=/root/pfd-ssg-env/bin/mkdocs
{
echo "# gate log — branch ${BRANCH}, content commit ${SHA}"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_rollout.sh (card t_a3480fb0)"
echo "# main $(git rev-parse --short main); site gates after the strict build"
echo
run() {
  local name="$1"; shift
  echo "## gate: ${name}"
  echo "cmd: $*"
  "$@" > /tmp/gate_out_rollout.txt 2>&1
  local rc=$?
  tail -n 40 /tmp/gate_out_rollout.txt
  echo "EXIT=${rc}"
  echo
  if [ "$rc" -ne 0 ]; then FAILED="${FAILED} ${name}=${rc}"; fi
}
FAILED=""
run verify_pems_canonical python3 scripts/verify_pems_canonical.py
run level_rule python3 scripts/level_rule.py --check
run mc_wording python3 scripts/mc_wording.py --check
run agency_names python3 scripts/agency_names.py --check
run internal_artifacts python3 scripts/internal_artifacts.py --check
run build_outstanding python3 scripts/build_outstanding_decisions.py --check
run pip_mapper python3 scripts/test_pip_strip_mapper.py
run mkdocs_strict "$MKDOCS" build --strict
run link_sweep python3 scripts/link_sweep.py site
run internal_artifacts_site python3 scripts/internal_artifacts.py --check --site site
run pip_strip_parity python3 scripts/verify_pip_strip.py --base site --quiet
run pip_strip_negative python3 scripts/negative_test_pip_strip.py
echo "## summary"
if [ -z "$FAILED" ]; then echo "ALL GATES EXIT=0"; else echo "FAILED:${FAILED}"; fi
} 2>&1 | tee "${LOG}"
