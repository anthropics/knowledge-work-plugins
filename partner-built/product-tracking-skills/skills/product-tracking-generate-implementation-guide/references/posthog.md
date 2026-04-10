<!-- Last verified: 2026-03-10 against PostHog docs -->
# PostHog Implementation Guide

## Overview

PostHog is an open-source product analytics suite. Beyond analytics, it includes session replay, feature flags, A/B testing, and surveys. Can be self-hosted or cloud.

## SDK Options

### Browser
```bash
npm install posthog-js
```

### Node.js
```bash
npm install posthog-node
```

## Initialization

### Browser
```typescript
import posthog from 'posthog-js';

posthog.init('YOUR_API_KEY', {
  api_host: 'https://us.i.posthog.com',  // EU Cloud: 'https://eu.i.posthog.com'
  defaults: '2026-01-30',  // Sets baseline behavior versions (enables modern defaults like SPA pageview tracking)

  // Tracking options
  autocapture: true,           // Auto-track clicks, inputs, etc.
  capture_pageview: true,      // Auto-track page views
  capture_pageleave: true,     // Track when users leave
  
  // Session recording
  disable_session_recording: false,
  
  // Performance
  loaded: (posthog) => {
    // Called when SDK is ready
    if (process.env.NODE_ENV !== 'production') {
      posthog.opt_out_capturing();  // Don't track in dev
    }
  }
});
```

### Node.js
```typescript
import { PostHog } from 'posthog-node';

const posthog = new PostHog('YOUR_API_KEY', {
  host: 'https://us.i.posthog.com',  // EU Cloud: 'https://eu.i.posthog.com'
  flushAt: 20,        // Batch size
  flushInterval: 10000  // Flush every 10s
});
```

## Core Concepts

### Identify
Link anonymous user to known identity:

```typescript
// Browser
posthog.identify('usr_123', {
  email: 'jane@example.com',
  name: 'Jane Smith',
  role: 'admin',
  plan: 'pro'
});

// Node.js
posthog.identify({
  distinctId: 'usr_123',
  properties: {
    email: 'jane@example.com',
    role: 'admin'
  }
});
```

### Capture Events
```typescript
// Browser
posthog.capture('Report Created', {
  report_id: 'rpt_789',
  report_type: 'standard',
  template_used: false
});

// Node.js (distinctId required)
posthog.capture({
  distinctId: 'usr_123',
  event: 'Report Created',
  properties: {
    report_id: 'rpt_789',
    report_type: 'standard'
  }
});
```

### Set Person Properties
```typescript
// Browser - inline with capture
posthog.capture('Login', {
  $set: { last_login: new Date().toISOString() },
  $set_once: { first_login: new Date().toISOString() }
});

// Browser - standalone
posthog.setPersonProperties({
  role: 'admin',
  plan: 'pro'
});

// Browser - set once
posthog.setPersonPropertiesForFlags({
  beta_user: true
});
```

## Groups (B2B / Account Analytics)

Groups enable account-level analysis for B2B. **Note:** Group analytics is a paid add-on in PostHog.

**Key requirements:**
- Events must be **identified** to link to groups. If `$process_person_profile` is `false`, events won't link to the group.
- Individual groups require **at least one property** to appear in the PostHog People tab.
- The `name` property is special — PostHog uses it to display the group in the UI. If not set, it falls back to the group key.

### Associate User with Group
```typescript
// Browser
posthog.group('company', 'acc_456', {
  name: 'Acme Corp',
  plan: 'enterprise',
  mrr: 999,
  employees: 50
});

// Node.js
posthog.groupIdentify({
  groupType: 'company',
  groupKey: 'acc_456',
  properties: {
    name: 'Acme Corp',
    plan: 'enterprise'
  }
});
```

### Track Event with Group Context

**Browser:** The JS SDK is stateful. After calling `group()`, all subsequent `capture()` calls automatically include that group — no need to pass it again.

```typescript
// Browser (automatically includes group after group() call)
posthog.capture('Feature Used', {
  feature: 'export'
  // Automatically includes company: acc_456
});
```

**Node.js:** Backend SDKs are stateless. You must pass `groups` explicitly on every `capture()` call.

```typescript
// Node.js (explicit groups required)
posthog.capture({
  distinctId: 'usr_123',
  event: 'Feature Used',
  properties: { feature: 'export' },
  groups: { company: 'acc_456' }
});
```

### Multi-Level Group Hierarchies

For B2B products with hierarchical groups (account > workspace > project), define every group level and attribute events to the correct level.

