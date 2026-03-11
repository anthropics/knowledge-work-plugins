---
name: submit-complaint
description: Intake a new patient, staff, or visitor complaint with clinical safety and severity assessment.
arguments:
  - name: type
    description: "Type of complaint: 'clinician' (performance/conduct) or 'service' (facilities/admin/wait times)."
    required: true
  - name: severity
    description: "Initial severity assessment: P1 (Critical/Life Threat), P2 (High), P3 (Medium), P4 (Low)."
    required: true
  - name: patient_safety_concern
    description: "Does this complaint involve a potential or actual risk to patient safety? (yes/no)"
    required: true
  - name: description
    description: "Detailed description of the complaint. DO NOT include patient names or PHI."
    required: true
---

# Submit Complaint Command

Follow this workflow to process a new healthcare complaint.

## 1. Intake Validation
- Verify the `type` matches clinician or service.
- If `patient_safety_concern` is **yes**, automatically escalate the priority to **P1** regardless of the input `severity`.

## 2. Invoke Skills
Use `~~health/complaints-management` to:
1. Validate the severity against the healthcare framework.
2. Determine the appropriate investigation path (e.g., Clinical Lead vs. Operations Manager).
3. Identify jurisdictional deadlines (AU/NZ default).

## 3. Generate Documentation
Produce a structured intake report:

### COMPLAINT INTAKE REPORT
- **Reference ID**: [Generate unique ID]
- **Date/Time**: {{current_timestamp}}
- **Type**: {{type}}
- **Severity**: {{severity}}
- **Patient Safety Concern**: {{patient_safety_concern}}
- **Summary**: [Summarize description without PHI]

### NEXT STEPS
- **Acknowledgment**: Due by [Timestamp + 2 days]
- **Resolution Target**: Due by [Timestamp + 30 days]
- **Action**: [Specify routing, e.g., "Assigned to Medical Director for urgent review"]

## 4. Execution
- Log the intake in `~~project tracker`.
- Notify the relevant team lead based on the routing rules.
