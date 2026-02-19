---
name: health/clinical-doc-coauthoring
description: This skill should be used when collaboratively developing clinical documents requiring precision, regulatory compliance, and multi-stakeholder review. Use for clinical protocols, care pathways, practice guidelines, HTA submissions, evidence summaries, and position statements. Invoked when users mention co-authoring, document development, clinical writing, multi-stakeholder review, evidence synthesis, or guideline creation.
version: 1.0.0
---

# Clinical Document Co-authoring

A comprehensive framework for three-stage collaborative development of clinical and regulatory documents. This skill guides document teams through structured workflows that ensure clinical accuracy, regulatory compliance, evidence integrity, and stakeholder alignment.

**Important**: This skill assists with document development workflows but does not replace clinical judgment, regulatory expertise, or institutional approval processes. Always verify compliance with local regulatory requirements and obtain appropriate sign-offs before publication or implementation.

## When to Use This Skill

Invoke this skill when:
- Developing clinical protocols or procedures requiring stakeholder input.
- Creating care pathways with multi-disciplinary team involvement.
- Drafting clinical practice guidelines with evidence synthesis.
- Preparing health technology assessment (HTA) submissions.
- Writing NHMRC evidence summaries or position statements.
- Collaborating on regulatory submissions (TGA, FDA, etc.).
- Producing patient information materials with clinical accuracy requirements.
- Developing educational resources for healthcare professionals.
- Creating institutional policies with clinical implications.
- Any document requiring structured review cycles and evidence grading.

## Regulatory Context

### Australia & New Zealand (Default)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **NHMRC Guidelines** | Evidence-based documents | Standardized evidence grading (A-D, GPP); systematic review requirements |
| **TGA Guidelines** | Regulatory submissions | Clinical evidence requirements; format specifications; safety reporting |
| **NSQHS Standards** | Clinical protocols | Governance for clinical documentation; version control; approval workflows |
| **Medical Board of Australia** | Professional practice | Guidelines for medical practitioners; scope of practice statements |
| **NZ Ministry of Health** | National guidance | Te Tiriti o Waitangi considerations; equity and accessibility requirements |
| **State/Territory Health Acts** | Jurisdiction-specific | Mandatory consultation periods; approval authorities |

### US/EU-lite Fallback

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **FDA Guidelines** (US) | Regulatory submissions | Good Clinical Practice (GCP); 21 CFR Part 11 documentation |
| **IOM Standards** (US) | Clinical guidelines | Trustworthy guidelines criteria; systematic review mandate |
| **EMA Guidelines** (EU) | Regulatory documents | Common Technical Document (CTD) format; pharmacovigilance requirements |
| **GRADE Working Group** | International | Evidence-to-decision frameworks; certainty of evidence ratings |

### Jurisdiction Matrix

| Jurisdiction | Applicable Regulator | Reporting Trigger | Timeframe | Required Artifacts | Escalation Point |
|--------------|---------------------|-------------------|-----------|-------------------|------------------|
| **AU - National** | NHMRC/Medical Board | Clinical guideline publication | 6-12 months | Evidence review; conflict of interest declarations | Committee Chair |
| **AU - TGA** | Therapeutic Goods Admin | Product registration submission | Varies by class | Clinical evidence package; risk assessment | Regulatory Affairs |
| **NZ** | Ministry of Health | National guidance document | 3-6 months | Consultation responses; equity impact assessment | Guideline Lead |
| **US** | FDA/Professional Societies | Clinical practice guideline | 12-24 months | Systematic review; public comment responses | Guideline Panel Chair |
| **EU** | EMA/Competent Authority | Marketing authorization | Varies | Module 5 clinical overview; risk management plan | EU Regulatory Lead |

## Quick Reference

1. **Define Scope**: Document type, target audience, regulatory requirements.
2. **Assemble Team**: Clinical lead, methodologist, medical writer, stakeholders.
3. **Stage 1 - Development**: Purpose, evidence base, initial draft, stakeholder mapping.
4. **Stage 2 - Review**: Clinical accuracy, regulatory compliance, citation grading, iterative feedback.
5. **Stage 3 - Finalization**: Reader testing, accessibility review, approval workflow.
6. **Evidence Grading**: Apply NHMRC levels (A-D) or GRADE to all clinical claims.
7. **Citations**: Every clinical claim requires verifiable reference.
8. **Conflict of Interest**: Declare and manage all competing interests.
9. **Version Control**: Track all changes with attribution and timestamps.
10. **Final Sign-off**: Obtain approvals from authorized signatories before release.

