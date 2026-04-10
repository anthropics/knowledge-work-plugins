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
  api_host: 'https://app.posthog.com',  // or your self-hosted URL
  
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
  host: 'https://app.posthog.com',  // or your self-hosted URL
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

Groups enable account-level analysis for B2B.

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
```typescript
// Browser (automatically includes group after group() call)
posthog.capture('Feature Used', {
  feature: 'export'
  // Automatically includes company: acc_456
});

// Node.js (explicit groups)
posthog.capture({
  distinctId: 'usr_123',
  event: 'Feature Used',
  properties: { feature: 'export' },
  groups: { company: 'acc_456' }
});
```

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
posthog.reset();  // Clears identity
// or
posthog.reset(true);  // Also resets device ID
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
// When anonymous user signs up
posthog.alias('usr_123', posthog.get_distinct_id());
posthog.identify('usr_123');
```

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
  api_host: 'https://eu.posthog.com'
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
