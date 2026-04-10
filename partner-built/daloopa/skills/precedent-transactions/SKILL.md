---
name: precedent-transactions
description: Precedent M&A transactions analysis with deal multiples and acquisition history
argument-hint: TICKER
---

Build a precedent transactions analysis for the company specified by the user: $ARGUMENTS

This is the third pillar of valuation (alongside trading comps and DCF) — it answers: what have acquirers actually paid for businesses like this one? The output is two tables: comparable M&A transactions with deal multiples, and the subject company's own acquisition history.

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

Follow these steps:

## 1. Company Lookup
Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations below (see `../data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5

Identify:
- Full legal company name
- Primary stock exchange and reporting currency
- Country of domicile and primary operations
- Industry and sub-sector
- Approximate revenue and EBITDA scale (to calibrate comparable deal sizing)

## 2. Subject Company Financials
Calculate 4 quarters backward from `latest_calendar_quarter`. Pull from Daloopa:
- Revenue (compute trailing 4Q / LTM total)
- EBITDA (compute trailing 4Q; if not available, use Operating Income + D&A, label "(calc.)")
- Operating Income
- Net Income
- Free Cash Flow (OCF - CapEx, label "(calc.)")

These serve as the reference point for comparing deal multiples — what would an acquirer be paying relative to this company's current financials?

## 3. Identify Comparable Precedent Transactions
Find 8-15 completed M&A transactions from the last 7-10 years involving target companies comparable to the subject. "Comparable" means:
- Same industry and sub-sector
- Similar business model (e.g., SaaS, semiconductor IP, consumer internet, industrials)
- Roughly comparable scale — within ~0.5x-4x of the subject's revenue
- Completed transactions only (not rumored, not pending)

**Research sources in priority order:**
1. **SEC EDGAR** (for US targets) — SC TO, DEFM14A, 8-K filings disclose EV and deal terms
2. **Equivalent regulators for non-US targets:** FCA (UK), EDINET (Japan), HKEx (Hong Kong), SEDAR+ (Canada), ASX (Australia)
3. **Official investor relations press releases** from acquirer or target
4. **Reputable financial news:** Reuters, Bloomberg, Wall Street Journal, Financial Times

Use web search to identify deals: `"{industry} acquisitions {sub-sector} last 10 years"`, `"{TICKER} comparable M&A transactions"`, `"{sector} deal comps precedent transactions"`.

**Do NOT use:** finance blogs, Seeking Alpha, Reddit, anonymous wiki contributions, or aggregators without a traceable primary source.

For each transaction, capture:
- Announcement date
- Acquirer name
- Target name
- Transaction Enterprise Value
- Deal consideration (All Cash / All Stock / Cash + Stock)
- Source (press release URL, SEC filing, or regulatory filing)

## 4. Source Target Financials via Daloopa
For each target company in the precedent transactions table, source LTM Revenue and EBITDA from Daloopa:

1. **Look up the target** using `discover_companies` with the target's ticker or name
2. **Find relevant series** using `discover_company_series` with keywords `["revenue", "EBITDA"]` and the appropriate period (the last complete fiscal year before the deal announcement)
3. **Pull the data** using `get_company_fundamentals` with the discovered series IDs
4. For EBITDA, look for series containing "Adjusted EBITDA", "EBITDA", or fall back to "Operating Income" + D&A
5. If a target is not in Daloopa (e.g., pre-IPO targets, private companies), fall back to SEC filings, press releases, or regulatory filings

**Daloopa is the primary source.** Only fall back to other sources when a target is genuinely unavailable in the database.

## 5. Compute Deal Multiples
For each transaction where both EV and financials are available:
- **EV/Revenue** = Transaction EV ÷ LTM Revenue
- **EV/EBITDA** = Transaction EV ÷ LTM EBITDA
- Round to one decimal, append "x"
- If a figure cannot be sourced, mark as **N/A** — do not estimate

Compute summary statistics (excluding N/A values):
- 75th Percentile
- **Average** (bold)
- **Median** (bold)
- 25th Percentile

If fewer than 3 valid data points exist for a multiple, note that the statistic is not meaningful.

## 6. Subject Company's Acquisition History
Find deals where the subject company itself was the acquirer. Sources: company IR page, SEC 8-K or equivalent filings, Reuters/Bloomberg/WSJ.

For each acquisition, capture:
- Date
- Target name
- Deal value (if disclosed)
- Consideration (Cash / Stock / Mix)
- Strategic rationale (one sentence from press release or filing)

## 7. Implied Valuation for Subject Company
Apply the precedent transaction multiples to the subject's current financials:

| Methodology | Percentile | Multiple | Subject LTM Metric | Implied EV |
|---|---|---|---|---|
| EV/Revenue | Median | XX.Xx | $XXX | $XXX |
| EV/Revenue | 25th-75th | XX.Xx-XX.Xx | $XXX | $XXX-$XXX |
| EV/EBITDA | Median | XX.Xx | $XXX | $XXX |
| EV/EBITDA | 25th-75th | XX.Xx-XX.Xx | $XXX | $XXX-$XXX |

Convert implied EV to implied equity value (EV - Net Debt) and implied share price where market data is available (see `../data-access.md` Section 2). Compare to current market price.

**Context matters more than precision:**
- Precedent transaction multiples are snapshots from specific deal contexts (competitive auctions, strategic premiums, distressed sales). Note which deals had unusual dynamics.
- Control premiums are embedded in these multiples — a public market investor should not expect to realize the full precedent transaction value unless a takeout actually happens.
- If the current market cap is well below precedent transaction implied value, that's a signal of takeout optionality, not necessarily undervaluation.

## 8. Deal Environment Commentary
Search filings and news for context on the M&A environment:
- Search: `"{industry} M&A outlook {current_year}"` — deal activity trends
- Search: `"{TICKER} acquisition target rumors"` — is the subject itself a takeout candidate?

Summarize in 3-5 bullets:
- Is deal activity in this sector accelerating or declining?
- What are typical premiums being paid (control premium trends)?
- Are strategic buyers or financial sponsors (PE) driving activity?
- Any regulatory headwinds to deals in this space (antitrust scrutiny)?
- Is the subject company a plausible acquisition target? Why or why not?

## 9. Save Report
Save to `reports/{TICKER}_precedent_transactions.html` using the HTML report template from `../design-system.md`. Write the full analysis as styled HTML with the design system CSS inlined. This is the final deliverable — no intermediate markdown step needed.

The report should include interactive features:
- **Clickable acquirer names** in Table 1 that open a modal showing all source links for that transaction (press release, SEC filing, Daloopa data links). Implement with `data-` attributes and safe DOM methods (`createElement`, `textContent`, `appendChild`) — never `innerHTML`.
- **Consideration badges** styled inline: All Cash (green background), All Stock (purple background), Cash + Stock (amber background).

Structure the report with these sections:

```
<h1>{Company Name} ({TICKER}) — Precedent Transactions Analysis</h1>
<p>Generated: {date}</p>

<h2>Summary</h2>
{2-3 sentences: What do precedent transactions imply for this company's valuation? How does it compare to the current market price?}

<h2>Subject Company Overview</h2>
{Exchange, currency, industry, LTM Revenue and EBITDA with Daloopa citations}
{Note: "Revenue and EBITDA sourced from Daloopa where available"}

<h2>Selected Precedent Transactions</h2>
<table>
| Date | Acquirer | Target | EV ($M) | LTM Rev ($M) | LTM EBITDA ($M) | EV/Rev | EV/EBITDA | Consideration |
{data rows with Daloopa-cited financials, footnote superscripts, clickable acquirers}
| 75th Percentile | | | | | | XX.Xx | XX.Xx | |
| **Average** | | | | | | **XX.Xx** | **XX.Xx** | |
| **Median** | | | | | | **XX.Xx** | **XX.Xx** | |
| 25th Percentile | | | | | | XX.Xx | XX.Xx | |
</table>

<h2>Implied Valuation</h2>
<table>
| Methodology | Multiple | Subject Metric | Implied EV | Implied Equity | Implied Price | vs Current |
{valuation bridge using median and range multiples}
</table>

<h2>{Company Name} Acquisition History</h2>
<table>
| Date | Target | Deal Value | Consideration | Strategic Rationale |
{company's own M&A deals}
</table>

<h2>Deal Environment</h2>
<ul>{3-5 bullets on sector M&A trends, control premiums, takeout potential}</ul>

<h2>Sources</h2>
{Numbered footnote list — each deal with press release link, SEC filing, Daloopa data links}
{Data sourced from Daloopa attribution}
```

All financial figures from Daloopa must use citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved.

Highlight: what precedent transactions imply about the company's takeout value, how it compares to the current market price, and whether the sector M&A environment supports deal activity.
