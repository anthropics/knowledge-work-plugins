---
name: earnings-prep
description: Pre-earnings preparation report for the night before a company reports
argument-hint: TICKER
---

Generate a pre-earnings preparation report for the company specified by the user: $ARGUMENTS

This is the note a L/S equity analyst reads the night before a company reports — it tells them exactly what to focus on when the print drops.

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

Follow these steps:

## 1. Company Lookup
Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations below (see `../data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5

Determine the **upcoming quarter** — the one AFTER `latest_calendar_quarter`. This is the quarter the company is about to report. All analysis is oriented around preparing the analyst for this print.

## 2. Last Quarter Recap
Pull the most recent quarter's full financials from Daloopa. Calculate 4 quarters backward from `latest_calendar_quarter` (for YoY context).

**Pull:**
- Revenue, Gross Profit, Operating Income, EBITDA, Net Income, Diluted EPS
- Operating Cash Flow, CapEx, FCF (calc.)
- Segment/product revenue breakdown
- Company-specific KPIs (use the business-model taxonomy: SaaS → ARR/NRR/RPO; Consumer → DAU/ARPU; E-commerce → GMV/take rate; etc.)

**Summarize the story of last quarter in 3-5 bullets:**
- What beat expectations (guidance or consensus)?
- What missed or disappointed?
- What was the stock reaction? (use WebSearch: `"{TICKER} earnings reaction {latest_quarter_label} {year}"`)
- What narrative emerged from the call? (e.g., "AI monetization acceleration," "margin expansion story intact," "consumer weakness")
- What was the single most debated metric?

This is the baseline everyone on the upcoming call will be anchoring to.

## 3. Outstanding Guidance for Upcoming Quarter
Search for ALL guidance series using keywords: "guidance", "outlook", "estimate", "forecast", "target". Apply the +1 quarter offset to identify which guidance applies to the upcoming print:
- CRITICAL: Guidance from Q(N) earnings call applies to Q(N+1) results
- The guidance issued during the `latest_calendar_quarter` earnings call is what applies to the upcoming quarter

**Pull and present:**
- Revenue guidance (point estimate or range)
- EPS guidance
- Margin guidance (gross, operating, EBITDA)
- CapEx guidance
- Segment-level guidance (if available)
- KPI guidance (subscriber adds, unit volumes, ARPU targets, etc.)

**Search filings for directional/qualitative guidance:**
- Search documents for: "expect", "anticipate", "similar to", "consistent with"
- Search documents for: "low single digit", "mid single digit", "double digit", "sequential"
- Search documents for: "headwind", "tailwind", "conservatively", "assumes"
- Capture exact management quotes with document citations

**Flag any guidance updates between quarters:**
- Search for "pre-announce", "update", "revise" in the most recent quarter's filings
- Check if the company issued an 8-K updating guidance after the last earnings call

Present all guidance in a single table: Metric | Guidance Value | Source Quarter | Type (Quantitative/Directional).

## 4. Guidance Credibility & Whisper Number
This section MUST be built entirely from Daloopa data — guidance series AND actual result series pulled via `get_company_fundamentals`. Do not use web search or estimates for this analysis.

**Step 1: Pull 8 quarters of guidance data.**
You already discovered guidance series in Section 3. Now pull ALL of those guidance series for the last 8 quarters (from `latest_calendar_quarter` backward). These are the guidance values management provided each quarter.

**Step 2: Pull 8 quarters of corresponding actuals.**
For every guided metric, identify the corresponding actual result series (e.g., if there is a "Revenue guidance" series, pull the actual "Revenue" series). Pull these actuals for the same 8-quarter period.

**Step 3: Build the complete beat/miss table.**
Apply the +1 quarter offset: guidance from Q(N) is compared to the actual result in Q(N+1). For EVERY quarter where both a guidance value and a corresponding actual exist, compute:
- Guidance value (midpoint if range)
- Actual value
- Delta (Actual - Guidance midpoint)
- Beat/Miss % ((Actual - Guidance midpoint) / |Guidance midpoint| × 100)
- Classification: Beat / In-line / Miss (use +/-1% threshold for in-line)

**Present a FULL detail table — every quarter, every guided metric.** This is the core analytical engine of the whisper number. Do not summarize or abbreviate — show all rows. Format:

| Guidance Source Qtr | Metric | Guidance (Mid) | Actual Qtr | Actual | Delta | Beat/Miss % |

If a company provides range guidance (low/high), show the midpoint and note the range width. If a company only provides directional guidance for some metrics (e.g., "revenue growth in low teens"), convert to an implied numeric value for comparison (e.g., 12-13% → midpoint ~12.5% applied to prior year actual).

**Step 4: Compute summary statistics from the detail table:**
- Beat rate per metric (% of quarters where actual > guidance midpoint)
- Average beat magnitude per metric (in absolute terms and %)
- Beat pattern trend: is the beat getting larger (sandbagging increasing), shrinking (guidance getting more accurate), or volatile? Look at the last 4 vs. prior 4.
- Range width trend: is management tightening or widening guidance ranges?

**Step 5: Calculate the implied "whisper number":**
- Whisper = Current guidance midpoint + Average historical beat (from the detail table above)
- This is the REAL bar the stock is trading against, not the stated guidance
- If the company beats by 2% on average, the market expects a 2% beat — an in-line result to guidance is effectively a miss
- Calculate whisper for EVERY guided metric, not just revenue

**Present the whisper summary:**
| Metric | Current Guidance (Mid) | Avg Historical Beat | Implied Whisper | Beat Rate (n/N) |

**Credibility verdict:** Is management's guidance informative (tight, accurate) or performative (always sandbagged, uninformative)? If the beat rate is >90%, say so — it means the guidance number is a floor, not a forecast. If the beat magnitude is increasing, management is becoming MORE conservative over time.

## 5. Peer & Adjacent Company Read-Throughs
This is the most differentiated section. For companies in the same sector that have ALREADY reported this earnings season, their results contain direct signal about the upcoming print.

**Identify the read-through universe (aim for 5-8 companies):**
- **Competitors**: Direct rivals in the same market
- **Suppliers**: Companies that sell to the target company
- **Customers**: Companies that buy from the target company
- **Industry bellwethers**: Large companies whose results signal sector trends

**CRITICAL: Always use Daloopa as the primary data source for peer analysis.** For each peer:

1. **Look up the peer in Daloopa:** `discover_companies` with the peer's ticker. If Daloopa has the company, check `latest_calendar_quarter` to determine whether they have already reported the relevant quarter.
2. **If the peer has data for the current earnings season quarter:** Pull their financials from Daloopa (`discover_company_series` → `get_company_fundamentals`). Focus on 2-4 metrics most relevant to the read-through (e.g., for a supplier: revenue, segment breakdown, inventory; for a competitor: revenue growth, market share proxies, pricing commentary).
3. **Search the peer's filings in Daloopa:** `search_documents` with keywords related to the target company's products, markets, or industry (e.g., for an Apple supplier, search for "Apple", "smartphone", "consumer electronics").
4. **Use WebSearch only to supplement Daloopa data** — for earnings-season timing confirmation, stock price reactions, or analyst commentary that Daloopa filings don't cover.

**For each read-through, extract (with Daloopa citations):**
1. **The specific data point** — the peer's metric that creates signal. Cite the Daloopa `fundamental_id`.
2. **The implication** — bullish or bearish for the target company, and why
3. **Confidence level** — High (direct disclosed relationship), Moderate (inferred from industry), Low (circumstantial)

**For peers that haven't reported yet:** Note them as "reports after {TICKER}" — their results will be a read-through in the opposite direction.

**Group read-throughs by:**
- **Competitors** — share shift signals, pricing environment, demand trends
- **Suppliers** — order book signals, inventory levels, capacity commentary
- **Customers** — demand signals, inventory destocking/restocking, spending priorities
- **Industry Bellwethers** — macro/sector health, end-market demand

**Web research for sector context (supplementary only — after Daloopa pulls):**
- Search: `"{TICKER} sector earnings season {year} read through"` — analyst commentary on cross-company signals
- Search: `"{TICKER} competitors results {upcoming_quarter_label} {year}"` — what peers have already signaled

## 6. Key Metrics to Watch
Identify the 5-7 metrics the analyst should focus on when the print drops. For each metric:

| Metric | Current Level | Guidance/Expected | Bullish Threshold | Bearish Threshold | Why It Matters |

**Be specific with thresholds** — not "revenue growth" but "revenue above $95B signals iPhone cycle acceleration; below $92B confirms China weakness." Not "margins" but "gross margin above 47% confirms services mix shift; below 45% signals hardware pricing pressure."

**Prioritize by information value:**
1. Metrics where guidance has been vague or directional (highest uncertainty)
2. Metrics where peer read-throughs are conflicting (the print will resolve the debate)
3. Metrics that drive the forward multiple (the ones the market will re-rate on)
4. KPIs that lead revenue by 1-2 quarters (predictive of next quarter's financials)

## 7. Consensus & Positioning
Gather available consensus context:

**From data sources (consensus estimates if available per ../data-access.md Section 3):**
- Consensus revenue and EPS for the upcoming quarter
- Number of analysts at Buy / Hold / Sell
- Consensus price target (median and range)
- Recent estimate revision trends (last 30/60/90 days — moving up or down?)

**From web search (supplement or replace if consensus data unavailable):**
- Search: `"{TICKER} earnings preview consensus estimates {upcoming_quarter_label} {year}"` — sell-side previews
- Search: `"{TICKER} analyst expectations {year}"` — positioning and sentiment

**Note limitations** if consensus data is not directly available. Even directional context ("estimates have been revised up 3% over the last 90 days") is valuable.

## 8. Historical Earnings Reaction
Use web search to find how the stock has reacted to the last 4-6 earnings prints:
- Search: `"{TICKER} earnings stock reaction history {year}"` — post-earnings moves
- Search: `"{TICKER} options implied move earnings {upcoming_quarter_label}"` — current implied volatility

**Present as a table:**
| Quarter | Revenue Beat/Miss | EPS Beat/Miss | Next-Day Move | Notes |

**Pattern identification:**
- Does the stock tend to sell off on beats? (buy-the-rumor, sell-the-news pattern)
- Does it rally on in-line results? (low expectations already embedded)
- Is there a pattern of post-earnings drift (continued move in the days after)?
- What's the current implied move from the options market? If it's elevated vs. history, the market expects a big move.

## 9. Macro & Sector Backdrop
Web search for developments since last quarter that could affect results:
- Search: `"{TICKER} {industry} outlook {current_year}"` — sector developments
- Search: `"{TICKER} headwinds tailwinds {current_year}"` — company-specific macro factors

**Distill into 5-8 bullets, each with a directional tag (Positive / Negative / Uncertain):**
- Industry-specific: new regulations, competitor product launches, market share shifts
- Macro: FX moves (specify currencies and direction), commodity prices, interest rates
- Policy: tariffs, trade restrictions, tax changes
- Channel: inventory levels in the channel, distributor commentary, supply chain status
- Company-specific: product launches since last quarter, management changes, M&A

Keep each bullet to one sentence. The analyst needs context, not a macro essay.

## 10. Potential Surprises & Call Catalysts
Beyond the numbers, what could management announce that would move the stock? Search filings and news for signals:
- Search documents: "restructuring", "acquisition", "buyback", "dividend" in recent filings
- Search: `"{TICKER} potential announcement catalyst {year}"` — speculative but grounded

**Categories:**
- **Capital allocation**: New buyback authorization, dividend change (hike/cut/initiation), M&A announcement, asset sale/spinoff
- **Operational**: Restructuring/layoffs, new product launch, partnership/contract win, segment reporting changes
- **Strategic**: New guidance metrics, long-term targets update, management changes, investor day announcement
- **Accounting/Disclosure**: Guidance methodology change, segment redefinition, one-time charge pre-announcement

For each potential surprise, note the signal strength (rumored / speculated / no signal) and the likely stock impact direction.

## 11. Pre-Earnings Checklist
A concise, actionable summary that fits on a single card. This is what the analyst tapes to their monitor:

**The Numbers:**
- Revenue whisper: $X.XX (guidance: $X.XX, avg beat: +X.X%)
- EPS whisper: $X.XX (guidance: $X.XX, avg beat: +X.X%)

**Top 3 Metrics to Watch:**
1. [Metric] — current: X, bull: >Y, bear: <Z
2. [Metric] — current: X, bull: >Y, bear: <Z
3. [Metric] — current: X, bull: >Y, bear: <Z

**The Bull Catalyst:** What would make this stock go up 5%+ after the print? (one sentence)

**The Bear Risk:** What would make this stock go down 5%+ after the print? (one sentence)

**Read-Through Signal:** After this company reports, what does it mean for [2-3 other names]?

**Historical Pattern:** Last 4 prints averaged +/-X% next-day move; options imply +/-X% this time.

## 12. Save Report
Save to `reports/{TICKER}_earnings_prep_{UPCOMING_CQ}.html` (e.g., `AAPL_earnings_prep_2026Q1.html`) using the HTML report template from `../design-system.md`. The period in the filename is the **upcoming calendar quarter** being prepped for — the one AFTER `latest_calendar_quarter`. Write the full analysis as styled HTML with the design system CSS inlined. This is the final deliverable — no intermediate markdown step needed.

The report should include:
- Executive summary (2-3 sentences: what quarter is coming, what the key debate is, what the whisper number implies)
- Last quarter recap (story + key metrics table)
- Outstanding guidance table with source citations
- Whisper number calculation with historical beat/miss detail table
- Peer read-throughs (grouped by Competitors / Suppliers / Customers / Industry, with Daloopa citations on peer data)
- Key metrics to watch (table with specific thresholds)
- Consensus & positioning summary
- Historical earnings reaction table
- Macro & sector backdrop (bulleted list with directional tags)
- Potential surprises & call catalysts
- Pre-earnings checklist (prominently styled — this is the payoff of the whole report)

All financial figures must use Daloopa citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved.

Highlight what makes this print particularly interesting: Is the whisper number meaningfully above guidance (setting up for disappointment even on a beat)? Are peer read-throughs conflicting (creating genuine uncertainty)? Is there a potential surprise catalyst that could overshadow the numbers? Give the analyst the single most important thing to watch.
