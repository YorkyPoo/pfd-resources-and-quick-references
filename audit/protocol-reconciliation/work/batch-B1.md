# Batch B1 audit — PEMS2024 vs published site (parent t_d3600e06, task t_04b8386e)

READ-ONLY audit. No edits under docs/, the vault, or scripts. No scripts run (no shell). PEMS source: `pems_chunks/PEMS2024_full.txt` (flattened text). Severity per work/00 policy.

**Totals: 74 discrepancies — CRITICAL 18 · MODERATE 51 · MINOR 5.** Per protocol: Sepsis 16 (7/8/1), Hypotension 10 (4/5/1), Nausea 11 (0/10/1), OB 37 (7/28/2). Inferred level decodes: 2 (HYP-06, OB-04).

**Caveats.** (1) Pearl blocks on PEMS p.114, p.130, p.141 and p.147 are truncated mid-sentence in the text extraction; those tails were not read, and statements that depend on them are marked PROVISIONAL or unverified. (2) PDF extraction fails with NeedsOcrError (pages 47, 151 of 280), so the PDF could not serve as an independent check; a human should eyeball the PDF before the developer edits any blocking row, per work/00. (3) Cross-batch consistency: IV-fluid rows are CRITICAL here (SEP-02, HYP-05, OB-19) but MODERATE in batch A1 (F-AL-08/09); ECG is MODERATE here (HYP-04) but CRITICAL in chest pain. The parent should rule once for each class.

---

