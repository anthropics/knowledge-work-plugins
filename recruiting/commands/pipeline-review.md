---
description: Review pipeline health and identify bottlenecks
argument-hint: "<role, team, or pipeline data>"
---

# Pipeline Review

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Analyze your recruiting pipeline to surface bottlenecks, stalled candidates, and conversion rate issues. Produces actionable recommendations to improve pipeline velocity.

## Input

The user provides one or more of:
- Role or team to review
- Pipeline data (pasted from ATS, spreadsheet, or described)
- Current candidate counts by stage
- Time-in-stage data
- Hiring goals and deadlines

If no data is provided, ask: "Share your pipeline data — paste candidate counts by stage, export from your ATS, or describe where things stand for a role or team."

## Workflow

1. **Parse pipeline data** — Extract candidates by stage, time-in-stage, and any conversion metrics
2. **Calculate funnel metrics** — Conversion rates between stages, pipeline velocity, projected time-to-fill
3. **Identify bottlenecks** — Flag stages with below-benchmark conversion, stalled candidates, or capacity constraints
4. **Assess pipeline health** — Compare current pipeline against what's needed to make the hire on time
5. **Model scenarios** — If conversion rates hold, how many candidates are needed at top-of-funnel?
6. **Generate recommendations** — Prioritized actions to unblock the pipeline
7. **If ATS connected** — Pull live pipeline data, identify specific stalled candidates, and check interviewer capacity

## Output Structure

```
## Pipeline Review: [Role/Team]
**As of**: [date] | **Target hire date**: [date] | **Days open**: [N]

### Funnel Summary

| Stage | Candidates | Conversion | Benchmark | Status |
|-------|-----------|-----------|-----------|--------|
| Applied/Sourced | [N] | — | — | |
| Recruiter screen | [N] | [%] | 25-30% | ✅/⚠️/❌ |
| Hiring manager screen | [N] | [%] | 40-50% | ✅/⚠️/❌ |
| Technical/Skills | [N] | [%] | 30-40% | ✅/⚠️/❌ |
| Onsite/Final | [N] | [%] | 40-50% | ✅/⚠️/❌ |
| Offer | [N] | [%] | 70-85% | ✅/⚠️/❌ |
| Hire | [N] | — | — | |

### Bottlenecks
1. **[Stage]**: [Description of the problem, e.g., "Conversion from screen to HM review is 15% vs 40% benchmark — likely a calibration issue between sourcing criteria and HM expectations"]
2. ...

### Stalled Candidates
| Candidate | Stage | Days in stage | Recommended action |
|-----------|-------|--------------|-------------------|
| [Name] | [Stage] | [N] | [action] |

### Pipeline Math
- To make **1 hire** by [date] at current conversion rates, you need **[N] candidates** at top of funnel
- Current pace: [X candidates/week entering] → projected hire by [date]
- Gap: [N more candidates needed] or [improve conversion at stage X]

### Recommendations
1. **[Priority 1]**: [Specific action with expected impact]
2. **[Priority 2]**: [Specific action]
3. **[Priority 3]**: [Specific action]
```

## With Connectors

- **If ATS connected**: Pull real-time pipeline data, identify stalled candidates by name, check interviewer load
- **If calendar connected**: Assess interviewer availability and scheduling bottlenecks
- **If chat connected**: Post the pipeline summary to the hiring channel

## Tips

- Run weekly for active roles to catch problems early
- Include time-in-stage data for the most actionable analysis
- Compare across similar roles to identify systemic vs. role-specific issues
