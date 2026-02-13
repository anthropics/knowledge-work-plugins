---
description: Conduct commercial, operational, or strategic due diligence for M&A or investment decisions
argument-hint: "<target company> <due diligence type>"
---

# /due-diligence -- Due Diligence

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Execute comprehensive due diligence to assess investment opportunities. Supports commercial, operational, and strategic due diligence for M&A, private equity, or strategic investments.

## Invocation

```
/due-diligence [target company] [due diligence type]
```

If parameters not provided, ask for:
- Target company/organization
- Type of due diligence (commercial, operational, strategic)
- Deal context (acquisition, investment, partnership)
- Available data sources

## Workflow

### Step 1: Define Due Diligence Scope

Determine the focus area:

| DD Type | Focus | Key Questions |
|---------|-------|---------------|
| Commercial | Market position, customers, growth | Can we win? |
| Operational | Processes, systems, efficiency | Can we run it? |
| Strategic | Fit with strategy | Should we do it? |
| Financial | Historical performance, projections | Is it real? |
| Technical | Technology, IP | Is it viable? |

### Step 2: Commercial Due Diligence

For market and customer assessment:

```
## Commercial Due Diligence: [Target Company]

### Market Position
- **Market share**: [X]%
- **Share trend**: [Growing/Stable/Declining]
- **Competitive position**: [Leader/Challenger/Niche]

### Revenue Analysis
| Revenue Stream | % of Total | Growth | Sustainability |
|----------------|------------|--------|----------------|
| [Stream 1] | X% | X% | [High/Med/Low] |
| [Stream 2] | X% | X% | [High/Med/Low] |

### Customer Analysis
| Metric | Value | Assessment |
|--------|-------|------------|
| # Customers | X | |
| Top 10 concentration | X% | [High/Med/Low risk] |
| Retention rate | X% | [Strong/Weak] |
| NPS/CSAT | X | [Strong/Weak] |

### Customer Deep Dive
| Customer | Revenue | Contract Terms | Renewal History |
|----------|---------|----------------|-----------------|
| [Customer 1] | $X | [Terms] | [History] |
| [Customer 2] | $X | [Terms] | [History] |

### Growth Sustainability
- **Historical growth**: [X]% CAGR
- **Growth drivers**: [What drove growth]
- **Future growth**: [Can it continue?]

### Market Opportunity
- **TAM**: $XXB
- **SAM**: $XXB
- **SOM**: $XXB
- **Growth rate**: X% CAGR

### Key Findings & Risks
| Finding | Impact | Mitigant |
|---------|--------|----------|
| [Finding 1] | [H/M/L] | [Mitigant] |
| [Finding 2] | [H/M/L] | [Mitigant] |
```

### Step 3: Operational Due Diligence

For process and efficiency assessment:

```
## Operational Due Diligence: [Target Company]

### Operational Performance
| Metric | Target | Actual | Gap |
|--------|--------|--------|-----|
| [Metric 1] | [Benchmark] | [Actual] | [Gap] |
| [Metric 2] | [Benchmark] | [Actual] | [Gap] |

### Process Assessment
| Process | Efficiency | Scalability | Assessment |
|---------|------------|--------------|------------|
| [Process 1] | [H/M/L] | [H/M/L] | [Assessment] |
| [Process 2] | [H/M/L] | [H/M/L] | [Assessment] |

### Technology Assessment
| System | Criticality | Health | Investment Needed |
|--------|-------------|--------|-------------------|
| [System 1] | [High] | [Good/Poor] | [High/Med/Low] |
| [System 2] | [Medium] | [Good/Poor] | [High/Med/Low] |

### Organizational Assessment
| Dimension | Assessment | Notes |
|-----------|------------|-------|
| Headcount | [Appropriate/Over/Under] | |
| Skill levels | [Assessment] | |
| Key person risk | [High/Med/Low] | |
| Culture | [Assessment] | |

### Cost Structure
| Cost Category | % Revenue | Benchmark | Assessment |
|---------------|-----------|-----------|------------|
| COGS | X% | X% | [High/Low] |
| Opex | X% | X% | [High/Low] |

### Operational Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Mitigation] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Mitigation] |
```

