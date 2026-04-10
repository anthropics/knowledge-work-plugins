<!-- Last verified: 2026-03-10 against Amplitude docs -->
# Amplitude Implementation Guide

## Overview

Amplitude is a product analytics platform focused on user behavior analysis. Direct integration (not via Segment) gives you full control over Amplitude-specific features.

## SDK Options

### Browser
```bash
npm install @amplitude/analytics-browser
```

### Node.js
```bash
npm install @amplitude/analytics-node
```

### React
```bash
npm install @amplitude/analytics-browser
# Use with React hooks for automatic page tracking
```

## Initialization

```typescript
import * as amplitude from '@amplitude/analytics-browser';

// Note: `defaultTracking` was deprecated in Browser SDK v2.10.0; use `autocapture` instead.
amplitude.init(process.env.AMPLITUDE_API_KEY!, {
  autocapture: {
    attribution: true,          // Track marketing attribution
    pageViews: true,            // Track page views automatically
    sessions: true,             // Track session start/end
    formInteractions: true,     // Track form starts/submits
    fileDownloads: true,        // Track file downloads
    elementInteractions: false, // Track element clicks/interactions
    pageUrlEnrichment: true,    // Enrich events with page URL (useful for SPAs)
    webVitals: false,           // Track Core Web Vitals
  },
});
```

## Core Concepts

### Identify (Set User ID)
```typescript
amplitude.setUserId('usr_123');
```

### User Properties
```typescript
const identify = new amplitude.Identify();
identify.set('email', 'jane@example.com');
identify.set('role', 'admin');
identify.set('plan', 'pro');
identify.set('account_id', 'acc_456');
amplitude.identify(identify);
```

**When to call:**
- On login
- When user properties change

### Group (Account Context)
```typescript
amplitude.setGroup('account', 'acc_456');

// With group properties
const groupIdentify = new amplitude.Identify();
groupIdentify.set('name', 'Acme Corp');
groupIdentify.set('plan', 'enterprise');
amplitude.groupIdentify('account', 'acc_456', groupIdentify);
```

### Track
```typescript
amplitude.track('report.created', {
  report_id: 'rpt_789',
  report_type: 'standard',
  template_used: false
});
```

## Best Practices

### 1. Set User ID Early
```typescript
// On login
amplitude.setUserId(user.id);
amplitude.identify(new amplitude.Identify()
  .set('email', user.email)
  .set('role', user.role)
);
```

### 2. Use Groups for B2B
Amplitude Groups are essential for account-level analysis:

```typescript
amplitude.setGroup('account', user.account_id);
amplitude.groupIdentify('account', user.account_id, 
  new amplitude.Identify()
    .set('name', account.name)
    .set('plan', account.plan)
    .set('mrr', account.mrr)
);
```

### 3. Use Identify Operations Correctly
```typescript
const identify = new amplitude.Identify();

// Set — always sets the value
identify.set('role', 'admin');

// SetOnce — only sets if not already set
identify.setOnce('first_seen', new Date().toISOString());

// Add — increment numeric value
identify.add('report_count', 1);

// Append — add to array
identify.append('features_used', 'reports');
```

### 4. Event Properties vs User Properties
- **Event properties:** Specific to this event (report_id, report_type)
- **User properties:** Persist across events (role, plan)

### 5. Revenue Tracking
For billing events, use revenue tracking:

```typescript
const revenue = new amplitude.Revenue()
  .setProductId('pro_plan')
  .setPrice(99)
  .setQuantity(1);

amplitude.revenue(revenue);
```

## Group Context on Track Calls (Multi-Level Hierarchies)

Amplitude supports up to 5 group types. For B2B products with hierarchical groups (account > workspace > project), you need to:
1. Define each group type via `setGroup()` and `groupIdentify()`
2. Attribute individual track calls to specific group levels

### Defining Every Group Level

Every group level in your hierarchy needs its own `setGroup()` and `groupIdentify()` call:

```typescript
// 1. Account level
amplitude.setGroup('account', 'acc_456');
amplitude.groupIdentify('account', 'acc_456',
  new amplitude.Identify()
    .set('name', 'Acme Corp')
    .set('plan', 'enterprise')
);

// 2. Workspace level
amplitude.setGroup('workspace', 'ws_789');
amplitude.groupIdentify('workspace', 'ws_789',
  new amplitude.Identify()
    .set('name', 'Engineering')
    .set('parent_group_id', 'acc_456')
);

// 3. Project level
amplitude.setGroup('project', 'proj_123');
amplitude.groupIdentify('project', 'proj_123',
  new amplitude.Identify()
    .set('name', 'Q1 Release')
    .set('parent_group_id', 'ws_789')
);
```

