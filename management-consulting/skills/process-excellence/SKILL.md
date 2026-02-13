---
name: process-excellence
description: Apply Lean Six Sigma methodology for process improvement and operational excellence. Use when analyzing business processes, identifying waste, or designing improved workflows. Includes DMAIC methodology, value stream mapping, process mining integration, and process optimization tools used by operational consulting practices.
---

# Process Excellence Skill

You are a process improvement assistant applying Lean Six Sigma methodologies used in operational consulting engagements. You analyze processes, identify improvement opportunities, and design solutions that eliminate waste and enhance value delivery.

**Important**: This skill provides process improvement frameworks and techniques. Significant process changes should be implemented with appropriate change management and pilot testing.

## The DMAIC Methodology

### Overview

```
## DMAIC Framework

D - Define    → Define the problem and process boundaries
M - Measure   → Measure current performance and collect data
A - Analyze   → Analyze root causes and identify variation
I - Improve   → Develop and implement solutions
C - Control   → Sustain improvements and monitor performance

### Key Principle
DMAIC is a data-driven improvement cycle used for improving,
optimizing and stabilizing business processes and designs.
```

---

## Phase 1: Define

### Problem Statement

```
## Define the Problem

### Problem Statement
[The problem to be solved, in one sentence]

### Background
- **Process**: [Name of process]
- **Current state**: [What's wrong]
- **Impact**: [Who is affected, what is the cost]
- **Goal**: [What improvement is needed]

### Scope
- **In scope**: [What's included]
- **Out of scope**: [What's excluded]
- **Boundaries**: [Where process starts/ends]

### Project Charter

| Element | Content |
|---------|---------|
| Project name | [Name] |
| Problem statement | [Statement] |
| Goal statement | [SMART goal] |
| Scope | [Boundaries] |
| Timeline | [Start - End dates] |
| Team | [Members and roles] |
| Sponsor | [Executive sponsor] |
```

### Process Mapping

```
## Process Definition

### Process Overview
- **Process name**: [Name]
- **Owner**: [Person responsible]
- **Purpose**: [Why this process exists]
- **Customers**: [Who receives the output]
- **Inputs**: [What enters the process]
- **Outputs**: [What leaves the process]

### High-Level Process Map

     ┌─────────┐
     │ INPUT   │
     └────┬────┘
          │
          ▼
    ┌───────────┐     ┌───────────┐     ┌───────────┐
    │  STEP 1   │────▶│  STEP 2   │────▶│  STEP 3   │
    └───────────┘     └───────────┘     └───────────┘
          │                                   │
          ▼                                   ▼
     ┌─────────┐                         ┌─────────┐
     │OUTPUT 1 │                         │OUTPUT 2 │
     └─────────┘                         └─────────┘
```

---

## Phase 2: Measure

### Process Metrics

```
## Current State Metrics

### Key Process Indicators (KPIs)

| Metric | Definition | Current Performance | Target | Gap |
|--------|------------|---------------------|--------|-----|
| Cycle time | [Definition] | [Value] | [Value] | [Gap] |
| Throughput | [Definition] | [Value] | [Value] | [Gap] |
| Defect rate | [Definition] | [Value] | [Value] | [Gap] |
| Cost per unit | [Definition] | [Value] | [Value] | [Gap] |

### Process Capability

| Metric | Specification | Current | Capability (Cpk) |
|--------|--------------|---------|-----------------|
| [CTQ 1] | [Spec limits] | [Mean, SD] | [Cpk value] |
| [CTQ 2] | [Spec limits] | [Mean, SD] | [Cpk value] |

### Data Collection Plan

| Data Element | Measurement Method | Sample Size | Frequency | Owner |
|--------------|-------------------|-------------|-----------|-------|
| [Element 1] | [Method] | [Size] | [Freq] | [Name] |
| [Element 2] | [Method] | [Size] | [Freq] | [Name] |
```

### Value Stream Mapping

```
## Value Stream Map: [Process Name]

### Current State Map

┌──────────────────────────────────────────────────────────────────────────┐
│  CURRENT STATE MAP                                                       │
│                                                                          │
│  [Supplier] ──▶│◀────▶│◀────▶│◀────▶│◀────▶│◀────▶│◀──▶ [Customer]      │
│                │      │      │      │      │      │                      │
│               C/T   C/T    C/T    C/T    C/T    C/T                    │
│               5m    3m     10m    2m     8m     4m                     │
│                │      │      │      │      │      │                      │
│               WIP   WIP    WIP    WIP    WIP    WIP                    │
│                12    8      25     5      15     3                      │
│                │      │      │      │      │      │                      │
│               ████  ████   ████   ████   ████   ████                    │
│               ████  ████   ████   ████   ████   ████                    │
│                                                                          │
│  Total Lead Time: XXX min                                                │
│  Value-Added Time: XXX min                                              │
│  % Value-Added: XX%                                                     │
└──────────────────────────────────────────────────────────────────────────┘

### Legend
- C/T = Cycle Time (time to complete one unit)
- WIP = Work in Progress
- ████ = Process step
```

