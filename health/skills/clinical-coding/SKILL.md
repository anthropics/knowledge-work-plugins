---
name: health/clinical-coding
description: This skill should be used when classifying clinical documentation into standardized codes (ICD-10-AM, ICD-11, SNOMED-CT) or validating existing coding for research, billing, or population health. Use when a user mentions coding clinical notes, DRG assignment, ICD lookup, terminology mapping, or ACHI procedures.
version: 1.0.0
---

# Clinical Coding and Classification

Guidance for the accurate translation of clinical documentation into standardized codes for clinical governance, research, financial management, and population health reporting.

**Important**: This skill assists with clinical coding workflows but does not provide clinical advice or definitive coding for financial reimbursement without review by a certified Clinical Coder. All coding must be validated against current official classification standards and clinical documentation.

## When to Use This Skill

Invoke when:
- Classifying clinical diagnoses and procedures using ICD-10-AM, ICD-11, or ACHI.
- Mapping clinical terms to SNOMED-CT for electronic health records (EHR) interoperability.
- Validating the accuracy of coded research datasets.
- Reviewing clinical documentation for coding specificity (e.g., identifying missing acuity or complications).
- Analyzing Diagnosis Related Group (DRG) assignments for clinical services planning.
- Assisting in the preparation for coding audits or quality reviews.
- Mapping between different classification versions or systems.

Do not use for direct patient billing in jurisdictions requiring certified coder signatures without explicit human verification.

## Regulatory Context

| Jurisdiction | Regulator / Statute | Coding Standard | Compliance Trigger |
|--------------|---------------------|-----------------|---------------------|
| **AU/NZ (Baseline)** | IHACPA (AU), Te Whatu Ora (NZ) | ICD-10-AM/ACHI/ACS | Discharge, Clinical Coding Audit, Research Data Submission |
| **United States (Lite)** | CMS / NCHS | ICD-10-CM/PCS | Billing Cycle, Medicare/Medicaid Reporting |
| **European Union (Lite)** | National Health Authorities / WHO | ICD-10 / ICD-11 | Hospital Episode Statistics, Public Health Reporting |

### AU/NZ Specifics
- **Australian Coding Standards (ACS)**: The primary source for coding rules in Australia.
- **ICD-10-AM**: International Statistical Classification of Diseases and Related Health Problems, Tenth Revision, Australian Modification.
- **ACHI**: Australian Classification of Health Interventions.
- **DRG**: Australian Refined Diagnosis Related Groups (AR-DRG).

### US/EU-Lite Portability
- When US context is requested, use **ICD-10-CM** for diagnoses and **CPT/HCPCS/PCS** for procedures.
- When EU context is requested, use **ICD-10** or **ICD-11** as per the specific country's implementation.

## Quick Reference

1.  **Analyze Documentation**: Review the entire clinical record (discharge summary, operation notes, pathology).
2.  **Identify Principal Diagnosis**: The condition established after study to be chiefly responsible for occasioning the episode of care.
3.  **Identify Additional Diagnoses**: Conditions that exist at the time of admission or develop subsequently and affect patient management.
4.  **Identify Procedures**: Interventions that are surgical in nature, carry a procedural risk, require anaesthesia, or require specialized facilities.
5.  **Look Up Codes**: Use the Alphabetical Index first, then verify in the Tabular List.
6.  **Apply Standards**: Follow the Australian Coding Standards (or local equivalent) for specific rules (e.g., coding of diabetes, injuries).
7.  **Validate DRG**: Ensure the combination of codes correctly reflects the resource intensity and clinical complexity.
8.  **Document Rationale**: Note why specific codes were chosen if documentation is ambiguous.

## Detailed Guidance

### Clinical Coding Workflow

#### 1. Documentation Analysis
- **Discharge Summary**: Often the primary source, but must be validated against the clinical record.
- **Operation Reports**: Essential for accurate ACHI/CPT procedure coding.
- **Pathology/Radiology**: Use to add specificity to documented diagnoses (e.g., identifying the organism in pneumonia) but do not code from these results alone if the clinician hasn't documented the diagnosis.
- **Progress Notes**: Check for complications or comorbidities (CCs) that occurred during the admission.

#### 2. Diagnosis Coding (ICD-10-AM / ICD-11)
- **Principal Diagnosis (PDx)**: Must be the "condition established after study". If multiple conditions meet the criteria, follow the ACS hierarchy.
- **Additional Diagnoses (ADx)**: Only code if they require clinical evaluation, therapeutic treatment, diagnostic procedures, increased nursing care, or monitoring.
- **Specificity**: Always code to the highest level of specificity (e.g., "Type 2 diabetes mellitus with ketoacidosis" rather than just "Diabetes").

