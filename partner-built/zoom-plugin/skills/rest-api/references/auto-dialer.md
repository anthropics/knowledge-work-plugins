# Zoom Auto Dialer API

Authoritative endpoint inventory for Auto Dialer. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/auto-dialer/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 14 |
| Path templates | 8 |
| Tags | 3 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Call History & Reporting | 2 |
| Call List Management | 5 |
| Prospect Management | 7 |

## Endpoints by Tag

### Call History & Reporting

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/dialer/call-histories/{callHistoryId}` | Get Call History by ID | `GetCallDetailsbyCallID` |
| GET | `/dialer/call-history` | Get Call History | `GetCallHistory` |

### Call List Management

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/dialer/call-lists` | List Call Lists | `ListCallLists` |
| POST | `/dialer/call-lists` | Create Call List | `CreateCallList` |
| DELETE | `/dialer/call-lists/{callListId}` | Delete Call List | `DeleteCallList` |
| GET | `/dialer/call-lists/{callListId}` | Get Call List by ID | `GetCallListbyID` |
| PATCH | `/dialer/call-lists/{callListId}` | Update Call List | `UpdateCallList` |

### Prospect Management

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/dialer/call-lists/{callListId}/prospects` | List All Prospects in Call List | `ListAllProspectsInCallList` |
| PATCH | `/dialer/call-lists/{callListId}/prospects` | Update Prospects batch | `UpdateProspects` |
| POST | `/dialer/call-lists/{callListId}/prospects` | Create Prospect | `CreateProspect` |
| POST | `/dialer/call-lists/{callListId}/prospects/batch` | Create Prospects batch | `CreateProspects` |
| DELETE | `/dialer/call-lists/{callListId}/prospects/{prospectId}` | Delete Prospect | `DeleteProspect` |
| PATCH | `/dialer/call-lists/{callListId}/prospects/{prospectId}` | Update Prospect | `UpdateProspect` |
| GET | `/dialer/prospects/{prospectId}` | Get Prospect by ID | `GetProspectbyID` |
