---
name: health/research-ethics
description: This skill should be used when preparing Research Ethics Committee (REC) or Institutional Review Board (IRB) applications, reviewing research protocols for ethical compliance, drafting informed consent documents, navigating ethics governance processes, or preparing for ethics committee submissions. Use for clinical trials, human research, biobanking, data linkage studies, and qualitative research requiring ethics approval.
version: 1.0.0
---

# Research Ethics

A comprehensive framework for navigating research ethics approval processes, preparing REC/IRB submissions, and ensuring ethical compliance in human research. This skill guides researchers through protocol development, informed consent drafting, and committee preparation with jurisdiction-specific requirements.

**Important**: This skill assists with research ethics workflows but does not guarantee ethics approval or replace institutional ethics committee authority. Always submit to your institution's designated ethics review body.

## When to Use This Skill

Invoke this skill when:
- Preparing a new REC/IRB application for human research.
- Drafting or reviewing informed consent documents for research participation.
- Designing research protocols that involve human participants, data, or tissue.
- Navigating multi-site or multi-jurisdictional ethics approval processes.
- Responding to ethics committee queries or requests for modification.
- Conducting ethical risk assessments for proposed research.
- Preparing for ethics committee meetings or oral presentations.
- Determining whether a project requires formal ethics review.
- Managing ethics amendments, renewals, or adverse event reporting.
- Establishing data sharing or biobanking governance arrangements.

## Regulatory Context

### Australia & New Zealand (Default)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **NHMRC National Statement** (AU) | Ethical conduct in human research | Values: Respect, research merit, justice, beneficence. Risk-benefit assessment mandatory. |
| **NHMRC Chapter 2.1** (AU) | General requirements | Research merit and integrity; justice; beneficence; respect. |
| **NHMRC Chapter 2.2** (AU) | Qualitative methods | Risk assessment for sensitive topics; appropriate consent processes. |
| **NHMRC Chapter 3.1** (AU) | Clinical trials | Safety monitoring; data safety monitoring boards; trial registration. |
| **HRC Guidelines** (NZ) | Human research ethics | Te Ara Tika (Māori ethical framework); community engagement requirements. |
| **Privacy Act 1988** (AU) | Data handling | APP 3: Collection of solicited personal information; lawful collection. |
| **Privacy Act 2020** (NZ) | Privacy protection | Information privacy principles; cross-border data disclosure restrictions. |
| **Gene Technology Act 2000** (AU) | GMO research | OGTR approval required for genetically modified organisms research. |

### US/EU-lite Fallback

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **Belmont Report** (US) | Ethical principles | Respect for persons; beneficence; justice. Foundation for 45 CFR 46. |
| **45 CFR Part 46** (US) | Federal regulations | Subparts A-D: Basic protections; pregnant women; prisoners; children. |
| **ICH-GCP E6(R2)** (International) | Clinical trials | Informed consent standards; independent ethics committee; investigator responsibilities. |
| **Declaration of Helsinki** (International) | Medical research | WMA ethical principles; placebo use restrictions; post-trial access. |
| **GDPR** (EU) | Data protection | Lawful basis for processing; data minimization; special category data (Article 9). |
| **Clinical Trials Regulation EU 536/2014** | EU trials | Single submission portal; informed consent requirements; safety reporting. |

### Jurisdiction Matrix

| Jurisdiction | Applicable Regulator | Reporting Trigger | Timeframe | Required Artifacts | Escalation Point |
|--------------|---------------------|-------------------|-----------|-------------------|------------------|
| **AU - NHMRC** | HREC (Human Research Ethics Committee) | Research with human participants | Pre-commencement | Ethics application; protocol; PICF; risk assessment | Deputy Chair, HREC |
| **AU - State** | State Health Dept | Research in public health facilities | Pre-commencement + site authorisation | Site authorisation; insurance certificate | Research Governance Officer |
| **NZ - HRC** | Ethics Committee (EC) | Health and disability research | Pre-commencement | Ethics application; protocol; consent form; Māori consultation | Ethics Committee Chair |
| **US - Federal** | IRB (Institutional Review Board) | Human subjects research | Pre-commencement | IRB application; protocol; consent form; HIPAA authorization | IRB Chair/Admin |
| **EU** | National Competent Authority | Clinical trials | Pre-commencement via CTIS | EudraCT number; protocol; IMPD; insurance | Ethics Committee Chair |

