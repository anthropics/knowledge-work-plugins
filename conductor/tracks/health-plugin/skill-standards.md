# Health Skill Standards

All skills implemented within the `health` plugin must adhere to these specialized standards in addition to the repository-wide `skill-quality` requirements.

## 1. Structural Mandate: 14-Section Architecture
Every health skill must use the full 14-section template from `conductor/tracks/skill-quality/spec.md`. Do not omit sections; use "N/A" with a brief explanation if a section is truly not applicable.

### Critical Sections for Health:
- **Common Mistakes (Anti-Patterns):** Must include clinical, regulatory, or administrative errors (e.g., "Assigning diagnosis codes based on symptoms when a definitive diagnosis exists").
- **Tool Requirements:** Explicitly list healthcare-specific MCP connectors (e.g., `~~health/clinical-systems`, `~~health/icd-10`).
- **Success Indicators:** Checklist items must verify clinical accuracy and regulatory compliance.

## 2. Clinical Safety & Confidence Indicators
To manage risk in high-stakes clinical workflows, every skill must include a **Confidence Indicators** table. This guides the agent on when to proceed autonomously vs. when to flag for human review.

| Scenario | Confidence | Action |
|----------|------------|--------|
| Explicit, unambiguous documentation | High | Propose final output/action |
| Conflicting or ambiguous records | Medium | Flag for human review with summary of conflict |
| High-risk clinical decisions | Low | Draft options but REQUIRE human sign-off |

## 3. Security & Privacy (PHI/PII Guardrails)
Every skill must have a **Security & Privacy Considerations** section addressing Protected Health Information (PHI).

- **No Logging:** Explicit instructions to never include PHI/PII in logs or persistent chat history.
- **Minimum Necessary:** Guidance on using only the minimum data required for the task (Privacy Act/HIPAA principle).
- **De-identification:** Patterns for summarizing clinical data without identifying the patient.

## 4. Jurisdiction & Regulatory Context
Healthcare is jurisdictionally sensitive. Where applicable, include a **Regulatory Context** or **Jurisdiction Matrix** in the "Detailed Guidance" section.

- Default jurisdiction: **Australia and New Zealand**.
- Include explicit AU/NZ references before any other jurisdiction.
- Include a **US/EU-lite** variant for portability when users request those regions.

### 4.1 Required Jurisdiction Matrix Columns
- Jurisdiction
- Applicable regulator or statute
- Reporting or compliance trigger
- Timeframe or SLA
- Required artifacts or evidence
- Escalation point

### 4.2 Baseline References
- AU/NZ default: `./jurisdiction-au-nz.md`
- US/EU-lite adaptation: `./jurisdiction-us-eu-lite.md`

## 5. Interoperability & Evidence Rigor
All skills must align with the [Health Interoperability & Evidence Standards](./interoperability-standards.md).

- **Data Standards:** Use FHIR/SNOMED-CT terminology for structured clinical outputs.
- **Evidence Management:** Implement "Hybrid Evidence Management" (Strict Citation + Narrative Referencing + Workstream Mapping).
- **Persona Adaptation:** Explicitly document how the skill adapts for different healthcare personas (Clinician, Admin, Researcher).

## 6. Metadata & Trigger Quality
Health skill frontmatter must use consistent trigger semantics:

- `name`: unique and domain-specific.
- `description`: start with `This skill should be used when...` and include concrete trigger phrases.
- `version`: required (semantic versioning).

## 7. Progressive Disclosure
Health skills must keep core workflow guidance in `SKILL.md` and move deep details into `references/`.

- `references/jurisdiction-au-nz.md` for AU/NZ-specific detail.
- `references/jurisdiction-us-eu-lite.md` for lightweight US/EU adaptation.
- `references/validation-checklists.md` for detailed QA and compliance checklists.

## 8. Standard and Lite Modes
Each health skill must define two operating modes:

- `Standard`: Full clinical and compliance workflow, complete evidence capture.
- `Lite`: Minimal safe guidance for constrained contexts, clearly marked as non-comprehensive.

Lite mode must never suppress high-risk escalation requirements.

## 9. Quality Gates for Health
A health skill is considered "Release Ready" only when:
- [ ] Minimum 300 lines of high-quality guidance.
- [ ] At least 5 "Common Mistakes" documented.
- [ ] Confidence Indicators cover at least 3 clinical scenarios.
- [ ] PHI/PII guardrails are explicitly defined.
- [ ] AU/NZ-default jurisdiction matrix is present.
- [ ] US/EU-lite variant guidance is present.
- [ ] Standard and Lite operating modes are documented.
- [ ] FHIR/SNOMED-CT alignment is verified for data outputs.
- [ ] Evidence management follows the "Hybrid" strategy (for evidence-heavy skills).
- [ ] All cross-references to `health-core` and related skills are valid.
