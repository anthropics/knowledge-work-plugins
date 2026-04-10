<!-- Last verified: 2026-03-10 against Usermaven docs -->

# Usermaven Implementation Reference

## Overview

Usermaven is a privacy-friendly, full-stack product analytics platform. It provides user identification, custom event tracking, and company-level (B2B) analytics without relying on third-party cookies. It positions itself as a simpler alternative to Mixpanel and Amplitude with built-in attribution, funnels, and journeys. Cloud-only, proprietary SaaS. Usermaven auto-captures page views, clicks, and form interactions by default, reducing the amount of manual instrumentation needed.

**Forge-approved domains:** `*.events.usermaven.com`, `*.um.contentstudio.io`

## SDK Options

| Environment | Integration | Install |
|---|---|---|
| Browser | Usermaven JS SDK (`@usermaven/sdk-js`) | `npm install @usermaven/sdk-js` |
| Browser (CDN) | Script tag | No install — CDN snippet |
| Node.js / Server | Usermaven JS SDK (isomorphic) or HTTP API | `npm install @usermaven/sdk-js` or raw `fetch()` calls |

The `@usermaven/sdk-js` package (v1.5.13+) is isomorphic and works in both browser and Node.js environments. For Node.js, it wraps the server-side Events API. Usermaven also provides a dedicated Python SDK for Python backends.

## Initialization

### Browser (npm)

```typescript
import { usermavenClient } from '@usermaven/sdk-js';

const usermaven = usermavenClient({
  key: 'YOUR_API_KEY',
  tracking_host: 'https://events.usermaven.com',
  autocapture: true,       // Auto-capture clicks, form submissions, page views
  autoPageview: true,      // Track page views on route change automatically
});
```

<!-- NOTE: The SDK accepts both snake_case (tracking_host) and camelCase (trackingHost) for config keys. Official docs predominantly use tracking_host. -->

### Browser (CDN)

The CDN snippet uses `data-` attributes on the script element for configuration rather than a separate `init` call:

```html
<script type="text/javascript">
  (function () {
    window.usermaven = window.usermaven || (function () {
      (window.usermavenQ = window.usermavenQ || []).push(arguments);
    });
    var t = document.createElement('script'),
        s = document.getElementsByTagName('script')[0];
    t.defer = true;
    t.id = 'um-tracker';
    t.setAttribute('data-tracking-host', 'https://events.usermaven.com');
    t.setAttribute('data-key', 'YOUR_API_KEY');
    t.setAttribute('data-autocapture', 'true');
    t.setAttribute('data-auto-pageview', 'true');
    t.setAttribute('data-randomize-url', 'true');
    t.src = 'https://t.usermaven.com/lib.js';
    s.parentNode.insertBefore(t, s);
  })();
</script>
```

Key `data-` attributes:
- `data-key` — API key (required)
- `data-tracking-host` — event collection endpoint (default: `https://events.usermaven.com`)
- `data-autocapture` — `'true'` or `'false'` for automatic event capture
- `data-auto-pageview` — `'true'` for SPA page view tracking on route change
- `data-randomize-url` — `'true'` to emit events to dynamic endpoints (helps bypass ad blockers)
- `data-privacy-policy` — `'strict'` for cookie-less, GDPR-compliant tracking
- `data-cross-domain-linking` — `'true'` to track users across multiple domains
- `data-domains` — comma-separated list of domains for cross-domain tracking

### Node.js (npm)

The same `@usermaven/sdk-js` package works server-side:

```typescript
import { usermavenClient } from '@usermaven/sdk-js';

const usermaven = usermavenClient({
  key: 'YOUR_API_KEY',
  tracking_host: 'https://events.usermaven.com',
  autocapture: false,
});

// Identify with doNotSendEvent=true to prevent a separate identify event
usermaven.id({
  id: 'usr_123',
  email: 'jane@example.com',
}, true);

// Track events — for Express, pass env context:
// usermaven.track('pageview', { env: envs.express(req, res) });
usermaven.track('report_created', { report_id: 'rpt_789' });
```

### HTTP API (Server-to-Server)

Usermaven exposes a server-side HTTP API for sending events from backend services. The endpoint is the S2S (server-to-server) events endpoint:

