---
name: financial-modeling
description: Build financial models for business cases including ROI, NPV, IRR, scenario analysis, and total cost of ownership. Use when developing investment recommendations, comparing strategic options, quantifying the value of initiatives, building business cases, performing cost-benefit analysis, or valuing a business unit for strategic decisions. Covers standard financial analysis workflows (ROI, business case, cash flow projections, break-even, DCF) and advanced techniques (EVA, MIRR, real options, Monte Carlo thinking, discount rate selection).
---

# Financial Modeling

Build business cases, calculate investment returns, and structure financial analyses to support strategic recommendations. Every output should be table-heavy, assumption-explicit, and end with a clear decision recommendation.

## Before You Begin

Financial models are only as good as their inputs. Ask for actual data rather than fabricating figures:
- What are the actual cost figures (labor costs, infrastructure spend, operating costs)?
- What revenue or benefit figures should the model use?
- What is the organization's discount rate, WACC, or hurdle rate?
- When using numbers the user didn't provide, flag every one explicitly: "I'm assuming $22M annual labor cost based on [300 FTEs at $73K average loaded cost]. This is a placeholder... validate with actual payroll data." Never present fabricated financial inputs as if they were the user's real numbers.

---

## Behavioral Principles

1. **Document every assumption.** State the source, basis, and confidence level for each assumption. Undocumented assumptions are the #1 cause of flawed business cases.
2. **Be conservative by default.** Use realistic, not optimistic, assumptions. Stretch goals are not baseline projections. If a client pushes for aggressive numbers, flag the risk explicitly.
3. **Sensitivity over precision.** A precise but wrong number is worse than an approximate range. Always identify which 2-3 variables drive 80% of the outcome and test them.
4. **Show alternatives.** Never present a single option. Always show a "do nothing" baseline (quantified, not just mentioned) and one alternative to the recommended path.
5. **Separate facts from forecasts.** Clearly distinguish historical data from projected values. Label assumptions as "verified," "estimated," or "placeholder."
6. **Make it auditable.** Structure analyses so a third party can trace any output back to its source assumptions in under 5 minutes.
7. **The number supports the decision.** The business case exists to support a decision, not to generate a number. If the financial analysis doesn't lead to a clear recommendation, the framing is wrong.

---

## Analysis Type Selection

| Analysis Type | Use Case | Key Outputs |
|---|---|---|
| ROI Analysis | Quick investment assessment | Return %, payback period |
| Business Case | Comprehensive investment case | NPV, IRR, payback |
| DCF Valuation | Company or business unit valuation | Enterprise value, equity value |
| Scenario Analysis | Risk assessment | Best/base/worst case, probability-weighted NPV |
| Break-even Analysis | Volume or revenue threshold | Break-even point, margin of safety |
| TCO Comparison | Comparing competing solutions | Annualized cost, cost per user |
| EVA | Cross-unit performance comparison | Value creation vs. capital cost |

---

## Interpreting Client Inputs

When clients provide financial parameters, clarify before modeling:

- **Percentage improvements**: "Reduce costs by 30%" ... 30% of what? Get the absolute base number. $22M labor bill at 30% = $6.6M. $8M labor bill at 30% = $2.4M. The percentage is meaningless without the base.
- **Rate vs. cost vs. outcome**: "15% quality improvement" could mean defect rate drops 15% (3.2% to 2.7%), cost of poor quality drops 15% ($4.5M to $3.8M), or yield improves 15% (85% to 97.8%). Each has very different financial impact. State your interpretation explicitly and flag it for validation.
- **When the base isn't provided**: State your assumption, show the math, and mark it as a placeholder. "Assuming $22M annual labor cost based on 300 FTEs at $73K average loaded cost [placeholder ... validate with client payroll data]."

---

## Capex vs. Opex Distinction

This matters for financial statement impact and CFO evaluation. Always classify costs.

| Dimension | Capex | Opex |
|---|---|---|
| P&L impact | Depreciated over useful life | Expensed in period |
| Cash flow | Large upfront outflow | Spread over time |
| Balance sheet | Increases asset base | No asset impact |
| CFO preference | Varies by company; some prefer capex (asset build), others prefer opex (flexibility) |
| Tax treatment | Depreciation shield over years | Immediate deduction |

