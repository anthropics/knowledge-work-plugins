# Transcript and Summary Retrieval

Use the Zoom MCP server when the goal is to search meeting content, retrieve meeting-linked
assets, or fetch recording-oriented resources after a meeting.

## Path 1: Semantic Search and Meeting Assets

Use this path when the user starts from content, topic, or time range.

### Prerequisites

- `meeting:read:search`
- `meeting:read:assets`
- AI Companion features such as **Smart Recording** and **Meeting Summary** enabled for useful recap data

### Step 1: Search meetings

```text
search_meetings
  q: "Q4 budget discussion"
  from: "2026-03-01"
  to: "2026-03-06"
  page_size: 20
```

### Step 2: Choose a meeting and retrieve assets

```text
get_meeting_assets
  meetingId: "MEETING_ID_OR_UUID"
```

Expect the result to contain a meeting-linked asset bundle. In practice, this can include:
- AI summary or recap-linked content
- recording references
- linked documents
- whiteboard links

Do not hardcode exact field names without checking a current live response.

## Path 2: Recording-Oriented Retrieval

Use this path when the user needs transcript-capable resources, recording playback resources,
or recording lookup by user/date range.

### Prerequisites

- `cloud_recording:read:list_user_recordings`
- `cloud_recording:read:content`

### Step 1: List recordings

```text
recordings_list
  userId: "me"
  from: "2026-03-01"
  to: "2026-03-06"
  page_size: 50
```

### Step 2: Retrieve recording resources

```text
get_recording_resource
  meetingId: "MEETING_UUID_OR_RECORDING_ID"
```

Use this when the user needs recording-oriented data such as:
- transcript timelines
- summary segments
- next-step segments
- playback URLs
- recording metadata

## Choosing Between the Paths

| Need | Preferred path |
|------|----------------|
| Search by topic or what was discussed | `search_meetings` → `get_meeting_assets` |
| Inspect all meeting-linked assets | `get_meeting_assets` |
| List recordings by user/date | `recordings_list` |
| Fetch recording-oriented resources for a specific meeting | `get_recording_resource` |

## Direct Downloads

If a returned recording resource includes a direct URL, fetch it with the same bearer token.
The URL is not public by default.

## Troubleshooting

**`search_meetings` fails with missing scope:**
- add `meeting:read:search`

**`get_meeting_assets` fails with missing scope:**
- add `meeting:read:assets`

**`recordings_list` fails with missing scope:**
- add `cloud_recording:read:list_user_recordings`

**`get_recording_resource` fails with missing scope:**
- add `cloud_recording:read:content`

**Search results are sparse or low quality:**
- enable Smart Recording and Meeting Summary
- widen the date window
- fall back to `recordings_list` if the user is really asking for post-meeting recording content
