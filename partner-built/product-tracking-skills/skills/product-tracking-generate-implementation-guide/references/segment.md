<!-- Last verified: 2026-03-10 against Segment docs -->
# Segment Implementation Reference

Segment is a customer data platform (CDP) that routes events to multiple destinations. Three integration paths depending on environment:

| Environment | Integration | Install |
|---|---|---|
| Browser (SPA, website) | Analytics.js (`@segment/analytics-next`) | `npm install @segment/analytics-next` |
| Server (Node.js) | Analytics Node (`@segment/analytics-node`) | `npm install @segment/analytics-node` |
| Sandboxed / HTTP-only (Forge, edge, serverless) | HTTP API direct | No SDK — raw `fetch()` calls |

## Browser Setup

### npm (recommended for SPAs)

```javascript
import { AnalyticsBrowser } from '@segment/analytics-next';

const analytics = AnalyticsBrowser.load({
  writeKey: 'YOUR_WRITE_KEY'
});
```

Analytics.js automatically collects `anonymousId` (stored in `localStorage`), page `url`, `title`, `referrer`, and `path`.

### Snippet (traditional websites)

The Segment snippet goes in `<head>`. It loads asynchronously and won't block page rendering. The snippet auto-fires a `page()` call on load.

## Server Setup (Node.js)

```javascript
import { Analytics } from '@segment/analytics-node';

const analytics = new Analytics({ writeKey: process.env.SEGMENT_WRITE_KEY });
```

Server-side calls require explicit `userId` on every call — there is no implicit user context like the browser SDK maintains.

## HTTP API (Direct)

Use when you cannot install an SDK (Forge backend, edge functions, serverless without npm). Base URLs:

- Default (Oregon): `https://api.segment.io/v1/`
- EU (Dublin): `https://events.eu1.segmentapis.com/v1/`

### Regional Endpoints

Since April 2025, Segment enforces regional data routing. EU workspaces **MUST** use the EU endpoints — data sent to the wrong region is silently rejected (the API returns `200` but the data is dropped).

| Integration | Default (Oregon) | EU (Dublin) |
|---|---|---|
| HTTP API | `https://api.segment.io/v1/` | `https://events.eu1.segmentapis.com/v1/` |
| Node.js SDK (`host`) | _(default, no config needed)_ | `https://eu1.api.segmentapis.com` |

**Node.js EU configuration:**
```javascript
const analytics = new Analytics({
  writeKey: process.env.SEGMENT_WRITE_KEY,
  host: 'https://eu1.api.segmentapis.com'
});
```

**Warning:** There is no error signal when data is sent to the wrong region. Verify your workspace region in Segment Settings → Workspace before configuring endpoints.

### Authentication

Simplest: include `writeKey` in the JSON body. Alternative: Basic Auth header with write key as username and empty password — `Authorization: Basic <base64(writeKey:)>`.

All requests require `Content-Type: application/json`.

## Core Methods

All three integrations support the same four methods. The API shape is identical — only the calling convention differs.

### Identify

Associates a user with their traits. Call on signup, login, or when traits change.

**Browser:**
```javascript
analytics.identify('usr_123', {
  email: 'jane@example.com',
  name: 'Jane Smith',
  role: 'admin',
  created_at: '2024-01-15T10:30:00Z'
});
```

**Node.js:**
```javascript
analytics.identify({
  userId: 'usr_123',
  traits: {
    email: 'jane@example.com',
    name: 'Jane Smith',
    role: 'admin',
    created_at: '2024-01-15T10:30:00Z'
  }
});
```

**HTTP API:**
```json
POST /v1/identify
{
  "userId": "usr_123",
  "traits": {
    "email": "jane@example.com",
    "name": "Jane Smith",
    "role": "admin",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "writeKey": "YOUR_WRITE_KEY"
}
```

### Group

Associates a user with an account/organization. Critical for B2B — without this, downstream tools like Accoil, Intercom, and Totango cannot do account-level analysis.

**Browser:**
```javascript
analytics.group('acc_456', {
  name: 'Acme Corp',
  plan: 'enterprise',
  industry: 'technology',
  employee_count: 150
});
```

**Node.js:**
```javascript
analytics.group({
  userId: 'usr_123',
  groupId: 'acc_456',
  traits: {
    name: 'Acme Corp',
    plan: 'enterprise',
    industry: 'technology',
    employee_count: 150
  }
});
```

**HTTP API:**
```json
POST /v1/group
{
  "userId": "usr_123",
  "groupId": "acc_456",
  "traits": {
    "name": "Acme Corp",
    "plan": "enterprise",
    "industry": "technology",
    "employee_count": 150
  },
  "writeKey": "YOUR_WRITE_KEY"
}
```

### Track

