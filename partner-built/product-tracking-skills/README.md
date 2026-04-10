# Product Tracking Skills

**Your analytics tool isn't the problem. Your product tracking is.**

Most SaaS products have inconsistent events, missing context, and no real tracking plan. You're paying for Amplitude, Mixpanel, or PostHog — they work fine. You still can't answer basic questions because the instrumentation feeding them is broken.

Product Tracking Skills scans your codebase, audits what's tracked, and generates the instrumentation needed to make your analytics tools actually work — for 25+ platforms, in any AI agent tool.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/accoil/product-tracking-skills)](https://github.com/accoil/product-tracking-skills)

**Works in:** Claude Code &middot; Codex &middot; VS Code &middot; any tool with AI agent support

---

## See It In Action

Open your codebase in any AI agent tool and start talking:

```
You: audit tracking
AI:  [Finds every tracking call, identifies gaps and issues]
     Found 14 events across 8 files. Saved to .telemetry/current-state.yaml

You: design tracking plan
AI:  [Designs best-practice tracking plan, produces delta from current state]
     22 events. Delta: add 10, rename 3, change 4, remove 1. Review and adjust.

You: implement tracking
AI:  [Generates typed wrapper functions, delivery infrastructure, event constants]
     Tracking code ready in tracking/
```

Seven skills and a tracking watchdog agent. Your analytics tools finally work.

---

## The Problem

Most B2B products have one of these situations:

**No tracking.** You know you need it. It's been on the backlog for six months. It never happens.

**Broken tracking.** 14 events across 23 files. Some camelCase, some snake_case. No account context. Three events that do the same thing. Five that nobody uses.

**Decayed tracking.** Someone set it up 18 months ago. Twelve features have shipped since. None were instrumented. The tracking plan — if one exists — is a lie.

In all three cases, your CS team can't see which accounts are healthy. Your product team can't measure feature adoption. You can't give investors real usage numbers. The analytics tool you're paying for works fine — it just can't help when the tracking feeding it is missing, inconsistent, or broken.

---

## What These Skills Do

They fix the instrumentation layer feeding your analytics tools — so your product is properly tracked and any analytics tool downstream can answer real questions about how customers use your product.

The focus is **users, accounts, features, and lifecycle events**. The raw signals your product emits. Not vanity pageviews. Not generic clicks. Semantic events with meaning, properties, and account attribution.

### What They Don't Do

- Define KPIs or success metrics
- Build dashboards or reports
- Interpret what the data means
- Replace any analytics tool

