# Segment Implementation Guide

## Overview

Segment is a customer data platform (CDP) that routes events to multiple destinations. It's the most common choice for companies that need to send data to multiple tools.

## SDK Options

### Browser (JavaScript)
```bash
npm install @segment/analytics-next
```

### Node.js (Server)
```bash
npm install @segment/analytics-node
```

## Core Concepts

### Identify
Associates a user with their traits:

```typescript
analytics.identify('usr_123', {
  email: 'jane@example.com',
  name: 'Jane Smith',
  role: 'admin',
  created_at: '2024-01-15T10:30:00Z'
});
```

**When to call:**
- On signup (new user)
- On login (existing user)
- When traits change

### Group
Associates a user with an account/organization:

```typescript
analytics.group('acc_456', {
  name: 'Acme Corp',
  plan: 'enterprise',
  industry: 'technology',
  employee_count: 150
});
```

**When to call:**
- After identify, when account context is known
- When account traits change
- On account switch (if multi-account)

### Track
Records an event:

```typescript
analytics.track('report.created', {
  report_id: 'rpt_789',
  report_type: 'standard',
  template_used: false
});
```

**When to call:**
- When the action happens
- After success (not on button click, but on completion)

### Page
Records a page view:

```typescript
analytics.page('Reports', 'Report Detail', {
  report_id: 'rpt_789'
});
```

**When to call:**
- On page load / route change
- Use sparingly — not every page needs tracking

## Best Practices

### 1. Identify Early
Call `identify()` as soon as you know the user. Don't wait for the first event.

### 2. Always Include User Context
Segment automatically attaches the identified user to subsequent track calls. But verify this is happening.

### 3. Group for B2B
If you have accounts, always call `group()`. This is critical for B2B analytics tools like Accoil.

### 4. Use Anonymous IDs Correctly
Segment generates an anonymous ID before identify. After identify, it merges the anonymous sessions with the known user.

```typescript
// Before login — events tracked with anonymous ID
analytics.track('page.viewed');

// On login — identify merges anonymous history
analytics.identify('usr_123', { email: 'jane@example.com' });

// After login — events associated with user
analytics.track('report.created');
```

### 5. Server-Side for Sensitive Events
Track billing and security events server-side:

```typescript
// Server-side Node.js
import { Analytics } from '@segment/analytics-node';

const analytics = new Analytics({ writeKey: process.env.SEGMENT_WRITE_KEY });

analytics.track({
  userId: 'usr_123',
  event: 'plan.upgraded',
  properties: {
    from_plan: 'free',
    to_plan: 'pro'
  }
});
```

## Common Pitfalls

### 1. Not Calling Identify
Events without identify are anonymous and hard to analyze.

### 2. Calling Identify Too Often
Once per session is usually enough. Excessive identify calls can cause issues with some destinations.

### 3. Missing Group Calls
B2B analytics tools need group context. Without it, you lose account-level insights.

### 4. PII in Event Properties
Put PII in user traits (identify), not event properties. Event properties should be IDs and metadata.

### 5. Not Flushing on Exit
Browser SDK batches calls. On page unload, flush pending events:

```typescript
window.addEventListener('beforeunload', () => {
  analytics.flush();
});
```

## Debugging

### Enable Debug Mode
```typescript
analytics.debug(true);
```

### Use the Segment Debugger
Chrome extension shows events in real-time.

### Check the Source Debugger
In Segment UI: Sources → [Your Source] → Debugger

## Destinations Setup

Common destinations for B2B SaaS:

| Destination | Purpose |
|-------------|---------|
| Amplitude | Product analytics |
| Mixpanel | Product analytics |
| Accoil | Engagement scoring |
| Intercom | Customer messaging |
| HubSpot | CRM |
| Salesforce | CRM |
| BigQuery | Data warehouse |
| Slack | Alerts |

Configure each in Segment UI. Most work automatically once events flow.
