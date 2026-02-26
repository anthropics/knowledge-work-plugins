---
name: health/hta-submission
description: This skill should be used when preparing Health Technology Assessment (HTA) submissions to reimbursement authorities including PBAC (Australia), MSAC (Australia), PHARMAC (New Zealand), NICE (UK), CADTH (Canada), or when structuring health technology assessment dossiers, submission templates, evidence packages, or preparing for HTA committee meetings.
version: 1.0.0
---

# HTA Submission Preparation

A comprehensive framework for preparing Health Technology Assessment (HTA) submissions to pharmaceutical and medical services reimbursement authorities. This skill guides users through jurisdiction-specific submission requirements, evidence compilation, and common pitfalls to avoid in the reimbursement process.

**Important**: This skill assists with HTA submission preparation but does not guarantee reimbursement approval. Submission requirements change periodically—always verify current guidelines from the relevant authority. Complex submissions should involve qualified health economists and regulatory specialists.

## When to Use This Skill

Invoke this skill when:
- Preparing a PBAC (Pharmaceutical Benefits Advisory Committee) submission in Australia.
- Compiling an MSAC (Medical Services Advisory Committee) application for new medical services.
- Developing a PHARMAC funding proposal in New Zealand.
- Creating a NICE (National Institute for Health and Care Excellence) technology appraisal submission.
- Preparing a CADTH (Canadian Agency for Drugs and Technologies in Health) submission.
- Structuring health economic evidence for HTA dossiers.
- Planning submission timelines and milestones for reimbursement decisions.
- Preparing for pre-submission meetings with HTA authorities.
- Compiling evidence packages including clinical, economic, and budget impact analyses.
- Writing responses to HTA evaluation reports or listing recommendations.
- Preparing for HTA committee presentations or expert advisory meetings.
- Understanding jurisdiction-specific evidence requirements and reference cases.
- Compiling patient and clinician input for HTA submissions.
- Addressing comparator selection and standard of care definitions.
- Preparing justification for orphan drug or rare disease designations.
- Planning managed entry agreements or risk-sharing schemes.

## Regulatory Context

### Australia & New Zealand (Default)

| Authority | Scope | Submission Type | Key Requirements |
|-----------|-------|-----------------|------------------|
| **PBAC** | Pharmaceutical reimbursement | Major/Minor submission; Sub-Committee meeting | Section A: Submission body; Section B: Economic analysis; Budget impact model; Pre-meeting recommended |
| **MSAC** | Medical services (MBS) | Application; Protocol Assessment (PASC) | Safety, effectiveness, cost-effectiveness; Assessment vs. Advisory track |
| **PHARMAC** | NZ pharmaceutical funding | Funding proposal (PTAC/PHARMAC) | Nine decision criteria; equity emphasis; cost-effectiveness one factor among many |
| **TGA** | Market authorization | Separate from reimbursement | Safety/efficacy registration; no cost-effectiveness requirement |

### US/EU-lite Fallback

| Authority | Scope | Submission Type | Key Requirements |
|-----------|-------|-----------------|------------------|
| **NICE** (UK) | NHS England & Wales funding | Single/ Multiple Technology Appraisal; Highly Specialised Technologies | Reference case compliance; £20,000-30,000/QALY threshold; Committee evidence review |
| **CADTH** (Canada) | Provincial/territorial funding | Common Drug Review; pan-Canadian Oncology Drug Review | Canadian Agency review; provincial implementation varies |
| **ICER** (US) | Value assessment (non-regulatory) | Evidence report; public meeting | $50,000-150,000/QALY thresholds; contextual considerations |
| **FDA** (US) | Market authorization only | NDA/BLA submission | No cost-effectiveness required for approval; separate from reimbursement |
| **EMA** (EU) | EU market authorization | Marketing Authorization Application | No HTA component; national reimbursement separate |

### Jurisdiction Matrix

