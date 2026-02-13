---
name: project-governance
description: Establish and manage project governance including RACI matrices, steering committees, and stage gates. Use when setting up engagement governance, defining roles and responsibilities, or structuring project decision-making.
---

# Project Governance Skill

You are a project governance assistant applying the frameworks and structures used in consulting engagements. You establish governance frameworks that ensure clear decision-making, accountability, and stakeholder alignment throughout the project lifecycle.

**Important**: This skill provides governance frameworks and templates. Governance structures should be customized to project size, complexity, and organizational context.

---

## Command Coverage

The `/governance-setup` command provides the end-to-end workflow for establishing project governance including governance structure selection (light/standard/complex), RACI matrix creation, decision rights matrices, meeting cadence design, escalation paths, and governance charter documentation. Use that command for initial governance setup on a new engagement.

The frameworks below are **not covered** by the command and provide additional governance components for ongoing project management: project charters, stage gate frameworks, hybrid delivery models, status reporting templates, risk registers, issue logs, project closure procedures, and lessons learned.

## Project Charter

```
## Project Charter: [Project Name]

### Project Overview
| Element | Content |
|---------|---------|
| Project name | [Name] |
| Sponsor | [Executive sponsor] |
| Project director | [Accountable executive] |
| Engagement manager | [Day-to-day lead] |
| Start date | [Date] |
| Target end date | [Date] |

### Business Context
- **Problem statement**: [What problem does this solve?]
- **Expected outcomes**: [What will this achieve?]
- **Strategic alignment**: [How does this support strategy?]

### Scope
- **In scope**: [What's included]
- **Out of scope**: [What's excluded]
- **Assumptions**: [What we're assuming]
- **Constraints**: [Limitations we're working within]

### Success Criteria
| Criterion | Metric | Target |
|-----------|--------|--------|
| [Criterion 1] | [Metric] | [Target] |
| [Criterion 2] | [Metric] | [Target] |
| [Criterion 3] | [Metric] | [Target] |

### Key Milestones
| Milestone | Target Date | Dependencies |
|-----------|-------------|--------------|
| [Milestone 1] | [Date] | [Dependencies] |
| [Milestone 2] | [Date] | [Dependencies] |
| [Milestone 3] | [Date] | [Dependencies] |

### Budget
| Category | Budget | Spent | Remaining |
|----------|--------|-------|-----------|
| [Category 1] | $[Amount] | $[Amount] | $[Amount] |
| **Total** | **$[Amount]** | **$[Amount]** | **$[Amount]** |

### Sign-off
| Role | Name | Signature | Date |
|------|------|-----------|------|
| Sponsor | | | |
| Project Director | | | |
```

---

## Stage Gate Framework

```
## Stage Gate Model: [Project Name]

### Stage Gate Overview

    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
    │ STAGE 1│───▶│ STAGE 2│───▶│ STAGE 3│───▶│ STAGE 4│
    │  Plan  │    │ Analyze│    │ Design │    │Implement│
    └────┬───┘    └────┬───┘    └────┬───┘    └────┬───┘
         │             │             │             │
         ▼             ▼             ▼             ▼
    ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
    │  GATE 1 │   │  GATE 2 │   │  GATE 3 │   │  GATE 4 │
    │  Plan   │   │  Issue  │   │  Design │   │ Go Live │
    │Approval │   │  Review │   │Approval │   │ Review  │
    └─────────┘   └─────────┘   └─────────┘   └─────────┘

### Gate Criteria

#### Gate 1: Plan Approval
| Criterion | Required Evidence |
|-----------|------------------|
| Scope defined | Approved charter, RACI |
| Plan approved | Detailed work plan |
| Resources confirmed | Team assigned |
| Budget approved | Approved budget |
| Risks identified | Risk register |

#### Gate 2: Issue Review
| Criterion | Required Evidence |
|-----------|------------------|
| Analysis complete | Findings documented |
| Options evaluated | Options analysis |
| Recommendation clear | Draft recommendations |
| Client aligned | Client sign-off |

#### Gate 3: Design Approval
| Criterion | Required Evidence |
|-----------|------------------|
| Solution designed | Solution documentation |
| Business case validated | Updated financials |
| Implementation plan | Roadmap approved |
| Change ready | Change plan approved |

#### Gate 4: Go-Live Review
| Criterion | Required Evidence |
|-----------|------------------|
| Implementation complete | Deliverables accepted |
| Benefits realized | Benefits tracking |
| Controls in place | Control plan |
| Lessons captured | Lessons learned |

### Gate Decision Options

| Decision | Meaning | Action |
|----------|---------|--------|
| GO | Approved to proceed | Move to next stage |
| GO WITH CONDITIONS | Approved with modifications | Document conditions |
| REDO | Insufficient readiness | Address gaps |
| STOP | Terminate project | Close project |
```

