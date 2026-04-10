# Identity and Group Calls

How to properly identify users and associate them with accounts (and other group levels).

> **For hierarchical group structures** (workspaces, projects, etc.), see [Group Hierarchy](group-hierarchy.md) for detailed guidance on tracking events at the correct level.

## The Identify Call

Identify calls link user actions to a unique identifier and assign traits to that user.

### When to Call Identify

- **User signup:** Immediately after a user is created
- **User login:** At session start to associate subsequent events
- **Trait changes:** When user information changes (role, name, etc.)

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | String | Unique identifier for the user. **Required.** |
| `timestamp` | String | ISO 8601 or Unix timestamp |

### Recommended Traits

Traits are stable, enduring attributes that persist across events and sessions. Unlike event properties that capture moment-to-moment context, user traits build a comprehensive profile over time. They change infrequently and are critical for segmentation, personalization, and targeted communication.

| Trait | Recommendation | Description |
|-------|----------------|-------------|
| `email` | Highly recommended | Universal identifier across platforms |
| `name` | Highly recommended | Full name for personalized interfaces |
| `created_at` | Highly recommended | Signup date for tenure tracking |
| `role` | Highly recommended | User's role in account (Admin, Member, etc.) |
| `subscription_level` | Recommended | Current subscription tier (free, premium, enterprise) |
| `preferred_language` | Recommended | Language preference for communication |
| `last_login` | Recommended | Date/time of most recent login |
| `industry` | Recommended | Industry the user's organization operates in |

### Example

```javascript
identify('usr_12345', {
  email: 'jane@example.com',
  name: 'Jane Smith',
  created_at: '2024-08-01',
  role: 'Admin',
  subscription_level: 'pro',
  preferred_language: 'English'
});
```

### Best Practices

1. **Always include user_id** — Anonymous tracking is not supported in most B2B analytics tools
2. **Use consistent timestamps** — ISO 8601 preferred
3. **Update traits when they change** — Role changes, subscription changes, etc.
4. **Identify before tracking** — Ensures all events are associated with the correct user

---

## The Group Call

Group calls associate users with accounts and define account-level traits. Essential for B2B.

### When to Call Group

- **Account creation:** Link the creating user and set initial traits
- **User joins account:** Associate user with their account
- **Account changes:** Subscription status, plan, MRR updates
- **At login:** Ensure account context for subsequent events

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `group_id` | String | Unique identifier for the account. **Required.** |
| `user_id` | String | User being associated with the account |
| `timestamp` | String | ISO 8601 or Unix timestamp |

### Recommended Traits

Account traits are stable attributes that describe the organization over time. They persist across sessions and are updated infrequently -- typically when account details change (plan upgrade, billing change) or via scheduled syncs for computed values.

| Trait | Recommendation | Description |
|-------|----------------|-------------|
| `name` | **Highly recommended** | Account name. Without this, accounts display as numeric IDs. |
| `created_at` | Highly recommended | Account creation date for tenure calculation |
| `status` | Highly recommended | Subscription status: `trial`, `paid`, `canceled` |
| `plan` | Highly recommended | Plan tier: `starter`, `pro`, `enterprise` |
| `mrr` | Recommended | Monthly recurring revenue (in cents) |
| `industry` | Recommended | Vertical the account operates in |
| `employee_count` | Recommended | Company size for segmentation |
| `number_of_users` | Recommended | Total users associated with the account |
| `billing_cycle` | Recommended | Billing frequency: `monthly`, `annual` |
| `support_level` | Recommended | Support tier: `standard`, `priority` |

### Example

```javascript
group('acc_67890', {
  name: 'Acme Corp',
  status: 'paid',
  plan: 'enterprise',
  mrr: 100000,  // $1,000 in cents
  created_at: '2023-01-15',
  industry: 'technology',
  employee_count: 150,
  billing_cycle: 'annual'
});
```

### Best Practices

1. **Always include group_id** — Without it, account-level analysis is impossible
2. **Always include name** — Otherwise accounts are just meaningless IDs
3. **Use the same ID as other tools** — Match HubSpot, Intercom, Salesforce IDs for cross-platform consistency
4. **Update traits when they change** — Plan upgrades, MRR changes, etc.
5. **Call group after identify** — User context should exist first

---

## Hierarchical Groups

Most B2B products have more structure than a single "account." Activity happens inside nested entities like workspaces, projects, or teams.

### Defining Group Hierarchy

When your product has multiple levels, define each group with a `parent_group_id`:

```javascript
// Account (top level)
group("acc_456", {
  group_type: "account",
  name: "Acme Inc"
});

// Workspace (child of account)
group("ws_789", {
  group_type: "workspace",
  name: "Engineering",
  parent_group_id: "acc_456"
});

// Project (child of workspace)
group("proj_123", {
  group_type: "project",
  name: "Q1 Release",
  parent_group_id: "ws_789"
});
```

