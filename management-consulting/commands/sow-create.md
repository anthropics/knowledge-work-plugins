---
description: Create detailed Statement of Work with scope, deliverables, timeline, governance, and commercial terms
argument-hint: "<project name> <scope summary>"
---

# /sow-create -- Statement of Work Development

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Develop a comprehensive Statement of Work that clearly defines scope, deliverables, timeline, governance, and commercial terms. Reduces scope disputes and establishes clear expectations.

## Invocation

```
/sow-create [project name] [scope summary]
```

If parameters are not provided, ask for:
- Project/engagement name
- High-level scope and objectives
- Client organization
- Expected timeline

## Workflow

### Step 1: Define Project Context

Gather or confirm:

1. **Background**
   - Business context and rationale
   - Strategic importance
   - Client organization details

2. **Objectives**
   - Primary objective (what success looks like)
   - Secondary objectives
   - Success metrics

3. **Scope**
   - What's IN scope
   - What's explicitly OUT of scope
   - Key assumptions

### Step 2: Structure the SOW

A comprehensive SOW includes:

```
## 1. Engagement Overview
## 2. Objectives & Success Criteria
## 3. Scope of Work
## 4. Approach & Methodology
## 5. Deliverables
## 6. Timeline & Milestones
## 7. Team & Roles
## 8. Governance
## 9. Assumptions & Dependencies
## 10. Commercial Terms
## 11. Acceptance Criteria
```

### Step 3: Develop Each Section

The SOW must be exhaustive in scope definition to prevent scope creep. Modern best practices emphasize explicit out-of-scope declarations and clear acceptance criteria.

#### Engagement Overview

```
## 1. Engagement Overview

### Background
[2-3 paragraphs on why this engagement is needed]

### Purpose
[What this SOW will accomplish]

### Scope Overview
[Brief summary of what is included]
```

#### Objectives & Success Criteria

```
## 2. Objectives & Success Criteria

### Primary Objective
[Clear statement of primary goal]

### Success Criteria
The engagement will be considered successful when:

| # | Criterion | Measurement | Target |
|---|-----------|-------------|--------|
| 1 | [Criterion 1] | [How measured] | [Target] |
| 2 | [Criterion 2] | [How measured] | [Target] |
| 3 | [Criterion 3] | [How measured] | [Target] |
```

#### Scope of Work

Be exhaustive — list all tasks and deliverables. Crucially, define what is explicitly OUT of scope to prevent scope creep:

```
## 3. Scope of Work

### In Scope
- [Deliverable or activity 1]
- [Deliverable or activity 2]
- [Deliverable or activity 3]

### Out of Scope — Explicitly Excluded
- [Activity or deliverable 1 that client might assume is included]
- [Activity or deliverable 2 that client might assume is included]
- [These exclusions prevent scope creep and misaligned expectations]

### Assumptions
- [Assumption 1]
- [Assumption 2]

### Dependencies
- [External dependency 1 - client action required]
- [External dependency 2 - third-party action required]
```

#### Approach & Methodology

```
## 4. Approach & Methodology

### Methodology
[Brief description of approach - e.g., hypothesis-driven, design thinking, etc.]

### Phase Structure

| Phase | Description | Duration |
|-------|-------------|----------|
| Phase 1 | [Name] | [Weeks] |
| Phase 2 | [Name] | [Weeks] |
| Phase 3 | [Name] | [Weeks] |
```

#### Deliverables

```
## 5. Deliverables

### Phase 1 Deliverables

| Deliverable | Description | Format | Timing |
|-------------|-------------|--------|--------|
| D1.1 | [Name] | [Format] | [When] |
| D1.2 | [Name] | [Format] | [When] |

### Phase 2 Deliverables
[...]

### Phase 3 Deliverables
[...]
```

#### Timeline & Milestones

