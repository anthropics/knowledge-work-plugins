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
  const url = `${process.env.ANALYTICS_ENDPOINT}/v1/${eventType}`;
  
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
ANALYTICS_ENDPOINT=https://your-provider.example.com
ANALYTICS_API_KEY=dev_key
ANALYTICS_DEBUG=true

# Production
ANALYTICS_ENDPOINT=https://your-provider.example.com
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

## Group Context on Track Calls

In B2B products with hierarchical groups (account > workspace > project), every track call must carry the group ID for the level the event belongs to. This is how analytics tools know which group the event should be attributed to.

### The Pattern

The tracking plan assigns each event a `group_level` (e.g., project, workspace, account). The implementation must:

1. **Issue a group() call for every level in the hierarchy** — Each group must exist before events reference it
2. **Pass the correct group ID on every track() call** — Via context object, groups property, or $groups property depending on the SDK

### Updated track() Helper

The core `track()` function must accept and forward group context:

```javascript
// events.js — track helper with group context

export const track = async (context, eventName, groupId) => {
  const userId = getUserId(context);
  const accountId = getAccountId(context);

  // Bundle identify + group + track with group context
  const events = [
    { type: 'identify', userId, groupId: accountId, traits: { name: userId } },
    { type: 'group', groupId: accountId, traits: { name: accountId } },
    { type: 'track', userId, event: eventName, context: { groupId: groupId || accountId } },
  ];

  await analyticsQueue.push(events);
};
```

### Updated Event Functions

Each event function passes the appropriate group ID based on the tracking plan's `group_level` assignment:

```javascript
// events.js — event functions with group context

/**
 * Track task creation (group_level: project)
 * @category core_value
 */
export const trackTaskCreated = async (context, projectId) => {
  await track(context, 'Task Created', projectId);
};

/**
 * Track workspace settings change (group_level: workspace)
 * @category configuration
 */
export const trackWorkspaceSettingsUpdated = async (context, workspaceId) => {
  await track(context, 'Workspace Settings Updated', workspaceId);
};

/**
 * Track plan upgrade (group_level: account)
 * @category billing
 */
export const trackPlanUpgraded = async (context) => {
  const accountId = getAccountId(context);
  await track(context, 'Plan Upgraded', accountId);
};
```

### Updated Dispatcher

The dispatcher must forward group context to the analytics provider:

```javascript
// dispatcher.js — handles group context

export const handleTrack = async (userId, event, groupContext) => {
  await dispatch('events', {
    user_id: userId,
    event,
    context: groupContext   // { groupId: 'proj_123' }
  });
};
```

### Updated Consumer

The consumer passes group context through to the dispatcher:

```javascript
// consumer.js — passes group context

export const processAnalyticsEvent = async (payload) => {
  switch (payload.type) {
    case 'identify':
      await handleIdentify(payload.userId, payload.groupId, payload.traits);
      break;
    case 'group':
      await handleGroup(payload.groupId, payload.traits);
      break;
    case 'track':
      await handleTrack(payload.userId, payload.event, payload.context);
      break;
  }
};
```

### Establishing the Full Group Hierarchy

Before tracking events against sub-account groups, ensure every level has been established via `group()` calls:

```javascript
// utils.js — group hierarchy setup

export const establishGroupHierarchy = async (context) => {
  const accountId = getAccountId(context);
  const workspaceId = getWorkspaceId(context);
  const projectId = getProjectId(context);

  // Account (top level)
  await analyticsQueue.push({
    type: 'group',
    groupId: accountId,
    traits: {
      name: context.accountName,
      group_type: 'account'
    }
  });

  // Workspace (if applicable)
  if (workspaceId) {
    await analyticsQueue.push({
      type: 'group',
      groupId: workspaceId,
      traits: {
        name: context.workspaceName,
        group_type: 'workspace',
        parent_group_id: accountId
      }
    });
  }

  // Project (if applicable)
  if (projectId) {
    await analyticsQueue.push({
      type: 'group',
      groupId: projectId,
      traits: {
        name: context.projectName,
        group_type: 'project',
        parent_group_id: workspaceId
      }
    });
  }
};
```

Call `establishGroupHierarchy()` on login or when the user enters a new group context (switches workspace, opens a project, etc.).

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

## Forge Platform Implementation Notes

When implementing analytics in a Forge app (`meta.platform: forge`), these platform-specific constraints apply on top of the general patterns above.

### Hard Constraints

- **No direct network from frontend.** Forge Custom UI frontends run in a sandboxed iframe. They cannot call `fetch()` to external services. All analytics must route through `invoke()` to a backend resolver.
- **Forge-specific fetch required.** In the backend, use `import { fetch } from '@forge/api'` -- standard `fetch` and `node-fetch` fail in Forge's sandboxed runtime.
- **Queue via `@forge/events`.** Use `new Queue({ key: 'analytics-queue' })` from `@forge/events`. The queue key must match between the producer code and the `manifest.yml` consumer declaration.
- **Environment variables via CLI.** Use `forge variables set` instead of `.env` files. Per-environment: `forge variables set --environment production ANALYTICS_API_KEY <key>`.
- **External fetch must be declared** in `manifest.yml` with structured format including `category: analytics` and `inScopeEUD: false`. Without this metadata, the app fails Atlassian compliance review.

### Forge File Structure

```
src/analytics/
├── dispatcher.js    # HTTP transport using @forge/api fetch
├── consumer.js      # Queue event processor (Resolver-based)
├── events.js        # Backend event definitions + queue producer
├── resolvers.js     # Frontend → backend bridge (privacy barrier)
├── utils.js         # Identity extraction (cloudId, accountId)
└── schedule.js      # Daily scheduled group trait updates

static/spa/src/
└── analytics.js     # Frontend event wrappers (invoke calls only)
```

### Key Differences from General Patterns

| General Pattern | Forge-Specific |
|---|---|
| `import { Queue } from 'your-queue-library'` | `import { Queue } from '@forge/events'` |
| `fetch(url, ...)` | `import { fetch } from '@forge/api'` |
| `invoke('track-event', ...)` from any RPC | `invoke()` from `@forge/bridge` |
| ENV vars in `.env` | `forge variables set` |
| Consumer is a standalone process | Consumer declared in `manifest.yml` as a Forge module |
| Scheduled jobs via cron | `scheduledTrigger` in `manifest.yml` |

### Privacy Architecture

The resolver bridge (`src/analytics/resolvers.js`) is the privacy barrier. The frontend sends only the event name via `invoke()`. The resolver adds `cloudId` and `accountId` from the Forge context server-side. No user-generated content, no browser data, no IPs reach the analytics provider.
