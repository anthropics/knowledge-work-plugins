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

Organizations, companies, or workspaces. Account traits are stable, enduring attributes that describe the organization over time. They persist across sessions and are updated infrequently -- typically when account details change or via scheduled syncs.

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

## Instance-Level Tracking (Cost Optimization)

In many B2B products, individual user identity is not needed for product analytics. The questions that matter are account-level: "Is this account adopting the feature?" not "Is this specific user adopting the feature?"

Instance-level tracking assigns a single shared user ID to all users within an account or instance. Instead of tracking each user separately, all activity is attributed to one representative identity per account.

### When to Use It

- **Products where account-level analytics are sufficient.** Most B2B tools care about account health, not individual user journeys.
- **Products with anonymous or public users.** If your product has public-facing pages or anonymous usage, roll that activity into a single anonymous identity rather than creating throwaway user records.
- **High-user-count accounts.** If accounts have hundreds or thousands of users, per-user tracking may be wasteful.
- **Privacy-sensitive contexts.** Instance-level tracking avoids storing individual user IDs, simplifying GDPR and privacy compliance.

### Cost Impact

Most analytics platforms bill by MTU (monthly tracked users). Instance-level tracking can reduce MTU counts dramatically:

| Scenario                  | Per-User MTUs | Instance-Level MTUs |
|---------------------------|---------------|---------------------|
| 100 accounts x 50 users   | 5,000         | 100                 |
| 500 accounts x 200 users  | 100,000       | 500                 |

This is often a 95%+ reduction in MTU-based billing.

**Important caveat:** Some platforms (like Segment) also apply quotas based on event volume per MTU. Reducing MTUs does not help if event volume per identity is very high. Factor in both dimensions.

### Implementation Pattern

Use the account or instance identifier as the user ID for all analytics calls:

```javascript
// Instead of per-user identity
analytics.identify(user.id, { ... });

// Use account/instance identity
analytics.identify(account.cloudId || account.id, { ... });
```

This can be made configurable so you can switch between per-user and instance-level tracking without code changes.

### What You Keep

- Feature usage at the account level
- Workflow and adoption metrics
- Subscription and licensing context
- Object counts via snapshot metrics

### What You Give Up

- Individual user journeys and funnels
- Per-user segmentation (by role, tenure, etc.)
- User-level cohort analysis

### Decision Framework

Ask: "Do our product questions require knowing *which user* did something, or just *which account*?"

If the answer is account, use instance-level tracking. You can always switch to per-user later if needs change — the reverse (rolling up after the fact) is harder.

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

### Per-User Tracking When Account-Level Would Suffice
If your product analytics are account-level ("Is Acme Corp adopting this feature?"), tracking every individual user inflates MTU costs for no analytical benefit. Consider instance-level tracking (see above).
