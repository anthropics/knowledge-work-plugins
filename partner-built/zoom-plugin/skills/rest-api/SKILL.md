---
name: build-zoom-rest-api-app
description: "Reference skill for Zoom REST API. Use after choosing an API-based workflow when you need endpoint selection, resource-management patterns, OAuth requirements, rate-limit awareness, or API error debugging."
triggers:
  - "api call"
  - "rest api"
  - "api create meeting"
  - "api get meeting"
  - "api list meetings"
  - "api update meeting"
  - "api delete meeting"
  - "meeting endpoint"
  - "/v2/meetings"
  - "create user"
  - "zoom api"
  - "api endpoint"
  - "recordings api"
  - "users api"
  - "webinars api"
  - "server-to-server oauth"
  - "account_credentials"
  - "account id"
  - "invalid access token"
  - "does not contain scopes"
  - "access token is expired"
  - "webhook verification"
  - "crc"
  - "download_url"
---

# /build-zoom-rest-api-app

Background reference for deterministic server-side Zoom automation and resource management. Prefer `plan-zoom-product`, `plan-zoom-integration`, or `debug-zoom` first, then route here for endpoint-level detail.

# Zoom REST API

Expert guidance for building server-side integrations with the Zoom REST API. This API provides 600+ endpoints for managing meetings, users, webinars, recordings, reports, and all Zoom platform resources programmatically.

**Official Documentation**: https://developers.zoom.us/api-hub/
**API Hub Reference**: https://developers.zoom.us/api-hub/meetings/
**OpenAPI Inventories**: `https://developers.zoom.us/api-hub/<domain>/methods/endpoints.json`

## Quick Links

**New to Zoom REST API? Follow this path:**

1. **[API Architecture](concepts/api-architecture.md)** - Base URLs, regional URLs, `me` keyword, ID vs UUID, time formats
2. **[Authentication Flows](concepts/authentication-flows.md)** - OAuth setup (S2S, User, PKCE, Device Code)
3. **[Meeting URLs vs Meeting SDK](concepts/meeting-urls-and-sdk-joining.md)** - Stop mixing `join_url` with Meeting SDK
3. **[Meeting Lifecycle](examples/meeting-lifecycle.md)** - Create → Update → Start → End → Delete with webhooks
4. **[Rate Limiting Strategy](concepts/rate-limiting-strategy.md)** - Plan tiers, per-user limits, retry patterns

**Reference:**
- **[Meetings](references/meetings.md)** - Meeting CRUD, types, settings
- **[Users](references/users.md)** - User provisioning and management
- **[Recordings](references/recordings.md)** - Cloud recording access and download
- **[AI Services](references/ai-services.md)** - Scribe endpoint inventory and current AI Services path surface
- **[GraphQL Queries](examples/graphql-queries.md)** - Alternative query API (beta)
- **Integrated Index** - see the section below in this file

Most domain files under `references/` are aligned to the official API Hub `endpoints.json` inventories. Treat those files as the local source of truth for method/path discovery.

**Having issues?**
- Start with preflight checks → [5-Minute Runbook](RUNBOOK.md)
- 401 Unauthorized → [Authentication Flows](concepts/authentication-flows.md) (check token expiry, scopes)
- 429 Too Many Requests → [Rate Limiting Strategy](concepts/rate-limiting-strategy.md)
- Error codes → [Common Errors](troubleshooting/common-errors.md)
- Pagination confusion → [Common Issues](troubleshooting/common-issues.md)
- Webhooks not arriving → [Webhook Server](examples/webhook-server.md)
- Forum-derived FAQs → [Forum Top Questions](troubleshooting/forum-top-questions.md)
- Token/scope failures → [Token + Scope Playbook](troubleshooting/token-scope-playbook.md)

**Building event-driven integrations?**
- [Webhook Server](examples/webhook-server.md) - Express.js server with CRC validation
- [Recording Pipeline](examples/recording-pipeline.md) - Auto-download via webhook events

## Quick Start

### Get an Access Token (Server-to-Server OAuth)

```bash
curl -X POST "https://zoom.us/oauth/token" \
  -H "Authorization: Basic $(echo -n 'CLIENT_ID:CLIENT_SECRET' | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=account_credentials&account_id=ACCOUNT_ID"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "meeting:read meeting:write user:read"
}
```

### Create a Meeting

