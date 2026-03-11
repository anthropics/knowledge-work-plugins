# Health Manuscripts Track Plan

## Phase 1: Manuscript Preparation Skill
*Dependencies: health-core*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/manuscript-prep/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: Implements [Hybrid Evidence Management](../health-plugin/interoperability-standards.md)
  - Acceptance: AU/NZ publication and governance defaults are explicit, with US/EU-lite fallback
  - Acceptance: Standard mode and Lite mode are explicitly documented
  - Acceptance: Journal selection guidance
  - Acceptance: Study type to checklist mapping
  - Acceptance: Structure templates by article type
  - Acceptance: Reporting guideline compliance checking
  - Acceptance: Figure/table preparation guidance
  - Acceptance: Reference formatting
  - MCP: `~~research literature` (PubMed)
  - Source patterns: `scientific-writing`, `venue-templates`

## Phase 2: Prepare Manuscript Command
*Dependencies: Phase 1*
*Estimated: 0.5 sessions*

- [x] Create `health/commands/prepare-manuscript.md`
  - Acceptance: Study type selection
  - Acceptance: Target journal input
  - Acceptance: Generates manuscript checklist

**Checkpoint:** `conductor(checkpoint): Health manuscripts workflow complete`
