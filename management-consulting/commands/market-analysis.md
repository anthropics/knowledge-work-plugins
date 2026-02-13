---
description: Conduct comprehensive market and competitive analysis including industry research, market sizing, competitive landscape, and positioning. Use when researching new markets, developing strategy, preparing for competitive response, or assessing market opportunity.
argument-hint: "<industry or market> <focus areas>"
---

# /market-analysis -- Market and Competitive Analysis

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Conduct integrated market and competitive analysis combining industry research with competitive intelligence. Provides the foundation for strategic recommendations.

## Invocation

```
/market-analysis [industry or market] [focus areas]
```

If parameters not provided, ask for:
- Industry or market to analyze
- Geographic scope
- Specific focus (market size, competitive positioning, trends)
- Purpose (strategy, market entry, investment)

## Workflow

### Step 1: Define Analysis Scope

Determine what to analyze:

```
## Analysis Scope

### Market Definition
- Primary sector: [Industry]
- Sub-sectors: [Sub-sector 1], [Sub-sector 2]
- Related sectors: [Related industry]

### Geographic Scope
- [Global / Regional / Country-specific]

### Competitive Scope
- Direct competitors: [List]
- Indirect competitors: [List]
- Potential new entrants: [List]

### Focus Areas
| Area | Priority | Data Sources |
|------|---------|--------------|
| Market sizing | High | Industry reports, company data |
| Competitive analysis | High | Public filings, websites |
| Trends | Medium | Research, news |
| Customer insights | Medium | Reviews, surveys |
```

### Step 2: Conduct Market Analysis

Analyze market dynamics:

```
## Market Analysis: [Industry]

### Market Size
| Metric | Value | Year | Source |
|--------|-------|------|--------|
| TAM | $X | Current | [Report] |
| SAM | $X | Current | [Calculation] |
| SOM | $X | Current | [Estimation] |

### Growth Trends
| Period | CAGR | Driver |
|--------|------|--------|
| Historical | X% | |
| Forecast | X% | |

### Market Drivers
| Driver | Impact | Timeline |
|--------|--------|----------|
| [Driver 1] | [High/Med/Low] | [Short/Med/Long] |
| [Driver 2] | [High/Med/Low] | [Short/Med/Long] |

### Market Constraints
| Constraint | Impact | Mitigation |
|------------|--------|------------|
| [Constraint 1] | | |
```

### Step 3: Conduct Competitive Analysis

Analyze the competitive landscape:

```
## Competitive Landscape: [Industry]

### Competitive Map
| Company | Share | Revenue | Growth | Positioning |
|---------|-------|---------|--------|-------------|
| [Competitor 1] | X% | $X | X% | [Position] |
| [Competitor 2] | X% | $X | X% | [Position] |
| [Target] | X% | $X | X% | [Position] |

### Competitive Forces
| Force | Strength | Key Factors |
|-------|----------|--------------|
| rivalry | [High/Med/Low] | |
| substitutes | [High/Med/Low] | |
| new entrants | [High/Med/Low] | |
| supplier power | [High/Med/Low] | |
| buyer power | [High/Med/Low] | |

### Competitive Positioning
| Dimension | Us | Competitor A | Competitor B |
|-----------|----|--------------|---------------|
| Price | [Position] | [Position] | [Position] |
| Quality | [Position] | [Position] | [Position] |
| Reach | [Position] | [Position] | [Position] |
| Innovation | [Position] | [Position] | [Position] |

### Competitor Profiles
| Aspect | [Competitor 1] | [Competitor 2] |
|--------|----------------|-----------------|
| Strengths | | |
| Weaknesses | | |
| Strategy | | |
| Threats | | |
```

### Step 4: Synthesize Insights

Generate strategic implications:

```
## Strategic Implications

### Market Opportunities
| Opportunity | Size | Timing | Fit |
|-------------|------|--------|-----|
| [Opportunity 1] | $X | [When] | [High/Med/Low] |

### Market Threats
| Threat | Likelihood | Impact | Mitigation |
|--------|------------|--------|------------|
| [Threat 1] | | | |

### Competitive Advantages
| Capability | Us | Competitor A | Sustainable? |
|------------|----|--------------|---------------|
| [Capability] | [Yes/No] | [Yes/No] | [Why] |

### Strategic Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]
```

## Output Format

Generate:

1. **Market Overview** — Size, growth, drivers
2. **Competitive Landscape** — Map, positioning, forces
3. **Opportunity Assessment** — Market gaps, timing
4. **Strategic Implications** — Recommendations

After generating, ask:

> "Would you like me to:
> - Deep dive into a specific competitor?
> - Build a SWOT analysis?
> - Develop competitive response scenarios?"

## Notes

- Triangulate market size estimates using top-down and bottom-up approaches
- Distinguish between market size (TAM/SAM/SOM) and addressable opportunity
- Competitive analysis should focus on capabilities, not just market share
- Look for emerging competitors, not just established players
- Customer insights are as important as industry data
- Refresh analysis regularly — markets shift faster than reports update
- Use primary research to validate secondary data where possible
- Consider adjacent markets and substitution threats
- Quantify findings wherever possible — specificity builds credibility
