#!/bin/bash
# evidence.sh — reproducible proof for the findings the reviewer asked to see committed.
# Run from the root of the sedation-p55 worktree, on the deliverable tip.
#   1. the content commit touches no script;
#   2. the pharmacology section is untouched (whole branch, not just one commit);
#   3. level_rule.py --check still bites: a planted wrong chip exits 1, reverting restores 0;
#   4. page inventory;
#   5. the nowhere_expected set edit in 8d3f90d, shown in full.
set -u
OUT="$(dirname "$0")/evidence.txt"
PAGE=docs/protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md
{
  echo "evidence for the p.55 sedation pass"
  echo "tip:    $(git rev-parse HEAD)  ($(git log -1 --format='%s'))"
  echo "date:   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "======"
  echo
  echo "[1] content commit 7815b5e touches no script"
  git diff --quiet ff4fa3b 7815b5e -- scripts/ ; echo "EXIT=$?  (0 = no script change)"
  echo
  echo "[1b] generator commit 8d3f90d: full scripts/ diff (all comment + emitted-string prose)"
  echo "  diffstat:"; git diff --stat 7815b5e 8d3f90d -- scripts/ | sed 's/^/    /'
  echo "  lines that are neither a comment nor a line containing a quote (i.e. code):"
  n=$(git diff 7815b5e 8d3f90d -- scripts/ | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)' \
      | grep -vE '^[+-][[:space:]]*($|#)' | grep -vE "['\"]" | wc -l)
  echo "    count = $n   (0 = every changed line is a comment, blank, or carries a string literal)"
  git diff 7815b5e 8d3f90d -- scripts/ | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)' \
      | grep -vE '^[+-][[:space:]]*($|#)' | grep -vE "['\"]" | sed 's/^/    CODE? /'
  echo "  full diff follows:"
  git diff 7815b5e 8d3f90d -- scripts/ | sed 's/^/    /'
  echo
  echo "[2] pharmacology section untouched, base ff4fa3b -> tip"
  git diff --quiet ff4fa3b 8d3f90d -- docs/pharmacology/ ; echo "EXIT_8d3f90d=$?  (0 = untouched)"
  git diff --quiet ff4fa3b HEAD -- docs/pharmacology/ ;      echo "EXIT_tip=$?      (0 = untouched)"
  git diff --stat ff4fa3b HEAD -- docs/pharmacology/ | sed 's/^/  /'
  echo "  docs/pharmacology/Ketamine.md sha256 at tip: $(sha256sum docs/pharmacology/Ketamine.md | cut -d' ' -f1)"
  echo "  docs/pharmacology/Ketamine.md sha256 at base ff4fa3b: $(git show ff4fa3b:docs/pharmacology/Ketamine.md | sha256sum | cut -d' ' -f1)"
  echo
  echo "[3] planted-defect test: level_rule.py --check still bites on a wrong chip"
  echo "  file:   $PAGE"
  echo "  blob sha256 committed: $(git show HEAD:$PAGE | sha256sum | cut -d' ' -f1)"
  echo "  worktree sha256 before: $(sha256sum $PAGE | cut -d' ' -f1)"
  git diff --quiet HEAD -- "$PAGE" ; echo "  clean before plant: EXIT=$?  (0 = clean)"
  # plant: row 3 chip I -> A in BOTH text and class (the checker reads the chip text)
  sed -i '31s#<span class="lvl lvl-i">I</span>#<span class="lvl lvl-a">A</span>#' "$PAGE"
  echo "  planted row 3 chip I -> A:"
  sed -n '31p' "$PAGE" | cut -c1-80 | sed 's/^/    /'
  python3 scripts/level_rule.py --check > /tmp/planted-check.log 2>&1 ; echo "  level_rule.py --check EXIT=$?  (expect 1)"
  grep -E 'row 3' /tmp/planted-check.log | head -5 | sed 's/^/    /'
  # revert
  git checkout -- "$PAGE"
  python3 scripts/level_rule.py --check > /tmp/planted-revert.log 2>&1 ; echo "  after revert EXIT=$?  (expect 0)"
  echo "  worktree sha256 after revert: $(sha256sum $PAGE | cut -d' ' -f1)"
  git diff --quiet HEAD -- "$PAGE" ; echo "  clean after revert: EXIT=$?  (0 = clean)"
  echo
  echo "[4] page inventory"
  echo "  rows in the protocol table: $(grep -cE '^\| [0-9]+ \| <span class="lvl' "$PAGE")"
  echo "  chips: $(grep -oE 'lvl lvl-[a-z]+' "$PAGE" | sed 's/lvl lvl-//' | tr '\n' ' ')"
  echo "  ketamine occurrences in the page: $(grep -ci ketamine "$PAGE")"
  echo "  OWNER_REQUIRED flags on the page: $(grep -c OWNER_REQUIRED "$PAGE")"
  echo
  echo "[5] nowhere_expected edit in 8d3f90d (build_outstanding_decisions.py)"
  git diff 7815b5e 8d3f90d -- scripts/build_outstanding_decisions.py \
    | sed -n '/nowhere_expected/,/^ *}/p' | sed 's/^/    /'
  echo "  the assertion still compares the set by EQUALITY (nowhere_got == nowhere_expected),"
  echo "  so removing an entry only makes the check stricter for that row: if the row is ever"
  echo "  flagged 'PEMS prints this nowhere' again, the extra member fails the build."
} > "$OUT" 2>&1
cat "$OUT"
