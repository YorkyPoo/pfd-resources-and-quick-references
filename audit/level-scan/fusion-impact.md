# PEMS row fusion — impact assessment (`pems_table.json`)

Read-only measurement of how many extracted PEMS level-table rows fuse two or more *printed* rows, and how far
that reaches into the converted site. The only files written are this one and `fusion-impact.json`.

## The number

**12 of the 79 measurable PEMS pages carry at least one fused row** (17 fused rows in total, absorbing 38 printed rows).

- extracted rows in `pems_table.json`: **535** (`len()` of the flattened row list = 535)
- pages carrying extracted rows: **82**
- rows the method can measure: **527** on **79** pages (531 printed action rows found on those pages)
- rows it cannot measure: **8** — p.7 'How to Read the Protocols' (a legend, no badges), p.43 'Trauma Field Triage' (no ruled table), p.52 (no badged cells)
- **pages affected: 12** — p.22, p.28, p.67, p.104, p.120, p.141, p.153, p.235, p.247, p.252, p.263, p.269
- **pages affected inside the converted set (the 54 `TARGETS` + 1 `PENDING_TARGETS` page): 4** — p.67, p.235, p.247, p.269

## Definition of "fused"

A fused row is one pems_table.json row whose verbatim_text contains text that the PDF prints in more than one bordered level-table row. Printed rows are the table cells separated by the PDF horizontal ruling lines (extracted with pdfplumber); only cells that carry a printed badge (EMR/EMT/A/I/P/MC) count as action rows. A row is credited with a printed row when (a) its first tokens open that printed row ("own"), (b) its first tokens begin inside that printed row ("starts_mid_row" - the previous extracted row took the opening), (c) it contains that printed row's opening 6 tokens at a word boundary, only if that opening is unique on the page ("next_row_opening"), or (d) it contains every token of that printed row ("whole_row_embedded"). n_printed >= 2 means fused.

## Detector, validated against the known cases

