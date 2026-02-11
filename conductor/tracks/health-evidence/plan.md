# Health Evidence Synthesis Track Plan

## Phase 1: Systematic Review Skill
*Dependencies: health-core*
*Estimated: 1-2 sessions*

- [ ] Create `health/skills/systematic-review/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: Implements [Hybrid Evidence Management](../health-plugin/interoperability-standards.md)
  - Acceptance: AU/NZ evidence and governance defaults are explicit, with US/EU-lite fallback
  - Acceptance: Standard mode and Lite mode are explicitly documented
  - Acceptance: PRISMA workflow guidance
  - Acceptance: Search strategy development framework
  - Acceptance: Screening and selection process
  - Acceptance: Data extraction templates
  - Acceptance: Risk of bias tools (RoB 2, ROBINS-I)
  - Acceptance: GRADE evidence grading
  - MCP: `~~research literature` (PubMed), `~~clinical terminology` (SNOMED/LOINC)
  - Source patterns: `bio-research`, PRISMA guidelines

## Phase 2: Evidence Synthesis Skill
*Dependencies: Phase 1*
*Estimated: 1 session*

- [ ] Create `health/skills/evidence-synthesis/SKILL.md`
  - Acceptance: Review type selection guidance
  - Acceptance: Scoping/rapid review adaptations
  - Acceptance: Evidence mapping methodology

## Phase 3: Start Review Command
*Dependencies: Phase 1*
*Estimated: 0.5 sessions*

- [ ] Create `health/commands/start-review.md`
  - Acceptance: Review type selection
  - Acceptance: Protocol template generation
  - Acceptance: Project setup checklist

**Checkpoint:** `conductor(checkpoint): Health evidence synthesis workflow complete`
