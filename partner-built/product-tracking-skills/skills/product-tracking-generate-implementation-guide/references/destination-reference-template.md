# Destination Reference Template

Guide for creating implementation reference files for new analytics destinations. Follow this when adding support for a new analytics tool.

## Where Reference Files Go

Each destination needs a reference file in:

```
product-tracking-generate-implementation-guide/references/{provider}.md
```

Optionally, a shorter version in `product-tracking-audit-current-tracking/references/{provider}.md` for SDK detection patterns (create when the tool is commonly encountered in audits).

**File naming:** lowercase, hyphenated. Examples: `segment.md`, `posthog.md`, `google-analytics.md`, `simple-analytics.md`.

## Step 1: Classify the Tool

Determine the tool's category. This determines which sections of the reference are required.

| Category | Examples | identify | group | track | page | B2B Fit |
|---|---|---|---|---|---|---|
| **Product Analytics** | Amplitude, Mixpanel, PostHog | Required | Required | Required | Required | Full |
| **Customer Data Platform** | Segment, RudderStack | Required | Required | Required | Required | Full |
| **B2B Engagement** | Accoil, Journy | Required | Required | Required | Optional | Full |
| **Web Analytics** | Plausible, Fathom, Simple Analytics, Beam, Microanalytics, WithCabin | N/A | N/A | Limited | Core | Minimal |
| **Full-Stack Analytics** | Google Analytics, Usermaven | Optional | Optional | Required | Required | Partial |
| **Error / Performance** | Sentry, New Relic, Azure AppInsights | Context only | N/A | Errors/perf | N/A | None |
| **Feature Flags / Experimentation** | LaunchDarkly, Statsig | Context | Context | Flag evals | N/A | Partial |
| **Session / Behavior** | HotJar, UserPilot | Tag only | N/A | Events | Auto | Minimal |
| **Tag Management** | Google Tag Manager | N/A | N/A | Routing layer | N/A | None |

**B2B Fit** indicates how well the tool maps to the standard identify → group → track model:
- **Full** — native users, accounts, and custom events with properties
- **Partial** — user identity supported, limited or no account-level grouping
- **Minimal** — session tagging only, no persistent identity model
- **None** — not designed for user/account analytics

## Step 2: Research Checklist

Answer these before writing. Not all apply to every category.

### Provider Basics
- [ ] Official name (exact casing)
- [ ] One-line description of what it does
- [ ] Open-source or proprietary?
- [ ] Cloud-only, self-hosted, or both?
- [ ] Pricing model — is group/account analytics a paid add-on?
- [ ] Forge-approved domains (from `forge-platform.md`)

### Authentication
- [ ] API key / token / write key — what is it called?
- [ ] How is it passed? (Authorization header, query param, JSON body field)
- [ ] Write key vs read key distinction?
- [ ] Where to find it in the provider's dashboard

