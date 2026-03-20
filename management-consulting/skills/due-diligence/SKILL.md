---
name: due-diligence
description: Conduct commercial, operational, and strategic due diligence for M&A, investment, or partnership decisions. Use when assessing acquisition targets, investment opportunities, vendor evaluations, or any situation requiring rigorous business assessment and risk identification.
---

# Due Diligence

Assess business opportunities through rigorous analytical frameworks. This covers commercial, operational, financial, strategic, and technology due diligence, from scoping the engagement through risk synthesis and investment recommendation.

## Before You Begin

If the user hasn't provided key inputs, ask for them rather than fabricating deal details:
- What is the target company, its industry, and approximate size (revenue, headcount)?
- What is the transaction type (acquisition, PE investment, partnership, vendor assessment)?
- What financial data is available (actuals, management accounts, data room access)?
- Present assessment thresholds (e.g., customer concentration flags, cash conversion benchmarks) as general guidelines, not absolute rules. When using numbers the user didn't provide, flag them: "I'm assuming X based on [typical range for this deal type]. Please confirm or provide actuals."

## DD Types and When to Use Them

| DD Type | Core Question | Focus Areas |
|---------|---------------|-------------|
| Commercial | Can we win? | Market position, customers, growth, competitive dynamics |
| Operational | Can we run it? | Processes, systems, people, efficiency, scalability |
| Financial | Is it real? | Revenue quality, working capital, cash flow, projections |
| Strategic | Should we do it? | Strategic fit, synergies, integration, cultural compatibility |
| Technology & IP | Is it viable? | Architecture, technical debt, IP ownership, security |
| Legal & Regulatory | Is it clean? | Litigation, compliance, contracts, data privacy |

Most transactions require at least commercial, operational, and financial DD. The mix depends on the deal.

## Phase 1: Scope Definition

Define the boundaries before doing any analysis. Unfocused DD wastes time and misses what matters.

### Transaction Context

Establish:
- **Transaction type**: Acquisition, PE investment, strategic partnership, vendor assessment, internal assessment
- **Target**: Company name, industry, size
- **Deal value**: Estimated range
- **Timeline**: How much time for DD
- **Access**: Data room contents, management availability, ability to speak with customers/suppliers
- **Team**: Who's doing the work, what expertise is available

### Focus Area Prioritization

| Area | Priority | Key Questions | Data Available? |
|------|----------|---------------|-----------------|
| Market | High/Med/Low | What must we understand about the market? | Y/N |
| Customers | High/Med/Low | What must we understand about the customer base? | Y/N |
| Operations | High/Med/Low | What must we understand about how the business runs? | Y/N |
| Financials | High/Med/Low | What must we validate about the numbers? | Y/N |
| Technology | High/Med/Low | What must we understand about the tech stack? | Y/N |
| Legal/Regulatory | High/Med/Low | What risks need legal review? | Y/N |

Prioritize ruthlessly. Focus on what could kill the deal or materially change the price.

## Phase 2: Information Gathering

### Standard Information Request List

**Corporate:**
- Articles of incorporation
- Board minutes (last 2 years)
- Organizational charts
- Shareholder agreements
- Material contracts and amendments

**Financial:**
- Audited financials (3-5 years)
- Monthly management accounts (last 24 months)
- Revenue by segment, product, geography, customer
- Cash flow statements
- Debt schedules and covenant compliance
- Budget vs. actual analysis (last 2 years)
- Tax returns and outstanding tax positions

**Commercial:**
- Customer list with revenue by customer (last 3 years)
- Contract templates and key customer contracts
- Pricing history and discount schedules
- Sales pipeline and win/loss data
- Customer churn data and reasons
- NPS or customer satisfaction data

**Operational:**
- Process documentation for key workflows
- Technology systems inventory
- Key vendor list with spend and contract terms
- Headcount by function, level, tenure
- Capacity utilization data
- Quality metrics and incident history

**Technology:**
- Architecture diagrams
- Technical debt assessment (if available)
- Security audit results
- IP portfolio (patents, trademarks, trade secrets)
- Open-source dependency audit
- Development team metrics (deploy frequency, incident response)