## Quick Reference

1. **Ethics Determination**: First establish if formal review is required (some QI may be exempt).
2. **Risk Stratification**: Minimal risk vs. more than minimal risk drives review pathway.
3. **Consent Quality**: Information, comprehension, voluntariness—the three pillars.
4. **Vulnerable Populations**: Additional safeguards required; enhanced review required.
5. **Privacy by Design**: Embed data protection from protocol inception.
6. **Māori/Pacific Engagement**: Mandatory in NZ; respectful partnership in AU.
7. **Conflict of Interest**: Disclose all financial and non-financial interests.
8. **Data Safety**: Plan for monitoring, interim analyses, and stopping rules.
9. **Multi-site**: Identify lead HREC/IRB and site-specific requirements.
10. **Post-approval**: Understand reporting obligations for deviations and adverse events.

## Operating Modes

### Standard Mode
Full research ethics workflow with comprehensive protocol review, detailed informed consent development, complete risk assessment, and formal governance documentation. Use for interventional research, clinical trials, vulnerable population research, and any study requiring full HREC/IRB review. Includes committee preparation and response to queries.

### Lite Mode
Streamlined guidance for minimal risk research, student projects, or secondary data analysis with established ethics approval. Focuses on essential ethics principles, abbreviated consent processes, and expedited review pathways. Never suppresses high-risk escalation requirements or vulnerable population safeguards.

## Detailed Guidance

### 1. Ethics Requirement Determination

Before commencing application preparation, determine if formal ethics review is required:

#### Research vs. Quality Improvement

| Characteristic | Research | Quality Improvement |
|----------------|----------|---------------------|
| **Intent** | Generate generalizable knowledge | Improve local processes |
| **Design** | Systematic investigation | Systematic improvement |
| **Population** | Different from those at institution | Same as those receiving care |
| **Randomization** | Often present | Rarely present |
| **Generalizability** | Primary goal | Secondary or absent |
| **Ethics Review** | Usually required | May be exempt |

**When QI Becomes Research**:
- Intent shifts to publication with generalizable findings.
- Additional risk or burden beyond standard care.
- Randomization of interventions.
- Use of control groups for comparison.
- New treatments or experimental procedures.

#### Exemptions and Expedited Review

**Potential Exemptions** (AU/NZ context):
- Secondary use of de-identified data (no re-identification risk).
- Publicly available information (statistics, archival records).
- Quality assurance/audit activities.
- Case series (n≤3) with ethics committee notification.
- Evaluation of public programs.

**Expedited Review Eligible** (US 45 CFR 46.110):
- Minor changes in previously approved research.
- Research on existing data/documents (no identifiers).
- Prospective collection of biological samples (non-invasive).
- Voice/video recordings (limited categories).

**Note**: Exemption determinations must be made by the ethics committee, not the researcher.

### 2. Protocol Development and Review

#### Essential Protocol Elements

A research protocol must include:

1. **Background and Rationale**
   - Scientific justification for the research.
   - Summary of existing evidence (literature review).
   - Knowledge gap being addressed.

2. **Research Question and Objectives**
   - Primary and secondary objectives.
   - Hypothesis (if applicable).
   - Outcome measures with definitions.

3. **Study Design and Methods**
   - Study type (RCT, observational, qualitative, etc.).
   - Participant population and eligibility criteria.
   - Sample size justification (statistical power).
   - Recruitment methods and materials.
   - Data collection procedures.
   - Intervention details (if interventional).

4. **Risk Assessment and Management**
   - Identification of potential risks (physical, psychological, social, economic).
   - Risk minimization strategies.
   - Risk-benefit justification.
   - Withdrawal procedures.

5. **Ethical Considerations**
   - How ethical principles will be upheld.
   - Specific issues (vulnerability, consent capacity).
   - Cultural considerations.

6. **Data Management**
   - Collection, storage, and security.
   - Retention and disposal.
   - Future use/sharing plans.

7. **Governance and Oversight**
   - Safety monitoring plan.
   - Data safety monitoring board (if required).
   - Adverse event definitions and reporting.
   - Insurance and indemnity.

#### Risk Stratification Framework

