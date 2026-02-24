---
name: prepare-report
description: Initiate preparation of medicolegal documents including expert witness reports, child protection notifications, affidavits, IME reports, and capacity assessments. Interactive command guides selection of document type, jurisdiction, and generates appropriate templates.
---

# /prepare-report

Initiates a structured workflow for preparing medico-legal documents, guiding clinicians and legal teams through document type selection, jurisdiction-specific requirements, and appropriate template generation. This command integrates with the health-medicolegal skills ecosystem to provide context-aware guidance for child protection reports, affidavits, expert witness statements, and other court-directed medical documentation.

**Prerequisites**: 
- Active patient/client file or case context
- Understanding of document purpose and legal context
- Jurisdiction identification

## When to Use This Command

Use `/prepare-report` when you need to:
- Draft a new medico-legal report or expert witness statement
- Prepare a child protection notification or mandatory report
- Create an affidavit or sworn statement for court proceedings
- Conduct an independent medical examination (IME) and draft the report
- Prepare a capacity assessment or guardianship report
- Document a reportable death for coronial purposes
- Respond to a subpoena with authenticated records

## Arguments

### document_type
The type of medico-legal document to prepare.

**Type**: `choice`

**Required**: Yes

**Options**:
| Value | Description | Typical Use Case |
|-------|-------------|------------------|
| `expert-witness` | Expert witness report for court proceedings | Litigation; personal injury; family court |
| `child-protection` | Child protection notification/report | Mandatory reporting; risk assessment |
| `affidavit` | Sworn affidavit or statutory declaration | Court proceedings; evidence authentication |
| `ime` | Independent medical examination report | Workers compensation; personal injury |
| `capacity` | Capacity assessment report | Guardianship; power of attorney; consent |
| `coronial` | Coronial report for reportable death | Death notification; autopsy findings |
| `records-auth` | Medical records authentication affidavit | Subpoena response; litigation support |
| `forensic` | Forensic medical examination report | Sexual assault; physical assault documentation |

**Example**: `/prepare-report document_type=expert-witness`

### jurisdiction
The legal jurisdiction governing the document requirements.

**Type**: `choice`

**Required**: Yes

**Options**:
| Value | Description | Default Context |
|-------|-------------|-----------------|
| `au-federal` | Australian Federal Court | Federal litigation |
| `au-nsw` | New South Wales | State court matters |
| `au-vic` | Victoria | State court matters |
| `au-qld` | Queensland | State court matters |
| `au-wa` | Western Australia | State court matters |
| `au-sa` | South Australia | State court matters |
| `au-tas` | Tasmania | State court matters |
| `au-act` | Australian Capital Territory | Territory matters |
| `au-nt` | Northern Territory | Territory matters |
| `nz` | New Zealand | NZ court matters |
| `us-federal` | United States Federal | Federal court |
| `us-state` | US State (specify in notes) | State-specific |
| `eu` | European Union member state | Cross-border proceedings |

**Example**: `/prepare-report document_type=expert-witness jurisdiction=au-nsw`

### urgency
The urgency level affecting preparation timeline and review requirements.

**Type**: `choice`

**Required**: No

**Default**: `standard`

**Options**:
| Value | Timeline | Review Requirements |
|-------|----------|---------------------|
| `routine` | Standard preparation | Normal legal review |
| `standard` | 2-4 weeks | Standard legal review |
| `priority` | 1-2 weeks | Expedited review |
| `urgent` | 3-7 days | Senior review required |
| `critical` | <48 hours | Immediate escalation |

**Example**: `/prepare-report urgency=priority`

### mode
The operating mode for document preparation complexity.

**Type**: `choice`

**Required**: No

**Default**: `standard`

**Options**:
| Value | Complexity | Appropriate For |
|-------|------------|-----------------|
| `lite` | Streamlined | Simple cases; clear facts; preliminary opinions |
| `standard` | Comprehensive | Most litigation; contested matters |
| `forensic` | Full forensic | Complex cases; high stakes; criminal matters |

**Example**: `/prepare-report mode=standard`

### case_context
Brief description of the case context (no PHI/PII).

**Type**: `string`

**Required**: No

**Guidelines**:
- Do not include patient names, dates of birth, or other identifying information
- Describe matter type (e.g., "personal injury MVA", "child protection concern", "guardianship application")
- Include relevant timeframe (e.g., "incident 6 months ago")

**Example**: `/prepare-report case_context="Personal injury matter, motor vehicle accident, lumbar spine injury"`

## Interactive Workflow

### Step 1: Document Type Selection

