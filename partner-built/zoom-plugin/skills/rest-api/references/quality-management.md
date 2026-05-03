# Zoom Quality Management API

Authoritative endpoint inventory for Quality Management. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/quality-management/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 6 |
| Path templates | 5 |
| Tags | 2 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Evaluations | 3 |
| Interactions | 3 |

## Endpoints by Tag

### Evaluations

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/qm/automated_evaluations` | List automated evaluations | `ListAutomatedEvaluations` |
| GET | `/qm/evaluation` | List evaluations | `Listevaluations` |
| GET | `/qm/evaluation/{evaluationId}` | View evaluation detail | `EvaluationDetail` |

### Interactions

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/qm/interactions` | List interactions | `ListInteractions` |
| POST | `/qm/interactions` | Add an interaction | `Addinteraction` |
| GET | `/qm/interactions/{interactionId}` | View interaction detail | `InteractionDetail` |
