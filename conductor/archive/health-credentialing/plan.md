# Health Credentialing Track Plan

## Phase 1: Credentialing Skill
*Dependencies: health-core*
*Estimated: 1 session*

- [x] Create `health/skills/credentialing/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: Includes Confidence Indicators for primary source verification
  - Acceptance: AU/NZ credentialing defaults are explicit, with US/EU-lite fallback
  - Acceptance: PHI/PII guardrails for provider data
  - Acceptance: Credentialing workflow by provider type
  - Acceptance: Primary source verification checklist
  - Acceptance: Committee preparation guidance

## Phase 2: Privileging Skill
*Dependencies: Phase 1*
*Estimated: 1 session*

- [x] Create `health/skills/privileging/SKILL.md`
  - Acceptance: Privilege delineation categories
  - Acceptance: Competency verification requirements
  - Acceptance: Renewal timeline tracking

## Phase 3: Verify Credentials Command
*Dependencies: Phase 1*
*Estimated: 0.5 sessions*

- [x] Create `health/commands/verify-credentials.md`
  - Acceptance: Initiates verification workflow
  - Acceptance: Tracks verification status

**Checkpoint:** `conductor(checkpoint): Health credentialing workflow complete`
