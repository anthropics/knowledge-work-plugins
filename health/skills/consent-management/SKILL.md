---
name: health/consent-management
description: This skill should be used when managing patient consent for treatment, research, or information sharing. Use when a user mentions informed consent, consent forms, treatment authorization, advance directives, capacity assessment, proxy decision makers, or withdrawing consent.
version: 1.0.0
---

# Consent Management

Structured guidance for managing informed consent workflows, validating documentation, and ensuring compliance with clinical and ethical standards for patient autonomy.

**Important**: This skill supports clinical and administrative workflows for obtaining and documenting consent. It does not replace the face-to-face informed consent discussion between a clinician and patient. All consent processes must align with local health statutes and organizational policies.

## When to Use This Skill

Invoke when:
- Identifying the correct consent type for a specific clinical procedure or initiative.
- Validating that a consent form is complete and legally sufficient.
- Documenting a patient's withdrawal of consent or change in preferences.
- Identifying requirements for surrogate or proxy decision-makers (e.g., Power of Attorney).
- Reviewing documentation requirements for patients with impaired decision-making capacity.
- Aligning advance directives or living wills with current treatment plans.
- Managing consent for participation in clinical trials or research studies.

Do not use for Release of Information (ROI) processing (use `~~health/release-of-information`) unless specific authorization validation is required as part of the consent check.

## Operating Modes

### Standard Mode
Full consent governance workflow:
- Formal identification of consent type and requirements.
- Detailed validation of documentation and capacity assessment records.
- Verification of proxy/surrogate authority.
- Integration with clinical records and procedure scheduling.
- Compliance check against jurisdiction-specific consent laws.

### Lite Mode
Rapid consent screening (e.g., during emergency intake or high-volume clinics):
- Quick check for presence of signed consent and ID verification.
- Identification of immediate missing fields.
- Flagging for urgent clinician review if capacity or proxy issues are detected.

Lite mode is for initial screening only and does not replace the full clinical validation required before a procedure begins.

## Regulatory Context

Default jurisdiction is Australia/New Zealand. Use US/EU-lite framing only when explicitly requested.

| Jurisdiction | Framework/Statute | Consent Requirement | Required Documentation | Capacity Assessment Trigger | Escalation Point |
|---|---|---|---|---|---|
| Australia | State-based Guardianship Acts, NHMRC National Statement (Research) | Informed consent for all procedures; explicit for high-risk | Signed form, witness (if required), notation in records | Evidence of impaired decision-making | Clinical Lead, Ethics Committee |
| New Zealand | HDC Code of Health and Disability Services Consumers' Rights | Right 7: Right to make an informed choice and give informed consent | Written consent for significant procedures | Reasonable grounds to doubt capacity | Quality Lead, Clinical Governance |
| United States (lite) | State statutes, Joint Commission standards | Patient Self-Determination Act (PSDA) | Consent form, Advance Directive (if present) | Change in mental status | Risk Management, Ethics Consult |
| European Union (lite) | GDPR (for data), national health laws (for clinical) | Informed, explicit, and freely given | Documented consent record | Per national implementation | DPO (for data), Clinical Lead |

## Quick Reference

1. **Identify Consent Type**: Treatment, Surgical/Invasive, Research, Data Sharing, or Advance Directive.
2. **Verify Capacity**: Has the clinician documented that the patient understands the risks, benefits, and alternatives?
3. **Identify Decision-Maker**: The patient, or a legally authorized representative (Proxy/Guardian/Attorney)?
4. **Validate Document**: Check for signature, date, specific procedure name, and risks discussed.
5. **Check for Withdrawal**: Is there any record of the patient revoking this consent?
6. **Final Verification**: Ensure the consent matches the planned clinical action exactly.

## Consent Taxonomy

### 1. Clinical & Treatment Consent

| Type | Description | Documentation Requirement |
|---|---|---|
| **Implied** | Minor, routine procedures (e.g., blood pressure check) | Notation of cooperation in clinical notes |
| **Verbal** | Non-invasive, low-risk procedures (e.g., standard physical exam) | Explicit note: "Patient gave verbal consent after discussion" |
| **Written (Standard)** | Invasive procedures, high-risk medications, sedation | Formal signed consent form detailing specific risks |
| **Written (Specialized)** | Clinical trials, research, organ donation | Specialized IRB-approved forms with extensive disclosure |