The command will prompt for document type if not provided:

```
What type of medico-legal document do you need to prepare?

1. Expert Witness Report - For court proceedings; litigation support
2. Child Protection Report - Mandatory reporting; risk assessment
3. Affidavit - Sworn statement for court
4. IME Report - Independent medical examination
5. Capacity Assessment - Decision-making capacity evaluation
6. Coronial Report - Death notification/report
7. Records Authentication - Authenticate medical records
8. Forensic Report - Assault/sexual assault documentation

Enter your choice (1-8):
```

### Step 2: Jurisdiction Selection

Based on document type, relevant jurisdictions are presented:

```
Select the applicable jurisdiction:

[AU/NZ Jurisdictions]
- Australian Federal Court
- New South Wales
- Victoria
- Queensland
- [Other states...]
- New Zealand

[International]
- US Federal
- US State (specify)
- European Union

Enter jurisdiction:
```

### Step 3: Context Gathering

The command gathers essential context (without PHI):

```
Please provide case context (do not include patient names or identifying information):

- Matter type: [e.g., personal injury, child protection, family law]
- Brief factual background: [injury mechanism, concerns identified]
- Current stage: [pre-litigation, active litigation, hearing pending]
- Special considerations: [urgent safety concerns, complex issues]
```

### Step 4: Template Generation

Based on selections, the command generates:

1. **Document Structure**: Jurisdiction-specific template with required sections
2. **Checklist**: Pre-submission checklist for document type
3. **Timeline**: Key dates and deadlines for preparation and filing
4. **Review Points**: Critical review requirements before finalization
5. **Skill Invocation**: Relevant skills loaded (`~~health/medicolegal-reports`, `~~health/child-protection`, `~~health/affidavit-drafting`)

## Generated Templates

### Expert Witness Report Template (Australia)

```markdown
# EXPERT WITNESS REPORT

## Court: [Federal/State] Court of [Jurisdiction]
## Matter: [Case Name]
## Case Number: [XXXX/YYYY]
## Date of Report: [DATE]

---

### 1. QUALIFICATIONS AND INSTRUCTIONS

#### 1.1 Professional Qualifications
- Name: [Full Name]
- Qualifications: [Degrees, Fellowships]
- Current Position: [Title, Institution]
- Relevant Experience: [X years in specialty]

#### 1.2 Instructions Received
- Engaged by: [Party/Lawyer]
- Date of Instructions: [Date]
- Scope of Instructions: [Specific questions to address]
- Documents Provided: [List of materials reviewed]

#### 1.3 Conflict of Interest Declaration
- [ ] No conflicts of interest identified
- [ ] Conflicts disclosed: [Details]

#### 1.4 Expert Duty Declaration
I understand that my primary duty is to the Court and I have complied with 
the Expert Witness Code of Conduct.[Cite applicable rules]

---

### 2. BACKGROUND AND HISTORY

#### 2.1 Sources of Information
[Document interviews, records reviewed, investigations]

#### 2.2 Chronological History
[Present relevant medical history chronologically]

#### 2.3 Current Complaints
[Document current symptoms and functional impact]

---

### 3. EXAMINATION FINDINGS

#### 3.1 Clinical Examination
[Objective findings from physical examination]

#### 3.2 Investigation Results
[Relevant imaging, pathology, other investigations]

---

### 4. OPINION

#### 4.1 Causation
[Opinion on relationship between incident and condition]

#### 4.2 Diagnosis and Prognosis
[Current diagnosis; expected trajectory]

#### 4.3 Treatment and Rehabilitation
[Future treatment needs and associated costs]

#### 4.4 Addressing Contrary Views
[Consider and respond to alternative explanations]

---

### 5. CONCLUSIONS

[Concise summary of key opinions]

---

**I declare that I have made all the inquiries that I believe are desirable 
and appropriate, and that no matters of significance have been withheld 
from the Court.**

**Signed:** _________________________
**Date:** _________________________
**Name:** [Full Name]
```

### Child Protection Notification Template (Australia)

