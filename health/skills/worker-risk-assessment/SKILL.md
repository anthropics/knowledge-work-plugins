---
name: health/worker-risk-assessment
description: This skill should be used when assessing risks to clinicians and healthcare workers, including occupational hazards, physical safety, psychological risk, and workplace violence. Use when a user mentions worker safety, occupational health and safety (WHS/OHS), workplace violence, clinician burnout, needle stick injury, exposure risk, or staff wellbeing.
version: 1.0.0
---

# Worker and Clinician Risk Assessment

Structured guidance for identifying, scoring, treating, and monitoring risks to the health, safety, and wellbeing of clinicians and healthcare workers.

**Important**: This skill supports occupational health and safety (WHS) workflows within healthcare settings. It does not replace formal WHS advice, legal counsel, or organization-specific safety policies. All assessments must align with local work health and safety legislation and be reviewed by qualified safety professionals.

## When to Use This Skill

Invoke when:
- Assessing hazards in a clinical workspace (e.g., emergency department, psychiatric ward, home visiting).
- Reviewing risks associated with specific clinical tasks (e.g., manual handling, sharp management, chemotherapy preparation).
- Addressing reports of workplace violence, aggression, or psychological distress.
- Planning for new facility designs or clinical service changes affecting staff.
- Investigating staff incidents to identify systemic safety gaps.
- Evaluating clinician burnout or psychological safety within a team.

Do not use for patient safety risks (use `~~health/clinical-risk-assessment`) or enterprise-level strategic risks (use `~~health/enterprise-risk-assessment`).

## Operating Modes

### Standard Mode
Full WHS risk governance workflow:
- Comprehensive hazard identification across physical, biological, chemical, and psychosocial domains.
- Formal risk scoring using the Worker Safety Matrix.
- Detailed control selection following the WHS Hierarchy of Controls.
- Documentation of consultation with affected workers.
- Integration with the organization's WHS management system.

### Lite Mode
Rapid safety screening (e.g., dynamic risk assessment before a home visit or during an emerging crisis):
- Quick identification of immediate threats (e.g., "Look, Point, Tell" method).
- Focus on immediate "STOP/GO" decisions and essential PPE/controls.
- Mandatory escalation for any identified high-risk factor.

Lite mode is for immediate operational safety only and must be followed by a Standard assessment for permanent risks.

## Regulatory Context

Default jurisdiction is Australia/New Zealand. Use US/EU-lite framing only when explicitly requested.

| Jurisdiction | Framework/Statute | Compliance Trigger | Review Cadence | Required Artifacts | Escalation Point |
|---|---|---|---|---|---|
| Australia | Work Health and Safety (WHS) Act 2011 (and state equivalents) | Notification of incident, new equipment/process, annual review | Annual or post-incident | Risk Assessment, SWMS (High Risk Construction/Work) | WHS Manager, Health and Safety Representative (HSR) |
| New Zealand | Health and Safety at Work Act 2015 (HSWA) | Notifiable event, change in work environment | Annual or post-incident | Risk Register, Control Plan | H&S Lead, WorkSafe NZ (if notifiable) |
| United States (lite) | OSHA Standards (General Duty Clause), NIOSH guidelines | Occupational injury/illness, OSHA inspection | Annual | OSHA 300 Log, Hazard Assessment | Safety Officer, HR |
| European Union (lite) | Framework Directive 89/391/EEC, country-specific OSH laws | New hazard identified, periodic audit | Per national law | Risk Assessment Document | OSH Coordinator |

## Quick Reference

1. **Identify the Hazard**: Physical (trips, manual handling), Biological (needlesticks, infection), Chemical (cleaning agents, cytotoxics), Psychosocial (violence, bullying, burnout).
2. **Consult**: Engage with the workers performing the task to understand actual practice.
3. **Assess Inherent Risk**: Score consequence and likelihood without new controls.
4. **Apply Hierarchy of Controls**: Prioritize Elimination over PPE.
5. **Verify Effectiveness**: Ensure controls don't create new hazards.
6. **Monitor**: Schedule regular reviews and check incident data.

## Risk Assessment Framework

### Worker Consequence Scale

| Level | Label | Safety Descriptor | Psychosocial / Health Descriptor |
|---|---|---|---|
| 1 | **Insignificant** | Near miss; no injury or very minor injury requiring no treatment | Brief stress; no lasting impact |
| 2 | **Minor** | Minor injury requiring first aid (e.g., small cut, minor bruise) | Short-term distress; manageable within normal support |
| 3 | **Moderate** | Medical treatment injury; restricted work or short-term lost time | Significant distress; temporary impairment; requires formal support |
| 4 | **Major** | Serious injury; long-term disability; significant lost time | Severe psychological injury; prolonged absence; burnout |
| 5 | **Catastrophic** | Fatality; permanent total disability | Permanent psychological disability; organizational-wide impact |

### Worker Likelihood Scale

| Level | Label | Frequency Descriptor |
|---|---|---|
| 1 | **Rare** | Only in exceptional circumstances; not heard of in similar settings |
| 2 | **Unlikely** | Could occur but not expected; infrequent precedent |
| 3 | **Possible** | Might occur at some time; has happened in this setting before |
| 4 | **Likely** | Will probably occur in most circumstances; regular occurrence |
| 5 | **Almost Certain** | Expected to occur in most circumstances; occurs frequently |

