# Batch F2 — Administrative protocols + Universal Patient Care vs PEMS2024

Read-only audit (reviewer, no shell). PEMS source: `pems_chunks/PEMS2024_full.txt` (page markers used for page numbers). Site files read in full. Method and severity policy: `work/00_method_and_notes.md`. Administrative protocols are not level-gated, so their level columns were not compared; only the Universal Patient Care file was level-checked.

**Totals: 55 discrepancies — CRITICAL 8, MODERATE 25, MINOR 22.** Status: 1 VERIFIED (Pediatric transport), 4 FIXABLE with verified=true or false as noted, 1 MANUAL (Restraint). Inferred level decodes: 0.

Truncation caveat: several PEMS passages are cut off in the flattened text (Trauma p.44 step 3, Restraint p.31 chemical procedure, Death p.22 pearls, Communications p.17 MCI procedure, Universal p.50 SpO2 row). Those tails are listed under each protocol and need a PDF check. The PDF itself could not be read (OCR-needed pages).

---

## docs/protocols/administrative/01_Trauma_Field_Triage_PROC.md

Coverage: PEMS p.43-45 read in full (p.46 blank). Physiologic, anatomic, mechanism, special considerations, procedure and pearls checked. Truncated: p.44 step 3 ("If HEMS is delayed or unavailable, transport patients meet... [truncated]"). Status FIXABLE, verified=false.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F2-01 | absent | Physiologic Criteria - Respiratory rate | Respiratory rate of less than 10 or greater than 29 breaths per minute (less than 20 breaths per minute in infants less than 1 year old) | (absent) | CRITICAL | Add RR criterion with infant <20/min threshold. |
| F2-02 | absent | Mechanism - Falls | Falls o Adults – greater than 20 feet o Children less than 15 years old – greater than 10 feet, or two to three times child’s height | (absent) | CRITICAL | Add falls mechanism criteria. |
| F2-03 | absent | Mechanism - High-risk auto intrusion | High-risk auto crash o Intrusion – more than 12 inches into occupant site or more than 18 inches into any site | (absent) | CRITICAL | Add intrusion thresholds (>12 in occupant site; >18 in any site). |
| F2-04 | absent | Anatomic Criteria (whole block) | Penetrating injury...; Flail chest; Two or more proximal long-bone fractures; Crushed, degloved, or mangled extremity; Amputation proximal to wrist and ankle; Pelvic fracture; Open or depressed skull fracture; Paralysis | (absent) | CRITICAL | Add the 8-item anatomic criteria block. |
| F2-05 | absent (criteria bullet) | Mechanism - Auto vs pedestrian/bicyclist | Auto versus pedestrian/bicyclists - thrown, run over, or with significant impact (greater than 20 mph) | Auto vs pedestrian/bicyclist (thrown, run over, >20 mph) | MODERATE | Reword to PEMS; confirm in PDF whether >20 mph qualifies thrown/run-over (ambiguous). |
| F2-06 | 5 | Routing - Mechanism-only | A trauma patient who meets any of the following criteria shall be transported to the closest appropriate trauma center within a 30-minute ground transport time. | Mechanism-Only Routing: If patient meets mechanism criteria but NOT physiologic/anatomic criteria, contact Medical Control to determine destination. | CRITICAL | Mechanism criteria alone route to closest appropriate trauma center; MC is additive, not a gate. |
| F2-07 | 4 | HEMS consideration conditions | HEMS should be considered: a. if patient meets the clinical triage criteria ... Level I or II; b. if patient requires a level of care greater than ... AND HEMS can be on scene in a time shorter than ... ground unit | Out of Range (Ground) / HEMS Consideration: ... transport to closest hospital UNLESS HEMS can deliver to trauma center faster. | MODERATE | Replace with PEMS (a)/(b) conditions and "should be considered" wording. |
| F2-08 | 4 | HEMS request authority | Technicians can request HEMS transport without authorization by medical control. | (absent) | MODERATE | Add technician HEMS-request authority. |
| F2-09 | 6 | Burn criteria - full-thickness | Consider transport to a burn center (Sentara Norfolk General Hospital or VCU Medical Center) ... Partial-thickness burn of greater than 10% BSA; Electrical burns, including lightning injury; Full-thickness burns; Circumferential burns; Chemical burns | Burns meeting criteria (full/partial >10% TBSA, circumferential, electrical/chemical, inhalation, face/hands/feet/genitals) go to Burn Center. | CRITICAL | Restore full-thickness burns as a stand-alone criterion (no %BSA threshold); restore lightning and chemical. |
| F2-10 | 6 | Burn criteria - additions | (same PEMS burn list as F2-09; no inhalation or face/hands/feet/genitals criterion) | Burns meeting criteria (... inhalation, face/hands/feet/genitals) go to Burn Center. | MODERATE | Remove non-PEMS criteria or cite regional source. |
| F2-11 | 6 | Burn center destinations | Consider transport to a burn center (Sentara Norfolk General Hospital or VCU Medical Center) | (absent) | MINOR | Name the burn centers. |
| F2-12 | 7 | Pediatric trauma destination | Severely injured pediatric patients should be transferred to a trauma center or pediatric trauma center; pearl: Consider transport to a pediatric center (CHKD or VCU Medical Center) | Transport severely injured pediatric patients to a pediatric trauma center (CHKD or VCU). | MODERATE | Restate as trauma center or pediatric trauma center; pediatric center "consider" wording. |
| F2-13 | 3 | Transport immediately / document delay | Transport immediately; otherwise document the reason for the delay. | Physiologic Criteria Met Routing: Transport to closest appropriate trauma center (Level I or II) within 30-min ground transport. | MINOR | Add "document reason for delay". |
| F2-14 | absent | Pregnancy wording | Pregnancy – ... should be considered for transport to trauma center or a hospital with obstetrical resources. | Pregnancy: >20 weeks pregnant → trauma center or OB-capable hospital. | MINOR | Use "should be considered for". |