#### 3. Procedure Coding (ACHI / CPT)
- **Primary Procedure**: Usually the procedure performed for the principal diagnosis.
- **Component Procedures**: Do not code components of a procedure if they are integral to the main procedure (e.g., "Incision" as part of an "Appendicectomy").
- **Anaesthesia**: Ensure the appropriate anaesthesia code (e.g., General, Spinal, Sedation) is assigned for each procedure where required.

#### 4. Terminology Mapping (SNOMED-CT)
- Use SNOMED-CT for granular clinical terminology in the EHR.
- Map SNOMED-CT concepts to ICD-10 for statistical and financial reporting.
- Use the **Reference Sets (RefSets)** provided by the Australian Digital Health Agency (or equivalent) for specific clinical domains.

#### 5. DRG Assignment and Complexity
- Understand how Additional Diagnoses impact the **Complexity Level** (e.g., with or without CCs).
- Monitor for **Major Diagnostic Categories (MDCs)** to ensure the episode is grouped correctly.

## Documentation Requirements

- [ ] **Principal Diagnosis**: Explicitly identified with rationale if ambiguous.
- [ ] **Additional Diagnoses**: Evidence of management in the clinical record.
- [ ] **Procedures**: Linked to the relevant clinical intervention documentation.
- [ ] **Classification Version**: Specify which version (e.g., ICD-10-AM 12th Ed) was used.
- [ ] **Coding Queries**: Documentation of any queries sent to clinicians for clarification.
- [ ] **DRG Assignment**: The final grouped DRG and its description.

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| Coding from pathology results only | Clinicians must confirm the diagnosis; results alone are not a diagnosis. | Query the clinician if a result is significant but undocumented. |
| Coding "Symptoms" instead of "Diagnosis" | Once a definitive diagnosis is made, the symptoms are integral and not coded separately. | Code the definitive diagnosis (e.g., "Pneumonia" instead of "Cough and Fever"). |
| Including "History of" conditions as active | Historical conditions only code if they impact the current admission management. | Use "Z" codes for relevant history if they meet the ADx criteria. |
| Missing "Complications of Care" | Failure to code iatrogenic injuries or infections leads to inaccurate quality data. | Monitor for and code post-operative infections, falls, or pressure injuries. |
| Unbundling procedures | Coding every step of a surgery separately leads to incorrect resource reporting. | Use the comprehensive code for the main procedure performed. |

## When to Escalate

Escalate to a Senior Clinical Coder or Health Information Manager (HIM) when:
- There is a conflict between different parts of the clinical record (e.g., surgeon says one thing, pathologist says another).
- The documentation is illegible or significantly incomplete.
- A "Query to Clinician" is required for a high-impact diagnosis.
- The coding involves a complex "New Technology" not yet covered by standard classifications.
- There is suspicion of "Upcoding" or "DRG Creep" without clinical justification.

## Privacy Considerations

- **PHI involved**: Yes. Coding involves highly sensitive clinical data.
- **Data minimization**: Use only the documentation required to assign the correct codes.
- **De-identification**: For research datasets, ensure that the mapping process does not inadvertently re-identify patients through rare code combinations.
- **Retention**: Coded data should be stored within the secure hospital information system; do not retain local copies of identifiable clinical notes.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Unambiguous documentation with direct ICD-10-AM index match | High | Propose code and document rationale. |
| Documentation uses vague terms (e.g., "Possible", "Likely", "?") | Medium | Flag for human review; suggest a clinician query. |
| Complex multi-organ failure with multiple procedures and conflicting notes | Low | Draft a coding summary and REQUIRE review by a Senior Coder. |

## Standard and Lite Modes

- **Standard**: Full coding workflow including documentation review, standard application, and DRG verification.
- **Lite**: Rapid code lookup and terminology mapping for non-reporting purposes (e.g., quick research search terms).

## Tool Requirements

- `~~health/clinical-systems` - For EHR access.
- `~~health/icd-10` - For code lookup.
- `~~health/snomed-browser` - For terminology mapping.
- `~~project tracker` - For managing coding queries.

## Success Indicators

You've applied this skill well when:
- [ ] Every assigned code is supported by clinical documentation.
- [ ] The Principal Diagnosis meets the ACS/WHO definition.
- [ ] Coding specificity is maximized (e.g., appropriate 4th/5th characters).
- [ ] Common mistakes/anti-patterns have been avoided.
- [ ] DRG assignment reflects the clinical complexity.

## Related Skills

- `~~health/data-validation` - Patterns for validating health datasets.
- `~~health/manuscript-prep` - For reporting coded data in research.
- `~~health/incident-reporting` - For coding complications and safety events.
