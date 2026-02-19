---
description: Build financial models including ROI analysis, business case financials, DCF, and scenario analysis
argument-hint: "<analysis type> <context>"
---

# /financial-analysis -- Financial Analysis and Modeling

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Build comprehensive financial models for investment decisions, business cases, and strategic recommendations. Supports ROI, NPV, IRR, DCF, and scenario analysis.

## Invocation

```
/financial-analysis [analysis type] [context]
```

If parameters not provided, ask for:
- Type of analysis (ROI, business case, DCF, valuation)
- Investment/project context
- Available financial data
- Key assumptions

## Workflow

### Step 1: Define Analysis Type

Select appropriate financial analysis:

| Analysis Type | Use Case | Key Outputs |
|---------------|----------|-------------|
| ROI Analysis | Quick investment assessment | Return %, Payback |
| Business Case | Comprehensive investment case | NPV, IRR, Payback |
| DCF Valuation | Company/business valuation | Enterprise value |
| Scenario Analysis | Risk assessment | Best/Base/Worst case |
| Break-even | Volume analysis | Break-even point |

### Step 2: ROI Analysis

For quick investment assessment:

```
## ROI Analysis: [Investment/Project]

### Investment Summary
| Component | Amount |
|-----------|--------|
| Initial investment | $XX |
| Ongoing investment | $XX/year |
| Project life | X years |

### Benefits
| Benefit | Year 1 | Year 2 | Year 3 | Total |
|---------|--------|--------|--------|-------|
| [Benefit 1] | $X | $X | $X | $X |
| [Benefit 2] | $X | $X | $X | $X |
| **Total Benefits** | **$X** | **$X** | **$X** | **$X** |

### Return Metrics
| Metric | Value | Benchmark | Assessment |
|--------|-------|-----------|------------|
| Simple ROI | [X]% | [Y]% | [Acceptable/Strong] |
| Payback Period | [X] years | [Y] years | [Acceptable/Strong] |
| NPV | $X | >0 | [Positive/Negative] |
| IRR | [X]% | [Cost of capital] | [Above/Below] |

### Sensitivity
| Variable | -10% Impact | +10% Impact |
|----------|--------------|-------------|
| [Variable 1] | [NPV impact] | [NPV impact] |
| [Variable 2] | [NPV impact] | [NPV impact] |
```

### Step 3: Business Case Development

For comprehensive investment cases:

```
## Business Case: [Investment/Project]

### Executive Summary
[2-3 sentences on the investment and recommendation]

### Problem Statement
[What problem does this investment solve?]

### Recommended Solution
[What are we investing in?]

### Financial Summary
| Metric | Value |
|--------|-------|
| Total Investment | $XX |
| NPV (Base case) | $XX |
| IRR | XX% |
| Payback Period | X years |
| ROI | XX% |

### Investment Details
| Cost Category | Year 0 | Year 1 | Year 2 | Year 3 | Total |
|---------------|--------|--------|--------|--------|-------|
| Capital costs | $X | $X | $X | $X | $X |
| Implementation | $X | $X | $X | $X | $X |
| Ongoing Opex | | $X | $X | $X | $X |
| **Total** | **$X** | **$X** | **$X** | **$X** | **$X** |

### Benefit Projections
| Benefit | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 | Total |
|---------|--------|--------|--------|--------|--------|-------|
| Revenue growth | $X | $X | $X | $X | $X | $X |
| Cost reduction | $X | $X | $X | $X | $X | $X |
| Risk mitigation | $X | $X | $X | $X | $X | $X |
| **Total** | **$X** | **$X** | **$X** | **$X** | **$X** | **$X** |

### Cash Flow Analysis
| Year | Cash Flow | Discount Factor | PV |
|------|-----------|-----------------|-----|
| 0 | ($X) | 1.000 | ($X) |
| 1 | $X | 0.909 | $X |
| 2 | $X | 0.826 | $X |
| 3 | $X | 0.751 | $X |
| 4 | $X | 0.683 | $X |
| 5 | $X | 0.621 | $X |
| **NPV** | | | **$X** |

### Assumptions
- [Assumption 1]
- [Assumption 2]
- [Discount rate: X%]
- [Analysis period: X years]

### Sensitivity Analysis
| Scenario | NPV | IRR | Assessment |
|----------|-----|-----|-----------|
| Upside | $X | X% | |
| Base case | $X | X% | |
| Downside | $X | X% | |

### Risks and Mitigations
| Risk | Impact | Likelihood | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | $X | [H/M/L] | [Mitigation] |
| [Risk 2] | $X | [H/M/L] | [Mitigation] |

### Recommendation
[Go/No-Go recommendation with rationale]
```

