---
name: health/clinical-risk-assessment
description: This skill should be used when assessing clinical risks to patient safety, scoring severity and likelihood, selecting controls, and documenting residual risk. Use when a user mentions clinical risk register, patient safety risk, risk matrix, risk scoring, clinical hazard, residual risk, or risk treatment plan.
version: 1.0.0
---

# Clinical Risk Assessment

Structured guidance for identifying, scoring, treating, and monitoring clinical risks to patient safety in healthcare organizations.

**Important**: This skill supports clinical governance workflows. It does not replace clinician judgment, legal advice, or organization-specific risk management policy. All risk assessments must be reviewed and endorsed by appropriately qualified clinical and governance personnel.

## When to Use This Skill

Invoke when:
- A clinical team needs to assess patient safety risks for a service, process, or change.
- A risk register entry needs to be created, scored, or reviewed.
- A new clinical service, pathway, or standing order requires risk analysis before approval.
- An incident investigation identifies systemic risks requiring formal treatment.
- A governance committee requests a risk assessment for accreditation or regulatory purposes.
- A clinical services plan or model-of-care change needs a risk checkpoint.

Do not use for workforce/occupational hazard risks (use `~~health/worker-risk-assessment`) or strategic/enterprise risks (use `~~health/enterprise-risk-assessment`).

## Operating Modes

### Standard Mode
Full clinical risk governance workflow:
- Complete hazard identification and context analysis.
- Formal severity and likelihood scoring with documented rationale.
- Control selection with effectiveness assessment.
- Residual risk calculation and acceptance criteria.
- Audit-ready documentation and governance sign-off.

### Lite Mode
Use only for constrained contexts (rapid risk screening, time-critical triage):
- Capture minimum risk description, preliminary severity, and immediate actions.
- Flag unknowns and require follow-up with full Standard assessment.
- High-risk escalation obligations remain unchanged.

Lite mode is not acceptable for final risk register entries or governance committee submissions.

## Regulatory Context

Default jurisdiction is Australia/New Zealand. Use US/EU-lite framing only when explicitly requested.

| Jurisdiction | Framework/Statute | Risk Governance Trigger | Review Cadence | Required Artifacts | Escalation Point |
|---|---|---|---|---|---|
| Australia | AS/NZS ISO 31000:2018, NSQHS Standards (Std 1 Clinical Governance), state WHS Acts | New service/pathway, post-incident, accreditation cycle, significant change, standing order introduction | At least annually; after every SAC 1-2 incident; before significant clinical change | Risk register entry, risk treatment plan, governance endorsement record | Clinical Governance Committee, Chief Medical Officer, Board Risk Sub-committee |
| New Zealand | AS/NZS ISO 31000:2018, HDSS Act 2001, Te Whatu Ora risk frameworks | New service introduction, post-serious-adverse-event, national standards review | At least annually; after SAE; before model-of-care change | Risk register entry, risk treatment plan, quality committee endorsement | Clinical Governance Committee, Chief Medical Officer, Quality & Safety Lead |
| United States (lite) | Joint Commission standards, CMS CoPs, organization risk policy | New service, sentinel event, TJC survey preparation | Per organization policy (typically quarterly review) | Risk assessment summary, mitigation plan | Risk Management, CMO, Quality Committee |
| European Union (lite) | ISO 31000, country-specific clinical governance frameworks | Service change, serious incident, regulatory audit | Per national implementation | Risk assessment summary, treatment plan | Clinical Governance Lead, Risk Officer |

## Quick Reference

1. Define the scope: what clinical process, service, or change is being assessed.
2. Identify hazards: what could go wrong and cause patient harm.
3. Determine existing controls already in place.
4. Score consequence (severity) using the Clinical Consequence Scale.
5. Score likelihood using the Clinical Likelihood Scale.
6. Calculate risk score (Consequence x Likelihood).
7. Classify risk level (LOW / MEDIUM / HIGH / EXTREME).
8. Select additional controls to reduce risk to acceptable level.
9. Calculate residual risk after proposed controls.
10. Document and submit for governance endorsement.

