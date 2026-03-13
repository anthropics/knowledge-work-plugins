# Health Incidents Track Plan

## Phase 1: Incident Reporting Skill
*Dependencies: health-core*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/incident-reporting/SKILL.md`
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: AU/NZ incident-reporting defaults are explicit, with US/EU-lite fallback
  - Acceptance: Standard mode and Lite mode are explicitly documented
  - Acceptance: Includes Confidence Indicators for clinical severity (SAC scores)
  - Acceptance: PHI/PII guardrails for incident documentation
  - Acceptance: Incident type taxonomy
  - Acceptance: Severity classification (SAC or equivalent)
  - Acceptance: Immediate response protocol
  - Acceptance: Investigation methodology (RCA)
  - Acceptance: Mandatory reporting triggers
  - Acceptance: QI documentation requirements

## Phase 2: Incident Command
*Dependencies: Phase 1*
*Estimated: 1 session*

- [x] Create `health/commands/report-incident.md`
  - Acceptance: Rapid intake workflow
  - Acceptance: Captures immediate safety concerns
  - Acceptance: Routes to appropriate severity path
  - Acceptance: Triggers notifications where required

**Checkpoint:** `conductor(checkpoint): Health incidents workflow complete`

## Notes

- Coordinate with `health-complaints` - some complaints are incident reports
- May need `health-risk` integration for trend analysis
- Regulatory requirements vary significantly by jurisdiction
