---
name: pre-call-brief
description: >
  Generates a concise pre-call brief for an upcoming customer meeting — pulls account context from
  HubSpot, top open tickets from Linear, recent meeting history from Granola, and recent Slack
  mentions. Produces a 60-second read so you walk into every call fully prepared.
  Use when: pre-call brief, brief for my call, prep for my meeting, what do I need to know before
  my call, call prep, brief on [customer], prepare for my call with, what's the situation with [customer].
---

# Pre-Call Brief

## Purpose
Give the user everything they need to know before a customer call — in a format that takes under 60 seconds to read. This is a forward-looking snapshot, not a deep audit. The goal is confident, informed preparation.

## When to Use
- "Pre-call brief for [Customer]"
- "Prep me for my call with [Customer]"
- "What do I need to know before my meeting with [Customer]?"
- "Brief on [Customer] — I have a call in 10 minutes"
- "Call prep for [Customer]"
- Any time a calendar event with a customer is coming up soon

---

## Core Workflow

### Step 1 — Identify the Customer and Meeting

**If the user names the customer directly**: use that name throughout.

**If the user says "my next call" or "upcoming meeting"**:
- Call `Google Calendar:gcal_list_events` for the next 4 hours
- Find the next customer-facing event (exclude internal meetings like 1:1s, standups, or Quandri team syncs)
- Confirm the customer name with the user before proceeding

Once confirmed, note:
- Meeting title, time, and duration
- Attendees (if available from the calendar invite)
- Any agenda or description in the invite

---

### Step 2 — Pull HubSpot Account Context

Look up the company in HubSpot using `HubSpot:search_crm_objects` (object type: `companies`).

Collect:
- **Full company name** (use this exact name when searching Linear)
- **Plan tier and ARR**
- **Named CSM** and account owner
- **Renewal date** — flag if within 90 days
- **HubSpot health/status** — any risk flags, NPS scores, or health ratings if present
- **Recent HubSpot ticket activity** — any open tickets, especially high-priority or unresolved ones opened in the last 30 days (use `HubSpot:search_crm_objects` filtered to object type `tickets`)
- **Last interaction date** — when was the last logged activity or email?

If the company is not found in HubSpot, note this clearly and continue with what's available.

---

### Step 3 — Pull Top Open Linear Tickets

Use the Linear Customers API to find tickets linked to this customer (same approach as the ticket-breakdown skill — use `list_customers` with `includeNeeds: true`).

**For this brief, do not pull every ticket.** Focus only on:
- All **Urgent** and **High** priority open tickets
- Any ticket in **Blocked** status
- Any tickets that have had **no updates in 14+ days** (stale)

Cap at **8 tickets maximum** for the brief. If the account has more, note the total count and indicate that the top issues are shown. Direct the user to the ticket breakdown skill for a full audit.

For each ticket, collect:
- Ticket ID, title, status, priority, assignee
- Most recent comment or update (date + one-line summary)

---

### Step 4 — Review Recent Meeting History

Use `Granola:query_granola_meetings` to find past meetings with this customer.

Pull the **3 most recent meetings**. For each:
- Date and meeting title
- 2–3 sentence summary of what was discussed and what was committed to
- Any open action items that were assigned to Quandri

If no past meetings are found in Granola, note it — this may be a first call or early-stage relationship.

---

### Step 5 — Check Recent Slack Mentions

Use `Slack:slack_search_public_and_private` to search for the customer name in the last 14 days.

Look for:
- Any escalations or urgent flags raised about this account
- Internal discussions about known issues or commitments
- Sentiment signals (positive or negative chatter)

Keep this light — flag only what's notable. If nothing relevant, skip this section in the output.

---

### Step 6 — Compose the Brief

Follow the structure in `references/brief-template.md` exactly. The output must be **short and scannable** — this is not a report. Aim for something readable in under 60 seconds.

**Health signal guidance** (use in the header):
- 🟢 **Healthy** — Renewing far out, low ticket volume, positive sentiment, no escalations
- 🟡 **Watch** — Renewal within 90 days, elevated ticket volume, or one open escalation
- 🔴 **At Risk** — Renewal within 30 days + open issues, active escalation, or explicit churn signals

If there is insufficient data to judge, use ⚪ **Unknown**.

---

### Step 7 — Offer Next Steps

After presenting the brief, offer:

1. **Full ticket audit** — "Want the full ticket breakdown for [Customer]?" (triggers the ticket-breakdown skill)
2. **Draft a talking points doc** — Expand the suggested talking points into a structured agenda
3. **Post-call follow-up** — Remind the user to run the meeting follow-up automator after the call

---

## Smart Defaults & Judgment Calls

| Situation | Default Behavior |
|-----------|-----------------|
| Customer has no open Linear tickets | Note positively — "No open tickets" |
| No past Granola meetings found | Flag as first call or no recorded history |
| Renewal date not in HubSpot | Note "Renewal date not on file" |
| Multiple HubSpot companies match | Show the top 2 matches and ask the user to confirm |
| Call is in < 5 minutes | Lead with the header and top tickets only — skip Slack search to save time |
| User says "quick brief" | Output header + top 3 tickets + last meeting only |

---

## Tool Reference

| Tool | Use |
|------|-----|
| `Google Calendar:gcal_list_events` | Find upcoming customer meetings |
| `HubSpot:search_crm_objects` | Look up company and recent tickets |
| `HubSpot:get_crm_objects` | Retrieve detailed account or ticket records |
| `Linear:list_customers` | Find all Linear tickets linked to this customer |
| `Linear:get_issue` | Pull ticket details, status, and latest comments |
| `Linear:list_comments` | Get most recent comment on a ticket |
| `Granola:query_granola_meetings` | Find past meetings with this customer |
| `Granola:get_meeting_transcript` | Pull summary/notes from a specific meeting |
| `Slack:slack_search_public_and_private` | Check recent Slack mentions of the customer |

---

## Team Context (Quandri CX)

- **Support team**: Nick (Manager), Alma St. Hilaire, Syed
- **CSM team**: Jenel McKenney (CSM Manager), Andrew Millar, Jonathan Cox
- **Support email**: support@quandri.io
- **Linear workspace**: linear.app/quandriio
- **Tone**: Crisp and factual — this brief is for internal use only

---

## Example Invocations

- "Pre-call brief for BrokerLink"
- "Prep me for my call with Acera"
- "What do I need to know before my 2pm with First America?"
- "Quick brief on Go Insurance — call in 10 minutes"
- "What's the situation with Wawanesa before my call?"