## Risk Assessment Framework

### Clinical Consequence Scale

Consequences are assessed in terms of impact on patient safety and clinical outcomes.

| Level | Label | Patient Safety Descriptor | Service Impact |
|---|---|---|---|
| 1 | **Negligible** | No harm or injury; near miss with no patient impact | No service disruption |
| 2 | **Minor** | Minor harm requiring first aid or additional observation; temporary discomfort | Minor service delay, managed locally |
| 3 | **Moderate** | Moderate harm requiring additional treatment or extended stay; reversible injury | Temporary service reduction or workaround required |
| 4 | **Major** | Major harm; permanent impairment, disability, or significant prolonged treatment | Significant service disruption; external review triggered |
| 5 | **Catastrophic** | Death or permanent severe disability directly attributable to the hazard | Service suspended; mandatory external notification; organizational crisis response |

### Clinical Likelihood Scale

| Level | Label | Clinical Descriptor |
|---|---|---|
| 1 | **Rare** | May occur only in exceptional circumstances; no known precedent in similar clinical settings |
| 2 | **Unlikely** | Could occur but not expected; isolated precedent in similar services |
| 3 | **Possible** | May occur; has happened in comparable clinical settings or services |
| 4 | **Likely** | Probably will occur; clear pattern in similar clinical environments |
| 5 | **Almost Certain** | Expected to occur frequently; systemic weakness is known and uncontrolled |

### Risk Score Calculation

**Risk Score = Consequence x Likelihood**

| Score Range | Risk Level | Color | Governance Response |
|---|---|---|---|
| 1-4 | **LOW** | GREEN | Accept and monitor; local management; routine review |
| 5-9 | **MEDIUM** | YELLOW | Treat with specific controls; assign risk owner; active monitoring |
| 10-15 | **HIGH** | ORANGE | Senior clinical leadership review; dedicated mitigation plan; escalate to governance committee |
| 16-25 | **EXTREME** | RED | Immediate executive and board escalation; consider service suspension pending risk reduction; mandatory external notification assessment |

### Risk Matrix

```
                        LIKELIHOOD
                  Rare  Unlikely  Possible  Likely  Almost Certain
                  (1)     (2)       (3)      (4)        (5)
CONSEQUENCE
Catastrophic (5) |   5   |   10   |   15   |   20   |     25     |
Major        (4) |   4   |    8   |   12   |   16   |     20     |
Moderate     (3) |   3   |    6   |    9   |   12   |     15     |
Minor        (2) |   2   |    4   |    6   |    8   |     10     |
Negligible   (1) |   1   |    2   |    3   |    4   |      5     |
```

## Risk Classification and Required Actions

### GREEN - Low Risk (Score 1-4)

**Characteristics:**
- Minor or negligible hazards that are unlikely to cause patient harm.
- Risks within normal clinical operating parameters.
- Existing controls are adequate and well-maintained.

**Required Actions:**
- **Accept**: Acknowledge the risk and continue with current controls.
- **Document**: Record in the clinical risk register for tracking.
- **Monitor**: Include in periodic clinical governance reviews (at least annually).
- **Local ownership**: Managed by service-level clinical lead.

**Clinical Examples:**
- Minor medication transcription risk mitigated by electronic prescribing.
- Low-acuity patient identification risk in a single-specialty outpatient clinic with existing ID protocols.
- Equipment maintenance delay for non-critical device with backup available.

### YELLOW - Medium Risk (Score 5-9)

**Characteristics:**
- Moderate hazards that could materialize under foreseeable clinical circumstances.
- Risks that require targeted intervention but do not necessitate immediate service change.
- Existing controls partially effective; enhancement needed.