### SDK Availability
- [ ] **Browser** — npm package name, CDN snippet availability
- [ ] **Node.js** — npm package name
- [ ] **HTTP API** — base URL, auth method, content type
- [ ] **Other** — Python, Ruby, Go, mobile (note availability, don't document in detail)

### Method Mapping

For each supported method, research:

**identify() equivalent:**
- [ ] Method name and call signature (browser and server)
- [ ] How is user ID set?
- [ ] How are user traits/properties set? (inline vs separate call)
- [ ] `set` vs `setOnce` vs `increment` operations available?
- [ ] Persistence — does it remember across page loads?

**group() equivalent:**
- [ ] Does the tool have a native group/account concept?
- [ ] Method name and call signature
- [ ] Is it a paid add-on?
- [ ] Max group types supported
- [ ] Hierarchical groups / parent-child support?
- [ ] How are subsequent track calls attributed to groups? (automatic vs explicit)

**track() equivalent:**
- [ ] Method name and call signature
- [ ] Does it accept event properties?
- [ ] Event name constraints (length, case, characters)
- [ ] Auto-tracked events (sessions, page views, clicks)

**page() equivalent:**
- [ ] Method name and call signature
- [ ] Auto-tracking available?
- [ ] What's auto-collected? (url, title, referrer, path)

### Infrastructure
- [ ] Batching — does the SDK batch? Config options (size, interval)
- [ ] Flush/shutdown — how to ensure events send on exit
- [ ] Rate limits (requests/sec, events/sec)
- [ ] Max payload size (single event, batch)
- [ ] Data residency (US, EU regions)

### Debugging
- [ ] Debug mode / verbose logging — how to enable
- [ ] Dashboard debugger / live events view
- [ ] HTTP response codes and error meanings

## Step 3: Write the Reference File

Use the skeleton below. **Include only sections relevant to the tool's category.** A privacy-focused web analytics tool (Plausible) will be much shorter than a full product analytics platform (Amplitude).

---

```markdown
# {Provider Name} Implementation Reference

## Overview

{1-2 sentences: what the tool is, its primary use case. Note if open-source, self-hosted, etc.}

## SDK Options

| Environment | Integration | Install |
|---|---|---|
| Browser | {package or CDN} | `npm install {package}` |
| Node.js | {package} | `npm install {package}` |
| HTTP API | Direct | No SDK — raw `fetch()` calls |

## Initialization

### Browser
{Setup code with standard config options.}

### Node.js
{Setup code with standard config options.}

## Core Methods

{Map the tool's API to identify/group/track. If a method has no equivalent, state it clearly. Show browser, Node.js, and HTTP API variants.}

### identify()

{How user identification works in this tool.}

**Browser:**
{code}

**Node.js:**
{code}

**HTTP API:**
{code}

**When to call:** {trigger points}

### group()

{How account/group context works. Note if paid add-on. State clearly if not supported.}

**Browser:**
{code}

**Node.js:**
{code}

**HTTP API:**
{code}

### track()

{How event tracking works. Note any constraints (e.g., no properties, name format rules).}

**Browser:**
{code}

**Node.js:**
{code}

**HTTP API:**
{code}

### page()

{Only if the tool has explicit page tracking. Note auto-tracking if available.}

## Group Context on Track Calls

{Required for tools with B2B Fit of "Full" or "Partial". Explain how to:}
{1. Define multiple group levels}
{2. Attribute individual events to specific group levels}
{3. Hierarchy limitations and workarounds}

## Required Fields

| Method | Required Fields | Notes |
|---|---|---|
| {method} | {fields} | {notes} |

## Limits

| Constraint | Value |
|---|---|
| Rate limit | {value} |
| Max event size | {value} |
| Max batch size | {value} |

## Common Pitfalls

1. **{Mistake}** — {what goes wrong and how to fix it}
2. ...

## Debugging

{Debug mode, dashboard debugger, HTTP error codes.}

## Further Documentation

This reference covers the essentials for product tracking implementation. For advanced topics, consult {Provider}'s official documentation:

- **Getting Started:** {url}
- **{SDK} SDK:** {url}
- **{Key feature}:** {url}
```

---

## Category-Specific Guidance

### Product Analytics (Amplitude, Mixpanel, PostHog, Usermaven)

Full reference required. All sections apply. Pay special attention to:
- Group analytics — is it a paid feature? How many group types?
- How events are attributed to groups (automatic vs explicit)
- Hierarchy support (parent-child rollups)
- Session management
- Auto-capture / auto-track features

### Customer Data Platforms (Segment, RudderStack)

Full reference required. Additionally document:
- How events route to downstream destinations
- Destination filtering (sending specific events to specific tools)
- Batch endpoint for bundling multiple call types
- The fact that `group()` context does NOT auto-attach to `track()` calls

### B2B Engagement Platforms (Accoil, Journy)

Full reference required. Emphasize:
- Group calls are essential — the tool is account-centric
- Any property limitations (Accoil: event names only, no properties)
- Account trait recommendations (MRR, plan, created_at)
- Hierarchical group support and rollup behavior

### Web Analytics (Plausible, Fathom, Simple Analytics, Beam, etc.)

Shorter reference. Focus on:
- **Page view tracking** — this is the core capability
- **Custom events** — if supported, syntax and limitations
- **Privacy model** — cookieless? GDPR-compliant by default?
- **What it does NOT do** — no identify, no group, no event properties (or very limited)
- **When to use it** — complements product analytics, not a replacement

Example note for the reference:

> **B2B Limitation:** {Tool} is a privacy-focused web analytics tool. It does not support user identification, account grouping, or rich event properties. It is useful for aggregate traffic metrics but cannot replace a product analytics tool for B2B user/account tracking. Use it alongside (not instead of) tools like Amplitude, Mixpanel, or PostHog.

### Error / Performance Monitoring (Sentry, New Relic, Azure AppInsights)

These are NOT product analytics tools but appear on the Forge approved list. Keep the reference short and focused on:
- **Setting user context** — so errors/performance data map to known users
- **Custom breadcrumbs or tags** — for product context in error reports
- **What it is NOT** — not a replacement for product analytics
- **Integration pattern** — typically runs alongside a product analytics SDK

### Feature Flags / Experimentation (LaunchDarkly, Statsig)

Focus on:
- **User/group context for flag evaluation** — how to pass identity and account context so flags target correctly
- **Tracking flag evaluations as events** — how to pipe flag exposure data to product analytics
- **Integration pattern** — typically paired with a product analytics tool for experiment analysis

### Session / Behavior Tools (HotJar, UserPilot)

Focus on:
- **User identification** — how to tag sessions with known user IDs
- **Custom events** — triggering recordings, surveys, or guides based on product events
- **Privacy** — session recording has significant privacy implications; document opt-out and masking
- **Integration pattern** — supplements product analytics with qualitative data

### Tag Management (Google Tag Manager)

GTM is a routing layer, not an analytics destination. The reference should explain:
- How GTM loads and configures other analytics tools
- DataLayer events — how product events are pushed and routed
- Why GTM adds complexity vs direct SDK integration
- When GTM makes sense (marketing teams need tag control) vs when it doesn't (engineering-led instrumentation)

## Step 4: Update Plugin Metadata

After creating the reference file:

1. **SKILL.md Reference Index** — If the reference is needed by the `generate-implementation-guide` skill, add it to the Reference Index table (it will be auto-included by filename convention, but the index helps humans)
2. **forge-platform.md** — Verify the provider's approved domains are listed (if applicable)

## Quality Checklist

Before submitting a new destination reference:

- [ ] All code examples use the standard B2B example identifiers: `usr_123`, `acc_456`, `ws_789`, `proj_123`, `rpt_789`
- [ ] Code examples show real, working API calls — not pseudocode
- [ ] Properties use `snake_case` per plugin naming conventions
- [ ] The "Further Documentation" section links to current, working URLs
- [ ] Common Pitfalls include at least 3 tool-specific gotchas
- [ ] Group context section explains how events are attributed to specific group levels (for tools with B2B Fit of Full/Partial)
- [ ] The overview clearly states what category the tool falls into
- [ ] No marketing language — describe capabilities factually
