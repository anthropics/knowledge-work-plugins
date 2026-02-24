---
name: health/incident-reporting
description: This skill should be used when reporting, triaging, investigating, or escalating healthcare incidents and serious adverse events. Use when a user mentions incident forms, near misses, sentinel events, SAC severity, mandatory notifications, or root cause analysis.
version: 1.0.0
---

# Incident Reporting

Structured guidance for healthcare incident intake, severity classification, escalation, investigation, and quality improvement follow-through.

**Important**: This skill supports clinical governance workflows. It does not replace clinician judgment, legal advice, or organization-specific policy requirements.

## When to Use This Skill

Invoke when:
- A user needs to log a patient safety incident, adverse event, or near miss.
- A team asks how to classify severity using SAC 1-4 (or local equivalent).
- A report may trigger mandatory external notification.
- The incident needs immediate containment and escalation routing.
- The organization needs a root cause analysis (RCA) plan.
- Quality teams need CAPA or improvement tracking from incident findings.

Do not use this as a replacement for emergency response channels. If immediate harm is ongoing, direct escalation to emergency and on-call clinical leadership is mandatory.

## Operating Modes

### Standard Mode
Use full incident governance workflow:
- Full incident chronology and evidence capture.
- Formal severity classification with confidence statement.
- Regulatory trigger screen (AU/NZ default).
- RCA initiation and quality improvement linkage.
- Complete audit-ready output package.

### Lite Mode
Use only for constrained contexts (limited time or partial data):
- Capture minimum safe fields.
- Apply preliminary severity and immediate actions.
- Flag unknowns and require follow-up completion.
- Keep high-risk escalation obligations unchanged.

Lite mode is not acceptable for final closure of serious incidents.

## Regulatory Context

Default jurisdiction is Australia/New Zealand. Use US/EU-lite framing only when explicitly requested.

| Jurisdiction | Regulator/Statute | Trigger | Timeframe/SLA | Required Artifacts | Escalation Point |
|---|---|---|---|---|---|
| Australia | NSQHS governance context, Privacy Act 1988 (Cth), state health incident rules | SAC 1-2, sentinel event, serious harm, mandatory notifier events | Immediate internal escalation; external timing per state policy | Incident form, chronology, clinical review notes, notification record | Clinical Director, Risk/Legal, Executive on call |
| New Zealand | HDC Code context, Health Information Privacy Code 2020, Te Whatu Ora pathways | Serious adverse events, rights breaches, reportable harm | Immediate internal escalation; external timing per district/national requirements | Incident record, actions taken, duty of candour documentation | Clinical Director, Quality Lead, Legal advisor |
| United States (lite) | HIPAA + organization/state reporting policy | Serious patient harm, privacy/security concerns | Per state and facility policy | De-identified incident summary, compliance log | Risk Management + Compliance |
| European Union (lite) | GDPR + country-specific health rules | Serious harm, data/privacy incidents | Per member-state implementation | Incident summary, DPIA/compliance references where applicable | Clinical Governance + DPO |

## Quick Reference

1. Confirm if immediate patient safety risk is present.
2. If risk is active, escalate before documentation depth.
3. Record incident type and preliminary severity.
4. Capture only minimum necessary PHI/PII.
5. Determine whether mandatory reporting triggers apply.
6. Route to clinical and governance owners based on severity.
7. Start RCA for major incidents and sentinel events.
8. Define immediate containment actions and owners.
9. Set due dates for acknowledgment, investigation, and closure.
10. Register QI actions (CAPA/PDSA) tied to root causes.

## Incident Type Taxonomy

Use one primary type and optional secondary tags:

| Primary Type | Examples |
|---|---|
| Medication / ADR | Wrong dose, omitted medication, adverse drug reaction |
| Procedure / Treatment | Wrong-site, delayed treatment, protocol breach |
| Clinical Deterioration | Failure to recognize or escalate deterioration |
| Device / Equipment | Device failure, alarm failure, unavailability |
| Infection / IPC | Healthcare-associated infection, isolation breach |
| Falls / Injury | Patient fall, transfer injury |
| Documentation / Communication | Handover failure, incomplete records |
| Privacy / Information | Unauthorized disclosure, incorrect recipient |
| Near Miss | Event intercepted before patient harm |
| Sentinel Event | Death or severe permanent harm requiring immediate executive oversight |

## Severity Classification (SAC-Aligned)

| SAC | Severity Signal | Typical Response |
|---|---|---|
| SAC 1 | Extreme consequence or immediate severe risk | Immediate executive + clinical escalation, urgent investigation, potential external notification |
| SAC 2 | Major consequence or high risk requiring urgent action | Same-day escalation, formal investigation, targeted notification assessment |
| SAC 3 | Moderate impact with manageable risk | Structured review, corrective actions, service-level oversight |
| SAC 4 | Minor impact or near miss with low residual risk | Local review, lessons learned, trend monitoring |

If local policy uses a different matrix, map to equivalent levels and document the mapping.

## Immediate Response Protocol

### Step 1: Safety Containment
- Stop unsafe process.
- Stabilize and treat affected patient(s).
- Isolate compromised medication/device/information pathway.
- Assign a clinical lead for immediate decisions.

### Step 2: Escalation
- Notify charge nurse/unit lead.
- Notify clinical director for SAC 1-2 indicators.
- Notify risk/compliance/legal when regulatory threshold may be met.
- Notify executive duty manager for sentinel events.

