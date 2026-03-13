---
name: health/health-data-report
description: This skill should be used when analyzing health data, generating epidemiological reports, creating statistical summaries, or producing population health visualizations. Use when users mention health statistics, epidemiological analysis, cohort studies, survival analysis, forest plots, Kaplan-Meier curves, population health metrics, or health data dashboards.
version: 1.0.0
---

# Health Data Analysis and Reporting

Comprehensive guidance for epidemiological data analysis, statistical reporting, and population health visualization. Supports descriptive and analytical epidemiology, survival analysis, and evidence-based health reporting.

**Important**: This skill assists with health data analysis workflows but does not replace biostatistical expertise, epidemiological consultation, or institutional review board oversight. All analyses involving human subjects data require appropriate ethical approvals.

## When to Use This Skill

Invoke when:
- A user needs to analyze health or epidemiological data (cohort, cross-sectional, case-control).
- Population health metrics need calculation and interpretation (incidence, prevalence, SMR).
- Statistical reports for clinical governance, quality improvement, or research are required.
- Survival analysis outputs (Kaplan-Meier curves, hazard ratios) need generation.
- Meta-analysis visualizations (forest plots, funnel plots) are requested.
- Health data visualization for dashboards or publications is needed.
- Epidemiological study design guidance is required before analysis.
- Risk adjustment or comparative outcome reporting is requested.
- Users need guidance on appropriate statistical tests for health data.

Do not use this skill for:
- Individual patient diagnosis or treatment decisions (use clinical decision support tools).
- Real-time clinical monitoring or alert systems.
- Pharmaceutical trial regulatory submissions without biostatistical oversight.
- Analyses requiring protected health information (PHI) without proper de-identification protocols.

## Operating Modes

### Standard Mode
Use full epidemiological analysis workflow:
- Complete study design review and data quality assessment.
- Formal statistical analysis plan with power calculations where applicable.
- Full regulatory and ethical compliance verification (AU/NZ default).
- Comprehensive visualization package with publication-ready figures.
- Detailed interpretation with confidence intervals and uncertainty quantification.
- Hybrid evidence management with strict citations and narrative referencing.

### Lite Mode
Use for constrained contexts (exploratory analysis, limited data, or rapid insights):
- Basic descriptive statistics and summary measures only.
- Preliminary visualizations without formal statistical testing.
- High-level population health metrics with clear uncertainty flags.
- Flag limitations and recommend full analysis when conclusions are needed.
- Lite mode is not acceptable for regulatory submissions, peer-reviewed publications, or clinical decision-making.

Lite mode must never suppress high-risk findings or statistical significance warnings.

## Regulatory Context

Default jurisdiction is Australia/New Zealand. Use US/EU-lite framing only when explicitly requested.

| Jurisdiction | Regulator/Statute | Trigger | Timeframe/SLA | Required Artifacts | Escalation Point |
|---|---|---|---|---|---|
| Australia | Privacy Act 1988 (Cth), NHMRC National Statement on Ethical Conduct in Human Research, state health privacy principles | Research involving human data, identifiable health records, population health reporting | Ethics approval required before analysis; privacy impact assessments for identifiable data | Ethics approval certificate, data governance agreement, statistical analysis plan, de-identification protocol | Human Research Ethics Committee (HREC), Privacy Officer, Chief Medical Officer |
| New Zealand | Privacy Act 2020, Health Information Privacy Code 2020, HDC Code of Health and Disability Services Consumers' Rights, Te Whatu Ora governance | Research with health data, identifiable information, population health surveillance | Ethics approval via HDEC (Health and Disability Ethics Committee); privacy assessments for identifiable data | Ethics approval, data access agreement, statistical analysis plan, privacy impact assessment | HDEC, Privacy Officer, Clinical Governance |
| United States (lite) | HIPAA Privacy Rule, Common Rule (45 CFR 46), FDA regulations for clinical trials | Human subjects research, identifiable health data, clinical trial analyses | IRB approval required; data use agreements for PHI | IRB approval, DUA, statistical analysis plan | IRB, Privacy Officer, Compliance |
| European Union (lite) | GDPR (health data special category), Clinical Trials Regulation (EU) No 536/2014, national health research laws | Health data processing, clinical trials, epidemiological studies | Ethics committee approval; DPIA for high-risk processing; GDPR lawful basis documented | Ethics approval, DPIA, statistical analysis plan, data processing agreements | Ethics Committee, DPO, Clinical Governance |

