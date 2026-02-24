---
name: health/policy-development
description: This skill should be used when developing, drafting, or reviewing healthcare organizational policies. Use when a user mentions policy initiation, stakeholder consultation, policy drafting, approval workflows, or review cycles.
version: 1.0.0
---

# Policy Development

Structured guidance for the development, drafting, review, and approval of healthcare organizational policies to ensure clinical safety, regulatory compliance, and operational efficiency.

**Important**: This skill assists with the administrative process of policy development but does not provide legal advice or definitive clinical governance endorsements. All policies must be reviewed by appropriate subject matter experts, legal counsel, and approved by the designated governance authority.

## When to Use This Skill

Invoke when:
- Initiating a new organizational policy in response to regulatory changes or clinical needs.
- Reviewing and updating an existing policy during its scheduled review cycle.
- Drafting policy content based on stakeholder feedback or evidence-based practices.
- Identifying the appropriate approval pathway and governance committee for a policy.
- Managing the consultation process with clinical and administrative stakeholders.
- Ensuring consistency in formatting and structure across organizational policies.

Do not use for clinical procedures (use `~~health/procedure-development`) or specific clinical guidelines (use `~~health/guideline-development`).

## Regulatory Context

| Regulation | Relevance | Key Requirements |
|------------|-----------|------------------|
| **AU/NZ Baseline** | National Safety and Quality Health Service (NSQHS) Standards (AU), Health and Disability Services (Safety) Act 2001 (NZ) | Standard 1: Clinical Governance requires a comprehensive policy framework that is regularly reviewed and aligned with legislative requirements. |
| **US/EU-lite (optional)** | Joint Commission Standards (US), ISO 9001:2015 (Quality Management) | Policies must be accessible, version-controlled, and evidence-based. Specific requirements for document retention and periodic review apply. |

### Jurisdiction-Specific Triggers
- **Australia**: Changes in state-based Health Acts or AHPRA regulations.
- **New Zealand**: Directives from Te Whatu Ora or ManatÅ« Hauora.

## Quick Reference

1.  **Identify Need**: Confirm the gap or trigger requiring a new or updated policy.
2.  **Assign Lead**: Identify the Policy Owner and Lead Author.
3.  **Consult Stakeholders**: Map and engage clinical, operational, and legal experts.
4.  **Draft Content**: Use the standard organizational template.
5.  **Review Phase**: Circulate for feedback and perform impact assessment.
6.  **Approval Workflow**: Submit to the designated governance committee.
7.  **Publish & Communicate**: Upload to the policy portal and notify affected staff.
8.  **Set Review Date**: Typically 2-3 years, or earlier if high-risk.

## Detailed Guidance

### Policy Structure Template
Every healthcare policy should include:
- **Title**: Clear and descriptive.
- **Policy Statement**: Concise declaration of the organization's position.
- **Purpose/Objectives**: Why the policy exists and what it aims to achieve.
- **Scope**: Who and what is covered (e.g., all clinical staff, specific department).
- **Definitions**: Clarification of technical or ambiguous terms.
- **Roles and Responsibilities**: Specific accountabilities for implementation.
- **Principles/Procedures**: High-level rules governing the activity.
- **Monitoring and Evaluation**: How compliance and effectiveness are measured.
- **References**: Evidence base, legislation, and related documents.
- **Version Control**: Tracking of changes and approvals.

### Development Workflow

#### 1. Initiation
- Verify if a similar policy already exists to avoid duplication.
- Determine the policy's impact level (Clinical, Administrative, Strategic).

#### 2. Consultation
- **Clinical**: Ensure frontline clinicians review for practicality.
- **Legal/Risk**: Verify alignment with statutes and insurance requirements.
- **Consumer**: Include patient representatives for person-centered policies.

#### 3. Drafting
- Use the active voice and imperative mood.
- Avoid jargon and keep the language accessible.
- Ensure the policy states "what" is required (leave the "how" for procedures).

#### 4. Approval Pathway
- **Minor/Admin**: Department Head or Director.
- **Clinical**: Clinical Governance Committee / Medical Executive.
- **Organizational**: CEO or Board Risk Sub-committee.

## Documentation Requirements

- [ ] **Policy Draft**: Using the approved organizational template.
- [ ] **Stakeholder Matrix**: List of consulted parties and their feedback.
- [ ] **Impact Assessment**: Evaluation of financial, clinical, and workforce impact.
- [ ] **Committee Minutes**: Record of endorsement and final approval.
- [ ] **Communication Plan**: How the policy will be disseminated.

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| Combining Policy and Procedure | Makes the document too long and difficult to update. | Keep policies high-level and create separate procedures for "how-to" steps. |
| Lack of Version Control | Staff may use outdated or conflicting versions. | Use a centralized repository with clear version numbers and dates. |
| Over-consultation | Leads to "design by committee" and contradictory content. | Set a clear Lead Author and defined consultation window. |
| Ignoring Local Legislation | May lead to legal liability or non-compliance during audits. | Explicitly map policy to relevant AU/NZ or regional statutes. |
| Setting Unrealistic Review Cycles | Leads to a backlog of expired policies. | Set reviews based on risk level (e.g., 1 year for high-risk, 3 for low). |

## When to Escalate

Escalate to the Clinical Governance Lead or Policy Manager when:
- There is a significant conflict between stakeholder feedback that cannot be resolved.
- A proposed policy contradicts national legislation or professional standards.
- A high-risk clinical gap is identified that requires an immediate "Emergency Policy".
- The approval process is delayed beyond the mandatory review date.

## Privacy Considerations

- **PHI involved**: No (usually). Policies should be generic and not contain patient data.
- **Data minimization**: N/A for policy drafting.
- **Retention**: Policies should be archived according to organizational retention schedules (often 7-10 years post-superseding).

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Standard review of a low-risk administrative policy | High | Propose updates based on current standards. |
| Drafting content for a new, complex clinical intervention | Medium | Provide draft framework but require SME input for clinical specifics. |
| Interpretation of conflicting legislative requirements | Low | Draft options and REQUIRE legal/compliance review. |

## Standard and Lite Modes

- **Standard**: Full policy development lifecycle including impact assessment and formal consultation.
- **Lite**: Rapid drafting of memo-style guidance or "preliminary policy position" for urgent feedback.

## Tool Requirements

- `~~cloud storage` - For document repository and version control.
- `~~project tracker` - For workflow tracking and milestone management.
- `~~clinical systems` - To review existing data for evidence-based drafting.

## Success Indicators

You've applied this skill well when:
- [ ] The policy draft follows the 14-section template.
- [ ] Stakeholder feedback has been documented and addressed.
- [ ] The approval pathway is clearly identified.
- [ ] Version control and review dates are assigned.
- [ ] The policy is mapped to AU/NZ regulatory requirements.

## Related Skills

- `~~health/procedure-development` - For documenting the steps to implement policy.
- `~~health/guideline-development` - For evidence-based clinical recommendations.
- `~~health/governance-review` - For evaluating the effectiveness of the policy framework.
