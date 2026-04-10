---
name: working-capital
description: Cash conversion cycle, earnings quality, and working capital deep-dive
argument-hint: TICKER
---

Perform a cash conversion cycle, earnings quality, and working capital deep-dive for the company specified by the user: $ARGUMENTS

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

Follow these steps:

## 1. Company Lookup
Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations below (see `../data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5

## 2. Series Discovery & Working Capital Profile Detection
Cast a wide net to discover ALL available series for this company. Search with multiple keyword sets to maximize coverage:
- Balance sheet: "receivable", "inventory", "payable", "deferred revenue", "contract", "prepaid", "accrued", "current asset", "current liabilit"
- Cash flow: "cash flow from operations", "working capital", "depreciation", "amortization", "stock-based comp", "capital expenditure", "free cash flow"
- Income statement: "revenue", "cost of goods", "cost of revenue", "operating income", "net income"
- Business-specific: "backlog", "billing", "remaining performance obligation", "provision", "allowance", "reserve", "unearned premium", "loss ratio"

Collect all unique series IDs. Read every series name carefully. You need to understand:
- What balance sheet line items are available (receivables, inventory, payables, deferred revenue, contract assets/liabilities, prepaid expenses, accrued liabilities, etc.)
- What cash flow statement detail exists (CFO, changes in working capital components, capex, stock-based comp, D&A, etc.)
- What business-specific KPIs exist that contextualize working capital (e.g., backlog for industrials, deferred revenue for SaaS, policy reserves for insurance, loan loss provisions for banks)

Based on series availability, classify the business's working capital profile:

| If you find series like... | Profile | Primary focus |
|---|---|---|
| Inventory, COGS, accounts payable, accounts receivable | **Inventory-intensive (manufacturing, retail, consumer goods)** | Full CCC decomposition: DIO + DSO − DPO. Inventory is the core risk. Watch for inventory-to-sales divergence, channel stuffing signals, obsolescence risk |
| Deferred revenue, contract liabilities, billings, remaining performance obligations | **Negative working capital / SaaS / subscription** | Deferred revenue is the key asset — cash collected before revenue recognized. Focus on billings vs. revenue spread, deferred revenue growth vs. revenue growth, and whether the cash-first dynamic is strengthening or weakening |
| Receivables and payables but minimal/no inventory | **Asset-light services (consulting, staffing, advertising, tech services)** | DSO is the main event. Receivables quality, aging, concentration. Unbilled receivables or contract assets as early warning. DPO as a secondary lever |
| Loans, deposits, allowance for credit losses, provision expense, net charge-offs | **Financial institutions (banks, specialty finance)** | Traditional CCC is meaningless. Focus on provision adequacy (allowance/loans, provision/NCOs, reserve coverage), deposit cost and mix, and the gap between provision expense and actual cash losses realized as the earnings quality signal |
| Policy reserves, loss reserves, unearned premiums, LAE | **Insurance** | Reserve adequacy is the working capital equivalent. Prior-year reserve development (favorable/adverse), loss ratio trends, reserve-to-premium ratios. Cash flow from underwriting vs. reported underwriting income |
| Contract assets, unbilled receivables, costs to obtain contracts, progress billings | **Long-cycle / contract-based (construction, defense, engineering)** | Percentage-of-completion dynamics. Overbilling vs. underbilling, contract asset growth vs. revenue, cash collection timing on milestones. Watch for aggressive revenue recognition through under-reserved contract losses |
| Deferred commissions, capitalized content/software, prepaid expenses dominate | **High-intangible / platform** | "Hidden" working capital in capitalized costs. Focus on capitalization rate vs. amortization, whether capitalizing faster than amortizing (building a balloon), and the cash flow impact of these non-traditional working capital items |

If the company is a hybrid or doesn't map cleanly, construct a blended framework. The profile is a guide, not a constraint.

**Edge cases:**
- **SaaS / negative working capital businesses**: Traditional CCC is misleading or meaningless. The entire framework should pivot to deferred revenue dynamics, billings analysis, and RPO trends. Working capital is a source of cash, not a use — frame accordingly. The earnings quality analysis still applies (accruals ratio, CFO/NI) but interpret directionally opposite: declining deferred revenue growth is the red flag here, not rising receivables.
- **Financial institutions**: Skip CCC entirely. The balance sheet IS the product. Focus the entire report on credit quality and reserve adequacy: allowance for loan losses / total loans, provision expense / net charge-offs (the "reserve build" or "reserve release"), vintage analysis if available, and the gap between provision expense booked through earnings and actual cash losses realized.
- **Insurance companies**: Skip CCC. Focus on loss reserve adequacy and development. Prior-year reserve development (favorable = prior reserves were adequate or over-reserved; adverse = prior reserves were insufficient). Show the trend. Connect reserve movements to reported combined ratio and operating income.
- **Pre-revenue / early-stage companies**: Focus on burn rate and cash runway. Working capital analysis still applies but framed as "how much cash is being consumed by the operating cycle" rather than earnings quality (since there are no meaningful earnings).
- **Conglomerates / multi-segment**: Use consolidated working capital data but flag if segment mix makes the consolidated CCC misleading. Note which segments are likely driving the consolidated working capital dynamics.
- **Seasonal businesses**: Explicitly normalize for seasonality by comparing each quarter to the same quarter prior year, not the prior sequential quarter. Call out the seasonal pattern so the reader doesn't mistake a normal seasonal build for a structural deterioration.
- **Companies with large non-cash charges**: SBC, amortization of intangibles, and impairments can distort the CFO/NI ratio. When calculating earnings quality metrics, provide both the unadjusted and adjusted (ex-SBC, ex-amortization) versions and explain which is more informative for this specific business.

## 3. Working Capital Data Pull
Calculate 10 quarters backward from `latest_calendar_quarter`. Pull all working capital components identified in Step 2 for those periods:

**Balance sheet** (all working capital components):
- Accounts receivable
- Inventory (total, and breakdown into raw materials / WIP / finished goods if available)
- Accounts payable
- Deferred revenue / contract liabilities
- Contract assets / unbilled receivables
- Prepaid expenses
- Accrued liabilities / other current liabilities
- Total current assets, total current liabilities

**Income statement:**
- Revenue
- COGS / cost of revenue (if applicable)
- Operating income
- Net income

**Cash flow statement:**
- Cash flow from operations (CFO)
- Changes in each working capital component (if available as separate line items)
- Depreciation & amortization
- Stock-based compensation
- Capital expenditures
- Free cash flow (compute as CFO - CapEx if not available directly, label "(calc.)")

**Important: YTD-to-quarterly conversion.** Some companies (e.g., Apple) report cash flow items on a fiscal year-to-date basis rather than quarterly. Check whether CF data appears to be YTD (values increasing monotonically through the fiscal year, then resetting). If so, convert to quarterly values by subtracting the prior quarter's YTD figure. Note this conversion in the report.

**Business-specific KPIs** as identified in Step 2.

**Derived metrics** (calculate from pulled data, label each as "(calc.)" and show formulas):
- DSO = (Accounts Receivable / Revenue) × days-in-period
- DIO = (Inventory / COGS) × days-in-period (if inventory-intensive)
- DPO = (Accounts Payable / COGS) × days-in-period
- CCC = DSO + DIO − DPO (if applicable)
- Accrual ratio = (Net Income − CFO) / Average Total Assets
- Cash conversion ratio = CFO / Net Income
- Working capital intensity = ΔNet Working Capital / ΔRevenue
- Profile-specific derived metrics (e.g., deferred revenue days for SaaS, allowance/loans for banks, reserve-to-premium for insurance)

## 4. Qualitative Research
Search SEC filings for context on working capital dynamics. Use profile-specific search terms:
- **Inventory-intensive**: Try "inventory reserves", "inventory write-down"; fallback to "excess and obsolete", "channel inventory", "sell-through"
- **SaaS/subscription**: Try "remaining performance obligations", "deferred revenue"; fallback to "billings", "contract liabilities", "revenue recognition"
- **Services**: Try "unbilled receivables", "days sales outstanding"; fallback to "allowance for doubtful accounts", "contract assets"
- **Financials**: Try "allowance for credit losses", "provision"; fallback to "net charge-offs", "reserve adequacy", "CECL"
- **General (all profiles)**: Try "accounts receivable", "accounts payable"; fallback to "working capital", "cash conversion", "liquidity"

Extract management commentary on working capital trends, collection issues, inventory management, supplier terms, etc. with document citations.

## 5. Analysis & Report Synthesis

**Section 1: Working Capital Profile (brief)**
- 2-3 sentences identifying the business's working capital archetype and why it matters
- What is the "unit of working capital risk" for this business? (inventory for a manufacturer, receivables for a services firm, deferred revenue for SaaS, reserves for insurance)
- One sentence on the headline finding: is working capital a source of strength, a neutral factor, or a red flag for this company right now?

**Section 2: Cash Conversion Cycle (or profile-adapted equivalent)**
For inventory-intensive businesses, show the full CCC decomposition:
- DSO, DIO, DPO, CCC — quarterly history (10 quarters)
- Include YoY change as sub-rows
- Highlight any quarter where a component moved more than 5 days (or equivalent threshold) — this is a flag

For non-inventory businesses, adapt the framework:
- SaaS/subscription: Show "Days Deferred Revenue Outstanding" (deferred revenue / revenue × days), billings-to-revenue ratio, and net working capital as % of revenue
- Services: DSO decomposition (billed vs. unbilled), DPO, net working capital days
- Financials: Skip CCC entirely — use provision/NCO coverage, allowance/loans, deposit mix
- Insurance: Skip CCC — use reserve development, combined ratio decomposition, cash flow from underwriting vs. reported income

**Section 3: Earnings Quality Assessment**
This is the section that makes the report valuable for a short-seller or skeptical long. Three sub-analyses:

*3a. Accruals Analysis*
- Calculate the Sloan accrual ratio: (Net Income − CFO) / Average Total Assets
  - Persistent high positive accruals = low earnings quality = earnings running ahead of cash
  - Negative accruals (CFO > Net Income) = high earnings quality
- Show the quarterly trend. Is the accrual ratio rising (deteriorating) or falling (improving)?
- Decompose the accrual: which specific working capital line items are driving the gap between earnings and cash flow? Is it receivables growing faster than revenue? Inventory building? Payables shrinking? Deferred revenue decelerating?

*3b. Cash Conversion Ratio*
- CFO / Net Income, quarterly and trailing-twelve-month
- A healthy business should convert >80% of net income to CFO over time (adjust by business model — SaaS may be >100% due to deferred revenue; capex-heavy businesses need FCF/NI instead)
- Flag any quarter where conversion drops below 60% and explain why

*3c. Revenue-to-Receivables Divergence*
- Show revenue growth vs. receivables growth on the same basis (YoY)
- When receivables growth persistently exceeds revenue growth, it's a classic red flag: the company may be extending payment terms to pull forward sales, booking revenue on deteriorating credits, or facing collection issues
- Calculate the divergence spread (receivables growth − revenue growth) and show whether it's widening or narrowing

**Section 4: Working Capital Intensity & Growth Drag**
How much incremental working capital does this business consume for each dollar of revenue growth?
- Calculate: ΔNet Working Capital / ΔRevenue for each period (the "working capital intensity ratio"). **Use YoY changes (not sequential QoQ)** for this ratio to avoid seasonal noise — QoQ denominators can flip sign due to seasonality, making the ratio meaningless. If computing on a TTM rolling basis, show that instead.
- Show the trend: is the business becoming more or less capital-efficient as it scales?
- Quantify the FCF impact: "In the last four quarters, working capital consumed $Xm of cash, reducing FCF by X% vs. what it would have been at stable working capital"
- For high-growth companies, this is critical: a business growing 30% with 15% working capital intensity is funding growth very differently than one growing 30% with 2% intensity
- Contextualize with capex intensity: total investment requirement = capex + working capital investment. Show both as % of revenue

**Section 5: Component Deep-Dives**
For each material working capital component (the 2-3 that matter most for this business type), provide a focused analysis:

*Structure for each component:*
- Current level (absolute and as days/% of revenue)
- Historical trend (10 quarters)
- Rate of change: is it improving or deteriorating, and is the rate of change itself accelerating?
- Context: why might this be happening? Reference management commentary from filings if available
- Benchmark: where does this sit vs. the company's own history? (Don't fabricate peer comps — only include if data supports it)

*Which components to deep-dive depends on the profile:*
- Inventory-intensive: Inventory (breakdown by raw/WIP/finished if available), Receivables, Payables
- SaaS: Deferred Revenue, Contract Assets, Deferred Commissions (capitalized contract costs)
- Services: Receivables (billed + unbilled), Accrued Liabilities
- Financials: Loan Loss Allowance, Provision Expense, Net Charge-Offs
- Insurance: Loss Reserves, Unearned Premiums, Prior-Year Development

**Section 6: Red Flags & Green Flags**
Explicit, concise checklist format. Scan the data for each of the following and report findings:

*Red flags (earnings quality / liquidity concerns):*
- DSO increasing while revenue growth is slowing (demand deterioration masked by term extensions)
- Inventory growing faster than COGS or revenue (demand softening, potential write-down ahead)
- DPO declining (suppliers tightening terms — potential credit deterioration signal)
- Accrual ratio rising above +5% (earnings quality deteriorating)
- CFO/Net Income < 0.6x for two or more consecutive quarters
- Receivables growth > revenue growth for 3+ consecutive quarters
- Deferred revenue growth decelerating faster than revenue growth (pipeline weakening for subscription businesses)
- Unbilled receivables / contract assets growing rapidly (aggressive percentage-of-completion or ASC 606 recognition)
- Capitalized costs (software, commissions, content) growing faster than associated revenue (building an amortization balloon)
- Working capital intensity ratio rising (growth becoming more capital-consumptive)
- Allowance/loans declining while loan growth accelerates (under-reserving for banks)

*Green flags (strong cash generation / conservative accounting):*
- DSO declining or stable while revenue grows (pricing power, healthy demand)
- CCC shortening over time (operational improvement)
- CFO/Net Income persistently > 1.0x (earnings over-earned in cash)
- Negative net working capital (float-funded business model — customers pay before you deliver)
- Deferred revenue growing faster than revenue (strong forward visibility)
- Accrual ratio consistently negative (cash earnings exceed reported earnings)
- Allowance/loans stable or rising modestly while credit metrics are benign (conservative reserving)

For each flag triggered, include the specific data that triggered it and the implication. Use Daloopa citations for every figure.

**Section 7: Key Drivers & What to Watch**
The forward-looking, analytically highest-value section:
- **The 3-5 working capital metrics that matter most** for this specific company, ranked by sensitivity to the investment thesis
- For each: current level, direction, historical range, and what would cause an inflection
- **Scenario analysis**: "If DSO increases another 5 days from here, the company would need an additional ~$Xm in working capital, reducing FCF by ~X%" — quantify the P&L/cash flow impact of plausible working capital scenarios
- **What to watch next quarter**: specific items to monitor in the next earnings release or 10-Q filing. Be concrete: "Watch the inventory line relative to the revenue guide — if inventory grows >X% sequentially while revenue is guided flat, it would be the third consecutive quarter of inventory build and a meaningful negative signal"

**Section 8: Summary Assessment**
- 3-4 sentence verdict on working capital health and earnings quality
- Is this a cash-generative business with conservative accounting, or is there a gap between reported earnings and economic reality?
- What is the single biggest risk (or source of comfort) in the working capital profile?

**Analytical standards:**
- **Three-layer density**: every metric should have a data point, context (vs. history, vs. expectations), and an implication (so what?)
- **Show your math**: all derived metrics (DSO, DIO, DPO, CCC, accruals ratio, cash conversion ratio, working capital intensity) should show the formula and inputs used, so the reader can verify or adjust
- **Use quarterly data, but show TTM where appropriate**: some metrics (like the accruals ratio) are more meaningful on a trailing-twelve-month basis to smooth seasonality. Show both quarterly and TTM when relevant
- **Flag seasonality**: many businesses have seasonal working capital patterns (retail builds inventory in Q3 for Q4, etc.). Compare YoY, not just QoQ, for directional conclusions. Note when a move is seasonal vs. structural
- **Distinguish levels from changes**: a company can have structurally high DSO (that's the business model) but stable DSO (not a red flag). The concern is when DSO is rising, not when it's high in absolute terms. Always emphasize the direction and rate of change, not just the level
- **No false precision**: working capital metrics calculated from quarterly balance sheets are point-in-time snapshots. Acknowledge this limitation. If average balances are available, use them; if not, use period-end and note the limitation
- **Source everything**: every number traceable to Daloopa. Use citations per the design system conventions
- **Flag data gaps**: if a key balance sheet component isn't broken out in Daloopa's data (e.g., inventory broken into raw/WIP/finished), say so and explain what that limits

## 6. Charts
Use `infra/chart_generator.py` for charts. Include at minimum:
1. **CCC trend chart** (time-series or waterfall showing DSO + DIO − DPO = CCC by quarter, or the equivalent decomposition for non-inventory businesses)
2. **Earnings quality chart** (time-series showing net income vs. CFO over time, with the accrual gap visible)
3. **Revenue vs. receivables growth chart** (two lines on the same axis showing YoY growth rates, with divergence highlighted)
4. Additional charts as warranted by the profile (e.g., inventory/COGS ratio for manufacturers, deferred revenue waterfall for SaaS, reserve adequacy trend for financials)

**All charts must be embedded in the HTML as base64 data URIs** (e.g., `<img src="data:image/png;base64,...">`) so the report is fully self-contained with no external file dependencies. After generating each chart PNG, read the file and convert to base64 for embedding. Do not use relative `<img src="filename.png">` paths.

If chart_generator.py is unavailable, embed simple inline SVG charts directly in the HTML.

## 7. Save Report
Save to `reports/{TICKER}_working_capital.html` using the HTML report template from `../design-system.md`. Write the full analysis as styled HTML with the design system CSS inlined. This is the final deliverable — no intermediate markdown step needed.

Structure the report with these sections:

```
<h1>{Company Name} ({TICKER}) — Working Capital & Earnings Quality Analysis</h1>
<p>Generated: {date}</p>

<h2>Summary</h2>
{2-3 sentences: What is the working capital profile? Headline finding on earnings quality. Key risk or comfort.}

<h2>Working Capital Profile</h2>
{Section 1 content}

<h2>Cash Conversion Cycle</h2>
<table>
| Metric | Q(-9) | Q(-8) | ... | Q(latest) |
{DSO, DIO, DPO, CCC (or profile equivalent) — with Daloopa citations and YoY change sub-rows}
</table>
{Commentary on CCC trend and any flagged moves}

<h2>Earnings Quality Assessment</h2>

<h3>Accruals Analysis</h3>
<table>
| Metric | Q(-9) | Q(-8) | ... | Q(latest) |
{Net Income, CFO, Accrual Ratio — with Daloopa citations}
</table>
{Decomposition of the accrual and trend analysis}

<h3>Cash Conversion Ratio</h3>
<table>
| Metric | Q(-9) | Q(-8) | ... | Q(latest) |
{CFO, Net Income, CFO/NI ratio, TTM CFO/NI — with Daloopa citations}
</table>
{Assessment of cash conversion quality}

<h3>Revenue vs. Receivables Divergence</h3>
<table>
| Metric | Q(-9) | Q(-8) | ... | Q(latest) |
{Revenue YoY growth, Receivables YoY growth, Divergence spread}
</table>
{Analysis of divergence trend}

<h2>Working Capital Intensity & Growth Drag</h2>
<table>
| Metric | Q(-9) | Q(-8) | ... | Q(latest) |
{ΔNet WC, ΔRevenue, WC Intensity Ratio, CapEx % Rev, Total Investment % Rev}
</table>
{FCF impact quantification and growth drag assessment}

<h2>Component Deep-Dives</h2>
{2-3 focused deep-dives on the most material components for this business type}

<h2>Red Flags & Green Flags</h2>
{Checklist format with specific data citations for each triggered flag}

<h2>Key Drivers & What to Watch</h2>
{Ranked drivers with scenario analysis and next-quarter monitoring items}

<h2>Summary Assessment</h2>
{3-4 sentence verdict}
```

All financial figures must use Daloopa citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved.

Highlight the key findings: Is this a cash-generative business? Are there earnings quality concerns? What should an analyst focus on in the next filing?