```
POST https://events.usermaven.com/api/v1/s2s/event?token=YOUR_API_KEY.YOUR_SERVER_TOKEN
Content-Type: application/json
```

Authentication options (use one):
1. **Query parameter (recommended):** `?token=YOUR_API_KEY.YOUR_SERVER_TOKEN` — compound token using period delimiter
2. **Authorization header:** `Authorization: Bearer YOUR_API_KEY.YOUR_SERVER_TOKEN`
3. **JSON body:** include `"api_key": "YOUR_API_KEY"` in the payload

Both the API Key and Server Token are found in **Workspace Settings > Setup > HTTP API tab**.

## Core Methods

### identify()

Sets the current user identity and traits. Usermaven calls this `id()` in its SDK. Once called, all subsequent events are attributed to this user.

**Browser (npm):**
```typescript
usermaven.id({
  id: 'usr_123',
  email: 'jane@example.com',
  first_name: 'Jane',
  last_name: 'Doe',
  created_at: '2024-01-15T00:00:00Z',
  custom: {
    role: 'admin',
    plan: 'pro',
  },
});
```

**Browser (CDN):**
```javascript
usermaven('id', {
  id: 'usr_123',
  email: 'jane@example.com',
  first_name: 'Jane',
  last_name: 'Doe',
  created_at: '2024-01-15T00:00:00Z',
  custom: {
    role: 'admin',
    plan: 'pro',
  },
});
```

**HTTP API:**
```json
POST /api/v1/s2s/event?token=YOUR_API_KEY.YOUR_SERVER_TOKEN
{
  "api_key": "YOUR_API_KEY",
  "event_type": "user_identify",
  "user": {
    "id": "usr_123",
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "created_at": "2024-01-15T00:00:00Z",
    "custom": {
      "role": "admin",
      "plan": "pro"
    }
  }
}
```

**When to call:** On login, signup, or when user traits change. The SDK persists the user identity in a cookie (`__eventn_id_{API_KEY}`) across page loads.

**Standard user fields:** `id`, `email`, `first_name`, `last_name`, `created_at`. Additional properties go inside the `custom` object.

**Server-side note:** When calling `id()` from Node.js, pass `true` as the second argument to suppress a separate identify event: `usermaven.id({...}, true)`.

### group() / Company Tracking

Usermaven has native company-level tracking. This is a core feature, not a paid add-on. Company data can be set in two ways:

1. **Via the `id()` call** — pass a `company` object to associate the user with an account as part of identification. This is the primary and most-documented approach.
2. **Via the `group()` method** — the SDK (v1.5.13+) also exposes a standalone `group(groupProperties)` method for associating users with groups/organizations.

The `id()` approach with an embedded `company` object remains the canonical pattern shown throughout Usermaven's official documentation.

**Browser (npm) — via id():**
```typescript
usermaven.id({
  id: 'usr_123',
  email: 'jane@example.com',
  company: {
    id: 'acc_456',
    name: 'Acme Corp',
    created_at: '2023-06-01T00:00:00Z',
    custom: {
      plan: 'enterprise',
      mrr: 5000,
      industry: 'technology',
      employee_count: 150,
    },
  },
});
```

**Browser (CDN) — via id():**
```javascript
usermaven('id', {
  id: 'usr_123',
  email: 'jane@example.com',
  company: {
    id: 'acc_456',
    name: 'Acme Corp',
    created_at: '2023-06-01T00:00:00Z',
    custom: {
      plan: 'enterprise',
      mrr: 5000,
      industry: 'technology',
      employee_count: 150,
    },
  },
});
```

**HTTP API:**
```json
POST /api/v1/s2s/event?token=YOUR_API_KEY.YOUR_SERVER_TOKEN
{
  "api_key": "YOUR_API_KEY",
  "event_type": "user_identify",
  "user": {
    "id": "usr_123",
    "email": "jane@example.com"
  },
  "company": {
    "id": "acc_456",
    "name": "Acme Corp",
    "created_at": "2023-06-01T00:00:00Z",
    "custom": {
      "plan": "enterprise",
      "mrr": 5000,
      "industry": "technology",
      "employee_count": 150
    }
  }
}
```

