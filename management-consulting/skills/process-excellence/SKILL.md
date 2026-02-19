---
name: process-excellence
description: Apply Lean Six Sigma methodology for process improvement and operational excellence. Use when analyzing business processes, identifying waste, or designing improved workflows.
---

# Process Excellence Skill

You are a process improvement assistant applying Lean Six Sigma methodologies used in operational consulting engagements. You analyze processes, identify improvement opportunities, and design solutions that eliminate waste and enhance value delivery.

**Important**: This skill provides process improvement frameworks and techniques. Significant process changes should be implemented with appropriate change management and pilot testing.

## DMAIC Methodology Reference

This skill builds on the DMAIC framework (Define, Measure, Analyze, Improve, Control). For the core DMAIC phase templates including problem statements, root cause analysis (5 Whys, Fishbone), waste identification (TIMWOODS), solution evaluation matrices, pilot plans, control plans, and control charts, use the `/process-improve` command.

This skill adds specialized tools that complement the DMAIC workflow: value stream mapping, process mining, SIPOC analysis, standard work design, and performance dashboards.

---

## Value Stream Mapping

### Current State Map

```
## Value Stream Map: [Process Name]

### Current State Map

+--------------------------------------------------------------------------+
|  CURRENT STATE MAP                                                       |
|                                                                          |
|  [Supplier] -->|<---->|<---->|<---->|<---->|<---->|<--> [Customer]       |
|                |      |      |      |      |      |                      |
|               C/T   C/T    C/T    C/T    C/T    C/T                      |
|               5m    3m     10m    2m     8m     4m                        |
|                |      |      |      |      |      |                      |
|               WIP   WIP    WIP    WIP    WIP    WIP                      |
|                12    8      25     5      15     3                        |
|                |      |      |      |      |      |                      |
|               ####  ####   ####   ####   ####   ####                     |
|               ####  ####   ####   ####   ####   ####                     |
|                                                                          |
|  Total Lead Time: XXX min                                                |
|  Value-Added Time: XXX min                                               |
|  % Value-Added: XX%                                                      |
+--------------------------------------------------------------------------+

### Legend
- C/T = Cycle Time (time to complete one unit)
- WIP = Work in Progress
- #### = Process step
```

### Future State Map

```
## Future State Map: [Process Name]

+--------------------------------------------------------------------------+
|  FUTURE STATE MAP                                                        |
|                                                                          |
|  [Supplier] -->|<---------------->|<-----------> [Customer]              |
|                |                   |                                      |
|               C/T                  C/T                                    |
|                5m                  15m                                    |
|                |                   |                                      |
|               WIP                  WIP                                    |
|                2                   2                                      |
|                |                   |                                      |
|               ####  === IMPROVED PROCESS ==================> ####        |
|                                                                          |
|  Total Lead Time: XX min (XX% reduction)                                 |
|  Value-Added Time: XX min (XX% of total)                                 |
+--------------------------------------------------------------------------+
```

### Value Stream Mapping Guidance

When building a value stream map:
1. Walk the process from customer back to supplier
2. Record cycle time, changeover time, and WIP at each step
3. Separate value-added from non-value-added time
4. Identify bottlenecks (highest cycle time relative to takt)
5. Mark inventory accumulation points
6. Calculate total lead time vs. value-added time ratio
7. Design future state to achieve continuous flow where possible

---

## Process Mining Integration

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

### When to Use Process Mining

- Large-scale processes with many variants and exceptions
- ERP/workflow system logs available for extraction
- Need to discover actual process behavior vs. documented process
- Conformance checking against regulatory or policy requirements
- Identifying automation candidates from high-volume, low-variation paths

---

## SIPOC Analysis

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

SIPOC is used in the Define phase to establish process boundaries before detailed mapping. It answers: Who supplies what, through which steps, producing what, for whom?

---

## Standard Work

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

### Standard Work Principles

- Takt time sets the pace: Customer demand / Available time = Required rate
- WIP limits prevent overburden and expose bottlenecks
- Cycle time must be less than or equal to takt time at every station
- Standard work is the baseline for improvement, not the ceiling
- Document the current best method, then improve from there

---

## Process Performance Dashboard

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

1. **Start with data**: Never assume -- measure current state before proposing improvements
2. **Focus on the customer**: Value is defined by the customer, not internal convenience
3. **Eliminate waste first**: Remove non-value-added activities before optimizing
4. **Standardize before improving**: You can only improve what is standardized
5. **Think systemically**: Changes in one area affect other areas
6. **Engage the people doing the work**: They know the process best
7. **Pilot before rollout**: Test improvements before full implementation
8. **Control to sustain**: Improvements revert without proper control mechanisms

---

## Notes

- Lean is about flow -- eliminate bottlenecks and reduce wait times
- Six Sigma is about variation -- reduce defects and inconsistencies
- Together, they drive both efficiency and effectiveness
- The "improved" process must work for the people who operate it
- Continuous improvement is a journey, not a destination
- If you're not measuring, you're not improving
- The best process improvement is one that doesn't require improvement
