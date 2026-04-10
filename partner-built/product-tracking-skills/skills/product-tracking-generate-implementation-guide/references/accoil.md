<!-- Last verified: 2026-03-10 against developer.accoil.com -->
# Accoil Implementation Guide

## Overview

Accoil is a B2B product engagement analytics platform built specifically for B2B SaaS with accounts and users as first-class entities. It calculates engagement scores at the account level.

## Three Integration Methods

| Method | Best For | Account Context |
|--------|----------|-----------------|
| **Accoil tracker.js** | Browser-side, no other CDP | Built-in via `.group()` |
| **Accoil Direct API (v2)** | Server-side, no Segment | Via `/v2/group` endpoint |
| **Via Segment** | Already using Segment | Segment `group()` flows through |

Additional integration destinations include **RudderStack**, **PostHog**, and **Amplitude**. All methods achieve the same result. Choose based on your stack.

---

## Method 1: Accoil tracker.js (Browser)

A zero-dependency JavaScript library loaded from CDN.

### Setup

Add to your top-level template:

```html
<script type="text/javascript">
(function() {
  var accoil = window.accoil = window.accoil || {q: []};
  var calls = ['load', 'identify', 'group', 'track'];
  for (var i = 0; i < calls.length; i++) (function(call) {
    accoil[call] = function() { accoil.q.push([call, arguments]); };
  })(calls[i]);
  var s = document.createElement('script'); s.src = 'https://cdn.accoil.com/tracker.js'; s.async = true;
  var f = document.getElementsByTagName('script')[0]; f.parentNode.insertBefore(s, f);
})();
</script>
<script type="text/javascript">
  accoil.load("YOUR_API_KEY");
</script>
```

### Identify (required before tracking)

Call on every page load. The library keeps track of the current user — all subsequent `.track()` calls are scoped to them.

```javascript
accoil.identify("usr_123", {
  email: "jane@example.com",
  name: "Jane Doe",
  created_at: "2024-01-15T00:00:00Z",
  role: "admin"
});
```

### Group (required for account context)

Call when accounts are created or traits change (upgrade, downgrade, cancellation).

```javascript
accoil.group("acc_456", {
  name: "Acme Corp",
  status: "active",
  mrr: 500000, // $5,000 in cents — MRR is specified in cents, not dollars
  created_at: "2023-06-01T00:00:00Z"
});
```

### Track

```javascript
accoil.track("Report_Created");
```

**Important:** Accoil track calls accept **only the event name**. No event properties are stored. Encode meaningful distinctions in the event name itself.

### Audit patterns for tracker.js

```
accoil.load(
accoil.identify(
accoil.group(
accoil.track(
```

---

## Method 2: Accoil Direct API (v2)

Server-side REST API. Async processing — returns 202 immediately, processes in background.

### Authentication

```
Authorization: Basic YOUR_API_KEY
```

API key found under Account > General settings in Accoil.

### Base URL

```
https://in.accoil.com
```

### POST /v2/identify

```json
{
  "userId": "usr_123",
  "groupId": "acc_456",
  "timestamp": "2025-01-01T00:00:00Z",
  "traits": {
    "email": "jane@example.com",
    "name": "Jane Doe",
    "created_at": "2024-01-15T00:00:00Z",
    "role": "admin"
  }
}
```

Required: `userId`. Recommended traits: `email`, `name`, `created_at`.

### POST /v2/group

```json
{
  "groupId": "acc_456",
  "userId": "usr_123",
  "timestamp": "2025-01-01T00:00:00Z",
  "traits": {
    "name": "Acme Corp",
    "created_at": "2023-06-01T00:00:00Z",
    "status": "paid",
    "mrr": 500000
  }
}
```

Required: `groupId`. `userId` is optional on group calls — omit it for scheduled account-only trait updates (e.g., snapshot metrics syncs). MRR is specified in cents, not dollars (e.g., `500000` = $5,000). Recommended traits: `name`, `created_at`.

### POST /v2/track