```markdown
# CHILD PROTECTION NOTIFICATION

## Jurisdiction: [State/Territory] Child Protection Services
## Date of Notification: [DATE]
## Notification Type: [Mandatory/Voluntary]

---

### 1. CHILD IDENTIFICATION

- Full Name: [As provided]
- Date of Birth: [DOB]
- Address: [Current address]
- School/Childcare: [Institution name]
- Cultural Background: [Aboriginal/Torres Strait Islander status if known]

---

### 2. NOTIFICATION DETAILS

#### 2.1 Nature of Concerns
- Type: [Physical abuse/Sexual abuse/Emotional abuse/Neglect]
- Specific Indicators: [Detailed description of observations/disclosures]
- Timeline: [When concerns identified; duration]

#### 2.2 Source of Information
- Who provided information: [Child/Parent/Professional/Other]
- How concerns came to light: [Context of disclosure/observation]

---

### 3. RISK ASSESSMENT

#### 3.1 Risk Factors Present
- [List specific risk factors identified]

#### 3.2 Protective Factors
- [List protective factors identified]

#### 3.3 Immediate Safety Concerns
- [ ] No immediate safety concerns
- [ ] Immediate safety concerns: [Details]

---

### 4. ACTIONS TAKEN

- Medical treatment provided: [Details]
- Safety planning: [Actions taken]
- Agencies notified: [Police, other services]
- Family involvement: [How family was engaged]

---

### 5. CONTACT DETAILS

**Reporter:**
- Name: [Name]
- Position: [Title]
- Organization: [Institution]
- Phone: [Contact number]
- Available for follow-up: [Yes/No]

---

**This notification is made under [relevant legislation section].**
**I believe on reasonable grounds that [child] is at risk of [significant harm/harm].**
```

### Affidavit Template

```markdown
# AFFIDAVIT

## Court: [Court Name]
## Matter: [Case Name] v [Case Name]
## Case Number: [XXXX/YYYY]
## Affidavit of: [Deponent Full Name]

---

I, [FULL NAME], of [ADDRESS], [OCCUPATION], make oath/affirm and say as follows:

### 1. INTRODUCTION

1. I am a [registered medical practitioner/clinical psychologist/other] with 
   [X] years of post-graduate experience in [specialty area].

2. [Statement of how deponent has knowledge of facts]

3. The facts stated in this affidavit are within my personal knowledge, 
   except where stated to be on information and belief, in which case I 
   believe them to be true.

---

### 2. BACKGROUND

4. [Chronological statement of relevant facts]

5. [Continue with numbered paragraphs, one fact per paragraph where possible]

---

### 3. EXPERT OPINION (if applicable)

6. Based on my examination/review, I form the following opinions:

7. [Opinion 1]: [Statement of opinion with foundation]

8. [Opinion 2]: [Statement of opinion with foundation]

---

### 4. EXHIBITS

9. The documents annexed hereto and marked ["A", "B", etc.] are true copies 
   of [description].

---

**Sworn/Affirmed at:** _________________________

**On:** _________________________

**Signature of Deponent:** _________________________

---

**Before me:**

**[Authorized Witness Name]**
**[Capacity - Justice of the Peace/Solicitor/Notary Public]**

**Signature of Witness:** _________________________
```

## Pre-Submission Checklists

### Expert Witness Report Checklist
- [ ] Report complies with applicable court rules
- [ ] Expert qualifications clearly stated and relevant
- [ ] Instructions and scope clearly documented
- [ ] Conflict of interest disclosure complete
- [ ] Duty to court acknowledged
- [ ] All opinions supported by stated facts and reasoning
- [ ] Alternative explanations addressed
- [ ] Technical terms defined
- [ ] Exhibits properly referenced and attached
- [ ] Legal counsel has reviewed report
- [ ] Truth declaration included

### Child Protection Checklist
- [ ] Child's details accurate and complete
- [ ] Nature of concerns clearly described
- [ ] Exact words of child recorded (if disclosed)
- [ ] Risk assessment completed
- [ ] Immediate safety concerns addressed
- [ ] Actions taken documented
- [ ] Reporter contact details provided
- [ ] Notification made within required timeframe
- [ ] Follow-up plan established
- [ ] Documentation filed securely

### Affidavit Checklist
- [ ] Proper court form and formatting used
- [ ] Deponent details accurate
- [ ] All statements true to best of knowledge
- [ ] Personal knowledge distinguished from information/belief
- [ ] Facts presented in logical order
- [ ] Exhibits properly labeled and referenced
- [ ] No legal arguments or conclusions included
- [ ] Jurat completed by authorized witness
- [ ] Sworn/affirmed properly
- [ ] Filed and served within deadlines

## Examples

### Example 1: Expert Witness Report

```
User: /prepare-report document_type=expert-witness jurisdiction=au-nsw 
       case_context="Personal injury, workplace fall, lumbar spine injury" 
       urgency=standard

Claude: I'll help you prepare an expert witness report for this NSW personal 
injury matter. Let me generate the appropriate template and checklist.

[Generated template with NSW-specific requirements]

Key NSW Requirements:
- UCPR Schedule 7 Expert Witness Code of Conduct applies
- Report must comply with Practice Note SC Gen 11
- 28-day service deadline typical unless ordered otherwise
- Concurrent expert evidence may be ordered

Would you like me to load the detailed ~~health/medicolegal-reports skill 
for comprehensive guidance on report preparation?
```

