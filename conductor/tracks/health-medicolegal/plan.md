# Health Medicolegal Track Plan

## Phase 1: Medicolegal Reports Skill
*Dependencies: health-core*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/medicolegal-reports/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: AU/NZ medicolegal defaults are explicit, with US/EU-lite fallback
  - Acceptance: Standard mode and Lite mode are explicitly documented
  - Acceptance: Includes Confidence Indicators for legal admissibility
  - Acceptance: PHI/PII guardrails for sensitive reports
  - Acceptance: Document type taxonomy
  - Acceptance: General structure requirements
  - Acceptance: Legal admissibility guidance
  - Acceptance: Confidentiality considerations
  - Source patterns: `legal/contract-review`

## Phase 2: Child Protection Skill
*Dependencies: Phase 1*
*Estimated: 1 session*

- [x] Create `health/skills/child-protection/SKILL.md`
  - Acceptance: Mandatory reporting triggers
  - Acceptance: Report structure template
  - Acceptance: Risk assessment documentation
  - Acceptance: Jurisdiction variations

## Phase 3: Affidavit Drafting Skill
*Dependencies: Phase 1*
*Estimated: 1 session*

- [x] Create `health/skills/affidavit-drafting/SKILL.md`
  - Acceptance: Affidavit structure
  - Acceptance: Swearing requirements
  - Acceptance: Court formatting
  - Acceptance: Common pitfalls

## Phase 4: Prepare Report Command
*Dependencies: Phases 1-3*
*Estimated: 0.5 sessions*

- [x] Create `health/commands/prepare-report.md`
  - Acceptance: Document type selection
  - Acceptance: Jurisdiction selection
  - Acceptance: Generates appropriate template

**Checkpoint:** `conductor(checkpoint): Health medicolegal workflow complete`
