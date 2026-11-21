#!/usr/bin/env bash
# Gate runner for cards t_75b6aba8 (captions are labels) and t_a4b01dd6 (a chip
# may not repeat its row's caption).
#
# Branch caption-labels-r2 is origin/main + the caption work + this card's label
# disambiguation, so the suite runs against origin/main as the base: the diff
# gates below would otherwise count every file the merge brought in.
# `mkdocs build --strict` exits 0 even when a caption is an anchor again (every
# href is valid) and when a chip repeats its caption, so caption_labels and
# caption_label_negative are the only things that see those.
set -uo pipefail
cd "$(dirname "$0")/../.."
BRANCH=$(git rev-parse --abbrev-ref HEAD)
SHA=$(git rev-parse --short HEAD)
LOG="audit/gates/caption-labels-${SHA}.log"
export PATH=/root/pfd-ssg-env/bin:$PATH
mkdir -p audit/gates
{
echo "# gate log — branch ${BRANCH}, content commit ${SHA}"
echo "# written $(date -u '+%Y-%m-%d %H:%M:%S') UTC by run_gates_caption_labels.sh (cards t_75b6aba8, t_a4b01dd6)"
echo "# base: origin/main $(git rev-parse --short origin/main)"
echo
run() {
  local name="$1"; shift
  echo "## gate: ${name}"
  echo "cmd: $*"
  "$@" > /tmp/cap_labels_gate_out.txt 2>&1
  local rc=$?
  tail -n 30 /tmp/cap_labels_gate_out.txt
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
run caption_labels python3 scripts/check_caption_labels.py site
run caption_label_negative python3 audit/gates/caption_label_negative.py site
run hub_anchors python3 scripts/check_hub_anchors.py site
run bottom_bar python3 scripts/check_bottom_bar.py site

echo "## gate: caption_anchor_crosscheck"
echo "cmd: python3 audit/gates/caption_anchor_count.py site/index.html  (independent regex, not the guard's parser)"
python3 audit/gates/caption_anchor_count.py site/index.html > /tmp/cap_labels_cross.txt 2>&1
RC=$?
tail -n 8 /tmp/cap_labels_cross.txt
echo "EXIT=${RC}"
[ "$RC" -ne 0 ] && FAILED="${FAILED} caption_anchor_crosscheck=${RC}"
echo

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
CHANGED=$(git diff --name-only origin/main..HEAD -- docs/protocols/ | tee /tmp/cap_labels_protocols.txt | wc -l)
cat /tmp/cap_labels_protocols.txt
echo "protocol files changed: ${CHANGED}"
if [ "${CHANGED}" -eq 0 ]; then echo "EXIT=0"; else echo "EXIT=1"; FAILED="${FAILED} protocols_untouched=1"; fi
echo

echo "## gate: slate_untouched"
echo "cmd: git diff origin/main..HEAD -- docs/stylesheets/extra.css | grep -E '^[+-].*\\[data-md-color-scheme=\"slate\"\\]'  (no slate-selector line may change)"
echo "     permitted: the neutral .pfd-chip--all accent, which is a slate-scheme value by design (card t_a4b01dd6)"
git diff origin/main..HEAD -- docs/stylesheets/extra.css | grep -E '^[+-].*\[data-md-color-scheme="slate"\]' | tee /tmp/cap_labels_slate.txt
SLATE_TOTAL=$(grep -c . /tmp/cap_labels_slate.txt || true)
SLATE_ALLOWED=$(grep -cE 'a\.pfd-chip--all \{ --pfd-accent:' /tmp/cap_labels_slate.txt || true)
SLATE=$(( SLATE_TOTAL - SLATE_ALLOWED ))
echo "changed slate-selector lines: ${SLATE_TOTAL} (${SLATE_ALLOWED} permitted pfd-chip--all, ${SLATE} unexpected)"
if [ "${SLATE}" -eq 0 ]; then echo "EXIT=0"; else echo "EXIT=1"; FAILED="${FAILED} slate_untouched=${SLATE}"; fi
echo

echo "## gate: only_expected_files"
echo "cmd: git diff --name-only origin/main..HEAD  (captions + css + generator + guards only)"
git diff --name-only origin/main..HEAD | tee /tmp/cap_labels_files.txt
EXTRA=$(grep -vE '^(docs/index\.md|docs/stylesheets/extra\.css|scripts/gen_resource_pages\.py|scripts/check_caption_labels\.py|audit/gates/.*)$' /tmp/cap_labels_files.txt | wc -l)
echo "unexpected files changed: ${EXTRA}"
if [ "${EXTRA}" -eq 0 ]; then echo "EXIT=0"; else echo "EXIT=1"; FAILED="${FAILED} only_expected_files=1"; fi
echo

echo "## summary"
if [ -z "$FAILED" ]; then echo "ALL GATES EXIT=0"; else echo "FAILED:${FAILED}"; fi
} 2>&1 | tee "${LOG}"