**Legal:**
- Pending or threatened litigation
- Regulatory filings and compliance status
- Material contract summary
- Insurance policies
- Data privacy compliance documentation
- FCPA/anti-bribery compliance program documentation (see FCPA/Anti-Corruption section)
- ESG reports, sustainability commitments, and environmental liabilities (see ESG section)

### Minimum Viable DD Request (Time-Constrained)

When time is short (PE secondary, small bolt-on, compressed timeline), request these first. They cover 80% of deal-critical information in 20% of the volume.

**Tier 1 (request immediately, review first)**:
- Last 2 years audited financials + trailing 12 months management accounts
- Revenue by customer (top 20 customers, 3 years)
- Customer churn/retention data
- Org chart + headcount by function
- Material contracts summary (top 10 by value)
- Pending litigation summary

**Tier 2 (request immediately, review after Tier 1)**:
- Monthly revenue and gross margin detail (24 months)
- Sales pipeline and bookings data
- Key vendor contracts
- Technology architecture overview (1-pager)
- Cap table and shareholder agreements

**Tier 3 (request if time permits or red flags emerge)**:
- Full data room contents per standard list above

The goal is to identify deal-killers and major valuation issues within 5-7 business days. Anything that survives Tier 1 and Tier 2 review without red flags is likely worth the full DD investment.

## Phase 3: Analysis

### Commercial Due Diligence

#### Market Assessment

| Metric | Finding | Source | Confidence |
|--------|---------|--------|------------|
| Total addressable market (TAM) | $ | Industry reports, bottom-up analysis | H/M/L |
| Target's market share | % | Company data vs. market estimates | H/M/L |
| Market growth rate (CAGR) | % | Historical trend, analyst consensus | H/M/L |
| Market position | #X of Y competitors | Competitive analysis | H/M/L |

Key questions: Is the market growing or shrinking? Is growth structural or cyclical? What disruption risks exist? How defensible is the target's position?

#### Customer Analysis

| Metric | Finding | Risk Level | Trend |
|--------|---------|------------|-------|
| Top 10 customer concentration | % of revenue | H/M/L | Improving/Stable/Worsening |
| Average contract value | $ | | Direction |
| Net revenue retention (NRR) | % | Above/Below 100% | Direction |
| Gross churn rate | % | vs. industry benchmark | Direction |
| Logo churn rate | % | Segment comparison | Direction |
| Average contract duration | months | vs. industry | Direction |

Customer concentration above 20% in top 3 customers is a yellow flag; above 40% is a red flag, as a general rule of thumb, though significance depends on contract duration, switching costs, and industry norms. NRR below 100% means the installed base is shrinking, the business must sell faster than it leaks.

#### Revenue Quality

| Metric | Finding | Assessment |
|--------|---------|------------|
| Recurring vs. one-time revenue | % recurring | Strong (>80%) / Moderate (50-80%) / Weak (<50%) (illustrative bands; vary significantly by industry. SaaS businesses typically target >90% recurring; project-based businesses may have structurally lower recurring percentages.) |
| Revenue recognition risks | Assessment | H/M/L |
| Backlog / committed revenue | $ | Coverage ratio vs. plan |
| Pricing power | Assessment | Expanding / Stable / Eroding |
| Cross-sell / upsell as % of new ACV | % | Growing or declining |

#### Competitive Position

| Factor | Target | Comp A | Comp B | Assessment |
|--------|--------|--------|--------|------------|
| Market share | % | % | % | Position and trajectory |
| Pricing | $ | $ | $ | Premium / Par / Discount |
| Differentiation | Claim | Claim | Claim | Sustainable? |
| Win rate vs. competitors | % | — | — | Strong / Weak |

#### Unit Economics (SaaS and Subscription Businesses)

For recurring revenue businesses, unit economics are the most revealing lens on business quality. A growing SaaS company can look healthy on a P&L while burning cash on unprofitable customer acquisition.

