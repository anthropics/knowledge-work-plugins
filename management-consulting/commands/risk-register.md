---
description: Create and manage project risk registers with probability-impact analysis. Use when identifying, assessing, prioritizing, and developing mitigation strategies for project or business risks.
argument-hint: "<project or context for risk assessment>"
---

# /risk-register -- Risk Identification and Management

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Create comprehensive risk registers using probability-impact matrices and industry-standard risk management methodologies. Supports project risk identification, assessment, and mitigation planning.

## Invocation

```
/risk-register [project or context for risk assessment]
```

If no context is provided, ask the user to describe the project or business context for risk identification.

## Workflow

### Step 1: Identify Risks

Systematically identify potential risks using **ISO 31000 and COSO ERM frameworks**:

```
## Risk Identification

### Risk Categories
| Category | Description | Example Risks |
|----------|-------------|---------------|
| Strategic | External factors affecting strategy | Market changes, competitor actions, AI disruption |
| Financial | Budget, cost, revenue risks | Cost overruns, currency fluctuation, inflation |
| Operational | Process, system, people risks | System failures, key person dependency, supply chain |
| Technical | Technology and technical risks | Technology obsolescence, integration issues, cybersecurity |
| Regulatory | Compliance and legal risks | Regulatory changes, compliance failures, data privacy |
| Reputational | Brand and perception risks | Negative publicity, service failures, ESG failures |
| Schedule | Timeline and delivery risks | Delays, dependencies |
| Quality | Output and deliverable risks | Defects, scope creep |
| **Digital/ML Risks** | Digital-specific risks | Model bias, algorithmic accountability, automation risks |
| **Climate/ESG** | Sustainability risks | Physical climate risks, transition risks, greenwashing |

### Emerging Risk Areas
| Risk Type | Description | Relevance |
|-----------|-------------|-----------|
| AI Governance | Algorithmic decision-making accountability | High |
| Digital Trust | Cybersecurity, data privacy, deepfakes | High |
| Supply Chain Resilience | Geopolitical, climate-related disruptions | High |
| Workforce Transformation | Skills gaps, automation impact | Medium-High |
| Regulatory Change | AI regulation, ESG disclosure requirements | High |

### Risk Identification Techniques
| Technique | Description | Best For |
|-----------|-------------|----------|
| Brainstorming | Open discussion with team | Early identification |
| Delphi Method | Anonymous expert input | Complex/technical risks |
| SWOT Analysis | Internal strengths/weaknesses, external threats/opportunities | Strategic risks |
| Checklists | Based on historical risks | Repeatable projects |
| Expert Judgment | Leverage experienced team members | Specialized domains |
| Root Cause Analysis | Work backwards from potential problems | Process risks |
| **Horizon Scanning** | Systematic future risk identification | Strategic risks |
| **Scenario Analysis** | Explore future risk scenarios | Long-term planning |

### Initial Risk List
| Risk ID | Category | Risk Description | Trigger | Early Indicator |
|---------|----------|-------------------|---------|-----------------|
| R001 | [Cat] | [Description] | [What causes it] | [Early warning sign] |
| R002 | [Cat] | [Description] | [What causes it] | [Early warning sign] |
| R003 | [Digital/ML] | [Digital model performance degradation] | [Data drift, concept drift] | [Monitoring metrics] |
```

### Step 2: Assess and Score Risks

Evaluate each risk's probability and impact:

```
## Risk Assessment

### Probability Scale
| Level | Score | Description | Frequency |
|-------|-------|-------------|-----------|
| Very High | 5 | Almost certain to occur | >80% likelihood |
| High | 4 | Likely to occur | 60-80% likelihood |
| Medium | 3 | Might occur | 40-60% likelihood |
| Low | 2 | Unlikely to occur | 20-40% likelihood |
| Very Low | 1 | Rare | <20% likelihood |

### Impact Scale
| Level | Score | Schedule | Cost | Quality | Reputation |
|-------|-------|----------|------|---------|------------|
| Very High | 5 | >30% delay | >20% over | Major defects | Severe damage |
| High | 4 | 15-30% delay | 10-20% over | Significant defects | Major damage |
| Medium | 3 | 5-15% delay | 5-10% over | Moderate defects | Moderate damage |
| Low | 2 | <5% delay | <5% over | Minor defects | Limited damage |
| Very Low | 1 | Minimal | Minimal | Cosmetic | Minor issue |

### Risk Score Calculation
```
Risk Score = Probability × Impact

Score Range:
- 19-25: CRITICAL (Red) - Immediate action required
- 10-18: HIGH (Orange) - Priority mitigation needed
- 5-9: MEDIUM (Yellow) - Active monitoring
- 1-4: LOW (Green) - Accept with monitoring
```

### Probability-Impact Matrix
```
                    IMPACT
              1     2     3     4     5
           ┌─────┬─────┬─────┬─────┬─────┐
        5  │  5  │ 10  │ 15  │ 20  │ 25  │
P       4  │  4  │  8  │ 12  │ 16  │ 20  │
R       3  │  3  │  6  │  9  │ 12  │ 15  │
O       2  │  2  │  4  │  6  │  8  │ 10  │
B       1  │  1  │  2  │  3  │  4  │  5  │
           └─────┴─────┴─────┴─────┴─────┘
              │     │     │     │     │
            LOW  LOW  MED   HIGH  CRIT
           (1-4)(1-4)(5-9)(10-18)(19-25)
```

### Assessed Risks
| ID | Risk | Probability | Impact | Score | Status |
|----|------|-------------|--------|-------|--------|
| R001 | [Description] | [1-5] | [1-5] | [Score] | [Open] |
| R002 | [Description] | [1-5] | [1-5] | [Score] | [Open] |
```

