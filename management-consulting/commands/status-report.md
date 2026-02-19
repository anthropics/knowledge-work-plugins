---
description: Generate project status reports with RAG status, milestone tracking, and risk summaries. Use when preparing weekly or monthly status updates for steering committees, sponsors, or project governance bodies.
argument-hint: "<project name and reporting period>"
---

# /status-report -- Project Status Reporting

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate professional project status reports using the RAG (Red-Amber-Green) methodology standard in consulting and project management. Creates clear, concise updates for steering committees and project sponsors.

## Invocation

```
/status-report [project name and reporting period]
```

If no project details are provided, ask the user to identify the project, reporting period, and current status information.

## Workflow

### Step 1: Assess Current Status

Evaluate project health across key dimensions:

```
## Status Assessment

### Overall RAG Status
| Dimension | Status | Trend | Comments |
|-----------|--------|-------|----------|
| Schedule | [R/A/G] | [↑/→/↓] | [Brief comment] |
| Budget | [R/A/G] | [↑/→/↓] | [Brief comment] |
| Scope | [R/A/G] | [↑/→/↓] | [Brief comment] |
| Quality | [R/A/G] | [↑/→/↓] | [Brief comment] |
| Resources | [R/A/G] | [↑/→/↓] | [Brief comment] |

### Overall Project Status
- **Overall RAG**: [RED / AMBER / GREEN]
- **Overall Trend**: [Improving / Stable / Declining]

### RAG Definitions
| Status | Definition | Action Required |
|--------|------------|-----------------|
| GREEN | On track, no significant issues | Continue normal monitoring |
| AMBER | Some concerns, mitigation in place | Monitor closely, escalate if worsens |
| RED | Critical issues, intervention needed | Immediate escalation, recovery plan |
```

### Step 2: Document Progress

Track accomplishments and work completed:

```
## Progress Summary

### Period: [Date Range]
- **Report Date**: [Date]
- **Reporting Period**: [Week/Month] [X]
- **Project Start**: [Date]
- **Project End**: [Date]
- **% Complete**: [X]%

### Deliverables Completed This Period
| Deliverable | Status | Completion Date | Notes |
|-------------|--------|------------------|-------|
| [Deliverable 1] | ✓ Complete | [Date] | [Notes] |
| [Deliverable 2] | ✓ Complete | [Date] | [Notes] |

### Work in Progress
| Deliverable | % Complete | Expected Completion | Notes |
|-------------|------------|----------------------|-------|
| [D1] | [X]% | [Date] | [Status] |
| [D2] | [X]% | [Date] | [Status] |

### Milestone Status
| Milestone | Target Date | Actual Date | Status |
|-----------|-------------|-------------|--------|
| [M1] | [Date] | [Date] | ✓ / ⚠ / ✗ |
| [M2] | [Date] | [Date] | ✓ / ⚠ / ✗ |
| [M3] | [Date] | [Date] | ✓ / ⚠ / ✗ |

Legend: ✓ = Achieved | ⚠ = At Risk | ✗ = Missed
```

### Step 3: Update on Budget

Track financial performance:

```
## Budget Summary

### Budget Overview
| Metric | Amount |
|--------|--------|
| Total Budget | $[Amount] |
| Committed | $[Amount] |
| Spent to Date | $[Amount] |
| Remaining | $[Amount] |
| % Budget Used | [X]% |
| % Project Complete | [X]% |

### Burn Rate Analysis
| Period | Planned Spend | Actual Spend | Variance |
|--------|---------------|--------------|----------|
| [Month 1] | $[Amount] | $[Amount] | $[Variance] |
| [Month 2] | $[Amount] | $[Amount] | $[Variance] |
| [Total] | $[Amount] | $[Amount] | $[Variance] |

### Budget Status
- **Variance**: $[Amount] ([X]%)
- **Forecast at Completion**: $[Amount]
- **Status**: [GREEN/AMBER/RED]

### Cost Breakdown
| Category | Budget | Spent | Remaining |
|----------|--------|-------|-----------|
| [Category 1] | $[X] | $[X] | $[X] |
| [Category 2] | $[X] | $[X] | $[X] |
```

### Step 4: Identify Risks and Issues

Document current and potential problems:

```
## Risk and Issue Register

### Critical Issues (RED)
| Issue | Impact | Owner | Resolution | Status |
|-------|--------|-------|------------|--------|
| [Issue 1] | [Impact description] | [Name] | [Resolution approach] | [Open/Resolved] |

### Active Risks
| Risk | Probability | Impact | Score | Mitigation | Owner |
|------|-------------|--------|-------|------------|-------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Score] | [Mitigation] | [Name] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Score] | [Mitigation] | [Name] |

### Resolved Issues This Period
| Issue | Resolution Date | Resolution |
|-------|-----------------|------------|
| [Issue 1] | [Date] | [How resolved] |

### Risk Scoring Matrix
| | Low Impact | Medium Impact | High Impact |
|---|---|---|---|
| **High Probability** | Amber | Red | Red |
| **Medium Probability** | Green | Amber | Red |
| **Low Probability** | Green | Green | Amber |
```