**Key details:**
- Company context is most commonly set as part of the `id()` call using the nested `company` object.
- The SDK also exposes a standalone `group(groupProperties)` method (added in SDK v1.5.x), though official docs still primarily show the `id()` approach. <!-- UNVERIFIED: group() method is listed in SDK README but not documented in Usermaven's official docs pages. Behavior and parameter signature for group() should be confirmed against SDK source or Usermaven support. -->
- The `company.id` field is the unique account identifier.
- Standard company fields: `id`, `name`, `created_at`. Additional properties go inside `custom`.
- Once the company is set via `id()`, subsequent `track()` calls are automatically attributed to that company.

### track()

Records a custom event with optional properties.

**Browser (npm):**
```typescript
usermaven.track('report_created', {
  report_id: 'rpt_789',
  report_type: 'standard',
  template_used: false,
});
```

**Browser (CDN):**
```javascript
usermaven('track', 'report_created', {
  report_id: 'rpt_789',
  report_type: 'standard',
  template_used: false,
});
```

**HTTP API:**
```json
POST /api/v1/s2s/event?token=YOUR_API_KEY.YOUR_SERVER_TOKEN
{
  "api_key": "YOUR_API_KEY",
  "event_type": "report_created",
  "user": {
    "id": "usr_123"
  },
  "company": {
    "id": "acc_456"
  },
  "event_attributes": {
    "report_id": "rpt_789",
    "report_type": "standard",
    "template_used": false
  }
}
```

**When to call:** After the action succeeds, not on button click.

### page()

Page views are auto-tracked by default when `autoPageview: true` (npm) or `data-auto-pageview="true"` (CDN) is set during initialization. The SDK detects History API (`pushState`) route changes for SPAs automatically.

**Manual page view (if autoPageview is disabled):**
```typescript
usermaven.pageview();
```

**CDN:**
```javascript
usermaven('pageview');
```

Auto-collected data: URL, page title, referrer, UTM parameters, screen resolution.

### set() / unset() / reset()

The SDK provides additional state-management methods:

- **`set(properties, options)`** — stores persistent properties that are included with all future events (e.g., A/B test variant)
- **`unset(propertyName, options)`** — removes a previously set persistent property
- **`reset()`** — clears all client state and local storage (call on logout)

## Group Context on Track Calls

When a user is identified with a `company` via the `id()` call, all subsequent `track()` calls are automatically attributed to that company. Unlike Segment or RudderStack, there is no need to pass `groupId` on each track call — the SDK maintains the company context internally.

**Browser behavior:**
```typescript
// 1. Identify user with company
usermaven.id({
  id: 'usr_123',
  company: { id: 'acc_456', name: 'Acme Corp' },
});

// 2. All subsequent track calls are attributed to acc_456
usermaven.track('report_created', { report_id: 'rpt_789' });
usermaven.track('dashboard_viewed', {});
```

**HTTP API behavior:** For server-side calls, include both `user.id` and `company.id` on each event to ensure correct attribution:

```json
{
  "api_key": "YOUR_API_KEY",
  "event_type": "report_created",
  "user": { "id": "usr_123" },
  "company": { "id": "acc_456" },
  "event_attributes": { "report_id": "rpt_789" }
}
```

**Hierarchical groups limitation:** Usermaven supports a single company level per user. There is no native multi-level hierarchy (account > workspace > project) like Amplitude or Accoil. If your product has nested group levels, Usermaven can only represent the top-level company. Encode additional context in event properties or company custom fields as a workaround.

## Required Fields

| Method | Required Fields | Notes |
|---|---|---|
| `id()` | `id` | `email` strongly recommended |
| `id()` with company | `id`, `company.id` | `company.name` strongly recommended |
| `track()` | event name | User must be identified first for attribution |
| `pageview()` | none | Auto-captured data is sufficient |
| HTTP API event | `api_key`, `event_type`, `user` (with at least one of `id`, `email`, or `anonymous_id`) | `company.id` needed for account attribution |

## Limits

| Constraint | Value |
|---|---|
| Event properties per event | No hard documented limit; keep under 50 for performance |
| Property value types | Strings, numbers, booleans (no nested objects in event attributes) |
| Company custom properties | No hard documented limit |
| Auto-capture events | Page views, clicks, form submissions, downloads |
| Data retention | Varies by plan |
| API rate limit | Not publicly documented; contact support for high-volume use |

