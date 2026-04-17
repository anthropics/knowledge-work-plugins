# Meeting Lifecycle — Use REST for CRUD

The current Zoom MCP surface does **not** expose deterministic meeting
create, update, list, or delete tools.

If the user needs meeting lifecycle management, route to the REST API skill:
- [../../rest-api/SKILL.md](../../rest-api/SKILL.md)

## What Zoom MCP Is Good For

Use Zoom MCP for:
- semantic search across meetings
- retrieval of meeting-linked assets
- recording-resource retrieval
- Zoom Docs creation from Markdown

## What To Use Instead for CRUD

Use the REST API for:
- create a meeting
- reschedule or update a meeting
- list scheduled meetings deterministically
- delete a meeting or occurrence

## Hybrid Pattern

Use MCP first when the user starts with meeting content or recap intent, then hand off to REST
only if the next action becomes a deterministic resource-management step.

Example:

```text
1. search_meetings
   q: "client onboarding"
   from: "2026-03-01"
   to: "2026-03-06"

2. get_meeting_assets
   meetingId: "MEETING_ID_OR_UUID"

3. If the user then wants to reschedule or delete the meeting,
   route to zoom-rest-api and perform the CRUD operation there.
```

## Example Prompts That Should Route to REST

- "Create a 45-minute design review for next Tuesday."
- "Move my Q1 planning meeting to Friday at 3pm Pacific."
- "Delete the team sync meeting scheduled for March 10th."
- "Show me all my scheduled meetings for this week."
