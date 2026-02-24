# Health Procurement Track Plan

## Phase 1: Device Procurement Skill
*Dependencies: health-core*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/device-procurement/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: Includes Confidence Indicators for regulatory compliance (TGA/FDA/CE)
  - Acceptance: AU/NZ procurement defaults are explicit, with US/EU-lite fallback
  - Acceptance: Device evaluation criteria
  - Acceptance: Regulatory compliance checklist
  - Acceptance: Vendor assessment framework
  - Source patterns: `legal/contract-review`

## Phase 2: Business Case Skill
*Dependencies: Phase 1*
*Estimated: 1 session*

- [x] Create `health/skills/business-case/SKILL.md`
  - Acceptance: Business case structure
  - Acceptance: ROI calculation guidance
  - Acceptance: Risk assessment section

## Phase 3: Commands
*Dependencies: Phases 1, 2*
*Estimated: 0.5 sessions*

- [x] Create `health/commands/procurement-request.md`
- [x] Create `health/commands/business-case.md`

**Checkpoint:** `conductor(checkpoint): Health procurement workflow complete`
