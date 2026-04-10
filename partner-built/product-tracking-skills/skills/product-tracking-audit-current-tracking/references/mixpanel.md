# Mixpanel Implementation Guide

## Overview

Mixpanel is a product analytics platform focused on user behavior and journey analysis. Known for powerful funnel and cohort analysis with intuitive query building.

## SDK Options

### Browser
```html
<!-- CDN (simplest) -->
<script src="https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js"></script>
```

```bash
# NPM
npm install mixpanel-browser
```

### Node.js
```bash
npm install mixpanel
```

## Initialization

### Browser
```typescript
import mixpanel from 'mixpanel-browser';

mixpanel.init('YOUR_PROJECT_TOKEN', {
  track_pageview: true,           // Auto-track page views
  persistence: 'localStorage',     // or 'cookie'
  api_host: 'https://api.mixpanel.com',  // or api-eu.mixpanel.com
  debug: process.env.NODE_ENV !== 'production'
});
```

### Node.js
```typescript
import Mixpanel from 'mixpanel';

const mixpanel = Mixpanel.init('YOUR_PROJECT_TOKEN', {
  host: 'api.mixpanel.com',  // or api-eu.mixpanel.com
  debug: process.env.NODE_ENV !== 'production',
  geolocate: false  // Prevent server IP geolocation
});
```

## Core Concepts

### Identify
Link events to a specific user:

```typescript
// Browser
mixpanel.identify('usr_123');

// After identify, set user profile properties
mixpanel.people.set({
  $email: 'jane@example.com',
  $name: 'Jane Smith',
  role: 'admin',
  plan: 'pro'
});
```

**When to call:**
- On login
- On signup (after user ID is known)
- When switching users (call reset first)

### Track Events
```typescript
// Browser
mixpanel.track('Report Created', {
  report_id: 'rpt_789',
  report_type: 'standard',
  template_used: false
});

// Node.js (requires distinct_id)
mixpanel.track('Report Created', {
  distinct_id: 'usr_123',
  report_id: 'rpt_789',
  report_type: 'standard'
});
```

### Super Properties (Browser)
Properties automatically added to all subsequent events:

```typescript
// Set super properties
mixpanel.register({
  'User Type': 'Pro',
  'Account ID': 'acc_456'
});

// Set only if not already set
mixpanel.register_once({
  'First Visit Date': new Date().toISOString()
});

// Remove a super property
mixpanel.unregister('Account ID');
```

### User Profile Properties
```typescript
// Set properties (overwrites existing)
mixpanel.people.set({
  $email: 'jane@example.com',
  plan: 'pro'
});

// Set only if not already set
mixpanel.people.set_once({
  'First Login': new Date().toISOString()
});

// Increment numeric values
mixpanel.people.increment('login_count', 1);

// Append to list
mixpanel.people.append('features_used', 'reports');

// Union (add unique values to list)
mixpanel.people.union('tags', ['power_user']);
```

### Time Events
Measure duration between actions:

```typescript
// Start timing
mixpanel.time_event('Checkout');

// ... user completes checkout ...

// Complete (automatically includes 'Duration' property)
mixpanel.track('Checkout', {
  items: 3,
  total: 99.99
});
```

## B2B / Group Analytics

Group Analytics is a paid add-on. Enables account-level analysis.

### Associate User with Group
```typescript
// Browser
mixpanel.set_group('company', 'acc_456');

// Multiple groups
mixpanel.set_group('company', ['acc_456', 'acc_789']);

// Remove from group
mixpanel.remove_group('company', 'acc_789');
```

### Set Group Properties
```typescript
// Browser
mixpanel.get_group('company', 'acc_456').set({
  name: 'Acme Corp',
  plan: 'enterprise',
  mrr: 999,
  employees: 50
});

// Set once
mixpanel.get_group('company', 'acc_456').set_once({
  'First Event': new Date().toISOString()
});

// Node.js
mixpanel.groups.set('company', 'acc_456', {
  name: 'Acme Corp',
  plan: 'enterprise'
});
```

### Track Event with Group
```typescript
// Events automatically include group context after set_group
mixpanel.track('Feature Used', {
  feature: 'export',
  // Automatically includes company: acc_456
});
```

## Best Practices

### 1. Identify Before Tracking
```typescript
// On login
mixpanel.identify(user.id);
mixpanel.people.set({
  $email: user.email,
  $name: user.name,
  role: user.role
});

// Then track
mixpanel.track('Session Started');
```

### 2. Use Super Properties for Context
```typescript
// After login, register persistent context
mixpanel.register({
  'User Role': user.role,
  'Account Plan': account.plan,
  'Account ID': account.id
});

// All subsequent tracks include this context
mixpanel.track('Report Created'); // Includes role, plan, account
```

### 3. Reset on Logout
```typescript
mixpanel.reset();  // Clears identity and super properties
```

### 4. Reserved Properties
Use `$` prefix for Mixpanel's reserved properties:
- `$email` — User's email
- `$name` — User's display name
- `$phone` — Phone number
- `$created` — Account creation date
- `$city`, `$region`, `$country` — Location (auto-filled from IP)

### 5. Historical Data Import (Node.js)
For events older than 5 days, use `import` instead of `track`:

```typescript
mixpanel.import('Historical Event', new Date('2023-01-15'), {
  distinct_id: 'usr_123',
  property: 'value'
});
```

## Server-Side Considerations

### Disable Geolocation
Server requests use server IP, not user IP:

```typescript
const mixpanel = Mixpanel.init(token, {
  geolocate: false
});

// Or per-request
mixpanel.track('Event', {
  distinct_id: 'usr_123',
  ip: '0'  // Disable geolocation for this event
});
```

### Pass User IP (if known)
```typescript
mixpanel.track('Event', {
  distinct_id: 'usr_123',
  ip: req.ip  // Pass client IP
});
```

## Autocapture (Browser)

Enable automatic event capture:

```typescript
mixpanel.init(token, {
  autocapture: {
    pageview: true,
    click: true,
    input: true,
    submit: true
  }
});

// Exclude specific elements
// Add class 'mp-no-track' to exclude from tracking
// Add class 'mp-exclude' to exclude from all tracking (including as parent)
```

## Common Pitfalls

### 1. Calling Track Before Identify
Events tracked before identify are anonymous. Call identify first.

### 2. Not Using Super Properties
Leads to repetitive property inclusion and potential inconsistency.

### 3. Forgetting Reset on Logout
Old user context persists for new user if you don't reset.

### 4. Server IP Geolocation
All users appear in your server's location. Disable geolocation server-side.

### 5. Too Many User Properties
Mixpanel limits properties. Use event properties for high-cardinality data.

## Debugging

### Enable Debug Mode
```typescript
// Browser
mixpanel.init(token, { debug: true });

// Node.js
const mixpanel = Mixpanel.init(token, { debug: true });
```

### Browser Console
```typescript
mixpanel.get_distinct_id();  // Check current user ID
mixpanel.get_property('$user_id');  // Check specific property
```

### Mixpanel Live View
In Mixpanel dashboard: Activity → Live View to see events in real-time.

## EU/India Data Residency

```typescript
// Browser - EU
mixpanel.init(token, {
  api_host: 'https://api-eu.mixpanel.com'
});

// Node.js - EU
const mixpanel = Mixpanel.init(token, {
  host: 'api-eu.mixpanel.com'
});

// India
const mixpanel = Mixpanel.init(token, {
  host: 'api-in.mixpanel.com'
});
```