## Operating Modes

### Standard Mode
Full three-stage collaborative workflow with complete evidence capture, systematic stakeholder review cycles, regulatory compliance verification, and formal approval processes. Use for clinical guidelines, HTA submissions, regulatory documents, and any publication-bound materials. Includes comprehensive reader testing and accessibility review.

### Lite Mode
Streamlined two-stage workflow (Development → Finalization) for internal documents, rapid guidance updates, or time-critical materials. Retains mandatory citation requirements and clinical review but reduces stakeholder consultation scope and reader testing. Never suppress high-risk escalation requirements or conflict of interest declarations.

## Detailed Guidance

### The Three-Stage Workflow

All clinical document development follows a structured three-stage process designed to ensure quality, accuracy, and stakeholder alignment.

---

### Stage 1: Context Gathering & Development

**Objective**: Establish document foundation including purpose, scope, evidence base, and stakeholder requirements.

#### 1.1 Purpose and Scope Definition

**Document Purpose Statement**:
- Primary objective: What is the document intended to achieve?
- Target audience: Who will use this document? (clinicians, patients, administrators, regulators)
- Clinical context: In what settings will this document apply?
- Outcomes: What decisions or actions should result from this document?

**Scope Boundaries**:
- Population: Who is included/excluded?
- Setting: Where does this apply? (tertiary, community, primary care)
- Interventions: What treatments, tests, or procedures are covered?
- Outcomes: What endpoints are considered?
- Timeframe: Is this interim or long-term guidance?

**Document Type Selection**:

| Document Type | Purpose | Evidence Requirement | Review Intensity |
|---------------|---------|---------------------|------------------|
| **Clinical Protocol** | Standardize care processes | Moderate (institutional evidence) | Standard |
| **Care Pathway** | Guide patient journey | High (pathway-specific evidence) | Standard |
| **Clinical Practice Guideline** | Evidence-based recommendations | Very High (systematic review) | Intensive |
| **HTA Submission** | Support funding/reimbursement | Very High (cost-effectiveness) | Intensive |
| **Evidence Summary** | Synthesize research findings | High (review of reviews) | Standard |
| **Position Statement** | State organizational stance | Moderate (expert consensus) | Standard |
| **Patient Information** | Educate patients/families | Moderate (plain language focus) | Standard |
| **Policy Document** | Govern organizational practice | Low-Moderate (compliance focus) | Standard |

#### 1.2 Target Audience Analysis

**Audience Segmentation**:
- **Primary Audience**: Main users of the document (e.g., emergency physicians)
- **Secondary Audience**: Occasional users or implementers (e.g., nurses, administrators)
- **Tertiary Audience**: Interested parties (e.g., patients, policymakers)

**Audience Needs Assessment**:
- Clinical decision-making requirements
- Knowledge prerequisites
- Resource and setting constraints
- Preferred format and length
- Language and literacy considerations

**Persona Development**:
- Create 2-3 representative user personas
- Document their goals, constraints, and pain points
- Test content against persona scenarios

#### 1.3 Regulatory Requirements Assessment

**Applicable Standards**:
- Clinical standards (NHMRC, IOM, SIGN, NICE)
- Regulatory requirements (TGA, FDA, EMA)
- Accreditation standards (NSQHS, Joint Commission)
- Organizational policies and procedures

**Compliance Checkpoints**:
- Required consultation periods
- Mandatory review authorities
- Conflict of interest disclosures
- Public comment requirements
- Approval signatures needed

#### 1.4 Evidence Base Assessment

**Evidence Inventory**:
- Systematic reviews and meta-analyses
- Randomized controlled trials
- Cohort and case-control studies
- Case series and expert opinion
- Existing guidelines and protocols

