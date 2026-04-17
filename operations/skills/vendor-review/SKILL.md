---
name: vendor-review
description: Evaluate a vendor — cost analysis, risk assessment, and recommendation. Use when reviewing a new vendor proposal, deciding whether to renew or replace a contract, comparing two vendors side-by-side, or building a TCO breakdown and negotiation points before procurement sign-off.
argument-hint: "<vendor name or proposal>"
---

# /vendor-review

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Evaluate a vendor with structured analysis covering cost, risk, performance, and fit.

## Usage

```
/vendor-review $ARGUMENTS
```

## What I Need From You

- **Vendor name**: Who are you evaluating?
- **Context**: New vendor evaluation, renewal decision, or comparison?
- **Details**: Contract terms, pricing, proposal document, or current performance data

## Evaluation Framework

### Cost Analysis (Total Cost of Ownership)
- Total cost of ownership (not just license fees)
- Implementation and migration costs
- Training and onboarding costs
- Ongoing support and maintenance
- Exit costs (data migration, contract termination)

### Risk Assessment
- Vendor financial stability
- Security and compliance posture
- Concentration risk (single vendor dependency)
- Contract lock-in and exit terms
- Business continuity and disaster recovery

### Performance Metrics
- SLA compliance
- Support response times
- Uptime and reliability
- Feature delivery cadence
- Customer satisfaction

### Comparison Matrix
When comparing vendors, produce a side-by-side matrix covering: pricing, features, integrations, security, support, contract terms, and references.

## Output

```markdown
## Vendor Review: [Vendor Name]
**Date:** [Date] | **Type:** [New / Renewal / Comparison]

### Summary
[2-3 sentence recommendation]

### Cost Analysis
| Component | Annual Cost | Notes |
|-----------|-------------|-------|
| License/subscription | $[X] | [Per seat, flat, usage-based] |
| Implementation | $[X] | [One-time] |
| Support/maintenance | $[X] | [Included or add-on] |
| **Total Year 1** | **$[X]** | |
| **Total 3-Year** | **$[X]** | |

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [Mitigation] |

### Strengths
- [Strength 1]
- [Strength 2]

### Concerns
- [Concern 1]
- [Concern 2]

### Recommendation
[Proceed / Negotiate / Pass] — [Reasoning]

### Negotiation Points
- [Leverage point 1]
- [Leverage point 2]
```

## If Connectors Available

If **~~knowledge base** is connected:
- Search for existing vendor evaluations, contracts, and performance reviews
- Pull procurement policies and approval thresholds

If **~~procurement** is connected:
- Pull current contract terms, spend history, and renewal dates
- Compare pricing against existing vendor agreements

## Tips

1. **Upload the proposal** — I can extract pricing, terms, and SLAs from vendor documents.
2. **Compare vendors** — "Compare Vendor A vs Vendor B" gets you a side-by-side analysis.
3. **Include current spend** — For renewals, knowing what you pay now helps evaluate price changes.
