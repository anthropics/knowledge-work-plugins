# Naming Conventions

Consistent naming makes telemetry queryable, readable, and maintainable.

## Why Naming Consistency Matters During Implementation

During implementation, you are the last line of defense for naming quality. A tracking plan may specify event names, but inline tracking calls without centralized definitions will drift. When implementing, always:

1. **Reference the tracking plan** -- do not invent event names
2. **Use centralized event definitions** -- never hardcode event name strings at the call site
3. **Match the existing convention exactly** -- check existing events before adding new ones

If the codebase uses `Object Verb` (Title Case), every new event must use that format. If it uses `object.action` (snake_case), every new event must use that format. Mixing conventions is worse than picking the "wrong" one.

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

## When to Use Properties vs. Separate Events

During implementation, you may encounter situations where the tracking plan does not explicitly cover a variant. The rule: **use properties for variants of the same action; use separate events for fundamentally different actions.**

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

**The test:** Can you write a single sentence that describes all variants? "A report was created" covers standard, custom, and template reports. "A report was created" and "a report was shared" are fundamentally different actions that deserve separate events.

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

During implementation, always define events in a central location rather than hardcoding strings at every call site.

**The problem:**
```
// File A
track('user performed search')

// File B
track('Search Performed')

// File C
track('SEARCH_EXECUTED')
```

**The fix:** Centralize all event definitions in dedicated files. Every tracking call references the central definition. For larger applications, organize by domain (user events, billing events, etc.) but keep them in a known location.

This gives you:
- A single audit point for all events
- Typo prevention through reusable definitions
- Easy discovery of what is tracked
- Consistent naming enforced by structure, not discipline

---

## Implementation Checklist

Before implementing a new event, verify:

- [ ] Event name matches the tracking plan exactly
- [ ] Event is defined in the central event definitions file
- [ ] Properties use `snake_case` with consistent suffixes
- [ ] No PII in event name or properties
- [ ] `account_id` is included (B2B)
- [ ] Boolean properties use actual booleans, not strings
- [ ] ID properties use prefixed format
- [ ] The same property name is not reused with a different meaning
- [ ] Track call has error handling (non-blocking)
- [ ] Event fires at the canonical moment (usually after success confirmation)

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
