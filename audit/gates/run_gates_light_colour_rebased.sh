#!/usr/bin/env bash
# Gate runner for card t_ecef0aea — light-colour REBASED onto home-r4 (a869a4c3).
#
# The rebased tip is home-r4's structure + light-colour's classes (+ the offline
# banner commit, which home-r4 predates and which replayed cleanly). So this runs
# the union of the two suites the two parent cards used: home-r4's 18 gates and
# the two extra invocations from the light-colour runner.
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=$(git rev-parse --abbrev-ref HEAD)
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/light-colour-r2-${SHA}.log"
export PATH=/root/pfd-ssg-env/bin:$PATH
mkdir -p audit/gates
{
echo "# gate log — branch ${BRANCH}, content commit ${SHA}"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_light_colour_rebased.sh (card t_ecef0aea)"
echo "# base: home-r4 a869a4c3; rebased light-colour on top; offline banner replayed as 0763113d"
echo
run() {
  local name="$1"; shift
  echo "## gate: ${name}"
  echo "cmd: $*"
  "$@" > /tmp/lc_r2_gate_out.txt 2>&1
  local rc=$?
  tail -n 30 /tmp/lc_r2_gate_out.txt
  echo "EXIT=${rc}"
  echo
  if [ "$rc" -ne 0 ]; then FAILED="${FAILED} ${name}=${rc}"; fi
}
FAILED=""
run gen_resource_pages python3 scripts/gen_resource_pages.py --check
run connected_notes python3 scripts/gen_connected_notes.py --check
run pip_mapper python3 scripts/test_pip_strip_mapper.py
run verify_pems_canonical python3 scripts/verify_pems_canonical.py --check
run verify_pems_canonical_raw python3 scripts/verify_pems_canonical.py
run level_rule python3 scripts/level_rule.py --check
run mc_wording python3 scripts/mc_wording.py --check
run agency_names python3 scripts/agency_names.py --check
run build_outstanding python3 scripts/build_outstanding_decisions.py --check
run internal_artifacts python3 scripts/internal_artifacts.py --check
run internal_artifacts_raw python3 scripts/internal_artifacts.py
run mkdocs_strict mkdocs build --strict
run verify_pip_strip python3 scripts/verify_pip_strip.py --base site --archive audit/archive/tables-2026-11-20
run link_sweep python3 scripts/link_sweep.py site
run internal_artifacts_site python3 scripts/internal_artifacts.py --check --site site
run scroller_hrefs python3 scripts/check_scroller_hrefs.py site
run hub_anchors python3 scripts/check_hub_anchors.py site
run bottom_bar python3 scripts/check_bottom_bar.py site

echo "## gate: naming_sweep"
echo "cmd: grep -ri 'drugs & drip|medications & calculators' docs/ mkdocs.yml scripts/ overrides/"
if grep -ri "drugs & drip\|medications & calculators" docs/ mkdocs.yml scripts/ overrides/; then
  echo "EXIT=1"; FAILED="${FAILED} naming_sweep=1"
else
  echo "(no matches)"; echo "EXIT=0"
fi
echo

echo "## gate: protocols_untouched"
echo "cmd: git diff --name-only origin/main..HEAD -- docs/protocols/ | wc -l  (must print 0)"
CHANGED=$(git diff --name-only origin/main..HEAD -- docs/protocols/ | tee /tmp/lc_r2_protocols.txt | wc -l)
cat /tmp/lc_r2_protocols.txt
echo "protocol files changed: ${CHANGED}"
if [ "${CHANGED}" -eq 0 ]; then echo "EXIT=0"; else echo "EXIT=1"; FAILED="${FAILED} protocols_untouched=1"; fi
echo

echo "## gate: slate_untouched"
echo "cmd: git diff a869a4c3..HEAD -- docs/stylesheets/extra.css | grep -E '^[+-].*\[data-md-color-scheme=\"slate\"\]' | wc -l  (must print 0)"
SLATE=$(git diff a869a4c3..HEAD -- docs/stylesheets/extra.css | grep -E '^[+-].*\[data-md-color-scheme="slate"\]' | wc -l)
echo "changed slate-selector lines: ${SLATE}"
if [ "${SLATE}" -eq 0 ]; then echo "EXIT=0"; else echo "EXIT=1"; FAILED="${FAILED} slate_untouched=1"; fi
echo

echo "## summary"
if [ -z "$FAILED" ]; then echo "ALL GATES EXIT=0"; else echo "FAILED:${FAILED}"; fi
} 2>&1 | tee "${LOG}"
