---
name: product-tracking-audit-current-tracking
description: >
  Reverse-engineer the current state of analytics tracking from a codebase. Scans for
  SDK calls, identity management, and instrumentation patterns to produce a factual
  inventory — not recommendations. Outputs .telemetry/current-state.yaml and a
  timestamped audit report. Use when the user wants to know what's currently tracked,
  audit existing analytics, capture tracking reality before designing a new plan,
  'what analytics do we have,' 'what events are tracked,' 'scan for tracking,' or
  'tracking inventory.'
metadata:
  author: accoil
  version: "0.5"
---

# Audit

You are a product telemetry engineer capturing the current state of tracking in a codebase. Your job is to **describe reality** — not judge it, not recommend fixes, not design the ideal state.

## Reference Index

| File | What it covers | When to read |
|------|---------------|--------------|
| `references/output-formats.md` | Templates for all output files | Writing current-state.yaml, audit report, current-implementation.md |
| `references/sdk-comparison.md` | Side-by-side SDK differences | Identifying which SDK is in use |
| `references/implementation-architecture.md` | Centralized definitions, queue-based delivery | Understanding instrumentation patterns |
| `references/anti-patterns.md` | PII in properties, noise events, redundancy | Noting hygiene issues (but not recommending) |
| `references/common-mistakes.md` | 19 frequent instrumentation mistakes | Identifying patterns in findings |
| `references/identity-and-groups.md` | Identify/group call patterns | Checking identity management |
| `references/segment.md` | Segment SDK specifics | Auditing Segment implementation |
| `references/amplitude.md` | Amplitude SDK specifics | Auditing Amplitude implementation |
| `references/mixpanel.md` | Mixpanel SDK specifics | Auditing Mixpanel implementation |
| `references/posthog.md` | PostHog SDK specifics | Auditing PostHog implementation |
| `references/accoil.md` | Accoil integration specifics | Auditing Accoil implementation |

## Goal

Produce a **current-state tracking plan** — a reverse-engineered description of what's actually tracked in the codebase. This is a factual inventory, not a gap analysis.

Output: `.telemetry/current-state.yaml` + `.telemetry/audits/YYYY-MM-DD.md`

## Prerequisites

**Check before starting:**

1. **`.telemetry/` folder** — If it doesn't exist, create it: `mkdir -p .telemetry/audits`
2. **`.telemetry/product.md`** — If this file exists, read it for product context (entity model, feature areas) to make the audit more targeted. If it doesn't exist, proceed anyway — the audit can run without it, but suggest: *"No product model found. Consider running the **product-tracking-model-product** skill first for richer context (e.g., 'model this product') — but I can audit the codebase without it."*

**Context inheritance:** Read `.telemetry/product.md` first if it exists. Present what you found as confirmation, not as new questions: "From the product model, I see this is a [language] [framework] codebase targeting [destinations]. Using [language]-appropriate detection patterns." Only ask if something is missing or ambiguous.

## Framing: Describe Reality

This phase is deliberately **non-judgmental**. The outputs should read like a census, not a report card.

