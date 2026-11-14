# Batch audit protocol — PEMS2024 vs published site (parent task t_d3600e06)

READ-ONLY audit. Do NOT edit anything under `docs/`, the vault, or scripts. Do NOT run scripts (no shell is
available; you have read_file / search_files / write_file only). Never claim you ran something you did not run.

## 1. Inputs
- Repo root: `/root/projects/pfd-resources-and-quick-references`
- Method, PEMS level-code decode rule, severity policy: `audit/protocol-reconciliation/work/00_method_and_notes.md` — READ FIRST.
- PEMS source (flattened PDF text): `pems_chunks/PEMS2024_full.txt` (1408 lines, page markers `--- PAGE N ---`).
  Each PEMS page has a running header `PEMS Regional Patient Care Protocols, Policies and Procedures <TITLE>`.
  Find your protocol with `search_files` (target=content, pattern = the title, limit ~5, output_mode=files_only is NOT
  useful here — use the page-marker list: `search_files` pattern `--- PAGE \d+ ---` gives page→line map), then read the
  full page range with `read_file` offset/limit. Read every page of your protocol, including PEARLS and dose notes.
- Converted site: `docs/protocols/<folder>/<file>.md`. Matrix format: `| # | Action / Intervention | EMR | EMT | A | I | P |`
  (a `•` in a level column = that level and above; `[X]` = that level must contact MC; `MC` = all levels must contact MC).

## 2. Doctrine (settled — do NOT re-litigate; DO verify the site conforms)
- A level row means that level AND every level above may perform it.
- Bracketed `[A]` = that level must contact Medical Control; levels above are standing; levels below may not perform.
- Bare `MC` in every cell = ALL levels must contact MC.
- Administrative protocol rows are not level-gated.
- Divider rows (section labels) carry no level and are never discrepancies.
- 04_Supraventricular_Tachycardia rows 3/11 are deliberate dividers.
- 04_Cardiac_Arrest_Non_Traumatic is a deliberate merge of PEMS Asystole/PEA (p.57-58) + V-Fib/pVT (p.63-66); level evidence comes from both, row by row.
- 07_Allergic_Reaction rows 3,4,5,6,10,11,12,13 are published `I`, PEMS codes `A` (known over-restriction) — report it if still present (it is).

## 3. Severity (from the skill; policy detail in work/00 notes)
- CRITICAL: wrong drug/dose/route/concentration that could injure; a time-critical life-saving intervention omitted or
  its level narrowed (e.g. EMT blocked from IM epinephrine); site over-authorizes a high-alert drug/procedure PEMS does not grant; PEMS-required MC omitted for a high-alert drug; contraindication omitted.
- MODERATE: wrong/missing provider level on lower-harm rows; missing level cell on an existing non-high-alert row; threshold drift that does not change action; missing PEMS pearl with clinical content.
- MINOR: formatting, header naming, phone numbers, non-clinical wording.

## 4. Coverage requirement
Every protocol in your batch must be audited row by row (every PEMS step and every site row), not sampled.
If a PEMS section cannot be located or read, record the protocol as MANUAL with verified=false and say why. Do not invent findings.

## 5. Required outputs (write exactly these three files into `audit/protocol-reconciliation/work/`)
Use the batch id in the filenames, e.g. `batch-A1.json`, `batch-A1.md`, `batch-A1.fixlist.md`.

### A. `batch-<ID>.json`
JSON array, one object per protocol in the skill's shape plus fields needed for the FIXLIST:
```
{"protocol": "<display name>", "file": "<repo-relative path>", "pems_pages": "p.X-Y",
 "status": "VERIFIED" | "FIXABLE" | "MANUAL",
 "discrepancies": [
   {"id": "<ID>-<nn>", "row": <int or null>, "field": "<e.g. Provider Level / Dose / Missing Row>",
    "pems_original": "<EXACT PEMS text, verbatim>", "converted_text": "<EXACT site text, verbatim>",
    "current_value": "<site value>", "correct_value": "<PEMS-correct value>",
    "level_decode": "direct" | "inferred", "severity": "CRITICAL|MODERATE|MINOR",
    "recommendation": "<one line fix>"}
 ],
 "missing_sections": ["<PEMS steps/rows absent from the site>"],
 "verified": true | false, "notes": "<coverage notes, MANUAL reasons>"}
```
Use `"row": null` for rows that are missing from the site entirely (put the PEMS step in `pems_original`, and `converted_text` = "(absent)").
`level_decode` = "inferred" whenever the level came from the flattened-text decode rule rather than an unambiguous level token.

### B. `batch-<ID>.md`
One section per protocol: `## <file>`; a one-line coverage note; then a table:
`| ID | Row | Field | PEMS source (exact quote) | Converted (exact quote) | Severity | Required fix |`
One table row per discrepancy. Protocols with zero discrepancies: `No discrepancies — VERIFIED` plus the list of rows checked.

### C. `batch-<ID>.fixlist.md`
One line per discrepancy, self-contained (no "see above"):
`- [SEVERITY] <ID>-<nn> | <repo-relative file> | row <n or "absent"> | current: "<site value>" | correct: "<PEMS value>" | <one-line edit>`

### Count reconciliation (MUST hold before you complete)
Total discrepancies in A == table rows in B == lines in C. Count them explicitly and state the totals.

## 6. Completion
- Do not create kanban tasks. Do not block unless a required file is absent (then kanban_block kind=dependency or needs_input).
- Complete with `kanban_complete`: summary = per-protocol counts and totals by severity; metadata = {batch, protocols,
  counts_per_protocol, counts_by_severity, inferred_level_count, manual_protocols, count_reconciled: true/false};
  artifacts = the three absolute paths.
- Never put secrets or PII in the handoff.
