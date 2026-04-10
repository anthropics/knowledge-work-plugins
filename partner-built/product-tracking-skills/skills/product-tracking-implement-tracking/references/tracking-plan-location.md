# Where the Tracking Plan Lives

A strong opinion on maintaining your tracking plan.

## The Options

### 1. Separate Documentation (YAML/Markdown)

```
docs/tracking-plan.yaml
```

**Pros:**
- Human-readable for non-technical stakeholders
- Easy to review in PRs
- Tool-agnostic

**Cons:**
- Separate from code = drift
- No compile-time enforcement
- Requires discipline to keep in sync
- Extra step to generate code

### 2. TypeScript Types with JSDoc

```typescript
// src/analytics/events.ts
```

**Pros:**
- Type safety at compile time
- Can't drift — types break if wrong
- IDE autocomplete catches errors
- Documentation lives with code
- Engineers naturally maintain it

**Cons:**
- Requires TypeScript
- Less accessible to non-engineers

### 3. Both (YAML generates Types)

```
tracking-plan.yaml → codegen → events.ts
```

**Pros:**
- Best of both worlds
- Stakeholders review YAML
- Engineers get type safety

**Cons:**
- Build step complexity
- Two places to understand

---

## Our Recommendation: TypeScript Types ARE the Plan

**For TypeScript codebases, the type definitions should BE the tracking plan.**

Not a separate doc that generates types. Not types that implement a doc. The types themselves, with comprehensive JSDoc comments, are the canonical source of truth.

### Why This Works

1. **Can't drift** — If the types are wrong, the code won't compile
2. **Self-documenting** — JSDoc comments describe intent and context
3. **IDE enforcement** — Autocomplete prevents typos and wrong properties
4. **Review happens naturally** — PRs that add events show the full definition
5. **One place** — No sync issues between doc and implementation

### The Structure

```
src/analytics/
├── events/
│   ├── index.ts           # Barrel export
│   ├── lifecycle.ts       # User/account lifecycle events
│   ├── core.ts            # Core product events
│   └── billing.ts         # Billing events
├── types.ts               # Entity traits (User, Account)
├── track.ts               # Track function wrapper
└── README.md              # How to add events (for engineers)
```

### Event Definition Format

```typescript
// src/analytics/events/core.ts

import { track } from '../track';

/**
 * Fired when a user creates a new report.
 * 
 * This is a core value event — reports are the primary output
 * of the product. Track every report creation.
 * 
 * @category core_value
 * @since 1.0.0
 */
export interface ReportCreatedEvent {
  /** Unique identifier for the report */
  report_id: string;
  
  /** 
   * Type of report created.
   * - standard: Default report format
   * - custom: User-configured layout
   * - template: Started from a template
   */
  report_type: 'standard' | 'custom' | 'template';
  
  /** Whether user started from a template */
  template_used?: boolean;
}

/**
 * Track report creation.
 * @see ReportCreatedEvent
 */
export function trackReportCreated(
  userId: string, 
  props: ReportCreatedEvent
) {
  track(userId, 'Report Created', props);
}
```

### What the JSDoc Should Include

For each event interface:

```typescript
/**
 * [One-line description of what triggers this event]
 * 
 * [Context: Why this event matters, when to fire it, 
 * any nuances about the timing or conditions]
 * 
 * @category lifecycle | core_value | collaboration | configuration | billing
 * @since [version when added]
 * @deprecated [if deprecated, why and what replaces it]
 */
```

For each property:

```typescript
/** 
 * [What this property represents]
 * [If enum, explain each value]
 */
```

### Adding a New Event (The Workflow)

1. **Define the interface** in the appropriate file with full JSDoc
2. **Create the track function** that wraps the interface
3. **Export from index.ts**
4. **Use the typed function** in your code — IDE will autocomplete
5. **PR review** shows the full event definition inline

### Generating Documentation (Optional)

If non-engineers need a readable doc, generate it from types:

```bash
# Generate markdown from JSDoc
npx typedoc --plugin typedoc-plugin-markdown src/analytics/events
```

This creates docs FROM the types, not the other way around. Types remain the source of truth.

---

## For Non-TypeScript Codebases

The principle remains: **centralized event definitions with documentation**.

### JavaScript (no types)

Use JSDoc comments for documentation:

```javascript
// events.js

/**
 * Track todo creation.
 * @param {Object} context - Request context with userId, accountId
 * @category core_value
 */
export const trackTodoCreated = async (context) => {
  await track(context, 'Todo Created');
};
```

### Python

Use docstrings:

```python
# events.py

def track_todo_created(context):
    """
    Track todo creation.
    
    Category: core_value
    """
    track(context, 'Todo Created')
```

### Ruby

```ruby
# events.rb

# Track todo creation.
# @category core_value
def track_todo_created(context)
  track(context, 'Todo Created')
end
```

### Any Language

The pattern is the same:
1. **One file** with all event definitions
2. **Named functions** for each event (no inline strings)
3. **Comments/docstrings** describing purpose and category
4. **Common track helper** that handles context

This IS your tracking plan. The documentation lives with the code.

---

## Anti-Patterns

### ❌ Separate doc, no code connection
```
docs/tracking-plan.md  ← Gets stale
src/analytics.js       ← Does its own thing
```

### ❌ Types without documentation
```typescript
// No JSDoc = mystery events
interface ReportCreatedEvent {
  report_id: string;
  report_type: string;
}
```

### ❌ Inline string events
```typescript
// No central definition = chaos
track('report created');
track('Report Created');
track('report.created');
```

---

## Summary

| Codebase | Recommendation |
|----------|----------------|
| TypeScript | Types with JSDoc ARE the plan |
| JavaScript | Consider TS analytics module, or YAML → codegen |
| Python/Ruby/Go | YAML tracking plan → generate SDK code |
| Multi-language | YAML source of truth → generate for each |

**The best tracking plan is one that:**
1. Can't drift from implementation
2. Is reviewed in normal code review
3. Provides IDE/compiler enforcement
4. Documents intent, not just shape
