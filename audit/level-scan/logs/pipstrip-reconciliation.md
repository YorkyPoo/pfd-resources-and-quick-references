# Pip-strip rollout — reconciliation evidence (developer)

Derived in code at branch tip `2b4fac5` from the markdown under `docs/protocols/` and `docs/procedures/`, then checked against the live preview slot. Generator: `reconcile_rollout.py` (walks the docs tree, applies the verifier's own `page_tables()` rules, and emits the table below). Nothing in this table is hand-written.

## 1. Page-by-page reconciliation — all 75 pages in scope

| page | has lv-wrap table? | converted? | if not, why |
|---|---|---|---|
| `protocols/outstanding-decisions.md` | no | no | no table, nothing to convert |
| `protocols/administrative/01_ALS_Release_to_BLS_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_Abuse_Recognition_and_Mandated_Reporting_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_Behavioral_Health_Transportation_Decision_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_Communications_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_Death_Criteria_for_Withholding_Resuscitation_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_Helicopter_EMS_HEMS_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_Infant_Abandonment_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_Patient_Restraint_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_STEMI_Field_Triage_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_Safe_Transport_of_Pediatric_Patients_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_Stroke_Field_Triage_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md` | yes | no | policy table |
| `protocols/administrative/01_Trauma_Field_Triage_PROC.md` | yes | no | policy table |
| `protocols/cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Bradycardia_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Chest_Pain_ACS_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Hypertensive_Crisis_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Post_Resuscitation_Care_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md` | yes | yes | 3 of 3 table(s) |
| `protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.md` | yes | no | pending table |
| `protocols/front-matter/00 - AI Formatting Guidelines.md` | no | no | no table, nothing to convert |
| `protocols/front-matter/00 - Introduction.md` | no | no | no table, nothing to convert |
| `protocols/front-matter/01 - How to Read the Protocols.md` | no | no | no table, nothing to convert |
| `protocols/front-matter/Universal Patient Care.md` | yes | yes | 1 of 1 table(s) |
| `protocols/general/02_Behavioral_Patient_Restraint_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/general/02_Cold_Exposure_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/general/02_Diving_and_Drowning_Emergencies_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/general/02_Heat_Exposure_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/general/02_Pain_Control_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/medical/07_Allergic_Reaction_Anaphylaxis_PROC.md` | yes | yes | 3 of 3 table(s) |
| `protocols/medical/07_Hypotension_Shock_Non_Trauma_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/medical/07_OB_Emergencies_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/medical/07_Sepsis_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/neurologic/05_Hypoglycemia_Hyperglycemia_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/neurologic/05_Seizure_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/neurologic/05_Stroke_TIA_PROC.md` | yes | no | PENDING row in the table |
| `protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Pediatric_Stridor_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Pneumothorax_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Respiratory_Arrest_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Respiratory_Distress_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Smoke_Inhalation_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/toxicology/06_Nausea_Vomiting_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/toxicology/06_Nerve_Agents_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/toxicology/06_Overdose_Poisoning_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/trauma/09_Burns_Thermal_PROC.md` | yes | no | PENDING row in the table |
| `protocols/trauma/09_Crush_Syndrome_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/trauma/09_Electrical_Injuries_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/trauma/09_Hemorrhage_Control_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/trauma/09_Lightning_Injuries_PROC.md` | yes | yes | 1 of 1 table(s) |
| `protocols/trauma/09_Trauma_PROC.md` | yes | yes | 1 of 1 table(s) |
| `procedures/CPAP.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Capnography.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Chest_Decompression.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Endotracheal_Intubation.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Intraosseous_Access.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Medical_Devices_Pumps.md` | no | no | no table, nothing to convert |
| `procedures/Medication_Administration.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Nasogastric_Tube.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Neonatal_Resuscitation.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Spinal_Motion_Restriction.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Surgical_Airway.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Taser_Barb_Removal.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Tourniquet_Application.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Transcutaneous_Pacing.md` | yes | yes | 1 of 1 table(s) |
| `procedures/Vaccination.md` | no | no | no table, nothing to convert |

## 2. Arithmetic, reconciled

```
total pages under docs/protocols + docs/procedures: 75
  carry an lv-wrap table: 69
    converted: 52
    skipped (table publishes no provider level): 17
  no lv-wrap table: 6
check: 52 + 17 + 6 = 75 -> True
expected_pages() size: 52; unchanged_pages() size: 17
```

Where 52 comes from: 75 pages in scope, minus 6 pages with no `lv-wrap` table at all (front matter, how-to-read, index, `Medical_Devices_Pumps`, `Vaccination`), minus 17 pages whose only tables publish no provider level. The 17 skips are 14 `policy` tables, 1 `pending` table, and 2 tables containing a `PENDING` row (Stroke/TIA, Burns). No page with a convertible table was skipped.

## 3. Row parity — one line, as requested

```
502 rows in markdown / 502 rows in HTML / 502 compared / 0 mismatches
```

`scripts/verify_pip_strip.py` against the live slot exited 0:

```
pages converted : 52
action rows     : 502
pages untouched : 17 (no provider level in any table)
OK — every converted page matches its markdown, row by row; every untouched page is unchanged
```

## 4. The `enabled: false` switch, built both ways

Same tip, same `mkdocs.yml`, only `extra.pip_strip.enabled` changed; built with `/root/pfd-ssg-env/bin/mkdocs build`.

```
off build: pages with lv-wrap = 69, pages with data-pip-block = 0
on  build: pages with lv-wrap = 17, pages with data-pip-block = 52
```

Same page (`procedures/CPAP.html`), chip table in the off build:

```html
<div class="lv-wrap">
<table>
<thead>
<tr>
<th style="text-align: center;">#</th>
<th>Level</th>
<th>Action / Intervention</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;">1</td>
<td>
<span class="lvl lvl-emt">EMT</span>
</td>
<td>Explain procedure and indications to the patient.</td>
</tr>
<tr>
```

Same page in the on build:

```html
<div class="pip-block" data-pip-block>
<p class="pip-pick-label">Tap your certification level</p>
<div class="pip-pick" role="group" aria-label="Show the protocol as your certification level">
<button type="button" class="pip-btn" data-level="R" aria-pressed="false">R</button>
<button type="button" class="pip-btn" data-level="B" aria-pressed="false">B</button>
<button type="button" class="pip-btn" data-level="A" aria-pressed="false">A</button>
<button type="button" class="pip-btn" data-level="I" aria-pressed="false">I</button>
<button type="button" class="pip-btn" data-level="P" aria-pressed="false">P</button>
<button type="button" class="pip-btn pip-btn-all" data-level="all" aria-pressed="true">Show all</button>
</div>
<p class="pip-tally" aria-live="polite">Show all — 6 actions. Each row names the level its action starts at; tap a level to see this protocol as you.</p>
<div class="pip-wrap">
<table class="pip-table">
<colgroup>
<col class="pip-col-n">
<col>
<col class="pip-col-strip">
</colgroup>
```

## 5. Fallback checks

```
tag tables-backup-2026-11-20 -> d5fd03cf7972e9534a8587c6c031f1927bab2054
tag object                  -> 2e880651431e240509fa1de62e11442775cc1429
main / origin/main          -> d5fd03c (unchanged)
archive page files          -> 69
archive index converted rows-> 52
archive index skipped rows  -> 17
converted pages missing an archive file -> 0
archive files for pages not in either set -> 0
```

The archive holds 69 page snapshots — every page with an `lv-wrap` table, including the 17 skipped pages — so all 52 converted pages have a snapshot (0 missing) and the 17 untouched pages are preserved too. `index.md` lists 52 converted and 17 skipped.

## 6. Pages still rendering the old chip table at the live slot

These are the 17 skipped pages; all other 52 pages serve the strip:


- `protocols/administrative/01_ALS_Release_to_BLS_PROC.md`
- `protocols/administrative/01_Abuse_Recognition_and_Mandated_Reporting_PROC.md`
- `protocols/administrative/01_Behavioral_Health_Transportation_Decision_PROC.md`
- `protocols/administrative/01_Communications_PROC.md`
- `protocols/administrative/01_Death_Criteria_for_Withholding_Resuscitation_PROC.md`
- `protocols/administrative/01_Helicopter_EMS_HEMS_PROC.md`
- `protocols/administrative/01_Infant_Abandonment_PROC.md`
- `protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md`
- `protocols/administrative/01_Patient_Restraint_PROC.md`
- `protocols/administrative/01_STEMI_Field_Triage_PROC.md`
- `protocols/administrative/01_Safe_Transport_of_Pediatric_Patients_PROC.md`
- `protocols/administrative/01_Stroke_Field_Triage_PROC.md`
- `protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md`
- `protocols/administrative/01_Trauma_Field_Triage_PROC.md`
- `protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.md`
- `protocols/neurologic/05_Stroke_TIA_PROC.md`
- `protocols/trauma/09_Burns_Thermal_PROC.md`

## 7. Defect statement

No page with a convertible level table was left unconverted. The only tables not converted are the 14 `policy` tables, the 1 `pending` table, and the 2 mixed-`PENDING` tables. The two mixed-PENDING pages (Stroke/TIA rows 8-9, Burns row 6) are a deliberate skip, not a silent miss: the strip has no slot for "no level exists", so converting them would invent a clinical claim. They keep today's chip table until the owner rules on PENDING row rendering.
