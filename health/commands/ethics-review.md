---
name: ethics-review
alias:
  - ethics
  - ethics-consult
description: Initiate an ethics review for research protocols or clinical cases, routing to the appropriate ethics skill (research-ethics or clinical-ethics) based on the nature of the ethical question.
arguments:
  - name: review_type
    description: "Type of ethics review needed: 'research' for REC/IRB applications and study protocols, or 'clinical' for clinical ethics consultations and patient care dilemmas."
    required: true
  - name: title
    description: "Title of the study (for research) or brief description of the clinical case/ethical dilemma."
    required: true
  - name: description
    description: "Detailed description of the research protocol, clinical situation, or ethical question."
    required: true
  - name: urgency
    description: "Urgency level: 'emergency', 'urgent', 'routine', or 'non-clinical'. Defaults to 'routine'."
    required: false
---

# Ethics Review Initiation

Use this command to initiate an ethics review for research ethics (REC/IRB) or clinical ethics consultation. The command routes to the appropriate skill based on review type.

## 1. Validate Input

- Ensure `review_type` is either "research" or "clinical". If ambiguous, ask for clarification.
- If `urgency` is not provided, default to "routine".
- For research reviews, confirm if this is a new application, amendment, or query.
- For clinical reviews, confirm if capacity assessment is involved.

## 2. Route to Appropriate Skill

### If `review_type` = "research":

Use `~~health/research-ethics` to:
1. Determine if ethics review is required (research vs. QI determination).
2. Assess risk level and appropriate review pathway.
3. Guide protocol development and review.
4. Assist with informed consent document drafting.
5. Prepare ethics application components.
6. Navigate committee submission process.

### If `review_type` = "clinical":

Use `~~health/clinical-ethics` to:
1. Conduct ethical case analysis using four-box method.
2. Assess decision-making capacity if relevant.
3. Guide surrogate decision-making process.
4. Facilitate family conference planning.
5. Navigate end-of-life decision-making.
6. Prepare ethics committee case presentation.

## 3. Generate Structured Output

### For Research Ethics Review

Produce:

---

#### ETHICS REVIEW INITIATED: {{title}}

**Review Type**: Research Ethics (REC/IRB)
**Initiated**: {{current_timestamp}}
**Urgency**: {{urgency or "routine"}}
**Status**: UNDER REVIEW

---

##### 1. REVIEW OVERVIEW

**Study/Protocol Description**:
{{description}}

**Initial Ethics Determination**:
- [ ] Research (requires full ethics review)
- [ ] Quality Improvement (may be exempt - requires determination)
- [ ] Unclear (requires clarification from HREC/IRB)

**Recommended Review Pathway**:
- [ ] Full Committee Review
- [ ] Expedited Review
- [ ] Chair/Executive Review
- [ ] Exemption Determination

---

##### 2. RISK STRATIFICATION

| Risk Category | Assessment | Implications |
|---------------|------------|--------------|
| **Physical Risk** | [To be assessed] | |
| **Psychological Risk** | [To be assessed] | |
| **Social/Economic Risk** | [To be assessed] | |
| **Privacy Risk** | [To be assessed] | |

**Overall Risk Level**:
- [ ] Negligible (Chair review)
- [ ] Minimal (Expedited review)
- [ ] Minor (Full committee)
- [ ] More than Minimal (Full committee + monitoring)
- [ ] Significant (External review required)

---

##### 3. KEY ETHICAL CONSIDERATIONS

**Consent Requirements**:
- [ ] Standard informed consent
- [ ] Simplified consent (minimal risk)
- [ ] Waiver of consent (requires justification)
- [ ] Surrogate consent required
- [ ] Assent + parental consent (pediatric)

**Vulnerable Populations**:
- [ ] Children/Minors
- [ ] Cognitively impaired
- [ ] Prisoners
- [ ] Pregnant women
- [ ] Economically disadvantaged
- [ ] None identified

**Special Considerations**:
- [ ] Indigenous/Māori/Pacific consultation required
- [ ] Biobanking/genetics involved
- [ ] Data linkage/secondary use
- [ ] Multi-site research
- [ ] International data transfer
- [ ] Conflict of interest identified

