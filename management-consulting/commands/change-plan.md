---
description: Create change management and communication plan for transformation initiatives
argument-hint: "<initiative> <stakeholder scope>"
---

# /change-plan -- Change Management Planning

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Develop a comprehensive change management plan to drive adoption and minimize resistance during organizational transformations.

## Invocation

```
/change-plan [initiative] [stakeholder scope]
```

If parameters are not provided, ask for:
- Change initiative or project name
- Scope of stakeholders affected
- Current readiness assessment
- Timeline for change

## Workflow

### Step 1: Change Impact Assessment

Assess the scope and nature of change:

```
## Change Impact Assessment

### Change Profile

| Dimension | Assessment | Implications |
|-----------|------------|--------------|
| Scope | [Enterprise/Functions/Teams] | [Implication] |
| Depth | [Process/Tools/Behavior/Culture] | [Implication] |
| Number affected | [X people] | [Implication] |
| Urgency | [High/Medium/Low] | [Implication] |

### Stakeholder Groups

| Group | Impact Level | Change Complexity | Readiness |
|-------|--------------|------------------|-----------|
| [Group 1] | [High/Med/Low] | [High/Med/Low] | [Ready/Resistant/Uncertain] |
| [Group 2] | [High/Med/Low] | [High/Med/Low] | [Ready/Resistant/Uncertain] |
```

### Step 2: Change Readiness Analysis

Apply the Change Readiness framework:

```
## Change Readiness Assessment: [Change Initiative]

### Current State by Element

| Change Readiness Element | Current State | Gap | Strategy |
|---------------|---------------|-----|----------|
| Awareness | [High/Med/Low] | [Gap] | [Strategy] |
| Desire | [High/Med/Low] | [Gap] | [Strategy] |
| Knowledge | [High/Med/Low] | [Gap] | [Strategy] |
| Ability | [High/Med/Low] | [Gap] | [Strategy] |
| Reinforcement | [High/Med/Low] | [Gap] | [Strategy] |

### AI/Digital Change Specific Considerations
| Element | AI-Specific Considerations |
|---------|---------------------------|
| Awareness | Explain AI role, limitations, and human-AI collaboration |
| Desire | Address job security concerns, highlight new opportunities |
| Knowledge | Technical training + interpretability training |
| Ability | Hands-on practice with AI tools, sandbox environments |
| Reinforcement | AI performance monitoring, continuous learning loops |
```

### Step 3: Communication Strategy

Develop targeted communications:

```
## Communication Strategy

### Key Messages by Audience

| Audience | Core Message | Channel | Frequency | Owner |
|----------|--------------|---------|-----------|-------|
| [Audience 1] | [Message] | [Channel] | [Freq] | [Name] |
| [Audience 2] | [Message] | [Channel] | [Freq] | [Name] |

### Communication Timeline

| Phase | Message | Audience | Channel | Timing |
|-------|---------|----------|---------|--------|
| Announce | [Message] | All | Town hall | Week 1 |
| Educate | [Details] | Affected | Training | Weeks 2-4 |
| Reinforce | [Updates] | All | Newsletter | Ongoing |
```

### Step 4: Training Plan

Develop learning and enablement:

```
## Training Strategy

### Training Needs

| Group | Current Skills | Target Skills | Gap | Training Approach |
|-------|----------------|---------------|-----|-------------------|
| [Group] | [Skills] | [Skills] | [Gap] | [Approach] |

### Training Delivery

| Training | Format | Duration | Audience | Start |
|----------|--------|----------|---------|-------|
| [Training 1] | [Format] | [Time] | [Audience] | [Date] |
| [Training 2] | [Format] | [Time] | [Audience] | [Date] |
```

## Output Format

Generate a complete change management plan:

```
# Change Management Plan: [Initiative]

## Executive Summary
[Overview of change scope and approach]

## Change Impact Assessment
[Scope and stakeholder analysis]

## Change Readiness Strategy
[Approach for each Change Readiness element]

## Communication Plan
[Messaging and channel strategy]

## Training Plan
[Learning and enablement approach]

## Resistance Management
[Proactive resistance handling]

## Reinforcement Strategy
[Sustaining change]
```

## Notes

- Change management is not optional — it's integral to implementation
- Start early — change takes time
- One size doesn't fit all — customize by stakeholder
- Address resistance proactively — it won't resolve itself
- Measure change adoption — track leading indicators
- Celebrate wins — reinforcement matters
- For AI initiatives, explicitly address workforce concerns about automation
- Include AI governance and ethics in training for digital transformations
- Use digital channels (Slack, Teams, intranet) for real-time change communication
- Track adoption metrics through digital tools and usage analytics
- Build feedback loops for continuous improvement of change approach
