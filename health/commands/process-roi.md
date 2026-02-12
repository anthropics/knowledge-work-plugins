---
name: process-roi
description: Intake and validate a healthcare Release of Information (ROI) request with authorization checks and "Minimum Necessary" guidance.
arguments:
  - name: request_type
    description: "Type of request (e.g., patient, legal, insurance, referral, research)."
    required: true
  - name: data_scope
    description: "Description of the information requested (e.g., 'All bloods Jan 2026', 'Full chart')."
    required: true
  - name: authorization_status
    description: "Has a signed authorization been received? (yes/no/pending)"
    required: true
  - name: summary
    description: "Short description of the purpose of the request. Do not include PHI."
    required: true
  - name: jurisdiction
    description: "Optional: au, nz, us, or eu. Defaults to au-nz if omitted."
    required: false
---

# Process ROI

Use this command for rapid ROI intake, authorization validation, and processing kickoff.

## 1. Validate Intake and Authorization

- Check `authorization_status`. If `no` or `pending`, flag as "Blocked" until documentation is received.
- Validate `request_type` against jurisdiction-specific rules (e.g., patient access vs. third-party).

## 2. Invoke Skill

Use `~~health/release-of-information` to:
1. Execute the **Authorization Validation Checklist**.
2. Perform a **"Minimum Necessary" Analysis** for the `data_scope`.
3. Screen for "Sensitive Content" or "Legal Hold" triggers.
4. Determine the processing timeline based on `jurisdiction`.

## 3. Generate Structured Output

Produce:

### ROI REQUEST INTAKE
- **Request ID**: [Generate unique ID]
- **Timestamp**: {{current_timestamp}}
- **Request Type**: {{request_type}}
- **Data Scope**: {{data_scope}}
- **Jurisdiction**: {{jurisdiction or "AU/NZ default"}}

### VALIDATION STATUS
- **Authorization Verified**: [Yes/No/Partial]
- **Identity Confirmed**: [Yes/No/Pending]
- **Authority Type**: [Patient / Proxy / Legal Order]
- **Deficiencies**: [List any missing requirements]

### PROCESSING GUIDANCE
- **Minimum Necessary Data Set**: [List specific records to be released]
- **Redaction Required**: [Yes/No] - [List targets: 3rd party names, sensitive codes]
- **Legal/Sensitive Flag**: [Clean / Sensitive Content / Legal Hold]

### NEXT STEPS
- **HIM Action**: [Wait for Auth / Pull Records / Redact / Release]
- **Timeline**:
  - Acknowledgment Due: [Timestamp + 5 days]
  - Decision Due: [Timestamp + local SLA]
  - Fulfillment Target: [Timestamp + local SLA]

## 4. Execute Routing

- Log ROI package in `~~project tracker`.
- For `Sensitive Content` or `Legal Hold` flags:
  - Notify HIM Manager immediately.
  - Notify Privacy/Legal as required.
- If `Authorization Verified` is `No`, send "Missing Information" request to the requester.

## 5. Output Guardrails

- **No PHI**: Never include patient names or identifiers in the output summary.
- **Provisional Result**: If `data_scope` is "Full Chart", force an HIM review to apply Minimum Necessary before fulfillment.
