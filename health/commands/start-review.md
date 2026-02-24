---
name: start-review
alias:
  - sr-init
  - review-start
  - begin-review
description: Initiate a systematic review or evidence synthesis project with structured protocol development, search strategy planning, and project setup following PRISMA guidelines.
arguments:
  - name: review_title
    description: "Title of the systematic review or evidence synthesis project."
    required: true
  - name: review_type
    description: "Type of review: systematic-review, scoping-review, rapid-review, evidence-map, umbrella-review, qualitative-synthesis."
    required: true
  - name: research_question
    description: "The primary research question using PICO or PCC framework."
    required: true
  - name: population
    description: "Description of the target population or participants."
    required: true
  - name: intervention_or_concept
    description: "The intervention, exposure, diagnostic test, or concept being studied."
    required: true
  - name: comparison
    description: "The comparator (for systematic reviews) or context (for scoping reviews)."
    required: false
  - name: outcomes
    description: "Primary and secondary outcomes to be measured (for systematic reviews)."
    required: false
  - name: team_lead
    description: "Name or role of the systematic review team lead."
    required: true
  - name: timeline_months
    description: "Estimated project duration in months."
    required: false
---

# Start Systematic Review / Evidence Synthesis

Use this command to initiate a structured systematic review or evidence synthesis project with proper protocol development, PRISMA-compliant methodology, and documentation setup.

## 1. Validate Input

- Ensure `review_type` is one of: systematic-review, scoping-review, rapid-review, evidence-map, umbrella-review, qualitative-synthesis.
- If `review_type` is systematic-review and `outcomes` is not provided, prompt for primary outcomes.
- If `review_type` is scoping-review and `comparison` is not provided, use PCC framework (Population, Concept, Context).
- If `timeline_months` is not provided, default based on review type:
  - systematic-review: 12 months
  - scoping-review: 4 months
  - rapid-review: 2 months
  - evidence-map: 6 months
  - umbrella-review: 6 months
  - qualitative-synthesis: 6 months

## 2. Invoke Appropriate Skill

Use skill based on `review_type`:

### For systematic-review:
Use `~~health/systematic-review` to:
1. Validate PICOS framework completeness.
2. Develop comprehensive search strategy framework.
3. Plan risk of bias assessment approach.
4. Design data extraction templates.
5. Establish GRADE evidence grading framework.

### For scoping-review, rapid-review, evidence-map, umbrella-review, qualitative-synthesis:
Use `~~health/evidence-synthesis` to:
1. Validate review type selection rationale.
2. Develop appropriate methodology for review type.
3. Plan streamlined or comprehensive approach as appropriate.
4. Establish quality assessment approach (if applicable).
5. Design evidence visualization or synthesis plan.

## 3. Generate Structured Output

Produce:

### SYSTEMATIC REVIEW / EVIDENCE SYNTHESIS PROJECT CHARTER

**Project ID**: [Generate unique ID: SR-YYYY-NNN or ES-YYYY-NNN]
**Initiated**: {{current_timestamp}}
**Review Type**: {{review_type}}
**Team Lead**: {{team_lead}}
**Timeline**: {{timeline_months or "default by type"}} months
**Status**: INITIATED

---

## 1. REVIEW OVERVIEW

**Title**: {{review_title}}

**Review Type**: {{review_type}}

**Research Question**: {{research_question}}

### 1.1 Framework