**Evidence Quality Evaluation**:
- Currency: When was the evidence published?
- Relevance: Does it apply to the target population/setting?
- Validity: Are the study methods rigorous?
- Applicability: Can findings be implemented in practice?

#### 1.5 Stakeholder Mapping

**Stakeholder Identification**:
- Clinical stakeholders (specialty colleges, professional associations)
- Consumer representatives (patients, carers, advocacy groups)
- Administrative stakeholders (hospital executives, department heads)
- Regulatory stakeholders (TGA, state health departments)
- Other affected parties (industry, insurers)

**Stakeholder Analysis Matrix**:

| Stakeholder | Interest | Influence | Engagement Strategy |
|-------------|----------|-----------|---------------------|
| [Name/Group] | High/Low | High/Low | [Consult/Inform/Partner] |

**Engagement Planning**:
- Consultation methods (survey, interview, focus group, workshop)
- Timeline for stakeholder input
- Mechanisms for feedback incorporation
- Communication channels and protocols

#### 1.6 Initial Draft Development

**Document Structure**:
1. **Title Page**: Document title, version, date, authors, approving body
2. **Executive Summary**: Key recommendations in 1-2 pages
3. **Introduction**: Background, purpose, scope, target audience
4. **Methods**: Evidence search strategy, selection criteria, grading approach
5. **Recommendations**: Numbered, graded, with rationale and evidence
6. **Implementation**: Resources required, training needs, monitoring
7. **Review Schedule**: Date for next review and triggers for early review
8. **References**: Full citations with evidence grading
9. **Appendices**: Supporting materials, tools, templates
10. **Conflict of Interest**: Declarations from all contributors

**Drafting Principles**:
- Use active voice and present tense
- Write for the target audience's knowledge level
- One recommendation per sentence
- Avoid ambiguous terms ("consider," "may") unless uncertainty is genuine
- Include strength of recommendation (strong/weak/conditional)

---

### Stage 2: Review & Refinement

**Objective**: Ensure clinical accuracy, regulatory compliance, evidence integrity, and stakeholder alignment through iterative review cycles.

#### 2.1 Clinical Accuracy Review

**Clinical Review Panel**:
- Subject matter experts from relevant specialties
- Frontline clinicians who will use the document
- Methodologists for evidence interpretation
- Consumer representatives for patient perspective

**Review Checklist**:
- [ ] Recommendations align with current evidence
- [ ] Clinical scenarios are realistic and comprehensive
- [ ] Contraindications and precautions are identified
- [ ] Drug dosages and administration details are correct
- [ ] Diagnostic criteria are accurate and current
- [ ] Risk stratification is appropriate
- [ ] Complications and adverse events are addressed
- [ ] Follow-up and monitoring guidance is practical

**Clinical Safety Check**:
- Identify any recommendations that could cause patient harm if misapplied
- Flag areas requiring special expertise or training
- Ensure appropriate caveats and limitations are stated
- Verify emergency protocols and escalation pathways

#### 2.2 Regulatory Compliance Check

**Compliance Verification**:
- [ ] Document meets applicable regulatory standards
- [ ] Required approval authorities are identified
- [ ] Consultation requirements are satisfied
- [ ] Conflict of interest declarations are complete
- [ ] Patient safety requirements are addressed
- [ ] Privacy and consent considerations are included
- [ ] Version control and document history are maintained

**Jurisdiction-Specific Checks**:
- **AU**: TGA requirements, state health department guidelines, NHMRC standards
- **NZ**: Ministry of Health requirements, Te Tiriti considerations
- **US**: FDA requirements, Joint Commission standards, state licensing boards
- **EU**: EMA guidelines, country-specific competent authority requirements

#### 2.3 Evidence Grading Application

**NHMRC Evidence Hierarchy**:

| Level | Description | Study Types |
|-------|-------------|-------------|
| **I** | Excellent | Systematic review of RCTs; individual RCT with narrow confidence interval |
| **II** | Good | Systematic review of cohort studies; individual cohort study or low-quality RCT |
| **III-1** | Satisfactory | Systematic review of case-control studies; individual case-control study |
| **III-2** | Adequate | Cohort or case-control study with high risk of bias; ecological studies |
| **III-3** | Limited | Case series; case reports; cross-sectional studies |
| **IV** | Expert Opinion | Expert opinion based on clinical experience; physiological/bench research |
| **GPP** | Good Practice Point | Consensus-based recommendations when evidence insufficient |

