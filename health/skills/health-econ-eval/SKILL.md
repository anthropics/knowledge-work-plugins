---
name: health/health-econ-eval
description: This skill should be used when conducting health economic evaluations including cost-effectiveness analysis (CEA), cost-utility analysis (CUA), cost-benefit analysis (CBA), budget impact analysis (BIA), decision modeling, sensitivity analysis, QALY/DALY calculations, or preparing economic evidence for healthcare decision-making.
version: 1.0.0
---

# Health Economic Evaluation

A comprehensive framework for conducting health economic evaluations to support healthcare resource allocation decisions. This skill guides users through cost-effectiveness, cost-utility, and cost-benefit analyses with jurisdiction-specific reference case requirements and decision modeling methodologies.

**Important**: This skill assists with economic evaluation methodology but does not replace specialist health economist expertise. Complex models or submissions to reimbursement authorities should involve qualified health economists. Always verify compliance with jurisdiction-specific reference case requirements.

## When to Use This Skill

Invoke this skill when:
- Conducting cost-effectiveness analysis (CEA) for a new intervention vs. comparator.
- Performing cost-utility analysis (CUA) with QALY or DALY outcomes.
- Preparing cost-benefit analysis (CBA) for healthcare investments.
- Developing decision models (decision trees, Markov models, microsimulation).
- Calculating quality-adjusted life years (QALYs) or disability-adjusted life years (DALYs).
- Conducting budget impact analysis (BIA) for formulary or policy decisions.
- Performing deterministic or probabilistic sensitivity analysis.
- Preparing economic evidence for HTA submissions (PBAC, MSAC, PHARMAC, NICE, CADTH).
- Evaluating healthcare interventions from multiple perspectives (healthcare sector, societal).
- Estimating incremental cost-effectiveness ratios (ICERs) and cost-effectiveness acceptability curves (CEACs).
- Addressing reference case requirements by jurisdiction.
- Calculating utility weights for health state valuations.
- Estimating costs for economic evaluation (direct medical, direct non-medical, indirect).
- Conducting equity-informative economic evaluations.

## Regulatory Context

### Australia & New Zealand (Default)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **PBAC Guidelines** (AU) | Pharmaceutical reimbursement | Section A: Submission requirements; Reference case for CEA/CUA; mandatory societal perspective analysis; $50,000-75,000/QALY informal threshold |
| **MSAC Guidelines** (AU) | Medical services evaluation | Application requirements for new medical technologies; emphasis on safety, effectiveness, and cost-effectiveness |
| **PHARMAC Decision Criteria** (NZ) | Pharmaceutical funding | Nine decision criteria including health gains, cost, equity, and need; cost-effectiveness not sole determinant |
| **ANZHTA Guidelines** | Economic evaluation methods | Reporting standards for health economic evaluations in Australia and New Zealand |
| **MBS/PBS Costing** | Cost data sources | Schedule fees for direct costs; utility weights from Australian preference-based studies preferred |

### US/EU-lite Fallback

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **ISPOR Good Practices** | International standards | Conduct, reporting, and interpretation of cost-effectiveness analyses; reference case guidance |
| **ICER Guidelines** (US) | Value assessment framework | Cost-effectiveness thresholds ($50,000-150,000/QALY); contextual considerations for pricing |
| **NICE Reference Case** (UK) | HTA methodology | NHS/PSS perspective; QALY as outcome; £20,000-30,000/QALY threshold; societal perspective optional |
| **CADTH Guidelines** (Canada) | Health technology assessment | Canadian healthcare system perspective; CUA preferred; $50,000 CAD/QALY threshold considered |

### Jurisdiction Matrix

