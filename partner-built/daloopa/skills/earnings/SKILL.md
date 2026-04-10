---
name: earnings
description: Full earnings analysis with guidance tracking for a given company
argument-hint: TICKER
---

Perform a comprehensive earnings analysis for the company specified by the user: $ARGUMENTS

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

Follow these steps:

## 1. Company Lookup
Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations below (see `../data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5

## 2. Core Financial Metrics
Calculate 8 quarters backward from `latest_calendar_quarter`. Search for these metrics, then pull:

**Income Statement:**
- Revenue / Net Sales
- Gross Profit
- Operating Income / EBIT
- EBITDA (if not reported, compute as Operating Income + D&A — label it "EBITDA (calc.)")
- Net Income
- Diluted EPS
- Operating Expenses (SG&A, R&D where available)

**Cash Flow & Balance Sheet:**
- Operating Cash Flow
- CapEx (Purchases of property, plant and equipment)
- Free Cash Flow (compute as Operating Cash Flow - CapEx — label it "FCF (calc.)")
- D&A (needed for EBITDA calc if not directly reported)

For any derived/computed metric, mark it with "(calc.)" so the reader knows it's not directly sourced.

Flag any one-time items that distort a quarter (e.g., tax charges, impairments, litigation settlements) with a footnote so YoY comparisons aren't misleading.

## 3. Company-Specific KPIs
First, think about what the most important KPIs are for THIS specific company based on its business model and what drives its valuation. For example:
- **SaaS/cloud**: ARR, net revenue retention, RPO/cRPO, customers >$100K
- **Consumer tech**: DAU/MAU, ARPU, engagement metrics, installed base, paid subscribers
- **E-commerce/marketplace**: GMV, take rate, active buyers/sellers, order frequency
- **Retail**: same-store sales, store count, average ticket, transactions
- **Telecom/media**: subscribers, churn, ARPU, content spend
- **Hardware**: units shipped, ASP, attach rate
- **Financial services**: AUM, NIM, loan growth, credit quality metrics
- **Pharma/biotech**: pipeline stage, patient starts, scripts, market share

Then search for those specific KPIs by name, plus cast a wider net for anything else available. Also search for:
- Segment/product revenue breakdown
- Geographic revenue breakdown

Pull for the same 8-quarter period. If some KPIs only have data for recent quarters, include what's available and note the gap.

## 4. Growth & Margins
Calculate and present:
- YoY revenue growth for each of the last 4 quarters (not just one)
- Gross margin, operating margin, EBITDA margin, net margin trends over 8 quarters
- EPS growth YoY for each of the last 4 quarters
- Segment revenue YoY growth for the most recent quarter
- Geographic revenue YoY growth for the most recent quarter
- KPI growth rates where applicable

If the company has strong seasonality (e.g., retail Q4 holiday, back-to-school, cyclical patterns), add a note so the reader interprets QoQ swings correctly.

## 4.5. Cost Structure & Margin Drivers
Decompose what's driving margin trends. This turns the margin table from Section 4 into an analytical narrative.

**COGS Analysis:**
- Pull product COGS and services COGS (or equivalent cost breakdown) if available
- Identify the 3-5 biggest cost line items and their YoY trends
- Is COGS growing faster or slower than revenue? If slower, what's driving the efficiency — input costs, mix shift, pricing power, or scale leverage?

**OpEx Breakdown:**
- Pull R&D and SG&A separately for the last 8 quarters
- Compute R&D % of revenue and SG&A % of revenue trends
- Is the company investing more in R&D (growth mode) or cutting SG&A (efficiency mode)? Both? Neither?
- Flag any quarter where OpEx growth materially exceeds revenue growth — that's operating deleverage

**Margin Driver Synthesis:**
For each major margin (gross, operating, net), write 1-2 sentences identifying what's driving expansion or compression:
- Pricing power vs cost inflation
- Mix shift (higher-margin products/services growing faster)
- Scale leverage vs investment spending
- One-time items distorting the trend
- FX impact if material

Include this as a commentary block after the margins table in the report. Cite specific Daloopa figures.

## 5. Guidance vs Actuals
Search for guidance series (revenue guidance, EPS guidance, margin guidance, OpEx guidance, any KPI guidance). If available:
- Pull guidance and actual results
- CRITICAL: Apply +1 quarter offset — guidance from Q(N) applies to Q(N+1) results
- Calculate beat/miss amounts and percentages
- Note patterns (consistent beats, narrows, etc.)
- If the company provides directional guidance (e.g., "low-to-mid-teens growth") rather than hard numbers, note this and compare against the actual growth rate

If no formal guidance series exist, note that the company does not provide quantitative guidance.

## 6. Consensus Context (if available)
If consensus estimates are available (see ../data-access.md Section 3), add:
- Consensus revenue and EPS vs actual results — beat/miss vs Street
- Estimate revision trends (are estimates moving up or down?)
- Note the source of consensus data used

If consensus data is not available, skip this section and note "consensus data not available."

## 7. Management Commentary
Search SEC filings/documents for management commentary. Try multiple searches to get broad coverage:
- First search: "results" or "record" for earnings highlights
- Second search: "outlook" or "guidance" for forward-looking commentary
- Third search: strategy-specific terms relevant to the company (e.g., "AI", "cloud", "subscribers")
- If a search returns empty, try broader single-keyword searches before giving up

Extract:
- Earnings results and key drivers
- Forward outlook and guidance language
- Segment performance highlights
- Any notable call-outs (one-time items, macro commentary, strategic updates)
- Direct management quotes where available (with document citations)

## 7.5. News Context
Run 2 WebSearch queries to add external context around the earnings:
1. `"{TICKER} {company_name} earnings {latest_quarter} {year}"` — coverage and analyst reactions
2. `"{TICKER} analyst price target {year}"` — sell-side sentiment

Distill into a brief **Earnings Context** block (3-5 bullet points):
- How did the stock react to earnings? (if available from search results)
- What were the key analyst takeaways or debates?
- Any price target changes or rating changes post-earnings?
- Any macro/industry context that affected the quarter?

Keep this concise — it supplements the Daloopa data with market reaction context. Include it as a short section in the report before the Forward Outlook.

## 7.6. Forward Outlook & Revenue Drivers

Synthesize the backward-looking data into a forward-looking view. This section turns the earnings analysis from "what happened" into "what it means for the future."

**Forward Guidance Analysis:**
- What is management guiding for NEXT quarter and/or full year? Extract specific numbers (revenue range, EPS range, margin targets, CapEx plans).
- Is the guide conservative or aggressive? Compare to: (a) the company's historical beat rate from Section 5, (b) the current run rate extrapolated forward, (c) consensus if available. A company that beats by 3% every quarter and guides flat is sandbagging; a company that guides for acceleration after 3 quarters of deceleration is aggressive.
- How does forward guidance compare to trailing trends? If revenue grew +8% YoY last quarter and guidance implies +5%, is management signaling deceleration or being conservative?

**Revenue Driver Decomposition:**
- Break down what's driving growth: volume vs price vs mix. Which segments are contributing vs dragging?
- For each major segment, identify the unit economics driver: units x ASP, subscribers x ARPU, GMV x take rate, etc.
- What has to happen for current growth rates to sustain? If growth is coming from price increases, is there a ceiling? If from volume, is the TAM expanding or saturating?

**KPI Trajectory Implications:**
- Connect KPI trends to revenue outlook. If subscriber growth is decelerating, what does that imply for next quarter's revenue? If ASPs are rising but units are flat, is that sustainable?
- If backlog/RPO/deferred revenue is building, when does it convert to recognized revenue? If it's declining, that's a leading indicator of future revenue pressure.
- Flag any KPI-to-revenue divergences (e.g., user growth accelerating but ARPU declining — net effect on revenue?)

**Trend Synthesis:**
- Looking at the last 4-8 quarters holistically — is this company accelerating, decelerating, or at a plateau?
- What's the single most important metric to watch next quarter? Why?
- Are operating KPIs leading or lagging the financial results?

**Risks to the Forward View:**
- What could go wrong with the guidance? What assumptions are embedded that could break?
- Identify the 2-3 biggest risks to the forward trajectory: competitive threats, macro sensitivity, product cycle dependency, regulatory risk, customer concentration.
- If the bull case requires multiple things to go right simultaneously, flag that explicitly.

## 7.7. Read-Throughs & Competitive Implications

This is one of the most valuable sections of the report. Every company's earnings contain signal about adjacent companies — suppliers, customers, competitors, and the broader industry. An analyst covering a sector doesn't just read one company's print; they read it for what it says about every other name in their portfolio.

**Identify the Read-Through Universe:**
Think about who is most affected by this company's results. Consider:
- **Suppliers**: If this company's revenue/COGS/CapEx changed materially, which suppliers feel it? (e.g., AAPL iPhone strength → TSMC, Broadcom, Corning benefit; AAPL CapEx guidance up → supplier order books filling)
- **Customers**: If this company is a major input to others, what do its pricing/volume trends imply? (e.g., TSMC price increases → margin pressure for AAPL, AMD, NVDA)
- **Direct competitors**: How does this quarter compare to what peers have reported or guided? Is this company gaining or losing share? (e.g., MSFT cloud growth accelerating while AMZN AWS decelerates → share shift)
- **Indirect competitors / substitutes**: Any signals about demand shifting between categories? (e.g., strong enterprise software spend → weak services/consulting spend)
- **Industry bellwether signals**: If this is a large company, what do its results say about the macro/sector? (e.g., consumer discretionary weakness at WMT → read-through to all retail)

**For each read-through (aim for 5-8), state:**
1. **The affected company** (ticker + name)
2. **The specific data point** from this earnings that creates the read-through — cite the Daloopa figure
3. **The implication** — bullish or bearish for the adjacent company, and why
4. **Confidence level** — is this a direct/disclosed relationship (high confidence) or an inferred/estimated one (moderate)?

**Example read-throughs:**
- "AAPL Services revenue grew +14% YoY to $26.3B → **Positive for APP (AppLovin)**: Apple's App Store is a major distribution channel; growing Services revenue confirms healthy app ecosystem spending. **Negative for GOOG**: AAPL's growing services monetization strengthens their negotiating leverage on the Google TAC agreement."
- "TSMC guided CapEx up 25% YoY → **Positive for ASML, AMAT, LRCX, KLAC**: equipment spend is the most direct read-through to semicap names. ASML in particular given EUV concentration."
- "NFLX added 19M subscribers vs 13M expected → **Negative for DIS, WBD, PARA**: In a zero-sum attention economy, NFLX's accelerating sub growth likely came partly at the expense of other streamers."

**Sequencing context:**
- Note whether this company reported before or after its peers this earnings season. If it's early in the cycle, the read-throughs are forward-looking predictions. If it's late, compare against what peers already reported — confirm or contradict the emerging narrative.
- If a peer has already reported, note any divergence: "MSFT reported cloud growth of +29% last week; today's AMZN AWS at +19% confirms the share shift narrative."

**Web research for validation:**
Run 1-2 targeted searches to validate read-throughs:
- `"{TICKER} earnings read through implications {year}"` — analyst commentary on cross-company signals
- `"{TICKER} {peer_ticker} competitive positioning {year}"` — specific competitive dynamics

Present as a structured list in the report, grouped by relationship type (Suppliers / Customers / Competitors / Industry). Each read-through should be a concise 2-3 sentence paragraph with the data citation, the affected name, and the implication.

## 8. Save Report
Save to `reports/{TICKER}_earnings_{PERIOD}.html` (where PERIOD is the most recent quarter analyzed) using the HTML report template from `../design-system.md`. Write the full analysis as styled HTML with the design system CSS inlined. This is the final deliverable — no intermediate markdown step needed.

The report should include:
- Executive summary (2-3 sentence overview of the quarter + 2-3 most notable findings)
- Core financial metrics table (8 quarters, periods as columns, metrics as rows, including FCF)
- Segment and geographic revenue breakdown tables
- KPI table (with notes on any data gaps)
- Margin trends table (8 quarters)
- Cost structure & margin driver commentary (after margins table)
- YoY growth rates table (last 4 quarters, showing each quarter's YoY)
- Guidance vs actuals table (if applicable) with pattern analysis
- News context (analyst reactions, price target changes, market sentiment)
- Forward outlook and revenue drivers analysis
- Management commentary with direct quotes and document citations
- Read-throughs & competitive implications (grouped by Suppliers / Customers / Competitors / Industry)
- Seasonality note if applicable

All financial figures must use Daloopa citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved.

Highlight the 2-3 most notable findings with a critical lens:
- **Quality of earnings**: Are the beats sustainable or driven by one-time items, favorable timing, or accounting changes? Is revenue growth real or pulled forward?
- **Red flags**: Any deterioration in cash conversion, growing GAAP vs non-GAAP gaps, rising SBC dilution, margin expansion from under-investment?
- **What the market is missing**: What does the data say that consensus might not be pricing in — positive or negative?
