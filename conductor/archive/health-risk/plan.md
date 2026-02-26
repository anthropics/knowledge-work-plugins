# Health Risk Assessment Track Plan

## Phase 1: Clinical Risk Skill
*Dependencies: health-core*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/clinical-risk-assessment/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: AU/NZ risk-governance defaults are explicit, with US/EU-lite fallback
  - Acceptance: Standard mode and Lite mode are explicitly documented
  - Acceptance: Confidence Indicators for medical risk scoring
  - Acceptance: Structured risk taxonomy for clinical contexts
  - Acceptance: Severity and likelihood scoring guidance
  - Acceptance: Control selection and residual risk documentation
  - Source patterns: `legal/legal-risk-assessment`

## Phase 2: Worker and Enterprise Risk Skills
*Dependencies: Phase 1*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/worker-risk-assessment/SKILL.md`
  - Acceptance: Workforce and occupational hazard checklist
  - Acceptance: Escalation criteria and urgent action triggers

- [x] Create `health/skills/enterprise-risk-assessment/SKILL.md`
  - Acceptance: Enterprise risk categories and ownership mapping
  - Acceptance: Governance review and reporting cadence

## Phase 3: Assess Risk Command
*Dependencies: Phase 1, Phase 2*
*Estimated: 0.5-1 session*

- [x] Create `health/commands/assess-risk.md`
  - Acceptance: Intake prompts for risk domain selection
  - Acceptance: Recommended controls and residual risk output
  - Acceptance: Escalation and follow-up checklist

**Checkpoint:** `conductor(checkpoint): Health risk assessment workflow complete`
