# Implementation Architecture

General patterns for building reliable analytics infrastructure.

## Core Principles

1. **Centralized definitions** — All events defined in one place
2. **Queue-based delivery** — Reliable, async event processing
3. **Backend routing** — Frontend events route through backend
4. **Debug mode** — Log instead of send during development
5. **Error resilience** — Analytics failures never break the product
6. **Bundled context** — Identify + Group + Track together

---

## Directory Structure

Regardless of language, organize analytics code consistently:

```
src/analytics/
├── dispatcher.{js,ts,py}   # HTTP transport to provider
├── consumer.{js,ts,py}     # Queue processor (if using queues)
├── events.{js,ts,py}       # Event definitions (THE tracking plan)
├── utils.{js,ts,py}        # Context extraction helpers
└── README.md               # How to add events
```

### events file (The Tracking Plan)

This is where all events are defined. One place, centralized:

```javascript
// events.js

/**
 * Track todo creation.
 * @category core_value
 */
export const trackTodoCreated = async (context) => {
  await track(context, 'Todo Created');
};

/**
 * Track todo update.
 * @category core_value  
 */
export const trackTodoUpdated = async (context) => {
  await track(context, 'Todo Updated');
};

/**
 * Track search performed.
 * @category navigation
 */
export const trackSearchPerformed = async (context) => {
  await track(context, 'Search Performed');
};
```

**Key points:**
- Every event is a named function
- JSDoc comments describe purpose
- All events call common `track()` helper
- No inline string events anywhere else in codebase

### dispatcher (HTTP Transport)

Handles communication with your analytics provider:

```javascript
// dispatcher.js

const dispatch = async (eventType, payload) => {
  const apiKey = process.env.ANALYTICS_API_KEY;
  const url = `https://in.accoil.com/v1/${eventType}`;
  
  const body = JSON.stringify({
    ...payload,
    api_key: apiKey,
    timestamp: Date.now(),
  });

  // Debug mode: log instead of send
  if (process.env.ANALYTICS_DEBUG === 'true') {
    console.log(`[Analytics Debug] ${eventType}:`, body);
    return;
  }

  await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body,
  });
};

export const handleTrack = async (userId, event) => {
  await dispatch('events', { user_id: userId, event });
};

export const handleIdentify = async (userId, groupId, traits) => {
  await dispatch('users', { user_id: userId, group_id: groupId, traits });
};

export const handleGroup = async (groupId, traits) => {
  await dispatch('groups', { group_id: groupId, traits });
};
```

### utils (Context Extraction)

Helper functions to extract IDs from your app's context:

```javascript
// utils.js

export const getUserId = (context) => {
  // Option: instance-level tracking for cost savings
  if (process.env.ANALYTICS_INSTANCE_LEVEL === 'true') {
    return context.accountId;  // All users share account ID
  }
  return context.userId;
};

export const getAccountId = (context) => {
  return context.accountId;
};
```

---

## Queue-Based Delivery

For reliability, use a queue instead of direct HTTP calls.

### Why Queues?

- **Retry on failure** — Transient errors don't lose events
- **Non-blocking** — User actions don't wait for analytics
- **Batching** — Combine multiple events for efficiency
- **Backpressure** — Handle traffic spikes gracefully

### Pattern

```javascript
// events.js with queue

import { Queue } from 'your-queue-library';

const analyticsQueue = new Queue({ key: 'analytics-queue' });

export const track = async (context, eventName) => {
  const userId = getUserId(context);
  const groupId = getAccountId(context);

  // Bundle identify + group + track
  const events = [
    { type: 'identify', userId, groupId, traits: { name: userId } },
    { type: 'group', groupId, traits: { name: groupId } },
    { type: 'track', userId, event: eventName },
  ];

  await analyticsQueue.push(events);
};
```

```javascript
// consumer.js - processes queue

