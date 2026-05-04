---
name: proactive-reminders
description: Set time-based reminders that deliver via chat when they come due. Supports natural language times ("next Tuesday at 9am"), recurrence (daily/weekly/weekdays/monthly), and cross-team reminders ("remind Sarah to send the proposal"). Use when someone says "remind me to...", "follow up on...", "ping me about...", or "set a reminder for [person]".
---

# Proactive Reminders

Go beyond static task lists — set reminders that **deliver themselves** at the right time via ~~chat. Supports natural language scheduling, recurrence, teammate reminders, and optional links to ~~CRM deals or ~~project tracker items.

## Connectors

| Connector | What It Adds |
|-----------|-------------|
| **~~chat** (required) | Delivers reminders as DMs when they come due |
| **~~CRM** | Links reminders to deals for pipeline follow-up context |
| **~~project tracker** | Links reminders to tasks/issues |
| **~~calendar** | Cross-references with scheduled meetings |

> **Minimum requirement:** A ~~chat connector is needed to deliver reminders. Without it, this skill can still help _draft_ reminders but cannot deliver them proactively.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                   PROACTIVE REMINDERS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. PARSE          Natural language → structured reminder    │
│     "remind me to call Acme next Tuesday at 2pm"            │
│     → who: me, what: call Acme, when: Tue 2:00 PM           │
│                                                              │
│  2. VALIDATE        Ensure the date is in the future         │
│     ⚠️  If year looks wrong, auto-correct to current year   │
│     ⚠️  If time is ambiguous, default to 9:00 AM            │
│                                                              │
│  3. STORE           Save to persistent storage               │
│     → reminder table / file with: who, what, when,           │
│       created_by, recurrence, deal/task link                 │
│                                                              │
│  4. DELIVER         When time arrives, send via ~~chat       │
│     → DM to the assigned person                              │
│     → Include context (deal name, task link)                 │
│     → Handle recurrence (create next occurrence)             │
│                                                              │
│  5. MANAGE          List, dismiss, reschedule                │
│     → "show my reminders" → list upcoming                    │
│     → "cancel the Acme reminder" → dismiss                   │
│     → "push that to Friday" → reschedule                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Usage

### Setting Reminders

When the user says "remind me to...", "follow up on...", "ping me about...", or "set a reminder for...":

**1. Parse the request into structured fields:**

| Field | Source | Default |
|-------|--------|---------|
| `message` | What to be reminded about | Required |
| `remind_at` | When to deliver (ISO 8601 timestamp) | Required — parse from natural language |
| `assigned_to` | Who gets the reminder | Current user |
| `recurrence` | Repeat pattern | None |
| `deal_id` / `task_id` | Linked item | None |

**2. Parse natural language times:**

| User says | Interpret as |
|-----------|-------------|
| "tomorrow at 2pm" | Next day, 2:00 PM in user's timezone |
| "next Tuesday" | The upcoming Tuesday, 9:00 AM |
| "Friday at 8am" | The upcoming Friday, 8:00 AM |
| "in 2 hours" | Current time + 2 hours |
| "end of day" | Today 5:00 PM |
| "next week" | Next Monday, 9:00 AM |
| "every weekday at 9am" | Recurrence: weekdays, starting tomorrow 9:00 AM |

**3. Validate the timestamp:**

⚠️ **Critical: Date validation.** AI models may generate timestamps with incorrect years (e.g., 2025 instead of 2026). Always validate:

```
IF remind_at is in the past:
  TRY replacing year with current year
    IF now in the future → use corrected date
  TRY replacing year with current year + 1
    IF now in the future → use corrected date (Dec→Jan edge case)
  ELSE → ask user to clarify
```

This server-side validation prevents reminders from firing immediately due to year errors.

**4. Confirm with the user:**

> ✅ Reminder set for **Tuesday, Mar 25 at 2:00 PM**: "Call Acme about the proposal"

Always confirm with a human-readable date (not ISO format) so the user can verify at a glance.

### Cross-Team Reminders

When someone says "remind Sarah to..." or "ping Nick about...":

- Set `assigned_to` to the named person
- The reminder delivers to **both** the sender and recipient (group DM if possible via ~~chat)
- Include attribution: "💬 Reminder from **Jackson**: Call Acme about the proposal"

This turns reminders into a lightweight delegation tool.

