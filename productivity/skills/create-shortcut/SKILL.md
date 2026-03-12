---
name: create-shortcut
description: Save reusable workflow shortcuts to SHORTCUTS.md for manual invocation
---

# Create Shortcut

Create a named shortcut that captures a repeated workflow so the user can invoke it with a short phrase.

> **Note on scheduled/recurring execution**: Cowork does not have a built-in scheduler. Shortcuts created here are saved as named workflows you invoke manually (e.g., "run my morning briefing"). For automatic scheduling on a recurring basis, see the [Scheduling section](#scheduling-recurring-execution) below.

## What Is a Shortcut

A shortcut is a saved entry in `SHORTCUTS.md` — a plain-language description of a workflow that Claude will execute when the user invokes it by name. Examples:

- "morning briefing" → pull calendar, summarize email, list today's tasks
- "end-of-day wrap-up" → log completed tasks, flag blockers, draft tomorrow's plan
- "weekly report" → aggregate task completions, draft summary for manager

## File Location

Save shortcuts in `SHORTCUTS.md` in the current working directory.

- If it exists, append to it
- If it doesn't exist, create it with the template below

## SHORTCUTS.md Template

```markdown
# Shortcuts

Invoke any shortcut by name (e.g., "run morning briefing").

## Shortcuts

| Name | What it does | Invoke with |
|------|-------------|-------------|
```

## Shortcut Format

Each shortcut entry:

```markdown
### [Shortcut Name]

**Invoke with**: "[short phrase]" (e.g., "morning briefing", "run daily wrap-up")

**What it does**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Output**: [What the user will see when they run it]
```

## How to Create a Shortcut

1. **Clarify the workflow** — If the user's description is vague, ask what steps they want included. Keep it focused: a shortcut should do one coherent thing.

2. **Name it** — Suggest a short, memorable name. Confirm with the user before saving.

3. **Write the steps** — Describe each action Claude should take when the shortcut is invoked. Be specific about what tools or data sources to use (calendar, email, TASKS.md, etc.).

4. **Save it** — Append to `SHORTCUTS.md`. Create the file if it doesn't exist.

5. **Confirm** — Tell the user the shortcut is saved and how to invoke it. Example:
   > "Saved. Say 'morning briefing' and I'll run through your calendar, email, and tasks."

## Running a Shortcut

When the user invokes a shortcut by name, read `SHORTCUTS.md`, find the matching shortcut, and execute its steps in order.

## Scheduling Recurring Execution

Cowork does not provide a `set_scheduled_task` platform tool or any built-in scheduler — shortcuts must be invoked manually each time. To run a shortcut automatically on a schedule, use your operating system's native scheduling tools:

**macOS / Linux — cron**:
```
# Open crontab editor
crontab -e

# Example: run "morning briefing" every weekday at 8am
# (requires a script that opens a Cowork session and sends the message)
0 8 * * 1-5 /path/to/your-briefing-script.sh
```

**Windows — Task Scheduler**:
1. Open Task Scheduler → Create Basic Task
2. Set the trigger (daily, weekly, etc.)
3. Set the action to run your briefing script

For both platforms, the script would need to invoke Cowork programmatically, which depends on your setup. Let the user know this is a manual step outside Cowork and offer to help them write the script if they have a supported automation method.

**Practical recommendation**: Most users find it easiest to simply ask Cowork to "run [shortcut name]" at the start of their session, rather than setting up OS-level scheduling.
