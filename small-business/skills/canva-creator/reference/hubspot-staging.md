# HubSpot Campaign Staging Reference

Requires: **HubSpot Marketing Hub Professional** (or higher).  
Base URL: `https://api.hubapi.com`  
Auth: Bearer token (OAuth 2.0 or private app token).

---

## Table of contents

1. [Tier check](#tier-check)
2. [Create a campaign](#create-a-campaign)
3. [Create a social post](#create-a-social-post)
4. [Verify the scheduled queue](#verify-the-scheduled-queue)
5. [CSV fallback (non-Professional users)](#csv-fallback-non-professional-users)
6. [Field reference](#field-reference)

---

## Tier check

If you're unsure whether the user has Marketing Hub Professional:

```
GET /crm/v3/objects/companies?limit=1
```

Check the `subscriptionType` on the account. If the API returns a 403 on
social endpoints, tell the user: "HubSpot campaign staging requires Marketing
Hub Professional. Your current plan doesn't include it. I can export a
scheduling CSV instead — would that work?"

---

## Create a campaign

```
POST /marketing/v3/campaigns
{
  "name": "Summer Sale 2026 — Social",
  "startDate": "2026-06-01",
  "endDate":   "2026-06-30",
  "currencyCode": "USD",
  "utm": {
    "source": "social",
    "medium": "owned",
    "campaign": "summer-sale-2026"
  }
}
```

Response: `{ "id": "<campaign_id>", ... }` — save this for social post association.

---

## Create a social post

One call per calendar row. Stage as `SCHEDULED`, never `PUBLISHED`.

```
POST /marketing/v3/social/posts
{
  "campaignId": "<campaign_id>",
  "channelId":  "<hubspot_channel_id>",
  "content": {
    "body": "<approved caption text>"
  },
  "scheduledAt": "2026-06-03T10:00:00Z",
  "attachments": [
    {
      "url": "<canva_export_png_url>"
    }
  ],
  "status": "SCHEDULED"
}
```

**`channelId`** — the HubSpot Social account ID (not the platform name).
Retrieve connected accounts:
```
GET /marketing/v3/social/channels
```
Match by `type` (`INSTAGRAM`, `FACEBOOK`, `TWITTER`, `LINKEDIN`) and use the `id` field.

**`scheduledAt`** — must be in the future (relative to the time of the API
call). Use noon local time for the owner's timezone unless they specify
otherwise.

---

## Verify the scheduled queue

After staging all posts:

```
GET /marketing/v3/social/posts?status=SCHEDULED&campaignId=<campaign_id>
```

Surface results in a table: date, channel, first 60 chars of caption, status.
Provide the direct HubSpot campaign URL:
`https://app.hubspot.com/content/{portalId}/social/campaigns/{campaign_id}`

Tell the user: "Posts are scheduled and will publish automatically. You can
cancel or edit any post in HubSpot before the send time."

---

## CSV fallback (non-Professional users)

When HubSpot staging is not available, export a CSV the user can import into
Buffer, Later, or their scheduler of choice.

Column headers:
```
Date,Time,Channel,Caption,ImageURL,Status
```

Example row:
```
2026-06-03,10:00 AM CDT,Instagram,"Summer Sale: 30% off candles ☀️ ...",https://canva.com/export/...,Scheduled
```

Tell the user: "I've prepared a scheduling CSV since your HubSpot plan doesn't
include social staging. You can import this into Buffer or Later. [file path]"

---

## Field reference

| Field | Type | Notes |
|-------|------|-------|
| `campaignId` | string | UUID from campaign creation |
| `channelId` | string | From `GET /social/channels` |
| `content.body` | string | Caption text; max 2,000 chars |
| `scheduledAt` | ISO 8601 | Must be future time; include timezone offset |
| `attachments[].url` | string | Public URL (Canva export URL works) |
| `status` | enum | Always `"SCHEDULED"` — never `"PUBLISHED"` |
