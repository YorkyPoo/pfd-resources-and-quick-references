# Hermes Agent PEMS Audit Pipeline

## Overview
This pipeline enables Hermes Agent + qwen3.6:27b (Ollama) to verify all 55 converted Poquoson EMS protocols against the original PEMS 2024 source document.

## Requirements
- Ollama running with **qwen3.6:27b** model loaded
- Hermes Agent configured with:
  - File reading tools enabled
  - Memory enabled
  - This directory accessible

## Files in This Pipeline
| File | Purpose |
| :--- | :--- |
| `pems_chunks/` | 43 protocol text chunks extracted from PEMS2024.pdf |
| `pems_chunks/PEMS2024_full.txt` | Full 280-page extracted text (320K chars) |
| `master_tracker.md` | 55-protocol tracker with status and file paths |
| `hermes_skill_audit.md` | Hermes Agent skill with comparison instructions |

## Setup (One-Time)

### 1. Ensure Ollama is running
```bash
ollama serve
```

### 2. Load the audit skill into Hermes Agent
In Hermes Agent, run:
```
/skill install hermes_skill_audit.md
```

### 3. Verify file access
```bash
ollama run qwen3.6:27b "Read the file master_tracker.md and tell me how many protocols are listed."
```

## Running the Audit

### Option A: Interactive Hermes Agent (Recommended)
Paste this prompt into Hermes Agent:

```
You are a clinical EMS protocol auditor. Your task is to verify each protocol in master_tracker.md.

1. Read master_tracker.md to find the next PENDING protocol.
2. Read the PEMS source chunk file listed for that protocol.
3. Read the converted protocol file listed.
4. Compare them using the criteria in hermes_skill_audit.md.
5. Output findings in JSON format as specified in the skill.
6. Update master_tracker.md with the new status (VERIFIED/FIXABLE/MANUAL).
7. Repeat for the next PENDING protocol.

Start with protocol #1 and work sequentially.
```

### Option B: Python Batch Script
Run a Python script that loops through the tracker and calls Ollama via CLI for each protocol. (To be written; ask Agent Zero.)

## Protocol Categories
- Administrative Policies (14)
- General (6)
- Respiratory (9)
- Cardiac (10, 1 missing)
- Neurologic (3)
- Toxicology (3)
- Medical (4)
- Trauma (6)

## Missing Protocol
**Aortic Dissection** - PEMS chunk exists but no converted .md file yet. Hermes Agent can create it from the source.

## Post-Audit Steps
1. Review all MANUAL and FIXABLE entries
2. Apply corrections to the converted .md files
3. Run `link_drugs.py` to rebuild medication cross-references
4. Rebuild the MkDocs site: `mkdocs build`
5. Deploy: `mkdocs gh-deploy`
