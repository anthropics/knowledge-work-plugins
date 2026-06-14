---
name: process-excellence
description: Apply Lean Six Sigma methodology for process improvement and operational excellence. Covers the full DMAIC cycle (Define, Measure, Analyze, Improve, Control), value stream mapping, process mining, waste identification, root cause analysis, and sustained performance control. Use when analyzing business processes, identifying inefficiencies, or designing improved workflows.
---

# Process Excellence

Apply Lean Six Sigma methodology to analyze, improve, and control business processes. Lean eliminates waste and improves flow. Six Sigma reduces variation and defects. Together they drive both efficiency and effectiveness.

## Before You Begin

Process improvement requires real process data. Ask for it rather than building on assumptions:
- What process is in scope, and what are its boundaries (start point, end point)?
- What metrics exist today (cycle time, error rates, volumes, cost per transaction)?
- What has been tried before to improve this process?
- Present industry benchmarks as reference points for comparison, not as targets for the user's specific process. When using numbers the user hasn't provided, flag them: "I'm using the median industry benchmark of X days for [process type]. How does your actual cycle time compare?"

## Lean vs. Six Sigma: When to Use Which

The two methodologies solve different problems. Choosing the wrong lens wastes time.

| Dimension | Lean Focus | Six Sigma Focus |
|-----------|-----------|----------------|
| Core problem | Waste and flow | Variation and defects |
| Primary question | "Why does this take so long?" | "Why is the output inconsistent?" |
| Typical symptoms | Long cycle times, excess WIP, many handoffs, waiting | High defect rates, rework, unpredictable output quality |
| Key tools | Value stream mapping, 5S, kanban, pull systems | Control charts, hypothesis testing, DPMO, Cp/Cpk |
| Best for | Service processes, order fulfillment, onboarding, approval chains | Manufacturing quality, transaction accuracy, compliance processes |

**Use Lean when** the process takes too long, costs too much, or has too many steps. The problem is waste and flow.

**Use Six Sigma when** the process produces inconsistent results, high defect rates, or unpredictable output. The problem is variation.

**Use both when** (most common in practice) you have flow problems AND quality problems. Start with Lean to simplify, then apply Six Sigma to stabilize what remains.

## DMAIC Methodology

DMAIC (Define, Measure, Analyze, Improve, Control) is the structured approach for improving existing processes. Each phase has specific deliverables and gate criteria before moving to the next.

### Define

Clearly articulate the improvement opportunity before jumping to solutions.

**Problem statement**: Quantify the current problem in terms of cycle time, cost, quality, or customer satisfaction. A vague problem statement produces vague solutions.

**Scope**: Define what's in scope and what's not. Process improvement projects that try to fix everything fix nothing.

**Success criteria**: Establish measurable targets for each key metric. Include current state, target state, and the percentage improvement expected.

**Project charter elements**:
- Problem statement with quantified impact
- Process boundaries (start point, end point)
- Success metrics with baselines and targets
- Timeline for each DMAIC phase
- Team: process owner, sponsor, project lead, team members

**Project charter template**:

```
PROJECT CHARTER: [Process Name] Improvement

Problem Statement:
[Specific, quantified description of the problem]
Example: "Order-to-cash cycle time averages 45 days vs. industry benchmark
of 15 days, trapping ~$20M in working capital and generating $2.1M/year in
excess financing costs."

Scope:
  In scope:    [Start point] to [End point]
  Out of scope: [Explicitly excluded elements]

Success Metrics:
| Metric           | Baseline | Target   | Improvement |
|------------------|----------|----------|-------------|
| Cycle time       | 45 days  | 20 days  | -56%        |
| DSO              | 62 days  | 38 days  | -39%        |
| First pass yield | 72%      | 95%      | +32%        |

Timeline:
  Define:  Weeks 1-2    Measure: Weeks 3-4    Analyze: Weeks 5-6
  Improve: Weeks 7-10   Control: Weeks 11-12

Team:
  Sponsor:       [Name, Title]
  Process Owner:  [Name, Title]
  Project Lead:   [Name, Title]
  Team Members:   [Names]
```

**Digital context**: Assess automation potential, current level of process digitization, data availability, and RPA opportunity. This shapes the analysis approach and solution space.

### Measure

Collect baseline data and map the process as it actually operates (not as documentation says it should).