## Common Pitfalls

1. **Calling track() before id()** — Events fired before the user is identified are attributed to an anonymous session. Always call `id()` on login before tracking custom events. The SDK generates an anonymous ID (stored in the `__eventn_id_{API_KEY}` cookie) for pre-login events. In cookie-based mode (default), calling `id()` stitches anonymous history to the identified profile. In strict/cookieless mode, `id()` must fire from the browser first, not the backend, to ensure stitching works.

2. **Expecting group() to be documented like other platforms** — While the SDK does expose a `group()` method (v1.5.x+), Usermaven's primary documented pattern for company association is through the `id()` call with a nested `company` object. Most official docs and examples use this approach. If you call `id()` without the `company` object, the user has no company attribution.

3. **Confusing standard fields with custom fields** — User traits like `role` and `plan` must go inside the `custom` object, not at the top level. Only `id`, `email`, `first_name`, `last_name`, and `created_at` are top-level user fields. The same applies to company: `id`, `name`, `created_at` are top-level; everything else goes in `custom`.

4. **Not updating company traits on change** — When account traits change (plan upgrade, MRR change), you must call `id()` again with the updated `company` object. There is no separate "update company" call — the same `id()` method handles both creation and updates.

5. **Assuming hierarchical group support** — Usermaven supports one company per user, not multi-level hierarchies. Products with account > workspace > project structures cannot model all levels natively. Use event properties to carry sub-group context if needed.

6. **Auto-capture noise** — With `autocapture: true`, Usermaven tracks every click, form interaction, and page view automatically. This generates high event volumes. For Forge apps or privacy-sensitive deployments, consider disabling auto-capture and tracking only intentional business events. Use the `um-no-capture` CSS class on specific HTML elements to exclude them from auto-capture without disabling it globally.

7. **Using the wrong server-side endpoint** — The server-side API endpoint is `/api/v1/s2s/event` (not `/api/v1/event`). Authentication requires a compound token: `YOUR_API_KEY.YOUR_SERVER_TOKEN`. Both values are found in Workspace Settings > Setup > HTTP API tab.

8. **Using wrong event_type for identify via HTTP API** — The correct `event_type` for identification via the server-side API is `"user_identify"`, not `"identify"`.

## Debugging

**Browser DevTools:** Open the Network tab and filter for requests to `events.usermaven.com`. Each event sends a POST request. Inspect the request body to verify the event type, user ID, company ID, and properties.

**SDK debug mode:** Pass `logLevel: 'debug'` in the initialization config to enable verbose console logging:

```typescript
const usermaven = usermavenClient({
  key: 'YOUR_API_KEY',
  tracking_host: 'https://events.usermaven.com',
  logLevel: 'debug',
});
```

**Usermaven dashboard:** Navigate to the Live Events or Activity Feed view to see events arriving in near real-time. Verify that user and company associations are correct.

**HTTP API debugging:** The API returns `{"status": 1}` on success (HTTP 200). Check the response body for error details if you receive `400` (bad request) or `401` (invalid API key/token).

**Identity resolution verification:** After calling `id()`, check the Contacts Hub timeline to confirm that pre-login anonymous page views appear under the user's authenticated profile.

## Further Documentation

This reference covers the essentials for product tracking implementation. For advanced topics, consult Usermaven's official documentation:

- **Getting Started:** https://usermaven.com/docs/getting-started/installing-usermaven
- **JavaScript SDK (CDN):** https://usermaven.com/docs/integrations/javascript
- **NPM Package:** https://usermaven.com/docs/integrations/npm-package
- **Node.js SDK:** https://usermaven.com/docs/integrations/node-js
- **Identifying Users:** https://usermaven.com/docs/getting-started/sending-your-users-data
- **Identity Resolution:** https://usermaven.com/docs/getting-started/identity-resolution
- **Custom Events:** https://usermaven.com/docs/getting-started/event-tracking-setup
- **Server-Side Events API:** https://usermaven.com/docs/integrations/event-api
- **Parameters Reference:** https://usermaven.com/docs/integrations/reference/parameters
- **Auto-Capture:** https://usermaven.com/docs/advanced-tracking/exclude-autocapture-events
- **All Integrations:** https://usermaven.com/docs/integrations-and-sdks-overview