## Control Selection (WHS Hierarchy)

Apply controls in order of priority:

1. **Elimination**: Remove the hazard (e.g., automate a heavy lift, remove a dangerous chemical).
2. **Substitution**: Replace with a safer alternative (e.g., use needle-less connectors, use non-toxic cleaning agents).
3. **Engineering**: Isolate people from the hazard (e.g., duress alarms, physical barriers in ED, sharps disposal containers).
4. **Administrative**: Change the way people work (e.g., safe work procedures, training, job rotation, debriefing protocols).
5. **PPE**: Personal Protective Equipment (e.g., masks, gloves, safety glasses). *Note: PPE is the last line of defense.*

## Documentation Standards

### Worker Risk Assessment Report

```
## Worker Safety Risk Assessment

**Date**: [Date]
**Assessor**: [Name/Role]
**Team/Area**: [Specific clinical area or staff group]

### 1. Hazard Description
[Detail the physical, biological, or psychosocial hazard]

### 2. Consultation
[Summarize feedback from staff/Health and Safety Representatives]

### 3. Risk Analysis
- **Consequence**: [1-5] - [Rationale]
- **Likelihood**: [1-5] - [Rationale]
- **Current Risk Level**: [LOW/MEDIUM/HIGH/EXTREME]

### 4. Control Plan (Hierarchy)
- **Elimination/Substitution**: [Planned actions]
- **Engineering**: [Planned actions]
- **Administrative**: [Procedures/Training]
- **PPE**: [Required equipment]

### 5. Residual Risk
- **Expected Level**: [Target Risk Score]

### 6. Review Schedule
- **Next Review**: [Date]
```

## Security & Privacy Considerations

- **Employee Confidentiality**: Do not include specific staff names or medical details in shared risk registers. Use roles (e.g., "Night shift RN") or de-identified incident IDs.
- **Sensitive Content**: Psychosocial risk assessments may contain sensitive information regarding workplace culture or interpersonal conflict. Access should be restricted to relevant management and HR personnel.
- **Compliance**: Ensure storage of worker health records (e.g., immunization status, injury reports) complies with the Privacy Act (AU) or Privacy Act 2020 (NZ).

## Confidence Indicators

| Scenario | Confidence | Action |
|---|---|---|
| Well-defined physical hazard with clear legislative controls | High | Propose standard risk assessment and control plan |
| Complex psychosocial risk with conflicting staff reports | Medium | Suggest a preliminary assessment; recommend formal culture/wellbeing survey |
| Immediate threat of violence or emerging infectious hazard | Medium | Initiate Lite Mode/Immediate safety protocol; escalate to executive immediately |
| Risk involving novel technology or specialized clinical equipment | Low | Search for manufacturer safety data; recommend specialist WHS consultation |

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---|---|---|
| Relying solely on PPE for high-likelihood risks | PPE often fails or is used incorrectly; it doesn't remove the hazard | Use engineering or administrative controls as the primary mitigation |
| Assessing risk without talking to the staff doing the work | Desktop assessments miss the "work as imagined" vs "work as done" gap | Conduct walk-throughs and interview clinicians about their daily tasks |
| Ignoring psychosocial risks (burnout, bullying) | Psychosocial hazards cause as much harm as physical ones and are legally compensable | Include workload, support, and workplace behavior in regular assessments |
| Failing to update assessment after a "near miss" | Near misses are warnings of future incidents; the current risk score is likely wrong | Conduct a full re-assessment after every significant near-miss |
| Using generic risk assessments for specialized areas | Hazards in ICU are different from Home Care | Tailor the assessment to the specific clinical environment and task |

## When to Escalate

- **Immediate Danger**: Any hazard posing an immediate threat to life or limb (e.g., active violence, major chemical spill).
- **Notifiable Event**: Any incident meeting the legislative definition of "notifiable" (death, serious injury/illness).
- **Unresolved Risk**: High or Extreme risks where proposed controls are not feasible or have been rejected.
- **Legislative Breach**: Any identified non-compliance with WHS/HSWA regulations.

## Tool Requirements

- `~~health/clinical-systems` for de-identified incident data.
- `~~project tracker` for safety action tracking.
- `~~health/worker-wellness` (if available) for psychosocial trend analysis.
- `~~search` for latest WHS/OSHA guidelines.

## Success Indicators

- [ ] Hazard is clearly categorized (Physical, Biological, Chemical, Psychosocial).
- [ ] Consultation with staff/HSR is documented.
- [ ] Risk scoring uses the 5x5 Worker Safety Matrix.
- [ ] Controls follow the Hierarchy (Elimination is considered first).
- [ ] Escalation triggers for high/extreme risks are explicit.
- [ ] Privacy of individual staff members is maintained.

## Related Skills

- `~~health/clinical-risk-assessment` for patient-centric risks.
- `~~health/incident-reporting` for post-injury analysis.
- `~~health/enterprise-risk-assessment` for strategic safety governance.

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-02-12 | Initial worker risk assessment skill with WHS hierarchy and psychosocial coverage |
