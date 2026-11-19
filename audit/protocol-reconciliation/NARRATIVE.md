### 8.1 Sample-of-10 hand verification (result first)

Method: the 10 items come from `random.Random(20261114)` over all cell-level literal discrepancies (section 6 lists them with raw lines). For each one I re-read the source line with `awk -F'|'` on the raw file (independent of the parser), checked the row number, the column for the stated level (fields [3]=EMR, [4]=EMT, [5]=A, [6]=I, [7]=P), and confirmed the intervention text matches once links and bold markers are stripped.

**Result: 10 of 10 agree with the automated classification.** Nine are `site_narrower` (site blank, vault `•`) and one is `bracket_shape` (site `[I]`, vault `MC`, both "must call MC"). Two of the ten are administrative rows (items 1 and 9), so they are not level-gated and are reported, not ranked. No disagreements were found.

### 8.2 Corrections to the brief

1. **The row-6 mechanism is wrong.** Before 16c0627 the site's ALS row 6 (BLS Documentation) had all five level cells blank (`git show 16c0627^`). The inheritance script only copies a mark that already exists below, so it could not have produced any mark there. The five `•` came from commit 3fed1a8 (2026-11-13), a hand application of the 2026-11-11 admin ruling to that one row. Under the cumulative rule the vault's EMT-only `•` already means EMT, A, I and P, so the only real row-6 difference is EMR: the site grants EMR and the vault does not.
2. **"The vault never got the upward fill" is largely false.** The vault writes the cumulative chain explicitly almost everywhere: only **8** of its blank cells rely on inference (ALS row 6 A/I/P; Respiratory Distress row 7 A/I; Bradycardia rows 3, 5, 6 P). The site had 0 such cells after the script. So the script moved the site toward the vault's own convention. It also reduced literal cell drift from 799 to 367 (section 3), without changing what any level may do.
3. **The `[P]` vs `•` "bracket_shape" example does not occur in the data.** No `[X]`-against-`•` pair exists. Under the owner rules, `[X]` against `•` is a narrowing, not a notation difference, and the classifier treats it that way.
4. **"Administrative rows are not level-gated" has not been applied.** The site still gates 88 administrative cells (blank EMR/EMT/A/I/P where the vault grants `•`). Only ALS row 6 was changed, by 3fed1a8.
5. **The 424 / 493 figures are not reused and not comparable.** This audit compares 474 rows that share the same number and identical intervention text, and reports 468 of them with at least one cell difference.
6. **The "65 files" count is docs-wide.** The replay of the script reproduces 699 fills in 65 files, which matches the commit message. That count includes non-protocol files (the 16c0627 numstat lists 57 changed files under `docs/protocols`, front matter included). The audit universe is 54 paired protocol files, plus 1 site-only file (below).
7. **Unpaired files, stated explicitly.** One site-only file has a matrix and no vault counterpart: `cardiac/04b_Aortic_Dissection_AAA_PROC.md`. Thirty-three vault-only files are 32 pharmacology pages (`08_*`) and the master tracker; none of the pharmacology basenames exist under the site's `docs/`.

### 8.3 Which copy looks correct? Mixed evidence, no winner declared

Evidence for the **site**:
- Its How-to-Read legend (HEAD) encodes the owner rules: cumulative by level, MC not implied, blanks meaningful only absent a lower grant. The vault's legend (4cdd60c, edited today) has neither rule and still says a blank means "NOT within your scope".
- The vault is behind the owner's rulings. Its matrices are unchanged since its 2026-10-13 snapshot. It has none of the 19 bracket rulings (3eca400, 2026-11-13), none of the admin ruling (3fed1a8, 2026-11-11), and none of the MC-inheritance reversal (39c7da8, 2026-11-05).

