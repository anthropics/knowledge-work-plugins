---
name: comps
description: Trading comparables analysis with peer multiples and implied valuation
argument-hint: TICKER
---

Build a trading comparables analysis for the company specified by the user: $ARGUMENTS

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

Follow these steps:

## 1. Company Lookup
Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations below (see `../data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5

## 2. Identify Peer Group
Based on the company's business model, sector, size, and competitive landscape, identify 5-10 comparable companies. Consider:
- **Direct competitors** in the same market
- **Business model peers** (similar revenue model even if different sector)
- **Size peers** (similar market cap range)
- **Growth profile peers** (similar growth rate)

Prioritize relevance over size matching. A direct competitor at a different scale is more useful than a similar-sized company in a different industry.

List the peer tickers and briefly justify each selection (1 sentence).

## 3. Target Company Fundamentals
Calculate 4 quarters backward from `latest_calendar_quarter`. Pull from Daloopa for the target company:
- Revenue (compute trailing 4Q total)
- EBITDA (compute trailing 4Q; if not available, use Op Income + D&A, label "(calc.)")
- Net Income (trailing 4Q)
- Diluted EPS (trailing 4Q sum)
- Free Cash Flow (trailing 4Q; compute as OCF - CapEx, label "(calc.)")
- Revenue YoY growth (most recent quarter)
- Operating Margin (most recent quarter)
- Net Margin (most recent quarter)

## 4. Peer Market Multiples
For each peer, get trading multiples and current quote (see ../data-access.md Section 2):
- P/E (trailing and forward), EV/EBITDA, P/S, P/B, dividend yield, PEG ratio
- Price, market cap, enterprise value

If market data is unavailable, note that peer multiples cannot be sourced and provide a framework for manual completion.

If a peer ticker fails (delisted, no data), drop it and note why.

## 5. Peer Fundamentals from Daloopa
For each peer that is available in Daloopa:
- Look up the company
- Calculate 4 quarters backward from `latest_calendar_quarter`. Pull revenue, operating income, net income for those periods.
- Compute revenue growth YoY, operating margin, net margin

For peers not in Daloopa, rely on market data multiples only (see ../data-access.md Section 2) and note the data source limitation.

## 5.5. Peer Operational KPIs

For each company (target + all peers available in Daloopa), discover and pull company-specific operational KPIs. Use the sector taxonomy below to know what to search for:

- **SaaS/Cloud**: ARR, net revenue retention, RPO/cRPO, customers >$100K, cloud gross margin
- **Consumer Tech**: DAU/MAU, ARPU, engagement metrics, installed base, paid subscribers
- **E-commerce/Marketplace**: GMV, take rate, active buyers/sellers, order frequency
- **Retail**: same-store sales, store count, average ticket, transactions
- **Telecom/Media**: subscribers, churn, ARPU, content spend
- **Hardware**: units shipped, ASP, attach rate, installed base
- **Financial Services**: AUM, NIM, loan growth, credit quality metrics, fee income ratio
- **Pharma/Biotech**: pipeline stage, patient starts, scripts, market share
- **Industrials/Energy**: backlog, book-to-bill, utilization, production volumes, reserves

Pull the same 4 calendar quarters for each peer. Not all peers will have the same KPIs — build a sparse matrix and note which are comparable across the group vs company-specific.

Add KPI columns to the comps table in Section 6 where comparable metrics exist (e.g., subscriber growth, ARPU, units alongside P/E and EV/EBITDA). This shows whether valuation premiums are supported by operational outperformance.

## 6. Build Comps Table
Create the main comparables table with these columns:
| Company | Ticker | Mkt Cap | EV | P/E | Fwd P/E | EV/EBITDA | P/S | Rev Growth | Op Margin | Net Margin | FCF Yield |

Sort by market cap descending. Include:
- **Peer median** row
- **Peer mean** row
- **Target company** row (highlighted / separated)
- Target's percentile rank within the peer group for each metric

## 7. Implied Valuation
Apply peer group median and mean multiples to the target's fundamentals:

| Methodology | Peer Median Multiple | Target Metric | Implied Value |
|---|---|---|---|
| P/E | XX.Xx | $X.XX EPS | $XXX |
| EV/EBITDA | XX.Xx | $XXX EBITDA | $XXX |
| P/S | XX.Xx | $XXX Revenue | $XXX |
| FCF Yield | X.X% | $XXX FCF | $XXX |

For each:
- Implied Enterprise Value = Multiple × Target's Metric
- Implied Equity Value = EV - Net Debt (for EV-based multiples) or direct (for equity multiples)
- Implied Share Price = Equity Value / Shares Outstanding

Compute range (min to max implied price) and central tendency.

## 8. Consensus Forward Estimates (if available)
If consensus estimates are available (see ../data-access.md Section 3):
- Add NTM (next twelve months) revenue and EPS estimates for target and each peer
- Compute forward P/E and forward EV/EBITDA using consensus NTM estimates
- Note where the target's forward multiples sit vs the peer group
- Flag any peers with significant estimate revision trends

If consensus data is not available, use trailing multiples only and note the limitation.

## 9. Premium/Discount Analysis
Assess whether the target trades at a premium or discount to peers:
- For each multiple, show target vs peer median as a % premium/discount
- Consider whether a premium/discount is justified based on:
  - Growth differential (higher growth = deserves premium)
  - Margin differential (higher margins = deserves premium)
  - Market position (leader vs challenger)
  - Risk profile

**Be honest about whether the premium is truly justified:**
- A company can deserve a premium and still be overvalued if the premium has stretched too far beyond fundamentals. Quantify: how much growth differential is needed to justify the current premium? Is the company delivering that?
- If the stock trades at a significant premium but growth is decelerating toward peer levels, flag the derating risk explicitly.
- Don't default to "premium is justified because it's the market leader" — that's already in the price. What justifies the premium *expanding* or *sustaining* from here?
- **Reference KPI outperformance as justification (or lack thereof).** Example: "AAPL trades at 34x P/E vs peer median 28x — premium partly justified by +14% Services growth vs peer median +8%, but Wearables decline (-2.2% YoY) is a drag peers don't have." If the target's KPIs are in line with or worse than peers, the premium is harder to defend.

## 10. Save Report
Save to `reports/{TICKER}_comps.html` using the HTML report template from `../design-system.md`. Write the full analysis as styled HTML with the design system CSS inlined. This is the final deliverable — no intermediate markdown step needed.

Structure the report with these sections:

```
<h1>{Company Name} ({TICKER}) — Comparable Companies Analysis</h1>
<p>Generated: {date}</p>

<h2>Summary</h2>
{2-3 sentences: Where does the company trade relative to peers? Is it cheap or expensive and why?}

<h2>Peer Group Selection</h2>
<table>
| Peer | Ticker | Rationale |
{table with justification for each peer}
</table>

<h2>Comparables Table</h2>
<table>
| Company | Ticker | Mkt Cap | P/E | Fwd P/E | EV/EBITDA | P/S | Rev Growth | Op Margin |
{full comps table with target highlighted}
| **Peer Median** | | | XX.Xx | XX.Xx | XX.Xx | XX.Xx | X.X% | X.X% |
| **Peer Mean** | | | XX.Xx | XX.Xx | XX.Xx | XX.Xx | X.X% | X.X% |
| **{TICKER}** | | | **XX.Xx** | **XX.Xx** | **XX.Xx** | **XX.Xx** | **X.X%** | **X.X%** |
</table>

<h2>Target vs Peer Premium/Discount</h2>
<table>
| Multiple | Target | Peer Median | Premium/Discount |
{table showing where target is rich/cheap}
</table>

<h2>Implied Valuation</h2>
<table>
| Methodology | Multiple | Target Metric | Implied Price | vs Current |
{table with implied values}
</table>

<table>
| **Valuation Range** | **Low** | **Median** | **High** |
| Implied Price | $XXX | $XXX | $XXX |
| vs Current Price | -X% | +X% | +X% |
</table>

<h2>Premium/Discount Justification</h2>
{Analysis of whether current premium/discount is warranted}

<h2>Peer Operational KPIs</h2>
<table>
| KPI | {TICKER} | Peer 1 | Peer 2 | ... | Peer Median |
{KPI comparison table — sparse where data unavailable, footnoted}
</table>

<h2>Key Observations</h2>
<ul>{3-5 bullet points on relative valuation, standout metrics, peer group dynamics, KPI differentiation}</ul>
```

All financial figures from Daloopa must use citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved.

Highlight: where the stock trades relative to peers (premium/discount), the implied valuation range, and the most relevant multiple for this company.
