---
name: health/credentialing
description: This skill should be used when verifying the qualifications, experience, and professional standing of healthcare providers. Use when a user mentions provider credentialing, primary source verification, medical license check, board certification, malpractice history, or credentialing committee preparation.
version: 1.0.0
---

# Provider Credentialing

Structured guidance for the verification of healthcare provider qualifications, licenses, and professional background to ensure clinical safety and regulatory compliance.

**Important**: This skill assists with the credentialing process but does not replace the formal review and endorsement by a Credentialing Committee or Medical Executive. All verifications must be performed through authorized primary sources and documented according to organizational and regulatory standards.

## When to Use This Skill

Invoke when:
- Processing initial credentialing applications for new medical, nursing, or allied health staff.
- Conducting periodic re-credentialing reviews for existing staff members.
- Performing Primary Source Verification (PSV) for licenses, degrees, and certifications.
- Coordinating background checks, including criminal history and work rights.
- Reviewing professional indemnity (malpractice) history and current insurance status.
- Preparing documentation and summaries for Credentialing Committee review.
- Identifying missing or expired credentials for a specific provider.

Do not use for general HR onboarding (use `~~productivity/task-management`) or for clinical privilege delineation (use `~~health/privileging`).

## Regulatory Context

| Jurisdiction | Regulator / Statute | Credentialing Standard | Compliance Trigger |
|--------------|---------------------|-----------------------|---------------------|
| **AU/NZ (Baseline)** | AHPRA (AU), Medical Council (NZ) | NSQHS Standard 1 (Clinical Governance) | Appointment, 3-yearly Review, License Expiry |
| **United States (Lite)** | NCQA / Joint Commission | CMS Conditions of Participation | Initial Appointment, Bi-annual Re-appointment |
| **European Union (Lite)** | National Health Boards | Country-specific Medical Acts | Registration Renewal, Post-incident Review |

### AU/NZ Specifics
- **AHPRA (Australian Health Practitioner Regulation Agency)**: Use for real-time license verification in Australia.
- **HPCA (Health Professional Councils Authority)**: For disciplinary history in specific states (e.g., NSW).
- **MCNZ (Medical Council of New Zealand)**: Primary registration body for NZ doctors.

### US/EU-Lite Portability
- When US context is requested, emphasize **NPDB (National Practitioner Data Bank)** checks and **AMA/AOI** profile verifications.
- When EU context is requested, focus on national registration registries and evidence of "Good Standing" from previous jurisdictions.

## Quick Reference

1.  **Verify Identity**: Confirm the provider's legal name and identity documents.
2.  **Verify Registration**: Check the current status and any conditions/restrictions via primary source (e.g., AHPRA).
3.  **Primary Source Verification (PSV)**: Directly verify qualifications (degrees), training, and past employment.
4.  **Check Background**: Coordinate criminal history and working with children/vulnerable people checks.
5.  **Review Indemnity**: Ensure current professional indemnity insurance meets organizational minimums.
6.  **Review Malpractice/Disciplinary**: Check for adverse history or pending investigations.
7.  **Identify Peer Referees**: Obtain and verify references from recent clinical supervisors.
8.  **Prepare Summary**: Create a consolidated profile for committee review.

## Detailed Guidance

### Credentialing Workflow by Provider Type

#### 1. Medical Practitioners (Doctors)
- **Specialty Check**: Verify board certification or fellowship (e.g., RACP, RACS).
- **Scope of Practice**: Ensure the provider's qualifications align with the requested clinical role.
- **Provider Number**: Verify eligibility for Medicare (AU) or health fund billing.

#### 2. Nursing and Midwifery
- **Registration Type**: Registered Nurse (RN), Enrolled Nurse (EN), or Midwife.
- **Endorsements**: Check for specific endorsements (e.g., Nurse Practitioner, Prescribing).

