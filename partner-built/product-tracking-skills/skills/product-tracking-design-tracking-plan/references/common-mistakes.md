# Common Mistakes

Telemetry anti-patterns we see repeatedly. Learn from others' errors.

## 1. No Tracking Plan

**Mistake:** Adding tracking ad-hoc without documentation.

**Result:**
- Inconsistent event names (`UserSignedUp`, `user_signed_up`, `signup`)
- Missing events discovered too late
- Tribal knowledge about what events mean
- Technical debt compounds

**Fix:** Always start with a tracking plan. This plugin exists for that reason.

---

## 2. Ignoring Account Context (B2B)

**Mistake:** Only tracking user-level events without account association.

**Result:**
- Can't analyze account health
- Can't segment by account traits
- B2B analytics tools don't work
- Lost the most important dimension

**Fix:** Always call `group()`. Always include `account_id`.

---

## 3. Tracking Everything

**Mistake:** "We might need this someday" approach.

**Result:**
- Massive data volume and cost — on volume-billed platforms, every speculative event is a recurring charge
- Signal buried in noise
- Nobody trusts the data because there's too much
- Performance impact on client

**Fix:** Track what answers real questions. Add more when needed. Every event you choose not to track is money saved and noise reduced. The cost of adding an event later is trivial; the cost of paying for a useless event for months is not.

---

## 4. Scattered Event Definitions

**Mistake:** Defining events inline throughout the codebase.

```javascript
// ❌ Events defined everywhere
// FileA.js
track('user performed search');

// FileB.js
track('Search Performed');

// FileC.js
track('SEARCH_EXECUTED');
```

**Result:**
- Same event tracked differently
- No way to audit all events
- Typos create phantom events
- Hard to maintain consistency

**Fix:** Centralize event definitions in dedicated files:

```
src/analytics/
├── events.js        # All event definitions
└── dispatcher.js    # Track/identify/group logic
```

```javascript
// events.js - Single source of truth
export const trackSearchPerformed = (context) =>
  trackEvent(context, 'Search Performed');

export const trackTodoCreated = (context) =>
  trackEvent(context, 'Todo Created');
```

---

## 5. Inconsistent Naming

**Mistake:** Different conventions across the codebase.

```javascript
track('UserCreatedReport');
track('report_created');
track('Report Created');
track('created-report');
```

**Result:**
- Events split across different names
- Hard to query and analyze
- New developers confused
- The cost of fixing naming retroactively is enormous -- you either migrate historical data (expensive, error-prone) or live with a permanent seam in your analytics

**Fix:** Pick a convention (we recommend `object.action` snake_case) and enforce it. The convention itself matters less than consistency. What matters most:
- Object first, verb second (groups related events when sorted)
- Always past tense (events are facts, not intentions)
- One format across the entire codebase (no mixing Title Case and snake_case)

Enforce through centralized event definitions, not developer discipline. Make the right name the easy path.

---

## 6. PII in Event Properties

**Mistake:** Including personal data in event properties.

```javascript
// BAD
track('order.placed', { 
  customer_email: 'john@example.com',
  shipping_address: '123 Main St'
});
```

**Result:**
- Privacy/compliance risk
- Data can't be easily anonymized
- Limits where data can be sent

**Fix:** PII goes in user traits via `identify()`. Events get IDs only.

---

## 7. Button Click Events

**Mistake:** Tracking UI interactions instead of outcomes.

```javascript
// BAD
track('submit_button.clicked');
track('create_report_button.clicked');
```

**Result:**
- Breaks when UI changes
- Doesn't capture business meaning
- Coupled to implementation
- The button click is implied by the outcome -- if a report was created, someone clicked the button

**Fix:** Track outcomes: `report.created`, not `create_report_button.clicked`. The button click is redundant when you track the result. Focus on what the user accomplished, not the UI mechanism they used.

**Exception:** When you are A/B testing different UI paths to the same outcome, the mechanism temporarily matters. But this is the exception, not the rule.

---

## 8. No Error Handling

**Mistake:** Letting analytics break the user experience.

```javascript
// BAD - blocking call with no error handling
await analytics.track('critical.action');
doNextThing();
```

**Result:**
- If analytics fails, app fails
- Slow analytics = slow app
- Users have bad experience

**Fix:** Non-blocking calls with error handling:

```javascript
analytics.track('action').catch(console.error);
doNextThing();
```

---

## 9. Missing Timestamps

**Mistake:** Relying on server-side timestamps.

**Result:**
- Offline events get wrong timestamps
- Mobile events timestamped when sent, not when occurred
- Time-based analysis is inaccurate

**Fix:** Include client-side timestamp. Most SDKs do this automatically, but verify.

---

## 10. Duplicate Events

**Mistake:** Same event fired multiple times for one action.

**Common causes:**
- Event in component that re-renders
- Event in both frontend and backend
- Event in multiple code paths

**Result:**
- Inflated metrics
- Conversion rates look wrong
- Hard to trust data

**Fix:** Track at the canonical moment, in one place. Often server-side for important events.

---

## 11. Not Testing Tracking

**Mistake:** No QA process for analytics.

**Result:**
- Broken tracking goes unnoticed for weeks
- Dashboards show wrong data
- Decisions made on bad data

