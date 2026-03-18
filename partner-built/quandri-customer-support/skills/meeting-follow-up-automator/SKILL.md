---
name: meeting-follow-up-automator
description: Automatically processes meeting notes from Granola to extract action items, create tasks in Asana or Linear, and draft follow-up messages in Slack or email. Use this skill whenever the user mentions following up after a meeting, capturing action items, post-meeting tasks, or anything like "what came out of my meeting", "create tasks from my meeting", "send a follow-up", "meeting recap", or "what do I need to do after my call". Also trigger when the user finishes describing a meeting and asks what to do next. This skill is especially valuable for Customer Experience team members who frequently run customer calls, internal syncs, and onboarding sessions.
---

# Meeting Follow-Up Automator

## Purpose
Automatically turns meeting notes (from Granola) into action items, tasks, and follow-up communications — eliminating manual post-meeting work for the CX team.

## When to Use
- "Follow up from my meeting" / "post-meeting actions"
- "What came out of my [meeting/call/sync]?"
- "Create tasks from my meeting notes"
- "Send a recap to the team"
- "Draft a follow-up to [customer/person]"
- Any time a meeting just ended and there's work to capture
- After customer calls, onboarding sessions, internal syncs, escalation reviews

---

## Core Workflow

### Step 1 — Identify the Meeting
- Use `Granola:list_meetings` to fetch recent meetings (last 24–48 hours)
- If multiple meetings exist, show a brief list and ask which one to process
- If the user names a meeting, use `Granola:query_granola_meetings` to find it
- Once identified, use `Granola:get_meeting_transcript` to pull the full transcript

### Step 2 — Extract Action Items
Analyze the transcript for:
- **Action items**: Explicit tasks, commitments, promises made ("I'll send you...", "We need to...", "Can you follow up on...")
- **Owners**: Who is responsible for each action (assign to self if unclear and user is CX team member)
- **Deadlines**: Any mentioned dates or urgency signals ("by EOW", "before the next call", "urgent")
- **Decisions made**: Key outcomes or agreements reached
- **Open questions**: Things that were flagged but not resolved
- **Customer sentiment** (if customer-facing): Note any frustration, satisfaction, or risk signals

Format extracted items clearly before proceeding:
```
📋 Action Items Found:
1. [Action] — Owner: [Name] — Due: [Date or ASAP]
2. ...

✅ Decisions Made:
- ...

❓ Open Questions:
- ...
```

**Always show this summary to the user and confirm before creating tasks or sending messages.**

### Step 3 — Create Tasks (with user confirmation)
Based on confirmed action items:

#### Asana Tasks
- Use `Asana:asana_create_task` for each action item
- Set due dates where specified
- Assign to the correct team member
- Add meeting name and date as context in the task description
- Group related tasks under the relevant Asana project if identifiable

#### Linear Tickets (for product/bug-related items)
- Use `Linear:save_issue` for any action items that are bugs, feature requests, or product feedback surfaced in the meeting
- Tag with appropriate labels (e.g., "customer-feedback", "cx-request")
- Link to customer name or HubSpot contact if relevant

**Default behavior**: Create in Asana unless the action item is clearly product/engineering-related, in which case use Linear.

### Step 4 — Draft Follow-Up Communication
After tasks are created, offer to draft one or more of the following:

#### Option A: Internal Slack Summary
- Post to the relevant team channel (e.g., #cx-team, #support-team)
- Format:
  ```
  📝 *Meeting Recap: [Meeting Name] — [Date]*
  
  *Key Decisions:*
  - ...
  
  *Action Items:*
  - [ ] [Task] → @owner (due: [date])
  
  *Open Questions:*
  - ...
  ```
- Use `Slack:slack_send_message_draft` to save as draft for review before sending

#### Option B: Customer Follow-Up Email
- Draft a professional follow-up to the customer/attendees
- Summarize what was discussed, decisions made, and next steps
- Use `Gmail:gmail_create_draft` to save as a draft
- Keep tone warm and action-oriented; avoid internal jargon

#### Option C: Both
- Create both the internal Slack summary and the external email draft simultaneously

**Always create drafts — never send directly without user review.**

---

## Smart Defaults & Judgment Calls

| Situation | Default Behavior |
|-----------|-----------------|
| No explicit owner on action item | Assign to the user running the skill |
| No deadline mentioned | Leave due date blank, note "no deadline set" |
| Customer name mentioned | Flag for potential HubSpot follow-up |
| Recurring meeting | Note it's recurring, still create tasks for this meeting's items |
| Very short meeting (<15 min) | Still process, may have few items |
| Meeting with no action items | Report this clearly, offer to send a quick "no actions" summary |

---

## Output Format

After completing the workflow, provide a clean summary:

```
✅ Meeting Follow-Up Complete: [Meeting Name]

📋 Tasks Created:
- [X] tasks in Asana
- [X] tickets in Linear (if any)

📨 Drafts Ready:
- Slack draft in [#channel]
- Email draft to [recipient] in Gmail

🔔 Reminders:
- Review and send drafts when ready
- [Any open questions that still need answers]
```

---

## Tool Reference

| Tool | Use |
|------|-----|
| `Granola:list_meetings` | Find recent meetings |
| `Granola:get_meeting_transcript` | Pull full transcript |
| `Granola:query_granola_meetings` | Search for specific meeting |
| `Asana:asana_create_task` | Create action item tasks |
| `Asana:asana_get_projects` | Find relevant project to attach tasks |
| `Linear:save_issue` | Create product/bug tickets |
| `Slack:slack_send_message_draft` | Save internal recap as Slack draft |
| `Gmail:gmail_create_draft` | Save customer follow-up as email draft |
| `Google Calendar:gcal_get_event` | Cross-reference meeting details if needed |

---

## Team Context (Quandri CX)

- **Team channels**: #cx-team, #cx-leaders, #support-team
- **Key roles**: Nick (Manager), Alma (direct report), Syed (direct report)
- **Meeting types to expect**: Customer onboarding calls, escalation reviews, 1:1s, team syncs, product feedback sessions
- **Customer-facing follow-ups**: Keep professional, concise, and action-oriented
- **Internal follow-ups**: Can be more casual, use Slack-friendly formatting

---

## Example Invocations

- "Follow up from my meeting with BrokerLink this morning"
- "What are the action items from my 2pm call?"
- "Create tasks from today's onboarding session"
- "Draft a recap for the team from my escalation review"
- "Post-meeting actions from my Granola notes"
- "Send a follow-up to the customer from this morning's call"