| Metric | Finding | Benchmark | Assessment |
|--------|---------|-----------|------------|
| Customer acquisition cost (CAC) | $ | Varies by segment | Blended and by channel |
| CAC payback period | months | <18 months (good), <12 months (strong) | Including gross margin |
| Lifetime value (LTV) | $ | Based on gross margin and churn | By segment if possible |
| LTV:CAC ratio | X:1 | >3:1 (healthy), >5:1 (strong or underinvesting) | By segment |
| Gross margin | % | >70% (SaaS), >50% (managed services) | By revenue type |
| Rule of 40 | Revenue growth % + EBITDA margin % | >40% (strong) | Trajectory matters more than snapshot |
| Burn multiple | Net burn / net new ARR | <1.5x (efficient), >2x (concern) | For pre-profit companies |
| Magic number | Net new ARR / prior quarter S&M spend | >0.75 (efficient), <0.5 (inefficient) | Sales efficiency indicator |

**CAC calculation notes**: Fully loaded CAC includes sales and marketing salaries, commissions, marketing spend, sales tools, and allocated overhead. Many companies understate CAC by excluding components. Always ask for the build-up.

**LTV calculation**: LTV = (Average revenue per account * Gross margin %) / Annual churn rate. Use logo churn for conservative estimate, revenue churn for optimistic. For businesses with strong expansion revenue, net revenue retention can substitute for the churn component: LTV = (ARPA * Gross margin %) / (1 - NRR).

**LTV:CAC by segment**: Blended LTV:CAC can mask problems. Enterprise segment might be 5:1 while SMB is 1.5:1. If growth strategy depends on SMB expansion, the blended number is misleading.

#### Cohort Analysis (SaaS and Subscription Businesses)

Cohort analysis is the single most revealing analysis for subscription businesses. It shows the true behavior of customer groups over time, cutting through the aggregation that makes topline metrics look better than reality.

**Revenue cohort analysis**: Group customers by signup quarter. For each cohort, track cumulative revenue retention at 3, 6, 12, 18, 24 months.

| Cohort | Month 0 (ARR) | Month 6 | Month 12 | Month 18 | Month 24 |
|--------|--------------|---------|----------|----------|----------|
| Q1 2023 | $1.0M | 95% | 88% | 82% | 78% |
| Q2 2023 | $1.2M | 93% | 85% | 79% | — |
| Q3 2023 | $1.4M | 90% | 81% | — | — |
| Q4 2023 | $1.6M | 87% | — | — | — |

What to look for:
- **Improving cohorts over time**: Later cohorts retaining better = product-market fit improving, or better customer targeting. Bullish.
- **Deteriorating cohorts**: Later cohorts retaining worse = possible growth at the expense of quality, or market saturation forcing the company downmarket. Bearish.
- **Revenue retention above 100%**: Expansion revenue exceeding churn within cohorts. Strong signal for pricing power and product stickiness.
- **Cliff patterns**: Sharp drop at a specific month (e.g., Month 12) often indicates annual contract non-renewals. Check contract terms.
- **Cohort shape divergence**: If early cohorts show a different retention curve than recent ones, something structural changed. Investigate.

**Logo cohort analysis**: Same structure but tracking customer count instead of revenue. Divergence between logo and revenue cohorts reveals whether you're losing small customers (less concerning) or large ones (very concerning).

### Operational Due Diligence

#### Process and Efficiency

| Area | Finding | Risk | Improvement Potential |
|------|---------|------|---------------------|
| Capacity utilization | % | H/M/L | Assessment |
| Key process bottlenecks | Findings | H/M/L | Assessment |
| Automation level | % | H/M/L | Assessment |
| Quality metrics | Findings | H/M/L | Assessment |

#### Technology Assessment

| Area | Finding | Risk | Detail |
|------|---------|------|--------|
| Architecture scalability | Assessment | H/M/L | Can it support 3-5x growth? |
| Technical debt | Quantified estimate | H/M/L | Remediation cost and timeline |
| IP ownership and protection | Status | H/M/L | Patents, trade secrets, licenses |
| Security posture | Assessment | H/M/L | Last audit, certifications, incidents |
| Data architecture | Findings | H/M/L | Quality, governance, portability |
| Open-source dependencies | Audit status | H/M/L | License compliance, security |
| Development velocity | Metrics | H/M/L | Deploy frequency, lead time, MTTR |
| Cloud infrastructure | Status | H/M/L | Provider, costs, lock-in risk |

