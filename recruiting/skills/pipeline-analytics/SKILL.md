---
name: pipeline-analytics
description: "Analyze recruiting funnel metrics, conversion rates, time-to-fill, and pipeline velocity. Identifies bottlenecks and models scenarios to hit hiring targets. Trigger with \"pipeline metrics\", \"conversion rates\", \"time to fill\", \"funnel analysis\", \"how's the pipeline\", \"hiring velocity\", or when the user shares recruiting data, asks about hiring progress, or discusses pipeline health."
---

# Pipeline Analytics

Recruiting funnel analysis and optimization. Turns raw pipeline data into actionable insights about where candidates are getting stuck, what's working, and what needs to change.

## How It Works

- **Standalone**: Paste pipeline data (counts by stage, time-in-stage, or just describe the situation) and get a full funnel analysis with benchmarks and recommendations.
- **With connectors**: Pull live ATS data for real-time pipeline snapshots, historical trend analysis, and automated bottleneck detection.

## Core Metrics Framework

### Funnel Metrics

| Metric | Formula | Benchmark (varies by role) | What it tells you |
|--------|---------|---------------------------|-------------------|
| **Application-to-screen rate** | Screens / Applications | 15-30% | Sourcing quality and JD effectiveness |
| **Screen-to-interview rate** | Interviews / Screens | 30-50% | Recruiter calibration with hiring manager |
| **Interview-to-offer rate** | Offers / Interviews | 20-40% | Interview process effectiveness and bar clarity |
| **Offer acceptance rate** | Accepts / Offers | 70-90% | Comp competitiveness and candidate experience |
| **Overall yield** | Hires / Applications | 1-5% | End-to-end process efficiency |

### Velocity Metrics

| Metric | Benchmark | Red flag |
|--------|-----------|----------|
| **Time to fill** (req open → start date) | 30-60 days (varies) | > 90 days |
| **Time in stage** (per pipeline stage) | 3-7 days | > 14 days |
| **Scheduling latency** (interview requested → scheduled) | 2-3 days | > 7 days |
| **Feedback turnaround** (interview → scorecard) | 24-48 hours | > 5 days |
| **Offer turnaround** (debrief → offer extended) | 2-5 days | > 10 days |

### Quality Metrics

| Metric | What it measures |
|--------|-----------------|
| **New hire retention** (90-day, 1-year) | Were we hiring the right people? |
| **Hiring manager satisfaction** | Did we deliver what they needed? |
| **Candidate NPS** | How was the candidate experience? |
| **Source quality** (by channel) | Which sourcing channels produce hires? |
| **Interviewer calibration** | Do interviewer scores predict performance? |

## Bottleneck Diagnosis

When a stage shows poor conversion or high time-in-stage, diagnose by category:

| Symptom | Likely causes | Recommended actions |
|---------|--------------|-------------------|
| Low screen-to-interview | Calibration gap between recruiter and HM | Joint calibration session, review recent passes and rejects |
| High time-in-stage at scheduling | Interviewer availability | Add interviewers, reduce panel size, use scheduling tools |
| Low offer acceptance | Below-market comp or slow process | Comp benchmarking, speed up offer turnaround |
| High drop-off at onsite | Poor candidate experience or bar mismatch | Candidate experience audit, interviewer training |
| Low application volume | JD issues, employer brand, or wrong channels | JD rewrite, source channel analysis |

## Pipeline Math

Model the pipeline needed to hit a hiring goal:

```
Working backward from 1 hire:
  Offers needed:      1 / acceptance rate     = [X]
  Final interviews:   offers / interview-offer = [X]
  Phone screens:      finals / screen-final    = [X]
  Applications:       screens / app-screen     = [X]

At current inflow of [Y] candidates/week:
  Weeks to fill:      applications needed / Y  = [X weeks]
```

## Output Format

When analyzing a pipeline, produce:

1. **Funnel snapshot** — current candidates by stage with conversion rates
2. **Benchmark comparison** — how each stage compares to industry benchmarks
3. **Bottleneck identification** — specific stages causing problems, with root cause hypotheses
4. **Pipeline math** — what's needed to hit the hiring goal on time
5. **Prioritized recommendations** — 3-5 actions ranked by expected impact

## Connectors

| Connector | Enhancement |
|-----------|------------|
| ATS | Live pipeline data, historical trends, per-role analytics |
| Calendar | Scheduling bottleneck detection, interviewer capacity analysis |
| HRIS | Headcount targets, approved roles, time-to-fill goals |