| Jurisdiction | Applicable Regulator | Reporting Trigger | Timeframe | Required Artifacts | Escalation Point |
|--------------|---------------------|-------------------|-----------|-------------------|------------------|
| **AU - Pharmaceutical** | PBAC | Pre-submission meeting → Main submission | 17 weeks (clock start to PBAC meeting) | Submission document; economic model; budget impact model | Health Economist; PBAC Meeting |
| **AU - Medical Services** | MSAC | Application for new MBS item | Variable by committee schedule | Application form; clinical evidence; economic evaluation | MSAC Executive Officer |
| **NZ** | PHARMAC | Proposal for funding (PTAC) | Rolling consideration; no fixed timeline | Proposal document; clinical and cost-effectiveness evidence | PHARMAC Assessment Team |
| **UK** | NICE | Technology appraisal referral | ~40 weeks (STA process) | Submission; economic model; evidence synthesis | NICE Committee Meeting |
| **Canada** | CADTH | CDR submission | ~180 days | Submission dossier; economic model | CADTH Review Panel |

## Quick Reference

1. **Select Evaluation Type**: CEA (natural units), CUA (QALYs), CBA (monetary), BIA (budget impact).
2. **Define Perspective**: Healthcare sector (default for PBAC), Societal (required for PBAC), Other (specify).
3. **Choose Time Horizon**: Capture all relevant differences in costs and outcomes; lifetime typical for chronic conditions.
4. **Select Comparator**: Standard of care in jurisdiction; do-nothing rarely appropriate.
5. **Estimate Costs**: Direct medical (healthcare system), Direct non-medical (patient), Indirect (productivity).
6. **Measure Outcomes**: Natural units (CEA), QALYs (CUA preferred), DALYs (burden of disease).
7. **Calculate ICER**: (Cost_new - Cost_comparator) / (Effect_new - Effect_comparator).
8. **Apply Discounting**: Costs and outcomes at 5% (AU), 3% or 1.5% (varies); 0% for <1 year.
9. **Conduct Sensitivity Analysis**: Deterministic (univariate, scenario) and probabilistic (PSA).
10. **Report Uncertainty**: CEACs, tornado diagrams, budget impact projections.
11. **Address Equity**: Consider distributional impacts; equity-informative analysis when relevant.
12. **Follow Reference Case**: Jurisdiction-specific requirements for comparability.

## Operating Modes

### Standard Mode
Full economic evaluation with complete decision modeling, comprehensive sensitivity analysis, detailed costing, and adherence to reference case requirements. Includes probabilistic sensitivity analysis, extensive scenario analyses, and detailed reporting for HTA submission. Use when preparing for PBAC, MSAC, or formal reimbursement submissions.

### Lite Mode
Streamlined economic evaluation for preliminary assessment, internal decision-making, or proof-of-concept. Includes basic decision tree or simple Markov model, deterministic sensitivity analysis only, and simplified costing. Never suppresses critical model validation requirements or high-stakes reimbursement decisions. Clearly mark as preliminary and recommend full evaluation before formal submission.

## Detailed Guidance

### 1. Evaluation Type Selection

#### Cost-Effectiveness Analysis (CEA)
- **When to Use**: Single outcome measure in natural units (e.g., lives saved, mmHg reduction).
- **Outcome**: Clinical effectiveness measure without quality adjustment.
- **Limitation**: Cannot compare across different disease areas.
- **Comparator ICER**: Reported as cost per natural unit gained.
- **Reference Case**: Acceptable when QALY measurement not feasible; must justify.

#### Cost-Utility Analysis (CUA) - Preferred
- **When to Use**: Comparing interventions across different health conditions.
- **Outcome**: Quality-adjusted life years (QALYs) or disability-adjusted life years (DALYs).
- **Advantage**: Enables cross-program comparisons; preferred by most HTA bodies.
- **Utility Sources**: Preference-based measures (EQ-5D, SF-6D, AQoL for Australia).
- **Reference Case**: PBAC, NICE, CADTH require CUA as primary analysis.

#### Cost-Benefit Analysis (CBA)
- **When to Use**: Comparing healthcare with non-health investments; environmental health.
- **Outcome**: Monetary value of health benefits (willingness-to-pay or human capital).
- **Challenge**: Controversial valuation of life/health; ethical concerns.
- **Use in Health**: Rare for clinical interventions; more common for public health policy.

