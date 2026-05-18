---
name: content-strategy
description: >
  Analyzes sales data from PayPal and QuickBooks to find top performers and
  slow movers, layers in seasonality, and produces a prioritized 30-day
  content brief: what to push, what offers to run, what to hold. Strategic
  output only — no calendars or assets. Use when the user asks what to post,
  wants a content plan, asks what's selling, or what to promote this month.
---

# Content Strategy

> **Status:** MVP draft
> **Owner:** JJ
> **Version:** 0.2.0 · Phase MVP
> **Category:** Marketing & Sales

## Quick start

When an SMB owner asks "what should I post this month?" or "what's my content plan?", this skill:

1. **Pulls sales data** from QuickBooks or PayPal (transaction history, product/service revenue by date)
2. **Identifies patterns** — top-selling products, slow movers, seasonal trends
3. **Layers in context** — seasonality (user-provided or industry benchmarks), past performance
4. **Produces a 30-day brief** — ranked recommendations of what to push, what to hold, what offers to consider
5. **Gets owner approval** before the brief feeds into `canva-creator` for asset generation

The output is strategic only — no calendar scheduling, no creative assets.

---

## Workflow

### Step 1: Pre-flight check (QuickBooks only)

If using QuickBooks, verify the business profile is set up:

1. Call `company-info` to check if `Industry` is populated
2. If missing or "Unknown":
   - Ask: "I need your business category to pull the right seasonality benchmarks. What industry are you in?" (e.g., retail, services, SaaS)
   - Call `quickbooks-profile-info-update` with the user's industry
   - Confirm: "Profile updated. Ready to pull your sales data."
3. If profile is set, proceed to Step 2

**Note:** PayPal and Square do not require profile setup.

### Step 2: Clarify priorities & metrics

When triggered, ask the user:

- **"How do you want me to measure 'top performers'?"**
  - By total revenue?
  - By profit margin?
  - By sales velocity (how fast they're selling)?
  - Combination of the above?

- **"Do you have seasonality patterns in mind?"**
  - If yes: "Tell me about them" (capture user's known seasonality)
  - If no: "I'll use industry benchmarks for your category"

### Step 3: Pull and analyze sales data

Fetch data from the authenticated connector (QuickBooks, PayPal, or Square, user's choice):

- **Date range:** Last 90 days (or full history if <90 days available)
- **Extract:** Product/service name, date sold, revenue, quantity

**Connector-specific notes:**

- **QuickBooks:** Fetch invoice line items via `profit-loss-quickbooks-account` (pre-flight sets industry context)
- **PayPal:** Fetch merchant transactions via `list_transactions`. *Rate-limiting:* If you hit rate limits, pause 30 seconds and retry once. If still blocked, gracefully offer: "PayPal is rate-limited. Would you like to switch to QuickBooks or Square instead, or I can continue with historical data I already pulled?"
- **Square:** Requires location ID first. Call `make_api_request(service="locations", method="list")` to discover available locations, then fetch orders for each location. *Future enhancement:* Square integration is stubbed; full path documented in `reference/square-integration.md`.

**Fallback:** If <3 months of data, use industry seasonality benchmarks for the SMB's category (e.g., retail, services, e-commerce)

Identify:
- **Top 3–5 performers** (by user's chosen metric)
- **Bottom 3–5 slow movers** (consider holding or repositioning)
- **Trending up** (gaining momentum in last 30 days)
- **Trending down** (losing momentum)

### Step 4: Layer in seasonality

- **User-provided:** If they shared seasonal patterns, weight recommendations against them
- **Industry benchmarks:** For categories without strong user data (e.g., "Q1 is strong for tax services")
- **Timing:** Flag products that should ramp up/down in the next 30 days based on seasonal patterns

### Step 5: Build the 30-day brief

Structure:
- **Executive summary** (1–2 sentences: "Your best sellers are X and Y. Seasonal shift to Z is starting.")
- **Push hard** (Top 2–3 products + recommended content angle, e.g., "Case study on ROI", "How-to video")
- **Hold steady** (Middle performers; maintain visibility but no heavy lift)
- **Reposition or pause** (Slow movers; consider discounting, bundling, or pausing)
- **Seasonal opportunities** (What's coming next month that you should position for now)
- **Recommended offers** (Bundle, discount, or free-trial strategy based on data)

Example length: **200–400 words** (brief and actionable, not essay-length).

### Step 6: Owner approval & iteration

Present the brief to the owner. Ask:
- "Does this match your gut?"
- "Anything to adjust?"
- "Ready to feed this to canva-creator for asset generation?"

Iterate if needed; once approved, return the final brief as structured JSON (ready for downstream tools).

---

## Gotchas & edge cases

See [`reference/gotchas.md`](reference/gotchas.md) for common pitfalls.

---

## Examples

See [`reference/examples/`](reference/examples/) for worked examples (SaaS, retail, services).