| Jurisdiction | Applicable Regulator | Reporting Trigger | Timeframe | Required Artifacts | Escalation Point |
|--------------|---------------------|-------------------|-----------|-------------------|------------------|
| **AU - PBS** | PBAC | New drug listing; price change; restriction change | 17 weeks (clock start to PBAC meeting) | Submission document; Economic model; Budget impact model; Response to delegate comments | PBAC Secretariat; Sponsor Representative |
| **AU - MBS** | MSAC | New MBS item number; service modification | Variable; PASC → Assessment/Advisory → Committee | Application; Protocol; Clinical evidence; Economic evaluation | MSAC Executive Officer |
| **NZ** | PHARMAC | Funding application; renewal | Rolling consideration; priority by clinical need | Proposal document; Clinical and cost-effectiveness; Equity assessment | PTAC Chair; Pharmac Staff |
| **UK** | NICE | Technology appraisal referral from DHSC/NHS England | ~40 weeks (STA); ~90 weeks (MTA) | Submission dossier; Evidence review group critique; Committee papers | NICE Committee Chair; Topic Lead |
| **Canada** | CADTH | Manufacturer submission to CDR | ~180 days | Submission dossier; CDR report; Expert committee recommendation | CADTH Review Officer |

## Quick Reference

1. **Start Early**: Engage HTA authority at pre-submission phase; understand reference case.
2. **Know Your Comparator**: Use current standard of care in jurisdiction; justify selection.
3. **Follow Reference Case**: Adhere to perspective, time horizon, discounting, and outcome requirements.
4. **Include Both Perspectives**: Healthcare sector and societal (PBAC requirement).
5. **Validate Your Model**: Face validity, internal validity, external validation if possible.
6. **Conduct PSA**: Probabilistic sensitivity analysis required for formal submissions.
7. **Provide Budget Impact**: Affordability analysis alongside cost-effectiveness.
8. **Address Uncertainty**: Scenario analyses; threshold analyses; explain key drivers.
9. **Be Transparent**: Provide model files; document assumptions; acknowledge limitations.
10. **Plan for Questions**: Prepare for delegate/clarification questions; response timelines tight.
11. **Patient Input**: Include patient organization perspectives where possible.
12. **Clinical Engagement**: Clinician endorsement strengthens real-world applicability case.
13. **Managed Entry**: Consider risk-sharing if evidence uncertain or budget impact high.
14. **Appeal Rights**: Understand appeal/reconsideration processes if recommendation unfavorable.

## Operating Modes

### Standard Mode
Full HTA submission preparation with comprehensive evidence synthesis, detailed economic modeling following reference case requirements, extensive sensitivity analysis, and formal submission documentation. Includes pre-submission meeting preparation, response to evaluator comments, and committee presentation materials. Use for major reimbursement decisions with significant budget implications.

### Lite Mode
Streamlined guidance for minor submissions, line extensions, or exploratory discussions with HTA authorities. Focuses on essential requirements, key evidence summary, and basic economic analysis. Never suppresses critical reference case requirements. Clearly mark as preliminary and recommend full submission preparation for novel therapies or significant budget impacts.

## Detailed Guidance

### 1. PBAC (Australia) Submission Framework

#### Submission Types

**Major Submissions**:
- New chemical entities (NCEs) not currently listed.
- Significant changes to existing listings (new indications, expanded population).
- Requests for unrestricted benefit status (authority required to unrestricted).

**Minor Submissions**:
- Price reductions (no clinical data required).
- Administrative changes (pack size, formulation).
- Restricted benefit adjustments within existing indication.

#### Section A: Submission Body

**Part I: Summary**:
- Product name, form, strength, sponsor.
- Proposed listing and restrictions.
- Comparator and justification.
- Summary of clinical evidence.
- Summary of economic evaluation.
- Budget impact summary.

**Part II: Product Information**:
- TGA registration details.
- Indication(s) and dosage.
- Place in therapy.

**Part III: Comparator**:
- Current therapy in Australia.
- Justification for comparator selection.
- If no PBS-listed comparator, justify standard medical practice.

**Part IV: Clinical Evidence**:
- Systematic review methodology.
- Included studies (RCTs, observational).
- Efficacy/effectiveness outcomes.
- Safety profile.
- GRADE evidence quality assessment.
- Network meta-analysis if indirect comparisons required.

**Part V: Economic Evaluation**:
- Evaluation type (CUA preferred).
- Model structure (decision tree, Markov, etc.).
- Perspective (healthcare sector + societal).
- Time horizon.
- Discounting (5%).
- Costing methodology.
- Utility values (AQoL/EQ-5D Australian tariffs preferred).
- Base case results (incremental costs, QALYs, ICER).
- Sensitivity analysis (deterministic and probabilistic).