#### Every Group Level Needs a group() Call

```typescript
// Browser: Define all levels of the hierarchy
posthog.group('company', 'acc_456', {
  name: 'Acme Corp',
  plan: 'enterprise'
});

posthog.group('workspace', 'ws_789', {
  name: 'Engineering',
  parent_group_id: 'acc_456'
});

posthog.group('project', 'proj_123', {
  name: 'Q1 Release',
  parent_group_id: 'ws_789'
});
```

```typescript
// Node.js: Define group properties
posthog.groupIdentify({
  groupType: 'company',
  groupKey: 'acc_456',
  properties: { name: 'Acme Corp', plan: 'enterprise' }
});

posthog.groupIdentify({
  groupType: 'workspace',
  groupKey: 'ws_789',
  properties: { name: 'Engineering', parent_group_id: 'acc_456' }
});

posthog.groupIdentify({
  groupType: 'project',
  groupKey: 'proj_123',
  properties: { name: 'Q1 Release', parent_group_id: 'ws_789' }
});
```

#### Attributing Events to Specific Group Levels

**Browser:** After calling `group()` for multiple types, PostHog associates the user with all active groups. Every `capture()` call is attributed to all active groups. To target a specific level, set only the desired group before the event, or use the `$groups` property:

```typescript
// Attribute to a specific project
posthog.capture('task.completed', {
  task_id: 'task_456',
  $groups: { project: 'proj_123' }
});

// Attribute to a specific workspace
posthog.capture('workspace.settings_updated', {
  setting: 'notifications',
  $groups: { workspace: 'ws_789' }
});

// Attribute to account level
posthog.capture('plan.upgraded', {
  from_plan: 'free',
  to_plan: 'pro',
  $groups: { company: 'acc_456' }
});
```

**Node.js:** Always pass `groups` explicitly on every capture call:

```typescript
// Project-level event
posthog.capture({
  distinctId: 'usr_123',
  event: 'task.completed',
  properties: { task_id: 'task_456' },
  groups: { project: 'proj_123' }
});

// Workspace-level event
posthog.capture({
  distinctId: 'usr_123',
  event: 'workspace.settings_updated',
  properties: { setting: 'notifications' },
  groups: { workspace: 'ws_789' }
});

// Account-level event
posthog.capture({
  distinctId: 'usr_123',
  event: 'plan.upgraded',
  properties: { from_plan: 'free', to_plan: 'pro' },
  groups: { company: 'acc_456' }
});
```

**Important:**
- PostHog supports up to 5 group types per project.
- Multiple groups of the same type cannot be assigned to a single event.
- PostHog does not natively support hierarchical rollups — use `parent_group_id` as a group property for downstream hierarchy reconstruction.

## Feature Flags

PostHog includes built-in feature flags.

### Check Flag (Browser)
```typescript
// Async check (recommended for server-rendered apps)
posthog.onFeatureFlags(() => {
  if (posthog.isFeatureEnabled('new-checkout')) {
    // Show new checkout
  }
});

// Sync check (flags may not be loaded yet)
if (posthog.isFeatureEnabled('new-checkout')) {
  // Show new checkout
}

// Get flag payload
const variant = posthog.getFeatureFlag('pricing-experiment');
const payload = posthog.getFeatureFlagPayload('pricing-experiment');
```

### Check Flag (Node.js)
```typescript
const isEnabled = await posthog.isFeatureEnabled('new-checkout', 'usr_123');

// With person properties for evaluation
const isEnabled = await posthog.isFeatureEnabled(
  'new-checkout',
  'usr_123',
  {
    personProperties: { plan: 'pro' },
    groupProperties: { company: { plan: 'enterprise' } }
  }
);
```

## Session Recording (Browser)

Automatically records user sessions (clicks, scrolls, inputs).

```typescript
// Enable/disable at init
posthog.init(key, {
  disable_session_recording: false
});

// Control at runtime
posthog.startSessionRecording();
posthog.stopSessionRecording();

// Check status
const isRecording = posthog.sessionRecordingStarted();
```

### Privacy Controls
```typescript
posthog.init(key, {
  session_recording: {
    maskAllInputs: true,      // Mask all input values
    maskTextSelector: '.sensitive'  // Mask specific elements
  }
});
```

## Autocapture

Automatically captures user interactions.

```typescript
posthog.init(key, {
  autocapture: true,  // Enable all
  // or granular control:
  autocapture: {
    dom_event_allowlist: ['click', 'submit'],
    element_allowlist: ['a', 'button', 'form', 'input'],
    css_selector_allowlist: ['[ph-capture]']
  }
});
```

