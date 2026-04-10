<!-- Last verified: 2026-03-10 against Mixpanel docs -->
# Mixpanel Implementation Guide

## Overview

Mixpanel is a product analytics platform for user behavior and journey analysis. This guide covers the base case: identifying users, associating groups, and tracking events.

## Installation

```bash
npm install mixpanel-browser
```

## Initialization

```typescript
import mixpanel from 'mixpanel-browser';

mixpanel.init('YOUR_PROJECT_TOKEN', {
  track_pageview: true,
  persistence: 'localStorage'
});
```

## Core Flow: Identify, Group, Track

### 1. Identify the User

Call on login or signup, once the user ID is known.

```typescript
mixpanel.identify('usr_123');

mixpanel.people.set({
  $email: 'jane@example.com',
  $name: 'Jane Smith',
  role: 'admin',
  plan: 'pro'
});
```

### 2. Associate User with Groups

Group Analytics is a paid add-on. Each group type (e.g. `company_id`, `workspace_id`) must first be registered as a Group Key in Mixpanel project settings.

```typescript
// Associate user with a company
mixpanel.set_group('company_id', 'acc_456');

// Associate user with multiple values for the same group type
mixpanel.set_group('company_id', ['acc_456', 'acc_789']);

// Set group profile properties
mixpanel.get_group('company_id', 'acc_456').set({
  name: 'Acme Corp',
  plan: 'enterprise',
  employees: 50
});
```

After `set_group()`, all subsequent events from this user automatically include the group association.

### 3. Track Events

```typescript
mixpanel.track('Report Created', {
  report_id: 'rpt_789',
  report_type: 'standard'
});
```

Events automatically include the user's group associations set via `set_group()`.

To attribute an event to a specific group (overriding or supplementing the user's default associations), pass the group key directly as a property:

```typescript
// Single group association
mixpanel.track('Task Completed', {
  task_id: 'task_456',
  company_id: 'acc_456'
});

// Multiple values for the same group key — use an array
mixpanel.track('Report Shared', {
  report_id: 'rpt_789',
  company_id: ['acc_456', 'acc_789', 'acc_012']
});

// Multiple group types on one event
mixpanel.track('Task Completed', {
  task_id: 'task_456',
  company_id: 'acc_456',
  workspace_id: 'ws_789'
});
```

### 4. Reset on Logout

```typescript
mixpanel.reset();  // Clears identity, super properties, and group associations
```

## Super Properties

Properties automatically added to all subsequent events:

```typescript
mixpanel.register({
  'User Role': 'admin',
  'Account Plan': 'enterprise'
});
```

## Multiple Group Types

Mixpanel supports associating events with multiple group types simultaneously. Each group type must be registered as a Group Key in project settings.

```typescript
// Associate user with groups at different levels
mixpanel.set_group('company_id', 'acc_456');
mixpanel.set_group('workspace_id', 'ws_789');
mixpanel.set_group('project_id', 'proj_123');

// Set profile properties for each group
mixpanel.get_group('company_id', 'acc_456').set({
  name: 'Acme Corp',
  plan: 'enterprise'
});

mixpanel.get_group('workspace_id', 'ws_789').set({
  name: 'Engineering',
  member_count: 12
});

mixpanel.get_group('project_id', 'proj_123').set({
  name: 'Q1 Release',
  status: 'active'
});
```

A single event can be attributed to up to 300 group keys.

**Critical limitation:** Mixpanel does NOT support group hierarchies. There is no native parent-child relationship between group types. An event attributed to `workspace_id: 'ws_789'` does NOT automatically roll up to the parent `company_id: 'acc_456'`. If you need hierarchy-aware rollups, you must either include all relevant group keys on each event or handle rollups in downstream processing.

## Node.js (Server-Side)

```typescript
import Mixpanel from 'mixpanel';

const mixpanel = Mixpanel.init('YOUR_PROJECT_TOKEN');

// Server-side requires distinct_id on every call
mixpanel.track('Report Created', {
  distinct_id: 'usr_123',
  report_id: 'rpt_789',
  company_id: 'acc_456'
});

// Set user profile
mixpanel.people.set('usr_123', {
  $email: 'jane@example.com',
  plan: 'pro'
});

// Set group profile
mixpanel.groups.set('company_id', 'acc_456', {
  name: 'Acme Corp',
  plan: 'enterprise'
});
```

## Reserved Properties

- `$email` -- User's email
- `$name` -- User's display name
- `$created` -- Account creation date

## Common Pitfalls

1. **Calling track before identify** -- Events are anonymous until identify is called
2. **Forgetting reset on logout** -- Old user context persists for the next user
3. **Assuming group hierarchy exists** -- Mixpanel has no parent-child rollup between group types
4. **Not registering Group Keys** -- Group keys must be created in project settings before data is sent
5. **Using `people.track_charge()`** -- Deprecated as of May 2025; the method is a no-op and only prints a console error

## Further Documentation

This reference covers the essentials for product tracking implementation. For advanced topics, consult Mixpanel's official documentation:

- **Getting Started:** https://docs.mixpanel.com/docs/quickstart/install-mixpanel
- **JavaScript SDK:** https://docs.mixpanel.com/docs/tracking-methods/sdks/javascript
- **Node.js SDK:** https://docs.mixpanel.com/docs/tracking-methods/sdks/nodejs
- **Identifying Users:** https://docs.mixpanel.com/docs/tracking-methods/id-management/identifying-users-simplified
- **Group Analytics:** https://docs.mixpanel.com/docs/data-structure/group-analytics
- **User Profiles:** https://docs.mixpanel.com/docs/data-structure/user-profiles
- **HTTP API:** https://docs.mixpanel.com/docs/tracking/http-api
- **Data Governance:** https://docs.mixpanel.com/docs/data-governance