#### Management and Team Assessment

| Dimension | Finding | Risk | Detail |
|-----------|---------|------|--------|
| Leadership depth | Assessment | H/M/L | Bench strength below C-suite |
| Key person dependencies | Names/roles | H/M/L | Single points of failure |
| Succession planning | Status | H/M/L | Documented plans, readiness |
| Track record | Performance history | H/M/L | Delivery on past commitments |
| Cultural assessment | Findings | H/M/L | Values, decision-making, adaptability |
| Retention risk | Assessment | H/M/L | Turnover trends, engagement, comp benchmarking |
| Organizational structure | Assessment | H/M/L | Efficiency, spans of control, layers |

Management assessment often predicts post-deal success better than financial analysis. A mediocre business with a strong team outperforms a strong business with a mediocre team.

#### Management Interview Guide

Management interviews are where you test the narrative against reality. The data room tells you what happened; interviews reveal why, and whether leadership understands their own business.

**Core questions (ask every management team)**:
1. Walk me through how you win a new customer, from first contact to signed contract. What's your typical sales cycle? (Tests: process maturity, self-awareness about go-to-market)
2. Which customers have you lost in the last 12 months, and why? (Tests: honesty, customer understanding. Red flag: "We don't really lose customers" when churn data says otherwise)
3. What are the 2-3 things that keep you up at night about this business? (Tests: self-awareness, strategic thinking. Red flag: "Nothing, business is great")
4. If you had an extra $5M to invest in the business, where would you put it? (Tests: growth understanding, capital allocation thinking)
5. Tell me about a time something went significantly wrong operationally. What happened and what did you change? (Tests: learning orientation, operational resilience)
6. Who are your key people, and what happens if any of them leave? (Tests: talent awareness, succession planning, key person risk)
7. How do you set prices, and when was the last time you raised them? (Tests: pricing sophistication, competitive position)

**SaaS-specific questions**:
8. Walk me through your cohort economics. How has CAC payback evolved over the last 2 years? (Tests: unit economics understanding)
9. What percentage of your revenue comes from customers who've been with you more than 2 years? (Tests: retention quality)
10. What's your product roadmap, and how much of it is customer-requested vs. market-driven? (Tests: product strategy, customer dependency)

**Triangulation technique**: Ask the same factual question of multiple team members separately. Compare answers. Consistent answers build confidence. Divergent answers on factual matters (market size, competitive position, churn reasons) indicate either poor internal communication or deliberate narrative management.

**Red flags in management responses**:
- Inability to discuss unit economics or cohort metrics (for a data-driven business)
- Blaming external factors for all negative trends
- Defensive response to straightforward questions about customer losses or operational failures
- Answers that contradict data room documents
- Excessive preparation and scripting (often indicates PE coaching that may mask genuine understanding)
- "Trust me" or "You'll see when you talk to customers" in response to data requests

### FCPA / Anti-Corruption Due Diligence

Critical for any cross-border deal, and increasingly scrutinized in domestic transactions involving government-adjacent customers.

| Area | What to Assess | Red Flags |
|------|---------------|-----------|
| Compliance program | Written anti-bribery policy, training records, reporting hotline, designated compliance officer | No written policy, no training records, compliance function reports to legal (conflict of interest) |
| Third-party intermediaries | Agents, distributors, consultants in high-risk jurisdictions; commission structures | Unusually high commissions (>15-20%), agents with no clear business rationale, payments to shell companies or personal accounts |
| Government touchpoints | Government customers, permits/licenses, state-owned enterprise relationships | Revenue concentration in government contracts without documented procurement processes |
| Payment patterns | Cash payments, payments to jurisdictions that don't match contract geography, split invoicing | Payments routed through intermediary jurisdictions, round-number payments with no supporting documentation |
| Historical issues | Prior investigations, self-disclosures, settlements | Any DOJ/SEC history is a major risk factor; successor liability can attach to acquirers |

