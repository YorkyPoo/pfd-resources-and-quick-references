# Batch C1 — respiratory protocols vs PEMS2024 (read-only audit)

Source: `pems_chunks/PEMS2024_full.txt`. No shell, so no scripts were run; PDF extraction fails (OCR needed on pp. 47 and 151), so the flattened text is the only source. Level decodes marked `inferred` need a human PDF check before developer edits. The JSON holds full verbatim quotes; the table quotes below are shortened excerpts.

Protocol-to-PEMS mapping: three of the five protocols have no PEMS title in the flattened text (Pneumothorax, Respiratory Arrest, Upper Airway Obstruction). Those are audited against the closest PEMS procedure text and recorded MANUAL, verified=false, following the C2 precedent.

Totals: 65 discrepancies — CRITICAL 27, MODERATE 38, MINOR 0. Inferred-level decodes: 14.

## 03_Respiratory_Distress_PROC.md (21: CRITICAL 8, MODERATE 13) — FIXABLE, verified
Coverage: PEMS p.123-125 (all rows, Asthma/Stridor/Bronchiolitis/Pulmonary Edema subsections, pearls); Nitroglycerin drug sheet. All 16 site rows and pearls compared. Pearl line 699 is truncated in the read tool output (tail not visible).

| ID | Row | Field | PEMS source | Converted | Severity | Required fix |
|---|---|---|---|---|---|---|
| C1-01 | 1 | Provider Level (EMR) | "EMR Follow Universal Patient Care" | EMT ● | MODERATE | EMR ● |
| C1-02 | 2 | Provider Level (EMR) | "EMR Perform a focused evaluation" | EMT ● | MODERATE | EMR ● |
| C1-03 | 4 | Provider Level (EMR) | "EMR Provide supplemental oxygen to maintain SpO2 > 94%" | EMT ● | MODERATE | EMR ● |
| C1-04 | 4 | Threshold | "maintain SpO2 > 94%" | "target 88-92%" (COPD) | MODERATE | Remove or owner ruling |
| C1-05 | 6 | Provider Level | "EMT Consider non-invasive (CPAP)" | EMT blank; A/I MC; P blank | CRITICAL | EMT/A/I/P standing |
| C1-06 | 6 | MC bracket | (no MC bracket in PEMS) | MC at A and I; pearl 3 | MODERATE | Remove MC at A/I |
| C1-07 | 7 | Missing levels (SGA) | "EMT ... invasive (SGA)" | all blank | CRITICAL | EMT/A/I/P ● |
| C1-08 | 8 | Provider Level (I) | "I Consider invasive ventilatory support via endotracheal intubation" | P only | CRITICAL | I ● (P for <12) |
| C1-09 | 9 | Provider Level (A) | "A Obtain IV/IO access" (Universal p.50) | I/P ● | MODERATE | A ● (inferred) |
| C1-10 | 11 | Provider Level | "A Administer: ... Epinephrine 3 mg [1 mg/mL] nebulized" | A MC, I MC, P blank | CRITICAL | A/I/P standing |
| C1-11 | 11 | Condition | "For moderate to severe symptoms, also administer" | "Administer simultaneously" | MODERATE | Restore condition |
| C1-12 | 12 | Missing levels | "A Provide suctioning ... 0.9% Sodium Chloride, 6 mL nebulized" | all blank | MODERATE | A/I/P ●; add suction step |
| C1-13 | 13 | Missing levels | "A Administer: ADULT: Nitroglycerine 0.4 mg SL" | all blank | CRITICAL | A/I/P ● (inferred) |
| C1-14 | 13 | Threshold | "(MAP 65 mmHg)" | "MAP >65" | MODERATE | MAP >=65 |
| C1-15 | absent | Contraindication | "assess for the recent use of PDE inhibitors" (Nitro drug sheet: PDE inhibitors contraindicated) | absent in respiratory folder | CRITICAL | Add PDE contraindication + IV/SBP/MAP prerequisites |
| C1-16 | absent | Missing row | "I Administer: ADULT: Furosemide (Lasix) 40 mg IV/IO slow push" | absent | MODERATE | Add row at I (inferred) |
| C1-17 | 14 | Missing levels (Mg) | "I For severe symptoms ... Magnesium Sulfate 2 g" | all blank; refers to Asthma | CRITICAL | I/P ● |
| C1-18 | 16 | Provider Level (BVM) | "EMT Support respirations with BVM" (Airway p.239) | P only | CRITICAL | EMT/A/I ● |
| C1-19 | absent | Pearl | "Use caution when administering epinephrine ... congestive heart failure" | absent | MODERATE | Add pearl |
| C1-20 | absent | Pearl | "wheezing may paradoxically worsen before improving" | absent | MODERATE | Add pearl |
| C1-21 | absent | Pearl | "RSI is not addressed in PEMS regional protocols" | absent | MODERATE | Add RSI note |