**Part VI: Budget Impact Analysis**:
- Target population estimation.
- Current treatment patterns.
- Uptake assumptions.
- Cost calculations over 4 years.
- Scenario analyses (conservative, optimistic).

**Part VII: Requested Listing**:
- Exact wording for PBS schedule.
- Restriction requirements.
- PBS code requirements.

**Part VIII: Other Information**:
- Patient/carer input.
- Clinician input.
- International pricing and listing status.
- Managed entry/risk-sharing proposals.

#### Section B: Economic Analysis

- Detailed model description.
- Full mathematical specification.
- Parameter tables with sources and uncertainty.
- Cohort trace (Markov models).
- Cost-effectiveness plane.
- CEACs (Cost-Effectiveness Acceptability Curves).
- Scenario analyses.
- Model validation documentation.

#### Supporting Documents

- Technical report (economic evaluation full details).
- Model files (Excel, TreeAge, R).
- Budget impact model.
- Systematic review report.
- Clinical study reports (if requested).

### 2. MSAC (Australia) Application Framework

#### Application Pathways

**Assessment Track** (Full evaluation):
- New MBS items with significant cost or utilization implications.
- Requires comprehensive clinical evidence and economic evaluation.
- MSAC assessment report prepared.
- Committee recommendation for/against funding.

**Advisory Track** (Streamlined):
- Minor modifications to existing items.
- Low-cost/low-volume services.
- Advisory opinion only; no formal assessment report.

#### Application Components

**Section A: Service Details**:
- Service description (items, fees, co-claiming).
- Proposed MBS item descriptors.
- Provider type and qualifications.

**Section B: Clinical Evidence**:
- Safety data (adverse events, complications).
- Effectiveness data (clinical outcomes, diagnostic accuracy).
- Comparative effectiveness vs. current practice.
- Evidence quality (risk of bias assessment).

**Section C: Economic Analysis**:
- Cost-effectiveness vs. comparator.
- Cost-utility analysis preferred where applicable.
- Budget impact on MBS expenditure.
- Resource implications (workforce, infrastructure).

**Section D: Implementation**:
- Volume estimates.
- Workforce capacity.
- Training requirements.
- Safety and quality considerations.

**Section E: Stakeholder Input**:
- Professional colleges/societies.
- Consumer organizations.
- State/territory health departments.

### 3. PHARMAC (New Zealand) Proposal Framework

#### PHARMAC Decision Criteria

PHARMAC uses nine criteria; cost-effectiveness is only one factor:

1. **Health needs of all New Zealanders**: Burden of disease; population impact.
2. **Health needs of particular groups**: Māori, Pacific peoples, vulnerable populations.
3. **Effectiveness**: Clinical benefit; quality of evidence.
4. **Cost**: Acquisition cost; administration costs; monitoring costs.
5. **Cost-effectiveness**: Value for money; opportunity cost.
6. **Budget impact**: Total cost to pharmaceutical budget; year-by-year projection.
7. **Government priorities**: Alignment with health strategy; other ministerial priorities.
8. **Practicality**: Implementation feasibility; workforce capacity.
9. **Consistency**: Equity in access; consistency with other funded treatments.

#### Proposal Structure

**Part 1: Pharmaceutical and Indication**:
- Product details (name, form, strength).
- Proposed indication and target population.
- Current treatment pathway in NZ.

**Part 2: Clinical Evidence**:
- Efficacy and safety data.
- Comparator and relative effectiveness.
- Quality of evidence (risk of bias).

**Part 3: Cost and Cost-Effectiveness**:
- Proposed price and pricing history.
- Cost per patient (annual).
- Cost-effectiveness vs. comparator (ICER).
- Budget impact (3-year projection).

**Part 4: Equity and Access**:
- Impact on health disparities.
- Access for Māori and Pacific populations.
- Consistency with existing funding decisions.

**Part 5: Implementation**:
- Expected utilization.
- Prescriber restrictions (if any).
- Monitoring requirements.
- Risk-sharing proposals (if applicable).

### 4. NICE (UK) Submission Framework

#### Technology Appraisal Types

**Single Technology Appraisal (STA)**:
- One intervention vs. standard care.
- ~40-week timeline.
- Evidence review group (ERG) critique commissioned by NICE.

