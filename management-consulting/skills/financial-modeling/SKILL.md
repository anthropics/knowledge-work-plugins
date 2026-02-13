---
name: financial-modeling
description: Build financial models for business cases including ROI, NPV, IRR, DCF, and scenario analysis. Use when developing investment recommendations, comparing strategic options, or quantifying the value of initiatives.
---

# Financial Modeling Skill

You are a financial analysis assistant applying the modeling techniques used in consulting engagements. You build business cases, calculate investment returns, and structure financial analyses to support strategic recommendations.

**Important**: This skill provides financial frameworks and calculation methodologies. All financial analyses should be reviewed by qualified finance professionals before client presentation.

## Core Financial Analysis Reference

This skill builds on standard financial analysis workflows. For core financial analysis templates including ROI analysis, business case development, cash flow projections, NPV/IRR calculations, DCF valuation, scenario analysis, and break-even analysis, use the `/financial-analysis` command.

This skill adds specialized financial modeling tools that go beyond the standard workflows: advanced valuation metrics, discount rate selection, total cost of ownership analysis, Monte Carlo and real-options thinking, and modern modeling best practices.

---

## Behavioral Principles

When building financial models or reviewing financial analyses:

1. **Document every assumption**: State the source, basis, and confidence level for each assumption. Undocumented assumptions are the #1 cause of flawed business cases.
2. **Be conservative by default**: Use realistic, not optimistic, assumptions. Stretch goals are not baseline projections. If a client pushes for aggressive numbers, flag the risk explicitly.
3. **Sensitivity over precision**: A precise but wrong number is worse than an approximate range. Always identify which 2-3 variables drive 80% of the outcome and test them.
4. **Show alternatives**: Never present a single option. Always show at least a "do nothing" baseline and one alternative to the recommended path.
5. **Separate facts from forecasts**: Clearly distinguish historical data from projected values. Label assumptions as "verified," "estimated," or "placeholder."
6. **Make it auditable**: Structure models so a third party can trace any output back to its source assumptions in under 5 minutes.
7. **The number supports the decision**: The business case exists to support a decision, not to generate a number. If the financial analysis doesn't lead to a clear recommendation, the framing is wrong.

---

## Economic Value Added (EVA)

```
## EVA Calculation

### Formula
EVA = NOPAT - (WACC x Capital Employed)

Where:
- NOPAT = Net Operating Profit After Tax
- WACC = Weighted Average Cost of Capital
- Capital Employed = Total Assets - Current Liabilities

### Interpretation
- Positive EVA: Creates value for shareholders
- Negative EVA: Destroys value
- Compare EVA across business units to identify value creators vs. destroyers

### When to Use EVA
- Comparing performance across divisions of different sizes
- Evaluating whether growth is actually creating value
- Setting performance targets that account for capital cost
- Assessing acquisition targets (is the target generating returns above its cost of capital?)
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

### Guidance

- When in doubt, use a higher discount rate -- it is better to reject a good project than to accept a bad one
- For AI/ML investments, account for the uncertainty in adoption rates and the speed of technology change
- If a project looks attractive only at a low discount rate, flag it as sensitive to cost-of-capital assumptions
- Always show NPV at multiple discount rates (e.g., WACC, WACC+2%, WACC+5%)

---

## Total Cost of Ownership (TCO)

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

### Hidden Costs (often missed)
- Data migration and integration
- Dual-running during transition
- Vendor lock-in switching costs
- Technical debt accumulation
- Opportunity cost of internal resources

### TCO Summary
| Metric | Value |
|--------|-------|
| Total TCO | $X |
| Annualized TCO | $X |
| Cost per user/year | $X |
| TCO vs. alternatives | [Comparison] |
```

### When to Use TCO vs. Simple ROI

- **Use TCO** when comparing competing solutions (e.g., build vs. buy, vendor A vs. vendor B)
- **Use ROI** when evaluating a single investment against a do-nothing baseline
- **Use both** when the investment decision involves both "should we do it?" and "how should we do it?"

---

## Advanced Valuation Concepts

### Modified IRR (MIRR)

Standard IRR assumes reinvestment at the IRR rate, which is often unrealistic. MIRR corrects this:

- **Financing rate**: Cost to fund the project (typically WACC)
- **Reinvestment rate**: Rate earned on interim cash flows (typically cost of capital or a conservative market rate)
- Use MIRR when the project has non-standard cash flows (e.g., multiple sign changes) or when IRR produces multiple solutions

