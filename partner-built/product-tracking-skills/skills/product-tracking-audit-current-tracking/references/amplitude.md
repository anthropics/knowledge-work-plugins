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

amplitude.init(process.env.AMPLITUDE_API_KEY!, {
  defaultTracking: {
    sessions: true,        // Track session start/end
    pageViews: true,       // Track page views automatically
    formInteractions: true, // Track form starts/submits
    fileDownloads: true,   // Track file downloads
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
import { Amplitude } from '@amplitude/analytics-node';

const amplitude = new Amplitude(process.env.AMPLITUDE_API_KEY!);

amplitude.track('plan.upgraded', {
  user_id: 'usr_123',
  from_plan: 'free',
  to_plan: 'pro'
});
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
