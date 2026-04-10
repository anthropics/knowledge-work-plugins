# Naming Conventions

Consistent naming makes telemetry queryable, readable, and maintainable.

## Naming New Feature Events

When instrumenting a new feature, you are adding events to an existing system. The most important rule: **match the existing conventions exactly.** Before naming any event:

1. **Check existing events** -- look at the codebase's central event definitions to see what convention is in use
2. **Follow the same pattern** -- if existing events use `Object Verb` Title Case, your new events must too
3. **Name the outcome, not the UI** -- `Report Created` not `Create Button Clicked`

New feature instrumentation is the most common source of naming drift. Be disciplined about consistency.

## Event Names

There are two common conventions. Pick one and stick to it across your entire codebase.

### The Core Principles: Descriptive, Consistent, Contextual

Regardless of which format you pick, three principles govern event naming:

1. **Descriptive** -- Use names that clearly describe the action being tracked, so anyone reviewing the data can immediately understand what happened.
2. **Consistent** -- Stick to one naming convention across your entire codebase. Consistency simplifies querying and analysis.
3. **Contextual** -- Keep event names concise; use properties to add context rather than expanding the event name. Instead of `PurchasedTShirtOnSale`, use `Purchase Completed` with properties like `{ product: 'T-shirt', discount: '20%' }`.

And the structural rules:

4. **Object first** -- Name the thing that was acted upon. This naturally groups related events together in sorted lists.
5. **Past tense verb** -- The event describes something that already happened. Events are facts, not intentions.
6. **Describe outcomes, not mechanisms** -- Track what the user accomplished, not how they accomplished it.

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

### Action Vocabulary

Use past tense. The event already happened.

| Action | Meaning | Notes |
|--------|---------|-------|
| `created` | New thing made | |
| `updated` | Existing thing modified | |
| `deleted` | Thing removed | |
| `viewed` | Thing displayed to user | Use sparingly |
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

---

## When to Create a New Event vs. Use Properties

When instrumenting a new feature, you will often face this question. The rule: **use properties for variants of the same action; use separate events for fundamentally different actions.**

**Use properties (one event, different property values):**
```
report.created  { report_type: 'standard' }
report.created  { report_type: 'custom' }
report.created  { report_type: 'template' }
```

**Use separate events (different actions):**
```
report.created
report.shared
report.exported
```

**The test:** Can you write a single sentence that describes all variants? "A report was created" covers all report types. "A report was created" and "a report was shared" are fundamentally different -- so use separate events.

---

## Property Names

### Format: `snake_case`

Always use `snake_case` for property names, regardless of which event naming convention you chose.

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

### Common Properties

These should appear consistently across events:

| Property | Format | Notes |
|----------|--------|-------|
| `user_id` | `usr_xxx` | Always include |
| `account_id` | `acc_xxx` | Always include (B2B) |
| `session_id` | `ses_xxx` | If tracking sessions |
| `timestamp` | ISO 8601 | Usually auto-added by SDK |

### The Same Property Must Always Mean the Same Thing

If `report_id` appears on `report.created` and `report.shared`, it must reference the same entity in the same format. Never reuse a property name with a different meaning across events.

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

This makes IDs self-documenting in logs and queries.

---

## Centralized Event Definitions

When adding events for a new feature, always add them to the existing central event definition files. Never define events inline at the call site.

**Why this matters for new features specifically:** New features are the most common source of naming drift. The developer adding the feature may not know all existing conventions. Centralized definitions force them to see existing events and match the pattern.

For larger applications, event definitions may be organized by domain. Add your new feature's events in the appropriate domain file, or create a new domain file if the feature represents a genuinely new domain.

---

## New Feature Instrumentation Checklist

Before shipping instrumentation for a new feature:

- [ ] Event names follow the existing codebase convention exactly
- [ ] Events are defined in the central event definitions file
- [ ] Events describe outcomes, not UI interactions
- [ ] Properties use `snake_case` with consistent suffixes
- [ ] Variants use properties, not separate event names
- [ ] `account_id` is included on every event (B2B)
- [ ] No PII in event names or properties
- [ ] The same property name is not reused with a different meaning elsewhere
- [ ] Track calls have error handling
- [ ] Events fire at the canonical moment (after success confirmation, not on button click)

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
