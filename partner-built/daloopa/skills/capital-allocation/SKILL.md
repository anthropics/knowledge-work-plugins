---
name: capital-allocation
description: Deep dive into capital deployment, buybacks, dividends, and shareholder yield
argument-hint: TICKER
---

Perform a deep dive into capital allocation for the company specified by the user: $ARGUMENTS

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

Follow these steps:

## 1. Company Lookup
Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations below (see `../data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5

## 2. Market Data
Get the current stock price, market cap, and shares outstanding for {TICKER} (see ../data-access.md Section 2 for how to source market data in your environment).
- This is needed to compute yields and per-share metrics

If market data is unavailable, note that market-derived metrics (yields, etc.) cannot be computed and proceed with Daloopa data only.

## 3. Capital Allocation Data
Calculate 8 quarters backward from `latest_calendar_quarter`. Pull:

**Share Count & Buybacks:**
- Diluted shares outstanding
- Share repurchase amounts (dollars)
- Shares retired/repurchased (units, if available)

**Dividends:**
- Dividends per share
- Total dividend payments
- Special dividends (if any)

**Cash Flow:**
- Operating Cash Flow
- Capital Expenditures
- Free Cash Flow (compute as OCF - CapEx, label "(calc.)")
- D&A (for reference)

**Balance Sheet:**
- Cash and equivalents
- Short-term investments / marketable securities
- Total debt (short + long term)
- Net debt (compute as Total Debt - Cash - Investments, label "(calc.)")

**M&A / Investments:**
- Search for "acquisition", "purchase of business", "investment" in series
- Pull any available M&A-related series

## 4. Compute Capital Allocation Metrics
Calculate for each quarter where data is available:

**Shareholder Returns:**
- Total Buyback Amount
- Total Dividend Amount
- Total Shareholder Return = Buybacks + Dividends
- Shareholder Yield = (Buybacks + Dividends) / Market Cap (annualized)
- Buyback Yield = Buybacks / Market Cap (annualized)
- Dividend Yield = Dividends / Market Cap (annualized)

**FCF Deployment:**
- FCF Payout Ratio = Total Shareholder Return / FCF
- CapEx as % of Revenue
- CapEx as % of OCF
- FCF Margin = FCF / Revenue

**Leverage:**
- Net Debt / EBITDA (if EBITDA available; compute from Operating Income + D&A if needed)
- Net Debt / Equity
- Interest Coverage = Operating Income / Interest Expense (if available)
- Cash as % of Market Cap

**Share Count Dynamics:**
- QoQ share count change
- YoY share count change
- Implied buyback rate (QoQ % reduction)
- At current buyback rate, years to retire X% of shares

## 5. Qualitative Research
Search SEC filings for capital allocation strategy and context. Try multiple searches:
- **Buyback program**: Try "repurchase program", "share repurchase"; fallback to "buyback", "authorization"
- **Dividend policy**: Try "dividend", "capital return"; fallback to "distribution", "payout"
- **M&A strategy**: Try "acquisition", "strategic"; fallback to "purchase", "investment"
- **Capital priorities**: Try "capital allocation", "priorities"; fallback to "deploy", "balance sheet"
- **Debt management**: Try "debt", "refinance"; fallback to "leverage", "maturity"

Extract:
- Board-authorized buyback programs (remaining authorization amount)
- Dividend policy (commitment to growth, payout ratio targets)
- M&A philosophy (bolt-on vs transformational, deal pipeline commentary)
- Management's stated capital allocation framework and priorities
- Any changes in capital allocation strategy
- Direct quotes with document citations

## 6. Historical Analysis & Value Judgment
Analyze the 8-quarter trend:
- Is buyback activity accelerating or decelerating?
- Is the company buying back more shares when price is lower (disciplined) or higher (less disciplined)?
- Dividend growth rate (if applicable)
- Shift between CapEx, buybacks, dividends, and debt repayment over time
- FCF conversion trend (is more/less of OCF converting to FCF?)

**Honestly assess whether capital allocation is creating or destroying value:**
- If the company is buying back stock at all-time-high prices with deteriorating fundamentals, call it value destruction — even if EPS looks better from the lower share count.
- If the company is under-investing in CapEx or R&D to fund buybacks, flag the risk to long-term competitiveness.
- If FCF payout ratio exceeds 100%, the company is funding returns with debt or cash drawdowns — flag this as unsustainable.
- Compare the implied return from buybacks (inverse of P/E at purchase prices) to what the company could earn from organic reinvestment or M&A.

## 6.5. Reinvestment Assessment

Assess whether the company is adequately reinvesting in its business or funding returns at the expense of long-term competitiveness.

**Pull reinvestment metrics (8 quarters):**
- R&D expense (and R&D as % of revenue)
- Capital Expenditures (and CapEx as % of revenue)
- Key growth KPIs relevant to the business model (use sector taxonomy):
  - **SaaS/Cloud**: ARR, net revenue retention, RPO/cRPO, customers >$100K
  - **Consumer Tech**: DAU/MAU, ARPU, installed base, paid subscribers
  - **E-commerce/Marketplace**: GMV, take rate, active buyers/sellers
  - **Retail**: same-store sales, store count, average ticket
  - **Telecom/Media**: subscribers, churn, ARPU, content spend
  - **Hardware**: units shipped, ASP, attach rate
  - **Financial Services**: AUM, NIM, loan growth, fee income ratio
  - **Pharma/Biotech**: pipeline stage, patient starts, scripts, market share
  - **Industrials/Energy**: backlog, book-to-bill, utilization, production volumes

**Assess reinvestment adequacy:**
- Is R&D/revenue trending down while buybacks are increasing? This may indicate the company is funding shareholder returns by underinvesting in innovation.
- Is CapEx/revenue declining while the business requires sustained infrastructure investment (e.g., cloud, manufacturing, stores)?
- Are growth KPIs (subscriber adds, customer growth, same-store sales) deteriorating while capital returns are at record levels? This is a red flag — the company may be harvesting rather than growing.
- Compare R&D intensity and CapEx intensity vs peers (if available from /industry or /comps data). Is the company investing more or less than competitors?

**Value creation vs extraction verdict:**
- Net assessment: Is the company's capital allocation creating long-term value (reinvesting at high ROIC, buying back cheap stock, growing dividends sustainably) or extracting value (under-investing to fund buybacks at premium valuations, leveraging up for returns)?

## 7. Save Report
Save to `reports/{TICKER}_capital_allocation.html` using the HTML report template from `../design-system.md`. Write the full analysis as styled HTML with the design system CSS inlined. This is the final deliverable — no intermediate markdown step needed.

Structure the report with these sections:

```
<h1>{Company Name} ({TICKER}) — Capital Allocation Analysis</h1>
<p>Generated: {date}</p>

<h2>Summary</h2>
{2-3 sentences: How does this company deploy its capital? Key takeaways.}

<h2>Current Snapshot</h2>
<table>
| Metric | Value |
| Market Cap | $XXX |
| Trailing 4Q FCF | $XXX |
| FCF Yield | X.X% |
| Shareholder Yield | X.X% |
| Net Debt / EBITDA | X.Xx |
| Remaining Buyback Authorization | $XXX |
</table>

<h2>Cash Flow & FCF (8 Quarters)</h2>
<table>
| Metric | Q1 | Q2 | ... | Q8 |
{OCF, CapEx, FCF, FCF Margin % — with Daloopa citations}
</table>

<h2>Share Repurchases & Dividends (8 Quarters)</h2>
<table>
| Metric | Q1 | Q2 | ... | Q8 |
{Buyback $, Dividends $, Total Return, Share Count — with Daloopa citations}
</table>

<h2>Shareholder Yield Analysis</h2>
<table>
| Metric | Q1 | Q2 | ... | Q8 |
{Buyback Yield, Div Yield, Total Yield, FCF Payout Ratio}
</table>

<h2>Leverage & Balance Sheet (8 Quarters)</h2>
<table>
| Metric | Q1 | Q2 | ... | Q8 |
{Cash, Debt, Net Debt, Net Debt/EBITDA — with Daloopa citations}
</table>

<h2>Capital Allocation Framework</h2>
{Management's stated priorities from filings, with document citations}

<h2>Reinvestment Assessment</h2>
<table>
| Metric | Q1 | Q2 | ... | Q8 |
{R&D, R&D % Rev, CapEx, CapEx % Rev, key growth KPIs — with Daloopa citations}
</table>
{Analysis: Is the company adequately reinvesting? R&D/CapEx trends vs growth KPI trends. Value creation vs extraction verdict.}

<h2>Buyback Discipline Analysis</h2>
{Analysis of buyback timing vs price, share count reduction trend, authorization remaining}

<h2>M&A Activity</h2>
{Any acquisitions from filings, deal sizes, strategic rationale}

<h2>Key Observations</h2>
<ul>{3-5 bullet points on capital allocation quality, trends, and implications}</ul>
```

All financial figures must use Daloopa citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved.

Highlight the key capital allocation story (e.g., "AAPL returned $XX billion to shareholders over the last year, a X.X% shareholder yield, with buybacks accelerating").
