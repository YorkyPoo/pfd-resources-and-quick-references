# PEMS Protocol Audit Skill

## Purpose
Audit converted Poquoson Fire & Rescue EMS protocols against the original PEMS 2024 source text. Identify clinical discrepancies and report them for correction.

## Instructions

For each protocol in the master tracker:

1. **Read both files:**
   - PEMS source chunk from `pems_chunks/` directory
   - Converted protocol from `docs/protocols/` directory

2. **Compare for discrepancies in:**
   - Medication names, dosages, routes, concentrations
   - Indications and contraindications
   - Provider-level authorizations (EMT, AEMT, Intermediate, Paramedic)
   - Clinical decision points and algorithms
   - Age-specific considerations (pediatric vs adult)
   - Vital sign thresholds
   - PEMS-to-Poquoson terminology replacements that may have altered clinical meaning

3. **Report findings in this JSON format:**

```json
{
  "protocol": "Display Name",
  "status": "VERIFIED" | "FIXABLE" | "MANUAL",
  "discrepancies": [
    {
      "field": "e.g. Medication Dosage",
      "pems_original": "exact text from PEMS source",
      "converted_text": "exact text from converted file",
      "severity": "CRITICAL" | "MODERATE" | "MINOR",
      "recommendation": "what to change"
    }
  ],
  "missing_sections": ["section names found in PEMS but missing from converted"],
  "verified": true | false
}
```

4. **Update the master_tracker.md** with:
   - Status: VERIFIED, FIXABLE, or MANUAL
   - Number of discrepancies found
   - Any notes for human review

## Severity Definitions
- **CRITICAL**: Wrong medication, dosage, or contraindication that could cause patient harm
- **MODERATE**: Missing or incorrect provider level, outdated threshold, terminology drift
- **MINOR**: Formatting, header naming, or non-clinical wording differences

## Files
- PEMS source chunks: `pems_chunks/` directory
- PEMS full text: `pems_chunks/PEMS2024_full.txt` (for protocols not cleanly split)
- Converted protocols: `docs/protocols/*/` directories
- Master tracker: `master_tracker.md`
