# Zoom Video SDK API

Authoritative endpoint inventory for Video SDK. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/video-sdk/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 38 |
| Path templates | 28 |
| Tags | 4 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Byos Storage | 6 |
| Cloud Recording | 6 |
| Sessions | 21 |
| Video SDK Reports | 5 |

## Endpoints by Tag

### Byos Storage

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| PATCH | `/videosdk/settings/storage` | Update Bring Your Own Storage settings | `byosStorageSwitchPatch` |
| GET | `/videosdk/settings/storage/location` | List storage location | `byosStorageGet` |
| POST | `/videosdk/settings/storage/location` | Add storage location | `byosStoragePost` |
| DELETE | `/videosdk/settings/storage/location/{storageLocationId}` | Delete storage location detail | `byosStorageDetailDelete` |
| GET | `/videosdk/settings/storage/location/{storageLocationId}` | Storage location detail | `byosStorageDetailGet` |
| PATCH | `/videosdk/settings/storage/location/{storageLocationId}` | Change storage location detail | `byosStorageDetailPatch` |

### Cloud Recording

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/videosdk/recordings` | List recordings of an account | `recordingsList` |
| DELETE | `/videosdk/sessions/{sessionId}/recordings` | Delete session's recordings | `recordingDelete` |
| GET | `/videosdk/sessions/{sessionId}/recordings` | List session's recordings | `recordingGet` |
| PUT | `/videosdk/sessions/{sessionId}/recordings/status` | Recover session's recordings | `recordingStatusUpdate` |
| DELETE | `/videosdk/sessions/{sessionId}/recordings/{recordingId}` | Delete session's recording file | `recordingDeleteOne` |
| PUT | `/videosdk/sessions/{sessionId}/recordings/{recordingId}/status` | Recover a single recording | `recordingStatusUpdateOne` |

### Sessions

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/videosdk/sessions` | List sessions | `sessions` |
| POST | `/videosdk/sessions` | Create a session | `Createasession` |
| DELETE | `/videosdk/sessions/{sessionId}` | Delete a session | `sessionDelete` |
| GET | `/videosdk/sessions/{sessionId}` | Get session details | `sessionDetail` |
| PATCH | `/videosdk/sessions/{sessionId}/events` | Use in-session events controls | `inSessionEventsControl` |
| GET | `/videosdk/sessions/{sessionId}/livestream` | Get session live stream details | `getLiveStreamDetails` |
| PATCH | `/videosdk/sessions/{sessionId}/livestream` | Update a session live stream | `sessionLiveStreamUpdate` |
| PATCH | `/videosdk/sessions/{sessionId}/livestream/status` | Update session livestream status | `sessionLiveStreamStatusUpdate` |
| PATCH | `/videosdk/sessions/{sessionId}/rtms_app/status` | Update Realtime Media Streams (RTMS) app status | `updateSessionRtmsAppStatus` |
| POST | `/videosdk/sessions/{sessionId}/sip_dialing` | Get a session SIP URI with passcode | `GetASessionSIPURIWithPasscode` |
| PUT | `/videosdk/sessions/{sessionId}/status` | Update session status | `sessionStatus` |
| GET | `/videosdk/sessions/{sessionId}/stream_ingestions` | List session streaming ingestions | `Listsessionstreamingingestions` |
| GET | `/videosdk/sessions/{sessionId}/users` | List session users | `sessionUsers` |
| GET | `/videosdk/sessions/{sessionId}/users/qos` | List session users QoS | `sessionUsersQOS` |
| GET | `/videosdk/sessions/{sessionId}/users/sharing` | Get sharing/recording details | `sessionParticipantShare` |
| GET | `/videosdk/sessions/{sessionId}/users/{userId}/qos` | Get session user QoS | `sessionUserQOS` |
| GET | `/videosdk/stream_ingestions` | List stream ingestions | `Liststreamingestions` |
| POST | `/videosdk/stream_ingestions` | Create a stream ingestion | `Createastreamingestion` |
| DELETE | `/videosdk/stream_ingestions/{streamId}` | Delete a stream ingestion | `Deleteastreamingestion` |
| GET | `/videosdk/stream_ingestions/{streamId}` | Get a stream ingestion | `Getastreamingestion` |
| PATCH | `/videosdk/stream_ingestions/{streamId}` | Update a stream ingestion | `Updateastreamingestion` |

### Video SDK Reports

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/videosdk/report/cloud_recording` | Get cloud recording usage report | `vsdkReportCloudRecording` |
| GET | `/videosdk/report/daily` | Get daily usage report | `vsdkReportDaily` |
| GET | `/videosdk/report/operationlogs` | Get operation logs report | `vsdkReportOperationLogs` |
| GET | `/videosdk/report/telephone` | Get telephone report | `vsdkReportTelephone` |
| GET | `/videosdk/report/webhook_logs` | Get webhook logs | `getWebhookLogs` |
