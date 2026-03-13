---
name: health/enterprise-risk-assessment
description: This skill should be used when assessing strategic, operational, financial, and reputational risks for a healthcare organization. Use when a user mentions enterprise risk management (ERM), strategic risk, clinical governance, financial sustainability, reputation risk, regulatory compliance, or board-level risk reporting.
version: 1.0.0
---

# Enterprise Risk Assessment

Structured guidance for identifying, scoring, treating, and monitoring risks that impact the strategic objectives, financial viability, and overall reputation of a healthcare organization.

**Important**: This skill supports senior executive and board-level risk governance. It focuses on high-level organizational risks and should be used in conjunction with clinical and worker safety assessments. It does not replace professional financial, legal, or strategic consulting advice.

## When to Use This Skill

Invoke when:
- Conducting an annual or quarterly Enterprise Risk Management (ERM) review.
- Developing or updating the organization's Strategic Risk Register.
- Assessing risks associated with major capital projects, mergers, or service expansions.
- Evaluating the impact of significant regulatory or funding changes (e.g., new activity-based funding models).
- Addressing enterprise-level threats such as cyberattacks, large-scale clinical failures, or major workforce shortages.
- Preparing for board risk sub-committee meetings or executive leadership retreats.

Do not use for individual patient safety events (use `~~health/clinical-risk-assessment`) or local occupational hazards (use `~~health/worker-risk-assessment`).

## Operating Modes

### Standard Mode
Full enterprise risk governance workflow:
- Alignment with ISO 31000 or COSO ERM frameworks.
- Detailed analysis across Strategic, Operational, Financial, Compliance, and Reputational domains.
- Assessment of risk appetite and tolerance levels.
- Documentation of executive ownership and board oversight.
- Integration with the organization's strategic planning and budgeting cycles.

### Lite Mode
High-level risk scan or "Pre-mortem" for a specific initiative:
- Identification of top 5-10 strategic threats.
- Rapid scoring of impact and likelihood.
- Preliminary identification of mitigation strategies.
- Useful for project steering committees or early-stage strategy sessions.

## Regulatory Context

Default jurisdiction is Australia/New Zealand. Use US/EU-lite framing only when explicitly requested.

| Jurisdiction | Framework/Statute | Compliance Trigger | Review Cadence | Required Artifacts | Escalation Point |
|---|---|---|---|---|---|
| Australia | ISO 31000, Corporations Act (for relevant entities), NSQHS Standards (Clinical Governance) | Annual review, significant adverse event, regulatory change | Quarterly for Board, Monthly for Exec | Enterprise Risk Register, Board Risk Report | Board Risk Committee, CEO |
| New Zealand | ISO 31000, Crown Entities Act 2004, Te Whatu Ora governance frameworks | Planning cycle, national health directive change | Quarterly | Strategic Risk Profile, Governance Statement | Board, Chief Executive |
| United States (lite) | COSO ERM Framework, Sarbanes-Oxley (if applicable), CMS regulations | Fiscal year start, major audit findings | Quarterly | ERM Dashboard, Compliance Report | Audit & Risk Committee, CFO |
| European Union (lite) | ISO 31000, country-specific health system governance codes | Strategy review, major public health event | Bi-annual or Quarterly | Risk Landscape Report | Supervisory Board, Director General |

## Quick Reference

1. **Scan the Horizon**: Identify external (political, economic, regulatory, technological) and internal (workforce, clinical, financial) threats.
2. **Categorize**: Assign risks to domains (Strategic, Operational, Financial, Compliance, Reputational).
3. **Assess Inherent Risk**: Score impact and likelihood on the organization's strategic objectives.
4. **Identify Controls**: Focus on governance structures, policies, audits, and financial hedges.
5. **Determine Residual Risk**: Evaluate if the risk sits within the organization's **Risk Appetite**.
6. **Assign Accountability**: Ensure an Executive Lead is responsible for each major risk.

## Risk Assessment Framework

### Enterprise Impact (Consequence) Scale

| Level | Label | Strategic / Reputational | Financial | Clinical / Operational |
|---|---|---|---|---|
| 1 | **Minor** | Localized negative publicity; minor objective delay | <1% of budget; manageable locally | Negligible impact on service delivery |
| 2 | **Moderate** | Short-term media interest; minor regulator inquiry | 1-3% of budget; requires re-allocation | Brief service disruption in one department |
| 3 | **Serious** | Sustained media coverage; formal regulatory intervention | 3-5% of budget; affects capital plan | Significant service reduction; accreditation at risk |
| 4 | **Major** | Significant loss of public trust; major regulatory breach | 5-10% of budget; requires emergency funding | Systemic service failure; multiple site impacts |
| 5 | **Catastrophic** | Total loss of license/trust; organizational collapse | >10% of budget; insolvency risk | Permanent closure of core services; catastrophic harm |

### Enterprise Likelihood Scale