```json
{
  "userId": "usr_123",
  "event": "Report_Created",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

Required: `userId`, `event`. **No properties accepted** — only the event name is stored.

### Response codes

| Code | Meaning |
|------|---------|
| 202 | Accepted (processed async) |
| 413 | Payload too large |
| 503 | Service unavailable |

**Gotcha:** The API returns 202 even if the API key is invalid. It validates asynchronously. If events don't appear in the Accoil UI, check your Authorization header.

### Server-side example (Node.js)

```typescript
const ACCOIL_API_KEY = process.env.ACCOIL_API_KEY!;
const ACCOIL_BASE = 'https://in.accoil.com';

async function accoilPost(path: string, body: object) {
  await fetch(`${ACCOIL_BASE}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Basic ${ACCOIL_API_KEY}`,
    },
    body: JSON.stringify(body),
  });
}

function identifyUser(userId: string, groupId: string, traits: Record<string, unknown>) {
  accoilPost('/v2/identify', { userId, groupId, traits });
}

function groupAccount(groupId: string, traits: Record<string, unknown>) {
  accoilPost('/v2/group', { groupId, traits });
}

function trackEvent(userId: string, event: string) {
  accoilPost('/v2/track', { userId, event });
}
```

---

## Method 3: Via Segment

If already using Segment, add Accoil as a destination. All `identify`, `group`, and `track` calls flow through automatically.

1. In Segment: Destinations > Add Destination > Accoil
2. Enter your Accoil API key
3. Map group ID to Accoil's account identifier

```typescript
// Segment calls that Accoil receives
analytics.identify({ userId: 'usr_123', traits: { email: 'jane@example.com' } });
analytics.group({ userId: 'usr_123', groupId: 'acc_456', traits: { name: 'Acme Corp', plan: 'pro' } });
analytics.track({ userId: 'usr_123', event: 'Report_Created', properties: { report_id: 'rpt_789' } });
```

Note: Segment passes properties, but Accoil only stores the event name from track calls.

---

## Group Context on Track Calls (Hierarchical Groups)

**EARLY ACCESS: Group Context/Hierarchy is in early access**

Accoil has full support for hierarchical group structures. When your product has multiple group levels (account > workspace > project), every track call must include a `context.groupId` to attribute the event to the correct group.

### Every Group Level Needs a group() Call

Define each level of the hierarchy with a `group()` call. Use `parent_group_id` in traits to establish the parent-child relationship.

**tracker.js (Browser):**
```javascript
// 1. Account (top level)
accoil.group("acc_456", {
  name: "Acme Corp",
  plan: "enterprise"
});

// 2. Workspace (child of account)
accoil.group("ws_789", {
  name: "Engineering",
  parent_group_id: "acc_456"
});

// 3. Project (child of workspace)
accoil.group("proj_123", {
  name: "Q1 Release",
  parent_group_id: "ws_789"
});
```

**Direct API (v2):**
```json
POST /v2/group
{
  "groupId": "acc_456",
  "userId": "usr_123",
  "traits": {
    "name": "Acme Corp",
    "plan": "enterprise"
  }
}

POST /v2/group
{
  "groupId": "ws_789",
  "userId": "usr_123",
  "traits": {
    "name": "Engineering",
    "parent_group_id": "acc_456"
  }
}

POST /v2/group
{
  "groupId": "proj_123",
  "userId": "usr_123",
  "traits": {
    "name": "Q1 Release",
    "parent_group_id": "ws_789"
  }
}
```

### Attributing Track Calls to a Specific Group

Include `context.groupId` on every track call to tell Accoil which group the event belongs to. Accoil uses this plus the `parent_group_id` relationships to roll metrics up the hierarchy automatically.

**tracker.js (Browser):**
```javascript
// Project-level event — rolls up to workspace and account
accoil.track("Task_Completed", {
  context: { groupId: "proj_123" }
});

// Workspace-level event — rolls up to account only
accoil.track("Workspace_Settings_Updated", {
  context: { groupId: "ws_789" }
});

