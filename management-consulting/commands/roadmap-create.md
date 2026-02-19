---
description: Create strategic roadmap with phases, milestones, and dependencies
argument-hint: "<strategy or initiative> <timeframe>"
---

# /roadmap-create -- Strategic Roadmap Development

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Develop a comprehensive strategic roadmap that translates strategy into actionable phases with clear milestones, dependencies, and resource requirements.

## Invocation

```
/roadmap-create [strategy or initiative] [timeframe]
```

If parameters not provided, ask for:
- Strategic initiative
- Planning horizon (1 year, 3 years, 5 years)
- Phase structure
- Key milestones

## Workflow

### Step 1: Define Roadmap Structure

Determine the approach:

```
## Roadmap Approach

### Time Horizon
- [X] years
- [X] phases

### Phase Structure
| Phase | Duration | Focus |
|-------|----------|-------|
| Phase 1 | [Time] | [Foundation/Quick Wins] |
| Phase 2 | [Time] | [Build/Scale] |
| Phase 3 | [Time] | [Optimize/Mature] |

### Key Principles
1. [Principle 1]
2. [Principle 2]
3. [Principle 3]
```

### Step 2: Define Phases

Structure each phase:

```
## Phase 1: [Phase Name] — [Timeframe]

### Objectives
- [Objective 1]
- [Objective 2]
- [Objective 3]

### Key Initiatives
| Initiative | Description | Priority | Dependencies |
|------------|-------------|----------|---------------|
| [Initiative 1] | [Description] | [High] | [Dependencies] |
| [Initiative 2] | [Description] | [High] | [Dependencies] |
| [Initiative 3] | [Description] | [Medium] | [Dependencies] |

### Deliverables
- [Deliverable 1]
- [Deliverable 2]

### Success Criteria
| Criterion | Target | Measurement |
|-----------|--------|-------------|
| [Criterion 1] | [Target] | [How measured] |
| [Criterion 2] | [Target] | [How measured] |

---

## Phase 2: [Phase Name] — [Timeframe]

[Same structure]

---

## Phase 3: [Phase Name] — [Timeframe]

[Same structure]
```

### Step 3: Milestone Planning

Define key milestones:

```
## Milestone Roadmap

| Milestone | Target Date | Phase | Description | Success Criteria |
|-----------|-------------|-------|-------------|------------------|
| M1 | [Date] | Phase 1 | [Milestone] | [Criteria] |
| M2 | [Date] | Phase 1 | [Milestone] | [Criteria] |
| M3 | [Date] | Phase 2 | [Milestone] | [Criteria] |
| M4 | [Date] | Phase 2 | [Milestone] | [Criteria] |
| M5 | [Date] | Phase 3 | [Milestone] | [Criteria] |
| M6 | [Date] | Phase 3 | [Milestone] | [Criteria] |

### Milestone Definitions

#### M1: [Milestone Name]
- **Description**: [What happens]
- **Criteria**: [How we know we're there]
- **Dependencies**: [What must be complete]
- **Risks**: [What could delay]
```

### Step 4: Dependencies Mapping

Identify dependencies:

```
## Dependency Map

### Critical Dependencies
| Initiative | Depends On | Risk if Delayed | Mitigation |
|------------|------------|-----------------|------------|
| [Initiative] | [Dependency] | [Impact] | [Mitigation] |

### Resource Dependencies
- [Dependency 1]
- [Dependency 2]

### External Dependencies
- [Dependency 1]
- [Dependency 2]
```

### Step 5: Resource Planning

Outline resources:

```
## Resource Requirements

### By Phase

| Resource Category | Phase 1 | Phase 2 | Phase 3 | Total |
|-------------------|---------|---------|---------|-------|
| FTEs | X | X | X | X |
| Capital | $X | $X | $X | $X |
| Opex | $X | $X | $X | $X |

### By Year

| Year | Investment | FTEs | Key Focus |
|------|------------|------|-----------|
| Year 1 | $X | X | [Focus] |
| Year 2 | $X | X | [Focus] |
| Year 3 | $X | X | [Focus] |
```

### Step 6: Risk and Contingency

Document risks:

```
## Risk Assessment

### Roadmap Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Mitigation] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Mitigation] |

### Contingency Triggers
- [Trigger 1]: [Response]
- [Trigger 2]: [Response]
```

### Step 7: Governance

Define roadmap management:

```
## Governance

### Review Cadence
| Forum | Frequency | Purpose |
|-------|-----------|---------|
| Steering Committee | Quarterly | Phase approval, major decisions |
| Program Review | Monthly | Progress, issues, decisions |
| Team Standup | Weekly | Work coordination |

### Decision Rights
| Decision Type | Decider | Process |
|---------------|---------|---------|
| Scope changes | Steering Committee | Approval |
| Timeline changes | Program Manager | Notification |
| Resource changes | Steering Committee | Approval |

### Change Management
- [Process for adjusting roadmap]
```

## Output Format

Generate:

1. **Executive Overview** — High-level roadmap
2. **Phase Structure** — Detailed phase plans
3. **Milestone Timeline** — Key dates and criteria
4. **Dependencies** — Critical path and dependencies
5. **Resources** — Investment and FTE requirements
6. **Governance** — Management and review approach

After generating, ask:

> "Would you like me to:
> - Create a visual timeline graphic?
> - Develop detailed initiative plans for specific phases?
> - Add detailed resource plans?
> - Create an executive summary presentation?"

## Notes

- Link to strategy — every initiative should connect to strategic objective
- Be realistic about pace — organizations can only absorb so much change
- Prioritize — not everything can be "high priority"
- Make dependencies explicit — know the critical path
- Build in contingencies — things will change
- Review and update regularly — a roadmap is a living document
- Communicate clearly — different audiences need different views
- Balance ambition with feasibility — aggressive roadmaps need strong execution plans
- Consider agile/incremental approaches for uncertain environments
- Include quick wins early to build momentum and stakeholder confidence