| Level | Label | Description | Probability |
|---|---|---|---|
| 1 | **Rare** | Only in exceptional circumstances; no industry precedent | <5% |
| 2 | **Unlikely** | Has occurred in other organizations but not locally | 5-25% |
| 3 | **Possible** | Might occur at some time; industry-wide trend | 25-50% |
| 4 | **Likely** | Will probably occur; clear local vulnerability | 50-75% |
| 5 | **Almost Certain** | Expected to occur; high frequency or systemic issue | >75% |

## Enterprise Risk Domains

| Domain | Focus | Key Indicators |
|---|---|---|
| **Strategic** | Ability to achieve long-term goals | Market share, clinical outcomes, innovation rate |
| **Operational** | Effectiveness of internal processes | Wait times, staffing ratios, system downtime |
| **Financial** | Sustainability and resource management | EBITDA, cash on hand, payer mix, insurance coverage |
| **Compliance** | Meeting legal and regulatory requirements | Audit findings, breach reports, credentialing status |
| **Reputational** | Public and stakeholder perception | Media sentiment, patient satisfaction, donor confidence |

## Documentation Standards

### Enterprise Risk Register Format

| Field | Description |
|---|---|
| Risk Title | Concise name (e.g., "Workforce Shortage - Specialty Nursing") |
| Category | Strategic, Operational, etc. |
| Risk Owner | Executive Lead (e.g., Chief Nursing Officer) |
| Risk Description | The "Event -> Cause -> Impact" narrative |
| Inherent Risk | Impact x Likelihood |
| Controls | Governance, Policies, Audits, Systems |
| Residual Risk | After controls |
| Risk Appetite | Within / Outside / Close to |
| Action Plan | Specific strategic initiatives to mitigate |
| Last Review | Date and brief update on status |

## Security & Privacy Considerations

- **Commercial-in-Confidence**: Enterprise risk documents often contain sensitive financial or strategic data. Protect with restricted access.
- **Regulatory Privilege**: In some jurisdictions, certain risk reviews (e.g., Quality Assurance Committees) may have statutory protection from discovery. Ensure these are marked correctly.
- **De-identification**: While patient data is rarely in ERM reports, avoid using specific clinician or staff names where a role title suffices.

## Confidence Indicators

| Scenario | Confidence | Action |
|---|---|---|
| Clear financial or compliance risk with established metrics | High | Propose risk entry and mitigation plan based on standard templates |
| Emergent strategic shift with high uncertainty | Medium | Produce "Scenario Analysis" rather than a single score; highlight assumptions |
| Reputational risk based on anecdotal or early-stage social media sentiment | Low | Recommend sentiment monitoring; do not score until evidence of sustained impact |
| Risk involving complex legal or constitutional changes | Low | Flag as "Under Review"; require expert legal/governance opinion |

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---|---|---|
| Setting "Risk Appetite" to zero for all risks | Stifles innovation and is realistically impossible in healthcare | Define clear, tiered appetite levels (e.g., "Averse" for safety, "Open" for innovation) |
| Confusing "Issues" with "Risks" | An issue is happening now; a risk is a future event | Manage issues in operations; track risks in the register |
| Using the ERM as a "Set and Forget" list | Risk profiles change rapidly; outdated registers provide false assurance | Integrate risk review into monthly executive meetings |
| Failing to link enterprise risks to clinical data | Organizational failure often starts with clinical deterioration | Ensure the ERM reflects high-level trends from clinical risk registers |
| Assigning enterprise risks to mid-level managers | If it's an enterprise risk, it needs an executive owner with budget authority | Assign ownership to C-suite or Executive Director level |

## When to Escalate

- **Risk Appetite Breach**: Any residual risk score that exceeds the board-approved appetite for that category.
- **New Emerging Threat**: Sudden external changes (e.g., global pandemic, sudden withdrawal of a major insurer).
- **Control Failure**: Identification that a major strategic control (e.g., clinical governance framework) is ineffective.
- **Media/Regulator Crisis**: Any event likely to cause sustained level 4-5 reputational impact.

## Tool Requirements

- `~~finance/financial-reports` for sustainability data.
- `~~legal/compliance-tracker` for regulatory status.
- `~~health/clinical-governance-dashboard` for high-level safety trends.
- `~~search` for industry benchmarking and competitor analysis.

## Success Indicators

- [ ] Risks are linked to specific strategic objectives.
- [ ] Executive ownership is clearly assigned.
- [ ] Scoring reflects organizational-wide impact (not just local).
- [ ] Controls are systemic (governance/policy) rather than just operational.
- [ ] Risk appetite alignment is explicitly evaluated.
- [ ] Confidentiality of strategic data is maintained.

## Related Skills

- `~~health/clinical-risk-assessment` for the clinical foundation of ERM.
- `~~health/worker-risk-assessment` for workforce safety impact on operations.
- `~~finance/variance-analysis` for financial risk identification.

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-02-12 | Initial enterprise risk assessment skill focusing on ERM, strategic objectives, and governance |