#### 3. Allied Health
- **Accreditation**: Verify registration with the appropriate board (e.g., Physiotherapy Board) or professional association for non-registered roles.

### Primary Source Verification (PSV) Checklist
- [ ] **License**: Real-time check via the regulatory body's online portal.
- [ ] **Qualifications**: Direct contact with the issuing University or use of an authorized verification service (e.g., DataFlow).
- [ ] **Board Certification**: Verification via the relevant Specialty College.
- [ ] **Work History**: Verbal or written confirmation from previous Medical Directors/Department Heads.

## Documentation Requirements

- [ ] **Current License**: Copy of the primary source verification record.
- [ ] **Qualification Records**: Verified copies of all relevant degrees/certifications.
- [ ] **Insurance Certificate**: Current Professional Indemnity Insurance (PII) policy.
- [ ] **Referee Reports**: At least two verified peer references.
- [ ] **Background Checks**: Current National Police Check and Working with Children check.
- [ ] **Credentialing Summary**: A standard profile sheet for the committee.

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| Accepting copies of documents as "verified" | Increases risk of fraudulent or modified qualifications. | Always perform Primary Source Verification (PSV). |
| Relying on provider-supplied CV only | Employment dates and roles may be inaccurate or exaggerated. | Verify work history directly with past employers. |
| Missing license conditions/restrictions | A provider may be "Registered" but not allowed to perform certain tasks. | Check the "Conditions" and "Undertakings" sections of the registry carefully. |
| Neglecting to check the NPDB (US) or equivalent | May miss critical disciplinary or malpractice history from other jurisdictions. | Perform a comprehensive adverse history check. |
| Delaying re-credentialing | Leads to providers working with expired credentials, creating legal and safety risk. | Set alerts 6 months prior to expiry. |

## When to Escalate

Escalate to the Medical Director or Chief Medical Officer (CMO) when:
- A primary source verification reveals a discrepancy or potential fraud.
- A provider is found to have an active restriction or suspension on their license.
- A background check returns a relevant criminal conviction.
- Peer references raise significant concerns about clinical competency or professional conduct.
- A provider refuses to supply mandatory documentation or authorization for verification.

## Privacy Considerations

- **PHI involved**: No (Provider Data, not Patient Data).
- **Sensitive PII**: Yes. Credentialing files contain highly sensitive personal information (DOB, home address, criminal history).
- **Data minimization**: Only share provider data with authorized personnel (HR, Credentialing Committee).
- **De-identification**: Not usually applicable, as verification is person-specific.
- **Retention**: Follow organizational policy for personnel files (often 7-10 years post-resignation).

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| AHPRA search returns clear match with no conditions | High | Proceed with summary preparation. |
| Primary Source reports a name mismatch or date discrepancy | Medium | Flag for investigation; request explanation from provider. |
| Discovery of a previously undisclosed disciplinary action | Low | Escalate immediately to Medical Executive. |

## Standard and Lite Modes

- **Standard**: Full credentialing lifecycle including multi-source PSV and committee summary.
- **Lite**: Rapid "Spot Check" of a provider's current registration status and expiration dates.

## Tool Requirements

- `~~health/clinical-systems` - For clinician profile access.
- `~~health/regulatory-registries` - Links to AHPRA, MCNZ, etc.
- `~~project tracker` - For managing the verification workflow and follow-ups.
- `~~secure storage` - For storing verified documentation.

## Success Indicators

You've applied this skill well when:
- [ ] Every qualification has a corresponding primary source verification record.
- [ ] Current registration status and conditions are accurately documented.
- [ ] Adverse history (if any) is clearly identified and summarized.
- [ ] Professional indemnity status is verified.
- [ ] The credentialing file is complete and audit-ready.

## Related Skills

- `~~health/privileging` - To delineate the specific tasks the provider is authorized to perform.
- `~~health/incident-reporting` - To review a provider's history of adverse clinical events.
- `~~health/governance-review` - For the oversight of the credentialing framework.