---

##### 4. REQUIRED DOCUMENTATION

**Core Documents**:
- [ ] Ethics application form
- [ ] Research protocol (comprehensive)
- [ ] Participant Information and Consent Form (PICF)
- [ ] Plain language summary
- [ ] Recruitment materials
- [ ] Data collection instruments
- [ ] Risk assessment plan

**Study-Specific Documents**:
- [ ] Investigator's Brochure (clinical trials)
- [ ] Insurance certificate
- [ ] CVs and GCP certificates
- [ ] DSMB charter (if required)
- [ ] Statistical analysis plan
- [ ] Māori/Pacific consultation documentation

**Governance Documents**:
- [ ] Conflict of interest declarations
- [ ] Funding agreement
- [ ] Site authorization letters (multi-site)
- [ ] Material transfer agreements

---

##### 5. REGULATORY FRAMEWORK

**Jurisdiction**: AU/NZ (default)

| Regulation | Requirement | Status |
|------------|-------------|--------|
| NHMRC National Statement (AU) | Ethical principles | [ ] Reviewed |
| HRC Guidelines (NZ) | Health research ethics | [ ] Reviewed |
| Privacy Act 1988/2020 | Data protection | [ ] Addressed |
| ICH-GCP (if applicable) | Clinical trial standards | [ ] Reviewed |

**Approval Timeline Estimate**:
- Full Committee: 4-8 weeks
- Expedited: 2-4 weeks
- Chair Review: 1-2 weeks

---

##### 6. NEXT STEPS

1. [ ] **Confirm Review Type**: Verify research vs. QI determination with HREC office
2. [ ] **Complete Risk Assessment**: Document all potential risks and mitigations
3. [ ] **Draft Protocol**: Ensure all required elements included
4. [ ] **Prepare PICF**: Draft consent form at appropriate reading level
5. [ ] **Gather Documents**: Compile all required supporting documents
6. [ ] **Pre-submission Query**: Consider informal consultation for novel/complex studies
7. [ ] **Submit Application**: Submit to HREC/IRB per institutional process
8. [ ] **Track Progress**: Monitor application status and respond to queries

---

### For Clinical Ethics Review

Produce:

---

#### CLINICAL ETHICS CONSULTATION: {{title}}

**Review Type**: Clinical Ethics
**Initiated**: {{current_timestamp}}
**Urgency**: {{urgency or "routine"}}
**Status**: UNDER REVIEW

---

##### 1. CASE OVERVIEW

**Clinical Situation**:
{{description}}

**Urgency Assessment**:
- [ ] Emergency (<2 hours) - Immediate response required
- [ ] Urgent (24-48 hours) - Evolving clinical situation
- [ ] Routine (3-5 days) - Standard consultation
- [ ] Non-clinical (1-2 weeks) - Policy/educational question

---

##### 2. STAKEHOLDER IDENTIFICATION

**Primary Stakeholder** (center of concern):
- Patient: [Name/ID]
- Location: [Ward/Unit]
- Clinical Status: [Brief status]

**Secondary Stakeholders**:
- [ ] Family members (specify relationship)
- [ ] Substitute decision-maker (if applicable)
- [ ] Treating clinicians
- [ ] Nursing staff
- [ ] Allied health
- [ ] Administration

**Ethical Tensions Identified**:
- [ ] Autonomy vs. Beneficence
- [ ] Patient vs. Family preferences
- [ ] Clinical judgment vs. Patient refusal
- [ ] Resource allocation concerns
- [ ] End-of-life decision-making
- [ ] Cultural/religious values conflict

---

##### 3. CAPACITY ASSESSMENT

**Decision-Making Capacity**:
- [ ] Has capacity for this decision
- [ ] Lacks capacity (substitute decision required)
- [ ] Capacity uncertain (requires assessment)
- [ ] Fluctuating capacity (delirium suspected)

