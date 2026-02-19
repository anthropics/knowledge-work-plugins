---
description: Develop comprehensive business case with problem statement, solution, financials, and recommendation
argument-hint: "<investment or initiative> <purpose>"
---

# /business-case -- Business Case Development

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Create a comprehensive business case that secures approval and funding for strategic initiatives. Includes problem statement, solution, financial analysis, and recommendation.

## Invocation

```
/business-case [investment or initiative] [purpose]
```

If parameters not provided, ask for:
- Investment or initiative
- Purpose (new investment, process change, technology)
- Available analysis/data
- Target audience (board, steering committee, etc.)

## Workflow

### Step 1: Structure the Business Case

Determine the appropriate structure:

```
## Business Case Structure

### 1. Executive Summary
[1 page max - the "decision brief"]

### 2. Problem Statement
[What problem are we solving?]

### 3. Current State
[Where we are today - with data]

### 4. Future State
[What we'll achieve]

### 5. Options Analysis
[Alternatives considered]

### 6. Recommendation
[What we're proposing]

### 7. Financial Analysis
[The numbers]

### 8. Implementation Plan
[How we'll do it]

### 9. Risks and Mitigations
[What's standing in the way]

### 10. Conclusion
[Summary and call to action]
```

### Step 2: Executive Summary

Create the standalone summary:

```
## Executive Summary

### The Challenge
[1-2 sentences on the problem]

### The Opportunity
[What we can achieve]

### The Investment
$[Total investment]

### The Return
- NPV: $XX
- IRR: XX%
- Payback: X years
- ROI: XX%

### Recommendation
[PROCEED with option X]

### Key Decision Points
- [Decision point 1]
- [Decision point 2]
```

### Step 3: Problem Statement

Define the problem:

```
## Problem Statement

### Current Pain Points
| Pain Point | Impact | Frequency | Priority |
|------------|--------|-----------|----------|
| [Pain 1] | $[Impact] | [Frequency] | [High] |
| [Pain 2] | $[Impact] | [Frequency] | [High] |
| [Pain 3] | $[Impact] | [Frequency] | [Medium] |

### Cost of Inaction
| Factor | Annual Cost |
|--------|-------------|
| [Cost 1] | $X |
| [Cost 2] | $X |
| **Total** | **$X** |

### Root Cause
[What's causing these problems]
```

### Step 4: Current State Assessment

Document baseline:

```
## Current State

### Operational Metrics
| Metric | Current | Industry Benchmark | Gap |
|--------|---------|-------------------|-----|
| [Metric 1] | [Value] | [Benchmark] | [Gap] |
| [Metric 2] | [Value] | [Benchmark] | [Gap] |

### Pain Points
- [Pain point 1 with data]
- [Pain point 2 with data]

### Constraints
- [Constraint 1]
- [Constraint 2]
```

### Step 5: Future State

Describe the target:

```
## Future State

### Vision
[2-3 sentences on what success looks like]

### Expected Outcomes
| Outcome | Current | Target | Improvement |
|---------|---------|--------|-------------|
| [Outcome 1] | [Current] | [Target] | [X%] |
| [Outcome 2] | [Current] | [Target] | [X%] |

### Capabilities Required
- [Capability 1]
- [Capability 2]
```

### Step 6: Options Analysis

Present alternatives:

```
## Options Analysis

### Options Considered

| Option | Description | Investment | NPV | Risk |
|--------|-------------|------------|-----|------|
| A | [Full solution] | $XX | $XX | [Med] |
| B | [Partial solution] | $XX | $XX | [Low] |
| C | [Status quo] | $0 | $0 | [N/A] |

### Recommendation
[Option A] — selected because:
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]
```

### Step 7: Financial Analysis

Build detailed financials:

```
## Financial Analysis

### Investment Required
| Category | Year 0 | Year 1 | Year 2 | Year 3 | Total |
|----------|--------|--------|--------|--------|-------|
| Capital | $X | $X | $X | $X | $X |
| Implementation | $X | $X | $X | $X | $X |
| Training | $X | | | | $X |
| AI/ML infrastructure | $X | $X | | | $X |
| Change management | $X | $X | | | $X |
| **Total** | **$X** | **$X** | **$X** | **$X** | **$X** |

### Benefits Realization
| Benefit | Type | Year 1 | Year 2 | Year 3 | Total |
|---------|------|--------|--------|--------|-------|
| Revenue growth | Top-line | $X | $X | $X | $X |
| Cost reduction | Bottom-line | $X | $X | $X | $X |
| Risk avoidance | Quantified | $X | $X | $X | $X |
| Time savings | Productivity | $X | $X | $X | $X |
| Error reduction | Quality | $X | $X | $X | $X |
| **Total** | | **$X** | **$X** | **$X** | **$X** |

### Return Metrics
| Metric | Value | Threshold | Assessment |
|--------|-------|-----------|------------|
| NPV | $XX | > 0 | [Positive] |
| IRR | XX% | XX% | [Above threshold] |
| Payback | X years | X years | [Within threshold] |
| ROI | XX% | XX% | [Above threshold] |

### AI/Automation Specific Metrics (if applicable)
| Metric | Value | Industry Benchmark |
|--------|-------|-------------------|
| Process automation rate | X% | 60-80% |
| Error reduction | X% | 30-60% |
| Time-to-value | X months | 6-12 months |
| Operational cost reduction | X% | 15-35% |

### Sensitivity Analysis
| Variable | -20% Impact | Base | +20% Impact | Swing |
|----------|-------------|------|--------------|-------|
| Benefits | $XX | $XX | $XX | $XX |
| Costs | $XX | $XX | $XX | $XX |
| Timeline | $XX | $XX | $XX | $XX |
| Adoption rate | $XX | $XX | $XX | $XX |

### Monte Carlo Analysis (if applicable)
- Probability of NPV > 0: [X]%
- 90% confidence interval: $[Low] - $[High]
- Most likely outcome: $[Amount]
- Downside scenario: $[Amount]

### Total Cost of Ownership (TCO)
| Component | Years 1-3 | Years 4-5 | Years 6-10 | Total |
|-----------|-----------|-----------|------------|-------|
| Initial investment | $X | | | $X |
| Ongoing licensing | $X | $X | $X | $X |
| Maintenance | $X | $X | $X | $X |
| Training & support | $X | $X | $X | $X |
| **TCO** | **$X** | **$X** | **$X** | **$X** |

### Breakeven Analysis
- **Minimum benefits to break even**: $X
- **Breakeven point**: [Time period]
- **Risk-adjusted breakeven**: [Time period]
```

### Step 8: Implementation Plan

Outline execution:

```
## Implementation Plan

### Phases

| Phase | Duration | Key Activities | Deliverables |
|-------|----------|----------------|--------------|
| 1 | X weeks | [Activities] | [Deliverables] |
| 2 | X weeks | [Activities] | [Deliverables] |
| 3 | X weeks | [Activities] | [Deliverables] |

### Timeline
[Visual timeline or Gantt]

### Resource Requirements
| Role | FTE | Duration |
|------|-----|----------|
| [Role 1] | X.X | [Time] |
| [Role 2] | X.X | [Time] |

### Dependencies
- [Dependency 1]
- [Dependency 2]
```

### Step 9: Risk Assessment

Document risks:

```
## Risks and Mitigations

### Key Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Mitigation] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Mitigation] |

### Contingency Plans
- [Contingency 1]
- [Contingency 2]
```

## Output Format

Generate complete business case:

1. **Executive Summary** — 1-page decision brief
2. **Problem & Opportunity** — Why this matters
3. **Solution** — What we're proposing
4. **Financial Analysis** — ROI, NPV, IRR, payback
5. **Implementation** — How we'll do it
6. **Risks** — What could go wrong and what we're doing about it

After generating, ask:

> "Would you like me to:
> - Adjust the financial assumptions?
> - Create executive presentation slides?
> - Develop detailed implementation plan?
> - Add scenario analysis for different risk profiles?"

## Notes

- Executive summary must stand alone — it's often the only thing read
- Quantify everything — "significant savings" isn't convincing
- Connect to strategic priorities — why THIS investment now?
- Be realistic about benefits — don't over-promise
- Acknowledge risks — hiding them destroys credibility
- Make the recommendation CLEAR — don't waffle
- Anticipate objections and address them proactively
- Match format to audience — board vs. steering committee vs. sponsor
- For AI/automation investments, include specific automation rates and error reduction metrics
- Consider total cost of ownership over 5-10 years, not just initial investment
- Include change management costs explicitly — they are often underestimated
- Run Monte Carlo analysis for high-stakes investments to show confidence ranges
- Address technical debt and ongoing maintenance in financial projections