### Example 2: Child Protection Report

```
User: /prepare-report document_type=child-protection jurisdiction=au-vic 
       urgency=urgent

Claude: I'll help you prepare a child protection notification for Victoria. 
Given the urgent priority, immediate reporting is required.

[Generated template with VIC-specific requirements]

URGENT VIC Requirements:
- Report to DHHS Child Protection immediately for urgent cases
- After-hours: 13 12 78
- Reasonable belief threshold applies
- Mandatory reporter status confirmation required

CRITICAL: If there are immediate safety concerns, phone Child Protection 
NOW before completing written notification.

Would you like me to load the ~~health/child-protection skill for detailed 
guidance on mandatory reporting requirements?
```

### Example 3: Affidavit

```
User: /prepare-report document_type=affidavit jurisdiction=nz 
       case_context="Family Court parenting matter, capacity assessment" 
       mode=standard

Claude: I'll help you prepare an affidavit for the NZ Family Court. Let me 
generate the appropriate template with NZ-specific requirements.

[Generated template with NZ-specific requirements]

Key NZ Requirements:
- Family Court affidavit requirements apply
- Affidavit of service may be required
- Swearing before Justice of the Peace, Solicitor, or Registrar
- High Court Rules apply for formatting

Would you like me to load the ~~health/affidavit-drafting skill for 
detailed guidance on affidavit preparation?
```

## Error Handling

### Missing Required Arguments

If `document_type` or `jurisdiction` is not provided:

```
Error: Required argument 'document_type' not provided.

Please specify the document type:
- expert-witness: Expert witness report for court
- child-protection: Child protection notification  
- affidavit: Sworn affidavit for court
- ime: Independent medical examination report
- capacity: Capacity assessment report
- coronial: Coronial report
- records-auth: Records authentication
- forensic: Forensic medical report

Usage: /prepare-report document_type=<type> jurisdiction=<jurisdiction>
```

### Invalid Combinations

Some document types may have limited jurisdiction support:

```
Warning: Document type 'coronial' has specific requirements that vary 
significantly by jurisdiction. Please confirm:
- State/Territory specific Coroners Act applies
- Immediate notification requirements may apply
- Death must be reportable under applicable legislation

Would you like to proceed with [jurisdiction] template?
```

### PHI/PII Detection

If potentially identifying information is detected in case_context:

```
Warning: The case_context may contain personally identifiable information.

Please revise case_context to exclude:
- Patient/client names
- Dates of birth
- Medical record numbers
- Addresses or specific locations
- Other identifying details

Example acceptable format: "Personal injury matter, motor vehicle accident, 
lumbar spine injury, 6 months post-incident"
```

## Integration with Skills

This command automatically invokes relevant skills based on document type:

| Document Type | Primary Skill | Secondary Skills |
|---------------|---------------|------------------|
| expert-witness | `~~health/medicolegal-reports` | `~~health/clinical-documentation` |
| child-protection | `~~health/child-protection` | `~~health/medicolegal-reports` |
| affidavit | `~~health/affidavit-drafting` | `~~health/medicolegal-reports` |
| ime | `~~health/medicolegal-reports` | `~~health/clinical-documentation` |
| capacity | `~~health/medicolegal-reports` | `~~health/mental-health-assessment` |
| coronial | `~~health/medicolegal-reports` | `~~health/forensic-examination` |
| records-auth | `~~health/affidavit-drafting` | `~~health/clinical-documentation` |
| forensic | `~~health/medicolegal-reports` | `~~health/forensic-examination` |

## Success Indicators

The command has successfully initiated report preparation when:
- [ ] Appropriate template generated with jurisdiction-specific requirements
- [ ] Document type matches the intended legal purpose
- [ ] Pre-submission checklist provided for document type
- [ ] Key deadlines and timeframes identified
- [ ] Relevant skills loaded for detailed guidance
- [ ] No PHI/PII detected in provided context
- [ ] User understands next steps in preparation workflow

## Related Commands

- `/initiate-incident-report` - For clinical incident reporting (internal)
- `/generate-certificate` - For statutory medical certificates
- `/request-records` - For accessing medical records for report preparation
- `/consult-legal` - For engaging legal counsel review (conceptual)