Un-sourced, not counted: row 3 (continuous monitoring, EMT+), row 5 (positioning), row 10 (fluid bolus with MC at A/I — owner review), row 15 (cardiac ischemia referral), pearls 5, 8, 9, 10.

## 03_Asthma_COPD_Reactive_Airway_PROC.md (12: CRITICAL 4, MODERATE 8) — FIXABLE, verified
Coverage: PEMS Asthma subsection (p.123-124), Stridor epinephrine/methylprednisolone (p.124), CPAP procedure and RD pearls (p.125). All 11 rows and 7 pearls compared. Verified with no finding: row 3 albuterol (EMT+, 3 mL 0.083%, repeat as necessary); row 4 ipratropium (EMT+, 3 mL 0.02%, once); row 7 BVM; pearl 4 pediatric max doses.

| ID | Row | Field | PEMS source | Converted | Severity | Required fix |
|---|---|---|---|---|---|---|
| C1-22 | 1 | Provider Level (EMR) | RD R1 "EMR Follow Universal" | EMT ● | MODERATE | EMR ● |
| C1-23 | 2 | Provider Level and threshold | "EMR ... maintain SpO2 > 94%" | EMT ●; ">= 94%" | MODERATE | EMR ●; > 94% |
| C1-24 | 5 | Provider Level (A) | "A For moderate to severe symptoms ... Methylprednisolone 125 mg" | I/P ● | MODERATE | A ● |
| C1-25 | 6 | Provider Level (I) | "I For severe symptoms ... Magnesium Sulfate 2 g" | P only | CRITICAL | I ● |
| C1-26 | 6 | Trigger | "For severe symptoms" | "unresponsive to initial therapy" | MODERATE | Replace trigger |
| C1-27 | 8 | Provider Level (EMT, A) | CPAP procedure (red-dot all levels); RD R4 EMT | I/P ● only | CRITICAL | EMT ● and A ● |
| C1-28 | 8 | Contraindications | 8 PEMS CPAP contraindications | 3 listed (pneumothorax, hypotension, GCS, etc. omitted) | CRITICAL | Full list |
| C1-29 | 8 | Settings | "PEEP 5 ... up to 10 cmH2O (I/P only)" | "Initiate 5-10" | MODERATE | Initial 5; 10 at I/P |
| C1-30 | 9 | Provider Level (EMT) | "A Administer: Epinephrine 3 mg [1 mg/mL] nebulized" | EMT ● | CRITICAL | Blank EMT |
| C1-31 | 10 | Provider Level (A) | "A For moderate to severe symptoms ... Methylprednisolone" | I/P ● | MODERATE | A ● |
| C1-32 | absent | Pearl | epinephrine-in-CHF caution | absent | MODERATE | Add pearl |
| C1-33 | absent | Pearl | wheeze paradox | absent | MODERATE | Add pearl |

## 03_Pneumothorax_PROC.md (9: CRITICAL 1, MODERATE 8) — MANUAL, verified=false
Coverage: no PEMS "Pneumothorax" title exists. Audited against Chest Decompression procedure (p.243), CPAP contraindications (p.245-246), Airway Management pearls (p.239-240), RD pearl (p.125). Findings are limited to these; this is not a full protocol audit.

