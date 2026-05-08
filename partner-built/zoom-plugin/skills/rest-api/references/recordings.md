# REST API - Recordings

Cloud recording management endpoints.

## Overview

Access and manage Zoom cloud recordings.

## Endpoints

### List User Recordings

```bash
GET /users/{userId}/recordings
```

Query parameters:
- `from` - Start date (YYYY-MM-DD)
- `to` - End date (YYYY-MM-DD)

### Get Meeting Recordings

```bash
GET /meetings/{meetingId}/recordings
```

### Delete Recordings

```bash
DELETE /meetings/{meetingId}/recordings
```

### Delete Single Recording File

```bash
DELETE /meetings/{meetingId}/recordings/{recordingId}
```

## Recording Files

Response includes multiple file types:

| Type | Description |
|------|-------------|
| `shared_screen_with_speaker_view` | Screen share + speaker |
| `shared_screen_with_gallery_view` | Screen share + gallery |
| `active_speaker` | Speaker view only |
| `gallery_view` | Gallery view only |
| `audio_only` | Audio file (M4A) |
| `chat_file` | Chat transcript |
| `timeline` | Meeting timeline |
| `audio_transcript` | VTT transcript |

## Download Recordings

```bash
# Get download URL from recording files
GET {download_url}?access_token={token}
```

**Note:** Download URLs require authentication.

## Required Scopes

- `recording:read` - View/download recordings
- `recording:write` - Delete recordings

## Resources

- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Cloud-Recording
