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

Apply the Individual Adoption framework:

```
## Change Readiness Assessment: [Change Initiative]

### Current State by Stage

| Adoption Stage | Current State | Gap | Strategy |
|----------------|---------------|-----|----------|
| Understanding | [High/Med/Low] | [Gap] | [Strategy] |
| Motivation | [High/Med/Low] | [Gap] | [Strategy] |
| Capability | [High/Med/Low] | [Gap] | [Strategy] |
| Proficiency | [High/Med/Low] | [Gap] | [Strategy] |
| Sustainability | [High/Med/Low] | [Gap] | [Strategy] |

### AI/Digital Change Specific Considerations
| Stage | AI-Specific Considerations |
|-------|---------------------------|
| Understanding | Explain AI role, limitations, and human-AI collaboration |
| Motivation | Address job security concerns, highlight new opportunities |
| Capability | Technical training + interpretability training |
| Proficiency | Hands-on practice with AI tools, sandbox environments |
| Sustainability | AI performance monitoring, continuous learning loops |
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

### Step 5: Stakeholder Engagement Strategy

Design targeted engagement by influence and disposition:

```
## Stakeholder Engagement

### Power/Interest Grid

| Stakeholder / Group | Power | Interest | Current Disposition | Target Disposition | Strategy |
|---------------------|-------|----------|--------------------|--------------------|----------|
| [Stakeholder 1] | [H/M/L] | [H/M/L] | [Champion/Supporter/Neutral/Skeptic/Resistor] | [Target] | [Manage Closely / Keep Satisfied / Keep Informed / Monitor] |
| [Stakeholder 2] | [H/M/L] | [H/M/L] | [Disposition] | [Target] | [Strategy] |

### Change Champion Network

| Champion | Department | Role in Change | Activities | Support Needed |
|----------|------------|----------------|------------|----------------|
| [Name/Role] | [Dept] | [Advocate / Trainer / Feedback channel] | [Specific activities] | [Training, materials, time allocation] |
| [Name/Role] | [Dept] | [Role] | [Activities] | [Support] |

Champion responsibilities:
- Model new behaviors and processes
- Provide peer-level coaching and support
- Collect feedback and surface concerns early
- Celebrate wins within their teams
```

### Step 6: Resistance Management

Proactively identify and address resistance:

```
## Resistance Management

### Anticipated Resistance

| Source / Group | Resistance Type | Root Cause | Mitigation Strategy | Owner |
|----------------|----------------|------------|---------------------|-------|
| [Group 1] | [Active/Passive] | [Fear of job loss / Loss of status / Uncertainty / Skill gap] | [Strategy] | [Name] |
| [Group 2] | [Type] | [Root cause] | [Strategy] | [Name] |

### Response Playbook

| Resistance Signal | Indicator | Response | Owner | Escalation |
|-------------------|-----------|----------|-------|------------|
| Vocal opposition in meetings | Direct pushback | Acknowledge concern, invite 1:1, address root cause | [Name] | If persistent → Sponsor intervention |
| Passive non-compliance | Low adoption metrics | Targeted coaching, peer support, identify barriers | [Name] | If systemic → Adjust approach |
| Shadow processes | Teams using old methods | Understand why, address gaps in new process | [Name] | If widespread → Pause and fix |
| Influencer resistance | Key person undermining | Private conversation, address concerns, co-create solution | [Name] | If unresolved → Sponsor |
```

### Step 7: Reinforcement and Adoption Measurement

Sustain change and measure adoption:

```
## Reinforcement Strategy

### Reinforcement Mechanisms
| Mechanism | Description | Timing | Owner |
|-----------|-------------|--------|-------|
| Quick wins | Celebrate early successes visibly | Weeks 2-4 | [Name] |
| Recognition | Acknowledge adopters publicly | Ongoing | [Name] |
| KPI alignment | Tie new behaviors to performance metrics | Month 2+ | [Name] |
| Coaching | Ongoing support for struggling teams | Months 2-6 | [Name] |
| Process embedding | Integrate into standard operating procedures | Month 3+ | [Name] |

### Adoption Measurement Dashboard

| Metric | Type | Target | Current | Measurement Method | Frequency |
|--------|------|--------|---------|-------------------|-----------|
| [Tool/process adoption rate] | Leading | [X%] | [Y%] | [System analytics] | Weekly |
| [Training completion] | Leading | [X%] | [Y%] | [LMS data] | Weekly |
| [Behavior change indicator] | Leading | [X%] | [Y%] | [Observation/survey] | Bi-weekly |
| [Business outcome metric] | Lagging | [Target] | [Current] | [Business data] | Monthly |
| [Employee satisfaction] | Lagging | [X/5] | [Y/5] | [Pulse survey] | Monthly |

### Pulse Survey Questions (sample)
1. I understand why we are making this change (1-5)
2. I have the tools and training I need (1-5)
3. My manager supports me through this change (1-5)
4. I can see the benefits of the new way of working (1-5)
5. I know where to go for help (1-5)
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
[Approach for each adoption stage]

## Stakeholder Engagement
[Power/interest analysis and change champion network]

## Communication Plan
[Messaging and channel strategy]

## Training Plan
[Learning and enablement approach]

## Resistance Management
[Anticipated resistance and response playbook]

## Reinforcement & Adoption
[Sustaining change and measuring adoption]
```

## Notes

- Change management is not optional — it's integral to implementation
- Start early — change takes time
- One size doesn't fit all — customize by stakeholder
- Address resistance proactively — it won't resolve itself
- Measure change adoption — track leading indicators
- Celebrate wins — reinforcement matters
- Change champions are your force multiplier — invest in them
- For AI initiatives, explicitly address workforce concerns about automation
- Include AI governance and ethics in training for digital transformations
- Use digital channels (Slack, Teams, intranet) for real-time change communication
- Track adoption metrics through digital tools and usage analytics
- Build feedback loops for continuous improvement of change approach
- Resistance is information — it tells you what you haven't addressed yet
