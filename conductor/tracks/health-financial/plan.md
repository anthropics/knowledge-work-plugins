# Health Financial Track Plan

## Phase 1: Payer Contracts Skill
*Dependencies: health-core*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/payer-contracts/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: Includes Confidence Indicators for contract risk
  - Acceptance: AU/NZ financial and payer defaults are explicit, with US/EU-lite fallback
  - Acceptance: Healthcare-specific contract review checklist
  - Acceptance: Key term identification (rates, timeliness, medical necessity)
  - Acceptance: Renewal tracking guidance
  - Source patterns: `legal/contract-review`

## Phase 2: Charge Capture Skill
*Dependencies: Phase 1*
*Estimated: 1 session*

- [ ] Create `health/skills/charge-capture/SKILL.md`
  - Acceptance: CDM review methodology
  - Acceptance: Coding validation guidance
  - Acceptance: Compliance red flags
  - Source patterns: `finance/reconciliation`

## Phase 3: Review Payer Contract Command
*Dependencies: Phase 1*
*Estimated: 0.5 sessions*

- [ ] Create `health/commands/review-payer-contract.md`
  - Acceptance: Contract intake workflow
  - Acceptance: Generates analysis report

**Checkpoint:** `conductor(checkpoint): Health financial workflow complete`