| Risk Level | Definition | Review Pathway | Consent Requirements |
|------------|------------|----------------|---------------------|
| **Negligible** | No foreseeable harm; inconvenience only | Chair review or exemption | Standard or waiver possible |
| **Minimal** | Everyday risks; minor discomfort | Expedited review | Standard consent |
| **Minor** | Temporary harm; reversible | Full committee review | Enhanced consent; monitoring |
| **More than Minimal** | Significant harm possible | Full committee; DSMB required | Enhanced; re-consent; audit |
| **Significant** | Serious harm; lasting effects | Full committee; external review | Extensive; independent witness |

### 3. Informed Consent Framework

#### The Three Pillars of Valid Consent

**Information**:
- Nature and purpose of research.
- Procedures involved (all visits, time commitment).
- Risks and discomforts (reasonably foreseeable).
- Benefits (to participant and others).
- Alternatives to participation.
- Confidentiality protections.
- Compensation and costs.
- Voluntary nature and right to withdraw.
- Contact information for questions.

**Comprehension**:
- Written at appropriate reading level (typically grade 6-8).
- Use plain language; avoid jargon.
- Visual aids for complex concepts.
- Teach-back method to verify understanding.
- Allow time for questions.
- Interpreter services for non-English speakers.

**Voluntariness**:
- No coercion (including therapeutic misconception).
- No undue influence (excessive payment).
- Free to refuse or withdraw without penalty.
- No impact on clinical care relationship.
- Independent decision-making supported.

#### Consent Document Templates

**Standard Elements** (NHMRC/National Statement; ICH-GCP):

```
1. STUDY TITLE: [Plain language title]

2. INVITATION TO PARTICIPATE
   - Why you are being asked
   - Voluntary nature

3. WHAT IS THE STUDY ABOUT?
   - Background and purpose
   - Why this research is important

4. WHAT WILL PARTICIPATION INVOLVE?
   - Procedures (visit-by-visit)
   - Time commitment
   - What happens if you withdraw

5. ARE THERE ANY RISKS?
   - Side effects or discomforts
   - How risks will be managed
   - Compensation for injury (if applicable)

6. ARE THERE ANY BENEFITS?
   - Direct benefits to you
   - Benefits to others/future patients

7. WHAT ARE THE ALTERNATIVES?
   - Standard care if you don't participate

8. WILL MY INFORMATION BE KEPT CONFIDENTIAL?
   - How data is protected
   - Who will see your information
   - Limits to confidentiality (mandatory reporting)
   - Data sharing plans

9. WHAT ARE THE COSTS?
   - Costs to you
   - Reimbursement for expenses
   - Compensation for participation

10. WHAT IF I HAVE QUESTIONS?
    - Researcher contact
    - Ethics committee contact
    - Complaints process

11. CONSENT DECLARATION
    - Statement of understanding
    - Voluntary agreement
    - Signature blocks (participant, researcher, witness if applicable)
    - Date
```

#### Special Consent Considerations

**Vulnerable Populations**:
- **Children/Minors**: Assent from child; consent from parent/guardian. Age-appropriate information sheets.
- **Cognitively Impaired**: Consent from legal representative; participant assent if possible.
- **Prisoners**: Enhanced protections; minimal risk preference; no undue inducements.
- **Pregnant Women**: Fetal protections; research purpose must justify inclusion.
- **Emergency Settings**: Exception from informed consent (EFIC) procedures if applicable.

**Waiver of Consent**:

Possible only if ALL of the following apply (NHMRC paragraph 2.2.10):
1. Research involves no more than minimal risk.
2. Waiver is unlikely to adversely affect rights/welfare.
3. Research could not practicably be carried out without waiver.
4. Privacy and confidentiality protections adequate.
5. Additional safeguards (if vulnerable).

**Secondary Use of Data**:
- Consent for future use at initial collection (opt-in/opt-out).
- Broad consent for biobanking.
- Re-consent if use diverges from original scope.
- Consider tiered consent options.

### 4. Ethics Application Preparation

#### Application Components Checklist

**Core Documents**:
- [ ] Completed ethics application form (institution-specific).
- [ ] Research protocol (comprehensive, version-controlled).
- [ ] Participant Information and Consent Form (PICF).
- [ ] Plain language summary.
- [ ] Recruitment materials (advertisements, letters, scripts).
- [ ] Data collection instruments (surveys, interview guides).
- [ ] Risk assessment and management plan.
- [ ] Privacy and data security plan.
- [ ] CVs and GCP certificates for investigators.

