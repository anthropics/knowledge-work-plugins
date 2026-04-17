# Zoom AI Services API

Authoritative endpoint inventory for AI Services / Scribe. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/ai-services/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Product skill: [../../scribe/SKILL.md](../../scribe/SKILL.md)
- Authentication details: [authentication.md](authentication.md)

## Notes

- Current OpenAPI surface is Scribe-focused.
- Auth uses Build-platform JWT, which differs from the standard OAuth-centric paths in most REST API product areas.
- Use this file for endpoint discovery and inventory. Use the `scribe` skill for workflow, webhook, and mode-selection guidance.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 6 |
| Path templates | 4 |
| Tags | 1 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Scribe | 6 |

## Endpoints by Tag

### Scribe

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/aiservices/scribe/jobs` | List Batch Jobs | `listBatchJobs` |
| POST | `/aiservices/scribe/jobs` | Submit Batch Scribe Job | `submitBatchAsr` |
| GET | `/aiservices/scribe/jobs/{jobId}` | Get Batch Job Status | `getBatchJobStatus` |
| DELETE | `/aiservices/scribe/jobs/{jobId}` | Cancel Batch Job | `cancelBatchJob` |
| GET | `/aiservices/scribe/jobs/{jobId}/files` | List Batch Job Files | `listBatchJobFiles` |
| POST | `/aiservices/scribe/transcribe` | Scribe (Synchronous) | `createFastAsr` |
