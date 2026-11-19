# Batch C1 fixlist (65 discrepancies: CRITICAL 27, MODERATE 38, MINOR 0)

## 03_Respiratory_Distress_PROC.md (21)
- [MODERATE] C1-01 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 1 | current: "EMT+" | correct: "EMR+" | set EMR ● on row 1
- [MODERATE] C1-02 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 2 | current: "EMT+" | correct: "EMR+" | set EMR ● on row 2
- [MODERATE] C1-03 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 4 | current: "EMT+" | correct: "EMR+" | set EMR ● on row 4
- [MODERATE] C1-04 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 4 | current: "COPD target 88-92%" | correct: "SpO2 >94% (no COPD exception in PEMS)" | remove 88-92% or get owner ruling
- [CRITICAL] C1-05 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 6 | current: "EMT blank; A and I require MC; P blank" | correct: "EMT, A, I, P standing" | set EMT/A/I/P ● and remove MC at A/I
- [MODERATE] C1-06 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 6 | current: "MC required at A and I (pearl 3)" | correct: "no MC for CPAP at A/I" | remove MC; align pearl 3
- [CRITICAL] C1-07 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 7 | current: "all level cells blank" | correct: "EMT, A, I, P" | set EMT/A/I/P ● on SGA row
- [CRITICAL] C1-08 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 8 | current: "P only" | correct: "I and P (ETI >=12 at I; <12 at P)" | set I ● on row 8
- [MODERATE] C1-09 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 9 | current: "I+" | correct: "A+" | set A ● on IV/IO row
- [CRITICAL] C1-10 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 11 | current: "A MC, I MC, P blank" | correct: "A, I, P standing" | remove MC at A/I; set P ●
- [MODERATE] C1-11 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 11 | current: "Administer simultaneously with epinephrine" | correct: "only for moderate to severe symptoms" | restore severity condition
- [MODERATE] C1-12 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 12 | current: "all level cells blank" | correct: "A, I, P" | set A/I/P ● on bronchiolitis row; add suction step
- [CRITICAL] C1-13 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 13 | current: "all level cells blank" | correct: "A, I, P" | set A/I/P ● on nitroglycerin row
- [MODERATE] C1-14 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 13 | current: "MAP >65" | correct: "MAP >=65" | change to >=65
- [CRITICAL] C1-15 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | absent (nitro) | current: "no PDE-inhibitor contraindication anywhere in respiratory folder; no IV prerequisite" | correct: "PDE inhibitors contraindicated; IV access; SBP>=100/MAP>=65" | add contraindication and prerequisites before row 13
- [MODERATE] C1-16 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | absent | current: "absent" | correct: "Furosemide 40 mg IV/IO slow push, I and above" | add furosemide row
- [CRITICAL] C1-17 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 14 | current: "all level cells blank" | correct: "I and P" | set I/P ● on Mg referral row (agree with Asthma file)
- [CRITICAL] C1-18 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | row 16 | current: "P only" | correct: "EMT, A, I, P" | set EMT/A/I ● on BVM row
- [MODERATE] C1-19 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | absent (pearl) | current: "absent" | correct: "PEMS epinephrine/CHF caution, MC for doubt" | add pearl
- [MODERATE] C1-20 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | absent (pearl) | current: "absent" | correct: "PEMS wheeze-paradox and judge-response pearl" | add pearl
- [MODERATE] C1-21 | docs/protocols/respiratory/03_Respiratory_Distress_PROC.md | absent (pearl) | current: "absent" | correct: "PEMS RSI scope note" | add pearl

## 03_Asthma_COPD_Reactive_Airway_PROC.md (12)
- [MODERATE] C1-22 | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | row 1 | current: "EMT+" | correct: "EMR+" | set EMR ● on row 1
- [MODERATE] C1-23 | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | row 2 | current: "EMT+; >=94%" | correct: "EMR+; >94%" | set EMR ●; change to >94%
- [MODERATE] C1-24 | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | row 5 | current: "I+" | correct: "A+" | set A ● on methylprednisolone row
- [CRITICAL] C1-25 | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | row 6 | current: "P only" | correct: "I and P" | set I ● on Mg row
- [MODERATE] C1-26 | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | row 6 | current: "unresponsive to initial therapy" | correct: "for severe symptoms" | replace trigger
- [CRITICAL] C1-27 | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | row 8 | current: "I+ only" | correct: "EMT+" | set EMT ● and A ● on CPAP row
- [CRITICAL] C1-28 | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | row 8 | current: "3 contraindications" | correct: "full PEMS CPAP contraindication list (8)" | add the 8 contraindications
- [MODERATE] C1-29 | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | row 8 | current: "Initiate 5-10 cm H2O" | correct: "initial PEEP 5; up to 10 at I/P only" | restate settings
- [CRITICAL] C1-30 | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | row 9 | current: "EMT, A, I, P" | correct: "A and above" | blank EMT on epinephrine stridor row
- [MODERATE] C1-31 | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | row 10 | current: "I+" | correct: "A+" | set A ● on stridor methylprednisolone row
- [MODERATE] C1-32 | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | absent (pearl) | current: "absent" | correct: "PEMS epinephrine/CHF caution" | add pearl
- [MODERATE] C1-33 | docs/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md | absent (pearl) | current: "absent" | correct: "PEMS wheeze-paradox pearl" | add pearl

