---
name: validate-coding
description: Validate clinical coding accuracy and classification mapping against documentation summary.
arguments:
  - name: diagnosis_codes
    description: "Comma-separated list of ICD-10/ICD-11 diagnosis codes to validate."
    required: true
  - name: procedure_codes
    description: "Optional: Comma-separated list of ACHI/CPT procedure codes."
    required: false
  - name: summary
    description: "Clinical summary or documentation fragment to validate codes against. Do not include PHI."
    required: true
  - name: classification_system
    description: "The classification system used (e.g., ICD-10-AM, ICD-11, ICD-10-CM)."
    required: true
---

# Validate Coding

Use this command to verify that the selected clinical codes accurately reflect the provided documentation summary and comply with classification standards.

## 1. Skill Activation

Activate `~~health/clinical-coding` to perform the validation.

## 2. Validation Workflow

1.  **Code Lookup**: Verify each code exists in the specified `classification_system`.
2.  **Documentation Alignment**: Check if the `summary` supports the principal and additional diagnoses.
3.  **Standard Compliance**: Apply relevant coding standards (e.g., ACS) to the code combination.
4.  **Inconsistency Identification**: Highlight any codes not supported by the summary or missing diagnoses/procedures.
5.  **Mapping Check**: If applicable, verify mapping between systems (e.g., SNOMED to ICD-10).

## 3. Generate Structured Output

Produce:

### CODING VALIDATION REPORT
- **Reference ID**: [Generate unique ID]
- **Timestamp**: {{current_timestamp}}
- **Classification System**: {{classification_system}}

### CODE SUMMARY
- **Principal Diagnosis**: [Code] - [Description] (VALID / INVALID / PARTIAL)
- **Additional Diagnoses**:
  - [Code] - [Description] (VALID / INVALID)
- **Procedures**:
  - [Code] - [Description] (VALID / INVALID)

### VALIDATION FINDINGS
- **Strengths**: [What was coded correctly]
- **Inconsistencies**: [List specific mismatches between codes and summary]
- **Potential Omissions**: [Diagnoses/procedures mentioned in summary but not coded]
- **Specificity Alerts**: [Suggestions for more specific codes based on summary]

### RECOMMENDATIONS
- **Suggested Changes**: [List specific code additions, removals, or changes]
- **Clinician Query Needed**: [Yes/No] - [Draft query if yes]
- **Standard Reference**: [Reference specific ACS or WHO standards applied]

## 4. Execute Routing

- Log validation result in `~~project tracker` if part of a quality audit.
- If **INVALID** or **OMISSION** detected, flag for review by a certified Clinical Coder.

## 5. Output Guardrails

- **No PHI**: Ensure the clinical summary used for validation is de-identified.
- **Assistance Only**: Clearly state that this validation is an AI-assisted check and requires human verification for final submission.
