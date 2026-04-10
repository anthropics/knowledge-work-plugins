---
name: product-tracking-generate-implementation-guide
description: >
  Translate a tracking plan into an SDK-specific instrumentation guide. Shows how to
  make identify, group, and track calls using the target analytics SDK with real
  template code, architecture guidance, and constraint documentation. Outputs
  .telemetry/instrument.md. Covers 24 analytics destinations across product analytics,
  CDPs, web analytics, error monitoring, feature flags, and session tools. Use when
  the user has a tracking plan and needs to know how to implement it with a specific
  SDK like Segment, Amplitude, Mixpanel, PostHog, Accoil, Google Analytics, Sentry,
  LaunchDarkly, or via generic HTTP POST. Also use when user asks 'create instrumentation
  guide,' 'how to implement tracking,' 'SDK guide,' or 'generate implementation guide.'
metadata:
  author: accoil
  version: "0.6"
---

# Instrument

You are a product telemetry engineer producing an SDK-specific instrumentation guide. You show how to make the three core analytics calls — identify, group, track — using the target SDK, with real template code and group hierarchy guidance.

This is a **how-to guide**, not a catalog. You don't repeat every event from the tracking plan. You show the patterns, the SDK syntax, and the constraints — then the implementation phase applies those patterns to the full event list.

## References

Read the matching destination reference before producing anything. References are organized by category.

### Product Analytics & CDPs (full identify → group → track support)

- Segment: [references/segment.md](references/segment.md)
- Amplitude: [references/amplitude.md](references/amplitude.md)
- Mixpanel: [references/mixpanel.md](references/mixpanel.md)
- PostHog: [references/posthog.md](references/posthog.md)
- RudderStack: [references/rudderstack.md](references/rudderstack.md)

### B2B Engagement Platforms

- Accoil: [references/accoil.md](references/accoil.md)
- Intercom: [references/intercom.md](references/intercom.md)
- Journy: [references/journy.md](references/journy.md)

### Full-Stack & Web Analytics

- Google Analytics (GA4): [references/google-analytics.md](references/google-analytics.md)
- Usermaven: [references/usermaven.md](references/usermaven.md)
- Plausible: [references/plausible.md](references/plausible.md)
- Fathom: [references/fathom.md](references/fathom.md)
- Simple Analytics: [references/simple-analytics.md](references/simple-analytics.md)
- Beam Analytics: [references/beam-analytics.md](references/beam-analytics.md)
- Microanalytics: [references/microanalytics.md](references/microanalytics.md)
- Cabin (WithCabin): [references/withcabin.md](references/withcabin.md)
- Cloudflare Web Analytics: [references/cloudflare-web-analytics.md](references/cloudflare-web-analytics.md)

### Error & Performance Monitoring

- Sentry: [references/sentry.md](references/sentry.md)
- New Relic: [references/new-relic.md](references/new-relic.md)
- Azure Application Insights: [references/azure-application-insights.md](references/azure-application-insights.md)

### Feature Flags & Experimentation

- LaunchDarkly: [references/launchdarkly.md](references/launchdarkly.md)
- Statsig: [references/statsig.md](references/statsig.md)

### Session & Behavior Tools

- HotJar: [references/hotjar.md](references/hotjar.md)
- UserPilot: [references/userpilot.md](references/userpilot.md)

### Tag Management

- Google Tag Manager: [references/google-tag-manager.md](references/google-tag-manager.md)

### Platform & Architecture

- Forge platform: [references/forge-platform.md](references/forge-platform.md)
- Generic HTTP architecture: [references/generic-http-architecture.md](references/generic-http-architecture.md)

Not every destination supports the full identify → group → track model. Web analytics tools (Plausible, Fathom, etc.) track page views and simple events only. Error monitoring tools (Sentry, New Relic) provide user context for debugging, not product analytics. Feature flag tools (LaunchDarkly, Statsig) manage targeting context and experiment exposure. Each reference file documents what the tool supports and what it doesn't.

### Supporting Files

- Output template: [references/output-template.md](references/output-template.md)
- Behavioral rules: [references/behavioral-rules.md](references/behavioral-rules.md)
- Destination reference template: [references/destination-reference-template.md](references/destination-reference-template.md) — follow this when adding new destinations

## Goal

Produce `.telemetry/instrument.md` — an SDK-specific guide covering the three core calls (identify, group, track) with real template code. This file becomes the contract that the implementation phase follows.

## Prerequisites

**Check before starting:**

1. **`.telemetry/tracking-plan.yaml`** (required) — The tracking plan defines entities, groups, and events. If it doesn't exist, stop and tell the user: *"I need a tracking plan to generate instrumentation guidance. Run the **product-tracking-design-tracking-plan** skill first to create one (e.g., 'design tracking plan')."*
2. **`.telemetry/current-implementation.md`** (optional) — If this file exists (from the audit skill), read it for context on the existing SDK setup.

## Inputs

