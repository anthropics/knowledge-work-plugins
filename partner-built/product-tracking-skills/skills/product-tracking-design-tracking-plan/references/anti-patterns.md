# Telemetry Anti-Patterns

Things to avoid when designing and implementing product telemetry.

**Cost context:** Most analytics platforms bill based on event volume, MTU count, or both. Every anti-pattern below is not just a signal-quality problem — it is a cost problem. Noisy, redundant, and speculative events directly increase your analytics bill.

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

These generate massive volume with minimal signal — and on volume-billed platforms, they generate massive cost. A single user scrolling and clicking through your app can produce hundreds of events per session. If you need this data, use session recording tools (FullStory, Hotjar), not your analytics pipeline.

### 3. Redundant Events

**Bad:**
```javascript
track('create_report_button.clicked');
track('report.created');
```

The button click is implied by the report creation. Track the outcome, not the mechanism. Every redundant event doubles your cost for that interaction with zero additional insight.

**Exception:** When the mechanism matters (A/B testing different UI paths to same outcome).

### 4. Implementation Details in Event Names or Properties

**Don't leak implementation into event names:**
```javascript
// Bad - exposes technical implementation
track('div#search-input focused');
track('GET /api/search?q=test Success');
track('Redux Action SEARCH_EXECUTED');

// Good - describes user intent
track('search.performed');
track('filter.applied');
```

**Don't track operational internals as product events:**
- `api.called`
- `cache.hit`
- `database.queried`
- `job.enqueued`

This is operational telemetry (for Datadog, etc.), not product telemetry. Product telemetry answers "what did the user do?" -- operational telemetry answers "how is the system performing?" Keep them separate.

### 5. Speculative Events

**Don't add events because:**
- "We might need this someday"
- "More data is better"
- "Just in case"

Every event has a maintenance cost and a billing cost. On volume-billed platforms, speculative events are not free options — they are recurring charges for data nobody uses. Track what you need now, add more when you actually need it.

---

## Cost Anti-Patterns

### Page View Tracking

**Bad:**
```javascript
track('page.viewed', { page: '/dashboard' });
track('page.viewed', { page: '/settings' });
track('page.viewed', { page: '/reports' });
track('page.viewed', { page: '/reports/123' });
```

Page views are the single largest source of event volume inflation. A user navigating through your app can generate dozens of page views per session, and most of them tell you nothing actionable.

**Why this is costly:** Page views often outnumber meaningful feature events by 10:1 or more. On volume-billed platforms, this means paying ten times more for data that rarely answers a useful product question.

**What to do instead:** Track feature engagement events. `report.created` tells you more than fifty `page.viewed` events on the reports page. If you need to understand navigation patterns or page-level engagement, use a dedicated product analytics tool with auto-capture (PostHog, FullStory) rather than polluting your event pipeline.

**Exception:** A small number of strategic page views (pricing page, upgrade page) may be worth tracking as commercial intent signals. These are the exception, not the rule.

### Lifecycle Step Inflation

**Bad:**
```javascript
track('report.creation_started');
track('report.running');
track('report.run_completed');
track('report.created');
```

**Good:**
```javascript
track('report.created', {
  report_type: 'standard',
  duration_ms: 3400
});
```

Track the **outcome**, not every intermediate state. If a report was created, it was obviously started and run — those steps are implied. Four events for one user action means four times the cost with zero additional insight. The completion event is the only one anyone will ever query.

**When to track start + completion:** Only when abandonment is a meaningful signal. A multi-step onboarding wizard where users drop off at step 3 justifies `onboarding.started` + `onboarding.completed`. A synchronous report generation does not.

**During design, actively look for lifecycle bloat.** When the audit reveals chains of events tracking the same workflow (`*.started` → `*.in_progress` → `*.completed` → `*.created`), collapse them to the outcome event with properties for any useful context (duration, step count, method).

### Variant Proliferation Instead of Properties

**Bad:**
```javascript
track('standard_report.created');
track('custom_report.created');
track('template_report.created');
```

**Good:**
```javascript
track('report.created', {
  report_type: 'standard'   // or 'custom', 'template'
});
```

Three events where one would suffice means three times the volume on your analytics bill. Use properties to distinguish variants, not separate event names.

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

Track the outcome with enough properties to understand the shape. Fewer events with richer properties costs less and tells you more.

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

Object-first naming groups related events together in sorted lists. When you sort alphabetically, all report events cluster together, all task events cluster together. Verb-first naming scatters related events across the list.

### Present or Future Tense

**Bad:**
```javascript
track('Performing Search');
track('Will Generate Export');
track('Is Applying Filter');
```

**Good:**
```javascript
track('search.performed');
track('export.generated');
track('filter.applied');
```

Events are records of things that already happened. Past tense is non-negotiable. Present tense implies the action is in progress (ambiguous -- did it complete?). Future tense implies intent, not action (the user might not follow through).

### Vague or Generic Names

**Bad:**
```javascript
track('action');
track('event_happened');
track('user_did_something');
```

**Good:**
```javascript
track('search.performed');
track('report.generated');
track('subscription.upgraded');
```

If you cannot immediately understand what happened from the event name alone, the name is too vague. Every event name should pass the "sentence test": you should be able to say "The user's [object] was [verb]" and have it be meaningful.

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

### Scattered Event Definitions

**Bad:** Events defined inline across the codebase with no central registry.

```javascript
// File A
track('user performed search');

// File B
track('Search Performed');

// File C
track('SEARCH_EXECUTED');
```

**Why this is structural, not just a naming problem:** Without centralization, consistency depends on every developer remembering conventions. That does not scale. Three developers writing the same event three different ways is not a discipline failure -- it is a system design failure. Centralize event definitions so that the correct name is the easy path, and the wrong name requires going out of your way.

### Same Property, Different Meanings

**Bad:**
```javascript
track('report.created', { type: 'standard' });    // type = report type
track('export.generated', { type: 'pdf' });        // type = file format
track('user.invited', { type: 'admin' });           // type = user role
```

**Good:**
```javascript
track('report.created', { report_type: 'standard' });
track('export.generated', { export_format: 'pdf' });
track('user.invited', { invited_role: 'admin' });
```

When the same property name (`type`) means different things on different events, every query requires remembering which meaning applies. Use specific, self-describing property names.
