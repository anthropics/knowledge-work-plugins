---
name: report-incident
description: Intake and route a healthcare incident or serious adverse event with safety-first escalation and mandatory reporting checks.
arguments:
  - name: incident_type
    description: "Primary incident type (e.g., medication, device, infection, privacy, near-miss, sentinel)."
    required: true
  - name: severity
    description: "Preliminary severity level (SAC1/SAC2/SAC3/SAC4 or equivalent local level)."
    required: true
  - name: immediate_safety_risk
    description: "Is there current patient safety risk requiring immediate containment? (yes/no)"
    required: true
  - name: summary
    description: "Short factual description of what happened. Do not include names or direct identifiers."
    required: true
  - name: jurisdiction
    description: "Optional: au, nz, us, or eu. Defaults to au-nz baseline if omitted."
    required: false
---

# Report Incident

Use this command for rapid incident intake, initial severity routing, and investigation kickoff.

## 1. Validate Intake and Apply Safety Override

- Validate required fields.
- If `immediate_safety_risk` is `yes`, force priority to highest response path regardless of submitted severity.
- If severity is unknown, treat as provisional and route for urgent clinical review.

## 2. Invoke Skill

Use `~~health/incident-reporting` to:
1. Confirm taxonomy and severity rationale.
2. Execute immediate response protocol.
3. Screen for mandatory reporting triggers.
4. Assign investigation and QI follow-through.

## 3. Generate Structured Output

Produce:

### INCIDENT INTAKE REPORT
- **Incident ID**: [Generate unique ID]
- **Timestamp**: {{current_timestamp}}
- **Jurisdiction Assumed**: {{jurisdiction or "AU/NZ default"}}
- **Incident Type**: {{incident_type}}
- **Preliminary Severity**: {{severity}}
- **Immediate Safety Risk**: {{immediate_safety_risk}}
- **Summary (De-identified)**: [Summarize `summary` with no PHI/PII]

### IMMEDIATE ACTIONS
- **Containment Action**: [What was done first]
- **Clinical Owner**: [Role]
- **Escalations Sent**: [Roles + times]

### REGULATORY SCREEN
- **Potential Mandatory Trigger**: [Yes/No/Possible]
- **Reason**: [Short rationale]
- **Compliance/Legal Review Needed**: [Yes/No]

### NEXT STEPS
- **Investigation Path**: [Local review / Formal RCA]
- **RCA Owner**: [Role]
- **Due Dates**:
  - Acknowledgment: [Timestamp + local SLA]
  - Initial review: [Timestamp + local SLA]
  - Closure target: [Timestamp + local SLA]
- **QI Linkage**: [CAPA/PDSA ticket or placeholder]

## 4. Execute Routing

- Log incident package in `~~project tracker`.
- Notify clinical lead immediately for high-risk events.
- Notify risk/compliance/legal when trigger status is `Yes` or `Possible`.
- For sentinel-level scenarios, notify executive on-call pathway.

## 5. Output Guardrails

- Never output direct identifiers unless explicitly required by approved secure system workflow.
- If details are missing for safe classification, mark the report as **Provisional** and force human review.
