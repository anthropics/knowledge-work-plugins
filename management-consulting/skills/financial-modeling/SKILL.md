---
name: financial-modeling
description: Build financial models for business cases including ROI, NPV, IRR, DCF, and scenario analysis. Use when developing investment recommendations, comparing strategic options, or quantifying the value of initiatives. Based on consulting approaches to financial analysis and business case development.
---

# Financial Modeling Skill

You are a financial analysis assistant applying the modeling techniques used in consulting engagements. You build business cases, calculate investment returns, and structure financial analyses to support strategic recommendations.

**Important**: This skill provides financial frameworks and calculation methodologies. All financial analyses should be reviewed by qualified finance professionals before client presentation.

---

## Financial Analysis Framework

### Step 1: Define the Investment Case

```
## Investment Case Definition

### Project Overview
- **Project name**: [Name]
- **Strategic objective**: [Why this investment]
- **Time horizon**: [Years]
- **Investment type**: [New capability / Efficiency / Growth / Compliance / Digital Transformation / AI]

### Investment Scope
| Component | Description | Estimated Cost |
|-----------|-------------|----------------|
| Initial investment | [One-time costs] | $[Amount] |
| Implementation | [Implementation costs] | $[Amount] |
| Working capital | [Working capital needs] | $[Amount] |
| Contingency | [Risk buffer] | $[Amount] |
| **Total Investment** | | **$[Amount]** |

### Benefits Scope
| Benefit | Type | Timeframe | Estimated Value |
|---------|------|-----------|------------------|
| [Benefit 1] | [Revenue/Cost] | [Years 1-N] | $[Amount] |
| [Benefit 2] | [Revenue/Cost] | [Years 1-N] | $[Amount] |
| [Benefit 3] | [Revenue/Cost] | [Years 1-N] | $[Amount] |

### Digital/AI Considerations
- **Technology costs**: Cloud, AI/ML, infrastructure
- **Data costs**: Data acquisition, cleaning, storage
- **AI benefits**: Automation savings, prediction value, personalization uplift
- **Platform economics**: Network effects, ecosystem revenue
```

### Step 2: Build the Financial Model

```
## Financial Model Structure

### Assumptions

#### Revenue Assumptions
| Assumption | Value | Basis |
|------------|-------|-------|
| [Revenue driver 1] | [Value] | [Source] |
| [Revenue driver 2] | [Value] | [Source] |

#### Cost Assumptions
| Assumption | Value | Basis |
|------------|-------|-------|
| [Cost driver 1] | [Value] | [Source] |
| [Cost driver 2] | [Value] | [Source] |

#### Timing Assumptions
| Milestone | Timing | Dependencies |
|-----------|--------|--------------|
| [Milestone 1] | [Date] | [Dependencies] |
| [Milestone 2] | [Date] | [Dependencies] |

### Base Case Model

#### Cash Flow Projection

| Line Item | Year 0 | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|-----------|--------|--------|--------|--------|--------|--------|
| **Investment** | | | | | | |
| Capital expenditure | ($X) | | | | | |
| Implementation cost | ($X) | | | | | |
| Working capital | ($X) | | | | | |
| **Total Investment** | ($X) | | | | | |
| | | | | | | |
| **Benefits** | | | | | | |
| Revenue increase | | $X | $X | $X | $X | $X |
| Cost reduction | | $X | $X | $X | $X | $X |
| **Total Benefits** | | $X | $X | $X | $X | $X |
| | | | | | | |
| **Net Cash Flow** | ($X) | $X | $X | $X | $X | $X |
| **Cumulative Cash Flow** | ($X) | ($X) | $X | $X | $X | $X |
```

---

## Key Financial Metrics

### 1. Net Present Value (NPV)

```
## NPV Calculation

### Formula
NPV = Σ [Cash Flow / (1 + r)^t] - Initial Investment

Where:
- r = Discount rate
- t = Time period

### Calculation

| Year | Cash Flow | Discount Factor (r=X%) | Present Value |
|------|-----------|------------------------|---------------|
| 0 | ($X) | 1.000 | ($X) |
| 1 | $X | 0.XXX | $X |
| 2 | $X | 0.XXX | $X |
| 3 | $X | 0.XXX | $X |
| 4 | $X | 0.XXX | $X |
| 5 | $X | 0.XXX | $X |
| **NPV** | | | **$X** |

### Interpretation
- NPV > 0: Investment creates value (accept)
- NPV = 0: Investment breaks even (indifferent)
- NPV < 0: Investment destroys value (reject)

### Enhancement: Real-Options NPV
- Consider flexibility value of staged investments
- Model optionality to expand/contract
- Include AI learning value
```

### 2. Internal Rate of Return (IRR)

```
## IRR Calculation

### Formula
IRR = Rate where NPV = 0

### Calculation Method
Use iterative calculation or Excel IRR function

### Results

| Scenario | IRR | Decision |
|----------|-----|----------|
| Base case | X% | [Accept/Reject] |
| Upside | X% | [Accept/Reject] |
| Downside | X% | [Accept/Reject] |

### Interpretation
- IRR > Hurdle rate: Accept the investment
- IRR = Hurdle rate: Indifferent
- IRR < Hurdle rate: Reject the investment

### Modified IRR (MIRR)
- Use when reinvestment rate differs from financing rate
- More accurate for projects with non-standard cash flows
```