```bash
curl -X POST "https://api.zoom.us/v2/users/HOST_USER_ID/meetings" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Team Standup",
    "type": 2,
    "start_time": "2025-03-15T10:00:00Z",
    "duration": 30,
    "settings": {
      "join_before_host": false,
      "waiting_room": true
    }
  }'
```

For S2S OAuth, use an explicit host user ID or email in the path. Do not use `me`.

### List Users with Pagination

```bash
curl "https://api.zoom.us/v2/users?page_size=300&status=active" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

## Base URL

```
https://api.zoom.us/v2
```

### Regional Base URLs

The `api_url` field in OAuth token responses indicates the user's region. Use regional URLs for data residency compliance:

| Region | URL |
|--------|-----|
| Global (default) | `https://api.zoom.us/v2` |
| Australia | `https://api-au.zoom.us/v2` |
| Canada | `https://api-ca.zoom.us/v2` |
| European Union | `https://api-eu.zoom.us/v2` |
| India | `https://api-in.zoom.us/v2` |
| Saudi Arabia | `https://api-sa.zoom.us/v2` |
| Singapore | `https://api-sg.zoom.us/v2` |
| United Kingdom | `https://api-uk.zoom.us/v2` |
| United States | `https://api-us.zoom.us/v2` |

**Note:** You can always use the global URL `https://api.zoom.us` regardless of the `api_url` value.

## Key Features

| Feature | Description |
|---------|-------------|
| **Meeting Management** | Create, read, update, delete meetings with full scheduling control |
| **User Provisioning** | Automated user lifecycle (create, update, deactivate, delete) |
| **Webinar Operations** | Webinar CRUD, registrant management, panelist control |
| **Cloud Recordings** | List, download, delete recordings with file-type filtering |
| **Reports & Analytics** | Usage reports, participant data, daily statistics |
| **Team Chat** | Channel management, messaging, chatbot integration |
| **Zoom Phone** | Call management, voicemail, call routing |
| **Zoom Rooms** | Room management, device control, scheduling |
| **Webhooks** | Real-time event notifications for 100+ event types |
| **WebSockets** | Persistent event streaming without public endpoints |
| **GraphQL (Beta)** | Single-endpoint flexible queries at `v3/graphql` |
| **AI Companion** | Meeting summaries, transcripts, AI-generated content |
| **AI Services / Scribe** | File and archive transcription via Build-platform JWT-authenticated endpoints |

## Prerequisites