### Step 3: Develop Mitigation Strategies

Create responses for each risk:

```
## Risk Mitigation

### Mitigation Strategy Options
| Strategy | Description | When to Use |
|----------|-------------|--------------|
| Avoid | Change approach to eliminate risk | High impact, high probability |
| Mitigate | Reduce probability or impact | Most common approach |
| Transfer | Shift risk to another party | Insurance, outsourcing |
| Accept | Acknowledge and monitor | Low impact, cost > benefit |
| Exploit | Increase probability of opportunity | For opportunities |

### Risk Response Plan
| ID | Risk | Strategy | Response Actions | Owner | Due Date |
|----|------|----------|------------------|-------|----------|
| R001 | [Risk] | [Avoid/Mitigate/Transfer/Accept] | [Specific actions] | [Name] | [Date] |
| R002 | [Risk] | [Avoid/Mitigate/Transfer/Accept] | [Specific actions] | [Name] | [Date] |

### Detailed Mitigation Plans

#### Risk R001: [Risk Title]
**Strategy**: [Strategy chosen]

**Mitigation Actions**:
| Action | Description | Owner | Timeline | Status |
|--------|-------------|-------|----------|--------|
| 1 | [Action] | [Name] | [Date] | [Complete/In Progress] |
| 2 | [Action] | [Name] | [Date] | [Complete/In Progress] |

**Contingency Plan** (if risk occurs):
- [Specific response if risk materializes]
- [Fallback approach]

**Cost of Mitigation**: $[Amount]
**Cost of Risk Occurrence**: $[Amount]
**Cost-Effective?**: [Yes/No]
```

### Step 4: Monitor and Review

Establish ongoing risk management:

```
## Risk Monitoring

### Risk Register Review Cadence
| Review Type | Frequency | Participants | Focus |
|-------------|-----------|--------------|-------|
| Status Check | Weekly | Project Manager | Trigger monitoring |
| Full Review | Monthly | Project Team | New risks, status changes |
| Deep Dive | Quarterly | Steering Committee | Trends, strategic risks |

### Early Warning Indicators
| Risk ID | Early Warning Signal | Monitoring Method | Frequency |
|---------|---------------------|-------------------|-----------|
| R001 | [Signal] | [Method] | [Weekly] |
| R002 | [Signal] | [Method] | [Monthly] |

### Risk Trends
| Metric | Current | Previous | Trend |
|--------|---------|----------|-------|
| Total Risks | [n] | [n] | [↑/→/↓] |
| High/Critical Risks | [n] | [n] | [↑/→/↓] |
| Closed Risks | [n] | [n] | [↑/→/↓] |
| Risks per Category | [n] | [n] | [↑/→/↓] |

### Risk Trigger Log
| Date | Risk ID | Trigger Event | Response Taken | Outcome |
|------|---------|---------------|----------------|----------|
| [Date] | R001 | [What happened] | [Response] | [Result] |
```

## Output Format

```
# Risk Register: [Project/Program Name]

## Executive Summary
- Total Risks Identified: [n]
- Critical/High Risks: [n]
- Risks Closed This Period: [n]
- Overall Risk Profile: [Improving/Stable/Deteriorating]

## Risk Register

### Critical Risks (Score 19-25)
| ID | Risk | Probability | Impact | Score | Mitigation | Owner | Status |
|----|------|-------------|--------|-------|------------|-------|--------|
| R001 | [Description] | [1-5] | [1-5] | [Score] | [Strategy] | [Name] | [Open] |

### High Risks (Score 10-18)
| ID | Risk | Probability | Impact | Score | Mitigation | Owner | Status |
|----|------|-------------|--------|-------|------------|-------|--------|
| R002 | [Description] | [1-5] | [1-5] | [Score] | [Strategy] | [Name] | [Open] |

### Medium Risks (Score 5-9)
| ID | Risk | Probability | Impact | Score | Mitigation | Owner | Status |
|----|------|-------------|--------|-------|------------|-------|--------|
| R003 | [Description] | [1-5] | [1-5] | [Score] | [Strategy] | [Name] | [Open] |

### Low Risks (Score 1-4)
| ID | Risk | Probability | Impact | Score | Mitigation | Owner | Status |
|----|------|-------------|--------|-------|------------|-------|--------|
| R004 | [Description] | [1-5] | [1-5] | [Score] | [Strategy] | [Name] | [Open] |

## Risk by Category
| Category | Count | Critical | High | Medium | Low |
|----------|-------|----------|------|--------|-----|
| Strategic | [n] | [n] | [n] | [n] | [n] |
| Financial | [n] | [n] | [n] | [n] | [n] |
| Operational | [n] | [n] | [n] | [n] | [n] |
| Technical | [n] | [n] | [n] | [n] | [n] |
| Regulatory | [n] | [n] | [n] | [n] | [n] |

## Mitigation Cost Summary
| Total Mitigation Budget | Spent | Remaining |
|-------------------------|-------|------------|
| $[Amount] | $[Amount] | $[Amount] |

## Trigger Log
[Record of when risks materialized and responses]

## Review Schedule
- Next Review: [Date]
- Owner: [Name]
- Frequency: [Weekly/Monthly/Quarterly]

---
Register Last Updated: [Date]
Next Review: [Date]
```

## Notes

- Review and update the risk register regularly
- Involve the team in risk identification - diverse perspectives find more risks
- Don't just identify risks - develop actionable responses
- Consider both threats and opportunities
- Document lessons learned for future projects
- Communicate risks clearly to stakeholders
- Prioritize mitigation efforts based on risk scores
- Monitor early warning indicators proactively
- Review risks at each project stage gate
- Consider residual risks after mitigation
- Accept only calculated, documented risks
- Never assume a risk has disappeared without verification
