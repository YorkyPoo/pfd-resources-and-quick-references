#!/usr/bin/env bash
# Gate runner for card t_09250ff7 — merge of pipstrip-rollout (b3ff73b) into main.
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=pipstrip-rollout
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/${BRANCH}-${SHA}.log"
MKDOCS=/root/pfd-ssg-env/bin/mkdocs
TMPOUT=/root/.hermes/profiles/developer/cache/scratch/gate_out_pipstrip_deploy.txt
{
echo "# gate log — merge of ${BRANCH} into main, merge commit ${SHA}"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_merge_pipstrip.sh (card t_09250ff7)"
echo "# parents: main d5fd03c + ${BRANCH} b3ff73b"
echo "# ancestry precondition: git merge-base --is-ancestor origin/main b3ff73b -> exit 0 (main had not moved)"
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
run internal_artifacts python3 scripts/internal_artifacts.py --check
run build_outstanding python3 scripts/build_outstanding_decisions.py --check
run pip_mapper python3 scripts/test_pip_strip_mapper.py
run mkdocs_strict "$MKDOCS" build --strict
run link_sweep python3 scripts/link_sweep.py site
run internal_artifacts_site python3 scripts/internal_artifacts.py --check --site site
run pip_strip_parity python3 scripts/verify_pip_strip.py --base site --quiet
run pip_strip_negative python3 scripts/negative_test_pip_strip.py
echo "## summary"
if [ -z "$FAILED" ]; then echo "ALL GATES EXIT=0 (12 of 12)"; else echo "FAILED:${FAILED}"; fi
} 2>&1 | tee "${LOG}"