**Required Actions:**
- **Treat**: Implement specific additional controls or process changes.
- **Assign owner**: Designate a named clinician or manager responsible for monitoring and mitigation.
- **Monitor actively**: Review at defined intervals (monthly or after relevant incidents).
- **Document thoroughly**: Record risk, controls, rationale, and review dates in the risk register.
- **Brief stakeholders**: Inform relevant clinical and operational leaders.
- **Define escalation triggers**: Specify conditions that would elevate the risk level.

**Clinical Examples:**
- Medication error risk in a ward with high nurse-to-patient ratios and partial electronic ordering.
- Deterioration recognition risk in a ward without continuous monitoring for intermediate-acuity patients.
- Infection control risk during a planned facility renovation with mitigation plan in place.

### ORANGE - High Risk (Score 10-15)

**Characteristics:**
- Significant hazards with meaningful probability of causing serious patient harm.
- Risks requiring senior clinical leadership attention and dedicated mitigation.
- Current controls are insufficient; service modifications may be necessary.

**Required Actions:**
- **Escalate to governance**: Present to the Clinical Governance Committee with full risk assessment.
- **Develop mitigation plan**: Specific, time-bound actions with named owners.
- **Brief executive**: Inform CMO/CEO and relevant directors.
- **Set review cadence**: Weekly or milestone-based review until risk is reduced.
- **Consider service modification**: Evaluate whether clinical pathway, staffing, or process changes are required.
- **Document in detail**: Full risk assessment with analysis, treatment options, and recommendations.
- **Define contingency plan**: What actions are taken if the risk materializes despite controls.

**Clinical Examples:**
- Surgical site risk in a theatre with identified ventilation deficiency pending remediation.
- Staffing model that regularly operates below safe minimum for clinical acuity.
- New high-risk medication pathway without adequate clinical decision support.

### RED - Extreme Risk (Score 16-25)

**Characteristics:**
- Severe hazards that are likely or certain to cause death, permanent disability, or major harm.
- Risks requiring immediate executive and board-level response.
- Service continuation in current form may be unsafe.

**Required Actions:**
- **Immediate escalation**: Brief CMO, CEO, and Board Risk Sub-committee.
- **Consider service suspension**: Evaluate whether the service, procedure, or pathway must be suspended pending risk reduction.
- **Establish response team**: Dedicated multidisciplinary team with clear roles and authority.
- **Mandatory external notification assessment**: Determine if regulators, accreditation bodies, or insurers must be notified.
- **Daily or more frequent review**: Active management until the risk is resolved or reduced to an acceptable level.
- **Board reporting**: Include in formal board risk reporting.
- **Preserve evidence**: If linked to an incident, implement evidence preservation protocols.
- **Communicate**: Open disclosure obligations and stakeholder communication as required.

**Clinical Examples:**
- Equipment failure pattern in a critical care unit creating imminent patient harm risk.
- Identified systematic prescribing error with potential for catastrophic patient outcomes.
- Infection outbreak in a high-dependency unit with inadequate containment.

## Control Selection Framework

### Hierarchy of Controls (Clinical Adaptation)

Apply controls in order of effectiveness (most to least effective):

| Priority | Control Type | Clinical Application | Effectiveness |
|---|---|---|---|
| 1 | **Elimination** | Remove the hazard entirely (discontinue unsafe process, withdraw defective device) | Highest |
| 2 | **Substitution** | Replace with a safer alternative (different medication formulation, alternative procedure) | High |
| 3 | **Engineering** | Physical or system barriers (forcing functions, automated alerts, physical interlocks) | High |
| 4 | **Administrative** | Policies, procedures, training, checklists, competency verification | Moderate |
| 5 | **PPE / Barriers** | Personal protective equipment, clinical safety devices, visual cues | Lowest |

### Control Effectiveness Assessment

