# Needs authoring — everything `--apply` refused to touch

`pems_level_scan.py --apply` writes only EMR/EMT/A/I/P level cells. The
findings below are clinical-prose, dose, contraindication, destination or
missing-row work: they change what the protocol *says*, not who may perform it,
and they need an author (or the OMD) — not a script. Source: the audit FIXLIST.

Total: **489** items across **54** files.

## protocols/administrative/01_ALS_Release_to_BLS_PROC.md

- `AUD-0216` [MODERATE] row row 8 — current: "Officer or Acting Officer, next day" | correct: "Agency QA/QI process (no officer/timeline specified)" | Restore 'agency Quality Assurance/Quality Improvement process'; keep the officer/next-day step only as a labelled local SOP addition.
- `AUD-0217` [MODERATE] row row absent — current: "No reporting step" | correct: "Quarterly report of inappropriate-release determinations to PEMS PI Committee" | Add quarterly reporting of inappropriate-release determinations to the PEMS PI Committee.
- `AUD-0618` [MINOR] row row absent — current: "Scope not stated as patient-contact-made" | correct: "Applies once patient contact has been made" | Add the PEMS policy scope sentence.
- `AUD-0619` [MINOR] row row absent — current: "'Always consult ... for edge cases' (non-PEMS broadening)" | correct: "Contact MC when there is a concern about appropriateness of release" | Align to PEMS wording or label the 'edge cases' sentence as a local addition.

## protocols/administrative/01_Abuse_Recognition_and_Mandated_Reporting_PROC.md

- `AUD-0218` [MODERATE] row row 4 — current: "DSS or APS; law enforcement only if imminent danger" | correct: "report elder abuse types to APS AND law enforcement" | Change step 4 to 'Report to APS and law enforcement (and local DSS per PEMS)'. Human may escalate: this is a mandated-reporting compliance gap, not a clinical one, so it is rated MODERATE under the batch severity rule.
- `AUD-0219` [MODERATE] row row 4 — current: "no timing requirement" | correct: "report IMMEDIATELY" | Add 'immediately' to step 4.
- `AUD-0220` [MODERATE] row row 4 — current: "trigger = 'imminent danger of death/serious injury or death'" | correct: "trigger includes suspected sexual abuse, and death, serious bodily injury or disease believed to result from abuse or neglect (no 'imminent' qualifier)" | Rewrite the trigger to match the PEMS bullet. The bullet's placement is inferred from flattened text, so eyeball the PDF before editing. | inferred: confirm in P
- `AUD-0221` [MODERATE] row row 5 — current: "'Notify local DSS or CPS' (no timing, no locality)" | correct: "report IMMEDIATELY to local DSS (locality where child resides or abuse occurred) or to the 24-hour VDSS CPS hotline" | Add 'immediately' and the locality rule (or the 24-hour VDSS CPS hotline) to step 5.
- `AUD-0222` [MODERATE] row row 6 — current: "5-day deadline only" | correct: "notice IMMEDIATELY (statute), with the 5-day written report requirement" | Add the statutory 'immediately' notice requirement alongside the 5-day report.
- `AUD-0620` [MINOR] row row absent — current: "no child-abuse hotline number anywhere in the protocol" | correct: "800-552-7096 (VDSS 24-hour CPS hotline)" | Add '24-hour CPS hotline 800-552-7096' to the pearls. Rated MINOR per the phone-number rule; operationally it is the only child-abuse reporting line.

## protocols/administrative/01_Behavioral_Health_Transportation_Decision_PROC.md

- `AUD-0001` [CRITICAL] row row absent — current: "no physical-exam criteria anywhere in the protocol" | correct: "Temp > 100.4; HR < 50 or > 120; BP < 90 or > 180; RR < 12 or > 28; glucose < 70 or > 350 mg/dL; any loss of consciousness; any stroke/TIA symptoms; need for supplemental O2 or airway support" | Add the PEMS physical-exam gate verbatim as a criteria block before the 'Consider direct transport' step; any positive item means no
- `AUD-0002` [CRITICAL] row row absent — current: "not listed" | correct: "no significant trauma AND no strangulation injury required" | Add 'No significant trauma' and 'No strangulation injury' to the Signs & Symptoms / Differential criteria.
- `AUD-0003` [CRITICAL] row row absent — current: "not listed" | correct: "patient must NOT have been chemically sedated" | Add 'Has the patient been chemically sedated?' as a criterion (no -> proceed).
- `AUD-0004` [CRITICAL] row row absent — current: "no age criterion" | correct: "age 5 to 60 required for direct BH transport" | Add the age 5-60 criterion; patients outside the range go to the appropriate ED (see row absent, docs/protocols/administrative/01_Behavioral_Health_Transportation_Decision_PROC.md).
- `AUD-0005` [CRITICAL] row row absent — current: "no pregnancy branch" | correct: "pregnant -> contact RMHRC Medical Control with gestational age, prenatal care, abdominal pain, bleeding; disposition per MC / local ED" | Add the pregnancy branch: contact RMHRC Medical Control with the four items listed; note the flattened flowchart Yes/No mapping must be eyeballed in the PDF before the edit. | inferred: confirm in PDF before edit
- `AUD-0223` [MODERATE] row row 2 — current: "'a Mental Health Facility' (unnamed)" | correct: "BH Center: contact RMHRC or CHKD" | Name RMHRC and CHKD as the contacts and state that Medical Control is contacted for RMHRC, per PEMS. The CHKD number is (757) 668-8000 in the PEMS Communications list; no RMHRC number is in the readable PEMS text.
- `AUD-0224` [MODERATE] row row absent — current: "no disposition when BH direct-transport criteria are not met" | correct: "Transport to appropriate ED" | Add: 'If any criterion above is not met, transport to the appropriate ED.'

## protocols/administrative/01_Communications_PROC.md

- `AUD-0225` [MODERATE] row row 4 — current: "No MC grant of as-written protocols during MCI" | correct: "MC may grant a request to follow regional protocols as written once contact with coordinating ED established" | Add the MCI as-written protocol grant step and its effect (no repeat MC contact needed for care within level).
- `AUD-0226` [MODERATE] row row 6 — current: "No MC Incident Form; review by Officer/Acting Officer" | correct: "MC Incident Form and PCR to OMD within 48 hours; OMD may require information/meeting" | Add MC Incident Form and 48-hour OMD submission; make the OMD the review authority.
- `AUD-0621` [MINOR] row row 1 — current: "Absent" | correct: "HEAR report brief; detailed report at arrival; follow regional format" | Add these three reporting-format sentences to the HEAR row or pearls.
- `AUD-0622` [MINOR] row row 6 — current: "'nature' only" | correct: "nature and location of the communication problem" | Add 'and location' to the nature-of-problem item.
- `AUD-0623` [MINOR] row row absent — current: "Absent" | correct: "HEAR for physician consultation only when COR not available" | Add the HEAR-consultation limit to the HEAR vs COR pearl.
- `AUD-0624` [MINOR] row row absent — current: "Says to use an internal list, while the same page gives the full table" | correct: "Regional resources and numbers are listed in PEMS p.19-20" | Delete the 'internal contact list' sentence (the table is already present); also fix duplicate pearl numbering '5.'.

## protocols/administrative/01_Death_Criteria_for_Withholding_Resuscitation_PROC.md

- `AUD-0006` [CRITICAL] row row absent — current: "No hypothermia exception to withholding/termination" | correct: "Resuscitation and ED transport indicated for any patient with suspected hypothermia" | Add the PEMS hypothermia pearl to the Pearls list, next to the TOR-is-MC-only pearl, so withholding is never applied to suspected hypothermia.
- `AUD-0227` [MODERATE] row row absent — current: "Absent" | correct: "Consider previously diagnosed medical condition" | Add the PEMS pearl.
- `AUD-0228` [MODERATE] row row absent — current: "No statement that full resuscitation is the default" | correct: "Full resuscitation is default unless an indication of death is present" | Add the default-rule statement above the withholding criteria list.
- `AUD-0229` [MODERATE] row row absent — current: "No verbal-order row" | correct: "Honor direct verbal order from attending physician present at death; record name and time on PCR" | Add an intervention row for the physician verbal order and PCR documentation.
- `AUD-0230` [MODERATE] row row absent — current: "'Other' DNR orders not named; no 'must accompany the patient to the hospital'" | correct: "Honor any VA DOH-issued/approved form, including alternate jewelry, 'other' DNR orders, and out-of-state DNR forms; document must accompany patient to hospital" | Add 'other DNR orders' and out-of-state forms to the honored list, and the accompaniment-to-hospital requirement.
- `AUD-0231` [MODERATE] row row absent — current: "Staff-confirmed DNR without form -> 'contact MC' (no CPR directive in this bullet)" | correct: "DDNR must be in chart; any doubt -> begin CPR and contact MC immediately" | Replace the staff-confirmation sentence with the PEMS doubt rule: begin CPR and contact MC immediately; DDNR must be in chart.
- `AUD-0625` [MINOR] row row absent — current: "No review-of-reasons step" | correct: "MC to review reasons resuscitation may not be indicated (e.g., terminal illness)" | Add the PEMS MC review item to the living-will bullet.
- `AUD-0626` [MINOR] row row absent — current: "Absent" | correct: "Document physical findings and patient history on PCR" | Add the PCR documentation step.
- `AUD-0627` [MINOR] row row absent — current: "'faxed copy' added" | correct: "photocopy (digital copy is accepted for DDNR per PEMS); 'faxed' not stated" | Drop 'faxed' or cite the source that accepts faxed copies.

## protocols/administrative/01_Helicopter_EMS_HEMS_PROC.md

