---
description: Apply Lean Six Sigma DMAIC methodology for process optimization and continuous improvement. Use when analyzing current-state processes, identifying waste and variation, designing improved processes, and establishing control mechanisms for sustained performance.
argument-hint: "<process description or current state analysis request>"
---

# /process-improve -- Process Excellence and Continuous Improvement

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Apply Lean Six Sigma DMAIC methodology to analyze, improve, and control business processes. This command supports process optimization initiatives using proven continuous improvement practices.

## Invocation

```
/process-improve [process description or current state analysis request]
```

If no process information is provided, ask the user to describe the process they want to improve.

## Workflow

### Step 1: Define the Process Problem

Clearly articulate the process improvement opportunity with modern digital process excellence focus:

```
## Process Improvement Charter

### Problem Statement
[What is the current problem? Quantify impact: cycle time, cost, quality, customer satisfaction]

### Digital Context
| Digital Factor | Current State | Implication |
|---------------|---------------|-------------|
| AI/Automation potential | [Assessment] | [Impact on improvement approach] |
| Process digitization | [Manual/Partial/Full] | [Impact on measurement] |
| Data availability | [None/Limited/Comprehensive] | [Impact on analysis] |
| RPA opportunity | [Yes/No] | [Automation potential] |

### Scope
- **In Scope**: [Process boundaries]
- **Out of Scope**: [What's not included]

### Success Criteria
| Metric | Current State | Target State | Improvement | AI-Enhanced Target |
|--------|---------------|--------------|-------------|--------------------|
| Cycle Time | [X days/hours] | [Y days/hours] | [Z% reduction] | [Y-AI days] |
| Cost/Unit | $[Amount] | $[Amount] | [Z% reduction] | $[AI target] |
| Defect Rate | [X%] | [Y%] | [Z% reduction] | [Y with AI] |
| Throughput | [X units/day] | [Y units/day] | [Z% increase] | [Y with AI] |

### Timeline
- Define: [Date]
- Measure: [Date]
- Analyze: [Date]
- Improve: [Date]
- Control: [Date]

### Team
- Process Owner: [Name]
- Sponsor: [Name]
- Green Belt/Lead: [Name]
- Team Members: [Names]
- **AI/Automation Specialist**: [Name - if applicable]
```

### Step 2: Measure Current State

Collect baseline data and map the process:

```
## Process Measurement

### Process Mapping
Create detailed process maps:
- **SIPOC Diagram**: Suppliers, Inputs, Process, Outputs, Customers
- **Value Stream Map**: End-to-end flow with value-added vs. non-value-added time
- **Process Flow Chart**: Detailed steps with decision points

### Baseline Metrics
| Metric | Measurement Method | Sample Size | Current Baseline | Sigma Level |
|--------|-------------------|-------------|------------------|-------------|
| [Metric 1] | [Method] | [n] | [Value] | [σ] |
| [Metric 2] | [Method] | [n] | [Value] | [σ] |

### Data Collection Plan
| Data Point | Definition | Collection Method | Frequency | Responsible |
|------------|------------|-------------------|-----------|-------------|
| [Point 1] | [Definition] | [Method] | [Freq] | [Name] |
| [Point 2] | [Definition] | [Method] | [Freq] | [Name] |

### Process Capability Analysis
- Cp/Cpk indices: [Values]
- Process stability: [Stable/Unstable]
- Common cause vs. special cause variation: [Assessment]
```

### Step 3: Analyze Root Causes

Identify and validate the sources of process variation and waste:

```
## Root Cause Analysis

### Waste Identification (TIMWOODS)
| Waste Type | Evidence | Impact | Priority |
|------------|---------|--------|----------|
| Transportation | [Evidence] | [Impact] | [High/Med/Low] |
| Inventory | [Evidence] | [Impact] | [High/Med/Low] |
| Motion | [Evidence] | [Impact] | [High/Med/Low] |
| Waiting | [Evidence] | [Impact] | [High/Med/Low] |
| Overproduction | [Evidence] | [Impact] | [High/Med/Low] |
| Overprocessing | [Evidence] | [Impact] | [High/Med/Low] |
| Defects | [Evidence] | [Impact] | [High/Med/Low] |
| Skills (underutilized) | [Evidence] | [Impact] | [High/Med/Low] |

### Root Cause Tools

#### 5 Whys Analysis
```
Problem: [Problem statement]
Why 1: [First cause] → Why 2: [Second cause] → Why 3: [Third cause]
→ Why 4: [Fourth cause] → Why 5: [Root cause]
```

#### Fishbone Diagram (Ishikawa)
```
                    [Effect]
                       │
    ┌─────────┬────────┼────────┬─────────┐
    ▼         ▼        ▼        ▼         ▼
[People]  [Process]  [Machine] [Material] [Environment]
    │         │        │        │         │
 [Cause]   [Cause]   [Cause]   [Cause]   [Cause]
```

### Hypothesis Testing
| Hypothesis | Test Method | Result | Validated? |
|------------|-------------|--------|------------|
| [H1] | [Test] | [Result] | [Yes/No] |
| [H2] | [Test] | [Result] | [Yes/No] |

### Prioritized Root Causes
| Root Cause | Impact (Pareto %) | Evidence Strength | Recommendation |
|------------|-------------------|-------------------|----------------|
| [RC1] | [X%] | [Strong/Medium/Weak] | [Address] |
| [RC2] | [X%] | [Strong/Medium/Weak] | [Address] |
| [RC3] | [X%] | [Strong/Medium/Weak] | [Monitor] |
```

