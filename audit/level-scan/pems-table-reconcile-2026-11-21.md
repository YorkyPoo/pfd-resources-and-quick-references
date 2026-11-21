# pems_table.json reconciliation — 2026-11-21

Re-froze `audit/level-scan/pems_table.json` against `origin/main` (`420d1f74`,
which contains the how-to pip-strip rewrite) and made
`scripts/verify_pems_canonical.py` check the table against the tree instead of
against itself.

Base: `origin/main` @ `420d1f74`. The audit that found the drift ran on
`ia-r3` @ `fbe71bc7`; its "widen `SITE_HDR_RE` to `R|B|A|I|P`" step does **not**
apply here — see §2.

## 1. Table

`python3 scripts/pems_canonical.py --stage all` on `420d1f74`:

| | committed | re-frozen |
|---|---|---|
| `counts.site_pages_with_level_table` | 57 | **56** |
| `counts.administrative` | 15 | **14** |
| `counts.level_gated` | 41 | 41 |
| `counts.skipped` | 1 | 1 |
| `len(page_decisions)` | 57 | **56** |
| level-gated decisions unchanged | — | 41/41, no decision flipped |

**One decision removed:** `protocols/front-matter/01 - How to Read the Protocols.md`.
On `420d1f74` the page explains the pip strip in prose and carries **no table at
all** (verified: zero markdown tables in the file; `C.site_pages()` does not
return it; the structural detector in the new gate does not see it either). It
was the only administrative page that no longer has a grid, so it correctly
leaves `page_decisions` — it is explanatory front matter, which is the
conclusion `level_rule` reached in t_15798568. Nothing replaced it: there are
**no pages in the tree without a decision**.

**17 pages re-counted** (derived fields only: `rows`, `numbered_rows`,
`filled_level_cells`, `blank_level_cells`, and the `contested_because` sentence
that quotes the two cell counts). No `decision`, `ruling`, `pems_pages` or
`source_declared` value changed on any of them.

Actual published row counts, checked against the pages themselves:

* `protocols/respiratory/03_Pneumothorax_PROC.md` — table said **15**, page has
  **20** numbered rows (`1 2 3 4 4a 4b 6 7 8 9 10 11 12 12a 13 13a 13b 14 15 15a`).
  The five extra rows are the `row_splits.yaml` fused-row splits.
* `protocols/general/02_Cold_Exposure_PROC.md` — table said **9**, page has
  **7** (`1 2 3 4 5 7 8`; row 6 was deleted from the grid).
* Remaining 15 drift pages: Asystole/PEA 12→14, Cardiac Arrest Non-Traumatic
  14→16, Cardiac Arrest Traumatic 11→12, V-Fib/pVT 12→13, Sedation 6→7,
  Airway Inhalation 12→13, Asthma/COPD 11→13, Pulmonary Edema 13→10,
  Respiratory Distress 16→20, Smoke Inhalation 14→16, Upper Airway 14→13,
  Electrical 9→10, Lightning 9→10, Behavioral Health Transport 7→5,
  Stroke Field Triage 8→7.

No published level changed: the re-freeze records what the pages already say.

The only other structural change is the removal of the
`exception_path_repaired` marker that the frozen table carried on the
Pneumothorax record: with the declaration repointed (§2) there is nothing left
to repair. Every other record's field set is identical to the committed table —
no field was added, dropped or renamed anywhere else.

## 2. `exceptions.yaml`

`protocols/trauma/09_Pneumothorax_PROC.md` (a path that no longer exists) is
repointed to `protocols/respiratory/03_Pneumothorax_PROC.md`, keeping
`pems_pages: [243]`. Repointed rather than deleted because the entry declares a
*forced source*: the needle/finger thoracostomy content lives in the Chest
Decompression procedure (p.243), not in a protocol page, and deleting it would
let the page fall back to title matching. The generator already repaired this
declaration internally by basename; with the path fixed, `stale_exception_paths`
is now `[]`.

## 3. Gate: `scripts/verify_pems_canonical.py`