- `AUD-0232` [MODERATE] row row absent — current: "closed list with no 'not limited to' qualifier" | correct: "indications include but are not limited to STEMI, Stroke, Trauma, Burns, Critical Pediatrics, VAD" | Add 'including but not limited to' to the Indications list (the site's Overview may carry it).
- `AUD-0628` [MINOR] row row 4 — current: "'(within provider scope)' added" | correct: "IV/IO access as time allows (no scope qualifier in PEMS)" | Remove '(within provider scope)' or move it to a footnote, since PEMS has no scope qualifier.

## protocols/administrative/01_Infant_Abandonment_PROC.md

- `AUD-0233` [MODERATE] row row absent — current: "Unconditional immunity" | correct: "Immunity unless injury results from gross negligence or willful misconduct" | Add the gross negligence / willful misconduct exception to the immunity pearl.
- `AUD-0629` [MINOR] row row absent — current: "§8.01-226.5:2 not cited" | correct: "Add § 8.01-226.5:2 for immunity" | Add the immunity citation § 8.01-226.5:2.
- `AUD-0630` [MINOR] row row absent — current: "Non-PEMS pearl" | correct: "Not in PEMS - remove or label as local guidance" | Remove or label as a local addition not from PEMS.

## protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md

- `AUD-0007` [CRITICAL] row row absent — current: "no DNR section" | correct: "DNR applies only in cardiac arrest; valid DNR or DDNR jewelry required outside qualified facilities/hospice; if any doubt about a DNR in cardiac arrest, begin CPR and contact Medical Control immediately" | Add the PEMS DNR/cardiac-arrest block verbatim, including 'if any doubt ... begin CPR and contact Medical Control immediately'. Cross-reference the Death & 
- `AUD-0234` [MODERATE] row row 2 — current: "absolute criterion: no impairing condition may be present" | correct: "assess for and take into consideration any impairing condition (not an automatic bar)" | Reword HPI bullet to 'Assess for and consider any condition that may impair capacity (psychiatric illness, intoxication, CVA, hypotension, hypoglycemia, hypoxia, head trauma)'.
- `AUD-0235` [MODERATE] row row 3 — current: "no surrogate-capacity check" | correct: "ensure the surrogate has clinical decision-making capacity" | Append: 'Ensure the surrogate has clinical decision-making capacity.'
- `AUD-0236` [MODERATE] row row absent — current: "no in-loco-parentis surrogate rule" | correct: "adult caregiver of a minor may act as surrogate when parents unavailable" | Add the in-loco-parentis pearl verbatim to the pearls section.
- `AUD-0237` [MODERATE] row row absent — current: "one narrow rule (minor as parent consenting for her child)" | correct: "deemed-adult list (STD/reportable infectious disease; birth control/pregnancy/family planning; outpatient substance-abuse care; outpatient mental/emotional care) and pregnant-minor consent for herself and her child for delivery-related care" | Replace Pearl 3 with the PEMS deemed-adult list and the pregnant-minor rul
- `AUD-0631` [MINOR] row row 4 — current: "adult witness required" | correct: "adult witness 'when possible'" | Add 'when possible' after the witness requirement.

## protocols/administrative/01_Patient_Restraint_PROC.md

- `AUD-0632` [MINOR] row row 3 — current: "supine on backboard (no 'long')" | correct: "face up on a long backboard" | Change to 'face up on a long backboard'.
- `AUD-0633` [MINOR] row row 4 — current: "No strap specification" | correct: "Use stretcher straps, particularly over-the-shoulder straps" | Add 'using the stretcher straps, particularly the over-the-shoulder straps'.
- `AUD-0634` [MINOR] row row absent — current: "Single item, no handcuff/ 'why not' prompts" | correct: "Identify officer; if handcuffed, which officer accompanied; if none, why" | Expand the LE item to the three PEMS prompts.

## protocols/administrative/01_STEMI_Field_Triage_PROC.md

- `AUD-0238` [MODERATE] row row 3 — current: "< 30 minutes (PCI); > 30 minutes (row 4 HEMS); exactly 30 minutes undefined" | correct: "within 30 minutes (<= 30) -> closest PCI-capable hospital" | Change row 3 to '<= 30 minutes' and make row 4 '> 30 minutes' so the boundary is covered exactly once.
- `AUD-0239` [MODERATE] row row 4 — current: "'evaluate' HEMS transport within 30 minutes" | correct: "'Activate' HEMS when HEMS is within 30 minutes of patient location, then transport to the closest listed PCI-capable hospital with surgical capabilities" | Replace 'evaluate' with 'activate' and state the destination (closest listed PCI-capable hospital with surgical capability).
- `AUD-0635` [MINOR] row row 2 — current: "AND-only criterion in row 2" | correct: "cardiac symptoms AND (>= 1 mm ST elevation in >= 2 contiguous leads OR 'ACUTE MI' statement by qualified provider or machine)" | Add the 'OR machine ACUTE MI statement' branch to row 2 (the site's Decision Scheme section already has it, so row 2 is merely incomplete).
- `AUD-0636` [MINOR] row row absent — current: "(540) 373-0348 only" | correct: "(540) 373-0348 or (540) 741-4768" | Add the second number (540) 741-4768 to the table row.

## protocols/administrative/01_Stroke_Field_Triage_PROC.md

- `AUD-0240` [MODERATE] row row 2 — current: "treat only if < 60 mg/dL (60 mg/dL does not trigger treatment)" | correct: "glucose must be > 60 to proceed; 60 mg/dL or less -> correct per Hypoglycemia protocol" | Change row 2 to 'If 60 mg/dL or less, treat per Hypoglycemia protocol' so it matches the site's own Differential line ('Must be > 60').
- `AUD-0637` [MINOR] row row 1 — current: "goal scene time < 15 minutes" | correct: "no PEMS basis on p.37" | Remove, or footnote as an agency performance target not sourced to PEMS.
- `AUD-0638` [MINOR] row row 3 — current: "BEFAST + RACE" | correct: "RACE is the PEMS trigger; BEFAST is not on p.37" | Keep RACE as the stated trigger; label BEFAST as an agency adjunct or remove it.
- `AUD-0639` [MINOR] row row 8 — current: "no 'questions -> contact local Medical Control' instruction" | correct: "If you have questions contact local medical control." | Add: 'If you have questions, contact local Medical Control.'
- `AUD-0640` [MINOR] row row absent — current: "family contact info pearl" | correct: "no PEMS basis on p.37" | Remove, or source to an agency policy.

## protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md

- `AUD-0008` [CRITICAL] row row absent — current: "no row for emergent transport to closest hospital" | correct: "unstable patients (i-viii) -> EMERGENT transport to the CLOSEST hospital" | Add a row: 'Unstable patient (airway not protectable, severe respiratory distress unresponsive to prehospital therapy, circulatory failure, abnormal delivery, post-arrest, seizures unresponsive to midazolam, non-trauma shock, other time-critical life 
- `AUD-0009` [CRITICAL] row row absent — current: "time-critical conditions override preference 'to ensure specialized care'" | correct: "for unstable patients (1.e) the override sends to the CLOSEST hospital; specialized destinations apply to STEMI/stroke/trauma/burn (1.a-1.d)" | Split Pearl 2: unstable-patient exception (1.e) goes to the closest hospital; STEMI, stroke, trauma and burn exceptions go to the specialized destination.
- `AUD-0241` [MODERATE] row row absent — current: "no trauma-center or burn-center exception rows" | correct: "trauma-center exception (1.c) and burn-center exception (1.d)" | Add rows for trauma-center and burn-center destination exceptions, cross-referenced to the Trauma Field Triage protocol.
- `AUD-0641` [MINOR] row row 2 — current: "Poquoson Regional STEMI Plan" | correct: "PEMS Regional STEMI Plan" | Replace 'Poquoson Regional STEMI Plan' with 'PEMS Regional STEMI Plan'.
- `AUD-0642` [MINOR] row row 3 — current: "Poquoson Stroke Triage Plan" | correct: "PEMS Stroke Triage Plan" | Replace 'Poquoson Stroke Triage Plan' with 'PEMS Stroke Triage Plan'.

## protocols/administrative/01_Trauma_Field_Triage_PROC.md

- `AUD-0010` [CRITICAL] row row 5 — current: "Mechanism-only -> MC determines destination" | correct: "Mechanism criteria alone -> closest appropriate trauma center (shall be transported)" | Replace row 5 with PEMS routing: mechanism criteria met -> closest appropriate trauma center; MC consult for unclear destination only in addition to transport.
- `AUD-0011` [CRITICAL] row row 6 — current: "Full-thickness burns only when also >10% TBSA" | correct: "Partial-thickness >10% BSA; full-thickness burns (no size threshold); electrical incl. lightning; circumferential; chemical" | Restore full-thickness burns as a stand-alone burn-center criterion (no %BSA threshold) and restore lightning/chemical wording.
- `AUD-0012` [CRITICAL] row row absent — current: "RR criterion absent" | correct: "RR <10 or >29/min; <20/min in infants <1 yr" | Add RR physiologic criterion with the infant (<1 yr) <20/min threshold to Signs & Symptoms > Physiologic Criteria.
- `AUD-0013` [CRITICAL] row row absent — current: "Falls mechanism absent" | correct: "Adults >20 ft; children <15 y >10 ft or 2-3x child height" | Add Falls mechanism criteria (adult >20 ft; child <15 y >10 ft or 2-3x height) to Mechanism of Injury list.
- `AUD-0014` [CRITICAL] row row absent — current: "Intrusion criterion absent (only ejection and death in compartment present)" | correct: "Intrusion >12 in into occupant site or >18 in into any site" | Add high-risk auto intrusion thresholds (>12 in occupant site; >18 in any site) to Mechanism of Injury list.
- `AUD-0015` [CRITICAL] row row absent — current: "No anatomic criteria block (only 'Time-Sensitive Extremities' in Special Considerations)" | correct: "8 anatomic criteria as listed in PEMS" | Add the full Anatomic Criteria block (8 items) as a criteria group that routes to trauma center.
- `AUD-0242` [MODERATE] row row 4 — current: "Single condition: HEMS faster to trauma center" | correct: "HEMS 'should be considered' if (a) criteria-met -> Level I/II, or (b) greater level of care needed AND HEMS on scene faster than ground to closest hospital" | Replace row 4 conditions with PEMS (a) and (b) and 'should be considered' wording.
- `AUD-0243` [MODERATE] row row 4 — current: "No statement on who may request HEMS" | correct: "Technicians may request HEMS without MC authorization" | Add: technicians may request HEMS without MC authorization.
- `AUD-0244` [MODERATE] row row 6 — current: "Adds inhalation and face/hands/feet/genitals as burn-center criteria" | correct: "No inhalation or face/hands/feet/genitals criterion in PEMS list" | Remove non-PEMS criteria, or cite the regional source that adopts them.
- `AUD-0245` [MODERATE] row row 7 — current: "Pediatric trauma center only (mandatory)" | correct: "Trauma center or pediatric trauma center; pediatric center (CHKD or VCU) considered for patients meeting triage criteria" | Restate as trauma center or pediatric trauma center (CHKD or VCU), with pediatric center 'consider' wording per PEMS pearl.
- `AUD-0246` [MODERATE] row row absent — current: ">20 mph applied to thrown and run-over" | correct: "thrown, run over, or significant impact (>20 mph); scope of the >20 mph qualifier ambiguous in flattened text" | Reword to mirror PEMS; confirm in the PDF whether >20 mph qualifies thrown/run-over or only significant impact.
- `AUD-0643` [MINOR] row row 3 — current: "No requirement to document delay" | correct: "Transport immediately; otherwise document the reason for the delay" | Add: transport immediately; if delayed, document the reason.
- `AUD-0644` [MINOR] row row 6 — current: "Destinations not named" | correct: "Sentara Norfolk General Hospital or VCU Medical Center" | Name the burn centers (Sentara Norfolk General or VCU Medical Center).
- `AUD-0645` [MINOR] row row absent — current: "Mandatory routing ('route to')" | correct: "'should be considered for' transport" | Change to 'should be considered for transport to a trauma center or hospital with obstetrical resources'.

## protocols/cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.md

- `AUD-0016` [CRITICAL] row row 2 — current: "EMR blank; EMT and above" | correct: "EMR and above" | Set EMR filled on row 2. Time-critical life-saving intervention narrowed from EMR to EMT.
- `AUD-0017` [CRITICAL] row row 8 — current: "EMR blank; EMT and above; rhythm ID restricted to EMT-I/P; 'maximum joules'" | correct: "EMR filled for AED use; adult 200 J biphasic / 360 J monophasic; pediatric 2 J/kg then 4 J/kg" | Set EMR AED filled; replace 'maximum joules' with PEMS energies; remove the EMT-I/P-only rhythm restriction for AED advice. Defibrillation energy and EMR AED level are PEMS VF/pVT content; INFERRED bracke
- `AUD-0018` [CRITICAL] row row 9 — current: "I and P only; restricted to bradycardia criteria; 'as needed'" | correct: "A and above; any pediatric arrest; repeat every 3-5 min during cardiac arrest" | Set A filled on row 9; delete the 'unconscious and hypotensive, HR < 60' qualifier (bradycardia text imported from Bradycardia protocol); replace 'as needed' with 'during cardiac arrest'.
- `AUD-0019` [CRITICAL] row row 10 — current: "P only" | correct: "I and above" | Set I filled and P filled on row 10. Level narrowed from I to P (I is blocked from life-saving CaCl / NaHCO3 for hyperkalemia / CCB overdose). INFERRED from split pair (A I) at page 57-58. | inferred: confirm in PDF before edit
- `AUD-0020` [CRITICAL] row row 11 — current: "P only" | correct: "I and above" | Set I filled on row 11 (doses are correct). INFERRED from split pair (A I). | inferred: confirm in PDF before edit
- `AUD-0021` [CRITICAL] row row absent — current: "absent" | correct: "Epinephrine 1 mg IV/IO [0.1 mg/mL] adult, repeat every 3-5 min; level A" | Add an adult epinephrine 1 mg IV/IO [0.1 mg/mL] row at A, repeat every 3-5 minutes during arrest.
- `AUD-0247` [MODERATE] row row 1 — current: "EMR blank; EMT and above" | correct: "EMR and above" | Set EMR filled on row 1.
- `AUD-0248` [MODERATE] row row 1 — current: "EMR blank; EMT and above" | correct: "EMR and above" | Set EMR filled on row 1 (or split DNR into its own EMR row).
- `AUD-0249` [MODERATE] row row 3 — current: "EMR blank; EMT and above" | correct: "EMR and above" | Set EMR filled on row 3.
- `AUD-0250` [MODERATE] row row 6 — current: "I and above" | correct: "A and above" | Set A filled on row 6. INFERRED from split pair (EMT A) at page 57. | inferred: confirm in PDF before edit
- `AUD-0251` [MODERATE] row row 7 — current: "no sudden-increase ROSC check; no 35-45 target; no avoid-excess-ventilation" | correct: "PEMS EtCO2 and airway pearls as quoted" | Add the >30-40 mmHg ROSC check, 35-45 mmHg post-ROSC target, avoid-excess-ventilation and SGA-vs-intubation pearls.
- `AUD-0252` [MODERATE] row row 12 — current: "MC-only statement; TOR criteria absent" | correct: "Add: not witnessed by EMS, after 20 min CPR, no ROSC AND no shocks delivered" | Add the three TOR criteria to the pearls, verbatim.
- `AUD-0253` [MODERATE] row row absent — current: "absent" | correct: "Full PEMS reversible-cause list plus IV/IO patency" | Add the full reversible-causes list and IV/IO patency pearl.

## protocols/cardiac/04_Bradycardia_PROC.md

- `AUD-0025` [CRITICAL] row row 6 — current: "no level (all blank)" | correct: "[I]: I must contact MC; P and above standing" | Add [I] bracket (MC contact required at I) on row 6; keep SBP targets and max dose text.
- `AUD-0027` [CRITICAL] row row absent — current: "absent" | correct: "EMR+ (children/infants only)" | Add EMR row for pediatric compressions with the Pediatric CPR and Asystole/PEA cross-references. Time-critical life-saving step omitted (re-rated from draft MODERATE).
- `AUD-0028` [CRITICAL] row row absent — current: "absent" | correct: "EMT+" | Add EMT row: obtain and transmit 12-lead ECG.
- `AUD-0029` [CRITICAL] row row absent — current: "absent" | correct: "A+ (children/infants only): epinephrine 0.01 mg/kg IV/IO [0.1 mg/mL] q3-5 min" | Add pediatric epinephrine 0.01 mg/kg IV/IO (0.1 mg/mL) q3-5 min row at A.
- `AUD-0255` [MODERATE] row row 8 — current: "EMR blank, EMT blank; A [A]; I +; P +" | correct: "MC in all five level cells (bare MC: all levels must contact MC)" | Set MC in all five level cells on row 8 (replaces [A] and standing I/P). Draft F-BR-14 CONFIRMED.
- `AUD-0256` [MODERATE] row row absent — current: "absent" | correct: "EMR+" | Add EMR row: ensure adequate oxygenation; refer to Airway Management and Ventilatory Support.
- `AUD-0257` [MODERATE] row row absent — current: "absent" | correct: "EMR+" | Add EMR row; the reversible-causes list is in AUD-0262.
- `AUD-0258` [MODERATE] row row absent — current: "absent" | correct: "A+" | Add A row: obtain IV/IO access (do not delay pacing for access; see row absent, docs/protocols/cardiac/04_Bradycardia_PROC.md).
- `AUD-0259` [MODERATE] row row absent — current: "absent" | correct: "present" | Add pearl verbatim.
- `AUD-0260` [MODERATE] row row absent — current: "absent" | correct: "present" | Add pearl verbatim.
- `AUD-0261` [MODERATE] row row absent — current: "absent" | correct: "present (p.105 Compressions / Airway pearls)" | Add the p.105 compression, EtCO2, and airway pearls verbatim, or cross-reference the CPR procedure explicitly.
- `AUD-0262` [MODERATE] row row absent — current: "absent" | correct: "present" | Add the reversible-causes list verbatim under the EMR reversible-causes row (AUD-0257).
- `AUD-0646` [MINOR] row row absent — current: "absent" | correct: "present" | Add pearl verbatim (non-clinical-action wording).
- `AUD-0647` [MINOR] row row absent — current: "present" | correct: "not in PEMS Symptomatic Bradycardia" | Source to a PEMS or medical-director document or remove.
- `AUD-0648` [MINOR] row row absent — current: "absent" | correct: "CHKD COR (757) 668-8000; VCU CHoR Communications Room (804) 828-3989" | Add both numbers under row 8.

## protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md

- `AUD-0030` [CRITICAL] row row 2 — current: "EMR blank; EMT and above" | correct: "EMR and above" | Set EMR filled on row 2. Time-critical life-saving intervention narrowed from EMR to EMT.
- `AUD-0031` [CRITICAL] row row 5 — current: "EMR blank; EMT and above" | correct: "EMR filled for AED use (AED-only); manual defibrillation I and above per row token I" | Set EMR to AED-only filled and annotate row 5 AED (EMR/EMT) vs manual (I/P). Same root issue in row 4 (AED / Rhythm Assessment, EMT and above). INFERRED: the [EMR] bracket is inline text in flattened PDF text; eyeball PEMS2024.pdf p.63 before editing. | inferred: 
- `AUD-0032` [CRITICAL] row row 8 — current: "I and above" | correct: "A and above" | Set A filled on row 8. Epinephrine at A is narrowed to I.
- `AUD-0033` [CRITICAL] row row 9 — current: "Lidocaine alternative absent; replaced by Contact Medical Control" | correct: "Lidocaine 1 mg/kg IV/IO slow push, adult max 100 mg, pediatric max 50 mg, I and above, no MC gate" | Replace the MC-only alternative with the PEMS lidocaine 1 mg/kg (adult max 100 mg, peds max 50 mg) at I. INFERRED level I from split token pair (A I) at page 63-64 boundary; eyeball PDF. | inferred: confirm in 
- `AUD-0034` [CRITICAL] row row 10 — current: "I and above; scope limited to Asystole/PEA" | correct: "A and above; applies to VF/pVT and Asystole/PEA" | Change level I to A and remove the 'Asystole/PEA Only' scope label so VF/pVT fluids are covered.
- `AUD-0035` [CRITICAL] row row 13 — current: "I filled (standing TOR authority)" | correct: "MC (MC gate for all levels)" | Change I cell from filled dot to MC. TOR is an MC-only decision per PEMS at every level.
- `AUD-0036` [CRITICAL] row row absent — current: "absent" | correct: "Amiodarone 150 mg adult; peds 5 mg/kg max 150 mg with MC contact; lidocaine 0.5 mg/kg adult max 100 mg, peds 1 mg/kg max 50 mg; level I" | Add second-line antiarrhythmic row at I with the PEMS doses and the peds [Contact Medical Control] gate. Current merged file has no second-line row.
- `AUD-0037` [CRITICAL] row row absent — current: "absent" | correct: "Magnesium sulfate 2 g IV/IO slow push adult; peds 40 mg/kg max 2 g with MC contact; level I" | Add Magnesium Sulfate row at I with the adult 2 g and pediatric MC-gated 40 mg/kg (max 2 g) doses.
- `AUD-0264` [MODERATE] row row 1 — current: "EMR blank; EMT and above" | correct: "EMR and above" | Set EMR filled on row 1 for DNR determination, or split DNR into its own row at EMR.
- `AUD-0265` [MODERATE] row row 1 — current: "Exclusions: DNR, injuries" | correct: "Exclusions: DNR, rigor mortis, lividity, decomposition, injuries inconsistent with survival" | Add rigor mortis, lividity and decomposition to the exclusion list (PEMS Asystole/PEA criteria, p.57).
- `AUD-0266` [MODERATE] row row 3 — current: "No avoid-excess-ventilation, no 35-45 mmHg ROSC target, no <20 mmHg post-ROSC reassessment" | correct: "Add the PEMS airway and EtCO2 pearls verbatim" | Add the three PEMS airway/EtCO2 pearl bullets to the Pearls section. Row 3 level EMT and above has no PEMS row to compare against; left unchanged.
- `AUD-0267` [MODERATE] row row 6 — current: "A and above (EMT blank)" | correct: "EMT and above" | Set EMT filled on row 6. | inferred: confirm in PDF before edit
- `AUD-0268` [MODERATE] row row 7 — current: "I and above" | correct: "A and above" | Set A filled on row 7 (narrowed from A to I; same pattern as F-AL-08). | inferred: confirm in PDF before edit
- `AUD-0269` [MODERATE] row row 9 — current: "P = MC" | correct: "P filled (standing, no MC gate)" | Change P cell from MC to filled dot. MC gate is added where PEMS grants standing use. INFERRED level from split token pair (A I) at page 63-64. | inferred: confirm in PDF before edit
- `AUD-0270` [MODERATE] row row 11 — current: "P = MC" | correct: "P filled (standing)" | Change P cell from MC to filled dot. I level is correct.
- `AUD-0271` [MODERATE] row row 12 — current: "EMR blank; EMT and above" | correct: "EMR and above" | Set EMR filled on row 12.
- `AUD-0272` [MODERATE] row row 13 — current: "blank (no authority)" | correct: "MC" | Set EMR, EMT and A cells to MC so those levels can request TOR through MC.
- `AUD-0273` [MODERATE] row row 14 — current: "EMR blank; EMT and above" | correct: "EMR and above" | Set EMR filled on row 14. INFERRED from split pair (I EMR) at page 64. | inferred: confirm in PDF before edit
- `AUD-0274` [MODERATE] row row absent — current: "absent" | correct: "Contact Medical Control for guidance as needed - MC in all five level cells" | Add a row 'Contact Medical Control for guidance as needed' with MC in all cells (PEMS bare MC, p.57 and p.64).
- `AUD-0275` [MODERATE] row row absent — current: "Hyper/hypothermia and IV patency absent" | correct: "Include Hyperthermia or Hypothermia and Ensure IV/IO patency" | Add hyperthermia/hypothermia to the reversible-causes list and add the IV/IO patency pearl.
- `AUD-0276` [MODERATE] row row absent — current: "absent" | correct: "Magnesium indications verbatim" | Add the PEMS magnesium indication pearl with the magnesium row (see row absent, docs/protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md).
- `AUD-0277` [MODERATE] row row absent — current: "absent" | correct: "Preparation instruction for 0.1 mg/mL (PEMS typo 'syrine' is a PEMS error; do not copy)" | Add the 0.1 mg/mL dilution instruction to the epinephrine pearls.
- `AUD-0649` [MINOR] row row 11 — current: "absent" | correct: "preferably via separate lines" | Add 'preferably via separate lines' to the CaCl / NaHCO3 row.
- `AUD-0650` [MINOR] row row absent — current: "no two-lead check; no AED advice criterion" | correct: "check two leads; AED advising to shock / not to shock" | Add 'check two leads' and AED advice criterion to Signs and Symptoms.

## protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md

- `AUD-0043` [CRITICAL] row row absent — current: "absent" | correct: "I+ for adults and children 12 and older; P only for children under 12 (red-dot note)" | Add an intubation row: I column bullet (adult/12+); P only for under 12 with the 'red dot' Paramedic-only note; cross-reference Endotracheal Intubation procedure.
- `AUD-0044` [CRITICAL] row row absent — current: "absent" | correct: "A+ Adult 1 mg Epinephrine 0.1 mg/mL IV/IO; Pediatric 0.01 mg/kg IV/IO; single dose only; PEA with no ROSC" | Add an epinephrine row at the A level with the PEMS adult and pediatric doses, 0.1 mg/mL concentration, PEA indication after no ROSC, and single-dose limit.
- `AUD-0283` [MODERATE] row row 11 — current: "MC all levels; no time trigger" | correct: "MC all levels; trigger: no signs of life after 15-20 minutes of resuscitation" | Keep the bare MC row and add the PEMS 15-20 minute no-signs-of-life trigger.
- `AUD-0284` [MODERATE] row row absent — current: "absent" | correct: "both statements present" | Add both PEMS statements to the Pearls section.

## protocols/cardiac/04_Chest_Pain_ACS_PROC.md

- `AUD-0047` [CRITICAL] row row 6 — current: "destination optional ('consider ... if indicated')" | correct: "mandatory transport to nearest PCI-capable hospital on STEMI/ACUTE MI, per STEMI Field Triage policy" | Replace 'Consider destination ... if indicated' with mandatory PCI-capable transport wording. Not flagged in draft; added.
- `AUD-0049` [CRITICAL] row row 10 — current: "no dose, no route" | correct: "Adult 324 mg PO, chewed" | Add 'ADULT: Aspirin 324 mg PO chewed' to row 10.
- `AUD-0051` [CRITICAL] row row 11 — current: "no dose, interval, maximum, or SBP/MAP gate" | correct: "0.4 mg SL; may repeat q5 min up to 3 doses; only if SBP >100 and MAP >=65" | Add dose, repeat interval, maximum, and SBP/MAP gate to row 11. The Pain Control cross-reference was not verified in this batch.
- `AUD-0052` [CRITICAL] row row absent — current: "absent" | correct: "present: do not give NTG within 48 h of sildenafil, vardenafil, tadalafil" | Add the contraindication to the NTG row and pearls before any NTG dosing text is restored. | [OWNER]
- `AUD-0053` [CRITICAL] row row absent — current: "absent" | correct: "present" | Add pearl verbatim. Re-rated from draft MODERATE to CRITICAL: it is the destination override for the most unstable STEMI/ACS patients.
- `AUD-0287` [MODERATE] row row 2 — current: "no target" | correct: "Maintain SpO2 94-98%" | Replace 'Assess SpO2' with 'Maintain SpO2 94-98%' (keep assessment wording).
- `AUD-0288` [MODERATE] row row 4 — current: "transmit within 10 minutes" | correct: "obtain AND transmit within 5 minutes of patient contact" | Change transmit window to 5 minutes (also pearl 4 in site file).
- `AUD-0290` [MODERATE] row row 7 — current: "[I] at I; P bullet" | correct: "MC (all levels contact MC), inferred" | Replace the [I] bracket with MC across all levels, or source a level for serial ECGs. PDF check required (see notes). | inferred: confirm in PDF before edit
- `AUD-0293` [MODERATE] row row 13 — current: "EMR blank, EMT blank; A [A]; I +; P +" | correct: "MC in all five level cells" | Set MC in all five cells on row 13. Draft finding confirmed.
- `AUD-0294` [MODERATE] row row absent — current: "absent" | correct: "EMR+: if hypotensive, refer to Hypotension and Shock protocol" | Add EMR referral row. Draft rated MINOR; re-rated MODERATE (clinical pathway for hypotensive chest-pain patient).
- `AUD-0295` [MODERATE] row row absent — current: "absent" | correct: "present" | Add pearl verbatim.
- `AUD-0296` [MODERATE] row row absent — current: "absent" | correct: "present" | Add pearl verbatim.
- `AUD-0297` [MODERATE] row row absent — current: "absent" | correct: "present" | Add pearl verbatim (links to AUD-0290).
- `AUD-0298` [MODERATE] row row absent — current: "absent" | correct: "present" | Add pearl verbatim.
- `AUD-0651` [MINOR] row row 4 — current: "present" | correct: "not in PEMS chest pain protocol" | Source or remove.
- `AUD-0652` [MINOR] row row 8 — current: "I+P" | correct: "no PEMS chest-pain row or level" | Verify against the Intraosseous Access / IV procedure level grant, or remove from this protocol. Draft ignored this row; not ignored now.
- `AUD-0653` [MINOR] row row 14 — current: "[I] (MC bracket at I)" | correct: "no level; PEMS pearl is not level-gated or MC-gated" | Remove the [I] bracket or source it to a PEMS level.
- `AUD-0654` [MINOR] row row absent — current: "present" | correct: "not in PEMS Chest Pain protocol" | Verify sources (some may come from other PEMS protocols) or move/remove.

## protocols/cardiac/04_Hypertensive_Crisis_PROC.md

- `AUD-0304` [MODERATE] row row absent — current: "absent" | correct: "present" | Add the PEMS statement verbatim; it is the central management message of the protocol.
- `AUD-0305` [MODERATE] row row absent — current: "absent" | correct: "present" | Add pearl verbatim. Draft rated MINOR; re-rated MODERATE per missing clinical pearl rule.
- `AUD-0655` [MINOR] row row 2 — current: "EMT+" | correct: "no PEMS row or level" | Source to a PEMS procedure or remove the leveled row.
- `AUD-0656` [MINOR] row row 3 — current: "present" | correct: "not named in PEMS Hypertension" | Source to Stroke/TIA protocol or remove.
- `AUD-0657` [MINOR] row row 4 — current: "A+ I+ P+" | correct: "not in PEMS hypertension protocol" | Remove or align with AUD-0045 (EMT ECG).
- `AUD-0658` [MINOR] row row 5 — current: "EMT+" | correct: "not in PEMS hypertension protocol" | Source to Airway/Ventilatory procedure or remove.
- `AUD-0659` [MINOR] row row absent — current: "present" | correct: "not in PEMS Hypertension" | Verify with medical director or remove; permissive-hypertension and aortic-dissection directions are clinical content not sourced to PEMS.
- `AUD-0660` [MINOR] row row absent — current: "Hypertensive Crisis" | correct: "Hypertension (PEMS title)" | Align title or add 'Hypertensive Crisis' as alias.

## protocols/cardiac/04_Post_Resuscitation_Care_PROC.md

- `AUD-0309` [MODERATE] row row 6 — current: "absent" | correct: "Norepinephrine 4 mg in 250 mL NS = 16 mcg/mL; Epinephrine 1 mg in 100 mL NS = 10 mcg/mL" | Add both PEMS concentrations to row 6 so the infusion can be prepared correctly.
- `AUD-0310` [MODERATE] row row 7 — current: "absent" | correct: "Epinephrine 1 mg in 100 mL NS = 10 mcg/mL" | Add the PEMS pediatric epinephrine concentration to row 7.
- `AUD-0311` [MODERATE] row row 8 — current: "absent" | correct: "100 mcg epinephrine (1 mL of 0.1 mg/mL) in 9 mL NS = 10 mcg/mL" | Add the push-dose preparation (10 mcg/mL) to row 8.
- `AUD-0312` [MODERATE] row row absent — current: "absent" | correct: "EMR+ Follow Universal Patient Care / Initial Patient Contact protocol" | Add a Universal Patient Care / Initial Patient Contact row with a bullet in the EMR column.

## protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md

- `AUD-0317` [MODERATE] row row 10 — current: "[I] at I, bullet at P (EMR/EMT/A blank)" | correct: "MC in all five level cells (bare MC)" | Set MC in all five level cells per doctrine (bare MC = all levels must contact MC).
- `AUD-0320` [MODERATE] row row absent — current: "absent" | correct: "all three statements present" | Add the wide-complex referral to VT with a Pulse, the unstable-vs-stable definition, and the potential-causes pearl.

## protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md

- `AUD-0065` [CRITICAL] row row 1 — current: "EMR blank; EMT and above" | correct: "EMR and above" | Split CPR into its own row at EMR and set EMR filled (currently merged with DNR at EMT).
- `AUD-0066` [CRITICAL] row row 4 — current: "I and above" | correct: "A and above" | Set A filled on row 4.
- `AUD-0068` [CRITICAL] row row 6 — current: "I and P only" | correct: "A and above" | Set A filled on row 6 (epinephrine narrowed from A to I). INFERRED from split pair (I A) at page 63; eyeball PDF. | inferred: confirm in PDF before edit
- `AUD-0069` [CRITICAL] row row 7 — current: "P only" | correct: "I and above" | Set I filled on row 7. Amiodarone narrowed from I to P. INFERRED from split pair (A I) at page 63-64. | inferred: confirm in PDF before edit
- `AUD-0070` [CRITICAL] row row 8 — current: "P only" | correct: "I and above" | Set I filled on row 8.
- `AUD-0071` [CRITICAL] row row 9 — current: "P only" | correct: "I and above (peds MC-gated)" | Set I filled on row 9. Magnesium narrowed from I to P.
- `AUD-0072` [CRITICAL] row row 10 — current: "P only" | correct: "I and above" | Set I filled on row 10. CaCl / NaHCO3 narrowed from I to P.
- `AUD-0321` [MODERATE] row row 1 — current: "EMR blank; EMT and above" | correct: "EMR and above" | Set EMR filled for DNR determination (split with CPR row, see row 1, docs/protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md).
- `AUD-0322` [MODERATE] row row 2 — current: "A and above (EMT blank)" | correct: "EMT and above" | Set EMT filled on row 2. INFERRED from split pair (EMR EMT) at page 63. | inferred: confirm in PDF before edit
- `AUD-0323` [MODERATE] row row 3 — current: "I and above" | correct: "A and above" | Set A filled on row 3. INFERRED from split pair (EMT A). | inferred: confirm in PDF before edit
- `AUD-0324` [MODERATE] row row 4 — current: "no 250-500 mL bolus size; no 60 mL/kg total cap" | correct: "250-500 mL boluses; repeat to 60 mL/kg total" | Add 250-500 mL bolus size and the 60 mL/kg total cap.
- `AUD-0325` [MODERATE] row row 5 — current: "absent" | correct: "2 minutes CPR after each shock, reassess; re-shock if persists; manufacturer's recommendation accepted" | Add the 2-minute CPR and re-shock instruction and the manufacturer's recommendation clause.
- `AUD-0326` [MODERATE] row row 10 — current: "absent" | correct: "Repeat in 5 minutes if no change" | Add 'Repeat in 5 minutes if no change.' to row 10.
- `AUD-0327` [MODERATE] row row 11 — current: "EMT and above" | correct: "EMR and above" | Set EMR filled on row 11. INFERRED from split pair (I EMR) at page 64. | inferred: confirm in PDF before edit
- `AUD-0328` [MODERATE] row row absent — current: "absent" | correct: "EMR and above" | Add a universal-care row at EMR.
- `AUD-0329` [MODERATE] row row absent — current: "absent" | correct: "EMR and above" | Add a reversible-causes row at EMR.
- `AUD-0330` [MODERATE] row row absent — current: "no slow-push rate on rows 7-10" | correct: "slow push on each antiarrhythmic, magnesium, CaCl and NaHCO3" | Add 'slow push' to rows 7, 8, 9 and 10 (rate affects hypotension / bradycardia with rapid amiodarone).
- `AUD-0331` [MODERATE] row row absent — current: "absent" | correct: "Verbatim PEMS indication list" | Add the magnesium indication pearl.
- `AUD-0332` [MODERATE] row row absent — current: "absent" | correct: "Dilution instruction for 0.1 mg/mL" | Add the dilution instruction to the pearls.
- `AUD-0333` [MODERATE] row row absent — current: "absent" | correct: "PEMS airway and EtCO2 pearls" | Add the PEMS airway and EtCO2 pearls.
- `AUD-0334` [MODERATE] row row absent — current: "absent" | correct: "PEMS TOR criteria (p.66)" | Add the three TOR criteria verbatim to pearls.
- `AUD-0335` [MODERATE] row row absent — current: "label only" | correct: "Full PEMS list" | Add the full reversible-causes list to pearls.
- `AUD-0661` [MINOR] row row 10 — current: "flush with no volume; no separate-lines instruction" | correct: "20 mL 0.9% sodium chloride flush; preferably via separate lines" | Add 20 mL flush volume and separate-lines instruction.
- `AUD-0662` [MINOR] row row absent — current: "no adjustment instruction" | correct: "PEMS pad placement pearl" | Add the refractory-VF pad placement / adjustment sentence.
- `AUD-0663` [MINOR] row row absent — current: "no two-lead check" | correct: "check 2 leads" | Add 'check 2 leads' to Signs and Symptoms.

## protocols/front-matter/Universal Patient Care.md

- `AUD-0664` [MINOR] row row 4 — current: "Absent" | correct: "Closely monitor; attention to condition before/after interventions" | Add the monitoring sentence to row 4.
- `AUD-0665` [MINOR] row row 11 — current: "'contact' (mandatory)" | correct: "'consider contacting' Medical Control" | Change to 'consider contacting Medical Control'.
- `AUD-0666` [MINOR] row row absent — current: "Absent (self-reference)" | correct: "EMR - Follow Universal Patient Care protocol" | Optional: add a note that this protocol is the baseline for all others; no clinical content.
- `AUD-0667` [MINOR] row row absent — current: "Specific cross-references absent" | correct: "Named cross-references as listed" | Add the named cross-references to rows 2, 3, 6, 7, 8, 10.
- `AUD-0668` [MINOR] row row absent — current: "'medication noncompliance' omitted; 'intracranial' omitted" | correct: "Includes 'medication noncompliance' and 'intracranial hemorrhage'" | Add 'medication noncompliance' and 'intracranial' to the SMASHED 2 pearl.

## protocols/general/02_Behavioral_Patient_Restraint_PROC.md

- `AUD-0352` [MODERATE] row row absent — current: "absent" | correct: "EMT: blood glucose, continuous resp/vitals monitoring, BP q5 min" | Add EMT row with glucose check, continuous monitoring and BP every 5 minutes.
- `AUD-0353` [MODERATE] row row absent — current: "absent" | correct: "Pearl: empiric high-flow O2 by mask if SpO2 cannot be monitored" | Add pearl with PEMS wording.
- `AUD-0354` [MODERATE] row row absent — current: "absent" | correct: "Physical restraint procedure: supine on board, circulation check q15 min, no chest-strap restriction, SpO2/O2 when indicated" | Add physical-restraint safety steps or a link to the Patient Restraint policy text; the never-prone pearl is present.
- `AUD-0669` [MINOR] row row absent — current: "absent" | correct: "Pearl: implied consent and least restrictive restraint, maintain dignity" | Add pearl (legal/ethical).
- `AUD-0670` [MINOR] row row absent — current: "absent" | correct: "Pearl: LEO accompaniment for LE restraints; consider EMS-sanctioned restraints" | Add pearl.
- `AUD-0671` [MINOR] row row absent — current: "absent" | correct: "Pearl: refusal documentation requirements" | Add pearl or cross-reference explicitly.
- `AUD-0672` [MINOR] row row absent — current: "mnemonic only" | correct: "PEMS enumerated cause list" | List the PEMS causes (mnemonic may be kept as an aid).

## protocols/general/02_Cold_Exposure_PROC.md

- `AUD-0360` [MODERATE] row row 8 — current: "EMR, EMT, A, I, P" | correct: "EMT, A, I, P" | Remove EMR column from transport row 8 (EMR transport not granted by PEMS).
- `AUD-0673` [MINOR] row row 6 — current: "EMT, A, I, P" | correct: "No level in PEMS (pearl); site EMT+ is unsourced" | Either move to Pearls or confirm EMT+ level with PEMS owner; no PEMS level token exists. | inferred: confirm in PDF before edit
- `AUD-0674` [MINOR] row row absent — current: "present" | correct: "not found in PEMS p.67-68 (text truncated at pearl 3 tail)" | Verify against PDF; remove or source if absent.

## protocols/general/02_Diving_and_Drowning_Emergencies_PROC.md

- `AUD-0367` [MODERATE] row row absent — current: "absent" | correct: "Pearl: extremity-before-trunk rewarming hypotension caution" | Add pearl.
- `AUD-0368` [MODERATE] row row absent — current: "absent" | correct: "Pearl: high suspicion for head/spine trauma" | Add pearl.
- `AUD-0369` [MODERATE] row row absent — current: "absent" | correct: "Pearl: cold-water submersion arrest, MC guidance on-scene vs ED" | Add pearl with MC contact instruction.
- `AUD-0370` [MODERATE] row row absent — current: "absent" | correct: "Pearl: gentle handling of hypothermic submersion patients" | Add pearl.
- `AUD-0371` [MODERATE] row row absent — current: "absent" | correct: "Pearl: delayed pulmonary edema; transport all nonfatal drowning" | Add pearl.
- `AUD-0372` [MODERATE] row row absent — current: "absent" | correct: "Pearl: barotrauma, bends and arterial gas emboli presentations and initial management" | Add pearl.

## protocols/general/02_Heat_Exposure_PROC.md

- `AUD-0378` [MODERATE] row row absent — current: "absent" | correct: "EMR+ universal care row" | Add row 0 Follow General Universal Patient Care / Initial Patient Contact protocol, EMR+.
- `AUD-0379` [MODERATE] row row absent — current: "absent" | correct: "Pearl: cold IV fluids in heat stroke only; caution in conscious patient" | Add pearl with the PEMS wording.

## protocols/general/02_Pain_Control_PROC.md

- `AUD-0077` [CRITICAL] row row 6 — current: "0.5-1 mcg/kg for IV, IN and IM" | correct: "IV/IO 0.5 mcg/kg; IN/IM 1 mcg/kg; max dose 25 mcg" | Split pediatric fentanyl into IV/IO 0.5 mcg/kg and IN/IM 1 mcg/kg; a 1 mcg/kg IV dose is double the PEMS IV dose.
- `AUD-0385` [MODERATE] row row 6 — current: "I, P (no MC gate)" | correct: "A with MC contact; I, P standing" | Add A column marked [A] (must contact MC) on row 6. Escalate to CRITICAL if the program treats high-alert opioid narrowing as CRITICAL.
- `AUD-0386` [MODERATE] row row 6 — current: "no rate" | correct: "IV/IO over 2 minutes" | Add 'over 2 minutes' for IV/IO route.
- `AUD-0387` [MODERATE] row row 6 — current: "absent" | correct: "Repeat every 10-15 min titrated to pain relief" | Add repeat interval to rows 6 and 7; max totals are already present.
- `AUD-0388` [MODERATE] row row 7 — current: "I, P (no MC gate)" | correct: "A with MC contact; I, P standing" | Add A column marked [A] on row 7 (same as row 6).

## protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md

- `AUD-0078` [CRITICAL] row row 4 — current: "P" | correct: "No PEMS pre-intubation sedation dosing in batch PEMS source; PEMS ketamine card lists RSI indication only" | Remove pre-intubation ketamine/midazolam doses or source them to a PEMS RSI document; over-authorization of high-alert sedatives.
- `AUD-0079` [CRITICAL] row row 5 — current: "P, ketamine" | correct: "Not granted in PEMS for post-intubation sedation" | Remove post-intubation ketamine row or obtain PEMS authority; ketamine is dissociative and high-alert.
- `AUD-0081` [CRITICAL] row row 6 — current: "midazolam parallel first-line" | correct: "fentanyl first; midazolam only if fentanyl insufficient" | Restructure row 6 so midazolam is the second-line agent only if fentanyl is insufficient. | inferred: confirm in PDF before edit
- `AUD-0082` [CRITICAL] row row 6 — current: "0.05 mg/kg IV/IO" | correct: "0.1 mg/kg IV/IO (max 2.5 mg per dose)" | Correct pediatric midazolam IV/IO dose to 0.1 mg/kg; 0.05 mg/kg matches the Behavioral protocol dose (copy error risk).
- `AUD-0083` [CRITICAL] row row 6 — current: "no per-dose max; total 50 mcg" | correct: "per-dose maximum 25 mcg" | Add per-dose maximum 25 mcg for pediatric fentanyl.
- `AUD-0084` [CRITICAL] row row absent — current: "absent" | correct: "EMT+ confirm and monitor airway placement with continuous SpO2 and box-waveform EtCO2" | Add EMT row for continuous EtCO2/SpO2 confirmation of airway placement (ETI protocol also requires it).
- `AUD-0085` [CRITICAL] row row absent — current: "absent" | correct: "MC: all levels must contact MC" | Add MC row (all levels contact Medical Control) for sedation not adequately managed; PEMS-required MC for high-alert sedation.
- `AUD-0390` [MODERATE] row row 6 — current: "IV/IO only" | correct: "IV/IO 2.5 mg or IN/IM 5 mg; peds IN/IM 0.2 mg/kg" | Add IN/IM routes with PEMS doses and max 5 mg IN/IM.
- `AUD-0391` [MODERATE] row row 6 — current: "total caps present" | correct: "no total cap in PEMS p.55" | Source the total caps or remove them; PEMS only specifies per-dose maxima and repeat interval.
- `AUD-0392` [MODERATE] row row 6 — current: "IV/IO only" | correct: "IV/IO or IN/IM" | Add IN/IM route for fentanyl with PEMS doses.
- `AUD-0393` [MODERATE] row row absent — current: "absent" | correct: "Pearl: EtCO2 target 35-45 mmHg post advanced airway" | Add pearl.
- `AUD-0394` [MODERATE] row row absent — current: "absent" | correct: "Pearl: monitor for post-intubation hypotension; PPV risk" | Add pearl.
- `AUD-0395` [MODERATE] row row absent — current: "generic sedatives; 3 criteria" | correct: "fentanyl-specific; 6 criteria incl. low weight, hypotensive, hemodynamically labile" | Replace with PEMS wording.
- `AUD-0675` [MINOR] row row 1 — current: "present" | correct: "not in PEMS p.55-56" | Keep as cross-reference only or source it.
- `AUD-0676` [MINOR] row row 2 — current: "A, I, P" | correct: "not a PEMS row on this page" | Source to PEMS pearl or Pain Control criteria, or keep as site-added precaution.
- `AUD-0677` [MINOR] row row 3 — current: "I, P" | correct: "not a PEMS row on this page" | Source or keep as site-added step; note I level is the one that gives PEMS midazolam/fentanyl IV/IO.
- `AUD-0678` [MINOR] row row absent — current: "Sedation (Non-Paralytic)" | correct: "Sedation Post Advanced Airway" | Rename header to PEMS title.
- `AUD-0679` [MINOR] row row absent — current: "absent" | correct: "January 2025" | Add version/date to front matter and align with PEMS body.
- `AUD-0680` [MINOR] row row absent — current: "absent" | correct: "Pearl: suction as needed" | Add pearl.
- `AUD-0681` [MINOR] row row absent — current: "present" | correct: "not in PEMS sedation page (ketamine card has a caution in cardiac disease)" | Source to PEMS ketamine/midazolam/fentanyl drug cards or remove.

## protocols/medical/07_Allergic_Reaction_Anaphylaxis_PROC.md

- `AUD-0088` [CRITICAL] row row absent — current: "absent" | correct: "I+ (I and P): MAP > 65 after non-response to repeat IM epi; epinephrine infusion 2-10 mcg/min" | Add an epinephrine infusion row at level I (adult) with the MAP and non-response conditions and the 1 mg/100 mL mix.
- `AUD-0089` [CRITICAL] row row absent — current: "absent" | correct: "[I]: I must contact MC; P and above standing; levels below may not perform" | Add pediatric epinephrine infusion row at [I] (MC contact required at I) with SBP targets (<1 yr >70; >1 yr >90) and 10 mcg/min max.
- `AUD-0090` [CRITICAL] row row absent — current: "absent" | correct: "P (inferred; the [ I ] token is read as the pediatric row's bracket, see notes)" | Add adult push-dose epinephrine row at P (5-10 mcg IV/IO q2-3 min; 100 mcg in 9 mL NS). PDF check the bracket placement before publishing. | inferred: confirm in PDF before edit
- `AUD-0091` [CRITICAL] row row absent — current: "absent" | correct: "MC (all levels must contact Medical Control)" | Add Medical Control contact row with MC in all five level cells; this gates the high-alert vasopressor rows above.
- `AUD-0398` [MODERATE] row row 3 — current: "I+ (A blank)" | correct: "A+" | Move the bullet from I to A on row 3 (I/P stay).
- `AUD-0407` [MODERATE] row row absent — current: "absent (generic 'immediately' only)" | correct: "PEMS sequencing statement present" | Add the PEMS sequencing pearl verbatim.
- `AUD-0408` [MODERATE] row row absent — current: "absent" | correct: "present" | Add pearl verbatim.
- `AUD-0409` [MODERATE] row row absent — current: "absent" | correct: "present" | Add pearl verbatim.
- `AUD-0410` [MODERATE] row row absent — current: "absent" | correct: "present (remainder of pearl not readable, see notes)" | Add pearl; complete the text from the PDF (tool truncation, see notes).

## protocols/medical/07_Hypotension_Shock_Non_Trauma_PROC.md

- `AUD-0682` [MINOR] row row absent — current: "present" | correct: "not in PEMS - verify or remove" | Flag for medical director verification; not level-gated.

## protocols/medical/07_OB_Emergencies_PROC.md

- `AUD-0097` [CRITICAL] row row 2 — current: "dry/warm/stimulate only" | correct: "EMR: assess HR, RR, SpO2; follow Neonatal Resuscitation protocol" | Add the HR/RR/SpO2 assessment and the Neonatal Resuscitation protocol referral at EMR level (time-critical neonatal resuscitation).
- `AUD-0098` [CRITICAL] row row 5 — current: "legs and body only" | correct: "Full PEMS breech sequence incl. arm delivery and neck flexion" | Add the omitted breech manoeuvres (towel, torso rotation, arm delivery via scapula, second-provider suprapubic pressure, neck flexion with two-finger maxilla traction) to row 5.
- `AUD-0101` [CRITICAL] row row 7 — current: "no half-dose caution" | correct: "Half-dose midazolam for frail, hypotensive, underweight patients" | Add the half-dose instruction to row 7 (benzodiazepine dosing in hypotensive patients could injure).
- `AUD-0103` [CRITICAL] row row absent — current: "no placenta-delivery or post-partum bleeding management" | correct: "EMR: check for additional pregnancies; gentle cord traction and fundal massage until placenta delivers and bleeding stops; transport placenta; skin-to-skin; direct pressure for bleeding (tail unverified)" | Add EMR placenta-delivery / post-partum haemorrhage row(s) from PEMS p.141; verify the truncated 'direct pressure'
- `AUD-0417` [MODERATE] row row 2 — current: "no exception stated" | correct: "Suction only if thick meconium present or airway obstructed" | Add 'unless thick meconium is present or the airway is obstructed' to row 2.
- `AUD-0418` [MODERATE] row row 2 — current: "check only" | correct: "Check for nuchal cord; unwrap if possible; clamp and cut if necessary" | Add 'unwrap if possible; clamp and cut if necessary' to row 2.
- `AUD-0419` [MODERATE] row row 2 — current: "steps omitted" | correct: "Include clothing removal, bony-skull (not fontanel) pressure, head support during shoulder/torso delivery" | Add the three PEMS delivery-technique steps; 'not fontanel' is a safety-relevant qualifier.
- `AUD-0421` [MODERATE] row row 3 — current: "no MC step" | correct: "If no progress, contact MC immediately" | Append 'If no progress, contact Medical Control immediately for guidance.' to row 3.
- `AUD-0423` [MODERATE] row row 4 — current: "no transport instruction" | correct: "Immediately transport to a facility with obstetric capability" | Add 'Immediately transport to a facility with obstetric capability' to row 4.
- `AUD-0425` [MODERATE] row row 5 — current: "no transport or MC-as-feasible step" | correct: "Initiate transport to OB-capable facility; if delivery imminent, contact MC as soon as feasible" | Add the transport and MC-as-feasible sentences to row 5.
- `AUD-0427` [MODERATE] row row 8 — current: "no transport instruction" | correct: "transport immediately" | Append 'and transport immediately' to row 8.
- `AUD-0428` [MODERATE] row row 10 — current: "no restraint or neonate-transport instruction" | correct: "All patients secured with safety restraints; do not transport baby in mother's arms" | Add the restraint and neonate-transport sentences to the transport guidance (row 10 level cells already correct: MC at all levels).
- `AUD-0429` [MODERATE] row row absent — current: "no destination step" | correct: "EMT: transport to facility with L&D capability" | Add eclampsia transport-to-L&D step at EMT level.
- `AUD-0430` [MODERATE] row row absent — current: "no >20 weeks threshold" | correct: "Pregnant or recently pregnant, over 20 weeks gestation, seizing" | Add '>20 weeks gestational age' to eclampsia criteria (site also lacks the 'recently pregnant' 8-week window in criteria; pearl has it).
- `AUD-0431` [MODERATE] row row absent — current: "BP '>160/110' (ambiguous and/or); edema; no RUQ/epigastric pain; no pulmonary edema; no >20 weeks" | correct: "SBP >160 OR DBP >110; severe/persistent headache; RUQ or epigastric pain; new visual disturbance; pulmonary edema; >20 weeks" | Rewrite pre-eclampsia criteria to the PEMS list (SBP or DBP wording, RUQ/epigastric pain, pulmonary edema; replace 'edema').
- `AUD-0432` [MODERATE] row row absent — current: "no ABC, O2 or shock-referral rows" | correct: "EMR: ABC support, O2 as needed, refer to Hypotension/Shock if shock" | Add the three EMR rows to the bleeding/rupture/abruptio section.
- `AUD-0433` [MODERATE] row row absent — current: "no hemorrhagic-shock referral" | correct: "EMR: if significant bleeding, refer to Hemorrhagic Shock protocol" | Add the EMR hemorrhagic-shock referral row to the childbirth section.
- `AUD-0434` [MODERATE] row row absent — current: "no cord-clamping instruction" | correct: "EMR: consider delayed cord clamping 1-3 min; clamp ~4 and ~6 inches; cut between" | Add the delayed cord clamping row at EMR level.
- `AUD-0435` [MODERATE] row row absent — current: "none" | correct: "as quoted" | Add the GA / resuscitation-threshold pearl and the premature-ROM pearl.
- `AUD-0436` [MODERATE] row row absent — current: "none" | correct: "as quoted" | Add both pearls (neonatal SpO2 reference ranges are needed to interpret the row 2 assessment).
- `AUD-0437` [MODERATE] row row absent — current: "none" | correct: "as quoted (PEMS typo 'No NOT' verbatim)" | Add the no-fundal-pressure pearl.
- `AUD-0438` [MODERATE] row row absent — current: "no maximum, no IM-midazolam bridge" | correct: "as quoted" | Add the 4 g total-maximum and IM-midazolam-bridge pearl under eclampsia.
- `AUD-0439` [MODERATE] row row absent — current: "none" | correct: "as quoted" | Add both magnesium cautions; the vitals-every-5-min tail is truncated in extraction - verify in PDF.
- `AUD-0440` [MODERATE] row row absent — current: "none" | correct: "as quoted" | Add the early hospital-notification pearl.
- `AUD-0441` [MODERATE] row row absent — current: "generic third-trimester bleeding" | correct: "Uterine rupture: severe vaginal bleeding, second half of pregnancy; abruptio: separation after 20 weeks, before birth" | Replace the generic bleeding criterion with the PEMS rupture and abruptio definitions.
- `AUD-0442` [MODERATE] row row absent — current: "none" | correct: "as quoted" | Add the age-risk pearl under abruptio.
- `AUD-0683` [MINOR] row row absent — current: "present" | correct: "not in PEMS - verify with medical director" | Flag for medical director verification; keep or remove.
- `AUD-0684` [MINOR] row row absent — current: "present" | correct: "not in PEMS - verify or remove" | Flag for medical director verification; not level-gated.

## protocols/medical/07_Sepsis_PROC.md

- `AUD-0106` [CRITICAL] row row 3 — current: "no concentration stated" | correct: "Norepinephrine 4 mg in 250 mL NS = 16 mcg/mL; Epinephrine 1 mg in 100 mL NS = 10 mcg/mL" | Add both mixing statements under row 3 (high-alert infusion cannot be dosed in mcg/min without concentration).
- `AUD-0108` [CRITICAL] row row 4 — current: "no SBP targets, no concentration" | correct: "Titrate SBP >70 mmHg (<1 yr) / >90 mmHg (>1 yr); 1 mg in 100 mL = 10 mcg/mL; IV pump preferred; watch for extravasation" | Add titration targets, 10 mcg/mL concentration and pump/extravasation note to row 4 (copy from Hypotension row 8).
- `AUD-0110` [CRITICAL] row row 5 — current: "no dilution stated" | correct: "100 mcg (1 mL of 0.1 mg/mL) in 9 mL NS = 10 mcg/mL" | Add the 10 mcg/mL dilution to row 5 (5-10 mcg volume depends on it).
- `AUD-0444` [MODERATE] row row 6 — current: "EMR blank, EMT blank, [A], I •, P •" | correct: "[EMR] [EMT] [A] [I] [P] (bare MC = every level contacts MC)" | Replace row 6 cells with bracketed MC at all five levels (I and P must contact MC; EMR and EMT get MC bracket).
- `AUD-0445` [MODERATE] row row absent — current: "> 2 seconds" | correct: "> 3 seconds" | Change CRT threshold in Signs & Symptoms from >2 s to >3 s (changes whether criterion is met).
- `AUD-0446` [MODERATE] row row absent — current: "no numeric thresholds" | correct: "SBP <70 (infant) / <90 (>1 yr); MAP <55 / <65; RR >60 / >30; HR <100 / <90 by age band" | Insert numeric age-banded thresholds from PEMS criteria table; verify column mapping in PDF (flattened table). | inferred: confirm in PDF before edit
- `AUD-0447` [MODERATE] row row absent — current: "HPI only" | correct: "Counted criterion ('High Risk') in the 2-or-more set" | Move High Risk into Signs & Symptoms as a criterion counted toward the 2-of-criteria requirement. | inferred: confirm in PDF before edit
- `AUD-0448` [MODERATE] row row absent — current: "no 250 mL bolus guidance, no early-vasopressor or MC-if-doubt advice" | correct: "250 mL boluses then reassess; early vasopressors if poor fluid tolerance; contact MC if in doubt" | Add the 250 mL bolus / early vasopressor / MC-if-in-doubt sentences to the CAUTION pearl.
- `AUD-0449` [MODERATE] row row absent — current: "partial list" | correct: "Full list incl. age <56 days, asplenia/sickle cell, immunosuppressant medications" | Add the PEMS high-risk list (age <56 days, asplenia/SCD, immunosuppressants) as a pearl.
- `AUD-0450` [MODERATE] row row absent — current: "pump only" | correct: "Vasopressor via largest, most proximal IV (AC or higher) or IO; verify patency; monitor for extravasation (pain, pallor, absent distal pulses, swelling)" | Verify exact PEMS wording in PDF p.130, then add access-site and extravasation guidance to the WARNING pearl. | inferred: confirm in PDF before edit
- `AUD-0685` [MINOR] row row absent — current: "present" | correct: "not in PEMS - verify against medical director source or remove" | Flag for medical director verification; not level-gated, no action change required.

## protocols/neurologic/05_Hypoglycemia_Hyperglycemia_PROC.md

- `AUD-0453` [MODERATE] row row absent — current: "absent" | correct: "present" | Add pearl verbatim (fallback to IO dextrose).
- `AUD-0454` [MODERATE] row row absent — current: "absent" | correct: "present" | Add pearl verbatim.
- `AUD-0455` [MODERATE] row row absent — current: "absent" | correct: "present" | Add pearl verbatim to the hyperglycemia fluid row (row 5).
- `AUD-0456` [MODERATE] row row absent — current: "absent" | correct: "present" | Add the recurrence-risk list verbatim (drives transport and reassessment decisions).
- `AUD-0686` [MINOR] row row 1 — current: "unconditional check; AMS trigger not stated" | correct: "AMS trigger stated (check blood glucose for any AMS patient)" | Optionally add the AMS trigger wording; the site check is broader than PEMS, so no harm.
- `AUD-0687` [MINOR] row row absent — current: "present" | correct: "not stated in PEMS Hypoglycemia; monograph gives no explicit D10-over-D50 rule" | Source to the Dextrose monograph or medical director, or remove.

## protocols/neurologic/05_Seizure_PROC.md

- `AUD-0116` [CRITICAL] row row 6 — current: "frail, hypotensive, elderly >65y" | correct: "frail, hypotensive, underweight, and/or elderly >65y" | Add 'underweight' to the half-dose criteria. PEMS midazolam monograph (p.205) defines underweight as <50 kg; the site omits this group, which is a benzodiazepine dosing error risk.
- `AUD-0461` [MODERATE] row row absent — current: "(absent)" | correct: "EMR: Follow Universal Patient Care" | Add universal care row with EMR cell.
- `AUD-0688` [MINOR] row row 7 — current: "initiate transport (no destination)" | correct: "initiate transport to closest emergency department" | Add 'to the closest emergency department'.

## protocols/neurologic/05_Stroke_TIA_PROC.md

- `AUD-0119` [CRITICAL] row row 6 — current: "<24 hrs only" | correct: "<24 hrs OR unknown onset" | Add 'or unknown' onset to row 6 so unknown-onset LVO patients route to CSC; row 7 currently leaves them unrouted.
- `AUD-0466` [MODERATE] row row 7 — current: "Primary Stroke Center only" | correct: "closest stroke center (any designated level)" | Replace 'closest Primary Stroke Center' with 'closest stroke center' per PEMS row text; cross-check against Stroke Field Triage flowchart (p.37), which allows Acute Stroke Ready, Primary or Comprehensive.
- `AUD-0467` [MODERATE] row row absent — current: "(absent)" | correct: "MC (all levels contact MC for guidance)" | Add MC contact row: 'Contact Medical Control for guidance as needed' with MC in all five cells.
- `AUD-0468` [MODERATE] row row absent — current: "(absent)" | correct: "full RACE scoring table" | Add the RACE scoring table (PEMS p.133) to the protocol.
- `AUD-0469` [MODERATE] row row absent — current: "(absent)" | correct: "onset-time determination pearl with symptom list" | Add PEMS pearl on determining onset time and the symptom list.
- `AUD-0689` [MINOR] row row 8 — current: "I+" | correct: "no level stated in PEMS (pearl)" | Either remove the level assignment or confirm with PEMS owner which level may place the IV; PEMS does not grant it at a level.
- `AUD-0690` [MINOR] row row 9 — current: "A+" | correct: "no level stated in PEMS (pearl)" | Confirm the level for the COR call against PEMS; PEMS gives it as a pearl only.
- `AUD-0691` [MINOR] row row absent — current: "no restriction on where endovascular therapy is available" | correct: "endovascular therapy available only at comprehensive/thrombectomy-capable centers" | Add 'available only at comprehensive/thrombectomy-capable stroke centers'.

## protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.md

- `AUD-0121` [CRITICAL] row row 5 — current: "A+" | correct: "EMT+" | Set EMT to • on row 5 (time-critical airway management narrowed from EMT to A).
- `AUD-0122` [CRITICAL] row row 10 — current: "P only (all ages)" | correct: "I for ≥12 years; P for <12 years" | Set I to • for ETI in patients ≥12 (rows 9 and 10); keep P-only for <12 and keep the red-dot note. Row 9 is the same root cause.
- `AUD-0470` [MODERATE] row row 1 — current: "EMT+" | correct: "EMR+" | Set EMR to • on row 1.
- `AUD-0471` [MODERATE] row row 6 — current: "I+" | correct: "A+" | Set A to • on row 6. Dose and repeat wording already match.
- `AUD-0472` [MODERATE] row row 7 — current: "I+" | correct: "A+" | Set A to • on row 7. Dose matches PEMS.
- `AUD-0473` [MODERATE] row row 8 — current: "I+" | correct: "A+" | Set A to • on row 8. Level token sits between the methylprednisolone row and the chlorine row in flattened text; verify on PDF p.153. | inferred: confirm in PDF before edit
- `AUD-0474` [MODERATE] row row 12 — current: "[I] at I, • at P" | correct: "MC in all five level cells (bare MC)" | Set MC in all five level cells.
- `AUD-0475` [MODERATE] row row absent — current: "absent" | correct: "refer to Nerve Agents protocol" | Add the exclusion/referral line to the criteria so organophosphate distress is routed to the Nerve Agents protocol.
- `AUD-0692` [MINOR] row row 8 — current: "confirmed-exposure wording" | correct: "suspected chlorine gas exposure" | Reword to 'suspected chlorine gas exposure' to match PEMS.

## protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md

- `AUD-0123` [CRITICAL] row row 6 — current: "P only" | correct: "I and P" | Set I ● on row 6. Time-critical bronchospasm drug narrowed from I to P.
- `AUD-0124` [CRITICAL] row row 8 — current: "I+ only" | correct: "EMT+ (PEMS EMT: consider CPAP; PEEP 5 initial; up to 10 at I/P)" | Set EMT ●, A ● on row 8 (CPAP authorized at EMT per RD R4 and CPAP procedure). | [OWNER]
- `AUD-0125` [CRITICAL] row row 8 — current: "3 contraindications" | correct: "8 PEMS contraindications" | Replace with the full PEMS contraindication list (pneumothorax, hypotension SBP<90/MAP<65, GCS<=13, facial trauma/burns/surgery, penetrating neck/chest trauma, mask intolerance are all omitted). | [OWNER]
- `AUD-0126` [CRITICAL] row row 9 — current: "EMT, A, I, P" | correct: "A and above" | Set EMT to blank on row 9. PEMS grants nebulized epinephrine at A only; EMT over-authorization of a high-alert drug is CRITICAL.
- `AUD-0476` [MODERATE] row row 1 — current: "EMT+" | correct: "EMR+" | Set EMR ● on row 1 (universal gating, consistent with AUD-0507).
- `AUD-0477` [MODERATE] row row 2 — current: "EMT+; target >=94%" | correct: "EMR+; target >94%" | Set EMR ● on row 2 and change >= to > 94% per PEMS.
- `AUD-0478` [MODERATE] row row 5 — current: "I+" | correct: "A+" | Set A ● on row 5 (dose already matches).
- `AUD-0479` [MODERATE] row row 6 — current: "requires failure of initial therapy" | correct: "for severe symptoms (no unresponsive-to-therapy precondition)" | Replace the trigger with PEMS 'for severe symptoms'; the added precondition delays Mg and changes the action.
- `AUD-0480` [MODERATE] row row 8 — current: "initiate 5-10" | correct: "initial PEEP 5; titrate up to 10 at I/P only" | Set initial PEEP 5 for all levels; restrict titration to 10 at I and P. | [OWNER]
- `AUD-0481` [MODERATE] row row 10 — current: "I+" | correct: "A+" | Set A ● on row 10 (same root cause as AUD-0478).
- `AUD-0482` [MODERATE] row row absent — current: "absent" | correct: "PEMS epinephrine-in-CHF caution with MC for doubt" | Add the PEMS caution as a pearl adjacent to row 9.
- `AUD-0483` [MODERATE] row row absent — current: "absent" | correct: "PEMS wheeze-paradox pearl" | Add the PEMS wheeze-paradox and response-judgment pearl.

## protocols/respiratory/03_Pediatric_Stridor_PROC.md

- `AUD-0127` [CRITICAL] row row 4 — current: "A+" | correct: "EMR+" | Set EMR and EMT to • for supplemental oxygen to SpO2 >94%. The 'high-flow' device wording is not in PEMS (PEMS says supplemental oxygen); medical director to decide.
- `AUD-0128` [CRITICAL] row row 6 — current: "P only" | correct: "EMT+ per PEMS general RD/CPAP text; PEMS CPAP indication is respiratory distress from pulmonary edema/infection/near-drowning (upper airway obstruction is not listed)" | Medical director decision first: if CPAP is intended for stridor, set EMT+ (and PEEP 5 mmHg, not cmH2O) and note red-dot status; if not intended, remove the CPAP row rather than re-leveling it. Do not
- `AUD-0129` [CRITICAL] row row 10 — current: "no level (blocked at all levels)" | correct: "A+" | Set A to • (and above). Site's 'moderate to severe' qualifier is not in the PEMS stridor epinephrine line; keep only if medical director approves.
- `AUD-0130` [CRITICAL] row row absent — current: "I may attempt pediatric intubation with MC" | correct: "I not permitted for <12 (Paramedic only)" | Rewrite pearl 1: pediatric (<12) intubation is Paramedic-only per PEMS. Delete the 'Intermediate providers must contact MC' permission. Aligns with row 11.
- `AUD-0484` [MODERATE] row row 1 — current: "EMT+" | correct: "EMR+" | Set EMR to • on row 1.
- `AUD-0485` [MODERATE] row row 8 — current: "P only; references a dosing table that is not in the file" | correct: "A+ for moderate to severe symptoms" | Set A to • with the moderate-to-severe condition; delete 'per dosing table below' or add the table (doses already inline).
- `AUD-0486` [MODERATE] row row 9 — current: "P only" | correct: "A+ (IV/IO needed for A-level IV methylprednisolone)" | Set A to • on IV/IO access. Inferred from the A-level IV route; verify the intended scope on PDF p.124. | inferred: confirm in PDF before edit
- `AUD-0487` [MODERATE] row row 11 — current: "[P] - P only with MC bracket" | correct: "<12: P only, no MC bracket in PEMS; ≥12: I" | Pediatric scope decision needed. For <12, P only, remove the MC bracket unless the medical director adds it. For ≥12, add I. If the protocol's population includes ≥12-year-olds, escalate this row to CRITICAL.
- `AUD-0488` [MODERATE] row row absent — current: "absent" | correct: "RSI not addressed in PEMS; refer to agency protocols" | Add the RSI note to the advanced-airway row or pearls.

## protocols/respiratory/03_Pneumothorax_PROC.md

- `AUD-0131` [CRITICAL] row row 13 — current: "P only" | correct: "I (>=12 years) and P (<12 years)" | Set I ● on row 13; keep P for <12 years.
- `AUD-0489` [MODERATE] row row 1 — current: "EMT+" | correct: "EMR+" | Set EMR ● on row 1.
- `AUD-0490` [MODERATE] row row 2 — current: "EMT+" | correct: "EMR+" | Set EMR ● on row 2.
- `AUD-0491` [MODERATE] row row 3 — current: "EMT+" | correct: "EMR+" | Set EMR ● on row 3.
- `AUD-0492` [MODERATE] row row 4 — current: "A+ for cardiac monitoring" | correct: "I+ for cardiac monitoring; A+ for IV/IO access" | Split row 4: keep IV/IO at A+; move continuous cardiac monitoring to I+ (or confirm owner intent). Cross-protocol, verify against Universal batch. | inferred: confirm in PDF before edit
- `AUD-0493` [MODERATE] row row 5 — current: "A+" | correct: "EMR+ for suctioning" | Set EMR and EMT ● for the suction step; keep airway-intervention preparation at A+ if owner wishes.
- `AUD-0494` [MODERATE] row row 9 — current: "suspicion of thoracoabdominal trauma" | correct: "evidence of significant blunt or penetrating thoracoabdominal trauma" | Replace 'suspicion' with PEMS 'evidence of significant ... trauma'; trigger change alters bilateral vs unilateral action.
- `AUD-0495` [MODERATE] row row 10 — current: "EMT+" | correct: "I+ for decompression reassessment (basic vitals at EMR per Universal, owner to confirm)" | Owner question: confirm whether basic reassessment at EMT is intended; PEMS procedure is I-level. | inferred: confirm in PDF before edit
- `AUD-0496` [MODERATE] row row absent — current: "absent" | correct: "PEMS failure-rate, second-attempt, and assume-PTX pearls" | Add the PEMS failure-rate, second-attempt and assume-PTX pearls.

## protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md

- `AUD-0132` [CRITICAL] row row 3 — current: "EMT+" | correct: "EMR+" | Set EMR to • on row 3 (time-critical oxygen in respiratory distress).
- `AUD-0133` [CRITICAL] row row 4 — current: "A+; 'for severe respiratory distress'" | correct: "EMT+; PEMS indication = respiratory distress due to pulmonary edema/infection/near-drowning" | Set EMT to • for CPAP and initial settings; remove 'for severe respiratory distress' unless the medical director approves. Note PEEP unit cmH2O vs PEMS mmHg (MINOR, same row). Rows 6-8 contraindications are content-correct and should move with 
- `AUD-0134` [CRITICAL] row row 10 — current: "I+" | correct: "A+" | Set A to • on row 10 (A and above).
- `AUD-0135` [CRITICAL] row row 10 — current: "omitted" | correct: "contraindications: hypotension, PDE-5 inhibitor use, allergy, <12 years; pre-checks: IV access, SBP≥100/MAP≥65, PDE-inhibitor assessment" | Add the nitroglycerin contraindications and pre-administration checks (PDE-5 inhibitor exclusion is high-risk). | [OWNER]
- `AUD-0136` [CRITICAL] row row 11 — current: "I+; MAP > 65" | correct: "A+; MAP 65 (≥65)" | Set A to • on row 11; change MAP '> 65' to '≥ 65' (PEMS 65 / pre-check ≥65).
- `AUD-0137` [CRITICAL] row row 12 — current: "caution only; no contraindication list" | correct: "contraindications: pregnancy; hypovolemia/dehydration; SBP <110 or MAP <65" | Add the furosemide contraindication list (SBP<110/MAP<65 is stricter than the nitro threshold and must be stated).
- `AUD-0497` [MODERATE] row row 1 — current: "EMT+" | correct: "EMR+" | Set EMR to • on row 1.
- `AUD-0498` [MODERATE] row row 2 — current: "EMT+" | correct: "EMR+" | Set EMR to • on row 2.
- `AUD-0499` [MODERATE] row row 9 — current: "P only; cap 10" | correct: "EMT+; PEEP range 9-15 mmHg (confirm on PDF)" | Set EMT to • for titration; change cap to the PEMS range (confirm 15 vs 10 on PDF).
- `AUD-0500` [MODERATE] row row 12 — current: "P only" | correct: "I+" | Set I to • on row 12 (I and above). Dose matches PEMS.
- `AUD-0501` [MODERATE] row row absent — current: "omitted" | correct: "aspiration caution, conscious/alert only, remove mask if vomiting, consider RSI, needle thoracostomy for pneumothorax" | Add the CPAP pearl content from PEMS p.246.

## protocols/respiratory/03_Respiratory_Arrest_PROC.md

- `AUD-0138` [CRITICAL] row row 6 — current: "A+" | correct: "EMT+" | Set EMT ● on row 6. EMT is blocked from BVM for an apneic patient, a time-critical life-saving intervention.
- `AUD-0139` [CRITICAL] row row 8 — current: "P only" | correct: "I and P" | Set I ● on row 8.
- `AUD-0140` [CRITICAL] row row 9 — current: "no level for any provider" | correct: "P only" | Set P ● on row 9. Pediatric intubation at P only per PEMS; site blank omits even P.
- `AUD-0141` [CRITICAL] row row 10 — current: "P only" | correct: "I and P" | Set I ● on row 10. | inferred: confirm in PDF before edit
- `AUD-0142` [CRITICAL] row row 11 — current: "no level for any provider" | correct: "P (decode inferred)" | Set P ● on row 11 after human PDF check on ETI p.248; the surgical airway is a life-saving last-resort step. | inferred: confirm in PDF before edit
- `AUD-0143` [CRITICAL] row row 12 — current: "P only" | correct: "I and P" | Set I ● on row 12 after PDF check of ETI p.248. | inferred: confirm in PDF before edit
- `AUD-0144` [CRITICAL] row row 13 — current: "P only" | correct: "EMT and above" | Set EMT ●, A ●, I ● on row 13. EMT is blocked from ETT monitoring.
- `AUD-0145` [CRITICAL] row row 14 — current: "no level for any provider" | correct: "I and P" | Set I ● and P ● on row 14 (high-alert opioid).
- `AUD-0146` [CRITICAL] row row 15 — current: "no level for any provider" | correct: "I and P" | Set I ● and P ● on row 15 (high-alert benzodiazepine).
- `AUD-0147` [CRITICAL] row row absent — current: "absent" | correct: "MC in all level cells (bare MC)" | Add the bare-MC contact row for sedation (all levels must contact MC when agitation not manageable) to the midazolam row or a new row. | inferred: confirm in PDF before edit
- `AUD-0502` [MODERATE] row row 1 — current: "EMT+" | correct: "EMR+" | Set EMR ● on row 1.
- `AUD-0503` [MODERATE] row row 5 — current: "EMT+" | correct: "EMR+" | Set EMR ● on row 5.
- `AUD-0504` [MODERATE] row row 5 — current: "no 100% O2 / 3-minute duration" | correct: "100% O2 via NRB or BVM for 3 minutes; monitor SpO2" | Add 100% O2 via NRB or BVM for 3 minutes.
- `AUD-0505` [MODERATE] row row 7 — current: "A+" | correct: "EMT+" | Set EMT ● on row 7 (same root cause as AUD-0138).
- `AUD-0506` [MODERATE] row row absent — current: "absent" | correct: "I and P (decode inferred)" | Add a preparation row at I (confirm level on PDF). | inferred: confirm in PDF before edit

## protocols/respiratory/03_Respiratory_Distress_PROC.md

- `AUD-0148` [CRITICAL] row row 6 — current: "A and I require MC; EMT blank; P blank" | correct: "EMT, A, I, P standing (no MC bracket in PEMS)" | Set EMT, A, I and P to ● on row 6 and remove MC from A/I (see row 6, docs/protocols/respiratory/03_Respiratory_Distress_PROC.md). CPAP is a red-dot procedure at all levels per PEMS CPAP procedure. | [OWNER]
- `AUD-0149` [CRITICAL] row row 7 — current: "no level for any provider" | correct: "EMT, A, I, P (EMT level per PEMS)" | Set EMT ●, A ●, I ●, P ● on row 7 (EMT SGA is a PEMS EMT-level airway).
- `AUD-0150` [CRITICAL] row row 8 — current: "P only" | correct: "I and P (ETI >=12 years at I; <12 years at P per ETI procedure)" | Set I ● on row 8; keep P for <12 years per ETI procedure. Row text already says I-level; the cell contradicts it.
- `AUD-0151` [CRITICAL] row row 11 — current: "A and I require MC; P blank" | correct: "A, I, P standing (no MC bracket)" | Remove MC from A and I; set P ● (level and above may perform). Time-critical airway drug; the MC requirement narrows A and P omitted.
- `AUD-0152` [CRITICAL] row row 13 — current: "no level for any provider" | correct: "A, I, P (A and above)" | Set A ●, I ●, P ● on row 13 (same drug/policy as chest pain audit, where nitro narrowing was treated CRITICAL). | inferred: confirm in PDF before edit
- `AUD-0153` [CRITICAL] row row 14 — current: "no level for any provider; dose only by reference" | correct: "I and above, with Mg dose stated here or referenced" | Set I ● and P ● on row 14. The Asthma file narrows Mg to P only (see Asthma C1 finding), so the two files must agree on I.
- `AUD-0154` [CRITICAL] row row 16 — current: "P only" | correct: "EMT, A, I, P" | Set EMT ●, A ●, I ● on row 16 for BVM ventilation (EMT and above per Airway Management procedure).
- `AUD-0155` [CRITICAL] row row absent — current: "no PDE-inhibitor contraindication anywhere in the respiratory folder; no IV-access prerequisite" | correct: "PDE-inhibitor contraindication, IV access, SBP>=100 / MAP>=65 before nitro" | Add the PDE-inhibitor contraindication and the IV-access and SBP/MAP prerequisites to the nitroglycerin row and pearl 7 before any further edit to row 13. | [OWNER]
- `AUD-0510` [MODERATE] row row 4 — current: "COPD target 88-92%" | correct: "SpO2 >94% (no COPD exception in PEMS text)" | Remove the 88-92% COPD target or obtain owner/medical director ruling; it changes the O2 action versus PEMS. Owner question. | [OWNER]
- `AUD-0511` [MODERATE] row row 6 — current: "MC required at A and I" | correct: "No MC requirement at A/I for CPAP" | Remove the MC requirement at A and I; align pearl 3 with the PEMS cell. | [OWNER]
- `AUD-0512` [MODERATE] row row 9 — current: "I+" | correct: "A+" | Set A ● on row 9 (cross-referenced to Universal Patient Care; verify against Universal batch). | inferred: confirm in PDF before edit
- `AUD-0513` [MODERATE] row row 11 — current: "simultaneous, no severity condition" | correct: "conditional: only for moderate to severe symptoms" | Restore the 'for moderate to severe symptoms' condition and drop 'simultaneously' unless owner directs.
- `AUD-0514` [MODERATE] row row 12 — current: "no level for any provider" | correct: "A and above" | Set A ●, I ●, P ● on row 12. Add the suction-as-needed step and 'due to secretions' repeat trigger.
- `AUD-0515` [MODERATE] row row 13 — current: "MAP >65" | correct: "MAP 65 (PEMS prerequisite text: SBP >=100 and MAP >=65)" | Change MAP >65 to MAP >=65 to match PEMS; boundary change affects the action at MAP exactly 65.
- `AUD-0516` [MODERATE] row row absent — current: "absent" | correct: "Furosemide 40 mg IV/IO slow push, I and above" | Add furosemide 40 mg IV/IO slow push at I (with P) to the pulmonary edema section; no existing site row covers it. | inferred: confirm in PDF before edit
- `AUD-0517` [MODERATE] row row absent — current: "absent" | correct: "PEMS caution with the CHF/asthma-epinephrine overlap, with MC for doubt" | Add the PEMS epinephrine-in-CHF caution and MC-for-doubt instruction as a pearl.
- `AUD-0518` [MODERATE] row row absent — current: "absent" | correct: "PEMS wheeze-paradox and judge-response pearl" | Add the PEMS pearl on paradoxical worsening of wheeze and response-based escalation.
- `AUD-0519` [MODERATE] row row absent — current: "absent" | correct: "PEMS RSI note" | Add the PEMS RSI scope note to the advanced airway row or pearls.

## protocols/respiratory/03_Smoke_Inhalation_PROC.md

- `AUD-0156` [CRITICAL] row row 9 — current: "no dose stated" | correct: "Adult 5 g IV/IO over 15 min; Pediatric 70 mg/kg IV/IO over 15 min; (if available)" | Insert PEMS adult and pediatric doses and infusion time for a high-alert antidote; OMD guidance may supplement but not replace the PEMS dose.
- `AUD-0157` [CRITICAL] row row 11 — current: "I+ ; no volumes or trigger" | correct: "A+ ; SBP<90 & TBSA>20% trigger; 500 / 250 / 125 mL/hr" | Move to A+; add trigger and the three rates, or confirm the referenced Burn Injuries protocol carries them.
- `AUD-0158` [CRITICAL] row row absent — current: "airway-involving burns routed to burn center; no airway-priority rule" | correct: "airway compromise / impending arrest → closest ED (MC if unclear); burn center only when none apply; airway/hemodynamic priority" | Rewrite pearl 7 and row 14 with PEMS destination priority; state that airway compromise goes to closest ED and burn-center routing follows only when no airway/arrest criteria 
- `AUD-0522` [MODERATE] row row 5 — current: "P" | correct: "I and P (no MC bracket in PEMS)" | Add I to the consider-ETI-vs-transport decision row. Net I-level ETI is also available via row 6 (MC-bracketed); see row 6, docs/protocols/respiratory/03_Smoke_Inhalation_PROC.md.
- `AUD-0523` [MODERATE] row row 6 — current: "[I] (I must contact MC)" | correct: "I (no MC bracket)" | Replace [I] with • at I unless the medical director adds an MC requirement; keep the <12 red-dot warning.
- `AUD-0524` [MODERATE] row row 7 — current: "trigger list omits suspected cyanide poisoning; [I] bracket" | correct: "trigger list includes suspected cyanide poisoning; I (no bracket)" | Add 'or suspected cyanide poisoning' to the trigger; remove [I] unless medical director directs.
- `AUD-0525` [MODERATE] row row 8 — current: "No transfer-spike, fill-to-line, mixing (invert/rock ≥60 s, do not shake) steps" | correct: "Add transfer-spike, fill-to-line, invert/rock ≥60 s, do not shake" | Add the PEMS mixing steps verbatim in substance.
- `AUD-0526` [MODERATE] row row 12 — current: "[I] at I, • at P" | correct: "MC in all five level cells (bare MC)" | Set MC in all five level cells per doctrine (bare MC = all levels).
- `AUD-0527` [MODERATE] row row 12 — current: "vague 'significant burn injuries'" | correct: "PEMS burn-center criteria list (inhalation injuries explicitly listed)" | Replace 'significant burn injuries' with the PEMS criteria list.
- `AUD-0528` [MODERATE] row row absent — current: "absent" | correct: "A+ IV/IO access on non-burned extremity" | Add an IV/IO access row at A+ (non-burned site first).
- `AUD-0529` [MODERATE] row row absent — current: "no RSI scope statement" | correct: "RSI Paramedic-only; not addressed in PEMS" | Add the PEMS RSI scope statement to pearl 2.

## protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md

- `AUD-0161` [CRITICAL] row row 12 — current: "P bracketed MC; I omitted" | correct: "I and P standing (no MC)" | Set I ● and remove the [P] MC bracket. I is omitted from adult ETI and P is over-restricted. | inferred: confirm in PDF before edit
- `AUD-0162` [CRITICAL] row row absent — current: "absent" | correct: "Epinephrine 3 mg nebulized repeat once, A and above; methylprednisolone conditional, A and above" | Add the stridor epinephrine and methylprednisolone rows at A and above, cross-referencing the Asthma file rows 9-10 for consistency. | inferred: confirm in PDF before edit
- `AUD-0530` [MODERATE] row row 1 — current: "EMT+" | correct: "EMR+" | Set EMR ● on row 1.
- `AUD-0531` [MODERATE] row row 9 — current: "EMT+" | correct: "EMR+" | Set EMR ● on row 9.
- `AUD-0532` [MODERATE] row row 13 — current: "I bracketed MC; fentanyl fixed at 25 mcg" | correct: "I and P standing; fentanyl 25-50 mcg; midazolam 2.5 mg" | Remove the [I] MC bracket; restate fentanyl as 25-50 mcg; cross-reference the Respiratory Arrest rows 14-15 once they carry levels. | inferred: confirm in PDF before edit
- `AUD-0533` [MODERATE] row row 14 — current: "I bracketed MC" | correct: "I standing per PEMS ETI for >=12; MC bracket un-sourced" | Remove the [I] bracket unless the medical director directs; the MC-for-complex-airways guidance can stay as text. | inferred: confirm in PDF before edit

## protocols/toxicology/06_Nausea_Vomiting_PROC.md

- `AUD-0538` [MODERATE] row row 4 — current: "no repeat instruction" | correct: "May repeat in 10-15 minutes as needed" | Add 'May repeat in 10-15 minutes, as needed' to rows 4 and 5.
- `AUD-0540` [MODERATE] row row 6 — current: "EMR blank, EMT blank, [A], I •, P •" | correct: "[EMR] [EMT] [A] [I] [P] (bare MC)" | Replace row 6 with bracketed MC at all five levels (same class as SEP-09 and F-BR-14).
- `AUD-0541` [MODERATE] row row absent — current: "over 2-5 minutes" | correct: "at least 30 seconds, preferably 2 minutes" | Replace with 'at least 30 seconds, preferably 2 minutes' (threshold drift; does not change action but differs from source).
- `AUD-0542` [MODERATE] row row absent — current: "no QTc threshold, no named QT-prolonging drugs" | correct: "QTc >=500 ms and co-administered QT-prolonging drugs (amiodarone, haloperidol) - assess before giving" | Add the QTc >=500 ms threshold and the amiodarone/haloperidol examples.
- `AUD-0543` [MODERATE] row row absent — current: "prophylaxis 'generally not recommended'" | correct: "prophylactic or pre-emetic dosing is often more effective (per PEMS)" | Reconcile with PEMS wording (or medical director decision, documented). Site statement directly conflicts with PEMS.
- `AUD-0693` [MINOR] row row absent — current: "present" | correct: "not in PEMS - verify or remove" | Flag for medical director verification; not level-gated.

## protocols/toxicology/06_Nerve_Agents_PROC.md

- `AUD-0166` [CRITICAL] row row 6 — current: "DuoDote unavailable only" | correct: "symptoms persist OR DuoDote unavailable" | Replace '(Use if DuoDote unavailable)' with 'If symptoms persist, or if DuoDote is unavailable'. As written, atropine is never a second line after DuoDote fails.
- `AUD-0167` [CRITICAL] row row absent — current: "no weight bands or doses" | correct: "Yellow <7 kg 0.25 mg; Blue 7-18 kg 0.5 mg; Red 18-41 kg 1 mg; Green >41 kg 2 mg" | Insert the four AtroPen weight bands and doses from PEMS; a bare reference to 'weight-based dosing guidelines' leaves the dose undefined for a high-alert drug.
- `AUD-0168` [CRITICAL] row row absent — current: "unbounded repeated atropine" | correct: "repeat q5 min up to three doses (row cap)" | Delete 'Large and repeated doses may be required' or replace with the PEMS three-dose cap and medical control contact.
- `AUD-0547` [MODERATE] row row absent — current: "4 military agents" | correct: "pesticide OP/carbamates plus Sarin, Soman, Tabun, VX, Novichok" | Add pesticide OP/carbamate examples and Novichok to the pearl.
- `AUD-0548` [MODERATE] row row absent — current: "decon must occur prior to transport" | correct: "decon and PPE per row 2; do not proceed until reasonably safe; SCBA / chemical protective clothing" | Replace 'Decontamination must occur prior to transport' with the PEMS language and add SCBA/chem protective clothing requirement.
- `AUD-0549` [MODERATE] row row absent — current: "(absent)" | correct: "off-gassing after decon; SCBA and chemical protective clothing" | Add off-gassing and PPE pearl.
- `AUD-0550` [MODERATE] row row absent — current: "(absent)" | correct: "small exposures (≤1 mL) can be symptomatic; onset up to 18 h" | Add delayed-onset and small-exposure pearl.
- `AUD-0551` [MODERATE] row row absent — current: "(absent)" | correct: "recovery position for non-ambulatory patients not transported immediately" | Add recovery position pearl.
- `AUD-0694` [MINOR] row row 5 — current: "'based on symptom severity'" | correct: "'If symptoms persist'; 'If available'" | Replace with PEMS wording.

## protocols/toxicology/06_Overdose_Poisoning_PROC.md

- `AUD-0173` [CRITICAL] row row 7 — current: "20 mg/kg, no maximum" | correct: "20 mg/kg, max 1 g, then 20 mL NS flush" | Add maximum dose 1 g and the 20 mL NS flush to the pediatric CaCl line.
- `AUD-0174` [CRITICAL] row row 7 — current: "0.5-1 mg range, no weight band" | correct: "<25 kg: 0.5 mg; ≥25 kg: 1 mg" | Replace '0.5-1 mg' with the two weight bands from PEMS.
- `AUD-0177` [CRITICAL] row row absent — current: "(absent)" | correct: "I: Hydroxocobalamin (CYANOKIT) 5 g IV/IO over 15 min (adult); 70 mg/kg (pediatric); reconstitute with 200 mL NS" | Add cyanide section: hydroxocobalamin row at I with dosing, indications, reconstitution steps. Note PEMS states it is not in the regional drug box. | inferred: confirm in PDF before edit
- `AUD-0555` [MODERATE] row row 3 — current: "no SpO2 target" | correct: "maintain SpO2 94-98%" | Add 'maintain SpO2 94-98%' to row 3.
- `AUD-0556` [MODERATE] row row 5 — current: "no apneic/bradypneic trigger; no repeat" | correct: "if apneic/bradypneic; repeat at double initial dose if no response in 5 min" | Add the apneic/bradypneic trigger and the 5-minute repeat-at-double instruction.
- `AUD-0557` [MODERATE] row row 6 — current: "no repeat instruction" | correct: "repeat at double the initial dose if no response in 5 minutes" | Add repeat-at-double instruction to row 6 (adult and pediatric).
- `AUD-0558` [MODERATE] row row 7 — current: "no indication" | correct: "if hypotensive with signs of poor perfusion; if no response, refer to Hypotension and Shock" | Add the hypotension/poor-perfusion indication and the Hypotension and Shock referral.
- `AUD-0559` [MODERATE] row row 8 — current: "no bronchorrhea trigger; no repeat" | correct: "for respiratory distress due to bronchorrhea; repeat every 5 min until secretions reduce" | Add the bronchorrhea indication and the q5min repeat-to-effect instruction.
- `AUD-0561` [MODERATE] row row 10 — current: ">100 ms (pearl); no arrhythmia trigger" | correct: ">120 ms adult / >90 ms ped, or arrhythmia" | Correct pearl to adult >120 ms / ped >90 ms and add 'or arrhythmia' trigger.
- `AUD-0562` [MODERATE] row row 10 — current: "no repeat" | correct: "repeat once in 5-10 min for cardiac arrest or persistent ECG changes" | Add repeat instruction to row 10.
- `AUD-0563` [MODERATE] row row absent — current: "(absent)" | correct: "EMR: refer to Seizure protocol" | Add referral row at EMR.
- `AUD-0564` [MODERATE] row row absent — current: "(absent)" | correct: "MC (all levels contact MC)" | Add the MC contact row to the cyanide section with MC in all cells.
- `AUD-0565` [MODERATE] row row absent — current: "(absent)" | correct: "Poison Control 1-800-222-1222; not online medical control" | Add Poison Control pearl with the 'not online medical control' caveat.
- `AUD-0566` [MODERATE] row row absent — current: "(absent)" | correct: "low threshold to transport well-appearing children after toxic ingestion" | Add pediatric transport pearl.
- `AUD-0695` [MINOR] row row 8 — current: "'>40 kg'" | correct: "'≥40 kg'" | Change '>40kg' to '≥40kg' so exactly 40 kg is dosed.

## protocols/trauma/09_Burns_Thermal_PROC.md

- `AUD-0178` [CRITICAL] row row 6 — current: "no level for any provider (row blank)" | correct: "Level not determinable from flattened PEMS text. Human must confirm the level in the PDF before the cells are populated." | Adjudicate the HF calcium level from the PDF p.88 and populate the level cells. Treated as CRITICAL until resolved because a high-alert drug row has no authorized provider. | inferred: confirm in PDF before edit
- `AUD-0179` [CRITICAL] row row absent — current: "absent" | correct: "A: adult 500 mL/hr; ped 6-12 y 250 mL/hr; ped <=5 y 125 mL/hr when SBP <90 and TBSA >20%" | Add the A-level fluid row with its SBP and TBSA trigger and the three rates (rates copied from the verified Electrical page).
- `AUD-0180` [CRITICAL] row row absent — current: "absent" | correct: "I: consider ETI vs immediate transport to nearest ED for airway-injury signs" | Add the I-level airway-injury row with its signs list.
- `AUD-0181` [CRITICAL] row row absent — current: "absent" | correct: "Pediatric (<12 y) intubation: Paramedic red-dot skill only" | Add the red-dot scope limit to the airway row (see row absent, docs/protocols/trauma/09_Burns_Thermal_PROC.md).
- `AUD-0182` [CRITICAL] row row absent — current: "absent" | correct: "I: hydroxocobalamin 5 g IV/IO over 15 min (adult); 70 mg/kg (pediatric); reconstitution per PEMS" | Add the I-level hydroxocobalamin row with the doses and reconstitution steps.
- `AUD-0572` [MODERATE] row row 7 — current: "eyes, ears, perineum omitted; impending arrest omitted" | correct: "full PEMS list: face, eyes, ears, hands, feet, genitalia, perineum, skin over major joints; cardiac arrest, impending arrest, or airway compromise" | Complete the burn-center and closest-ED criteria lists to PEMS wording.
- `AUD-0573` [MODERATE] row row absent — current: "absent" | correct: "EMR: follow Universal Patient Care" | Add the EMR universal-care row.

## protocols/trauma/09_Crush_Syndrome_PROC.md

- `AUD-0184` [CRITICAL] row row 4 — current: "I+P, no MC requirement" | correct: "[A] - A must contact MC; I and P standing; levels below may not perform" | Set row 4 to [A] with MC contact required at A (A blocked from continuous albuterol in the site). Human check on the PDF: the bracket sits across the row 3 and row 4 tokens. | inferred: confirm in PDF before edit
- `AUD-0185` [CRITICAL] row row 5 — current: "I+P, no MC requirement" | correct: "[I] - I must contact MC; P standing; A may not perform" | Add the MC requirement at I (high-alert drug) and keep the I+ level. Dose verified. Human check on the PDF: the bracket is a two-token pair. | inferred: confirm in PDF before edit
- `AUD-0186` [CRITICAL] row row 6 — current: "I+P, no MC requirement" | correct: "[I] - I must contact MC; P standing; A may not perform" | Add the MC requirement at I (high-alert drug) and keep the I+ level. Dose verified. Human check on the PDF. | inferred: confirm in PDF before edit
- `AUD-0576` [MODERATE] row row 4 — current: "timing omitted" | correct: "when able, initiate prior to release" | Add the initiate-prior-to-release timing to row 4. | inferred: confirm in PDF before edit
- `AUD-0577` [MODERATE] row row 7 — current: "A+" | correct: "I+" | Set the monitor row to I+ (A over-granted).

## protocols/trauma/09_Electrical_Injuries_PROC.md

- `AUD-0190` [CRITICAL] row row absent — current: "absent" | correct: "I: consider ETI vs immediate transport to nearest ED for airway-injury signs" | Add the I-level airway-injury row with its signs list and the ETI-procedure reference.
- `AUD-0191` [CRITICAL] row row absent — current: "absent" | correct: "Pediatric (<12 y) intubation: Paramedic red-dot skill only" | Add the red-dot scope limit to the airway row (see row absent, docs/protocols/trauma/09_Electrical_Injuries_PROC.md) and state the RSI-is-not-in-regional-protocols note.
- `AUD-0584` [MODERATE] row row 7 — current: "A+" | correct: "I+" | Set monitor part to I+ (A over-granted). Human check on the PDF: the A and I tokens are split. | inferred: confirm in PDF before edit
- `AUD-0586` [MODERATE] row row absent — current: "absent" | correct: "MC (all levels): destination guidance with burn-center criteria" | Add the MC destination row and the burn-center criteria list.
- `AUD-0587` [MODERATE] row row absent — current: "absent" | correct: "Airway/inhalation injury pearl (p.97)" | Add the pearl.
- `AUD-0588` [MODERATE] row row absent — current: "absent" | correct: "Hypotension solely from burns <20% TBSA unlikely; assess for trauma, cardiac, cyanide" | Add the pearl.
- `AUD-0589` [MODERATE] row row absent — current: "absent" | correct: "IV through burned area only if no other site" | Add the pearl.
- `AUD-0590` [MODERATE] row row absent — current: "absent" | correct: "Stabilize first; do not bypass trauma center for burn center if unstable" | Add the pearl.

## protocols/trauma/09_Hemorrhage_Control_PROC.md

- `AUD-0193` [CRITICAL] row row 2 — current: "No depressed-skull-fracture exclusion; hemostatic dressing listed beside direct pressure" | correct: "Direct pressure only if no depressed skull fracture; hemostatic dressing only if direct pressure ineffective" | Add the depressed-skull-fracture exclusion and make hemostatic dressing conditional on failed direct pressure.
- `AUD-0196` [CRITICAL] row row 4 — current: "No tighten-to-pulse-loss endpoint; no not-over-a-joint rule; no commercial-device wording" | correct: "Tighten until distal pulse is no longer palpable; continually reassess; not over a joint; commercial tourniquet" | Add the endpoint, reassessment, not-over-a-joint and commercial-device statements to row 4.
- `AUD-0197` [CRITICAL] row row 4 — current: "absent" | correct: "EMR: if tourniquet(s) not controlling bleeding, continuously maintain direct pressure to wound over packing" | Add this EMR step under row 4.
- `AUD-0201` [CRITICAL] row row absent — current: "BP cuff authorized as tourniquet substitute" | correct: "Commercial tourniquet only; no substitute in PEMS" | Delete the BP-cuff sentence. Human check: confirm no agency-approved substitute exists before any reinstatement.
- `AUD-0592` [MODERATE] row row 9 — current: "MC for all levels" | correct: "No MC gate in PEMS Hemorrhage Control" | Remove the MC-gating row; the closest-ED transport rule for uncontrolled hemorrhage is sourced to PEMS Trauma p.83 (EMT) and carries no MC gate.
- `AUD-0593` [MODERATE] row row absent — current: "absent" | correct: "EMR: monitor airway and breathing; reassess bleeding after treatments" | Add an EMR row for monitor airway and breathing and reassess bleeding.
- `AUD-0594` [MODERATE] row row absent — current: "present" | correct: "absent from PEMS" | Remove unless sourced to an approved PEMS or agency protocol.
- `AUD-0696` [MINOR] row row 5 — current: "hemostatic gauze as the default; no secure-for-transport step" | correct: "roller gauze (hemostatic if available); secure dressing for transport" | Reword to PEMS gauze wording and add the secure-for-transport step.
- `AUD-0697` [MINOR] row row 6 — current: "chest seal only; no vented or three-sided occlusive dressing" | correct: "vented or three-sided occlusive dressing or chest seal" | Add the vented or three-sided occlusive option.
- `AUD-0698` [MINOR] row row 8 — current: "EMT+ on a row with no PEMS table row" | correct: "No PEMS table row or level; pearl only" | Keep as a pearl or drop the leveled row; do not present an unsourced leveled row.
- `AUD-0699` [MINOR] row row absent — current: "adds report to ED" | correct: "date/time/location written on tourniquet" | Drop the report-to-ED clause or source it.
- `AUD-0700` [MINOR] row row absent — current: "no criteria statement" | correct: "criteria: uncontrolled or profuse external bleeding; refer to Trauma for general care" | Add the criteria statement and the Trauma cross-reference.

## protocols/trauma/09_Lightning_Injuries_PROC.md

- `AUD-0204` [CRITICAL] row row absent — current: "absent" | correct: "I: consider ETI vs immediate transport to nearest ED for airway-injury signs" | Add the I-level airway-injury row (source is the Electrical p.95 row, which applies to lightning).
- `AUD-0205` [CRITICAL] row row absent — current: "absent" | correct: "Pediatric (<12 y) intubation: Paramedic red-dot skill only" | Add the red-dot scope limit with the airway row (see row absent, docs/protocols/trauma/09_Lightning_Injuries_PROC.md).
- `AUD-0601` [MODERATE] row row 7 — current: "A+" | correct: "I+" | Set the monitor part to I+ (A over-granted). Human check on the PDF. | inferred: confirm in PDF before edit
- `AUD-0603` [MODERATE] row row absent — current: "absent" | correct: "MC (all levels): destination guidance with burn-center criteria" | Add the MC destination row with burn-center criteria.
- `AUD-0604` [MODERATE] row row absent — current: "absent" | correct: "Airway/inhalation injury pearl (p.97)" | Add the pearl.
- `AUD-0605` [MODERATE] row row absent — current: "absent" | correct: "Hypotension solely from burns <20% TBSA unlikely" | Add the pearl.
- `AUD-0606` [MODERATE] row row absent — current: "absent" | correct: "Stabilize before burn-center transport; do not bypass trauma center if unstable" | Add the pearl.
- `AUD-0701` [MINOR] row row absent — current: "present" | correct: "absent from PEMS" | Non-clinical advisory; keep or source it. Recorded per batch method (site content PEMS does not cover).

## protocols/trauma/09_Trauma_PROC.md

- `AUD-0208` [CRITICAL] row row 8 — current: "wide open; maximum 2 L" | correct: "up to 1 L IV/IO in 250-500 mL boluses" | Replace with up to 1 L IV/IO in 250-500 mL boluses, repeated as needed.
- `AUD-0209` [CRITICAL] row row 8 — current: "absent" | correct: "Judicious fluids if bleeding suspected; target SBP 80-90" | Add the judicious-fluids and SBP 80-90 caution to row 8.
- `AUD-0214` [CRITICAL] row row absent — current: "absent; no do-not-remove-impaled-object instruction" | correct: "EMR: immobilize and secure; do not remove impaled object unless impeding CPR" | Add the EMR row with the do-not-remove-impaled-object contraindication.
- `AUD-0215` [CRITICAL] row row absent — current: "no closest-ED rule for uncontrolled airway or hemorrhage; row 12 routes to trauma center" | correct: "EMT: transport uncontrolled airway or uncontrolled hemorrhage to the closest ED" | Add the EMT closest-ED row and state precedence against trauma-center routing. Also source the Trauma Field Triage p.45 pearl (closest hospital ED). Human check on the PDF. | inferred: confirm in PDF befor
- `AUD-0610` [MODERATE] row row 8 — current: "one repeat only (about 40 mL/kg)" | correct: "repeat as needed up to 60 mL/kg total" | Change to repeat as needed to adequate perfusion, up to 60 mL/kg total.
- `AUD-0611` [MODERATE] row row absent — current: "absent" | correct: "EMR: keep warm if shock or potential for shock" | Add the EMR keep-warm row.
- `AUD-0612` [MODERATE] row row absent — current: "absent" | correct: "EMR: assess distal perfusion; MC if pulse absent; splint long bone fractures; reassess perfusion before and after splinting" | Add the EMR extremity row.
- `AUD-0613` [MODERATE] row row absent — current: "absent" | correct: "EMR: wrap in dry sterile dressing; sealed bag; ice-water container; label" | Add the EMR amputation-part care row.
- `AUD-0614` [MODERATE] row row absent — current: "absent" | correct: "A: consider pain management/analgesia (Pain Control)" | Add the A-level analgesia referral row. Human check on the PDF: the EMT and A tokens are split. | inferred: confirm in PDF before edit
- `AUD-0615` [MODERATE] row row absent — current: "absent" | correct: "Vasopressors worsen hemorrhage; generally not indicated in trauma" | Add the pearl.
- `AUD-0616` [MODERATE] row row absent — current: "absent" | correct: "Pregnancy pearl, including third-trimester backboard position" | Add the pregnancy pearl.
- `AUD-0617` [MODERATE] row row absent — current: "absent" | correct: "Cool/diaphoretic and tachycardic = shock until proven otherwise" | Add the pearl.
- `AUD-0702` [MINOR] row row 2 — current: "EMT+" | correct: "No PEMS Trauma row or level" | Source the row to PEMS or remove it. Scene-safety wording in PEMS belongs to Electrical p.96.
- `AUD-0703` [MINOR] row row 6 — current: "A+ (EMT blank)" | correct: "No PEMS level token for this row" | Source or remove the leveled row; the shock pearl itself is missing (see row absent, docs/protocols/trauma/09_Trauma_PROC.md).
- `AUD-0704` [MINOR] row row absent — current: "absent" | correct: "Isolated stable spinal injury: utmost care; rapid transport not indicated" | Add the pearl.
- `AUD-0705` [MINOR] row row absent — current: "one-site wording" | correct: "two large-bore IV sites when possible" | Add the two-large-bore wording.
- `AUD-0706` [MINOR] row row absent — current: "absent" | correct: "BLS care generally preferred for major trauma; consider benefit/risk of ALS interventions" | Add the pearl after checking the full text; the PEMS source chunk truncates this pearl block.
- `AUD-0707` [MINOR] row row absent — current: "range only" | correct: "adult and pediatric GCS scoring components (PEMS p.85)" | Link or add the GCS scoring tables.