### 2. Decision-Making Authority

| Role | Description | Authority Verification |
|---|---|---|
| **Patient** | Competent adult or mature minor | ID verification |
| **Legal Guardian** | Appointed by court/tribunal | Official Guardianship Order |
| **Enduring Power of Attorney** | Appointed by patient while competent | Signed and witnessed EPOA document |
| **Statutory Surrogate** | Next of kin (per local legislative hierarchy) | Proof of relationship and unavailability of primary |

## Capacity Assessment Guidance

Capacity is task-specific and can fluctuate. Documentation must show:
- [ ] **Understanding**: Patient can explain the procedure and the problem.
- [ ] **Retention**: Patient can hold the information long enough to make a decision.
- [ ] **Reasoning**: Patient can weigh the risks vs. benefits.
- [ ] **Communication**: Patient can clearly state their choice.

## Documentation Standards

### Consent Validation Checklist

- [ ] **Specific**: Name of procedure/initiative is written in plain language.
- [ ] **Informed**: Risks, benefits, and alternatives (including doing nothing) are listed.
- [ ] **Voluntary**: No evidence of coercion or undue influence.
- [ ] **Current**: Signed within the required timeframe (e.g., within 6 months).
- [ ] **Signatures**: Patient/Proxy and the Clinician performing the procedure.

## Security & Privacy (PHI/PII Guardrails)

- **Confidentiality of Choice**: A patient's refusal of treatment or advance directive is highly sensitive. Access should be restricted to the direct care team.
- **Minimum Necessary**: When validating consent for research or data sharing, ensure only the authorized data sets are discussed.
- **De-identification**: Use `[Patient Consent A]` when discussing scenarios in the agent. Never include names or MRNs in persistent logs.

## Confidence Indicators

| Scenario | Confidence | Action |
|---|---|---|
| Standard surgical consent signed by patient and performing surgeon | High | Confirm validation and proceed with documentation |
| Consent signed by a proxy without a verified POA document on file | Medium | Flag as "Authority Pending"; request POA documentation |
| Patient with documented dementia or delirium signing their own consent | Low | Escalate to Clinical Lead; require capacity assessment review |
| Conflict between an Advance Directive and family wishes | Low | Escalate to Clinical Governance/Ethics Committee immediately |

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---|---|---|
| Treating consent as a "signed piece of paper" only | Consent is a process of communication, not just a document | Verify that the discussion of risks and benefits is documented |
| Accepting "blanket" consents for future unknown procedures | Legally invalid; consent must be specific to the intervention | Ensure each procedure has its own specific consent or is explicitly listed |
| Failing to verify the identity of a phone-in proxy | High risk of unauthorized decision-making and legal liability | Follow strict ID verification protocols for all non-present decision makers |
| Using jargon or acronyms in the procedure description | Patient cannot give informed consent if they don't understand the term | Use plain language descriptions (e.g., "Gallbladder removal" instead of "Cholecystectomy") |
| Ignoring a patient's verbal "No" if they already signed the form | A patient can withdraw consent at any time, even on the theatre table | Stop immediately and re-verify consent if any doubt arises |

## When to Escalate

- **Conflict**: Any disagreement between patient, family, and clinicians regarding treatment.
- **Impairment**: Unclear decision-making capacity without a designated proxy.
- **Legal/Ethics**: Requests for treatment withdrawal in life-sustaining situations.
- **Minors**: Consent issues involving "Mature Minor" status or conflicting parental wishes.

## Tool Requirements

- `~~health/clinical-records` (EHR) for consent forms and clinical notes.
- `~~health/id-verification` for confirming patient/proxy identity.
- `~~legal/guardianship-registry` (where available) for verifying legal orders.

## Success Indicators

- [ ] Consent type correctly identified.
- [ ] Documentation completeness and validity verified.
- [ ] Decision-making authority (Patient vs. Proxy) confirmed.
- [ ] Capacity assessment presence checked (if applicable).
- [ ] "Informed" criteria (Risks/Benefits/Alternatives) validated.
- [ ] Privacy of sensitive choices maintained.

## Related Skills

- `~~health/release-of-information` for disclosures requiring specific consent.
- `~~health/clinical-risk-assessment` for the risks discussed during consent.
- `~~health/ethics-review` for research or complex clinical ethics cases.

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-02-12 | Initial consent management skill with taxonomy and capacity guidance |