## docs/protocols/medical/07_Sepsis_PROC.md
Coverage: PEMS p.129-130 — criteria table, all 6 PEMS rows (+ MC) and all 6 site rows compared; pearl tail (p.130) truncated, not verified. Status FIXABLE; verified: false.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| SEP-01 | 1 | Provider level (Universal) | "EMR Follow Universal Patient Care / Initial Patient Contact protocol." | "Follow Universal Patient Care \| \| • \| • \| • \| •" (EMR blank) | MODERATE | Set EMR • on row 1 |
| SEP-02 | 2 | Provider level (IV/IO + NS bolus) | "A Obtain IV/IO access. Administer: ADULT: 0.9% Sodium chloride up to 1 L IV/IO in 250 – 500 mL boluses" | "Obtain IV/IO access and administer **0.9% Normal Saline** … " (I, P only) | CRITICAL | Set A • on row 2 |
| SEP-03 | 3 | Provider level (norepi/epi adult infusion) | "I Maintain mean arterial pressure (MAP) above 65 mmHg. Consider: ADULT: Norepinephrine (Levophed) infusion 5 – 20 mcg/min" | "Maintain MAP > 65 mmHg. **Norepinephrine** infusion **5-20 mcg/min** OR **Epinephrine** … (Adult)" (P only) | CRITICAL | Set I • on row 3 |
| SEP-04 | 3 | Concentration | "(Add 4 mg of Norepinephrine to 250 mL 0.9% Sodium chloride = 16 mcg/mL) … (Add 1 mg of Epinephrine [1mg/mL] to 100 mL of 0.9% Sodium chloride = 10 mcg/mL)" | (absent) | CRITICAL | Add both mixing statements to row 3 |
| SEP-05 | 4 | Provider level (peds epi infusion, MC-bracket) | "[ I ] Maintain age adjusted SBP. Consider: PEDIATRIC: Epinephrine 0.1 - 1 mcg/kg/min IV/IO infusion." | "Maintain age adjusted SBP. **Epinephrine 0.1 - 1 mcg/kg/min** infusion max **10 mcg/min** (Pediatric)" (P only) | CRITICAL | Set I to [I] on row 4 |
| SEP-06 | 4 | Dose targets / concentration | "Under 1 year old: Titrate to SBP > 70 mmHg Over 1 year old: Titrate to SBP > 90 mmHg (Add 1 mg of Epinephrine [1mg/mL] to 100 mL …)" | (absent) | CRITICAL | Add SBP targets, 10 mcg/mL concentration, pump/extravasation note |
| SEP-07 | 5 | Provider level (push-dose epi adult) | "[ I ] P To maintain MAP > 65 mmHg until a vasopressor infusion is prepared, consider: ADULT: Push dose Epinephrine 5-10 mcg IV/IO every 2-3 minutes" | "Push dose **[Epinephrine] 5-10 mcg** IV/IO every 2-3 mins …" (all levels blank) | CRITICAL | Set P • on row 5 |
| SEP-08 | 5 | Concentration (push dose) | "(Add 100 mcg Epinephrine (1mL of 0.1 mg/mL) to 9mL of 0.9% Normal Saline = 10 mcg / mL)" | (absent) | CRITICAL | Add 10 mcg/mL dilution to row 5 |
| SEP-09 | 6 | Provider level (MC, bare in PEMS) | "P MC Contact Medical Control for guidance as needed, and advise of a 'Prehospital Sepsis Alert.' MC" | "Contact Poquoson Medical Control / Prehospital Sepsis Alert \| \| \| [A] \| • \| •" | MODERATE | Bracket MC at all five levels |
| SEP-10 | — | CRT threshold | "Capillary Refill Greater than 3 seconds" | "Capillary Refill > 2 seconds" | MODERATE | Change to > 3 seconds |
| SEP-11 | — | Numeric thresholds by age | "Systolic BP Less than 70 mmHg … Less than 90 mmHg; MAP Less than 55 / 65; Respiratory Rate > 60 / > 30; Bradycardia < 100 / < 90" | "SBP/MAP thresholds by age"; "RR abnormalities"; "Bradycardia" (no values) | MODERATE | Insert age-banded values (inferred from flattened table — confirm in PDF) |
| SEP-12 | — | High Risk criterion | "High Risk Immunocompromised, Malignancy, Indwelling catheters/tech, Sickle Cell Disease" (criteria-table row) | HPI bullets only, not a counted criterion | MODERATE | Make High Risk a counted criterion |
| SEP-13 | — | Pearl: bolus size | "Administer smaller boluses (eg 250 mL then reassess) and consider early administration of vasopressors …" | "Administer IV fluids carefully … Monitor closely for signs of fluid overload" | MODERATE | Add 250 mL / reassess / early-vasopressor / MC-if-doubt |
| SEP-14 | — | Pearl: high-risk list | "Age < 56 days (8 weeks), presence of an indwelling catheter, malignancy, asplenia/sickle cell disease, use of immunosuppressant medications" | (partial, in HPI) | MODERATE | Add full list |
| SEP-15 | — | Pearl: vasopressor access/extravasation (PROVISIONAL) | p.130 pearl block truncated; text search indicates vasopressor-access pearl present | "should ideally be administered via an infusion pump" only | MODERATE | Verify wording in PDF p.130, then add access-site and extravasation guidance |
| SEP-16 | — | Unsourced HPI/Differential | (no PEMS equivalent) | "Differential Considerations … Monitor for fluid overload …" | MINOR | Medical director to verify or remove |

---

