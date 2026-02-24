---
name: prepare-manuscript
alias:
  - manuscript
  - submit-paper
description: Initiate manuscript preparation for journal submission with structured planning, reporting guideline compliance, and submission readiness framework.
arguments:
  - name: study_type
    description: "Type of study (RCT, observational, systematic_review, case_report, QI, economic_evaluation, protocol)."
    required: true
  - name: target_journal
    description: "Name of target journal for submission."
    required: true
  - name: manuscript_title
    description: "Working title of the manuscript."
    required: true
  - name: first_author
    description: "Name of first author."
    required: true
  - name: senior_author
    description: "Name of senior/corresponding author."
    required: true
  - name: study_registered
    description: "Is the study registered? (yes/no/na)."
    required: false
  - name: ethics_approved
    description: "Does the study have ethics approval? (yes/no/na)."
    required: false
  - name: mode
    description: "Operating mode: 'standard' (full) or 'lite' (streamlined)."
    required: false
---

# Prepare Manuscript Command

Use this command to initiate structured manuscript preparation with appropriate reporting guideline compliance, journal-specific formatting requirements, and submission readiness verification.

## 1. Validate Input

### Study Type Validation

Acceptable study types:
- `RCT` or `randomized_trial` → CONSORT 2010
- `observational` or `cohort` or `case_control` → STROBE
- `systematic_review` or `meta_analysis` → PRISMA 2020
- `case_report` → CARE Guidelines
- `QI` or `quality_improvement` → SQUIRE 2.0
- `economic_evaluation` or `cost_effectiveness` → CHEERS 2022
- `protocol` → SPIRIT 2013
- `diagnostic_accuracy` → STARD 2015
- `qualitative` → SRQR or COREQ

If `study_type` does not match above, prompt user to select from list.

### Journal Validation

- Verify `target_journal` is a recognized peer-reviewed journal.
- If ambiguous, provide matching options.
- Note: Journal selection affects structure template and reference style.

### Mode Selection

- If `mode` not specified, default to `standard`.
- `lite`: Streamlined checklist (essential items only).
- `standard`: Full compliance workflow.

### Ethics and Registration Checks

- If `study_type` is `RCT` and `study_registered` is `no`, flag as critical issue.
- If `study_type` involves human subjects and `ethics_approved` is `no`, flag as critical issue.

## 2. Map Study Type to Reporting Checklist

| Study Type | Checklist | Items | Key Requirements |
|------------|-----------|-------|------------------|
| RCT | CONSORT 2010 | 25 | Flow diagram; trial registration |
| Observational | STROBE | 22 | Cohort/cross-sectional extensions |
| Systematic Review | PRISMA 2020 | 27 | Flow diagram; registration |
| Case Report | CARE | 13 | Timeline; patient perspective |
| QI Study | SQUIRE | 18 | Context; improvement framework |
| Economic Evaluation | CHEERS | 28 | Perspective; time horizon |
| Protocol | SPIRIT | 33 | Trial registration; ethics |
| Diagnostic | STARD | 30 | Flow diagram; accuracy metrics |

## 3. Generate Manuscript Checklist

### STUDY TYPE: {{study_type}}
### TARGET JOURNAL: {{target_journal}}
### MANUSCRIPT: {{manuscript_title}}

---

## PREPARATION CHECKLIST

### A. Study Registration & Ethics (CRITICAL)

- [ ] **Trial Registration**: {{study_registered or "VERIFY"}}
  - Registry: ___________________
  - Number: ___________________
  - Date Registered: ____________
  {% if study_type in ['RCT', 'protocol'] and study_registered == 'no' %}
  ⚠️ **CRITICAL**: Clinical trials must be registered before first patient enrollment per ICMJE.
  {% endif %}

- [ ] **Ethics Approval**: {{ethics_approved or "VERIFY"}}
  - Ethics Committee: ___________
  - Approval Number: ___________
  - Date Approved: _____________
  {% if ethics_approved == 'no' %}
  ⚠️ **CRITICAL**: Human subjects research requires documented ethics approval.
  {% endif %}

### B. Reporting Guideline Compliance

Based on {{study_type}} → **[CHECKLIST NAME]**

Download the checklist from EQUATOR Network: https://www.equator-network.org/

**Core Items to Address**:

{% if study_type == 'RCT' %}
#### CONSORT 2010 Key Items
- [ ] Background and objectives (Item 2a, 2b)
- [ ] Trial design (Item 3a, 3b)
- [ ] Participants: eligibility, settings (Item 4a, 4b)
- [ ] Interventions: precise details (Item 5)
- [ ] Outcomes: definitions, time points (Item 6a, 6b)
- [ ] Sample size: calculation, assumptions (Item 7a, 7b)
- [ ] Randomization: sequence generation (Item 8a)
- [ ] Randomization: allocation concealment (Item 9)
- [ ] Blinding: masking procedures (Item 11a, 11b)
- [ ] Statistical methods (Item 12a, 12b)
- [ ] Participant flow diagram (Item 13a)
- [ ] Recruitment: dates, periods (Item 14a)
- [ ] Baseline data: demographics (Item 15)
- [ ] Numbers analyzed: intention-to-treat (Item 16)
- [ ] Outcomes and estimation (Item 17a, 17b)
- [ ] Ancillary analyses: subgroups (Item 18)
- [ ] Harms: adverse events (Item 19)
- [ ] Limitations: sources of bias (Item 20)
- [ ] Generalizability (Item 21)
- [ ] Interpretation: benefits vs harms (Item 22)
- [ ] Registration: number, registry (Item 23)
- [ ] Protocol: where accessible (Item 24)
- [ ] Funding: sources, role (Item 25)
{% endif %}