**Multiple Technology Appraisal (MTA)**:
- Multiple interventions (class review).
- ~90-week timeline.
- More complex evidence synthesis required.

**Highly Specialised Technologies (HST)**:
- For ultra-rare diseases (often enzyme replacement therapies).
- Modified criteria; higher acceptable ICERs (£100,000+/QALY possible).

#### Submission Requirements

**Company Evidence Submission Template**:

**Section A: Decision Problem**:
- Technology description.
- Target population (NICE scope alignment).
- Comparator(s) (NICE specified).
- Perspective (NHS and PSS).

**Section B: Clinical Evidence**:
- Systematic review.
- Direct and indirect evidence.
- Network meta-analysis if applicable.
- Safety data.

**Section C: Cost-Effectiveness Evidence**:
- Model structure and rationale.
- Clinical parameters (efficacy, safety, utilities).
- Cost parameters (drug, administration, monitoring).
- Base case results.
- Sensitivity analysis (PSA required).
- Subgroup analyses (pre-specified only).

**Section D: Budget Impact**:
- Eligible population.
- Current treatment mix.
- Technology uptake assumptions.
- Annual costs over 5 years.

**Section E: Other Considerations**:
- Patient/carer evidence.
- Clinical expert evidence.
- Innovation/specific considerations.
- Equality considerations (protected characteristics).

#### NICE Committee Process

1. **Submission deadline**: Company submission + list price.
2. **ERG critique**: Independent assessment of company submission.
3. **Committee papers**: Combined pack for Committee members.
4. **Committee meeting**: Company and ERG presentations; discussion.
5. **Appraisal consultation document (ACD)**: Draft guidance published.
6. **Consultation**: Stakeholder comments (2 weeks).
7. **Final appraisal document (FAD)**: Final guidance published.
8. **Appeal**: Limited grounds; 15 days post-FAD.

### 5. CADTH (Canada) Submission Framework

#### Common Drug Review (CDR)

**Submission Components**:

**Module 1: Summary**:
- Product and indication.
- Listing request.
- Key findings (clinical and economic).
- Budget impact highlights.

**Module 2: Background**:
- Disease background.
- Current treatment landscape in Canada.
- Unmet needs.

**Module 3: Systematic Review**:
- Search strategy.
- Inclusion/exclusion criteria.
- Study characteristics table.
- Risk of bias assessment.
- Results synthesis.

**Module 4: Economic Evaluation**:
- Evaluation type (CUA standard).
- Model structure.
- Input parameters.
- Base case results.
- Sensitivity analysis.

**Module 5: Budget Impact**:
- Population eligible.
- Uptake assumptions.
- Annual cost projections (3 years).

**Module 6: Other Considerations**:
- Patient input.
- Clinician input.
- Health equity considerations.
- Implementation issues.

#### CADTH Review Process

1. **Submission**: Manufacturer submits to CADTH.
2. **Clinical review**: CADTH clinical team assessment.
3. **Economic review**: CADTH health economist critique.
4. **CADTH report**: Published (non-confidential version).
5. **Committee review**: Canadian Drug Expert Committee (CDEC).
6. **Recommendation**: Recommend, recommend with criteria/conditions, or do not list.
7. **Provincial implementation**: Each province/territory decides on funding.

### 6. Evidence Requirements by Jurisdiction

#### Clinical Evidence Standards

| Jurisdiction | RCT Preference | Observational Data | Real-World Evidence | Network Meta-Analysis |
|--------------|----------------|-------------------|--------------------|----------------------|
| **PBAC** | Gold standard; head-to-head preferred | Accepted if RCTs limited; bias assessment required | Increasingly accepted; must address confounding | Standard for indirect comparisons |
| **MSAC** | Preferred; diagnostic accuracy studies for diagnostics | Safety data often observational | Useful for implementation and safety monitoring | Less common |
| **PHARMAC** | Preferred; pragmatic trials valued | Accepted with caveats | Utility for NZ context and adherence | Used when no head-to-head |
| **NICE** | Required as primary evidence; ITC/Meta-analysis expected | Supplementary only | Not primary basis; may inform subgroups | Required if no direct comparison |
| **CADTH** | Primary evidence; pivotal trials | Safety; long-term outcomes | Supplementary; bias assessment critical | Expected if indirect comparison needed |

#### Economic Evidence Standards