### 3. Payback Period

```
## Payback Period Calculation

### Simple Payback
Time to recover initial investment from cumulative cash flows

| Year | Cumulative Cash Flow |
|------|----------------------|
| 0 | ($X) |
| 1 | ($X) |
| 2 | $X |
| 3 | $X |

**Payback Period**: Between Year 1 and Year 2
= 1 + [($X) / $X] = X.X years

### Discounted Payback
Time to recover initial investment from discounted cumulative cash flows

**Discounted Payback Period**: X.X years

### Interpretation
- Shorter payback: Lower risk, faster capital recovery
- Industry benchmarks: Compare to typical payback in sector
- Consider tech/hype cycle - faster payback may indicate faster obsolescence
```

### 4. Return on Investment (ROI)

```
## ROI Calculation

### Simple ROI
ROI = (Total Benefits - Total Costs) / Total Costs × 100%

### Calculation
ROI = ($X - $X) / $X × 100% = X%

### Annualized ROI
Annual ROI = [(Total Benefits / Total Costs)^(1/n) - 1] × 100%

### Interpretation
- Higher ROI: More efficient use of capital
- Compare to cost of capital or alternative investments
```

### 5. Economic Value Added (EVA)

```
## EVA Calculation

### Formula
EVA = NOPAT - (WACC × Capital Employed)

Where:
- NOPAT = Net Operating Profit After Tax
- WACC = Weighted Average Cost of Capital
- Capital Employed = Total Assets - Current Liabilities

### Interpretation
- Positive EVA: Creates value for shareholders
- Negative EVA: Destroys value
```

---

## Scenario Analysis

### Building Scenarios

```
## Scenario Framework

### Scenario Design

| Variable | Base Case | Upside Case | Downside Case |
|----------|-----------|-------------|---------------|
| [Driver 1] | [Value] | [Value] | [Value] |
| [Driver 2] | [Value] | [Value] | [Value] |
| [Driver 3] | [Value] | [Value] | [Value] |

### Scenario Results Summary

| Metric | Upside | Base | Downside |
|--------|--------|------|----------|
| NPV | $X | $X | $X |
| IRR | X% | X% | X% |
| Payback | X yrs | X yrs | X yrs |
| ROI | X% | X% | X% |

### Sensitivity Analysis

| Variable | -20% Impact on NPV | +20% Impact on NPV |
|----------|-------------------|-------------------|
| [Driver 1] | $X | $X |
| [Driver 2] | $X | $X |
| [Driver 3] | $X | $X |

**Key insight**: [Which variables most impact the investment case]

### Monte Carlo Analysis
- Model 10,000+ scenarios with variable distributions
- Show probability distribution of outcomes
- Calculate probability of loss, target returns
- Use AI to identify key risk factors
```

### Break-Even Analysis

```
## Break-Even Analysis

### Unit Economics
| Metric | Value |
|--------|-------|
| Price per unit | $X |
| Variable cost per unit | $X |
| Contribution margin | $X |
| Contribution margin % | X% |

### Break-Even Calculation
Fixed Costs / Contribution Margin = Break-Even Units

Break-Even = $X / $X = X,XXX units

### Break-Even Chart
[Visual showing break-even point]

### Implications
- Current capacity: X,XXX units
- Break-even: X,XXX units
- Margin of safety: X%
```

---

## Business Case Template

### Executive Summary

```
## Business Case: [Project Name]

### Executive Summary

**Recommendation**: [One-sentence recommendation]

**Investment Required**: $[Amount] over [Timeline]

**Expected Returns**:
- NPV: $[Amount] (at X% discount rate)
- IRR: X%
- Payback: X years
- ROI: X%

**Key Benefits**:
1. [Benefit 1 quantified]
2. [Benefit 2 quantified]
3. [Benefit 3 quantified]

**Risks**:
- [Risk 1] — [Mitigation]
- [Risk 2] — [Mitigation]

**Decision Required**: [What approval is needed]
```

### Detailed Business Case

