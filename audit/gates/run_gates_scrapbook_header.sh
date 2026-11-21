#!/usr/bin/env bash
# Gate runner for card t_515ccda5 — homepage "FD SCRAPbook — Coming Soon… Hopefully"
# placeholder block. Every EXIT= in the log is the subprocess's real return code,
# never typed by hand.
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=scrapbook-header
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/${BRANCH}-${SHA}.log"
MKDOCS=/root/pfd-ssg-env/bin/mkdocs
OUT=$(mktemp /dev/shm/gate_out_scrap.XXXXXX)
{
echo "# gate log — homepage FD SCRAPbook placeholder (card t_515ccda5)"
echo "# commit ${SHA} on branch $(git rev-parse --abbrev-ref HEAD)"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_scrapbook_header.sh"
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
run gen_resource_pages_check /root/pfd-ssg-env/bin/python scripts/gen_resource_pages.py --check
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
if [ -z "$FAILED" ]; then echo "ALL GATES EXIT=0 (11 of 11)"; else echo "FAILED:${FAILED}"; fi
} 2>&1 | tee "${LOG}"
rm -f "$OUT"
grep -q "ALL GATES EXIT=0" "${LOG}"