export const processAnalyticsEvent = async (payload) => {
  switch (payload.type) {
    case 'identify':
      await handleIdentify(payload.userId, payload.groupId, payload.traits);
      break;
    case 'group':
      await handleGroup(payload.groupId, payload.traits);
      break;
    case 'track':
      await handleTrack(payload.userId, payload.event);
      break;
  }
};
```

---

## Frontend → Backend Routing

**Never send analytics directly from frontend to provider.**

### Why Backend Routing?

1. **Privacy** — API keys stay server-side
2. **Compliance** — Control what data leaves your system
3. **Consistency** — Same context extraction logic
4. **Enrichment** — Add server-side data to events

### Pattern

Frontend calls backend, backend sends to provider:

```javascript
// Frontend
import { invoke } from 'your-rpc-library';

export const track = async (eventName) => {
  try {
    await invoke('track-event', { event: eventName });
  } catch (error) {
    // Never let analytics break the UI
    console.error('[Analytics] Failed:', error);
  }
};

export const trackSearchPerformed = () => track('Search Performed');
```

```javascript
// Backend resolver
export const trackEvent = async ({ payload, context }) => {
  await track(context, payload.event);
};
```

---

## Debug Mode

Essential for development. Log instead of send:

```javascript
const dispatch = async (eventType, payload) => {
  if (process.env.ANALYTICS_DEBUG === 'true') {
    console.log(`[Analytics Debug] ${eventType}:`, JSON.stringify(payload, null, 2));
    return;
  }
  
  // Actual HTTP call
  await fetch(url, { ... });
};
```

### Environment Variables

```bash
# Development
ANALYTICS_API_KEY=dev_key
ANALYTICS_DEBUG=true

# Production
ANALYTICS_API_KEY=prod_key
# ANALYTICS_DEBUG not set or false
```

---

## Error Resilience

Analytics should never break the product.

### Frontend

```javascript
export const track = async (eventName) => {
  try {
    await invoke('track-event', { event: eventName });
  } catch (error) {
    // Log but don't throw
    console.error('[Analytics]', error);
  }
};
```

### Backend

```javascript
export const trackTodoCreated = async (context) => {
  try {
    await track(context, 'Todo Created');
  } catch (error) {
    // Log, maybe alert, but don't fail the request
    console.error('[Analytics] Failed to track:', error);
  }
};
```

### Non-Blocking

Don't await analytics on the critical path:

```javascript
// ❌ Blocks user action
const createTodo = async (data) => {
  const todo = await db.todos.create(data);
  await trackTodoCreated(context);  // User waits for this
  return todo;
};

// ✅ Fire and forget (with queue for reliability)
const createTodo = async (data) => {
  const todo = await db.todos.create(data);
  trackTodoCreated(context).catch(console.error);  // Non-blocking
  return todo;
};
```

---

## Context: Client-Side vs Server-Side

How you handle identity depends on whether you're client-side or server-side.

### Client-Side (Browser/Mobile SDKs)

Segment and similar SDKs **maintain state**. Call identify and group once, then just track:

```javascript
// On login — call once
analytics.identify('usr_123', { email: 'jane@example.com' });
analytics.group('acc_456', { name: 'Acme Corp' });

// Later — just track, userId is automatic
analytics.track('Report Created', { report_id: 'rpt_789' });
analytics.track('Todo Completed', { todo_id: 'todo_123' });
```

The SDK stores the userId from identify and automatically attaches it to all subsequent track calls. You don't need to bundle on every event.

**When to re-identify:**
- User logs in
- User traits change (role, name, etc.)
- Account traits change (plan, MRR)

### Server-Side (Node/Backend)

Server-side has **no session state**. You must pass userId on every call:

```javascript
// Each call needs userId explicitly
analytics.track({
  userId: 'usr_123',
  event: 'Report Created',
  properties: { report_id: 'rpt_789' }
});
```

**Options for server-side:**

1. **Pass userId per call** (simple, stateless):
```javascript
export const trackReportCreated = async (userId, props) => {
  analytics.track({ userId, event: 'Report Created', properties: props });
};
```

2. **Bundle identify + group + track** (when you can't guarantee prior calls):
```javascript
export const track = async (userId, accountId, eventName, props) => {
  await analytics.identify({ userId, traits: { account_id: accountId } });
  await analytics.group({ userId, groupId: accountId });
  await analytics.track({ userId, event: eventName, properties: props });
};
```

3. **Identify/Group on key moments, track everywhere else**:
```javascript
// On signup/login — set context
await analytics.identify({ userId, traits });
await analytics.group({ userId, groupId, traits });

