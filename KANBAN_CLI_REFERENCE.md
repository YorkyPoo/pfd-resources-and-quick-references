# Kanban Audit Board — Quick Reference for Local AI

This file teaches you (the local AI) how to interact with the Hermes Kanban board for the PEMS Protocol Audit.

## How to Access the Kanban

Use the **terminal tool** to run `hermes kanban` commands:

```
# Switch to the audit board
terminal(command="hermes kanban boards switch pems-audit", timeout=10)

# List all tasks by priority (lowest number = highest priority)
terminal(command="hermes kanban list --sort priority", timeout=10)

# Show a specific task's details
terminal(command="hermes kanban show TASK_ID", timeout=10)

# Mark a task as complete after auditing it
terminal(command="hermes kanban complete TASK_ID", timeout=10)

# Block a task with a reason
terminal(command="hermes kanban block TASK_ID reason here", timeout=10)

# View board stats
terminal(command="hermes kanban stats", timeout=10)
```

## How to Load the Audit Skill

Do NOT use `/skill pems-protocol-audit` - that searches the hub registry. Instead:

```
skill_view(name="pems-protocol-audit")
```

## Audit Workflow (One Protocol)

1. Run `terminal(command="hermes kanban list --status ready --sort priority", timeout=10)` - find first ready task, note its ID
2. Read the task body with `terminal(command="hermes kanban show TASK_ID", timeout=10)` - has file paths for PEMS chunk and converted protocol
3. Read both files
4. Compare for discrepancies using the pems-protocol-audit skill criteria
5. Output findings in JSON format
6. Update master_tracker.md with the result
7. Run `terminal(command="hermes kanban complete TASK_ID", timeout=10)` - mark done
8. Move to next ready task

## Priority System

- Priority 1 = Administrative (do first)
- Priority 2 = General
- Priority 3 = Respiratory
- Priority 4 = Cardiac
- Priority 5 = Neurologic
- Priority 6 = Toxicology
- Priority 7 = Medical
- Priority 8 = Trauma (do last)
- Priority 100 = Post-audit pipeline (blocked until audits done)

## File Paths

All paths are relative to: D:\mindpalace\30 - projects\Active\Fire and EMS Resources SSG\
