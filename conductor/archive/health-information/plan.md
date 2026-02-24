# Health Information Management Track Plan

## Phase 1: Release of Information Skill
*Dependencies: health-core*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/release-of-information/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: AU/NZ default jurisdiction matrix plus US/EU-lite variant guidance
  - Acceptance: Standard mode and Lite mode are explicitly documented
  - Acceptance: PHI/PII guardrails (Minimum Necessary Principle)
  - Acceptance: Authorization validation checklist
  - Acceptance: Request types and processing timelines
  - Acceptance: Minimum necessary guidance
  - Acceptance: Accounting of disclosures requirements
  - Source patterns: `legal/compliance`, `customer-support/response-drafting`

## Phase 2: Consent Management Skill
*Dependencies: Phase 1*
*Estimated: 1 session*

- [x] Create `health/skills/consent-management/SKILL.md`
  - Acceptance: Consent type taxonomy
  - Acceptance: Documentation requirements
  - Acceptance: Capacity assessment guidance

## Phase 3: Process ROI Command
*Dependencies: Phase 1*
*Estimated: 0.5 sessions*

- [x] Create `health/commands/process-roi.md`
  - Acceptance: ROI request intake
  - Acceptance: Validation workflow
  - Acceptance: Processing checklist

**Checkpoint:** `conductor(checkpoint): Health information management workflow complete`
