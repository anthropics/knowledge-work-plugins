---
name: health/privileging
description: This skill should be used when defining and managing the clinical scope of practice for healthcare providers. Use when a user mentions clinical privileges, scope of practice delineation, competency verification, proctoring, or privilege renewal.
version: 1.0.0
---

# Clinical Privileging

Structured guidance for the delineation, verification, and monitoring of clinical privileges to ensure that healthcare providers only perform tasks for which they are qualified, competent, and authorized.

**Important**: This skill assists with the privileging process but does not grant clinical authority. All privileges must be recommended by a Department Head and formally approved by the Credentialing Committee or Medical Executive. Clinical competence must be verified through objective evidence and peer review.

## When to Use This Skill

Invoke when:
- Delineating the scope of practice for a new clinical staff member (e.g., medical, nursing, allied health).
- Reviewing and renewing privileges for existing staff members (typically every 2-3 years).
- Evaluating a request for "New Technology" or "Complex Procedure" privileges.
- Documenting competency verification for specific clinical skills (e.g., robotic surgery, advanced life support).
- Coordinating proctoring or supervision requirements for newly appointed staff.
- Identifying the organizational requirements for "Emergency" or "Temporary" privileges.
- Mapping clinical privileges to the available facilities and resources of the organization.

Do not use for initial verification of qualifications (use `~~health/credentialing`) or for managing clinical rosters (use `~~productivity/task-management`).

## Regulatory Context

| Jurisdiction | Regulator / Statute | Privileging Standard | Compliance Trigger |
|--------------|---------------------|----------------------|---------------------|
| **AU/NZ (Baseline)** | ACSQHC / Health Boards | NSQHS Standard 1 (Clinical Governance) | Initial Appointment, Re-appointment, Incident Review |
| **United States (Lite)** | Joint Commission / CMS | MS.06.01.03 (Delineation of Privileges) | Bi-annual Review, New Procedure Request |
| **European Union (Lite)** | National Clinical Leads | Country-specific Safety Codes | Scope of Practice Review, Specialty Transition |

### Jurisdiction-Specific Details
- **AU/NZ**: Use the **ACSQHC Credentialing and Delineating Scope of Practice Guide** as the primary framework.
- **US**: Follow the **OPPE (Ongoing Professional Practice Evaluation)** and **FPPE (Focused Professional Practice Evaluation)** models.

## Quick Reference

1.  **Identify Specialty**: Determine the provider's primary specialty and sub-specialties.
2.  **Select Privilege Set**: Use the standard organizational list for that specialty.
3.  **Verify Competency**: Review logbooks, procedure counts, and outcome data.
4.  **Check Resources**: Ensure the organization has the necessary equipment and staff to support the requested privileges.
5.  **Set Levels**: Delineate between Core (standard) and Special (complex/high-risk) privileges.
6.  **Assign Supervision**: Define proctoring requirements for new or high-risk tasks.
7.  **Obtain Endorsement**: Submit for Department Head and Credentialing Committee sign-off.
8.  **Monitor Performance**: Integrate with the organization's quality and incident monitoring systems.

## Detailed Guidance

### Privilege Delineation Categories

#### 1. Core Privileges
- Standard procedures and patient management tasks expected of any qualified practitioner in that specialty.
- Usually approved based on proof of successful completion of training (e.g., Residency/Fellowship).

#### 2. Special/Enhanced Privileges
- High-risk or complex procedures requiring additional training, certification, or experience (e.g., TAVI, ERCP).
- May require a minimum number of procedures performed in the last 12-24 months.

#### 3. Temporary Privileges
- Granted for a short duration (e.g., 3 months) for locum staff or while a full application is processed.
- Must be supported by a "Clean" primary source check.

#### 4. Emergency Privileges
- Granted during a declared disaster or mass casualty event.
- Allows practitioners to perform tasks outside their normal scope to save life or limb.

### Competency Verification Requirements
Evidence of competency may include:
- **Procedure Logbooks**: Verified counts of successful procedures.
- **Outcome Data**: Readmission rates, complication rates, and mortality data (risk-adjusted).
- **CPD Records**: Continuing Professional Development relevant to the requested privileges.
- **Peer References**: Specific feedback on clinical skill and judgment.

## Documentation Requirements

- [ ] **Privilege Delineation Form**: Signed by the provider and Department Head.
- [ ] **Evidence Dossier**: Procedural logbooks and competency certificates.
- [ ] **Proctoring Reports**: Documentation of supervised cases (if applicable).
- [ ] **OPPE/FPPE Reports**: Periodic performance evaluations.
- [ ] **Renewal Timeline**: Alert for the next review cycle.

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| Granting privileges based on "Years of Experience" only | Experience does not always equate to current competency. | Use objective data like procedure counts and outcome metrics. |
| Neglecting the "Organization Resource" check | Allowing a procedure that the hospital cannot safely support. | Ensure facilities and support staff are available for all approved tasks. |
| Accepting "Vague" Scope of Practice | Leads to confusion and potential safety gaps in the clinical team. | Use specific, action-oriented privilege lists. |
| Failing to monitor "Low Volume" practitioners | Skills degrade if procedures are performed too infrequently. | Set minimum volume requirements or require proctoring after a gap. |
| Ignoring "Near Miss" data during renewal | Misses an opportunity to address emerging clinical risks. | Review incident and complaint history as part of the privileging cycle. |

## When to Escalate

Escalate to the Medical Director or Chief Medical Officer (CMO) when:
- A practitioner requests privileges for which the organization lacks the necessary infrastructure.
- Competency evidence is insufficient or contradictory.
- A practitioner is performing tasks outside their approved scope of practice.
- Monitoring data (OPPE) reveals a significant downward trend in clinical performance.
- There is a dispute between a Department Head and a practitioner regarding scope of practice.

## Privacy Considerations

- **PHI involved**: No (Provider Performance Data).
- **Sensitive PII**: Yes. Peer review and outcome data are highly sensitive and often legally protected from discovery.
- **Data minimization**: Only share performance data with authorized reviewers (e.g., Quality Committee).
- **Retention**: Maintain privileging records for the duration of employment plus 7 years.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Provider requests standard core privileges for their certified specialty | High | Propose endorsement. |
| Request for complex privileges with borderline procedure counts | Medium | Recommend "Focused" review (FPPE) or proctoring period. |
| Clinical outcome data shows significant deviation from peers | Low | REQUIRE immediate human clinical review; do not propose renewal. |

## Standard and Lite Modes

- **Standard**: Full privileging workflow including competency analysis and resource mapping.
- **Lite**: Rapid "Scope Check" to verify if a specific practitioner is authorized for a specific task.

## Tool Requirements

- `~~health/clinical-systems` - For performance and incident data.
- `~~project tracker` - For managing the renewal pipeline.
- `~~secure storage` - For storing peer review and competency evidence.

## Success Indicators

You've applied this skill well when:
- [ ] The scope of practice is clearly defined and specialty-specific.
- [ ] Every "Special" privilege is supported by objective evidence of competency.
- [ ] Facilities and resources have been verified for the requested scope.
- [ ] Proctoring/Supervision requirements are documented where needed.
- [ ] The privileges are mapped to the organization's clinical governance framework.

## Related Skills

- `~~health/credentialing` - The prerequisite verification of identity and training.
- `~~health/incident-reporting` - For the "Post-market" surveillance of clinical performance.
- `~~health/quality-improvement` - For addressing performance gaps identified during privileging.
