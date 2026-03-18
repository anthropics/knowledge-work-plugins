---
name: daily-triage-brief
description: >
  Generates a prioritized morning triage brief for the Quandri support team — surfaces new Linear
  tickets since yesterday, overnight bot run failures, HubSpot tickets needing a response, and any
  escalations or urgent flags from Slack. Produces a clear "work through this today" priority list
  so Alma and Syed can hit the ground running. Use when: morning triage, daily triage, triage brief,
  start of day, what do I work on today, what came in overnight, what's in the queue, morning brief,
  daily queue, what needs attention today, triage queue.
---

# Daily Triage Brief

## Purpose
Give the support team a prioritized starting point every morning. This is an operational brief — not a summary of what happened, but a concrete answer to "what do I work on right now?" Covers new tickets, bot run failures, customer escalations, and anything that came in since the previous working day.

## When to Use
- "Morning triage" / "Daily triage brief"
- "What do I work on today?"
- "What came in overnight?"
- "What's in the queue?"
- "Start of day brief"
- Any time a support team member is beginning their workday and needs to orient quickly

---

## Core Workflow

### Step 1 — Establish the Lookback Window

- Default to **since end of previous business day** (i.e., after 5pm the prior weekday)
- If today is Monday, look back to **Friday EOD** — capture the full weekend
- Use today's date to anchor all time calculations

---

### Step 2 — Scan for Overnight Bot Run Failures

This is the first thing to check — failed bot runs are time-sensitive because customers may be waiting on results and the support team is often the first to catch them.

**Search two sources:**

1. **Linear ONC team** — Use `Linear:list_issues` filtered to the ONC team, created after the lookback window. ONC tickets are often auto-created when a bot run fails. Look for tickets with titles containing terms like "failed", "stuck", "0%", "processing rate", or "exception".

2. **#support-team Slack** — Use `Slack:slack_read_channel` on **#support-team** to catch any run failures or monitoring flags posted since EOD yesterday.

For each failed run identified, collect:
- Customer name
- Product line (RR = Renewal Rounds, RQ = Renewal Queue, EE = another product line)
- What failed and when
- Whether a Linear ticket already exists (link it) or needs to be created
- Suggested first action (e.g., "check if re-run is possible", "investigate config", "escalate to ONC")

---

### Step 3 — Pull New Linear Tickets in the Triage Queue

Use `Linear:list_issues` to find tickets created since the lookback window that are unassigned or in a **Triage** / **Todo** state. Focus on the ONC team and any other teams the support team covers.

For each new ticket:
- Ticket ID, title, team, priority
- 1-sentence description of the issue (from the ticket description)
- Suggested owner (Alma or Syed based on product/customer familiarity if determinable, otherwise "Unassigned")
- Suggested first action (investigate, reach out to customer, escalate to engineering, etc.)

Also flag any **existing tickets** that have jumped to **Urgent** priority since yesterday — these may have been escalated overnight.

---

### Step 4 — Check HubSpot for Customer Replies Needing a Response

Use `HubSpot:search_crm_objects` (object type: `tickets`) to find open tickets where the customer has sent a message that hasn't been replied to yet.

Prioritize:
- **Tickets with a customer reply > 24 hours old** and no Quandri response — flag as overdue
- **New tickets opened since EOD yesterday** — need an acknowledgement or first response
- **Any ticket marked Urgent or High priority** in HubSpot

For each, note:
- Ticket ID, company name, subject
- What the customer is asking or reporting (1 sentence)
- How long since their last message
- Suggested response type (acknowledgement, investigation needed, quick answer)

---

### Step 5 — Scan #support-team for Overnight Context

Use `Slack:slack_read_channel` on **#support-team** for messages since the lookback window.

Look for:
- Any escalations or urgent flags posted by teammates
- Customer mentions with unresolved questions
- Any context from Nick about priorities for today
- Anything from the previous evening that needs a follow-up action today

Surface only what's actionable — skip informational messages that don't require a response.

---

### Step 6 — Check for Sev-1 Tickets Needing Cleanup

