# Evidence — rebase `rows-one-action` onto `main` (card t_dbfc8107)

**Branch:** `rows-rebased`
**Base:** `main` @ `8132ac3c7dc2a5af421a6055deea8c5a6a3b78aa`
**Content commit the gates ran on:** `acec1ce` (9/9 gates EXIT=0, log
`audit/gates/rows-rebased-acec1ce.log`)
**Tip at handoff:** `8eff9cd` (logs-only commit; no page changed after `acec1ce`)
**Rebased-from:** `rows-one-action` @ `29d5378`, merge base `05addb2`

Method: `git merge --squash rows-one-action` onto `main` in a private worktree, conflicts
resolved by hand (6 files), then the two generated files (ledger, outstanding-decisions)
were **regenerated from their generators** rather than hand-merged.

## 1. Conflicts and how each was resolved

| file | resolution |
|---|---|
| `docs/protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md` | **main wins**: rows 6-8 do not come back; the eight-bullet block stays. Row-splits untouched (this page has no lettered split). |
| `audit/level-scan/relocated-rows.yaml` (add/add) | union: main's 5 pilot records (Pulmonary 6-8, Cold 6/9) + the branch's 4 row-structure records, one schema, `proves` spans re-keyed. |
| `scripts/level_rule.py` | main's flag-counting logic and the lifted-ketamine prose; two duplicated pre-merge definitions (`load_relocated`, `relocated_proofs_missing`, `RELOCATED_YAML`) that the auto-merge left in place were removed. |
| `scripts/build_outstanding_decisions.py` | the "prints nowhere" assertion now expects an empty set (see §5) — it was verified against the built ledger, not typed. |
| `audit/level-scan/level-rule-ledger.md`, `docs/protocols/outstanding-decisions.md` | regenerated: `level_rule.py --write`, `build_outstanding_decisions.py`. |
| `docs/protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md` | not a conflict; touch nothing (see §2). |

## 2. Sedation page untouched

```
$ git diff main..HEAD --stat -- docs/protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md
(no output — 0 lines)
$ git diff main..HEAD --stat -- docs/pharmacology/Ketamine.md
(no output — 0 lines)
```

## 3. Pulmonary Edema render (built `site/`, same tree pushed to the preview slot)

```
== Pulmonary Edema — action table (10 rows in render) ==
  row  1 | EMR          | Follow Universal Patient Care / Initial Patient Contact protocol
  row  2 | EMR          | Perform focused evaluation including assessment of airway and lung sounds
  row  3 | EMR          | Provide supplemental oxygen to maintain SpO2 > 94%
  row  4 | EMT          | Consider non-invasive positive pressure ventilation (CPAP) for severe respiratory distress
  row  5 | EMT          | CPAP Initial Settings: PEEP 5 cmH2O
  row  9 | P [flag]     | CPAP Titration: Adjust PEEP up to 10 cmH2O to support ventilation and work of breathing
  row 10 | A            | Nitroglycerin Adult: 0.4 mg SL
  row 11 | A            | Nitroglycerin Repeat Administration: May repeat every 5 minutes as needed if SBP remains > 100 mmHg / MAP > 65 mmHg (maximum 3 doses)
  row 12 | I            | Furosemide (Lasix) Adult: 40 mg IV/IO slow push
  row 13 | MC           | Contact Medical Control for guidance as needed

rows citing "CPAP CONTRAINDICATIONS": 0
```

References & Good Practice block — 8 bullets, no `<em>`:

```
1. Apnea / agonal respirations
2. Decreased level of consciousness (GCS ≤ 13)
3. Pneumothorax
4. Facial trauma, burns, or recent surgery
5. Penetrating neck/chest trauma
6. Active vomiting / severe nausea
7. Hypotension (SBP < 90 mmHg, MAP < 65)
8. Inability to tolerate a tight-fitting mask

CPAP contraindications apply at EMT: the contraindications gate the CPAP decision, which an EMT may make.
Why and what next: CPAP/BiPAP/PEEP procedure — contraindications and pearls · How to Read the Protocols — level chips, ⚠ cautions and MC
```

Row 9 note on the page (no repository path anywhere on the page — `mc_wording.py` guard):

```
⚑ OWNER_REQUIRED — row 9: PEMS 2024 does not settle which provider level may titrate PEEP.
The level shown is unverified pending a Medical Control decision.
```

(Level stays `P`; the ⚑ marker stays. The first wording used "Medical Director" and the
`agency_names` gate caught it — that is the source of the superseded log
`audit/gates/rows-rebased-7957884.log`, EXIT=1.)

