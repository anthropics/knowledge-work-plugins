# Zoom Virtual Agent API

Authoritative endpoint inventory for Virtual Agent. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/virtual-agent/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 12 |
| Path templates | 9 |
| Tags | 2 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Knowledge Management | 7 |
| Report | 5 |

## Endpoints by Tag

### Knowledge Management

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/km/kbs/{kbId}/articles` | Get articles | `GetArticles` |
| POST | `/km/kbs/{kbId}/articles` | Create article | `CreateArticle` |
| DELETE | `/km/kbs/{kbId}/articles/{articleId}` | Delete article | `DeleteArticle` |
| GET | `/km/kbs/{kbId}/articles/{articleId}` | Get article | `GetArticle` |
| PUT | `/km/kbs/{kbId}/articles/{articleId}` | Update article | `UpdateArticle` |
| POST | `/km/kbs/{kbId}/sync` | Create sync request | `CreateSyncRequest` |
| GET | `/km/kbs/{kbId}/sync/{syncId}` | Get sync | `GetSync` |

### Report

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/virtual_agent/report/engagements` | Get ZVA engagements | `GetZVAEngagements` |
| GET | `/virtual_agent/report/engagements/query_details` | Get ZVA query details | `GetZVAQueryDetails` |
| GET | `/virtual_agent/report/engagements/variables` | Get ZVA variable details | `GetZVAengagementvariabledetails` |
| GET | `/virtual_agent/report/surveys` | Get ZVA Surveys | `GetZVASurveys` |
| GET | `/virtual_agent/report/transcripts` | Get ZVA transcripts | `GetZVATranscripts` |
