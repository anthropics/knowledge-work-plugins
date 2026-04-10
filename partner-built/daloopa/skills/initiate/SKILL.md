---
name: initiate
description: Initiate coverage — generate both research note (HTML) and Excel model (.xlsx)
argument-hint: TICKER
---

Initiate coverage on the company specified by the user: $ARGUMENTS

**Before starting, read `data-access.md` for data access methods and `design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

This is the capstone skill that produces both a research note (styled HTML) and an Excel model (React artifact with SheetJS) from a single comprehensive data gathering pass.

## Strategy
Rather than running `/research-note` and `/build-model` independently (which would duplicate data gathering), this skill gathers a superset of data once, then renders both outputs.

## Phase 1 — Company Setup
Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations (see `data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `data-access.md` Section 4.5

Get market data using the 3-step resolution: (1) MCP market data tools if available, (2) web search, (3) sensible defaults (see data-access.md Section 2):
- Current price, market cap, shares outstanding, beta
- Trading multiples (P/E, EV/EBITDA, P/S, P/B)
- Risk-free rate (for DCF)

Initialize context: `context = {company_name, ticker, date, price, market_cap, firm_name, ...}`

## Phase 2 — Comprehensive Data Gathering
Calculate 8-16 quarters backward from `latest_calendar_quarter`. Pull:

**Income Statement — search and pull all available:**
- Revenue / Net Sales
- Cost of Revenue / COGS
- Gross Profit
- Research & Development
- Selling, General & Administrative
- Total Operating Expenses
- Operating Income
- Interest Expense / Income
- Pre-tax Income
- Tax Expense
- Net Income
- Diluted EPS
- Diluted Shares Outstanding
- EBITDA (or compute from Op Income + D&A, label "(calc.)")
- D&A

**Balance Sheet — search and pull all available:**
- Cash and Equivalents
- Short-term Investments
- Accounts Receivable
- Inventory
- Total Current Assets
- PP&E (net)
- Goodwill
- Total Assets
- Accounts Payable
- Short-term Debt
- Long-term Debt
- Total Liabilities
- Total Equity

**Cash Flow — search and pull all available:**
- Operating Cash Flow
- Capital Expenditures
- Depreciation & Amortization
- Acquisitions
- Dividends Paid
- Share Repurchases
- Free Cash Flow (compute if not direct: OCF - CapEx, label "(calc.)")

**Segments:**
- Revenue by segment
- Operating income by segment (if available)

**Geographic:**
- Revenue by geography

**KPIs:**
- All company-specific operating metrics (subscribers, units, ARPU, retention, etc.)

**Guidance:**
- All guidance series and corresponding actuals

**Share Activity:**
- Share count, buyback amounts

**For every value returned by `get_company_fundamentals`, record its `fundamental_id` (the `id` field).** Store each data point as `{value, fundamental_id}` so citations can be rendered in both outputs.

Compute margins, YoY growth rates, and ratios for each quarter.

### Cost Structure & Margin Analysis
After the core financial pull:
- **COGS driver identification**: Search for cost-related series ("cost of goods", "materials", "manufacturing", "input cost"). Identify 3-5 biggest cost line items and their trends.
- **OpEx breakdown**: Pull R&D and SG&A separately. Compute R&D % of revenue and SG&A % of revenue trends.
- **Margin driver analysis**: For each major margin (gross, operating, net), identify what's driving expansion or compression — pricing power, cost leverage, mix shift, or one-time items.

## Phase 3 — Industry-Specific Deep Dive
Determine the company's sector and apply the relevant analysis template:

- **Manufacturing/Industrial**: Bookings & backlog, book-to-bill ratio, pipeline by geography, capacity utilization
- **SaaS/Technology**: ARR/MRR trajectory, net retention rate, customer cohort analysis, RPO/deferred revenue trends
- **Retail/Consumer**: Same-store sales, store count trajectory, traffic vs ticket decomposition, inventory health
- **Financials/Banks**: NIM trajectory, provision trends, loan growth by category, capital ratios (CET1, TCE)
- **Healthcare/Pharma**: Pipeline summary (drug, indication, phase, milestone), product revenue breakdown, patent cliff timeline
- **Energy**: Production volumes, realized pricing vs benchmark, proved reserves, breakeven analysis

