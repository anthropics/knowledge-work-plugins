# Zoom Healthcare API

Authoritative endpoint inventory for Healthcare. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/healthcare/methods/endpoints.json
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
| Path templates | 2 |
| Tags | 1 |

## Tag Index

| Tag | Operations |
|-----|------------|
| clinicalnotes | 3 |

## Endpoints by Tag

### clinicalnotes

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/clinical_notes/notes` | List clinical notes | `GetClinicalNote` |
| GET | `/clinical_notes/notes/{noteId}` | Get a Clinical Note | `GetaClinicalNote` |
| PATCH | `/clinical_notes/notes/{noteId}` | Update a Clinical Note | `UpdateClinicalNote` |