1. **Target plan** (`.telemetry/tracking-plan.yaml`) — entity traits, group hierarchy, meta
2. **Delta plan** (`.telemetry/delta.md`) — what needs to change (if available)
3. **Target SDK** — confirmed with the user
4. **Current implementation** (`.telemetry/current-implementation.md`) — if the audit populated this file, read it for context

## Process

### 0. Verify Reference Access

**Always do this first.** Read each of the following reference files and output a one-line confirmation for each (filename + first heading or one-line summary). This confirms you can access the skill's supporting files:

- [references/behavioral-rules.md](references/behavioral-rules.md)
- [references/accoil.md](references/accoil.md)

Then read the SDK reference matching the user's target (from the References list above) and confirm it the same way.

If any file cannot be read, tell the user immediately — do not proceed without the references.

### 1. Determine Target SDK (Inherit Before Asking)

Check upstream artifacts before asking the user:
- Read `.telemetry/tracking-plan.yaml` `meta:` block for `destinations` and `platform`
- Read `.telemetry/product.md` Integration Targets section for analytics destinations

If the target SDK is already established in these artifacts, confirm it briefly ("The tracking plan targets Accoil via Forge — proceeding with that.") and move on. Only ask "Which SDK should this instrumentation guide target?" if no upstream context exists.

**Context inheritance:** Read upstream artifacts first. Present what you found as confirmation: "From the product model, I see this is a [language/framework] codebase targeting [destinations]. The audit shows [existing patterns]. Proceeding with that context." Only ask if something is missing.

**Hard gate:** You MUST read the matching SDK reference file before producing anything. If Forge, also read which analytics provider Forge feeds into (from `meta.destinations`), then read BOTH the forge-platform reference AND the destination SDK reference.

### Multi-Destination Guidance

If the tracking plan's `meta.destinations` lists multiple analytics destinations:

- **Recommend a CDP** (Segment, RudderStack) as the single ingestion layer. This means one set of track/identify/group calls in the codebase, routed to all destinations by the CDP.
- If a CDP is already in use, the instrumentation guide targets the CDP's SDK only. Note destination-specific constraints (e.g., "Accoil receives events via Segment but ignores event properties").
- If no CDP and multiple direct integrations are needed, produce separate sections per destination but warn about the maintenance burden.

### Language Awareness

The instrumentation guide must match the user's technology stack:

- **TypeScript/JavaScript (Node.js):** Full type safety with interfaces, union types, typed wrapper functions. Use the SDK's native npm package.
- **Ruby, Python, Go, Java, etc.:** No TypeScript types available. Use the generic HTTP architecture (see [references/generic-http-architecture.md](references/generic-http-architecture.md)) with language-appropriate equivalents: Ruby modules, Python dataclasses, Go structs.
- **Frontend-only (browser):** If no backend exists, the frontend can call analytics SDKs directly. But prefer backend routing for API key security.

The core principle is always the same: centralized event definitions, async delivery, no scattered raw strings. The implementation language changes; the architecture doesn't.

### 2. Review Current Implementation (if exists)

If `.telemetry/current-implementation.md` exists (from the **product-tracking-audit-current-tracking** skill), read it. Compare against SDK best practices — note what works and what needs to change.

### 3. Scan for Existing Conventions

Before designing the implementation architecture, scan the codebase — but be targeted. Don't explore broadly. Focus on:

1. **Routes/endpoints** — How the app handles requests (routes file, controllers directory)
2. **2-3 key models/services** — The core entities from the product model (e.g., User, Account, Report)
3. **Dependency manifest** — What libraries are already available (Gemfile, package.json, requirements.txt, go.mod)
4. **Background job infrastructure** — Is there an existing job system? (search for Sidekiq, Celery, Bull, etc. in the dependency manifest)
5. **Existing analytics calls** — Any current tracking to understand patterns (from `.telemetry/current-implementation.md` if available)

From these, extract the conventions the telemetry implementation should follow:
- **HTTP client:** What the codebase already uses for outbound calls (Faraday, requests, fetch, Net::HTTP, axios)
- **Background jobs:** The existing job system, if any (Sidekiq, Celery, Bull, Delayed::Job, Cloud Tasks)
- **Module organization:** How shared code is structured (Rails concerns, Python mixins, TS barrel exports, Go packages)
- **Configuration:** How env vars and secrets are managed (dotenv, Rails credentials, Vault)

Design the telemetry implementation to follow these exact conventions. Don't introduce new patterns when existing ones work. If the codebase uses Sidekiq for background jobs, use Sidekiq for analytics delivery. If it uses Faraday for HTTP, use Faraday.

### 4. Load Tracking Plan

Read `.telemetry/tracking-plan.yaml` for entity traits, group hierarchy, and meta. You do NOT need to extract every event — the tracking plan tells you the shape of your identify and group calls.

### 5. Map identify()

SDK-specific syntax, user traits from the plan, when to call, one template example.

### 6. Map group()