### Step 4: Strategic Due Diligence

For strategic fit assessment:

```
## Strategic Due Diligence: [Target Company]

### Strategic Fit Assessment

#### With Acquirer Strategy
| Dimension | Fit | Rationale |
|-----------|-----|-----------|
| [Strategic pillar] | [High/Med/Low] | [Rationale] |
| [Strategic pillar] | [High/Med/Low] | [Rationale] |

#### Synergy Assessment
| Synergy Type | Potential Value | Realizability | Confidence |
|--------------|------------------|---------------|------------|
| Revenue | $X | [High/Med/Low] | [High/Med/Low] |
| Cost | $X | [High/Med/Low] | [High/Med/Low] |
| Strategic | Qualitative | [High/Med/Low] | [High/Med/Low] |

### Competitive Positioning
- **Current position**: [Assessment]
- **Post-acquisition position**: [Assessment]
- **Sustainability**: [Assessment]

### Integration Complexity
| Dimension | Complexity | Notes |
|-----------|------------|-------|
| Technology | [High/Med/Low] | |
| Culture | [High/Med/Low] | |
| Operations | [High/Med/Low] | |
| Customer | [High/Med/Low] | |

### Strategic Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [H/M/L] | [Mitigation] |
| [Risk 2] | [H/M/L] | [Mitigation] |
```

### Step 5: Investment Recommendation

Synthesize findings:

```
## Due Diligence Summary: [Target Company]

### Investment Thesis
[What makes this investment attractive]

### Key Findings

#### Strengths
- [Strength 1]
- [Strength 2]

#### Concerns
- [Concern 1]
- [Concern 2]

### Risk Assessment
| Category | Risk Level | Key Risks |
|----------|------------|-----------|
| Commercial | [H/M/L] | [Risks] |
| Operational | [H/M/L] | [Risks] |
| Strategic | [H/M/L] | [Risks] |

### Valuation Implications
- **Pre-deal valuation**: $XX
- **Adjustments for findings**: [+$X/-$X]
- **Adjusted valuation**: $XX

### Recommendation

| Factor | Assessment | Weight | Score |
|--------|------------|--------|-------|
| Market | [Strong/Weak] | X% | [Score] |
| Business | [Strong/Weak] | X% | [Score] |
| Operations | [Strong/Weak] | X% | [Score] |
| Strategic | [Strong/Weak] | X% | [Score] |
| **Total** | | **100%** | **[X/100]** |

**Recommendation**: [PROCEED / PROCEED WITH CAUTION / DO NOT PROCEED]

### Conditions Precedent
- [Condition 1]
- [Condition 2]
```

## Output Format

Generate:

1. **Executive Summary** — Key findings and recommendation
2. **Due Diligence Report** — Detailed findings by area
3. **Risk Register** — Key risks with mitigants
4. **Valuation Adjustments** — Impact on value
5. **Investment Memo** — Go/No-Go recommendation

After generating, ask:

> "Would you like me to:
> - Deep-dive on a specific due diligence area?
> - Build a detailed financial model?
> - Develop integration playbooks?
> - Create a post-deal value creation plan?"

## Notes

- Due diligence is about CONFIRMING, not just finding — validate assumptions
- Red flags are opportunities to NEGOTIATE, not always walk away
- Look for surprises — what would change your recommendation?
- Connect findings to valuation and deal terms
- Document everything — legal implications
- Don't over-rely on management representations
- Talk to customers and suppliers if possible
- Consider "ask" vs. "tell" — what can they tell you vs. what won't they tell you
- Include talent/culture due diligence — key value creation lever in PE
- Use AI and data analytics for pattern recognition in large data sets
- Cross-functional approach essential — commercial, operational, financial, tech, talent
