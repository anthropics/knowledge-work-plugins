---
name: eod-cx-wrapup
description: Generates a concise end-of-day wrap-up for the Quandri CX team by reviewing today's HubSpot tickets, Asana tasks, Slack activity, and calendar events. Summarizes what was accomplished, what's still open, and what needs attention tomorrow. Use this skill whenever the user says "end of day", "EOD summary", "wrap up my day", "what did I accomplish today", "daily wrap-up", "close out my day", "end of day report", or "what's left for today". Also trigger when the user asks to summarize the day's customer support activity or prepare a team update at the end of the workday. Ideal for CX managers and team leads who want a quick daily pulse before signing off.
---

# End of Day CX Wrap-Up

## Purpose
A quick daily close-out for the Quandri CX team — summarizes what was accomplished today, what's still open, any customer flags, and sets up tomorrow's priorities. Should take under 2 minutes to read.

## When to Use
- "EOD summary" / "end of day wrap-up"
- "Wrap up my day"
- "What did I accomplish today?"
- "What's still open before I sign off?"
- "Daily wrap-up" / "Close out my day"
- Any time the user is wrapping up their workday

---

## Core Workflow

### Step 1 — Establish Today's Date
- Default to **today** as the reporting period
- Use today's date to filter all data pulls

---

### Step 2 — Review Today's HubSpot Tickets
Use HubSpot to get a snapshot of today's ticket activity:

**Collect:**
- Tickets opened today
- Tickets resolved/closed today
- Tickets updated today (responses sent, status changes)
- Any new escalations or high-priority tickets
- Tickets that went unanswered today (opened but no response)

Use `HubSpot:search_crm_objects` filtered to today's date range.

---

### Step 3 — Check Task Completion in Asana
- Use `Asana:asana_get_tasks` to find tasks completed today by Nick, Alma, and Syed
- Pull tasks that were due today but not completed (carry-forwards)
- Pull any new tasks created today
- Use `Asana:asana_search_tasks` with today's date filter

---

### Step 4 — Scan Key Slack Channels
- Use `Slack:slack_read_channel` to scan today's activity in:
  - **#cx-team**
  - **#cx-leaders**
  - **#support-team**
- Surface: any unresolved threads, action items mentioned, customer mentions, or open questions that still need a response

---

### Step 5 — Review Today's Calendar & Meetings
- Use `Google Calendar:gcal_list_events` to pull today's meetings
- Cross-reference with `Granola:list_meetings` to check for notes
- Note: meetings that happened, any follow-ups generated, and meetings missed or rescheduled

---

### Step 6 — Identify Carry-Forwards & Tomorrow's Setup
Based on all data, identify:
- **Unfinished tasks** that should move to tomorrow
- **Open tickets** that need a response first thing tomorrow
- **Slack threads** still needing a reply
- **Any customer commitments** made today that need follow-through

---

### Step 7 — Compile the Wrap-Up
Keep it tight and scannable — this is an EOD check, not a full report.

```
# End of Day Wrap-Up — [Today's Date]

## ✅ Accomplished Today
**Tickets:**
- X opened | X resolved | X updated

**Tasks completed:**
- [Name]: [Task 1], [Task 2]
- [Name]: [Task 1]

**Meetings held:** X
- [Meeting name / account] — [one-line outcome]

---

## 🔁 Still Open
**Tickets needing attention:**
- [Ticket / account] — [issue, time open]

**Tasks not completed today:**
- [Task] — [Owner] — suggest moving to [tomorrow/date]

**Slack threads needing reply:**
- [Thread summary] in [#channel]

---

## 🔥 Flags & Escalations
- [Account / issue] — [urgency / next step]

---

## 🗓️ Tomorrow's Top 3
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

---
*Quandri CX — End of Day Wrap-Up*
```

---

### Step 8 — Offer to Share
After generating the wrap-up, offer:

**A) Post to Slack**
- Draft a brief EOD update to **#cx-team** or **#cx-leaders**
- Keep it to 3–5 bullet points — just the headlines
- Use `Slack:slack_send_message_draft` to save as draft

**B) Update Notion**
- Save the full wrap-up to Notion under CX Team > Daily Logs
- Use `Notion:notion-create-pages`

**Always save as draft — never post without user review.**

---

## Tool Reference

| Tool | Use |
|------|-----|
| `HubSpot:search_crm_objects` | Today's ticket activity |
| `HubSpot:get_crm_objects` | Ticket details |
| `Asana:asana_get_tasks` | Tasks completed and outstanding today |
| `Asana:asana_search_tasks` | Filter by today's date and assignee |
| `Slack:slack_read_channel` | Scan key CX channels for open threads |
| `Google Calendar:gcal_list_events` | Today's meetings |
| `Granola:list_meetings` | Meeting notes and outcomes |
| `Slack:slack_send_message_draft` | Draft EOD Slack update |
| `Notion:notion-create-pages` | Save wrap-up to Notion daily log |

---

## Smart Defaults & Judgment Calls

| Situation | Default Behavior |
|-----------|-----------------|
| No tickets opened today | Note positively — "Quiet day on tickets" |
| All tasks completed | Celebrate it — "Clean slate for tomorrow" |
| No meetings today | Note it, still check Slack for async activity |
| Heavy escalation day | Lead the report with the Flags section |
| User asks for yesterday's wrap-up | Adjust date range to previous workday |

---

## Team Context (Quandri CX)

- **Team members**: Nick (Manager), Alma (direct report), Syed (direct report)
- **Key Slack channels**: #cx-team, #cx-leaders, #support-team
- **Tone**: Concise and action-oriented — this is a 2-minute read, not a report
- **Notion**: Save to CX Team > Daily Logs
- **Audience**: Primarily for Nick to close out his day and prep for tomorrow

---

## Example Invocations
- "EOD summary"
- "Wrap up my day"
- "End of day wrap-up"
- "What did I accomplish today?"
- "What's still open before I sign off?"
- "Close out my day"
- "Daily wrap-up for the CX team"
