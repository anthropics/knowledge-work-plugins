---
name: guidance-tracker
description: Track management guidance accuracy over time for a given company
argument-hint: TICKER
---

Track management guidance accuracy for the company specified by the user: $ARGUMENTS

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

Follow these steps:

## 1. Company Lookup
Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations below (see `../data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5

## 2. Discover Guidance Series
Search for series with keywords like "guidance", "outlook", "estimate", "forecast", "target" to find all available guidance metrics. Common guidance series include:

**Financial guidance:**
- Revenue guidance (quarterly and/or annual)
- EPS guidance
- Operating income / margin guidance
- EBITDA guidance
- Segment-level revenue guidance
- CapEx guidance
- Free Cash Flow guidance

**Operational KPI guidance** — many companies guide on KPIs, and tracking these beats/misses is often more informative than financial guidance:
- Subscriber / user count guidance (e.g., "we expect to add X million subscribers")
- Unit shipment guidance (e.g., "iPhone units", "deliveries")
- ARPU / ASP guidance
- Same-store sales guidance
- GMV / bookings guidance
- Net revenue retention guidance
- Store openings / closings guidance
- Production volume / capacity guidance

Search explicitly for KPI-specific guidance series using terms like "subscriber guidance", "unit guidance", "ARPU guidance", "same-store sales outlook", "deliveries forecast", "bookings target". These are separate from financial guidance and often reside in different series.

## 3. Pull Guidance Data
Calculate 8+ quarters backward from `latest_calendar_quarter`. Pull all discovered guidance series for those periods.

## 4. Pull Actual Results
For each guidance metric, pull the corresponding actual result series for the same periods.

## 5. Build Guidance vs Actuals Tracker
CRITICAL OFFSET RULES:
- **Quarterly guidance**: Guidance from Q(N) earnings call applies to Q(N+1) results. Compare Q(N) guidance -> Q(N+1) actual.
- **Annual guidance from Q1/Q2/Q3**: Applies to current fiscal year. Compare to FY actual.
- **Annual guidance from Q4**: Applies to NEXT fiscal year. Compare to next FY actual.

For each guidance-actual pair, calculate:
- Guidance value
- Actual value
- Delta (Actual - Guidance)
- Beat/Miss % ((Actual - Guidance) / |Guidance| x 100)
- Classification: Beat / In-line / Miss (use +/-1% threshold for in-line)

## 6. Pattern Analysis
Analyze the guidance track record:
- Overall beat rate (% of quarters where actual > guidance)
- Average beat/miss magnitude
- Trend in guidance accuracy (getting tighter? more conservative? less reliable?)
- Any metrics where management is notably conservative or aggressive
- Guidance range width trends (if range guidance is given)

**Management credibility assessment:**
- If the company consistently beats by a similar margin, call out sandbagging — this suggests management is deliberately setting low bars, which can mask underlying deceleration. A 100% beat rate is not necessarily bullish; it may mean guidance is uninformative.
- If guidance has been cut or missed, assess whether management acknowledged the miss honestly or buried it in adjusted metrics.
- Flag any pattern where qualitative language ("strong demand," "robust pipeline") didn't translate to actual results.

## 7. Commentary from Filings
Search SEC filings/documents across multiple queries to build a complete picture of guidance practices. If any search returns empty, try alternative keywords before giving up.

- **Explicit guidance language**: Try "guidance", "outlook"; fallback to "expect", "anticipate", "forecast"
- **Qualitative / directional guidance**: Try "similar to", "consistent with", "growth rate"; fallback to "low single digit", "mid single digit", "high single digit", "double digit", "sequential"
  - Many companies provide directional revenue guidance on earnings calls (e.g., "similar to the March quarter" or "low-to-mid-single-digit growth") rather than numeric ranges. Capture these and compare against actual growth rates.
- **Guidance methodology changes**: Try "change", "methodology", "no longer providing"; fallback to "withdraw", "suspend", "discontinue"
  - Flag any quarters where the company changed what metrics it guides on, or withdrew guidance entirely
- **Key drivers behind guidance**: Try "assumes", "includes", "excludes"; fallback to "headwind", "tailwind", "impact"
  - Capture what management said about the assumptions underpinning their guidance (e.g., FX assumptions, macro assumptions, one-time items included/excluded)

Extract direct management quotes where available and cite the document source.

## 7.5. Guidance Read-Throughs to Adjacent Companies

When a company raises, cuts, or materially changes its guidance, the implications often matter more for adjacent names than for the company itself. This section translates guidance signals into actionable read-throughs.

**For each major guidance change identified in the tracker, analyze the implications for adjacent companies:**

**Identify who is affected by this company's guidance:**
- **Suppliers**: Revenue/CapEx guidance changes directly affect supplier order books. A CapEx guidance raise is a near-term purchase order for equipment/component suppliers. A revenue guide-down signals softer demand flowing upstream.
- **Customers**: If this company supplies critical inputs, pricing or capacity guidance affects customer margins. Guiding for price increases = margin headwind for customers. Guiding for capacity expansion = supply relief.
- **Competitors**: Guidance on market growth, pricing environment, or demand trends is often the most honest signal about the competitive landscape. If Company A guides for share gains, that's a direct share loss for Company B.
- **Channel partners / distributors**: Volume guidance changes affect channel inventory and distributor revenue.

**For each read-through (aim for 4-6), state:**
1. **The guidance data point** — which metric changed, by how much, and in which quarter's call
2. **The affected company** (ticker + name)
3. **The implication** — bullish or bearish, with specific logic
4. **Timing** — is this a next-quarter impact or a multi-quarter trend?

**Focus on the highest-signal guidance changes:**
- Guidance raises after a period of conservatism → strong signal that the underlying business is inflecting
- Guidance cuts or "reaffirmed" when the market expected a raise → often more bearish than an explicit cut
- New metrics being guided on (or old metrics withdrawn) → management is redirecting attention, which itself is a signal
- Segment-level guidance changes → more specific read-throughs than consolidated figures
- KPI guidance (subscriber adds, unit volumes, ARPU) → often the most direct read-through to suppliers and competitors

**Example:**
- "NFLX raised Q2 subscriber guidance from +5M to +8M → **Negative for DIS+, WBD**: attention economy is zero-sum; NFLX's accelerating growth likely pressures competing streamers' subscriber adds. **Positive for cloud/CDN names (AMZN/AWS, NET)**: more streaming = more infrastructure demand."
- "TSMC raised full-year CapEx guidance by $4B (from $32B to $36B) → **Positive for ASML**: TSMC is ASML's largest customer; incremental CapEx skews toward EUV tools. **Positive for AMAT, LRCX, KLAC**: broader equipment spend benefits all semicap names."

**Web research for validation:**
Run 1 targeted search: `"{TICKER} guidance change implications read through {year}"` — analyst commentary on cross-company signals from guidance moves.

Present as a structured section in the report after the Pattern Analysis, grouped by guidance change (each major guide raise/cut gets its own sub-block with the read-throughs beneath it).

## 8. Save Report
Save to `reports/{TICKER}_guidance_tracker.html` using the HTML report template from `../design-system.md`. Write the full analysis as styled HTML with the design system CSS inlined. This is the final deliverable — no intermediate markdown step needed.

The report should include:
- Summary header with company name, ticker, and period covered
- Quarter mapping reference table showing the +1 offset explicitly:
  ```
  | Guidance Source Quarter | Guidance Applies To | Actual Result Quarter |
  | CQ1 2024               | CQ2 2024            | CQ2 2024              |
  | CQ2 2024               | CQ3 2024            | CQ3 2024              |
  ```
  This makes the offset rule visible and auditable for every row in the tracker.
- Main tracker table with columns: Guidance Source, Metric, Guidance, Actual Period, Actual, Delta, Beat/Miss (with Daloopa citations on all values)
- Summary statistics (beat rate, avg beat/miss by metric)
- Pattern analysis narrative
- Guidance read-throughs to adjacent companies (grouped by guidance change, with affected tickers and implications)
- Key guidance quotes from filings with document citations

All financial figures must use Daloopa citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved.

Highlight the key patterns (e.g., "Management has beat revenue guidance 7 of the last 8 quarters by an average of 2.3%"). Include an honest credibility verdict: Is management's guidance informative or performative? Should investors trust the forward guidance, and if not, what should they anchor to instead?
