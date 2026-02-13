---
description: Develop detailed implementation plan with workstreams, dependencies, and resource allocation
argument-hint: "<project name> <scope>"
---

# /implementation-plan -- Implementation Planning

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Create a detailed implementation plan that translates strategy into actionable execution. Break down initiatives into workstreams, define dependencies, and establish realistic timelines.

## Invocation

```
/implementation-plan [project name] [scope]
```

If parameters are not provided, ask for:
- Project or initiative name
- Scope and boundaries
- Available resources
- Strategic objectives

## Workflow

### Step 1: Define Workstreams

Structure the implementation into logical workstreams:

```
## Implementation Workstreams

### Workstream Structure

| Workstream | Description | Lead | Key Deliverables |
|------------|-------------|------|-----------------|
| [WS 1] | [What it covers] | [Name] | [Deliverables] |
| [WS 2] | [What it covers] | [Name] | [Deliverables] |
| [WS 3] | [What it covers] | [Name] | [Deliverables] |

### Workstream Dependencies
- [WS 1] must complete before [WS 2] can start
- [WS 3] runs in parallel with [WS 1]
```

### Step 2: Develop Detailed Timeline

Create phase-based timeline with milestones:

```
## Implementation Timeline

### Phase 1: Foundation ([Duration])
**Objective**: [What we achieve]

| Milestone | Target | Dependencies | Owner |
|-----------|--------|--------------|-------|
| [M1] | [Date] | [None] | [Name] |
| [M2] | [Date] | [M1] | [Name] |

### Phase 2: Build ([Duration])
**Objective**: [What we achieve]

| Milestone | Target | Dependencies | Owner |
|-----------|--------|--------------|-------|
| [M3] | [Date] | [M2] | [Name] |
| [M4] | [Date] | [M3] | [Name] |

### Phase 3: Deploy ([Duration])
**Objective**: [What we achieve]

| Milestone | Target | Dependencies | Owner |
|-----------|--------|--------------|-------|
| [M5] | [Date] | [M4] | [Name] |
```

### Step 3: RACI Matrix

Define accountability across workstreams:

```
## Responsibility Matrix (RACI)

| Activity / Deliverable | Sponsor | Program Lead | WS Lead | Team | Client SMEs |
|------------------------|---------|--------------|---------|------|-------------|
| [Phase 1 deliverable] | A | R | C | I | C |
| [Phase 2 deliverable] | I | A | R | R | C |
| [Key decision point] | A | R | C | I | I |
| [Change mgmt activity] | I | A | C | R | C |

Legend: R=Responsible (does the work), A=Accountable (one per activity), C=Consulted, I=Informed

### RACI Rules
- One and only one "A" per activity
- At least one "R" per activity
- Minimize "C" to avoid bottlenecks
- "A" cannot also be "I" for the same activity
```

### Step 4: Governance Structure

Define implementation governance:

```
## Implementation Governance

### Meeting Cadence
| Forum | Frequency | Attendees | Purpose | Duration |
|-------|-----------|-----------|---------|----------|
| Steering Committee | Bi-weekly | Sponsor, Program Lead, WS Leads | Decisions, escalations, progress | 60 min |
| Program Review | Weekly | Program Lead, WS Leads | Progress, risks, dependencies | 45 min |
| Workstream Standup | 2-3x/week | WS Lead, Team | Task coordination, blockers | 15 min |

### Phase Gate Criteria
| Gate | Transition | Entry Criteria | Exit Criteria | Approver |
|------|-----------|----------------|---------------|----------|
| G1 | Foundation → Build | [Requirements defined, team staffed] | [Current state assessed, design approved] | [Sponsor] |
| G2 | Build → Deploy | [Solutions developed, tested] | [Pilot successful, rollout plan approved] | [Sponsor] |
| G3 | Deploy → Operate | [Full rollout complete] | [Adoption targets met, handover complete] | [Sponsor] |

### Escalation Path
- **Level 1**: WS Lead resolves within 24 hours
- **Level 2**: Program Lead resolves within 48 hours
- **Level 3**: Steering Committee resolves at next meeting (or emergency session)

### Change Control
| Change Type | Approval Required | Process |
|-------------|-------------------|---------|
| Scope change (minor) | Program Lead | Document, assess impact, approve/reject |
| Scope change (major) | Steering Committee | Formal change request, impact analysis, SteerCo decision |
| Timeline shift (< 2 weeks) | Program Lead | Update plan, notify stakeholders |
| Timeline shift (> 2 weeks) | Steering Committee | Root cause analysis, recovery plan, SteerCo approval |
| Budget variance (< 10%) | Program Lead | Document, adjust within contingency |
| Budget variance (> 10%) | Steering Committee | Business case for additional funding |
```

### Step 5: Resource Allocation

Define resource requirements by workstream:

```
## Resource Requirements

### Team Requirements

| Role | Workstream | FTE | Duration | Skills Required |
|------|------------|-----|----------|----------------|
| [Role 1] | [WS 1] | X.X | [Time] | [Skills] |
| [Role 2] | [WS 2] | X.X | [Time] | [Skills] |

### Budget by Workstream

| Workstream | Labor | External | Other | Total |
|------------|-------|----------|-------|-------|
| [WS 1] | $[Amount] | $[Amount] | $[Amount] | $[Amount] |
| [WS 2] | $[Amount] | $[Amount] | $[Amount] | $[Amount] |
| Contingency (10-15%) | — | — | — | $[Amount] |
| **Total** | **$[Amount]** | **$[Amount]** | **$[Amount]** | **$[Amount]** |
```

### Step 6: Risk and Contingency

Identify implementation risks:

```
## Implementation Risks

| Risk | Impact | Probability | Mitigation | Owner |
|------|--------|-------------|------------|-------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Mitigation] | [Name] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Mitigation] | [Name] |

### Contingency Plans
- [If X happens, we will Y]
- [If A happens, we will B]

### Critical Path
Identify the longest dependency chain that drives the overall timeline:
- [Activity A] → [Activity B] → [Activity C] → [Final milestone]
- Any delay on the critical path directly delays the project end date
- Non-critical activities have float — quantify the float for each
```

## Output Format

Generate a comprehensive implementation plan:

```
# Implementation Plan: [Project Name]

## Executive Summary
[2-3 sentence overview]

## Workstream Overview
[Summary of all workstreams with dependencies]

## Detailed Timeline
[Phase-by-phase breakdown with milestones]

## RACI Matrix
[Responsibility assignments across workstreams]

## Governance
[Meeting cadence, phase gates, escalation path, change control]

## Resource Plan
[Team and budget requirements]

## Risk Management
[Key risks, mitigations, critical path, contingency plans]
```

## Notes

- Break workstreams into activities small enough to track (2-4 week deliverables)
- Build in contingency for complex implementations (10-15% of timeline and budget)
- Identify critical path — what drives the timeline
- Plan for dependencies — what must happen first
- Resource load carefully — avoid over-commitment
- Consider agile/sprint-based approaches for uncertain requirements
- Include change management activities in implementation timeline
- Build in pilot/testing phases before full rollout
- One accountable owner per deliverable — shared accountability means no accountability
- Phase gates prevent premature transitions — enforce them
