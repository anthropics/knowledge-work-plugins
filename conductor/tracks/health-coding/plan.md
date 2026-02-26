# Health Clinical Coding Track Plan

## Phase 1: Clinical Coding Skill
*Dependencies: health-core*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/clinical-coding/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: AU/NZ coding and compliance defaults are explicit, with US/EU-lite mapping notes
  - Acceptance: Standard mode and Lite mode are explicitly documented
  - Acceptance: Includes Confidence Indicators for diagnosis mapping
  - Acceptance: PHI/PII guardrails for patient records
  - Acceptance: ICD-10-AM coding guidance
  - Acceptance: Classification system overview
  - Acceptance: Code selection methodology
  - Acceptance: Mapping between systems
  - Acceptance: Common coding errors
  - Acceptance: Documentation requirements
  - Source patterns: `data/data-validation`
  - MCP: `~~medical coding` (ICD-10), `~~clinical terminology` (SNOMED)

## Phase 2: Validate Coding Command
*Dependencies: Phase 1*
*Estimated: 0.5 sessions*

- [x] Create `health/commands/validate-coding.md`
  - Acceptance: Code validation workflow
  - Acceptance: Generates validation report

**Checkpoint:** `conductor(checkpoint): Health clinical coding workflow complete`