### Step 4: DCF Valuation (if applicable)

For business/company valuation:

```
## DCF Valuation: [Business/Asset]

### Valuation Summary
| Method | Value |
|--------|-------|
| DCF (Base) | $XX |
| Terminal Value | $XX |
| Enterprise Value | $XX |
| Equity Value | $XX |
| Value per share | $XX |

### Revenue Projections
| Year | Revenue | Growth | EBITDA | Margin |
|------|---------|--------|--------|--------|
| Current | $X | - | $X | X% |
| Year 1 | $X | X% | $X | X% |
| Year 2 | $X | X% | $X | X% |
| Year 3 | $X | X% | $X | X% |
| Year 4 | $X | X% | $X | X% |
| Year 5 | $X | X% | $X | X% |

### Terminal Value
- **Method**: [Gordon Growth / Exit Multiple]
- **Terminal growth rate**: X%
- **Exit multiple**: Xx EBITDA
- **Terminal value**: $XX

### WACC Calculation
| Component | Weight | Cost | WACC Contrib |
|-----------|--------|------|--------------|
| Debt | X% | X% | X% |
| Equity | X% | X% | X% |
| **WACC** | | | **X%** |

### Valuation Sensitivity
| | Terminal Growth -1% | Base | Terminal Growth +1% |
|---|---|---|---|
| WACC -1% | $XX | $XX | $XX |
| Base WACC | $XX | $XX | $XX |
| WACC +1% | $XX | $XX | $XX |
```

### Step 5: Scenario Analysis

For risk assessment:

```
## Scenario Analysis: [Investment/Project]

### Scenario Definitions
| Scenario | Description | Probability |
|----------|-------------|-------------|
| Upside | [Optimistic assumptions] | X% |
| Base | [Most likely assumptions] | X% |
| Downside | [Conservative assumptions] | X% |

### Scenario Comparison
| Metric | Upside | Base | Downside |
|--------|--------|------|----------|
| Revenue | $X | $X | $X |
| Costs | $X | $X | $X |
| NPV | $X | $X | $X |
| IRR | X% | X% | X% |
| Payback | X yrs | X yrs | X yrs |

### Probability-Weighted
| Scenario | NPV | Probability | Weighted NPV |
|----------|-----|-------------|--------------|
| Upside | $X | X% | $X |
| Base | $X | X% | $X |
| Downside | $X | X% | $X |
| **Expected NPV** | | | **$X** |

### Break-even Analysis
- **Break-even revenue**: $X
- **Break-even volume**: X units
- **Margin of safety**: X%
```

## Output Format

Generate:

1. **Analysis Summary** — Key metrics and recommendation
2. **Financial Model** — Detailed projections
3. **Sensitivity Analysis** — What affects outcomes most
4. **Risk Assessment** — Scenario analysis
5. **Recommendation** — Go/No-Go with rationale

After generating, ask:

> "Would you like me to:
> - Build a detailed Excel model?
> - Run additional scenarios?
> - Develop alternative funding options?
> - Create an investment memo for stakeholders?"

## Notes

- Always show your assumptions — financial models are only as good as their inputs
- Perform sensitivity analysis — know what drives value
- Scenario analysis is essential, not optional
- Connect financial analysis to strategic rationale
- Use appropriate discount rates — cost of capital matters
- Be conservative with assumptions — avoid over-optimism on growth rates and cost savings
- Be realistic about benefits — "stretch goals" aren't baseline
- Consider tax and financing impacts
- Document caveats and limitations explicitly
- Use probability-weighted scenarios to capture uncertainty
