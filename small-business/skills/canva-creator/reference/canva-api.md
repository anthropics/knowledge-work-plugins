# Canva Connect API Reference

Base URL: `https://api.canva.com/rest/v1`  
Auth: Bearer token (OAuth 2.0). Scopes needed: `design:content:read`, `design:content:write`, `asset:read`, `asset:write`, `brandtemplate:content:read` (Enterprise only).

---

## Table of contents

1. [Tier requirements](#tier-requirements)
2. [Brand templates (Enterprise)](#brand-templates-enterprise)
3. [Autofill (Enterprise)](#autofill-enterprise)
4. [Design copy (Pro/Teams)](#design-copy-proteams)
5. [Asset upload](#asset-upload)
6. [Export](#export)
7. [Error codes](#error-codes)

---

## Tier requirements

| Feature | Free | Pro | Teams | Enterprise |
|---------|------|-----|-------|------------|
| Create designs | ✓ | ✓ | ✓ | ✓ |
| List own designs | ✓ | ✓ | ✓ | ✓ |
| Brand templates (read) | — | — | — | ✓ |
| Autofill brand templates | — | — | — | ✓ |
| Asset upload (brand kit) | — | — | — | ✓ |
| Asset upload (user) | — | ✓ | ✓ | ✓ |

---

## Brand templates (Enterprise)

**List brand templates:**
```
GET /brand-templates?query={keyword}&ownership=organization
```
Response fields of interest:
- `id` — pass this to autofill
- `title` — human-readable name
- `thumbnail.url` — preview image
- `dataset[].label` — autofill field labels (e.g., "Headline", "ProductName")

Filter by `title` contains the asset type keyword (e.g., "square post", "story", "email header").

---

## Autofill (Enterprise)

Populates a brand template's variable fields and creates a new design:

```
POST /autofills
{
  "brand_template_id": "<template_id>",
  "title": "Summer Sale — Post 1",
  "data": {
    "Headline": { "type": "text", "text": "Summer Sale: 30% off candles" },
    "ProductImage": { "type": "image", "asset_id": "<uploaded_asset_id>" }
  }
}
```

Response: `{ "job": { "id": "<job_id>", "status": "queued" } }`

Poll `GET /autofills/{job_id}` until `status == "success"`. The response
includes `result.design.id` — use this for export.

---

## Design copy (Pro/Teams)

There is no direct "copy template" endpoint for Pro/Teams users. Workflow:

1. `GET /designs?ownership=any&query={template name}` — list designs by name
2. Show top 3 to user; get confirmation
3. `POST /designs` with `asset_type` to create a blank design of the right
   dimensions, then describe what the user needs to update manually in Canva.

Pro/Teams asset generation is semi-manual: Claude creates the design shell and
populates what the API allows; the user applies brand-specific edits in Canva
and returns the design ID for export.

---

## Asset upload

Use when the brief references product photos stored on the user's Desktop or
file system.

**Step 1 — Initialize upload:**
```
POST /asset-uploads
{ "name_base64": "<base64(filename)>", "types": ["image/jpeg"] }
```
Response: `{ "job": { "id": "<job_id>" }, "upload_url": "<presigned_s3_url>" }` 

**Step 2 — Upload file:**
```
PUT <upload_url>
Content-Type: image/jpeg
Body: <raw file bytes>
```

**Step 3 — Poll until ready:**
`GET /asset-uploads/{job_id}` → wait for `status == "success"` → capture `asset.id`.

Maximum file size: 100 MB. Supported types: `image/jpeg`, `image/png`, `image/webp`.

---

## Export

**Why export every design:** the autofill response thumbnail returned at
`design.canva.ai/...` is a short-lived authenticated CDN URL — it expires
within minutes and renders as a broken "Show Image" placeholder if embedded
in a markdown image after expiry. The `POST /exports` output is a
**permanent URL** that's safe to embed in chat previews, attach to HubSpot
posts, and share with the owner.

Always export each design after generation, before showing previews.

```
POST /exports
{
  "design_id": "<design_id>",
  "format": {
    "type": "png",
    "export_quality": "regular",
    "pages": [1]
  }
}
```

Poll `GET /exports/{job_id}` until `status == "success"`. Response includes
`urls[]` — use `urls[0]` as the preview link and HubSpot attachment URL.

**Canva MCP equivalents** (when using Cowork's Canva connector instead of
direct REST):

| Need | MCP tool | Returns |
|------|---------|---------|
| Permanent preview URL | `export-design` | Permanent download URL (safe to embed) |
| Per-page thumbnail (more stable than autofill response, not permanent) | `get-design-thumbnail` | Page thumbnail URL |
| Design metadata only | `get-design` | Title, owner, page count, thumbnail |
| Upload from owner's machine | `upload-asset-from-url` | `asset_id` (one URL per call) |

**Format guidance by channel:**

| Channel | Type | Dimensions |
|---------|------|-----------|
| Instagram feed | `png` | 1080×1080 (square) |
| Instagram story / Reels cover | `png` | 1080×1920 |
| Facebook feed | `png` | 1200×630 |
| Email header | `png` | 600×200 |

---

## Rate limits & generation budgeting

**Hard limit:** 100 requests per minute per token.

**Cost per design:** ~5 API calls — 1 `POST /autofills` + 1 `POST /exports`
+ ~3 polling rounds (`GET /autofills/{job_id}`, `GET /exports/{job_id}`).
Polling cadence should be 3-5 seconds; faster polling burns quota without
speeding up completion.

**Safe ceiling:** ~15-20 designs per minute leaves comfortable headroom
under the 100 req/min cap.

**Recommended pacing (used by Stage 3):**

```
3 candidates per row × 1 row at a time × 30s gap between rows
= 6 designs (~30 API calls) per 30 seconds
= 12 designs / minute, about half the ceiling
```

**Pre-flight budget formula:**

```
total_designs = (Canva-bound rows) × (candidates per row, default 3)
total_api_calls ≈ total_designs × 5
generation_time ≈ (total_designs / 12) minutes
```

**Back-off pattern for `RATE_LIMIT_EXCEEDED`:**

1. First hit in a session → wait 60s, retry that one candidate. Treats
   the error as a transient spike.
2. Second hit in the same session, or any `quota_exceeded` / daily-cap
   error → stop generation and surface progress to the owner. Do not
   retry. The skill asks the owner whether to (a) drop to 1 candidate
   per remaining row, (b) pause and resume in 60 minutes, or (c) stop
   and move to captions with what's already generated.

---

## Error codes

| Code | Meaning | What to do |
|------|---------|-----------|
| `PERMISSION_DENIED` | Scope missing or wrong tier | Check tier; ask user to reconnect Canva with correct scopes |
| `DESIGN_NOT_FOUND` | Wrong design ID | Re-list designs and confirm ID |
| `AUTOFILL_FIELD_NOT_FOUND` | Template field name mismatch | Call `GET /brand-templates/{id}` and re-read `dataset[].label` |
| `RATE_LIMIT_EXCEEDED` | Too many requests | First hit: wait 60s, retry once. Second hit: stop and ask owner (see Rate limits above) |
| `JOB_FAILED` | Async job failed | Check `job.error.message`; common cause is oversized asset |
