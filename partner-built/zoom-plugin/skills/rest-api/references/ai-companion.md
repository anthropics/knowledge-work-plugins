# Zoom AI Companion API

Authoritative endpoint inventory for AI Companion. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/ai-companion/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 1 |
| Path templates | 1 |
| Tags | 1 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Archive | 1 |

## Endpoints by Tag

### Archive

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/aic/users/{userId}/conversation_archive` | Get AI Companion conversation archives | `GetAICconversationarchives` |
