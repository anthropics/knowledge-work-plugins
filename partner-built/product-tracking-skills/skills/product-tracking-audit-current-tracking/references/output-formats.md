# Output Format Templates

Detailed templates for all audit output files.

---

## `.telemetry/current-state.yaml`

Machine-readable reverse-engineered tracking plan.

```yaml
# Current State: reverse-engineered from codebase
# Scanned: YYYY-MM-DD
# SDK: [detected SDK]

events:
  - name: "[exact event name from code]"
    status: LIVE  # or ORPHANED
    locations:
      - file: "src/auth/signup.ts"
        line: 42
    properties: [source, user_id]  # list format, must be valid YAML
    source: frontend  # or backend

  - name: "[next event]"
    # ...

identity:
  identify_calls:
    - location: "src/auth/login.ts:34"
      traits_set: [email, name, role]
  group_calls:
    - location: "[file:line]"
      group_type: "[type]"
      traits_set: [name, plan]
  # or: "No group() calls found"

patterns:
  naming_style: "[observed: camelCase / snake_case / mixed / Title Case]"
  naming_format: "[observed: object.action / action_object / free-form / mixed]"
  centralized: "[true/false — are tracking calls in a wrapper or scattered?]"
  error_handling: "[try/catch present? non-blocking?]"
```

---

## `.telemetry/audits/YYYY-MM-DD.md`

Human-readable audit report.

```markdown
# Tracking Audit: YYYY-MM-DD

**Codebase:** [path]
**SDK:** [name and package]

## Current Tracking Inventory

| # | Event Name | Category (inferred) | Locations | Properties |
|---|-----------|--------------------|-----------|-----------|
| 1 | `event_name` | [lifecycle/value/config/...] | `file:line` | prop1, prop2 |
| ... | ... | ... | ... | ... |

**Total events found:** [count]

## Identity Management

| Call Type | Present | Location | Details |
|-----------|---------|----------|---------|
| identify() | YES/NO | `file:line` | Traits: [list] |
| group() | YES/NO | `file:line` | Group type: [type], Traits: [list] |
| page()/screen() | YES/NO | `file:line` | [details] |
| reset()/logout | YES/NO | `file:line` | [details] |

## Observed Patterns

- **Naming style:** [camelCase / snake_case / mixed / Title Case]
- **Naming format:** [object.action / action_object / free-form / mixed]
- **Centralization:** [wrapper/scattered] — [details]
- **Error handling:** [present/absent/partial]
- **Blocking calls:** [yes/no — are track calls awaited on critical paths?]

## Hygiene Notes

*Factual observations, not recommendations.*

1. [Observation about duplicates, inconsistencies, etc.]
2. [...]
```

---

## `.telemetry/current-implementation.md`

How analytics is currently wired. This file is read by the **product-tracking-generate-implementation-guide** skill as input.

```markdown
## Current Implementation

**SDK:** [name and version]
**Captured:** YYYY-MM-DD

### Initialization
[Where and how the SDK is initialized. File paths, config patterns.]

### Client vs Server
[Where tracking calls are made — browser, server, or both.]

### Call Routing
[Direct SDK calls / centralized wrapper / queue-based / scattered]

### Identity Management
[How identify and group calls are made — on login, on page load, etc.]

### Environment Variables
[What config keys are used — e.g., SEGMENT_WRITE_KEY, ANALYTICS_API_KEY]

### Error Handling
[Try/catch present? Non-blocking? Silent failures?]

### Shutdown / Flush
[Handled or not? How?]
```
