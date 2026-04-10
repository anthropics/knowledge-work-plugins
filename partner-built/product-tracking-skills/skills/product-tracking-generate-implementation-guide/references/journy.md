<!-- Last verified: 2026-03-10 against Journy.io docs -->
# Journy Implementation Reference

## Overview

Journy.io is a B2B customer journey orchestration platform focused on account-level engagement and lifecycle management. It ingests user and account data via its API to build account health profiles, trigger playbooks, and drive customer success workflows. Journy is account-centric — the account (company) is the primary entity, and users are tracked within the context of accounts. Cloud-only, proprietary SaaS.

**Forge-approved domain:** `*.journy.io`

## SDK Options / API

| Environment | Integration | Install |
|---|---|---|
| Browser | JavaScript snippet | No install — generated via dashboard/API with CNAME |
| Node.js | `@journyio/sdk` | `npm install @journyio/sdk` |
| PHP | `journy-io/sdk` | `composer require journy-io/sdk` |
| Python | `journyio-sdk` | `pip install journyio-sdk` |
| HTTP API | REST API | No SDK — raw `fetch()` calls |

Journy provides a JavaScript snippet for browser-side tracking (generated per-domain with a CNAME-based tracking URL), server-side SDKs for Node.js, PHP, and Python, and a REST API usable from any environment.

## Initialization

### Browser (JavaScript Snippet)

The browser tracking snippet is **not a static code block** — it is generated per-domain via the Journy dashboard (or the `getTrackingSnippet` SDK method). When connecting a website, you create a CNAME record pointing to `analyze.journy.io` (e.g., `go.example.com CNAME analyze.journy.io`), and Journy generates a snippet that references your custom tracking URL. The snippet sets a `__journey` cookie to link web activity to users.

Retrieve the snippet programmatically via the Node.js SDK:

```typescript
const result = await client.getTrackingSnippet({
  domain: 'www.example.com',
});

if (result.success) {
  // result.data contains the snippet HTML and domain info
  console.log(result.data);
}
```

Then embed the returned snippet in your HTML. Journy recommends using the snippet for page/screen view tracking and the backend API for syncing users, accounts, and tracking events.

### Node.js

```typescript
import { Client } from '@journyio/sdk';

const client = Client.withDefaults(process.env.JOURNY_API_KEY!);
```

For custom HTTP client implementations:

```typescript
import { Client } from '@journyio/sdk';

const http = new CustomHttpClient();
const client = new Client(http, { apiKey: process.env.JOURNY_API_KEY! });
```

### HTTP API

```
Base URL: https://api.journy.io
X-Api-Key: YOUR_API_KEY
Content-Type: application/json
```

All API calls require the `X-Api-Key` header for authentication. All requests must be made over HTTPS. The API key is found in the Journy dashboard under the Connections tab.

## Core Methods

### identify()

Identifies a user and sets user-level properties. In Journy's model, users exist within the context of accounts.

**Browser:**
```javascript
journy.identify({
  userId: 'usr_123',
  email: 'jane@example.com',
  properties: {
    first_name: 'Jane',
    last_name: 'Doe',
    role: 'admin',
    registered_at: '2024-01-15T00:00:00Z',
  },
});
```

**Node.js:**
```typescript
await client.upsertUser({
  userId: 'usr_123',
  email: 'jane@example.com',
  properties: {
    first_name: 'Jane',
    last_name: 'Doe',
    role: 'admin',
    registered_at: new Date('2024-01-15'),
  },
});
```

**HTTP API:**
```json
POST /users/upsert
{
  "identification": {
    "userId": "usr_123",
    "email": "jane@example.com"
  },
  "properties": {
    "first_name": "Jane",
    "last_name": "Doe",
    "role": "admin",
    "registered_at": "2024-01-15T00:00:00Z"
  }
}
```

**When to call:** On login, signup, or when user traits change.

### group() / Account Tracking

Account tracking is central to Journy's model. Accounts are the primary entity for health scoring, playbooks, and lifecycle stages. Journy uses the term "account" rather than "group."

**Browser:**
```javascript
journy.account({
  accountId: 'acc_456',
  domain: 'acme.com',
  properties: {
    name: 'Acme Corp',
    plan: 'enterprise',
    mrr: 5000,
    industry: 'technology',
    employee_count: 150,
    registered_at: '2023-06-01T00:00:00Z',
  },
});
```

**Node.js:**
```typescript
await client.upsertAccount({
  accountId: 'acc_456',
  domain: 'acme.com',
  properties: {
    name: 'Acme Corp',
    plan: 'enterprise',
    mrr: 5000,
    industry: 'technology',
    employee_count: 150,
    registered_at: new Date('2023-06-01'),
  },
});
```

