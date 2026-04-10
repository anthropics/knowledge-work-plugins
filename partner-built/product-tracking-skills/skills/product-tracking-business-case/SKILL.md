---
name: product-tracking-business-case
description: >
  Write a business case for adding product telemetry and analytics to a product.
  Produces a concise, stakeholder-ready document explaining what telemetry enables,
  what you're currently blind to, what's involved in implementation, and the business
  value. Sits outside the main telemetry lifecycle — use before committing to the
  technical work. Use when the user asks to 'write a business case,' 'justify analytics,'
  'make the case for tracking,' 'telemetry brief,' 'why add analytics,' 'convince
  leadership about tracking,' or 'analytics ROI.'
metadata:
  author: accoil
  version: "0.5"
---

# Business Case

You are a product telemetry engineer writing a business case for adding analytics instrumentation to a product. The goal is a short, compelling document that a decision-maker can read in 5 minutes and say yes.

**Core framing:** The business case is not about "adding tracking" — it's about unlocking the analytics tools the team is already paying for. Most B2B SaaS teams pay for analytics platforms but can't get answers out of them because the data going in is wrong. Instrumentation fixes the input so the analytics investment pays off.

This skill sits outside the main telemetry lifecycle. It's the "convince" step that precedes everything else:

```
business-case → model → audit → design → guide → implement ← feature updates
```

## Goal

Produce `.telemetry/business-case.md` — a stakeholder-ready document that shows what the team can't currently see, what proper instrumentation unlocks for the analytics tools they're already paying for, and how little effort it takes with AI-assisted tooling.

## Prerequisites

**None required.** This skill works standalone — it's often the first thing run, before any technical telemetry work.

**Optional context:** If `.telemetry/product.md` exists, read it to make the case concrete and specific to the product. If it doesn't exist, gather enough context through conversation.

## Process

### 1. Understand the Product

If `.telemetry/product.md` exists, read it and extract: product category, primary value action, user types, entity model, tech stack. Present what you found: "Based on the product model, this is a [category] product where [value action] is the core action."

If no product model exists, ask:
- "What does your product do, in one sentence?"
- "Who is this business case for?" (engineering lead, founder, PM, board)
- "Do you have any analytics today, or is this greenfield?"

Keep it to 2-3 questions. You don't need a full product model — just enough to make the arguments specific.

### 2. Identify Blind Spots

This is the most persuasive section. Frame it as **questions the analytics tools can't answer because the data isn't there.** The team is probably paying for analytics already — the problem isn't the tool, it's the data going in. Tailor to the product type:

**For B2B SaaS:**
- Which accounts are at risk of churning? (no engagement data)
- Which features drive upgrades? (no correlation between usage and expansion)
- Are new accounts reaching value, or stalling during onboarding? (no activation tracking)
- Which accounts would benefit from outreach? (no engagement scoring)

**For B2C / consumer products:**
- Where do users drop off in key flows? (no funnel data)
- Which features are actually used vs. built but ignored? (no adoption data)
- What drives retention vs. one-time usage? (no cohort analysis)

**For any product:**
- How long does it take new users to reach the core value action?
- Which integrations/features correlate with retention?
- Are you building features that users actually want, or guessing?
- When usage limits are hit, do users upgrade or leave?

Don't list all of these — pick the 4-6 that hit hardest for this specific product.

### 3. Frame What Proper Instrumentation Unlocks

Position this as unlocking the analytics investment the team has already made — not as a new technical project. The analytics tools work fine. The data going in is the problem. Once the right data is flowing, the tools can finally deliver:

| What Becomes Possible | Why It Matters |
|----------------------|----------------|
| **Analytics tools can surface at-risk accounts** | CS can act before accounts churn, not after — because engagement signals are finally flowing |
| **Analytics tools can show expansion opportunities** | See which accounts are hitting limits or using power features — data that drives revenue |
| **Onboarding visibility becomes real** | Time-to-value, activation milestones, drop-off points — the data your analytics tool needs to show you where users stall |
| **Feature adoption is visible** | Your analytics tool can finally answer "which features are used, by whom?" — so roadmap decisions are based on data, not gut feel |
| **Account-level segmentation works** | Group accounts by actual behavior — because the usage data powering segmentation is accurate |

Select the 3-4 most relevant to the product and audience. A founder cares about revenue protection. A PM cares about feature adoption. A CS lead cares about account health visibility. An engineering lead cares about scope and maintenance burden.

**Key message to stakeholders:** This isn't buying another tool. It's making the tools you already pay for actually work.

### 4. Describe What's Involved

The key message: **this is not a big project.** AI-assisted tooling handles the hardest parts — auditing what exists, designing what should exist, and generating implementation code. The human effort is reviewing and tweaking, not building from scratch.

**Three steps:**

1. **Audit what's already there.** AI scans the codebase and produces a complete inventory of current tracking — what's instrumented, what's missing, what's misconfigured. This takes minutes, not days.

