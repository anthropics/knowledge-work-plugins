---
name: support-handoff
description: >
  Generates a clean coverage handoff doc for the support team when a team member is out —
  pulls active Linear investigations, open HubSpot tickets, pending customer responses,
  bot runs to monitor, and any open Slack threads needing attention. Produces a handoff
  ready to post in #support-team. Use when: handoff, coverage doc, I'm going out of office,
  OOO handoff, coverage for [person], I'm off tomorrow, create a handoff, leaving for [time],
  who's covering, support coverage, out of office handoff, going on vacation.
---

# Support Handoff

## Purpose
Generate a structured coverage handoff when a support team member is going out. The output should give whoever is covering full context on what's active, what needs monitoring, and what can wait — without having to dig through Linear, HubSpot, or Slack themselves.

## When to Use
- "I'm off tomorrow, create a handoff"
- "Coverage doc for [person] while they're out"
- "OOO handoff — I'm out [dates]"
- "Create a handoff for Alma before her vacation"
- "What does Syed need to know while I'm gone?"
- Any time someone on the support team is going out and needs to brief their coverage

---

## Core Workflow

### Step 1 — Establish the Handoff Details

Collect from the user's message or ask if not provided:
- **Who is going out** (default: the user running the skill)
- **Dates out** (start and end)
- **Who is covering** (if known — otherwise leave as "TBD" and note it)
- **Any specific context** the user wants to highlight upfront (e.g., "there's a big run happening Friday", "we have an angry customer at Acera")

If the dates span a weekend, note that only business days are covered.

---

### Step 2 — Pull Active Linear Investigations

Find all open tickets currently assigned to the person going out.

Use `Linear:list_issues` filtered by assignee. Focus on:
- All tickets in **In Progress** or **Todo** status assigned to this person
- Any **Blocked** tickets they own
- Any **Urgent or High** priority tickets assigned to them regardless of status

For each ticket, collect:
- Ticket ID, title, status, priority
- 1–2 sentence summary of where things stand
- Most recent comment or update (date + content) via `Linear:list_comments`
- Specific next action needed from the coverage person (e.g., "check if the run completes", "follow up with customer if no response by Thursday", "waiting on engineering — just monitor")

**Flag separately** any tickets that have a time-sensitive deadline or a customer waiting on a response — these need prominent placement in the handoff doc.

---

### Step 3 — Pull Open HubSpot Tickets

Use `HubSpot:search_crm_objects` (object type: `tickets`) to find open tickets currently owned by or involving the person going out.

Focus on:
- **Tickets awaiting a customer response** — these can probably wait, but note them
- **Tickets where the customer has responded and is waiting on Quandri** — these are time-sensitive
- **Any ticket open > 5 days with no recent activity** — flag as at-risk of going stale

For each, note:
- Ticket ID, company name, subject
- Current status and last activity date
- What action is needed and by when

---

### Step 4 — Check for Bot Runs and Scheduled Events to Monitor

This is Quandri-specific. The support team monitors automated renewal bot runs for customers. Use `Slack:slack_search_public_and_private` to search **#support-team** for the past 7 days for any mentions of:
- Scheduled runs, bot runs, or processing schedules
- Customer names paired with run-related terms ("run", "bot", "processing", "stuck", "failed", "schedule")
- Any customers the person flagged as needing monitoring

Also check `Slack:slack_read_channel` on **#support-team** for the last few days to catch any recent context.

Produce a "Runs to Watch" list: for each flagged customer, note what to look for and what to do if a run fails (e.g., "re-run manually", "create a Linear ticket", "tag Alma in Slack").

If no specific runs are identified, note this clearly — it's not always applicable.

---

### Step 5 — Scan for Open Slack Threads Needing a Response

Use `Slack:slack_read_channel` on **#support-team** and **#cx-team** for the last 3 days. Look for:
- Threads with a question or request that the person going out hasn't responded to yet
- Any thread where the person is the last responder and something is still pending
- DMs or mentions that haven't been addressed (search `to:<@user>` or `from:<@user>` if helpful)

List each open thread with a one-line summary and the channel it's in.

---

### Step 6 — Note Outstanding Customer Commitments

Cross-reference recent Granola meetings using `Granola:query_granola_meetings` for any customer-facing commitments the person made that fall due during their absence:
- "I'll follow up by end of week"
- "We'll send you the update next Tuesday"
- Any promises to check on a run or investigate an issue

Flag these explicitly — they're the things most likely to fall through the cracks during OOO.

---

### Step 7 — Compose the Handoff Doc

Follow the structure in `references/handoff-template.md` exactly.

Keep the tone practical and direct — this is a working doc for the coverage person, not a report. It should be pasteable directly into **#support-team**.

---

### Step 8 — Offer to Post to Slack

After generating the handoff, offer to:
- **Draft a Slack post** for #support-team using `Slack:slack_send_message_draft` — formatted for Slack (shorter, with key sections only)
- **Save the full doc to Notion** under CX Team for reference

**Always save as draft — never post without user review.**

---

## Smart Defaults & Judgment Calls

| Situation | Default Behavior |
|-----------|-----------------|
| No active Linear tickets | "No active investigations — clean handoff on tickets" |
| No open HubSpot tickets | "No open HubSpot tickets requiring coverage" |
| Coverage person not named | Note "Coverage: TBD — assign before going out" |
| Out for one day only | Trim to urgent items only — skip the full ticket list |
| Out over a weekend | Note "Weekend gap — flag anything time-sensitive for Monday" |
| Multiple people sharing coverage | List each person and what they're covering |
| User is Nick handing off to both Alma and Syed | Address the handoff to both and split responsibilities if logical |

---

## Tool Reference

| Tool | Use |
|------|-----|
| `Linear:list_issues` | Pull open tickets assigned to the person going out |
| `Linear:get_issue` | Get ticket details and current status |
| `Linear:list_comments` | Get the most recent activity on a ticket |
| `HubSpot:search_crm_objects` | Find open support tickets owned by this person |
| `HubSpot:get_crm_objects` | Get ticket details |
| `Slack:slack_read_channel` | Check recent #support-team and #cx-team activity |
| `Slack:slack_search_public_and_private` | Find bot run mentions and open threads |
| `Granola:query_granola_meetings` | Check for outstanding customer commitments |
| `Slack:slack_send_message_draft` | Draft the Slack handoff post for #support-team |
| `Notion:notion-create-pages` | Save the full handoff to Notion |

---

## Team Context (Quandri CX)

- **Support team**: Nick (Manager), Alma St. Hilaire, Syed
- **Primary handoff channel**: #support-team
- **Bot runs**: A core part of the support team's daily monitoring — scheduled bot runs for customer renewal processing. Failures typically require a Linear ticket (ONC team) or a manual re-run.
- **Tone**: Practical and thorough — the coverage person should be able to hit the ground running with zero follow-up questions

---

## Example Invocations

- "I'm off Thursday and Friday — create a handoff for Syed"
- "Alma's on vacation next week, what does she need to hand off?"
- "OOO handoff — I'm out Dec 23–27, Syed is covering"
- "Create a coverage doc before I go"
- "What should I hand off before my long weekend?"