The support team periodically does Sev-1 cleanup — reviewing severity-1 tickets that may be resolved or stale. Use `Linear:list_issues` to surface any **Sev-1 / Urgent** tickets that:
- Have had **no update in 7+ days**
- Are marked as resolved in practice but not yet closed in Linear
- Have a status mismatch (e.g., still "In Progress" but last comment says issue is fixed)

Flag these as a secondary cleanup task if the queue is otherwise manageable.

---

### Step 7 — Build the Prioritized Work List

Using everything gathered, produce a synthesized priority list following the structure in `references/triage-template.md`.

**Priority order logic:**
1. 🔴 **P1 — Do first**: Overnight bot run failures, overdue customer responses (>24h), Urgent tickets with no owner
2. 🟠 **P2 — Do today**: New unassigned tickets needing triage, new HubSpot tickets needing acknowledgement, escalated tickets
3. 🟡 **P3 — Do when P1/P2 are clear**: Sev-1 cleanup, stale tickets, monitoring runs that haven't failed but are scheduled today
4. ⚪ **On radar**: Things to be aware of but no action needed yet

The list should be **concrete and actionable** — not "review open tickets" but "ONC-712: Go Insurance run failed overnight — check if manual re-run is needed."

---

### Step 8 — Offer to Assign and Post

After generating the brief, offer:

1. **Assign tickets in Linear** — Use `Linear:save_issue` to assign unowned tickets to Alma or Syed based on the suggested owners in the brief
2. **Post to #support-team** — Draft a short Slack summary of today's top priorities using `Slack:slack_send_message_draft`
3. **Create Asana tasks** for any follow-ups that don't belong in Linear (customer outreach, internal coordination tasks)

**Always create drafts — never post or assign without user confirmation.**

---

## Smart Defaults & Judgment Calls

| Situation | Default Behavior |
|-----------|-----------------|
| No new tickets or failures overnight | "Clean queue — nothing new since EOD. Here's what's already open to work through." Then surface top existing open tickets |
| Monday morning | Automatically extends lookback to Friday EOD — note "covering Friday EOD through Monday morning" |
| Heavy overnight queue (10+ items) | Lead with P1 items only, summarize P2/P3 as counts with a note to review after clearing P1 |
| User is Nick (not Alma/Syed) | Frame the brief as a team overview — "here's what Alma and Syed are walking into today" |
| Ticket already assigned | Skip assigning, just list it |
| Bot run failure with an existing ONC ticket | Link the ticket, don't create a duplicate |

---

## Tool Reference

| Tool | Use |
|------|-----|
| `Linear:list_issues` | Pull new and triage-queue tickets; ONC overnight failures |
| `Linear:get_issue` | Get details on specific tickets |
| `Linear:list_comments` | Check latest activity on existing tickets |
| `Linear:save_issue` | Assign tickets to team members (with confirmation) |
| `Linear:list_teams` | Confirm ONC and other team IDs |
| `HubSpot:search_crm_objects` | Find customer replies and new HubSpot tickets |
| `HubSpot:get_crm_objects` | Get ticket details |
| `Slack:slack_read_channel` | Scan #support-team for overnight context and run flags |
| `Slack:slack_send_message_draft` | Draft the Slack summary post for #support-team |
| `Asana:asana_create_task` | Create follow-up tasks for non-Linear items |

---

## Team Context (Quandri CX)

- **Primary users**: Alma St. Hilaire and Syed (this brief is built for them)
- **Manager**: Nick (uses it as a team overview)
- **Linear team for incidents**: ONC — this is where bot run failures live
- **Product lines to know**:
  - **RR** = Renewal Rounds (most common)
  - **RQ** = Renewal Queue
  - **EE** = another product line
- **Bot run failures** are time-sensitive — customers run scheduled renewal processing and failures can block their workflows
- **Sev-1 tickets** = highest severity, map to Urgent priority in Linear
- **Triage channel**: #support-team

---

## Example Invocations

- "Morning triage"
- "What do I work on today?"
- "What came in overnight?"
- "Daily triage brief"
- "What's in the queue this morning?"
- "Start of day brief for the support team"
- "Alma, what does your queue look like today?"
