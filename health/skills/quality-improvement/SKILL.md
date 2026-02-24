---
name: health/quality-improvement
description: This skill should be used when planning, executing, or reporting quality improvement (QI) projects in healthcare settings. Use for PDSA cycles, accreditation preparation, clinical indicator monitoring, and continuous quality improvement initiatives.
version: 1.0.0
---

# Quality Improvement

A comprehensive framework for healthcare quality improvement projects, supporting clinicians and administrators in systematic approaches to enhance patient care, safety, and service delivery. This skill integrates evidence-based methodologies with healthcare regulatory requirements.

**Important**: This skill assists with quality improvement workflows but does not replace clinical judgment or statutory reporting obligations. Always verify compliance with local regulatory requirements.

## When to Use This Skill

Invoke this skill when:
- Planning a new quality improvement project or initiative.
- Designing or executing a Plan-Do-Study-Act (PDSA) cycle.
- Preparing for accreditation surveys or quality audits.
- Analyzing clinical indicator data and identifying improvement opportunities.
- Developing data collection plans for quality monitoring.
- Writing QI project reports for governance or regulatory submission.
- Implementing statistical process control (SPC) charts.
- Conducting root cause analysis for quality gaps.
- Mapping QI activities to jurisdictional accreditation standards (AU/NZ default).

## Regulatory Context

### Australia & New Zealand (Default)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **NSQHS Standards** (AU) | Acute care quality | Standard 1: Governance; Standard 3: Preventing Controlling Healthcare-Associated Infection |
| **ACHS EQuIP6** (AU) | Accreditation program | Assessment, monitoring, and improvement of clinical care and service delivery |
| **HQSC NZ** | National quality agency | National Patient Safety Framework; Learning from adverse events |
| **CQC Standards** (NZ) | Health and disability services | Quality assurance and risk management requirements |
| **State/Territory Acts** | Jurisdiction-specific | Mandatory reporting of serious incidents; QI data retention |

### US/EU-lite Fallback

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **Joint Commission** (US) | Hospital accreditation | ORYX performance measurement; PI.01.01.01 systematic improvement |
| **CMS Quality Measures** (US) | Federal programs | Core quality measures for reimbursement; mandatory reporting |
| **ISO 9001:2015** | International | Quality management systems; PDCA methodology alignment |

### Jurisdiction Matrix

| Jurisdiction | Applicable Regulator | Reporting Trigger | Timeframe | Required Artifacts | Escalation Point |
|--------------|---------------------|-------------------|-----------|-------------------|------------------|
| **AU - National** | ACSQHC (NSQHS) | Accreditation survey | 3-4 years | QI portfolio; SPC charts; RCA reports | Quality Manager |
| **AU - State** | State Health Dept | Serious incident review | 24-72 hours | Root cause analysis; action plans | Chief Medical Officer |
| **NZ - National** | HQSC | Sentinel event | Immediate | Notification form; preliminary review | Quality & Risk Director |
| **US** | Joint Commission/CMS | Hospital-acquired condition | Quarterly | Core measure data; improvement plans | VP Quality |

## Quick Reference

1. **Define the Problem**: Use operational definitions and baseline data.
2. **Form the Team**: Include frontline staff, data analyst, and executive sponsor.
3. **PDSA Cycles**: Plan small, test small, scale gradually.
4. **Data Quality**: Ensure valid, reliable, and timely data collection.
5. **Statistical Thinking**: Distinguish common cause vs. special cause variation.
6. **Patient-Centered**: Include patient/family input in design and evaluation.
7. **Sustainability**: Plan for control phase before implementation.
8. **Documentation**: Maintain QI file for accreditation and audit purposes.

## Operating Modes

### Standard Mode
Full quality improvement methodology with complete documentation, statistical process control, multidisciplinary team engagement, and formal reporting to governance. Use for accreditation-mandated QI projects and clinical indicator monitoring.

### Lite Mode
Streamlined guidance for rapid cycle improvements or informal "just do it" changes. Focuses on essential PDSA elements and basic data collection. Never suppresses high-risk escalation requirements or mandatory reporting obligations.

## Detailed Guidance

### 1. QI Project Framework

Every quality improvement project should follow a structured approach:

#### Phase 1: Initiation
- **Problem Statement**: Describe the gap between current and desired performance.
- **Operational Definition**: Precisely define the process or outcome being measured.
- **Aim Statement**: SMART format (Specific, Measurable, Achievable, Relevant, Time-bound).
- **Business Case**: Resources required, expected benefits, alignment with strategic priorities.

#### Phase 2: Analysis
- **Baseline Measurement**: Current state data collection (minimum 20-30 data points).
- **Process Mapping**: Flowchart the current process; identify value-add vs. waste steps.
- **Root Cause Analysis**: Fishbone diagrams, 5 Whys, or FMEA for complex issues.
- **Driver Diagram**: Primary drivers → Secondary drivers → Change ideas.

