---
name: build-model
description: Build a multi-tab Excel financial model
argument-hint: TICKER
---

Build a comprehensive Excel financial model (.xlsx) for the company specified by the user: $ARGUMENTS

**Before starting, read `data-access.md` for data access methods and `design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

This skill gathers all available financial data and builds a multi-tab Excel model as a React artifact using SheetJS (xlsx library) that the user can download directly in their browser.

## Phase 1 — Company Setup
Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations (see `data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `data-access.md` Section 4.5

Get current stock price, market cap, shares outstanding, beta, and trading multiples for {TICKER}. Use the 3-step resolution: (1) MCP market data tools if available, (2) web search, (3) sensible defaults (see data-access.md Section 2).

## Phase 2 — Comprehensive Data Pull
Calculate periods backward from `latest_calendar_quarter`. Pull as much data as Daloopa has for this company. Target 8-16 quarters.

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
- EBITDA (or compute from Op Income + D&A)
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
- Free Cash Flow (compute if not direct)

**Segments:**
- Revenue by segment
- Operating income by segment (if available)

**KPIs:**
- All company-specific operating metrics

**Guidance:**
- All guidance series and corresponding actuals

## Phase 3 — Market Data & Peers
- Identify 5-8 peers and get their trading multiples using the same 3-step resolution: (1) MCP market data tools, (2) web search, (3) sensible defaults
- Get risk-free rate using the same 3-step resolution
- If consensus forward estimates are available (data-access.md Section 3), include NTM estimates for peers

## Phase 4 — Projections
Build forward estimates using the following methodology:
- **Revenue:** Start with latest guidance (if available), then decay to long-term growth rate (industry average or historical trend). Apply quarterly seasonality patterns from trailing data.
- **Gross Margin:** Mean-revert to trailing 8-quarter average, with adjustment for recent trends or guidance commentary.
- **Operating Expenses:** Project as % of revenue, trending toward trailing averages. R&D and SG&A may have different trajectories.
- **CapEx:** Project as % of revenue based on trailing 4-8 quarter average and guidance.
- **D&A:** Project based on trailing average as % of revenue or PP&E.
- **Tax Rate:** Use trailing effective tax rate or guidance.
- **Share Count:** Project dilution/buyback based on trailing trends and guidance.
- **Working Capital:** Project DSO, DIO, DPO based on trailing averages.

Calculate all quarterly projections, then sum to annual. Project 4-8 quarters forward.

## Phase 5 — DCF Inputs
Calculate:
- **WACC:** Use CAPM for cost of equity (Rf + Beta × ERP, where ERP = 6.0%). Cost of debt = Interest Expense / Total Debt. WACC = (E/V × Re) + (D/V × Rd × (1 - Tax Rate)).
- **5-year FCF projections:** Annualize from quarterly projections (FCF = Op Cash Flow - CapEx).
- **Terminal Value:** Use perpetuity growth at 2.5-3.0%.
- **Sensitivity Matrix:** WACC (7 values: -3% to +3% from base) × Terminal Growth (6 values: 1.5% to 4.0%).

## Phase 6 — Build Excel Model
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
Present the React artifact directly to the user with:
- Summary of what tabs were built
- Key model outputs: trailing revenue, projected revenue growth, implied DCF value, peer-implied range
- Note that yellow cells in the Projections tab are editable inputs
- Instruction to click the download button to save the .xlsx file

All financial figures gathered must use Daloopa citation format: [$X.XX million](https://daloopa.com/src/{fundamental_id})