## docs/protocols/medical/07_OB_Emergencies_PROC.md
Coverage: PEMS Childbirth/Labor/Delivery p.141-145; Eclampsia p.147-148; Pregnancy Related Emergencies p.149 (located by title; no "OB" heading). All 10 site rows and all PEMS rows compared; several pearl tails truncated. Status FIXABLE; verified: false.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| OB-01 | 1 | Provider level (Universal, PPE) | "EMR Follow Universal Patient Care / Initial Patient Contact protocol. Don appropriate PPE" | "Follow Universal Patient Care, don appropriate PPE, and visualize perineum …" (EMR blank) | MODERATE | Set EMR • on row 1 |
| OB-02 | 2 | Provider level (normal delivery) | "EMR EMR If crowning, apply gentle pressure on the bony part of the skull (not fontanel)" | "**Normal Delivery:** Apply gentle pressure on infant's skull …" (EMR blank) | MODERATE | Set EMR • on row 2 |
| OB-03 | 2 | Suction exception | "Only perform pharyngeal/tracheal suctioning if thick meconium is present or when the airway is obstructed." | "DO NOT perform routine airway suctioning." | MODERATE | Add meconium/obstruction exception |
| OB-04 | 3 | Provider level (shoulder dystocia) | "Shoulder Dystocia If unable to deliver the anterior shoulder, place the patient in McRobert's position … EMR EMR Once delivery is complete" | "**Shoulder Dystocia:** Place mother in McRobert's position …" (EMR blank) | MODERATE | Set EMR • on row 3 (INFERRED) |
| OB-05 | 3 | MC step | "If no progress, contact Medical Control immediately for guidance." | (absent) | MODERATE | Add MC step |
| OB-06 | 4 | Provider level (cord prolapse) | "EMR UMBILICAL CORD PROLAPSE Immediately transport to a facility with obstetric capability." | "**Umbilical Cord Prolapse:** …" (EMR blank) | MODERATE | Set EMR • on row 4 |
| OB-07 | 4 | Transport | "Immediately transport to a facility with obstetric capability." | (absent) | MODERATE | Add transport instruction |
| OB-08 | 5 | Provider level (breech) | "EMR BREECH DELIVERY Initiate transport, preferably to a facility with obstetric capability." | "**Breech Delivery:** Allow controlled, spontaneous delivery …" (EMR blank) | MODERATE | Set EMR • on row 5 |
| OB-09 | 5 | Breech manoeuvres | "Once the scapula is visible, gently rotate a few degrees and swipe across the chest to deliver the arms. … Maintain flexion of the neck (chin to chest) with downward traction by two fingers on the maxilla." | "Deliver the legs and support the body." only | CRITICAL | Add towel, torso rotation, arm delivery, second-provider pressure, neck flexion |
| OB-10 | 5 | Transport / MC | "Initiate transport, preferably to a facility with obstetric capability. If delivery is imminent: Contact Medical Control as soon as feasible" | (absent) | MODERATE | Add transport and MC-as-feasible sentences |
| OB-11 | 6 | Provider level (Mg 4 g eclampsia) | "EMT I If actively seizing or a seizure has occurred (Eclampsia), administer: ADULT: Magnesium Sulfate 4 g IV/IO infusion over 10 minutes." | "**Magnesium Sulfate 4 g** IV/IO infusion over 10 minutes." (P only) | CRITICAL | Set I • on row 6 |
| OB-12 | 7 | Provider level (midazolam >5 min) | "I I If seizure continues for more than five minutes, also administer: ADULT: Midazolam (Versed) 5 mg IV/IO or 10 mg IM" | "If seizures persist > 5 minutes, administer **Midazolam 5 mg** IV/IO or **10 mg** IM." (P only) | CRITICAL | Set I • on row 7 |
| OB-13 | 7 | Half-dose caution | "Use half dose Midazolam for frail, hypotensive, and/or underweight patients." | (absent) | CRITICAL | Add half-dose instruction |
| OB-14 | absent | EMT transport to L&D | "EMT Transport to a facility with labor and delivery capability." | (absent) | MODERATE | Add EMT L&D transport step |
| OB-15 | — | Criteria: >20 weeks | "Any pregnant or recently pregnant patient over 20 weeks gestational age experiencing seizures." | "**Eclampsia:** Active seizures during pregnancy or postpartum." | MODERATE | Add >20 weeks |
| OB-16 | — | Criteria: pre-eclampsia | "Systolic blood pressure greater than 160 mmHg or diastolic blood pressure greater than 110 mmHg … Right upper quadrant or epigastric abdominal pain … Pulmonary edema" | "BP > 160/110 mmHg, severe headache, visual disturbances, edema" | MODERATE | Rewrite to PEMS criteria |
| OB-17 | 8 | Provider level (rupture/abruptio) | "EMR Place patient in left lateral recumbent position and transport immediately." | "**Bleeding / Rupture / Abruptio:** Place patient in left lateral recumbent position." (EMT+) | MODERATE | Set EMR • on row 8 |
| OB-18 | 8 | Transport immediately | "… and transport immediately." | (absent) | MODERATE | Append "transport immediately" |
| OB-19 | 9 | Provider level (IV + NS 20 mL/kg ≤1,000 mL) | "EMR A Establish IV access and administer 20 mL/kg 0.9% Normal Saline bolus up to 1,000 mL" | "Establish IV access and administer **0.9% Normal Saline 20 mL/kg** up to **1,000 mL**." (I, P only) | CRITICAL | Set A • on row 9; add reassess-fluids sentence |
| OB-20 | absent | ABC / O2 / shock referral | "EMR Support life threatening problems associated with airway, breathing and circulation. … If patient exhibits signs of shock, see Medical – Hypotension/Shock" | (absent) | MODERATE | Add three EMR rows |
| OB-21 | absent | Hemorrhagic-shock referral | "EMR If significant bleeding, refer to Hemorrhagic Shock protocol." | (absent) | MODERATE | Add EMR referral row |
| OB-22 | absent | Placenta / post-partum bleeding | "Assess for additional pregnancies. If none, apply gentle traction to the umbilical cord and perform fundal massage until the placenta delivers and bleeding stops." (final sentence truncated) | (absent) | CRITICAL | Add EMR placenta-delivery / PPH row; verify truncated sentence in PDF |
| OB-23 | 2 | Neonatal assessment / resus referral | "Assess heart rate, respirations, and oxygen saturation. Follow Neonatal Resuscitation protocol." | "Dry, warm, and stimulate the neonate." only | CRITICAL | Add HR/RR/SpO2 assessment and Neonatal Resuscitation referral |
| OB-24 | absent | Delayed cord clamping | "consider delayed cord clamping until 1 – 3 minutes after birth … clamps at approximately 4” and 6”" | (absent) | MODERATE | Add row |
| OB-25 | 2 | Nuchal cord management | "Unwrap if possible. Clamp and cut if necessary." | "Check for nuchal cord." | MODERATE | Add unwrap and clamp/cut |
| OB-26 | 1–2 | Delivery technique | "Remove all clothing below the waist." / "bony part of the skull (not fontanel)" / "Support the head while delivering the shoulders and torso." | Omitted; "gentle pressure on infant's skull" without "not fontanel" | MODERATE | Add three steps |
| OB-27 | — | Pearl: GA / resuscitation / ROM | "Resuscitation should be attempted for any fetus born after 22 weeks gestational age." "Rupture of membranes … prior to 37 weeks gestation is considered premature." | (absent) | MODERATE | Add pearls |
| OB-28 | — | Pearl: transport unit / neonatal SpO2 | "Consider requesting an additional transport unit …" "Normal newborn SpO2 is 60-70% in the first minute …" | (absent) | MODERATE | Add pearls |
| OB-29 | — | Pearl: no fundal pressure | "No NOT apply pressure to the uterine fundus." | (absent) | MODERATE | Add pearl (verbatim, incl. PEMS typo) |
| OB-30 | — | Pearl: Mg max / IM midazolam | "the total maximum dose is 4g Magnesium Sulfate." "consider early IM administration of midazolam followed by Magnesium infusion" | (absent) | MODERATE | Add pearl |
| OB-31 | — | Pearl: Mg cautions | "Administration of Magnesium and Benzodiazepines may lead to respiratory/CNS depression." "rapid administration of Magnesium may cause vasodilation and hypotension" | (absent) | MODERATE | Add pearls (vitals q5 min tail truncated) |
| OB-32 | — | Pearl: early notification | "Provide early notification to the hospital as non-ED care teams such as OBGYN and anesthesia" | (absent) | MODERATE | Add pearl |
| OB-33 | — | Abruptio / rupture criteria | "Premature separation of the placenta from the uterine wall after the 20th week of gestation and prior to birth." | "Third-Trimester Bleeding: Painless or painful vaginal bleeding" | MODERATE | Use PEMS definitions |
| OB-34 | — | Pearl: abruptio age risk | "Patients younger than 20 and greater than 35 years of age are at greater risk for placental abruption." | (absent) | MODERATE | Add pearl |
| OB-35 | 10 | MC row content | "All patients must be secured with appropriate safety restraints for transport. Do not transport the baby in the mother's arms." | MC level cells correct; restraint and neonate-transport text absent | MODERATE | Add the two sentences |
| OB-36 | — | Unsourced pearl | (not found in PEMS) | "Do not pull on the umbilical cord or infant during delivery." | MINOR | Verify or remove |
| OB-37 | — | Unsourced HPI/Differential | (no PEMS equivalent) | "Differential Considerations … Normal labor vs. false labor …" | MINOR | Verify or remove |