## Quick Reference

1. **Define study question** - Specify hypothesis, outcomes, and target population.
2. **Assess data quality** - Completeness, validity, and bias assessment.
3. **Select analysis type** - Descriptive, analytical, survival, or meta-analysis.
4. **Choose appropriate metrics** - Incidence, prevalence, rates, ratios as appropriate.
5. **Apply risk adjustment** - Account for confounders and case-mix differences.
6. **Calculate confidence intervals** - Always report uncertainty with point estimates.
7. **Create visualizations** - Forest plots, survival curves, or population dashboards.
8. **Interpret cautiously** - Distinguish association from causation; note limitations.
9. **Document methods** - Reproducible analysis with version control and code.
10. **Report ethically** - De-identified outputs; appropriate data governance.

## Detailed Guidance

### Step-by-Step Analysis Workflow

#### Step 1: Study Design and Question Specification
- Define primary research question using PICO/PECO framework (Population, Exposure/Intervention, Comparator, Outcome).
- Specify study type: descriptive (cross-sectional), analytical (cohort, case-control), or experimental.
- Identify target population and sampling strategy.
- Define inclusion/exclusion criteria explicitly.
- Document potential biases (selection, information, confounding).

#### Step 2: Data Quality Assessment
- Evaluate completeness: missing data patterns and proportions.
- Assess validity: range checks, logical consistency, outlier detection.
- Check accuracy: comparison with gold standard or duplicate verification.
- Document data provenance: source systems, extraction date, transformation history.
- Flag data quality issues before analysis begins.

#### Step 3: Statistical Analysis Plan
- Pre-specify primary and secondary analyses before data inspection.
- Define statistical significance threshold (typically alpha = 0.05).
- Specify adjustment for multiple comparisons (Bonferroni, FDR).
- Plan for missing data handling (complete case, imputation, sensitivity analysis).
- Document subgroup analyses and interaction tests.
- Calculate required sample size/power for primary hypothesis.

#### Step 4: Descriptive Analysis
- Report baseline characteristics: demographics, comorbidities, exposure distribution.
- Use appropriate summary statistics: mean (SD) or median (IQR) for continuous; counts (%) for categorical.
- Calculate stratified summaries by key variables (e.g., exposure groups).
- Visualize distributions: histograms, box plots, bar charts.
- Report data completeness for each variable.

#### Step 5: Analytical Epidemiology
- **Cohort Studies**: Calculate incidence rates, rate ratios, risk ratios, risk differences. Use survival analysis for time-to-event outcomes.
- **Case-Control Studies**: Calculate odds ratios with confidence intervals. Assess for selection bias and recall bias.
- **Cross-Sectional Studies**: Calculate prevalence, prevalence ratios. Note inability to establish temporality.
- **Risk Adjustment**: Use multivariable regression (logistic, Poisson, Cox) to control for confounders.
- **Sensitivity Analyses**: Test robustness to assumptions and missing data methods.

#### Step 6: Survival Analysis (when applicable)
- Calculate Kaplan-Meier estimates with log-rank tests for group comparisons.
- Fit Cox proportional hazards models for adjusted hazard ratios.
- Check proportional hazards assumption (Schoenfeld residuals, time-dependent covariates).
- Handle competing risks (Fine-Gray subdistribution hazards) when appropriate.
- Report median survival times with confidence intervals.
- Create Kaplan-Meier plots with number-at-risk tables.

