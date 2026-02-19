---
description: Establish project governance including RACI matrix, steering committee, and decision rights
argument-hint: "<project name>"
---

# /governance-setup -- Project Governance Setup

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Design and establish project governance structures including roles, responsibilities, decision rights, and meeting cadences. Ensures clear accountability and efficient decision-making.

## Invocation

```
/governance-setup [project name]
```

If parameters are not provided, ask for:
- Project/engagement name
- Stakeholder list
- Organization structure
- Complexity level

## Workflow

### Step 1: Define Governance Structure

Determine the appropriate governance model:

```
## Governance Structure Options

### Option A: Light (Small project, trusted relationship)
- Project Sponsor + Engagement Manager
- Weekly check-ins
- Minimal formal governance

### Option B: Standard (Most projects)
- Steering Committee + Working Team
- Monthly steering committee
- Bi-weekly working sessions

### Option C: Complex (Large transformation, multiple workstreams)
- Executive Sponsor + Program Director
- Steering Committee + Project Boards
- Weekly program review
- Multiple workstream leads
```

Recommend a structure based on:
- Project size and complexity
- Number of stakeholders
- Risk level
- Organization culture

### Step 2: Develop RACI Matrix

Create detailed responsibility assignment:

```
## RACI Matrix: [Project Name]

### Phase 1: Discovery

| Activity | Sponsor | Project Lead | Engagement Manager | Analyst | Client Team |
|----------|---------|--------------|--------------------|---------|--------------|
| Conduct interviews | I | A | R | C | C |
| Gather data | I | A | R | R | C |
| Synthesize findings | I | A | R | C | I |
| Review current state | I | C | A | R | C |

### Phase 2: Analysis

| Activity | Sponsor | Project Lead | Engagement Manager | Analyst | Client Team |
|----------|---------|--------------|--------------------|---------|--------------|
| Framework application | I | C | A | R | C |
| Financial modeling | I | C | A | R | C |
| Options development | I | A | R | C | C |

### Phase 3: Recommendations

| Activity | Sponsor | Project Lead | Engagement Manager | Analyst | Client Team |
|----------|---------|--------------|--------------------|---------|--------------|
| Strategy development | A | C | R | C | C |
| Business case | A | C | R | C | C |
| Executive presentation | A | C | R | C | I |

### Key
- **R** = Responsible (does the work)
- **A** = Accountable (final decision authority)
- **C** = Consulted (provides input)
- **I** = Informed (kept updated)
```

### Step 3: Define Decision Rights

Clarify decision authority:

```
## Decision Rights Matrix

| Decision Type | Decider | Input Required | Process |
|---------------|---------|----------------|---------|
| Scope changes | Sponsor | EM, Client Lead | Change request |
| Methodology | EM | Analyst | Team decision |
| Deliverable content | EM | Client Lead | Review & approve |
| Timeline adjustments | EM | Sponsor | Notification |
| Budget reallocation | Sponsor | EM | Approval required |
| Resource changes | EM | HR/PMO | Coordination |
| Go/no-go recommendations | EM | Team | Team consensus |

### Escalation Path

| Issue Type | First Escalation | Second Escalation | Timeline |
|------------|-------------------|-------------------|----------|
| Technical | EM → Client Lead | Sponsor | 48 hours |
| Schedule | EM → Sponsor | Steering Committee | 24 hours |
| Budget | EM → Sponsor | Finance | 24 hours |
| Strategic | Sponsor → Steering Committee | Board | Immediate |
```

### Step 4: Establish Meeting Cadence

Define meeting structure:

```
## Meeting Cadence

### Steering Committee
- **Frequency**: Monthly
- **Duration**: 60-90 minutes
- **Attendees**: Sponsor, Client Exec, Partner, EM
- **Purpose**: Strategic direction, major decisions, risk review
- **Agenda**:
  - Status overview (5 min)
  - Key decisions needed (15 min)
  - Deep dive topic (30 min)
  - Risks and issues (15 min)
  - Next steps (5 min)

### Project Team
- **Frequency**: Weekly
- **Duration**: 60 minutes
- **Attendees**: EM, Analysts, Client Lead
- **Purpose**: Work coordination, progress, blockers
- **Agenda**:
  - Quick wins/blockers (10 min)
  - Workstream updates (30 min)
  - Decisions needed (10 min)
  - Next week planning (10 min)

### Working Sessions
- **Frequency**: 2-3x per week as needed
- **Duration**: 60-90 minutes
- **Attendees**: As needed for specific work
- **Purpose**: Analysis, draft development, problem-solving

### Status Updates
- **Frequency**: Bi-weekly
- **Format**: Written report
- **Distribution**: Extended stakeholders
```

### Step 5: Create Governance Charter

Document the complete governance structure:

```
# Project Governance Charter

## 1. Governance Overview

### Purpose
[Why governance matters for this project]

### Principles
- Clear decision authority
- Efficient escalation
- Appropriate oversight
- Stakeholder alignment

## 2. Roles & Responsibilities

### Executive Sponsor
- **Name**: [Name]
- **Organization**: [Org]
- **Responsibilities**:
  - Strategic direction
  - Budget authority
  - Escalation point
  - Stakeholder alignment

### Project Lead
- **Name**: [Name]
- **Organization**: [Org]
- **Responsibilities**:
  - Day-to-day oversight
  - Client relationship
  - Deliverable quality

### Engagement Manager
- **Name**: [Name]
- **Organization**: [Firm]
- **Responsibilities**:
  - Work management
  - Team leadership
  - Quality assurance

[Continue for all roles]

## 3. RACI Matrix
[Full RACI as developed above]

## 4. Decision Rights
[Decision matrix as developed above]

## 5. Meeting Cadence
[Meeting schedule as developed above]

## 6. Communication Protocols

### Status Reporting
- **Format**: [Report template]
- **Frequency**: Bi-weekly
- **Distribution**: [List]

### Escalation
- **Process**: [How to escalate]
- **Timeline**: [Response expectations]

### Documentation
- **Where**: [Location]
- **Version control**: [Convention]
```

## Output Format

Generate:

1. **Governance Structure Recommendation** — Based on project complexity
2. **RACI Matrix** — Detailed responsibility assignment
3. **Decision Rights Matrix** — Authority clarity
4. **Meeting Cadence** — Schedule and agenda templates
5. **Governance Charter** — Complete documentation

After generating, ask:

> "Would you like me to:
> - Adjust the governance for different complexity levels?
> - Create specific meeting agendas?
> - Develop RACI for additional workstreams?
> - Add decision logging templates?"

## Notes

- Governance should enable, not slow down — right-size to project complexity
- "One A per activity" rule — multiple Accountables create confusion
- Document explicitly — verbal agreements fade
- Get sign-off on decision rights early — before issues arise
- Review and adjust governance as project evolves
- Keep sponsor engaged but not overwhelmed — protect their time
- Escalation paths should be clear BEFORE they're needed
- Start with key processes in RACI — don't overcomplicate with every task