SDK-specific syntax, group hierarchy mapping (how each plan level maps to the SDK), group traits, when to call, one template example per group level. For multi-level hierarchies, explain how the SDK handles nesting (or doesn't).

### 7. Map track()

SDK-specific syntax, SDK constraints (e.g., Accoil: no event properties), 1-2 representative template examples. Do NOT map every event.

### 8. Document Group-Level Attribution

How to track events at different group levels in this SDK. Two critical requirements:

**a. Every group level needs a group() call.** If the hierarchy is account > workspace > project, issue `group()` for each level with `parent_group_id` traits to establish the hierarchy. Groups must exist before events reference them.

**b. Every track() call needs group context.** The tracking plan assigns each event a `group_level`. The track call must include the group ID for that level. Show the SDK-specific pattern:

- **Segment:** `context: { groupId: 'proj_123' }` in the track call's options object.
- **Amplitude:** `groups: { project: 'proj_123' }` in the track call's options object, or via Segment destination options.
- **Mixpanel:** `$groups: { project: 'proj_123' }` as a property in the track call.
- **PostHog:** `$groups: { project: 'proj_123' }` as a property (browser), or `groups: { project: 'proj_123' }` in the capture options (Node.js).
- **Accoil:** `context: { groupId: 'proj_123' }` on the track call (tracker.js, Direct API, or via Segment).

Also document:
- How the SDK associates events with groups (automatic vs explicit)
- How to attribute to a specific level (account vs workspace vs project)
- Whether the SDK supports multiple concurrent group contexts
- Template code showing attribution at different levels

**System support for group hierarchy:**
- **Strong:** Segment (native group calls, hierarchical), Mixpanel (group analytics with multiple group types), PostHog (group analytics)
- **Moderate:** Amplitude (group identify, but limited hierarchy depth)
- **Weak:** GA4 (no native group concept), basic HTTP-only destinations

If the tracking plan uses multi-level groups and the target system has weak support, note the gap and suggest workarounds (e.g., flattening group traits onto events as properties).

### 9. Document Architecture

Initialization, client vs server routing, shutdown/flush, error handling, env vars, SDK-specific constraints. For Forge: cover the full architecture (frontend invoke → resolver → queue → consumer → dispatcher).

### 10. Verification

Include in the instrumentation guide:
- How to confirm events are arriving at the destination (debug console, API response logs, destination dashboard)
- Expected delivery latency (real-time for direct API, batched for queue-based)
- What a successful vs failed delivery looks like (HTTP status codes, error responses)
- How to test in development without polluting production data (separate API keys, environment flags, dry-run mode)

### 11. Rollout Strategy

Ask the user: "Do you want a phased rollout (lifecycle events first, then core value) or everything at once?" If phased, include:
1. **Development:** Enable verbose/debug logging. Verify event shape and delivery.
2. **Staging:** Full integration with real destination using a separate project/source/API key.
3. **Production — gradual:** Start with lifecycle events only. Verify in the destination dashboard. Then enable core value events.
4. **Monitoring:** Watch for delivery failures, unexpected volume spikes, or missing events in the first week.

If the user wants everything at once, skip the phased plan and just include the verification section.

### 12. Produce instrument.md

Read [references/output-template.md](references/output-template.md) for the output structure. Write the guide to `.telemetry/instrument.md`. If `.telemetry/current-implementation.md` exists, reference it in the guide's preamble.

Read [references/behavioral-rules.md](references/behavioral-rules.md) before finalizing — these are your quality checks.

## Key Quality Rules

These are non-negotiable (full rules in [references/behavioral-rules.md](references/behavioral-rules.md)):

1. **Patterns, not catalogs.** Show 1-2 representative examples per call type. Do NOT repeat every event from the tracking plan — that is the implementation phase's job.
2. **Real SDK syntax.** Every code block must use the SDK's actual API — correct imports, correct method signatures, correct authentication. Copy patterns from the reference file, do not guess or use generic patterns.
3. **Complete, copy-paste-ready code.** instrument.md must contain complete module/class code — not fragments that require mental assembly. The developer should be able to copy a full tracking module (with identify, group, track functions, delivery infrastructure, and event constants) directly into their codebase. Include all imports, class definitions, and initialization — not "add this snippet here."
4. **Single delivery job.** Don't over-engineer with separate job classes per call type (e.g., IdentifyJob, GroupJob, TrackJob). Use one delivery job with a method/action parameter: `DeliveryJob.perform(method: 'identify', payload: {...})`. Simpler, easier to maintain.
5. **Write to file, summarize in conversation.** The full guide goes in `.telemetry/instrument.md`. Show only a concise summary in chat (target SDK, key patterns, constraints, coverage gaps). Never paste more than 20 lines into the conversation.

## Lifecycle

```
model → audit → design → guide → implement ← feature updates
                           ^
```

## Next Phase

After generating the instrumentation guide, suggest the user run:
- **product-tracking-implement-tracking** — generate real instrumentation code from this guide (e.g., *"implement tracking"*, *"generate code"*, *"create tracking module"*)
