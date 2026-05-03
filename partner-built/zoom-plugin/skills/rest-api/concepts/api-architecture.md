# API Architecture

Core design patterns for the Zoom REST API — base URLs, regional routing, identifiers, time formats, and request conventions.

## Base URL

All requests use HTTPS with API version `/v2` in the path:

```
https://api.zoom.us/v2/
```

**GraphQL** uses a separate versioned endpoint:

```
https://api.zoom.us/v3/graphql
```

## Regional Base URLs

The OAuth token response includes an `api_url` field indicating the user's data region. Use this for data residency compliance:

```json
{
  "access_token": "eyJ...",
  "api_url": "https://api-eu.zoom.us"
}
```

Construct your regional base URL by appending `/v2/`:

| Region | API URL | Base URL |
|--------|---------|----------|
| Global (default) | `https://api.zoom.us` | `https://api.zoom.us/v2` |
| Australia | `https://api-au.zoom.us` | `https://api-au.zoom.us/v2` |
| Canada | `https://api-ca.zoom.us` | `https://api-ca.zoom.us/v2` |
| European Union | `https://api-eu.zoom.us` | `https://api-eu.zoom.us/v2` |
| India | `https://api-in.zoom.us` | `https://api-in.zoom.us/v2` |
| Saudi Arabia | `https://api-sa.zoom.us` | `https://api-sa.zoom.us/v2` |
| Singapore | `https://api-sg.zoom.us` | `https://api-sg.zoom.us/v2` |
| United Kingdom | `https://api-uk.zoom.us` | `https://api-uk.zoom.us/v2` |
| United States | `https://api-us.zoom.us` | `https://api-us.zoom.us/v2` |
| Vanity account | `https://{vanity}.zoom.us` | `https://{vanity}.zoom.us/v2` |

**Important:** The global URL `https://api.zoom.us` always works regardless of user region. Regional URLs are for compliance, not required.

### Node.js — Dynamic Base URL from Token

```javascript
async function getZoomClient(accountId, clientId, clientSecret) {
  const credentials = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');

  const tokenRes = await fetch('https://zoom.us/oauth/token', {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${credentials}`,
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: `grant_type=account_credentials&account_id=${accountId}`
  });

  const tokenData = await tokenRes.json();
  const baseUrl = tokenData.api_url
    ? `${tokenData.api_url}/v2`
    : 'https://api.zoom.us/v2';

  return {
    accessToken: tokenData.access_token,
    baseUrl,
    async request(method, path, body = null) {
      const res = await fetch(`${this.baseUrl}${path}`, {
        method,
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: body ? JSON.stringify(body) : undefined
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(`Zoom API ${res.status}: ${err.message}`);
      }
      return res.json();
    }
  };
}
```

## The `me` Keyword

The `me` keyword substitutes for `userId` or `accountId` in API paths. Its behavior varies by app type:

| App Type | `me` Behavior | When to Use |
|----------|---------------|-------------|
| **User-level OAuth** | Resolves to the authenticated user | **MUST use** — providing `userId` causes invalid token error |
| **Server-to-Server OAuth** | Not supported | **MUST NOT use** — provide actual `userId` or email |
| **Account-level OAuth** | Resolves to the user who installed the app | Can use either `me` or `userId` |

### Examples

```bash
# User OAuth app — MUST use me
GET /v2/users/me
GET /v2/users/me/meetings

# S2S OAuth app — MUST use actual userId or email
GET /v2/users/abc123def
GET /v2/users/john@example.com
GET /v2/users/john@example.com/meetings
```

### Common Error

Using `userId` with a User-level OAuth token:

```json
{
  "code": 4700,
  "message": "Invalid access token, does not contain scopes."
}
```

**Fix:** Replace the `userId` with `me`.

## Meeting ID vs UUID

- **Meeting ID**: Numeric identifier for the meeting. Reusable for recurring meetings. Expires 30 days after last use.
- **UUID**: Unique identifier for a specific meeting *instance*. Never expires. Generated per occurrence of recurring meetings.

### When to Use Which

| Use Case | Use |
|----------|-----|
| Get a scheduled meeting | Meeting ID |
| Get a past meeting instance | UUID |
| Get recordings for a specific session | UUID |
| Report on a specific occurrence | UUID |

### Double-Encoding UUIDs

UUIDs that begin with `/` or contain `//` **must be double URL-encoded**:

```javascript
function encodeUUID(uuid) {
  // Check if double-encoding is needed
  if (uuid.startsWith('/') || uuid.includes('//')) {
    return encodeURIComponent(encodeURIComponent(uuid));
  }
  return encodeURIComponent(uuid);
}

// UUID: /abcABC123==
// Single encode: %2FabcABC123%3D%3D
// Double encode: %252FabcABC123%253D%253D  ← Required

const meetingUUID = '/abcABC123==';
const url = `https://api.zoom.us/v2/past_meetings/${encodeUUID(meetingUUID)}`;
```

### Python

```python
from urllib.parse import quote

def encode_uuid(uuid_str):
    if uuid_str.startswith('/') or '//' in uuid_str:
        return quote(quote(uuid_str, safe=''), safe='')
    return quote(uuid_str, safe='')

uuid = '/abcABC123=='
url = f'https://api.zoom.us/v2/past_meetings/{encode_uuid(uuid)}'
```

## Time Formats

Zoom API uses ISO 8601 with two variants:

| Format | Meaning | Example |
|--------|---------|---------|
| `yyyy-MM-ddTHH:mm:ssZ` | **UTC time** (Z suffix) | `2025-03-15T10:00:00Z` |
| `yyyy-MM-ddTHH:mm:ss` | **Local time** (no Z, uses `timezone` field) | `2025-03-15T10:00:00` |

### Setting Meeting Time

```json
{
  "topic": "Team Meeting",
  "type": 2,
  "start_time": "2025-03-15T10:00:00",
  "timezone": "America/Los_Angeles",
  "duration": 60
}
```

Or using UTC directly:

```json
{
  "topic": "Team Meeting",
  "type": 2,
  "start_time": "2025-03-15T17:00:00Z",
  "duration": 60
}
```

**Note:** Some Report APIs only accept UTC format. Always check the endpoint reference for the accepted format.

### Date-Only Parameters

Some endpoints (e.g., recordings list) use `YYYY-MM-DD` format:

```bash
GET /v2/users/me/recordings?from=2025-01-01&to=2025-01-31
```

## Download URLs

Recording `download_url` values in API responses and webhook payloads are dynamically generated. They require authentication:

### Authentication Methods

1. **Bearer token in Authorization header** (recommended):
```bash
curl -L -H "Authorization: Bearer ACCESS_TOKEN" \
  "https://zoom.us/rec/archive/download/xyz"
```

2. **`download_access_token`** from webhook payload (for webhook-triggered downloads):
```bash
curl -L -H "Authorization: Bearer DOWNLOAD_ACCESS_TOKEN" \
  "https://zoom.us/rec/archive/download/xyz"
```

### Follow Redirects

Download URLs may return HTTP 301/302 redirects. Always follow redirects:

```javascript
// Node.js — fetch follows redirects by default
const response = await fetch(downloadUrl, {
  headers: { 'Authorization': `Bearer ${accessToken}` },
  redirect: 'follow'
});

const fileBuffer = await response.arrayBuffer();
```

```python
# Python — requests follows redirects by default
import requests

response = requests.get(
    download_url,
    headers={'Authorization': f'Bearer {access_token}'},
    allow_redirects=True,
    stream=True
)

with open('recording.mp4', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

## Personal Meeting ID (PMI)

Users can create meetings with their PMI. The API returns a unique meeting ID in the response, but webhook events still reference the PMI. Use the PMI when passing IDs to API endpoints for PMI-based meetings.

## Shared Access Permissions

Users with Schedule Privilege or role-based access can act on behalf of other users. If your app accesses resources of a user other than the one who installed the app, that user must have authorized shared access permissions.

**Error when shared access is not granted:**

```json
{
  "code": 403,
  "message": "authenticated user has not permitted access to the targeted resource"
}
```

**Resolution:** Direct the user to enable shared access permissions in their Zoom settings. See [Zoom Help Center](https://support.zoom.us/hc/en-us/articles/4413265586189) for the user-facing instructions.

## Email Address Display Rules

External participant emails are only shown if:
- The participant entered their email during registration
- The host provided the email via calendar integration, authentication exception, or breakout room assignment
- A CSV was imported for webinar panelists/attendees

## High API Failure Rates

If your app has a consistently high error-to-request ratio, Zoom may disable it. Build robust error handling and graceful retry logic.

## Request Authentication

All API requests require a Bearer token in the Authorization header:

```
Authorization: Bearer {access_token}
```

> **Full auth implementation:** See [Authentication Flows](authentication-flows.md) or the **[zoom-oauth](../../oauth/SKILL.md)** skill.

## Resources

- **Using Zoom APIs**: https://developers.zoom.us/docs/api/using-zoom-apis/
- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/
