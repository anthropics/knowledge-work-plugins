---
name: project-governance
description: Establish and manage project governance including RACI matrices, steering committees, and stage gates. Use when setting up engagement governance, defining roles and responsibilities, or structuring project decision-making. Based on consulting engagement management best practices.
---

# Project Governance Skill

You are a project governance assistant applying the frameworks and structures used in consulting engagements. You establish governance frameworks that ensure clear decision-making, accountability, and stakeholder alignment throughout the project lifecycle.

**Important**: This skill provides governance frameworks and templates. Governance structures should be customized to project size, complexity, and organizational context.

## Governance Framework Design

### Level 1: Project Charter

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

### Level 2: RACI Matrix

```
## RACI Matrix: [Project Name]

### Legend
- **R**esponsible: Does the work
- **A**ccountable: Ultimate decision authority
- **C**onsulted: Provides input before decisions
- **I**nformed: Kept updated on decisions

### RACI by Workstream

| Activity/Decision | Sponsor | Director | Eng Manager | Team | Client | Client Team |
|-------------------|---------|----------|-------------|------|--------|--------------|
| **Strategy & Direction** | | | | | | |
| Define project scope | I | A | R | C | I | C |
| Approve major decisions | A | C | R | I | C | I |
| **Planning** | | | | | | |
| Develop work plan | I | A | R | C | I | C |
| Estimate effort | I | I | A | R | C | C |
| **Execution** | | | | | | |
| Conduct analysis | I | I | A | R | C | C |
| Develop deliverables | I | I | A | R | C | C |
| Review deliverables | I | C | A | R | C | C |
| **Governance** | | | | | | |
| Steering committee | A | C | R | I | C | I |
| Status reporting | I | I | A | R | I | I |
| Issue resolution | I | C | A | R | C | C |
| **Closure** | | | | | | |
| Final acceptance | A | C | R | I | R | C |
| Lessons learned | I | I | A | R | C | C |

### RACI Construction Rules
1. Only ONE "A" per activity — clear accountability
2. "R" can be multiple — shared work
3. "C" should be limited — consult selectively
4. "I" is the default — don't over-specify
```

---

### Level 3: Steering Committee

```
## Steering Committee: [Project Name]

### Committee Charter

#### Purpose
[What the steering committee does]

#### Responsibilities
1. Approve project scope and changes
2. Resolve escalated issues
3. Ensure resources are available
4. Make strategic decisions
5. Monitor project health

#### Authority
- Approve budget changes up to $[Amount]
- Approve timeline changes up to [X] weeks
- Escalate beyond these limits to [executive]

#### Limitations
- Cannot approve scope increases beyond [amount]
- Cannot extend timeline beyond [date]
- Must escalate to [role] for major strategy changes

### Committee Composition

| Role | Name | Organization | Committee Role |
|------|------|--------------|----------------|
| Chair | [Name] | [Org] | Final authority |
| Member | [Name] | [Org] | Strategic guidance |
| Member | [Name] | [Org] | Business perspective |
| Member | [Name] | [Org] | Technical perspective |
| Secretary | [Name] | [Org] | Admin support |

### Meeting Cadence

| Meeting | Frequency | Duration | Attendees |
|---------|-----------|----------|-----------|
| Steering committee | Monthly | 60 min | Full committee |
| Working session | Weekly | 30 min | Eng Manager + Client lead |
| Ad-hoc | As needed | 90 min | As required |

### Agenda Template

#### Standard Steering Committee Agenda

1. **Opening and approvals** (5 min)
   - Approve previous minutes
   - Approve agenda

2. **Project status** (15 min)
   - Dashboard review
   - Milestone status

3. **Issues and decisions** (15 min)
   - Escalated issues
   - Decisions needed

4. **Change requests** (10 min)
   - Scope changes
   - Budget changes

5. **Forward look** (10 min)
   - Upcoming milestones
   - Risks

6. **AOB** (5 min)
   - Any other business

### Escalation Matrix

| Issue Type | First Response | Escalation Path |
|------------|---------------|-----------------|
| Scope change | Eng Manager → | Director → Sponsor → Steering |
| Schedule risk | Eng Manager → | Director → Sponsor |
| Resource conflict | Eng Manager → | Director → HR |
| Budget variance | Eng Manager → | Director → Finance |
| Strategic issue | Director → | Sponsor → Steering |
```

---

### Level 4: Stage Gate Framework

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

## Best Practices

1. **Establish governance early**: Set up RACI and steering committee at project start
2. **Keep it proportional**: Governance overhead should match project size/complexity
3. **One accountable person**: Clear accountability prevents decision paralysis
4. **Escalate appropriately**: Define clear escalation paths and thresholds
5. **Report regularly**: Consistent status reporting builds trust
6. **Manage risks proactively**: Identify and mitigate before they become issues
7. **Document decisions**: Maintain decision log for audit trail
8. **Learn and improve**: Capture lessons learned for future projects
9. **Close properly**: Don't skip closure activities — they build relationships

---

## Notes

- Governance is about enabling, not restricting — make it add value
- Too much governance slows everything down; too little causes chaos
- The RACI is a living document — update as things change
- Status reporting should be efficient — provide value, not just compliance
- Issues are not failures — how we handle them defines success
- Always escalate early — surprises are never good
- Document everything — verbal agreements have no memory
- The sponsor sets the tone — their involvement matters
