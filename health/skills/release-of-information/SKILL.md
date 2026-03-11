---
name: health/release-of-information
description: This skill should be used when processing requests for the release of patient health information (ROI). Use when a user mentions ROI requests, medical record requests, information disclosure, authorization validation, minimum necessary standard, or patient access rights.
version: 1.0.0
---

# Release of Information (ROI)

Structured guidance for processing requests to release patient health information, ensuring legal compliance, authorization validation, and adherence to the "Minimum Necessary" principle.

**Important**: This skill supports healthcare information management (HIM) workflows. It does not replace legal advice or organization-specific privacy policies. All disclosures must comply with relevant jurisdiction-specific health privacy laws (e.g., Privacy Act in AU/NZ, HIPAA in US).

## When to Use This Skill

Invoke when:
- A patient or their authorized representative requests access to medical records.
- A third party (e.g., lawyer, insurer, government agency) submits a request for health information.
- Validating the sufficiency of a signed authorization or consent for disclosure.
- Determining the specific data elements to be released under the "Minimum Necessary" standard.
- Documenting an accounting of disclosures for a patient record.
- Responding to subpoenas or court orders for medical records.

Do not use for internal clinical use of records (covered by treatment relationship) or for managing clinical consent for procedures (use `~~health/consent-management`).

## Operating Modes

### Standard Mode
Full ROI governance workflow:
- Formal validation of the request and authorization.
- Comprehensive "Minimum Necessary" analysis.
- Detailed accounting of disclosure documentation.
- Compliance check against jurisdiction-specific timelines and requirements.
- Final quality review before release.

### Lite Mode
Use for rapid screening or preliminary request intake:
- Quick checklist for request completeness.
- Identification of immediate missing requirements (e.g., missing signature).
- High-level categorization of request type.

Lite mode is for initial triage only and must be followed by a Standard assessment before any information is actually released.

## Regulatory Context

Default jurisdiction is Australia/New Zealand. Use US/EU-lite framing only when explicitly requested.

| Jurisdiction | Framework/Statute | Disclosure Trigger | Processing Timeline | Required Artifacts | Escalation Point |
|---|---|---|---|---|---|
| Australia | Privacy Act 1988 (Cth), APP 12, State Health Records Acts | Written request, valid authorization, legal order | 30 days (typical) | Validated request, Disclosure log, Receipt | Privacy Officer, HIM Manager |
| New Zealand | Health Information Privacy Code 2020 | Written request, proof of identity, legal order | 20 working days | Request record, Decision letter, Disclosure log | Privacy Officer, HIM Manager |
| United States (lite) | HIPAA Privacy Rule (45 CFR 164.524) | Written request, valid authorization | 30 days (plus 30-day extension) | HIPAA-compliant authorization, Disclosure log | Privacy Officer, Compliance Office |
| European Union (lite) | GDPR Article 15 (Right of Access) | Subject Access Request (SAR) | 1 month | Identity verification, Disclosure record | Data Protection Officer (DPO) |

## Quick Reference

1. **Verify Request Integrity**: Is it in writing? Is identity confirmed? Is the scope clear?
2. **Validate Authorization**: Is it signed by the patient or legal representative? Is it current? Does it cover the requested scope?
3. **Apply Minimum Necessary**: Identify only the specific data points required to satisfy the request.
4. **Redact Non-Disclosable Data**: Remove third-party info, sensitive notes (if legally permitted), and out-of-scope data.
5. **Final Review**: Confirm the package matches the authorization exactly.
6. **Document Disclosure**: Record who, what, when, where, and why in the accounting of disclosures.

## ROI Processing Framework

### 1. Authorization Validation Checklist

Before processing, every request must pass these gates:
- [ ] **Identity Proof**: Copy of ID or signature match on file.
- [ ] **Authority**: If not the patient, is there a valid Power of Attorney (POA) or Guardianship order?
- [ ] **Date**: Is the authorization signed within the last 12 months (or local requirement)?
- [ ] **Scope**: Does the authorization explicitly name the data types (e.g., "Radiology reports only")?
- [ ] **Recipient**: Is the person/entity receiving the info clearly identified?
- [ ] **Purpose**: Is the reason for disclosure stated?

### 2. "Minimum Necessary" Analysis