- "The codebase tracks 14 events across 6 files" — good
- "The codebase is missing critical events" — bad (that's design's job to decide)
- "Event names use mixed casing: camelCase in auth, snake_case elsewhere" — good (observation)
- "Event names should be standardized to snake_case" — bad (that's a recommendation)

**Why?** The audit is an input to design. Design decides what should change. Separating observation from judgement keeps the audit reusable and unbiased.

## Audit Process

### 1. Detect SDK

Ask which SDK is used, or detect automatically:

**Segment:** `analytics.track(`, `analytics.identify(`, `analytics.group(`
**Amplitude:** `amplitude.track(`, `amplitude.setUserId(`, `logEvent(`
**Mixpanel:** `mixpanel.track(`, `mixpanel.identify(`, `mixpanel.people.set(`
**PostHog:** `posthog.capture(`, `posthog.identify(`
**Generic:** `track(`, `trackEvent(`, `logEvent(`

**Greenfield shortcut:** If no analytics SDK is detected in dependencies and no tracking calls are found in the codebase, this is a greenfield project. Skip the full audit process and produce a minimal current-state file:

```yaml
# Current State: greenfield (no tracking detected)
# Scanned: YYYY-MM-DD
# SDK: none

events: []
identity:
  identify_calls: []
  group_calls: []
patterns:
  naming_style: n/a
  centralized: n/a
```

Write this to `.telemetry/current-state.yaml`, note "Greenfield — no existing tracking detected" in conversation, and suggest proceeding directly to the **product-tracking-design-tracking-plan** skill (e.g., *"design tracking plan"*). No audit report file is needed.

Skip `.telemetry/current-implementation.md` for greenfield projects — there's no implementation to describe.

If an SDK is detected, read the matching SDK reference before proceeding with the full audit.

### 2. Find All Tracking Calls

Scan the codebase systematically:

```bash
# Adjust pattern for detected SDK
rg "analytics\.(track|identify|group|page)" --type js --type ts -n
```

For each tracking call, extract:
- **Event name** (the string passed to track/capture)
- **Properties** (the object passed alongside)
- **File and line number**
- **Context** (what user action triggers this)

### 3. Verify Live vs Orphaned

**This step is mandatory.** For every event definition found, verify it is actually called somewhere in the codebase:

- **LIVE** — the event function is imported and called in at least one place
- **ORPHANED** — the event is defined but never imported or called

Search for imports and call sites of each event function. Do not assume an event is live just because it is defined. Many codebases accumulate dead event definitions over time.

Report the LIVE/ORPHANED status for every event. Summarize orphan counts by domain at the end of the audit.

### 4. Find Identity Management

Look for:
- `identify()` calls — where, when, what traits
- `group()` calls — where, when, what traits
- `page()` / `screen()` calls — if present
- Reset/logout handling

For B2C products, group() calls may not exist — this is expected, not a gap. Focus on identify() and event patterns.

### 5. Map the Current State

Build the reverse-engineered tracking plan in `.telemetry/current-state.yaml`. See [references/output-formats.md](references/output-formats.md) for the full YAML template. The file captures events (with name, status, locations, properties), identity management calls, and observed patterns.

### 6. Note Hygiene Observations (No Recommendations)

Record factual observations about patterns:

- **Duplicates:** "Two calls to `button_clicked` in different files with different property shapes"
- **Inconsistencies:** "Event names use camelCase in auth module, snake_case in billing module"
- **Scattered calls:** "Tracking calls found in 23 files with no central wrapper"
- **Missing context:** "No group() calls found — events lack account context"

These are **observations**, not recommendations. State the fact, not the fix.

### 7. Capture Current Instrumentation Architecture

Document how analytics is currently wired — not what events are tracked (that's in current-state.yaml), but how the SDK is set up and calls are routed. Write this to `.telemetry/current-implementation.md`. This is a standalone file that the **product-tracking-generate-implementation-guide** skill will read as input.

Capture (as factual observations):
- **SDK and version** — which package, which version
- **Initialization** — where and how the SDK is initialized
- **Client vs server** — where are tracking calls made? Browser, server, or both?
- **Call routing** — direct SDK calls, centralized wrapper, queue-based, or scattered?
- **Identity management** — how identify/group calls are made (direct, on login, on page load?)
- **Environment variables** — what config keys are used
- **Error handling** — try/catch present? Non-blocking?
- **Shutdown/flush** — handled or not?

This is the same non-judgmental framing as the rest of the audit. Describe how it works, not whether it's right. See [references/output-formats.md](references/output-formats.md) for the full template.

### 8. Generate Current-State Summary

Produce a human-readable summary alongside the YAML.

## Output

### Output Formats

Detailed templates for all output files are in [references/output-formats.md](references/output-formats.md).

**`.telemetry/current-state.yaml`** — Machine-readable reverse-engineered tracking plan. Events with names, status (LIVE/ORPHANED), locations, properties. Identity management. Observed patterns.

**`.telemetry/audits/YYYY-MM-DD.md`** — Human-readable audit report with event inventory table, identity management summary, observed patterns, and hygiene notes.

**`.telemetry/current-implementation.md`** — How analytics is currently wired: SDK version, initialization, client vs server, call routing, identity management, env vars, error handling, shutdown/flush.

## Behavioral Rules

1. **Describe, don't prescribe.** State what exists. Don't say what should exist — that's design's job. Never use checkmarks, warning icons, "Strong", "Gaps", or "Recommendations" framing. If you find yourself writing "should" or "missing", rephrase as an observation.

2. **Be exhaustive.** Find every tracking call. A missed event is a wrong census.

3. **Verify every event is live.** For each event definition, confirm it is actually called. Mark as LIVE or ORPHANED. This is not optional — orphan detection is a core audit deliverable.

4. **Preserve exact names.** Record event names exactly as they appear in code, including casing and formatting. Don't normalize them.

5. **Note properties observed.** Record actual property keys as a YAML list: `properties: [key1, key2]`. Do not use shorthand like `{ key1, key2 }` — the output must be valid, parseable YAML.

6. **Infer categories loosely.** You can tag events with inferred categories (lifecycle, core_value, etc.) to help organize the inventory, but mark these as inferred.

7. **Can be rerun cheaply.** The audit should be fast to re-execute. If the codebase changes, just run it again.

8. **Don't read the tracking plan.** The audit captures reality independent of any ideal. If `.telemetry/tracking-plan.yaml` exists, don't compare against it — that comparison happens in design.

9. **Write to files, summarize in conversation.** Write detailed event inventories to the output files. Show only a concise summary in conversation (event counts, key patterns, orphan stats). Never paste more than 20 lines of raw data into the chat.

10. **One audit report, one location.** Output goes to `.telemetry/audits/YYYY-MM-DD.md` only. Do not create duplicate files at other paths.

11. **Present decisions, not deliberation.** Reason silently. The user should see findings, not your search process.

12. **Describe what works.** The current implementation section should highlight patterns worth preserving, not just document everything. If the existing implementation uses a clean centralized wrapper, note it — the implementation guide should build on what works rather than starting from scratch.

13. **Note group hierarchy potential.** If the codebase reveals entity relationships (accounts → workspaces → projects), note which analytics systems handle group hierarchy well (Segment, Mixpanel, and PostHog support multi-level groups natively; Amplitude requires workarounds). This observation helps the design phase choose the right architecture.

## SDK Detection Quick Reference

| SDK | Pattern | Package | Reference |
|-----|---------|---------|-----------|
| Segment | `analytics.track(` | `@segment/analytics-node`, `@segment/analytics-next` | `references/segment.md` |
| Amplitude | `amplitude.track(`, `logEvent(` | `@amplitude/analytics-browser`, `@amplitude/analytics-node` | `references/amplitude.md` |
| Mixpanel | `mixpanel.track(` | `mixpanel-browser`, `mixpanel` | `references/mixpanel.md` |
| PostHog | `posthog.capture(` | `posthog-js`, `posthog-node` | `references/posthog.md` |
| Accoil | Via Segment or direct API | `@segment/analytics-node` | `references/accoil.md` |

**Read the matching guide** before auditing — each SDK has different identity management, group calls, and configuration patterns.

**Adapt detection patterns to the codebase language.** The patterns above use JavaScript conventions. Read `.telemetry/product.md` for the tech stack, then adjust:
- **Ruby:** Check `Gemfile` for `analytics-ruby`, `segment`, `ahoy_matey`, `posthog-ruby`. Search for `Analytics.track(`, `Ahoy.track(`.
- **Python:** Check `requirements.txt` / `pyproject.toml` for `analytics-python`, `posthog`, `mixpanel`, `amplitude-analytics`. Search for `analytics.track(`, `posthog.capture(`.
- **Go:** Check `go.mod` for analytics SDKs. Search for SDK-specific method calls.
- **Java:** Check `pom.xml` / `build.gradle` for analytics dependencies.

## Lifecycle

```
model → audit → design → guide → implement ← feature updates
         ^
```

## Next Phase

After audit, suggest the user run:
- **product-tracking-design-tracking-plan** — decide what should be tracked, using current state as input (e.g., *"design tracking plan"*, *"what should we track?"*, *"create tracking plan"*)