### Recurrence

| Pattern | Behavior |
|---------|----------|
| `daily` | Repeats every day at the same time |
| `weekly` | Repeats every 7 days |
| `weekdays` | Mon-Fri only; skips Sat/Sun (Friday → Monday) |
| `monthly` | Same day each month |

When a recurring reminder is delivered:
1. Mark the current occurrence as triggered
2. Create the next occurrence with the appropriate offset
3. For `weekdays`: if the next day is Saturday, skip to Monday

### Listing Reminders

When the user asks "what are my reminders?" or "show upcoming reminders":

- Show upcoming (non-triggered, non-dismissed) reminders sorted by time
- Group by: Today, Tomorrow, This Week, Later
- Include: message, time (relative + absolute), recurrence badge, linked deal/task
- Support filtering: "show team reminders" for all, "show Nick's reminders" for specific person

### Dismissing / Rescheduling

When the user says "cancel the Acme reminder" or "push that to Friday":

- **Dismiss:** Mark as dismissed, confirm to user
- **Reschedule:** Update `remind_at`, confirm new time
- **Ownership check:** Only the assigned person or creator should be able to dismiss

---

## Delivery Mechanism

Reminders need a **background process** to check for due reminders and deliver them. Implementation options:

### Option A: Cron / Scheduled Function (Recommended)
Run a check every 5-15 minutes:
```
1. Query: SELECT * FROM reminders WHERE remind_at <= NOW() AND triggered = false AND dismissed = false
2. For each due reminder:
   a. Send DM via ~~chat to assigned_to
   b. Mark as triggered
   c. If recurring, create next occurrence
3. Log delivery for analytics
```

### Option B: Calendar Integration
Create a ~~calendar event for each reminder. The calendar handles delivery natively. Trade-off: no recurrence control, clutters calendar.

### Option C: Chat Scheduled Messages
Use ~~chat's scheduled message API (e.g., Slack's `chat.scheduleMessage`). Trade-off: limited to single delivery, no recurrence, harder to manage.

**Option A is recommended** because it supports recurrence, cross-team delivery, and integrates naturally with CRM/project-tracker links.

---

## Storage Schema

Reminders need persistent storage. Recommended schema:

```sql
CREATE TABLE reminders (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_by    text NOT NULL,           -- who set the reminder
  assigned_to   text NOT NULL,           -- who gets reminded
  remind_at     timestamptz NOT NULL,    -- when to deliver
  message       text NOT NULL,           -- what to remind about
  deal_id       uuid,                    -- optional ~~CRM link
  task_id       text,                    -- optional ~~project tracker link
  recurrence    text CHECK (recurrence IN ('daily', 'weekly', 'weekdays', 'monthly')),
  dismissed     boolean NOT NULL DEFAULT false,
  triggered     boolean NOT NULL DEFAULT false,
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_reminders_pending
  ON reminders (remind_at)
  WHERE triggered = false AND dismissed = false;
```

Alternative: For teams without a database, use a `REMINDERS.md` file (similar to how `task-management` uses `TASKS.md`), but note this cannot support background delivery.

---

## Integration with task-management

This skill complements `task-management`:

| | task-management | proactive-reminders |
|---|---|---|
| **Purpose** | Track what needs doing | Ensure it gets done on time |
| **Storage** | TASKS.md file | Database or file |
| **Delivery** | User checks manually | Push notification at set time |
| **Recurrence** | No | Yes |
| **Cross-team** | No (single user) | Yes (remind teammates) |
| **Time-based** | No | Yes |

They work best together: use `task-management` for your backlog, use `proactive-reminders` for time-sensitive follow-ups.

---

## Example Implementation

See [Dyrt's standup bot](https://github.com/dyrt-labs/standup-bot) for a production implementation that includes:
- Natural language parsing via Claude → ISO timestamp
- Server-side year auto-correction (handles AI model date errors)
- 15-minute cron delivery via Cloudflare Workers
- Slack DM delivery with group DM for cross-team reminders
- Supabase PostgreSQL storage with the schema above
- Recurrence handling (daily/weekly/weekdays/monthly)
- CRM deal linking for sales follow-up context
- Dashboard UI for viewing and managing reminders

Built by an 11-person waste management team running their entire CRM and operations stack on Claude Cowork + MCP tools.