For every disclosure, identify the smallest data set that fulfills the request:

| Request Type | Typical Minimum Necessary | Over-Disclosure Risk (Avoid) |
|---|---|---|
| Specialist Referral | Recent relevant notes, results, current meds, allergies | Entire historical record |
| Insurance Claim | Specific date range or incident-related records | Unrelated psychiatric or sexual health history |
| Legal Subpoena | Items explicitly listed in the schedule | Records outside the specified date range |
| Patient Personal Access | Full record (subject to legal exclusions) | N/A (unless harm likely) |

## Documentation Standards

### Accounting of Disclosures Entry

| Field | Requirement |
|---|---|
| Date of Disclosure | Exact date information was sent |
| Recipient Name/Address | Specific entity and person receiving information |
| Description of Info | Detailed list (e.g., "ED Summary 12/01/26, Bloods 14/01/26") |
| Basis for Disclosure | (e.g., "Patient Auth #123", "Subpoena #XYZ") |
| Disclosing Officer | Name/Role of person who processed the ROI |

## Security & Privacy (PHI/PII Guardrails)

- **Strict Minimum Necessary**: Always default to the narrowest interpretation of the request unless authorized otherwise.
- **Redaction Protocol**: Ensure third-party information (e.g., names of family members mentioned in notes) is redacted unless they are part of the clinical record.
- **De-identification for Triage**: When discussing requests in the agent, never include the patient's name, DOB, or MRN. Use `[Patient Request A]`.
- **Secure Delivery**: Guidance must assume information is delivered via encrypted channels or secure portal, never via unencrypted email.

## Confidence Indicators

| Scenario | Confidence | Action |
|---|---|---|
| Standard request with clear, valid patient authorization | High | Propose processing steps and document package content |
| Third-party request with questionable or expired authorization | Medium | Flag as "Authorization Deficient" and request updated documentation |
| Legal subpoena with broad schedule or conflicting dates | Medium | Propose draft response; request HIM Manager review |
| Request involves "Sensitive Information" (HIV, psych, DV) without specific auth | Low | Escalate to Privacy Officer immediately; do not process |
| Ambiguous relationship (e.g., separated parent requesting child records) | Low | Escalate to HIM Manager or Legal; verify custody/access rights |

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---|---|---|
| Releasing the "Whole Chart" by default | Violates Minimum Necessary principle and jurisdiction-specific privacy laws | Select only the specific records required for the purpose |
| Accepting digital signatures without verification | Increases risk of fraudulent requests and data breach | Verify against local policy (e.g., e-signature platform cert or phone verification) |
| Failing to document the disclosure in the log | Makes it impossible to audit what was sent or respond to patient accounting requests | Log every external disclosure immediately upon completion |
| Including third-party information in the release | Violates the privacy of individuals other than the patient | Redact any information that identifies non-clinical third parties |
| Missing legal hold flags | Releasing records that are under legal hold may interfere with litigation | Check the Legal Hold status in the HIM system before every ROI |

## When to Escalate

- **Red (Extreme)**: Request for records involving high-profile individuals, staff members, or active litigation against the organization.
- **Sensitive Content**: Records involving domestic violence, child protection, or highly sensitive psychiatric history where release may cause harm.
- **Legal Conflict**: Subpoenas that conflict with patient privacy rights or organizational policy.
- **Bulk Requests**: Unusually large requests or "fishing expeditions" from third parties.

## Tool Requirements

- `~~health/him-system` (e.g., Epic ROI, Cerner HIM) for record retrieval and logging.
- `~~project tracker` (Jira/ServiceNow) for request tracking and status.
- `~~health/id-verification` for verifying patient/representative identity.

## Success Indicators

- [ ] Request integrity and identity are verified.
- [ ] Authorization scope and validity are confirmed.
- [ ] Minimum Necessary analysis is documented.
- [ ] Jurisdiction-specific timelines are identified.
- [ ] Accounting of disclosure entry is prepared.
- [ ] Redaction requirements are flagged.

## Related Skills

- `~~health/consent-management` for managing the underlying consents.
- `~~health/incident-reporting` for reporting ROI-related privacy breaches.
- `~~legal/compliance` for broader privacy regulation mapping.

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-02-12 | Initial ROI skill with authorization validation and Minimum Necessary framework |
