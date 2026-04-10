# Effort Guide

Use this to give realistic effort estimates in the business case. The goal is fixing the data that flows into analytics tools — not building a new system. AI-assisted tooling handles the heavy lifting — the human effort is reviewing, adjusting, and integrating.

## The Three Steps

| Step | AI Does | Human Does | Typical Effort |
|------|---------|-----------|---------------|
| **Audit** | Scans codebase, inventories all current tracking calls, identifies gaps and issues | Reviews the audit output | Minutes for AI scan, 30 min to review |
| **Design** | Generates a best-practice tracking plan based on the product's domain, entities, and features | Reviews the plan, adjusts event names, adds/removes events, confirms naming conventions | 1-2 hours of review and discussion |
| **Implement** | Generates typed event definitions, SDK wrappers, delivery infrastructure following codebase conventions | Reviews generated code, integrates into codebase, tests delivery | 1-3 days to integrate and test |

**The hardest part — deciding what to track — is ~80% handled by AI.** The design skill applies proven patterns (event categories, naming conventions, property standards, group hierarchy) to the product's specific domain. The team's job is to review and tweak, not start from a blank page.

**Total realistic effort: a few days of focused work, not weeks.**

## What Affects Effort

More complexity = more review time, but AI still does the heavy lifting:

| Factor | Impact on Human Effort |
|--------|----------------------|
| Existing tracking to preserve/migrate | More review — need to reconcile old and new |
| Multiple analytics destinations | More design decisions — but AI flags constraints |
| Deep group hierarchy (account > workspace > project) | More review of attribution rules |
| Multiple codebases (frontend + backend + mobile) | More integration points to test |
| Greenfield (no existing tracking) | Less effort — nothing to reconcile, clean start |

## Ongoing Maintenance

After initial implementation:
- **Per new feature:** Minutes — add a tracking call alongside the feature code. AI can generate the event definition and hook placement.
- **Periodic review:** Occasional check that the tracking plan matches product reality. AI can re-audit and flag drift.

## What's NOT Included

The business case covers product telemetry instrumentation — fixing the data that flows into analytics tools so they can do their job. It does NOT include:
- Building dashboards or reports (that's the analytics tool's job — and it can finally do it once the data is right)
- Data warehouse or ETL pipelines
- Custom analytics infrastructure
- Marketing attribution or ad tracking
