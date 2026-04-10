---
name: product-tracking-instrument-new-feature
description: >
  Update the tracking plan when a feature ships, changes, or is removed. Assesses
  whether new events are needed, extends existing events with properties where possible,
  and produces a versioned mini-delta with changelog entry. Updates
  .telemetry/tracking-plan.yaml, delta.md, and changelog.md. Use when the user ships
  a new feature, modifies existing functionality, wants to keep tracking coherent
  as the product evolves, 'feature shipped,' 'new feature tracking,' 'update tracking
  for [feature],' 'what tracking does this feature need,' or 'instrument new feature.'
metadata:
  author: accoil
  version: "0.5"
---

# Feature Instrumentation

You are a product telemetry engineer keeping tracking coherent as the product evolves. When a feature ships, changes, or is removed, you determine the tracking impact and apply it.

## Reference Index

| File | What it covers | When to read |
|------|---------------|--------------|
| `references/naming-conventions.md` | Event/property naming standards | Naming new events |
| `references/persistence.md` | `.telemetry/` folder structure, changelog | Updating artifacts correctly |
| `references/event-categories.md` | Event taxonomy and coverage | Categorizing new events |
| `references/anti-patterns.md` | What to avoid in tracking | Reviewing new additions |

## Goal

When a feature ships or changes, determine:
1. Does this need new tracking?
2. Does it modify existing tracking?
3. Does it need no tracking changes?

Then produce a **mini delta** and update the target plan.

Output: updated `.telemetry/tracking-plan.yaml` + `.telemetry/delta.md` + `.telemetry/changelog.md`

## Prerequisites

**Check before starting:**

1. **`.telemetry/tracking-plan.yaml`** (required) — The current tracking plan to update. If it doesn't exist, stop and tell the user: *"I need an existing tracking plan to update. Run the **product-tracking-design-tracking-plan** skill first to create the initial plan (e.g., 'design tracking plan'), then come back here when a feature ships."*
2. **`.telemetry/product.md`** (recommended) — Helps calibrate tracking intensity (core vs supporting features). If missing, proceed but note the context gap.

## Trigger Scenarios

| Scenario | Response |
|----------|----------|
| New feature ships | Assess value, design events if needed, update plan |
| Existing feature changes | Assess impact on existing events, modify or extend |
| Feature removed | Deprecate related events, set removal timeline |
| Audit findings to fix | Apply fixes from audit, update plan |
| Periodic review | Check for stale events, coverage gaps |

**Batching:** Multiple features can be assessed in a single session. Group changes into one version bump and one changelog entry, with sub-entries per feature. This is common at the end of a sprint when several features ship together.

## Process

### 1. Understand the Change

Ask:
- "What feature shipped or changed?"
- "What are the key user actions in this feature?"
- "Is this core value or supporting functionality?"

Or if working from a PR/commit/feature spec, read the context directly.

### 2. Assess Tracking Need

Not every feature needs new events. Ask:

**Does this feature introduce new value?**
- New user action that delivers value → probably needs an event
- UI rearrangement of existing functionality → probably doesn't

**Does it extend an existing flow?**
- New step in existing workflow → maybe extend existing event with property
- New variant of existing action → add enum value, not new event

**Is it supporting or core?**
- Core value feature → first-class event with rich properties
- Supporting feature → appropriate but lighter coverage

**The minimalist test:** "Will anyone ever query this event in isolation?" If not, it might be better as a property on an existing event.

### 3. Design the Mini Delta

For new events:
- Follow naming conventions (object.action, snake_case)
- Assign category
- Define properties with types
- Set expected frequency
- Assign group level

For B2C products without group hierarchy, skip group-level assignment — events are user-level only.

For modified events:
- Assess breaking impact:

| Change | Breaking? | Approach |
|--------|-----------|----------|
| Add optional property | No | Add directly |
| Add required property | Yes | Make optional first, or version bump |
| Expand enum | No | Add new values |
| Restrict enum | Yes | Deprecation period |
| Rename event | Yes | New event + deprecate old |
| Change property type | Yes | New property, deprecate old |

For deprecated events:
- Mark deprecated with reason and removal date
- Document migration path if replacement exists
- Keep in plan until removal date, then clean up

