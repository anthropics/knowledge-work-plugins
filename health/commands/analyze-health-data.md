---
name: analyze-health-data
description: Initiate a health data analysis workflow for epidemiological reports, outcomes research, or clinical quality metrics. Guides selection of appropriate statistical methods and generates an analysis plan.
trigger: !health
color: blue
---

# /analyze-health-data Command

Initiate health data analysis for epidemiological reports, clinical outcomes, or quality metrics.

## When to Use

Use this command when:
- Starting a new health data analysis project
- Analyzing epidemiological surveillance data
- Evaluating clinical outcomes or quality metrics
- Preparing data for research manuscripts
- Conducting population health assessments

## Workflow

### 1. Analysis Type Selection

Ask the user to specify the analysis type:

1. **Descriptive Epidemiology**
   - Population characteristics
   - Disease burden estimation
   - Temporal/spatial patterns

2. **Comparative Effectiveness**
   - Treatment comparisons
   - Intervention outcomes
   - Risk factor analysis

3. **Quality Metrics Analysis**
   - Clinical indicator trends
   - Benchmark comparisons
   - Outlier identification

4. **Survival Analysis**
   - Time-to-event outcomes
   - Kaplan-Meier curves
   - Cox regression

5. **Meta-Analysis**
   - Evidence synthesis
   - Forest plots
   - Heterogeneity assessment

### 2. Data Requirements Checklist

Gather information about available data:

| Requirement | Question | Critical |
|-------------|----------|----------|
| **Outcome Variable** | What is the primary outcome of interest? | Yes |
| **Exposure Variable** | What exposures/interventions are being analyzed? | Yes |
| **Confounders** | What variables need adjustment? | Yes |
| **Sample Size** | How many observations/records available? | Yes |
| **Time Period** | What is the study/analytic time window? | Yes |
| **Data Quality** | Are there known quality issues (missing data, outliers)? | Yes |
| **Jurisdiction** | Which regulatory framework applies? | Yes |

### 3. Analysis Plan Generation

Based on selections, generate an analysis plan including:

#### A. Study Design Confirmation
- Confirm appropriate study design
- Identify potential biases
- Define inclusion/exclusion criteria

#### B. Statistical Approach
- Recommended statistical tests/models
- Power/sample size considerations
- Handling of missing data

#### C. Visualization Plan
- Recommended plot types
- Forest plots for meta-analysis
- Survival curves for time-to-event
- SPC charts for quality metrics

#### D. Regulatory Considerations
- Required approvals (ethics, data governance)
- Data privacy safeguards
- Reporting obligations

## Example Session

**User:** `/analyze-health-data`

**System:**
```
Health Data Analysis - Initiation

What type of analysis are you conducting?
1. Descriptive Epidemiology
2. Comparative Effectiveness
3. Quality Metrics Analysis
4. Survival Analysis
5. Meta-Analysis

Select a number or describe your analysis:
```

**User:** "3 - analyzing 30-day readmission rates across our hospital units"

**System:**
```
Quality Metrics Analysis - 30-Day Readmission Rates

Data Requirements Checklist:

✓ Outcome: 30-day all-cause readmission (yes/no)
✓ Unit: Hospital department/unit
✓ Time period: Last 12 months
⚠ Sample size: How many index admissions?
✓ Confounders: Patient demographics, comorbidities, discharge destination

Recommended Approach:
- Statistical: Multi-level logistic regression (patients nested in units)
- Visualization: Control charts (p-charts) by unit over time
- Benchmarking: Compare to national rates (CMS for US, CQI for AU)

Next Steps:
1. Verify data extraction query
2. Apply health-data-report skill for detailed methodology
3. Generate analysis plan document

Proceed with detailed methodology guidance? [Y/n]
```

## Output

The command generates:
1. **Analysis Plan Summary** - Study design and statistical approach
2. **Data Requirements** - Checklist of required variables
3. **Methodology Guidance** - Routes to health-data-report skill
4. **Regulatory Notes** - Privacy and approval requirements

## Integration Points

- **Input**: Raw data files, database connections, or data dictionary
- **Process**: Uses `health-data-report` skill for detailed methodology
- **Output**: Analysis plan document, statistical code templates
- **Downstream**: Results feed into manuscript-prep, report templates

## Error Handling

| Issue | Response |
|-------|----------|
| Insufficient sample size | Flag for biostatistician consultation |
| Missing critical variables | Halt and request data clarification |
| Complex design | Suggest specialist biostatistician involvement |
| Sensitive data | Enforce PHI/PII guardrails and de-identification |

## MCP Connectors

```yaml
connectors:
  - research literature: ~~pubmed_database
  - clinical terminology: ~~snomed_loinc
  - statistical computing: ~~r_stats
```
