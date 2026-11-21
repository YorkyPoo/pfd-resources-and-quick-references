#!/usr/bin/env bash
# Gate runner for card t_f0da5f65 — merge of caption-labels-r2, scrapbook-header,
# pems-table-reconcile, gate-rows-cache and legend-r2 into main.
# Every EXIT= in the log is the subprocess's real return code, never typed by hand.
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=merge-batch-2026-11-21-r2
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/${BRANCH}-${SHA}.log"
MKDOCS=/root/pfd-ssg-env/bin/mkdocs
OUT=$(mktemp /dev/shm/gate_out_batch_r2.XXXXXX)
{
echo "# gate log — merge batch 2 (caption-labels-r2, scrapbook-header, pems-table-reconcile, gate-rows-cache, legend-r2) into main"
echo "# merge commit ${SHA} on branch $(git rev-parse --abbrev-ref HEAD)"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_merge_batch_r2.sh (card t_f0da5f65)"
echo "# base origin/main was 73766d972fef461d0d5d6b722932564843269efe"
echo "# site gates run after the strict build; level-scan cache present (git-ignored, as in the primary checkout)"
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
run gen_resource_pages python3 scripts/gen_resource_pages.py --check
run mc_wording python3 scripts/mc_wording.py --check
run agency_names python3 scripts/agency_names.py --check
run build_outstanding python3 scripts/build_outstanding_decisions.py --check
run internal_artifacts python3 scripts/internal_artifacts.py --check
run mkdocs_strict "$MKDOCS" build --strict
# site gates — everything below reads the build mkdocs_strict just produced.
# caption_labels is one of them: pointed at a stale site/ it reports the previous
# build's captions and looks red (seen on the first run of this card).
run caption_labels python3 scripts/check_caption_labels.py site
run verify_pip_strip python3 scripts/verify_pip_strip.py --base site --archive audit/archive/tables-2026-11-20
run link_sweep python3 scripts/link_sweep.py site
run internal_artifacts_site python3 scripts/internal_artifacts.py --check --site site
run scroller_hrefs python3 scripts/check_scroller_hrefs.py site
run hub_anchors python3 scripts/check_hub_anchors.py site
run bottom_bar python3 scripts/check_bottom_bar.py site
echo "## summary"
if [ -z "$FAILED" ]; then echo "ALL GATES EXIT=0 (16 of 16)"; else echo "FAILED:${FAILED}"; fi
} 2>&1 | tee "${LOG}"
rm -f "$OUT"
grep -q "ALL GATES EXIT=0" "${LOG}"
