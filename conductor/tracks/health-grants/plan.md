# Health Grants Track Plan

## Phase 1: Grant Writer Skill
*Dependencies: health-core*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/grant-writer/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: Implements [Hybrid Evidence Management](../health-plugin/interoperability-standards.md)
  - Acceptance: AU/NZ funder defaults (NHMRC/MRFF/HRC) are explicit, with US/EU-lite fallback
  - Acceptance: Standard mode and Lite mode are explicitly documented
  - Acceptance: Funder/scheme selection guidance
  - Acceptance: NHMRC structure and requirements
  - Acceptance: MRFF structure and requirements
  - Acceptance: HRC (NZ) structure and requirements
  - Acceptance: Assessment criteria alignment
  - Acceptance: Budget justification framework
  - MCP: `~~research literature` (PubMed)
  - Source patterns: `research-grants`

## Phase 2: Grant Application Command
*Dependencies: Phase 1*
*Estimated: 0.5 sessions*

- [x] Create `health/commands/grant-application.md`
  - Acceptance: Funder selection
  - Acceptance: Scheme selection
  - Acceptance: Generates application checklist

**Checkpoint:** `conductor(checkpoint): Health grants workflow complete`
