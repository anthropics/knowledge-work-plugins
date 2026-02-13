---
description: Synthesize overnight activity into a morning brief with urgent items, progress, and recommended actions
argument-hint: "<date or 'today'>"
---

# Daily Brief

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Synthesize overnight activity into a prioritized morning brief.

## Workflow

### 1. Understand the Context

Ask the user:
- What date is this brief for? (Default to today)
- What team or product area to focus on?
- Any specific concerns or priorities to watch for?

### 2. Pull Context from Connected Tools

If **~~chat** is connected:
- Pull overnight messages from key product and engineering channels
- Identify threads with unresolved questions or escalations
- Surface decisions made asynchronously
- Note any direct messages or mentions requiring the user's attention

If **~~project tracker** is connected:
- Pull sprint status and recent ticket updates
- Identify items that changed status overnight (moved to blocked, completed, or at risk)
- Surface blockers or items flagged as urgent
- Check sprint burndown progress

If **~~user feedback** is connected:
- Pull recent support tickets and their severity
- Identify trending issues or spikes in ticket volume
- Surface any critical or P0 tickets opened overnight

If **~~meeting transcription** is connected:
- Pull notes from recent meetings
- Identify action items assigned to the user
- Surface any decisions that affect the user's priorities

If no tools are connected, ask the user to paste:
- Recent Slack messages or team chat activity
- Sprint or project updates from Jira, Linear, or similar
- Support tickets or customer feedback
- Community posts or feature requests

### 3. Generate the Brief

Produce a structured morning brief. See the **sprint-execution** skill for sprint health indicators and the **meeting-preparation** skill for upcoming meeting context.

- **TL;DR**: 2-3 sentence summary of the most important things from overnight
- **Urgent Items**: Blockers, escalations, critical bugs — anything requiring action today
- **Sprint Progress**: Current sprint status, notable completions, items at risk
- **Customer Signals**: Key feedback from support and community channels
- **Recommended Actions**: Top 3 things to focus on today, ordered by priority

### 4. Follow Up

After generating the brief:
- Offer to draft responses to urgent items
- Offer to create a standup update from the brief
- Offer to investigate any concerning signals in more depth
- Offer to prep for any meetings happening today

## Output Format

Use markdown with clear headers. Keep the brief scannable — the reader should get the essential picture in 60 seconds.

## Tips

- Prioritize ruthlessly. A brief that highlights everything highlights nothing.
- Blockers and escalations always come first, before progress updates.
- Customer signals are often the most strategically important part — do not bury them.
- Recommended actions should be specific and time-bound, not vague suggestions.
- If there is nothing urgent, say so. "No fires" is valuable information.