| ID | Row | Field | PEMS source | Converted | Severity | Required fix |
|---|---|---|---|---|---|---|
| C1-34 | 3 | Provider Level (EMR) | "EMR Provide supplemental oxygen" | EMT ● | MODERATE | EMR ● |
| C1-35 | 1 | Provider Level (EMR) | "EMR Scene Safety / PPE" (Universal p.49) | EMT ● | MODERATE | EMR ● |
| C1-36 | 2 | Provider Level (EMR) | "EMR Initial Assessment" (Universal p.49) | EMT ● | MODERATE | EMR ● |
| C1-37 | 4 | Provider Level (I) | "I Consider continuous cardiac monitoring" (Universal p.50) | A ● for monitoring | MODERATE | I+ for monitoring (inferred) |
| C1-38 | 5 | Provider Level (EMR) | "EMR Provide suctioning as needed" (Airway p.239) | A+ | MODERATE | EMR/EMT ● for suction |
| C1-40 | 9 | Trigger | "evidence of significant blunt or penetrating thoracoabdominal trauma" | "suspicion of thoracoabdominal trauma" | MODERATE | Restore trigger |
| C1-41 | 10 | Provider Level (I) | "I Reassess the patient ... consider repeating" | EMT ● | MODERATE | Owner question |
| C1-42 | 13 | Provider Level (I) | "I Consider endotracheal intubation" (ETI I >=12) | P only | CRITICAL | I ● |
| C1-43 | absent | Pearls | "failure rate of up to 50%"; "assumed ... pneumothorax regardless of air return" | absent | MODERATE | Add pearls |

Un-sourced, not counted: row 7 "3.25 inch" needle (PEMS says "longest available"), row 10 catheter patency, row 12 fluid/vasopressor thresholds (Hypotension protocol, out of batch), row 14–15 transport/monitoring.

## 03_Respiratory_Arrest_PROC.md (15: CRITICAL 10, MODERATE 5) — MANUAL, verified=false
Coverage: no PEMS "Respiratory Arrest" title. Audited against Airway Management (p.239-240), ETI (p.247-248), Sedation Post Advanced Airway (p.55, Jan 2025), Capnography (p.241). Rows 11, 12, 10 and 58 use inferred decodes from flattened tokens.

| ID | Row | Field | PEMS source | Converted | Severity | Required fix |
|---|---|---|---|---|---|---|
| C1-44 | 1 | Provider Level (EMR) | "EMR Follow Universal" | EMT ● | MODERATE | EMR ● |
| C1-45 | 5 | Provider Level (EMR) | "EMR Provide suctioning as needed" | EMT ● | MODERATE | EMR ● |
| C1-46 | 5 | Missing step | "100% Oxygen via NRB or BVM for 3 minutes" (ETI p.247) | "Pre-oxygenate before any airway manipulation" | MODERATE | Add 100% O2 for 3 min |
| C1-47 | 6 | Provider Level (EMT) | "EMT Support respirations with BVM" | A/I/P ● | CRITICAL | EMT ● |
| C1-48 | 7 | Provider Level (EMT) | "EMT ... Use in-line EtCO2 ... Adjust tidal volume" | A+ | MODERATE | EMT ● |
| C1-49 | 8 | Provider Level (I) | "I If apneic and >=12 years old: consider endotracheal intubation" | P only | CRITICAL | I ● |
| C1-50 | 9 | Provider Level (P) | "P Orally intubate. Patients <12 years old" | all blank | CRITICAL | P ● |
| C1-51 | 10 | Provider Level (I) | "EMT I Foreign body airway obstruction: ... perform laryngoscopy" | P only | CRITICAL | I ● (inferred) |
| C1-52 | 11 | Provider Level (P) | "IP If unable to intubate and unable to oxygenate ... Surgical Airway" | all blank | CRITICAL | P ● (inferred) |
| C1-53 | 12 | Provider Level (I) | "I Verify placement ... capnography and auscultation" | P only | CRITICAL | I ● (inferred) |
| C1-54 | 13 | Provider Level (EMT) | "EMT Monitor ET tube placement ... continuous box-waveform ETCO2" | P only | CRITICAL | EMT/A/I ● |
| C1-55 | 14 | Provider Level (I) | "I Administer: ADULT: Fentanyl 25-50 mcg" | all blank | CRITICAL | I/P ● |
| C1-56 | 15 | Provider Level (I) | "I If Fentanyl is not sufficient ... Midazolam 2.5 mg" | all blank | CRITICAL | I/P ● |
| C1-57 | absent | MC requirement | "I MC Contact Medical Control ... agitation" (bare MC) | absent | CRITICAL | Add bare-MC row (inferred) |
| C1-58 | absent | Missing row | "I Prepare equipment: IV/IO access; ET tube ..." (ETI p.247) | absent | MODERATE | Add row at I (inferred) |