| Element | PBAC | MSAC | PHARMAC | NICE | CADTH |
|---------|------|------|---------|------|-------|
| **Primary Analysis** | CUA (QALYs) | CUA preferred | CUA preferred | CUA (QALYs) | CUA preferred |
| **Perspective** | Healthcare + Societal | Healthcare | Healthcare | NHS + PSS | Public system |
| **Time Horizon** | Lifetime (chronic) | As appropriate | Sufficient duration | Sufficient duration | Lifetime typical |
| **Discounting** | 5% both | 5% both | 5% both | 3.5% (1.5% if >30 years) | 5% both |
| **Utilities** | AQoL, EQ-5D AU | EQ-5D preferred | EQ-5D preferred | EQ-5D-3L UK tariff | Canadian prefs |
| **PSA Required** | Yes | Recommended | Recommended | Yes | Yes |
| **Model Files** | Required | Recommended | Recommended | Required | Required |

### 7. Common Submission Pitfalls

#### Clinical Evidence Pitfalls

**Inadequate Comparator**:
- Pitfall: Comparing to placebo or outdated therapy not used in jurisdiction.
- Solution: Use current standard of care; if multiple comparators, use most relevant.

**Selective Reporting**:
- Pitfall: Only reporting favorable outcomes or subgroup results.
- Solution: Report all pre-specified outcomes; transparent about post-hoc analyses.

**Ignoring Safety**:
- Pitfall: Focusing only on efficacy; inadequate adverse event reporting.
- Solution: Comprehensive safety profile; rare/serious adverse events addressed.

**Poor Quality Evidence**:
- Pitfall: Relying on low-quality observational studies when RCTs available.
- Solution: Systematic review with quality assessment; GRADE methodology.

#### Economic Evidence Pitfalls

**Model Structure Issues**:
- Pitfall: Overly simple or overly complex model for disease.
- Solution: Match model complexity to decision problem; justify structure choices.

**Inappropriate Time Horizon**:
- Pitfall: Too short misses long-term benefits/costs; too long adds unnecessary uncertainty.
- Solution: Lifetime for chronic conditions; justification for horizon choice.

**Ignoring Half-Cycle Correction**:
- Pitfall: Markov models without half-cycle correction overestimate outcomes.
- Solution: Apply half-cycle correction or alternative methods (life-table, tunnel states).

**Double Discounting**:
- Pitfall: Discounting costs but not outcomes (or vice versa).
- Solution: Both at reference rate; sensitivity at 0% or alternative rates.

**Cherry-Picking Utilities**:
- Pitfall: Selecting most favorable utility values without justification.
- Solution: Systematic search for utilities; pre-specify selection criteria; sensitivity analysis.

**Insufficient Uncertainty Analysis**:
- Pitfall: Only deterministic sensitivity; no PSA.
- Solution: PSA mandatory for most submissions; CEACs reported.

**Foreign Data Without Adaptation**:
- Pitfall: Using overseas cost data or utilities without adjustment for jurisdiction.
- Solution: Local cost data; jurisdiction-specific utility tariffs; justify any adaptation.

#### Submission Process Pitfalls

**Late Engagement**:
- Pitfall: First contact with HTA authority at submission deadline.
- Solution: Pre-submission meetings; draft review; clarify reference case.

**Missing Deadline**:
- Pitfall: Late submission misses committee meeting; delays decision by months.
- Solution: Project management; buffer time; early warning if delays expected.

**Poor Response to Questions**:
- Pitfall: Delayed or inadequate response to evaluator clarification questions.
- Solution: Prepare FAQ; rapid response team; anticipate common questions.

**Inadequate Budget Impact**:
- Pitfall: Underestimating uptake or population; affordability shock.
- Solution: Conservative estimates; sensitivity analysis; scenario planning.

**Ignoring Equity**:
- Pitfall: Pure efficiency focus without equity considerations.
- Solution: PHARMAC requires equity; PBAC considers rule of rescue; NICE requires equality considerations.

**Lack of Transparency**:
- Pitfall: Black-box models; undocumented assumptions.
- Solution: Provide model files; technical appendix; clear documentation.

### 8. Pre-Submission Meeting Preparation

#### Objectives
- Clarify reference case interpretation.
- Discuss comparator selection.
- Seek advice on model structure.
- Understand evidence gaps.
- Identify potential issues early.

