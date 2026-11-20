# Evidence — rebase `rows-one-action` onto `main` (card t_dbfc8107, round 2)

**Branch:** `rows-rebased`
**Base:** `main` @ `8132ac3c7dc2a5af421a6055deea8c5a6a3b78aa`
**Content commit the gates ran on:** `4155092`
**Rebased-from:** `rows-one-action` @ `29d5378`, merge base `05addb2`
**Tip at handoff:** see `git log -1 rows-rebased` (this evidence + gate logs are the only
commits after `4155092`; no page changed after it)
**Gate log:** `audit/gates/rows-rebased-4155092.log` — 9 gates, **EXIT=0 each**

Method unchanged from round 1: `git merge --squash rows-one-action` onto `main` in a private
worktree, six conflicts hand-resolved in favour of the merged work, generated files
(ledger, outstanding-decisions) regenerated from their generators rather than hand-merged.

## Round-2 changes (what the review asked for)

| review item | disposition |
|---|---|
| 1. guard must cover `.yaml`, proved with a bare filename | Already covered — `REPO_FILE = re.compile(r'(?<![\w/.-])[\w-]+\.(?:ya?ml\|json\|md)\b')` (`scripts/mc_wording.py:136`). Now **proved** with two planted bare filenames, one `.yaml` and one `.yml` (§4). |
| 2. Endotracheal Intubation missing from the evidence | New §2 below: rows 0 and 11, the PEMS row each cites, the level basis, gate coverage, and the recorded numbering decision. |
| 3. Poquoson/OMD "zero" | Closed by the card author's ruling (comment 12:56). Measured again for this round: **net 0** occurrences added by the branch (§6). |
| 4. row 5→9 gap has no reader-facing explanation | Fixed on Pulmonary Edema **and** Cold Exposure (which had the same unexplained gap 5→7) (§5). |
| 5. Cold Exposure render | Fetched live and quoted (§5). |
| 6. Sedation diff stat re-run at the tip | Re-run; empty (§3). |

## 1. Pulmonary Edema — live render of the published slot

`…/preview/rows-rebased/protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.html?cb=…`
fetched after the slot republish (HTTP 200):

```
row  1 | EMR      | Follow Universal Patient Care / Initial Patient Contact protocol
row  2 | EMR      | Perform focused evaluation including assessment of airway and lung sounds
row  3 | EMR      | Provide supplemental oxygen to maintain SpO2 > 94%
row  4 | EMT      | Consider non-invasive positive pressure ventilation (CPAP) for severe respiratory distress
row  5 | EMT      | CPAP Initial Settings: PEEP 5 cmH2O
row  9 | P ⚑      | CPAP Titration: Adjust PEEP up to 10 cmH2O to support ventilation and work of breathing
row 10 | A        | Nitroglycerin Adult: 0.4 mg SL
row 11 | A        | Nitroglycerin Repeat Administration: May repeat every 5 minutes as needed if SBP remains > 100 mmHg / MAP > 65 mmHg (maximum 3 doses)
row 12 | I        | Furosemide (Lasix) Adult: 40 mg IV/IO slow push
row 13 | MC       | Contact Medical Control for guidance as needed

rows whose action contains "CPAP CONTRAINDICATIONS": 0
references-block bullets: 8
italic "this page" lines: 0
repository paths / file names in rendered prose: 0
```

Row 9 note, as printed (level stays `P`, ⚑ stays):

```
⚑ OWNER_REQUIRED — row 9: PEMS 2024 does not settle which provider level may titrate PEEP.
The level shown is unverified pending a Medical Control decision.
```

The eight contraindications appear **only** under References & Good Practice, as bullets:

```
1. Apnea / agonal respirations
2. Decreased level of consciousness (GCS ≤ 13)
3. Pneumothorax
4. Facial trauma, burns, or recent surgery
5. Penetrating neck/chest trauma
6. Active vomiting / severe nausea
7. Hypotension (SBP < 90 mmHg, MAP < 65)
8. Inability to tolerate a tight-fitting mask
```

### Row splits kept

25 lettered parts across 24 protocol pages + `Neonatal_Resuscitation.md` 5a; the ledger
records **20 bundled rows → 45 parts**, and 3 parts stay `owner_required` (Asystole 8a,
Cardiac Arrest Non-Traumatic 4a, Asthma 8a) and keep their ⚑ — no flag was retired on a row
that still bundles more than one printed level. `level_rule.py --check` re-derives every
chip from the PEMS row it cites (EXIT=0).

## 2. Endotracheal Intubation (content change carried by this rebase, now evidenced)

`docs/procedures/Endotracheal_Intubation.md` gains two printed PEMS rows that the page had
omitted. `git diff main..HEAD --stat` = `1 file changed, 2 insertions(+)`. Live render
(12 rows):