**Process mapping**: Create a SIPOC diagram (Suppliers, Inputs, Process, Outputs, Customers) to establish boundaries, then map the detailed process flow with decision points and handoffs.

**Baseline metrics**: For each key metric, document the measurement method, sample size, current baseline, and sigma level.

**Sigma level calculation**: Sigma level translates defect rates into a universal quality metric. Here's how to calculate it:

```
Step 1: Define what constitutes a "defect" (any output not meeting specification)
Step 2: Count defects and opportunities

  DPMO = (Number of Defects / Total Opportunities) x 1,000,000

Step 3: Convert DPMO to sigma level:

  | DPMO      | Sigma Level | Yield   | Plain English             |
  |-----------|-------------|---------|---------------------------|
  | 691,462   | 1.0 sigma   | 30.9%   | Barely functioning        |
  | 308,538   | 2.0 sigma   | 69.1%   | Poor                      |
  | 66,807    | 3.0 sigma   | 93.3%   | Average                   |
  | 6,210     | 4.0 sigma   | 99.4%   | Good                      |
  | 233       | 5.0 sigma   | 99.98%  | Very good                 |
  | 3.4       | 6.0 sigma   | 99.9997%| World class               |

Example: Invoice processing
  - 10,000 invoices processed per month
  - 450 contain errors (wrong amount, wrong address, missing PO)
  - Each invoice has 4 opportunities for error
  - DPMO = (450 / 40,000) x 1,000,000 = 11,250
  - Sigma level: ~3.8 (between 3.0 and 4.0)
  - Target: 4.0 sigma (6,210 DPMO = ~248 errors/month)
```

**Data collection plan**: Specify each data point, its operational definition, collection method, frequency, and responsible person. Ambiguous definitions produce unreliable data.

**Process capability analysis**:
- Cp/Cpk indices (process capability relative to specifications)
- Process stability assessment (in control vs. out of control)
- Common cause vs. special cause variation

### Analyze

Identify and validate root causes of process variation and waste. This is where discipline matters most. Don't skip to solutions.

**Waste identification (TIMWOODS)**:

| Waste Type | What to Look For |
|------------|-----------------|
| Transportation | Unnecessary movement of materials or information between steps |
| Inventory | Work piling up between process steps, excess WIP |
| Motion | Unnecessary movement of people (extra clicks, walking, searching) |
| Waiting | People or work idle, waiting for approvals, inputs, or capacity |
| Overproduction | Producing more, sooner, or faster than the next step requires |
| Overprocessing | Doing more work than the customer requires or values |
| Defects | Errors requiring rework, correction, or scrapping |
| Skills (underutilized) | People doing work below their capability, untapped expertise |