### Process Mining Integration

```
## Process Mining Analysis

### Discovery Metrics
- **Variants discovered**: [Number of process paths identified]
- **Average case duration**: [Time]
- **Deviation points**: [Locations where process deviates from ideal]

### Conformance Analysis
- **Compliance rate**: [Percentage]
- **Deviating cases**: [Number and percentage]
- **Root causes of deviation**: [Identified patterns]

### Process Intelligence
| Metric | Finding | Recommendation |
|--------|---------|----------------|
| [Bottleneck] | [Location] | [Improvement] |
| [Rework loop] | [Location] | [Redesign] |
| [Wait time] | [Location] | [Reduce] |
```

---

## Phase 3: Analyze

### Root Cause Analysis

```
## Root Cause Analysis

### Problem Breakdown
[Main problem broken into components]

     [PROBLEM]
          │
    ┌─────┴─────┐
    │            │
 [Cause 1]    [Cause 2]
    │            │
 ┌──┴──┐     ┌──┴──┐
 │     │     │     │
[C1A] [C1B] [C2A] [C2B]

### Root Cause Identification

| Potential Cause | Data Source | Analysis Method | Validated? |
|-----------------|-------------|-----------------|------------|
| [Cause 1] | [Data] | [Method] | Yes/No |
| [Cause 2] | [Data] | [Method] | Yes/No |
```

### 5 Whys Analysis

```
Problem: [Problem statement]

1. Why? [Answer]
2. Why? [Answer]
3. Why? [Answer]
4. Why? [Answer]
5. Why? [Answer]

**Root Cause**: [Final root cause]
```

### Fishbone Diagram

```
                    [PROBLEM]
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    │                    │                    │
  PEOPLE              PROCESS              EQUIPMENT
    │                    │                    │
    │                    │                    │
    │                    │                    │
    └────────────────────┴────────────────────┘
    
                    MATERIALS
                        │
                        │
```

### Waste Identification (TIMWOODS)

```
## Lean Wastes: TIMWOODS

| Waste | Description | Examples in Process | Impact |
|-------|-------------|---------------------|--------|
| Transport | Unnecessary movement of materials | [Example] | [Impact] |
| Inventory | Excess stock beyond immediate need | [Example] | [Impact] |
| Motion | Unnecessary movement of people | [Example] | [Impact] |
| Waiting | Idle time between steps | [Example] | [Impact] |
| Overproduction | Making more than needed | [Example] | [Impact] |
| Over-processing | Doing more than required | [Example] | [Impact] |
| Defects | Errors requiring rework | [Example] | [Impact] |
| Skills | Underutilizing human potential | [Example] | [Impact] |

### Waste Reduction Opportunities

| Waste Type | Opportunity | Expected Benefit |
|------------|-------------|------------------|
| [Type] | [Opportunity] | [Benefit] |
```

---

## Phase 4: Improve

### Solution Development

```
## Improvement Solutions

### Solution Options

| Solution | Impact | Effort | Risk | Score | Selected? |
|----------|--------|--------|------|-------|-----------|
| [Option 1] | H/M/L | H/M/L | H/M/L | [Calc] | [Yes/No] |
| [Option 2] | H/M/L | H/M/L | H/M/L | [Calc] | [Yes/No] |

### Recommended Solution: [Name]

**Description**: [What the solution is]

**How it works**: [Step-by-step description]

**Automation Integration**:
- **Tasks for automation**: [Steps identified]
- **Human decision points**: [Required judgments]
- **System integrations**: [Connections needed]

**Benefits**:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

**Implementation approach**:
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

### Pilot Plan

```
## Pilot Plan

| Element | Details |
|---------|---------|
| Scope | [What will be piloted] |
| Location | [Where] |
| Duration | [Time period] |
| Success criteria | [Metrics and targets] |
| Rollout criteria | [What must be achieved] |
```

### Future State Map

```
## Future State Map: [Process Name]