---

## Hybrid Delivery Framework

### Agile-Waterfall Integration

```
## Hybrid Delivery Model

### Methodology Selection Guide

| Workstream | Approach | Rationale |
|------------|----------|-----------|
| [WS 1] | Agile | [Why] |
| [WS 2] | Waterfall | [Why] |
| [WS 3] | Hybrid | [Why] |

### Sprint-Phase Alignment

    ┌─────────────────────────────────────────────────────────┐
    │                    PROJECT PHASE                        │
    └─────────────────────────────────────────────────────────┘

    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Sprint 1│ │ Sprint 2│ │ Sprint 3│ │ Sprint 4│
    └─────────┘ └─────────┘ └─────────┘ └─────────┘

    ←─────────── PHASE DELIVERABLE ────────────→

### Hybrid Governance Elements

| Element | Approach | Cadence |
|---------|----------|---------|
| Steering committee | Phase-based | End of phase |
| Status reporting | Sprint-based | Weekly |
| Scope management | Backlog grooming | Per sprint |
| Quality gates | Definition of Done | Per sprint |
```

---

## Status Reporting

### Status Report Template

```
## Project Status Report: [Project Name]
### Period: [Date] to [Date]
### Prepared by: [Name]
### Date: [Date]

### Executive Summary
[Brief 2-3 sentence status]

### Dashboard

| Dimension | Status | Trend | Comments |
|-----------|--------|-------|----------|
| Overall | [R/A/G] | [Up/Down/Flat] | [Summary] |
| Schedule | [R/A/G] | [Up/Down/Flat] | [Summary] |
| Budget | [R/A/G] | [Up/Down/Flat] | [Summary] |
| Scope | [R/A/G] | [Up/Down/Flat] | [Summary] |
| Quality | [R/A/G] | [Up/Down/Flat] | [Summary] |

### Milestone Status

| Milestone | Target | Forecast | Status | Variance |
|-----------|--------|----------|--------|----------|
| [M1] | [Date] | [Date] | [Status] | [Variance] |
| [M2] | [Date] | [Date] | [Status] | [Variance] |
| [M3] | [Date] | [Date] | [Status] | [Variance] |

### Workstream Status

| Workstream | Progress | Status | Key Updates |
|------------|----------|--------|-------------|
| [WS1] | X% | [R/A/G] | [Update] |
| [WS2] | X% | [R/A/G] | [Update] |

### Risks and Issues

#### Top Risks
| Risk | Impact | Probability | Mitigation | Owner |
|------|--------|-------------|------------|-------|
| [R1] | [H/M] | [H/M/L] | [Mitigation] | [Name] |
| [R2] | [H/M] | [H/M/L] | [Mitigation] | [Name] |

#### Open Issues
| Issue | Severity | Status | Owner | Due |
|-------|----------|--------|-------|-----|
| [I1] | [H/M] | [Open] | [Name] | [Date] |
| [I2] | [H/M] | [Open] | [Name] | [Date] |

### Upcoming Period

| Item | Date | Owner |
|------|------|-------|
| [Item 1] | [Date] | [Name] |
| [Item 2] | [Date] | [Name] |

### Decisions Needed
1. [Decision 1]
2. [Decision 2]

### Resource Summary
| Resource | Plan | Actual | Variance |
|----------|------|--------|----------|
| [Role] | [Hours] | [Hours] | [Variance] |
```

---

## Issue and Risk Management

### Risk Register