**Study-Specific Documents**:
- [ ] Investigators' Brochure (clinical trials).
- [ ] Clinical trial insurance certificate.
- [ ] Site authorization letters (multi-site).
- [ ] Material transfer agreements (tissue/data sharing).
- [ ] Māori/Pacific consultation documentation (NZ/AU where applicable).
- [ ] DSMB charter (if required).
- [ ] Statistical analysis plan.

**Governance Documents**:
- [ ] Conflict of interest declarations.
- [ ] Funding agreement or award letter.
- [ ] Sponsor indemnity (if industry-sponsored).
- [ ] Site-specific assessment (SSA) form.

#### Committee Submission Process

**Before Submission**:
1. Internal institutional review (if required).
2. Supervisor/CI sign-off.
3. Conflict of interest disclosure and management.
4. Budget review and approval.
5. Pre-submission query to ethics office (recommended for novel/complex).

**Submission Pathways**:

| Pathway | Timeline | Suitable For |
|---------|----------|--------------|
| **Full Committee** | 4-8 weeks | Interventional research; vulnerable populations; novel methods |
| **Executive/Chair** | 2-4 weeks | Minimal risk; student projects; amendments |
| **Out-of-Session** | 1-2 weeks | Urgent patient safety; administrative amendments |
| **Expedited** (US) | 2-3 weeks | Expedited categories; minor modifications |

**After Submission**:
- Receipt acknowledgment (3-5 business days).
- Queries or requests for information (RFI).
- Conditional approval with modifications.
- Full approval (ethics clearance number assigned).
- Provisional approval (minor conditions).

### 5. Committee Preparation and Presentation

#### Oral Presentation Guidelines

When presenting to the ethics committee:

**Structure** (10-15 minutes typical):
1. **Introduction** (2 min): Research team; study title; funding.
2. **Background** (2 min): Problem; evidence gap; significance.
3. **Methods** (3 min): Design; population; key procedures.
4. **Ethics** (5 min): Risk assessment; consent process; safeguards; vulnerable populations.
5. **Questions** (3 min): Anticipated committee concerns.

**Key Messages to Convey**:
- Scientific merit justifies any risk.
- Risks are minimized and proportionate.
- Consent process is robust.
- Vulnerable participants are protected.
- Research team is qualified and experienced.
- Monitoring and stopping rules are in place.

**Anticipate Questions**:
- How did you calculate sample size?
- What are the stopping rules?
- How will you handle withdrawal of consent?
- What happens if a participant is harmed?
- How will you ensure confidentiality?
- Why is this research necessary?

#### Responding to Committee Queries

**Process**:
1. Acknowledge receipt of queries within 48 hours.
2. Convene research team to address each point.
3. Prepare point-by-point response document.
4. Track changes in protocol/PICF.
5. Submit response by deadline.

**Response Quality**:
- Address every query specifically.
- Provide rationale for any disagreements (respectfully).
- Show track changes in revised documents.
- Update version numbers and dates.
- Escalate substantive disagreements to supervisor/CI.

### 6. Post-Approval Management

#### Ongoing Obligations

**Progress Reports**:
- Annual continuing review (US).
- Annual/final reports (AU/NZ).
- Protocol deviation log.
- Recruitment progress.

**Amendments**:
- **Administrative**: Typographical; contact changes (notification).
- **Minor**: Procedure modifications; eligibility expansion (expedited review).
- **Major**: New intervention; significant risk change (full review).

**Adverse Event Reporting**:

| Event Type | Definition | Reporting Timeline |
|------------|------------|-------------------|
| **SAE** (Serious Adverse Event) | Death; life-threatening; hospitalization; disability | 24-72 hours to sponsor; 24 hours to HREC for related events |
| **UADE** (Unanticipated Adverse Device Effect) | Device-related harm not in IFU | 24 hours to HREC/IRB |
| **SUSAR** (Suspected Unexpected SAR) | Drug-related serious unexpected reaction | 7-15 days per regulatory requirements |
| **Protocol Deviation** | Non-compliance with protocol | Quarterly or per protocol |
| **Breach** | Privacy/confidentiality breach | 72 hours to HREC; immediate remediation |

**Study Closure**:
- Final report within 90 days of completion/termination.
- Return of unused investigational product.
- Data lock and analysis completion.
- Archival of research records (minimum 15 years).