**GRADE Evidence Quality Ratings**:

| Quality Level | Interpretation | Symbol |
|---------------|----------------|--------|
| **High** | Very confident true effect lies close to estimate | ⊕⊕⊕⊕ |
| **Moderate** | Moderately confident; true effect likely close to estimate | ⊕⊕⊕○ |
| **Low** | Limited confidence; true effect may be substantially different | ⊕⊕○○ |
| **Very Low** | Very little confidence; true effect likely substantially different | ⊕○○○ |

**Evidence Grading Process**:
1. Assign initial level based on study design (NHMRC) or quality assessment (GRADE)
2. Rate down for risk of bias, inconsistency, indirectness, imprecision, publication bias
3. Rate up for large effect, dose-response, plausible confounders would reduce effect
4. Document rationale for final grade

#### 2.4 Citation Requirements for Clinical Claims

**Mandatory Citation Rule**: Every clinical claim must be supported by a verifiable reference.

**Claim Categories Requiring Citations**:
- Statistical claims ("50% of patients experience...")
- Treatment efficacy ("Drug X reduces mortality by...")
- Diagnostic accuracy ("Test Y has 90% sensitivity...")
- Risk factors ("Smoking increases risk of...")
- Prevalence/incidence ("Condition Z affects 1 in 100...")
- Clinical outcomes ("Procedure A results in...")

**Citation Format**:
- Use Vancouver referencing style for clinical documents
- Include DOI where available
- Format: Author(s). Title. Journal. Year;Volume(Issue):Pages. DOI
- For online sources: Include access date and URL

**Citation Quality Standards**:
- Prefer peer-reviewed sources over grey literature
- Prioritize systematic reviews and meta-analyses
- Use primary sources rather than secondary citations
- Ensure citations are current (generally <5 years, except for seminal studies)
- Verify all citations before finalization

**Citation Management**:
- Use reference management software (EndNote, Zotero, Mendeley)
- Maintain master reference library
- Track evidence-to-recommendation mapping
- Document excluded studies with rationale

#### 2.5 Iterative Stakeholder Feedback

**Review Rounds**:
- **Round 1**: Expert panel review (clinical and methodological)
- **Round 2**: Expanded stakeholder review (broader clinical community)
- **Round 3**: Public/consumer consultation (where required)
- **Round 4**: Final approval body review

**Feedback Management Process**:
1. Distribute document with structured feedback form
2. Set clear deadline for responses (typically 2-4 weeks)
3. Collate all feedback in tracking spreadsheet
4. Review team assesses each comment
5. Accept, modify, or reject with documented rationale
6. Communicate decisions to stakeholders
7. Revise document based on accepted feedback

**Stakeholder Feedback Template**:

| Section | Comment | Submitter | Response | Action | Rationale |
|---------|---------|-----------|----------|--------|-----------|
| [Reference] | [Comment text] | [Name/Org] | [Accepted/Rejected/Modified] | [Change made] | [Why] |

**Conflict Resolution**:
- When stakeholders disagree, convene discussion meeting
- Document areas of consensus and persistent disagreement
- Consider voting for unresolved issues (document dissenting views)
- Escalate to higher authority if consensus cannot be reached

---

### Stage 3: Reader Testing & Finalization

**Objective**: Validate document usability, comprehension, and implementation feasibility with target audience before final approval.

#### 3.1 Target Audience Review

**Reader Testing Cohorts**:
- Representative users from target audience
- Mixed experience levels (novice to expert)
- Various settings (if applicable)
- Consumer representatives (for patient-facing documents)

**Testing Methods**:
- **Comprehension Testing**: Can readers understand key messages?
- **Usability Testing**: Can readers find and apply information?
- **Implementation Testing**: Can readers operationalize recommendations?
- **Acceptability Testing**: Do readers find the document acceptable?

#### 3.2 Comprehension Testing Methodology