* The `57` literals are gone: the decision count is checked against
  `counts.site_pages_with_level_table` and distinctness against `len(dec)`.
* New manifest section **`stage1.tree_walk`** (7 checks) re-derives from
  `docs/` and fails on:
  * a decision for a page that no longer carries a level table (and on a page
    with a level table that carries no decision),
  * a decision whose path does not exist under `docs/`,
  * any row count (`rows`, `numbered_rows`, `filled_level_cells`,
    `blank_level_cells`) or `decision` that does not re-derive from a fresh
    parse of the published page.
  It also cross-checks the decision count against a **structural header
  detector**
  (`#` index column + `Level`/`Basis`/`POLICY` or all of `R B A I P`) that does
  not use `SITE_HDR_RE`, so a header relabel cannot silently drop a page from
  both the generator and the gate.

Proven to bite (defect planted in a copy of the table, never the repo file):

```
baseline                -> RESULT: PASS (7/7 ok)
drop one decision       -> FAIL every page under docs/ with a level table
                              carries a decision (1 missing):
                              protocols/respiratory/03_Pneumothorax_PROC.md
insert a dead path      -> FAIL every decided path exists under docs/
                              (missing: protocols/trauma/09_Pneumothorax_PROC.md)
bump Cold Exposure rows -> FAIL every row count and decision re-derives
                              (drift: ... rows: table 8 != tree 7)
real table restored     -> RESULT: PASS (7/7 ok)
```

Against the **old committed table** the same section is red exactly as it should
be: 1 stale decision (the how-to page), 57 vs 56 from the fresh walk, and 68
field drifts over the 17 pages.

## 4. Downstream consumers

`--stage all` regenerated `alignment.json` (site rows 417→434, matched 292→298,
ambiguous 125→136, absent 86→83 — the extra site rows are the `row_splits.yaml`
rows, which are in the tree but were not in the frozen alignment),
`reconciliation.json`, `text-binding.md`, `missing-rows.md` and
`ambiguous-rows.md`.

Split row labels (`4a`, `5a`, …) crashed three consumers that assumed numeric
labels; all now use a `row_key()` helper (int for numeric labels, str for split
labels):

* `scripts/recheck_ambiguous_badges.py` — `int(site_row)` crash
* `scripts/build_c2_scope.py` — `int(site_row)` and `ambiguous-rows.md` parser
  that only matched `\d+` labels (it parsed 117 of 136 rows)
* `scripts/build_split_map.py` — `int(site_row)`

## 5. Still red (not reconciliation, and not fixed here)

`verify_pems_canonical.py` exits 1 on four downstream invariants. All four come
from the **adjudicated C2 queue being older than the pages**, not from the
table:

```
FAIL at_risk_matched_rows equals the recheck script's output (2 listed, 2 derived)
FAIL at-risk list names 04_Cardiac_Arrest_Non_Traumatic_PROC.md r5
FAIL at-risk list names 04_Cardiac_Arrest_Traumatic_PROC.md r5
FAIL every recorded human review still maps to a pairing (1 stale)
```

* `audit/level-scan/c2-scope.json` is a 61-row queue whose decisions live in
  `adjudicated.json`. Re-running `build_c2_scope.py --write` today yields 59
  rows and a different disposition histogram, because (a) the cardiac-arrest
  rows that were adjudicated as row 5 are now published as rows 5/5a and (b)
  the queue's own ruling constant pins the 61-row histogram. Regenerating it
  re-opens adjudicated work — an owner decision, deliberately not taken here.
  The two at-risk rows are the same pairings under their new split labels; the
  Non-Traumatic one now flips `site_broader` (EMR row 5a vs p.63 #7) instead of
  `site_narrower`, which is a real finding for the owner.
* The stale human review is `('protocols/trauma/09_Trauma_PROC.md', p.83, #3)`:
  "Assess for shock" was moved out of the intervention grid into prose on that
  page, so the reviewed pairing no longer exists. Owner-facing finding, not a
  table defect.

No `docs/` file is modified by this change (`docs_clean` check is green).