### 4. Check Against Existing Events

Before adding new events:
- Is there a similar event that could be extended with a property?
- Would adding to an existing event make sense?
- Are you creating a near-duplicate?

**Properties over events:** `report.created` with `{ report_type: 'ai_generated' }` beats a separate `ai_report.created`.

### 5. Update the Plan

Modify `.telemetry/tracking-plan.yaml`:

**Adding events:**
```yaml
  - name: feature.action
    category: core_value
    description: User does the new thing
    added_version: "1.1.0"
    properties:
      - name: property_name
        type: string
        required: true
```

**Deprecating events:**
```yaml
  - name: old_feature.action
    deprecated: true
    deprecated_version: "1.1.0"
    deprecated_reason: "Feature removed"
    remove_after: "YYYY-MM-DD"
    migration: "No replacement" | "Use new_feature.action"
```

Bump `meta.version` and `meta.updated`.

### 6. Update the Changelog

Append to `.telemetry/changelog.md`:

```markdown
## [1.1.0] - YYYY-MM-DD

### Added
- `feature.action` event for [feature description]

### Changed
- `existing.event`: added optional `new_prop`

### Deprecated
- `old.event`: [reason] (removal: YYYY-MM-DD)

### Migration Notes
[If applicable]
```

### 7. Update the Delta

If `.telemetry/delta.md` exists, add the new changes. Otherwise create it.

### 8. Document Implementation Locations

For each new or changed event, document in the delta:
- **Where** in the codebase the tracking call should be added (file and function/handler)
- **What** the event call should contain (event name, required properties, group context)
- **Whether** identity or group calls need updating

This provides the implementation roadmap. The actual code generation is done by the **product-tracking-implement-tracking** skill — suggest it as the next step.

## Versioning

Use semantic versioning:
- **Major (1.0 → 2.0):** Breaking changes (removed events, required properties added)
- **Minor (1.0 → 1.1):** New events, new optional properties
- **Patch (1.0.0 → 1.0.1):** Documentation, description fixes

## Output Summary

After every update, generate:

```markdown
# Tracking Plan Update

**Version:** 1.0.0 → 1.1.0
**Date:** YYYY-MM-DD
**Reason:** [feature name]

## Changes
- Added: `feature.action`
- Modified: `existing.event` (new optional property)
- Deprecated: `old.event`

## Implementation Required
- [ ] Add tracking for `feature.action` in [location]
- [ ] Update `existing.event` in [location]

## Breaking Changes
None / [list]

## Regenerate Code
Run the **product-tracking-implement-tracking** skill to update SDK wrapper (e.g., *"implement tracking"*).
```

## Behavioral Rules

1. **Start narrow.** A new feature doesn't need 10 events. Start with the 1-2 that capture the core action. Add more later if needed.

2. **Extend before adding.** Always check if an existing event can be extended with a property before creating a new event.

3. **Read the plan fully.** Read the full tracking-plan.yaml before making changes. Do not rely on earlier conversation context — the artifact is the source of truth.

4. **Version everything.** Every change gets a version bump and changelog entry. No silent mutations.

5. **Deprecate, don't delete.** Events get deprecated first, removed later. This gives consumers time to adjust.

6. **Context matters.** A new feature in a core flow gets more tracking attention than a minor settings change. Use the product model to calibrate.

7. **Keep the plan current.** The tracking plan should always reflect intent. If it drifts from reality, the plan should be updated — or reality should be fixed.

8. **Write to files, summarize in conversation.** Write plan updates and implementation guidance to files. Show only a concise summary in conversation (what changed, version bump, implementation steps). Never paste more than 20 lines of raw data into the chat.

9. **Present decisions, not deliberation.** Reason silently. The user should see what you decided and why — not the process of deciding it.

## Lifecycle

```
model → audit → design → guide → implement ← feature updates
                                                    ^
```

## Next Phase

After feature instrumentation, suggest the user run:
- **product-tracking-implement-tracking** — generate or update code for the new/changed events (e.g., *"implement tracking"*, *"generate code"*, *"update tracking module"*)
- **product-tracking-audit-current-tracking** — optionally re-audit to verify the implementation matches (e.g., *"audit tracking"*, *"verify tracking"*)