**Totals (Trauma): 14 — CRITICAL 6, MODERATE 5, MINOR 3.**

---

## docs/protocols/administrative/01_ALS_Release_to_BLS_PROC.md

Coverage: PEMS p.15 read in full (no truncation; p.16 blank). Every procedure bullet and policy sentence checked against the 8 site rows and pearls. Status FIXABLE, verified=true.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F2-15 | 8 | QA/QI review authority | Any ALS Release to BLS must be reviewed by the agency Quality Assurance/Quality Improvement process. | Any ALS Release to BLS must be reviewed by the Officer or Acting Officer the following day, per departmental SOP. | MODERATE | Restore agency QA/QI process; officer/next-day step only as a labelled local SOP. |
| F2-16 | absent | QA/QI quarterly reporting | A determination of inappropriate release by the Quality Assurance/Quality Improvement review should be reported, quarterly, to the PEMS PI Committee. | (absent) | MODERATE | Add quarterly PI Committee reporting. |
| F2-17 | absent | Policy scope | This policy applies to all patients where patient contact has been made and the ALS provider desires to release the patient to a BLS provider. | (absent) | MINOR | Add scope sentence. |
| F2-18 | absent | Pearl 3 - MC wording | The ALS provider must contact Medical Control when there is a concern of the appropriateness of the release | Always consult Medical Control (Poquoson OMD) for edge cases or when there is any concern ... | MINOR | Align to PEMS or label the "edge cases" sentence as local. |

**Totals (ALS): 4 — CRITICAL 0, MODERATE 2, MINOR 2.**

---

## docs/protocols/administrative/01_Patient_Restraint_PROC.md

Coverage: PEMS p.31-32 read; physical restraint procedure, restraint guidelines and documentation procedure checked. **Not verifiable:** PEMS p.31 CHEMICAL RESTRAINT PROCEDURE is truncated after "Assess vital signs within the first 5 minutes and thereafter as appropriate (at least every 10 minutes and prior to any repeat dose of medication), or document reason for lack of vital... [truncated]". Site rows 7 and 8 (ECG/12-lead, IN meds, IV/IO, sedation referral) could not be compared. Status MANUAL, verified=false. Human PDF check of PEMS p.31 required.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F2-19 | 3 | Backboard orientation | Place the patient face up on a long backboard – NEVER PRONE. | Place patient supine on backboard NEVER PRONE. | MINOR | Change to "face up on a long backboard". |
| F2-20 | 4 | Backboard straps | Secure the backboard to the stretcher using the straps on the stretcher, particularly the over-the-shoulder straps. | Secure backboard to stretcher. | MINOR | Add stretcher straps / over-the-shoulder straps. |
| F2-21 | absent (differential) | Documentation - LE accompaniment | Which law enforcement officer was present? If patient was transported in handcuffs, which officer accompanied patient to ED ... If no law enforcement officer accompanied patient, why? | Law enforcement present/accompanied patient to ED | MINOR | Expand to the three PEMS prompts. |

