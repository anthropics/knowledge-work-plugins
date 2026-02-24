# Health Public Health Track Plan

## Phase 1: Notifiable Diseases Skill
*Dependencies: health-core, health-coding*
*Estimated: 1-2 sessions*

- [x] Create `health/skills/notifiable-diseases/SKILL.md` [created]
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: AU/NZ notification defaults are explicit, with US/EU-lite fallback
  - Acceptance: Standard mode and Lite mode are explicitly documented
  - Acceptance: Notifiable disease list by jurisdiction
  - Acceptance: Notification timeline requirements
  - Acceptance: Case definition criteria
  - Acceptance: Reporting form guidance
  - Acceptance: Contact tracing framework
  - Source patterns: `legal/compliance`

## Phase 2: Public Health Surveillance Skill
*Dependencies: Phase 1*
*Estimated: 1 session*

- [x] Create `health/skills/public-health-surveillance/SKILL.md` [created]
  - Acceptance: Follows [health skill standards](../health-plugin/skill-standards.md) (14-section template)
  - Acceptance: AU/NZ surveillance defaults are explicit, with US/EU-lite fallback
  - Acceptance: Surveillance types overview
  - Acceptance: Outbreak detection criteria
  - Acceptance: Response coordination workflow

## Phase 3: Report Notifiable Command
*Dependencies: Phase 1*
*Estimated: 0.5 sessions*

- [x] Create `health/commands/report-notifiable.md` [created]
  - Acceptance: Disease selection
  - Acceptance: Jurisdiction selection
  - Acceptance: Generates notification checklist

**Checkpoint:** `conductor(checkpoint): Health public health workflow complete`

## Cross-References

- Uses `health-coding` for disease coding
- Feeds `health-data-analysis` for epidemiology
- Coordinates with `health-incidents` for outbreak incidents