#### Step 7: Meta-Analysis (when applicable)
- Assess heterogeneity (I² statistic, Cochran's Q).
- Choose fixed-effect or random-effects model based on heterogeneity.
- Calculate pooled effect estimates with confidence intervals.
- Assess publication bias (funnel plots, Egger's test).
- Conduct sensitivity analyses (leave-one-out, subgroup analyses).
- Create forest plots showing individual and pooled estimates.

#### Step 8: Interpretation and Reporting
- Distinguish statistical significance from clinical importance.
- Report confidence intervals to show precision of estimates.
- Discuss generalizability to target population.
- Acknowledge limitations: residual confounding, selection bias, measurement error.
- Provide actionable conclusions with appropriate caveats.

## Analysis Types and Selection Guidance

| Analysis Type | When to Use | Key Metrics | Visualizations |
|---|---|---|---|
| **Descriptive Epidemiology** | Characterizing population health; generating hypotheses | Prevalence, incidence, rates, proportions | Bar charts, pie charts, population pyramids, maps |
| **Cohort Study Analysis** | Following exposed vs. unexposed over time | Incidence rate, rate ratio, risk ratio, risk difference, NNT | Survival curves, incidence plots, cumulative incidence |
| **Case-Control Analysis** | Rare diseases or outcomes with long latency | Odds ratio, exposure odds, matched OR | Forest plots, exposure distribution charts |
| **Cross-Sectional Analysis** | Snapshot of health status; prevalence studies | Prevalence, prevalence ratio, prevalence odds ratio | Bar charts, prevalence maps, age-standardized rates |
| **Survival Analysis** | Time-to-event outcomes; censored data | Hazard ratio, median survival, survival probability | Kaplan-Meier curves, Nelson-Aalen plots, hazard plots |
| **Trend Analysis** | Temporal patterns; surveillance data | Annual percent change, joinpoint regression | Time series plots, trend lines, heatmaps by time |
| **Comparative Effectiveness** | Comparing interventions or exposures | Relative risk reduction, absolute risk reduction, NNT | Forest plots, waterfall plots, volcano plots |
| **Risk Prediction** | Predicting individual outcomes | C-statistic, calibration slope, Brier score | ROC curves, calibration plots, risk score distributions |
| **Meta-Analysis** | Synthesizing multiple studies | Pooled effect size, I², prediction intervals | Forest plots, funnel plots, L'Abbe plots |
| **Geospatial Analysis** | Geographic variation in health | SMR, local Moran's I, spatial scan statistics | Choropleth maps, disease cluster maps, spatial smoothed rates |

## Epidemiological Methods Overview

### Measures of Disease Frequency

| Measure | Formula | Interpretation | When to Use |
|---|---|---|---|
| **Prevalence** | Cases / Total population | Proportion with disease at a point or period | Burden of disease; resource planning |
| **Incidence Rate** | New cases / Person-time at risk | Rate of new cases per unit time | Dynamic populations; varying follow-up |
| **Cumulative Incidence** | New cases / Initial population at risk | Risk of developing disease over time | Fixed cohorts with complete follow-up |
| **Attack Rate** | Cases / Exposed population | Cumulative incidence during outbreak | Outbreak investigations |
| **Secondary Attack Rate** | Cases among contacts / Total contacts | Transmissibility of infectious disease | Contact tracing; infectious disease control |

### Measures of Association

| Measure | Formula | Interpretation | Study Type |
|---|---|---|---|
| **Risk Ratio (RR)** | Risk exposed / Risk unexposed | Relative increase/decrease in risk | Cohort studies; RCTs |
| **Odds Ratio (OR)** | (a×d)/(b×c) | Approximates RR when disease rare | Case-control studies |
| **Rate Ratio** | Rate exposed / Rate unexposed | Relative difference in incidence rates | Cohort studies with person-time |
| **Risk Difference (RD)** | Risk exposed - Risk unexposed | Absolute difference in risk | Public health impact; NNT calculation |
| **Hazard Ratio (HR)** | h₁(t)/h₀(t) | Relative instantaneous risk | Survival analysis; Cox models |
| **Number Needed to Treat (NNT)** | 1 / Absolute risk reduction | Patients to treat to prevent one outcome | Clinical trials; intervention studies |
| **Population Attributable Fraction** | (Pₑ×(RR-1))/(Pₑ×(RR-1)+1) | Proportion of disease due to exposure | Public health policy; prevention priorities |

### Risk Adjustment Methods

| Method | Description | When to Use |
|---|---|---|
| **Direct Standardization** | Apply stratum-specific rates to standard population | Comparing rates across populations with different age structures |
| **Indirect Standardization** | Apply standard rates to study population; calculate SMR | Small strata; limited data; comparing to standard population |
| **Regression Adjustment** | Include covariates in multivariable model | Controlling for multiple confounders simultaneously |
| **Propensity Scores** | Match or weight on probability of exposure | Observational studies with many confounders |
| **Instrumental Variables** | Use external variation to isolate causal effect | Unmeasured confounding suspected |
| **Stratification/Matching** | Analyze within homogeneous subgroups | Simple confounder control; ensuring balance |

## Standard Health Metrics

### Population Health Indicators

| Metric | Definition | Benchmark/Interpretation |
|---|---|---|
| **Age-Standardized Rate** | Rate adjusted to standard population structure | Enables fair comparison across populations |
| **Standardized Mortality Ratio (SMR)** | Observed deaths / Expected deaths | SMR > 1 indicates excess mortality; < 1 indicates protective effect |
| **Years of Life Lost (YLL)** | Sum of (standard life expectancy - age at death) | Burden of premature mortality |
| **Disability-Adjusted Life Years (DALY)** | YLL + Years Lived with Disability (YLD) | Comprehensive burden of disease measure |
| **Quality-Adjusted Life Years (QALY)** | Life years weighted by quality of life | Health economic evaluation; cost-utility analysis |
| **Life Expectancy** | Average years of life remaining at given age | Population health status indicator |
| **Healthy Life Expectancy (HALE)** | Years lived in full health | Quality-adjusted longevity |
| **Infant Mortality Rate** | Deaths < 1 year / Live births | Sensitive indicator of population health |
| **Maternal Mortality Ratio** | Maternal deaths / 100,000 live births | Healthcare system performance |

### Healthcare Quality Metrics

| Metric | Definition | Use Case |
|---|---|---|
| **Readmission Rate** | Readmissions / Index admissions | Care transition quality; post-discharge outcomes |
| **Mortality Rate** | Deaths / Admissions or procedures | Outcome quality; safety indicator |
| **Length of Stay (LOS)** | Mean/median days from admission to discharge | Efficiency; resource utilization |
| **Complication Rate** | Complications / Procedures or admissions | Safety; process quality |
| **Infection Rate** | HAI cases / Patient days or device days | Infection control effectiveness |
| **Medication Error Rate** | Errors / Medication orders or doses | Medication safety |
| **Patient Satisfaction Score** | Mean or proportion satisfied | Patient experience; service quality |
| **Mortality/Hospital Volume Relationship** | Outcomes by hospital procedure volume | Volume-outcome relationship; care centralization |

## Visualization Types

### Forest Plots

**Purpose**: Display effect estimates from multiple studies or subgroups in meta-analysis or subgroup analysis.

**Components**:
- Left column: Study/subgroup labels
- Center: Effect estimates (squares) with confidence intervals (horizontal lines)
- Right column: Numerical values (effect size, CI, weight)
- Bottom: Pooled estimate (diamond)

**Best Practices**:
- Use log scale for ratio measures (OR, RR, HR).
- Show weights for meta-analysis (square size proportional to weight).
- Include heterogeneity statistics (I², p-value).
- Sort studies by effect size or chronologically.
- Use consistent color scheme (e.g., blue for benefit, red for harm).

**Tools**: R (meta, metafor), Python (matplotlib, forestplot), Stata, RevMan.

### Kaplan-Meier Survival Curves

**Purpose**: Estimate and visualize survival probability over time; compare survival between groups.

**Components**:
- X-axis: Time from origin (e.g., diagnosis, treatment)
- Y-axis: Survival probability (0-1 or 0-100%)
- Step function: Kaplan-Meier estimate
- Tick marks: Censoring events
- Shaded areas or dashed lines: Confidence intervals

**Best Practices**:
- Include number-at-risk table below plot.
- Show confidence intervals (95% typical).
- Mark censoring with vertical ticks.
- Use log-rank test p-value for group comparisons.
- State time origin and event definition clearly.
- Truncate x-axis when number-at-risk becomes small (<10-20).

**Tools**: R (survival, survminer), Python (lifelines, scikit-survival), Stata, SAS.

### Additional Health Data Visualizations

| Visualization Type | Purpose | Best Practices |
|---|---|---|
| **Funnel Plots** | Assess publication bias; compare institutional performance | Plot effect size vs. precision; add confidence limits; flag outliers |
| **ROC Curves** | Evaluate diagnostic/predictive model discrimination | Plot sensitivity vs. 1-specificity; show AUC with CI; mark optimal threshold |
| **Calibration Plots** | Assess prediction model calibration | Observed vs. predicted; perfect calibration line; Hosmer-Lemeshow or Brier score |
| **Heatmaps** | Show patterns across two dimensions (e.g., time × geography) | Use colorblind-safe palette; add values for key cells; dendrogram for clustering |
| **Population Pyramids** | Compare age-sex structure across populations | Centered at zero; consistent age groups; percentages or counts |
| **Choropleth Maps** | Geographic variation in health outcomes | Use rate ratios or SMRs; account for small area variation; provide uncertainty |
| **Volcano Plots** | Display significance vs. effect size (omics, multiple outcomes) | Log-scale axes; highlight significant findings; color by category |
| **Waterfall Plots** | Show change in continuous outcome (tumor response, biomarkers) | Sort by magnitude; add reference lines; color by response category |
| **Lexis Diagrams** | Show exposure, outcome, and follow-up in cohort studies | Calendar time vs. age; mark entry/exit/events; show person-time |
| **Bland-Altman Plots** | Assess agreement between two measurement methods | Mean difference ± 1.96 SD limits; scatter of differences vs. mean |

## Report Structure Templates

### Standard Epidemiological Report Template

```
1. EXECUTIVE SUMMARY
   - Key findings (2-3 bullet points)
   - Recommendations
   - Confidence level in conclusions

2. INTRODUCTION
   - Background and rationale
   - Research question/objectives
   - Scope and limitations

3. METHODS
   - Study design
   - Data sources and population
   - Variables and measurements
   - Statistical analysis plan
   - Ethical considerations

4. RESULTS
   - Data quality summary
   - Baseline characteristics (Table 1)
   - Primary outcome results
   - Secondary outcomes
   - Subgroup analyses
   - Sensitivity analyses

5. FIGURES
   - Figure 1: Study flow diagram
   - Figure 2: Primary outcome visualization
   - Figure 3: Secondary analyses
   - Supplementary figures

6. TABLES
   - Table 1: Baseline characteristics
   - Table 2: Primary analysis results
   - Table 3: Secondary/subgroup analyses
   - Supplementary tables

7. DISCUSSION
   - Summary of main findings
   - Comparison with existing literature
   - Strengths and limitations
   - Implications for practice/policy
   - Future research needs

8. CONCLUSIONS
   - Key takeaways
   - Actionable recommendations
   - Confidence statements

9. REFERENCES
   - Citations in Vancouver or APA format
   - Evidence quality indicators (GRADE, NHMRC levels)

10. APPENDICES
    - Statistical code
    - Data dictionary
    - Ethics approval
    - Sensitivity analysis results
```

### Rapid Health Data Summary Template (Lite Mode)

```
HEALTH DATA SUMMARY
Date: [Date]
Analyst: [Role/Name]
Data Source: [System/Database]

RESEARCH QUESTION
[One sentence]

POPULATION
- Total N: [Number]
- Key characteristics: [Brief summary]

KEY FINDINGS
1. [Primary finding with CI]
2. [Secondary finding]
3. [Notable pattern]

METRICS
| Metric | Value | 95% CI |
|--------|-------|--------|
| [Metric 1] | [Value] | [CI] |
| [Metric 2] | [Value] | [CI] |

LIMITATIONS
- [Data quality issue]
- [Analysis limitation]

RECOMMENDATIONS
- [Action item 1]
- [Action item 2]

CONFIDENCE: [High/Medium/Low]
NEXT STEPS: [Full analysis / Data collection / None]
```

## Security & Privacy Considerations

### PHI/PII Handling
- **Never include identifiers** in analysis outputs, logs, or reports (names, MRN, dates of birth, full dates, geographic detail < SA3 level in AU).
- **De-identify by default**: Use study IDs, age bands, and aggregated geography.
- **Secure data environments**: Analyze data only in approved secure environments with access controls.
- **Audit trails**: Log all data access and analysis activities for compliance.
- **Output review**: Review all outputs for potential re-identification risks before sharing.

### Data Minimization
- Use only variables necessary for the analysis objective.
- Aggregate small cells (<5 counts in AU; <11 in some jurisdictions) to prevent disclosure.
- Remove indirect identifiers (rare combinations of demographics) that could enable re-identification.
- Consider k-anonymity, l-diversity, or differential privacy for high-risk datasets.

### Retention and Disposal
- Retain analysis outputs only as long as required by governance or research protocols.
- Dispose of temporary analysis files securely when analysis is complete.
- Maintain documentation of data provenance and transformations for reproducibility without retaining raw identifiers.

### Jurisdiction-Specific Privacy

| Jurisdiction | Key Requirements |
|---|---|
| **Australia** | Privacy Act 1988 (APPs), state health privacy principles, AIHW small cell guidelines (suppress <5), ABS Census and Statistics Act |
| **New Zealand** | Privacy Act 2020, Health Information Privacy Code 2020, HDC guidance, Stats NZ confidentiality rules |
| **United States** | HIPAA Safe Harbor (18 identifiers), de-identification expert determination, state privacy laws |
| **European Union** | GDPR Article 9 (health data special category), Article 89 (research exemption), pseudonymization requirements |

## Confidence Indicators

| Scenario | Confidence | Action |
|---|---|---|
| Large sample size (>1000), complete data, clear study design, well-established statistical methods | High | Proceed with analysis; draft report; flag for peer review if publication intended |
| Moderate sample (100-1000), minimal missing data, standard methods but novel population or outcome | Medium | Complete analysis; explicitly document assumptions and limitations; recommend biostatistical review |
| Small sample (<100), substantial missing data (>20%), complex methods, potential confounding | Low | Proceed cautiously; conduct extensive sensitivity analyses; require biostatistical and clinical review before any conclusions |
| Data quality concerns (outliers, inconsistencies), unclear provenance, potential selection bias | Low | Halt analysis pending data clarification; document concerns; escalate to data governance |
| Results showing serious safety concerns, unexpected harms, or major public health implications | Low | Do not finalize autonomously; escalate to clinical governance and ethics immediately |
| Real-world evidence with strong confounding, immortal time bias, or indication bias potential | Medium-Low | Acknowledge limitations prominently; avoid causal language; recommend confirmatory studies |

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---|---|---|
| Reporting only p-values without effect sizes or confidence intervals | Misleading significance; no measure of precision | Always report point estimates with confidence intervals |
| Treating association as causation | Leads to incorrect conclusions and harmful decisions | Use cautious language; consider study design limitations; triangulate evidence |
| Ignoring missing data | Biased estimates; reduced power; misleading precision | Assess missingness pattern; use multiple imputation or sensitivity analyses |
| Not adjusting for multiple comparisons | Inflated Type I error; false positives | Apply Bonferroni, FDR, or pre-specify primary outcomes |
| Overfitting prediction models | Poor generalization; optimistic performance | Use cross-validation; restrict model complexity; validate externally |
| Using inappropriate statistical tests | Invalid conclusions; violated assumptions | Check assumptions; use non-parametric or robust methods when needed |
| Presenting unadjusted and adjusted analyses inconsistently | Confusing interpretation; selective reporting | Present both clearly; justify covariates in adjusted models |
| Ignoring competing risks in survival analysis | Biased cumulative incidence estimates | Use Fine-Gray or cause-specific hazards models |
| Failing to check proportional hazards assumption | Invalid hazard ratios; misleading inference | Test Schoenfeld residuals; use time-dependent covariates or stratification |
| Producing visualizations without uncertainty | Overconfidence in point estimates | Always show confidence intervals or uncertainty bands |
| Aggregating data without accounting for clustering | Underestimated standard errors; false positives | Use mixed effects models, GEE, or cluster-robust standard errors |
| Releasing small cell counts | Risk of individual disclosure; privacy breach | Suppress cells <5 (AU) or aggregate to higher level |
| Using causal language in observational studies | Overstates evidence strength; misleads decision-makers | Use "associated with," "higher risk of," not "causes" or "prevents" |
| Not documenting analysis code | Irreproducible results; scientific misconduct | Use version control; document code thoroughly; share analysis scripts |
| Analyzing data without ethics approval | Ethical violation; potential legal consequences | Obtain HREC/IRB approval before accessing or analyzing data |

## When to Escalate

Escalate immediately when:
- Analysis involves identifiable patient data without proper governance.
- Results suggest serious patient harm, safety signals, or unexpected adverse events.
- Statistical analysis exceeds your expertise (complex methods, advanced modeling).
- Data quality issues suggest potential data corruption or systematic errors.
- Analysis requires regulatory submission (TGA, FDA, EMA) or will inform clinical guidelines.
- Publication in high-impact journal is intended (requires rigorous methodology).
- Public health emergency implications (outbreak detection, epidemic thresholds).

Escalation targets:
- **Biostatistical**: Senior biostatistician, epidemiologist, or methodologist.
- **Clinical**: Clinical director, chief medical officer, or subject matter expert.
- **Governance**: Human Research Ethics Committee (HREC), privacy officer, data governance committee.
- **Regulatory**: Regulatory affairs team, compliance officer, quality assurance.

## Tool Requirements

- `~~research literature` (PubMed, Cochrane) for evidence synthesis and literature context.
- `~~clinical terminology` (SNOMED-CT, LOINC, ICD-10-AM/ICD-11) for standardized coding and phenotype definitions.
- `~~data/statistical-analysis` for statistical methods guidance and test selection.
- `~~data/data-visualization` for visualization best practices and figure generation.
- `~~document-skills/xlsx` for data extraction and tabular outputs.
- `~~document-skills/pdf` for report generation and publication outputs.
- `~~health/clinical-systems` for validated data retrieval from EHR/EMR systems.
- `~~health/coding` for ICD-10-AM/ACHI coding support when analyzing coded data.

## Success Indicators

You have applied this skill correctly when:
- [ ] Study design and analysis approach are documented and appropriate for the research question.
- [ ] Data quality has been assessed and limitations acknowledged.
- [ ] Appropriate statistical methods have been selected and applied correctly.
- [ ] Effect estimates are reported with confidence intervals, not just p-values.
- [ ] Visualizations follow health data best practices (forest plots, survival curves, etc.).
- [ ] Risk adjustment or confounding control has been applied where necessary.
- [ ] All outputs are de-identified and privacy-protective.
- [ ] Jurisdiction assumptions are explicit (AU/NZ default unless requested otherwise).
- [ ] Causal language is avoided in observational studies.
- [ ] Analysis code and methods are documented for reproducibility.
- [ ] Ethics and governance requirements have been verified.
- [ ] Limitations are clearly stated and interpreted cautiously.

## Related Skills

- `~~health/quality-improvement` for QI project data analysis and statistical process control.
- `~~health/clinical-coding` for working with ICD-10-AM/ACHI coded datasets.
- `~~health/clinical-decision-support` for translating evidence into clinical recommendations.
- `~~data/statistical-analysis` for detailed statistical methodology and test selection.
- `~~data/data-visualization` for visualization design and implementation guidance.
- `~~document-skills/xlsx` for spreadsheet-based analysis and reporting.
- `~~document-skills/pdf` for PDF report generation and formatting.

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-02-14 | Initial health-data-report skill with epidemiological methods, statistical analysis guidance, and health-specific visualization standards |
