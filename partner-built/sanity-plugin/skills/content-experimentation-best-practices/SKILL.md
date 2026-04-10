---
name: content-experimentation-best-practices
description: Content experimentation and A/B testing guidance covering experiment design, hypotheses, metrics, sample size, statistical foundations, CMS-managed variants, and common analysis pitfalls. Use this skill when planning experiments, setting up variants, choosing success metrics, interpreting statistical results, or building experimentation workflows in a CMS or frontend stack.
---

# Content Experimentation Best Practices

Principles and patterns for running effective content experiments to improve conversion rates, engagement, and user experience.

## When to Apply

Reference these guidelines when:
- Setting up A/B or multivariate testing infrastructure
- Designing experiments for content changes
- Analyzing and interpreting test results
- Building CMS integrations for experimentation
- Deciding what to test and how

## Core Concepts

### A/B Testing
Comparing two variants (A vs B) to determine which performs better.

### Multivariate Testing
Testing multiple variables simultaneously to find optimal combinations.

### Statistical Significance
The confidence level that results aren't due to random chance.

### Experimentation Culture
Making decisions based on data rather than opinions (HiPPO avoidance).

## References

Start with the reference that matches the current problem, such as design, statistics, CMS integration, or pitfalls. See `references/` for detailed guidance:
- `references/experiment-design.md` — Hypothesis framework, metrics, sample size, and what to test
- `references/statistical-foundations.md` — p-values, confidence intervals, power analysis, Bayesian methods
- `references/cms-integration.md` — CMS-managed variants, field-level variants, external platforms
- `references/common-pitfalls.md` — 17 common mistakes across statistics, design, execution, and interpretation