When relevant (cloud migration, build vs. buy, lease vs. purchase, M&A purchase price allocation): show the same investment under both capex and opex treatment. Cloud migrations are often justified partly on the capex-to-opex shift. For M&A, classify the purchase price into goodwill, identifiable intangibles (amortized), and tangible assets (depreciated). The amortization schedule affects reported earnings and tax shields, which matters for PE exit multiples and earnout calculations.

---

## Do-Nothing Baseline (Required)

Every business case must quantify the cost of inaction. "Do nothing" is never free. Include:

- **Ongoing costs**: Current run-rate, fully loaded
- **Cost escalation**: Aging infrastructure maintenance, rising labor costs, technical debt accumulation. Use 5-10% annual escalation for aging systems unless client provides actuals
- **Risk costs**: Probability x impact for known risks (outages, compliance, security)
- **Opportunity costs**: Revenue foregone, competitive disadvantage, inability to execute strategic initiatives

Example: A $50M/year on-prem environment isn't a $150M 3-year baseline. With aging hardware requiring $8-12M refresh, 8% cost growth, and $2M annual outage risk, the real 3-year baseline is $170-180M.

---

## ROI Analysis

For quick investment assessment, structure the analysis as:

**Investment Summary**: Initial investment, ongoing investment per year, project life. Classify each cost as capex or opex.

**Benefits Projection**: For each benefit category, project Year 1 through end of project life with totals. Show ramp-up (Year 1 benefits are rarely at full run-rate).

**Return Metrics**:

| Metric | Value | Benchmark | Assessment |
|---|---|---|---|
| Simple ROI (%) | [calc] | >50% | Exceeds / Meets / Below |
| Payback period | [calc] | <3 years | Exceeds / Meets / Below |
| NPV (at WACC) | [calc] | >$0 | Positive / Negative |
| IRR | [calc] | >WACC | Exceeds / Below |

**Sensitivity**: Identify the 2-3 variables that drive the outcome and show NPV impact at +/- 10% and +/- 20% variation.

---

## Business Case Development

For comprehensive investment cases, structure as:

**Executive Summary**: 2-3 sentences stating the investment, the recommendation (Go/No-Go/Conditional), and the headline number (NPV or ROI).

**Problem Statement**: What problem does this investment solve? Size the problem in dollars.

**Do-Nothing Baseline**: Quantified cost of inaction over the analysis period (see Do-Nothing Baseline section).

**Financial Summary**:

| Metric | Value |
|---|---|
| Total Investment | $[X]M |
| NPV (Base Case) | $[X]M |
| IRR | [X]% |
| Payback Period | [X] months |
| 3-Year ROI | [X]% |

**Investment Details**: Cost categories (capital, implementation, ongoing opex) projected across the analysis period. Use a year-by-year table.

**Benefit Projections**: Revenue growth, cost reduction, risk mitigation projected across the analysis period. Include a confidence column (High/Medium/Low) for each benefit line.

**Cash Flow Analysis**: Annual cash flows with discount factors and present values. Show cumulative PV building to the NPV.

| | Year 0 | Year 1 | Year 2 | Year 3 |
|---|---|---|---|---|
| Total Benefits | - | $[X]M | $[X]M | $[X]M |
| Total Costs (incremental) | ($[X]M) | ($[X]M) | ($[X]M) | ($[X]M) |
| Net Cash Flow | ($[X]M) | $[X]M | $[X]M | $[X]M |
| Discount Factor | 1.000 | 0.[X] | 0.[X] | 0.[X] |
| PV of Cash Flow | ($[X]M) | $[X]M | $[X]M | $[X]M |
| Cumulative PV | ($[X]M) | ($[X]M) | $[X]M | $[X]M |

**Assumptions**: List every assumption in a table with columns: #, Assumption, Value, Basis, Status (verified/estimated/placeholder).

**Sensitivity Analysis**: Show NPV, IRR, and assessment under upside, base, and downside scenarios. Also show a tornado-style table: the 3-5 key variables with NPV impact at +/-10%.

**Risks and Mitigations**: Each risk with quantified impact ($), likelihood (H/M/L), and specific mitigation action.

**Alternatives**: At least two alternatives to the recommended option (including "do nothing"), each with NPV and key trade-offs.

**Recommendation**: See Recommendation Template below.

---

## Phased Investment Structure

For investments >$5M or with significant execution risk, structure as a staged commitment:

**Phase 1 (Pilot)**: Smallest investment that tests the critical assumption.
- Scope: What's included, what's excluded
- Investment: Typically 20-35% of full program
- Duration: 3-6 months
- Success criteria: Specific, measurable thresholds (e.g., "achieve >25% labor cost reduction on Line 1")

**Gate Decision**: Explicit go/no-go with defined metrics.
- Metrics that trigger "proceed": [thresholds]
- Metrics that trigger "stop": [thresholds]
- Metrics that trigger "modify and re-evaluate": [thresholds]

**Phase 2 (Scale)**: Full investment, contingent on Phase 1 results.
- Incremental investment beyond Phase 1
- Updated projections incorporating Phase 1 actuals

Show NPV for three scenarios:
1. Phase 1 only (worst case: we learn it doesn't work; cost = Phase 1 investment)
2. Full program (expected case)
3. Expanded program (upside: Phase 1 exceeds expectations, justifying broader scope)

This approach reduces downside risk. If a $15M investment has a worst-case NPV of ($3.8M), but a phased approach limits Phase 1 to $5.5M, the worst case drops to ($1.2M).

---

## DCF Valuation

For business or company valuation:

**Revenue Projections**: Revenue, growth rate, gross profit, gross margin, EBITDA, and EBITDA margin for current year through Year 5. Model growth rate deceleration explicitly (high-growth companies at $30M revenue typically decelerate 3-4 percentage points per year).

Revenue projection methodology depends on business maturity:
- **Mature businesses**: Apply growth rate decay. Start from the current growth rate and decelerate toward GDP growth or industry average over the projection period. A 10% grower at $500M revenue is not growing 10% in Year 5.
- **Subscription/SaaS businesses**: Use cohort-based projections. Model existing customer revenue (base revenue x net retention rate) separately from new customer revenue (new logos x average ACV x ramp). This exposes the real growth engine and avoids masking churn behind gross bookings.
- **Early-stage/high-growth**: Use a top-down reasonableness check (implied market share in Year 5) alongside the bottom-up build to catch hockey-stick projections that imply implausible market capture.

**Unlevered Free Cash Flow (UFCF)**: Build from EBITDA:
- EBITDA
- Less: taxes on EBIT (EBIT x tax rate). Use the marginal tax rate, not the effective rate, for incremental cash flow analysis.
- Less: capex (or capitalized development costs). Distinguish maintenance capex (required to sustain current operations) from growth capex (investment in new capacity or capabilities).
- Less: change in net working capital. Model each component (receivables, inventory, payables) as a percentage of revenue or COGS. Watch for businesses where working capital is a significant cash drag during growth.
- Equals: Unlevered Free Cash Flow

**Terminal Value**: Terminal value often represents 60-80% of total enterprise value, so the methodology choice matters.

- **Exit Multiple method**: Year 5 EBITDA (or revenue for high-growth/pre-profit businesses) x an appropriate comparable multiple. Use when market comparables exist and the business will likely be sold or valued on a multiples basis. Select the multiple from comparable transactions, not from current trading multiples (which fluctuate with market sentiment).
- **Gordon Growth Model**: Year 5 FCF x (1 + g) / (WACC - g). More conservative; appropriate when the business is expected to reach steady state. The terminal growth rate (g) should not exceed long-term GDP growth (2-3% nominal) for most businesses. Using a higher g implies the business will eventually become larger than the economy.
- **When to weight each**: Use exit multiple as primary for businesses with clear comparable sets and likely M&A or IPO exit paths. Use Gordon Growth as a floor or sanity check. When the two methods diverge significantly, explain why (usually because the exit multiple embeds growth expectations above the terminal growth rate) and state which you're using as primary.

**WACC Calculation**: Build up from components:

| Component | Value | Basis |
|---|---|---|
| Risk-free rate | [X]% | 10-year Treasury |
| Equity risk premium | [X]% | Damodaran estimate |
| Beta (levered) | [X] | Industry median |
| Cost of equity (CAPM) | [X]% | Rf + Beta x ERP |
| Size premium | [X]% | If sub-$500M EV |
| Cost of debt (after-tax) | [X]% | If applicable |
| Debt/equity weights | [X]/[X] | Target structure |
| **WACC** | **[X]%** | |

**Valuation Summary**: PV of projected FCFs + PV of terminal value = enterprise value. Show implied multiples (EV/Revenue, EV/EBITDA) as sanity check against comparable transactions.

**Valuation Sensitivity**: Show enterprise value in a matrix of WACC (+/- 1%) vs. terminal value driver (exit multiple or growth rate).

---

## SaaS Valuation Metrics

For SaaS and subscription businesses, supplement DCF with these metrics. They drive multiples and investor perception.

| Metric | Definition | Healthy Benchmark | Red Flag |
|---|---|---|---|
| Net Revenue Retention (NRR) | Revenue from existing customers this year / same cohort last year | >110% (>120% = premium) | <100% (shrinking base) |
| LTV/CAC | Customer lifetime value / cost to acquire | >3x | <1x (destroying value) |
| CAC Payback | Months to recover acquisition cost from gross profit | <18 months | >24 months |
| Rule of 40 | Revenue growth % + EBITDA margin % | >40 (good), >60 (elite) | <20 |
| Gross Margin by Type | Subscription vs. services vs. usage | Subscription >75% | Blended <60% |
| Logo Churn vs. Revenue Churn | Customer count loss vs. dollar loss | Revenue churn < logo churn (expansion offsets) | Revenue churn > logo churn |
| ARR per Employee | Annual recurring revenue / headcount | $150K-250K+ | <$100K |

**How these affect valuation**:
- NRR >120%: supports 8-12x ARR multiples. NRR <100%: compresses to 3-5x.
- Rule of 40 >40: "good" SaaS company. Each point above 40 adds ~0.5x to ARR multiple.
- Always request NRR by cohort and vintage. Blended NRR can mask deteriorating cohorts.
- Only subscription gross margin should drive the revenue multiple. Services revenue should be valued at 1-2x at most.
- For M&A business cases involving SaaS targets, always calculate LTV/CAC with explicit inputs shown (not just assumed). Request cohort retention data by vintage and model value per cohort. If the target can't provide cohort-level data, flag as a data quality concern that affects valuation confidence.

---

## Scenario Analysis

For risk assessment:

**Scenario Definitions**: Upside, base, and downside with description and probability weighting (must sum to 100%).

**Scenario Comparison**: Revenue, costs, NPV, IRR, and payback under each scenario.

**Probability-Weighted NPV**: Each scenario's NPV times its probability, summed to expected NPV.

Example: (0.20 x $12.8M) + (0.50 x $7.5M) + (0.25 x $1.2M) + (0.05 x ($3.8M)) = $6.4M expected NPV.

**Break-even Analysis**: Break-even revenue, break-even volume, and margin of safety vs. base case.

---

## Monte Carlo Thinking

For major investments, three-point scenarios (best/base/worst) understate the range of outcomes. When appropriate, describe the simulation design:

- **Identify variable distributions**: Which assumptions should be modeled as ranges rather than point estimates? (e.g., "labor savings: triangular distribution, min 15%, mode 30%, max 40%")
- **Specify correlations**: Which variables move together? (e.g., higher adoption speed correlates with higher training costs)
- **Define outputs to track**: Probability of positive NPV, expected NPV, 5th/95th percentile range, maximum loss
- **Identify variance drivers**: Which input assumptions contribute most to output variance? (This is often the most actionable insight)

This provides a richer risk picture than three scenarios and identifies which assumptions to spend time validating.

---

## Economic Value Added (EVA)

**Formula**: EVA = NOPAT - (Capital Charge)

Where Capital Charge = WACC x Capital Employed.

**Building the Components**:

| Component | Calculation | Notes |
|---|---|---|
| NOPAT | EBIT x (1 - tax rate) | Use operating income, exclude financing costs and non-recurring items. Adjust for operating leases if material. |
| Capital Employed | Total Assets - Current Liabilities | Or equivalently: Net Fixed Assets + Net Working Capital. For asset-light businesses, include capitalized R&D and intangibles. |
| Capital Charge | WACC x Capital Employed | Use the same WACC as DCF analysis; adjust for division-specific risk if comparing business units. |

**Interpretation**:

| EVA Result | Meaning | Action |
|---|---|---|
| Positive, growing | Creating and increasing value | Invest more capital if returns hold |
| Positive, shrinking | Still creating value, but declining | Investigate: margin erosion? Capital inefficiency? |
| Near zero | Earning approximately cost of capital | Business is a "rent payer" ... covering capital costs but not creating surplus value |
| Negative | Destroying shareholder value | Restructure, divest, or fundamentally change the business model |

**EVA for Cross-Unit Comparison**:

This is EVA's primary advantage over ROI or ROIC: it expresses value creation in absolute dollars, making units of different sizes directly comparable.

| Business Unit | NOPAT ($M) | Capital Employed ($M) | WACC | Capital Charge ($M) | EVA ($M) |
|---|---|---|---|---|---|
| Unit A | 25.0 | 150.0 | 10% | 15.0 | +10.0 |
| Unit B | 8.0 | 30.0 | 10% | 3.0 | +5.0 |
| Unit C | 12.0 | 140.0 | 10% | 14.0 | -2.0 |

Unit A has the highest absolute EVA, but Unit B has the highest EVA/Capital ratio (16.7% vs. 6.7%). Unit C is destroying value despite being profitable on a NOPAT basis.

**EVA-Based Performance Targets**:

Set targets as EVA improvement (delta EVA), not absolute EVA. This avoids penalizing units that inherited large capital bases. Decompose EVA improvement into three levers:
1. **Increase NOPAT** without proportional capital increase (operational efficiency)
2. **Reduce capital employed** without proportional NOPAT decline (asset efficiency, working capital management)
3. **Invest new capital** at returns above WACC (value-creating growth)

**When to Use EVA**:
- Comparing performance across divisions of different sizes (EVA's sweet spot)
- Evaluating whether growth is actually creating value (a division can grow revenue and NOPAT while destroying value if capital grows faster)
- Setting management incentive targets that align with shareholder value creation
- Assessing acquisition targets: is the target generating returns above its cost of capital? If EVA is negative, the acquisition price must account for the turnaround investment needed to get EVA positive
- Capital allocation decisions: direct incremental capital to units with the highest marginal EVA per dollar invested

---

## Discount Rate Selection

### Factors

| Factor | Consideration | Impact on Rate |
|---|---|---|
| Cost of capital | Company's WACC | Baseline |
| Risk level | Project risk vs. company average | +/- adjustment |
| Industry | Industry average returns | Benchmark |
| Inflation | Expected inflation rate | Include |
| Market conditions | Current interest rates | Adjust |
| Technology risk | AI/technology implementation uncertainty | + adjustment |

### Typical Ranges by Risk Level

These ranges are illustrative and depend on the prevailing interest rate environment, geography, and company-specific cost of capital. Always anchor to the organization's actual WACC or hurdle rate.

| Risk Level | Discount Rate Range | Examples |
|---|---|---|
| Low risk | 5-8% | Core operations, efficiency improvements |
| Medium risk | 8-12% | Growth initiatives |
| High risk | 12-20% | New market entry |
| Very high risk | 20%+ | New ventures, R&D |
| Platform/AI | 15-25% | Digital transformation, AI investments |

### Guidance

- When in doubt, use a higher discount rate. Better to reject a good project than to accept a bad one.
- If a project looks attractive only at a low discount rate, flag it as sensitive to cost-of-capital assumptions.
- Always show NPV at multiple discount rates (e.g., WACC, WACC+2%, WACC+5%).

---

## Real vs. Nominal Cash Flows

A common modeling error: mixing real and nominal values in the same analysis. Pick one convention and apply it consistently.

| Convention | Cash Flows | Discount Rate | When to Use |
|---|---|---|---|
| **Nominal** | Include expected inflation in revenue growth, cost escalation, etc. | Use nominal WACC (includes inflation expectations) | Default for most business cases. Easier to tie to budgets, contracts, and reported financials. |
| **Real** | Strip out inflation; express all values in today's purchasing power | Use real WACC (nominal WACC - expected inflation) | Long-horizon analyses (10+ years) where inflation compounds significantly. Infrastructure, energy, real estate. |

**The rule**: nominal cash flows with nominal discount rate, or real cash flows with real discount rate. Never cross them. Mixing nominal cash flows with a real discount rate overstates NPV; mixing real cash flows with a nominal rate understates it.

**Practical guidance**:
- For 3-5 year business cases, use nominal. The inflation distortion is small and nominal is easier for stakeholders to follow.
- For 10+ year analyses, consider real. It keeps the focus on whether the project creates genuine value above inflation.
- When inflation rates differ significantly across cost and revenue lines (e.g., labor inflating at 4% but software costs deflating at 2%), model each line's escalation explicitly in nominal terms rather than applying a blanket inflation rate.
- Always state the assumed inflation rate and its source. A seemingly small difference (2% vs. 4%) compounds dramatically over long horizons.

---

## Foreign Currency Considerations

For multi-country business cases, currency effects can materially alter the economics. Address these explicitly.

**Step 1: Identify Currency Exposure**

Map each cash flow line to its currency denomination:

| Cash Flow Item | Currency | Exposure Type |
|---|---|---|
| Revenue from US customers | USD | Revenue exposure |
| European subsidiary costs | EUR | Cost exposure |
| Manufacturing in China | CNY | Cost exposure |
| Debt service | USD | Financing exposure |

**Step 2: Choose a Modeling Approach**

| Approach | Method | When to Use |
|---|---|---|
| **Constant exchange rate** | Use today's spot rate for all future periods | Simplest. Acceptable for short-horizon cases (1-2 years) or when FX exposure is <10% of total cash flows. Label clearly: "at constant exchange rates." |
| **Forward rates** | Use market forward rates for each future period | Better for 3-5 year cases. Forward rates embed market expectations of currency movements. Source from Bloomberg or central bank data. |
| **Scenario-based** | Model base/upside/downside exchange rate paths | Best for material FX exposure. Show NPV sensitivity to +/-10% and +/-20% currency moves on the dominant exposure. |

**Step 3: Address Key Risks**

- **Translation risk**: Reporting currency impact when consolidating foreign subsidiary results. Affects reported earnings but not necessarily cash flow.
- **Transaction risk**: Actual cash flow impact when revenues and costs are in different currencies. This is the one that matters for business case economics.
- **Natural hedging**: Does the business have offsetting exposures? (e.g., EUR revenues and EUR costs in Europe net out.) Quantify the net exposure after natural offsets.
- **Hedging costs**: If the business hedges FX risk, include the cost (typically 1-3% annually for major currency pairs). Note that hedging removes volatility but not the long-term trend.

**In the analysis**: Show the base case NPV at current exchange rates, then show NPV sensitivity to the top 1-2 currency exposures. Flag if any scenario flips the recommendation from Go to No-Go.

---

## Total Cost of Ownership (TCO)

### Cost Categories

**Direct Costs** (by year): Acquisition, implementation, operation, maintenance, upgrade/replacement. Classify each as capex or opex.

**Indirect Costs**: Training, productivity loss during implementation, support overhead, compliance/certification.

**Hidden Costs** (often missed):
- Data migration and integration
- Dual-running during transition
- Vendor lock-in switching costs
- Technical debt accumulation
- Opportunity cost of internal resources

**TCO Summary**: Total TCO, annualized TCO, cost per user/year, and comparison vs. alternatives.

### When to Use TCO vs. Simple ROI

- **Use TCO** when comparing competing solutions (build vs. buy, vendor A vs. vendor B)
- **Use ROI** when evaluating a single investment against a do-nothing baseline
- **Use both** when the decision involves both "should we do it?" and "how should we do it?"

---

## Advanced Valuation Concepts

### Modified IRR (MIRR)

Standard IRR assumes reinvestment at the IRR rate, which is often unrealistic. MIRR corrects this by specifying:
- **Financing rate**: Cost to fund the project (typically WACC)
- **Reinvestment rate**: Rate earned on interim cash flows (typically cost of capital or a conservative market rate)

Use MIRR when the project has non-standard cash flows (multiple sign changes) or when IRR produces multiple solutions.

### Real-Options Valuation

Traditional NPV undervalues projects with embedded flexibility. Real-options thinking adds value for:
- **Option to expand**: Invest small now, scale up if successful
- **Option to abandon**: Cut losses if early results are poor
- **Option to defer**: Wait for better information before committing
- **Option to switch**: Change inputs, outputs, or technology mid-project

Apply real-options thinking when:
- Investments are staged (especially R&D, pilot programs)
- High-uncertainty environments where flexibility has tangible value
- Platform investments where future use cases are uncertain
- Traditional NPV is negative but "close" and flexibility may tip the balance

Connect to the Phased Investment Structure: a phased approach is how you capture option value in practice.

---

## AI and Technology Investment Modeling

Technology and AI investments have cost and benefit structures that differ from traditional capital projects.

### Cost Patterns
- **Cloud infrastructure**: Operating expense, scales with usage (not fixed capital)
- **Data costs**: Acquisition, cleaning, labeling, storage... often underestimated
- **AI/ML talent**: Scarce and expensive; model as ongoing cost, not one-time
- **Technical debt**: Accumulates if not managed; include remediation budget

### Benefit Patterns
- **Automation savings**: High confidence, easy to quantify
- **Prediction/decision quality**: Medium confidence, model as error-rate reduction
- **Personalization uplift**: Measurable via A/B testing, but adoption curve matters
- **Platform/network effects**: Hard to model precisely; use scenario analysis

### Modeling Guidance
- Separate "proven" benefits (automation) from "speculative" benefits (network effects)
- Use higher discount rates for speculative benefits
- Model adoption curves. AI benefits rarely arrive at full scale in Year 1
- Include a "technology pivot" scenario where the chosen approach needs to change

---

## Forecasting Approach

- **Driver-based forecasting**: Build from operational drivers (units, prices, headcount) rather than top-down growth rates. More transparent and auditable.
- **Growth deceleration**: For high-growth businesses, model explicit deceleration. A 25% growth company at $30M revenue typically decelerates 3-4 percentage points per year as the base grows.
- **Scenario generation**: Consider additional scenarios based on historical variance, not just optimistic/pessimistic.

---

## Recommendation Template

Every financial analysis must end with a recommendation. Use this structure:

**Decision**: Go / No-Go / Conditional Go

**Rationale**: 2-3 sentences tying the recommendation directly to the financial analysis. Lead with the strongest number.

**Conditions** (if conditional):
- What must be true for the recommendation to hold
- Specific thresholds that would change the decision

**Immediate Next Steps**: First 30-90 day actions.

**Decision Reversibility**: What's the cost if we change course after committing? (Sunk cost at each decision point.) This informs whether speed or caution is warranted.

**Timeline/Urgency**: When does the decision need to be made? What triggers urgency (e.g., hardware refresh deadline, competitive window, contract expiration)?

---

## Worked Example: 3-Year Business Case (Abbreviated)

**Prompt**: "Build a business case for a $15M factory automation investment. Expected to reduce labor costs by 30% and improve quality by 15%."

**Interpretation of inputs**: "30% labor cost reduction" interpreted as 30% of $22M annual labor bill = $6.6M/year at run-rate. "15% quality improvement" interpreted as 15% reduction in cost of poor quality ($4.5M COPQ) = $0.68M/year. [Both flagged as placeholder ... validate base figures with client.]

**Financial Summary**: Investment $15.5M (including $0.5M Year 0 setup), NPV $7.5M, IRR 29%, payback 2.5 years.

**Cash flow build**:

| | Year 0 | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|---|---|---|---|---|---|---|
| Labor savings | - | $3.3M | $6.6M | $6.6M | $6.6M | $6.6M |
| Quality savings | - | $0.34M | $0.68M | $0.68M | $0.68M | $0.68M |
| Other benefits | - | $0.2M | $1.2M | $2.1M | $2.1M | $2.1M |
| Investment + ongoing costs | ($15.5M) | ($1.8M) | ($1.8M) | ($1.8M) | ($1.8M) | ($1.8M) |
| **Net cash flow** | **($15.5M)** | **$2.04M** | **$6.68M** | **$7.58M** | **$7.58M** | **$7.58M** |
| PV (10% WACC) | ($15.5M) | $1.85M | $5.52M | $5.69M | $5.18M | $4.71M |
| Cumulative PV | ($15.5M) | ($13.65M) | ($8.13M) | ($2.44M) | $2.74M | $7.45M |

Year 1 labor savings at 50% of run-rate due to phased rollout. Full run-rate from Year 2.

**Key sensitivity**: Labor savings drive ~80% of the NPV. At 20% reduction instead of 30%, NPV drops to $2.6M but remains positive. Quality improvement is valuable but not material to the go/no-go decision.

**Recommendation**: Conditional Go. Invest $5.5M in Phase 1 (one production line). If Phase 1 achieves >25% labor cost reduction over 6 months, commit remaining $9.5M for Lines 2-3. This limits downside to ($1.2M) while preserving full upside.

---

## Key Principles

- The "number" is never the point. The business case supports a decision.
- Finance and strategy must work together. Numbers without story lack impact.
- Sensitivity analysis is more important than precise projections.
- Always stress-test the business case with realistic downside scenarios.
- Present financial outputs in tables, not prose. Tables are auditable; paragraphs of numbers are not.
- Be prepared to explain every assumption.
