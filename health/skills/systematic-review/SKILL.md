---
name: health/systematic-review
description: This skill should be used when conducting systematic reviews of healthcare literature following PRISMA guidelines. Use for protocol development, search strategy design, study screening, data extraction, risk of bias assessment, meta-analysis planning, and GRADE evidence grading. Invoke when users mention systematic reviews, literature reviews, PRISMA, PROSPERO registration, search strategies, or evidence synthesis.
version: 1.0.0
---

# Systematic Review

A comprehensive framework for conducting systematic reviews of healthcare literature following PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) guidelines. This skill guides researchers through the complete systematic review lifecycle from protocol development to evidence grading.

**Important**: This skill assists with systematic review methodology but does not replace expert clinical judgment, statistical expertise for meta-analysis, or ethics committee oversight. Always ensure appropriate methodological expertise is involved.

## When to Use This Skill

Invoke this skill when:
- Planning or conducting a systematic review of healthcare interventions, diagnostics, or prognostic factors.
- Developing a systematic review protocol for PROSPERO or similar registry registration.
- Designing search strategies for electronic databases (PubMed, Cochrane, Embase).
- Screening and selecting studies using PRISMA methodology.
- Extracting data from primary studies for synthesis.
- Assessing risk of bias using RoB 2, ROBINS-I, or other validated tools.
- Planning or conducting meta-analysis of study results.
- Grading evidence quality using GRADE methodology.
- Preparing PRISMA-compliant review reports for publication.
- Conducting updates to existing systematic reviews.
- Responding to peer review feedback on systematic review manuscripts.

## Regulatory Context

### Australia & New Zealand (Default)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **NHMRC Standards** (AU) | Research synthesis | Standards for Synthesis and Translation of Research Evidence (2016) |
| **NH&MRC Act 1992** (AU) | Health advice | Evidence review requirements for clinical practice guidelines |
| **Health Research Council NZ** | Research standards | Systematic review standards for funding applications |
| **Te Whatu Ora** (NZ) | Health evidence | Requirements for evidence reviews informing policy |
| **State/Territory Health Acts** | Local requirements | Ethics approval for systematic reviews using patient-level data |

### US/EU-lite Fallback

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **IOM Standards** (US) | Systematic reviews | Finding What Works in Health Care: Standards for Systematic Reviews (2011) |
| **AHRQ Methods Guide** (US) | Comparative effectiveness | Systematic review methodology for CERs |
| **EUnetHTA Guidelines** (EU) | Health technology assessment | HTA-specific systematic review guidance |
| **Cochrane Handbook** | International | Methodological standards for systematic reviews |

### Jurisdiction Matrix

| Jurisdiction | Applicable Regulator | Reporting Trigger | Timeframe | Required Artifacts | Escalation Point |
|--------------|---------------------|-------------------|-----------|-------------------|------------------|
| **AU - National** | NHMRC | Clinical guideline development | Per guideline cycle | Systematic review report; GRADE tables; Evidence profiles | Guidelines Committee Chair |
| **AU - Research** | University HREC | Patient-level data meta-analysis | Ethics approval timeline | Ethics application; Data management plan | Research Office |
| **NZ - National** | Health Research Council | Funding application evidence review | Per grant round | Protocol; Search strategy; PRISMA flow diagram | Grant Manager |
| **US** | AHRQ/IOM | Comparative effectiveness review | Project timeline | Technical brief; Systematic review report | Project Officer |
| **International** | Cochrane Collaboration | Cochrane Review publication | Review cycle | Protocol; Review; Plain language summary | Cochrane Review Group |

## Quick Reference

1. **Protocol First**: Register on PROSPERO or similar before starting the review.
2. **PICOS Framework**: Define Population, Intervention, Comparison, Outcomes, Study designs clearly.
3. **Comprehensive Search**: Search multiple databases with documented strategy; include grey literature.
4. **Dual Review**: Two independent reviewers for screening and data extraction; resolve conflicts.
5. **Risk of Bias**: Use validated tools (RoB 2 for RCTs, ROBINS-I for observational studies).
6. **GRADE Assessment**: Rate certainty of evidence for each outcome (High/Moderate/Low/Very Low).
7. **PRISMA Reporting**: Follow PRISMA 2020 checklist for transparent reporting.
8. **Data Synthesis**: Meta-analysis only when appropriate (clinical homogeneity, low heterogeneity).
9. **Sensitivity Analyses**: Test robustness of findings to methodological choices.
10. **Publication Bias**: Assess funnel plot asymmetry when sufficient studies available (≥10).

## Operating Modes

