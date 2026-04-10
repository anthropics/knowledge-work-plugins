---
name: unit-economics
description: Bottoms-up unit economics decomposition for any public company
argument-hint: TICKER
---

Perform a bottoms-up unit economics decomposition for the company specified by the user: $ARGUMENTS

**Before starting, read `../data-access.md` for data access methods and `../design-system.md` for formatting conventions.** Follow the data access detection logic and design system throughout this skill.

Follow these steps:

## 1. Company Lookup
Look up the company by ticker using `discover_companies`. Capture:
- `company_id`
- `latest_calendar_quarter` — anchor for all period calculations below (see `../data-access.md` Section 1.5)
- `latest_fiscal_quarter`
- Firm name for report attribution (default: "Daloopa") — see `../data-access.md` Section 4.5

## 2. Series Discovery & Business Archetype Detection
Cast a wide net to discover ALL available series for this company. Search with multiple keyword sets to maximize coverage:
- Financial: "revenue", "income", "profit", "margin", "eps", "cost"
- Operating KPIs: "subscriber", "user", "customer", "unit", "arpu", "retention", "churn"
- Segment/Product: "segment", "product", "service", "geographic"
- Business-specific: "store", "gmv", "order", "booking", "backlog", "premium", "loan", "aum", "room", "seat", "bed", "acreage"

Collect all unique series IDs. Read every series name and description returned. **This is how you learn what kind of business this is and what unit-level KPIs Daloopa tracks for it.**

Based on series availability, classify the business into one of these archetypes (or a hybrid). This classification drives the entire report structure:

| If you find series like... | Archetype | Unit = |
|---|---|---|
| ARR, MRR, net dollar retention, customers, ACV, churn, CAC, LTV | **SaaS / Subscription** | Customer or subscription |
| Store count, same-store sales, AUV, restaurant-level margin, new openings | **Unit-based retail / Restaurant** | Store or unit |
| GMV, take rate, orders, AOV, active buyers/sellers | **Marketplace / E-commerce** | Order or transaction |
| Subscribers, ARPU, churn, content spend per sub | **Consumer subscription (media/streaming)** | Subscriber |
| Premiums written, loss ratio, combined ratio, policies in force | **Insurance** | Policy |
| NIM, loans, deposits, provision for credit losses, NCOs | **Banking / Lending** | Loan or account |
| ASP, units shipped, cost per unit, gross margin per unit | **Hardware / Manufacturing** | Unit shipped |
| AUM, management fee rate, performance fees, fund flows | **Asset Management** | Dollar of AUM |
| Revenue per available room (RevPAR), occupancy, ADR | **Hospitality / Lodging** | Room night |
| RPM, RASM, CASM, load factor, ASMs | **Airlines / Transportation** | Available seat mile |
| Revenue per user, DAU, MAU, ARPU, engagement | **Digital platform / Advertising** | User |
| Beds, admissions, revenue per admission, case mix | **Healthcare facilities** | Admission or bed |
| Acreage, production per acre, realized price per unit | **Commodity / E&P** | Unit of production |

If the business is a hybrid or doesn't fit neatly, construct a custom framework from the available series. The archetype is a starting guide, not a constraint.

**Edge cases:**
- **Diversified / multi-segment companies**: Pick the largest or most analytically interesting segment for primary analysis. Note other segments briefly. If the user specifies a segment, focus there.
- **Pre-revenue / early-stage companies**: Focus on burn rate per unit of growth, cash efficiency, and path to unit profitability.
- **Financial companies (banks, insurance, asset managers)**: These have specialized unit economics. For banks, the "unit" is a dollar of assets — focus on NIM, fee income/assets, efficiency ratio, credit costs. For insurance, focus on the combined ratio decomposition. Don't force a SaaS or retail framework onto financials.
- **Companies with no obvious unit-level KPIs in Daloopa**: Fall back to a margin bridge / operating leverage analysis using standard income statement data. Decompose revenue into whatever sub-components are available (segment, geography, product line) and analyze profitability at that level. Note the limitation.
- **Companies that stopped disclosing unit data**: Some major companies (e.g., Apple post-2018) no longer report unit shipments or ASPs. If unit-level data is not available, adapt to the highest-resolution decomposition the data supports (e.g., segment revenue × segment margin). Clearly flag the data gap and explain what proxy you used. Do not fabricate unit estimates.