#### Budget Impact Analysis (BIA)
- **When to Use**: Assessing affordability and financial sustainability.
- **Complement**: Always alongside CEA/CUA, not instead of.
- **Timeframe**: Typically 3-5 years.
- **Perspective**: Payer/health system budget; may include patient out-of-pocket.
- **Outputs**: Annual budget impact; cumulative impact; per-patient vs. population.

### 2. Decision Modeling Framework

#### Decision Trees
- **Appropriate When**: Single decision point; short time horizon; no recurrence.
- **Structure**: Decision node → Chance nodes → Terminal nodes.
- **Elements**: Probabilities, costs, utilities at each branch.
- **Analysis**: Roll-back analysis to calculate expected values.
- **Software**: TreeAge Pro, R (heemod), Excel.

**Key Considerations**:
- Ensure probabilities sum to 1.0 at each chance node.
- Include all relevant pathways (don't truncate early without justification).
- Validate probabilities against clinical evidence.

#### Markov Models
- **Appropriate When**: Chronic conditions; recurring events; long time horizons.
- **Structure**: Mutually exclusive health states; transition probabilities; cycle length.
- **Key Elements**:
  - Health states (e.g., stable, progression, death).
  - Transition probabilities (per cycle).
  - Costs and utilities per state (or transition).
  - Cycle length (e.g., monthly, yearly).
  - Half-cycle correction (recommended for simple Markov).
- **Analysis**: Cohort simulation or Monte Carlo microsimulation.

**Half-Cycle Correction**:
- Apply to account for transitions assumed to occur mid-cycle.
- Subtract half a cycle's cost and utility from initial state.
- Add half a cycle's cost and utility to final state.
- Alternative: Life-table method or tunnel states.

**Markov Model Validation**:
- Face validity: Clinical experts review state definitions and transitions.
- Internal validity: Check transition probabilities sum to ≤1.0 (allowing for death).
- External validity: Compare model outcomes to real-world data if available.
- Cohort trace: Review state occupancy over time for plausibility.

#### Microsimulation (Individual-Level Simulation)
- **Appropriate When**: Heterogeneous population; complex patient history; need for individual tracking.
- **Approach**: Simulate individual patients through the model; aggregate results.
- **Advantage**: Captures patient history; handles heterogeneity; memory-less assumption relaxed.
- **Disadvantage**: Computationally intensive; longer run times.
- **Sample Size**: Typically 1,000-100,000 individuals depending on precision needed.

#### Discrete Event Simulation (DES)
- **Appropriate When**: Resource constraints; queueing important; complex timing.
- **Use Cases**: ED modeling, surgical scheduling, capacity planning.
- **Software**: Simul8, Arena, R (simmer package).

### 3. Reference Case Requirements by Jurisdiction

#### PBAC (Australia) Reference Case

| Element | Requirement | Notes |
|---------|-------------|-------|
| **Perspective** | Healthcare sector + Societal | Two perspectives required; societal includes productivity |
| **Comparator** | Standard therapy in Australia | Current PBS-listed therapy or best supportive care |
| **Time Horizon** | Sufficient to capture all differences | Lifetime typical for chronic conditions |
| **Discounting** | 5% (costs and outcomes) | Sensitivity analysis at 0% and 3.5% |
| **Outcome** | QALYs preferred | CEA acceptable if QALYs not feasible; justify |
| **Utility Source** | Australian preference-based | AQoL, EQ-5D-5L (Australian tariffs) preferred |
| **Cost Data** | PBS/MSAC schedule fees | Publicly listed prices; patient co-payments |
| **ICER Threshold** | $50,000-75,000/QALY (informal) | Consider "rule of rescue" and other factors |
| **Uncertainty** | PSA required | Deterministic and probabilistic sensitivity analysis |
| **Subgroups** | Pre-specified and justified | Clinical or economic rationale required |

#### MSAC (Australia) Reference Case
- Similar to PBAC but focused on medical services.
- MBS fees for cost estimation.
- Emphasis on safety data alongside effectiveness and cost-effectiveness.
- May include diagnostic accuracy parameters (sensitivity, specificity).

#### PHARMAC (New Zealand) Considerations
- Nine decision criteria beyond cost-effectiveness.
- Cost-effectiveness important but not determining factor.
- Equity considerations (access for Māori and vulnerable populations).
- Comparator: Current best practice in New Zealand.
- Threshold: Not explicitly defined; assess on case-by-case basis.

#### NICE (UK) Reference Case
- Perspective: NHS and Personal Social Services (PSS).
- Outcome: QALYs calculated using EQ-5D-3L (UK tariff).
- Time horizon: Long enough to capture all costs and benefits.
- Discounting: 1.5% (interventions >30 years); 3.5% otherwise.
- Threshold: £20,000-30,000/QALY (can be exceeded with strong justification).
- PSA: Required for all evaluations.

#### CADTH (Canada) Reference Case
- Perspective: Publicly funded healthcare system.
- Outcome: QALYs preferred; life years acceptable for life-saving interventions.
- Utility: Canadian preference-based measures preferred; EQ-5D acceptable.
- Discounting: 5% (with 0% and 3% sensitivity); 1.5% for vaccines.
- Time horizon: Lifetime for most conditions.
- Productivity: Optional; include in supplementary analysis.

### 4. Costing Methodology

#### Cost Categories

**Direct Medical Costs**:
- Pharmaceuticals (drug acquisition, administration, monitoring).
- Hospitalizations (admissions, procedures, ED visits).
- Outpatient care (consultations, diagnostics, allied health).
- Device costs (purchase, maintenance, replacement).
- **Source**: PBS/MSAC schedules, DRG costs, hospital cost data.

**Direct Non-Medical Costs**:
- Patient transport to care.
- Carer costs (formal and informal).
- Over-the-counter medications.
- **Inclusion**: Required for societal perspective (PBAC); optional for healthcare perspective.

**Indirect Costs (Productivity)**:
- Absenteeism (time off work due to illness).
- Presenteeism (reduced productivity at work).
- Mortality costs (lost future productivity).
- **Method**: Human capital approach (standard) or friction cost approach.
- **PBAC**: Required for societal perspective; include in supplementary analysis.

#### Cost Estimation Approaches

**Micro-costing** (Bottom-up):
- Detailed measurement of resource use for each activity.
- Accurate but time-consuming.
- Preferred for high-cost components or when precise estimates needed.

**Gross-costing** (Top-down):
- Average costs per episode or patient.
- Efficient for large components with less variation.
- Common for hospitalizations (DRG-based).

**Hybrid Approach**:
- Micro-costing for key cost drivers.
- Gross-costing for less critical components.
- Most practical for most economic evaluations.

#### Future Costs in Life-Years Gained

**PBAC/NICE/CADTH Position**:
- Related costs (for the condition being treated): Include.
- Unrelated costs (other diseases in added life-years): Exclude.
- Exception: Where specified in reference case or treatment affects other conditions.

**Rationale**: Including unrelated costs discriminates against life-saving interventions for younger patients (who have more future costs).

### 5. QALY/DALY Calculation Guidance

#### Quality-Adjusted Life Years (QALYs)

**Calculation**:
```
QALYs = Σ (Utility_state × Time_in_state)
```

**Utility Values**:
- Range: 0 (dead) to 1 (full health); can be negative (worse than dead).
- Measured using preference-based instruments.
- Sources: Clinical trials, observational studies, published literature.

**Preference-Based Instruments**:

| Instrument | Description | Preferred For |
|------------|-------------|---------------|
| **EQ-5D-5L** | 5 dimensions (mobility, self-care, usual activities, pain/discomfort, anxiety/depression), 5 levels each | General HTA; PBAC, NICE, CADTH |
| **EQ-5D-3L** | Original 3-level version | Legacy studies; NICE UK tariff |
| **SF-6D** | Derived from SF-36 health survey | When SF-36 collected in trials |
| **AQoL** (AU) | Australian Quality of Life instrument | PBAC preference for Australian context |
| **HUI-3** | Health Utilities Index | Pediatric populations; vision/hearing |
| **15D** | 15 dimensions | Finnish and Scandinavian contexts |

**Mapping**:
- When trial collects non-preference measure (e.g., disease-specific HRQoL).
- Use published mapping algorithms to estimate utility.
- Report uncertainty from mapping in sensitivity analysis.

**Time Trade-Off (TTO)**:
- Direct utility elicitation method.
- Patients choose between living X years in health state vs. Y years in full health.
- Utility = Y/X.
- Used to value EQ-5D health states.

**Standard Gamble (SG)**:
- Alternative direct elicitation.
- Choice between certain health state vs. gamble (probability p of full health, 1-p of immediate death).
- Utility = p that makes respondent indifferent.
- Theoretically grounded in expected utility theory but less intuitive.

#### Disability-Adjusted Life Years (DALYs)

**Calculation**:
```
DALYs = YLL + YLD
```

Where:
- YLL (Years of Life Lost): Premature mortality component.
- YLD (Years Lived with Disability): Morbidity component.

**Formula**:
```
YLL = N × L × DCF
YLD = I × DW × L × DCF
```

Where:
- N = Number of deaths
- I = Number of incident cases
- DW = Disability weight (0 = full health, 1 = death)
- L = Duration or life expectancy
- DCF = Discounting and age-weighting correction factor

**Key Differences from QALYs**:
- DALYs measure burden (lower is better); QALYs measure benefit (higher is better).
- DALYs use disability weights (not utilities); different valuation methods.
- DALYs can incorporate age-weighting and discounting differently.
- Cost per DALY averted (intervention perspective) vs. cost per QALY gained.

**WHO Global Burden of Disease**:
- Standardized DALY methodology for cross-national comparison.
- Updated disability weights in GBD 2019 using population surveys.
- Useful for public health priority setting and global health economics.

### 6. Sensitivity Analysis Framework

#### Deterministic Sensitivity Analysis (DSA)

**Univariate Analysis**:
- Vary one parameter at a time across plausible range.
- Identify key drivers of model results.
- Report as tornado diagrams (ranked by impact).
- Typical ranges: ±20% of base case; 95% CI from evidence; expert opinion.

**Scenario Analysis**:
- Test alternative assumptions or structural choices.
- Examples: Different time horizons, alternative comparators, inclusion/exclusion of specific costs.
- Best/worst case scenarios using extreme but plausible parameter values.

**Threshold Analysis**:
- Identify parameter value at which decision changes.
- Useful for negotiations (e.g., maximum acceptable price).

#### Probabilistic Sensitivity Analysis (PSA)

**Purpose**: Characterize joint uncertainty across all parameters simultaneously.

**Method**:
1. Assign probability distributions to uncertain parameters.
2. Run model for large number of iterations (typically 1,000-10,000).
3. Record results for each iteration.
4. Analyze distribution of results.

**Distribution Selection**:

| Parameter Type | Distribution | Rationale |
|----------------|--------------|-----------|
| Probabilities | Beta (α, β) | Bounded 0-1; conjugate for binomial |
| Costs | Gamma (shape, scale) | Bounded 0+; right-skewed |
| Utilities | Beta or Normal (truncated) | Bounded 0-1 or plausible range |
| Relative Effects | Log-normal | Multiplicative; bounded 0+ |
| Counts | Poisson or Gamma | Count data or rates |

**Cost-Effectiveness Acceptability Curves (CEAC)**:
- Plot probability that intervention is cost-effective across range of willingness-to-pay thresholds.
- X-axis: Willingness-to-pay threshold ($/QALY).
- Y-axis: Probability cost-effective.
- Interpret: At $50,000/QALY, 80% probability intervention is cost-effective.

**Cost-Effectiveness Plane**:
- Scatter plot of incremental costs (y-axis) vs. incremental effects (x-axis).
- Quadrants: NE (more effective, more costly - trade-off), SE (dominant), SW (less effective, less costly - trade-off), NW (dominated).
- Ellipse: 95% confidence region.

**Expected Value of Perfect Information (EVPI)**:
- Value of eliminating all uncertainty.
- Guides research prioritization.
- Population EVPI: EVPI per patient × eligible population over technology lifetime.

### 7. Equity-Informative Economic Evaluation

**Extended Cost-Effectiveness Analysis (ECEA)**:
- Incorporates distributional impacts (e.g., by socioeconomic status).
- Analyzes financial risk protection (catastrophic health expenditure).
- Useful for universal health coverage decisions.

**Distributional Cost-Effectiveness Analysis (DCEA)**:
- Estimates cost-effectiveness for different population subgroups.
- Incorporates equity weights (societal value placed on gains to disadvantaged groups).
- Can justify interventions with higher ICERs if they benefit disadvantaged populations.

**PBAC Equity Considerations**:
- Consider "rule of rescue" for life-threatening conditions with no alternatives.
- Impact on specific populations (rare diseases, indigenous populations).
- Uncertainty and its consequences (higher threshold for greater uncertainty).

**PHARMAC Equity Criteria**:
- Health needs of particular populations (including Māori).
- Impact on health disparities.
- Access for vulnerable groups.

### 8. Model Validation and Transparency

**Validation Types**:

1. **Face Validity**: Does the model structure make clinical sense?
   - Review by clinical experts.
   - Plausibility of assumptions.

2. **Internal Validity**: Does the model produce expected results?
   - Check transition probabilities sum correctly.
   - Verify cohort survival matches life tables.
   - Test extreme parameter values (0, 1) for logical behavior.

3. **External Validity**: Do model predictions match real-world data?
   - Comparison to clinical trial results if available.
   - Validation against observational datasets.
   - Cross-validation with published models.

4. **Cross-Validation**: Compare results to other models addressing same question.
   - Important for PBAC/NICE submissions with multiple sponsor models.

**Transparency Requirements**:
- Full model documentation (conceptual, mathematical, programming).
- Access to model for HTA reviewers (Excel, TreeAge, R code).
- Clear reporting of assumptions and limitations.
- CHEERS checklist adherence for publications.

### 9. Software and Tools

**Decision Modeling**:
- TreeAge Pro: Commercial; industry standard for HTA submissions.
- R (heemod, BCEA, dampack packages): Open-source; increasingly accepted.
- Excel: Widely used; transparency advantage; PSA via add-ins or manual.

**Statistical Analysis**:
- R: Preferred for PSA, meta-analysis, survival analysis.
- Stata: Common in health economics; extensive econometric capabilities.
- WinBUGS/OpenBUGS: Bayesian analysis; increasingly used for network meta-analysis.

**Reporting**:
- Shiny (R): Interactive web applications for presenting results.
- VOItools: Value of information analysis.

## Documentation Requirements

### Economic Evaluation Report
- [ ] Executive summary with key findings and ICER.
- [ ] Clear statement of decision problem and research question.
- [ ] Description of intervention and comparator(s).
- [ ] Specification of target population and subgroups.
- [ ] Perspective(s) and time horizon with justification.
- [ ] Model structure diagram and description (or rationale for no model).
- [ ] Data inputs table with sources and uncertainty ranges.
- [ ] Costing methodology and unit costs with sources.
- [ ] Utility derivation (instrument, source, mapping if applicable).
- [ ] Base case results (incremental costs, effects, ICER).
- [ ] Sensitivity analysis results (deterministic and probabilistic).
- [ ] Cost-effectiveness plane and CEACs.
- [ ] Budget impact analysis (if applicable).
- [ ] Scenario analyses and threshold analyses.
- [ ] Validation approach and results.
- [ ] Limitations and generalizability.
- [ ] Conclusions and recommendations.
- [ ] Technical appendix with detailed model specification.
- [ ] Model files provided in appropriate format (Excel, TreeAge, R code).

### HTA Submission Documentation
- [ ] Submission template completed per jurisdiction requirements.
- [ ] Evidence synthesis (systematic review or network meta-analysis).
- [ ] Clinical evidence summary with GRADE assessment.
- [ ] Economic evaluation report (as above).
- [ ] Budget impact model with scenario analyses.
- [ ] De novo model or adaptation justification.
- [ ] Model validation documentation.
- [ ] Uncertainty analysis (PSA results, CEACs).
- [ ] Equity and distributional considerations.
- [ ] Patient and clinician input (if available).
- [ ] Implementation considerations and feasibility.

### Model Documentation
- [ ] Conceptual model description and rationale.
- [ ] Mathematical specification (equations, formulas).
- [ ] Programming documentation (code comments, structure).
- [ ] Parameter table with all values, distributions, and sources.
- [ ] Transition matrix (for Markov models).
- [ ] Decision tree structure with all branches and terminal nodes.
- [ ] Cohort trace or individual patient simulation description.
- [ ] Calculation verification (checksums, independent replication).

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **Wrong comparator** | Comparing to placebo or outdated therapy doesn't inform reimbursement decisions | Use current standard of care in jurisdiction |
| **Inappropriate time horizon** | Too short misses long-term costs/outcomes; too long adds uncertainty unnecessarily | Use lifetime for chronic conditions; justify horizon choice |
| **Discounting costs but not outcomes** | Violates time preference consistency; reference cases require both or neither | Discount costs AND QALYs at reference case rate; 0% for both in sensitivity |
| **Ignoring half-cycle correction** | Introduces systematic bias in Markov models; especially problematic with long cycles | Apply half-cycle correction or use life-table/tunnel state methods |
| **Double-counting outcomes** | Including both survival and QALYs as separate outcomes in same analysis | Use QALYs only (which incorporate survival and quality) or disaggregate carefully |
| **PSA with inappropriate distributions** | Using normal distribution for probabilities (can sample >1 or <0) | Use Beta for probabilities, Gamma for costs, Log-normal for relative effects |
| **Insufficient PSA iterations** | Too few iterations (<1,000) leads to unstable CEACs and imprecise estimates | Use minimum 1,000 iterations; 5,000-10,000 preferred for final submission |
| ** cherry-picking favorable subgroups** | Post-hoc subgroup analysis inflates Type I error; not pre-specified | Pre-specify subgroups with clinical rationale; adjust for multiple comparisons |
| **Using foreign utility weights** | Utilities vary by country due to cultural differences in health valuation | Use jurisdiction-specific tariffs when available (e.g., AQoL for Australia) |
| **Ignoring structural uncertainty** | Model structure choices (e.g., number of health states) can drive results more than parameters | Conduct scenario analyses for structural assumptions; consider model averaging |
| **Presenting average cost-effectiveness ratios** | Comparing intervention to no treatment instead of relevant comparator | Always report INCREMENTAL cost-effectiveness ratios vs. appropriate comparator |
| **Failing to validate the model** | Model may produce implausible results or contain programming errors | Face validity with experts; internal checks; external validation when possible |
| **Not addressing equity** | May miss important societal considerations beyond efficiency | Include equity analysis when relevant; report distributional impacts |
| **Omitting budget impact analysis** | Cost-effective interventions may still be unaffordable at population level | Always accompany CEA with BIA for decision-making |

## When to Escalate

Escalate to Health Economist, Health Economics Lead, or HTA Specialist when:
- ICER exceeds jurisdiction threshold ($50,000-75,000/QALY in Australia; £20,000-30,000 in UK).
- Model structure decisions have major impact on results (structural uncertainty).
- Parameter uncertainty is so high that decision is not robust.
- Complex modeling required (microsimulation, DES, complex disease progression).
- Submission to PBAC, MSAC, NICE, CADTH, or PHARMAC.
- Novel intervention without existing economic evidence or comparators.
- Equity considerations suggest differential cost-effectiveness by subgroup.
- Budget impact exceeds acceptable threshold despite favorable ICER.
- Model validation reveals significant discrepancies from expected results.
- Intervention affects multiple disease areas or health system sectors.
- Need for sophisticated sensitivity analysis (EVPPI, expected value of sample information).

## Privacy Considerations

- **PHI Involved**: Minimal - economic evaluations typically use aggregate data or de-identified patient-level data.
- **Data Minimization**: Use summary statistics rather than individual patient data where possible.
- **De-identification**: If using patient-level data for costing or utility estimation, remove all identifiers (names, MRNs, dates of birth).
- **Access Controls**: Limit access to underlying datasets to those with legitimate need.
- **Retention**: Retain economic models and documentation per organizational policy (typically 7+ years for HTA submissions).
- **No Persistence**: Do not store patient-level data in model files or documentation.
- **Third-Party Data**: Ensure appropriate data sharing agreements when using external datasets.
- **Public Release**: Models submitted to HTA bodies may become public; ensure no embedded PHI.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Standard CUA with well-established comparator, clear clinical evidence, and standard Markov model | High | Proceed with evaluation; document assumptions; standard QA |
| Complex microsimulation or DES with heterogeneous population | Medium | Consult health economist; validate model extensively; consider external review |
| ICER near or above jurisdiction threshold; requires sensitivity analysis interpretation | Medium | Escalate to health economics lead; document uncertainty thoroughly |
| Novel therapy without comparators or natural history data available | Low | **BLOCKER**: Escalate immediately; require expert health economist involvement; may need de novo data collection |
| Budget impact exceeds health system capacity despite favorable ICER | Medium | Escalate for policy discussion; affordability separate from cost-effectiveness |
| Structural uncertainty dominates over parameter uncertainty | Low | Flag for model validation review; consider multiple model structures or model averaging |
| Equity concerns suggest differential cost-effectiveness by disadvantaged group | Medium | Conduct distributional analysis; escalate for equity-informed decision-making |
| Submission to HTA body with strict reference case requirements | Medium | Engage specialist health economist; ensure full compliance with guidelines |
| External validation fails (model predictions diverge from real-world data) | Low | **BLOCKER**: Halt submission pending model revision and re-validation |
| Multiple competing interventions requiring network meta-analysis | Medium | Escalate for statistical support; ensure transitivity and consistency assumptions |

## Tool Requirements

- `~~research literature` (PubMed) - For clinical evidence and utility weights.
- `~~data/statistical-analysis` - For meta-analysis, survival analysis, PSA.
- `~~health/evidence-synthesis` - For systematic reviews and network meta-analysis.
- `~~cloud storage` - For model files and documentation storage.
- `~~document collaboration` - For team review of economic evaluation reports.
- `~~project tracker` - For HTA submission timelines and milestones.
- `~~health/clinical-systems` - For accessing cost data and administrative datasets (if applicable).

## Success Indicators

You've applied this skill well when:
- [ ] Evaluation type (CEA/CUA/CBA) is appropriate for decision context and justified.
- [ ] Comparator represents current standard of care in jurisdiction.
- [ ] Time horizon captures all relevant differences in costs and outcomes.
- [ ] Perspective(s) align with reference case requirements.
- [ ] Discounting applied correctly to both costs and outcomes.
- [ ] QALYs calculated using appropriate utility instrument and jurisdiction-specific tariffs.
- [ ] Model structure is appropriate for disease natural history and decision context.
- [ ] All parameters sourced from best available evidence with uncertainty characterized.
- [ ] Sensitivity analysis includes both deterministic and probabilistic approaches.
- [ ] CEACs and cost-effectiveness plane visualize decision uncertainty.
- [ ] Model has been validated (face, internal, and external where possible).
- [ ] Budget impact analysis accompanies cost-effectiveness results.
- [ ] Documentation follows reference case requirements for jurisdiction.
- [ ] Equity and distributional considerations addressed where relevant.
- [ ] Submission package complete with model files and technical appendix.
- [ ] All PHI has been removed or appropriately de-identified.
- [ ] Health economist has reviewed complex models or high-stakes submissions.

## Related Skills

- `~~health/hta-submission` - For preparing formal HTA submissions to PBAC, MSAC, NICE, CADTH, PHARMAC.
- `~~health/evidence-synthesis` - For systematic reviews and meta-analyses feeding into economic models.
- `~~health/clinical-guidelines` - For understanding comparator therapies and standard of care.
- `~~data/statistical-analysis` - For statistical methods in evidence synthesis and PSA.
- `~~research/grants` - For health economics components of research grant applications.
- `~~finance/budgeting` - For budget impact analysis and financial planning.
- `~~document/technical-writing` - For preparing economic evaluation reports and HTA submissions.