### Exclude Elements
```html
<!-- Add data-ph-capture-attribute-* for custom properties -->
<button data-ph-capture-attribute-button-type="primary">Click</button>

<!-- Exclude from autocapture -->
<button data-ph-no-capture>Don't track me</button>
```

## Best Practices

### 1. Identify Early
```typescript
// On login
posthog.identify(user.id, {
  email: user.email,
  role: user.role
});

// Set group context
posthog.group('company', user.accountId, {
  name: account.name,
  plan: account.plan
});
```

### 2. Reset on Logout
```typescript
posthog.reset();  // Clears identity and group associations
// or
posthog.reset(true);  // Also resets device ID

// To reset only groups (keep user identity):
posthog.resetGroups();
```

### 3. Use $set and $set_once Inline
```typescript
posthog.capture('Plan Upgraded', {
  from_plan: 'free',
  to_plan: 'pro',
  $set: { plan: 'pro', upgraded_at: new Date().toISOString() },
  $set_once: { first_upgrade_date: new Date().toISOString() }
});
```

### 4. Alias for Merging Identities
```typescript
// When anonymous user signs up — link the new user ID to the anonymous ID
// alias(aliasId, distinctId) — aliasId becomes an alias for distinctId
posthog.alias('usr_123');  // Links 'usr_123' to current anonymous distinct ID
posthog.identify('usr_123');
```

**Note:** Alias is rarely needed. `identify()` automatically links anonymous and identified users in most cases. Use alias only when you need to merge two known distinct IDs (e.g., frontend ID to backend ID).

### 5. Shutdown Gracefully (Node.js)
```typescript
process.on('SIGTERM', async () => {
  await posthog.shutdown();
  process.exit(0);
});
```

## Common Pitfalls

### 1. Not Waiting for Feature Flags
Flags load async. Use `onFeatureFlags` callback.

### 2. Missing Group Context (Node.js)
Server-side, groups aren't automatic. Pass explicitly:
```typescript
posthog.capture({
  distinctId: 'usr_123',
  event: 'Event',
  groups: { company: 'acc_456' }  // Required!
});
```

### 3. Session Recording in Sensitive Areas
Disable recording on sensitive pages:
```typescript
posthog.stopSessionRecording();
```

### 4. Forgetting to Flush (Node.js)
Events are batched. Flush before exit:
```typescript
await posthog.shutdown();
```

## Debugging

### Browser Console
```typescript
posthog.debug();  // Enable debug mode
posthog.get_distinct_id();  // Current user ID
posthog.getFeatureFlags();  // All flags
```

### PostHog Activity
In PostHog dashboard: Activity → Live Events to see real-time events.

## Self-Hosted Setup

For self-hosted PostHog:

```typescript
posthog.init('your-project-key', {
  api_host: 'https://posthog.yourcompany.com'  // Your PostHog URL
});
```

## EU Cloud

```typescript
posthog.init('your-project-key', {
  api_host: 'https://eu.i.posthog.com'
});
```

## Comparison: PostHog vs Others

| Feature | PostHog | Amplitude | Mixpanel |
|---------|---------|-----------|----------|
| Open Source | ✓ | ✗ | ✗ |
| Self-Hosted | ✓ | ✗ | ✗ |
| Session Replay | ✓ Built-in | Paid add-on | ✓ |
| Feature Flags | ✓ Built-in | ✓ (Experiment) | ✗ |
| A/B Testing | ✓ Built-in | ✓ | ✗ |
| Autocapture | ✓ | ✓ | ✓ |

## Further Documentation

This reference covers the essentials for product tracking implementation. For advanced topics, consult PostHog's official documentation:

- **Getting Started:** https://posthog.com/docs/getting-started/install
- **JavaScript SDK:** https://posthog.com/docs/libraries/js
- **Node.js SDK:** https://posthog.com/docs/libraries/node
- **Identify & User Properties:** https://posthog.com/docs/product-analytics/identify
- **Group Analytics (B2B):** https://posthog.com/docs/product-analytics/group-analytics
- **Session Replay:** https://posthog.com/docs/session-replay
- **Feature Flags:** https://posthog.com/docs/feature-flags
- **A/B Testing (Experiments):** https://posthog.com/docs/experiments
- **Autocapture:** https://posthog.com/docs/product-analytics/autocapture
- **API Reference:** https://posthog.com/docs/api
- **Self-Hosting:** https://posthog.com/docs/self-host