- **p.247 #3 (the proven defect) — FLAGGED**, credited with 3 printed rows (`{'2': 'starts_mid_row', '3': 'next_row_opening', '4': 'next_row_opening'}`):
    - printed row 2: Position the patient: Ear to sternal notch. Maintain in-line cervical spine stabilization if there is concern for t
    - printed row 3: Prepare equipment: o IV/IO access o ET tube of appropriate size + 1 size below o Stylet or bougie o Oxygen ON o Suc
    - printed row 4: Orally intubate. Patients 12 years and older. Advance laryngoscope in the midline, identifying airway structures pr
    (the card calls it "four printed rows": the fourth, `Position the patient: Ear to sternal notch.`, is the first half that the extractor put in #2 — #2+#3 together span four printed rows.)
- **p.107 #1 (known-clean control) — NOT FLAGGED**, credited `{'1': 'own'}`.

## Fused rows

| extracted row | badge in table | printed rows absorbed | rule fired | first printed row of the fusion |
|---|---|---|---|---|
| p.22 #5 | MC | 2 | next_row_opening, own | When treating cardiac arrest victims who possess a "living will" or an adva |
| p.28 #9 | A | 2 | next_row_opening, starts_mid_row | For patients in cardiac arrest: • • • • • • A DNR/DDNR/DNAR (Do Not Resusci |
| p.67 #1 | EMR | 2 | next_row_opening, own | Place patient in a warm environment and prevent further heat loss |
| p.67 #2 | EMR | 2 | next_row_opening, starts_mid_row | Remove all wet clothing and replace with warm blankets. Handle the patient  |
| p.104 #13 | MC | 2 | next_row_opening, starts_mid_row | To maintain MAP > 65 until a vasopressor infusion is prepared, consider: AD |
| p.120 #10 | EMR | 2 | next_row_opening | Begin active cooling if temperature is greater than 104F / 40C. Refer to He |
| p.141 #9 | EMR | 3 | next_row_opening, starts_mid_row | Routine suctioning is no longer recommended. Only perform pharyngeal/trache |
| p.141 #11 | EMR | 2 | next_row_opening, starts_mid_row | Assess for additional pregnancies. If none, apply gentle traction to the um |
| p.153 #4 | A | 2 | next_row_opening, starts_mid_row | Administer: ADULT: Albuterol Sulfate 3 mL of 0.083% solution, nebulized. Re |
| p.235 #2 | EMR | 2 | next_row_opening, own | Begin chest compressions. Push hard and fast. Allow full chest recoil. Limi |
| p.235 #4 | EMR | 3 | next_row_opening, starts_mid_row | Administer 100% oxygen. Do not over-ventilate. Maintain compression-ventila |
| p.247 #3 | I | 3 | next_row_opening, starts_mid_row | Position the patient: Ear to sternal notch. Maintain in-line cervical spine |
| p.247 #7 | P | 2 | next_row_opening, starts_mid_row | If unsuccessful, reoxygenate between attempts with 100% Oxygen. Adjust posi |
| p.247 #9 | I | 3 | next_row_opening, starts_mid_row | Verify placement. o Ensure the presence of continuous box-waveform capnogra |
| p.252 #11 | MC | 2 | next_row_opening, starts_mid_row | If unresponsive and without palpable pulses, assist ventilations. Ensure th |
| p.263 #5 | EMR | 2 | next_row_opening, own | Alternate compressors every 2 minutes or sooner if fatigued. |
| p.269 #1 | P | 2 | next_row_opening | Make a vertical incision (2 – 3 cm) across the cricothyroid membrane. |

## PDF cross-checks (`pdftoppm -r 150`, page read visually)

| page | extracted row | what the printed page shows | verdict |
|---|---|---|---|
| p.247 | #3 | "Position the patient: Ear to sternal notch. / Maintain in-line cervical spine stabilization…" (EMT) is ONE cell; "Prepare equipment: • IV/IO access…" (I) is the next; "Orally Intubate. Patients 12 years and older. / Advance laryngoscope…" (I) the next. #3 starts inside the EMT cell and runs through both. | fused — confirmed |
| p.247 | #7 | "After two failed attempts… Surgical Airway." and "If unable to intubate and unable to oxygenate…" are two separate bordered rows. | fused — confirmed |
| p.247 | #9 | "Verify placement. o Ensure… o Auscultate…" (I), "Secure the tube. Use tape…" (I) and "Administer analgesia/sedation…" (I) are three separate bordered rows. | fused — confirmed |
| p.235 | #2 | "Begin chest compressions…"; "Administer 100% oxygen. Do not overventilate."; "Maintain compression-ventilation ratio 30:2…" — separate bordered rows. | fused — confirmed |
| p.235 | #4 | "If respiratory pathogen is suspected…"; "Apply AED / Assess cardiac rhythm every 2 minutes."; "If AED is advising to shock…" — three separate bordered rows. | fused — confirmed |
| p.269 | #1 | "Position the patient supine… palpate the cricothyroid membrane." is one cell; "Make a vertical incision (2 – 3 cm)…" the next. #1 starts at "membrane." and continues into the incision row. | fused — confirmed |
| p.67 | #1, #2 | "Place patient in a warm environment…"; "Remove all wet clothing…"; "In the event of cardiac arrest…" — three separate bordered rows. | fused — confirmed |
| p.141 | #9, #11 | "Routine suctioning…"; "If the neonate does not require immediate resuscitation…"; "Assess for additional pregnancies…"; "Apply direct pressure…" — four separate bordered rows. | fused — confirmed |
| p.245 | — (control) | all five CPAP rows are separate cells and the detector flags none of them; it does not fire simply on long rows. | clean — confirmed |

## Second question: is the badge wrong?

**4 of 17 fused rows carry a badge that belongs to a later printed row inside the fusion:**

| extracted row | badge in table | badge of the first printed row | effect |
|---|---|---|---|
| p28 #9 | A | EMT | chip can print a level the printed row does not authorise |
| p104 #13 | MC | P | chip can print a level the printed row does not authorise |
| p247 #3 | I | EMT | chip can print a level the printed row does not authorise |
| p247 #7 | P | I | chip can print a level the printed row does not authorise |

The other fused rows happen to start on a printed row with the same badge; their defect is content, not level.

## Blast radius on published content

Site rows whose binding in `audit/level-scan/row-bindings.yaml` cites a fused PEMS row:

| site page | site rows | PEMS rows cited |
|---|---|---|
| `procedures/Endotracheal_Intubation.md` | 2, 3, 4, 6, 7, 8, 9, 10 | p247#3, p247#7, p247#9 |
| `procedures/Surgical_Airway.md` | 2 | p269#1 |
| `protocols/respiratory/03_Respiratory_Arrest_PROC.md` | 12 | p247#9 |
| `protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md` | 14 | p247#7 |

Total: **11 site rows on 4 converted site pages**. The fused rows on p.67 and p.235 are not cited by any binding yet (their site pages bind different PEMS rows).

## Limits of this number

- Only *fusion* is counted. The mirror defect — one printed row split across two extracted rows (p.247 #2/#4, p.269 #2) — is excluded and would add to the damage.
- Three pages (7 rows) have no ruled, badged table; they are reported unmeasured, not clean.
- A fusion whose absorbed fragment is shorter than a six-token opening is not detected; the count is a floor, not a ceiling.