**Totals (Restraint): 3 — CRITICAL 0, MODERATE 0, MINOR 3.**

---

## docs/protocols/administrative/01_Death_Criteria_for_Withholding_Resuscitation_PROC.md

Coverage: PEMS p.21 read in full; PEMS p.22 read through the withholding protocol rows. PEMS p.22 PEARLS truncated after "For POST (Physician Orders for Scope of Treatment) forms, Sec..." — any further POST/DNR pearls unverified. Status FIXABLE, verified=false. The site's 20-minute TOR criteria are sourced to PEMS V-Fib p.66 ("Consider contacting Medical Control to request TOR if the arrest was not witnessed by EMS and after 20 minutes of continuous CPR"), not a finding here.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F2-22 | absent (pearls) | Hypothermia pearl | Resuscitation efforts and transport to the emergency department are indicated for any patient having suspected hypothermia. | (absent) | CRITICAL | Add hypothermia pearl: do not withhold in suspected hypothermia. |
| F2-23 | absent (pearls) | Previously diagnosed condition | Consider patient's previously diagnosed medical condition. | (absent) | MODERATE | Add pearl. |
| F2-24 | absent | Default full-resuscitation rule | In accordance with Commonwealth of Virginia law, full resuscitation measures shall be undertaken for all victims of cardiopulmonary arrest except in the presence of one or more of the indications of death | (absent) | MODERATE | Add default rule above the criteria list. |
| F2-25 | absent | Physician verbal order at death | EMS providers shall honor a direct verbal order from a physician who is present ... Record physician’s name and time of order on PCR. | (absent) | MODERATE | Add verbal-order row and PCR documentation. |
| F2-26 | absent | "Other" DNR orders / accompaniment | Providers shall honor any form ... Alternate DDNR Jewelry ... "other" DNR Orders including out of state DNR forms; this document must accompany the patient to the hospital. | Valid DDNR from any State ...; ALERT bracelet/necklace (no "other DNR orders"; no accompany-to-hospital requirement) | MODERATE | Add "other DNR orders" and accompany-to-hospital requirement. |
| F2-27 | absent (facility bullet) | No-form pathway / doubt rule | If there is any doubt as to the applicability or validity of a DNR ... begin CPR and contact Medical Control immediately (Patient Refusal p.28); DDNR must be in a patient's chart for nursing home or hospice calls (Death p.22) | If the form cannot be located but facility staff confirm a valid DNR exists, contact Medical Control for guidance. | MODERATE | Replace with PEMS: DDNR in chart; any doubt -> begin CPR and contact MC immediately. |
| F2-28 | absent (living will bullet) | MC review of reasons | Be prepared to review the reason(s) why resuscitation efforts may not be indicated (i.e. terminal illness). | (absent) | MINOR | Add MC review item. |
| F2-29 | absent | PCR documentation - findings/history | Document physical findings and patient history on the PCR form. | (absent) | MINOR | Add PCR documentation step. |
| F2-30 | absent (facility copy) | "Faxed copy" | This form ... can be a photocopy. (DDNR digital copy permitted) | photocopy, digital copy, or faxed copy is acceptable | MINOR | Drop "faxed" or cite source. |

**Totals (Death): 9 — CRITICAL 1, MODERATE 5, MINOR 3.**

---

## docs/protocols/administrative/01_Infant_Abandonment_PROC.md