**Service industry TIMWOODS examples** (most waste literature skews manufacturing; here's what each looks like in services):

| Waste Type | Service Industry Example |
|------------|------------------------|
| Transportation | Customer data re-entered across 3 systems because they don't integrate; loan application forwarded through 5 departments |
| Inventory | 2,000 unprocessed insurance claims in a queue; 500 unreviewed job applications backlogging HR |
| Motion | Agent toggling between 8 browser tabs to resolve one support ticket; nurse walking to a different floor for supplies |
| Waiting | Customer on hold 12 minutes for a transfer; contract sitting 9 days in legal review queue |
| Overproduction | Generating monthly reports nobody reads; pre-populating 50 onboarding forms when only 20 are needed |
| Overprocessing | Four levels of approval for a $200 purchase; manually formatting data that will be reformatted downstream |
| Defects | Incorrect invoice sent to client requiring credit note; wrong patient information on a lab order |
| Skills | Senior analyst doing data entry; licensed clinician handling scheduling tasks |

**Root cause tools**:

5 Whys: Start with the problem statement and ask "why" iteratively until you reach a root cause you can act on. Typically 3-5 iterations. The root cause should be something the team can influence.

Fishbone (Ishikawa) diagram: Organize potential causes into categories (People, Process, Machine, Material, Environment, Measurement). Useful for brainstorming with the team and ensuring you haven't missed a category.

**Hypothesis testing**: For each suspected root cause, define a hypothesis, test method, and acceptance criteria. Validate with data, not intuition.

**Pareto analysis**: Rank root causes by their contribution to the problem. Typically 20% of causes drive 80% of the impact. Address the vital few, not the trivial many.

### Improve

Design and deploy optimized process solutions.

**Solution evaluation matrix**: Score each potential solution on impact, effort, cost, and risk. Separate high-impact/low-effort wins from longer-term structural changes. Impact estimates require baseline process data from the Measure phase. If the matrix is built before Measure data is available, leave impact scores blank and flag them as pending. After populating with actuals, re-score the matrix and use it to drive the pilot selection conversation with the process owner.

**Pilot before rollout**: Test improvements in a controlled setting before full implementation. Measure pilot results against baseline and target. A solution that works in theory but fails in practice isn't a solution.

**Robotic Process Automation (RPA)**: For high-volume, rule-based, repetitive tasks identified during analysis, RPA is a solution pattern worth evaluating before redesigning the process itself.

RPA is a good fit when:
- The task is rule-based with clear decision logic (no judgment calls)
- Volume is high enough to justify bot development and maintenance
- The underlying systems lack APIs or integration options
- The process is stable (frequent process changes break bots)

RPA is a poor fit when:
- The process itself is broken (automating waste just produces waste faster)
- Inputs are unstructured or highly variable
- The process requires human judgment or exception handling for most cases
- A system integration or API would solve the problem more durably

**Common RPA candidates from process analysis**: invoice data extraction, employee onboarding form population, report generation and distribution, order status checking across systems, reconciliation between two data sources.

**Rule of thumb**: Fix the process first (eliminate waste, reduce variation), then automate what remains. RPA on top of a bad process locks in the bad process.

**Implementation planning**: Phase the rollout with clear activities, owners, timelines, and dependencies. Include training and communication alongside the technical changes.

**Full rollout plan**:
- Training for all affected staff
- Communication to stakeholders
- Phased schedule with go/no-go checkpoints
- Support model during transition

### Control

Ensure improvements are sustained. Without control mechanisms, processes revert to their pre-improvement state within months.

**Control plan**: For each critical process output, define the measurement, control method (control chart, checklist, automated alert), monitoring frequency, and response plan for out-of-control conditions.

**Control charts**: Select the appropriate chart type based on data characteristics:
- X-bar R / X-bar S: variable data, subgroups
- I-MR: variable data, individual measurements
- P-chart: proportion defective
- C-chart: count of defects

Define Upper Control Limit (UCL), Lower Control Limit (LCL), and Center Line (CL).

**Standard work documentation**: Update process flows, work instructions, SOPs, and training materials to reflect the improved process. If it's not documented, it will drift.

**Response protocol**: Define specific triggers and their required responses. When metric X exceeds threshold Y, person Z takes action A within timeframe T.

**Handover checklist**:
- Control charts deployed and understood
- Response plan documented and tested
- Process owner trained on monitoring
- SOPs updated and accessible
- Training completed for all operators
- Dashboard live and accurate
- Lessons learned documented

## Value Stream Mapping

### Building a Value Stream Map

Value stream mapping visualizes the end-to-end flow of materials and information required to deliver a product or service.

**Steps to map current state**:
1. Walk the process from customer back to supplier
2. Record cycle time, changeover time, and WIP at each step
3. Separate value-added from non-value-added time
4. Identify bottlenecks (highest cycle time relative to takt time)
5. Mark inventory accumulation points
6. Calculate total lead time vs. value-added time ratio

**Key metrics per step**: Cycle time (C/T), work in progress (WIP), changeover time, uptime, batch size.

**Summary metrics**: Total lead time, total value-added time, percentage value-added. Value-added time is typically a small fraction of total lead time in service processes. The exact ratio varies, but it's often surprisingly low. The gap is the improvement opportunity.

### Text-Based Value Stream Map Example

```
ORDER-TO-CASH VALUE STREAM MAP (Current State)

Customer                                                          Customer
  Order                                                            Payment
    │                                                                 ▲
    ▼                                                                 │
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Order    │    │  Credit  │    │  Order   │    │ Shipping │    │ Invoice  │
│  Entry    │───▶│  Check   │───▶│ Fulfill  │───▶│          │───▶│ & Collect│
│           │    │          │    │          │    │          │    │          │
│ C/T: 15m  │    │ C/T: 2d  │    │ C/T: 3d  │    │ C/T: 2d  │    │ C/T: 5m  │
│ WIP: 50   │    │ WIP: 200 │    │ WIP: 150 │    │ WIP: 75  │    │ WIP: 300 │
│ FPY: 85%  │    │ FPY: 70% │    │ FPY: 92% │    │ FPY: 95% │    │ FPY: 80% │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
     │  ▲            │  ▲            │  ▲            │                │  ▲
     └──┘            └──┘            └──┘            │                └──┘
    Rework          Rework          Rework           │               Rework
    (15%)           (30%)           (8%)             │               (20%)
                                                     │
                                              Wait: 5d between
                                              fulfill & ship

TIMELINE:
├─ 15m ─┤─── 2d ───┤─── 3d ───┤── 5d wait ──┤── 2d ──┤── 5m ──┤
         ├── 8d wait ──┤

Total Lead Time:    45 days (including rework loops and queue time)
Value-Added Time:   7 days, 20 minutes
% Value-Added:      15.6%

BOTTLENECK:  Credit Check (longest queue, lowest FPY, highest rework)
QUICK WINS:  Automate credit check for existing customers (<$50K)
             Combine order entry + invoice generation
```

**Future state design**: Design for continuous flow where possible. Eliminate steps that don't add value. Pull work through the system rather than pushing it. The future state should show reduced lead time, lower WIP, and higher value-added percentage.

## Process Mining

Process mining uses event log data from IT systems to discover, monitor, and improve actual processes. It is most valuable for high-volume transactional processes where the gap between "how we think it works" and "how it actually works" is large.

### When to Use Process Mining

- Large-scale processes with many variants and exceptions
- ERP or workflow system logs available for extraction
- Need to discover actual process behavior vs. documented process
- Conformance checking against regulatory or policy requirements
- Identifying automation candidates from high-volume, low-variation paths

### Data Requirements

Process mining requires event logs with three minimum fields: **Case ID** (unique identifier for each process instance, e.g., order number), **Activity** (what happened, e.g., "Create Purchase Order"), and **Timestamp** (when it happened). Additional fields like resource, cost, and department enrich the analysis.

**Common ERP extraction sources:**
- SAP: TSTCT (transaction codes), CDHDR/CDPOS (change documents), BKPF/BSEG (accounting documents)
- Oracle: workflow tables, audit trail tables
- Salesforce: activity history, case history

### Process Mining Analysis

**Discovery metrics**: Number of process path variants discovered, average case duration, deviation points where the process diverges from the intended flow.

**Conformance analysis**: Compliance rate, number and percentage of deviating cases, root causes of deviation (are deviations intentional workarounds or genuine errors?).

**Process intelligence findings**: Identify bottlenecks (where cases spend the most time), rework loops (where cases go backwards), and excessive wait times (where cases sit idle).

### Process Mining Tool Selection

The tool landscape is maturing rapidly. Selection depends on your data sources, scale, and whether you need one-time analysis or continuous monitoring.

| Tool | Strength | Best For |
|------|----------|----------|
| Celonis | Deep SAP integration, enterprise-grade, real-time process intelligence | Large enterprises with SAP/Oracle; continuous process monitoring; organizations wanting execution management beyond just mining |
| UiPath Process Mining | Tight integration with UiPath RPA platform | Organizations already using UiPath for automation; projects where mining feeds directly into RPA bot development |
| Disco (Fluxicon) | Simple, fast, excellent visualization | One-time or periodic analysis; consulting engagements where speed matters; teams new to process mining |
| Microsoft Power Automate Process Mining | Integrated into Microsoft 365 ecosystem | Organizations heavily invested in Microsoft stack; lower-budget entry point |
| QPR ProcessAnalyzer | Strong conformance checking, compliance focus | Regulated industries; audit and compliance use cases |

**Practical guidance**: For consulting engagements, start with Disco for quick discovery (hours to first insight). Recommend Celonis or UiPath for clients who need ongoing operational monitoring. The tool matters less than the quality of your event log extraction and your ability to translate process maps into actionable findings.

## Industry Benchmarks

Reference benchmarks for common business processes. Use these to size the improvement opportunity and set realistic targets.

### Order-to-Cash (O2C)

| Metric | Bottom Quartile | Median | Top Quartile | World Class |
|--------|----------------|--------|--------------|-------------|
| Cycle time (order to payment) | >45 days | 25-35 days | 15-20 days | <10 days |
| DSO (Days Sales Outstanding) | >60 days | 40-50 days | 30-35 days | <25 days |
| Invoice accuracy | <85% | 90-95% | 97-99% | >99.5% |
| Cost per invoice | >$15 | $8-12 | $4-6 | <$3 |
| Touchless order rate | <20% | 40-55% | 65-80% | >85% |

### Procure-to-Pay (P2P)

| Metric | Bottom Quartile | Median | Top Quartile | World Class |
|--------|----------------|--------|--------------|-------------|
| PO cycle time | >5 days | 2-3 days | <1 day | Same day |
| Invoice processing time | >15 days | 7-10 days | 3-5 days | <2 days |
| % invoices matched automatically | <30% | 50-65% | 75-85% | >90% |
| Cost per PO | >$35 | $15-25 | $8-12 | <$5 |
| Maverick spend (off-contract) | >40% | 20-30% | 10-15% | <5% |

### Record-to-Report (R2R)

| Metric | Bottom Quartile | Median | Top Quartile | World Class |
|--------|----------------|--------|--------------|-------------|
| Days to close (monthly) | >10 days | 6-8 days | 4-5 days | <3 days |
| Days to close (quarterly) | >15 days | 10-12 days | 6-8 days | <5 days |
| Journal entry error rate | >5% | 2-3% | <1% | <0.5% |
| % automated reconciliations | <20% | 40-55% | 70-85% | >90% |
| Finance FTE per $B revenue | >50 | 35-45 | 25-30 | <20 |

These benchmarks are directional. Actual performance depends on industry, complexity, geography, and ERP maturity. Use them to frame the conversation ("we're in the bottom quartile on X"), not as absolute targets.

## SIPOC Analysis

SIPOC establishes process boundaries before detailed mapping. It answers: Who supplies what, through which high-level steps, producing what outputs, for whom?

| Element | Question |
|---------|----------|
| **S**uppliers | Who provides inputs to this process? |
| **I**nputs | What enters the process (materials, information, triggers)? |
| **P**rocess | What are the 5-7 high-level steps? |
| **O**utputs | What does the process produce? |
| **C**ustomers | Who receives the outputs? |

Use SIPOC in the Define phase to align the team on process scope. It prevents scope creep and ensures you're mapping the right process.

## Standard Work

Standard work documents the current best method for performing a process. It is the baseline for improvement, not the ceiling.

**Standard work elements**:
- Takt time: customer demand rate (available time / customer demand)
- Cycle time: time to complete one unit (must be less than or equal to takt time)
- WIP limit: maximum work in progress allowed
- Work sequence: steps in order with time and quality checks at each step

**Principles**:
- Takt time sets the pace. If cycle time exceeds takt time at any station, that station is a bottleneck
- WIP limits prevent overburden and expose bottlenecks. If you limit WIP and work piles up, you've found the constraint
- Document the current best method, then improve from there. You can only improve what is standardized

## Process Performance Dashboard

Track three categories of metrics to monitor process health.

**Efficiency metrics**: Cycle time, throughput, utilization. These tell you how fast and how productively the process operates.

**Quality metrics**: Defect rate, first pass yield (FPY), customer complaints. These tell you whether the process produces acceptable output.

**Cost metrics**: Cost per unit, scrap cost, rework cost. These translate process performance into financial impact.

Use RAG status (Green = on target, Yellow = at risk, Red = off target) and track baseline, current, and target values to show direction of travel.

## Financial Impact

Every process improvement should be translated into financial terms.

| Category | How to Calculate |
|----------|-----------------|
| Cost savings (annual) | Reduction in labor, materials, rework, waste |
| Revenue impact | Increased throughput, reduced lead time enabling more sales |
| One-time implementation cost | Training, systems, consulting, pilot costs |
| ROI | (Annual savings - Implementation cost) / Implementation cost |
| Payback period | Implementation cost / Monthly savings |

## Principles

- Start with data. Never assume. Measure current state before proposing improvements
- Value is defined by the customer, not by internal convenience
- Eliminate waste first, then optimize what remains
- Standardize before improving. You can only improve what is standardized
- Changes in one part of a process affect other parts. Think systemically
- Engage the people doing the work. They know the process best and they'll be implementing the changes
- Pilot before rollout. Test improvements before full implementation
- Control to sustain. Improvements without control mechanisms revert within months
- If you're not measuring, you're not improving. And if your measurements are wrong, you're improving the wrong thing