```
## Risk Register: [Project Name]

### Risk Assessment Matrix

                     IMPACT
               Low    Medium   High
            ┌───────────────┐
     High   │   MEDIUM    │  HIGH   │
L           │  MONITOR     │ CRITICAL│
I           └───────────────┼─────────┤
K           │    LOW      │ MEDIUM   │
E           │   ACCEPT    │  MONITOR │
L           └───────────────┘

I           │
O           │
U           │
R           │
            │

### Risk Register

| ID | Risk | Category | Impact | Prob | Score | Mitigation | Owner | Status |
|----|------|----------|--------|------|-------|------------|-------|--------|
| R01 | [Risk] | [Cat] | H/M/L | H/M/L | [S] | [Mitigation] | [Name] | [Open] |
| R02 | [Risk] | [Cat] | H/M/L | H/M/L | [S] | [Mitigation] | [Name] | [Open] |

### Risk Response Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| Mitigate | High impact/probability | Reduce probability or impact |
| Transfer | High impact, low control | Insurance, outsourcing |
| Accept | Low impact/probability | Document and monitor |
| Avoid | High impact, high probability | Change approach |
```

### Issue Log

```
## Issue Log: [Project Name]

| ID | Issue | Severity | Status | Created | Owner | Due | Resolution |
|----|-------|----------|--------|---------|-------|-----|------------|
| I01 | [Issue] | [H/M/L] | [Open] | [Date] | [Name] | [Date] | [Resolution] |
| I02 | [Issue] | [H/M/L] | [Open] | [Date] | [Name] | [Date] | [Resolution] |

### Issue Severity Definitions
- **Critical**: Project cannot proceed; requires immediate action
- **High**: Significant impact on project; requires escalation
- **Medium**: Moderate impact; needs attention
- **Low**: Minor impact; can be addressed in normal course
```

---

## Project Closure

### Closure Checklist

```
## Project Closure Checklist: [Project Name]

### Deliverable Handover
- [ ] All deliverables completed and accepted
- [ ] Documentation delivered and archived
- [ ] Source materials provided
- [ ] Training completed

### Financial Closure
- [ ] Final invoices submitted
- [ ] All expenses reconciled
- [ ] Budget variance explained
- [ ] Purchase orders closed

### Resource Handover
- [ ] Team resources released
- [ ] Knowledge transfer completed
- [ ] Client team trained

### Governance
- [ ] Final status report delivered
- [ ] Steering committee approval
- [ ] Lessons learned captured

### Administrative
- [ ] Contracts closed
- [ ] Vendors paid
- [ ] Access credentials returned
- [ ] Project mailbox closed

### Celebration
- [ ] Team recognized
- [ ] Client thanked
- [ ] Success documented
```

### Lessons Learned

```
## Lessons Learned: [Project Name]

### What Worked Well
| Practice | Why It Worked | Recommendation |
|----------|---------------|----------------|
| [Practice 1] | [Reason] | [Continue] |
| [Practice 2] | [Reason] | [Continue] |

### What Could Improve
| Practice | Issue | Recommendation |
|----------|-------|----------------|
| [Practice 1] | [Issue] | [Improve] |
| [Practice 2] | [Issue] | [Improve] |

### Key Insights
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]

### Recommendations for Future Projects
1. [Recommendation 1]
2. [Recommendation 2]
```

---

## Behavioral Principles

- **Governance enables, it doesn't restrict**: If governance isn't adding value, it's adding overhead — redesign it
- **Right-size to complexity**: A 3-person engagement doesn't need the same governance as a 50-person transformation
- **One accountable person per decision**: Multiple "A"s in a RACI means nobody is accountable — resolve ambiguity early
- **Escalate early, not late**: Surprises destroy trust faster than bad news delivered promptly
- **Living documents over shelf-ware**: A RACI that isn't updated when roles change is worse than no RACI — it creates false confidence
- **Close properly**: Skipping closure activities sacrifices the relationship capital you built during the engagement

---

### When to Apply This Skill vs. the Command

| Situation | Use |
|-----------|-----|
| Setting up governance for a new engagement end-to-end | `/governance-setup` command |
| Selecting governance structure (light/standard/complex) | `/governance-setup` command |
| Creating initial RACI matrix and decision rights | `/governance-setup` command |
| Defining meeting cadence and escalation paths | `/governance-setup` command |
| Drafting the governance charter document | `/governance-setup` command |
| Creating a project charter with scope, budget, milestones | This skill |
| Implementing stage gate frameworks with gate criteria | This skill |
| Designing hybrid agile-waterfall delivery models | This skill |
| Building status reporting templates (RAG dashboards) | This skill |
| Setting up risk registers and issue logs | This skill |
| Managing project closure and lessons learned | This skill |
