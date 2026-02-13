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

### Step 2: Conduct Due Diligence Analysis

Apply the relevant analysis frameworks from the due-diligence skill based on the scope defined in Step 1. Cover each focus area identified, using the skill's detailed templates for:

- **Commercial DD**: Market assessment, customer analysis, revenue quality, competitive position
- **Operational DD**: Process & efficiency, technology DD, management & team assessment
- **Financial DD**: Quality of earnings, working capital, capex, cash flow
- **Strategic DD**: Strategic fit, synergy assessment, competitive positioning, integration complexity
- **Technology & IP DD**: Architecture, technical debt, IP protection, security posture
- **Legal & Regulatory DD**: Litigation, compliance, contract review, data privacy

For each area, document key findings with evidence, risk levels, and source confidence.

### Step 3: Investment Recommendation

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
