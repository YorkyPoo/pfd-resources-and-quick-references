# Verifier invariants — what the 6 failures actually were (2026-11-16)

`scripts/verify_pems_canonical.py` failed with 6 invariants after the conversion
(2026-11-15 21:05 run). **None of the six was a real defect in the pages, and none
was fixed by weakening a check.** All six had one root cause: the row reader.

## Root cause

`pems_level_scan.read_page()` recognises exactly one table shape — the legacy
7-column matrix, matched on the header `| EMR | EMT | A | I | P |`:

```python
HDR_RE = re.compile(r"\|\s*EMR\s*\|\s*EMT\s*\|\s*A\s*\|\s*I\s*\|\s*P\s*\|")
...
if len(c) != n or len(c) < 7:
    continue          # every collapsed row is skipped
```

`scripts/level_rule.py` rewrites a level table to
`| # | Level | Action / Intervention |` with one chip per action. On a converted
page `read_page()` therefore returns **zero rows**, and two consumers read that
as *fact* rather than as *"the parser did not look"*:

| consumer | what it did with the empty row list |
|---|---|
| `verify_pems_canonical.check_split_map` | `len(hits) != 1` → "row no longer exists … renumbered or merged away" |
| `build_c2_scope.site_cells_for` | raise `has_table` → `recheck_ambiguous_badges` caught the `SystemExit`, dropped the row, and reported **at_risk = 0** |

So a parse gap was published as (a) two deleted rows and (b) a clean
zero-at-risk result. The second is the dangerous one: "0 at risk" is exactly the
answer a user wants to see, so it would never have been questioned.

## Fix (one reader, both formats)

`pems_level_scan.read_action_rows(path)` returns the action rows of a page in
either format, with the five EMR/EMT/A/I/P cells a legacy row would carry:

* legacy matrix → the row's own five cells, unchanged;
* collapsed table → the row's single chip expanded cumulatively (a chip at `X`
  grants `X` and every level above, which is the same statement as filling `X`
  and the columns to its right). `MC` → MC in every column. `PENDING` → five
  blank cells, because a pending action authorises no level at all.

Per the owner's instruction the split entries were **rebound, not deleted**, and
the join key is the conversion ledger (`audit/level-scan/level-rule-ledger.json`):
`c2.split_map` now also fails when a named row's chip differs from the
`level_published` the ledger records for that `(file, row)`.

## The six invariants, before → after

