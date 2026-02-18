# Health Ethics Track Plan

## Phase 1: Research Ethics Skill
*Dependencies: health-core*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/research-ethics/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: AU/NZ ethics defaults (NHMRC/HRC) are explicit, with US/EU-lite fallback
  - Acceptance: Standard mode and Lite mode are explicitly documented
  - Acceptance: Includes Confidence Indicators for ethical risk assessment
  - Acceptance: PHI/PII guardrails for study protocols
  - Acceptance: REC/IRB application workflow
  - Acceptance: Protocol review checklist
  - Acceptance: Informed consent guidance
  - Acceptance: Study type variations
  - Source patterns: `bio-research`

## Phase 2: Clinical Ethics Skill
*Dependencies: Phase 1*
*Estimated: 1 session*

- [x] Create `health/skills/clinical-ethics/SKILL.md`
  - Acceptance: Consultation request workflow
  - Acceptance: Case analysis framework
  - Acceptance: Committee preparation guidance

## Phase 3: Ethics Review Command
*Dependencies: Phase 1*
*Estimated: 0.5 sessions*

- [x] Create `health/commands/ethics-review.md`
  - Acceptance: Review type selection
  - Acceptance: Routes to appropriate skill

**Checkpoint:** `conductor(checkpoint): Health ethics workflow complete`