**If Lacks Capacity**:
- [ ] Advance directive exists
- [ ] Enduring guardian/power of attorney
- [ ] Family hierarchy applicable
- [ ] Court/tribunal appointment required
- [ ] Person responsible (statutory hierarchy)

**Substitute Decision-Making Standard**:
- [ ] Substituted judgment (what would patient want?)
- [ ] Best interests (objective standard)
- [ ] Both standards to be considered

---

##### 4. ETHICAL ANALYSIS FRAMEWORK

**Four-Box Method Analysis**:

| Box | Key Questions | Status |
|-----|---------------|--------|
| **Medical Indications** | Diagnosis; prognosis; treatment options; likelihood of success | [ ] Information gathered |
| **Patient Preferences** | Expressed wishes; advance directive; values | [ ] Being explored |
| **Quality of Life** | Current status; likely future status; patient perspective | [ ] To be assessed |
| **Contextual Features** | Family dynamics; cultural factors; resources; conflicts | [ ] Being explored |

**Core Principles in Tension**:
- Autonomy: [How expressed?]
- Beneficence: [Benefits of treatment?]
- Non-maleficence: [Risks/burdens?]
- Justice: [Resource/fairness considerations?]

---

##### 5. CONSULTATION PLAN

**Information Needed**:
- [ ] Detailed medical history and prognosis
- [ ] Interview with patient (if capacity)
- [ ] Family conference required
- [ ] Prior statements/wishes from patient
- [ ] Cultural/religious consultation
- [ ] Second opinion on clinical facts
- [ ] Legal consultation (if guardianship issues)

**Meetings to Arrange**:
- [ ] Family conference (schedule within 24-48 hours)
- [ ] Care team meeting
- [ ] Multi-disciplinary team discussion
- [ ] Ethics committee review (if complex)

**Decision Timeline**:
- Target decision date: [Based on urgency]
- Time-limited trial option: [Yes/No]
- Review interval: [If ongoing decisions needed]

---

##### 6. POTENTIAL OUTCOMES

**Options to Explore**:
1. [Option A]: [Description]
2. [Option B]: [Description]
3. [Option C - Compromise]: [Description]
4. [Option D - Time-limited trial]: [Description if appropriate]

**Process Recommendations**:
- Facilitated family conference
- Cultural consultation
- Second opinion
- Palliative care consult
- Legal review

---

##### 7. NEXT STEPS

1. [ ] **Gather Information**: Complete clinical picture and patient values
2. [ ] **Assess Capacity**: Formal capacity assessment if uncertain
3. [ ] **Identify Surrogate**: Clarify legal decision-maker if needed
4. [ ] **Schedule Conference**: Family meeting within appropriate timeframe
5. [ ] **Consult Stakeholders**: Interview all relevant parties
6. [ ] **Apply Framework**: Complete four-box analysis
7. [ ] **Formulate Recommendations**: Ethically grounded advice
8. [ ] **Document**: Record analysis and recommendations
9. [ ] **Follow Up**: Monitor implementation and outcomes

---

## 4. Execute Routing

- Save review documentation to `~~cloud storage` in ethics review folder.
- Create tracker entry in `~~project tracker` for follow-up.
- If research ethics: Route to Research Office for HREC submission support.
- If clinical ethics: Notify appropriate clinical ethics service/team.
- Schedule reminder for follow-up based on urgency.

## 5. Output Guardrails

- **No PHI in Routing**: Do not include patient identifiers in routing documentation.
- **Jurisdiction Default**: AU/NZ ethics frameworks are default; ask if US/EU required.
- **Urgency Flag**: Emergency/urgent cases require immediate human notification.
- **Capacity Concerns**: Flag for capacity assessment if any uncertainty.
- **Child Protection**: Automatic escalation if child protection concerns identified.
- **Vulnerable Populations**: Enhanced safeguards required; flag for ethics committee.
- **Legal Issues**: Flag for legal consultation when court/guardianship involved.

---

**Note**: This ethics review initiation establishes the framework for addressing the ethical question. Detailed analysis and recommendations require engagement with the appropriate ethics skill and, for clinical cases, direct stakeholder consultation.