### Standard Mode
Full systematic review methodology with comprehensive search strategies, dual independent review, detailed risk of bias assessment, meta-analysis with subgroup and sensitivity analyses, and complete GRADE evidence profiles. Use for publication-grade systematic reviews intended for peer-reviewed journals or clinical guideline development.

### Lite Mode
Streamlined guidance for rapid reviews or scoping reviews with abbreviated search strategies, single-reviewer screening with verification sampling, simplified data extraction, and narrative synthesis without meta-analysis. Clearly mark outputs as "rapid review" or "scoping review" and acknowledge methodological limitations. Never suppress critical appraisal or risk of bias assessment entirely.

## Detailed Guidance

### 1. Protocol Development

Every systematic review must begin with a written protocol registered before screening begins.

#### 1.1 PICOS Framework

Define each element precisely:

| Element | Definition | Example |
|---------|------------|---------|
| **P**opulation | Who are the participants? | Adults with type 2 diabetes |
| **I**ntervention | What is the intervention? | Continuous glucose monitoring |
| **C**omparison | What is the comparator? | Self-monitoring of blood glucose |
| **O**utcomes | What outcomes are measured? | HbA1c; hypoglycemic events; quality of life |
| **S**tudy designs | What study types are included? | RCTs; systematic reviews |

**Key Questions**:
- Is the PICOS specific enough to guide search strategy development?
- Are all relevant outcomes included (primary and secondary)?
- Are subgroups for analysis predefined (e.g., age, disease severity)?

#### 1.2 Eligibility Criteria

**Inclusion Criteria**:
- Study designs: Be specific (e.g., "RCTs with parallel design"; "prospective cohort studies")
- Population characteristics: Age range, diagnosis criteria, setting
- Intervention details: Dose, duration, delivery method
- Outcomes: Minimum follow-up, measurement methods
- Language: English-only vs. no language restriction
- Publication timeframe: Date limits with rationale

**Exclusion Criteria**:
- Study designs to exclude (e.g., case reports, editorials)
- Population exclusions (e.g., children, pregnant women)
- Intervention exclusions (e.g., non-standard formulations)
- Setting exclusions (e.g., laboratory studies, animal studies)

#### 1.3 PROSPERO Registration

Register protocol before screening begins:

**Required Information**:
- Review title
- Review question (structured using PICOS or PICO)
- Searches (databases, dates, search terms)
- Condition or domain being studied
- Participants/population
- Intervention(s)/exposure(s)
- Comparator(s)/control
- Main outcome(s)
- Risk of bias assessment strategy
- Strategy for data synthesis

**Registration URL**: https://www.crd.york.ac.uk/prospero/

### 2. Search Strategy Development

#### 2.1 Database Selection

**Core Databases** (minimum):
- MEDLINE (via PubMed or Ovid)
- Embase
- Cochrane Central Register of Controlled Trials (CENTRAL)

**Supplementary Databases**:
- CINAHL (nursing and allied health)
- PsycINFO (psychological interventions)
- Web of Science or Scopus (citation tracking)
- ClinicalTrials.gov (ongoing/unpublished trials)
- WHO ICTRP (international trial registry)

#### 2.2 Search Strategy Structure

**Concept Combination**:
```
(Population terms) AND (Intervention terms) AND (Outcome terms)
```

**Example Search (PubMed)**:
```
#1 "Diabetes Mellitus, Type 2"[Mesh] OR "type 2 diabetes"[tiab] OR T2DM[tiab]
#2 "Blood Glucose Self-Monitoring"[Mesh] OR "continuous glucose monitoring"[tiab] OR CGM[tiab]
#3 "Hemoglobin A, Glycosylated"[Mesh] OR HbA1c[tiab] OR "glycemic control"[tiab]
#4 #1 AND #2 AND #3
#5 Randomized Controlled Trial[pt] OR "randomized"[tiab] OR "placebo"[tiab]
#6 #4 AND #5
#7 Animals[mh] NOT Humans[mh]
#8 #6 NOT #7
```

**Peer Review**: Consider using PRESS (Peer Review of Electronic Search Strategies) checklist.

#### 2.3 Grey Literature and Supplementary Searching

**Grey Literature Sources**:
- Dissertations and theses (ProQuest, OpenGrey)
- Conference abstracts (Embase conference abstracts)
- Government reports
- Pharmaceutical company trial registries
- Regulatory submissions (FDA, EMA)

**Supplementary Methods**:
- Citation searching (forward and backward)
- Author contacts for unpublished data
- Hand-searching key journals
- Contacting experts in the field

### 3. Study Screening and Selection

