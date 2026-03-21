---
name: strategic-analysis
description: Hypothesis-driven problem solving with strategic framework application. Use for MECE decomposition, issue trees, hypothesis development, analytical workplans, root cause analysis, and framework-based strategic analysis (Five Forces, PESTLE, VRIO, SWOT, 7S, Ansoff, BCG Growth-Share, Value Chain, Business Model Canvas, Strategy Canvas, Blue Ocean, competitive positioning). Covers the full arc from problem definition through structured decomposition, prioritization, hypothesis testing, framework application, cross-framework synthesis, and actionable recommendations.
---

# Strategic Analysis

Hypothesis-driven methodology for structuring complex business problems combined with established strategic frameworks as the analytical toolkit. The problem-solving process is the backbone; frameworks are the tools applied within it.

## Before You Begin

Good analysis starts with understanding the actual problem, not assuming one. Before structuring or applying frameworks:

- **Ask clarifying questions.** What exactly is happening? Since when? How is it measured? What is the company, its industry, and approximate scale (revenue, headcount, geography)?
- **Seize on contradictions.** "Costs are rising but headcount is flat" or "NPS is up but revenue is down" are signals, not just facts to accept. Name the tension explicitly and make it a primary hypothesis driver. The most valuable problems to solve are often hiding in the gap between two things that shouldn't both be true.
- **Establish the data landscape.** What data is available vs. what needs to be gathered? Don't fabricate baseline metrics, financial figures, or market data. When illustrating a structure with example numbers, flag them clearly: "Using $X as an illustrative figure to show the math. Replace with actuals."
- **When working without confirmed data**, flag every estimate with its basis and confidence level. Present market sizes, share figures, and growth rates as directional estimates to be validated, not as established facts.

### Two Modes of Operation

- **Structuring mode** (no data provided): Build the issue tree, form hypotheses, select frameworks, design the analytical workplan, and specify what data would prove or disprove each hypothesis. The output is a roadmap for the analysis.
- **Analysis mode** (data provided): Apply frameworks, run the analysis, test hypotheses against the data, synthesize findings, and deliver recommendations. The output is answers.

Default to structuring mode unless the user provides data to analyze. When operating in structuring mode, open with an explicit statement: "Operating in structuring mode since no data has been provided. The output will be a roadmap: issue tree, hypotheses, framework selection, and an analytical workplan specifying what data to collect and how to test each hypothesis." This sets expectations that the deliverable is a plan, not answers.

---

## The Problem-Solving Process

### Step 1: Define the Problem

Before any analysis, rigorously define the problem. Get outcome clarity and constraints upfront.

A good problem definition covers:

- **The Question**: What exactly are we trying to solve? State in one sentence.
- **The Context**: Industry dynamics, company position, timeframe, technology landscape.
- **Quantification**: Size the problem. What is the financial impact of the status quo? What is the value of solving it? Anchor all subsequent prioritization to these numbers. If exact figures aren't available, estimate the order of magnitude.
- **Success Criteria**: What does a successful solution look like? How will we measure it? What are the constraints? What is the decision timeline?
- **Out of Scope**: What are we NOT solving for? What boundaries exist?

**Look for contradictions and tensions in the problem statement.** "Market share declined despite increased marketing spend" contains a tension (more spend should equal more share). "Customer satisfaction scores are high but churn is rising" is another. Name the tension explicitly and make it a primary hypothesis driver.

**Validate the premise before proceeding:**

- Is the data behind this problem statement reliable? How was it measured?
- Is the comparison fair? (Apples-to-apples scope, same definitions, same time periods)
- Is the stated problem actually a problem, or is it a solution looking for justification?
- Are we solving symptoms or root causes?
- What would happen if we did nothing?

### Step 2: Structure the Problem

Apply MECE decomposition (Mutually Exclusive, Collectively Exhaustive) to break the problem into non-overlapping, complete branches.

**Issue tree templates by problem type:**

| Problem Type | Recommended Structure |
|---|---|
| Profitability decline | Revenue (price x volume) + Cost structure |
| Market entry | Market size x Achievable share + Entry requirements |
| Operational inefficiency | Throughput x Yield + Cycle time |
| Customer churn | Acquisition x Retention x Lifetime value |
| Growth strategy | Core business + Adjacent opportunities + Transformational bets |
| Digital transformation | Current state + Capability gaps + Technology options |
| Cost reduction | MECE cost waterfall by value chain stage + overhead |
| Build vs. buy | Strategic fit + Economics (TCO) + Execution risk |
| Pricing strategy | Value to customer + Cost to serve + Competitive positioning |
| Org effectiveness | Structure + Processes + People + Technology |
| M&A evaluation | Strategic rationale + Valuation + Integration feasibility |

**MECE in practice:**

NOT MECE (overlapping):
- North America, Europe, Emerging markets, Developed markets

MECE:
- North America, Europe, Asia-Pacific, Latin America, Middle East & Africa

NOT MECE (inconsistent categories):
- Product revenue, Service revenue, License revenue, Software

MECE:
- Product revenue, Service revenue, License revenue, Other revenue