Records an action. Call after the action succeeds, not on button click.

**Browser:**
```javascript
analytics.track('report.created', {
  report_id: 'rpt_789',
  report_type: 'standard',
  template_used: false
});
```

**Node.js:**
```javascript
analytics.track({
  userId: 'usr_123',
  event: 'report.created',
  properties: {
    report_id: 'rpt_789',
    report_type: 'standard',
    template_used: false
  }
});
```

**HTTP API:**
```json
POST /v1/track
{
  "userId": "usr_123",
  "event": "report.created",
  "properties": {
    "report_id": "rpt_789",
    "report_type": "standard",
    "template_used": false
  },
  "writeKey": "YOUR_WRITE_KEY"
}
```

### Page

Records a page view. Browser SDK auto-collects `url`, `title`, `referrer`, `path`. Call at least once per page load (the snippet does this automatically). For SPAs, call on route change.

**Browser:**
```javascript
analytics.page('Reports', 'Report Detail', {
  report_id: 'rpt_789'
});
```

**Node.js:**
```javascript
analytics.page({
  userId: 'usr_123',
  name: 'Report Detail',
  category: 'Reports',
  properties: {
    report_id: 'rpt_789',
    url: 'https://app.example.com/reports/rpt_789'
  }
});
```

**HTTP API:**
```json
POST /v1/page
{
  "userId": "usr_123",
  "name": "Report Detail",
  "properties": {
    "report_id": "rpt_789"
  },
  "writeKey": "YOUR_WRITE_KEY"
}
```

## HTTP API Batch Endpoint

Send multiple events in one request. Each event in the batch needs a `type` field. Use this to bundle identify + group + track atomically:

```json
POST /v1/batch
{
  "batch": [
    {
      "type": "identify",
      "userId": "usr_123",
      "traits": { "email": "jane@example.com", "name": "Jane Smith" }
    },
    {
      "type": "group",
      "userId": "usr_123",
      "groupId": "acc_456",
      "traits": { "name": "Acme Corp", "plan": "enterprise" }
    },
    {
      "type": "track",
      "userId": "usr_123",
      "event": "report.created",
      "properties": { "report_type": "standard" }
    }
  ],
  "writeKey": "YOUR_WRITE_KEY"
}
```

## Browser Batching

Analytics.js can batch events to reduce network requests. Configure in the `load` call:

```javascript
analytics.load('YOUR_WRITE_KEY', {
  integrations: {
    'Segment.io': {
      deliveryStrategy: {
        strategy: 'batching',
        config: {
          size: 10,      // flush after 10 events
          timeout: 5000  // or after 5 seconds, whichever comes first
        }
      }
    }
  }
});
```

On page unload, Analytics.js attempts to flush the queue using `fetch` with `keepalive`. The 64 KB `keepalive` limit means smaller batch sizes are safer for capturing exit events.

## Required Fields

| Method | Required | Notes |
|---|---|---|
| All calls | `userId` or `anonymousId` | Browser SDK manages `anonymousId` automatically |
| `track` | `event` (string) | The event name |
| `group` | `groupId` (string) | The account/org identifier |
| `identify` | at least one of `userId` / `anonymousId` | `traits` optional but recommended |

Omit `timestamp` to use server time (preferred for live events). Only set it explicitly for historical imports.

## Limits

| Constraint | Value |
|---|---|
| Rate limit | 1,000 requests/sec per workspace |
| Max single event | 32 KB |
| Max batch request | 500 KB (with each event still under 32 KB) |
| Max events per batch | 2,500 (excess events are silently dropped — API returns 200) |
| `messageId` | Auto-generated for dedup; if setting manually, keep under 100 chars |

## Typical Call Sequence

```
1. User signs up or logs in
   → identify(userId, traits)

2. Account context is known
   → group(groupId, traits)

3. User performs actions
   → track(eventName, properties)

4. Page navigation (browser)
   → page(category, name, properties)
```

For B2B SaaS, always call identify then group before any track calls. The browser SDK attaches the identified user to subsequent track calls automatically. Server-side, you must pass `userId` on every call.

## Anonymous ID Handling

Browser SDK generates and stores an `anonymousId` in `localStorage`/cookies. Before login, events are tracked with this anonymous ID. On `identify()`, the anonymous ID is associated with the real user — Segment merges the anonymous session history.

```javascript
// Before login — tracked with anonymousId
analytics.track('page.viewed');

// On login — merges anonymous history with known user
analytics.identify('usr_123', { email: 'jane@example.com' });

// After login — events tied to usr_123
analytics.track('report.created');
```

Server-side and HTTP API have no automatic anonymous ID. You must provide `userId` or `anonymousId` explicitly on each call.

## Destination Filtering

Control which destinations receive an event using the `integrations` object:

**Browser:**
```javascript
analytics.track('sensitive.event', { amount: 500 }, {
  integrations: {
    'All': false,
    'Mixpanel': true,
    'Accoil': true
  }
});
```

**HTTP API:**
```json
{
  "userId": "usr_123",
  "event": "sensitive.event",
  "integrations": {
    "All": false,
    "Mixpanel": true
  },
  "writeKey": "YOUR_WRITE_KEY"
}
```

Destination names are case-sensitive and must match the name in Segment's destination catalog.

## Debugging

**Browser:**
```javascript
analytics.debug(true); // logs all calls to console
```

**Segment UI:** Sources → [Your Source] → Debugger shows events in real-time.

**Chrome extension:** Segment Inspector shows event lifecycle, payload changes, and delivery status.

**HTTP API errors:**
- `200` — accepted (check Segment Debugger if events don't appear downstream)
- `400` — payload too large, invalid JSON, or missing required fields
- `429` — rate limited; check `Retry-After` header

## Group Context on Track Calls

Segment's `group()` call associates a user with a group, but it does **not** automatically attach group context to subsequent `track()` calls. To attribute an event to a specific group, you must include the `groupId` in the track call's `context` object.

### Why This Matters

In B2B products with hierarchical groups (account > workspace > project), each event belongs to a specific group level. Without explicit group context on the track call, downstream tools cannot determine which group the event should be attributed to.

### Pattern: context.groupId

**Browser:**
```javascript
analytics.track('task.completed', {
  task_id: 'task_456'
}, {
  context: { groupId: 'ws_789' }  // Attributes event to this workspace
});
```

**Node.js:**
```javascript
analytics.track({
  userId: 'usr_123',
  event: 'task.completed',
  properties: {
    task_id: 'task_456'
  },
  context: { groupId: 'ws_789' }  // Attributes event to this workspace
});
```

**HTTP API:**
```json
POST /v1/track
{
  "userId": "usr_123",
  "event": "task.completed",
  "properties": {
    "task_id": "task_456"
  },
  "context": {
    "groupId": "ws_789"
  },
  "writeKey": "YOUR_WRITE_KEY"
}
```

### Events at Different Group Levels

The tracking plan assigns each event to a group level. The track call must carry the correct group ID for that level:

```javascript
// Project-level event
analytics.track('task.completed', { task_id: 'task_456' }, {
  context: { groupId: 'proj_123' }
});

// Workspace-level event
analytics.track('workspace.settings_updated', { setting: 'notifications' }, {
  context: { groupId: 'ws_789' }
});

// Account-level event
analytics.track('plan.upgraded', { from_plan: 'free', to_plan: 'pro' }, {
  context: { groupId: 'acc_456' }
});
```

### Every Group Level Needs a group() Call

Before referencing a group ID in track calls, that group must be established via a `group()` call. For hierarchical products, issue a `group()` call for **every level** in the hierarchy:

```javascript
// 1. Establish account
analytics.group('acc_456', {
  name: 'Acme Corp',
  plan: 'enterprise'
});

// 2. Establish workspace (with parent reference)
analytics.group('ws_789', {
  name: 'Engineering',
  group_type: 'workspace',
  parent_group_id: 'acc_456'
});

// 3. Establish project (with parent reference)
analytics.group('proj_123', {
  name: 'Q1 Release',
  group_type: 'project',
  parent_group_id: 'ws_789'
});

// Now track calls can reference any of these group IDs
analytics.track('task.completed', { task_id: 'task_456' }, {
  context: { groupId: 'proj_123' }
});
```

**Note:** Segment's native `group()` only associates one group at a time per user. The `context.groupId` on track calls is what downstream tools (Accoil, Amplitude, Mixpanel) use to attribute the event to the correct group. Some downstream tools (like Accoil) support hierarchical rollups via `parent_group_id` traits on group calls.

## Common Pitfalls

1. **Not calling identify** — events are anonymous and hard to analyze.
2. **Missing group calls** — B2B tools lose account-level insights.
3. **PII in event properties** — put PII in user traits (identify), not event properties. Properties should be IDs and metadata.
4. **Calling identify too often** — once per session is enough. Excessive calls cause issues with some destinations.
5. **Not flushing on exit** — browser SDK batches calls. Analytics.js handles this automatically with `beforeunload`, but if you have a custom SPA teardown, call `analytics.flush()`.
6. **Server-side without userId** — unlike browser SDK, there's no implicit user. Every call needs explicit `userId`.

## Further Documentation

This reference covers the essentials. Segment's documentation is extensive — for advanced topics (middleware, plugins, custom proxies, consent management, specific destination configs, mobile SDKs, etc.), search the Segment docs at `https://www.twilio.com/docs/segment` for current guidance.
