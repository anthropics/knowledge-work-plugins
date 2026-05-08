# Zoom Cobrowse SDK API

Authoritative endpoint inventory for Cobrowse SDK. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/cobrowse-sdk/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 4 |
| Path templates | 4 |
| Tags | 1 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Sessions | 4 |

## Endpoints by Tag

### Sessions

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/cobrowsesdk/live_sessions` | List live sessions | `Listlivesessions` |
| GET | `/cobrowsesdk/past_sessions` | List past sessions | `Listpastsession` |
| GET | `/cobrowsesdk/sessions/{sessionId}` | Get session details | `Getasession` |
| GET | `/cobrowsesdk/sessions/{sessionId}/users` | List session users | `Listsessionusers` |