#### 3.1 PRISMA Flow Diagram

Document screening process:

```
Records identified from databases (n=X)
  ├─ Duplicates removed (n=Y)
  └─ Records screened (n=X-Y)
       ├─ Records excluded (n=Z)
       └─ Full-text assessed (n=A)
            ├─ Full-text excluded (n=B) [with reasons]
            └─ Studies included (n=C)
```

#### 3.2 Screening Process

**Title/Abstract Screening**:
- Two independent reviewers
- Liberal inclusion (when in doubt, include)
- Document exclusion reasons at full-text stage
- Use systematic review software (Covidence, Rayyan, DistillerSR)

**Full-Text Screening**:
- Two independent reviewers
- Document reasons for exclusion
- Resolve conflicts through discussion or third reviewer
- Calculate inter-rater reliability (Cohen's kappa target: ≥0.6)

**Conflict Resolution**:
- Primary: Discussion between reviewers
- Secondary: Third reviewer adjudication
- Document resolution method

### 4. Data Extraction

#### 4.1 Data Extraction Template

**Study Characteristics**:
- Author, year, country
- Study design
- Setting (hospital, community, etc.)
- Sample size (enrolled, analyzed)
- Follow-up duration
- Funding source

**Population Characteristics**:
- Age (mean/median, range)
- Gender distribution
- Diagnostic criteria
- Disease severity/stage
- Comorbidities
- Baseline characteristics

**Intervention Details**:
- Intervention name/description
- Dose/frequency
- Duration
- Delivery method
- Provider type
- Co-interventions

**Comparator Details**:
- Type (placebo, active control, usual care)
- Details matching intervention section

**Outcomes**:
- Definition and measurement method
- Timepoint(s) measured
- Results (mean, SD, n for each group)
- Effect estimates (RR, OR, MD with 95% CI)

#### 4.2 Data Extraction Process

- Two independent extractors
- Pilot test extraction form on 2-3 studies
- Resolve discrepancies through discussion
- Contact authors for missing data

### 5. Risk of Bias Assessment

#### 5.1 RoB 2 (Randomized Trials)

Five domains assessed as Low, Some Concerns, or High risk:

| Domain | Key Questions |
|--------|---------------|
| **D1: Randomization Process** | Was allocation sequence random? Was allocation concealed? |
| **D2: Deviations from Intended Interventions** | Were participants aware of assignment? Were care providers aware? |
| **D3: Missing Outcome Data** | Were outcome data available for all participants? |
| **D4: Outcome Measurement** | Were outcome assessors aware of assignment? |
| **D5: Selection of Reported Results** | Were multiple outcomes/analyses reported? |

**Overall Risk of Bias**: Lowest rating across domains (conservative approach).

#### 5.2 ROBINS-I (Non-Randomized Studies)

Seven domains assessed as Low, Moderate, Serious, Critical risk:

| Domain | Key Considerations |
|--------|-------------------|
| **D1: Confounding** | Baseline differences, prognostic factors |
| **D2: Selection of Participants** | Selection into study based on characteristics |
| **D3: Classification of Interventions** | Measurement/definition of intervention |
| **D4: Deviations from Intended Interventions** | Adherence, co-interventions |
| **D5: Missing Data** | Attrition, loss to follow-up |
| **D6: Measurement of Outcomes** | Blinding, objective vs. subjective |
| **D7: Selection of Reported Results** | Multiple outcomes, analyses |

#### 5.3 Assessment Process

- Two independent assessors
- Resolve disagreements through discussion
- Present results in risk of bias tables
- Consider sensitivity analyses excluding high-risk studies

### 6. Data Synthesis

#### 6.1 Narrative Synthesis

**When to Use**:
- Heterogeneous studies (clinical or methodological)
- Insufficient studies for meta-analysis
- Qualitative data synthesis

**Approach**:
- Group studies by intervention type, population, or outcome
- Tabulate study characteristics and results
- Describe direction and magnitude of effects
- Note patterns and inconsistencies

#### 6.2 Meta-Analysis

**Requirements**:
- Clinical homogeneity (similar populations, interventions, outcomes)
- Sufficient data for pooling (effect estimates with SE/CI)

**Statistical Methods**:

| Data Type | Effect Measure | Method |
|-----------|----------------|--------|
| Dichotomous | Risk Ratio (RR), Odds Ratio (OR) | Mantel-Haenszel or Inverse Variance |
| Continuous (same scale) | Mean Difference (MD) | Inverse Variance |
| Continuous (different scales) | Standardized MD (SMD) | Inverse Variance |
| Time-to-event | Hazard Ratio (HR) | Generic Inverse Variance |

**Heterogeneity Assessment**:
- Cochran's Q test (p < 0.10 suggests heterogeneity)
- I² statistic: 0-40% (low), 30-60% (moderate), 50-90% (substantial), 75-100% (considerable)
- Visual inspection of forest plots

**Model Selection**:
- Fixed-effect: When clinical/methodological homogeneity assumed
- Random-effects: When heterogeneity expected (DerSimonian-Laird or Restricted Maximum Likelihood)

#### 6.3 Subgroup and Sensitivity Analyses

**Pre-specified Subgroups**:
- Age groups
- Disease severity
- Intervention dose/intensity
- Study design
- Risk of bias level

**Sensitivity Analyses**:
- Exclude high risk of bias studies
- Exclude outlying studies
- Alternative statistical models
- Impute missing data (best/worst case scenarios)

#### 6.4 Assessment of Publication Bias

**Methods** (when ≥10 studies):
- Funnel plot visual inspection
- Egger's test (regression-based)
- Trim-and-fill analysis

**Interpretation**:
- Asymmetry may indicate publication bias or true heterogeneity
- Consider other causes: small-study effects, true differences

### 7. GRADE Evidence Assessment

#### 7.1 Rating Evidence Certainty

**Four Levels**:

| Level | Interpretation |
|-------|----------------|
| **High** | Very confident effect estimate is close to true effect |
| **Moderate** | Moderately confident; true effect likely close to estimate |
| **Low** | Limited confidence; true effect may be substantially different |
| **Very Low** | Very little confidence; true effect likely substantially different |

**Downgrade Factors** (RCTs):

| Factor | Criteria | Impact |
|--------|----------|--------|
| **Risk of Bias** | Most studies have methodological limitations | -1 or -2 levels |
| **Inconsistency** | Heterogeneity not explained (I² > 50%, inconsistent directions) | -1 or -2 levels |
| **Indirectness** | Differences between PICOS and evidence | -1 or -2 levels |
| **Imprecision** | Wide confidence intervals, few events, small sample | -1 or -2 levels |
| **Publication Bias** | Funnel plot asymmetry or missing studies suspected | -1 level |

**Upgrade Factors** (Observational Studies):
- Large magnitude of effect (RR > 2 or RR < 0.5)
- Dose-response gradient
- Plausible confounders would reduce demonstrated effect

#### 7.2 Evidence Profile Format

| Outcome | Studies (n) | Risk of Bias | Inconsistency | Indirectness | Imprecision | Publication Bias | Certainty | Comments |
|---------|-------------|--------------|---------------|--------------|-------------|------------------|-----------|----------|
| HbA1c reduction | 12 RCTs | No serious concerns | No serious inconsistency | No serious indirectness | No serious imprecision | Undetected | ⊕⊕⊕⊕ HIGH | Consistent benefit across studies |

## Documentation Requirements

### Systematic Review File

- [ ] Registered protocol (PROSPERO or other registry)
- [ ] Search strategies for all databases (including dates)
- [ ] PRISMA 2020 flow diagram
- [ ] Characteristics of included studies table
- [ ] Risk of bias assessment tables
- [ ] Data extraction forms/templates
- [ ] Forest plots and meta-analysis results
- [ ] GRADE evidence profiles
- [ ] PRISMA 2020 checklist
- [ ] Funding and conflict of interest declarations

### Protocol Requirements

- [ ] Rationale for review
- [ ] Objectives (structured using PICOS)
- [ ] Eligibility criteria
- [ ] Information sources and search strategy
- [ ] Study selection process
- [ ] Data extraction procedures
- [ ] Risk of bias assessment tools
- [ ] Data synthesis methods
- [ ] Subgroup and sensitivity analysis plans
- [ ] Timeline and milestones

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **No protocol registration** | Risk of outcome switching and selective reporting | Register on PROSPERO before screening begins |
| **Vague PICOS** | Unfocused search and heterogeneous studies | Define precise eligibility criteria with operational definitions |
| **Single database search** | Misses relevant studies; publication bias | Search minimum 3 databases plus grey literature |
| **No dual review** | Introduces selection and extraction bias | Two independent reviewers at all stages with conflict resolution |
| **Ignoring risk of bias** | Includes poor-quality studies that distort results | Systematically assess and report risk of bias; consider sensitivity analyses |
| **Clinical heterogeneity ignored** | Pooling apples and oranges | Only meta-analyze clinically homogeneous studies; use narrative synthesis otherwise |
| **Subgroup analyses not pre-specified** | Data dredging and false positives | Pre-specify subgroups in protocol; limit post-hoc analyses |
| **Missing grey literature** | Publication bias toward positive results | Search trial registries, conference abstracts, regulatory submissions |
| **GRADE not applied** | Uncertainty about evidence quality not transparent | Apply GRADE to all outcomes; report certainty ratings |
| **No sensitivity analyses** | Fragile findings not detected | Test robustness to methodological choices and outlying studies |

## When to Escalate

Escalate to Systematic Review Team Lead, Methodologist, or Biostatistician when:
- Network meta-analysis is being considered (requires specialized expertise).
- Individual participant data (IPD) meta-analysis is proposed.
- Significant heterogeneity (I² > 75%) cannot be explained by subgroup analyses.
- Risk of bias assessment reveals widespread methodological concerns across included studies.
- Publication bias assessment suggests major distortion of evidence base.
- Meta-analysis includes fewer than 5 studies (fragile findings).
- Results will inform clinical guideline recommendations or policy decisions.
- Study involves controversial or emotionally charged interventions (e.g., stem cells, unproven therapies).
- Conflicts of interest cannot be adequately managed.

## Privacy Considerations

- **PHI Involved**: Conditional - Patient-level data meta-analysis may involve PHI.
- **Data Minimization**: Extract only aggregate data when possible; avoid patient-level data unless IPD meta-analysis is justified.
- **De-identification**: All extracted data should be aggregate; no patient identifiers in extraction forms.
- **Access Controls**: Limit access to data extraction files to review team members.
- **Retention**: Retain systematic review files according to institutional policy (typically 7+ years).
- **No Persistence**: Do not store patient-level data in temporary workspaces or chat history.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Protocol registered; established review methods; experienced review team | High | Proceed with systematic review; document methodology |
| Novel intervention with limited studies; unclear risk of bias patterns | Medium | Consult with methodologist; consider broader eligibility criteria; plan sensitivity analyses |
| Highly heterogeneous studies; conflicting results across studies | Medium | Flag for clinical expert review; explore heterogeneity sources; consider not pooling |
| Individual patient data meta-analysis proposed | Low | Escalate to biostatistician and ethics committee; ensure data sharing agreements |
| Network meta-analysis considered | Low | Escalate to specialized methodologist; assess transitivity assumption carefully |
| Evidence will inform high-stakes clinical guideline | Medium | Ensure complete GRADE assessment; involve guideline panel early; document certainty |
| Rapid review timeline compromises dual review | Medium | Acknowledge limitation; use verification sampling; document quality control |

## Tool Requirements

- `~~research literature` - For PubMed, Embase, Cochrane database searches
- `~~clinical terminology` - For SNOMED-CT, LOINC terminology alignment
- `~~project tracker` - For systematic review project management and milestone tracking
- `~~cloud storage` - For review documentation, extraction forms, and data files
- `~~document collaboration` - For team coordination on screening and extraction
- `~~statistical analysis` - For meta-analysis and forest plot generation
- `~~reference manager` - For citation management and deduplication

## Success Indicators

You've applied this skill well when:
- [ ] Protocol is registered before screening begins
- [ ] PICOS framework clearly defines scope
- [ ] Search strategy is comprehensive and documented
- [ ] PRISMA flow diagram accurately reflects screening process
- [ ] Two independent reviewers conducted screening and extraction
- [ ] Risk of bias is systematically assessed using validated tools
- [ ] Data synthesis is appropriate for study heterogeneity
- [ ] GRADE evidence profiles are complete for all outcomes
- [ ] PRISMA 2020 checklist is completed for reporting
- [ ] Limitations are transparently acknowledged
- [ ] Results are contextualized for clinical decision-making

## Related Skills

- `~~health/evidence-synthesis` - For broader evidence synthesis methods including scoping and rapid reviews
- `~~health/quality-improvement` - When systematic review findings inform QI initiatives
- `~~health/guideline-development` - When systematic review evidence supports clinical guideline development
- `~~research/statistical-analysis` - For advanced meta-analysis methods and statistical support
- `~~research/literature-search` - For database-specific search strategy optimization

## References

- Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ. 2021;372:n71.
- Higgins JPT, Thomas J, Chandler J, et al. Cochrane Handbook for Systematic Reviews of Interventions version 6.3. Cochrane, 2022.
- Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. BMJ. 2019;366:l4898.
- Sterne JA, Hernán MA, Reeves BC, et al. ROBINS-I: a tool for assessing risk of bias in non-randomised studies of interventions. BMJ. 2016;355:i4919.
- Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. BMJ. 2008;336(7650):924-926.