**Key principle**: Under the FCPA and UK Bribery Act, acquiring companies can inherit liability for the target's past conduct. DD is not optional for cross-border deals. If the target operates in Transparency International's bottom-third countries, FCPA DD should be Tier 1 priority.

### ESG Due Diligence

ESG DD has moved from "nice to have" to required for most institutional investors, many strategic acquirers, and any deal involving European targets (CSRD, EU Taxonomy).

| Dimension | Key Questions | Valuation Impact |
|-----------|--------------|-----------------|
| Environmental | Emissions profile and reduction commitments? Environmental liabilities (contamination, remediation)? Carbon-intensive assets at risk of stranding? Regulatory exposure (carbon pricing, emissions caps)? | Remediation liabilities are direct price adjustments. Carbon-intensive assets may face accelerated depreciation. |
| Social | Labor practices and supply chain labor risk? DEI metrics and litigation history? Community relations and social license to operate? Health and safety record? | Labor violations create regulatory and reputational risk. Poor H&S records signal operational issues. |
| Governance | Board composition and independence? Executive compensation alignment with long-term value? Related-party transactions? Whistleblower mechanisms? | Governance gaps are often symptoms of deeper operational problems. |

**Practical approach**: Don't boil the ocean. Focus ESG DD on (1) material financial exposures (environmental liabilities, pending regulation), (2) reputational risks that could affect customer retention or talent acquisition, and (3) alignment with the acquirer's own ESG commitments and reporting obligations. If the acquirer has net-zero commitments, the target's emissions profile directly affects the consolidated position.

### Financial Due Diligence

#### Quality of Earnings

| Item | Reported | Adjusted | Adjustment Reason |
|------|---------|---------|-------------------|
| Revenue | $ | $ | Non-recurring items, timing differences |
| EBITDA | $ | $ | One-time costs, owner compensation, related-party transactions |
| Net income | $ | $ | Normalizing adjustments |

The gap between reported and adjusted EBITDA tells you how much the seller is dressing up the numbers. Adjustments exceeding 20% of reported EBITDA warrant extra scrutiny, as a general guideline, though significance depends on the nature of adjustments and business type (owner-operated businesses routinely require larger adjustments).

#### Organic Growth Isolation (Roll-Ups and Serial Acquirers)

For businesses that have grown by acquisition, reported revenue growth is misleading. You need to separate organic growth from acquired growth.

**Organic growth = same-store revenue growth / prior year same-store revenue.** "Same-store" means entities owned for the full comparable period in both years.

| Metric | Calculation | What It Reveals |
|--------|------------|-----------------|
| Reported revenue growth | (Current year total revenue - Prior year total revenue) / Prior year total revenue | Total growth including acquisitions. Often impressive but uninformative. |
| Organic revenue growth | (Current year same-store revenue - Prior year same-store revenue) / Prior year same-store revenue | The underlying growth engine. This is what survives when acquisitions stop. |
| Acquisition contribution | Reported growth - Organic growth | How dependent the growth story is on M&A. |

**If management can't provide the same-store split, flag it as a data quality concern.** This is a basic metric for any serial acquirer. Inability to produce it suggests either poor integration of financial systems or reluctance to show the organic number. Either is a problem.

**Red flags in roll-up DD**: organic growth below industry average (the platform is buying growth, not creating it), declining organic growth over successive periods (integration is consuming management attention), and no margin improvement in acquired entities post-integration (no operational value-add from the platform).

#### Working Capital

| Component | Current | Trend | Seasonal Pattern | Cash Impact |
|-----------|---------|-------|-----------------|-------------|
| Accounts receivable | $ (X days) | Direction | Pattern | $ |
| Accounts payable | $ (X days) | Direction | Pattern | $ |
| Inventory | $ (X days) | Direction | Pattern | $ |
| Net working capital | $ | Direction | Pattern | Funding need |

Working capital is where deals get renegotiated. Establish a normalized working capital figure and tie the purchase price to it. Seasonal businesses require month-by-month analysis.