**Fix:** 
- Test tracking in development
- Monitor event volume in production
- Automated tests for critical events

---

## 12. Orphaned Events

**Mistake:** Old events never cleaned up.

**Result:**
- Confusion about what's real
- Queries return stale data
- New developers don't know what to use

**Fix:** Deprecate with timeline, then remove. Keep changelog.

---

## 13. Missing User Identity

**Mistake:** Events fired before `identify()` is called.

**Result:**
- Anonymous events can't be attributed
- User journey is incomplete
- Identity resolution fails

**Fix:** Call `identify()` as early as possible. SDKs handle anonymous-to-known merging.

---

## 14. Over-Reliance on Auto-Track

**Mistake:** Thinking auto-tracking solves everything.

**Result:**
- Captured events lack business context
- Generic events like "click" are useless
- Still need manual instrumentation for meaning

**Fix:** Auto-track for basics, manual track for business events.

---

## 15. Not Versioning the Plan

**Mistake:** No version history for tracking plan changes.

**Result:**
- Can't explain historical data changes
- Breaking changes surprise everyone
- No migration path

**Fix:** Version your tracking plan. Keep a changelog.

---

## 16. Properties vs Events Confusion

**Mistake:** Creating events when properties would work.

```javascript
// BAD
track('standard_report.created');
track('custom_report.created');
track('template_report.created');
```

**Result:**
- Event explosion — three events where one would suffice, tripling volume and cost
- Hard to query "all reports created"
- Inconsistent analysis

**Fix:**
```javascript
// GOOD
track('report.created', { report_type: 'standard' });
```

This is one of the highest-impact cost optimizations in event design. During the design phase, actively scan the audit for event families that can be consolidated into a single event with a distinguishing property.

---

## 17. Ignoring Mobile/Offline

**Mistake:** Assuming events always send immediately.

**Result:**
- Mobile events lost on bad connection
- Offline actions not captured
- Data gaps

**Fix:** Use SDKs with offline queuing. Verify events arrive.

---

## 18. Deriving Counts from Events

**Mistake:** Calculating totals from events instead of snapshots.

```javascript
// ❌ Counting objects from events
totalTodos = todos_created.count() - todos_deleted.count()
```

**Result:**
- Drift over time from dropped/duplicate events
- Historical events predate your tracking
- Migrations and imports bypass events
- Never quite matches reality

**Fix:** Use snapshot metrics. Query your database directly on a schedule:

```javascript
// ✅ Snapshot from source of truth
group(accountId, {
  total_todos: await db.todos.count({ accountId }),
  last_sync: new Date().toISOString()
});
```

---

## 19. No Ownership

**Mistake:** Analytics is "everyone's job" (meaning no one's job).

**Result:**
- No one reviews tracking changes
- Quality degrades over time
- Institutional knowledge lost

**Fix:** Assign ownership. Product or eng, doesn't matter—someone owns it.

---

## 20. No Ongoing Data Validation

**Mistake:** Setting up tracking once and assuming it stays accurate.

**Result:**
- Data quality silently degrades over time
- Schema changes break event properties without anyone noticing
- Decisions made on stale or inaccurate data
- New team members introduce inconsistencies

**Fix:** Designate someone to regularly monitor and validate data quality. Set up validation processes to catch issues early -- before they affect analysis or decision-making. This includes verifying event schemas, checking for unexpected null values, and confirming that new code changes haven't broken existing tracking.

---

## 21. Poor Data Hygiene

**Mistake:** Never cleaning up tracked data or reviewing its relevance.

**Result:**
- Duplicate events accumulate from re-renders or retry logic
- Outdated information pollutes segmentation and targeting
- Trait values go stale (e.g., `last_login` never updated, `plan` reflects old tier)
- Analytics tools become cluttered with noise

**Fix:** Regularly review and clean your data. Set up processes for de-duplication, updating stale records, and pruning events that no longer serve analytical needs. Treat data hygiene as an ongoing practice, not a one-time setup task.

---

## 22. Undocumented Data Schema

**Mistake:** Tracking events and traits without maintaining documentation of the schema.

**Result:**
- New team members can't understand what's being tracked or why
- Troubleshooting issues requires reading code instead of consulting a reference
- Data strategy drifts from business goals without anyone noticing
- Onboarding new engineers to tracking takes weeks instead of hours

**Fix:** Maintain thorough documentation of your data schema and tracking plan. Document every event, its properties, and the traits you collect. Include use cases and the business questions each event answers. Keep documentation updated as the plan evolves -- this is what the `.telemetry/` folder is for.

---

## Checklist: Are You Making These Mistakes?

- [ ] Do you have a written tracking plan?
- [ ] Is account context on every B2B event?
- [ ] Is naming consistent across events?
- [ ] Is PII only in user traits, not event properties?
- [ ] Are you tracking outcomes, not UI clicks?
- [ ] Is there error handling on tracking calls?
- [ ] Do you test tracking before deploy?
- [ ] Is someone responsible for tracking quality?
- [ ] Is someone regularly validating data accuracy?
- [ ] Do you review and clean data on a regular cadence?
- [ ] Is your data schema documented and up to date?
