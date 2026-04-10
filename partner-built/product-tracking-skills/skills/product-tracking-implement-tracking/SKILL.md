---
name: product-tracking-implement-tracking
description: >
  Generate real instrumentation code from the tracking plan and instrumentation guide.
  Produces typed SDK wrapper functions, identity management, and integration guidance.
  Outputs files in a tracking/ directory. Use when the user wants to generate or
  regenerate tracking code, implement the delta plan, turn the instrumentation guide
  into working code, 'implement tracking,' 'generate code,' 'create tracking module,'
  or 'build analytics SDK wrapper.'
metadata:
  author: accoil
  version: "0.5"
---

# Implementation

You are a product telemetry engineer executing the delta plan — translating the difference between current tracking and the target plan into real, working instrumentation code.

## Reference Index

| File | What it covers | When to read |
|------|---------------|--------------|
| `references/naming-conventions.md` | Event/property naming standards | Ensuring generated code follows conventions |
| `references/sdk-comparison.md` | Side-by-side SDK differences | Understanding SDK trade-offs |
| `references/implementation-architecture.md` | Centralized definitions, queue-based delivery | Structuring instrumentation code |
| `references/tracking-plan-location.md` | Where types should live in codebase | Deciding output location |

## Goal

Translate the delta plan (or full target plan) into implementation-ready code. This means:
1. Typed event definitions matching the tracking plan
2. SDK wrapper functions for each event
3. Identity management (identify/group)
4. Validation helpers (optional, for dev-time)
5. Integration guidance for existing codebase

Output: tracking code + updated tracking plan reflecting implemented reality

## Prerequisites

**Context inheritance:** Read `.telemetry/instrument.md` and `.telemetry/product.md` before asking any questions. The instrumentation guide contains the SDK patterns, architecture decisions, and hook placement. The product model contains the tech stack and language. Present what you found: "The instrumentation guide targets [SDK] with [architecture pattern] in a [language/framework] codebase. Proceeding with that." Only ask if something is missing.

**Check before starting:**

1. **`.telemetry/instrument.md`** (required) — The SDK-specific instrumentation guide. If it doesn't exist, stop and tell the user: *"I need an instrumentation guide to generate code from. Run the **product-tracking-generate-implementation-guide** skill first to create one (e.g., 'create instrumentation guide')."*
2. **`.telemetry/tracking-plan.yaml`** (required) — The target tracking plan. If it doesn't exist, stop and tell the user: *"I need a tracking plan to generate types and functions from. Run the **product-tracking-design-tracking-plan** skill first to create one (e.g., 'design tracking plan')."*
3. **`.telemetry/delta.md`** (recommended) — If available, prioritize implementing the delta. If only the target plan exists, implement the full plan.

## Inputs

1. **Instrumentation guide** (`.telemetry/instrument.md`) — SDK-specific patterns, template code, API endpoints
2. **Target plan** (`.telemetry/tracking-plan.yaml`) — what should exist
3. **Delta plan** (`.telemetry/delta.md`) — what needs to change (if available)
4. **Current state** (`.telemetry/current-state.yaml`) — what exists now (if available)
5. **Environment** — Browser, Node.js, or both
6. **Language** — The project's primary language (TypeScript recommended for JS projects)

If a delta exists, prioritize implementing the delta. If only a target plan exists, implement the full plan.

## Implementation Process

### 1. Confirm Configuration

Read `.telemetry/instrument.md`. This contains the SDK-specific patterns, template code, and API endpoints produced by the instrument phase. If instrument.md doesn't exist, tell the user to run the **product-tracking-generate-implementation-guide** skill first (e.g., *"create instrumentation guide"*).

Ask:
- "What language/framework does the project use?" (recommend TypeScript if applicable)
- "Browser, Node.js, or both?"

The target SDK, API endpoints, and SDK-specific patterns are already defined in instrument.md. Do not re-ask for the SDK or re-read raw SDK references — follow the instrumentation guide.

### 2. Generate Types

Generate one typed definition per event. Required properties are non-optional, optional use `?` (or the language equivalent), enums become union types, PII only in trait interfaces. Follow the entity and event shapes from the tracking plan exactly.

For B2C products without group hierarchy, skip group-related types and functions. The tracking module only needs identify() and track() wrappers.

**Example (TypeScript):**

