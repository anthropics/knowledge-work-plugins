# Health Data Analysis Track Plan

## Phase 1: Health Data Report Skill
*Dependencies: health-core, health-coding*
*Estimated: 1-2 sessions*

- [ ] Create `health/skills/health-data-report/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: Includes Confidence Indicators for statistical validity
  - Acceptance: AU/NZ reporting defaults are explicit, with US/EU-lite fallback
  - Acceptance: Implements [Hybrid Evidence Management](../health-plugin/interoperability-standards.md)
  - Acceptance: Analysis type selection guidance
  - Acceptance: Epidemiological methods overview
  - Acceptance: Standard health metrics
  - Acceptance: Visualization types (forest plots, survival curves)
  - Acceptance: Report structure templates
  - MCP: `~~research literature` (PubMed), `~~clinical terminology` (SNOMED/LOINC)
  - Source patterns: `data/statistical-analysis`, `data/data-visualization`

## Phase 2: Analyze Health Data Command
*Dependencies: Phase 1*
*Estimated: 0.5 sessions*

- [ ] Create `health/commands/analyze-health-data.md`
  - Acceptance: Analysis type selection
  - Acceptance: Data requirements checklist
  - Acceptance: Generates analysis plan

**Checkpoint:** `conductor(checkpoint): Health data analysis workflow complete`