**HTTP API:**
```json
POST /accounts/upsert
{
  "identification": {
    "accountId": "acc_456",
    "domain": "acme.com"
  },
  "properties": {
    "name": "Acme Corp",
    "plan": "enterprise",
    "mrr": 5000,
    "industry": "technology",
    "employee_count": 150,
    "registered_at": "2023-06-01T00:00:00Z"
  }
}
```

**Linking users to accounts:** Users must be explicitly associated with accounts. This is a separate call:

**Node.js:**
```typescript
await client.addUsersToAccount({
  account: { accountId: 'acc_456' },
  users: [
    { identification: { userId: 'usr_123' } },
    { identification: { userId: 'usr_456' } },
  ],
});
```

**HTTP API:**
```json
POST /accounts/users/add
{
  "account": {
    "accountId": "acc_456"
  },
  "users": [
    { "identification": { "userId": "usr_123" } },
    { "identification": { "userId": "usr_456" } }
  ]
}
```

Up to 100 users can be added per call.

**Browser:** The browser snippet typically links users to accounts implicitly when both `identify()` and `account()` are called in the same session, or via an explicit parameter:

```javascript
journy.identify({
  userId: 'usr_123',
  accountId: 'acc_456',
  email: 'jane@example.com',
  properties: {
    role: 'admin',
  },
});
```

### track()

Records a custom event. Events in Journy are used to trigger playbooks, calculate health scores, and track engagement.

**Browser:**
```javascript
journy.track('report_created', {
  userId: 'usr_123',
  accountId: 'acc_456',
  properties: {
    report_id: 'rpt_789',
    report_type: 'standard',
  },
});
```

Alternatively, using the `addEvent` method:

```javascript
journy.addEvent({
  name: 'report_created',
  userId: 'usr_123',
  accountId: 'acc_456',
  metadata: {
    report_id: 'rpt_789',
    report_type: 'standard',
  },
});
```

**Node.js:**
```typescript
await client.addEvent({
  name: 'report_created',
  user: { userId: 'usr_123' },
  account: { accountId: 'acc_456' },
  metadata: {
    report_id: 'rpt_789',
    report_type: 'standard',
  },
});
```

**HTTP API:**
```json
POST /track
{
  "name": "report_created",
  "identification": {
    "userId": "usr_123",
    "accountId": "acc_456"
  },
  "metadata": {
    "report_id": "rpt_789",
    "report_type": "standard"
  }
}
```

> **Deprecation notice:** `POST /events` is deprecated and will be removed in the future. Use `POST /track` for all new implementations.

**When to call:** After the action succeeds. Include both `userId` and `accountId` to ensure correct attribution.

## Group Context on Track Calls

Journy requires explicit account context on every event. Unlike tools where `group()` sets a sticky context for subsequent `track()` calls, Journy's event model expects `accountId` to be passed on each event.

```typescript
// Every track call should include the accountId
await client.addEvent({
  name: 'task_completed',
  user: { userId: 'usr_123' },
  account: { accountId: 'acc_456' },
  metadata: { task_id: 'task_456' },
});
```

**For products with hierarchical groups:** Journy does not natively support multi-level group hierarchies (account > workspace > project). The platform operates at the account level. If your product has sub-account structures, attribute events to the top-level account and use event metadata to carry sub-group identifiers:

```typescript
await client.addEvent({
  name: 'task_completed',
  user: { userId: 'usr_123' },
  account: { accountId: 'acc_456' },
  metadata: {
    task_id: 'task_456',
    workspace_id: 'ws_789',
    project_id: 'proj_123',
  },
});
```

## Account Traits That Matter

Journy's health scoring and playbook engine relies on account properties. Keep these up to date:

| Trait | Why | Type |
|---|---|---|
| `name` | Account identification in dashboards | string |
| `domain` | Company matching and enrichment (also an identification field) | string |
| `registered_at` | Cohort analysis, onboarding tracking | Date / ISO 8601 |
| `plan` | Plan-based segmentation and triggers | string |
| `mrr` | Revenue-weighted health scoring | number |
| `is_paying` | Payment status segmentation | boolean |
| `industry` | Segmentation | string |
| `employee_count` | Size-based segmentation | number |
| `status` | Lifecycle stage (trial, active, churned) | string |

Call the account upsert whenever these traits change — not just on first creation. Stale traits degrade health score accuracy and trigger wrong playbooks.

## Required Fields

| Method | Required Fields | Notes |
|---|---|---|
| User upsert | `userId` or `email` | Both recommended for reliable matching |
| Account upsert | `accountId` or `domain` | Both recommended; `name` strongly recommended |
| Track event | `name`, `userId` or `accountId` | Both `userId` and `accountId` recommended |
| Link user to account | `account`, `users` array | Each user needs `identification` with `userId` or `email`; max 100 users per call |

## Limits