#### Phase 3: Intervention
- **Change Package**: Bundle of evidence-based interventions.
- **PDSA Cycles**: Sequential testing and refinement (see PDSA section below).
- **Implementation Strategy**: Planned adaptation using frameworks like i-PARIHS.

#### Phase 4: Evaluation
- **Outcome Measures**: Did we achieve the aim?
- **Process Measures**: Are we doing what we planned?
- **Balancing Measures**: Did we cause unintended harm?
- **Statistical Analysis**: Control charts, run charts, or appropriate statistical tests.

#### Phase 5: Sustainability
- **Control Plan**: Monitoring strategy post-implementation.
- **Spread Strategy**: Dissemination to other units or organizations.
- **Lessons Learned**: Document successes, failures, and adaptations.

### 2. PDSA Cycle Guidance

The Plan-Do-Study-Act cycle is the engine of quality improvement:

#### PLAN
- **Objective**: What are we trying to accomplish?
- **Questions**: What change might result in improvement? How will we know?
- **Prediction**: Hypothesize the outcome.
- **Plan**: Who, what, where, when for the test.
- **Data Collection**: Define measures and collection method.

**Key Questions**:
- Is the change idea feasible?
- What is the smallest scale we can test?
- What could go wrong?
- How will we collect data during the test?

#### DO
- **Execute**: Run the test according to plan.
- **Document**: Record observations, unexpected events, and deviations.
- **Collect Data**: Gather planned measures.
- **Protect Patients**: Safety monitoring throughout.

**Common Pitfalls**:
- Changing multiple variables simultaneously.
- Inadequate documentation of context.
- Not involving frontline staff in execution.

#### STUDY
- **Analyze Data**: Compare results to prediction.
- **Reflection**: What did we learn?
- **Variation**: Consider special cause vs. common cause.
- **Refinement**: What modifications are needed?

**Key Questions**:
- Did the change result in improvement?
- What contextual factors influenced results?
- Should we adapt, adopt, or abandon the change?

#### ACT
- **Decision**: What is our next action?
  - **Adopt**: Standardize the change.
  - **Adapt**: Modify and test again.
  - **Abandon**: Try a different change idea.
- **Next Cycle**: Plan the subsequent PDSA.
- **Communication**: Share learnings with stakeholders.

### 3. Data Collection Planning

#### Types of Measures

| Measure Type | Definition | Example |
|--------------|------------|---------|
| **Outcome** | Impact on patients/population | Mortality rate; patient satisfaction |
| **Process** | Steps in care delivery | % compliance with hand hygiene |
| **Structure** | Resources and capacity | Staff-to-patient ratio |
| **Balancing** | Unintended consequences | Time to treatment; staff workload |

#### Data Collection Methods

**Manual Collection**:
- Checklists and observation forms
- Chart audits (retrospective)
- Surveys and interviews
- Focus groups

**Automated Collection**:
- EHR reporting (FHIR queries)
- Clinical data warehouses
- Administrative databases
- Real-time monitoring systems

#### Sampling Strategy
- **Convenience**: Easiest to collect (risk of bias).
- **Random**: Every member of population has equal chance.
- **Systematic**: Every nth case (e.g., every 10th patient).
- **Stratified**: Ensure representation across subgroups.

**Sample Size Considerations**:
- Baseline: Minimum 20-30 data points for run charts.
- Control charts: 20-25 subgroups of 3-5 samples each.
- Statistical significance: Power analysis for hypothesis testing.

#### Measurement Reliability
- **Operational Definition**: Clear, precise definition of what is being measured.
- **Data Collection Tool**: Validated instrument or form.
- **Training**: Standardized training for data collectors.
- **Inter-rater Reliability**: Multiple collectors measuring same cases (target: kappa ≥ 0.8).
- **Pilot Testing**: Small-scale validation before full implementation.

### 4. Statistical Process Control

#### Run Charts
- **Use**: Track performance over time; detect trends.
- **Rules**: Non-random patterns (trend, shift, astronomical point).
- **Minimum**: 10-12 data points to apply rules.

#### Control Charts (SPC)
- **Purpose**: Distinguish common cause vs. special cause variation.
- **Types**:
  - p-chart: Proportions (e.g., infection rates).
  - c-chart: Counts (e.g., falls per month).
  - X-bar/R chart: Continuous data with subgroups.
  - I-MR chart: Individual measurements.
- **Interpretation**:
  - Points outside control limits = special cause.
  - Non-random patterns = special cause.
  - Points within limits = common cause (requires fundamental redesign).

### 5. Quality Improvement Methodologies

#### Model for Improvement (MFI)
Three fundamental questions:
1. What are we trying to accomplish?
2. How will we know that a change is an improvement?
3. What change can we make that will result in improvement?

#### Lean Healthcare
- **Focus**: Eliminate waste (muda) and optimize flow.
- **Waste Categories**: Defects, overproduction, waiting, non-utilized talent, transportation, inventory, motion, extra-processing (DOWNTIME).
- **Tools**: Value stream mapping, 5S, standard work, visual management.