**The Think-Aloud Protocol**:
1. Provide document section to reader
2. Ask reader to verbalize their thinking as they read
3. Note confusion points, misinterpretations, or questions
4. Do not correct or guide during test
5. Debrief afterward to understand reasoning

**Comprehension Questions**:
- What is the main recommendation in this section?
- Under what circumstances would you apply this guidance?
- What are the key contraindications?
- How would you explain this to a patient/colleague?

**Success Criteria**:
- ≥80% of readers correctly identify main recommendations
- ≤20% have significant comprehension errors
- No safety-critical misinterpretations
- Average reading time acceptable for document length

#### 3.3 Implementation Feasibility Testing

**Feasibility Assessment**:
- **Resource Requirements**: Are necessary resources available?
- **Workflow Integration**: Can recommendations be integrated into practice?
- **Training Needs**: Is required training available and adequate?
- **Barriers**: What obstacles exist to implementation?

**Pilot Testing**:
- Select 1-2 sites for document pilot
- Monitor implementation over defined period
- Collect feedback on practical application
- Document adaptations required for local context

**Implementation Tools**:
- Quick reference guides
- Decision algorithms/flowcharts
- Checklists and forms
- Training materials
- Audit tools

#### 3.4 Accessibility Review

**Health Literacy Assessment**:
- **Patient Materials**: Target grade 6-8 reading level
- **Professional Materials**: Target grade 10-12 reading level
- **Plain Language**: Use simple words, short sentences, active voice
- **Visual Design**: Clear headings, bullet points, white space

**Cultural Safety**:
- Consider cultural appropriateness for target populations
- Include culturally diverse perspectives in development
- Address health equity implications
- Use inclusive and respectful language

**Accessibility Standards**:
- Comply with Web Content Accessibility Guidelines (WCAG 2.1) for digital documents
- Provide alternative formats (large print, audio, Easy Read)
- Ensure screen reader compatibility
- Test with users who have disabilities

#### 3.5 Final Approval Workflow

**Approval Hierarchy**:

| Document Type | First Approval | Second Approval | Final Approval |
|---------------|----------------|-----------------|----------------|
| Clinical Protocol | Specialty Lead | Clinical Director | Medical Advisory Committee |
| Care Pathway | Pathway Working Group | Quality Committee | Executive |
| Clinical Guideline | Guideline Committee | Professional Society | Board/Council |
| HTA Submission | HTA Team | Clinical Evidence Committee | Funding Decision Body |
| Position Statement | Drafting Committee | Executive | Board |

**Approval Documentation**:
- [ ] All review comments addressed or documented
- [ ] Conflict of interest declarations signed
- [ ] Evidence grading completed and verified
- [ ] Citations checked for accuracy
- [ ] Version history complete
- [ ] Approval signatures obtained
- [ ] Publication authorization granted

**Final Checks**:
- Proofread for spelling, grammar, and formatting
- Verify all cross-references and hyperlinks
- Check tables, figures, and appendices
- Ensure consistent terminology throughout
- Confirm document metadata (version, date, status)

---

### Document Type Templates

#### Clinical Protocol Template

```
TITLE: [Condition/Procedure] Protocol
VERSION: X.X
DATE: DD/MM/YYYY
STATUS: [Draft/Review/Approved]

1. PURPOSE
   [Statement of intent and objectives]

2. SCOPE
   [Population, setting, exclusions]

3. DEFINITIONS
   [Key terms and abbreviations]

4. CLINICAL INDICATIONS
   [When to use this protocol]

5. CONTRAINDICATIONS AND PRECAUTIONS
   [When NOT to use; special cautions]

6. PROCEDURE/PROCESS
   [Step-by-step instructions]

7. MEDICATIONS/DOSAGES (if applicable)
   [Drug names, doses, routes, frequencies]

8. MONITORING AND FOLLOW-UP
   [Assessment parameters, frequency, criteria for escalation]

9. DOCUMENTATION REQUIREMENTS
   [What must be recorded]

10. QUALITY INDICATORS
    [Metrics for protocol adherence and outcomes]

11. REFERENCES
    [Citations with evidence grades]

12. REVIEW HISTORY
    [Version, date, changes, approver]

APPENDICES
    [Forms, tools, patient information]
```