{% if study_type == 'observational' %}
#### STROBE Key Items
- [ ] Title/abstract: design indication (Item 1)
- [ ] Background/rationale (Item 2)
- [ ] Objectives: hypotheses (Item 3)
- [ ] Study design (Item 4)
- [ ] Setting: location, time (Item 5)
- [ ] Participants: eligibility (Item 6)
- [ ] Variables: exposures, outcomes (Item 7)
- [ ] Data sources/measurement (Item 8)
- [ ] Bias: methods to address (Item 9)
- [ ] Study size: how determined (Item 10)
- [ ] Quantitative variables (Item 11)
- [ ] Statistical methods (Item 12a, 12b, 12c)
- [ ] Participants: numbers, reasons (Item 13a, 13b, 13c)
- [ ] Descriptive data: characteristics (Item 14)
- [ ] Outcome data (Item 15)
- [ ] Main results: estimates, CI (Item 16)
- [ ] Other analyses: subgroups (Item 17)
- [ ] Key results: summary (Item 18)
- [ ] Limitations: bias, imprecision (Item 19)
- [ ] Interpretation: generalizability (Item 20)
- [ ] Generalizability: external validity (Item 21)
- [ ] Funding: sources (Item 22)
{% endif %}

{% if study_type == 'systematic_review' %}
#### PRISMA 2020 Key Items
- [ ] Title: identify as review (Item 1)
- [ ] Abstract: structured (Item 2)
- [ ] Rationale: context (Item 3)
- [ ] Objectives: PICO/PECO (Item 4)
- [ ] Eligibility criteria (Item 5)
- [ ] Information sources (Item 6)
- [ ] Search strategy (Item 7)
- [ ] Selection process (Item 8)
- [ ] Data collection (Item 9)
- [ ] Data items (Item 10)
- [ ] Risk of bias (Item 11)
- [ ] Effect measures (Item 12)
- [ ] Synthesis methods (Item 13)
- [ ] Certainty assessment (Item 14)
- [ ] Study selection: results (Item 15)
- [ ] Study characteristics: table (Item 16)
- [ ] Risk of bias: results (Item 17)
- [ ] Results of studies (Item 18)
- [ ] Synthesis: results (Item 19)
- [ ] Certainty: results (Item 20)
- [ ] Limitations: studies, review (Item 21)
- [ ] Conclusions: implications (Item 22)
- [ ] Registration: number (Item 23)
- [ ] Support: funding (Item 24)
- [ ] Competing interests (Item 25)
- [ ] Availability: data, code (Item 26)
- [ ] Flow diagram (Item 27)
{% endif %}

{% if study_type == 'case_report' %}
#### CARE Guidelines Key Items
- [ ] Title: "Case Report" designation (Item 1)
- [ ] Keywords (Item 2)
- [ ] Abstract: structured (Item 3)
- [ ] Introduction: background (Item 4)
- [ ] Patient information (Item 5)
- [ ] Clinical findings (Item 6)
- [ ] Timeline (Item 7)
- [ ] Diagnostic assessment (Item 8)
- [ ] Differential diagnosis (Item 9)
- [ ] Therapeutic interventions (Item 10)
- [ ] Follow-up/outcomes (Item 11)
- [ ] Discussion: review, rationale (Item 12)
- [ ] Patient perspective (Item 13)
- [ ] Informed consent statement
{% endif %}

{% if study_type == 'QI' %}
#### SQUIRE 2.0 Key Items
- [ ] Title: QI design indicated (Item 1)
- [ ] Abstract: summary (Item 2)
- [ ] Problem description (Item 3)
- [ ] Available knowledge (Item 4)
- [ ] Rationale (Item 5)
- [ ] Specific aims (Item 6)
- [ ] Context: setting (Item 7)
- [ ] Intervention(s) (Item 8)
- [ ] Study of intervention (Item 9)
- [ ] Measures: outcomes, process (Item 10)
- [ ] Analysis: statistical (Item 11)
- [ ] Ethical considerations (Item 12)
- [ ] Results: participants, flow (Item 13)
- [ ] Results: context, setting (Item 14)
- [ ] Results: intervention (Item 15)
- [ ] Results: measures (Item 16)
- [ ] Results: main outcomes (Item 17)
- [ ] Results: unintended (Item 18)
- [ ] Limitations (Item 19)
- [ ] Conclusions: interpretation (Item 20)
{% endif %}

### C. Manuscript Structure

#### Title Page Elements
- [ ] Title (≤150 characters, informative)
- [ ] Running head (≤50 characters)
- [ ] Author names and full affiliations
- [ ] Corresponding author contact
- [ ] Word counts (abstract, main text)
- [ ] Keywords (3-5 MeSH terms)

