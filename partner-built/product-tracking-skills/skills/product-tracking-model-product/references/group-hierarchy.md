# Tracking Events at the Group Level

Most B2B SaaS products have more structure than a single "account." Activity happens inside nested entities like organizations, instances, products, workspaces, projects, or teams.

Group-level event tracking captures **where activity occurs** inside these structures, so you can:
- Measure engagement accurately at each level
- Roll metrics up cleanly to parent entities
- Avoid misleading analytics from over-aggregation

This guide explains:
- Why group-level event tracking matters
- How multi-level product structures work
- How to attach events to the correct group
- SDK/platform support for hierarchical groups

---

## Why Track Events at the Group Level?

In B2B products, a single user often:
- Belongs to multiple workspaces or projects
- Performs actions in different contexts
- Has both end-user actions and admin-level actions

If events are only tracked at the user or account level, you lose critical context:
- Which workspace was active?
- Which project or product is being adopted?
- Where is engagement strong or weak?

By tracking events at the group level, analytics tools can answer questions like:
- "Which workspaces are healthy vs at risk?"
- "Which projects are driving most usage?"
- "Is adoption strong in one product but weak in another?"
- "Are admins active at the instance level, but teams inactive in workspaces?"

---

## Products Naturally Have Multiple Levels

Most B2B SaaS products form a hierarchy of groups. This is normal and expected.

### Example Hierarchies

**Atlassian**
```
Customer
└── Instance
    └── Product
        └── Project
```

**Accoil**
```
Customer Account
└── Product
    └── Workspace
```

**Slack**
```
Enterprise Org
└── Workspace
    └── Channel
```

**Generic SaaS**
```
Account
└── Workspace
    └── Project
        └── Resource
```

Each level represents a group where activity can occur.

> **Key idea:** Every event happens in a specific group context, even if that group is not always the lowest level.

---

## Core Principle: One Event, One Group

Each event is attributed to a **single group**. That group should represent where the event occurred.

- The group can be a workspace, project, product, instance, or account
- Analytics tools use group relationships to derive higher-level attribution automatically
- You do not need to attach multiple group IDs to an event

---

## Defining Your Group Hierarchy

Before tracking events, you need to define the objects in your product. Each group:
- Has a globally unique `groupId`
- Represents a real entity in your product
- Includes a reference to its parent group via `parent_group_id`

### Example: Atlassian-Style Hierarchy

```javascript
// Account (top level)
analytics.group("account_456", {
  group_type: "account",
  name: "Acme Inc"
});

// Instance
analytics.group("instance_abc", {
  group_type: "instance",
  domain: "abc.atlassian.net",
  parent_group_id: "account_456"
});

// Product
analytics.group("product_jira", {
  group_type: "product",
  product_key: "jira",
  parent_group_id: "instance_abc"
});

// Project (lowest level)
analytics.group("project_PROJ", {
  group_type: "project",
  project_key: "PROJ",
  parent_group_id: "product_jira"
});
```

The `parent_group_id` relationship allows analytics tools to understand the full hierarchy and roll activity upward automatically.

---

## Tracking Events with Group Context

When sending events, include the group where the event took place.

### Accoil: Use `context.groupId`

```json
{
  "type": "track",
  "event": "View Form",
  "userId": "2697241129",
  "context": {
    "groupId": "ws_2251430565_001"
  },
  "timestamp": "2021-06-01T12:29:13.481+00:00"
}
```

In this example:
- The event occurred inside a workspace
- Accoil attributes the event to that workspace
- Accoil then rolls the event up to its parent product and account automatically

### Amplitude: Use `groups` Property

```javascript
analytics.track("View Form", {
  formId: "form_123"
}, {
  integrations: {
    Amplitude: {
      groups: {
        workspace: "ws_2251430565_001"
      }
    }
  }
});
```

### Mixpanel: Pass Group Key as Event Property

In Mixpanel, the group key name (e.g. `workspace_id`) is passed directly as an event property. If the user has been associated with groups via `set_group()`, those group keys are included automatically. You can also pass them explicitly:

```javascript
// Single group association
mixpanel.track("View Form", {
  formId: "form_123",
  company_id: "acc_456"
});

// Multiple values for the same group key — use an array
mixpanel.track("Report Shared", {
  formId: "form_123",
  company_id: ["acc_456", "acc_789", "acc_012"]
});

// Multiple group types on one event
mixpanel.track("Task Completed", {
  task_id: "tsk_123",
  company_id: "acc_456",
  workspace_id: "ws_001"
});
```

### PostHog: Use `$groups` Property (Browser) or `groups` Option (Node.js)

