---
name: deep-work-planner
description: Turn your task list, calendar, and memory into a concrete deep-work plan. Use when planning focus blocks for today or the week, deciding which task deserves an uninterrupted window, reconciling TASKS.md against your calendar to find real focus capacity, or producing a plan that respects the working preferences in memory.
argument-hint: "[--week] [--window HH:MM-HH:MM] [--duration MIN]"
---

# Deep Work Planner

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Produce a grounded deep-work plan: which tasks deserve focus, which calendar blocks are actually available, and the concrete first action for each block. The plan is proposed, not auto-applied — nothing is written to `TASKS.md` or the calendar without confirmation.

## Usage

```bash
/productivity:deep-work-planner
/productivity:deep-work-planner --week
/productivity:deep-work-planner --window 14:00-17:00
/productivity:deep-work-planner --duration 90
```

- Default: plan deep work for the rest of today.
- `--week`: plan across the current working week.
- `--window HH:MM-HH:MM`: restrict to a specific window today.
- `--duration MIN`: minimum uninterrupted block size (default `60`).

## Instructions

### 1. Load Current State

Read:

- `TASKS.md` — current Active and Waiting On sections.
- `CLAUDE.md` — for the Preferences section and active projects/people.
- `memory/projects/` — for deeper context when a task references a project.

If `TASKS.md` or `CLAUDE.md` don't exist, stop and suggest `/productivity:start` first.

### 2. Classify Tasks

For every Active task in `TASKS.md`, classify as **deep** or **shallow**:

| Signal | Deep | Shallow |
|--------|------|---------|
| Requires multi-step thinking or writing | ✓ | |
| Owned by the user (not blocked on someone else) | ✓ | |
| Benefits from uninterrupted flow | ✓ | |
| Quick reply, review, approval, or status ping | | ✓ |
| Already blocked / waiting on another person | | ✓ (skip) |

Set aside shallow items — they belong in batched "admin" time, not deep-work blocks.

### 3. Honour Preferences from Memory

Before scheduling, pull constraints from `CLAUDE.md` Preferences:

- Preferred block length (e.g. "25-min meetings with buffers" → default deep-work blocks to 50 or 90 min).
- No-meeting windows (e.g. "No meetings Friday afternoons" → prefer deep work there).
- Energy patterns if noted (e.g. "mornings for writing").

If preferences contradict a flag the user passed (e.g. `--duration 30` vs. a stated "90-min blocks" preference), surface the conflict and ask.

### 4. Find Real Focus Capacity

Using `~~calendar` (if connected), list events in the target window (today, this week, or the user-specified window).

Compute uninterrupted gaps ≥ the minimum duration. A gap only counts if:

- No events on the calendar.
- Not inside a stated no-work window from memory (e.g. lunch, school pickup).
- Padded by the user's preferred buffer (default 10 minutes on each side).

If `~~calendar` is not connected, ask the user for their available windows instead. Do not invent availability.

### 5. Match Deep Tasks to Blocks

Assign deep tasks to the available blocks. For each pairing, derive a concrete first action — not the task title, the *first 15 minutes*:

```
Block: Tue 09:30–11:00 (90 min)
Task:  **Draft Q2 roadmap** - for Greg, due Friday
First action: Open last quarter's roadmap doc and list the 3 themes
              that carried over. Don't write new content yet.
```

Prefer larger tasks in longer blocks. When two tasks compete, use (in order): deadline proximity, blocker status for others, project priority in `CLAUDE.md`.

### 6. Surface Conflicts and Gaps

Be honest about what the plan does and doesn't cover:

```
Heads up:
- **Budget review for Sarah** (due Friday) didn't fit — only a 45-min gap left today.
  Options: bump something, move to tomorrow AM, or accept it slips.
- Two back-to-back meetings 13:00–15:30 leave no afternoon deep-work window.
  Want to suggest declining the optional 14:00 sync?
```

### 7. Propose the Plan

Present the plan in a single block the user can scan at a glance:

```
## Deep Work — Tuesday

09:30–11:00  Draft Q2 roadmap (for Greg, due Fri)
             → Open last quarter's roadmap, list the 3 carry-over themes
11:15–12:00  Review API spec from Platform
             → Read sections 2–4, capture questions inline

Shallow batch (30 min, any time):
- PSR reply to Todd
- Approve Maya's design handoff
- Close out completed tasks in TASKS.md

Not scheduled today:
- Budget review for Sarah (no 60-min block left)
```

### 8. Confirm Before Writing

Ask the user what to persist. Offer, in order of reversibility:

1. **Append to `TASKS.md`** — a `## Today's Focus` section under Active, listing the planned blocks. Remove on completion or next run.
2. **Suggest calendar holds** — print ready-to-paste titles and times the user can drop into `~~calendar` manually. Do not create events directly unless the connected calendar MCP explicitly supports writes and the user says to.
3. **Do nothing** — just keep the plan in chat.

Default to option 1 if the user doesn't specify. Never write to `TASKS.md` silently.

### 9. Report

```
Deep-work plan ready:
- 2 focus blocks scheduled (2h 15m total)
- 3 shallow items batched for later
- 1 task flagged as not fitting today (budget review for Sarah)
- Appended to TASKS.md under ## Today's Focus
```

## Notes

- Never auto-create calendar events or mutate `TASKS.md` without explicit confirmation.
- If `~~calendar` isn't connected, ask the user for their windows — don't guess.
- Preferences in `CLAUDE.md` override defaults. Flags override preferences, but surface the conflict first.
- A task without a concrete first action isn't ready for deep work — ask a clarifying question or batch it for triage.
- Safe to run multiple times a day. Re-running replaces the previous `## Today's Focus` section, it doesn't stack.
- Shallow items are listed but never assigned to deep-work blocks — that defeats the point.
