# Naming Conventions

Consistent naming makes telemetry queryable, readable, and maintainable.

## Why Naming Strategy Matters

Without a naming strategy, analytics becomes chaos. Different developers invent different conventions, and the same action ends up tracked under multiple names:

```
user_searched_something
Search Executed
search-performed
SEARCH_ACTION
```

This is not a cosmetic problem. When the same action has four names, your data is fragmented. Dashboards undercount. Queries miss events. Nobody trusts the numbers. The cost of fixing naming after the fact is enormous -- you either migrate historical data (expensive, error-prone) or live with a permanent seam in your analytics.

With a strategy, analytics tell a clear, consistent story:

```
Search Performed
Filter Applied
Export Generated
Todo Created
```

Good naming is an investment that pays off in every query, every dashboard, and every decision that touches your data.

## Event Names

There are two common conventions. Pick one and stick to it across your entire codebase.

### The Core Principles: Descriptive, Consistent, Contextual

Regardless of which format you pick, three principles govern event naming:

1. **Descriptive** -- Use names that clearly describe the action being tracked. `Report Created` tells anyone reviewing the data -- developers, analysts, or business stakeholders -- exactly what happened. Clear, descriptive names reduce errors and confusion when setting up or analyzing data.
2. **Consistent** -- Stick to one naming convention across your entire codebase. Consistency simplifies querying and analysis. You should never need to remember multiple formats or deal with inconsistent naming across events.
3. **Contextual** -- Keep event names concise and focused; use properties to add context rather than expanding the event name. Instead of `PurchasedTShirtOnSale`, use `Purchase Completed` with properties like `{ product: 'T-shirt', discount: '20%' }`. This makes events easier to analyze and compare across different contexts.

And the structural rules:

4. **Object first** -- Name the thing that was acted upon. This naturally groups related events together in sorted lists (all `Report` events cluster, all `User` events cluster).
5. **Past tense verb** -- The event describes something that already happened. Events are facts, not intentions.
6. **Describe outcomes, not mechanisms** -- Track what the user accomplished, not how they accomplished it. `Report Created` tells you something meaningful. `Create Button Clicked` is coupled to your UI and breaks when the UI changes.

### Option A: `Object Verb` (Title Case)

```
Todo Created
User Invited
Search Performed
Integration Connected
```

**Why this format:**
- Reads naturally as a sentence
- Easy to search in analytics tools
- Groups related events when sorted alphabetically
- Clear what happened at a glance

**Rules:**
- Object first, then past-tense verb
- Title Case with spaces
- Always past tense (it already happened)

### Option B: `object.action` (snake_case)

```
todo.created
user.invited
search.performed
integration.connected
```

**Why this format:**
- Works in all databases without quoting
- Easy to parse programmatically
- Common in Segment/Amplitude ecosystems

**Rules:**
- Object first, dot separator, action
- All lowercase with underscores for multi-word
- Always past tense

### Which to Choose?

| Consideration | Object Verb | object.action |
|---------------|-------------|---------------|
| Readability in dashboards | Better | Good |
| Database compatibility | Needs quoting | Native |
| Programmatic parsing | Harder | Easier |
| Industry standard | Common | Common |

**Pick one. Be consistent. Don't mix.**

### Multi-Word Objects

When the object or action is more than one word, keep the same pattern:

**Title Case:**
```
Advanced Search Performed
Bulk Export Generated
Setup Wizard Completed
User Role Changed
```

**Dot notation:**
```
advanced_search.performed
bulk_export.generated
setup_wizard.completed
user_role.changed
```

Multi-word objects are fine and often necessary. The key is that the object still comes first and the past-tense verb still comes last. Do not abbreviate objects to avoid multi-word names -- clarity beats brevity.

### Singular vs Plural Objects

Use singular for individual actions, plural only for genuine bulk operations:

```
Todo Created          -- one todo was created
Todos Cleared         -- all todos were removed at once
Report Exported       -- one report
Reports Bulk Deleted  -- batch operation on many reports
```

### Action Vocabulary

Use past tense. The event already happened.

| Action | Meaning | Notes |
|--------|---------|-------|
| `created` | New thing made | |
| `updated` | Existing thing modified | |
| `deleted` | Thing removed | |
| `viewed` | Thing displayed to user | Use sparingly -- see note below |
| `clicked` | Avoid -- track the outcome instead | |
| `started` | Process began | |
| `completed` | Process finished | |
| `failed` | Process errored | |
| `abandoned` | Process left incomplete | Useful for workflows/wizards |
| `sent` | Message/notification dispatched | |
| `received` | Message/notification arrived | |
| `connected` | Integration/service linked | |
| `disconnected` | Integration/service unlinked | |
| `configured` | Settings/setup established | |
| `invited` | User invited someone | |
| `joined` | User accepted invite | |
| `left` | User departed | |
| `upgraded` | Plan/tier increased | |
| `downgraded` | Plan/tier decreased | |
| `generated` | Output produced (reports, exports) | |
| `applied` | Filter/template/rule put into effect | |
| `performed` | Action executed (search, sync) | |

**A note on `viewed` and `clicked`:** These describe UI mechanics, not user intent. Prefer tracking the meaningful outcome. If you must track navigation, keep it sparse -- key pages only, not every screen. See the anti-patterns reference for detail.

---

## When to Create a New Event vs. Use Properties

This is one of the most important naming decisions. The rule: **use properties for variants of the same action; use separate events for fundamentally different actions.**

**Use properties (one event, different property values):**
```
report.created  { report_type: 'standard' }
report.created  { report_type: 'custom' }
report.created  { report_type: 'template' }
```

**Use separate events (different actions on the same object):**
```
report.created
report.shared
report.exported
report.archived
```

**The test:** Can you write a single sentence that describes all variants? "A report was created" covers standard, custom, and template reports -- so use one event with a `report_type` property. But "a report was created" and "a report was shared" are fundamentally different actions -- so use separate events.

**Why this matters:**
- One event with properties lets you easily query "all reports created" and then break down by type
- Separate events per variant leads to event explosion and makes aggregate queries painful
- But collapsing genuinely different actions into one event with an `action_type` property makes every query require a filter and obscures what actually happened

---

## Property Names

### Format: `snake_case`

Always use `snake_case` for property names, regardless of which event naming convention you chose. This ensures consistency across your entire data model.

```javascript
{
  report_id: 'rpt_123',
  report_type: 'standard',
  created_by: 'usr_456',
  is_template: false
}
```

### Property Naming Patterns

Use consistent suffixes so properties are self-describing:

| Pattern | Type | Examples | Purpose |
|---------|------|----------|---------|
| `*_id` | String (prefixed) | `report_id`, `task_id` | Entity references |
| `*_type` | Enum string | `report_type: 'standard'` | Categorization |
| `*_count` | Integer | `recipient_count: 3` | Quantities |
| `is_*` | Boolean | `is_template: true` | State flags |
| `has_*` | Boolean | `has_description: true` | Presence flags |
| `*_at` | ISO 8601 timestamp | `created_at`, `expires_at` | Points in time |
| `*_source` | Enum string | `signup_source: 'google_oauth'` | Origin/attribution |
| `*_format` | Enum string | `export_format: 'pdf'` | Output format |

**Why consistent suffixes matter:** When someone sees `recipient_count` they immediately know it is an integer. When they see `is_template` they know it is a boolean. This eliminates guesswork in queries and dashboard building.

### Common Properties

These should appear consistently across events:

| Property | Format | Notes |
|----------|--------|-------|
| `user_id` | `usr_xxx` | Always include |
| `account_id` | `acc_xxx` | Always include (B2B) |
| `session_id` | `ses_xxx` | If tracking sessions |
| `timestamp` | ISO 8601 | Usually auto-added by SDK |