---

## docs/protocols/medical/07_Hypotension_Shock_Non_Trauma_PROC.md
Coverage: PEMS p.113-116 — all 9 rows plus MC row, criteria, pearls (visible portion), two drip charts. Re-verified from source; the partly-done decode in work/00 is confirmed. Pearl tail after p.114 "consider earl…" truncated, not verified. Status FIXABLE; verified: false.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| HYP-01 | 1 | Provider level (Universal) | "EMR Follow Universal Patient Care / Initial Patient Contact protocol." | "Follow Universal Patient Care / Initial Patient Contact protocol." (EMR blank) | MODERATE | Set EMR • on row 1 |
| HYP-02 | 2 | Provider level (history/focused assessment) | "EMR EMR Obtain relevant history and perform a focused assessment" | "Obtain relevant history and perform a focused assessment …" (EMR blank) | MODERATE | Set EMR • on row 2 |
| HYP-03 | 3 | Provider level (SpO2, airway) | "EMR EMR Maintain SpO2 94 – 98%." | "Maintain SpO2 **94 – 98%**." (EMR blank) | MODERATE | Set EMR • on row 3 |
| HYP-04 | 4 | Provider level (12-lead ECG) | "EMR EMT Obtain and transmit a 12-Lead ECG." | "Obtain and transmit a 12-Lead ECG." (A, I, P only) | MODERATE | Set EMT • on row 4 (diagnostic; see cross-note) |
| HYP-05 | 5 | Provider level (IV + NS bolus) | "EMT A Obtain IV/IO access. Administer: ADULT: 0.9% Sodium chloride up to 1 L IV/IO in 250 – 500 mL boluses" | "Obtain IV/IO access. Administer: ADULT: **0.9% Sodium chloride** up to **1 L** …" (I, P only) | CRITICAL | Set A • on row 5 |
| HYP-06 | 6 | Provider level (cardiac monitoring) | "A I Assess and continuously monitor cardiac rhythm." | "Assess and continuously monitor cardiac rhythm. …" (P only) | MODERATE | Set I • on row 6 (INFERRED from "A I" pair) |
| HYP-07 | 7 | Provider level (MAP: norepi/epi adult infusion) | "I I Maintain mean arterial pressure (MAP) above 65 mmHg. Consider: ADULT: Norepinephrine (Levophed) infusion 5 – 20 mcg/min" | (P only) | CRITICAL | Set I • on row 7 |
| HYP-08 | 8 | Provider level (peds epi infusion, MC-bracket) | "[ I ] Maintain age adjusted SBP. Consider: PEDIATRIC: Epinephrine 0.1 - 1 mcg/kg/min IV/IO infusion." | (P only) | CRITICAL | Set I to [I] on row 8 |
| HYP-09 | 9 | Provider level (push-dose epi adult) | "[ I ] P To maintain MAP > 65 mmHg until a vasopressor infusion is prepared … ADULT: Push dose Epinephrine 5-10 mcg IV/IO every 2-3 minutes" | (all levels blank) | CRITICAL | Set P • on row 9 |
| HYP-10 | — | Unsourced HPI | (not in PEMS CRITERIA) | "Vomiting, diarrhea, or poor fluid intake; Recent illness (infection, sepsis); History of cardiac disease" | MINOR | Verify or remove |