#### Preparation

**Before the Meeting**:
- Draft submission outline.
- Prepare specific questions (not general advice).
- Summary of clinical evidence.
- Preliminary economic model structure.
- List of uncertainties needing guidance.

**Questions to Ask**:
- Is our proposed comparator appropriate?
- Should we include subgroups? Which ones?
- Are there specific utility sources you prefer?
- How should we handle missing data?
- Is our proposed model structure acceptable?
- Any particular sensitivity analyses required?

**After the Meeting**:
- Document advice received.
- Confirm understanding in writing if significant decisions.
- Note that advice is non-binding; final submission assessed on merits.

### 9. Managed Entry and Risk-Sharing

#### When to Consider

**Evidence Uncertainty**:
- Limited clinical trial data (small populations, short follow-up).
- Uncertain real-world effectiveness.
- Uncertain long-term outcomes.

**Budget Impact Uncertainty**:
- Population size uncertain.
- Uptake difficult to predict.
- Price-volume considerations.

**High Cost/High Uncertainty**:
- Innovative therapies with transformative potential.
- Orphan drugs with limited evidence.
- Cell/gene therapies with long-term unknowns.

#### Types of Agreements

**Financial Agreements**:
- Discounts (confidential net pricing).
- Price caps (maximum expenditure).
- Price-volume agreements (lower price at higher volume).

**Outcome-Based Agreements**:
- Rebates if patient doesn't respond.
- Continuation based on treatment response.
- Warranties (replacement if failure).

**Evidence Development Agreements**:
- Coverage with evidence development (CED).
- Conditional approval with post-marketing studies.
- Registry-based follow-up.

#### HTA Authority Perspectives

**PBAC**: Willing to consider; must reduce uncertainty or budget impact.
**NICE**: Increasingly used; patient access schemes negotiated with NHS England.
**CADTH**: Considered case-by-case; doesn't substitute for poor evidence.

### 10. Patient and Clinician Input

#### Patient Input

**Value**:
- Real-world experience of condition and current treatments.
- Unmet needs perspective.
- Quality of life impact beyond clinical measures.
- Acceptability of proposed treatment.

**Sources**:
- Patient advocacy organizations.
- Individual patient submissions.
- Patient-reported outcome data from trials.
- Qualitative research (interviews, focus groups).

**HTA Use**:
- PBAC: Considered in deliberative framework.
- NICE: Committee considers patient evidence; separate committee for highly specialised technologies.
- PHARMAC: Important for equity criteria (population groups).

#### Clinician Input

**Value**:
- Current practice patterns.
- Standard of care definition.
- Implementation feasibility.
- Safety monitoring requirements.

**Sources**:
- Professional colleges/societies.
- Clinical experts.
- Delphi panels for practice variation.

### 11. Responding to Evaluation Reports

#### Timeline Management

Evaluation reports typically require rapid response:
- PBAC: Delegate comments typically 2-3 weeks before meeting.
- NICE: ACD consultation 2 weeks.
- CADTH: CDR report comments ~2 weeks.

**Response Preparation**:
- Rapid review team identified in advance.
- Template response format prepared.
- Access to original model and data.
- Clear decision-making authority.

#### Response Content

**Factual Corrections**:
- Errors in evidence summary.
- Misinterpretation of data.
- Technical errors in model critique.

**Substantive Responses**:
- Disagreement with comparator assessment.
- Challenge to cost-effectiveness interpretation.
- Additional evidence or analyses.

**Additional Analyses**:
- Post-hoc sensitivity analyses.
- Alternative scenario presentations.
- Additional subgroup analyses (if justified).

#### Hearing Presentation

**Structure**:
- Brief summary (5 minutes typical).
- Address key concerns from evaluation.
- Highlight key benefits and uncertainties.
- Be prepared for questions.

**Preparation**:
- Rehearse timing.
- Prepare backup slides.
- Anticipate questions.
- Have technical experts available.

## Documentation Requirements

### Submission Package Checklist

**Clinical Evidence**:
- [ ] Systematic review protocol and report.
- [ ] PRISMA flow diagram.
- [ ] Study characteristics tables.
- [ ] Risk of bias assessment (ROB-2, ROBINS-I).
- [ ] Forest plots for meta-analyses.
- [ ] GRADE evidence profiles.
- [ ] Clinical study reports (if requested).

