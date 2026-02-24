# Health Document Co-authoring Track Plan

## Phase 1: Clinical Document Co-authoring Skill
*Dependencies: health-core, health-governance*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/clinical-doc-coauthoring/SKILL.md`
  - [x] Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - [x] Acceptance: AU/NZ documentation and evidence defaults are explicit, with US/EU-lite fallback
  - [x] Acceptance: Standard mode and Lite mode are explicitly documented
  - [x] Acceptance: Three-stage workflow documented (Development, Review, Finalization)
  - [x] Acceptance: Document type templates (Protocol, Guideline, HTA)
  - [x] Acceptance: Evidence grading guidance (NHMRC levels I-IV, GPP; GRADE ratings)
  - [x] Acceptance: Citation requirements for clinical claims (Vancouver style)
  - [x] Acceptance: Stakeholder review workflow (4 rounds with feedback tracking)
  - [x] Acceptance: Reader testing methodology (think-aloud protocol, comprehension testing)

## Phase 2: Coauthor Command
*Dependencies: Phase 1*
*Estimated: 0.5 sessions*

- [x] Create `health/commands/coauthor.md`
  - [x] Acceptance: Document type selection (8 types)
  - [x] Acceptance: Stage selection/progression (stages 1-3, all)
  - [x] Acceptance: Generates document checklist (type-specific checklists)

**Checkpoint:** `conductor(checkpoint): Health document co-authoring workflow complete`

## Cross-References

- Outputs feed into `health-governance` (policies, guidelines)
- Supports `health-economics` (HTA submissions)
- Supports `health-ethics` (ethics applications)