- Zoom account (Free tier has API access with lower rate limits)
- App registered on [Zoom App Marketplace](https://marketplace.zoom.us/)
- OAuth credentials (Server-to-Server OAuth or User OAuth)
- Appropriate scopes for target endpoints

> **Need help with authentication?** See the **[zoom-oauth](../oauth/SKILL.md)** skill for complete OAuth flow implementation.

## Critical Gotchas and Best Practices

### ⚠️ JWT App Type is Deprecated

The JWT app type is deprecated. Migrate to **Server-to-Server OAuth**. This does NOT affect JWT token signatures used in Video SDK — only the Marketplace "JWT" app type for REST API access.

```javascript
// OLD (JWT app type - DEPRECATED)
const token = jwt.sign({ iss: apiKey, exp: expiry }, apiSecret);

// NEW (Server-to-Server OAuth)
const token = await getServerToServerToken(accountId, clientId, clientSecret);
```

### ⚠️ The `me` Keyword Rules

- **User-level OAuth apps**: MUST use `me` instead of `userId` (otherwise: invalid token error)
- **Server-to-Server OAuth apps**: MUST NOT use `me` — provide the actual `userId` or email
- **Account-level OAuth apps**: Can use either `me` or `userId`

### ⚠️ Meeting ID vs UUID — Double Encoding

UUIDs that begin with `/` or contain `//` must be **double URL-encoded**:

```javascript
// UUID: /abc==
// Single encode: %2Fabc%3D%3D
// Double encode: %252Fabc%253D%253D  ← USE THIS

const uuid = '/abc==';
const encoded = encodeURIComponent(encodeURIComponent(uuid));
const url = `https://api.zoom.us/v2/meetings/${encoded}`;
```

### ⚠️ Time Formats

- `yyyy-MM-ddTHH:mm:ssZ` — **UTC time** (note the `Z` suffix)
- `yyyy-MM-ddTHH:mm:ss` — **Local time** (no `Z`, uses `timezone` field)
- Some report APIs only accept UTC. Check the API reference for each endpoint.

### ⚠️ Rate Limits Are Per-Account, Not Per-App

All apps on the same Zoom account **share** rate limits. One heavy app can impact others. Monitor `X-RateLimit-Remaining` headers proactively.

### ⚠️ Per-User Daily Limits

Meeting/Webinar create/update operations are limited to **100 per day per user** (resets at 00:00 UTC). Distribute operations across different host users when doing bulk operations.

### ⚠️ Download URLs Require Auth and Follow Redirects

Recording `download_url` values require Bearer token authentication and may redirect. Always follow redirects:

```bash
curl -L -H "Authorization: Bearer ACCESS_TOKEN" "https://zoom.us/rec/download/..."
```

### Use Webhooks Instead of Polling

```javascript
// DON'T: Poll every minute (wastes API quota)
setInterval(() => getMeetings(), 60000);

// DO: Receive webhook events in real-time
app.post('/webhook', (req, res) => {
  if (req.body.event === 'meeting.started') {
    handleMeetingStarted(req.body.payload);
  }
  res.status(200).send();
});
```

> **Webhook setup details:** See the **[zoom-webhooks](../webhooks/SKILL.md)** skill for comprehensive webhook implementation.

## Complete Documentation Library

This skill includes comprehensive guides organized by category:

### Core Concepts
- **[API Architecture](concepts/api-architecture.md)** - REST design, base URLs, regional routing, `me` keyword, ID vs UUID, time formats
- **[Authentication Flows](concepts/authentication-flows.md)** - All OAuth flows (S2S, User, PKCE, Device Code)
- **[Rate Limiting Strategy](concepts/rate-limiting-strategy.md)** - Limits by plan, retry patterns, request queuing

### Complete Examples
- **[Meeting Lifecycle](examples/meeting-lifecycle.md)** - Full Create → Update → Start → End → Delete flow with webhook events
- **[User Management](examples/user-management.md)** - CRUD users, list with pagination, bulk operations
- **[Recording Pipeline](examples/recording-pipeline.md)** - Download recordings via webhooks + API
- **[Webhook Server](examples/webhook-server.md)** - Express.js server with CRC validation and signature verification
- **[GraphQL Queries](examples/graphql-queries.md)** - GraphQL queries, mutations, cursor pagination

### Troubleshooting
- **[Common Errors](troubleshooting/common-errors.md)** - HTTP status codes, Zoom error codes, error response formats
- **[Common Issues](troubleshooting/common-issues.md)** - Rate limits, token refresh, pagination pitfalls, gotchas

### References (39 files covering all Zoom API domains)

#### Core APIs
- **[references/meetings.md](references/meetings.md)** - Meeting CRUD, types, settings
- **[references/users.md](references/users.md)** - User provisioning, types, scopes
- **[references/webinars.md](references/webinars.md)** - Webinar management, registrants
- **[references/recordings.md](references/recordings.md)** - Cloud recording access
- **[references/reports.md](references/reports.md)** - Usage reports, analytics
- **[references/accounts.md](references/accounts.md)** - Account management

#### Communication
- **[references/team-chat.md](references/team-chat.md)** - Team Chat messaging
- **[references/chatbot.md](references/chatbot.md)** - Interactive chatbots
- **[references/phone.md](references/phone.md)** - Zoom Phone
- **[references/mail.md](references/mail.md)** - Zoom Mail
- **[references/calendar.md](references/calendar.md)** - Zoom Calendar

#### Infrastructure
- **[references/rooms.md](references/rooms.md)** - Zoom Rooms
- **[references/scim2.md](references/scim2.md)** - SCIM 2.0 provisioning APIs
- **[references/rate-limits.md](references/rate-limits.md)** - Rate limit details
- **[references/qss.md](references/qss.md)** - Quality of Service Subscription

#### Advanced
- **[references/graphql.md](references/graphql.md)** - GraphQL API (beta)
- **[references/ai-companion.md](references/ai-companion.md)** - AI features
- **[references/authentication.md](references/authentication.md)** - Auth reference
- **[references/openapi.md](references/openapi.md)** - OpenAPI specs, Postman, code generation

#### Additional API Domains
- **[references/events.md](references/events.md)** - Events and event platform APIs
- **[references/scheduler.md](references/scheduler.md)** - Zoom Scheduler APIs
- **[references/tasks.md](references/tasks.md)** - Tasks APIs
- **[references/whiteboard.md](references/whiteboard.md)** - Whiteboard APIs
- **[references/video-management.md](references/video-management.md)** - Video management APIs
- **[references/video-sdk-api.md](references/video-sdk-api.md)** - Video SDK REST APIs
- **[references/marketplace-apps.md](references/marketplace-apps.md)** - Marketplace app management
- **[references/commerce.md](references/commerce.md)** - Commerce and billing APIs
- **[references/contact-center.md](references/contact-center.md)** - Contact Center APIs
- **[references/quality-management.md](references/quality-management.md)** - Quality management APIs
- **[references/workforce-management.md](references/workforce-management.md)** - Workforce management APIs
- **[references/healthcare.md](references/healthcare.md)** - Healthcare APIs
- **[references/auto-dialer.md](references/auto-dialer.md)** - Auto dialer APIs
- **[references/number-management.md](references/number-management.md)** - Number management APIs
- **[references/revenue-accelerator.md](references/revenue-accelerator.md)** - Revenue Accelerator APIs
- **[references/virtual-agent.md](references/virtual-agent.md)** - Virtual Agent APIs
- **[references/cobrowse-sdk-api.md](references/cobrowse-sdk-api.md)** - Cobrowse SDK APIs
- **[references/crc.md](references/crc.md)** - Cloud Room Connector APIs
- **[references/clips.md](references/clips.md)** - Clips APIs
- **[references/zoom-docs.md](references/zoom-docs.md)** - Zoom docs and source references

## Sample Repositories

### Official (by Zoom)

| Type | Repository |
|------|------------|
| OAuth Sample | [oauth-sample-app](https://github.com/zoom/oauth-sample-app) |
| S2S OAuth Starter | [server-to-server-oauth-starter-api](https://github.com/zoom/server-to-server-oauth-starter-api) |
| User OAuth | [user-level-oauth-starter](https://github.com/zoom/user-level-oauth-starter) |
| S2S Token | [server-to-server-oauth-token](https://github.com/zoom/server-to-server-oauth-token) |
| Rivet Library | [rivet-javascript](https://github.com/zoom/rivet-javascript) |
| WebSocket Sample | [websocket-js-sample](https://github.com/zoom/websocket-js-sample) |
| Webhook Sample | [webhook-sample-node.js](https://github.com/zoom/webhook-sample-node.js) |
| Python S2S | [server-to-server-python-sample](https://github.com/zoom/server-to-server-python-sample) |

## Resources

- **API Reference**: https://developers.zoom.us/api-hub/
- **GraphQL Playground**: https://nws.zoom.us/graphql/playground
- **Postman Collection**: https://marketplace.zoom.us/docs/api-reference/postman
- **Developer Forum**: https://devforum.zoom.us/
- **Changelog**: https://developers.zoom.us/changelog/
- **Status Page**: https://status.zoom.us/

---

**Need help?** Start with Integrated Index section below for complete navigation.

---

## Integrated Index

_This section was migrated from `SKILL.md`._

## Quick Start Path

**If you're new to the Zoom REST API, follow this order:**

1. **Run preflight checks first** → [RUNBOOK.md](RUNBOOK.md)

2. **Understand the API design** → [concepts/api-architecture.md](concepts/api-architecture.md)
   - Base URLs, regional endpoints, `me` keyword rules
   - Meeting ID vs UUID, double-encoding, time formats

3. **Set up authentication** → [concepts/authentication-flows.md](concepts/authentication-flows.md)
   - Server-to-Server OAuth (backend automation)
   - User OAuth with PKCE (user-facing apps)
   - Cross-reference: [zoom-oauth](../oauth/SKILL.md)

4. **Create your first meeting** → [examples/meeting-lifecycle.md](examples/meeting-lifecycle.md)
   - Full CRUD with curl and Node.js examples
   - Webhook event integration

5. **Handle rate limits** → [concepts/rate-limiting-strategy.md](concepts/rate-limiting-strategy.md)
   - Plan-based limits, retry patterns, request queuing

6. **Set up webhooks** → [examples/webhook-server.md](examples/webhook-server.md)
   - CRC validation, signature verification, event handling

7. **Troubleshoot issues** → [troubleshooting/common-issues.md](troubleshooting/common-issues.md)
   - Token refresh, pagination pitfalls, common gotchas

---

## Documentation Structure

```
rest-api/
├── SKILL.md                              # Main skill overview + quick start
├── SKILL.md                              # This file - navigation guide
│
├── concepts/                             # Core architectural concepts
│   ├── api-architecture.md              # REST design, URLs, IDs, time formats
│   ├── authentication-flows.md          # OAuth flows (S2S, User, PKCE, Device)
│   └── rate-limiting-strategy.md        # Limits by plan, retry, queuing
│
├── examples/                             # Complete working code
│   ├── meeting-lifecycle.md             # Create→Update→Start→End→Delete
│   ├── user-management.md              # CRUD users, pagination, bulk ops
│   ├── recording-pipeline.md           # Download recordings via webhooks
│   ├── webhook-server.md               # Express.js CRC + signature verification
│   └── graphql-queries.md              # GraphQL queries, mutations, pagination
│
├── troubleshooting/                      # Problem solving
│   ├── common-errors.md                # HTTP codes, Zoom error codes table
│   └── common-issues.md               # Rate limits, tokens, pagination pitfalls
│
└── references/                           # 39 domain-specific reference files
    ├── authentication.md                # Auth methods reference
    ├── meetings.md                      # Meeting endpoints
    ├── users.md                         # User management endpoints
    ├── webinars.md                      # Webinar endpoints
    ├── recordings.md                    # Cloud recording endpoints
    ├── reports.md                       # Reports & analytics
    ├── accounts.md                      # Account management
    ├── rate-limits.md                   # Rate limit details
    ├── graphql.md                       # GraphQL API (beta)
    ├── zoom-team-chat.md                     # Team Chat messaging
    ├── chatbot.md                       # Chatbot integration
    ├── phone.md                         # Zoom Phone
    ├── rooms.md                         # Zoom Rooms
    ├── calendar.md                      # Zoom Calendar
    ├── mail.md                          # Zoom Mail
    ├── ai-companion.md                  # AI features
    ├── openapi.md                       # OpenAPI specs
    ├── qss.md                           # Quality of Service
    ├── contact-center.md                # Contact Center
    ├── events.md                        # Zoom Events
    ├── whiteboard.md                    # Whiteboard
    ├── clips.md                         # Zoom Clips
    ├── scheduler.md                     # Scheduler
    ├── scim2.md                         # SCIM 2.0
    ├── marketplace-apps.md              # App management
    ├── zoom-video-sdk-api.md                 # Video SDK REST
    └── ... (39 total files)
```

---

## By Use Case

### I want to create and manage meetings
1. [API Architecture](concepts/api-architecture.md) - Base URL, time formats
2. [Meeting Lifecycle](examples/meeting-lifecycle.md) - Full CRUD + webhook events
3. [Meetings Reference](references/meetings.md) - All endpoints, types, settings

### I want to manage users programmatically
1. [User Management](examples/user-management.md) - CRUD, pagination, bulk ops
2. [Users Reference](references/users.md) - Endpoints, user types, scopes

### I want to download recordings automatically
1. [Recording Pipeline](examples/recording-pipeline.md) - Webhook-triggered downloads
2. [Recordings Reference](references/recordings.md) - File types, download auth

### I want to receive real-time events
1. [Webhook Server](examples/webhook-server.md) - CRC validation, signature check
2. Cross-reference: [zoom-webhooks](../webhooks/SKILL.md) for comprehensive webhook docs
3. Cross-reference: [zoom-websockets](../websockets/SKILL.md) for WebSocket events

### I want to use GraphQL instead of REST
1. [GraphQL Queries](examples/graphql-queries.md) - Queries, mutations, pagination
2. [GraphQL Reference](references/graphql.md) - Available entities, scopes, rate limits

### I want to set up authentication
1. [Authentication Flows](concepts/authentication-flows.md) - All OAuth methods
2. Cross-reference: [zoom-oauth](../oauth/SKILL.md) for full OAuth implementation

### I'm hitting rate limits
1. [Rate Limiting Strategy](concepts/rate-limiting-strategy.md) - Limits by plan, strategies
2. [Rate Limits Reference](references/rate-limits.md) - Detailed tables
3. [Common Issues](troubleshooting/common-issues.md) - Practical solutions

### I'm getting errors
1. [Common Errors](troubleshooting/common-errors.md) - Error code tables
2. [Common Issues](troubleshooting/common-issues.md) - Diagnostic workflow

### I want to build webinars
1. [Webinars Reference](references/webinars.md) - Endpoints, types, registrants
2. [Meeting Lifecycle](examples/meeting-lifecycle.md) - Similar patterns apply

### I want to integrate Zoom Phone
1. [Phone Reference](references/phone.md) - Phone API endpoints
2. [Rate Limiting Strategy](concepts/rate-limiting-strategy.md) - Separate Phone rate limits

---

## Most Critical Documents

### 1. API Architecture (FOUNDATION)
**[concepts/api-architecture.md](concepts/api-architecture.md)**

Essential knowledge before making any API call:
- Base URLs and regional endpoints
- The `me` keyword rules (different per app type!)
- Meeting ID vs UUID double-encoding
- ISO 8601 time formats (UTC vs local)
- Download URL authentication

### 2. Rate Limiting Strategy (MOST COMMON PRODUCTION ISSUE)
**[concepts/rate-limiting-strategy.md](concepts/rate-limiting-strategy.md)**

Rate limits are per-account, shared across all apps:
- Free: 4/sec Light, 2/sec Medium, 1/sec Heavy
- Pro: 30/sec Light, 20/sec Medium, 10/sec Heavy
- Business+: 80/sec Light, 60/sec Medium, 40/sec Heavy
- Per-user: 100 meeting create/update per day

### 3. Meeting Lifecycle (MOST COMMON TASK)
**[examples/meeting-lifecycle.md](examples/meeting-lifecycle.md)**

Complete CRUD with webhook integration — the pattern most developers need first.

---

## Key Learnings

### Critical Discoveries:

1. **JWT app type is deprecated** — use Server-to-Server OAuth
   - The JWT *app type* on Marketplace is deprecated, NOT JWT token signatures
   - See: [Authentication Flows](concepts/authentication-flows.md)

2. **`me` keyword behaves differently by app type**
   - User OAuth: MUST use `me`
   - S2S OAuth: MUST NOT use `me`
   - See: [API Architecture](concepts/api-architecture.md)

3. **Rate limiting is nuanced (don’t assume a single global rule)**
   - Limits can vary by endpoint and may be enforced at account/app/user levels
   - Treat quotas as potentially shared across your account and implement backoff
   - Monitor rate limit response headers (for example `X-RateLimit-Remaining`)
   - See: [Rate Limiting Strategy](concepts/rate-limiting-strategy.md)

4. **100 meeting creates per user per day**
   - This is a hard per-user limit, not related to rate limits
   - Distribute across host users for bulk operations
   - See: [Rate Limiting Strategy](concepts/rate-limiting-strategy.md)

5. **UUID double-encoding is required for certain UUIDs**
   - UUIDs starting with `/` or containing `//` must be double-encoded
   - See: [API Architecture](concepts/api-architecture.md)

6. **Pagination: use `next_page_token`, not `page_number`**
   - `page_number` is legacy and being phased out
   - `next_page_token` is the recommended approach
   - See: [Common Issues](troubleshooting/common-issues.md)

7. **GraphQL is at `/v3/graphql`, not `/v2/`**
   - Single endpoint, cursor-based pagination
   - Rate limits apply per-field (each field = one REST equivalent)
   - See: [GraphQL Queries](examples/graphql-queries.md)

---

## Quick Reference

### "401 Unauthorized"
→ [Authentication Flows](concepts/authentication-flows.md) - Token expired or wrong scopes

### "429 Too Many Requests"
→ [Rate Limiting Strategy](concepts/rate-limiting-strategy.md) - Check headers for reset time

### "Invalid token" when using userId
→ [API Architecture](concepts/api-architecture.md) - User OAuth apps must use `me`

### "How do I paginate results?"
→ [Common Issues](troubleshooting/common-issues.md) - Use `next_page_token`

### "Webhooks not arriving"
→ [Webhook Server](examples/webhook-server.md) - CRC validation required

### "Recording download fails"
→ [Recording Pipeline](examples/recording-pipeline.md) - Bearer auth + follow redirects

### "How do I create a meeting?"
→ [Meeting Lifecycle](examples/meeting-lifecycle.md) - Full working examples

---

## Related Skills

| Skill | Use When |
|-------|----------|
| **[zoom-oauth](../oauth/SKILL.md)** | Implementing OAuth flows, token management |
| **[zoom-webhooks](../webhooks/SKILL.md)** | Deep webhook implementation, event catalog |
| **[zoom-websockets](../websockets/SKILL.md)** | WebSocket event streaming |
| **[zoom-general](../general/SKILL.md)** | Cross-product patterns, community repos |

---

**Based on Zoom REST API v2 (current) and GraphQL v3 (beta)**

## Environment Variables

- See [references/environment-variables.md](references/environment-variables.md) for standardized `.env` keys and where to find each value.