**Capital-intensive service businesses** (staffing, consulting, facilities management, outsourced services): The cash conversion cycle creates material risk that doesn't show up in standard working capital ratios. The core dynamic is weekly payroll out, 45-60 day receivables in. A fast-growing staffing firm can be profitable on paper while running out of cash. Model the payroll-to-collection gap explicitly, stress-test it against revenue growth scenarios, and assess whether existing credit facilities can fund the gap at scale.

#### Capital Expenditure

| Category | Historical (3-year avg) | Forecast | Maintenance vs. Growth |
|----------|------------------------|----------|----------------------|
| Category 1 | $/yr | $/yr | Split |
| Category 2 | $/yr | $/yr | Split |

Distinguish maintenance capex (required to keep the business running) from growth capex (investment in expansion). Underinvestment in maintenance capex flatters short-term earnings but creates a liability.

#### Cash Flow

| Metric | Year -2 | Year -1 | Current | Trend |
|--------|---------|---------|---------|-------|
| Operating cash flow | $ | $ | $ | Direction |
| Free cash flow | $ | $ | $ | Direction |
| Cash conversion (FCF/EBITDA) | % | % | % | Direction |

Cash conversion below 70% needs explanation, for established, asset-light businesses. Capital-intensive industries may have structurally lower conversion. Common culprits: growing working capital, high capex, or earnings quality issues.

## Phase 4: Risk Assessment

### Risk Categorization

**Critical risks (deal killers)** — Issues that could make the deal unviable:

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk description | H/M/L | H/M/L | What can be done |

Examples: undisclosed litigation, regulatory non-compliance, fraud indicators, irreplaceable key person with no retention plan, market in structural decline.

**Major risks (deal adjustments)** — Issues that materially affect valuation or deal terms:

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk description | H/M/L | H/M/L | What can be done |

Examples: customer concentration, technical debt requiring significant remediation, management gaps, integration complexity.

**Minor risks (price adjustments)** — Issues that affect value but are manageable:

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk description | H/M/L | H/M/L | What can be done |

Examples: operational inefficiencies (often upside opportunities), minor compliance gaps, below-market compensation structures.

### Red Flag Indicators

Watch for these, any one of them warrants deeper investigation:

- Revenue acceleration in the run-up to sale (pulling revenue forward)
- Unusual changes in accounting policies or estimates
- Customer concentration increasing while being presented as "diversified"
- Key employees departing in the months before the transaction
- Capital expenditure declining while revenue grows (underinvestment)
- Working capital trends diverging from revenue trends
- Related-party transactions at non-market terms
- Gaps or inconsistencies between management presentations and data room documents
- Reluctance to provide access to customers or key employees

Red flags are not necessarily deal killers. They're signals to investigate further. Sometimes the explanation is benign. Sometimes it changes the deal.

## Phase 5: Synthesis and Recommendation

### Investment Thesis

Frame the deal in terms of:
1. **What makes this attractive** — the strategic rationale and value creation opportunity
2. **What could go wrong** — the key risks and their mitigations
3. **What the deal is worth** — implied valuation given the findings

### Bridging DD Findings to Valuation

DD findings should directly inform valuation methodology selection and multiple adjustments. Every material finding translates to a valuation impact.

**How DD findings affect valuation approach**:

| DD Finding | Valuation Impact | Mechanism |
|------------|-----------------|-----------|
| High revenue quality (>80% recurring, strong NRR) | Higher multiple | Supports premium to peer multiples. Revenue predictability reduces risk premium. |
| Customer concentration (>30% in top 3) | Lower multiple or earn-out structure | Discount to peers, or structure portion of consideration as earn-out tied to customer retention. |
| Strong unit economics (LTV:CAC >4:1) | Higher multiple | Validates growth investment. Each dollar of S&M spend generates predictable returns. |
| Deteriorating cohorts | Lower multiple | Recent customers are less valuable than historical averages suggest. Adjust revenue projections downward. |
| Technical debt requiring >$2M remediation | Direct price adjustment | Deduct estimated remediation cost from enterprise value. |
| Key person dependency (no succession plan) | Retention package + price adjustment | Cost of retention packages deducted from price. Remaining risk discounts the multiple. |
| Operational inefficiency (below-benchmark margins) | Can increase or decrease value | If acquirer can fix: upside (value creation). If structural: margin risk (discount). |
| Regulatory risk | Escrow or indemnity | Don't discount the price; structure protection through escrow, indemnity, or reps & warranties. |

