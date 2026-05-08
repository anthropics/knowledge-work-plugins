# Search and Act — Zoom MCP Patterns

Patterns for finding meetings and taking action using the current Zoom MCP tool surface.

## Search by Topic or Time Range

```text
search_meetings
  q: "budget review"
  from: "2026-03-01"
  to: "2026-03-06"
  page_size: 10
```

Use this when the user starts from what was discussed rather than from a known meeting ID.

## Search Then Inspect Assets

```text
Step 1:
search_meetings
  q: "product roadmap"
  from: "2026-03-01"
  to: "2026-03-06"

Step 2:
get_meeting_assets
  meetingId: "MEETING_ID_OR_UUID"
```

This is the main MCP pattern for retrieving summaries, recording references, linked docs, and
other meeting-related assets.

## Search Then Inspect Recording Resources

```text
Step 1:
search_meetings
  q: "all hands"
  from: "2026-03-01"
  to: "2026-03-06"

Step 2:
get_recording_resource
  meetingId: "MEETING_ID_OR_UUID"
```

Use this when the user needs transcript-capable or playback-oriented resources after they have
identified the target meeting.

## Search Then Create a Zoom Doc

```text
Step 1:
search_meetings
  q: "Q1 planning"

Step 2:
get_meeting_assets
  meetingId: "MEETING_ID_OR_UUID"

Step 3:
switch to the dedicated zoom-docs-mcp server

Step 4:
create_file_with_content
  file_name: "Q1 Planning Summary"
  content: "# Decisions\n\n- ..."
```

## When to Hand Off to REST

If the user asks for deterministic operations such as:
- create a meeting
- reschedule a meeting
- update meeting settings
- delete a meeting

route to [../../rest-api/SKILL.md](../../rest-api/SKILL.md) instead of assuming the current
Zoom MCP surface exposes meeting CRUD.

## Example Prompts

- "Find meetings about the product launch in February and summarize them."
- "Look up last week's all-hands and pull the recording resources."
- "Search for Q1 planning discussions and create a Zoom Doc from the recap."
- "I need to reschedule a meeting" → hand off to the REST API skill.
