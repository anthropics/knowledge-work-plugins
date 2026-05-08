# Zoom Calendar API

Authoritative endpoint inventory for Calendar. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/calendar/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 28 |
| Path templates | 16 |
| Tags | 7 |

## Tag Index

| Tag | Operations |
|-----|------------|
| acl | 5 |
| calendar list | 5 |
| calendars | 4 |
| colors | 1 |
| events | 9 |
| freebusy | 1 |
| settings | 3 |

## Endpoints by Tag

### acl

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/calendars/{calId}/acl` | List ACL rules of specified calendar | `Listacl` |
| POST | `/calendars/{calId}/acl` | Create a new ACL rule | `Insertacl` |
| DELETE | `/calendars/{calId}/acl/{aclId}` | Delete an existing ACL rule | `Deleteacl` |
| GET | `/calendars/{calId}/acl/{aclId}` | Get the specified ACL rule | `Getacl` |
| PATCH | `/calendars/{calId}/acl/{aclId}` | Update the specified ACL rule | `Patchacl` |

### calendar list

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/calendars/users/{userIdentifier}/calendarList` | List the calendars in the user's own calendarList | `ListcalendarList` |
| POST | `/calendars/users/{userIdentifier}/calendarList` | Insert an existing calendar to the user's own calendarList | `InsertcalendarList` |
| DELETE | `/calendars/users/{userIdentifier}/calendarList/{calendarId}` | Delete an existing calendar from the user's own calendarList | `DeletecalendarList` |
| GET | `/calendars/users/{userIdentifier}/calendarList/{calendarId}` | Get a specified calendar from the user's own calendarList | `GetcalendarList` |
| PATCH | `/calendars/users/{userIdentifier}/calendarList/{calendarId}` | Update an existing calendar in the user's own calendarList | `PatchcalendarList` |

### calendars

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/calendars` | Create a new secondary calendar | `Insertcalendar` |
| DELETE | `/calendars/{calId}` | Delete a calendar owned by a user | `Deletecalendar` |
| GET | `/calendars/{calId}` | Get the specified calendar | `Getcalendar` |
| PATCH | `/calendars/{calId}` | Update the specified calendar | `Patchcalendar` |

### colors

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/calendars/colors` | Get the color definitions for calendars and events | `Getcolor` |

### events

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/calendars/{calId}/events` | List events on the specified calendar | `Listevent` |
| POST | `/calendars/{calId}/events` | Insert a new event to the specified calendar | `Insertevent` |
| POST | `/calendars/{calId}/events/import` | Import event to the specified calendar | `Importevent` |
| POST | `/calendars/{calId}/events/quickAdd` | Quick add an event to the specified calendar | `Quickaddevent` |
| DELETE | `/calendars/{calId}/events/{eventId}` | Delete an existing event from the specified calendar | `Deleteevent` |
| GET | `/calendars/{calId}/events/{eventId}` | Get the specified event on the specified calendar | `Getevent` |
| PATCH | `/calendars/{calId}/events/{eventId}` | Update the specified event on the specified calendar | `Patchevent` |
| GET | `/calendars/{calId}/events/{eventId}/instances` | List all instances of the specified recurring event | `Instanceevent` |
| POST | `/calendars/{calId}/events/{eventId}/move` | Move the specified event from a calendar to another specified calendar | `Moveevent` |

### freebusy

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/calendars/freeBusy` | Query freebusy information for a set of calendars | `Queryfreebusy` |

### settings

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/calendars/users/{userIdentifier}/settings` | List all user calendar settings of the authenticated user | `Listsettings` |
| GET | `/calendars/users/{userIdentifier}/settings/{settingId}` | Get the specified user calendar settings of the authenticated user | `Getsetting` |
| PATCH | `/calendars/users/{userIdentifier}/settings/{settingId}` | Patch the specified user calendar settings of the authenticated user | `Patchsetting` |