### 7. Study Type Variations

#### Clinical Trials

**Additional Requirements**:
- Clinical trial registration (ANZCTR, ClinicalTrials.gov, EudraCT).
- Trial insurance and injury compensation.
- DSMB for trials with significant risk.
- Safety reporting per ICH-GCP.
- Protocol compliance monitoring.

**IND/CTN Requirements** (AU):
- Clinical Trial Notification (CTN) or Clinical Trial Exemption (CTX).
- TGA approval for unapproved therapeutic goods.

#### Qualitative Research

**Ethical Considerations**:
- Emergent design may limit initial protocol specificity.
- Rapport building vs. therapeutic relationship boundaries.
- Vicarious trauma protection for researchers.
- Sensitive topic handling (abuse, trauma, illegal behaviors).
- Data re-use and secondary analysis consent.

**Consent Nuances**:
- Process consent (ongoing consent throughout).
- Opt-out options for sensitive questions.
- Audio recording consent.
- Anonymization challenges (rich descriptions).

#### Data Linkage and Secondary Data

**Ethical Considerations**:
- Original consent scope assessment.
- Re-identification risk evaluation.
- Data custodian approvals.
- Linkage key security.
- Population-level disclosure risk.

**Waiver Considerations**:
- Public benefit assessment.
- Privacy safeguards.
- Impossibility of re-consent.

#### Biobanking and Genetics

**Specific Issues**:
- Broad consent for future research.
- Return of results policy (incidental findings).
- Data sharing and international transfer.
- Commercialization and benefit sharing.
- Family implications (genetic information).

#### Indigenous and Māori Research

**New Zealand - Te Ara Tika**:
- Whakawhanaungatanga (relationship building).
- Mana (authority and control).
- Tika (ethical correctness).
- Manaakitanga (cultural safety and respect).

**Australia**:
- Aboriginal and Torres Strait Islander research ethics guidelines.
- Community consultation and consent.
- Cultural intellectual property.
- Benefit sharing and capacity building.

## Documentation Requirements

### Ethics Application File

- [ ] Ethics application form (all sections complete).
- [ ] Research protocol (dated; version-controlled).
- [ ] PICF and plain language statement.
- [ ] Recruitment materials.
- [ ] Data collection instruments.
- [ ] Risk assessment and mitigation plan.
- [ ] Privacy and security plan.
- [ ] Investigator CVs and GCP certificates.
- [ ] Conflict of interest declarations.
- [ ] Insurance certificates (if applicable).
- [ ] Site authorization documentation.
- [ ] Consultation documentation (Indigenous/Māori/Pacific).
- [ ] DSMB charter (if required).

### Ongoing Study File

- [ ] Ethics approval letter and clearance number.
- [ ] Approved protocol and PICF (master file).
- [ ] Amendment documentation and approvals.
- [ ] Adverse event log and reports.
- [ ] Protocol deviation log.
- [ ] Informed consent forms (signed).
- [ ] Safety reports and DSMB minutes.
- [ ] Progress reports to HREC/IRB.
- [ ] Site monitoring reports.

### Study Closure File

- [ ] Final study report.
- [ ] Final safety summary.
- [ ] Publication plan and acknowledgments.
- [ ] Data archival and retention plan.
- [ ] Destruction certificates (if applicable).

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **Assuming QI doesn't need ethics** | Some QI meets research definition; requires assessment | Use QI vs. research framework; seek determination from HREC |
| **Insufficient risk assessment** | Underestimating risks leads to inadequate protections | Systematic risk identification; include psychological/social risks |
| **Therapeutic misconception** | Participants conflate research with treatment | Clear distinction in consent; explain uncertainty and purpose |
| **Inadequate consent readability** | High reading level excludes vulnerable populations | Write at grade 6-8; use plain language; test with layperson |
| **Missing vulnerable population safeguards** | Enhanced protections required but omitted | Identify vulnerability; additional consent measures; monitoring |
| **Unclear data sharing plans** | Participants unclear on future use; re-identification risk | Explicit secondary use consent; tiered consent; data governance |
| **No DSMB for high-risk research** | Absence of independent safety monitoring | Establish DSMB for trials with significant risk; clear stopping rules |
| **Late adverse event reporting** | Delays compromise participant safety | 24-72 hour reporting; clear SAE definitions; training |
| **Consent form as information sheet** | Participants sign without reading/comprehending | Separate documents; teach-back; time for questions |
| **Ignoring cultural protocols** | Research fatigue; disrespect; non-participation | Engage Indigenous/Māori/Pacific communities early; follow cultural protocols |