```
row  0 | EMR | Follow Universal Patient Care / Initial Patient Contact protocol.
row  1 | EMT | Pre-oxygenate: 100% O₂ via NRB or BVM for 3 mins. Monitor SpO₂.
row  2 | EMT | Position patient: Ear to sternal notch. Maintain in-line C-spine stabilization if trauma suspected.
row  3 | I   | Prepare equipment: …
row  4 | I   | Orally intubate (Patients ≥ 12 years).
row  5 | P   | Orally intubate (Patients < 12 years).
row  6 | I   | If unsuccessful, re-oxygenate with 100% O₂. …
row  7 | P   | If unable to intubate and unable to oxygenate, proceed immediately to Surgical Airway.
row  8 | I   | Verify placement: Continuous box-waveform EtCO₂, …
row  9 | I   | Secure tube: Tape or commercial holder. Document depth.
row 10 | I   | Administer analgesia/sedation as needed.
row 11 | EMT | Monitor ET tube placement and ventilation with SpO₂ and continuous box-waveform EtCO₂.
```

| added row | PEMS citation (from `audit/level-scan/row-bindings.yaml`) | level basis |
|---|---|---|
| **0** | `pems_page: 247`, `pems_ordinal: 0` — "Follow Universal Patient Care / Initial Patient Contact protocol." | The badge PEMS prints on that row is **EMR**; the chip is that printed badge, not a judgement. Recorded as *gap-fill only; no existing row changes*. |
| **11** | `pems_page: 247`, `pems_ordinal: 13` — "Monitor ET tube placement and ventilation with SpO2 and Continuous box waveform ETCO2" (printed in red) | Printed badge **EMT**; chip is that badge. Recorded as *gap-fill only; no existing row changes*. |

No level on the page was decided by me: the two additions carry the badge their PEMS row
prints, and every other chip on the page is unchanged from `main`.

### Numbering decision (recorded, per the card author's ruling)

