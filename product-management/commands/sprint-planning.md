---
description: Plan a sprint — scope work, estimate capacity, set goals, and draft a sprint plan
argument-hint: "[sprint name or date range]"
---

# /sprint-planning

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Plan a sprint by scoping work, estimating capacity, and setting clear goals.

## Usage

```
/sprint-planning $ARGUMENTS
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    SPRINT PLANNING                                 │
├─────────────────────────────────────────────────────────────────┤
│  STANDALONE (always works)                                       │
│  ✓ Define sprint goals and success criteria                     │
│  ✓ Estimate team capacity (accounting for PTO, meetings)        │
│  ✓ Scope and prioritize backlog items                           │
│  ✓ Identify dependencies and risks                              │
│  ✓ Generate sprint plan document                                │
├─────────────────────────────────────────────────────────────────┤
│  SUPERCHARGED (when you connect your tools)                      │
│  + Project tracker: Pull backlog, create sprint, assign items   │
│  + Calendar: Account for PTO and meetings in capacity           │
│  + Chat: Share sprint plan with the team                        │
└─────────────────────────────────────────────────────────────────┘
```

## What I Need From You

- **Team**: Who's on the team and their availability this sprint?
- **Sprint length**: How many days/weeks?
- **Backlog**: What's prioritized? (Pull from tracker, paste, or describe)
- **Carryover**: Anything unfinished from last sprint?
- **Dependencies**: Anything blocked on other teams?

## Output

```markdown
## Sprint Plan: [Sprint Name]
**Dates:** [Start] — [End] | **Team:** [X] engineers
**Sprint Goal:** [One clear sentence about what success looks like]

### Capacity
| Person | Available Days | Allocation | Notes |
|--------|---------------|------------|-------|
| [Name] | [X] of [Y] | [X] points/hours | [PTO, on-call, etc.] |
| **Total** | **[X]** | **[X] points** | |

### Sprint Backlog
| Priority | Item | Estimate | Owner | Dependencies |
|----------|------|----------|-------|--------------|
| P0 | [Must ship] | [X] pts | [Person] | [None / Blocked by X] |
| P1 | [Should ship] | [X] pts | [Person] | [None] |
| P2 | [Stretch] | [X] pts | [Person] | [None] |

### Planned Capacity: [X] points | Sprint Load: [X] points ([X]% of capacity)

### Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [What happens] | [What to do] |

### Definition of Done
- [ ] Code reviewed and merged
- [ ] Tests passing
- [ ] Documentation updated (if applicable)
- [ ] Product sign-off

### Key Dates
| Date | Event |
|------|-------|
| [Date] | Sprint start |
| [Date] | Mid-sprint check-in |
| [Date] | Sprint end / Demo |
| [Date] | Retro |
```

## Tips

1. **Leave buffer** — Plan to 70-80% capacity. You will get interrupts.
2. **One clear sprint goal** — If you can't state it in one sentence, the sprint is unfocused.
3. **Identify stretch items** — Know what to cut if things take longer than expected.
4. **Carry over honestly** — If something didn't ship, understand why before re-committing.