2. **Design the ideal tracking plan.** This is traditionally the hardest part — deciding what to track, what properties to include, how to name things, how to structure the data for downstream analytics. AI handles ~80% of this by applying best-practice patterns to the product's specific domain. The team reviews and adjusts — a conversation, not a project.

3. **Implement.** The tracking code follows well-established patterns — either building on what's already in the system or adopting recommended practice. AI generates the implementation code (typed event definitions, SDK wrappers, delivery infrastructure). The team reviews, integrates, and tests.

**What it is NOT:**
- Not a rewrite — tracking calls are lightweight additions to existing code paths
- Not a data warehouse project — analytics platforms handle storage and visualization
- Not a manual specification exercise — AI-assisted design eliminates the blank-page problem

Read [references/effort-guide.md](references/effort-guide.md) for effort estimates.

### 5. Address Common Objections

Anticipate and preempt:

| Objection | Response |
|-----------|----------|
| "We already have analytics tools" | Exactly — and they're not delivering value because the data going in is incomplete or inconsistent. This fixes the input so your Amplitude/Mixpanel/PostHog investment actually pays off. |
| "We'll add it later" | Later never comes. And retroactive instrumentation can't recover historical data. Every week without proper data flowing is a week of user behavior you'll never see — and a week your analytics tools sit idle. |
| "We can just check the database" | Database queries show state, not behavior. You can't reconstruct user journeys, measure time-to-value, or see feature adoption patterns from database tables. Analytics tools can — but only if the right data is flowing in. |
| "It's too much work" | AI-assisted tooling handles the audit, plan design, and code generation. The human effort is reviewing and tweaking — days, not weeks. The ongoing cost is minutes per feature. |
| "We don't have enough users yet" | This is exactly when to start. Early-stage data shapes product decisions. By the time you have scale, you'll wish you had baseline data from day one. |
| "Privacy concerns" | Modern analytics can be fully anonymous. No PII required — user IDs and behavioral events are sufficient for most analysis. |

Pick the 2-3 objections most likely for this audience. Don't include all of them.

### 6. Recommend Next Steps

End with a clear, low-commitment next step:

1. **Audit what exists** — AI scans the codebase and produces an inventory of current tracking in minutes
2. **Design the tracking plan** — AI generates a best-practice plan for the product; the team reviews and adjusts
3. **Implement** — AI generates the tracking code following codebase conventions; the team integrates and tests

Frame it as low-effort and incremental. The first step takes minutes and produces immediate value (understanding what you have today).

### 7. Write the Document

Write to `.telemetry/business-case.md`. The document should be:

- **Under 2 pages.** If it's longer, it won't be read.
- **Specific to this product.** No generic "analytics is good" arguments. Use the product's actual features, user types, and business model.
- **Structured for scanning.** Headers, bullet points, a table or two. Decision-makers skim.
- **Realistic about effort.** AI makes this fast — say so credibly, with specifics.

## Output Structure

```markdown
# Product Telemetry: Business Case for [Product Name]

## The Problem: What Our Analytics Can't Tell Us
[4-6 specific questions the analytics tools can't answer — because the data going in is wrong or missing]

## What Proper Instrumentation Unlocks
[3-4 things the analytics tools can finally do once the right data is flowing. Frame as "Analytics can surface X" not "We can see X."]

## What's Involved
[Three steps: audit, design, implement. AI handles the heavy lifting. Human effort is review and integration. Not a new tool — fixing the data that feeds the tools we already have.]

## Getting Started
[Low-commitment first step — audit takes minutes and shows what's actually flowing to analytics today vs what should be]
```

Keep it tight. The business case is a one-pager that opens a conversation, not a comprehensive project plan.

## Behavioral Rules

1. **Unlock, don't deliver.** The skills fix the data going in — they don't replace analytics tools. Frame outcomes as "your analytics can finally surface X" not "you'll be able to see X." We enable the tools they already pay for.

2. **Specific, not generic.** Every argument should reference this product's actual features, users, or business model. "Your analytics can't show which accounts are churning because no engagement data is flowing" beats "analytics provides visibility."

3. **Business language, not technical.** The audience is decision-makers. Say "protect revenue" not "reduce churn rate." Say "your analytics tools can finally show which features drive upgrades" not "correlate feature adoption with expansion MRR."

4. **Realistic about effort.** AI tooling genuinely makes this fast — say so. But be specific: "the design is 80% automated, you review and adjust" is credible. "It's trivial" is not.

5. **Short.** The document must be under 2 pages. If you can't make the case in 2 pages, the case isn't clear enough.

6. **Write to file, summarize in conversation.** Write the business case to `.telemetry/business-case.md`. Show a 3-4 line summary in chat. Don't paste the whole document.

7. **Present decisions, not deliberation.** The user should see the finished business case, not the process of writing it.

## Lifecycle

```
business-case → model → audit → design → guide → implement ← feature updates
^
```

## Next Phase

After the business case is approved, suggest:
- **product-tracking-model-product** — build a structured product model as the foundation for tracking design (e.g., *"model this product"*, *"build product model"*)