**Economic Evidence**:
- [ ] Economic evaluation report following reference case.
- [ ] Model description and structure diagram.
- [ ] Parameter tables with sources and uncertainty.
- [ ] Cohort trace or patient simulation details.
- [ ] Base case results (ICER, incremental costs/effects).
- [ ] Deterministic sensitivity analysis (tornado diagrams).
- [ ] Probabilistic sensitivity analysis (CEACs, scatter plots).
- [ ] Scenario analyses.
- [ ] Model validation documentation.
- [ ] Model files (Excel, TreeAge, R code).

**Budget Impact**:
- [ ] Budget impact model.
- [ ] Target population estimation with sources.
- [ ] Current treatment pattern assumptions.
- [ ] Uptake projections with rationale.
- [ ] Cost calculations (annual, cumulative).
- [ ] Scenario analyses (conservative, optimistic).

**Stakeholder Input**:
- [ ] Patient organization submissions.
- [ ] Clinician/professional society input.
- [ ] Consumer representative perspectives.

**Administrative**:
- [ ] Cover letter with key messages.
- [ ] Submission checklist completed.
- [ ] Pricing information (may be confidential).
- [ ] Proposed listing wording.
- [ ] Product information (TGA/SmPC).

### Supporting Documentation

**Technical Appendix**:
- [ ] Detailed search strategies.
- [ ] Excluded studies list with reasons.
- [ ] Network meta-analysis geometry and consistency checks.
- [ ] Model equations and mathematical specification.
- [ ] Additional sensitivity analyses.
- [ ] Validation details.

**Response to Evaluation**:
- [ ] Point-by-point response document.
- [ ] Revised analyses if applicable.
- [ ] Additional evidence if available.
- [ ] Clarification of misunderstandings.

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **Submitting without pre-submission meeting** | May misunderstand reference case; increased risk of rejection | Engage early; clarify comparator, model structure, evidence requirements |
| **Using foreign cost data** | Costs vary significantly by jurisdiction; reimbursement decisions based on local prices | Use jurisdiction-specific cost data; PBS/MSAC schedule for Australia |
| **Insufficient PSA iterations** | Unstable CEACs; imprecise uncertainty estimates | Minimum 1,000 iterations; 5,000-10,000 for final submission |
| **Post-hoc subgroup analysis** | Inflated Type I error; not pre-specified; cherry-picking | Pre-specify subgroups with clinical rationale; adjust for multiple comparisons |
| **Ignoring societal perspective** | PBAC requires societal perspective analysis; work productivity matters | Include productivity costs; patient transport; carer costs |
| **Wrong discount rate** | Violates reference case; undermines comparability | Use jurisdiction-specific rate (5% AU; 3.5% UK; varies Canada) |
| **No model files provided** | Lack of transparency; inability to verify analyses | Provide Excel/TreeAge/R files; clear documentation |
| **Cherry-picking clinical evidence** | Selective reporting; bias in favor of intervention | Systematic review; all relevant evidence; risk of bias assessment |
| **Underestimating budget impact** | Affordability concerns; unrealistic uptake assumptions | Conservative estimates; sensitivity analysis; market research on likely uptake |
| **Late response to questions** | Misses committee meeting; delays decision by months | Rapid response team; project management; anticipate questions |
| **Ignoring equity considerations** | May fail equity criteria; particularly important for PHARMAC, NICE | Explicit equity analysis; impact on disadvantaged populations; distributional analysis |
| **No half-cycle correction** | Systematic bias in Markov models; incorrect results | Apply half-cycle correction or use appropriate alternative |
| **Poor comparator justification** | HTA authority may reject if comparator inappropriate | Clear rationale for comparator; discussion with authority pre-submission |
| **Missing trial data** | Exclusion of negative trials; publication bias | Comprehensive search; include unpublished data; clinical trial registry checks |

## When to Escalate

Escalate to HTA Specialist, Health Economics Lead, or Regulatory Affairs when:
- Novel intervention without existing HTA precedent.
- ICER significantly exceeds jurisdiction threshold.
- Complex model required (microsimulation, DES, hybrid models).
- Managed entry agreement or risk-sharing being considered.
- Significant equity or rare disease considerations.
- Budget impact exceeds health system capacity.
- Submission deadline at risk.
- Evaluation report contains fundamental disagreements requiring strategic response.
- Appeal or reconsideration being considered.
- International reference pricing implications.
- Multiple submissions to different jurisdictions simultaneously.
- Post-submission significant new evidence emerges.
- Committee requests major additional analyses with short timeline.

