---
name: health/business-case
description: This skill should be used when developing business cases for healthcare investments, equipment, or service changes. Use when a user mentions investment justification, ROI calculation, healthcare business case, clinical service plan funding, or project risk assessment.
version: 1.0.0
---

# Healthcare Business Case Development

Structured guidance for the creation, financial justification, and risk assessment of business cases within a healthcare setting to ensure informed decision-making and optimal resource allocation.

**Important**: This skill assists with the drafting and structuring of business cases but does not provide financial or clinical advice. All business cases must be reviewed by the organization's Finance, Clinical Governance, and Executive leadership teams before submission for final approval.

## When to Use This Skill

Invoke when:
- Requesting funding for new medical equipment or technology.
- Proposing a change to a clinical service delivery model.
- Justifying the recruitment of new staff or creation of new roles.
- Developing an investment case for facility upgrades or new buildings.
- Evaluating the financial and clinical viability of a pilot project.
- Preparing for annual budget bids or strategic planning cycles.
- Identifying and documenting the risks associated with a proposed healthcare investment.

Do not use for routine minor purchasing (use `~~productivity/procurement`) or for purely clinical treatment plans (use `~~health/clinical-risk-assessment`).

## Regulatory Context

| Regulation | Relevance | Key Requirements |
|------------|-----------|------------------|
| **AU/NZ Baseline** | Public Health Acts, Te Whatu Ora Funding Models | Compliance with government procurement and capital investment guidelines. Alignment with Activity-Based Funding (ABF) or relevant local models. |
| **US/EU-lite (optional)** | CMS Value-Based Purchasing, GDPR (for data projects) | Focus on Value-Based Care, patient outcomes per dollar spent, and data privacy impact. |

### Financial Governance Triggers
- **Thresholds**: Business cases are usually required for investments exceeding specific dollar amounts (e.g., >$50k).
- **Audit**: Every approved business case creates a baseline for post-implementation review (PIR).

## Quick Reference

1.  **Define Executive Summary**: State the "bottom line" clinical and financial impact.
2.  **State the Problem/Opportunity**: Why is this investment needed now?
3.  **Align with Strategy**: How does this link to the organization's 5-year plan?
4.  **Identify Options**: Compare "Do Nothing", "Preferred Option", and "Alternative Option".
5.  **Clinical Justification**: Document the patient safety and quality benefits.
6.  **Financial Analysis**: Calculate TCO, ROI, and Payback Period.
7.  **Risk Assessment**: Identify clinical, financial, and operational risks.
8.  **Implementation Plan**: Outline the high-level roadmap and milestones.
9.  **Stakeholder Endorsement**: List the clinical and administrative supporters.

## Detailed Guidance

### 1. Business Case Structure
A high-quality healthcare business case must include:

#### Strategic Case
- **Strategic Fit**: Link to national health targets or local strategic pillars.
- **Benefits Realization**: Specific, measurable clinical and operational improvements.

#### Economic Case
- **Options Appraisal**: Qualitative and quantitative comparison of different paths.
- **Value for Money**: Why the preferred option provides the best outcome for the cost.

#### Commercial Case
- **Market Analysis**: Overview of available vendors and solutions.
- **Procurement Strategy**: Leasing vs. buying, or Managed Service contracts.

#### Financial Case
- **Capital Cost**: Initial purchase and installation.
- **Operating Cost**: Annual maintenance, consumables, and staffing impact.
- **Funding Source**: Identified budget line or grant opportunity.

#### Management Case
- **Governance**: Project board and reporting structure.
- **Timeline**: Critical path and expected "Go-Live" date.

### 2. ROI Calculation Guidance
In healthcare, ROI includes both financial and "Social/Clinical ROI":
- **Financial Savings**: Reduced length of stay (LOS), lower complication rates, or reduced outsourcing costs.
- **Efficiency Gains**: Clinician time saved (expressed in FTE equivalents).
- **Revenue Generation**: Increased throughput or access to new funding streams (e.g., private patients).
- **Clinical ROI**: Improved survival rates, reduced readmissions, or improved patient reported outcome measures (PROMs).

### 3. Risk Assessment Section
Every business case must address:
- **Clinical Risk**: Risk of the new service/device failing or causing harm.
- **Financial Risk**: Cost overruns or failure to realize expected savings.
- **Operational Risk**: Disruption to existing services during implementation.
- **Regulatory Risk**: Non-compliance with TGA/FDA or privacy laws.

## Documentation Requirements

- [ ] **Business Case Document**: Using the approved organizational template.
- [ ] **Financial Worksheet**: Detailed spreadsheet showing 5-10 year cash flow.
- [ ] **Stakeholder Matrix**: Record of consultation with Clinicians, IT, and Finance.
- [ ] **Risk Register**: Mitigation plans for the top 5 project risks.

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| Underestimating Ongoing Costs | Operating costs usually outweigh capital costs within 3 years. | Include service contracts, consumables, and electricity/gas needs. |
| Ignoring "Hidden" Stakeholders | Missing IT or Facilities input leads to installation delays and unbudgeted costs. | Consult every department affected by the device/service. |
| Over-optimistic Benefits | Leads to failure in post-implementation reviews and loss of credibility. | Use conservative, evidence-based projections for savings and gains. |
| Vague Clinical Justification | "Improved quality" is not a business case; it needs data. | Use specific metrics like "Expected reduction in infection rate by 15%". |
| Forgetting the "Do Nothing" Option | Fails to provide a baseline for comparison and evaluation. | Always document the clinical and financial risk of the status quo. |

## When to Escalate

Escalate to the Project Sponsor or Finance Director when:
- The preferred option involves a significant conflict of interest.
- The financial analysis reveals that the investment will never reach a break-even point.
- A critical clinical stakeholder opposes the proposed service change.
- The project involves high-risk "Sovereign Data" or offshore hosting.

## Privacy Considerations

- **PHI involved**: Usually No, unless the business case contains patient data for research justification.
- **Data minimization**: Use aggregated clinical data rather than individual patient records.
- **Retention**: Business cases should be retained for 10-15 years according to capital investment policies.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Standard equipment replacement with a clear positive ROI | High | Propose the draft business case and financial summary. |
| New service model with complex cross-departmental impacts | Medium | Guide the structure but require SME input for operational flow. |
| Investment in experimental technology with no established ROI | Low | REQUIRE a detailed "Pre-mortem" and Ethics Committee review. |

## Standard and Lite Modes

- **Standard**: Full multi-disciplinary business case for major capital or service changes.
- **Lite**: Short-form "Memorandum of Justification" for low-cost items or urgent clinical needs.

## Tool Requirements

- `~~finance/roi-template` - For financial modeling.
- `~~project tracker` - For milestone and task tracking.
- `~~cloud storage` - For document collaboration.

## Success Indicators

You've applied this skill well when:
- [ ] The strategic link to organizational goals is explicit.
- [ ] Financial analysis includes Total Cost of Ownership (TCO).
- [ ] Clinical benefits are defined with measurable KPIs.
- [ ] A multi-disciplinary stakeholder group has been consulted.
- [ ] Risks are identified with corresponding mitigation strategies.

## Related Skills

- `~~health/device-procurement` - For the technical evaluation of the items being requested.
- `~~finance/audit-support` - For aligning with organizational financial standards.
- `~~health/quality-improvement` - For tracking the benefits after implementation.