**Browser:**
```javascript
posthog.capture("View Form", {
  formId: "form_123",
  $groups: {
    workspace: "ws_2251430565_001"
  }
});
```

**Node.js:**
```javascript
posthog.capture({
  distinctId: "2697241129",
  event: "View Form",
  properties: { formId: "form_123" },
  groups: { workspace: "ws_2251430565_001" }
});
```

### Segment: Use `context.groupId`

```javascript
analytics.track("View Form", {
  formId: "form_123"
}, {
  context: { groupId: "ws_2251430565_001" }
});
```

---

## Every Group Level Needs a group() Call

Before attributing events to groups, each group in the hierarchy must be established with its own `group()` call. This is true for **every** level — not just the top-level account.

### Why This Is Required

- Analytics tools cannot attribute events to groups that do not exist
- The `parent_group_id` trait on each group establishes the parent-child relationship
- Without group calls at every level, rollups will not work and events will be orphaned

### When to Issue group() Calls

| Trigger | What to Do |
|---------|------------|
| **User login** | Call group() for every level the user has access to |
| **Context switch** | Call group() when user navigates to a different workspace or project |
| **Entity creation** | Call group() when a new workspace, project, or instance is created |
| **Trait change** | Call group() when group properties change (plan upgrade, name change, etc.) |

### Example: Full Hierarchy Setup

```javascript
// On login or context entry, establish all levels:

// 1. Account (top level)
analytics.group("acc_456", {
  group_type: "account",
  name: "Acme Inc",
  plan: "enterprise"
});

// 2. Instance (child of account)
analytics.group("instance_abc", {
  group_type: "instance",
  domain: "abc.atlassian.net",
  parent_group_id: "acc_456"
});

// 3. Product (child of instance)
analytics.group("product_jira", {
  group_type: "product",
  product_key: "jira",
  parent_group_id: "instance_abc"
});

// 4. Project (child of product)
analytics.group("project_PROJ", {
  group_type: "project",
  project_key: "PROJ",
  parent_group_id: "product_jira"
});

// Now track calls can reference any of these group IDs
```

---

## Be As Specific As Possible

**Best practice:** Attach events to the most specific (lowest-level) group available.

### Why This Matters

- Accurate workspace and project engagement metrics
- Clean rollups to products and accounts
- No double counting
- Maximum flexibility for filtering, scoring, and segmentation

Analytics tools can always roll metrics **up** the hierarchy. They cannot reliably break them **down** if events are only tracked at higher levels.

### Example: Project-Level Event

```json
{
  "event": "Task Completed",
  "context": {
    "groupId": "project_PROJ"
  }
}
```

This event contributes to:
- Project-level metrics ✓
- Product-level metrics (via rollup) ✓
- Instance-level metrics (via rollup) ✓
- Account-level metrics (via rollup) ✓

---

## When Higher-Level Grouping Is Correct

Not all events belong at the lowest level. Examples:
- Admin settings changed at the instance level
- Billing updates at the account level
- Product-wide configuration changes

In these cases, attach the event to the most specific group that makes sense:

```json
{
  "event": "Instance Setting Updated",
  "userId": "2697241129",
  "context": {
    "groupId": "instance_abc"
  }
}
```

This event contributes to:
- Instance-level metrics ✓
- Account-level metrics (via rollup) ✓

It does **not** affect workspace or project engagement, which is intentional.

---

## Users and Top-Level Association

Analytics tools (like Accoil) automatically associate users to their top-level group based on the groups they interact with. You do not need to explicitly set a primary group on user identification.

This ensures:
- All activity is anchored to the correct customer
- Account-level analytics remain complete
- Group-level metrics remain clean and well-scoped

---

## SDK/Platform Support for Group Hierarchy

| Platform | User-Group Association | Event-Group Association | Hierarchical Groups |
|----------|------------------------|-------------------------|---------------------|
| **Accoil** | ✓ via group() | ✓ via context.groupId | ✓ Full support with parent_group_id |
| **Amplitude** | ✓ via identify groups | ✓ via groups property | ⚠️ Limited — up to 5 group types, no native hierarchy |
| **Mixpanel** | ✓ via set_group | ✓ via group key property | ✗ No hierarchy — multiple group types supported but no parent-child rollup |
| **Segment** | ✓ via group() | ✗ Not supported | ✗ No native hierarchy |
| **RudderStack** | ✓ via group() | ✗ Not supported | ✗ No native hierarchy |
| **PostHog** | ✓ via group() | ✓ via $groups | ⚠️ Limited — max 5 group types |

### Implications for Tracking Plan Design

1. **If using Accoil:** Full hierarchy support. Define parent_group_id relationships and use context.groupId on events.

2. **If using Amplitude:** Can associate events with groups (up to 5 group types), but hierarchy must be modeled via group properties (parent_group_id trait). Rollups require custom setup.

