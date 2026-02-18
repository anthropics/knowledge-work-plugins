# Health Complaints Track Plan

## Phase 1: Complaints Skill
*Dependencies: health-core*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/complaints-management/SKILL.md` (2026-02-12)
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: AU/NZ complaints-handling defaults are explicit, with US/EU-lite fallback
  - Acceptance: Standard mode and Lite mode are explicitly documented
  - Acceptance: Includes Confidence Indicators for clinical vs administrative triage
  - Acceptance: PHI/PII guardrails for patient data handling
  - Acceptance: Distinguishes clinician vs service complaints
  - Acceptance: Severity framework adapted for healthcare (P1-P4 with patient safety context)
  - Acceptance: Investigation workflow with timelines
  - Acceptance: Escalation triggers to legal/regulatory
  - Acceptance: Resolution documentation requirements
  - Source patterns: `customer-support/ticket-triage`, `customer-support/escalation`

## Phase 2: Complaints Command
*Dependencies: Phase 1*
*Estimated: 1 session*

- [x] Create `health/commands/submit-complaint.md` (2026-02-12)
  - Acceptance: Collects complaint type
  - Acceptance: Captures patient/staff safety concerns
  - Acceptance: Routes to appropriate skill path
  - Acceptance: Generates intake documentation

**Checkpoint:** `conductor(checkpoint): Health complaints workflow complete`

## Notes

- May need to coordinate with `health-incidents` track - some complaints may trigger incident reports
- Regulatory reporting requirements vary by jurisdiction - parameterize
