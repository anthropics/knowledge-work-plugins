---
name: earnings-flash
description: Rapid first-read earnings flash for a given company
argument-hint: TICKER
---

Generate a rapid earnings flash for the company specified by the user: $ARGUMENTS

This is a lightweight, speed-focused version of `/earnings` — designed for a quick first read within minutes of a filing. It pulls just enough context from Daloopa to frame BEAT/MISS verdicts, then focuses on what's new and surprising.

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

## 1. Company Lookup

Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations (see `../data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5

## 2. Prior Quarter Context (4 Quarters)

Calculate 4 quarters backward from `latest_calendar_quarter`. Search for and pull these core metrics:

**Income Statement:**
- Revenue / Net Sales
- Gross Profit
- Operating Income / EBIT
- Net Income
- Diluted EPS

**Cash Flow:**
- Operating Cash Flow
- Free Cash Flow (or CapEx to compute it)

This is lighter than `/earnings` (4Q vs 8Q, no cost structure breakdown). The goal is just enough history to frame the latest quarter's results — not a full trend analysis.

## 3. Company-Specific KPIs

Think about the 3-5 most important KPIs for THIS company based on its business model. Search for those specific KPIs and pull for the same 4-quarter period. Also search for:
- Segment/product revenue breakdown
- Geographic revenue breakdown (if material)

Keep this targeted — discover the critical operating metrics, not everything available.

## 4. Guidance Series

Search for guidance series (revenue guidance, EPS guidance, margin guidance, any KPI guidance). If available, pull guidance data for the latest 2 quarters so you can compare the most recent actual results against what management guided.

CRITICAL: Apply +1 quarter offset — guidance from Q(N) applies to Q(N+1) results.

## 5. Get the Earnings Document

Use `search_documents` to find the most recent earnings-related filing. Search strategy:
1. Search for keywords `["results", "earnings"]` in the latest 1-2 calendar quarters
2. If that returns nothing, try `["revenue"]` or `["financial"]` as broader terms

Read the document content from the search results. Focus on:
- **Earnings transcripts**: Full document (management commentary, prepared remarks, Q&A)
- **10-Q / 10-K**: Financial statements and MD&A sections
- **8-K**: Full document (short event-driven filings)

If no document is found, proceed with the MCP fundamentals data only and note "No earnings document found — analysis based on financial data only."

## 6. Executive Flash

Write 3-5 bullet-point verdicts. Each bullet MUST compare the latest quarter's results against prior periods from Step 2 and/or guidance from Step 4. Format:

**[BEAT/MISS/INLINE/MIXED] | Key number (YoY change) | One-sentence context**

Examples:
- **BEAT | Revenue $95.4bn (+6.1% YoY) | Acceleration from +4.8% last quarter driven by iPhone 16 cycle**
- **MISS | EPS $1.46 vs $1.52 prior year | Higher opex from AI investments weighed on margins**
- **GUIDANCE UP | FY2026 revenue guided $400-405bn | Management raised full-year outlook on cloud strength**

Use Daloopa citation links for all figures sourced from MCP. Use "(per filing)" for figures only found in the document.

Also include a one-line **Management Tone** assessment (confident/cautious/defensive/evasive/optimistic) if an earnings document was available. Support with specific language from the document.

## 7. Key Numbers Table

Present the latest quarter's results with comparison context:

| Metric | Latest Quarter | Prior Quarter | YoY Change | vs Guidance |
|--------|---------------|---------------|------------|-------------|

Include: revenue, EPS, margins, segment breakdowns, KPIs — all sourced from MCP with Daloopa citation links. Add a "vs Guidance" column if guidance data was available from Step 4 (show beat/miss amount).

Group by category: P&L, Segments, KPIs, Cash Flow.

For figures only available from the document (not in MCP), include them in a separate "Per Filing" sub-section below the table and note they are not cross-referenced.

## 8. Guidance & Outlook

Extract forward-looking statements from the earnings document (if available):
- Explicit numerical guidance (revenue, EPS, margin ranges)
- Changes from prior guidance (raised, lowered, narrowed, withdrawn)
- Qualitative outlook language
- Capex/investment plans

If guidance data was pulled from Daloopa in Step 4, compare new guidance against prior guidance with a table:

| Metric | New Guidance | Prior Guidance | Change |
|--------|-------------|---------------|--------|

If no document was found, summarize any guidance series data from Step 4 and note that no new guidance language is available.

## 9. Risk Flags

Call out concerning signals — this section should be sharp and skeptical:
- Guidance cuts or narrowing
- Missing disclosures or metrics that were previously reported
- Growing gap between GAAP and non-GAAP
- Cash flow divergence from earnings
- One-time items that flatter the headline numbers
- Management hedging or qualifying language (from document)

If no material risk flags, say so clearly: "No material risk flags identified."

## 10. Quick Read-Throughs

Write 2-3 bullets on what this filing implies for adjacent companies:
- **Suppliers**: Positive or negative signal for key input providers
- **Customers**: Demand signal for downstream buyers
- **Competitors**: Share shift, pricing, or market growth implications

Format: `**[COMPANY/SECTOR]**: [implication] (based on [specific data point])`

## 11. Save Report

Save the HTML report to: `reports/{TICKER}_earnings_flash_{PERIOD}.html` (where PERIOD is the latest calendar quarter analyzed).

Use the design-system HTML template from `../design-system.md`. Include all CSS inlined.

Add a **FLASH** banner at the top of the report. Insert this right after the opening `<body>` tag, before the `<h1>`:

```html
<div style="background: #C0392B; color: white; text-align: center; padding: 8px 16px; font-size: 14px; font-weight: bold; letter-spacing: 2px; margin-bottom: 16px;">
    EARNINGS FLASH — FIRST READ
</div>
```

The `<h1>` should be: `{TICKER} Earnings Flash — {PERIOD}`

Add a disclaimer after the flash banner:
```html
<p style="font-size: 10px; color: #6C757D; font-style: italic; margin-bottom: 16px;">
    This is a rapid first-read summary. For full analysis with 8-quarter trends, cost structure,
    and competitive read-throughs, run /earnings {TICKER}.
</p>
```

Replace `{FIRM_NAME}` in the footer — see `../data-access.md` Section 4.5.

All financial figures from Daloopa must use citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved and highlight the 2-3 most notable findings.

