---
name: tearsheet
description: Quick one-page company overview and snapshot
argument-hint: TICKER
---

Generate a concise company tearsheet for the company specified by the user: $ARGUMENTS

This should be a quick, one-page overview — the kind of snapshot an analyst pulls up before a meeting.

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

Follow these steps:

## 1. Company Lookup
Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations below (see `../data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5

## 2. Key Financials
Calculate periods backward from `latest_calendar_quarter` (8 quarters total: last 4 + year-ago for each to enable YoY):
Pull:
- Revenue
- Gross Profit
- Operating Income
- EBITDA (if not reported, compute as Operating Income + D&A — label it "EBITDA (calc.)" in the report)
- Net Income
- Diluted EPS
- Operating Cash Flow
- CapEx (Purchases of property, plant and equipment)
- Free Cash Flow (compute as Operating Cash Flow - CapEx — label it "FCF (calc.)" in the report)

For any derived/computed metric, mark it with "(calc.)" so the reader knows it's not directly sourced.

## 3. Key Operating KPIs
This section is strictly for **business-driver metrics** — the operational numbers that actually move revenue and earnings. Do NOT put financial statement items (D&A, share count, buybacks, dividends) here — those belong in the financials or capital return sections.

First, think about what the most important KPIs are for THIS specific company based on its business model and what drives its valuation. For example:
- **SaaS/cloud**: ARR, net revenue retention, RPO/cRPO, customers >$100K, cloud gross margin
- **Consumer tech**: DAU/MAU, ARPU, engagement metrics, installed base, paid subscribers
- **E-commerce/marketplace**: GMV, take rate, active buyers/sellers, order frequency
- **Retail**: same-store sales, store count, average ticket, transactions
- **Telecom/media**: subscribers, churn, ARPU, content spend
- **Hardware**: units shipped, ASP, attach rate, installed base, products vs services gross margin split
- **Financial services**: AUM, NIM, loan growth, credit quality metrics
- **Pharma/biotech**: pipeline stage, patient starts, scripts, market share
- **Industrials/energy**: backlog, book-to-bill, utilization, production volumes

Then search for those specific KPIs by name, plus cast a wider net for anything else Daloopa has. Also search for:
- Segment/product revenue breakdown
- Geographic revenue breakdown

**If the company discloses few operational KPIs** (e.g., Apple stopped reporting iPhone units in 2019), acknowledge the disclosure gap explicitly rather than padding the section with financial metrics. A short note like "Apple does not disclose unit volumes or ASPs; segment revenue is the finest granularity available" is more informative than showing D&A and buybacks as fake KPIs.

**Always search broadly** — companies often disclose more KPIs than you'd expect. For Apple, beyond segment revenue, Daloopa also has: installed base active devices (~2.5bn), products gross margin vs services gross margin (the mix shift story), and paid subscriptions. These are real operational metrics. Search with keywords like "installed", "active", "subscriber", "margin" by segment, not just the obvious financial terms.

Pull for the same period as financials.

## 3b. Capital Return
Pull share count, share repurchases, and dividends paid for the same periods. This is a separate section from operating KPIs — it shows how the company is returning cash to shareholders.

## 4. Compute Key Ratios
Show trend over the last 4 quarters with YoY change for EACH quarter (not just the earliest):
- Gross Margin %
- Operating Margin %
- EBITDA Margin %
- Net Margin %
- Revenue Growth (YoY)
- EPS Growth (YoY)

If the company has strong seasonality (e.g., retail Q4, back-to-school, etc.), add a brief note flagging it so YoY comparisons are read in context rather than sequential QoQ.

## 5. Recent Developments
Search the most recent 2 quarters of filings. Try multiple keyword searches to get coverage:
- First search: company name + "results" or "record" for earnings highlights
- Second search: "outlook" or "guidance" or "expect" for forward-looking commentary
- Third search: strategy-specific terms relevant to the company (e.g., "AI", "cloud", "subscribers", "margin")
- If a search returns empty, try broader single-keyword searches before giving up

Extract:
- Business description / what the company does (2-3 sentences)
- Key recent developments or announcements
- Management's top priorities or strategic focus areas
- Any notable management quotes (with document citations)
Keep this brief — 3-5 bullet points max.

## 6. Five Key Tensions
Identify the 5 most critical bull/bear debates for this stock. Each tension is a single line that frames both sides. Alternate between bullish-leaning and bearish-leaning tensions. Every tension must reference a specific data point from the analysis above.

Format as a numbered list:
1. "[Bullish factor] vs [Bearish factor]" — cite the specific metric
2. "[Bearish factor] vs [Bullish factor]" — cite the specific metric
...etc.

This goes at the top of the report, right after the Company Overview — it gives the reader the bull/bear framing before they dive into the data.

## 7. News Snapshot
Run 2 WebSearch queries to gather recent context:
1. `"{TICKER} {company_name} news {current_year}"` — recent headlines
2. `"{TICKER} catalysts risks {current_year}"` — forward-looking events

Distill into **3-5 key events** from the last 6 months, reverse chronological. Each event: date, one-line headline, sentiment tag (Positive / Negative / Mixed / Upcoming). Keep it tight — this is a tearsheet, not a research note.

## 8. What to Watch
Build a **Quantitative Monitors** list — 5 metrics with explicit thresholds:
- Format: "Metric: current value → bull threshold / bear threshold"
- Example: "Gross Margin: 45.2% → above 46% confirms pricing power / below 43% signals cost pressure"

Choose the 5 metrics that matter most for THIS company's thesis based on the data you pulled above. These should be actionable — an analyst should be able to check these next quarter and know whether the thesis is intact.

## 9. Save Report
Save to `reports/{TICKER}_tearsheet.html` using the HTML report template from `../design-system.md`. Write the full analysis as styled HTML with the design system CSS inlined. This is the final deliverable — no intermediate markdown step needed.

Structure the report with these sections:

```
<h1>{Company Name} ({TICKER}) — Tearsheet</h1>
<p>Generated: {date}</p>

<h2>Company Overview</h2>
{2-3 sentence description from filings}

<h2>Five Key Tensions</h2>
{numbered list of 5 bull/bear debates with data citations}

<h2>Key Financials (Last 4 Quarters)</h2>
<table>
| Metric | Q(oldest) | Q | Q | Q(latest) |
{table with Daloopa citations; derived metrics marked (calc.)}
</table>

<h2>Segment / Geographic Breakdown</h2>
{segment revenue table or geographic revenue table, whichever is more relevant}

<h2>Key Operating KPIs</h2>
<table>
| KPI | Q(oldest) | Q | Q | Q(latest) |
{table with Daloopa citations — ONLY business-driver metrics, NOT financial items}
{if few KPIs available, note the disclosure gap}
</table>

<h2>Capital Return</h2>
<table>
| Metric | Q(oldest) | Q | Q | Q(latest) |
{share count, buybacks, dividends — separate from operating KPIs}
</table>

<h2>Margins & Growth</h2>
<table>
| Metric | Q(oldest) | Q | Q | Q(latest) |
| Gross Margin % | X% | X% | X% | X% |
| ... | ... | ... | ... | ... |
| Rev Growth YoY | X% | X% | X% | X% |
| EPS Growth YoY | X% | X% | X% | X% |
{each cell shows the YoY change for THAT quarter}
{note on seasonality if applicable}
</table>

<h2>Recent Developments</h2>
<ul>{bullet points from filings with document citations}</ul>

<h2>News Snapshot</h2>
{3-5 recent events with date, headline, sentiment tag}

<h2>What to Watch</h2>
{5 quantitative monitors with current value and bull/bear thresholds}
```

All financial figures must use Daloopa citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved.

Give a 2-3 sentence summary of the company's current state, including an honest assessment: What is the single biggest risk or concern? Does the current valuation (price, implied multiples) seem warranted given the growth trajectory? What would make you cautious about owning this stock?