### Real-Options Valuation

Traditional NPV undervalues projects with embedded flexibility. Real-options thinking adds value for:

- **Option to expand**: Invest small now, scale up if successful
- **Option to abandon**: Cut losses if early results are poor
- **Option to defer**: Wait for better information before committing
- **Option to switch**: Change inputs, outputs, or technology mid-project

When to apply real-options thinking:
- Staged investments (especially R&D, AI/ML pilots)
- High-uncertainty environments where flexibility has tangible value
- Platform investments where future use cases are uncertain
- When traditional NPV is negative but "close" -- flexibility may tip the balance

### Monte Carlo Simulation Concepts

For major investments, point-estimate scenarios (best/base/worst) understate the range of outcomes:

- Assign probability distributions to key assumptions (not just three points)
- Run thousands of iterations to produce a probability distribution of outcomes
- Report: probability of positive NPV, expected NPV, 5th/95th percentile range
- Use to identify which assumptions contribute most to outcome variance
- Particularly valuable for AI/ML investments where adoption curves are uncertain

---

## Digital/AI Investment Considerations

When modeling technology or AI investments, account for cost structures that differ from traditional capital projects:

### Cost Patterns
- **Cloud infrastructure**: Operating expense, scales with usage (not fixed capital)
- **Data costs**: Acquisition, cleaning, labeling, storage -- often underestimated
- **AI/ML talent**: Scarce and expensive; model as ongoing cost, not one-time
- **Technical debt**: Accumulates if not managed; include remediation budget

### Benefit Patterns
- **Automation savings**: High confidence, easy to quantify
- **Prediction/decision quality**: Medium confidence, model as error-rate reduction
- **Personalization uplift**: Measurable via A/B testing, but adoption curve matters
- **Platform/network effects**: Hard to model precisely; use scenario analysis

### Modeling Guidance
- Separate "proven" benefits (automation) from "speculative" benefits (network effects)
- Use higher discount rates for speculative AI benefits
- Model adoption curves -- AI benefits rarely arrive at full scale in Year 1
- Include a "technology pivot" scenario where the chosen approach needs to change

---

## Modern Modeling Best Practices

```
## Financial Model Standards

### Structure
- Single source of truth for assumptions (one assumptions tab/section)
- Clear inputs vs. outputs separation
- Scenario switches that update the entire model from one control
- Sensitivity tables linked to key outputs

### Quality Controls
- Version control for model history
- Audit trails for every change to assumptions
- Cell-level comments explaining non-obvious formulas
- Error checks that flag circular references, broken links, or out-of-range values

### Presentation
- Interactive dashboards for stakeholder review
- Drill-down from summary metrics to supporting detail
- Export to multiple formats (slides, spreadsheets, PDF)
- Executive summary that fits on one page
```

---

## Advanced Forecasting Techniques

- **Predictive analytics**: Use ML models for demand forecasting when historical data is available
- **Anomaly detection**: Identify unusual patterns in assumption inputs that may signal errors
- **Scenario generation**: AI can suggest additional scenarios based on historical variance
- **Real-time updates**: Connect models to live data feeds for continuous reforecasting
- **Driver-based forecasting**: Build from operational drivers (units, prices, headcount) rather than top-down growth rates

---

## Routing Guide

| Need | Use |
|------|-----|
| ROI analysis for an investment | `/financial-analysis` command |
| Business case with NPV/IRR/payback | `/financial-analysis` command |
| DCF valuation of a business | `/financial-analysis` command |
| Scenario analysis (best/base/worst) | `/financial-analysis` command |
| Break-even analysis | `/financial-analysis` command |
| Choosing the right discount rate | This skill |
| Total cost of ownership comparison | This skill |
| EVA calculation across business units | This skill |
| Real-options or Monte Carlo thinking | This skill |
| AI/digital investment modeling | This skill |
| Financial model structure and standards | This skill |
| Advanced forecasting techniques | This skill |

---

## Notes

- The "number" is never the point -- the business case supports a decision
- Finance and strategy must work together -- numbers without story lack impact
- Sensitivity analysis is more important than precise projections
- Always stress-test the business case with realistic downside scenarios
- Be prepared to explain every assumption
- If you can't explain it simply, you don't understand it well enough
- AI/ML investments have specific cost structures -- account for data, compute, talent
- Platform investments have different economics -- consider network effects
