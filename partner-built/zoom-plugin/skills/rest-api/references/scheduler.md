# Zoom Scheduler API

Authoritative endpoint inventory for Scheduler. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/scheduler/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 21 |
| Path templates | 13 |
| Tags | 9 |

## Tag Index

| Tag | Operations |
|-----|------------|
| analytics | 1 |
| availability | 5 |
| Routing Forms | 1 |
| scheduled events | 5 |
| schedules | 5 |
| scheduling links | 1 |
| shares | 1 |
| team | 1 |
| users | 1 |

## Endpoints by Tag

### analytics

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/scheduler/analytics` | Report analytics | `report_analytics` |

### availability

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/scheduler/availability` | List availability | `list_availability` |
| POST | `/scheduler/availability` | Insert availability | `insert_availability` |
| DELETE | `/scheduler/availability/{availabilityId}` | Delete availability | `delete_availability` |
| GET | `/scheduler/availability/{availabilityId}` | Get availability | `get_availability` |
| PATCH | `/scheduler/availability/{availabilityId}` | Patch availability | `patch_availability` |

### Routing Forms

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/scheduler/routing/forms/{formId}/response/{responseId}` | get routing response | `Getroutingresponse` |

### scheduled events

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/scheduler/events` | List scheduled events | `list_scheduled_events` |
| DELETE | `/scheduler/events/{eventId}` | Delete scheduled events | `delete_scheduled_events` |
| GET | `/scheduler/events/{eventId}` | Get scheduled events | `get_scheduled_events` |
| PATCH | `/scheduler/events/{eventId}` | Patch scheduled events | `patch_scheduled_events` |
| GET | `/scheduler/events/{eventId}/attendees/{attendeeId}` | Get scheduled event attendee | `get_scheduled_event_attendee` |

### schedules

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/scheduler/schedules` | List schedules | `list_schedules` |
| POST | `/scheduler/schedules` | Insert schedules | `insert_schedule` |
| DELETE | `/scheduler/schedules/{scheduleId}` | Delete schedules | `delete_schedules` |
| GET | `/scheduler/schedules/{scheduleId}` | Get schedules | `get_schedule` |
| PATCH | `/scheduler/schedules/{scheduleId}` | Patch schedules | `patch_schedule` |

### scheduling links

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/scheduler/schedules/single_use_link` | Single use link | `single_use_link` |

### shares

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/scheduler/shares` | Create shares | `create_shares` |

### team

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/scheduler/teams` | List team | `Listteam` |

### users

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/scheduler/users/{userId}` | Get user | `get_user` |