```typescript
// Auto-generated from tracking-plan.yaml — regenerate with the implementation skill

export interface UserTraits {
  email?: string;
  name?: string;
  role: 'admin' | 'member' | 'viewer';
  created_at?: string;
}

export interface UserSignedUpEvent {
  signup_source: 'organic' | 'google' | 'invite' | 'api';
}
```

For non-TypeScript languages, use the equivalent pattern (Python dataclasses, Ruby modules, Go structs, etc.).

### 3. Generate SDK Wrapper

Generate typed wrapper functions following the patterns in `.telemetry/instrument.md`. The instrumentation guide contains the exact SDK call signatures, API endpoints, authentication patterns, and template code. Use these directly — do not deviate from the guide's patterns.

The guide covers:
- **identify()** — call signature, user traits, when to call
- **group()** — call signature, group hierarchy mapping, group traits
- **track()** — call signature, per-event mapping, SDK constraints
- **Architecture** — initialization, shutdown/flush, client vs server routing

Generate one function per event — clear API, easy to import.

### 4. Generate Validation Helpers

**Optional — skip unless requested.** Runtime validators are rarely needed in TypeScript projects where compile-time checking is sufficient. Only generate if the user requests runtime validation or the codebase uses JavaScript without TypeScript.

### 5. Generate Usage Examples

Show how to use the generated code in context:

```typescript
// On login
identifyUser('usr_123', { email: 'jane@example.com', role: 'admin' });
groupAccount('usr_123', 'acc_456', { name: 'Acme Corp', plan: 'pro' });

// When user creates a report
trackReportCreated('usr_123', {
  report_id: 'rpt_789',
  report_type: 'standard',
  template_used: false,
});
```

### 6. Generate Integration Guide

Create a README.md in the tracking/ directory as an integration guide for the codebase (not extraneous documentation). It should explain:
- How to install SDK dependencies
- How to set environment variables
- How to import and use the functions
- How to regenerate after plan changes

## Output Structure

The output structure adapts to the project's technology stack. See **Language Adaptation** below for non-TypeScript projects.

```
tracking/
├── types.ts          # TypeScript interfaces
├── tracking.ts       # SDK wrapper with typed functions
├── validate.ts       # Runtime validators (optional)
├── examples.ts       # Usage examples
├── index.ts          # Barrel export
└── README.md         # Integration guide
```

## Language Adaptation

The output structure adapts to the project's technology stack:

**TypeScript/JavaScript (default):**
```
tracking/
├── types.ts          # TypeScript interfaces
├── tracking.ts       # SDK wrapper with typed functions
├── validate.ts       # Runtime validators (optional)
├── examples.ts       # Usage examples
├── index.ts          # Barrel export
└── README.md         # Integration guide
```

**Ruby, Python, Go, or other languages:**
```
tracking/
├── events.[ext]      # Central event definitions (module/class/package)
├── tracking.[ext]    # SDK wrapper with typed/documented functions
├── examples.[ext]    # Usage examples
└── README.md         # Integration guide
```

For non-TypeScript languages:
- Replace TypeScript interfaces with language-appropriate equivalents (Ruby modules, Python dataclasses, Go structs)
- Maintain the same principle: centralized event definitions, typed/documented functions, no scattered raw strings
- If the instrumentation guide references the generic HTTP architecture, implement the queue-based pattern in the project's native language
- Skip validation helpers unless the language lacks static type checking

## Delta-Driven Implementation

When a delta plan exists, the implementation should be organized around the delta.

**Hook location mapping is this skill's job.** The instrumentation guide shows patterns and SDK syntax. This skill maps each event to the specific file and function in the codebase where the tracking call belongs. Scan the codebase to identify the right hook points — controllers, services, callbacks, handlers — for each event.

### For events to ADD:
- Generate new type interface
- Generate new tracking function
- Identify the exact file and function where the call should go
- Provide code snippet showing the call in context

### For events to RENAME:
- Generate new tracking function with correct name
- Identify files where the old call exists
- Provide search-and-replace guidance

### For events to CHANGE (wrong properties):
- Generate updated type interface
- Identify call sites
- Show before/after for each location

### For events to REMOVE:
- Identify call sites
- Provide removal guidance

## Incremental Updates

When `tracking/` code already exists from a previous run:

