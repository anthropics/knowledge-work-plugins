---
name: procurement-request
description: Initiate a medical device procurement request with preliminary regulatory and clinical screening.
arguments:
  - name: device_name
    description: "The name or type of medical device requested."
    required: true
  - name: clinical_purpose
    description: "The clinical problem the device is intended to solve."
    required: true
  - name: priority
    description: "Urgency of the request (Routine, Urgent, Emergency)."
    required: true
  - name: estimated_budget
    description: "Initial budget estimate if known."
    required: false
---

# Procurement Request

Use this command to intake a new medical device request and trigger the preliminary evaluation workflow.

## 1. Intake Validation

- Ensure `device_name` and `clinical_purpose` are clear.
- Categorize the request based on `priority`.

## 2. Preliminary Evaluation (Invoke Skill)

Use `~~health/device-procurement` to:
1. Identify the likely **ARTG/WAND classification** (Class I, IIa, IIb, III).
2. Perform a preliminary **Regulatory Screen** (TGA/FDA status).
3. Identify **Technical Dependencies** (Power, Network, EHR integration).
4. Outline the **Evaluation Path** (Standard trial vs. Bench review).

## 3. Generate Structured Output

Produce:

### PROCUREMENT INTAKE SUMMARY
- **Request ID**: [Generate unique ID]
- **Date**: {{current_timestamp}}
- **Device**: {{device_name}}
- **Priority**: {{priority}}
- **Clinical Lead**: [Role/Name of requester]

### PRELIMINARY SCREENING
- **Likely Classification**: [Class]
- **Regulatory Status**: [Found/Not Found/Pending]
- **Infrastructure Impact**: [None/Minor/Significant]

### ACTION PLAN
1. [ ] **Technical Review**: Clinical Engineering check for EHR/Power compatibility.
2. [ ] **Infection Control**: Review sterilization requirements.
3. [ ] **Financial Check**: Confirm budget availability for initial purchase and consumables.
4. [ ] **Clinical Trial**: Schedule 2-week pilot in [Department].

## 4. Execute Routing

- Create a ticket in `~~project tracker`.
- Notify the Department Head and Procurement Officer.
- For **Urgent** or **Emergency** requests, flag for immediate executive review.

## 5. Output Guardrails

- **Assistance Only**: Clearly state that this is an intake request and does not constitute approval to purchase.
- **No PII**: Ensure the requester's name is handled through the project tracker, not stored in the public command log.
