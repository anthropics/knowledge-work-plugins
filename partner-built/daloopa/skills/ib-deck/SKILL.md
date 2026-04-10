---
name: ib-deck
description: Generate an institutional-grade investment banking pitch deck (HTML)
argument-hint: TICKER [--category ib-advisory|activist-ls]
---

Build an institutional-grade pitch deck for the company specified by the user: $ARGUMENTS

**Before starting, read `design-system.md` for formatting conventions and `data-access.md` for data access methods.** Also read the reference files in this skill's `references/` directory for slide templates and components.

This skill generates a self-contained HTML presentation that can be opened in a browser and printed to PDF if needed.

## Phase 1 — Requirements

Determine the deck category and scope:

**Category** (infer from context, or default to IB Advisory):
- **IB Advisory** — M&A advisory, fairness opinions, board presentations. Navy/steel/gold palette. "CONFIDENTIAL" marking.
- **Activist / L-S Equity** — Shareholder campaigns, investment memos as decks. Navy/blue/orange or navy/sky/green palette.

**Firm Attribution:**
- Firm name defaults to "Daloopa". If the user specifies a firm name in their prompt, use that instead.
- **NEVER hallucinate a firm name** (Goldman Sachs, Morgan Stanley, JPMorgan, etc.). See `data-access.md` Section 4.5.
- Include firm name on the cover slide and in all slide footers.

**Gather from the user or infer:**
- Target company (ticker)
- Purpose (M&A pitch, fairness opinion, investment memo, activist campaign)
- Key thesis or strategic rationale
- Specific slides needed (or use the default 14-slide deck)

## Phase 2 — Data Gathering

Look up the company by ticker using `discover_companies`. Capture `company_id`, `latest_calendar_quarter`, and `latest_fiscal_quarter`. Use `latest_calendar_quarter` to anchor all period calculations (see `data-access.md` Section 1.5).

Use Daloopa MCP for all financial data. Target comprehensive coverage:
- **5+ years of quarterly financials** — calculate 20+ quarters backward from `latest_calendar_quarter` (income statement, balance sheet, cash flow)
- **Segment and geographic breakdowns**
- **All company-specific operating KPIs**
- **6-10 peers** — get trading multiples and fundamentals from Daloopa + market data (see data-access.md Section 2)
- **Guidance and consensus** (see data-access.md Section 3)
- **SEC filings** — risk factors, growth drivers, M&A commentary, strategic language

Get market data for the target and all peers:
- Current price, market cap, shares outstanding, beta, trading multiples
- Historical price data for TSR comparison

Market data resolution order (see `data-access.md` Section 2):
1. MCP market data tools (if available)
2. Web search for current quotes, multiples, and historical data
3. Sensible defaults (industry-average multiples if specific data unavailable)

## Phase 3 — Analysis

Run the core analyses needed for the deck:
- **Valuation**: DCF (WACC, 5Y FCF projections, terminal value, sensitivity), comps table, implied valuation range
- **Scenario analysis**: Bull/base/bear with bottoms-up segment builds — be honest about which scenario is most likely
- **Capital allocation**: Buybacks, dividends, shareholder yield, leverage — flag any value-destructive patterns
- **Financial projections**: 3-5 year forward estimates — challenge assumptions, don't just extrapolate

**DCF Methodology** (inline calculation):
- Project 5 years of unlevered free cash flows (UFCF = NOPAT + D&A - CapEx - ΔWC)
- Discount at WACC (beta-based or peer-median if unavailable)
- Terminal value using perpetuity growth method (TGR 2-3%)
- PV of FCFs + PV of TV = EV → subtract net debt → equity value → per-share price

**Critical assessment:** The deck should present an honest analytical view, not a promotional pitch. If the valuation looks stretched, say so. If growth is decelerating, show it clearly. If risks are material, give them proper weight. Institutional investors will dismiss analysis that reads as advocacy rather than research.

## Phase 4 — Build Presentation

Generate a self-contained HTML file following the templates in `references/slide-templates.md`. Use components from `references/financial-components.md`.

**Slide structure** (default 14-slide deck — adapt based on purpose):

1. **Cover** — Company name, deck title, date, "CONFIDENTIAL" (if IB Advisory)
2. **Disclaimer** — Standard legal boilerplate
3. **Table of Contents** — Numbered sections
4. **Section Divider: Situation Overview**
5. **Executive Summary** — Two-column: situation overview + key findings
6. **Company Overview** — KPI callout row + business description + segment breakdown
7. **Financial Summary** — Dense income statement + margins + per-share + growth rates
8. **Section Divider: Valuation Analysis**
9. **Peer Benchmarking** — Full comps table (6-10 peers, trading multiples, footnoted)
10. **Valuation Analysis** — Football field chart + methodology summary
11. **DCF Detail** — Projection table + sensitivity matrix + assumptions
12. **Section Divider: Conclusion**
13. **Scenario Analysis** — Bull/base/bear bars + metric comparison table
14. **Appendix** — Raw data tables, dense formatting

**Key rules:**
- Every content slide must have minimum 2-3 data-rich elements (tables, charts, commentary)
- No sparse slides — fill the space with analysis
- All financial figures must include Daloopa citations
- Follow design-system.md for colors, typography, number formatting
- Use CSS `@page` with landscape orientation, 16:9 aspect ratio (1280×720px per slide)
- Each slide is a `<div class="slide">` with `page-break-after: always`
- All data displayed in tables (no chart generation)

See `references/ib-advisory-patterns.md` for valuation methodology templates.

## Phase 5 — Output

Present the complete HTML deck directly in your response. Use the HTML Report Template structure from `design-system.md` with slide-specific CSS from `references/slide-templates.md`.

Tell the user:
- The deck is ready to view — open in any browser
- To create a PDF: open in Chrome/Edge → Print → Save as PDF → set to Landscape orientation
- 2-3 sentence summary of the deck's key findings
- Implied valuation range
- How many slides were generated

## Citation Format

Every financial figure must use Daloopa citation format: [$X.XX million](https://daloopa.com/src/{fundamental_id})

All tables must follow the standard financial analysis format:
- **Columns** = time periods (Q1 2024, Q2 2024, etc.)
- **Rows** = financial metrics (Revenue, Net Income, etc.)

Data sourced from Daloopa.