#### Abstract Requirements
- [ ] Structured format per journal
- [ ] Word limit: typically 250-300 words
- [ ] Background/Objective
- [ ] Methods (design, participants, interventions, outcomes)
- [ ] Results (key findings with numbers)
- [ ] Conclusions (interpretation)
- [ ] Trial Registration (if applicable)

#### Main Text Structure (IMRAD)
- [ ] Introduction (background, gap, objectives)
- [ ] Methods (design, participants, interventions, outcomes, analysis)
- [ ] Results (flow diagram, baseline, primary, secondary, safety)
- [ ] Discussion (summary, comparison, limitations, implications)
- [ ] Conclusion (1-2 sentences)

### D. Figures and Tables

#### Figure Requirements
- [ ] Flow diagram (CONSORT/STROBE/PRISMA as appropriate)
- [ ] Primary outcome visualization
- [ ] Resolution: minimum 300 DPI (TIFF/EPS preferred)
- [ ] Colorblind-safe palettes
- [ ] Self-contained legends
- [ ] Figure count within journal limits

#### Table Requirements
- [ ] Table 1: Baseline characteristics
- [ ] Primary outcome results table
- [ ] Secondary outcomes (if applicable)
- [ ] Adverse events table (if applicable)
- [ ] Clear titles and footnotes
- [ ] Table count within journal limits

### E. References and Citations

- [ ] Reference count within journal limits
- [ ] Journal reference style identified
- [ ] All references verified and retrievable
- [ ] DOIs included where available
- [ ] Self-citations disclosed

### F. Compliance Documentation

- [ ] Funding statement
- [ ] Conflicts of interest declaration (all authors)
- [ ] Authorship contributions (ICMJE criteria)
- [ ] Data availability statement
- [ ] Patient consent statement (if applicable)
- [ ] Acknowledgments

### G. Cover Letter Components

- [ ] Submission declaration
- [ ] Significance statement (novelty, importance)
- [ ] Fit with journal audience
- [ ] Confirmation of requirements met
- [ ] Suggested reviewers (optional)
- [ ] Excluded reviewers (if conflict)

## 4. Journal-Specific Requirements

### High-Impact Medical Journals

| Journal | Word Limit | Abstract | Refs | Special Requirements |
|---------|-----------|----------|------|---------------------|
| **NEJM** | 3000 | 250 | 50 | Structured; Clinical trial registration mandatory |
| **Lancet** | 3500 | 300 | 30 | Summary; Funding/conflicts on title page |
| **JAMA** | 3500 | 350 | 50 | Original Investigation format |
| **BMJ** | 4000 | 250 | 35 | Open peer review; Patient involvement |
| **Annals Internal Medicine** | 4500 | 300 | 75 | CONSORT flow diagram mandatory |
| **PLOS Medicine** | 7000 | 300 | 100 | Open access; Data availability mandatory |

### Check Journal Website For:
- [ ] Current author guidelines
- [ ] Word count limits (abstract, main text)
- [ ] Reference limits and style
- [ ] Figure/table limits
- [ ] Supplementary material policies
- [ ] Open access fees
- [ ] Data sharing requirements
- [ ] Preprint policies

## 5. Pre-Submission Verification

### Content Checks
- [ ] Abstract accurately reflects full manuscript
- [ ] All figures/tables cited in text
- [ ] All abbreviations defined
- [ ] Reporting checklist completed
- [ ] Flow diagram matches text numbers

### Compliance Checks
- [ ] Word counts within limits
- [ ] Ethics approval documented
- [ ] Trial registration included
- [ ] Data availability statement complete
- [ ] COI disclosures complete

### Technical Checks
- [ ] High-resolution figures uploaded
- [ ] References formatted correctly
- [ ] Supplementary files labeled
- [ ] Cover letter prepared
- [ ] All author approvals obtained

## 6. Invoke Skill

Use `~~health/manuscript-prep` to:
1. Validate manuscript structure against study type requirements
2. Generate journal-specific formatting guidance
3. Create detailed figure/table preparation specifications
4. Draft cover letter template
5. Identify additional compliance requirements

## 7. Output Routing

- Save checklist to `~~cloud storage` in manuscript folder.
- Create project tracker entry for submission timeline.
- Generate reminder for target journal word count verification.
- Share checklist with co-authors for collaborative completion.

## 8. Output Guardrails

- **No PHI**: Ensure no patient identifiers in any output.
- **Ethics Check**: Flag unregistered trials or missing ethics approval.
- **Mode Awareness**: Lite mode provides essential items only; note when full compliance review needed.
- **Journal Fit**: Verify study scope aligns with target journal aims.
- **Authorship**: Remind to verify ICMJE authorship criteria for all authors.

---

**Next Steps**:
1. Complete reporting guideline checklist from EQUATOR Network
2. Draft manuscript following structure template
3. Prepare figures at required resolution
4. Format references per journal style
5. Write cover letter emphasizing novelty and fit
6. Obtain all author approvals
7. Complete pre-submission verification
8. Submit to target journal