#### Six Sigma
- **Goal**: Reduce variation (target: 3.4 defects per million).
- **DMAIC**: Define, Measure, Analyze, Improve, Control.
- **Tools**: Statistical analysis, process capability, design of experiments.

## Documentation Requirements

### QI Project File
- [ ] Project charter with aim statement and scope
- [ ] Team membership and roles
- [ ] Literature review or evidence summary
- [ ] Baseline data and operational definitions
- [ ] Process maps and flowcharts
- [ ] Root cause analysis documentation
- [ ] PDSA cycle documentation (all iterations)
- [ ] Run/control charts with interpretation
- [ ] Sustainability and control plan
- [ ] Lessons learned and spread strategy

### Accreditation Evidence
- [ ] Alignment with applicable standards (NSQHS, EQuIP6, Joint Commission)
- [ ] Evidence of governance oversight and approval
- [ ] Demonstration of systematic improvement methodology
- [ ] Patient/family engagement documentation
- [ ] Staff training and competency records
- [ ] Evaluation of outcomes and balancing measures

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **No operational definition** | Ambiguity leads to inconsistent measurement | Define precisely what is being measured, including inclusion/exclusion criteria |
| **Insufficient baseline data** | Cannot distinguish improvement from random variation | Collect minimum 20-30 data points before intervention |
| **Multiple simultaneous changes** | Cannot determine which change caused effect | Test one change at a time using PDSA |
| **Ignoring balancing measures** | May cause unintended harm elsewhere | Always monitor for negative consequences |
| **Concluding too early** | Special cause may be temporary | Wait for sustained improvement over time |
| **Confusing audit with QI** | Audits identify gaps; QI improves systems | Use QI methodology to address audit findings |
| **Top-down mandates** | Frontline staff lack ownership | Engage those doing the work in design and testing |
| **No sustainability plan** | Improvements revert after project ends | Develop control plan before implementation |
| **Data without context** | Numbers alone don't explain variation | Annotate charts with contextual events |
| **Complex interventions first** | High risk of failure and resource waste | Start with small-scale tests of change |

## When to Escalate

Escalate to Quality Manager or Chief Medical Officer when:
- Patient safety is or may be compromised by the improvement effort.
- Data reveals sentinel events or serious incidents requiring statutory reporting.
- Project requires resources beyond team authority or budget.
- Resistance from clinical leaders or significant stakeholder conflict.
- Results suggest fundamental system redesign is needed (common cause variation).
- Accreditation survey is imminent and QI documentation is incomplete.
- Project timeline cannot meet regulatory or accreditation deadlines.

## Privacy Considerations

- **PHI Involved**: Yes - QI projects often use patient-level data.
- **Data Minimization**: Collect only data elements necessary for the specific QI question.
- **De-identification**: Use patient identifiers only for data linkage; remove before analysis and reporting.
- **Access Controls**: Limit QI data access to project team members with legitimate need.
- **Retention**: Retain QI records according to organizational policy (typically 7+ years for accreditation).
- **Aggregation**: Report results in aggregate to protect individual privacy.
- **No Persistence**: Do not store PHI in temporary workspaces or chat history.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Standard PDSA cycle with clear outcome measure and stable baseline | High | Proceed with testing; document and monitor |
| Complex system intervention with multiple variables | Medium | Consult with statistician or QI expert; consider stepped-wedge design |
| Results suggest patient harm or safety compromise | Low | **BLOCKER**: Escalate immediately; halt intervention pending review |
| Ambiguous data or unclear causation | Medium | Flag for QI specialist review; collect additional data before proceeding |
| Accreditation-critical QI project with survey imminent | Medium | Escalate to Quality Manager for oversight and resource allocation |
| Novel intervention without evidence base | Low | Require literature review and ethics consideration; involve Research Office if research intent |

## Tool Requirements

- `~~project tracker` - For QI project management and milestone tracking
- `~~cloud storage` - For QI file storage and team collaboration
- `~~health/clinical-systems` - For accessing EHR data and clinical indicators
- `~~data analysis` - For statistical analysis and visualization (SPC charts)
- `~~document collaboration` - For team documentation and reporting

## Success Indicators

You've applied this skill well when:
- [ ] Aim statement is SMART and aligned with organizational priorities
- [ ] Operational definitions are clear and measurement is reliable
- [ ] PDSA cycles are documented with predictions and reflections
- [ ] Data is displayed over time using run or control charts
- [ ] Team includes frontline staff and has executive sponsor
- [ ] Balancing measures are monitored and reported
- [ ] Documentation is complete for accreditation purposes
- [ ] Sustainability plan is in place before implementation
- [ ] Patient/family perspective is incorporated
- [ ] Results are statistically significant or practically important

## Related Skills

- `~~health/incident-reporting` - When QI reveals serious incidents requiring formal reporting
- `~~health/clinical-risk-assessment` - For risk assessment in QI project design
- `~~health/policy-development` - When QI results require policy changes
- `~~data/statistical-analysis` - For advanced statistical methods in QI evaluation
- `product-management/roadmap-management` - For prioritizing QI projects in organizational strategy
