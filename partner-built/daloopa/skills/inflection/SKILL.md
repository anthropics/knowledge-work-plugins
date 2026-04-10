---
name: inflection
description: Auto-detect biggest acceleration/deceleration inflections across all metrics
argument-hint: TICKER
---

Detect the biggest financial and operating inflections for the company specified by the user: $ARGUMENTS

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

Follow these steps:

## 1. Company Lookup
Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations below (see `../data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5

## 2. Broad Series Discovery
Cast a wide net to discover ALL available series for this company. Search with multiple keyword sets to maximize coverage:
- Financial: "revenue", "income", "profit", "margin", "eps", "cash flow"
- Operating: "subscriber", "user", "customer", "unit", "arpu", "retention"
- Segment: "segment", "product", "service", "geographic"
- Balance sheet: "debt", "asset", "equity", "cash"
- Other: "backlog", "bookings", "pipeline", "store", "employee"

Collect all unique series IDs. The goal is comprehensiveness — capture every metric Daloopa tracks for this company.

## 3. Pull 8 Quarters of Data
Calculate 8 quarters backward from `latest_calendar_quarter`. Pull all discovered series for those periods. This gives enough history to compute both QoQ and YoY rates plus their second derivatives.

## 4. Compute Growth Rates and Inflections
For each series with sufficient data (at least 5 quarters):

**YoY Growth Rate** for each quarter:
- growth_t = (value_t - value_{t-4}) / |value_{t-4}|

**YoY Acceleration (second derivative):**
- accel_t = growth_t - growth_{t-1}
- Positive = accelerating, Negative = decelerating

**QoQ Sequential Growth** (for non-seasonal metrics):
- seq_growth_t = (value_t - value_{t-1}) / |value_{t-1}|

**QoQ Acceleration:**
- seq_accel_t = seq_growth_t - seq_growth_{t-1}

Skip series where values are too small (< 1% of revenue) or where data is sparse. For margin/ratio series (values between 0-1 or percentages), compute change in basis points rather than % change.

## 5. Rank Inflections
Rank all series by the magnitude of their most recent acceleration/deceleration:

**Top 10 Accelerating** — series with the largest positive acceleration in the most recent quarter. These are metrics that are improving faster than before.

**Top 10 Decelerating** — series with the largest negative acceleration (or deceleration). These are metrics where momentum is fading.

For each inflection, note:
- Series name
- Most recent value (with Daloopa citation)
- Current YoY growth rate
- Prior-quarter YoY growth rate
- Acceleration (the delta)
- Whether this is a new trend (1Q) or sustained (2-3Q in same direction)

## 6. Contextualize Key Inflections
For the top 5 most significant inflections (by magnitude and importance to the business):
- Search SEC filings for context on what's driving the change
- Try keywords related to the specific metric (e.g., if "Services Revenue" is accelerating, search for "services", "subscription", "recurring")
- Extract management commentary explaining the inflection
- Note whether the inflection aligns with or contradicts management guidance

## 7. Synthesize
Identify the narrative:
- Is the company broadly accelerating or decelerating?
- Are there divergent trends (e.g., revenue accelerating but margins decelerating)?
- Which inflections matter most for the investment case?
- Are operating KPIs leading or lagging the financial inflections?

**Critically assess sustainability:**
- For positive inflections: Is this a durable trend change or a one-time comp effect? Will it persist next quarter when the base normalizes? Is it driven by organic strength or by pull-forward, price increases, or easy comps?
- For negative inflections: Is this the beginning of a structural deterioration or a temporary blip? Is the company investing through it (good) or cutting to protect margins (potentially bad long-term)?
- Flag any inflections where the magnitude seems too good/bad to be sustainable.

## 8. Save Report
Save to `reports/{TICKER}_inflection.html` using the HTML report template from `../design-system.md`. Write the full analysis as styled HTML with the design system CSS inlined. This is the final deliverable — no intermediate markdown step needed.

Structure the report with these sections:

```
<h1>{Company Name} ({TICKER}) — Inflection Analysis</h1>
<p>Generated: {date}</p>

<h2>Summary</h2>
{2-3 sentence overview: Is the company accelerating, decelerating, or mixed? What are the most important inflections?}

<h2>Top Accelerating Metrics</h2>
<table>
| Rank | Metric | Latest Value | YoY Growth | Prior YoY Growth | Acceleration | Trend |
{table with Daloopa citations}
</table>

<h2>Top Decelerating Metrics</h2>
<table>
| Rank | Metric | Latest Value | YoY Growth | Prior YoY Growth | Deceleration | Trend |
{table with Daloopa citations}
</table>

<h2>Key Inflection Deep Dives</h2>

<h3>1. {Metric Name} — {Accelerating/Decelerating}</h3>
{Context from filings, management commentary, what's driving it}

<h3>2. {Metric Name} — {Accelerating/Decelerating}</h3>
{...}

{repeat for top 5}

<h2>Divergences & Signals</h2>
{Analysis of divergent trends, leading indicators, and implications}

<h2>Inflection Heatmap</h2>
<table>
| Metric | Q(-3) YoY | Q(-2) YoY | Q(-1) YoY | Q(latest) YoY | Direction |
{visual trend using labels: Accelerating / Steady / Decelerating}
</table>
```

All financial figures must use Daloopa citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved.

Highlight the 2-3 most notable inflections and what they signal.
