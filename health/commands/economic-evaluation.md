---
name: /economic-evaluation
description: Initiate a health economic evaluation including cost-effectiveness, cost-utility, or cost-benefit analysis with jurisdiction-specific reference case requirements.
tools: ['Read', 'Write', 'skill']
---

# Economic Evaluation Command

Conduct a systematic health economic evaluation following jurisdiction-specific reference case requirements.

## Invocation

```
/economic-evaluation
```

## User Prompts

This command will guide you through:
1. **Evaluation Type Selection** - Choose CEA, CUA, CBA, or BIA
2. **Jurisdiction Selection** - AU/NZ (default), UK (NICE), Canada (CADTH), or US
3. **Intervention Details** - Describe the health intervention being evaluated
4. **Comparator Identification** - Current standard of care in jurisdiction
5. **Target Population** - Who will receive the intervention?
6. **Time Horizon** - Duration of analysis (lifetime, 5 years, etc.)
7. **Perspective** - Healthcare sector, societal, or payer
8. **Outcome Measures** - Natural units, QALYs, DALYs, or monetary

## Workflow

### Step 1: Evaluation Type Selection

The command will determine the appropriate evaluation type:

| Type | When to Use | Primary Outcome |
|------|-------------|-----------------|
| **CEA** | Comparing interventions with same outcome in natural units | Cost per unit gained (e.g., cost per mmHg reduction) |
| **CUA** | Cross-condition comparisons; preferred by most HTA bodies | Cost per QALY gained |
| **CBA** | Healthcare vs. non-health investments; public health policy | Net monetary benefit |
| **BIA** | Affordability analysis alongside CEA/CUA | Annual budget impact |

### Step 2: Jurisdiction Configuration

Select jurisdiction to apply appropriate reference case:

**Australia (PBAC)**:
- Dual perspective: Healthcare sector + Societal
- 5% discounting (costs and QALYs)
- QALYs preferred (AQoL or EQ-5D Australian tariffs)
- Time horizon: Sufficient to capture all differences
- PSA required

**Australia (MSAC)**:
- Healthcare perspective
- Similar to PBAC but for medical services
- MBS fees for costing

**New Zealand (PHARMAC)**:
- Healthcare perspective
- Nine decision criteria (not just cost-effectiveness)
- Equity considerations paramount
- 5% discounting

**UK (NICE)**:
- NHS and Personal Social Services perspective
- 3.5% discounting (1.5% if >30 years)
- EQ-5D-3L UK tariff for utilities
- £20,000-30,000/QALY threshold

**Canada (CADTH)**:
- Publicly funded healthcare system perspective
- 5% discounting
- Canadian preference-based utilities preferred
- CUA preferred outcome

### Step 3: Generate Evaluation Plan

Based on inputs, the command will generate:

1. **Evaluation Protocol**:
   - Research question and decision problem
   - Intervention and comparator specifications
   - Target population and subgroups
   - Perspective and time horizon
   - Discounting approach
   - Outcome measures

2. **Evidence Requirements**:
   - Clinical evidence needs (RCTs, observational data)
   - Cost data sources (PBS/MSAC schedules, DRG costs)
   - Utility data requirements (instrument selection)
   - Comparator evidence requirements

3. **Modeling Approach**:
   - Recommended model structure (decision tree, Markov, microsimulation)
   - Justification for approach
   - State definitions (if Markov)
   - Cycle length recommendation
   - Half-cycle correction requirements

4. **Analysis Plan**:
   - Base case analysis specifications
   - Sensitivity analysis requirements (deterministic and probabilistic)
   - Subgroup analyses (if applicable)
   - Budget impact analysis parameters
   - Scenario analyses

5. **Deliverables Checklist**:
   - Economic evaluation report structure
   - Model files required
   - Documentation requirements
   - Validation approach
   - HTA submission requirements (if applicable)

### Step 4: Operating Mode Selection

**Standard Mode**:
- Full evaluation with complete decision modeling
- Comprehensive PSA with 5,000-10,000 iterations
- Detailed costing methodology
- Extensive scenario analyses
- Formal reporting for potential HTA submission

**Lite Mode**:
- Streamlined evaluation for preliminary assessment
- Simple decision tree or basic Markov model
- Deterministic sensitivity analysis only
- Rapid turnaround for internal decision-making
- Clearly marked as preliminary

## Output

The command produces:

1. **Evaluation Summary**:
   - Evaluation type and jurisdiction
   - Key parameters and assumptions
   - Preliminary ICER estimate (if data available)
   - Critical uncertainties identified

2. **Work Plan**:
   - Step-by-step evaluation workflow
   - Data collection requirements
   - Analysis milestones
   - Timeline estimate

3. **Resource Requirements**:
   - Skill requirements (`~~health/health-econ-eval`)
   - Estimated time commitment
   - Specialist involvement needed (health economist, statistician)
   - Software requirements

4. **Next Steps**:
   - Immediate actions required
   - Evidence gaps to address
   - Stakeholder engagement needs
   - Review and validation checkpoints

## Example Usage

```
User: /economic-evaluation

Assistant: I'll help you conduct a health economic evaluation. Let me gather some information:

1. What type of evaluation do you need?
   - Cost-Effectiveness Analysis (CEA)
   - Cost-Utility Analysis (CUA) ← Recommended for most HTA submissions
   - Cost-Benefit Analysis (CBA)
   - Budget Impact Analysis (BIA)

2. Which jurisdiction will this support?
   - Australia (PBAC - Pharmaceutical Benefits)
   - Australia (MSAC - Medical Services)
   - New Zealand (PHARMAC)
   - UK (NICE)
   - Canada (CADTH)
   - Other/General methods

[Continue with guided intake...]
```

## Success Criteria

Evaluation plan is complete when:
- [ ] Evaluation type appropriate for decision context
- [ ] Jurisdiction reference case requirements identified
- [ ] Comparator represents standard of care
- [ ] Time horizon justified for condition
- [ ] Perspective aligns with reference case
- [ ] Outcome measures specified
- [ ] Model structure recommended with rationale
- [ ] Analysis plan includes PSA
- [ ] Deliverables checklist provided
- [ ] Resource requirements identified
- [ ] Operating mode selected (Standard/Lite)

## Related Skills

- `~~health/health-econ-eval` - Economic evaluation methodology and modeling
- `~~health/hta-submission` - HTA submission preparation
- `~~health/evidence-synthesis` - Systematic review for clinical evidence
- `~~data/statistical-analysis` - Statistical methods for PSA and evidence synthesis