### Step 4: Design and Implement Improvements

Develop and deploy optimized process solutions:

```
## Process Improvement Solutions

### Solution Options Matrix
| Solution | Impact | Effort | Cost | Risk | Recommendation |
|----------|--------|--------|------|------|----------------|
| [S1] | [High/Med/Low] | [High/Med/Low] | $[Amount] | [Low/Med/High] | [Select] |
| [S2] | [High/Med/Low] | [High/Med/Low] | $[Amount] | [Low/Med/High] | [Select] |
| [S3] | [High/Med/Low] | [High/Med/Low] | $[Amount] | [Low/Med/High] | [Contingency] |

### Selected Solution: [Solution Name]

#### Solution Design
[Detailed description of the improved process]

#### Implementation Plan
| Phase | Activity | Owner | Timeline | Dependencies |
|-------|----------|-------|----------|--------------|
| 1 | [Activity] | [Owner] | [Dates] | [Deps] |
| 2 | [Activity] | [Owner] | [Dates] | [Deps] |
| 3 | [Activity] | [Owner] | [Dates] | [Deps] |

#### Pilot Results
| Metric | Baseline | Pilot Target | Pilot Actual | Improvement |
|--------|----------|--------------|--------------|-------------|
| [M1] | [Value] | [Value] | [Value] | [X%] |
| [M2] | [Value] | [Value] | [Value] | [X%] |

#### Full Rollout Plan
- Training: [Plan]
- Communication: [Plan]
- Rollout schedule: [Timeline]
- Support model: [Model]
```

### Step 5: Establish Control Mechanisms

Ensure sustained improvement through monitoring and control systems:

```
## Control Phase

### Control Plan
| Process Output | Measurement | Control Method | Frequency | Response Plan |
|----------------|-------------|----------------|-----------|---------------|
| [Output 1] | [Metric] | [Control chart / Check sheet] | [Freq] | [Response] |
| [Output 2] | [Metric] | [Control chart / Check sheet] | [Freq] | [Response] |

### Control Charts
- Chart type: [X-bar R / X-bar S / I-MR / P-chart / C-chart]
- Upper Control Limit (UCL): [Value]
- Lower Control Limit (LCL): [Value]
- Center Line (CL): [Value]

### Standard Work Documentation
- Updated process flow: [Location]
- Work instructions: [Location]
- SOPs: [Location]
- Training materials: [Location]

### Monitoring Dashboard
| KPI | Target | Actual | Status | Trend |
|-----|--------|--------|--------|-------|
| [KPI 1] | [Target] | [Actual] | [RAG] | [↑/→/↓] |
| [KPI 2] | [Target] | [Actual] | [RAG] | [↑/→/↓] |

### Response Protocol
1. [Trigger]: [Action]
2. [Trigger]: [Action]
3. [Trigger]: [Action]

### Handover Checklist
- [ ] Control charts deployed
- [ ] Response plan documented
- [ ] Process owner trained
- [ ] SOPs updated
- [ ] Training completed
- [ ] Dashboard live
- [ ] Lessons learned documented
```

## Output Format

```
# Process Improvement Report: [Process Name]

## Executive Summary
[2-3 paragraphs summarizing the problem, approach, and results]

## 1. Define
### Problem Statement
[Quantified problem with business impact]

### Charter
[Scope, timeline, team, success criteria]

## 2. Measure
### Process Maps
[SIPOC, Value Stream Map, Flow Chart]

### Baseline Performance
[Current state metrics with sigma levels]

### Process Capability
[Cp/Cpk analysis, variation assessment]

## 3. Analyze
### Root Cause Analysis
[5 Whys, Fishbone, Pareto analysis]

### Validated Causes
[Prioritized list with evidence]

## 4. Improve
### Solutions Considered
[Options matrix with evaluation]

### Selected Solution
[Detailed design and implementation plan]

### Results
[Before/after comparison with quantified impact]

## 5. Control
### Control Plan
[Monitoring approach and response protocols]

### Sustained Performance
[Current metrics with trend analysis]

### Handover
[Documentation and knowledge transfer summary]

## Financial Impact
| Category | Amount |
|----------|--------|
| Cost savings (annual) | $[Amount] |
| Revenue impact | $[Amount] |
| One-time implementation cost | $[Amount] |
| ROI | [X%] |
| Payback period | [X months] |
```

## Notes

- Always baseline current performance before proposing improvements
- Use statistical methods to validate root causes, not just intuition
- Pilot solutions before full rollout whenever possible
- Ensure control mechanisms are practical and sustainable
- Document everything for knowledge transfer and audit trails
- Engage process owners early and throughout the improvement journey
- Consider digital/automation opportunities in the improve phase
- TIMWOODS waste categories should be reviewed for every process
- Incorporate AI/ML for process mining and pattern detection
- Apply intelligent automation (IPA) for cognitive tasks
- Use digital twins for process simulation before implementation
- Consider sustainability (green lean) in improvement designs
- Apply predictive analytics for proactive control mechanisms
- Include cybersecurity considerations in process digitization
- Leverage low-code platforms for rapid improvement implementation
