# Telemetry Anti-Patterns

Things to avoid when designing and implementing product telemetry.

## Hard Lines — Never Do These

### 1. PII in Event Properties

**Bad:**
```javascript
track('user.signed_up', {
  email: 'john@example.com',
  name: 'John Smith',
  phone: '+1-555-0123'
});
```

**Good:**
```javascript
track('user.signed_up', {
  user_id: 'usr_abc123',
  signup_source: 'google_oauth'
});
```

PII belongs in user traits (identify calls), not event properties. And even then, hash or tokenize where possible.

### 2. High-Frequency Noise

**Don't track:**
- Every keystroke
- Mouse movements
- Scroll position
- Window focus/blur (usually)
- Hover states

These generate massive volume with minimal signal. If you need this data, use session recording tools (FullStory, Hotjar), not your analytics pipeline.

### 3. Redundant Events

**Bad:**
```javascript
track('create_report_button.clicked');
track('report.created');
```

The button click is implied by the report creation. Track the outcome, not the mechanism.

**Exception:** When the mechanism matters (A/B testing different UI paths to same outcome).

### 4. Implementation Details

**Don't track:**
- `api.called`
- `cache.hit`
- `database.queried`
- `job.enqueued`

This is operational telemetry (for Datadog, etc.), not product telemetry.

### 5. Speculative Events

**Don't add events because:**
- "We might need this someday"
- "More data is better"
- "Just in case"

Every event has a maintenance cost. Track what you need now, add more when you actually need it.

---

## Granularity Anti-Patterns

### Too Vague

**Bad:**
```javascript
track('feature.used', { feature: 'reports' });
track('action.performed', { action: 'create', object: 'report' });
```

You can't write a sentence about behavior with these. "The user used a feature" tells you nothing.

**Good:**
```javascript
track('report.created', { report_type: 'standard' });
track('report.exported', { format: 'pdf' });
track('report.shared', { recipient_count: 3 });
```

### Too Granular

**Bad:**
```javascript
track('report.title.focused');
track('report.title.changed');
track('report.title.blurred');
track('report.description.focused');
track('report.description.changed');
// ... for every field
```

**Good:**
```javascript
track('report.created', { 
  has_title: true, 
  has_description: true,
  field_count: 5 
});
```

Track the outcome with enough properties to understand the shape.

---

## Naming Anti-Patterns

### Inconsistent Casing

**Bad:**
```javascript
track('UserSignedUp');
track('report_created');
track('Dashboard Viewed');
track('task.completed');
```

**Good:** Pick one convention and stick to it:
```javascript
// Recommended: object.action, snake_case
track('user.signed_up');
track('report.created');
track('dashboard.viewed');
track('task.completed');
```

### Verb-First Naming

**Bad:**
```javascript
track('created_report');
track('viewed_dashboard');
track('completed_task');
```

**Good:**
```javascript
track('report.created');
track('dashboard.viewed');
track('task.completed');
```

Object-first naming groups related events together in sorted lists.

### Generic Prefixes

**Bad:**
```javascript
track('app.report.created');
track('app.dashboard.viewed');
track('app.user.signed_up');
```

The `app.` prefix adds nothing. Every event is from your app.

---

## Property Anti-Patterns

### Stringly-Typed Booleans

**Bad:**
```javascript
track('report.created', { is_template: 'true' });
```

**Good:**
```javascript
track('report.created', { is_template: true });
```

### Inconsistent Property Names

**Bad:**
```javascript
track('report.created', { reportId: '123' });
track('report.shared', { report_id: '456' });
track('report.deleted', { id: '789' });
```

**Good:**
```javascript
// Always: report_id
track('report.created', { report_id: '123' });
track('report.shared', { report_id: '456' });
track('report.deleted', { report_id: '789' });
```

### Missing Context

**Bad:**
```javascript
track('button.clicked');
```

**Good:**
```javascript
track('upgrade_prompt.clicked', { 
  location: 'dashboard_header',
  current_plan: 'free'
});
```

If you must track a click, include enough context to make it useful.

---

## Structural Anti-Patterns

### No Account Context in B2B

**Bad:**
```javascript
track('report.created', { user_id: 'usr_123' });
```

**Good:**
```javascript
track('report.created', { 
  user_id: 'usr_123',
  account_id: 'acc_456'
});
```

In B2B, accounts are first-class. Every event should be attributable to both user and account.

### Inconsistent ID Formats

**Bad:**
```javascript
track('report.created', { report_id: '123' });
track('user.invited', { invitee_id: 'john@example.com' });
track('task.completed', { task_id: 'task-abc-123' });
```

**Good:**
```javascript
// Consistent format: entity_prefix + underscore + id
track('report.created', { report_id: 'rpt_123' });
track('user.invited', { invitee_id: 'usr_456' });
track('task.completed', { task_id: 'tsk_789' });
```
