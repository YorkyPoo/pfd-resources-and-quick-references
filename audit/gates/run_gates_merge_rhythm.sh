#!/usr/bin/env bash
# Gate runner for card t_c2820e77 — merge of rhythm-derive into main.
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=merge-rhythm-derive
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/${BRANCH}-${SHA}.log"
MKDOCS=/root/pfd-ssg-env/bin/mkdocs
{
echo "# gate log — ${BRANCH}, merge commit ${SHA}"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_merge_rhythm.sh (card t_c2820e77)"
echo "# merged origin/rhythm-derive (58e1626, synced with main) into main"
echo
FAILED=""
run() {
  local name="$1"; shift
  echo "## gate: ${name}"
  echo "cmd: $*"
  "$@" > /tmp/gate_out_rhythm.txt 2>&1
  local rc=$?
  tail -n 40 /tmp/gate_out_rhythm.txt
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