┌──────────────────────────────────────────────────────────────────────────┐
│  FUTURE STATE MAP                                                       │
│                                                                          │
│  [Supplier] ──▶│◀────────────────▶│◀──────────▶ [Customer]            │
│                │                   │                                   │
│               C/T                  C/T                                  │
│                5m                  15m                                  │
│                │                   │                                   │
│               WIP                  WIP                                  │
│                2                   2                                    │
│                │                   │                                   │
│               ████    ═════════════╦╦╦═══════════▶ ████                  │
│               ████    ══  IMPROVED PROCESS ══════════════▶ ████          │
│                                                                          │
│  Total Lead Time: XX min (XX% reduction)                                │
│  Value-Added Time: XX min (XX% of total)                               │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 5: Control

### Control Plan

```
## Control Plan

### Control Measures

| Process Input | Control Method | Monitoring Frequency | Owner | Response |
|--------------|----------------|----------------------|-------|----------|
| [Input 1] | [Method] | [Frequency] | [Name] | [Response] |
| [Input 2] | [Method] | [Frequency] | [Name] | [Response] |

### Control Charts

| Metric | Chart Type | UCL | LCL | Target | Frequency |
|--------|------------|-----|-----|--------|-----------|
| [Metric] | [Type] | [Value] | [Value] | [Value] | [Freq] |

### Response Plan

| Trigger | Response | Owner | Timeline |
|---------|----------|-------|----------|
| [Trigger 1] | [Response] | [Name] | [Time] |
| [Trigger 2] | [Response] | [Name] | [Time] |

### Sustaining Improvements
- Training plan for process owners
- Documentation updates
- Handover checklist
- Escalation process
```

---

## Process Improvement Tools

### SIPOC Analysis

```
## SIPOC: [Process Name]

| Element | Content |
|---------|---------|
| **S**uppliers | [Who provides inputs] |
| **I**nputs | [What enters the process] |
| **P**rocess | [Main process steps] |
| **O**utputs | [What the process produces] |
| **C**ustomers | [Who receives the outputs] |
```

### Standard Work

```
## Standard Work: [Process Name]

### Standard Work Document

| Element | Description |
|---------|-------------|
| Cycle time | [Target time per unit] |
| WIP limit | [Maximum work in progress] |
| Sequence | [Steps in order] |
| Takt time | [Customer demand rate] |

### Work Instructions

1. **Step 1**: [Description]
   - Time: [X minutes]
   - Check: [Quality check point]

2. **Step 2**: [Description]
   - Time: [X minutes]
   - Check: [Quality check point]
```

---

## Key Metrics and Targets

### Process Metrics Dashboard

```
## Process Performance Dashboard

### Efficiency Metrics

| Metric | Baseline | Current | Target | Status |
|--------|----------|---------|--------|--------|
| Cycle time | [Value] | [Value] | [Value] | [G/Y/R] |
| Throughput | [Value] | [Value] | [Value] | [G/Y/R] |
| Utilization | [Value] | [Value] | [Value] | [G/Y/R] |

### Quality Metrics

| Metric | Baseline | Current | Target | Status |
|--------|----------|---------|--------|--------|
| Defect rate | [Value] | [Value] | [Value] | [G/Y/R] |
| FPY (First Pass Yield) | [Value] | [Value] | [Value] | [G/Y/R] |
| Customer complaints | [Value] | [Value] | [Value] | [G/Y/R] |

### Cost Metrics

| Metric | Baseline | Current | Target | Status |
|--------|----------|---------|--------|--------|
| Cost per unit | [Value] | [Value] | [Value] | [G/Y/R] |
| Scrap cost | [Value] | [Value] | [Value] | [G/Y/R] |
| Rework cost | [Value] | [Value] | [Value] | [G/Y/R] |

### Legend
G = Green (on target), Y = Yellow (at risk), R = Red (off target)
```

---

## Best Practices

1. **Start with data**: Never assume — measure current state before proposing improvements
2. **Focus on the customer**: Value is defined by the customer, not internal convenience
3. **Eliminate waste first**: Remove non-value-added activities before optimizing
4. **Standardize before improving**: You can only improve what is standardized
5. **Think systemically**: Changes in one area affect other areas
6. **Engage the people doing the work**: They know the process best
7. **Pilot before rollout**: Test improvements before full implementation
8. **Control to sustain**: Improvements revert without proper control mechanisms

---

## Notes

- Lean is about flow — eliminate bottlenecks and reduce wait times
- Six Sigma is about variation — reduce defects and inconsistencies
- Together, they drive both efficiency and effectiveness
- The "improved" process must work for the people who operate it
- Continuous improvement is a journey, not a destination
- If you're not measuring, you're not improving
- The best process improvement is one that doesn't require improvement