| # | invariant | before | after | why |
|---|---|---|---|---|
| 1 | `c2.split_map` chest-pain-acs-r13 | FAIL: r13 no longer exists | ok: r13 → EMR/EMT/A/I/P, chip `MC` = p.107 #9 badge `MC` | r13 **does** exist (`04_Chest_Pain_ACS_PROC.md` line 51, chip `MC`) |
| 2 | `c2.split_map` stroke-tia-r6 | FAIL: r6 no longer exists | ok: r6 → EMT/A/I/P = p.131 #4 badge `EMT` | r6 **does** exist (chip `EMT`) |
| 3 | `c2.recheck` at_risk derived count | 2 listed, **0** derived | 2 listed, **2** derived | the re-check dropped both rows on the parse error |
| 4 | `c2.recheck` count vs list length | mismatch | 2 == 2 | same |
| 5 | at-risk names `04_Cardiac_Arrest_Non_Traumatic` r5 | absent | named (p.63 #7, flips to `EMR` narrower / `I` broader) | row publishes `EMT`; p.63#7 is badge `I` printing `[EMR]` |
| 6 | at-risk names `04_Cardiac_Arrest_Traumatic` r5 | absent | named (p.61 #4, flips to `EMT` narrower / `I` broader) | row publishes `A`; p.61#4 is badge `EMT` printing `(I / P)` |

**The recorded `c2-scope.json` at_risk list was correct and was not edited.** Once
the rows could be read, the re-derived list is byte-identical to the one already
in the file — same two rows, same `flips_if_badge`, same `directions`. Nothing was
relaxed to make the numbers agree; the artifact was right and the reader was blind.

## Standing invariant (unchanged, and now enforced harder)

Both at-risk rows are genuinely at risk today and stay on the list while
p.61#4 / p.63#7 remain unresolved (`badge-overrides.yaml` is empty — the rasters
have not been run). The moment an override settles a badge, the check requires
the row to leave the list *and* requires the row's direction to be re-derived
from the resolution. A zero-length at-risk list is only ever accepted when it is
*derived*, never when a reader failed.

## Known consequence — `build_c2_scope.py --verify` was already broken, and is now honest

`scripts/build_c2_scope.py --verify` is NOT the verifier this card is about, but
`c2.recheck` imports it (`site_cells_for`), so it moved with the same fix. Its
state, measured both ways:

| tree | `build_c2_scope.py --verify` |
|---|---|
| base `908f745` | **crash**: `protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md: no EMR\|EMT\|A\|I\|P table` — the same reader gap, uncaught. It has been unable to run since the first pages were converted. |
| this commit | runs, then fails the frozen-histogram assert: `held_level_correct 9 / ownership_adjudication 6` vs the ruling `7 / 8` |

The 2-row shift is the conversion, not a regression: `c2-scope.json` and the
`EXPECTED_DISPOSITIONS` ruling were recorded against the **pre-conversion 5-column
dot matrices**, and 12 of its rows still carry those old cells. Example: SVT r16
was recorded `['', '', '', '', '[P]']` (site_narrower); the converted page
publishes the chip `I`, i.e. `['', '', '', '•', '•']`. Stroke r9 moved
`site_narrower` → `site_gap` because its chip is now `PENDING`, which authorises
no level — the honest new reading.

**`c2-scope.json` was deliberately NOT regenerated.** Regenerating it would rewrite
the artifact the verifier's `c2.recheck` compares against, and re-deriving the
disposition ruling is a decision for the owner, not a side effect of a verifier
fix. Queued as follow-up work: rebuild the C2 scope artifact against the converted
tree and have the owner re-ratify the disposition histogram.

## Round 2 — the badge-bleed tolerance is now a named exception list, not a count

Review round 1 blocked on `verify_pems_canonical.py`'s bleed check, which read
`check(len(leaks) <= 2, ...)` — a bare count that tolerated **any two** leaks,
including a newly introduced one. Provenance first:

```
$ git log --oneline -S "leaks) <=" -- scripts/verify_pems_canonical.py
d21aa3d level-scan: canonical PEMS table (57 pages, per-page decision) + structural aligner
$ git show 908f745:scripts/verify_pems_canonical.py | grep -n "leaks) <="
377:    check(len(leaks) <= 2, f"badge column does not bleed into row text ({len(leaks)} leaks)")
$ git show 6115f48:... | grep -n "leaks) <="   # same line, 377
$ git show 56705be:... | grep -n "leaks) <="   # same line, 377
```

So the threshold **predates this branch** and was not introduced by the conversion.
The tolerance was still wrong — a count cannot say *which* leak is known — so it is
replaced by an enforced allow-list, which is stricter than the count in both
directions:

| old | new |
|---|---|
| passes with 0, 1 or 2 leaks of any kind | passes only when every leak is named in `verifier-exceptions.yaml` **and** every named entry still leaks |
| a new leak silently rides along under the count | a leak that is not listed fails (`N unexplained`) |
| an entry could rot unnoticed | a listed leak that has stopped leaking fails (`stale exception`) |
| an exception with no reason is expressible | an entry without page/ordinal/reason fails |

The one real leak is **p.81 #3** (Spinal Clearance): the row continues past a page
break and the continuation join glued the margin badge column onto the text
(`PEMS2024_full.txt`: `...Mechanism of Injury (MOI)   EMR   EMR • Patient is Alert…`).
It changes no decision — the row's `badge_tokens` come from the margin column and are
correct, and **no level-rule row cites p.81** — so it is documented, with that
evidence, in `audit/level-scan/verifier-exceptions.yaml` and rendered into
`level-rule-ledger.md` under "Verifier exceptions (known, documented, enforced)".
Fixing it means re-running the PDF layout extractor and re-freezing `pems_table.json`,
which is outside this branch.

Planted-defect proof of the new form (each plant applied, verifier run, files
restored byte-identically, then re-run):

| plant | exit | failing invariant |
|---|---|---|
| exception with `reason: ''` | **1** | `p.81 #3 has no reason` + `1 leak(s), 1 unexplained` |
| a new undocumented leak (synthetic p.81 #4 starting `EMT `) | **1** | `2 leak(s), 1 unexplained` |
| exception naming a row that does not leak (p.82 #0) | **1** | `every documented badge-bleed exception still leaks (no stale exception)` |
| restored tree | **0** | `1 leak(s), 0 unexplained` — `all invariants hold` |