Search for relevant series using `discover_company_series` with sector-appropriate keywords. Pull available data and build the narrative.

Build `context.industry_deep_dive` (string) — sector-specific analysis narrative with Daloopa citations, organized by the relevant template above.

## Phase 4 — Peer Analysis
Identify 5-8 comparable companies.
Get peer trading multiples using the 3-step resolution: (1) MCP market data tools if available, (2) web search, (3) sensible defaults (see data-access.md Section 2).
If consensus forward estimates are available (data-access.md Section 3), include NTM estimates.
Pull peer fundamentals from Daloopa where available (revenue growth, margins).

Build `context.comps` and `context.comps_table`.

## Phase 5 — Projections
Build forward estimates using the following methodology:
- **Revenue:** Start with latest guidance (if available), then decay to long-term growth rate (industry average or historical trend). Apply quarterly seasonality patterns from trailing data.
- **Gross Margin:** Mean-revert to trailing 8-quarter average, with adjustment for recent trends or guidance commentary.
- **Operating Expenses:** Project as % of revenue, trending toward trailing averages. R&D and SG&A may have different trajectories.
- **CapEx:** Project as % of revenue based on trailing 4-8 quarter average and guidance.
- **D&A:** Project based on trailing average as % of revenue or PP&E.
- **Tax Rate:** Use trailing effective tax rate or guidance.
- **Share Count:** Project dilution/buyback based on trailing trends and guidance.
- **Working Capital:** Project DSO, DIO, DPO based on trailing averages.

Calculate all quarterly projections, then sum to annual. Project 4-8 quarters forward. Describe methodology inline and perform calculations directly.

## Phase 6 — DCF Valuation
Calculate:
- **WACC:** Use CAPM for cost of equity (Rf + Beta × ERP, where ERP = 6.0%). Cost of debt = Interest Expense / Total Debt. WACC = (E/V × Re) + (D/V × Rd × (1 - Tax Rate)).
- **5-year FCF projections:** Annualize from quarterly projections (FCF = Op Cash Flow - CapEx).
- **Terminal Value:** Use perpetuity growth at 2.5-3.0%.
- **Implied Share Price:** (PV of FCFs + Terminal Value - Net Debt) / Shares Outstanding
- **Sensitivity Matrix:** WACC (7 values: -3% to +3% from base) × Terminal Growth (6 values: 1.5% to 4.0%).

Build `context.dcf` and `context.dcf_summary` (set `context.has_dcf = true`).

## Phase 7 — Qualitative Research + News & Catalysts

### SEC Filing Research
Search SEC filings across multiple queries:
- "risk" / "uncertainty" / "challenge" for risk factors
- "growth" / "opportunity" / "expansion" for growth drivers
- "competition" / "market share" for competitive dynamics
- "outlook" / "guidance" for management's forward view
- Company-specific strategic topics (e.g., "AI", "cloud", etc.)

Extract and organize into:
- `context.risks` — ranked list of risks with impact/probability
- `context.investment_thesis` — variant perception, thesis pillars, catalysts
- `context.company_description` — 2-3 sentence business description

### News & Catalysts via WebSearch
Run 4 WebSearch queries to gather recent external context:
1. `"{TICKER} {company_name} news {year}"` — recent headlines and developments
2. `"{TICKER} analyst upgrade downgrade price target"` — sell-side sentiment shifts
3. `"{TICKER} catalysts risks"` — forward-looking events and risk factors
4. `"{company_name} industry outlook {sector}"` — macro and industry trends

Organize results into:
- `context.news_timeline` (string) — 6-10 key events from the last 6-12 months in reverse chronological order. Each event: date, headline, 1-sentence impact, sentiment tag (Positive / Negative / Mixed / Upcoming). Format as a numbered list.