**Multiple adjustment framework**: Start with comparable company median multiple. Apply adjustments:

| Factor | Adjustment | Rationale |
|--------|------------|-----------|
| Growth premium/discount | +/- 1-3x | Revenue growth vs. peer median |
| Margin premium/discount | +/- 0.5-1.5x | EBITDA margin vs. peer median |
| Revenue quality | +/- 0.5-2x | Recurring %, NRR, contract duration |
| Market position | +/- 0.5-1x | #1-2 vs. #4-5 in category |
| Customer risk | - 0.5-2x | Concentration, churn, cohort trends |
| Management quality | +/- 0.5-1x | Track record, depth, PE readiness |
| Net adjustment | Sum | Implied target multiple vs. peer median |

### Recommendation Format

```
## Due Diligence Summary: [Target]

### Investment Thesis
[One paragraph: why this deal makes sense or doesn't]

### Key Strengths
1. [Strength with evidence]
2. [Strength with evidence]

### Key Concerns
1. [Concern with evidence and mitigation]
2. [Concern with evidence and mitigation]

### Risk Assessment
| Category | Risk Level | Key Risks |
|----------|------------|-----------|
| Commercial | H/M/L | [Risks] |
| Operational | H/M/L | [Risks] |
| Financial | H/M/L | [Risks] |
| Strategic | H/M/L | [Risks] |
| Technology | H/M/L | [Risks] |

### Valuation Implications
| Factor | Adjustment |
|--------|------------|
| Revenue quality adjustments | +/-$ or % |
| Customer risk discount | -$ or % |
| Operational improvement upside | +$ or % |
| Integration costs | -$ |
| Net adjustment | $ or % |

### Recommendation
[PROCEED / PROCEED WITH CONDITIONS / DO NOT PROCEED]

### Conditions Precedent (if proceeding)
1. [Condition — rationale]
2. [Condition — rationale]

### Next Steps
1. [Action — owner — timeline]
2. [Action — owner — timeline]
```

## Integration Assessment (M&A Context)

When DD is for an acquisition, integration planning starts during DD, not after close.

### Integration Complexity

| Area | Complexity | Timeline | Key Dependencies | Cost Estimate |
|------|-----------|----------|-----------------|---------------|
| Systems integration | H/M/L | Months | Dependencies | $ |
| Organization integration | H/M/L | Months | Dependencies | $ |
| Customer migration | H/M/L | Months | Dependencies | $ |
| Process harmonization | H/M/L | Months | Dependencies | $ |
| Culture integration | H/M/L | Months | Dependencies | $ |

### Synergy Quantification

| Synergy | Type | Year 1 | Year 2 | Year 3 | Confidence | Risk |
|---------|------|--------|--------|--------|------------|------|
| Revenue synergy | Revenue | $ | $ | $ | H/M/L | Timing risk |
| Cost synergy 1 | Cost | $ | $ | $ | H/M/L | Execution risk |
| Cost synergy 2 | Cost | $ | $ | $ | H/M/L | Execution risk |

Cost synergies are generally more reliable than revenue synergies. Revenue synergies take longer to materialize and depend on customer behavior you can't fully control. Revenue synergies typically warrant significant haircuts. The appropriate discount depends on synergy type, execution confidence, and acquirer track record.

### Day 1 Readiness

- Communication plan for employees, customers, vendors
- Interim operating model defined
- Key talent retention packages in place
- Regulatory approvals obtained
- IT systems access and continuity plan
- Customer-facing team briefed and scripted

## PE Investment Context

When conducting DD for a PE investment (buyout, growth equity, or add-on acquisition), the frame shifts from "should we buy this?" to "can we create value and exit profitably?"

### 100-Day Plan Structure

