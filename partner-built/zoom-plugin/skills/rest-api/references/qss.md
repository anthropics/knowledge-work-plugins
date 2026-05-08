# Zoom QSS API

Authoritative endpoint inventory for QSS. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/qss/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 3 |
| Path templates | 3 |
| Tags | 2 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Dashboards | 2 |
| Video SDK Sessions | 1 |

## Endpoints by Tag

### Dashboards

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/metrics/meetings/{meetingId}/participants/qos_summary` | List meeting participants QoS Summary | `dashboardMeetingParticipantsQOSSummary` |
| GET | `/metrics/webinars/{webinarId}/participants/qos_summary` | List webinar participants QoS Summary | `dashboardWebinarParticipantsQOSSummary` |

### Video SDK Sessions

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/videosdk/sessions/{sessionId}/users/qos_summary` | List session users QoS Summary | `sessionUsersQOSSummary` |
