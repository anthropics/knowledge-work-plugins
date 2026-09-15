---
name: content-strategy
description: >
  Analyzes sales data from PayPal and QuickBooks to find top performers and
  slow movers, layers in seasonality, and produces a prioritized 30-day
  content brief: what to push, what offers to run, what to hold. Strategic
  output only — no calendars or assets. Use when the user asks what to post,
  wants a content plan, asks what's selling, or what to promote this month.
allowed-tools: Read, WebFetch
---

# Content Strategy

## Quick start

When an SMB owner asks "what should I post this month?" or "what's my content plan?", this skill:

1. **Pulls sales data** from QuickBooks or PayPal (transaction history, product/service revenue by date)
2. **Identifies patterns** — top-selling products, slow movers, seasonal trends
3. **Layers in context** — seasonality (user-provided or industry benchmarks), past performance
4. **Produces a 30-day brief** — ranked recommendations of what to push, what to hold, what offers to consider
5. **Gets owner approval** before the brief feeds into `social-content-engine` for asset generation

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

- **QuickBooks:** Fetch invoice line items via `profit_loss_quickbooks_account` (pre-flight sets industry context). Read the rows or `monthlyBreakdown`; the response's `totalExpenses` reports 0 against real rows, so never read the summary fields
- **PayPal:** Fetch merchant transactions via `list_transactions`. *Rate-limiting:* If you hit rate limits, pause 30 seconds and retry once. If still blocked, gracefully offer: "PayPal is rate-limited. Would you like to switch to QuickBooks or Square instead, or I can continue with historical data I already pulled?"
- **Square:** Requires location ID first. Call `make_api_request(service="locations", method="list")` to discover available locations, then fetch orders for each location.

**No connectors at all?** This still runs, and it is a supported path — not a degraded one. Ask the owner to export their sales history and upload it. Name the export by the label they will actually see in the app:

- **QuickBooks** — Reports, then the "Sales by Product/Service Detail" report, set to the last 90 days, exported to Excel or CSV
- **PayPal** — Activity, then Download, set to the last 90 days, "Completed transactions" as CSV
- **Square** — Reports, then Item Sales, set to the last 90 days, exported as CSV

Any one of those carries product name, date, revenue, and usually quantity, which is everything Step 3 needs. A pasted list of what sold and roughly when also works — say plainly that the read is rougher, and run it.

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
- "Ready to feed this to social-content-engine for asset generation?"

Iterate if needed; once approved, return the final brief as structured JSON (ready for downstream tools).

---

## More sources, and direct invocation

Read `reference/v2_sources.md` for the mapping:

- **Shopify** — per-SKU velocity, variant performance, and product images that flow straight into asset generation downstream
- **Stripe** — subscription and recurring revenue, where relevant

### Direct invocation

If the owner asks for a sales brief, run this and return the brief. Don't route them anywhere.

## Gotchas & edge cases

See [`reference/gotchas.md`](reference/gotchas.md) for common pitfalls.

---

## Examples

See [`reference/examples/`](reference/examples/) for worked examples (SaaS, retail, services).

---

## Output

**Deliver the 30-day brief per the owner's stored output preference — never default to a markdown file.** Check the `## Business context` block's `Output preference` (shared style guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the brief as an HTML page in the house style — what to promote as the lead, the why behind each pick with its numbers in tabular-nums, and the channel call per push. The structured JSON for downstream tools rides along unchanged; it is an input to other skills, not a second deliverable.
- **docx / md / notion / canva preference:** deliver the same content in that form — a DOCX or markdown file, a Notion page created via the connector (named destination, never overwriting), or a Canva Doc created via the Canva connector (a new design each run, named with the date; tables become lists); fall back to the visual artifact if Notion or Canva is not connected — and say that is why.
- **Best for skill:** use the visual artifact — this output is a decision page, not prose.

## After the brief

The 30-day brief is approved and ready to act on. The natural next step is "make the content" — `social-content-engine` turns the brief into the standing calendar and the posts. Also nearby: "run this brief" (`canva-creator`) for a one-shot campaign build from this exact brief, and "is my marketing working" (`growth-pulse`) to check whether last month's push paid off. Offer at most three, and skip any offer the owner already declined this session.

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.