// Account-level event — no rollup needed
accoil.track("Plan_Upgraded", {
  context: { groupId: "acc_456" }
});
```

**Direct API (v2):**
```json
POST /v2/track
{
  "userId": "usr_123",
  "event": "Task_Completed",
  "context": {
    "groupId": "proj_123"
  }
}
```

**Via Segment:**
```javascript
analytics.track('Task_Completed', {}, {
  context: { groupId: 'proj_123' }
});
```

### How Rollups Work

When Accoil receives a track call with `context.groupId`:
1. The event is attributed to the specified group (e.g., `proj_123`)
2. Accoil follows the `parent_group_id` chain upward
3. The event contributes to engagement scores at every level in the hierarchy

**Example:** A `Task_Completed` event with `groupId: "proj_123"` contributes to:
- Project `proj_123` metrics
- Workspace `ws_789` metrics (parent)
- Account `acc_456` metrics (grandparent)

### Without context.groupId

If a track call does not include `context.groupId`, Accoil attributes the event to the user's most recently associated group from the last `group()` call. This is unreliable in multi-group products where users switch between workspaces or projects. **Always include context.groupId explicitly.**

---

## Critical: No Event Properties

Accoil stores **event names only** — not properties. This affects how you design events:

| Other SDKs | Accoil |
|-----------|--------|
| `track("report.created", { type: "standard" })` | `track("Report_Created")` |
| `track("report.created", { type: "template" })` | `track("Template_Report_Created")` |

If you need to distinguish variants in Accoil, encode the distinction in the event name. For other downstream tools (Amplitude, Mixpanel), you can still send properties — Accoil will simply ignore them.

## Critical: Group Calls Are Essential

Accoil is account-centric. Without `group()` calls, events can't be attributed to accounts and engagement scoring fails.

**Call `group()` when:**
- User logs in (associate user with account)
- Account is created
- Account traits change (upgrade, MRR change, cancellation)

## Account Traits That Matter

| Trait | Why | Type |
|-------|-----|------|
| `name` | Account identification | string |
| `created_at` | Cohort analysis | ISO 8601 |
| `plan` / `status` | Plan-based segmentation | string |
| `mrr` | Revenue weighting (in cents, not dollars) | number (integer) |
| `industry` | Segmentation | string |
| `employee_count` | Size segmentation | number |

## User Traits That Matter

| Trait | Why | Type |
|-------|-----|------|
| `email` | User identification | string |
| `name` | User identification | string |
| `created_at` | Cohort analysis | ISO 8601 |
| `role` | Role-based analysis | string |

## Common Pitfalls

### 1. Missing Group Calls
Most common issue. Accoil needs account context for scoring.
**Fix:** Call `group()` on login and when account traits change.

### 2. Expecting Event Properties
Accoil ignores event properties. Only the event name is stored.
**Fix:** Encode meaningful distinctions in the event name.

### 3. Silent Auth Failures
The API returns 202 even with invalid API keys — it validates async.
**Fix:** If events don't appear in the Accoil UI, check your API key / Authorization header.

### 4. Stale Account Traits
MRR, plan, status change but `group()` isn't called again.
**Fix:** Call `group()` whenever account traits change, not just on first login.

### 5. MRR Sent as Dollars Instead of Cents
Accoil expects MRR in cents (integer). Sending `5000` means $50.00, not $5,000.
**Fix:** Always multiply dollar amounts by 100. For example, $5,000 MRR should be sent as `500000`.

### 6. Using Email as userId
Emails change (e.g., name changes, domain migrations). Using email as `userId` creates duplicate user records.
**Fix:** Use stable database primary keys (e.g., UUIDs, auto-increment IDs) as `userId`.

## Debugging

- **Accoil Dashboard:** Live events appear in the debug console within seconds.
- **Segment Event Delivery:** If using Segment, check the delivery tab for Accoil destination.
- **Test Account:** Create a test account with known events, verify in Accoil's account view.

## Further Documentation

This reference covers the essentials for product tracking implementation. For advanced topics and support, consult Accoil's official resources:

- **Developer Docs:** https://developer.accoil.com/
- **JavaScript SDK:** https://developer.accoil.com/docs/js-tracking
- **REST API (Getting Started):** https://developer.accoil.com/docs/getting-started
- **Identify Call:** https://developer.accoil.com/docs/identify-call
- **Group Call:** https://developer.accoil.com/docs/group-call
- **Track Call:** https://developer.accoil.com/docs/track-call
- **Call Types:** https://developer.accoil.com/docs/call-types
- **Group Hierarchy:** https://developer.accoil.com/docs/concepts/group-hierarchy
- **Ingress API:** https://developer.accoil.com/docs/ingress-api
- **Segment Integration:** https://developer.accoil.com/docs/integrations/segment
- **RudderStack Integration:** https://developer.accoil.com/docs/integrations/rudderstack
