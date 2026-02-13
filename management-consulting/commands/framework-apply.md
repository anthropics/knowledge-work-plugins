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
- Framework to apply (or let recommend based on context)
- Situation/company context
- Available data or key questions

## Workflow

### Step 1: Select Appropriate Framework

Based on the question asked, recommend the best framework:

| Question Type | Recommended Frameworks |
|---------------|----------------------|
| "How is our organization aligned?" | 7S Framework |
| "How should we allocate resources?" | Growth-Share Matrix, GE Matrix |
| "How competitive is our industry?" | Five Forces Analysis |
| "What are our strengths and weaknesses?" | SWOT Analysis |
| "What external factors affect us?" | PESTLE |
| "How do we grow?" | Ansoff Matrix |
| "How do we create value?" | Value Chain |
| "What is our competitive strategy?" | Competitive Positioning Framework |
| "How do we measure performance?" | Balanced Scorecard |
| "What is our business model?" | Business Model Canvas |

### Step 2: Apply the Selected Framework

#### 7S Framework

```
## 7S Analysis: [Organization]

### Framework Overview
Seven internal elements that must be aligned for organizational effectiveness:

| Element | Description | Current State | Target State | Gap |
|---------|-------------|---------------|--------------|-----|
| Strategy | How we compete | [Current] | [Target] | [Gap] |
| Structure | Organizational design | [Current] | [Target] | [Gap] |
| Systems | Processes and IT | [Current] | [Target] | [Gap] |
| Shared Values | Culture and norms | [Current] | [Target] | [Gap] |
| Style | Leadership approach | [Current] | [Target] | [Gap] |
| Staff | People and capabilities | [Current] | [Target] | [Gap] |
| Skills | Core competencies | [Current] | [Target] | [Gap] |

### Insights
- [Key alignment insight 1]
- [Key alignment insight 2]
- [Recommendations to close gaps]
```

#### Growth-Share Matrix

```
## Growth-Share Matrix: [Portfolio]

### Framework Overview
Categorizes business units based on market growth and relative market share:

| Business Unit | Market Growth | Relative Share | Quadrant | Strategy |
|---------------|---------------|----------------|----------|----------|
| [Unit 1] | [High/Low] | [High/Low] | [Star/Cash Cow/Question Mark/Dog] | [Strategy] |
| [Unit 2] | [High/Low] | [High/Low] | [...] | [...] |

### Portfolio Implications
- **Stars**: [Invest to grow]
- **Cash Cows**: [Harvest profits]
- **Question Marks**: [Invest or divest]
- **Dogs**: [Divest or liquidate]

### Recommendations
- [Portfolio rebalancing recommendation]
```

#### Five Forces Analysis

```
## Five Forces Analysis: [Industry]

### Framework Overview
Analyzes competitive intensity and profitability of an industry:

| Force | Strength | Key Factors | Implications |
|-------|----------|-------------|--------------|
| Threat of New Entrants | [H/M/L] | [Barriers to entry] | [Impact on profitability] |
| Bargaining Power of Buyers | [H/M/L] | [Buyer concentration] | [Impact on pricing] |
| Bargaining Power of Suppliers | [H/M/L] | [Supplier concentration] | [Impact on costs] |
| Threat of Substitutes | [H/M/L] | [Substitute availability] | [Impact on demand] |
| Competitive Rivalry | [H/M/L] | [Number of competitors] | [Impact on margins] |

### Industry Attractiveness
[Overall assessment of industry profitability]

### Strategic Implications
- [How to compete in this industry]
- [Where to position]
```

#### SWOT Analysis

```
## SWOT Analysis: [Organization/Opportunity]

### Strengths (Internal, Positive)
| Strength | Impact | Sustainability |
|----------|--------|----------------|
| [S1] | [High/Med] | [High/Med] |
| [S2] | [High/Med] | [High/Med] |

### Weaknesses (Internal, Negative)
| Weakness | Impact | Remediation |
|----------|--------|-------------|
| [W1] | [High/Med] | [How to address] |
| [W2] | [High/Med] | [How to address] |

### Opportunities (External, Positive)
| Opportunity | Attractiveness | Probability |
|-------------|----------------|-------------|
| [O1] | [High/Med] | [High/Med] |
| [O2] | [High/Med] | [High/Med] |

### Threats (External, Negative)
| Threat | Likelihood | Impact | Mitigation |
|--------|------------|--------|------------|
| [T1] | [High/Med] | [High/Med] | [Response] |
| [T2] | [High/Med] | [High/Med] | [Response] |

### Strategic Implications
- [SO strategies: leverage strengths to capture opportunities]
- [WO strategies: address weaknesses to pursue opportunities]
- [ST strategies: use strengths to mitigate threats]
- [WT strategies: minimize weaknesses to avoid threats]
```

#### PESTLE Analysis

```
## PESTLE Analysis: [Industry/Market]

### Framework Overview
Analyzes external factors affecting the organization:

| Factor | Trend | Impact | Timeframe |
|--------|-------|--------|-----------|
| **Political** | | | |
| [Factor] | [Trend] | [H/M/L] | [Short/Med/Long] |
| **Economic** | | | |
| [Factor] | [Trend] | [H/M/L] | [Short/Med/Long] |
| **Social** | | | |
| [Factor] | [Trend] | [H/M/L] | [Short/Med/Long] |
| **Technological** | | | |
| [Factor] | [Trend] | [H/M/L] | [Short/Med/Long] |
| **Legal** | | | |
| [Factor] | [Trend] | [H/M/L] | [Short/Med/Long] |
| **Environmental** | | | |
| [Factor] | [Trend] | [H/M/L] | [Short/Med/Long] |

### Key Trends
1. [Most significant trend]
2. [Second significant trend]

### Strategic Implications
- [How to respond to trends]
```

### Step 3: Synthesize Insights

After framework application:

```
## Framework Analysis Summary

### Key Insights
1. [Insight from framework 1]
2. [Insight from framework 2]
3. [Cross-cutting insight]

### Implications for [Client]
- [Strategic implication 1]
- [Strategic implication 2]

### Recommended Next Steps
- [Next analysis needed]
- [Preliminary recommendation]
```

## Output Format

Generate:

1. **Framework Explanation** — Brief overview of the framework
2. **Completed Analysis** — Structured framework output
3. **Key Insights** — What the analysis reveals
4. **Strategic Implications** — What to do with insights

After generating, ask:

> "Would you like me to:
> - Apply a different framework to this situation?
> - Combine multiple frameworks for deeper analysis?
> - Develop recommendations based on the framework output?
> - Create a visual representation of the analysis?"

## Notes

- Frameworks are TOOLS, not answers — use them to structure thinking
- Select framework based on the QUESTION, not the other way around
- Combine frameworks for richer analysis (e.g., SWOT + PESTLE)
- Customize framework elements to your specific context
- Don't force data into frameworks — if it doesn't fit, note the gap
- Frameworks should generate INSIGHTS, not just templates filled in
- Apply structured problem decomposition — mutually exclusive, collectively exhaustive
- For digital transformation: consider digital strategy frameworks that address technology adoption, operating model redesign, and capability building
- Modern frameworks increasingly integrate AI/digital considerations into traditional strategy
