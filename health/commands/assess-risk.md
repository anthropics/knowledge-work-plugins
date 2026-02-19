---
name: assess-risk
description: Structured risk assessment intake for clinical, worker, or enterprise domains with scoring, control recommendations, and governance routing.
arguments:
  - name: risk_domain
    description: "The primary domain for assessment: clinical, worker, or enterprise."
    required: true
  - name: summary
    description: "Short description of the hazard or risk scenario. Avoid names or identifiers."
    required: true
  - name: initial_impact
    description: "Preliminary impact/consequence score (1-5)."
    required: true
  - name: initial_likelihood
    description: "Preliminary likelihood score (1-5)."
    required: true
  - name: jurisdiction
    description: "Optional: au, nz, us, or eu. Defaults to au-nz if omitted."
    required: false
---

# Assess Risk

Use this command to initiate a formal risk assessment workflow, calculate scores, and identify required controls and governance paths.

## 1. Domain Selection and Skill Activation

Route to the appropriate skill based on `risk_domain`:
- If `clinical`: Use `~~health/clinical-risk-assessment`
- If `worker`: Use `~~health/worker-risk-assessment`
- If `enterprise`: Use `~~health/enterprise-risk-assessment`

## 2. Risk Analysis

For the selected domain:
1. Validate impact and likelihood rationales against the domain-specific scale.
2. Calculate the **Inherent Risk Score** (Impact x Likelihood).
3. Identify relevant existing controls.
4. Recommend additional controls following the appropriate hierarchy (e.g., Clinical adaptation or WHS Hierarchy).
5. Calculate the **Residual Risk Score**.

## 3. Generate Structured Output

Produce:

### RISK ASSESSMENT SUMMARY
- **Risk ID**: [Generate unique ID]
- **Date**: {{current_timestamp}}
- **Domain**: {{risk_domain}}
- **Hazard Summary**: [Factual description]
- **Jurisdiction**: {{jurisdiction or "AU/NZ default"}}

### SCORING & CLASSIFICATION
- **Inherent Risk**: {{initial_impact}} x {{initial_likelihood}} = [Inherent Score] ([LEVEL])
- **Rationale**: [Brief explanation of why these scores were assigned]

### RECOMMENDED CONTROLS
1. [Primary Control - Hierarchy Level]
2. [Secondary Control - Hierarchy Level]
3. [Administrative/Monitoring Control]

### RESIDUAL RISK
- **Target Score**: [Residual Score] ([LEVEL])
- **Acceptance Threshold**: [Within Appetite / Requires Escalation]

### GOVERNANCE & ACCOUNTABILITY
- **Risk Owner**: [Recommended Role]
- **Governance Pathway**: [Local review / Governance Committee / Board]
- **Review Frequency**: [Daily/Weekly/Monthly/Quarterly/Annually]

## 4. Execute Routing

- Log risk entry in `~~project tracker`.
- For **ORANGE (High)** or **RED (Extreme)** risks:
  - Notify domain Executive (CMO, HR Director, or CEO/CFO).
  - Add to the next Governance Committee agenda.
  - For Extreme risks, initiate the immediate executive briefing protocol.

## 5. Output Guardrails

- **De-identification**: Ensure the summary and rationale do not contain PHI or PII.
- **Provisional Status**: If likelihood or impact rationale is weak, mark the assessment as **Provisional** and request clinical/management review.
- **Precautionary Principle**: For high-consequence scenarios with low-confidence likelihood, default to the higher risk level for initial treatment.
