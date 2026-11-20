#!/bin/bash
# evidence.sh — reproducible proof for the findings the reviewer asked to see committed.
# Run from the sedation-p55 worktree AFTER the code/docs commit and BEFORE the evidence
# commit: HEAD is then the code commit whose diff this transcript describes.
set -u
OUT="$(dirname "$0")/evidence.txt"
PAGE=docs/protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md
{
  echo "evidence for the p.55 sedation pass"
  echo "tip:    $(git rev-parse HEAD)  ($(git log -1 --format='%s'))"
  echo "date:   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "======(this transcript is committed in the NEXT commit, which touches only"
  echo "      audit/level-scan/logs/sedation-p55/; HEAD above is the code commit)"
  echo
  echo "[1] content commit 7815b5e touches no script"
  git diff --quiet ff4fa3b 7815b5e -- scripts/ ; echo "EXIT=$?  (0 = no script change)"
  echo
  echo "[1b] generator changes since the content commit: 7815b5e..HEAD -- scripts/"
  echo "  diffstat:"; git diff --stat 7815b5e HEAD -- scripts/ | sed 's/^/    /'
  echo "  LOGIC CHANGES IN THIS DIFF: exactly one — the nowhere_expected set loses the two"
  echo "  Sedation tuples (r4, r5). That is a logic change, not prose: both rows were"
  echo "  deleted from the page, so they cannot be flagged any more and the set-equality"
  echo "  assertion would fail with them still listed. Membership is still asserted by"
  echo "  EQUALITY (nowhere_got == nowhere_expected), so the check is not relaxed. Every"
  echo "  other changed line is a comment or a string emitted into the ledger markdown."
  echo "  Lines with neither a comment nor a quote (a heuristic, NOT proof of prose-only):"
  n=$(git diff 7815b5e HEAD -- scripts/ | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)' \
      | grep -vE '^[+-][[:space:]]*($|#)' | grep -v "['\"]" | wc -l)
  echo "    count = $n"
  echo "  full diff follows:"
  git diff 7815b5e HEAD -- scripts/ | sed 's/^/    /'
  echo
  echo "[2] pharmacology untouched"
  git diff --quiet ff4fa3b HEAD -- docs/pharmacology/ ; echo "EXIT_branch=$?  (0 = untouched)"
  echo "  Ketamine.md sha256 tip:  $(sha256sum docs/pharmacology/Ketamine.md | cut -d' ' -f1)"
  echo "  Ketamine.md sha256 base: $(git show ff4fa3b:docs/pharmacology/Ketamine.md | sha256sum | cut -d' ' -f1)"
  echo
  echo "[3] planted defect: level_rule.py --check still bites"
  git diff --quiet HEAD -- "$PAGE" ; echo "  clean before plant: EXIT=$?"
  sha_before=$(sha256sum "$PAGE" | cut -d' ' -f1)
  sed -i '31s#<span class="lvl lvl-i">I</span>#<span class="lvl lvl-a">A</span>#' "$PAGE"
  python3 scripts/level_rule.py --check > /tmp/planted-check.log 2>&1 ; echo "  planted chip I->A: level_rule --check EXIT=$?  (expect 1)"
  grep -m2 'row 3' /tmp/planted-check.log | sed 's/^/    /'
  git checkout -- "$PAGE"
  python3 scripts/level_rule.py --check > /tmp/planted-revert.log 2>&1 ; echo "  after revert: EXIT=$?  (expect 0)"
  echo "  page sha256 before=$sha_before after=$(sha256sum "$PAGE" | cut -d' ' -f1)"
  git diff --quiet HEAD -- "$PAGE" ; echo "  clean after revert: EXIT=$?"
  echo
  echo "[4] page inventory"
  echo "  rows in the protocol table: $(grep -cE '^\| [0-9]+ \| <span class="lvl' "$PAGE")"
  echo "  chips: $(grep -oE 'lvl lvl-[a-z]+' "$PAGE" | sed 's/lvl lvl-//' | tr '\n' ' ')"
  echo "  ketamine occurrences in the page: $(grep -ci ketamine "$PAGE")"
  echo "  OWNER_REQUIRED flags on the page: $(grep -c OWNER_REQUIRED "$PAGE")"
  echo
  echo "[5] nowhere_expected set diff (build_outstanding_decisions.py)"
  git diff ff4fa3b HEAD -- scripts/build_outstanding_decisions.py \
    | sed -n '/nowhere_expected/,/^ *}/p' | sed 's/^/    /'
  echo "  Trauma r6 carries its base label (not re-categorised):"
  grep -n "09_Trauma_PROC.md', 6" scripts/build_outstanding_decisions.py | sed 's/^/    /'
  echo
  echo "[6] adjudicated.json reverted to base (no C2 record retired in this branch)"
  git diff --quiet ff4fa3b HEAD -- audit/level-scan/adjudicated.json ; echo "  EXIT=$?  (0 = byte-identical to base)"
  echo "  sha256 tip:  $(sha256sum audit/level-scan/adjudicated.json | cut -d' ' -f1)"
  echo "  sha256 base: $(git show ff4fa3b:audit/level-scan/adjudicated.json | sha256sum | cut -d' ' -f1)"
  echo "  NOTE: the two base records for Sedation rows 5 and 6 now describe rows the page no"
  echo "  longer publishes. They are left verbatim rather than retired without owner sign-off;"
  echo "  a C2 regeneration will replace them."
  echo
  echo "[7] relocated-rows.yaml carries no Trauma or Sedation entry"
  if grep -qE 'Trauma|Sedation' audit/level-scan/relocated-rows.yaml; then
    echo "  UNEXPECTED: matches found"; grep -nE 'Trauma|Sedation' audit/level-scan/relocated-rows.yaml
  else
    echo "  no matches — and the ledger narrative no longer cites this file for those rows"
  fi
  echo "  ledger narrative mentions relocated-rows.yaml: $(grep -c 'relocated-rows.yaml' audit/level-scan/level-rule-ledger.md) time(s)"
} > "$OUT" 2>&1
cat "$OUT"
