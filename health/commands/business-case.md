---
name: business-case
description: Draft a healthcare business case structure with clinical justification, financial analysis, and risk assessment.
arguments:
  - name: project_title
    description: "The name of the clinical initiative or equipment purchase."
    required: true
  - name: objective
    description: "The primary clinical or operational goal."
    required: true
  - name: estimated_cost
    description: "Total project cost including capital and operating."
    required: true
  - name: key_benefit
    description: "The most significant patient safety or quality improvement expected."
    required: true
---

# Business Case Draft

Use this command to generate a structured healthcare business case draft ready for stakeholder review and financial modeling.

## 1. Structure Development (Invoke Skill)

Use `~~health/business-case` to:
1. Align the `objective` with **Strategic Goals**.
2. Draft the **Clinical Justification** based on the `key_benefit`.
3. Outline the **Economic Case** (TCO and preliminary ROI).
4. Identify the top 3 **Risks** and mitigations.

## 2. Generate Structured Output

Produce:

### BUSINESS CASE DRAFT: {{project_title}}
- **Reference**: [Generate unique ID]
- **Date**: {{current_timestamp}}
- **Status**: DRAFT (Not for submission)

### 1. EXECUTIVE SUMMARY
[Draft a 2-3 sentence summary of the need, cost, and benefit]

### 2. CLINICAL JUSTIFICATION
- **The Problem**: [Describe the clinical gap being addressed]
- **The Solution**: {{objective}}
- **Patient Impact**: {{key_benefit}}

### 3. FINANCIAL SUMMARY
- **Total Investment**: {{estimated_cost}}
- **Operating Model**: [Lease/Buy/Grant]
- **Preliminary ROI**: [Expected timeline to realize benefits]

### 4. RISK PROFILE
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Clinical Risk] | [High/Med/Low] | [Action] |
| [Financial Risk] | [High/Med/Low] | [Action] |
| [Operational Risk] | [High/Med/Low] | [Action] |

### 5. NEXT STEPS
1. [ ] **Financial Review**: Detailed ROI analysis with Finance team.
2. [ ] **Stakeholder Meeting**: Present draft to Clinical Governance Committee.
3. [ ] **Market Analysis**: Request quotes from at least 3 vendors.

## 3. Execute Routing

- Save draft to `~~cloud storage`.
- Notify the Project Lead and Finance Liaison.

## 4. Output Guardrails

- **Confidentiality**: Mark the output as **Commercial-in-Confidence**.
- **No PHI**: Ensure no patient-identifiable data is included in the draft text.