Un-sourced, not counted: 6–7 mL/kg tidal volume, 10–12 breaths/min, "14G 3.25 inch" surgical airway device, recovery-position wording. Pearls 1–8 verified where PEMS text exists.

## 03_Upper_Airway_Obstruction_PROC.md (8: CRITICAL 4, MODERATE 4) — MANUAL, verified=false
Coverage: no PEMS "Upper Airway Obstruction" title. Audited against FBAO text in Airway Management (p.239-240), RD Stridor (p.124), ETI (p.247-248), Sedation (p.55). Site rows 3–8 (thrusts and unconscious positioning/BLS adjuncts) match PEMS and are not counted.

| ID | Row | Field | PEMS source | Converted | Severity | Required fix |
|---|---|---|---|---|---|---|
| C1-59 | 1 | Provider Level (EMR) | "EMR Follow Universal" | EMT ● | MODERATE | EMR ● |
| C1-60 | 9 | Provider Level (EMR) | "EMR Provide suctioning as needed" | EMT ● | MODERATE | EMR ● |
| C1-61 | 10 | Provider Level (EMT) | "EMT Support respirations with BVM" | A/I/P ● (row title says EMT and above) | CRITICAL | EMT ● |
| C1-62 | 11 | Provider Level (I) | "I Foreign body airway obstruction: perform laryngoscopy" | P only (row title says I/P) | CRITICAL | I ● (inferred) |
| C1-63 | 12 | Bracket and level | "I If apneic and >=12 years old" (no MC) | "[P]" MC; I blank | CRITICAL | I ● (inferred) and remove [P] |
| C1-64 | 13 | Bracket and dose | "I Administer: Fentanyl 25-50 mcg; Midazolam 2.5 mg" (no MC) | "[I]" MC; fentanyl 25 mcg | MODERATE | Remove [I]; 25–50 mcg (inferred) |
| C1-65 | 14 | Bracket | no PEMS expanding-hematoma row | "[I]" MC | MODERATE | Remove bracket unless medical director directs (inferred) |
| C1-66 | absent | Missing row | "A Administer: Epinephrine 3 mg [1 mg/mL] nebulized" (RD Stridor p.124) | absent | CRITICAL | Add epinephrine and methylprednisolone rows at A (inferred) |

Un-sourced, not counted: row 2 scene/recognition; pearls 5–8 (no blind sweep, partial vs complete, post-obstruction transport, expanding-hematoma) have no PEMS text in this section.

## Count reconciliation
- Discrepancies in JSON: 65 (21 + 12 + 9 + 15 + 8). Table rows in this file: 65. Lines in fixlist: 65.
- By severity: CRITICAL 27 (8 + 4 + 1 + 10 + 4); MODERATE 38 (13 + 8 + 8 + 5 + 4); MINOR 0.
- Inferred decodes: 15 (RD 3; Pneumothorax 2; Respiratory Arrest 5; Upper Airway 5).
- count_reconciled: true