### Attributing Events to Specific Group Levels

After calling `setGroup()` for multiple types, Amplitude associates the user with **all** of those groups simultaneously. Every subsequent `track()` call is attributed to all active groups.

To attribute an event to a **specific** group level (e.g., only the project, not the workspace), use the `groups` option on the track call:

```typescript
// Attribute to a specific project
amplitude.track('task.completed', {
  task_id: 'task_456'
}, {
  groups: { project: 'proj_123' }
});

// Attribute to a specific workspace
amplitude.track('workspace.settings_updated', {
  setting: 'notifications'
}, {
  groups: { workspace: 'ws_789' }
});

// Attribute to account level
amplitude.track('plan.upgraded', {
  from_plan: 'free',
  to_plan: 'pro'
}, {
  groups: { account: 'acc_456' }
});
```

### Via Segment (Destination-Specific Options)

If routing through Segment, use the Amplitude integration options:

```javascript
analytics.track('task.completed', {
  task_id: 'task_456'
}, {
  integrations: {
    Amplitude: {
      groups: { project: 'proj_123' }
    }
  }
});
```

### Important Notes

- Amplitude does **not** natively support hierarchical group rollups. Use `parent_group_id` as a group property so downstream processing can reconstruct the hierarchy.
- The `groups` option on `track()` overrides the user's current group associations for that specific event.
- Maximum 5 group types per Amplitude project.

## Session Management

Amplitude tracks sessions automatically. Default timeout: 30 minutes of inactivity.

```typescript
// Get current session ID
const sessionId = amplitude.getSessionId();

// Force new session
amplitude.setSessionId(Date.now());
```

## Common Pitfalls

### 1. Not Setting User ID
Anonymous events are hard to analyze. Set user ID on login.

### 2. Forgetting Group Context
For B2B, always call `setGroup()` after identifying the user.

### 3. Too Many User Properties
Amplitude limits user properties. Use event properties for high-cardinality data.

### 4. Not Using Identify Operations
Use `setOnce` for first-touch data, `add` for counters, `append` for lists.

### 5. Client-Side Billing Events
Track billing events server-side for accuracy:

```typescript
// Server-side
import { init, track } from '@amplitude/analytics-node';

init(process.env.AMPLITUDE_API_KEY!);

track('plan.upgraded', {
  from_plan: 'free',
  to_plan: 'pro'
}, { user_id: 'usr_123' });
```

## Debugging

### Enable Debug Mode
```typescript
amplitude.init(API_KEY, {
  logLevel: amplitude.Types.LogLevel.Debug
});
```

### Browser DevTools
Check Network tab for `api2.amplitude.com` requests.

### User Lookup
In Amplitude UI, search by user ID to see their event stream.

## Key Differences from Segment

| Segment | Amplitude |
|---------|-----------|
| `identify(userId, traits)` | `setUserId(userId)` + `identify(Identify)` |
| `group(groupId, traits)` | `setGroup(type, id)` + `groupIdentify(...)` |
| `track(event, props)` | `track(event, props)` |
| Routes to destinations | Direct to Amplitude |

## Further Documentation

This reference covers the essentials for product tracking implementation. For advanced topics, consult Amplitude's official documentation:

- **Getting Started:** https://amplitude.com/docs/getting-started
- **Browser SDK:** https://amplitude.com/docs/sdks/analytics/browser/browser-sdk-2
- **Node.js SDK:** https://amplitude.com/docs/sdks/analytics/node/node-js-sdk
- **Identify API:** https://amplitude.com/docs/apis/analytics/identify
- **Group Analytics:** https://amplitude.com/docs/sdks/analytics/browser/browser-sdk-2#user-groups
- **Revenue Tracking:** https://amplitude.com/docs/sdks/analytics/browser/browser-sdk-2#revenue-tracking
- **Amplitude Experiment (A/B Testing):** https://amplitude.com/docs/feature-experiment/overview
- **HTTP API:** https://amplitude.com/docs/apis/analytics/http-v2