### Attributing Events to Groups

Each event should be attributed to the **most specific group** where it occurred.

**Accoil (recommended):**
```javascript
track("Task Completed", {
  task_id: "task_456"
}, {
  context: {
    groupId: "proj_123"  // Capital I in groupId
  }
});
```

**Amplitude:**
```javascript
track("Task Completed", {
  task_id: "task_456"
}, {
  integrations: {
    Amplitude: {
      groups: { project: "proj_123" }
    }
  }
});
```

**Mixpanel:**
```javascript
mixpanel.track("Task Completed", {
  task_id: "task_456",
  $groups: { project: "proj_123" }
});
```

**PostHog (Browser):**
```javascript
posthog.capture("Task Completed", {
  task_id: "task_456",
  $groups: { project: "proj_123" }
});
```

**PostHog (Node.js):**
```javascript
posthog.capture({
  distinctId: "usr_123",
  event: "Task Completed",
  properties: { task_id: "task_456" },
  groups: { project: "proj_123" }
});
```

**Segment:**
```javascript
analytics.track("Task Completed", {
  task_id: "task_456"
}, {
  context: { groupId: "proj_123" }
});
```

### Every Group Level Needs Its Own group() Call

Before referencing a group ID in track calls, that group must be established via `group()`. For hierarchical products, this means issuing a `group()` call for **every** level:

```javascript
// All three levels must exist before events reference them
group("acc_456", { group_type: "account", name: "Acme Inc" });
group("ws_789", { group_type: "workspace", name: "Engineering", parent_group_id: "acc_456" });
group("proj_123", { group_type: "project", name: "Q1 Release", parent_group_id: "ws_789" });
```

Call `group()` for each level on login, on context switch (user opens a different workspace), on entity creation, and when group traits change.

### Why Specificity Matters

- **Track at project level** → Metrics roll up to workspace and account automatically
- **Track only at account level** → No visibility into which workspace/project is engaged

Analytics tools can roll metrics **up** the hierarchy. They cannot break them **down** if you only track at higher levels.

> See [Group Hierarchy](group-hierarchy.md) for comprehensive documentation.

---

## Client-Side vs Server-Side

**Critical distinction:** Client-side and server-side SDKs handle identity differently.

### Client-Side (Browser/Mobile)

Segment and similar SDKs **maintain state**. Once you call identify/group, subsequent track calls automatically include the userId:

```javascript
// On login — call once
analytics.identify('usr_123', { email: 'jane@example.com' });
analytics.group('acc_456', { name: 'Acme Corp' });

// Later — userId is automatic
analytics.track('Report Created', { report_id: 'rpt_789' });
```

**You don't need to bundle on every event.** Just call identify/group when:
- User logs in
- User traits change
- Account traits change

### Server-Side (Node/Backend)

Server-side SDKs are **stateless**. You must pass userId on every call:

```javascript
analytics.track({
  userId: 'usr_123',  // Required
  event: 'Report Created',
  properties: { report_id: 'rpt_789' }
});
```

**Options:**
1. Pass userId on every track (simplest)
2. Identify/group on login, then track with userId only
3. Bundle identify + group + track on every call (overkill for most cases)

---

## Instance-Level vs User-Level Tracking

In some B2B scenarios, you may want to track at the account level rather than individual users.

### User-Level Tracking (Default)

- Each user has unique `user_id`
- Full user-level visibility
- Higher MTU costs
- More GDPR complexity

### Instance-Level Tracking

- All users in an account share the same `user_id` (typically the `account_id`)
- One "user" per account
- 90%+ reduction in MTU costs
- Simpler privacy posture

**When to use instance-level:**
- Privacy is paramount
- You don't need user-level segmentation
- Cost efficiency matters more than individual tracking
- Team/org level insights are sufficient

**Trade-offs:**
- Can't see which user did what
- Can't segment by user role
- No user-specific funnels

### Implementation

```javascript
function getUserId(context) {
  if (INSTANCE_LEVEL_TRACKING) {
    return context.accountId;  // All users share account ID
  }
  return context.userId;  // Default: per-user
}
```

---

## Handling Public/Anonymous Users

For products with public-facing usage (portals, forms, etc.), avoid tracking each anonymous user separately.

### The Problem

- Thousands of public users = thousands of MTUs
- Inflates analytics costs
- Pollutes data with anonymous IDs

### The Solution

Track all public user events under a shared instance ID:

```javascript
function trackPublicAction(accountId, event, properties) {
  track(event, {
    ...properties,
    user_id: accountId,  // Shared ID, not individual
    is_public_user: true  // Tag for filtering
  });
}
```

### Benefits

- **Reduces MTUs** — Shared ID prevents thousands of tracked users
- **Maintains visibility** — Still capture usage signals
- **Easy to segment** — Filter by `is_public_user` when needed
- **Privacy-safe** — No individual PII for anonymous users