{{#if review_type == "systematic-review"}}
**PICOS Framework**:
- **P**opulation: {{population}}
- **I**ntervention: {{intervention_or_concept}}
- **C**omparison: {{comparison or "Not specified - to be determined"}}
- **O**utcomes: {{outcomes or "To be defined in protocol"}}
- **S**tudy Designs: [To be specified in eligibility criteria]
{{else}}
**PCC Framework** (or appropriate framework for review type):
- **P**opulation: {{population}}
- **C**oncept: {{intervention_or_concept}}
- **C**ontext: {{comparison or "Not specified - to be determined"}}
{{/if}}

---

## 2. PROTOCOL DEVELOPMENT

### 2.1 Protocol Requirements Checklist

- [ ] Background and rationale
- [ ] Research question (structured)
- [ ] Objectives (primary and secondary)
- [ ] Eligibility criteria
  - [ ] Inclusion criteria
  - [ ] Exclusion criteria
- [ ] Information sources
  - [ ] Electronic databases
  - [ ] Trial registries
  - [ ] Grey literature sources
- [ ] Search strategy
  - [ ] Database-specific strategies
  - [ ] Search terms and synonyms
  - [ ] Date limits
- [ ] Study selection process
  - [ ] Screening workflow
  - [ ] Conflict resolution
- [ ] Data extraction
  - [ ] Extraction form design
  - [ ] Pilot testing plan
- [ ] {{#if review_type == "systematic-review"}}Risk of bias assessment
  - [ ] Tool selection (RoB 2 / ROBINS-I)
  - [ ] Assessment process{{/if}}
- [ ] Data synthesis
  - [ ] Narrative synthesis plan
  - [ ] Meta-analysis approach (if applicable)
- [ ] {{#if review_type == "systematic-review"}}Subgroup and sensitivity analyses{{/if}}
- [ ] {{#if review_type == "systematic-review"}}GRADE evidence assessment{{/if}}
- [ ] Ethics and dissemination
- [ ] Timeline and milestones
- [ ] Funding and conflicts of interest

### 2.2 PROSPERO / Registry Registration

{{#if review_type == "systematic-review"}}
**Registration Required**: YES

**Action Items**:
1. Complete protocol document
2. Register at https://www.crd.york.ac.uk/prospero/
3. Obtain registration number before screening begins
4. Update registration if protocol changes

**Key Registration Fields**:
- Review title and question
- Searches (databases, dates, terms)
- Participants/Population
- Intervention(s)/Exposure(s)
- Comparator(s)/Control
- Main outcome(s)
- Risk of bias assessment strategy
- Data synthesis method
{{else}}
**Registration**: Optional but recommended

**Recommended Registries**:
- Open Science Framework (OSF): https://osf.io/
- PROSPERO (if systematic elements included)
- Figshare or institutional repository

**Rationale for Registration**: 
Even for {{review_type}}, registration increases transparency and reduces risk of scope creep.
{{/if}}

---

## 3. SEARCH STRATEGY FRAMEWORK

### 3.1 Database Selection

**Core Databases** (Minimum):
- [ ] MEDLINE (via PubMed or Ovid)
- [ ] Embase
- [ ] Cochrane Central Register of Controlled Trials (CENTRAL)

**Supplementary Databases** (Select based on topic):
- [ ] CINAHL (nursing and allied health)
- [ ] PsycINFO (psychological interventions)
- [ ] Web of Science / Scopus (citation tracking)
- [ ] ClinicalTrials.gov
- [ ] WHO ICTRP

### 3.2 Search Strategy Development

**Concept Combination**:
```
({{population}} terms) AND ({{intervention_or_concept}} terms){{#if outcomes}} AND ({{outcomes}} terms){{/if}}
```

**Search Strategy Elements**:
- [ ] Population terms (MeSH + text words)
- [ ] Intervention/concept terms (MeSH + text words)
- [ ] Outcome terms (if applicable)
- [ ] Study design filters (if applicable)
- [ ] Language limits (specify rationale)
- [ ] Date limits (specify rationale)
- [ ] Animal filter (if human studies only)

**Peer Review**:
- [ ] Consider PRESS checklist peer review of search strategy

---

## 4. STUDY SELECTION PROCESS

### 4.1 Screening Workflow

**Stage 1: Title/Abstract Screening**
- Reviewers: [To assign - minimum 2 independent]
- Approach: Liberal inclusion (include if uncertain)
- Tool: [Covidence / Rayyan / DistillerSR / manual]

**Stage 2: Full-Text Screening**
- Reviewers: [To assign - minimum 2 independent]
- Documentation: Reasons for exclusion
- Conflict resolution: Discussion or third reviewer

### 4.2 PRISMA Flow Diagram

Document the flow:
```
Records identified from databases (n=___)
  ├─ Duplicates removed (n=___)
  └─ Records screened (n=___)
       ├─ Records excluded (n=___)
       └─ Full-text assessed (n=___)
            ├─ Full-text excluded (n=___) [with reasons]
            └─ Studies included (n=___)
                 └─ Studies included in synthesis (n=___)
```

---

## 5. DATA EXTRACTION PLAN

### 5.1 Extraction Categories

**Study Characteristics**:
- Author, year, country
- Study design
- Setting
- Sample size
- Follow-up duration
- Funding source

**Population Characteristics**:
- Age (mean/median, range)
- Gender distribution
- Diagnostic criteria
- Baseline characteristics

{{#if review_type == "systematic-review"}}
**Intervention/Exposure**:
- Description
- Dose/frequency/duration
- Delivery method
- Provider type

**Comparator**:
- Type and details
{{/if}}

**Outcomes**:
- Definition and measurement
- Timepoints
- Results by group
- Effect estimates

### 5.2 Extraction Process

- [ ] Design extraction form
- [ ] Pilot test on 2-3 studies
- [ ] Two independent extractors
- [ ] Resolve discrepancies
- [ ] Contact authors for missing data

---

{{#if review_type == "systematic-review"}}
## 6. RISK OF BIAS ASSESSMENT

### 6.1 Tool Selection

**For Randomized Controlled Trials**:
- Tool: RoB 2 (Revised Cochrane Risk of Bias tool)
- Domains: Randomization, deviations, missing data, measurement, reporting

**For Non-Randomized Studies**:
- Tool: ROBINS-I (Risk Of Bias In Non-randomized Studies of Interventions)
- Domains: Confounding, selection, classification, deviations, missing data, measurement, reporting

### 6.2 Assessment Process

- Two independent assessors
- Resolve disagreements through discussion
- Present results in risk of bias tables
- Consider sensitivity analyses excluding high-risk studies
{{/if}}

---

## 7. DATA SYNTHESIS PLAN

### 7.1 Synthesis Approach

{{#if review_type == "systematic-review"}}
**Narrative Synthesis**: For all included studies

**Meta-Analysis**: If appropriate
- Requirements: Clinical homogeneity, sufficient data
- Effect measures: [To specify based on data type]
- Statistical model: [Fixed-effect vs. random-effects]
- Heterogeneity assessment: I² statistic, visual inspection

**Subgroup Analyses** (Pre-specified):
- [ ] To be defined in protocol

**Sensitivity Analyses**:
- Exclude high risk of bias studies
- Alternative statistical models
- Outlier exclusion

**Publication Bias Assessment** (if ≥10 studies):
- Funnel plot inspection
- Egger's test
{{else}}
**Narrative Synthesis Approach**:
- Group studies by key characteristics
- Tabulate study features and findings
- Identify patterns and themes

{{#if review_type == "evidence-map"}}
**Evidence Visualization**:
- Bubble charts (intervention vs. outcome)
- Gap identification
- Interactive or static display
{{/if}}

{{#if review_type == "umbrella-review"}}
**AMSTAR Assessment**: Quality assessment of included systematic reviews
{{/if}}
{{/if}}

---

{{#if review_type == "systematic-review"}}
## 8. GRADE EVIDENCE ASSESSMENT

### 8.1 Rating Approach

**Evidence Certainty Levels**:
- High: Very confident in effect estimate
- Moderate: Moderately confident
- Low: Limited confidence
- Very Low: Very little confidence

**Downgrade Factors**:
- Risk of bias
- Inconsistency
- Indirectness
- Imprecision
- Publication bias

**Evidence Profile Format**:
- Outcomes table with certainty ratings
- Reasons for downgrading/upgrading
- Summary of findings tables
{{/if}}

---

## 9. PROJECT TIMELINE

| Phase | Activities | Duration | Target Completion |
|-------|-----------|----------|-------------------|
| **Month 1** | Protocol development; PROSPERO registration | 4 weeks | End Month 1 |
| **Month 2** | Search strategy development and execution | 4 weeks | End Month 2 |
| **Month 3** | Title/abstract screening; Full-text retrieval | 4 weeks | End Month 3 |
| **Month 4** | Full-text screening; Data extraction design | 4 weeks | End Month 4 |
| **Month 5** | Data extraction; Risk of bias assessment | 4 weeks | End Month 5 |
| **Month 6** | Data synthesis; Analysis | 4 weeks | End Month 6 |
| **Month 7-8** | GRADE assessment; Draft report | 8 weeks | End Month 8 |
| **Month 9** | Internal review; Revisions | 4 weeks | End Month 9 |
| **Month 10** | External peer review; Revisions | 4 weeks | End Month 10 |
| **Month 11-12** | Finalization; Submission/Publication | 8 weeks | End Month 12 |

*Note: Timeline is indicative for systematic reviews. {{review_type}} may have adjusted timelines.*

---

## 10. TEAM STRUCTURE

| Role | Name/Position | Responsibility |
|------|---------------|----------------|
| **Team Lead** | {{team_lead}} | Overall project coordination; Methodological oversight |
| **Clinical/Content Expert** | [To be assigned] | Clinical expertise; Eligibility decisions |
| **Information Specialist** | [To be assigned] | Search strategy development; Database searching |
| **Reviewers** | [To be assigned] | Study screening; Data extraction (minimum 2) |
| {{#if review_type == "systematic-review"}}| **Biostatistician** | [To be assigned] | Meta-analysis; Statistical consultation |{{/if}} |
| **Project Manager** | [To be assigned] | Timeline tracking; Documentation management |

---

## 11. TOOLS AND RESOURCES

### 11.1 Software and Tools

- **Screening**: [Covidence / Rayyan / DistillerSR / EndNote]
- **Data Extraction**: [Excel / Google Sheets / DistillerSR / REDCap]
- **Risk of Bias**: [Excel templates / Covidence]
- **Analysis**: [RevMan / R / Stata]
- **Reference Management**: [EndNote / Mendeley / Zotero]
- **Writing**: [Word / Google Docs / Overleaf]
- **Collaboration**: [Teams / Slack / Email]

### 11.2 Reporting Guidelines

- **PRISMA 2020**: For systematic reviews
- **PRISMA-ScR**: For scoping reviews
- **ENTREQ**: For qualitative syntheses
- **Appropriate checklist**: For other review types

---

## 12. DOCUMENTATION AND DELIVERABLES

### 12.1 Required Documents

- [ ] Protocol (registered)
- [ ] Search strategies (all databases)
- [ ] PRISMA flow diagram
- [ ] Study characteristics table
- [ ] {{#if review_type == "systematic-review"}}Risk of bias assessment tables{{/if}}
- [ ] Data extraction forms
- [ ] {{#if review_type == "systematic-review"}}Forest plots and meta-analysis results{{/if}}
- [ ] {{#if review_type == "systematic-review"}}GRADE evidence profiles{{/if}}
- [ ] PRISMA checklist
- [ ] Review manuscript/report
- [ ] Funding and COI declarations

### 12.2 File Organization

```
/{{review_title}}/
  ├── 01_Protocol/
  │   └── Protocol_{{review_title}}.docx
  ├── 02_Search/
  │   ├── Search_Strategy_MEDLINE.txt
  │   ├── Search_Strategy_Embase.txt
  │   └── Search_Results/
  ├── 03_Screening/
  │   ├── Title_Abstract_Screening.csv
  │   ├── Full_Text_Screening.csv
  │   └── Excluded_Studies_with_Reasons.csv
  ├── 04_Data_Extraction/
  │   ├── Extraction_Form.xlsx
  │   └── Extracted_Data.xlsx
  ├── 05_Risk_of_Bias/
│   └── RoB_Assessments.xlsx
  ├── 06_Analysis/
│   ├── Analysis_Plan.docx
│   └── Results/
  ├── 07_Reporting/
│   ├── PRISMA_Flow_Diagram.pptx
│   ├── PRISMA_Checklist.docx
│   └── Manuscript/
  └── 08_Admin/
      ├── Team_Contacts.xlsx
      ├── Timeline.mpp
      └── COI_Forms/
```

---

## 13. QUALITY ASSURANCE

### 13.1 Calibration Exercises

- [ ] Pilot screening on sample of 50-100 citations
- [ ] Calculate inter-rater reliability (target kappa ≥0.6)
- [ ] Calibration meeting to resolve disagreements
- [ ] Pilot data extraction on 2-3 studies

### 13.2 Ongoing Quality Checks

- [ ] Weekly team meetings during screening phase
- [ ] Spot-checks on screening decisions (10-20%)
- [ ] Verification of data extraction (10-20%)
- [ ] Second review of risk of bias assessments

---

## 14. REGULATORY AND ETHICAL CONSIDERATIONS

### 14.1 Jurisdiction-Specific Requirements

**Australia**:
- NHMRC standards for research synthesis
- Consider Human Research Ethics Committee (HREC) review if using individual patient data

**New Zealand**:
- Health Research Council standards
- Te Whatu Ora evidence requirements

**International**:
- Cochrane standards (if Cochrane review)
- Institutional requirements

### 14.2 Ethics Considerations

{{#if review_type == "systematic-review"}}
- [ ] Ethics approval required? [Yes/No]
  - Typically not required for aggregate data reviews
  - Required for individual patient data meta-analyses
- [ ] Data sharing agreements (if IPD involved)
{{/if}}
- [ ] Indigenous data sovereignty (if applicable)
- [ ] Patient/public involvement plan

---

## 15. PRIVACY AND DATA MANAGEMENT

### 15.1 Data Management Plan

- [ ] Data storage location (secure, backed-up)
- [ ] Access controls (team members only)
- [ ] Version control for documents
- [ ] Retention schedule (typically 7+ years)
- [ ] Data disposal procedures

### 15.2 Privacy Considerations

- **PHI Involved**: {{#if review_type == "systematic-review"}}Conditional (only if IPD){{else}}No{{/if}}
- **Data Minimization**: Aggregate data only unless IPD justified
- **De-identification**: Ensure all extracted data is de-identified
- **No Persistence**: Do not store PHI in temporary workspaces

---

## 16. NEXT STEPS

### Immediate Actions (Week 1-2)

1. [ ] **Finalize Team**: Confirm all team member assignments and roles
2. [ ] **Kickoff Meeting**: Schedule initial team meeting
3. [ ] **Protocol Drafting**: Begin writing detailed protocol
4. [ ] **Tool Setup**: Set up screening and extraction software
5. [ ] **File Structure**: Create project folder organization

### Short-Term Actions (Month 1)

6. [ ] **Complete Protocol**: Finalize all protocol sections
7. [ ] **Register Protocol**: Submit to PROSPERO or appropriate registry
8. [ ] **Develop Search**: Work with information specialist on strategy
9. [ ] **Design Forms**: Create extraction and assessment forms
10. [ ] **Calibration**: Conduct pilot screening and calibration

### Ongoing Actions

11. [ ] **Execute Search**: Run database searches
12. [ ] **Screen Studies**: Title/abstract and full-text screening
13. [ ] **Extract Data**: Systematic data extraction
14. [ ] **Assess Quality**: Risk of bias assessment
15. [ ] **Synthesize Evidence**: Analysis and synthesis
16. [ ] **Write Report**: Manuscript preparation

---

## 17. RISK REGISTER

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Insufficient studies identified | Medium | High | Broaden search; extend date limits; contact experts |
| High heterogeneity precluding meta-analysis | Medium | High | Plan narrative synthesis; explore subgroups |
| Team member unavailable | Medium | Medium | Cross-training; backup assignments |
| Timeline delays | Medium | Medium | Buffer time built in; regular milestone reviews |
| New evidence published during review | Low | Medium | Document search date; plan update strategy |
| Funding constraints | Low | High | Seek institutional support; adjust scope if needed |

---

## 4. Execute Routing

- Save charter to `~~cloud storage` in systematic review project folder.
- Create project tracker entry in `~~project tracker` with milestones.
- Notify {{team_lead}} of project initiation.
- Schedule kickoff meeting within 1 week.
- Set up screening software account and invite team members.

## 5. Output Guardrails

- **No PHI**: Do not include patient identifiers in any documentation.
- **Protocol Registration**: Emphasize importance of PROSPERO registration before screening begins.
- **Dual Review**: Ensure minimum dual independent review for screening and extraction.
- **Transparency**: All methodological choices must be documented and justified.
- **Lite Mode**: If user requests rapid start, generate minimal charter with core elements (question, search framework, team, timeline) and flag for protocol completion.

---

**Note**: This charter establishes the foundation for rigorous evidence synthesis. Update with specific details as the project progresses. Ensure all team members understand and commit to the methodology before proceeding.
