---
description: Apply strategic frameworks including 7S, Growth-Share Matrix, Five Forces, SWOT, PESTLE, and others
argument-hint: "<framework name> <situation context>"
---

# /framework-apply -- Strategic Framework Application

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Apply proven strategic frameworks to structure analysis and develop insights. Includes 20+ frameworks for organizational analysis, portfolio strategy, competitive positioning, and growth planning.

## Invocation

```
/framework-apply [framework name] [situation context]
```

If parameters are not provided, ask for:
- Framework to apply (or recommend based on context)
- Situation/company context
- Available data or key questions

## Workflow

### Step 1: Select Appropriate Framework(s)

Based on the question asked, recommend the best framework. Consider pairing with a complementary framework for deeper analysis -- single-framework analysis often misses important dimensions.

| Question Type | Primary Framework | Complementary Pairing |
|---------------|-------------------|----------------------|
| "How competitive is our industry?" | Five Forces Analysis | + PESTLE or Value Chain |
| "How should we compete?" | Competitive Positioning | + Strategy Canvas or VRIO |
| "How is our organization aligned?" | 7S Framework | + Balanced Scorecard or Digital Maturity |
| "What is our competitive advantage?" | VRIO | + Value Chain or Five Forces |
| "What are our strengths and weaknesses?" | SWOT Analysis | + PESTLE (external) or VRIO (internal) |
| "What external factors affect us?" | PESTLE | + Five Forces or SWOT |
| "How do we grow?" | Ansoff Matrix | + Growth-Share Matrix or Market Entry Framework |
| "How should we allocate resources?" | Growth-Share Matrix | + Nine-Box or Three Horizons |
| "How should we enter a new market?" | Market Entry Framework | + Five Forces or PESTLE |
| "What is our business model?" | Business Model Canvas | + Value Chain or Platform Strategy |
| "How do we create value?" | Value Chain | + Business Model Canvas or Competitive Positioning |
| "How do we measure performance?" | Balanced Scorecard | + 7S Framework or Digital Maturity |
| "How do we leverage AI?" | AI Strategy Framework | + Digital Maturity or Value Chain |

### Step 2: Apply the Selected Framework(s)

Use the framework's analytical structure to assess the situation. For each framework, provide substantive analysis with evidence and reasoning -- not empty templates.

**Available frameworks and what they analyze:**

- **Five Forces** -- Industry attractiveness and competitive intensity across five dimensions: entry threats, buyer power, supplier power, substitutes, and rivalry
- **PESTLE** -- External macro-environment across political, economic, social, technological, legal, and environmental dimensions
- **7S Framework** -- Organizational alignment across seven internal elements: strategy, structure, systems, shared values, style, staff, and skills
- **Growth-Share Matrix** -- Portfolio resource allocation by categorizing business units on market growth and relative market share
- **SWOT** -- Strategic position through internal strengths/weaknesses and external opportunities/threats, with cross-quadrant strategy generation
- **Ansoff Matrix** -- Growth strategy options across four paths: market penetration, product development, market development, and diversification
- **VRIO** -- Competitive advantage sustainability by evaluating resources as valuable, rare, inimitable, and organized
- **Value Chain** -- How value is created across primary and support activities, identifying cost and differentiation sources
- **Three Horizons** -- Balancing short-term optimization (H1), emerging business scaling (H2), and future option creation (H3)
- **Competitive Positioning** -- Strategic choice between cost leadership, differentiation, and focus
- **Nine-Box Matrix** -- Multi-business portfolio prioritization on market attractiveness vs. competitive position
- **Digital Maturity** -- Organizational readiness across digital strategy, customer experience, operations, data, and AI adoption
- **AI Strategy** -- AI opportunity assessment, roadmap, and capability requirements
- **Balanced Scorecard** -- Strategy execution measurement across financial, customer, process, and learning perspectives
- **Business Model Canvas** -- Complete business model mapping across nine building blocks from segments to cost structure
- **Strategy Canvas** -- Competitive differentiation visualization by comparing value curves across industry factors
- **Market Entry Framework** -- Market entry mode evaluation balancing investment, risk, speed, and control
- **Platform Strategy** -- Platform business model design covering network effects, ecosystem mapping, and platform economics

### Step 3: Synthesize Insights

After applying one or more frameworks, synthesize the findings into a unified view:

```
## Framework Analysis Summary

### Key Insights
1. [Primary insight from the analysis]
2. [Secondary insight]
3. [Cross-framework insight -- where findings converge or contradict]

### Blind Spots
- [What the framework(s) did not capture that matters for this situation]

### Implications for [Client/Organization]
- [Strategic implication 1]
- [Strategic implication 2]

### Prioritized Recommendations
1. [Highest-impact recommendation with rationale]
2. [Second recommendation]
3. [Third recommendation]
```

When multiple frameworks were applied, explicitly call out:
- **Converging findings** (high confidence) -- where 2+ frameworks agree
- **Contradictions** (needs judgment) -- where frameworks disagree and why
- **Gaps** -- what no framework captured but context suggests matters

## Output Format

Generate:

1. **Framework Explanation** -- Brief overview of the selected framework(s) and why they fit this question
2. **Completed Analysis** -- Structured framework output with substantive reasoning, not just filled-in placeholders
3. **Key Insights** -- What the analysis reveals, including cross-framework synthesis if multiple were applied
4. **Strategic Implications** -- Prioritized recommendations with clear rationale

After generating, ask:

> "Would you like me to:
> - Apply a complementary framework to deepen this analysis?
> - Explore a specific finding in more detail?
> - Develop an action plan based on these recommendations?
> - Create a visual representation of the analysis?"

## Notes

- Frameworks are TOOLS, not answers -- use them to structure thinking
- Select framework based on the QUESTION, not the other way around
- Pairing frameworks yields richer analysis (e.g., SWOT + PESTLE, Five Forces + Value Chain)
- Customize framework elements to your specific context
- Don't force data into frameworks -- if it doesn't fit, note the gap
- Frameworks should generate INSIGHTS, not just templates filled in
- Quantify wherever possible -- "High" is less useful than "High -- ~$15M revenue risk"
- Apply structured problem decomposition -- mutually exclusive, collectively exhaustive
- Always consider digital/AI implications within any framework
- For digital transformation: consider digital strategy frameworks that address technology adoption, operating model redesign, and capability building
- Modern frameworks increasingly integrate AI/digital considerations into traditional strategy