### Row splits kept

```
pages with lettered sub-rows in the rebased tree: 24 sub-row numbers
OK — every lettered sub-row from rows-one-action is present, none extra
```

Ledger: **20 bundled rows → 45 sub-rows**, each part chipped from the PEMS row that
prints that action; 3 parts stay `owner_required` (Asystole 8a, Cardiac Arrest
Non-Traumatic 4a, Asthma 8a) and keep their ⚑. `/preview/rows-rebased/protocols/cardiac/`
carries the same splits.

## 4. Row 9 defect and page-voice sweep

* Row 9's note no longer cites `audit/level-scan/level-rule-ledger.md`.
* Italic self-referential lines: **2 found, 2 rewritten**, 0 left.
  * Pulmonary Edema: *"This page records the list at **EMT**: the contraindications gate
    CPAP, an EMT skill."* → **"CPAP contraindications apply at EMT:** the
    contraindications gate the CPAP decision, which an EMT may make."
  * Cold Exposure: *"This page records the rewarming item at **EMR** (anyone can warm a
    patient) and the AED item at **MC**."* → **"Heat packs and warm blankets are an EMR
    skill** — anyone can warm a patient; **contacting Medical Control before the AED is a
    Medical Control decision.**"
* The stale pointers *"Rows 6–8 are covered under …"* (Pulmonary) and *"Rows 6 and 9 are
  covered under …"* (Cold) were dropped: they point at row numbers that no longer exist.
  `relocated-rows.yaml` `proves` spans were re-keyed to wording that stays on the pages.

### Guard proof (planted defect)

```
$ printf '\n<p class="lv-note">See `audit/level-scan/level-rule-ledger.md` for provenance.</p>\n' >> .../03_Asthma_COPD_Reactive_Airway_PROC.md
$ python3 scripts/mc_wording.py --check
EXIT=1
FAIL — 1 line(s) on reader-facing protocol pages print a repository path or file name.
 - protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md:71: audit/level-scan/level-rule-ledger.md
$ (restore) python3 scripts/mc_wording.py --check
EXIT=0
```

## 5. "Prints nowhere" bucket

`build_outstanding_decisions.py` asserts membership, and it passes with an empty set,
which is the merged truth: the four guidance rows moved below their tables (this branch)
and the two Sedation ketamine rows left the page with the p.55 rewrite (already on main).

## 6. Agency names (Poquoson / OMD)

`agency_names.py --check` **EXIT=0**. The guard's designed exemptions cover what remains:
page H1 / site title, "Poquoson Protocol(s)" cross-references, and the
"Pending OMD authorization" status label.

Measured, so the claim is not "zero": 78 occurrences of `Poquoson|OMD` on the protocol
pages this branch touches, every one of them present on `main` with the same disposition.
Lines **added** by this branch that contain one: 12; lines **removed** by it: 11 — the
added ones are the same sentences rewritten with the `audit/...ledger.md` reference
stripped out, so this branch introduces no new agency name.

## 7. Gates — `audit/gates/rows-rebased-acec1ce.log`

| gate | command | exit |
|---|---|---|
| verify_pems_canonical | `python3 scripts/verify_pems_canonical.py` | 0 |
| level_rule | `python3 scripts/level_rule.py --check` | 0 |
| mc_wording | `python3 scripts/mc_wording.py --check` | 0 |
| agency_names | `python3 scripts/agency_names.py --check` | 0 |
| build_outstanding | `python3 scripts/build_outstanding_decisions.py --check` | 0 |
| internal_artifacts | `python3 scripts/internal_artifacts.py --check` | 0 |
| mkdocs_strict | `/root/pfd-ssg-env/bin/mkdocs build --strict` | 0 |
| link_sweep | `python3 scripts/link_sweep.py site` | 0 |
| internal_artifacts_site | `python3 scripts/internal_artifacts.py --check --site site` | 0 |

## 8. Preview slot

Published to `/preview/rows-rebased/` only (gh-pages `d9d7c85`); `/preview/` root and
every other slot untouched (`git status --porcelain | grep -v 'preview/rows-rebased/'`
was empty before the push).

Live check (`?cb=` cache-buster, after CDN lag cleared):

```
status 200  rows in slot render: 1, 2, 3, 4, 5, 9, 10, 11, 12, 13
table rows naming CPAP CONTRAINDICATIONS: 0
italic "This page" lines: 0
repo path on the page (audit/ scripts/ docs/): 0
references bullets: 8
slot rows            200
slot airway-levels   200
slot sedation        200
slot main            200
```