Verified as correct (no finding): row 10 MC bare at all levels; norepinephrine drip chart 5→19 … 20→75 drops/min and epinephrine chart 1→6 … 10→60 drops/min (identical to PEMS p.115-116); concentrations 16 mcg/mL and 10 mcg/mL; push-dose dilution; peds titration targets on row 8.

---

## docs/protocols/toxicology/06_Nausea_Vomiting_PROC.md
Coverage: PEMS p.117 — full text visible (no truncation); all 6 PEMS rows and all 6 site rows compared; criteria, pearls compared. Status FIXABLE; verified: true.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| NAU-01 | 1 | Provider level (Universal) | "PROTOCOL EMR Follow Universal Patient Care / Initial Patient Contact protocol." | "Follow Universal Patient Care \| \| • \| • \| • \| •" (EMR blank) | MODERATE | Set EMR • on row 1 |
| NAU-02 | 2 | Provider level (position, suction) | "EMR EMR Place patient in a position of comfort. … provide suctioning." | "Place in position of comfort / recovery position if unresponsive; suction as needed" (EMR blank) | MODERATE | Set EMR • on row 2 |
| NAU-03 | 3 | Provider level (refer to Airway/Hypotension) | "EMR EMR Refer to Hypotension and Shock protocol, as needed." | "Refer to Airway and Hypotension protocols as needed" (EMR blank) | MODERATE | Set EMR • on row 3 |
| NAU-04 | 4 | Provider level (ondansetron 4 mg ODT) | "EMT Consider: ADULT: Ondansetron (Zofran) 4 mg ODT." | "**Ondansetron (Zofran) 4 mg** ODT" (EMR, EMT blank) | MODERATE | Set EMT • on row 4 |
| NAU-05 | 5 | Provider level (ondansetron IV/IO/IM/PO) | "EMT A Consider: ADULT: Ondansetron (Zofran) 4 mg IV/IO slow push, IM or PO." | "Adult: **Ondansetron (Zofran) 4 mg** IV/IO slow push, IM, or PO …" (I, P only) | MODERATE | Set A • on row 5 |
| NAU-06 | 6 | Provider level (MC, bare in PEMS) | "A MC Contact Medical Control for guidance as needed. MC" | "Contact Poquoson Medical Control for additional doses or orders \| \| \| [A] \| • \| •" | MODERATE | Bracket MC at all five levels |
| NAU-07 | 4–5 | Repeat interval | "May repeat in 10 - 15 minutes, as needed." (both rows) | (absent) | MODERATE | Add repeat interval to rows 4 and 5 |
| NAU-08 | — | Pearl: IV push duration | "Caution: Administer IV Ondansetron (Zofran) via slow push – at least 30 seconds, but preferably 2 minutes." | "must be administered as a SLOW IV push (over 2-5 minutes)" | MODERATE | Replace with PEMS wording (threshold drift) |
| NAU-09 | — | Pearl: QT | "patients taking other drugs which prolong the QT interval (e.g. Amiodarone, Haloperidol) and patients with pre-existing prolonged-QTc (≥ 500 ms)." | "known prolonged QT interval" only | MODERATE | Add QTc ≥500 ms and named drugs |
| NAU-10 | — | Pearl: prophylaxis (CONFLICT) | "Anti-emetic medications are often more effective when given prophylactically or for nausea prior to vomiting." | "Prophylactic use of antiemetics is generally not recommended unless specific clinical indications are present." | MODERATE | Reconcile; medical director to decide and document |
| NAU-11 | — | Unsourced HPI/Differential | (no PEMS equivalent) | "Differential Considerations … DKA … Pregnancy / Ectopic" | MINOR | Verify or remove |

---

## Count reconciliation
- Discrepancies in JSON (batch-B1.json): 74 (Sepsis 16, OB 37, Hypotension 10, Nausea 11).
- Rows in this report: 74 (Sepsis 16, OB 37, Hypotension 10, Nausea 11).
- Lines in fixlist (batch-B1.fixlist.md): 74.
- Totals by severity: CRITICAL 18 (SEP 7, OB 7, HYP 4, NAU 0) · MODERATE 51 (SEP 8, OB 28, HYP 5, NAU 10) · MINOR 5 (SEP 1, OB 2, HYP 1, NAU 1). 18 + 51 + 5 = 74.
- Manual protocols: none. Inferred level decodes: 2 (HYP-06, OB-04).
