# Health Economics Track Plan

## Phase 1: Economic Evaluation Skill
*Dependencies: health-core, health-evidence*
*Estimated: 2 sessions*

- [x] Create `health/skills/health-econ-eval/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: Implements [Hybrid Evidence Management](../health-plugin/interoperability-standards.md)
  - Acceptance: AU/NZ HTA defaults (PBAC/MSAC/PHARMAC) are explicit, with US/EU-lite fallback
  - Acceptance: Standard mode and Lite mode are explicitly documented
  - Acceptance: Includes Confidence Indicators for model validity
  - Acceptance: Evaluation type selection (CEA, CUA, CBA)
  - Acceptance: Reference case requirements by jurisdiction
  - Acceptance: Decision modeling guidance
  - Acceptance: Costing methodology
  - Acceptance: QALY/DALY calculation guidance
  - Acceptance: Sensitivity analysis framework
  - MCP: `~~research literature` (PubMed)
  - Source patterns: `data/statistical-analysis`

## Phase 2: HTA Submission Skill
*Dependencies: Phase 1*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/hta-submission/SKILL.md`
  - Acceptance: PBAC submission template
  - Acceptance: MSAC submission template
  - Acceptance: NICE submission template
  - Acceptance: Evidence requirements by jurisdiction
  - Acceptance: Common submission pitfalls

## Phase 3: Economic Evaluation Command
*Dependencies: Phase 1*
*Estimated: 0.5 sessions*

- [x] Create `health/commands/economic-evaluation.md`
  - Acceptance: Evaluation type intake
  - Acceptance: Jurisdiction selection
  - Acceptance: Generates evaluation plan

**Checkpoint:** `conductor(checkpoint): Health economics workflow complete`