Coverage: PEMS p.25 read in full (p.26 blank). Verified=true; status FIXABLE.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F2-31 | absent (pearl) | Immunity exception omitted | ...shall be immune from civil liability or criminal prosecution ... unless such injury or other damage is the result of gross negligence or willful misconduct by such personnel. | Virginia Safe Haven Law grants immunity from civil or criminal liability to receiving providers. | MODERATE | Add gross negligence / willful misconduct exception. |
| F2-32 | absent | Citation | Reference § 8.01-226.5:2 | Reference §18.2-371, §18.2-371.1, §40.1-103 (overview only) | MINOR | Add § 8.01-226.5:2. |
| F2-33 | absent (pearl) | Non-PEMS pearl | (not in PEMS) | Ensure safe and supportive environment for the surrendering parent if present. | MINOR | Remove or label as local addition. |

**Totals (Infant): 3 — CRITICAL 0, MODERATE 1, MINOR 2.**

---

## docs/protocols/administrative/01_Communications_PROC.md

Coverage: PEMS p.17-20 read. Regional resources (p.19-20) compared digit-by-digit: 6 air, 10 COR, 10 other entries — all match; none omitted. Pre-arrival list (p.18) and comm-failure criteria matched. **Not verifiable:** PEMS p.17 MCI procedure truncated after "...communicate patient information direc... [truncated]". Status FIXABLE, verified=false.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F2-34 | 4 | MCI as-written protocol grant | Once communication has been established with the coordinating emergency department, a request to follow Regional Medical Protocols as written can be granted by Medical Control. | MCI comms suspension/supervisor relay: Routine ambulance-to-ED communications suspended. Transport group supervisor communicates directly to coordinating ED. | MODERATE | Add MC as-written grant step. |
| F2-35 | 6 | Comm failure - MC Incident Form / OMD | Complete and submit a copy of the Medical Control Incident Form. ... PCR must be provided to your Operational Medical Director (OMD) within 48 hours of the occurrence. | Document comm failure ... on the PCR. Review with Officer/Acting Officer per department SOPs. | MODERATE | Add MC Incident Form; 48-hour OMD submission; OMD as review authority. |
| F2-36 | 6 | Documentation - location | nature and location of the communication problem | nature of comms problem | MINOR | Add "and location". |
| F2-37 | absent (pearl 3) | HEAR consultation limit | The HEAR system may be used for physician consultation only when COR ... access is not available. | (absent) | MINOR | Add HEAR limit. |
| F2-38 | 1 | HEAR report format | HEAR system reporting should be brief; a detailed patient report should be given ... upon arrival. Reports should follow the recommended regional format. | (absent) | MINOR | Add these sentences. |
| F2-39 | absent (pearl 5) | Resource source contradiction | REGIONAL RESOURCES & TELEPHONE NUMBERS (PEMS p.19-20 listed in full) | For contact information ..., refer to the department's internal contact list. | MINOR | Delete sentence; fix duplicate "5." pearl numbering. |

**Totals (Communications): 6 — CRITICAL 0, MODERATE 2, MINOR 4.**

---

## docs/protocols/administrative/01_Safe_Transport_of_Pediatric_Patients_PROC.md

No discrepancies — VERIFIED.

Coverage: PEMS p.33 read in full (no truncation; p.34 blank). Rows checked: row 1 secure equipment; row 2 safe driving; row 3 child restraint <40 kg (88 lb); row 4 all EMS providers use restraints; row 5 secure parents/caregivers with belts; row 6 alternative transport for non-patients; row 7 comfort/stress measures. Pearls checked: no holding by parents; ambulances not exempt from child safety law; no unrestrained passengers; trauma-criteria children in child restraint unless immobilization. Verified=true.

---

## front-matter/Universal Patient Care.md (PEMS p.49-53, level-gated)

Coverage: PEMS p.49-50 level tokens decoded for all 11 rows. Level tokens were bare codes immediately before each row text, so level_decode is direct for every row (0 inferred). PEMS p.50 "Assess SpO2" row truncated after "Consider assessing EtCO2 and/or SpC... [truncated]" — remainder unverified. PEMS p.51-53 (GCS, infant age, AEIOU TIPS, SMASHED 2) checked. Status FIXABLE, verified=false.

| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |
|---|---|---|---|---|---|---|
| F2-40 | absent | Self-referential row | PROTOCOL EMR Follow Universal Patient Care / Initial Patient Contact protocol. | (absent) | MINOR | Optional note. |
| F2-41 | 1 | Level - Scene Safety / PPE | EMR EMR Scene Safety / PPE / Patient Contact | EMR blank; EMT, A, I, P • | MODERATE | Set EMR •. |
| F2-42 | 2 | Level - Initial Assessment | EMR EMR Initial Assessment | EMR blank; EMT, A, I, P • | MODERATE | Set EMR •. |
| F2-43 | 3 | Level - Airway/Oxygenation | EMR EMR Ensure Adequate Airway, Oxygenation, and Ventilation | EMR blank; EMT, A, I, P • | MODERATE | Set EMR •. |
| F2-44 | 4 | Level - Vital Signs | EMR EMR Vital Signs | EMR blank; EMT, A, I, P • | MODERATE | Set EMR •. |
| F2-45 | 5 | Level - Assess SpO2 | EMR EMT Assess SpO2. | EMT blank; A, I, P • | MODERATE | Set EMT •. |
| F2-46 | 6 | Level - Consider 12-Lead ECG | EMT Consider 12-Lead ECG. ... Acquire within 5 minutes of patient contact. | EMT blank; A, I, P • | CRITICAL | Set EMT •. 12-lead within 5 min drives STEMI recognition; same rating as Chest Pain ECG finding. |
| F2-47 | 7 | Level - Medication Administration | EMT EMT Medication Administration | EMT blank; A, I, P • | MODERATE | Set EMT •. |
| F2-48 | 8 | Level - IV/IO access | EMT A Establish IV / IO access when indicated. | A blank; I, P • | MODERATE | Set A •. |
| F2-49 | 9 | Level - Continuous cardiac monitoring | A I Consider continuous cardiac monitoring. | P only | MODERATE | Set I •. |
| F2-50 | 10 | Level - Transport | I EMT Transport | EMT blank; A, I, P • | MODERATE | Set EMT •. |
| F2-51 | 11 | Level - Refer to protocols / MC | EMR EMR Refer to relevant and appropriate protocols. | EMR blank; EMT, A, I, P • | MODERATE | Set EMR •. |
| F2-52 | 11 | MC wording | consider contacting Medical Control | contact Medical Control | MINOR | Change to "consider contacting". |
| F2-53 | absent | Cross-references | Refer to Spinal Motion Restriction (row 2); Airway Management and Ventilatory support (row 3); Pharmacology (row 7); Chest Pain (Cardiac) protocol (row 6); Intraosseous (IO) Access (row 8); Patient Refusal of Treatment/Transport (row 10) | (absent) | MINOR | Add named cross-references. |
| F2-54 | 4 | Monitoring instruction | Closely monitor the patient, paying specific attention to their condition immediately before or after an intervention. | (absent) | MINOR | Add sentence. |
| F2-55 | absent (pearl) | SMASHED 2 wording | Mental illness: Acute psychosis, medication noncompliance, mania, depression; Accident: Head trauma, CVA, cerebral contusion, intracranial hemorrhage | Mental illness (Acute psychosis, mania, depression); Accident (Head trauma, CVA, cerebral contusion, hemorrhage) | MINOR | Add "medication noncompliance" and "intracranial". |

**Totals (Universal): 16 — CRITICAL 1, MODERATE 10, MINOR 5.**

---

## Count reconciliation

| Protocol | CRITICAL | MODERATE | MINOR | Total |
|---|---|---|---|---|
| Trauma Field Triage | 6 | 5 | 3 | 14 |
| ALS Release to BLS | 0 | 2 | 2 | 4 |
| Patient Restraint | 0 | 0 | 3 | 3 |
| Death & Withholding | 1 | 5 | 3 | 9 |
| Infant Abandonment | 0 | 1 | 2 | 3 |
| Communications | 0 | 2 | 4 | 6 |
| Safe Transport Pediatric | 0 | 0 | 0 | 0 |
| Universal Patient Care | 1 | 10 | 5 | 16 |
| **Total** | **8** | **25** | **22** | **55** |

Table rows in section B: 14 + 4 + 3 + 9 + 3 + 6 + 0 + 16 = 55. JSON discrepancies: 55 (F2-01 to F2-55). Fixlist lines: 55. count_reconciled = true.