#### Clinical Practice Guideline Template

```
TITLE: [Topic] Clinical Practice Guideline
VERSION: X.X
DATE: DD/MM/YYYY
SPONSOR: [Organization]

EXECUTIVE SUMMARY
   [Key recommendations in table format]

1. INTRODUCTION
   1.1 Background
   1.2 Purpose and Objectives
   1.3 Target Audience
   1.4 Scope (Inclusions/Exclusions)

2. METHODS
   2.1 Guideline Development Group
   2.2 Evidence Search Strategy
   2.3 Study Selection Criteria
   2.4 Evidence Grading Approach
   2.5 Conflict of Interest Management

3. RECOMMENDATIONS
   [Numbered recommendations with:
    - Recommendation strength
    - Evidence grade
    - Rationale
    - Key evidence citations
    - Implementation considerations]

4. IMPLEMENTATION
   4.1 Barriers and Facilitators
   4.2 Resource Implications
   4.3 Audit and Quality Indicators
   4.4 Tools and Materials

5. UPDATING
   5.1 Review Schedule
   5.2 Triggers for Early Review

6. REFERENCES

7. APPENDICES
   A. Evidence Tables
   B. Search Strategies
   C. Excluded Studies
   D. Conflict of Interest Declarations
   E. Abbreviations and Glossary

8. ACKNOWLEDGMENTS
```

#### HTA Submission Template

```
TITLE: Health Technology Assessment: [Technology Name]
SUBMISSION DATE: DD/MM/YYYY
APPLICANT: [Organization]

VOLUME 1: EXECUTIVE SUMMARY

VOLUME 2: CLINICAL EVIDENCE
   1. Technology Description
   2. Target Population
   3. Current Practice
   4. Clinical Effectiveness Evidence
   5. Safety Evidence
   6. Quality of Evidence Assessment

VOLUME 3: ECONOMIC EVIDENCE
   1. Economic Evaluation Methods
   2. Cost-Effectiveness Results
   3. Budget Impact Analysis
   4. Uncertainty Analysis

VOLUME 4: IMPLEMENTATION
   1. Regulatory Status
   2. Implementation Requirements
   3. Risk Management
   4. Post-Market Surveillance

VOLUME 5: SUPPORTING MATERIALS
   [Evidence tables, model details, appendices]

APPENDICES
   A. Systematic Review Protocol
   B. Search Strategies
   C. Data Extraction Forms
   D. Model Documentation
   E. Conflict of Interest Declarations
```

---

## Documentation Requirements

### Core Document Components
- [ ] Title page with version control metadata
- [ ] Executive summary (max 2 pages)
- [ ] Clear purpose and scope statements
- [ ] Target audience definition
- [ ] Methods section (evidence search and selection)
- [ ] Numbered recommendations with evidence grades
- [ ] Implementation guidance
- [ ] Review and updating schedule
- [ ] Complete reference list
- [ ] Conflict of interest declarations
- [ ] Acknowledgments and authorship

### Version Control Requirements
- [ ] Version number (semantic versioning: major.minor.patch)
- [ ] Date of current version
- [ ] Document status (Draft, Review, Approved, Superseded)
- [ ] Author(s) and reviewer(s) identified
- [ ] Approving authority and approval date
- [ ] Change log with version history
- [ ] Supersedes list (previous versions)

### Review Cycle Documentation
- [ ] Date of next scheduled review
- [ ] Triggers for early review documented
- [ ] Review responsibility assigned
- [ ] Outcome of last review documented

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **No evidence grading** | Readers cannot assess recommendation strength | Apply NHMRC or GRADE to every recommendation |
| **Missing citations** | Claims cannot be verified; undermines credibility | Cite every clinical claim with verifiable reference |
| **No conflict of interest declaration** | Bias may unduly influence recommendations | Declare all competing interests from all contributors |
| **Vague recommendations** | "Consider" or "may" creates ambiguity | Use strong/conditional language with explicit criteria |
| **No stakeholder consultation** | Recommendations may not reflect practice realities | Map stakeholders and conduct structured consultation |
| **Insufficient reader testing** | Document may be unusable by target audience | Test comprehension and feasibility with representative users |
| **Skipping regulatory checks** | Document may not meet compliance requirements | Verify all applicable regulatory standards before approval |
| **Inadequate version control** | Users may reference outdated guidance | Implement strict version control with clear change documentation |
| **No implementation plan** | Recommendations may not be adopted | Include barriers, facilitators, tools, and audit metrics |
| **Lone author development** | Lacks diverse perspectives and expertise | Assemble multi-disciplinary development group |
| **No review schedule** | Document becomes outdated | Set scheduled review with triggers for early update |
| **Ignoring equity implications** | Recommendations may disadvantage vulnerable groups | Consider health equity in all recommendations |