3. **If using Mixpanel:** Can associate events with multiple group types simultaneously (up to 300 group keys per event). However, Mixpanel has NO hierarchy support -- events attributed to a workspace do NOT automatically roll up to a parent account. You must either include all relevant group keys on each event or handle rollups downstream.

4. **If using Segment/RudderStack only:** Cannot associate individual events with groups — only users. Consider routing through a tool that supports event-level groups.

---

## Discovery Questions for Group Hierarchy

When discovering a product's structure, ask:

1. **"What are the main objects or containers in your product?"**
   - Accounts, organizations, workspaces, projects, teams, channels?

2. **"How do these objects relate to each other?"**
   - Draw the hierarchy: Account → Workspace → Project?
   - Can a lower-level object belong to multiple parents?

3. **"Where do most user actions happen?"**
   - At the project level? Workspace level?
   - This is typically the "default" group for events.

4. **"Are there admin actions that happen at higher levels?"**
   - Instance settings, billing, user management?
   - These should be tracked at their natural level.

5. **"Can users switch between contexts?"**
   - Multiple workspaces? Multiple projects?
   - This determines whether event-level grouping is needed vs. user-level.

---

## Tracking Plan Implications

### Group Definitions Section

Add a `groups` section to your tracking plan:

```yaml
groups:
  - type: account
    id_format: "acc_*"
    is_top_level: true
    traits:
      - name: name
        type: string
        required: true
      - name: plan
        type: string
        enum: [free, pro, enterprise]

  - type: workspace
    id_format: "ws_*"
    parent_type: account
    traits:
      - name: name
        type: string
        required: true
      - name: member_count
        type: integer

  - type: project
    id_format: "proj_*"
    parent_type: workspace
    traits:
      - name: name
        type: string
        required: true
      - name: status
        type: string
        enum: [active, archived]
```

### Event-Level Group Attribution

For each event, specify which group level it belongs to:

```yaml
events:
  - name: Task Completed
    category: core_value
    group_level: project  # Attach to project
    properties:
      - name: task_id
        type: string

  - name: Workspace Settings Updated
    category: configuration
    group_level: workspace  # Attach to workspace, not project
    properties:
      - name: setting_name
        type: string

  - name: Plan Upgraded
    category: billing
    group_level: account  # Attach to top-level account
    properties:
      - name: new_plan
        type: string
```

---

## Destination Comparison: Group Hierarchy Support

When choosing an analytics destination for a product with hierarchical groups, understand how each platform handles (or does not handle) parent-child relationships:

| Destination | Multiple Group Types on One Event | Automatic Hierarchy Rollup | Notes |
|-------------|-----------------------------------|---------------------------|-------|
| **Accoil** | N/A (uses single groupId) | Yes | Full hierarchy via parent_group_id. Events roll up automatically. |
| **Mixpanel** | Yes (up to 300 group keys) | **No** | Can track against company, workspace, and project simultaneously on one event. But an event on `workspace_id` does NOT roll up to the parent `company_id`. You must include all relevant group keys on each event yourself. |
| **Amplitude** | Yes (up to 5 group types) | **No** | Similar to Mixpanel -- supports multiple group types but no parent-child rollup. |
| **PostHog** | Yes (up to 5 group types) | **No** | Group types are independent. No hierarchy. |
| **Segment** | No | **No** | Only user-level group association. Cannot attribute individual events to groups. |

**Why this matters:** If your product has a hierarchy (e.g. Account > Workspace > Project) and you need rollup analytics, you have two options:

1. **Use a platform with native rollup** (e.g. Accoil) -- track events at the most specific level and let the platform roll up automatically.
2. **Use Mixpanel/Amplitude and include all group levels on each event** -- this works but requires discipline in implementation. Every track call must carry all relevant group keys, and any missing key means that event is invisible at that group level.

---

## Summary

| Concept | How It Works |
|---------|--------------|
| **Group hierarchy** | Groups reference parents to form a tree |
| **Event attribution** | Events include one groupId (the most specific level) |
| **Specificity** | Use the lowest-level group when possible |
| **Rollups** | Analytics tools derive higher-level metrics automatically |
| **Admin actions** | Track at the level where the action occurred |

---

## Common Mistakes

1. **Tracking everything at account level** — Loses all sub-account granularity
2. **Not defining parent relationships** — Prevents rollup calculations
3. **Attaching multiple groupIds to one event** — Causes double-counting
4. **Forgetting to group() new entities** — Groups must exist before events reference them
5. **Using Segment alone for event-level groups** — Segment doesn't support this; use Accoil/Amplitude/Mixpanel for event attribution
