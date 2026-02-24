---
description: Generate headcount, attrition, diversity, or org health reports
argument-hint: "<report type — headcount, attrition, diversity, org health>"
---

# /people-report

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate people analytics reports from your HR data. See the **people-analytics** skill for metric definitions, analysis frameworks, and benchmarks.

## Usage

```
/people-report $ARGUMENTS
```

## Report Types

**Headcount**: Current org snapshot — by team, location, level, tenure
**Attrition**: Turnover analysis — voluntary/involuntary, by team, trends
**Diversity**: Representation metrics — by level, team, pipeline
**Org Health**: Span of control, management layers, team sizes, flight risk

## What I Need From You

Upload a CSV or describe your data. Helpful fields:
- Employee name/ID, department, team
- Title, level, location
- Start date, end date (if applicable)
- Manager, compensation (if relevant)
- Demographics (for diversity reports, if available)

## Output

```markdown
## People Report: [Type] — [Date]

### Executive Summary
[2-3 key takeaways]

### Key Metrics
| Metric | Value | Trend |
|--------|-------|-------|
| [Metric] | [Value] | [up/down/flat] |

### Detailed Analysis
[Charts, tables, and narrative for the specific report type]

### Recommendations
- [Data-driven recommendation]
- [Action item]

### Methodology
[How the numbers were calculated, any caveats]
```

## If Connectors Available

If **~~HRIS** is connected:
- Pull live employee data — headcount, tenure, department, level
- Generate reports without needing a CSV upload

If **~~chat** is connected:
- Offer to share the report summary in a relevant channel