## Privacy Considerations

- **PHI Involved**: Minimal - HTA submissions use aggregate clinical trial data and economic models.
- **Data Minimization**: Use published summary data; individual patient data not required for submission.
- **De-identification**: If using patient-level data for economic modeling, ensure complete de-identification.
- **Commercial Confidentiality**: Pricing information may be marked confidential; model structure typically public.
- **Retention**: Retain submission documents and models per regulatory requirements (typically 7+ years).
- **No Persistence**: Do not store patient-level trial data in submission documents.
- **Transparency**: Many HTA authorities publish non-confidential versions of submissions and models.
- **Third-Party Data**: Ensure appropriate data licensing for any proprietary datasets used.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Well-established therapeutic class; clear comparator; robust evidence base | High | Proceed with standard submission preparation; follow reference case |
| New mechanism of action; no direct comparator; network meta-analysis required | Medium | Escalate for statistical support; validate indirect comparisons carefully |
| ICER near or above threshold; requires careful uncertainty analysis | Medium | Escalate to health economist; prepare robust sensitivity analyses |
| Orphan drug or ultra-rare disease; limited evidence | Low | **BLOCKER**: Engage specialist; consider managed entry; equity considerations paramount |
| Budget impact extremely high; affordability concerns | Medium | Escalate for policy discussion; consider risk-sharing or staged implementation |
| Submission deadline approaching; significant documentation incomplete | Low | **BLOCKER**: Escalate immediately; may need to defer to next committee cycle |
| Evaluation report fundamentally disagrees with key assumptions | Medium | Escalate for strategic response; may require revised analyses or additional evidence |
| Multiple jurisdictions with conflicting reference case requirements | Medium | Coordinate submissions; consider separate models or adaptable structure |
| Patient advocacy strongly supports; clinical evidence weak | Medium | Balance equity/access considerations with evidence requirements |
| Major new evidence emerges post-submission | Low | Escalate for strategy; may need to update submission or prepare for reconsideration |

## Tool Requirements

- `~~research literature` (PubMed) - For clinical evidence synthesis.
- `~~health/evidence-synthesis` - For systematic reviews and meta-analyses.
- `~~health/health-econ-eval` - For economic evaluation and decision modeling.
- `~~data/statistical-analysis` - For network meta-analysis and PSA.
- `~~cloud storage` - For submission document collaboration and model storage.
- `~~document collaboration` - For team review and submission assembly.
- `~~project tracker` - For HTA submission timelines and milestone tracking.
- `~~health/clinical-guidelines` - For comparator identification and standard of care.

## Success Indicators

You've applied this skill well when:
- [ ] Submission follows jurisdiction-specific reference case requirements.
- [ ] Comparator represents current standard of care and is justified.
- [ ] Clinical evidence is comprehensive with systematic review methodology.
- [ ] Economic model follows best practice and has been validated.
- [ ] Sensitivity analysis includes both deterministic and probabilistic approaches.
- [ ] Budget impact analysis is realistic with scenario planning.
- [ ] Model files are provided with clear documentation.
- [ ] Pre-submission meeting held and advice incorporated.
- [ ] Patient and clinician input included where appropriate.
- [ ] Response to evaluation questions is timely and thorough.
- [ ] All submission deadlines are met.
- [ ] Equity and distributional considerations addressed.
- [ ] Transparency requirements met; assumptions clearly documented.
- [ ] No PHI or confidential patient data in submission documents.
- [ ] Health economist and regulatory specialists have reviewed complex submissions.

## Related Skills

- `~~health/health-econ-eval` - For economic evaluation methodology and decision modeling.
- `~~health/evidence-synthesis` - For systematic reviews and meta-analyses supporting submissions.
- `~~health/clinical-guidelines` - For identifying comparators and standard of care.
- `~~research/grants` - For research funding applications supporting HTA evidence generation.
- `~~finance/budgeting` - For budget impact analysis preparation.
- `~~document/technical-writing` - For preparing submission documents and reports.
- `~~project/project-management` - For managing HTA submission timelines and cross-functional teams.