1. **Read existing code first.** Understand the current module structure before modifying.
2. **Apply the delta, don't regenerate.** If delta.md contains 3 new events, add 3 new functions — don't regenerate the entire module.
3. **Preserve custom modifications.** If the user has added custom logic (e.g., enrichment, conditional tracking), preserve it.
4. **Update types and exports.** Add new interfaces to types file, new functions to barrel exports.
5. **Version bump.** Update any version comments in generated files.

## Confidence Checks

Before considering implementation complete:

- [ ] Every event in the target plan has a typed function
- [ ] Identity management (identify + group) is covered
- [ ] SDK-specific patterns are correct (not generic)
- [ ] Server shutdown is handled (if Node.js)
- [ ] Environment variables are documented
- [ ] Examples cover the most common usage patterns

## Verification

Before considering implementation complete, verify the integration works:

- [ ] **Dry run:** Execute at least one track, identify, and group call in development
- [ ] **Delivery confirmation:** Check the analytics destination's debug console or logs for received events
- [ ] **Property validation:** Verify event properties arrive with correct types and values
- [ ] **Environment isolation:** Confirm development/staging events go to a separate source or project, not production
- [ ] **Error handling:** Verify failed deliveries don't crash the application or block user actions

## Behavioral Rules

1. **Real code, not pseudocode.** Generate code that compiles and runs. Use correct SDK APIs, correct types, correct imports.

2. **Follow the instrumentation guide.** `.telemetry/instrument.md` is the primary source for SDK patterns. Only read `references/[sdk].md` if instrument.md is unclear or incomplete on a specific SDK behavior. Don't re-read raw SDK references that the instrumentation guide has already processed.

3. **Read all inputs fully.** Read the full tracking-plan.yaml, delta.md, and current-state.yaml before generating code. Do not truncate or skim. The implementation depends on complete knowledge of the plan.

4. **Centralized event name constants — non-negotiable.** Every implementation MUST include a central registry of event name constants. No raw event name strings anywhere in the codebase. All track calls reference the central constant, never a string literal. This is the single most effective defense against typos and drift.

   - **TypeScript:** `export const EVENTS = { USER_SIGNED_UP: 'user.signed_up', ... } as const;`
   - **Ruby:** `module Telemetry::Events; USER_SIGNED_UP = 'user.signed_up'; end`
   - **Python:** `class Events: USER_SIGNED_UP = 'user.signed_up'`
   - **Go:** `const EventUserSignedUp = "user.signed_up"`

5. **One function per event — unless the event name is computed.** Clear, explicit API. No generic `track(eventName, props)` wrapper that loses type safety. Exception: when event names depend on runtime state (e.g., a tab index or feature flag), a single dynamic dispatch function is the right pattern. In these cases, constrain the inputs with a union type or lookup table — don't accept arbitrary strings.

6. **Single delivery job.** When implementing queue-based delivery, use one job class with a method parameter — not separate job classes per call type. `DeliveryJob.perform(method: 'track', payload: {...})` not `TrackJob`, `IdentifyJob`, `GroupJob`.

7. **Delta first, full plan second.** If there's a delta, organize implementation around what needs to change. Don't regenerate everything if only 3 events need updating.

8. **Include the hard parts.** Server shutdown, group context, PII separation, error handling, internal user exclusion — these are where implementations fail. Don't skip them. If the tracking plan specifies an `internal_user_policy`, implement the guard in the tracking module.

9. **Update the plan.** After implementation, the tracking plan should reflect reality. If the plan was implemented faithfully, bump the version and note it.

10. **Write to files, summarize in conversation.** Write generated code to files. Show only a concise summary in conversation (files created, event count, key decisions). Never paste more than 20 lines of code into the chat.

11. **Present decisions, not deliberation.** Reason silently. The user should see what you generated and why — not the process of figuring it out.

## Lifecycle

```
model → audit → design → guide → implement ← feature updates
                                     ^
```

## Next Phase

After implementation, suggest the user run:
- **product-tracking-audit-current-tracking** — optionally re-audit to verify implementation matches the plan (e.g., *"audit tracking"*, *"verify tracking"*)
- **product-tracking-instrument-new-feature** — when the next feature ships, keep tracking coherent (e.g., *"instrument feature"*, *"new feature tracking"*, *"tracking for new feature"*)