For each proposed control, document:
- **Description**: What the control does.
- **Type**: Which level in the hierarchy.
- **Owner**: Who is responsible for implementation and maintenance.
- **Implementation timeline**: When the control will be active.
- **Verification method**: How effectiveness will be measured.
- **Limitations**: Known gaps or dependencies.

## Documentation Standards

### Risk Register Entry Format

| Field | Content |
|---|---|
| Risk ID | Unique identifier (e.g., CR-2026-001) |
| Date Identified | Date risk was first identified |
| Risk Description | Clear description of the clinical hazard and potential harm |
| Risk Domain | Patient Safety, Clinical Pathway, Medication, Infection, Equipment, Service Design, Standing Orders |
| Source | How identified: incident, audit, complaint, proactive assessment, accreditation gap |
| Consequence | 1-5 with label and rationale |
| Likelihood | 1-5 with label and rationale |
| Inherent Risk Score | Calculated score before additional controls |
| Inherent Risk Level | GREEN / YELLOW / ORANGE / RED |
| Existing Controls | Current controls already in place |
| Additional Controls | Proposed new controls with hierarchy level |
| Residual Consequence | After proposed controls |
| Residual Likelihood | After proposed controls |
| Residual Risk Score | Calculated residual score |
| Residual Risk Level | GREEN / YELLOW / ORANGE / RED |
| Risk Owner | Named clinician or manager |
| Review Date | Next scheduled review |
| Governance Endorsement | Committee and date of endorsement |
| Status | Open / In Treatment / Accepted / Closed |

### Risk Assessment Report Structure

```
## Clinical Risk Assessment

**Date**: [assessment date]
**Assessor**: [role/team conducting assessment]
**Scope**: [clinical process, service, or change being assessed]
**Governance Authority**: [committee or executive sponsor]

### 1. Context and Scope
[What is being assessed and why]

### 2. Hazard Identification
[What could go wrong; what harm could result]

### 3. Existing Controls
[Controls already in place and their effectiveness]

### 4. Risk Analysis

#### Consequence: [1-5] - [Label]
[Rationale referencing patient safety descriptors]

#### Likelihood: [1-5] - [Label]
[Rationale referencing clinical evidence, incident history, and current conditions]

#### Inherent Risk Score: [Score] - [GREEN/YELLOW/ORANGE/RED]

### 5. Risk Treatment
[Proposed additional controls with hierarchy classification]

| Control | Type | Owner | Timeline | Verification |
|---------|------|-------|----------|--------------|
| [Control 1] | [Hierarchy level] | [Name/Role] | [Date] | [Method] |

### 6. Residual Risk
[Expected risk level after controls are implemented]

#### Residual Consequence: [1-5] - [Label]
#### Residual Likelihood: [1-5] - [Label]
#### Residual Risk Score: [Score] - [GREEN/YELLOW/ORANGE/RED]

### 7. Acceptance and Governance
[Who has authority to accept the residual risk; committee endorsement required]

### 8. Monitoring Plan
[Review schedule, trigger events for re-assessment, KPIs]

### 9. Next Steps
1. [Action - Owner - Deadline]
2. [Action - Owner - Deadline]
```

## Security & Privacy Considerations

- Use minimum necessary patient data when describing clinical scenarios in risk assessments.
- Never include patient names or specific identifiers in risk register entries or reports.
- De-identify by default: use `[Patient A]`, `[Case ID]`, `[Ward X]` in all working documents.
- Keep patient-identifiable supporting evidence in authorized clinical systems only.
- Do not copy PHI/PII into tool logs, code comments, or reusable templates.
- Respect access controls and need-to-know principles for risk assessment documentation.
- Risk register entries are governance documents and should be stored in controlled systems.

## Confidence Indicators

