# B2B SaaS Specification

Best practices for B2B product telemetry, synthesized from industry standards.

## The B2B Difference

B2B SaaS is fundamentally different from B2C:

| Aspect | B2C | B2B |
|--------|-----|-----|
| Primary entity | User | Account |
| Decision maker | Same as user | Different from user |
| Success metric | User engagement | Account health |
| Churn unit | User | Account (with users) |
| Value | Individual | Collective |

**Implication:** Every event needs user AND account context.

## The Two-Entity Model

### Users

Individual humans using your product. User traits are stable, enduring attributes that persist across events and sessions, building a comprehensive profile over time. They are critical for segmentation, personalization, and targeted communication.

**Required traits:**
- `user_id` — Stable identifier
- `email` — For identity resolution
- `account_id` — Which account they belong to
- `role` — Their role in the account

**Recommended traits:**
- `created_at` — When they signed up
- `last_active_at` — Recent engagement
- `subscription_level` — Current subscription tier
- `preferred_language` — Language preference for communication
- `last_login` — Date/time of most recent login
- `industry` — Industry the user's organization operates in

### Accounts

Organizations, companies, or workspaces. Account traits are stable, enduring attributes that persist across sessions and describe the organization over time. They are critical for segmentation, account health analysis, and targeted communication.

**Required traits:**
- `account_id` — Stable identifier
- `name` — Account name
- `plan` — Current pricing plan

**Recommended traits:**
- `created_at` — When account was created
- `mrr` — Monthly recurring revenue
- `employee_count` — Company size
- `industry` — Vertical
- `number_of_users` — Total users associated with the account
- `billing_cycle` — Billing frequency (`monthly`, `annual`)
- `support_level` — Support tier (`standard`, `priority`)

## Core B2B Events

These events should exist in every B2B SaaS tracking plan.

### Account Lifecycle

| Event | When | Key Properties |
|-------|------|----------------|
| `account.created` | New account/org created | `account_name`, `created_by` |

### User Lifecycle

| Event | When | Key Properties |
|-------|------|----------------|
| `user.signed_up` | User creates account | `signup_source`, `account_id` |
| `user.signed_in` | User logs in | `method` |
| `user.signed_out` | User logs out | — |
| `user.invited` | User invites someone | `invitee_role`, `invitee_email` (hashed) |
| `user.joined` | Invited user joins | `invitation_id`, `role` |

Note: "Activation" is a computed state defined in downstream analytics tools, not an event. Track the actions that might constitute activation (core value events, integrations connected, etc.) and let analytics define what combination means "activated."

### Billing

| Event | When | Key Properties |
|-------|------|----------------|
| `trial.started` | Trial begins | `trial_days`, `plan_trialing` |
| `trial.ended` | Trial ends | `converted`, `plan_selected` |
| `plan.upgraded` | Account upgrades | `from_plan`, `to_plan` |
| `plan.downgraded` | Account downgrades | `from_plan`, `to_plan`, `reason` |

## Group Calls Are Mandatory

In B2B, you MUST call `group()` to associate users with accounts.

```javascript
// After identify, always group
analytics.identify('usr_123', { email: 'jane@example.com' });
analytics.group('acc_456', { name: 'Acme Corp', plan: 'pro' });
```

Without group calls:
- Account-level analysis is impossible
- B2B analytics tools (like Accoil) can't function
- You lose the most important dimension

## Group Calls for Every Level in the Hierarchy

Many B2B products have more structure than a single account. If your product has workspaces, projects, instances, or other nested entities, you need a `group()` call for **every level** — not just the top-level account.

### Why Every Level Needs group()

- Each group must exist in your analytics tool before events can reference it
- The `parent_group_id` trait establishes the hierarchy so rollups work
- Without group calls at every level, events attributed to sub-account groups will be orphaned

### Example: Account > Workspace > Project

```javascript
// 1. Account (top level) — always required
analytics.group('acc_456', {
  name: 'Acme Corp',
  group_type: 'account',
  plan: 'enterprise'
});

// 2. Workspace (child of account)
analytics.group('ws_789', {
  name: 'Engineering',
  group_type: 'workspace',
  parent_group_id: 'acc_456'
});

// 3. Project (child of workspace)
analytics.group('proj_123', {
  name: 'Q1 Release',
  group_type: 'project',
  parent_group_id: 'ws_789'
});
```

### When to Call group() for Sub-Account Levels

- **On login** — Establish all groups the user has access to
- **On context switch** — When user navigates to a different workspace or project
- **On entity creation** — When a new workspace or project is created
- **On trait change** — When group properties change (name, status, etc.)

## Track Calls Need Group Context

Every `track()` call should include the group ID for the level where the event occurred. This is how analytics tools attribute the event to the correct group.

### The Pattern

```javascript
// Segment / Accoil: use context.groupId
analytics.track('task.completed', { task_id: 'task_456' }, {
  context: { groupId: 'proj_123' }
});

// Amplitude: use groups option
amplitude.track('task.completed', { task_id: 'task_456' }, {
  groups: { project: 'proj_123' }
});

// Mixpanel: use $groups property
mixpanel.track('task.completed', {
  task_id: 'task_456',
  $groups: { project: 'proj_123' }
});

// PostHog: use groups option (Node.js) or $groups property (browser)
posthog.capture({
  distinctId: 'usr_123',
  event: 'task.completed',
  properties: { task_id: 'task_456' },
  groups: { project: 'proj_123' }
});
```

### Match the Tracking Plan's group_level

The tracking plan assigns each event to a `group_level`. The implementation must carry that through:

| Event | group_level | groupId to use |
|-------|-------------|----------------|
| `task.completed` | project | `proj_123` |
| `workspace.settings_updated` | workspace | `ws_789` |
| `plan.upgraded` | account | `acc_456` |

## Multi-Account Users

Some B2B products allow users to belong to multiple accounts.

**Handling options:**

1. **Primary account model:** User has one primary account, can access others
   - Store `primary_account_id` as user trait
   - Include `account_id` on every event for current context

2. **Context switching:** User switches between accounts
   - Track `account.switched` event
   - Always include current `account_id` on events

3. **Always include account:** Regardless of model, every event needs account context

## Properties Standard

### On Every Event

Include on every track call:
- `user_id` — Who did it
- `account_id` — Which account (via context or property)
- `timestamp` — When (usually auto-added)

### Account Context via SDK

Most CDPs/SDKs support account context:

**Segment:**
```javascript
analytics.track('report.created', {
  report_id: 'rpt_123'
}, {
  context: { groupId: 'acc_456' }
});
```

**Amplitude:**
```javascript
amplitude.setGroup('account', 'acc_456');
amplitude.track('report.created', { report_id: 'rpt_123' });
```

## Anti-Patterns in B2B

### Ignoring Account Context
Every event without account context is a lost opportunity.

### User-Centric Analysis Only
Don't just count users. Count accounts and users per account.

### Missing Collaboration Events
In B2B, multiple users = higher stickiness. Track invites, shares, collaborations.

### No Billing Signals
Commercial events (trials, upgrades, limit reached) are critical for revenue analysis.

### Treating All Users Equally
Roles matter. Admin actions vs member actions have different weights.