## 03_Pneumothorax_PROC.md (9) — MANUAL, verified=false
- [MODERATE] C1-34 | docs/protocols/respiratory/03_Pneumothorax_PROC.md | row 3 | current: "EMT+" | correct: "EMR+" | set EMR ● on O2 row
- [MODERATE] C1-35 | docs/protocols/respiratory/03_Pneumothorax_PROC.md | row 1 | current: "EMT+" | correct: "EMR+" | set EMR ● on universal row
- [MODERATE] C1-36 | docs/protocols/respiratory/03_Pneumothorax_PROC.md | row 2 | current: "EMT+" | correct: "EMR+" | set EMR ● on primary assessment row
- [MODERATE] C1-37 | docs/protocols/respiratory/03_Pneumothorax_PROC.md | row 4 | current: "A+ for cardiac monitoring" | correct: "I+ for cardiac monitoring" | split row; keep IV/IO at A (owner confirm)
- [MODERATE] C1-38 | docs/protocols/respiratory/03_Pneumothorax_PROC.md | row 5 | current: "A+" | correct: "EMR+ for suctioning" | set EMR/EMT ● for suction step
- [MODERATE] C1-40 | docs/protocols/respiratory/03_Pneumothorax_PROC.md | row 9 | current: "suspicion of thoracoabdominal trauma" | correct: "evidence of significant blunt or penetrating thoracoabdominal trauma" | restore PEMS trigger
- [MODERATE] C1-41 | docs/protocols/respiratory/03_Pneumothorax_PROC.md | row 10 | current: "EMT+" | correct: "I+ (owner to confirm vitals at EMR)" | owner question
- [CRITICAL] C1-42 | docs/protocols/respiratory/03_Pneumothorax_PROC.md | row 13 | current: "P only" | correct: "I (>=12) and P (<12)" | set I ● on ETI row
- [MODERATE] C1-43 | docs/protocols/respiratory/03_Pneumothorax_PROC.md | absent (pearls) | current: "absent" | correct: "PEMS failure rate, second attempt, assume PTX regardless of return" | add pearls

## 03_Respiratory_Arrest_PROC.md (15) — MANUAL, verified=false
- [MODERATE] C1-44 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 1 | current: "EMT+" | correct: "EMR+" | set EMR ● on row 1
- [MODERATE] C1-45 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 5 | current: "EMT+" | correct: "EMR+" | set EMR ● on suction row
- [MODERATE] C1-46 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 5 | current: "pre-oxygenate before manipulation" | correct: "100% O2 via NRB or BVM for 3 minutes" | add the PEMS pre-oxygenation detail
- [CRITICAL] C1-47 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 6 | current: "A, I, P (EMT blank)" | correct: "EMT+" | set EMT ● on BVM row
- [MODERATE] C1-48 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 7 | current: "A+" | correct: "EMT+" | set EMT ● on EtCO2-guided row
- [CRITICAL] C1-49 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 8 | current: "P only" | correct: "I and P (>=12)" | set I ● on adult ETI row
- [CRITICAL] C1-50 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 9 | current: "all level cells blank" | correct: "P" | set P ● on pediatric ETI row
- [CRITICAL] C1-51 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 10 | current: "P only" | correct: "I and P" | set I ● on FBAO laryngoscopy row (inferred decode)
- [CRITICAL] C1-52 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 11 | current: "all level cells blank" | correct: "P" | set P ● on surgical airway row (inferred; PDF check p.248)
- [CRITICAL] C1-53 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 12 | current: "P only" | correct: "I and P" | set I ● on verification row (inferred; PDF check p.248)
- [CRITICAL] C1-54 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 13 | current: "P only" | correct: "EMT, A, I, P" | set EMT/A/I ● on ETT monitoring row
- [CRITICAL] C1-55 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 14 | current: "all level cells blank" | correct: "I and P" | set I/P ● on fentanyl row
- [CRITICAL] C1-56 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | row 15 | current: "all level cells blank" | correct: "I and P" | set I/P ● on midazolam row
- [CRITICAL] C1-57 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | absent (sedation) | current: "absent" | correct: "MC for all levels when agitation not manageable" | add bare-MC row (inferred decode)
- [MODERATE] C1-58 | docs/protocols/respiratory/03_Respiratory_Arrest_PROC.md | absent | current: "absent" | correct: "ETI equipment preparation at I (inferred)" | add prep row after PDF check

## 03_Upper_Airway_Obstruction_PROC.md (8) — MANUAL, verified=false
- [MODERATE] C1-59 | docs/protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md | row 1 | current: "EMT+" | correct: "EMR+" | set EMR ● on universal row
- [MODERATE] C1-60 | docs/protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md | row 9 | current: "EMT+" | correct: "EMR+" | set EMR ● on suction row
- [CRITICAL] C1-61 | docs/protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md | row 10 | current: "A, I, P (EMT blank)" | correct: "EMT+" | set EMT ● on BVM row (title already says EMT and above)
- [CRITICAL] C1-62 | docs/protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md | row 11 | current: "P only" | correct: "I and P" | set I ● on laryngoscopy row (title already says I/P)
- [CRITICAL] C1-63 | docs/protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md | row 12 | current: "[P] MC bracket; I blank" | correct: "I and P standing" | set I ● and remove [P] MC bracket
- [MODERATE] C1-64 | docs/protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md | row 13 | current: "[I] MC; fentanyl 25 mcg" | correct: "I and P standing; fentanyl 25-50 mcg" | remove [I] bracket; restate dose
- [MODERATE] C1-65 | docs/protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md | row 14 | current: "[I] MC bracket" | correct: "I standing (MC bracket un-sourced)" | remove bracket unless medical director directs
- [CRITICAL] C1-66 | docs/protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md | absent | current: "absent" | correct: "nebulized epinephrine 3 mg and methylprednisolone, A and above" | add stridor rows