Evidence for the **vault**:
- The site's 372 clinical cells where the vault grants more are not produced by the inheritance script. The site's initial commit (fbc666c, 2026-04-28) already had the gaps (ALS row 1 I-only, against the vault's A/I/P), so the gaps were in the site's original build.
- Administrative rows: the 2026-11-11 ruling says they apply to all levels. The site's 88 blank administrative EMR/EMT/A/I/P cells contradict that ruling; the vault's `•` cells agree with it. This favours the vault on those rows.
- The script cannot have caused the EMR gaps: EMR is never a destination in `fix_scope_inheritance.py`, so every EMR cell the site blanks was blank before 16c0627.
- One independent source checked: PEMS 2024 (regional, `/root/.hermes/cache/scratch/pems2024.txt`, lines 1416–1450, "Universal Patient Care"). It grants EMR on "Follow Universal Patient Care" and on the scene-safety, assessment and airway steps. The vault shows EMR `•` on the Asystole row 1 that carries that step; the site leaves EMR blank. One page is a small sample, not a verdict on all 372 cells.
- CPAP (`docs/procedures/CPAP.md`, a site-repo document): steps 1–5 are standing for EMT and above, and step 6 (PEEP titration) is standing for P only. For Respiratory Distress row 6, the vault's P `•` agrees with that procedure; the site's blank P does not. Both copies have A = MC on that row, which the procedure does not require. That is a source conflict for OMD.

Where the **site is ahead** is the owner's documented semantics. Where the **vault is ahead** is the level grants that the site lost or never had. Neither copy can be adopted wholesale.

### 8.4 The most safety-relevant items (site broader than vault)

There are 15 clinical cells where the site grants standing and the vault requires MC. Fourteen are P and I cells on rows where the site now carries a bracket with standing above it, which is the pattern 3eca400 produced from MC runs (the bracket rule carries "levels above act standing" over to I and P). One is EMR on the Cold Exposure row 8 ("Rapid transport…"). Five of the affected rows have step text that is itself an MC contact: Bradycardia row 8, Chest Pain row 13, SVT row 10, Airway Inhalation Irritants row 12, Smoke Inhalation row 12. For those, the site now tells an I or P provider they may act on a step that is an MC instruction. The commit message says all-MC rows were left alone, which is true, but these mixed rows encode a reading the owner has not confirmed.

Commit 39c7da8 (2026-11-05) argued the opposite for the three Respiratory Distress MC runs: "MC never inherited". The site's own history therefore contradicts itself on whether a plain MC implies standing above it. This is the single most important owner question.

### 8.5 Questions that need owner / OMD judgement (not resolved here)

1. **Bracket conversions (3eca400).** For the 19 rows changed from an MC run to `[X]` plus standing above, should I and P be standing (site) or MC (vault)? Should rows whose text is itself "Contact Medical Control" carry any standing grant above a bracket?
2. **Does a plain MC imply standing above it?** Commit 39c7da8 says no. The vault's Respiratory Distress row 6 (EMT `•`, A `MC`, I `MC`, P `•`) and CPAP.md say P is standing. The current site has P blank above I `MC` on rows 6, 10 and 11.
3. **Blank above a plain MC.** My model treats such a cell as not authorized. The legend sentence ("a blank cell excludes a tier only when no lower tier is authorized") is ambiguous on this case. Please confirm; it decides the three site cells above.
4. **Administrative ruling scope.** Does the 2026-11-11 "not level-gated" ruling apply to every administrative row? If so, 88 site cells change and the vault's ALS row 6 (EMT only) needs the same treatment. The site's EMR on row 6 is already ruled.
5. **The 372 clinical "vault grants more" cells.** Are the vault's EMR/EMT/A/I/P grants intended? The PEMS 2024 pages are the natural tiebreaker. A check across the affected steps is needed before any cell changes.
6. **Internal conflicts (legend: "route to OMD").** A lower `•` sits under an explicit MC/[X]: site 3 rows (Cardiac Arrest Non-Traumatic rows 9, 11, 13: P), vault 5 rows (Respiratory Distress row 6; Upper Airway Obstruction row 12; Cardiac Arrest Non-Traumatic rows 9, 11, 13). Which cell wins?
7. **Malformed vault rows.** `03 - Respiratory/03_Pediatric_Stridor_PROC.md` rows 6–11 have one level cell too many (8 cells against a 7-column header). The levels cannot be read without guessing. Which levels are intended for CPAP, Albuterol, Steroids, IV/IO, Nebulized Epinephrine and Advanced Airway? For comparison, the site has `•` at P for rows 6–9, all blank for row 10, and `[P]` at P for row 11 (the vault has MC at I and `•` at P on row 11).
8. **Intervention with no level at all on the site.** Bradycardia row 3 (Atropine): site all blank, vault I `•`. Bradycardia rows 5 and 6 (MAP / SBP pressor steps): site all blank, vault I `•`. Which levels may do these?
9. **Text differences (21 rows, section 7).** Which wording is authoritative? One example is ALS row 8 (QA/QI reviewer: "Officer or Acting Officer, per departmental SOP" on the site, "agency QA/QI process" in the vault). Those rows are excluded from the level counts, but the wording itself needs a decision.
10. **Row 9 "Incident Reporting" (ALS Release to BLS).** It exists in the vault and is absent from the site. Add to the site? Its level cells are A/I/P `•`.
11. **Vault parity.** Should the vault adopt the 19 bracket rulings (3eca400) and the admin ruling (3fed1a8)? As it stands, the two copies disagree on those rules, not just on levels.
12. **Aortic Dissection (`04b`).** It has a matrix on the site and no vault counterpart. Should it be in the vault?

### 8.6 Reproduce, and what changed on disk

- `python3 audit/protocol-reconciliation/reconcile.py` regenerates every file here from the two corpora. It reads the site working tree, the vault folder, and git history via `git show` (read-only). It writes only into `audit/protocol-reconciliation/`.
- Files: `reconcile.py`, `RECONCILIATION_REPORT.md`, `drift.json` (every row with a discrepancy, plus missing / unparseable / text-differs rows, each with the source line numbers and raw lines), `summary.json`, `sample10.json`, `top20.json`, `internal_conflicts.json`, `provenance.json`.
- Site repo: `git status` shows only the new untracked folder `audit/`. No tracked file changed and no commit was made.
- Vault: `git status` is clean for the EMS folder; no file was written there.