### Step 3: Evidence Preservation
- Preserve records, logs, orders, device metadata, and communication trails.
- Prevent alteration of source documentation.
- Record timestamps and involved roles.

### Step 4: Communication Discipline
- Use factual language; avoid blame statements.
- Provide internal updates with clear owner and ETA.
- Trigger open disclosure pathways where policy requires.

## Investigation Methodology (RCA)

Use structured RCA for SAC 1-2 and sentinel events.

1. Define incident statement (what happened, where, when).
2. Build verified chronology.
3. Identify active failures and latent system factors.
4. Apply contributory factors (people, process, technology, environment, communication).
5. Validate findings with multidisciplinary review.
6. Draft corrective/preventive actions with accountable owners.
7. Define measurable controls and monitoring windows.

Recommended outputs:
- Problem statement.
- Contributory factor map.
- Corrective Action and Preventive Action (CAPA) plan.
- Residual risk rating after interventions.

## Mandatory Reporting Trigger Screen

Evaluate and record yes/no with rationale:
- Death or severe permanent harm.
- Sentinel event category match.
- Serious medication/device adverse event.
- Notifiable infection/public health trigger.
- Significant privacy breach with patient impact.
- Practitioner conduct concerns requiring board notification.

If uncertain, classify as "possible trigger" and escalate to compliance/legal for determination.

## Documentation Requirements

Required minimum fields:
- Incident ID and timestamp.
- Location/service line.
- Reporter role (not full personal identifiers unless policy requires).
- De-identified patient references.
- Incident taxonomy and preliminary severity.
- Immediate actions taken.
- People notified and notification timestamps.
- Mandatory reporting assessment.
- Investigation owner and due dates.
- QI linkage (CAPA/PDSA ticket IDs).

For high-severity events, include:
- Confirmed chronology.
- RCA deliverables.
- Executive/committee review outcomes.
- Closure criteria and verification evidence.

## Security & Privacy Considerations

- Use minimum necessary data for triage and reporting.
- Never place full identifiers into ad hoc notes or shared chat channels.
- De-identify by default (`[Patient A]`, `[Staff B]`, `[Case ID]`).
- Keep patient-identifiable records in authorized systems only.
- Do not copy PHI/PII into tool logs, code comments, or reusable templates.
- Respect access controls and need-to-know principles.
- If a privacy incident is suspected, run incident and privacy workflows in parallel.

## Confidence Indicators

| Scenario | Confidence | Action |
|---|---|---|
| Clear near miss with complete chronology and no harm | High | Proceed with draft report, local review, and trend tagging |
| Event details incomplete but potential moderate harm | Medium | Produce provisional report, flag missing evidence, require clinical lead review |
| Possible sentinel event or severe harm with conflicting accounts | Low | Escalate immediately, require executive and legal/compliance review before closure |
| Suspected mandatory external notification trigger | Low | Do not finalize determination autonomously; escalate to compliance/legal |

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---|---|---|
| Treating incidents as complaints only | Misses patient safety and regulatory pathways | Run incident workflow first, then complaint workflow if applicable |
| Downgrading severity due to uncertainty | Delays needed response and notifications | Classify conservatively and escalate for confirmation |
| Recording excess PHI in broad channels | Increases privacy risk and non-compliance | Use de-identified summaries and secure systems |
| Starting RCA before containment is stable | Investigation quality drops and risk remains active | Complete immediate safety actions first |
| Closing incidents without QI linkage | Recurrence risk remains unmanaged | Attach CAPA/PDSA actions with owners and due dates |
| Missing notification timestamps | Weakens legal and governance auditability | Log each notification with exact time and recipient role |

## When to Escalate

Escalate immediately when:
- Ongoing patient safety risk exists.
- Severity appears SAC 1 or SAC 2.
- Sentinel event criteria may be met.
- Mandatory reporting threshold may be triggered.
- There is a privacy breach with potential harm.
- Conflicting evidence prevents safe closure decision.

Escalation targets:
- Clinical escalation: Charge nurse -> Clinical Director -> Executive on call.
- Governance escalation: Quality/Risk -> Compliance/Legal -> Governance committee.

## Tool Requirements

- `~~health/clinical-systems` for validated record and timeline retrieval.
- `~~project tracker` for incident IDs, tasks, and CAPA tracking.
- `~~cloud storage` for controlled evidence packs and investigation artifacts.
- `~~health/coding` or equivalent classification support for structured categorization.

## Success Indicators

You have applied this skill correctly when:
- [ ] Incident type and severity are documented with rationale.
- [ ] Immediate safety actions are recorded and owned.
- [ ] Mandatory reporting triggers were explicitly assessed.
- [ ] RCA is initiated for high-severity incidents.
- [ ] QI follow-through tasks are linked and tracked.
- [ ] Outputs avoid unnecessary PHI/PII exposure.
- [ ] Jurisdiction assumptions are explicit (AU/NZ default unless requested otherwise).

## Related Skills

- `~~health/complaints-management` for complaint handling when an incident also has service/communication concerns.
- `~~health/risk-management` for ongoing enterprise or clinical risk treatment after incident closure.
- `~~health/quality-improvement` for CAPA/PDSA execution and monitoring.

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-02-12 | Initial health-incidents implementation with SAC, RCA, and mandatory reporting workflow |
