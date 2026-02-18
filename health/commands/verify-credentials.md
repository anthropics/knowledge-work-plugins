---
name: verify-credentials
description: Initiate and track Primary Source Verification (PSV) for a healthcare provider's qualifications, license, and background.
arguments:
  - name: provider_name
    description: "The full legal name of the provider to be verified."
    required: true
  - name: provider_type
    description: "Type of provider (e.g., medical, nursing, allied-health, student)."
    required: true
  - name: verification_items
    description: "Comma-separated list of items to verify (e.g., license, degree, indemnity, board-cert)."
    required: true
  - name: jurisdiction
    description: "Optional: au, nz, us, or eu. Defaults to au-nz if omitted."
    required: false
---

# Verify Credentials

Use this command to initiate the formal credentialing verification workflow and generate a status tracking report for a specific provider.

## 1. Skill Activation

Activate `~~health/credentialing` to perform the verification procedures.

## 2. Verification Workflow

1.  **Item Identification**: Map the `verification_items` to the appropriate primary sources for the `jurisdiction`.
2.  **Regulatory Check**: Perform a real-time check of the provider's registration status (e.g., AHPRA, MCNZ).
3.  **Discrepancy Screening**: Check for name variations or previous disciplinary actions.
4.  **Requirement Mapping**: Identify any missing mandatory items based on `provider_type`.
5.  **Status Generation**: Update the tracking record for each requested item.

## 3. Generate Structured Output

Produce:

### CREDENTIAL VERIFICATION INITIATION
- **Case ID**: [Generate unique ID]
- **Timestamp**: {{current_timestamp}}
- **Provider**: {{provider_name}} ({{provider_type}})
- **Jurisdiction**: {{jurisdiction or "AU/NZ default"}}

### PRIMARY SOURCE VERIFICATION STATUS
| Item | Source | Status | Finding/Link |
|------|--------|--------|--------------|
| [Item 1] | [Source 1] | [INITIATED / VERIFIED / DEFICIENT] | [Result] |
| [Item 2] | [Source 2] | [INITIATED / VERIFIED / DEFICIENT] | [Result] |

### REGULATORY STANDING
- **Registration ID**: [Identified ID]
- **Current Status**: [Active / Suspended / Conditions]
- **Expiry Date**: [Date]
- **Disciplinary Alerts**: [None / Under Review / Formal Action]

### NEXT STEPS
- **Missing Info**: [List any items required from the provider]
- **Follow-up Action**: [e.g., Contact University, Request Indemnity Cert]
- **Target Completion**: [Timestamp + 14 days]

## 4. Execute Routing

- Create/Update provider profile in `~~project tracker`.
- If **DEFICIENT** or **SUSPENDED** status is found:
  - Notify Medical Director/Director of Nursing immediately.
  - Block clinical onboarding task in HR system.

## 5. Output Guardrails

- **Sensitive PII**: Do not output the provider's DOB or home address in the summary report.
- **Provisional Result**: Clearly mark the report as **In Progress** until all `verification_items` reach **VERIFIED** status.