## 3. Unit Economics Data Pull
Calculate 10 quarters backward from `latest_calendar_quarter`. Pull all archetype-relevant series identified in Step 2 for those periods, plus standard financials:
- Revenue (total and segment)
- COGS / cost of revenue
- Gross profit
- Operating income
- Net income
- All operating KPIs relevant to the detected archetype

**Derived metrics** (calculate from pulled data, label each as "(calc.)" and show formulas):
- Revenue per unit (Revenue / units)
- Gross margin per unit
- Contribution margin per unit (if variable costs are available)
- Unit growth rate (QoQ and YoY)
- Revenue per unit growth rate (QoQ and YoY)
- Any archetype-specific derived metrics (e.g., CAC payback = CAC / (ARPU × gross margin), LTV/CAC, 4-wall margin, take rate, combined ratio)

## 4. Qualitative Research
Search SEC filings for context on the unit economics. Use archetype-specific search terms:
- **SaaS**: Try "net dollar retention", "customer acquisition cost"; fallback to "expansion", "churn", "upsell"
- **Restaurant/Retail**: Try "average unit volume", "restaurant-level margin"; fallback to "same-store", "new unit", "unit opening"
- **Marketplace**: Try "take rate", "gross merchandise value"; fallback to "active buyers", "order volume", "monetization"
- **Hardware/Manufacturing**: Try "average selling price", "units shipped"; fallback to "ASP", "volume", "mix"
- **Insurance**: Try "combined ratio", "loss ratio"; fallback to "underwriting", "premium", "policy"
- **Banking**: Try "net interest margin", "provision"; fallback to "loan growth", "credit quality", "efficiency"
- **Digital platform**: Try "average revenue per user", "monthly active users"; fallback to "engagement", "monetization", "ARPU"
- **General (all archetypes)**: Try "unit economics", "pricing"; fallback to "profitability", "margin", "per unit"

Extract management commentary on pricing, retention, expansion, new unit openings, margin levers, etc. with document citations.

## 5. Analysis & Report Synthesis

**Section 1: Business Model & Unit Definition (brief)**
- 2-3 sentence description of what the "unit" is for this business
- Why this decomposition matters for understanding the company's economics
- What the revenue build-up looks like: units × revenue-per-unit, or equivalent

**Section 2: Revenue Decomposition**
- Show the bottoms-up revenue build: how units × price/rate × utilization (or equivalent) bridges to reported revenue
- Table: quarterly history (10 quarters) showing each component
- Highlight which lever is driving growth: volume vs. price vs. mix
- Include growth rates (YoY) as sub-rows beneath each metric

**Section 3: Unit-Level Profitability**
The core of the report. Show margin/profitability at the unit level over time:
- For SaaS: gross margin per customer, CAC payback period, LTV/CAC ratio
- For restaurants: 4-wall EBITDA margin, new unit payback, cash-on-cash return
- For marketplace: contribution margin per order, after accounting for fulfillment/transaction costs
- For insurance: loss ratio + expense ratio = combined ratio per policy
- For hardware: gross margin per unit, cost per unit breakdown
- Adapt to whatever the business actually is
- Table: historical trend with period-over-period change
- Explicitly call out whether unit economics are improving or deteriorating and by how much

**Section 4: Cohort / Vintage Analysis (if data supports it)**
- For subscription businesses: net retention curves, expansion vs. contraction
- For unit-based businesses: same-store vs. new-store contribution, unit maturation
- For lending: vintage loss curves, seasoning
- If insufficient data for true cohort analysis, note this and substitute with proxy analysis (e.g., new customer growth rate vs. retention rate implies cohort behavior)

**Section 5: Scalability & Operating Leverage**
- How do unit economics change as the business scales?
- Fixed cost absorption: which costs are truly fixed vs. variable per unit?
- Show operating leverage by plotting revenue growth vs. cost growth
- Incremental margins: are they expanding or compressing as the business grows?

