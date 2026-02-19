---
description: Map stakeholders, assess influence and interest, and develop engagement strategies. Use when starting engagements, managing complex change initiatives, navigating organizational politics, or aligning diverse stakeholder groups around strategic decisions.
argument-hint: "<project or initiative context>"
---

# /stakeholder-map -- Stakeholder Mapping and Engagement Strategy

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Identify, analyze, and develop engagement strategies for all stakeholders in an initiative. Creates influence maps, communication plans, and resistance management strategies.

## Invocation

```
/stakeholder-map [project or initiative context]
```

If no context is provided, ask for:
- Project or initiative name
- Organization and scope
- Key decisions or changes stakeholders are involved in
- Known stakeholder concerns or dynamics

## Workflow

### Step 1: Identify Stakeholders

Build a comprehensive stakeholder inventory:

```
## Stakeholder Inventory

### Internal Stakeholders
| Name/Role | Function | Relationship to Initiative | Current Stance |
|-----------|----------|---------------------------|----------------|
| [Name] | [C-suite / VP / Director / Manager] | [Sponsor / Decision-maker / Contributor / Affected] | [Champion / Supporter / Neutral / Skeptic / Opponent] |

### External Stakeholders
| Name/Role | Organization | Relationship to Initiative | Current Stance |
|-----------|-------------|---------------------------|----------------|
| [Name] | [Organization] | [Client / Regulator / Partner / Vendor] | [Stance] |

### Stakeholder Groups
| Group | Size | Influence | Impact on Them | Priority |
|-------|------|-----------|----------------|----------|
| [Group 1] | [n] | [High/Med/Low] | [High/Med/Low] | [1-5] |
```

### Step 2: Analyze Influence and Interest

Map stakeholders on the power-interest grid:

```
## Influence-Interest Analysis

### Power-Interest Grid
                    HIGH INTEREST
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    │   KEEP SATISFIED   │   MANAGE CLOSELY   │
    │                    │                    │
    │   - Regular updates│   - Active engagement│
    │   - Address concerns│  - Co-creation     │
    │                    │   - Regular 1:1s    │
HIGH├────────────────────┼────────────────────┤
POWER                    │
    │                    │                    │
    │   MONITOR          │   KEEP INFORMED    │
    │                    │                    │
    │   - Periodic check │   - Regular comms  │
    │   - Watch for      │   - Feedback loops │
    │     changes        │   - Town halls     │
    │                    │                    │
    └────────────────────┼────────────────────┘
                    LOW INTEREST

### Stakeholder Positioning
| Stakeholder | Power (1-5) | Interest (1-5) | Quadrant | Strategy |
|-------------|-------------|----------------|----------|----------|
| [Name] | [Score] | [Score] | [Manage Closely / Keep Satisfied / Keep Informed / Monitor] | [Approach] |
```

### Step 3: Assess Alignment and Resistance

Evaluate stakeholder readiness and barriers:

```
## Alignment Assessment

### Current vs. Desired State
| Stakeholder | Current Position | Desired Position | Gap | Difficulty |
|-------------|-----------------|------------------|-----|------------|
| [Name] | [Opponent / Skeptic / Neutral / Supporter / Champion] | [Target position] | [Size] | [High/Med/Low] |

### Resistance Analysis
| Stakeholder | Resistance Type | Root Cause | Severity | Mitigation |
|-------------|----------------|------------|----------|------------|
| [Name] | [Rational / Emotional / Political / Cultural] | [Why they resist] | [High/Med/Low] | [Approach] |

### Influence Networks
| Stakeholder | Influences | Influenced By | Coalition Opportunity |
|-------------|-----------|---------------|----------------------|
| [Name] | [Who they influence] | [Who influences them] | [Potential alliance] |
```

### Step 4: Develop Engagement Strategy

Create targeted engagement plans:

```
## Engagement Strategy

### By Stakeholder
| Stakeholder | Objective | Key Messages | Channel | Frequency | Owner |
|-------------|-----------|-------------|---------|-----------|-------|
| [Name] | [What we need from them] | [Tailored message] | [1:1 / Meeting / Email / Workshop] | [Weekly / Biweekly / Monthly] | [Team member] |

### Communication Plan
| Audience | Message | Format | Timing | Sender |
|----------|---------|--------|--------|--------|
| [Group] | [Key message] | [Presentation / Email / Town hall / Workshop] | [When] | [Who] |

### Escalation Triggers
| Signal | Meaning | Response | Escalate To |
|--------|---------|----------|-------------|
| [Observable behavior] | [What it indicates] | [Immediate action] | [Person/group] |
```

### Step 5: Build Coalition Strategy

Identify and activate champions:

```
## Coalition Building

### Champion Activation
| Champion | Sphere of Influence | Activation Approach | Support Needed |
|----------|-------------------|---------------------|----------------|
| [Name] | [Who they can mobilize] | [How to engage them] | [Resources / Air cover / Information] |

### Coalition Map
| Coalition | Members | Shared Interest | Collective Influence | Status |
|-----------|---------|----------------|---------------------|--------|
| [Name] | [Members] | [Common ground] | [High/Med/Low] | [Forming / Active / Stable] |

### Quick Wins for Buy-In
| Action | Target Stakeholder | Expected Impact | Timeline |
|--------|-------------------|-----------------|----------|
| [Quick win] | [Who benefits] | [Credibility / Trust / Proof] | [When] |
```

## Output Format

Generate:

1. **Stakeholder Map** — Visual grid with all stakeholders positioned by power and interest
2. **Engagement Strategy** — Tailored approach for each key stakeholder
3. **Communication Plan** — Messages, channels, and timing
4. **Coalition Strategy** — Champion activation and alliance building
5. **Risk Register** — Stakeholder-related risks and mitigation

## Notes

- Stakeholder positions shift over time — revisit the map regularly
- Informal influence is often more important than formal authority
- Listen before you advocate — understand concerns before proposing solutions
- Build coalitions of supporters before tackling resistors
- One-on-one conversations are more effective than group presentations for difficult stakeholders
- Document commitments and follow through consistently
- Cultural context matters — adapt engagement style to organizational norms
- Look for mutual benefits, not just compliance
- Early engagement prevents late-stage resistance
- Stakeholder mapping is confidential — handle with care
