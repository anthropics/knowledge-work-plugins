---
name: industry
description: Cross-company industry comparison across multiple tickers
argument-hint: TICKER1 TICKER2 ...
---

Perform an industry comparison across the companies specified by the user: $ARGUMENTS

The user will provide multiple tickers separated by spaces (e.g., "AAPL MSFT GOOG AMZN").

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

Follow these steps:

## 1. Company Lookups
Look up all provided tickers using `discover_companies`. For each company, capture:
- `company_id`
- `latest_calendar_quarter` — use the earliest `latest_calendar_quarter` across all companies as the anchor for period calculations (see `../data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Note each company's fiscal year end — this is critical for calendar quarter alignment
- Firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5

## 2. Comparable Financial Metrics
Calculate 8 quarters backward from the anchor `latest_calendar_quarter`. For each company, find and pull these metrics:

**Income Statement:**
- Revenue
- Gross Profit / Gross Margin
- Operating Income / Operating Margin
- EBITDA (if not reported, compute as Operating Income + D&A — label "(calc.)")
- Net Income / Net Margin
- Diluted EPS
- R&D Expense
- Stock-Based Compensation (SBC)

**Cash Flow:**
- Operating Cash Flow
- CapEx (Purchases of property, plant and equipment)
- Free Cash Flow (compute as OCF - CapEx — label "(calc.)")
- D&A (needed for EBITDA calc if not directly reported)

For any derived/computed metric, mark it with "(calc.)" so the reader knows it's not directly sourced.

## 3. Company-Specific KPIs
First, think about what KPIs matter for the specific industry being compared. Use the full sector taxonomy to guide discovery:

- **SaaS/Cloud**: ARR, net revenue retention, RPO/cRPO, customers >$100K, cloud gross margin
- **Consumer Tech**: DAU/MAU, ARPU, engagement metrics, installed base, paid subscribers
- **E-commerce/Marketplace**: GMV, take rate, active buyers/sellers, order frequency
- **Retail**: same-store sales, store count, average ticket, transactions
- **Telecom/Media**: subscribers, churn, ARPU, content spend
- **Hardware**: units shipped, ASP, attach rate, installed base
- **Financial Services**: AUM, NIM, loan growth, credit quality metrics, fee income ratio
- **Pharma/Biotech**: pipeline stage, patient starts, scripts, market share
- **Industrials/Energy**: backlog, book-to-bill, utilization, production volumes, reserves

For each company, discover and pull the most relevant KPIs. Note which KPIs are common across the group (apples-to-apples comparison) and which are unique to specific companies. For mixed-sector comparisons, focus on the KPIs that apply to the largest revenue segments of each company.

## 4. Normalize & Compare
- **Calendar quarter alignment is critical.** Ensure all companies are compared on the same calendar quarters. Note each company's fiscal year end and map fiscal quarters to calendar quarters.
- Build side-by-side comparison tables
- Calculate margins for ALL 4 recent quarters (not just the latest) to show trends
- Calculate YoY growth rates for each of the last 4 quarters

## 5. Ranking & Analysis
- Rank companies on each key metric (revenue growth, margins, FCF yield, etc.)
- Identify the leader and laggard for each metric
- Flag notable outliers (unusually high/low margins, accelerating/decelerating growth)
- Note any divergence in KPIs or business model differences
- Compute R&D as % of revenue and SBC as % of revenue for each company — these reveal structural differences in how each company invests and compensates
- Show YoY segment growth rates for the most recent quarter, not just absolute segment revenue
- Flag one-time items that distort any quarter's comparison

## 6. Document Search
For each company, search the most recent 2 quarters of filings across multiple queries. If any search returns empty, try alternative keywords before giving up.

- **Competitive positioning**: Try "competition", "market share"; fallback to "competitive", "leader", "position"
- **Industry trends**: Try "industry", "market", "demand"; fallback to "secular", "trend", "adoption"
- **Strategic differentiation**: Try "differentiate", "advantage", "moat"; fallback to "unique", "proprietary", "platform"
- **Growth strategy**: Try "growth", "opportunity", "expansion"; fallback to "invest", "launch", "new market"
- **Macro / headwinds**: Try "macro", "headwind"; fallback to "tariff", "regulatory", "geopolitical", "inflation"

If a company returns sparse results across all searches, try broader single-keyword searches (e.g., just "competitive" or just "growth") and search additional periods.

For each company, extract:
- How management describes their competitive position
- Key strategic priorities and investments
- Industry or macro commentary that affects the whole group
- Any direct references to competitors in the comparison set

Use these findings to enrich the rankings analysis — numbers tell you who's winning, filings tell you why.

## 7. Save Report
Save to `reports/{INDUSTRY_LABEL}_industry_comp.html` (where INDUSTRY_LABEL is derived from the tickers, e.g., "AAPL_MSFT_GOOG_AMZN") using the HTML report template from `../design-system.md`. Write the full analysis as styled HTML with the design system CSS inlined. This is the final deliverable — no intermediate markdown step needed.

The report should include:
- Summary header listing all companies compared, with fiscal year end dates
- Side-by-side financial metrics table (last 4 calendar quarters, companies as columns, metrics as rows, Daloopa citations)
- Trailing 4-quarter totals for revenue, operating income, net income, EPS, OCF, CapEx, FCF
- **Margin trend table**: Gross margin, operating margin, net margin for ALL 4 quarters per company (not just latest quarter snapshot)
- **Growth comparison table**: Revenue YoY and EPS YoY for each of the last 4 quarters per company
- **R&D and SBC comparison**: R&D % of revenue and SBC % of revenue for each company (latest quarter + trend)
- Segment revenue tables per company with YoY growth rates for each segment in the most recent quarter
- KPI comparison (where applicable), noting common vs company-specific KPIs
- **Cash flow comparison**: OCF, CapEx, FCF side-by-side with CapEx as % of revenue to highlight investment intensity differences
- Rankings summary table
- Key competitive insights from filings (with document citations)
- Note on calendar quarter alignment and any fiscal year differences

All financial figures must use Daloopa citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved.

Give a clear competitive verdict: Who is winning and who is losing? Which company has the strongest competitive position and why? Which company looks most vulnerable? Are any of the companies structurally mispriced relative to peers (too cheap or too expensive given the fundamentals)? Don't hedge — rank them honestly.
