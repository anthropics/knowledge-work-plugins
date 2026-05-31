---
name: update
description: Sync TF3 tasks and refresh memory from current activity. Use when pulling new ClickUp assignments into TASKS.md, triaging stale or overdue tasks, reading the Ops Note and Handoff Log, and summarising what needs Paskal today.
argument-hint: "[--comprehensive]"
---

# Update Command

> See tf3-context.md for ClickUp list IDs and Notion page IDs, and rex-protocols.md for the sweep protocol and signal formats.

Keep your task list and memory current. Two modes:

- **Default:** Sync ClickUp tasks, triage stale items, check memory for gaps
- **`--comprehensive`:** Default mode plus a deep read of the Ops Note and Handoff Log — flag missed todos and suggest new memories

## Usage

```bash
/productivity:update
/productivity:update --comprehensive
```

## Default Mode

### 1. Load Current State

Read `TASKS.md` and `memory/` directory. If they don't exist, suggest `/productivity:start` first.

### 2. Sync Tasks from ClickUp

Fetch urgent + high priority ClickUp tasks from spaces 90166324362 (TF3 HQ) and 90166324354 (Digital Growth). Compare against TASKS.md:

| ClickUp task | TASKS.md match? | Action |
|--------------|-----------------|--------|
| Found, not in TASKS.md | No match | Offer to add |
| Found, already in TASKS.md | Match by title (fuzzy) | Skip |
| In TASKS.md, not in ClickUp | No match | Flag as potentially stale |
| Completed in ClickUp | In Active section | Offer to mark done |

Present diff and let user decide what to add/complete.

### 3. Triage Stale Items

Review Active tasks in TASKS.md and flag:
- Tasks with due dates in the past
- Tasks in Active for 30+ days
- Tasks with no context (no person, no project)

Present each for triage: Mark done? Reschedule? Move to Someday?

### 4. Decode Tasks for Memory Gaps

For each task, attempt to decode all entities (people, projects, acronyms, clients, links) against tf3-context.md and `memory/`. Track what's fully decoded vs. what has gaps.

### 5. Fill Gaps

Present unknown terms grouped, then add answers to the appropriate memory files (people/, projects/, glossary.md).

### 6. Capture Enrichment

Tasks often contain richer context than memory. Extract and update links, status changes, relationships, and deadlines into the relevant project/people files.

### 7. Report

```
Update complete:
- Tasks: +3 from ClickUp, 1 completed, 2 triaged
- Memory: 2 gaps filled, 1 project enriched
- All tasks decoded ✓
```

## Comprehensive Mode (`--comprehensive`)

Everything in Default Mode, plus a deep read of TF3 system state:

### Extra Step: Read System State

1. Fetch urgent + high priority ClickUp tasks from spaces 90166324362 and 90166324354
2. Read Ops Note (Notion page 347871f7633d8113a73bf24a4e7ee9e9) for current system state
3. Read Handoff Log (Notion page 364871f7633d81a5be74f181d076278c) for pending items
4. Summarise: open tasks, pending handoffs, what needs Paskal today

### Extra Step: Flag Missed Todos

Compare the Ops Note and Handoff Log against TASKS.md. Surface action items that aren't tracked and let the user pick which to add.

### Extra Step: Suggest New Memories

Surface new people, clients, or projects not yet in memory, grouped by confidence. High-confidence items offered to add directly; low-confidence items asked about.

## Notes

- Never auto-add tasks or memories without user confirmation
- ClickUp task links are preserved when available
- Fuzzy matching on task titles handles minor wording differences
- Tasks live in ClickUp; never create Notion pages for tasks (see tf3-context.md)
- `--comprehensive` always runs interactively
