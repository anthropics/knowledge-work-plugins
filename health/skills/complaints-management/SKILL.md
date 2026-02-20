---
name: health/complaints-management
description: This skill should be used when managing patient, staff, or visitor complaints in a healthcare setting. Use when triaging, investigating, or resolving complaints, distinguishing between clinician conduct and service delivery issues.
version: 1.0.0
---

# Complaints Management

An expert framework for handling healthcare complaints with a focus on patient safety, clinical governance, and regulatory compliance. This skill ensures that every complaint is handled systematically, maintaining the delicate balance between service recovery and professional accountability.

## When to Use This Skill

Invoke this skill when:
- A new patient, family, or staff complaint is received.
- Triaging issues to determine if they involve clinical safety (clinical governance) or service quality (administration).
- Drafting investigation plans for formal complaints.
- Assessing the severity of an incident reported as a complaint.
- Preparing formal responses to complainants or regulators (e.g., AHPRA, Health Care Complaints Commission).
- Mapping complaints to jurisdictional requirements (AU/NZ default).

## Quick Reference

1. **Safety First**: Immediately check if the complaint implies an ongoing risk to patient safety.
2. **Categorize**: Determine if the complaint is **Clinician-focused** (conduct/competence) or **Service-focused** (systems/facilities).
3. **Assign Severity**: Use the P1-P4 healthcare framework (P1 = Immediate safety/legal risk).
4. **Identify Persona**: Tailor the workflow for the user (e.g., Patient Experience Officer vs. Head of Department).
5. **Protect PHI**: Never log patient names or specific identifiers in the chat history.
6. **Timeline Check**: Verify jurisdictional deadlines (e.g., 2-day acknowledgment, 30-day resolution).

## Operating Modes

### Standard Mode
Full clinical governance and compliance workflow. Requires complete evidence capture, stakeholder mapping, and adherence to formal regulatory timelines. Use for all formal written complaints.

### Lite Mode
Minimal safe guidance for "on-the-spot" resolution or informal verbal feedback. Focuses on immediate service recovery while still enforcing high-risk escalation triggers. Never suppresses clinical safety reporting.

## Detailed Guidance

### 1. Triage & Categorization

Every complaint must be assigned a primary type to drive the investigation path.

| Type | Focus | Investigation Path |
|------|-------|--------------------|
| **Clinician** | Performance, conduct, communication, competence | Clinical Lead / Medical Director / Nursing Director |
| **Service/Systems** | Facilities, wait times, access, billing, admin | Operations Manager / Patient Experience Team |
| **Privacy/Data** | Breach of confidentiality, unauthorized access | Privacy Officer / Health Information Manager |

### 2. Severity Framework (Healthcare Adaptation)

| Priority | Criteria | SLA (Acknowledgment) | SLA (Resolution) |
|----------|----------|----------------------|------------------|
| **P1 - Critical** | Direct threat to life, serious harm, major legal/media risk, mandatory reporting trigger | 2 Hours | 24-48 Hours |
| **P2 - High** | Clinical error with no harm, significant delay in care, high-value account/stakeholder | 4 Hours | 7 Days |
| **P3 - Medium** | Communication breakdown, minor service delay, facility issues | 1 Business Day | 30 Days |
| **P4 - Low** | General feedback, minor inconvenience, feature requests | 2 Business Days | 60 Days |

### 3. Investigation Workflow

#### Phase A: Fact Gathering
- **Record Review**: Access the clinical record via `~~clinical systems` (e.g., FHIR).
- **Staff Interviews**: Identify involved parties and request statements.
- **Timeline Construction**: Create a "source-of-truth" chronology.

#### Phase B: Analysis
- **Root Cause Analysis (RCA)**: Use for P1/P2 complaints to identify systemic failures.
- **Human Factors**: Consider fatigue, environment, and communication tools.

#### Phase C: Resolution
- **Open Disclosure**: If harm occurred, trigger the formal Open Disclosure process.
- **Service Recovery**: Propose tangible remediation (e.g., apology, billing adjustment, process change).

## Jurisdiction & Regulatory Context

### Australia & New Zealand (Default)
- **Australia**: Align with the *Australian Charter of Healthcare Rights* and state-based commissions (e.g., HCCC in NSW, OHHO in QLD).
- **New Zealand**: Align with the *Code of Health and Disability Services Consumers' Rights* and the HDC.
- **Mandatory Reporting**: Trigger AHPRA (AU) or Medical Council (NZ) notification for serious professional misconduct.

### US/EU-lite Fallback
- **USA**: Reference HIPAA privacy rules and CMS Quality Standards.
- **EU**: Reference GDPR Article 9 (Health Data) and national health acts.

## Confidence Indicators (Clinical Guardrails)

| Scenario | Confidence | Action |
|----------|------------|--------|
| Clear service failure (e.g., cold food) | High | Draft response and suggest immediate remediation. |
| Ambiguous clinical claim (e.g., "wrong dose") | Medium | Flag for Clinical Lead review; do not validate claim without record audit. |
| Allegation of serious harm or misconduct | Low | **BLOCKER**: Escalate to Legal and Executive immediately. Do not draft response. |

## Security & Privacy (PHI Handling)

- **Minimum Necessary**: Only request the specific portions of the clinical record relevant to the complaint.
- **De-identification**: Use tokens like `[Patient A]` or `[Clinician B]` in drafting.
- **No Persistence**: Explicitly remind the user to delete PHI from temporary workspaces after the response is generated.
- **Tool Access**: Only use `~~clinical systems` through authenticated organization-approved MCP gateways.

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| Defensive Tone | Escalates the conflict and reduces trust. | Use empathetic, neutral, and fact-based language. |
| Logging Patient Names | Risk of PHI exposure in LLM training/logs. | Use case IDs or generic identifiers. |
| Bypassing Governance | Clinician complaints handled by admin staff risk missing medical errors. | Always route clinical competence issues to the Medical Director. |
| Missing Deadlines | Jurisdictional regulators may penalize the organization. | Set automated alerts for 30-day windows. |

## Tool Requirements

- `~~clinical systems` (FHIR/HL7) - To verify clinical events and timelines.
- `~~project tracker` (Jira/ServiceNow) - To log and track complaint status.
- `~~cloud storage` (SharePoint) - To store formal investigation statements.
- `~~medical coding` (ICD-10) - To categorize complaints by diagnosis/procedure area.

## Success Indicators

- [ ] Complaint categorized correctly by root cause (Clinician vs. Service).
- [ ] Severity matches jurisdictional patient safety frameworks (e.g., SAC scores).
- [ ] No PHI/PII included in the skill's drafted output.
- [ ] Response includes an explicit apology (where appropriate) without admitting legal liability prematurely.
- [ ] Regulatory reporting triggers are identified and flagged.

## Related Skills

- `~~health/incident-reporting` - For complaints that meet the definition of a clinical incident.
- `~~health/policy-development` - For complaints leading to a change in standard operating procedures.
- `~~customer-support/response-drafting` - For generic communication patterns.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial healthcare adaptation of ticket-triage and escalation patterns. |