For digital businesses, consider alternative MECE cuts:
- Recurring revenue (subscriptions, SaaS), Transaction revenue (usage-based, marketplace), Professional services, Ecosystem/partner revenue

#### Which Tree Do You Need?

This is the most common point of confusion in structured problem solving. The diagnostic is simple:

**Ask: "Am I choosing between competing explanations, or breaking a known problem into its parts?"**

| Signal | You Need a... | Why |
|---|---|---|
| "Why is X happening?" with multiple plausible causes | **Hypothesis tree** | You're testing competing theories. The branches are mutually exclusive explanations, and the goal is to eliminate wrong answers. |
| "How do we improve X?" or "What drives X?" | **Logic tree** | You're decomposing a system into its component drivers. The branches coexist (they're all real), and the goal is to find the biggest lever. |
| "Revenue dropped 20% last quarter" | **Hypothesis tree** | Something changed. You need to figure out *what*. Was it pricing? Volume? Mix? Churn? These compete as explanations. |
| "How do we grow revenue by 20%?" | **Logic tree** | You need to map all the ways revenue can grow (price, volume, mix, new products, new segments) and size each lever. |
| You could be wrong about the cause | **Hypothesis tree** | The value is in disproving wrong theories fast. |
| The causes are known; the question is relative magnitude | **Logic tree** | The value is in comprehensive decomposition and prioritization. |

**The mistake**: Using a logic tree when you should be using a hypothesis tree. This happens when someone decomposes "revenue declined" into "price x volume" (logic tree) instead of asking "why did revenue decline?" and generating competing hypotheses (pricing error vs. competitive loss vs. customer churn vs. macro downturn). The logic tree maps the math; the hypothesis tree maps the possible causes. You often need both: the logic tree tells you *where* the problem is (volume dropped), and the hypothesis tree tells you *why* (competing theories about volume loss).

**Hypothesis Tree**

Use when you have competing theories about what's happening. The branches are alternative explanations, and the goal is to eliminate wrong answers quickly.

```
                    [Ultimate Question]

        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   [Hypothesis 1]  [Hypothesis 2]  [Hypothesis 3]
        │               │               │
   ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
   ▼         ▼     ▼         ▼     ▼         ▼
  [Proof 1] [Proof 2] [Proof 1] [Proof 2] [Proof 1] [Proof 2]
        │               │               │
   [Quick Test]    [Quick Test]    [Quick Test]
```

Start with the ultimate question. Branch into competing hypotheses. Under each hypothesis, identify the proof points needed and the quickest way to test them. The key discipline: design a quick test for each hypothesis that could *disprove* it, not just confirm it.

**Logic Tree**