**Row `0` is kept; the page is not renumbered.** The page's numbering is offset by one from
the printed page (site row 1 = print #2, pre-oxygenate), and the row numbers are audit keys
bound to PEMS citations. Compressing print #1 in as row `0` preserves all 11 existing
bindings; renumbering `0→1` and shifting would silently re-key board and ledger citations.
Renumbering, if ever wanted, is its own pass that re-keys `row-bindings.yaml` and the ledger
in the same commit — never a side effect of a rebase.

### Gate coverage of this page

* `level_rule.py --check` — `procedures/Endotracheal_Intubation.md` is in its Batch-7 page
  list; the run reports the page's 12 rows among "517 action rows across 54 pages", each
  chip equal to the level its cited PEMS row prints.
* `mc_wording.py --check` — every table row on the page, all levels, checked for
  office/director/agency naming: 0 hits.
* `verify_pems_canonical.py`, `mkdocs build --strict`, `link_sweep.py site`,
  `internal_artifacts.py --check --site site` — all EXIT=0 with the page in the built site.

## 3. Sedation page untouched — re-run at the tip

```
$ git diff main..HEAD --stat -- docs/protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md
(no output — 0 lines)
$ git diff main..HEAD --stat -- docs/pharmacology/Ketamine.md
(no output — 0 lines)
$ git rev-parse --short HEAD   # at time of run
4155092
```

## 4. `mc_wording.py` repo-path guard — two planted bare filenames

Guard: `scripts/mc_wording.py:136`
`REPO_FILE = re.compile(r'(?<![\w/.-])[\w-]+\.(?:ya?ml|json|md)\b')` — `ya?ml` covers both
`.yaml` and `.yml`. Proven this round with **bare file names, no directory prefix**, on a
page this branch does not otherwise touch:

```
$ printf '\n<p class="lv-note">Provenance: see row-bindings.yaml for the binding record.</p>\n' \
    >> docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md
$ python3 scripts/mc_wording.py --check
FAIL — 1 line(s) on reader-facing protocol pages print a repository path or file name. A provider on scene has no checkout; provenance belongs in the audit trail, not on the page.
 - protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md:71: row-bindings.yaml
     <p class="lv-note">Provenance: see row-bindings.yaml for the binding record.</p>
EXIT=1
$ (restore) python3 scripts/mc_wording.py --check
OK — 27 MC row(s) on 26 page(s) plus every other protocol table row (all levels): none name OMD / Poquoson / a Medical Director / a named individual.
     prose lines still mentioning the office (out of scope, not edited): 54
EXIT=0

$ printf '\n<p class="lv-note">Provenance: see split-map.yml for the record.</p>\n' >> (same page)
$ python3 scripts/mc_wording.py --check
FAIL — 1 line(s) on reader-facing protocol pages print a repository path or file name. …
 - protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md:71: split-map.yml
EXIT=1
$ (restore) python3 scripts/mc_wording.py --check  →  EXIT=0
```

A directory-prefixed path (`audit/level-scan/level-rule-ledger.md`) was already proven in
round 1 and is covered by `REPO_PATH`.

## 5. Page voice and the row-number gaps

* Italic self-referential lines: **2 found on the merged tree, 2 rewritten, 0 left**
  (Pulmonary Edema, Cold Exposure). Verified on the live render: `italic "this page"` = 0
  on both pages.
* Pulmonary Edema — the table ran 5 → 9 with no explanation (the pilot's pointer had been
  dropped because it named rows that no longer exist), now:

  ```
  Rows 6–8 were conditional rules for CPAP; they are listed under References & Good Practice below.
  ```

  printed under the table, after the row-9 note.
* Cold Exposure — same defect, corrected the same way (its table runs 5 → 7, rows 6 and 9
  having been relocated):

  ```
  Rows 6 and 9 were conditional rules for rewarming and AED use; they are listed under References & Good Practice below.
  ```

  Both sentences are generated-block-safe: `level_rule.py --write` is idempotent on both
  pages (file md5 unchanged across a second `--write`), so the note insertion cannot
  duplicate a sentence.
* Cold Exposure live render (`…/preview/rows-rebased/protocols/general/02_Cold_Exposure_PROC.html?cb=…`,
  HTTP 200): rows `1,2,3,4,5,7,8`; `italic "this page"` = 0; the rewritten line
  **"Heat packs and warm blankets are an EMR skill — anyone can warm a patient; contacting
  Medical Control before the AED is a Medical Control decision."** is present; References &
  Good Practice block present; `CPAP CONTRAINDICATIONS` rows 0; repo paths in prose 0.
  (The row 8 EMT chip is the page's own pre-existing chip, unchanged by this branch.)

## 6. Agency names (Poquoson / OMD) — measured, not assumed

Card-author ruling of 2026-11-20 12:56 is the governing text: accepted = site H1, `Version:`
/provenance lines, cross-references to agency SOPs by published name; **not** accepted = any
`OMD` / `Poquoson OMD` / named local medical director inside clinical prose, rows, notes,
flags or references blocks. Requirement on this branch: **zero new occurrences** and no
occurrence of the non-accepted class.

```
$ python3 (diff -U0 main..HEAD -- docs, counting \bOMD\b|\bPoquoson\b|\bOperational Medical Director\b|\bMedical Director\b)
office-name occurrences ADDED by branch: 24 on 11 line(s)
office-name occurrences REMOVED by branch: 24 on 11 line(s)
net delta: +0
```

* The 11 added lines are the same sentences the branch removed, rewritten with the
  `audit/…ledger.md` reference stripped. Round 1 measured 25 added / 24 removed; the extra
  one was the generated decisions page's row-9 reason saying "open owner/OMD decision". It
  now reads "open decision for the owner" (§ row-bindings.yaml, Pulmonary Edema row 9), and
  the ledger and `outstanding-decisions.md` were regenerated — hence 24/24, net zero.
* Every remaining occurrence is inside an `agency_names.py` documented exemption
  (H1 / document name, `Version:` provenance, agency-SOP cross-reference, or the
  "Pending OMD authorization" status label — the last allowlisted at `agency_names.py:65`).
* Clinical table rows naming the office: `mc_wording.py --check` reports **0** across all
  levels; `agency_names.py --check` EXIT=0.
* No `OMD` on any clinical page's prose, row, note, flag or references block beyond the
  allowlisted "Pending OMD authorization" status label; the branch adds none.

## 7. Gates — `audit/gates/rows-rebased-4155092.log`

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

Earlier logs kept as history: `audit/gates/rows-rebased-77a7a5d.log` and
`audit/gates/rows-rebased-d174664.log` (each 9/9 EXIT=0, superseded by `4155092` — the gap
sentence had to move below the generated note, and Cold Exposure gained its own).

## 8. Preview slot

Republished to **`/preview/rows-rebased/` only** — gh-pages `a5ef206`, pushed on top of the
then-current `origin/gh-pages` `36d558c` (not from a stale base). `git status` in the
gh-pages worktree before commit: 287 changed paths, **0 outside `preview/rows-rebased/`**.

Live checks after CDN propagation (`?cb=` cache-buster):

```
/preview/               200      /preview/rows/            200
/preview/rows-rebased/  200      /preview/airway-levels/   200
/preview/main/          200      /preview/sedation/        200
/preview/front-matter/  200
Pulmonary Edema : 10 rows (1,2,3,4,5,9,10,11,12,13), CPAP CONTRAINDICATIONS rows 0,
                  8 references bullets, gap sentence present, repo paths 0
Endotracheal     : 12 rows (0…11), repo paths 0
Cold Exposure    : 7 rows (1,2,3,4,5,7,8), gap sentence present, rewritten line present
```