**Section 6: Key Drivers & What to Watch**
This is the most analytically valuable section. Based on the data, identify:
- **The 3-5 metrics that matter most** for this company's unit economics, ranked by sensitivity / impact
- For each metric: current level, historical range, direction of travel, and what would cause it to inflect
- **Bull case drivers**: what would improve unit economics (e.g., pricing power, mix shift to higher-margin products, operating leverage kicking in, retention improving)
- **Bear case risks**: what would deteriorate unit economics (e.g., competitive pricing pressure, rising CAC, input cost inflation, regulatory impact on take rates)
- Connect each driver to its P&L impact: "a 100bps improvement in net retention would add ~$X to ARR" or "each new store generates ~$Xm in 4-wall EBITDA in year 2"

**Section 7: Summary Assessment**
- 3-4 sentence verdict on the health and trajectory of the company's unit economics
- Is this a business with improving, stable, or deteriorating unit economics?
- What is the single most important thing to monitor going forward?

**Analytical standards:**
- **Three-layer density**: every data point should have context (vs. prior period, vs. peers if known) and an implication (what it means for the investment case)
- **Show your math**: when you derive a metric (e.g., implied CAC = S&M expense / new customers added), show the calculation explicitly so the reader can verify
- **Flag data gaps**: if a key metric for the archetype isn't available in Daloopa's data, say so explicitly and explain what proxy you used or why the analysis is limited
- **No generic filler**: if you don't have data to support a section, skip it or shorten it. Never pad with boilerplate
- **Source everything**: every number should be traceable. Use Daloopa source citations per the design system conventions
- **Prefer rates and ratios over absolutes**: unit economics are about efficiency, not scale. Lead with margins, returns, and per-unit metrics. Include absolutes as context

## 6. Charts
Use `infra/chart_generator.py` for charts. Include at minimum:
1. A **revenue decomposition chart** (waterfall or time-series showing units × price → revenue)
2. A **unit profitability trend chart** (time-series showing the key unit margin metric over time)
3. Additional charts as warranted by the archetype (e.g., net retention waterfall for SaaS, same-store sales trend for restaurants, take rate trend for marketplaces)

**All charts must be embedded in the HTML as base64 data URIs** (e.g., `<img src="data:image/png;base64,...">`) so the report is fully self-contained with no external file dependencies. After generating each chart PNG, read the file and convert to base64 for embedding. Do not use relative `<img src="filename.png">` paths.

If chart_generator.py is unavailable, embed simple inline SVG charts directly in the HTML.

## 7. Save Report
Save to `reports/{TICKER}_unit_economics.html` using the HTML report template from `../design-system.md`. Write the full analysis as styled HTML with the design system CSS inlined. This is the final deliverable — no intermediate markdown step needed.

Structure the report with these sections:

```
<h1>{Company Name} ({TICKER}) — Unit Economics Analysis</h1>
<p>Generated: {date}</p>

<h2>Summary</h2>
{2-3 sentences: What is the "unit"? Are unit economics improving or deteriorating? Key takeaway.}

<h2>Business Model & Unit Definition</h2>
{Section 1 content}

<h2>Revenue Decomposition</h2>
<table>
| Component | Q(-9) | Q(-8) | ... | Q(latest) |
{Units, revenue per unit, revenue — with Daloopa citations and YoY growth sub-rows}
</table>
{Commentary on volume vs. price drivers}

<h2>Unit-Level Profitability</h2>
<table>
| Metric | Q(-9) | Q(-8) | ... | Q(latest) |
{Archetype-specific unit margins — with Daloopa citations}
</table>
{Commentary on unit economics trajectory}

<h2>Cohort / Vintage Analysis</h2>
{Section 4 content, or note if insufficient data}

<h2>Scalability & Operating Leverage</h2>
<table>
| Metric | Q(-9) | Q(-8) | ... | Q(latest) |
{Revenue growth vs cost growth, incremental margins}
</table>
{Operating leverage assessment}

<h2>Key Drivers & What to Watch</h2>
{Ranked drivers with sensitivity analysis and bull/bear scenarios}

<h2>Summary Assessment</h2>
{3-4 sentence verdict}
```

All financial figures must use Daloopa citation format: `<a href="https://daloopa.com/src/{fundamental_id}">$X.XX million</a>`

Tell the user where the HTML report was saved.

Highlight the 2-3 most important findings about the company's unit economics and what they signal for the investment case.
