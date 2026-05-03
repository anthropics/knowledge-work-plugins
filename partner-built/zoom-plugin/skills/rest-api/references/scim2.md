# Zoom SCIM2 API

Authoritative endpoint inventory for SCIM2. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/scim2/methods/endpoints.json
- Base URL: `https://api.zoom.us`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 11 |
| Path templates | 4 |
| Tags | 2 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Group | 5 |
| User | 6 |

## Endpoints by Tag

### Group

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/scim2/Groups` | List groups | `groupSCIM2List` |
| POST | `/scim2/Groups` | Create a group | `groupScim2Create` |
| DELETE | `/scim2/Groups/{groupId}` | Delete a group | `groupSCIM2Delete` |
| GET | `/scim2/Groups/{groupId}` | Get a group | `groupSCIM2Get` |
| PATCH | `/scim2/Groups/{groupId}` | Update a group | `groupSCIM2Update` |

### User

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/scim2/Users` | List users | `userSCIM2List` |
| POST | `/scim2/Users` | Create a user | `userScim2Create` |
| DELETE | `/scim2/Users/{userId}` | Delete a user | `userSCIM2Delete` |
| GET | `/scim2/Users/{userId}` | Get a user | `userSCIM2Get` |
| PATCH | `/scim2/Users/{userId}` | Deactivate a user | `userADSCIM2Deactivate` |
| PUT | `/scim2/Users/{userId}` | Update a user | `userSCIM2Update` |
