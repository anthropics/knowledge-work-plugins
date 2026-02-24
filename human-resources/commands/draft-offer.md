---
description: Draft an offer letter with comp details and terms
argument-hint: "<role and level>"
---

# /draft-offer

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Draft a complete offer letter for a new hire.

## Usage

```
/draft-offer $ARGUMENTS
```

## What I Need From You

- **Role and title**: What position?
- **Level**: Junior, Mid, Senior, Staff, etc.
- **Location**: Where will they be based? (affects comp and benefits)
- **Compensation**: Base salary, equity, signing bonus (if applicable)
- **Start date**: When should they start?
- **Hiring manager**: Who will they report to?

If you don't have all details, I'll help you think through them.

## Output

```markdown
## Offer Letter Draft: [Role] — [Level]

### Compensation Package
| Component | Details |
|-----------|---------|
| **Base Salary** | $[X]/year |
| **Equity** | [X shares/units], [vesting schedule] |
| **Signing Bonus** | $[X] (if applicable) |
| **Target Bonus** | [X]% of base (if applicable) |
| **Total First-Year Comp** | $[X] |

### Terms
- **Start Date**: [Date]
- **Reports To**: [Manager]
- **Location**: [Office / Remote / Hybrid]
- **Employment Type**: [Full-time, Exempt]

### Benefits Summary
[Key benefits highlights relevant to the candidate]

### Offer Letter Text

Dear [Candidate Name],

We are pleased to offer you the position of [Title] at [Company]...

[Complete offer letter text]

### Notes for Hiring Manager
- [Negotiation guidance if needed]
- [Comp band context]
- [Any flags or considerations]
```

## If Connectors Available

If **~~HRIS** is connected:
- Pull comp band data for the level/role
- Verify headcount approval
- Auto-populate benefits details

If **~~ATS** is connected:
- Pull candidate details from the application
- Update offer status in the pipeline

## Tips

1. **Include total comp** — Candidates compare total compensation, not just base.
2. **Be specific about equity** — Share count, current valuation method, vesting schedule.
3. **Personalize** — Reference something from the interview process to make it warm.
