#!/usr/bin/env bash
# Gate runner for card t_7b6df26e — make `verify_pems_canonical` run off a clean clone.
# Same 17 gates as the level-rule-ledger run; verify_pems_canonical is the one this
# card repairs (it used to demand the git-ignored audit/level-scan/.cache/pems_rows.jsonl
# and was therefore red on every fresh checkout). protocols_untouched proves no protocol
# page's clinical content moved.
#
# The point of this run: it is executed in a FRESH `git clone` with NO
# audit/level-scan/.cache, so a green suite means the gate built its own input.
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=gate-rows-cache
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/${BRANCH}-${SHA}.log"
export PATH=/root/pfd-ssg-env/bin:$PATH
mkdir -p audit/gates
{
echo "# gate log — branch ${BRANCH}, content commit ${SHA}"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_gate_rows_cache.sh (card t_7b6df26e)"
echo "# run in a fresh git clone with no audit/level-scan/.cache: $( [ -e audit/level-scan/.cache ] && echo 'CACHE PRESENT (unexpected)' || echo 'no .cache at start' )"
echo "# gates run on the content commit ${SHA}; site gates after the strict build"
echo
run() {
  local name="$1"; shift
  echo "## gate: ${name}"
  echo "cmd: $*"
  "$@" > /tmp/gate_rows_cache_out.txt 2>&1
  local rc=$?
  tail -n 30 /tmp/gate_rows_cache_out.txt
  echo "EXIT=${rc}"
  echo
  if [ "$rc" -ne 0 ]; then FAILED="${FAILED} ${name}=${rc}"; fi
}
FAILED=""
run gen_resource_pages python3 scripts/gen_resource_pages.py --check
run connected_notes python3 scripts/gen_connected_notes.py --check
run pip_mapper python3 scripts/test_pip_strip_mapper.py
run verify_pems_canonical python3 scripts/verify_pems_canonical.py
run level_rule python3 scripts/level_rule.py --check
run mc_wording python3 scripts/mc_wording.py --check
run agency_names python3 scripts/agency_names.py --check
run build_outstanding python3 scripts/build_outstanding_decisions.py --check
run internal_artifacts python3 scripts/internal_artifacts.py --check
run mkdocs_strict mkdocs build --strict
run verify_pip_strip python3 scripts/verify_pip_strip.py --base site --archive audit/archive/tables-2026-11-20
run link_sweep python3 scripts/link_sweep.py site
run internal_artifacts_site python3 scripts/internal_artifacts.py --check --site site
run scroller_hrefs python3 scripts/check_scroller_hrefs.py site
run hub_anchors python3 scripts/check_hub_anchors.py site
run bottom_bar python3 scripts/check_bottom_bar.py site

echo "## gate: protocols_untouched"
echo "cmd: git diff --name-only origin/main..HEAD -- docs/protocols/ | wc -l  (must print 0)"
CHANGED=$(git diff --name-only origin/main..HEAD -- docs/protocols/ | tee /tmp/gate_rows_protocols.txt | wc -l)
cat /tmp/gate_rows_protocols.txt
echo "protocol files changed: ${CHANGED}"
if [ "${CHANGED}" -eq 0 ]; then echo "EXIT=0"; else echo "EXIT=1"; FAILED="${FAILED} protocols_untouched=1"; fi
echo
echo "## rows cache after the run"
ls -l audit/level-scan/.cache/pems_rows.jsonl 2>&1 | sed 's/^/  /'
echo
echo "## summary"
if [ -z "$FAILED" ]; then echo "ALL GATES EXIT=0 (17 gates: 16 script gates + protocols_untouched)"; else echo "FAILED:${FAILED}"; fi
} 2>&1 | tee "${LOG}"