The 100-day plan bridges DD findings to value creation execution. Draft it during DD, refine it pre-close, execute from Day 1.

**Days 1-30: Stabilize and Assess**
- Confirm DD findings with full data access (post-close you get everything)
- Retain key talent (sign retention agreements, clarify roles, address uncertainty)
- Establish reporting cadence and KPI dashboards
- Identify and address any "Day 1 surprises" (issues that weren't visible in DD)
- Quick wins: implement 2-3 low-effort improvements identified during DD

**Days 31-60: Design and Prioritize**
- Finalize value creation plan with prioritized initiatives
- Size each initiative: revenue impact, cost impact, investment required, timeline
- Assign initiative owners and establish accountability structure
- Begin recruiting for identified management gaps
- Launch strategic pricing review (often the fastest path to margin improvement)

**Days 61-100: Launch and Execute**
- Kick off top 3-5 value creation initiatives
- Establish board reporting format and governance rhythm
- Complete first monthly operating review with new KPI framework
- Validate or adjust year 1 financial plan based on first 60 days of actuals
- Finalize technology roadmap and investment timeline

### Exit Scenario Analysis

Model three exit scenarios at entry to establish return expectations and inform hold period strategy.

| Scenario | Revenue at Exit | EBITDA at Exit | Exit Multiple | Enterprise Value | Equity Value | IRR | MOIC |
|----------|----------------|----------------|---------------|-----------------|-------------|-----|------|
| Bull | $ | $ | X.Xx | $ | $ | % | X.Xx |
| Base | $ | $ | X.Xx | $ | $ | % | X.Xx |
| Bear | $ | $ | X.Xx | $ | $ | % | X.Xx |

**Key assumptions to stress-test**:
- Revenue growth rate: What if growth is 50% of plan?
- Margin expansion: What if operational improvements deliver half the expected margin gain?
- Exit multiple: What if multiples compress by 2-3 turns from entry?
- Hold period: What if exit takes 6-7 years instead of 4-5?

**PE-specific DD questions**:
- Management incentive alignment: Is the team properly incentivized for a PE hold period? Do equity arrangements align with value creation and exit timeline?
- Add-on acquisition pipeline: Are there bolt-on targets that could accelerate growth or expand capabilities?
- PE readiness of the management team: Can they operate with PE-level reporting, governance, and performance expectations?
- Prior PE ownership: If the business has been PE-owned before, what was done and what's left to do?

## Context Adaptation

Adapt the DD approach based on the deal context:

| Context | Emphasis |
|---------|----------|
| **M&A** | Synergy assessment, integration complexity, valuation adjustments, Day 1 readiness |
| **PE Investment** | Value creation levers, exit scenarios, management incentive alignment, 100-day plan |
| **Strategic Partnership** | Capability complementarity, cultural fit, governance model, IP sharing terms |
| **Vendor Assessment** | Operational reliability, financial stability, contractual protections, business continuity |
| **Internal Assessment** | Capability gaps, improvement priorities, investment needs (drop M&A terminology) |

## Working Principles

- **Focus on materiality.** Prioritize issues that could kill the deal or change the price by more than 5%. Don't spend equal time on everything.
- **Triangulate everything.** Management tells one story. The data room tells another. Customers and suppliers tell a third. The truth is somewhere in the overlap.
- **Red flags are negotiation tools, not always walk-away signals.** A customer concentration risk discovered in DD becomes a price adjustment or an earn-out structure.
- **Document all assumptions and limitations.** What you couldn't verify is as important as what you confirmed. Future you (or the lawyer) will need to know.
- **Connect findings to valuation.** Every DD finding should translate to "and that means the deal is worth more/less/the same because..." (See Bridging DD Findings to Valuation section.)
- **Start integration planning during DD.** The information you gather during DD is the foundation for the integration plan. Don't throw it over the wall and start fresh.
- **Operational DD reveals upside.** Financial DD finds problems. Operational DD often finds improvement opportunities, inefficiencies the acquirer can fix, capabilities the acquirer can scale.
- **Talk to customers and suppliers when possible.** Management representations are necessary but insufficient. External validation changes the picture more often than you'd expect.
