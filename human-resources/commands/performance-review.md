---
description: Structure a performance review with self-assessment, manager template, and calibration prep
argument-hint: "<employee name or review cycle>"
---

# /performance-review

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate performance review templates and help structure feedback.

## Usage

```
/performance-review $ARGUMENTS
```

## Modes

```
/performance-review self-assessment       # Generate self-assessment template
/performance-review manager [employee]    # Manager review template for a specific person
/performance-review calibration           # Calibration prep document
```

If no mode is specified, ask what type of review they need.

## Output — Self-Assessment Template

```markdown
## Self-Assessment: [Review Period]

### Key Accomplishments
[List your top 3-5 accomplishments this period. For each, describe the situation, your contribution, and the impact.]

1. **[Accomplishment]**
   - Situation: [Context]
   - Contribution: [What you did]
   - Impact: [Measurable result]

### Goals Review
| Goal | Status | Evidence |
|------|--------|----------|
| [Goal from last period] | Met / Exceeded / Missed | [How you know] |

### Growth Areas
[Where did you grow? New skills, expanded scope, leadership moments.]

### Challenges
[What was hard? What would you do differently?]

### Goals for Next Period
1. [Goal — specific and measurable]
2. [Goal]
3. [Goal]

### Feedback for Manager
[How can your manager better support you?]
```

## Output — Manager Review

```markdown
## Performance Review: [Employee Name]
**Period:** [Date range] | **Manager:** [Your name]

### Overall Rating: [Exceeds / Meets / Below Expectations]

### Performance Summary
[2-3 sentence overall assessment]

### Key Strengths
- [Strength with specific example]
- [Strength with specific example]

### Areas for Development
- [Area with specific, actionable guidance]
- [Area with specific, actionable guidance]

### Goal Achievement
| Goal | Rating | Comments |
|------|--------|----------|
| [Goal] | [Rating] | [Specific observations] |

### Impact and Contributions
[Describe their biggest contributions and impact on the team/org]

### Development Plan
| Skill | Current | Target | Actions |
|-------|---------|--------|---------|
| [Skill] | [Level] | [Level] | [How to get there] |

### Compensation Recommendation
[Promotion / Equity refresh / Adjustment / No change — with justification]
```

## Output — Calibration

```markdown
## Calibration Prep: [Review Cycle]
**Manager:** [Your name] | **Team:** [Team] | **Period:** [Date range]

### Team Overview
| Employee | Role | Level | Tenure | Proposed Rating | Notes |
|----------|------|-------|--------|-----------------|-------|
| [Name] | [Role] | [Level] | [X years] | [Rating] | [Key context] |

### Rating Distribution
| Rating | Count | % of Team | Company Target |
|--------|-------|-----------|----------------|
| Exceeds Expectations | [X] | [X]% | ~15-20% |
| Meets Expectations | [X] | [X]% | ~60-70% |
| Below Expectations | [X] | [X]% | ~10-15% |

### Calibration Discussion Points
1. **[Employee]** — [Why this rating may need discussion, e.g., borderline, first review at level, recent role change]
2. **[Employee]** — [Discussion point]

### Promotion Candidates
| Employee | Current Level | Proposed Level | Justification |
|----------|-------------|----------------|---------------|
| [Name] | [Current] | [Proposed] | [Evidence of next-level performance] |

### Compensation Actions
| Employee | Action | Justification |
|----------|--------|---------------|
| [Name] | [Promotion / Equity refresh / Market adjustment / Retention] | [Why] |

### Manager Notes
[Context the calibration group should know — team changes, org shifts, project impacts]
```

## If Connectors Available

If **~~HRIS** is connected:
- Pull prior review history and goal tracking data
- Pre-populate employee details and current role information

If **~~project tracker** is connected:
- Pull completed work and contributions for the review period
- Reference specific tickets and project milestones as evidence

## Tips

1. **Be specific** — "Great job" isn't feedback. "You reduced deploy time 40% by implementing the new CI pipeline" is.
2. **Balance positive and constructive** — Both are essential. Neither should be a surprise.
3. **Focus on behaviors, not personality** — "Your documentation has been incomplete" vs. "You're careless."
4. **Make development actionable** — "Improve communication" is vague. "Present at the next team all-hands" is actionable.
