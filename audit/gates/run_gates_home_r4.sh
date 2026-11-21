#!/usr/bin/env bash
# Gate runner for card t_a2f382dd — homepage + naming round 4:
#   Drug Calculator rename (tile + page + nav + Protocols group heading),
#   new Pharmacology quick tile, SOPs scroller dropped, Protocols scroller -> EMS Hub.
#
# Same 16 gates as ia-r3 (the current gate floor for this repo), plus one card gate:
#   naming_sweep   no "Drugs & Drip Rates" / "Medications & Calculators" label survives
#                  in docs/, mkdocs.yml or scripts/ (the owner's own acceptance grep).
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=home-r4
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/${BRANCH}-${SHA}.log"
export PATH=/root/pfd-ssg-env/bin:$PATH
mkdir -p audit/gates
{
echo "# gate log — branch ${BRANCH}, content commit ${SHA}"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_home_r4.sh (card t_a2f382dd)"
echo "# gates run on the content commit ${SHA}; site gates after the strict build"
echo
run() {
  local name="$1"; shift
  echo "## gate: ${name}"
  echo "cmd: $*"
  "$@" > /tmp/home_r4_gate_out.txt 2>&1
  local rc=$?
  tail -n 30 /tmp/home_r4_gate_out.txt
  echo "EXIT=${rc}"
  echo
  if [ "$rc" -ne 0 ]; then FAILED="${FAILED} ${name}=${rc}"; fi
}
FAILED=""
run gen_resource_pages python3 scripts/gen_resource_pages.py --check
run connected_notes python3 scripts/gen_connected_notes.py --check
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
CHANGED=$(git diff --name-only origin/main..HEAD -- docs/protocols/ | tee /tmp/home_r4_protocols.txt | wc -l)
cat /tmp/home_r4_protocols.txt
echo "protocol files changed: ${CHANGED}"
if [ "${CHANGED}" -eq 0 ]; then echo "EXIT=0"; else echo "EXIT=1"; FAILED="${FAILED} protocols_untouched=1"; fi
echo
echo "## summary"
if [ -z "$FAILED" ]; then echo "ALL GATES EXIT=0 (18 of 18)"; else echo "FAILED:${FAILED}"; fi
} 2>&1 | tee "${LOG}"