## When to Escalate

Escalate to Chief Investigator, Research Office, or Ethics Committee Chair when:

- Serious adverse event occurs requiring immediate reporting.
- Unanticipated serious risk emerges during study conduct.
- Breach of confidentiality or data security incident.
- Participant complaint that cannot be resolved locally.
- Significant protocol deviation affecting risk-benefit.
- Suspicion of research misconduct or fraud.
- Media or public interest in the research.
- Legal challenge to ethics approval or consent.
- Multi-site dispute on governance or safety.

## Privacy Considerations

- **PHI Involved**: Yes - Research typically involves identifiable health information.
- **Data Minimization**: Collect only data elements required to answer research question.
- **De-identification**: Remove direct identifiers; use codes for linkage; assess re-identification risk.
- **Access Controls**: Role-based access; research team only; audit logs.
- **Storage Security**: Encrypted at rest and in transit; secure servers; password protection.
- **Retention**: Research records retained 15+ years (AU/NZ); secure destruction after period.
- **International Transfer**: Ensure adequacy decisions or standard contractual clauses (GDPR).
- **No Persistence**: Do not store identifiable participant data in chat history or temporary workspaces.
- **Consent for Data Use**: Explicit consent for collection, use, and sharing; right to withdraw data (within limits).

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Standard minimal risk observational study with clear consent process | High | Prepare full application; proceed with standard review |
| Complex interventional trial with vulnerable population | Low | Escalate to Research Office for specialist input; consider external consultant |
| Novel methodology without established precedent | Medium | Pre-submission query to HREC; involve methodology expert |
| Adverse event or safety concern identified | Low | **BLOCKER**: Report immediately; halt enrollment if required; notify HREC within 24-72 hours |
| Ambiguous determination on research vs. QI | Medium | Seek formal determination from HREC Chair; document decision |
| Multi-jurisdictional study with conflicting requirements | Low | Escalate to research governance; engage legal/compliance |
| Consent capacity concerns for participant | Medium | Assess capacity; involve legal representative; flag to HREC |
| Indigenous/Māori/Pacific research without consultation | Low | **BLOCKER**: Halt recruitment; engage communities per cultural protocols; amend protocol |
| Late-breaking amendment affecting risk profile | Medium | Urgent HREC notification; suspend enrollment pending approval |
| Potential conflict of interest identified | Medium | Disclose fully; develop management plan; flag to HREC |

## Tool Requirements

- `~~health/clinical-systems` - For accessing patient data and clinical indicators.
- `~~cloud storage` - For secure document storage and collaboration.
- `~~project tracker` - For ethics application milestones and approval tracking.
- `~~document collaboration` - For multi-investigator protocol development.
- `~~research/clinical-trials` - For trial registration and safety reporting.
- `~~legal/compliance` - For data governance and multi-jurisdictional compliance.

## Success Indicators

You've applied this skill well when:
- [ ] Ethics determination is correct (research vs. QI properly classified).
- [ ] Risk assessment is comprehensive and realistic.
- [ ] Protocol follows scientific and ethical standards.
- [ ] PICF meets readability and content requirements.
- [ ] Consent process supports comprehension and voluntariness.
- [ ] Vulnerable population safeguards are appropriate.
- [ ] Privacy protections are robust and documented.
- [ ] Application is complete and committee-ready.
- [ ] Committee queries are responded to promptly and thoroughly.
- [ ] Post-approval obligations are understood and tracked.
- [ ] Adverse events are reported within required timeframes.
- [ ] Study documentation meets audit standards.

## Related Skills

- `~~health/clinical-ethics` - For clinical ethics consultations distinct from research ethics.
- `~~health/quality-improvement` - For QI projects that may interface with research ethics.
- `~~health/incident-reporting` - For adverse event and safety incident workflows.
- `~~health/clinical-risk-assessment` - For risk management in clinical research.
- `~~bio-research/scientific-problem-selection` - For research design and problem framing.
- `~~legal/compliance` - For governance and regulatory compliance across jurisdictions.