### The Same Property Must Always Mean the Same Thing

If `report_id` appears on `report.created` and `report.shared`, it must reference the same entity in the same format. Never reuse a property name with a different meaning across events. This sounds obvious, but it drifts over time as different developers add properties independently.

### ID Formats

Use prefixed IDs for clarity:

| Entity | Prefix | Example |
|--------|--------|---------|
| User | `usr_` | `usr_abc123` |
| Account | `acc_` | `acc_def456` |
| Report | `rpt_` | `rpt_ghi789` |
| Task | `tsk_` | `tsk_jkl012` |
| Team | `tem_` | `tem_mno345` |
| Session | `ses_` | `ses_pqr678` |

This makes IDs self-documenting in logs and queries. When you see `usr_abc123` in a raw event, you know instantly it is a user ID without checking the property name.

---

## Centralized Event Definitions

Events should be defined in a single source of truth, not scattered across the codebase. When events are defined inline wherever tracking happens, you get inconsistency, typos, and phantom events.

**The problem:**
```
// File A
track('user performed search')

// File B
track('Search Performed')

// File C
track('SEARCH_EXECUTED')
```

Three files, three names, one action. Your analytics now has three separate events that should be one.

**The fix:** Centralize all event definitions in dedicated files. Every tracking call references the central definition. This gives you:
- A single audit point for all events
- Typo prevention through reusable definitions
- Easy discovery of what is tracked
- Consistent naming enforced by structure, not discipline

For larger applications, organize event definitions by domain (user events, billing events, etc.) but keep them in a known location.

---

## User & Account Traits

Traits are stable, enduring attributes that persist across events and sessions. Unlike event properties that capture moment-to-moment context, traits build a comprehensive profile over time. They change infrequently and are critical for segmentation, personalization, and targeted communication.

### User Traits

Set via `identify()` calls:

```javascript
identify('usr_123', {
  email: 'jane@example.com',      // PII - be careful
  name: 'Jane Smith',              // PII - be careful
  role: 'admin',
  created_at: '2024-01-15T10:30:00Z',
  subscription_level: 'pro',
  preferred_language: 'English',
  last_login: '2024-02-07T10:30:00Z',
  account_id: 'acc_456'
});
```

### Account Traits (Group)

Set via `group()` calls:

```javascript
group('acc_456', {
  name: 'Acme Corp',
  plan: 'enterprise',
  industry: 'technology',
  employee_count: 150,
  mrr: 999,
  created_at: '2023-06-01T00:00:00Z',
  number_of_users: 50,
  billing_cycle: 'annual',
  support_level: 'priority'
});
```

---

## Event Naming Checklist

Before adding a new event, verify:

- [ ] Follows your chosen naming format consistently
- [ ] Uses past tense verb (describes what happened, not what will happen)
- [ ] Object comes first, verb comes last
- [ ] Describes the outcome, not the UI mechanism
- [ ] No redundant prefixes (e.g., "Event:", "Track:", "App.")
- [ ] No implementation details (e.g., "Button1", "div#search-input")
- [ ] No PII in the event name
- [ ] Consistent with existing events for the same object
- [ ] Added to the central event definition file
- [ ] Would not be better served by an existing event with a new property value

---

## Examples by Category

### Lifecycle

```
user.signed_up
user.invited
user.onboarded
user.churned
account.created
```

### Core Value (Example: Analytics Product)

```
report.created
report.viewed
report.exported
report.shared
dashboard.created
dashboard.customized
insight.generated
```

### Collaboration

```
teammate.invited
teammate.joined
teammate.removed
comment.added
mention.created
permission.changed
```

### Configuration

```
integration.connected
integration.disconnected
setting.changed
webhook.configured
api_key.created
```

### Billing-Adjacent

```
trial.started
trial.extended
plan.viewed
plan.upgraded
plan.downgraded
limit.reached
```