The boundary is deliberate. This produces instrumentation. What happens downstream — scoring, dashboards, alerts — belongs to tools like [Amplitude](https://amplitude.com), [PostHog](https://posthog.com), [Mixpanel](https://mixpanel.com), or [Accoil](https://accoil.com).

---

## What's Inside

These aren't thin prompts. Each skill includes a built-in reference library:

- **19 common instrumentation mistakes** and how to detect them
- **Anti-pattern detection** — PII in event properties, noise events, redundant tracking, blocking calls
- **Naming conventions** — dot.notation for event names (`report.created`), snake_case for properties and traits (`signup_source`)
- **B2B entity modeling** — two-entity model, group hierarchies, instance vs user-level tracking
- **7 category templates** — opinionated starting points for B2B SaaS, AI/ML, dev tools, and more
- **Instrumentation references for 24 analytics destinations** — product analytics, CDPs, web analytics, error monitoring, feature flags, and session tools

The skills encode the kind of knowledge that usually lives in a senior analytics engineer's head — except it doesn't walk out the door when they leave.

---

## How It Works

Seven skills plus a background tracking watchdog. Each skill produces artifacts that feed the next. Everything version-controlled in your repo.

```
Business Case ──▶ Model ──▶ Audit ──▶ Design ──▶ Instrument ──▶ Implement ──▶ Maintain
```

| Phase | What Happens | You Get |
|-------|-------------|---------|
| **Business Case** | Builds a stakeholder-ready case for why product telemetry matters — blind spots, business value, effort involved | `.telemetry/business-case.md` |
| **Model** | Scans your codebase to understand the product — entities, features, value flow | `.telemetry/product.md` |
| **Audit** | Reverse-engineers current tracking. Every event, property, identity call. No judgment. | `.telemetry/current-state.yaml` |
| **Design** | Designs an opinionated tracking plan + explicit delta from current state | `.telemetry/tracking-plan.yaml` + `delta.md` |
| **Instrument** | Translates the plan into SDK-specific guidance with template code | `.telemetry/instrument.md` |
| **Implement** | Generates real typed wrapper functions, identity management, delivery infrastructure | `tracking/` directory |
| **Maintain** | Updates tracking when features ship. Versioned with changelog. | Updated plan + `changelog.md` |

### Tracking Watchdog (Background Agent)

Once your tracking plan is in place, the **tracking-watchdog** agent runs in the background while you develop. It monitors code changes for new features and modified user flows, compares them against your tracking plan, and suggests new events or properties when it finds coverage gaps.

It stays quiet when there's nothing to report. When it does speak up, it tells you exactly what event to add, what properties to include, and which entity level to attribute to — then recommends using the `instrument-new-feature` skill to make the changes.

This is how tracking stays current as your product evolves, without anyone remembering to check.

---

## Who Is This For?

**Founders** who know they need product analytics but it's been on the backlog for six months. You can go from zero to a complete tracking plan with working code in a single session.

**Product engineers** who inherited tracking that's scattered, inconsistent, and undocumented. You get a structured system: audit what exists, design what should exist, generate typed code to close the gap.

**Platform engineers** wiring up multiple tools — analytics, error monitoring, feature flags, session replay — who want consistent identity and event naming across all of them instead of six different instrumentation patterns scattered across the codebase.

**CS and product teams** who need feature adoption data and account health signals. You can't run the skills yourself, but you can hand engineering a clear process: "Run these skills. Get us the data we need."

If you're a B2B SaaS team and you can't answer *"which features does account X actually use?"* — or your Sentry errors have no user context, or your LaunchDarkly targeting is based on guesswork — start here.

---

## Supported Destinations

Instrumentation references for 25+ destinations across 7 categories. Each reference documents real SDK call patterns, authentication, constraints, and common pitfalls.

### Product Analytics & CDPs
Full identify → group → track lifecycle. Primary destinations for product usage data.

| Platform | Browser | Node.js |
|----------|---------|---------|
| **Segment** | `@segment/analytics-next` | `@segment/analytics-node` |
| **Amplitude** | `@amplitude/analytics-browser` | `@amplitude/analytics-node` |
| **Mixpanel** | `mixpanel-browser` | `mixpanel` |
| **PostHog** | `posthog-js` | `posthog-node` |
| **RudderStack** | `@rudderstack/analytics-js` | `@rudderstack/rudder-sdk-node` |

### B2B Engagement Platforms
Account-level engagement scoring and lifecycle signals.

| Platform | Browser | Server |
|----------|---------|--------|
| **Accoil** | `tracker.js` (CDN) | Direct API |
| **Intercom** | `@intercom/messenger-js-sdk` | `intercom-client` |
| **Journy** | — | `@journyio/sdk` |

### Web Analytics
Page-level and event tracking.

| Platform | Integration |
|----------|-------------|
| **Google Analytics (GA4)** | `gtag.js` / GTM |
| **Plausible** | Script tag / Events API |
| **Fathom** | Script tag / Events API |
| **Simple Analytics** | Script tag / Events API |
| **Usermaven** | `usermaven-js` / HTTP API |
| **Beam** *(shutting down Sept 2026)*, **Microanalytics, Cabin, Cloudflare** | Script tag |

### Error & Performance Monitoring
User context for debugging. Identify calls attach user/account info to error reports.

| Platform | Browser | Server |
|----------|---------|--------|
| **Sentry** | `@sentry/browser` | `@sentry/node` |
| **New Relic** | Browser agent | Node agent |
| **Azure Application Insights** | `@microsoft/applicationinsights-web` | `applicationinsights` |

### Feature Flags & Experimentation
Targeting attributes and experiment exposure tracking.

| Platform | Browser | Server |
|----------|---------|--------|
| **LaunchDarkly** | `launchdarkly-js-client-sdk` | `@launchdarkly/node-server-sdk` |
| **Statsig** | `@statsig/js-client` | `@statsig/statsig-node-core` |

### Session & Behavior Tools
Session recording and in-app guidance with user identification.

| Platform | Integration |
|----------|-------------|
| **Hotjar** | Script tag / Identify API |
| **UserPilot** | `userpilot.js` / Identify API |

### Tag Management & Architecture

| Platform | Use Case |
|----------|----------|
| **Google Tag Manager** | Container-based deployment for multiple destinations |
| **Generic HTTP** | Any destination with an HTTP/REST API |

Different tools serve different roles. The skills know what each destination supports and generate the right instrumentation for each. One audit covers all destinations. One tracking plan defines the events.

Want to add a destination? See the [destination reference template](skills/product-tracking-generate-implementation-guide/references/destination-reference-template.md).

---

## Category Templates

The design phase picks the best starting template for your product type. All extend `b2b-saas-core`.

| Template | Best For |
|----------|----------|
| `b2b-saas-core` | Generic B2B SaaS baseline |
| `ai-ml-tools` | AI/ML products, generation, models |
| `developer-tools` | APIs, SDKs, CLI tools |
| `collaboration-tools` | Team workspaces, real-time collab |
| `form-builders` | Form creation, submissions |
| `security-products` | Security events, alerts, compliance |
| `analytics-platforms` | Analytics products tracking their own usage |

---

## Design Principles

**Opinionated defaults.** dot.notation for event names (`user.signed_up`). snake_case for properties and traits (`signup_source`). Properties over events. Minimalist coverage. We take positions so you don't have to debate them.

**Audit before design.** Capture reality first, then decide intent. The audit describes what exists. Design is where opinions live.

**Delta-driven.** The diff between current state and tracking plan is the implementation backlog. "Add 10, rename 3, change 4, remove 1." No ambiguity.

**B2B-first.** Users and accounts are first-class. Group hierarchy (account → workspace → project) is built in. Every event attributed to the correct level.

**Maintainable.** Tracking decays when features ship without instrumentation. The maintain phase prevents that. Versioning, deprecation, and changelogs are built in.

---

## What You Get

Everything lives in `.telemetry/` in your repo. Version-controlled. Survives across sessions and engineers. Nothing in someone's head. Nothing in a third-party tool.

```
.telemetry/
├── business-case.md        # Why add telemetry — stakeholder-ready
├── product.md              # What your product does, entities, value flow
├── current-state.yaml      # What's tracked today (from audit)
├── tracking-plan.yaml      # What should be tracked
├── delta.md                # Current → target diff (the backlog)
├── instrument.md           # SDK-specific instrumentation guide
├── changelog.md            # How the plan evolved over time
└── audits/
    └── 2026-02-13.md       # Timestamped audit snapshots
```

---

## Skills Reference

Each skill is self-contained with its own `references/` directory. Trigger them with natural language.

| Skill | Try saying... |
|-------|---------------|
| `product-tracking-business-case` | *"write a business case for analytics"* or *"why add tracking?"* |
| `product-tracking-model-product` | *"model this product"* or *"understand this codebase"* |
| `product-tracking-audit-current-tracking` | *"audit tracking"* or *"what's currently tracked?"* |
| `product-tracking-design-tracking-plan` | *"design tracking plan"* or *"what should we track?"* |
| `product-tracking-generate-implementation-guide` | *"create instrumentation guide"* |
| `product-tracking-implement-tracking` | *"implement tracking"* or *"generate code"* |
| `product-tracking-instrument-new-feature` | *"instrument this feature"* |
| `tracking-watchdog` (agent) | *Runs automatically in background during feature development* |

---

## Installation

### Option 1: CLI Install (Recommended)

Use `npx skills` to install skills directly:

```bash
# Install all skills
npx skills add accoil/product-tracking-skills

# Install specific skills
npx skills add accoil/product-tracking-skills --skill audit design

# List available skills
npx skills add accoil/product-tracking-skills --list
```

This automatically installs to your `.claude/skills/` directory.

### Option 2: Claude Code Plugin

Install via Claude Code's built-in plugin system:

```bash
# Add the marketplace
/plugin marketplace add accoil/product-tracking-skills

# Install all skills
/plugin install product-tracking-skills
```

### Option 3: Clone and Copy

Clone the repo and copy the skills folder:

```bash
git clone https://github.com/accoil/product-tracking-skills.git
cp -r product-tracking-skills/skills/* .claude/skills/
```

Once installed, open your codebase in any AI agent tool and start with a prompt like this:

### Example Prompt

```
Use the product-tracking skills to model this product, audit the current tracking,
and design a complete tracking plan. Our tracking destination is Segment — use the
Segment library. Track at the account and user level. Give me a complete, product 
analytics tracking plan.
```

This runs the full skill chain — model, audit, design — and produces a tracking plan in `.telemetry/` ready for implementation.

---

## Feedback

Found a bug? Have a suggestion? [Open an issue](https://github.com/accoil/product-tracking-skills/issues).

---

## License

MIT — free for any use. Built by [Accoil](https://accoil.com).
