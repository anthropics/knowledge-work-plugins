---
name: comp-sheet
description: Build an industry comp sheet Excel model with deep operational KPIs
argument-hint: TICKER
---

Build a multi-company industry comp sheet Excel model for the company specified by the user: $ARGUMENTS

This produces an interactive `.xlsx` workbook — the kind of comp sheet every analyst on a coverage team maintains. Multi-company, multi-tab, with deep operational KPIs alongside standard financials.

**Before starting, read `data-access.md` for data access methods and `design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

Follow these steps:

## 1. Company & Peer Setup

Look up the target company by ticker using `discover_companies`. Capture `company_id`, `latest_calendar_quarter` (anchor for all period calculations — see `data-access.md` Section 1.5), and `latest_fiscal_quarter`. Note the firm name for report attribution (default: "Daloopa") — see `data-access.md` Section 4.5.

Then identify 6-10 comparable companies using the same logic as `/comps`:
- **Direct competitors** in the same market
- **Business model peers** (similar revenue model)
- **Size peers** (similar market cap range)
- **Growth profile peers** (similar growth rate)

Look up all peer company_ids via Daloopa. If a peer isn't available in Daloopa, include it with market data only and note the limitation.

List the full peer group with brief justification for each.

## 2. Deep Data Gathering

For each company (target + all peers), pull from Daloopa:

**Calculate 8 quarters backward from `latest_calendar_quarter`. Pull financials:**
- Revenue, Gross Profit, Operating Income, Net Income, Diluted EPS
- Operating Cash Flow, Capital Expenditures, D&A
- Free Cash Flow (compute as OCF - CapEx)
- R&D Expense, SG&A (where available)

**Segment revenue breakdown** (all available segments, 8 quarters)

**Company-specific operational KPIs** — use the 9-sector taxonomy to know what to search for:
- **SaaS/Cloud**: ARR, net revenue retention, RPO/cRPO, customers >$100K, cloud gross margin
- **Consumer Tech**: DAU/MAU, ARPU, engagement metrics, installed base, paid subscribers
- **E-commerce/Marketplace**: GMV, take rate, active buyers/sellers, order frequency
- **Retail**: same-store sales, store count, average ticket, transactions
- **Telecom/Media**: subscribers, churn, ARPU, content spend
- **Hardware**: units shipped, ASP, attach rate, installed base
- **Financial Services**: AUM, NIM, loan growth, credit quality metrics, fee income ratio
- **Pharma/Biotech**: pipeline stage, patient starts, scripts, market share
- **Industrials/Energy**: backlog, book-to-bill, utilization, production volumes, reserves

**Market data** for each company (see data-access.md Section 2):
- Price, market cap, enterprise value, shares outstanding, beta
- All trading multiples: P/E (trailing + forward), EV/EBITDA, P/S, P/B, EV/FCF, dividend yield

Follow the 3-step resolution order:
1. Check for MCP market data tools
2. Use web search if no MCP available
3. Fall back to sensible defaults if needed

## 3. KPI Discovery & Mapping

After pulling data, build the KPI mapping:
- Which KPIs are available for which companies? Build a coverage matrix.
- Group KPIs into categories:
  - **Segment Revenue**: product/service line breakdowns
  - **Growth KPIs**: subscriber growth, unit growth, same-store sales growth
  - **Unit Economics**: ARPU, ASP, take rate, retention
  - **Efficiency**: R&D % of revenue, SBC % of revenue, CapEx % of revenue
  - **Engagement**: DAU/MAU, retention, churn
- Flag KPIs that are comparable across peers vs company-specific

## 4. Compute Derived Metrics

For each company, calculate:

**Margins:**
- Gross Margin, Operating Margin, Net Margin, FCF Margin (each quarter)

**Growth rates:**
- Revenue YoY, EPS YoY, segment revenue YoY (each quarter where year-ago data exists)

**Capital metrics:**
- Net Debt (Total Debt - Cash)
- Net Debt/EBITDA
- FCF Yield (trailing 4Q FCF / Market Cap)
- Shareholder Yield (Buybacks + Dividends) / Market Cap

**Implied valuation:**
- For each valuation methodology (P/E, EV/EBITDA, P/S, EV/FCF):
  - Peer median multiple × target metric = implied value
  - Convert to implied share price
- Compute median implied price across methodologies

## 5. Build Excel Workbook

Generate a React artifact that uses SheetJS (xlsx library) to build and download the Excel file directly in the user's browser.

The workbook must contain 8 tabs with the following structure:

### Tab 1: Comp Summary
One-page overview with all companies side-by-side:
- Company name, ticker, price, market cap
- All valuation multiples (P/E, EV/EBITDA, P/S, P/B, EV/FCF, div yield)
- Latest quarter revenue, EBITDA, net income
- Growth rates (revenue YoY, EPS YoY)
- Key margins (gross, operating, net, FCF)
- Implied valuation for target (median across methodologies)
- Premium/discount vs peers

### Tab 2: Revenue Drivers
Unit economics decomposition per company (trailing 4 quarters):
- Total revenue (4Q sum)
- Segment revenue breakdown (% of total)
- Key unit economics: units × ASP, or subscribers × ARPU, etc.
- Growth trajectory by segment

### Tab 3: Operating KPIs
Cross-company KPI comparison matrix:
- Rows = KPIs (grouped by category from step 3)
- Columns = companies
- Show latest quarter value + YoY change where applicable
- Highlight cells where data is unavailable (sparse matrix)

### Tab 4: Financial Summary
Side-by-side income statements (trailing 4 quarters):
- Revenue, COGS, Gross Profit
- R&D, SG&A, Operating Income
- Interest, Tax, Net Income
- Diluted EPS
- Compute 4Q sums for each line item

### Tab 5: Growth & Margins
Trend analysis (up to 8 quarters):
- Revenue growth YoY (%)
- EPS growth YoY (%)
- Gross margin (%)
- Operating margin (%)
- Net margin (%)
- FCF margin (%)
- Show trends across all periods for each company

### Tab 6: Valuation Detail
Implied prices by methodology:
- P/E implied (peer median P/E × target EPS)
- EV/EBITDA implied
- P/S implied
- EV/FCF implied
- Median implied price
- Current price
- Premium/discount (%)

### Tab 7: Balance Sheet & Capital
Leverage and capital returns:
- Total Debt, Cash, Net Debt
- Net Debt/EBITDA
- Trailing 4Q: OCF, CapEx, FCF
- FCF Yield
- Shareholder Yield (buybacks + dividends)

### Tab 8: Raw Data
Full quarterly appendix for each company:
- All 8 quarters of financial data
- All KPIs by quarter
- All growth rates and margins by quarter
- Complete data backing the summary tabs

**Styling requirements:**
- Apply the design system color palette (Navy #1B2A4A headers, Steel Blue #4A6FA5 accents)
- Number formatting per design-system.md conventions
- Bold headers, freeze panes on all tabs
- Conditional formatting: green for positive growth, red for negative
- Auto-adjust column widths

The React artifact should:
1. Import the SheetJS library (xlsx)
2. Construct all 8 worksheets programmatically
3. Apply styling (bold headers, number formats, colors)
4. Generate the .xlsx file
5. Trigger browser download with filename: `{TARGET_TICKER}_comp_sheet_{DATE}.xlsx`

## 6. Output Summary

After generating the Excel workbook, provide a concise summary highlighting:

**Target positioning vs peers**:
- Where does it rank on growth, margins, and valuation?
- Quartile positioning across key metrics

**Most differentiated KPIs**:
- Which operational metrics set the target apart (positive or negative)?
- Notable outliers in the KPI matrix

**Implied valuation range**:
- What does the peer group suggest the stock is worth?
- Premium/discount vs current price
- Which methodology drives the highest/lowest implied value?

**Key risk**:
- What's the biggest vulnerability the comp sheet reveals (e.g., premium valuation with decelerating KPIs, margins below peers, concentration risk)?

All financial figures in the summary must use Daloopa citation format: [$X.XX million](https://daloopa.com/src/{fundamental_id})