- `context.forward_catalysts` (string) — Organized by timeframe:
  - **Near-term (0-3 months, HIGH priority)**: earnings dates, product launches, regulatory decisions
  - **Medium-term (3-12 months, MEDIUM priority)**: strategic milestones, contract renewals, industry events
  - **Long-term (1-3 years, LOW priority)**: secular trends, market expansion, competitive dynamics

- `context.policy_backdrop` (string) — Macro/regulatory context affecting the company. Tariffs, regulation, interest rates, sector-specific policy. Leave empty string if not material.

## Phase 8 — Guidance Track Record
Search for guidance series ("guidance", "outlook", "forecast", "estimate", "target").
Pull guidance and corresponding actuals. Apply +1 quarter offset rule for quarterly guidance, same-year rule for annual guidance from Q1/Q2/Q3, next-year rule for annual guidance from Q4.
Compute beat/miss rates and patterns.
Build `context.guidance` and `context.guidance_table` (set `context.has_guidance = true/false`).

## Phase 9 — What You Need to Believe
Build falsifiable bull/bear beliefs:

### Bull Beliefs (To Go Long)
Write 4-6 numbered beliefs, each with:
- One **bold statement** (the belief itself)
- 2-3 sentences of **evidence** with Daloopa citations supporting why this could be true
- Each belief must be **falsifiable** — testable with observable data within 6 months

Example format: "1. **Revenue growth re-accelerates to 15%+ as AI monetization scales.** Cloud segment grew [$X.Xbn](link) last quarter, up X% YoY, with management noting..."

### Bear Beliefs (To Go Short)
Same format — 4-6 numbered falsifiable beliefs with evidence for the downside case.

### Valuation Math
For each side:
- Bull target: forward multiple × forward earnings estimate = price target. Show the math.
- Bear target: same structure with bear-case multiple and earnings.

### Risk/Reward Assessment
- Compare bull upside % vs bear downside % from current price
- If asymmetry is significant (e.g., 30% upside vs 40% downside), flag it explicitly
- State which side has the better risk/reward and why

Build `context.bull_beliefs`, `context.bull_target`, `context.bear_beliefs`, `context.bear_target`, `context.risk_reward_assessment`.

## Phase 10 — Capital Allocation
Pull buyback, dividend, share count, FCF data.
Compute shareholder yield, FCF payout ratio, net leverage.
Build `context.capital_allocation_commentary`.

## Phase 11 — Synthesis + Tensions + Monitoring
This is the most judgment-intensive step. Be honest and critical — the reader is a professional investor who needs your real assessment, not a balanced summary.

### Core Synthesis
Write:
- **Executive Summary**: 3-4 sentence TL;DR covering current state, key thesis, valuation view. Include a clear directional view — is this stock attractive, fairly valued, or overvalued at the current price?
- **Variant Perception**: What does the market think vs what do you see in the data? Where is the consensus wrong? If you agree with consensus, say that too — but explain what could change.
- **Key Findings**: Top 3-5 most notable data points or trends — prioritize what changes the investment thesis, not just what's interesting
- **Red Flags & Concerns**: Any quality-of-earnings issues, sustainability questions, or risks the market may be underpricing
- Build `context.executive_summary`, `context.variant_perception`

### Five Key Tensions
Identify the 5 most critical bull/bear debates for this stock. Each tension is a single line that frames both sides. Alternate between bullish-leaning and bearish-leaning tensions. Every tension must reference a specific data point from the analysis.

Format as a numbered list:
1. "[Bullish factor] vs [Bearish factor]" — cite the specific metric
2. "[Bearish factor] vs [Bullish factor]" — cite the specific metric
...etc.

Build `context.five_key_tensions` (string).

### Monitoring Framework
Build two monitoring lists for ongoing tracking:

**Quantitative Monitors** — 5-7 specific metrics with explicit thresholds:
- Format: "Metric: current value → bull threshold / bear threshold"
- Example: "Gross Margin: 45.2% → above 46% confirms pricing power / below 43% signals cost pressure"

**Qualitative Monitors** — 5-7 factors to watch:
- Management tone shifts on earnings calls
- Competitive dynamics (new entrants, pricing pressure)
- Regulatory developments
- Customer concentration changes
- Capital allocation pivots

Build `context.monitoring_quantitative` and `context.monitoring_qualitative` (strings, numbered lists).

### Structured Tables
Build structured tables for both outputs:
- `context.key_metrics_table` — [{metric, value, vs_prior}] for the exec summary table
- `context.financials_table` — [{metric, q1, q2, ...}] for the financial analysis section
- `context.segments_table`, `context.geo_table`, `context.shares_outstanding_table`
- `context.opex_breakdown_table` — [{metric, q1, q2, ...}] for R&D, SG&A, % of revenue rows
- `context.guidance_table`, `context.comps_table`, etc.

## Phase 12 — Render Research Note (HTML)

Using the HTML Report Template from design-system.md, generate a styled HTML report with full CSS inlined. The report should include:

**Header Section:**
- Company name and ticker
- Report date and firm attribution
- Five Key Tensions (numbered list)

**Section 1: Executive Summary**
- Key metrics table
- Executive summary narrative
- Variant perception

**Section 2: Company Overview**
- Business description
- Investment thesis

**Section 3: Recent News & Catalysts**
- News timeline
- Forward catalysts
- Policy backdrop

**Section 4: Financial Analysis**
- Financials table (8-16 quarters)
- Cost structure & margin analysis
- OpEx breakdown table
- Segment and geographic tables
- Share count table

**Section 5: Industry-Specific Analysis**
- Industry deep dive narrative

**Section 6: Guidance Track Record**
- Guidance table and beat/miss analysis (if available)

**Section 7: What You Need to Believe**
- Bull beliefs with valuation target
- Bear beliefs with valuation target
- Risk/reward assessment

**Section 8: Catalysts**
- Forward catalysts
- Policy backdrop

**Section 9: Capital Allocation**
- Capital allocation commentary

**Section 10: Valuation**
- DCF summary and sensitivity (if available)
- Comps commentary (if available)

**Section 11: Risks**
- Risks summary

**Section 12: Monitoring Framework**
- Quantitative monitors
- Qualitative monitors

**Appendix:**
- Additional context or data

### Context Key Checklist
Verify these keys exist before rendering (set empty string if data unavailable):

**Cover & Summary:**
`company_name`, `ticker`, `date`, `price`, `market_cap`, `five_key_tensions`, `executive_summary`, `key_metrics_table`

**Thesis & Overview:**
`investment_thesis`, `variant_perception`, `company_description`

**News:**
`news_timeline`

**Financials:**
`financials_table`, `cost_margin_analysis`, `opex_breakdown_table`, `segments_table`, `geo_table`, `shares_outstanding_table`

**Industry:**
`industry_deep_dive`

**Guidance:**
`has_guidance`, `guidance_track_record`

**What You Need to Believe:**
`bull_beliefs`, `bull_target`, `bear_beliefs`, `bear_target`, `risk_reward_assessment`

**Catalysts:**
`forward_catalysts`, `policy_backdrop`

**Capital Allocation:**
`capital_allocation_commentary`

**Valuation:**
`has_dcf`, `dcf_summary`, `has_comps`, `comps_commentary`

**Risks:**
`risks_summary`

**Monitoring:**
`monitoring_quantitative`, `monitoring_qualitative`

**Appendix:**
`appendix_content`

**Citation enforcement:** Every financial figure from Daloopa in the HTML report must use citation format: `[$X.XX million](https://daloopa.com/src/{fundamental_id})`. If a number came from `get_company_fundamentals`, it must have a citation link. No exceptions.

## Phase 13 — Render Excel Model

Generate a React artifact that builds the .xlsx file using SheetJS (xlsx library). The artifact should:

1. Create 8 tabs with the following structure:

**Tab 1: Income Statement**
- Rows: Revenue, COGS, Gross Profit, R&D, SG&A, Total OpEx, Op Income, Interest, Pre-Tax Income, Tax, Net Income, Diluted EPS, Shares
- Columns: Historical periods (8-16Q) + Projected periods (4-8Q)
- Sub-rows: YoY growth %, margin % where applicable
- Header: Company name, ticker, report date
- Formatting: Numbers with commas/decimals, percentages, bold headers, frozen panes

**Tab 2: Balance Sheet**
- Rows: Assets section (Cash, Investments, AR, Inventory, Current Assets, PP&E, Goodwill, Total Assets), Liabilities section (AP, ST Debt, LT Debt, Total Liabilities, Equity)
- Columns: Historical + Projected periods
- Sub-rows: % of Total Assets for key line items
- Same formatting standards

**Tab 3: Cash Flow**
- Rows: Op Cash Flow, CapEx, Free Cash Flow, Acquisitions, Dividends, Buybacks, Net Change in Cash
- Columns: Historical + Projected periods
- Sub-rows: FCF yield %, CapEx as % Revenue
- Same formatting standards

**Tab 4: Segments**
- Rows: Revenue by segment, Op Income by segment (if available)
- Columns: Historical + Projected periods
- Sub-rows: Segment as % of total, segment growth rates
- Same formatting standards

**Tab 5: KPIs**
- Rows: All company-specific operating metrics discovered
- Columns: Historical + Projected periods
- Sub-rows: YoY growth or relevant unit economics
- Same formatting standards

**Tab 6: Projections**
- Editable assumption inputs (yellow highlighting): Revenue growth %, Gross margin %, Op margin %, CapEx % revenue, Tax rate %, Buyback rate QoQ
- Calculated outputs: Projected P&L, BS, CF driven by assumptions
- Commentary box explaining methodology
- Same formatting standards

**Tab 7: DCF**
- Inputs: WACC, Terminal Growth, Risk-Free Rate, ERP, Beta, Cost of Debt
- FCF Projection (5 years annualized)
- Terminal Value calculation
- PV calculations
- Enterprise Value → Equity Value → Implied Share Price
- Sensitivity table: WACC (rows) × Terminal Growth (cols) showing implied price
- Color scale: green (upside) to red (downside) vs current price
- Same formatting standards

**Tab 8: Summary**
- Company overview (name, ticker, sector, description)
- Current market data (price, market cap, shares, beta)
- Valuation summary: DCF implied price, peer-implied range, current price, upside/downside %
- Peer trading multiples table
- Key model outputs: Trailing revenue, Projected revenue growth, Trailing/Projected margins
- Same formatting standards

2. Apply design-system.md formatting conventions:
- Number format: $X.Xbn for large numbers, X.X% for percentages, X.Xx for multiples
- Color palette: Navy #1B2A4A (headers), Steel Blue #4A6FA5 (sub-headers), Gold #C5A55A (highlights), Green #27AE60 (positive), Red #C0392B (negative)
- Bold headers, frozen top row and left column
- Yellow fill (#FFEB3B) for editable input cells

3. Include a download button that triggers the .xlsx file download with filename: `{TICKER}_model.xlsx`

## Output
Present both deliverables to the user:

**Research Note (HTML):**
- Present the styled HTML report directly in the response
- Tell the user to save the HTML and open in browser for full formatting

**Excel Model (React Artifact):**
- Present the React artifact with SheetJS
- Tell the user to click the download button to save the .xlsx file
- Note that yellow cells in the Projections tab are editable inputs

**Summary:**
- 3-4 sentence executive summary
- Key valuation range (DCF implied price + comps range)
- Top 3 findings
- Bull upside % vs bear downside % risk/reward assessment

All financial figures must use Daloopa citation format: [$X.XX million](https://daloopa.com/src/{fundamental_id})