Use when you need to decompose a problem into its component drivers. The branches coexist (they're all real parts of the system), and the goal is to find the biggest lever.

```
                 [Problem Statement]

        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   [Driver A]    [Driver B]     [Driver C]
        │               │
   ┌────┴────┐     ┌────┴────┐
   ▼         ▼     ▼         ▼
 [Factor 1] [Factor 2] [Factor 3] [Factor 4]
        │               │
   [Root Cause]    [Root Cause]
```

Decompose the problem into its causal drivers. Keep branching until you reach actionable root causes. The key discipline: ensure MECE at every level (no overlaps, no gaps).

### Step 3: Prioritize Issues

Not all branches deserve equal attention. Rank branches by estimated impact and data availability.

Use a 2x2 prioritization:

|  | High Data Availability | Low Data Availability |
|---|---|---|
| **High Expected Impact** | Analyze first | Design data collection, analyze in parallel |
| **Low Expected Impact** | Quick scan, move on | Deprioritize |

Decision criteria:
- Where is the biggest lever? (Quantify: "This branch represents ~$Xm of the gap")
- Where is the data available?
- What can we test quickly with minimum viable analysis?
- What is the time sensitivity?

### Step 4: Select Frameworks and Develop Hypotheses

Once the problem is structured, select the right analytical frameworks and form testable hypotheses. Frameworks provide the lens; hypotheses focus the analysis.

#### Framework Selection

Match frameworks to the question being asked. For broad or high-stakes strategic questions, apply two or more frameworks and synthesize across them. For specific, well-defined questions, one framework applied rigorously is better than two applied superficially.

| Question | Primary Framework | Complementary Pairing | Avoid |
|---|---|---|---|
| How attractive is our industry? | Five Forces Analysis | PESTLE, Value Chain | SWOT (not designed for industry-level analysis) |
| How should we compete? | Competitive Positioning | Strategy Canvas, VRIO | Ansoff (growth strategy, not competitive strategy) |
| How is our organization aligned? | 7S Framework | Balanced Scorecard | Five Forces (external, not internal) |
| What is our competitive advantage? | VRIO | Value Chain, Five Forces | SWOT (too generic for advantage analysis) |
| How should we grow? | Ansoff Matrix | Growth-Share Matrix, Three Horizons | VRIO (diagnostic, not prescriptive for growth) |
| What external factors affect us? | PESTLE | Five Forces, SWOT | 7S (internal only) |
| What are our strengths and weaknesses? | SWOT Analysis | PESTLE (external), VRIO (internal) | Growth-Share Matrix (portfolio, not capability) |
| How should we enter a new market? | Market Entry Framework | Five Forces, PESTLE | Balanced Scorecard (performance tracking, not entry) |
| What is our business model? | Business Model Canvas | Value Chain, Platform Strategy | Five Forces (industry, not firm model) |
| How do we create value? | Value Chain | Business Model Canvas, Competitive Positioning | Ansoff (growth paths, not value creation) |
| How do we measure performance? | Balanced Scorecard | 7S Framework | Strategy Canvas (competitive, not performance) |
| How should we allocate resources? | Growth-Share Matrix | Nine-Box, Three Horizons | PESTLE (external context, not allocation) |
| What are our strategic options? | Strategy Canvas | Three Horizons, Ansoff Matrix | Balanced Scorecard (tracking, not option generation) |
| How do we build a platform? | Platform Strategy | Business Model Canvas, Five Forces | 7S (org alignment, not platform design) |

**Redirect framework requests when appropriate.** Clients often request a specific framework by name ("do a SWOT") when a different framework would better answer their actual question. When this happens: (a) acknowledge the request, (b) apply the requested framework, but (c) flag the better-fit framework and explain why. Never refuse the requested framework outright; instead, use it as one of the two required frameworks and pair it with the one that better fits the question.

#### Day 1 Answer

Before any analysis, state your best guess at the final answer based on available information. This is not a commitment. It is a focusing device.

The Day 1 answer should be:
- A complete sentence answering the original question
- Your current confidence level (low/medium/high)
- The 1-2 analyses that would most change your mind

This forces intellectual honesty. If you can't form even a tentative answer, you don't understand the problem well enough.

#### Hypothesis Development

A good hypothesis:
- Is specific and concrete
- Is testable with available data
- Implies a recommended action if proven true
- States "we believe X because Y"
- Has a quick validation path

For each hypothesis, define:
- **Current belief**: What we think is true
- **Evidence needed**: What would prove or disprove it
- **Data source**: Where to find the evidence
- **Quick test**: Fastest way to validate or invalidate
- **If true, then**: What we'd recommend

### Step 5: Conduct Analysis

Structure analysis to test hypotheses, not to generate data for its own sake. Apply selected frameworks to the prioritized branches.

For each analysis workstream, define:
- Which hypothesis it tests
- The analytical method (including which framework)
- Data inputs required
- Expected output and what it tells us

Analytical approaches by situation:

| Situation | Recommended Analysis |
|---|---|
| Profit driver identification | Bridge analysis, variance analysis |
| Market sizing | Top-down, bottom-up, triangulated |
| Competitive assessment | Five Forces, Strategy Canvas, relative positioning |
| Internal capability | VRIO, Value Chain, 7S |
| External environment | PESTLE, Five Forces |
| Financial projections | Scenario modeling, sensitivity analysis |
| Process optimization | Root cause analysis, process mining, time studies |
| Customer insights | Segmentation, cohort analysis, journey mapping |
| Cost gap analysis | Cost bridge/waterfall decomposition |
| Growth strategy | Ansoff Matrix, Three Horizons, Growth-Share |
| Business model | Business Model Canvas, Platform Strategy |

For each analysis, document assumptions, check sensitivity (which inputs matter most), and actively seek disconfirming evidence.

#### Data Confidence Markers

When working without access to proprietary client data or real-time market data:
- Flag estimates with confidence level: "~$30B (industry estimate, +/- 15%)"
- Distinguish between directionally certain and precisely uncertain: "Fee compression is directionally certain; the rate (estimate: 3-5% annually) requires validation"
- Identify the 2-3 data points that, if validated, would most change the recommendations
- Recommend specific data sources the client should validate against (industry reports, internal data, customer research)

### Step 6: Synthesize Findings

Synthesis is NOT summary. Summary says "we found X." Synthesis says "X means Y, which changes our recommendation to Z."

**Lead with the answer (Pyramid Principle):**

1. **The Answer** (1 sentence): Direct response to the original question
2. **Three supporting arguments**: The key reasons behind the answer, ordered by importance
3. **Evidence for each argument**: The specific data that proves each point

#### Cross-Framework Synthesis

When multiple frameworks have been applied, synthesize across them. Individual frameworks provide structure, but the connections between them drive insight.

**External Landscape**
- Industry attractiveness (Five Forces assessment, overall profit potential)
- Key external trends (PESTLE top 3 trends with timeline and impact)
- Competitive dynamics (where is power shifting?)

**Internal Position**
- Organizational alignment (7S assessment, where are the gaps?)
- Competitive advantage (VRIO assessment, what's truly sustainable?)
- Value creation (Value Chain insights, where do we win?)

**Growth Options**
- Current portfolio (Growth-Share assessment)
- Growth strategy (Ansoff recommendation with risk-adjusted view)
- Future pipeline (Three Horizons view, are we investing enough in H2/H3?)

**Cross-Framework Findings**
- **Converging findings**: Where 2+ frameworks agree (high confidence insights)
- **Contradictions**: Where frameworks disagree (requires judgment call, often reveals the most important insight)
- **Blind spots**: What none of the frameworks capture (qualitative factors, culture, timing)
- **Highest-leverage insight**: The single most important finding across all analyses

Look for the non-obvious connection. The most valuable insight from multi-framework analysis is usually where two frameworks, applied independently, point to a conclusion neither would reach alone. State this explicitly: "Five Forces shows X, VRIO shows Y, and together they suggest Z." If cross-framework synthesis only restates what each framework already said, you haven't synthesized... you've summarized.

#### End Each Framework Section with a "So What?"

One to two sentences stating the single most important implication of that framework for the client's decision. Not a summary of findings, but the actionable takeaway.

**Anti-patterns to avoid:**
- "We found many interesting things" (no hierarchy, no answer)
- Restating findings without interpretation
- Burying the answer at the end
- Presenting analysis in the order it was conducted rather than the order that supports the argument
- Confusing "thorough" with "useful" (every finding must connect to the answer)

**Test your synthesis:** Can someone read only the first paragraph and understand the answer and why? If not, restructure.

### Step 7: Develop Recommendations

Translate findings into action. Each recommendation needs:
- **Rationale**: Why this addresses the problem
- **Impact**: Expected outcome, quantified
- **Effort**: Resources required
- **Timing**: When to act (quick wins vs. structural changes)
- **Implementation approach**: How to execute
- **Risks**: What could go wrong and how to mitigate

**Key Risks**

| Risk | Likelihood (H/M/L) | Impact (H/M/L) | Mitigation |
|---|---|---|---|
| [Risk 1] | | | [Action] |
| [Risk 2] | | | [Action] |
| [Risk 3] | | | [Action] |

Identify the "single point of failure": the one risk that could invalidate the entire strategy.

**Implementation Priorities**
- Phase 1 (0-6 months): Quick wins that build momentum and prove the thesis
- Phase 2 (6-18 months): Medium-term capability building
- Phase 3 (18+ months): Long-term strategic positioning

---

## Behavioral Principles

1. **For broad or high-stakes strategic questions, apply at least 2 frameworks** and synthesize across them. For specific, well-defined questions, one framework applied rigorously is better than two applied superficially.
2. **Provide substantive analysis, not empty templates.** For each cell, give 2-3 sentences of reasoning with evidence.
3. **Quantify wherever possible.** Use specific numbers, not vague ratings:
   - Market share: "Competitor A holds ~35% share, representing ~$X.XB revenue"
   - Risk: "Regulatory change probability: ~40%, estimated revenue impact: $XM-$XM"
   - Timing: "Expected market entry window: Q3 2026-Q1 2027 based on [trigger]"
   - Investment: "Required investment: $XM-$XM with X-X year payback period"
4. **Synthesize across frameworks.** Call out where frameworks agree (high confidence), disagree (needs judgment), and what none of them capture (blind spots).
5. **End with prioritized recommendations.** Analysis without action items is incomplete.
6. **State key assumptions explicitly.** When client context is incomplete, list 3-5 assumptions at the top of the analysis. Flag which assumptions most affect the conclusions. Example: "Assumes client revenue is $200-400M (sensitivity: if <$100M, organic build becomes infeasible and acquisition is the only viable entry mode)."
7. **Validate data early.** Before deep analysis, flag the 2-3 data points that most affect the conclusions and recommend the client validate them. Structure as: "Data validation priorities: (1) [data point] ... if this is wrong, [which conclusion] changes. (2) [data point] ... needed to confirm [which recommendation]."

### Output Calibration

Calibrate depth to the use case. Default to working analysis unless the user specifies otherwise.

- **Executive summary** (500-800 words): Key findings from 2-3 frameworks applied briefly. Prioritized recommendations with sizing. No detailed tables.
- **Working analysis** (2,000-4,000 words): Full framework application with tables, cross-framework synthesis, and prioritized recommendations. This is the default.
- **Deep dive** (4,000-8,000 words): Comprehensive multi-framework analysis with detailed evidence per factor, scenario analysis, implementation roadmap, and risk register.

---

## Framework Reference

### External Analysis

#### Five Forces Analysis

**Purpose**: Assess industry attractiveness and competitive intensity.

For each of the five forces (New Entrants, Buyer Power, Supplier Power, Substitutes, Competitive Rivalry):
- Rate the force as High/Medium/Low with a 1-2 sentence justification
- Create a table with columns: Factor | Assessment | Implication
- Include 4-6 factors per force, including digital/platform dimensions (network effects as entry barrier, digital switching costs, platform supplier power, digital substitutes, winner-takes-all dynamics)
- After all five forces, provide an Industry Attractiveness Summary (overall profit potential) and Strategic Implications (how to compete, where to position, how to mitigate unfavorable forces)

**So What?** End with: "This industry is [attractive/unattractive/mixed] for [client] because [specific reason]. The dominant force shaping profitability is [X], which means [strategic implication]."

#### PESTLE Analysis

**Purpose**: Analyze external macro-environmental factors.

For each dimension (Political, Economic, Social, Technological, Legal, Environmental):
- Create a table with columns: Factor | Trend | Impact (H/M/L) | Timeframe (S/M/L) | Strategic Response
- Include 2-4 factors per dimension
- Conclude with Key Trends Summary: the top 3 most significant trends ranked by strategic impact

**So What?** End with: "The external environment is [favorable/hostile/shifting] on a [timeframe]. The single trend most likely to reshape the competitive landscape is [X], requiring [response] within [timeframe]."

#### SWOT Analysis

**Purpose**: Assess strategic position through internal strengths/weaknesses and external opportunities/threats.

Create four tables (Strengths, Weaknesses, Opportunities, Threats) with columns: Factor | Evidence | Strategic Significance (H/M/L). Include 3-5 factors per quadrant, grounded in evidence rather than generic claims. After the four quadrants, generate a Cross-Quadrant Strategy Matrix:
- **SO strategies**: Use strengths to capture opportunities
- **WO strategies**: Address weaknesses to capture opportunities
- **ST strategies**: Use strengths to counter threats
- **WT strategies**: Mitigate weaknesses against threats

Conclude with the 2-3 highest-priority strategic actions.

**So What?** End with: "The strategic position is [strong/vulnerable/mixed]. The highest-leverage move is [SO/WO/ST/WT strategy] because [reason]."

### Internal Analysis

#### 7S Framework

**Purpose**: Assess organizational alignment and capability.

Create two summary tables:
- Hard Elements (Strategy, Structure, Systems) with columns: Element | Current State | Target State | Gap | Priority
- Soft Elements (Shared Values, Style, Staff, Skills) with the same columns

For each of the 7 elements, provide 2-3 current-state observations and key gaps identified.

Conclude with:
- **Alignment Assessment**: Which elements are aligned, which have gaps, implications of misalignment
- **Recommendations**: 3-5 prioritized actions to close gaps

**So What?** End with: "The organization is [aligned/misaligned] on [X]. The most critical gap is [element], which is blocking [strategic objective]."

#### VRIO Framework

**Purpose**: Assess competitive advantage and resource sustainability.

Create a VRIO table with columns: Resource/Capability | Valuable? | Rare? | Costly to Imitate? | Organized to Capture? | Competitive Implication.

Map implications:
- Not Valuable = Competitive Disadvantage
- V only = Competitive Parity
- V+R = Temporary Advantage
- V+R+I+O = Sustained Advantage

Conclude with which resources provide sustained advantage, which need development, and what the imitation barriers are.

**So What?** End with: "[Client] has [N] sources of sustained advantage. The most defensible is [X] because [imitation barrier]. The critical gap is [resource that is V+R but not I or O]."

#### Balanced Scorecard

**Purpose**: Translate strategy into measurable objectives across four perspectives.

For each perspective (Financial, Customer, Internal Process, Learning & Growth), create a table with columns: Objective | Measure | Target | Initiative | Status. Include 3-4 objectives per perspective. Ensure objectives cascade logically: Learning & Growth capabilities enable Internal Process excellence, which drives Customer outcomes, which deliver Financial results.

Conclude with a Strategy Map narrative showing cause-effect linkages and identifying any broken links in the strategy logic.

**So What?** End with: "The strategy logic [holds/breaks] at [perspective]. The broken link is [X], meaning [investment/objective] won't deliver the expected [outcome] without [fix]."

#### Value Chain Analysis

**Purpose**: Understand how value is created in the business.

Create two tables:
- Primary Activities (Inbound Logistics, Operations, Outbound Logistics, Marketing & Sales, Service) with columns: Activity | Description | Value Created | Cost | Competitive Advantage (H/M/L)
- Support Activities (Procurement, Technology, HR, Infrastructure) with the same columns

Conclude with Value Chain Linkages (how activities reinforce each other), Cost Analysis, and Differentiation Sources.

**So What?** End with: "Value creation is concentrated in [activity]. The strongest linkage is between [X] and [Y]. The cost/differentiation trade-off suggests [strategic action]."

### Strategy Formulation

#### Growth-Share Matrix

**Purpose**: Analyze business portfolio and resource allocation.

Create a portfolio table with columns: Business Unit | Market Growth Rate (%) | Relative Market Share | Quadrant (Star/Question Mark/Cash Cow/Dog) | Strategy (Invest/Hold/Harvest/Divest).

Conclude with Portfolio Implications (cash flow dynamics, investment requirements, rebalancing needs) and 3-4 prioritized recommendations.

**So What?** End with: "The portfolio is [balanced/unbalanced]. Cash cows generate ~$XM to fund [Stars/Question Marks]. The critical decision is [invest/divest] on [specific unit]."

#### Ansoff Matrix

**Purpose**: Analyze growth strategies across four paths.

Start with the current position (products, markets, revenue). Then create a summary table with columns: Strategy | Risk Level | Opportunity | Key Consideration.

For each of the four strategies (Market Penetration, Product Development, Market Development, Diversification), assess: approach, opportunity size, risk level, and investment required.

Conclude with Recommended Strategy: primary choice with rationale, secondary option, and investment requirements.

**So What?** End with: "The recommended growth path is [strategy] because [reason], representing ~$XM opportunity at [risk level]. Avoid [strategy] because [reason]."

#### Nine-Box Matrix

**Purpose**: Multi-business portfolio prioritization.

Plot business units on a 3x3 matrix (Market Attractiveness vs. Competitive Position). Create a table with columns: Business Unit | Market Attractiveness (H/M/L) | Competitive Position (H/M/L) | Strategy (Invest/Select/Harvest/Divest). Conclude with investment allocation implications.

#### Three Horizons Model

**Purpose**: Balance short-term and long-term growth.

For each horizon, create an initiative table:
- **H1 (0-12 months)**: Defend and grow core. Columns: Initiative | Impact | Investment | Timeline
- **H2 (1-3 years)**: Nurture emerging businesses. Columns: Initiative | Market Size | Investment | Timeline
- **H3 (3-7+ years)**: Create future options. Columns: Option | Potential | Risk | Investment

Conclude with Investment Allocation (% split across horizons) and Key Risks per horizon.

**So What?** End with: "The current investment split is [X/Y/Z%] across horizons. The portfolio is [over-invested in H1/under-invested in H2-H3]. The most promising H2/H3 bet is [X]."

### Competitive Strategy

#### Competitive Positioning

**Purpose**: Define competitive positioning.

Assess current position across three dimensions (Target Scope, Cost Advantage, Differentiation). Then evaluate each generic strategy (Cost Leadership, Differentiation, Focus) covering: suitability conditions, required capabilities, and key risks.

Conclude with Recommended Strategy: chosen position, rationale, how to achieve, and how to defend.

**So What?** End with: "The winning position is [strategy] because [reason]. The single capability that must be built is [X]. The key risk is [stuck in the middle / competitor imitation / focus trap]."

#### Strategy Canvas

**Purpose**: Visualize competitive differentiation by comparing value curves across key factors.

Identify 6-10 factors the industry competes on (price, quality, features, service, brand, convenience, etc.). Create a table with columns: Competing Factor | Our Company (1-5) | Competitor A (1-5) | Competitor B (1-5) | Industry Average (1-5).

Identify where your curve diverges from competitors (differentiation) and where it converges (parity).

Then create an ERRC (Eliminate-Reduce-Raise-Create) table to define the target value curve:

| Action | Factor | Rationale |
|---|---|---|
| **Eliminate** | [factors to remove entirely] | [why: cost savings, irrelevant to target segment] |
| **Reduce** | [factors to reduce below industry average] | [why: over-served, diminishing returns] |
| **Raise** | [factors to raise above industry average] | [why: underserved need, willingness to pay] |
| **Create** | [new factors not currently competed on] | [why: unmet need, new value source] |

Conclude with Differentiation Assessment and a recommended Target Value Curve.

**So What?** End with: "The blue ocean opportunity is [create/raise X while eliminating/reducing Y], which redefines competition from [current basis] to [new basis]."

### Business Model and Platform

#### Business Model Canvas

**Purpose**: Map and evaluate the complete business model.

Analyze all nine building blocks in a table with columns: Block | Current State | Strengths | Vulnerabilities. The blocks: Customer Segments, Value Propositions, Channels, Customer Relationships, Revenue Streams, Key Resources, Key Activities, Key Partnerships, Cost Structure.

Assess how the blocks reinforce each other. Conclude with:
- **Model Coherence**: Where blocks align vs. conflict
- **Sustainability**: Which blocks are hardest for competitors to replicate
- **Evolution Opportunities**: Where shifts could transform the model

**So What?** End with: "The business model is [coherent/fragmented]. The most vulnerable block is [X] because [reason]. The highest-leverage evolution is [shift]."

#### Market Entry Framework

**Purpose**: Evaluate and select market entry strategies for new geographies or segments.

Assess market attractiveness in a table with columns: Factor | Assessment | Data Source | Implication (covering market size, growth rate, competitive intensity, regulatory barriers, cultural factors).

Evaluate entry modes (organic build, acquisition, joint venture, partnership, licensing, export) in a table with columns: Entry Mode | Investment Required | Risk Level | Speed to Market | Control Level | Recommendation.

Conclude with Recommended Entry Strategy, sequencing, and key success factors.

**So What?** End with: "Enter [market] via [mode] because [reason]. Investment: ~$XM. Break-even: [timeframe]. The go/no-go decision hinges on [single factor]."

#### Platform Strategy

**Purpose**: Assess and design platform-based business models.

**Step 1: Platform Classification**

Identify the platform type. This determines the economics and strategic playbook.

| Platform Type | Core Mechanism | Key Metric | Examples |
|---|---|---|---|
| Marketplace | Matches buyers and sellers | Liquidity (match rate, time-to-match) | Airbnb, Uber, eBay |
| Innovation platform | Enables third-party development | Developer adoption, API calls, app count | iOS, AWS, Salesforce |
| Social platform | Facilitates user interactions | DAU/MAU ratio, engagement, content creation rate | Facebook, Reddit, Discord |
| Data platform | Aggregates data to generate insights | Data volume, data freshness, unique data assets | Bloomberg, Palantir |
| Hybrid | Combines 2+ of the above | Varies by dominant mechanism | Amazon (marketplace + innovation), Google (data + innovation) |

**Step 2: Ecosystem Mapping**

Map participants in a table with columns: Participant Type | Role | Value Created | Value Captured | Incentive to Join | Switching Costs.

**Step 3: Network Effects Analysis**

Network effects are the primary source of platform defensibility. Assess each type:

| Network Effect Type | Description | Strength Assessment | Defensibility |
|---|---|---|---|
| **Same-side (direct)** | More users on one side attract more users on the same side | Strong if users actively recruit others; weak if value doesn't scale with user count | High if strong (hard to leave when your network is there) |
| **Cross-side (indirect)** | More users on one side attract more users on the other side | Strong if both sides see measurable value from the other's growth; weak if one side is indifferent | Medium to high (depends on multi-homing) |
| **Data network effects** | More usage generates more data, which improves the product, which attracts more users | Strong if data genuinely improves the core value prop; weak if improvements plateau | High if the improvement curve hasn't flattened |
| **Content/inventory** | More content/listings attract more consumers, whose demand attracts more content | Strong if supply is fragmented and hard to aggregate elsewhere; weak if supply is concentrated | Medium (content can be multi-homed) |

For each applicable network effect, assess:
- **Current strength**: Is the flywheel actually spinning, or is it theoretical?
- **Inflection point**: At what scale does the network effect become self-sustaining?
- **Diminishing returns**: At what point does adding more users/data stop improving the experience?

**Step 4: Multi-Homing Risk**

Multi-homing (users participating on competing platforms simultaneously) is the single biggest threat to platform economics. Assess:

| Factor | Low Multi-Homing Risk | High Multi-Homing Risk |
|---|---|---|
| Switching costs | High (data, reputation, integrations locked in) | Low (no data portability barriers, easy to join) |
| User investment | Users build profiles, reputations, content | Users are anonymous or transactional |
| Differentiated supply | Exclusive or hard-to-replicate supply | Commodity supply available everywhere |
| Pricing | Users penalized for splitting activity (volume discounts, loyalty rewards) | No cost to participating on multiple platforms |
| Integration depth | Deep workflow/API integrations | Standalone, shallow usage |

If multi-homing risk is high, the platform must compete on execution every transaction, not on lock-in. Strategy shifts from network effects to operational excellence, curation, and trust.

**Step 5: Platform Economics**

Assess the unit economics and monetization model:

- **Subsidized side vs. monetized side**: Which side do you subsidize to build critical mass? What's the subsidy cost and how long until the platform is self-sustaining?
- **Take rate / monetization**: What percentage of value does the platform capture? Sustainable range depends on the platform's value-add (5-15% for distribution; 20-30% for trust, payments, insurance; >30% risks disintermediation).
- **Winner-takes-all dynamics**: Does this market tend toward one dominant platform or can multiple coexist?
- **Margin structure**: Platform businesses often have high gross margins (60-80%+) but require significant investment in growth before profitability. Model the path to contribution margin breakeven by cohort or geography.

**Step 6: Conclusion**

Conclude with:
- **Platform Design**: Governance model (open vs. curated), openness strategy (API access, data sharing), monetization approach
- **Growth Strategy**: How to solve the chicken-and-egg problem (single-player mode, seeding supply, concentrating geographically, marquee partnerships). What is the minimum viable liquidity?
- **Defensibility Assessment**: Which network effects are real vs. theoretical? What is the multi-homing risk? How deep are switching costs?

**So What?** End with: "The platform's defensibility rests on [network effect type]. The critical mass threshold is [X users/transactions]. The biggest risk is [multi-homing/disintermediation/regulation]."

### Market and Competitive Analysis

When conducting market analysis, structure the work in layers:

**Market Sizing**
- Use TAM (Total Addressable Market), SAM (Serviceable Addressable Market), SOM (Serviceable Obtainable Market)
- Triangulate using both top-down and bottom-up approaches
- Distinguish between market size and addressable opportunity
- Document growth rates (historical CAGR and forecast) with drivers
- Apply data confidence markers to all estimates

**Competitive Landscape**
- Map competitors by market share, revenue, growth rate, and positioning
- Profile key competitors on strengths, weaknesses, strategy, and threats
- Assess competitive positioning across dimensions that matter to customers (price, quality, reach, innovation)
- Look for emerging competitors and adjacent-market entrants, not just established players

---

## Common Pitfalls

| Pitfall | Why It's Problematic | Solution |
|---|---|---|
| Defining the problem too broadly | Diffuses analysis, no clear success criteria | Narrow scope iteratively, quantify the problem |
| Skipping the Day 1 answer | Analysis drifts without a point of view | Force a tentative answer before analysis begins |
| Jumping to solutions | Misses root causes | Follow the process: define, structure, hypothesize, then solve |
| Collecting all data | Wastes time on low-value analysis | Prioritize by hypothesis, apply 80/20 |
| Confirming existing beliefs | Biases analysis | Actively seek disconfirming evidence |
| Summarizing instead of synthesizing | No actionable insight | Lead with the answer, then support it |
| Presenting findings without recommendations | Leaves client without action | Always translate findings to actions |
| Applying frameworks mechanically | Empty templates, no insight | Provide substantive reasoning per cell, end each with "So What?" |
| Using one framework alone | Incomplete picture, overfit to one lens | Always pair frameworks, synthesize across them |
| Wrong framework for the question | Misaligned analysis, wasted effort | Use the framework selection guide, redirect when appropriate |

---

## Worked Example

**Prompt**: "Our SaaS company's enterprise churn rate jumped from 8% to 14% last quarter. Help me structure an analysis to understand why and what we should do about it."

### Step 1: Define the Problem

- **Question**: Why did enterprise churn increase from 8% to 14% last quarter, and what can we do to reverse it?
- **Quantification**: A 6-point jump in one quarter is acute (not gradual drift), suggesting a triggering event. At 14% annualized, if average enterprise ACV is $200K and we have 300 enterprise accounts, we're losing ~$8.4M ARR/year vs. ~$4.8M at baseline. The incremental exposure is ~$3.6M ARR.
- **Premise check**: Is 14% calculated consistently with the prior 8%? Same denominator (beginning-of-period accounts)? Same definition of "churn" (logo vs. revenue, gross vs. net)?
- **Success criteria**: Identify the 2-3 root drivers, quantify their contribution, and develop interventions to return churn to <10% within 2 quarters.
- **Out of scope**: SMB/mid-market churn, new logo acquisition, pricing overhaul (unless directly implicated).

### Step 2: Structure (MECE)

This is a "why is X happening?" question with competing plausible causes, so we need a **hypothesis tree** (not a logic tree). Something changed; we need to figure out what.

Three branches (mutually exclusive, collectively exhaustive... every churn event is driven by one of these):

1. **We caused it** (Product/service failures): Feature regressions, support quality decline, CSM turnover
2. **Competitors caused it** (Market shift): New entrant, price undercut, feature parity shift
3. **Customer circumstances changed** (External): Budget cuts, M&A, leadership turnover

### Step 3: Prioritize

| Branch | Expected Impact | Data Availability | Priority |
|---|---|---|---|
| Product/Service | HIGH (most common SaaS churn driver) | HIGH (usage data, tickets, NPS) | Analyze first |
| Competitive | MEDIUM | MEDIUM (win/loss, exit surveys) | Parallel track |
| Customer-side | MEDIUM | LOW (requires outreach) | Quick scan of top 10 churned accounts |

### Step 4: Framework Selection, Day 1 Answer & Hypotheses

**Framework selection**: This is primarily a diagnostic problem (why did churn spike?), but it has a strategic component (how do we compete to retain?). Primary analysis: hypothesis-driven root cause. Complementary framework: **Five Forces** on the competitive dynamics (is buyer power or rivalry shifting?) and **VRIO** on retention capabilities (do we have defensible advantages that should prevent churn?).

**Day 1 answer**: "Enterprise churn spiked because a Q3 product release degraded the enterprise experience, compounded by CSM turnover that left accounts without a relationship anchor during the disruption." Confidence: Medium. The analysis that would most change my mind: usage data overlay with churn timing.

**Hypotheses:**

H1: A product release degraded the enterprise experience.
- Quick test: Overlay churn dates with release dates. Compare support ticket volume in churned vs. retained accounts.

H2: A competitor made a significant move.
- Quick test: Pull exit survey verbatims, count competitor mentions. Apply Five Forces lens: has buyer power shifted?

H3: CSM changes left accounts unanchored.
- Quick test: Compare churn rate for accounts with CSM reassignment vs. stable CSM coverage. Apply VRIO lens: is our CSM capability Valuable and Rare, or is it at parity?

H4: Enterprise customers are cutting vendor spend due to macro pressure.
- Quick test: Check top 10 churned accounts for public signals (layoffs, earnings warnings). PESTLE scan on macro conditions.

### Step 5: Analytical Workplan

| Workstream | Tests | Method | Framework | Timeline |
|---|---|---|---|---|
| Churn cohort analysis | H1-H4 | Segment churned accounts by tenure, size, industry, usage | Root cause decomposition | Week 1 |
| Product usage analysis | H1 | Usage metrics (DAU, feature adoption) in churned vs. retained, 90 days pre-churn | Variance analysis | Week 1 |
| Competitive assessment | H2 | Exit survey verbatims, 5-8 win-back interviews, competitive positioning map | Five Forces, Strategy Canvas | Week 1-2 |
| CSM coverage analysis | H3 | Churn rate by CSM tenure, reassignment events | VRIO on retention capabilities | Week 1 |
| External signal scan | H4 | Cross-reference churned accounts with public filings, layoff news | PESTLE (abbreviated) | Week 1 |

### Step 6: Synthesis (structure, not yet populated)

"Enterprise churn spiked from 8% to 14% because [root cause], accounting for [X%] of the incremental churn. [Secondary driver] contributed [Y%]. We recommend [top 3 actions] to return churn to <10% by [quarter]."

Three supporting arguments would follow, each backed by specific data from the workstreams above.

**Cross-framework synthesis would address:**
- **Converging**: Do Five Forces and VRIO agree on whether the churn is structural (industry shifting) or operational (fixable)?
- **Contradiction**: If VRIO says we have defensible advantages but churn is spiking anyway, the "O" (Organized to Capture) is the weak link.
- **Blind spot**: Neither framework captures relationship/trust dynamics well. The CSM analysis fills this gap.