## When to Escalate

Escalate to Guideline Committee Chair, Medical Director, or Governance Committee when:
- Recommendations conflict with established best practice or organizational policy.
- Evidence quality is very low but recommendation strength is strong.
- Stakeholder groups fundamentally disagree on key recommendations.
- Patient safety concerns are identified during review.
- Regulatory compliance cannot be achieved within timeline.
- Conflict of interest cannot be adequately managed.
- Significant resource implications require executive approval.
- Document status is contentious or politically sensitive.
- Approval authorities cannot reach consensus.

## Privacy Considerations

- **PHI Involved**: Conditional - document development may use de-identified patient scenarios or aggregate data.
- **Data Minimization**: Use only de-identified or aggregate data for case examples; avoid individual patient details.
- **De-identification**: Remove all direct and indirect identifiers from patient examples; use composite cases rather than real patients.
- **Access Controls**: Limit draft document access to development team and designated reviewers; use secure collaboration platforms.
- **Retention**: Retain all versions per organizational policy; maintain stakeholder feedback records for audit purposes.
- **No Persistence**: Do not store patient information in temporary workspaces or chat history during document development.
- **Publication Review**: Ensure patient examples in published documents cannot be re-identified.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Document based on high-quality systematic reviews with clear consensus | High | Proceed through standard workflow; routine review |
| Evidence base is mixed or conflicting | Medium | Flag for extended expert consultation; document uncertainty explicitly |
| Document involves high-risk clinical interventions | Low | Require additional safety review; escalate to clinical governance |
| Stakeholder input reveals significant disagreement | Medium | Convene consensus meeting; consider voting or dissenting opinions |
| Limited evidence available (expert opinion level) | Medium | Limit recommendation strength; schedule early review for new evidence |
| Regulatory requirements are unclear or complex | Low | Escalate to regulatory affairs; seek formal guidance |
| Target audience is highly diverse (e.g., multi-specialty) | Medium | Extended reader testing across all user groups |
| Document supersedes widely-used existing guidance | Low | Careful change management; extended consultation period |

## Tool Requirements

- `~~document collaboration` - For multi-author editing and review
- `~~reference management` - For citation tracking and bibliography management
- `~~health/literature-search` - For evidence retrieval and systematic reviews
- `~~health/evidence-grading` - For NHMRC/GRADE assessment tools
- `~~health/clinical-systems` - For accessing institutional protocols and policies
- `~~cloud storage` - For document version control and secure sharing
- `~~project tracker` - For managing review cycles and stakeholder feedback

## Success Indicators

You've applied this skill well when:
- [ ] Document follows appropriate template for document type
- [ ] All recommendations have evidence grades and citations
- [ ] Conflict of interest declarations are complete and transparent
- [ ] Stakeholder consultation was structured and documented
- [ ] Reader testing validates comprehension and usability
- [ ] Regulatory compliance is verified and documented
- [ ] Version control and change history are complete
- [ ] Implementation tools are provided
- [ ] Review schedule is established
- [ ] Document is approved by appropriate authority
- [ ] Health equity and cultural safety are addressed
- [ ] Final output is publication-ready and professional

## Related Skills

- `~~health/guideline-development` - For creating clinical practice guidelines specifically
- `~~health/policy-development` - For organizational policy documents
- `~~health/evidence-review` - For systematic literature reviews supporting documents
- `~~health/quality-improvement` - For QI projects that may inform document development
- `~~health/governance` - For documents requiring governance approval workflows
- `~~document-skills/docx` - For document formatting and production