| Constraint | Value |
|---|---|
| Event metadata properties | Keep payloads concise; strings, numbers, booleans, dates |
| Property value types | Strings, numbers, booleans, dates, arrays, null (to delete) |
| API rate limit | 1,800 requests per minute |
| Rate limit headers | `X-RateLimit-Limit`, `X-RateLimit-Remaining` |
| Users per add/remove call | 100 max |
| Batch API | Not publicly documented |

**Note:** Rate limit information is from the OpenAPI spec. The `X-RateLimit-Remaining` response header lets you monitor usage. Contact Journy support for higher-volume needs.

## Common Pitfalls

1. **Forgetting to link users to accounts** — In Journy, calling `identify()` and `account()` separately does not automatically associate the user with that account. You must explicitly link users to accounts, either by passing `accountId` in the identify call (browser) or by calling `addUsersToAccount()` (Node.js/API). Without this link, events cannot be attributed to accounts for health scoring.

2. **Not passing accountId on track calls** — Unlike tools with sticky group context (Mixpanel, Usermaven), Journy expects explicit `accountId` on each event. If you omit it, the event is user-level only and does not contribute to account health scores or playbook triggers.

3. **Stale account traits** — Journy's playbooks and health scores depend on current account properties. If a customer upgrades from `plan: 'starter'` to `plan: 'enterprise'` but you never call the account upsert again, Journy's segmentation and triggers use the old value. Call account upsert on every trait change.

4. **Expecting hierarchical group support** — Journy operates at a single account level. There is no native support for nested structures like account > workspace > project. Carry sub-group identifiers as event metadata properties, not as separate group entities.

5. **Using the wrong authentication header** — Journy uses `X-Api-Key: YOUR_KEY` as the authentication header, not `Authorization: Bearer` or `Authorization: Basic`. An incorrect header name or format results in `401` errors.

6. **Using the deprecated `POST /events` endpoint** — The `POST /events` endpoint is deprecated and will be removed. Use `POST /track` for all new HTTP API implementations. The Node.js SDK's `addEvent()` method handles this internally.

7. **Treating Journy as a product analytics replacement** — Journy is a customer journey orchestration platform, not a product analytics tool. It excels at account health scoring, playbooks, and lifecycle management. For funnel analysis, retention charts, and deep event exploration, pair it with a product analytics tool (Amplitude, Mixpanel, PostHog).

## Debugging

**HTTP response codes:** The Journy API returns standard HTTP status codes:
- `200` — Success (GET requests)
- `201` — Created (POST upsert/track requests)
- `202` — Accepted (DELETE requests)
- `204` — No Content (remove users from account)
- `400` — Bad request (check payload format against OpenAPI spec)
- `401` — Invalid API key (verify `X-Api-Key` header)
- `404` — Endpoint not found (check URL path)
- `429` — Rate limited (check `X-RateLimit-Remaining` header)

**Browser debugging:** Open DevTools Network tab and filter for requests to `api.journy.io` or your CNAME tracking domain (e.g., `go.example.com`). Inspect outgoing POST payloads to verify user IDs, account IDs, and event metadata.

**Node.js SDK:** The SDK methods return response objects. Check the response for success status:

```typescript
const result = await client.addEvent({
  name: 'report_created',
  user: { userId: 'usr_123' },
  account: { accountId: 'acc_456' },
  metadata: { report_id: 'rpt_789' },
});

if (!result.success) {
  console.error('[Journy] Event failed:', result.error);
  console.error('[Journy] Request ID:', result.requestId); // useful for support debugging
}
```

**Journy dashboard:** Check the account and user profiles in the Journy UI to verify that properties and events are arriving correctly. Account timelines show event history.

## Additional API Endpoints

Beyond the core tracking methods, the API exposes:

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/link` | Link web activity (device) to a user |
| POST | `/accounts/users/remove` | Remove users from an account (max 100) |
| DELETE | `/users` | Delete a user |
| DELETE | `/accounts` | Delete an account |
| GET | `/events` | List event definitions |
| GET | `/properties/users` | List user property definitions |
| GET | `/properties/accounts` | List account property definitions |

## Further Documentation

This reference covers the essentials for product tracking implementation. For advanced topics, consult Journy's official documentation:

- **API Reference (OpenAPI spec):** https://developers.journy.io
- **OpenAPI spec (raw):** https://api.journy.io/spec.json
- **Node.js SDK (GitHub):** https://github.com/journy-io/js-sdk
- **PHP SDK (GitHub):** https://github.com/journy-io/php-sdk
- **Python SDK (GitHub):** https://github.com/journy-io/python-sdk
- **SDKs Overview:** https://www.journy.io/integrations/journy-io-sdks
- **Help Center:** https://help.journy.io

**Documentation note:** Journy.io is a smaller platform. Its developer documentation is an OpenAPI spec rendered at `developers.journy.io`. The SDK method names, API endpoints, and authentication patterns described here are based on the OpenAPI spec (v1.0.0) and the `@journyio/sdk` npm package. Verify exact parameter names against the current spec.