```
## 1. Strategic Context

### Business Objective
[Why this investment matters strategically]

### Problem or Opportunity
[What problem does this solve or opportunity does it capture?]

### Options Considered
| Option | Description | NPV | IRR | Recommendation |
|--------|-------------|-----|-----|----------------|
| A | [Do nothing] | $X | X% | [Baseline] |
| B | [Option 1] | $X | X% | [Recommended] |
| C | [Option 2] | $X | X% | [Alternative] |

## 2. Financial Analysis

### Investment Summary
| Category | Year 0 | Year 1 | Year 2 | Year 3 | Total |
|----------|--------|--------|--------|--------|-------|
| Capital | $X | | | | $X |
| Operating | | $X | $X | $X | $X |
| Total | $X | $X | $X | $X | $X |

### Benefit Summary
| Benefit | Year 1 | Year 2 | Year 3 | Total |
|---------|--------|--------|--------|-------|
| [Benefit 1] | $X | $X | $X | $X |
| [Benefit 2] | $X | $X | $X | $X |
| Total | $X | $X | $X | $X |

### Returns Summary
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| NPV | $X | $X | [Met/Not Met] |
| IRR | X% | X% | [Met/Not Met] |
| Payback | X yrs | X yrs | [Met/Not Met] |
| ROI | X% | X% | [Met/Not Met] |

## 3. Risk Assessment

### Risk Register
| Risk | Likelihood | Impact | Mitigation | Residual Risk |
|------|------------|--------|------------|---------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Mitigation] | [H/M/L] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Mitigation] | [H/M/L] |

### Sensitivity
[Which variables most impact the business case]

## 4. Implementation Plan

### Timeline
| Phase | Duration | Start | End |
|-------|----------|-------|-----|
| Phase 1 | X months | [Date] | [Date] |
| Phase 2 | X months | [Date] | [Date] |

### Resource Requirements
| Role | FTE | Duration |
|------|-----|----------|
| [Role 1] | X.X | [Time] |
| [Role 2] | X.X | [Time] |

## 5. Recommendations and Next Steps

### Recommendation
[Clear statement of recommendation]

### Required Decisions
1. [Decision 1]
2. [Decision 2]

### Next Steps
| Action | Owner | Due Date |
|--------|-------|----------|
| [Action 1] | [Name] | [Date] |
| [Action 2] | [Name] | [Date] |
```

---

## Discount Rate Selection

### Factors to Consider

| Factor | Consideration | Impact on Rate |
|--------|---------------|----------------|
| Cost of capital | Company's WACC | [Higher/Lower] |
| Risk level | Project risk vs. company | [+/- adjustment] |
| Industry | Industry average returns | [Benchmark] |
| Inflation | Expected inflation rate | [Include] |
| Market conditions | Current interest rates | [Adjust] |
| **Tech risk** | AI/technology implementation risk | [+ adjustment] |

### Typical Discount Rates by Risk Level

| Risk Level | Discount Rate Range | Examples |
|------------|---------------------|----------|
| Low risk | 5-8% | Core operations, efficiency |
| Medium risk | 8-12% | Growth initiatives |
| High risk | 12-20% | New market entry |
| Very high risk | 20%+ | New ventures, R&D, AI/ML |
| Platform/AI | 15-25% | Digital transformation |

---

## Advanced Forecasting

- **Predictive analytics**: Use ML models for demand forecasting
- **Anomaly detection**: Identify unusual patterns in assumptions
- **Scenario generation**: AI can suggest additional scenarios
- **Real-time updates**: Connect models to live data feeds

### Modern Modeling Best Practices

```
## Financial Model Standards

### Structure
- Single source of truth for assumptions
- Clear inputs vs. outputs separation
- Scenario switches that update entire model
- Sensitivity tables linked to key outputs

### Technology Integration
- Cloud-based collaboration
- Version control for model history
- Audit trails for changes
- API connections for live data

### Visualization
- Interactive dashboards
- Drill-down capability
- Export to multiple formats
- Mobile-friendly views
```

### Total Cost of Ownership (TCO)

```
## TCO Analysis

### Direct Costs
| Cost Category | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|---------------|--------|--------|--------|--------|--------|
| Acquisition | $X | | | | |
| Implementation | $X | $X | | | |
| Operation | | $X | $X | $X | $X |
| Maintenance | | $X | $X | $X | $X |
| Upgrade/Replace | | | | $X | $X |

### Indirect Costs
- Training costs
- Productivity loss during implementation
- Support overhead
- Compliance/certification costs

### TCO Summary
| Metric | Value |
|--------|-------|
| Total TCO | $X |
| Annualized TCO | $X |
| Cost per user/year | $X |
```

---

## Best Practices

1. **Document all assumptions**: Future cash flows are only as good as the assumptions
2. **Be conservative**: Use realistic, not optimistic, assumptions
3. **Show your work**: Include supporting calculations
4. **Test sensitivity**: Identify which assumptions matter most
5. **Consider risks**: Include risk-adjusted scenarios
6. **Compare alternatives**: Always show options, not just recommended path
7. **Quantify intangible benefits**: Try to put numbers on soft benefits
8. **Update regularly**: Business cases should be living documents
9. **Include AI/Tech considerations**: Technology costs and benefits matter
10. **Apply Monte Carlo**: Use probability-based risk analysis for major investments
11. **Consider real options**: Value of flexibility in staged investments
12. **Make it auditable**: Structure for easy review and validation

---

## Notes

- The "number" is never the point — the business case supports a decision
- Finance and strategy must work together — numbers without story lack impact
- Sensitivity analysis is more important than precise projections
- Always stress-test the business case with realistic downside scenarios
- Be prepared to explain every assumption
- If you can't explain it simply, you don't understand it well enough
- Always include technology/digital dimension in business cases
- AI/ML investments have specific cost structures - account for data, compute, talent
- Platform investments have different economics - consider network effects
