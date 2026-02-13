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

### Step 3: Resource Allocation

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
| **Total** | **$[Amount]** | **$[Amount]** | **$[Amount]** | **$[Amount]** |
```

### Step 4: Risk and Contingency

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
```

## Output Format

Generate a comprehensive implementation plan:

```
# Implementation Plan: [Project Name]

## Executive Summary
[2-3 sentence overview]

## Workstream Overview
[Summary of all workstreams]

## Detailed Timeline
[Phase-by-phase breakdown]

## Resource Plan
[Team and budget requirements]

## Risk Management
[Key risks and mitigations]

## Governance
[How implementation will be managed and monitored]
```

## Notes

- Break workstreams into activities small enough to track
- Build in contingency for complex implementations
- Identify critical path — what drives the timeline
- Plan for dependencies — what must happen first
- Resource load carefully — avoid over-commitment
- Consider agile/sprint-based approaches for uncertain requirements
- Include change management activities in implementation timeline
- Build in pilot/testing phases before full rollout