```
## 6. Timeline & Milestones

### High-Level Timeline
[Duration: Start to Finish]

### Key Milestones

| Milestone | Description | Target Date |
|-----------|-------------|-------------|
| M1 | [Kickoff complete] | [Date] |
| M2 | [Discovery complete] | [Date] |
| M3 | [Analysis complete] | [Date] |
| M4 | [Recommendations] | [Date] |
| M5 | [Final delivery] | [Date] |

### Detailed Schedule
[Week-by-week or phase-by-phase breakdown]
```

#### Team & Roles

```
## 7. Team & Roles

### [Firm] Team

| Role | Name | Level | Commitment |
|------|------|-------|------------|
| Partner | [Name] | [Level] | [X% / as needed] |
| Principal | [Name] | [Level] | [X%] |
| Manager | [Name] | [Level] | [X%] |
| Analyst | [Name] | [Level] | [X%] |

### Client Team

| Role | Responsibility |
|------|----------------|
| [Role 1] | [Responsibility] |
| [Role 2] | [Responsibility] |
```

#### Governance

```
## 8. Governance

### Governance Structure

| Forum | Frequency | Attendees | Purpose |
|-------|-----------|-----------|---------|
| Steering Committee | [Monthly/Bi-weekly] | [C-suite], Partner | Strategic decisions |
| Working Sessions | [Weekly] | Team leads | Work progress |
| Status Reviews | [Bi-weekly] | Manager, Client lead | Status, issues |

### Escalation Path

| Issue Type | First Escalation | Second Escalation |
|------------|------------------|-------------------|
| Technical | [Role] | [Role] |
| Commercial | [Role] | [Role] |
| Strategic | [Role] | [Role] |

### Decision Rights
- [Decision 1]: [Who decides]
- [Decision 2]: [Who decides]
```

#### Commercial Terms

```
## 10. Commercial Terms

### Fees

| Component | Amount | Timing |
|-----------|--------|--------|
| Fixed Fee | $XX | [Payment terms] |
| Time & Materials | [Rate card] | [Terms] |
| Expenses | [Policy] | [Terms] |

### Payment Schedule

| Milestone | Payment | Timing |
|-----------|---------|--------|
| Contract signature | 20% | [Date] |
| Milestone 2 complete | 30% | [Date] |
| Milestone 4 complete | 30% | [Date] |
| Final delivery | 20% | [Date] |

### Change Control
[Any scope change process]

### Expenses
[Travel, third-party, etc.]
```

#### Acceptance Criteria

Define specific, measurable acceptance criteria for each deliverable. Vague criteria lead to rework and disputes:

```
## 11. Acceptance Criteria

Each deliverable will be accepted when:

| Deliverable | Acceptance Criteria | Review Period |
|-------------|-------------------|----------------|
| D1.1 | [Specific, measurable criteria - what "done" looks like] | [X business days] |
| D1.2 | [Specific, measurable criteria] | [X business days] |

### Acceptance Process
1. [Firm] delivers deliverable in specified format
2. Client reviews within [X] business days of receipt
3. Client provides written acceptance or detailed feedback
4. If rejected, [Firm] addresses feedback within [Y] business days
5. Process repeats until acceptance or dispute escalation

### Grounds for Rejection
Deliverables may only be rejected based on:
- Failure to meet specified acceptance criteria
- Material deviation from agreed scope
- Factual errors in content

### Acceptance Timeline
- Client acceptance deemed granted if no feedback within [X] business days
```

## Output Format

Generate a complete SOW document with:

1. Cover page (project name, parties, date, version)
2. All sections as structured above
3. Signature block for both parties
4. Appendices (if needed: rate card, detailed methodology)

After generating, ask:

> "Would you like me to:
> - Adjust the scope boundaries (in/out of scope)?
> - Modify the commercial terms?
> - Add detailed phase-by-phase work plans?
> - Create a pricing model variation (fixed vs. T&M)?"

## Notes

- Be specific on deliverables — vague deliverables lead to scope creep
- Define clear acceptance criteria for each deliverable
- Explicitly state what's NOT included to prevent scope expansion
- Include realistic timelines based on experience
- Ensure governance structure matches client organization
- Make payment terms align with deliverable milestones
- Include change control process for scope modifications
