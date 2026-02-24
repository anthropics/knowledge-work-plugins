---
description: Run an incident response workflow — triage, communicate, and write postmortem
argument-hint: "<incident description or alert>"
---

# /incident

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Manage an incident from detection through postmortem.

## Usage

```
/incident $ARGUMENTS
```

## Modes

```
/incident new [description]     # Start a new incident
/incident update [status]       # Post a status update
/incident postmortem            # Generate postmortem from incident data
```

If no mode is specified, ask what phase the incident is in. See the **incident-response** skill for severity definitions, response frameworks, and communication templates.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    INCIDENT RESPONSE                               │
├─────────────────────────────────────────────────────────────────┤
│  Phase 1: TRIAGE                                                  │
│  ✓ Assess severity (SEV1-4)                                     │
│  ✓ Identify affected systems and users                          │
│  ✓ Assign roles (IC, comms, responders)                         │
│                                                                    │
│  Phase 2: COMMUNICATE                                              │
│  ✓ Draft internal status update                                  │
│  ✓ Draft customer communication (if needed)                     │
│  ✓ Set up war room and cadence                                   │
│                                                                    │
│  Phase 3: MITIGATE                                                 │
│  ✓ Document mitigation steps taken                               │
│  ✓ Track timeline of events                                      │
│  ✓ Confirm resolution                                            │
│                                                                    │
│  Phase 4: POSTMORTEM                                               │
│  ✓ Blameless postmortem document                                 │
│  ✓ Timeline reconstruction                                       │
│  ✓ Root cause analysis (5 whys)                                  │
│  ✓ Action items with owners                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Output — Status Update

```markdown
## Incident Update: [Title]
**Severity:** SEV[1-4] | **Status:** Investigating | Identified | Monitoring | Resolved
**Impact:** [Who/what is affected]
**Last Updated:** [Timestamp]

### Current Status
[What we know now]

### Actions Taken
- [Action 1]
- [Action 2]

### Next Steps
- [What's happening next and ETA]

### Timeline
| Time | Event |
|------|-------|
| [HH:MM] | [Event] |
```

## Output — Postmortem

```markdown
## Postmortem: [Incident Title]
**Date:** [Date] | **Duration:** [X hours] | **Severity:** SEV[X]
**Authors:** [Names] | **Status:** Draft

### Summary
[2-3 sentence plain-language summary]

### Impact
- [Users affected]
- [Duration of impact]
- [Business impact if quantifiable]

### Timeline
| Time (UTC) | Event |
|------------|-------|
| [HH:MM] | [Event] |

### Root Cause
[Detailed explanation of what caused the incident]

### 5 Whys
1. Why did [symptom]? → [Because...]
2. Why did [cause 1]? → [Because...]
3. Why did [cause 2]? → [Because...]
4. Why did [cause 3]? → [Because...]
5. Why did [cause 4]? → [Root cause]

### What Went Well
- [Things that worked]

### What Went Poorly
- [Things that didn't work]

### Action Items
| Action | Owner | Priority | Due Date |
|--------|-------|----------|----------|
| [Action] | [Person] | P0/P1/P2 | [Date] |

### Lessons Learned
[Key takeaways for the team]
```

## If Connectors Available

If **~~monitoring** is connected:
- Pull alert details and metrics
- Show graphs of affected metrics

If **~~incident management** is connected:
- Create or update incident in PagerDuty/Opsgenie
- Page on-call responders

If **~~chat** is connected:
- Post status updates to incident channel
- Create war room channel

## Tips

1. **Start writing immediately** — Don't wait for complete information. Update as you learn more.
2. **Keep updates factual** — What we know, what we've done, what's next. No speculation.
3. **Postmortems are blameless** — Focus on systems and processes, not individuals.