| Scenario | Confidence | Action |
|---|---|---|
| Well-documented hazard with clear incident history and established controls | High | Proceed with full risk assessment and propose treatment plan |
| New or emerging risk with limited data; controls not yet validated | Medium | Produce provisional assessment, flag data gaps, require clinical lead review before governance submission |
| Conflicting evidence on severity or likelihood; multiple interpretations possible | Medium | Present range of plausible scores with rationale for each; require multidisciplinary review |
| Life-threatening or catastrophic risk scenario with incomplete information | Low | Escalate immediately to CMO/executive; apply precautionary principle; do not finalize assessment without senior clinical sign-off |
| Risk involves regulatory compliance uncertainty or novel clinical territory | Low | Draft assessment with explicit caveats; require governance committee and legal/compliance review |

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---|---|---|
| Scoring risk based on gut feeling without rationale | Produces inconsistent, non-reproducible assessments that fail audit | Document specific evidence and reasoning for each severity and likelihood score |
| Accepting high or extreme risk without executive endorsement | Exceeds local authority; creates unacceptable governance exposure | Escalate all HIGH and EXTREME risks to the appropriate governance authority |
| Confusing inherent and residual risk | Overstates or understates actual risk exposure; misleads governance decisions | Always assess inherent risk first, then calculate residual risk after controls |
| Applying only administrative controls to high-consequence risks | Administrative controls (training, policy) are least reliable; human error persists | Prioritize elimination, substitution, and engineering controls per the hierarchy |
| Treating the risk register as a static document | Risks evolve; unreviewed registers create false assurance | Set mandatory review dates and trigger-based re-assessment |
| Omitting existing controls from the assessment | Inflates inherent risk artificially; duplicates effort | Catalogue existing controls before proposing additional ones |
| Failing to link risk assessments to incident data | Misses evidence that would improve scoring accuracy | Cross-reference incident reports and near-miss data when scoring likelihood |

## When to Escalate

Escalate immediately when:
- Risk score reaches EXTREME (RED) on initial or any subsequent assessment.
- A risk previously rated LOW or MEDIUM has escalated due to a new incident or changed circumstances.
- There is disagreement among clinical staff on severity or likelihood scoring.
- The risk involves a mandatory reporting trigger (death, severe harm, sentinel event).
- Controls have failed or are no longer effective.
- External factors (regulatory change, supply disruption, workforce shortage) materially affect the risk profile.

Escalation targets:
- Clinical escalation: Service Lead -> Clinical Director -> Chief Medical Officer.
- Governance escalation: Quality/Risk Manager -> Clinical Governance Committee -> Board Risk Sub-committee.

## Tool Requirements

- `~~health/clinical-systems` (FHIR/HL7) for clinical record and incident data to support risk scoring.
- `~~project tracker` (Jira/ServiceNow) for risk register entries and action tracking.
- `~~cloud storage` (SharePoint) for risk assessment reports and governance endorsement records.
- `~~health/coding` or equivalent for structured categorization of clinical hazards.

## Success Indicators

You have applied this skill correctly when:
- [ ] Risk scope and context are clearly defined.
- [ ] Hazards are identified with reference to clinical evidence or incident history.
- [ ] Consequence and likelihood are scored with documented rationale.
- [ ] Inherent and residual risk scores are both calculated.
- [ ] Controls follow the hierarchy of controls (elimination > administrative).
- [ ] Risk owner and review date are assigned.
- [ ] Governance endorsement requirements are identified.
- [ ] Outputs avoid unnecessary PHI/PII exposure.
- [ ] Jurisdiction assumptions are explicit (AU/NZ default unless requested otherwise).

## Related Skills

- `~~health/worker-risk-assessment` for workforce and occupational hazard risk.
- `~~health/enterprise-risk-assessment` for strategic and organizational risk.
- `~~health/incident-reporting` for incident-triggered risk assessments.
- `~~health/quality-improvement` for QI projects arising from risk treatment plans.
- `~~health/complaints-management` for complaint-driven risk identification.

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-02-12 | Initial clinical risk assessment with severity x likelihood matrix, control hierarchy, and governance workflow |