// On actions — just track with userId
await analytics.track({ userId, event: 'Report Created', properties });
```

### Which to Use?

| Scenario | Approach |
|----------|----------|
| Browser with Segment | identify/group once, just track() after |
| Server with guaranteed login flow | identify/group on login, track with userId |
| Serverless / stateless | Pass userId on every track call |
| No prior identify guarantee | Bundle identify + group + track |

**The key insight:** Client-side SDKs manage state for you. Server-side, you manage it yourself.

---

## Language-Agnostic Patterns

These patterns apply regardless of language:

| Pattern | Implementation |
|---------|----------------|
| Centralized definitions | One file with all events |
| Debug mode | Environment variable check |
| Error resilience | Try/catch, don't throw |
| Queue-based | Use your platform's queue |
| Backend routing | RPC/API from frontend |
| Context bundling | Identify + Group + Track |

The structure and principles are the same whether you're in TypeScript, Python, Ruby, Go, or anything else.

---

## Forge-Specific Architecture Audit Points

When auditing a Forge app (`meta.platform: forge`), verify these additional architecture concerns. Forge apps use a queue-based, privacy-first architecture where all analytics flow through the backend: `Frontend invoke() --> Resolver --> Queue --> Consumer --> Dispatcher --> Provider`.

### Manifest Configuration

- [ ] `manifest.yml` declares the queue consumer with correct queue key matching the producer in `events.js`
- [ ] `manifest.yml` declares scheduled triggers for daily group analytics (if snapshot metrics are expected)
- [ ] External fetch permissions use the **structured object format** with `category: analytics` and `inScopeEUD: false`
- [ ] External fetch address is hostname only (no `https://` prefix, no path)
- [ ] The simple URL string format (e.g., `- "https://in.accoil.com"`) is NOT used — it lacks compliance metadata

```yaml
# CORRECT — structured format with compliance metadata
permissions:
  external:
    fetch:
      backend:
        - address: "in.accoil.com"
          category: analytics
          inScopeEUD: false

# WRONG — simple format, no compliance metadata
permissions:
  external:
    fetch:
      backend:
        - "https://in.accoil.com"
```

### Privacy Barrier

- [ ] Frontend sends **only event names** via `invoke()` — no properties, no user data, no context
- [ ] Backend resolver adds cloudId and accountId from Forge context (server-side only)
- [ ] No user-generated content (issue titles, form content, search queries) in any event properties or traits
- [ ] `@forge/api` fetch is used in the dispatcher (not standard `fetch` or `node-fetch` — these fail in Forge's sandboxed runtime)

### Data Flow Integrity

- [ ] Frontend-triggered events flow through the resolver bridge, not directly to the queue
- [ ] Backend-triggered events call tracking functions directly from business logic resolvers
- [ ] All events (frontend and backend) flow through the same queue/consumer/dispatcher chain
- [ ] Consumer re-throws errors to trigger Forge's automatic retry mechanism
- [ ] Scheduled analytics (daily group traits) bypass the queue and dispatch directly (already async)

### Identity and Groups

- [ ] `cloudId` is used as the top-level group ID (required for Marketplace billing correlation)
- [ ] `accountId` is used as the user ID
- [ ] Group traits include `domain` (derived from `context.siteUrl`)
- [ ] License status traits are populated from `context.license.isActive` and `context.license.isEvaluation`
- [ ] Identify + group + track calls are bundled atomically in each queue push

### Environment Configuration

- [ ] `ANALYTICS_API_KEY` is set via `forge variables set` (not `.env` files)
- [ ] `ANALYTICS_DEBUG` environment variable enables log-only mode for development
- [ ] Per-environment configuration uses `forge variables set --environment <env>`