### Step 5: Plan Next Period

Document upcoming work and focus areas:

```
## Forward Look

### Next Period Priorities
| Priority | Activity | Owner | Due Date |
|----------|----------|-------|----------|
| 1 | [Activity] | [Name] | [Date] |
| 2 | [Activity] | [Name] | [Date] |
| 3 | [Activity] | [Name] | [Date] |

### Upcoming Milestones
| Milestone | Target Date | Status |
|-----------|-------------|--------|
| [M1] | [Date] | [On Track/At Risk] |
| [M2] | [Date] | [On Track/At Risk] |

### Decisions Required
| Decision | Requested By | Decision Needed By | Status |
|----------|--------------|--------------------|--------|
| [Decision 1] | [Name] | [Date] | [Pending/Approved] |

### Dependency Awareness
| Dependency | Dependency On | Impact if Delayed | Contingency |
|------------|--------------|-------------------|-------------|
| [Dep 1] | [Description] | [Impact] | [Plan] |
```

### Step 6: Governance Updates

Document steering committee and governance activities:

```
## Governance

### Steering Committee
- **Last Meeting**: [Date]
- **Next Meeting**: [Date]
- **Key Decisions**: [List]

### Escalations
| Escalation | Date | Raised To | Status |
|------------|------|-----------|--------|
| [Escalation 1] | [Date] | [Name/Committee] | [Open/Resolved] |

### Change Log
| Change | Request Date | Impact | Approved By | Status |
|--------|--------------|--------|-------------|--------|
| [Change 1] | [Date] | [Impact] | [Name] | [Approved/Rejected] |
```

## Output Format

```
# Project Status Report: [Project Name]

## Executive Summary
[2-3 sentences: overall status, key wins, key concerns]

## Status Dashboard
### Overall RAG: [RED/AMBER/GREEN]
### Trend: [Improving/Stable/Declining]
### % Complete: [X]%

### RAG Summary
| Dimension | Status | Trend | Commentary |
|-----------|--------|-------|------------|
| Schedule | [R/A/G] | [↑/→/↓] | [Comment] |
| Budget | [R/A/G] | [↑/→/↓] | [Comment] |
| Scope | [R/A/G] | [↑/→/↓] | [Comment] |
| Quality | [R/A/G] | [↑/→/↓] | [Comment] |
| Resources | [R/A/G] | [↑/→/↓] | [Comment] |

## Progress This Period
### Deliverables Completed
- [Deliverable 1]
- [Deliverable 2]

### Key Achievements
1. [Achievement 1]
2. [Achievement 2]

## Milestone Status
| Milestone | Target | Status |
|-----------|--------|--------|
| [M1] | [Date] | [✓/⚠/✗] |
| [M2] | [Date] | [✓/⚠/✗] |

## Budget Status
| Metric | Value |
|--------|-------|
| Total Budget | $[Amount] |
| Spent to Date | $[Amount] |
| % Spent | [X]% |
| Forecast at Completion | $[Amount] |
| Variance | $[Amount] ([X]%) |
| Status | [R/A/G] |

## Risk & Issues
### Critical Issues
[If any - with resolution plan]

### Top Risks
| Risk | Score | Mitigation |
|------|-------|------------|
| [R1] | [H/M/L] | [Mitigation] |
| [R2] | [H/M/L] | [Mitigation] |

## Next Period
### Top 3 Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

### Upcoming Milestones
| Milestone | Date |
|-----------|------|
| [M1] | [Date] |

## Governance
### Decisions Needed
[Any decisions from steering committee]

### Change Log
[Any scope/budget changes]

---
Report prepared by: [Name]
Date: [Date]
Distribution: [List]
```

## Notes

- Be honest with RAG status — don't greenwash problems
- Escalate RED issues immediately, don't wait for status reports
- Quantify progress and impact wherever possible
- Focus on what's different since last report
- Highlight both wins and concerns clearly
- Always include clear next steps with owners
- Keep the executive summary to 3 sentences max
- Attach detailed backup for anyone who wants it
- Consistency in format helps stakeholders find information
- Send status reports at the same time each period
- Follow up verbally on critical issues
- Track action items from previous reports explicitly
- Include outcomes achieved, not just tasks completed
- Connect progress to strategic objectives for context
