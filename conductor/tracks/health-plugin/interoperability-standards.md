# Health Interoperability & Evidence Standards

To ensure the `health` plugin integrates with modern healthcare ecosystems and maintains the highest levels of scientific rigor, all skills must adhere to these data and evidence standards.

## 1. Data Interoperability Standards
Whenever a skill involves structured clinical data (Exchange, Analysis, or Reporting), it should reference and align with international standards.

- **FHIR (Fast Healthcare Interoperability Resources):** Use FHIR R4/R5 terminology and resource structures (e.g., `Patient`, `Observation`, `Condition`, `MedicationRequest`) where applicable.
- **SNOMED-CT / LOINC:** Prefer these terminologies for clinical findings and lab results.
- **ICD-10-AM / ICD-11:** For clinical coding and diagnostic grouping.
- **HL7 v2/v3:** For legacy system messaging patterns.

### AU/NZ-first Interoperability Profile
- Default to AU/NZ-compatible coding and reporting assumptions when jurisdiction is not specified.
- Prefer ICD-10-AM where Australian coding guidance is required.
- Include NZ-compatible terminology notes where coding or reporting obligations differ.

### US/EU-lite Portability
- Provide lightweight portability notes for US/EU requests without replacing AU/NZ defaults.
- Avoid deep jurisdiction-specific implementation detail unless explicitly requested.

## 2. Hybrid Evidence Management
Following the user's preferred strategy, skills involving evidence (Research, Guidelines, Manuscripts) must implement a **Hybrid Evidence Management** approach:

### A. Strict Citation
- Every clinical claim must be backed by a specific source.
- Use structured citation formats (e.g., Vancouver or APA) as required by the context.
- Include a "Evidence Level" indicator (e.g., NHMRC Levels I-IV or GRADE) for major recommendations.

### B. Narrative Referencing
- Evidence should be integrated into the narrative flow, explaining *why* a source is relevant to the current patient/case context.
- Avoid "source dumping"; prioritize synthesis.

### C. Workstream Mapping
- Map evidence directly to the current task or decision point.
- Show the "line of sight" from a research finding to a clinical action or policy recommendation.

## 3. Workflow Integration & Persona Adaptation
Healthcare workflows are highly role-dependent. Skills should include guidance on how the output changes based on the user persona.

| Persona | Primary Goal | Output Style |
|---------|--------------|--------------|
| Clinician | Patient safety, efficiency | Concise, actionable, risk-focused |
| Administrator | Compliance, throughput | Data-driven, policy-aligned |
| Researcher | Rigor, reproducibility | Methodological, highly cited |
| Patient | Understanding, consent | Plain language, empathetic |

## 4. Evidence Quality Gates
For evidence-heavy tracks (`health-evidence`, `health-manuscripts`, `health-economics`):
- [ ] PRISMA/CONSORT/STROBE compliance checklist included.
- [ ] Risk of Bias (RoB) assessment framework defined.
- [ ] Evidence grading (GRADE) integrated into recommendations.
- [ ] Reproducibility checklist for data analysis steps.
