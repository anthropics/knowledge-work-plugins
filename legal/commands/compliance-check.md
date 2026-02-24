---
description: Run a compliance check on a proposed action, product feature, or business initiative
argument-hint: "<action or initiative to check>"
---

# /compliance-check -- Compliance Review

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Run a compliance check on a proposed action, product feature, marketing campaign, or business initiative.

**Important**: This command assists with legal workflows but does not provide legal advice. Compliance assessments should be reviewed by qualified legal professionals.

## Usage

```
/compliance-check $ARGUMENTS
```

## What I Need From You

Describe what you're planning to do. Examples:
- "We want to launch a referral program with cash rewards"
- "We're adding biometric authentication to our mobile app"
- "We need to process EU customer data in our US data center"
- "Marketing wants to use customer testimonials in ads"

## Output

```markdown
## Compliance Check: [Initiative]

### Summary
[Quick assessment: Proceed / Proceed with conditions / Requires further review]

### Applicable Regulations and Policies
| Regulation/Policy | Relevance | Key Requirements |
|-------------------|-----------|-----------------|
| [GDPR / CCPA / HIPAA / etc.] | [How it applies] | [What you need to do] |

### Requirements
| # | Requirement | Status | Action Needed |
|---|-------------|--------|---------------|
| 1 | [Requirement] | [Met / Not Met / Unknown] | [What to do] |

### Risk Areas
| Risk | Severity | Mitigation |
|------|----------|------------|
| [Risk] | [High/Med/Low] | [How to address] |

### Recommended Actions
1. [Most important action]
2. [Second priority]
3. [Third priority]

### Approvals Needed
| Approver | Why | Status |
|----------|-----|--------|
| [Person/Team] | [Reason] | [Pending] |

### Further Review Recommended
[Areas where outside counsel or specialist review is advised]
```

## Tips

1. **Be specific** — "We want to email all our users" is better than "marketing campaign."
2. **Include the geography** — Compliance requirements vary by jurisdiction.
3. **Mention the data** — What personal data is involved? This drives most compliance requirements.
