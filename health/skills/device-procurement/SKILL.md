---
name: health/device-procurement
description: This skill should be used when evaluating, selecting, and procuring medical devices for healthcare organizations. Use when a user mentions medical device procurement, TGA/FDA/CE compliance, vendor assessment, medical equipment evaluation, or healthcare device contracts.
version: 1.0.0
---

# Medical Device Procurement

Structured guidance for the evaluation, regulatory verification, and procurement of medical devices to ensure clinical safety, operational efficiency, and financial viability.

**Important**: This skill assists with the procurement workflow and regulatory screening but does not provide legal advice or definitive clinical endorsement. All device selections must be reviewed by the organization's Clinical Engineering (Biomedical), Infection Control, and Clinical Governance committees.

## When to Use This Skill

Invoke when:
- A clinical department requests a new medical device or piece of equipment.
- Reviewing vendor proposals for medical technology.
- Verifying the regulatory status (TGA, FDA, CE marking) of a device.
- Conducting a clinical trial or pilot of a new medical device.
- Drafting or reviewing healthcare-specific contract terms for equipment.
- Managing the replacement cycle for aging medical devices.
- Evaluating the total cost of ownership (TCO) for a medical investment.

Do not use for general office supply procurement (use `~~productivity/procurement`) or for pharmaceutical procurement (use `~~health/pharmacy-management`).

## Regulatory Context

| Regulation | Relevance | Key Requirements |
|------------|-----------|------------------|
| **AU/NZ Baseline** | TGA (AU), Medsafe (NZ), AS/NZS 3551 | Devices must be on the ARTG (AU) or WAND (NZ). Compliance with AS/NZS 3551 for management of medical devices. |
| **US/EU-lite (optional)** | FDA (US), MDR/IVDR (EU) | FDA 510(k) or PMA approval. CE marking under MDR (2017/745) or IVDR (2017/746). |

### Compliance Triggers
- **New Device Intake**: Immediate verification of ARTG/Medsafe registration.
- **Safety Alerts**: Ongoing monitoring of TGA/FDA recall databases.
- **Maintenance**: Annual safety testing according to AS/NZS 3551.

## Quick Reference

1.  **Define Clinical Need**: Document the specific problem the device solves.
2.  **Regulatory Screen**: Verify the device is registered for use in the jurisdiction.
3.  **Technical Evaluation**: Review specifications against organizational infrastructure.
4.  **Clinical Evaluation**: Conduct trials or review peer-reviewed clinical data.
5.  **Financial Analysis**: Calculate TCO including consumables and maintenance.
6.  **Vendor Assessment**: Evaluate vendor stability, support, and security.
7.  **Risk Assessment**: Identify safety, privacy, and integration risks.
8.  **Contract Review**: Ensure healthcare-specific clauses are present.
9.  **Governance Approval**: Submit to relevant committees for endorsement.

## Detailed Guidance

### 1. Device Evaluation Criteria
Evaluation must cover three primary domains:

#### Clinical Suitability
- **Efficacy**: Does the device improve patient outcomes according to Level I/II evidence?
- **Usability**: Is the interface intuitive for the intended clinical user?
- **Ergonomics**: Does the device design minimize physical strain or error?
- **Patient Safety**: Are there built-in fail-safes and clear alarms?

#### Technical Compatibility
- **Interoperability**: Does it connect to the EHR (HL7/FHIR) or VNA (DICOM)?
- **Infrastructure**: Does it require specific power, gas, or network (Wi-Fi/Ethernet)?
- **Maintenance**: Can the local Clinical Engineering team service it, or is it "Vendor-Only"?
- **Longevity**: What is the expected lifecycle and "End of Support" date?

#### Operational Impact
- **Workflow**: How does it change the current clinical workflow?
- **Training**: What is the learning curve and ongoing training requirement?
- **Storage**: Does the device require specialized storage or charging stations?

### 2. Regulatory Compliance Checklist (AU/NZ Default)
Before any medical device is purchased, verify:
- [ ] **ARTG Entry (Australia)**: Valid entry number and correct classification (Class I, IIa, IIb, III).
- [ ] **WAND Entry (New Zealand)**: Verification of notification to Medsafe.
- [ ] **Manufacturer Evidence**: Proof of QMS (ISO 13485) and Essential Principles compliance.
- [ ] **GMDN Code**: Correct Global Medical Device Nomenclature assigned.
- [ ] **IVD Status**: If diagnostic, verify In-Vitro Diagnostic compliance.

### 3. Vendor Assessment Framework
Evaluate potential vendors based on:
- **Financial Stability**: Can they support the device lifecycle?
- **Clinical Support**: Availability of clinical application specialists.
- **Technical Support**: Response times for repairs and spare parts availability.
- **Cybersecurity**: Compliance with the Manufacturer Disclosure Statement for Medical Device Security (MDS2).
- **Sustainability**: Environmental impact of the device and its disposal.

## Documentation Requirements

- [ ] **Business Case**: Justification for the investment.
- [ ] **Clinical Trial Report**: Summary of user feedback and outcomes.
- [ ] **TCO Worksheet**: 5-10 year cost projection.
- [ ] **MDS2 Form**: For networked or software-based devices.
- [ ] **Acceptance Testing Record**: Baseline safety and functional check.

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| Ignoring Consumable Costs | Long-term costs can exceed the initial purchase price by 5x. | Perform a full Lifecycle Cost Analysis (LCA). |
| Skipping Infrastructure Check | Device arrives but cannot connect to Wi-Fi or fit through doors. | Involve Clinical Engineering and IT at the "Discovery" phase. |
| Accepting "Demo" Units without ARTG | Clinical use of unregistered devices is a major regulatory breach. | Verify registration before any patient contact occurs. |
| Buying Based on "Feature Bloat" | Unused features increase cost and complexity without clinical benefit. | Buy against documented "Minimum Essential Requirements". |
| Neglecting De-commissioning | Old devices create storage clutter and safety/privacy risks. | Include disposal/data-wipe costs in the initial business case. |

## When to Escalate

Escalate to the Chief Medical Officer or Procurement Director when:
- A device is identified as being used without valid regulatory registration.
- A vendor is unable to provide an MDS2 for a network-connected device.
- Significant clinical variation or adverse events are reported during a trial.
- There is a conflict of interest between a clinician and a vendor.
- The procurement exceeds the delegated financial authority of the department.

## Privacy Considerations

- **PHI involved**: Software-based devices often store or transmit patient data.
- **Data minimization**: Ensure devices only capture and transmit necessary clinical parameters.
- **De-identification**: Verify that "Export" functions for research de-identify data appropriately.
- **Retention**: Local storage on devices should be encrypted and cleared according to policy.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Standard replacement of an ARTG-registered, Class I device | High | Propose procurement path and checklist. |
| Procurement of a new Class III invasive device | Medium | Guide the evaluation but require SME clinical lead review. |
| Device involves novel AI/ML clinical decision support | Low | REQUIRE review by the Clinical Governance and Ethics committees. |

## Standard and Lite Modes

- **Standard**: Full procurement lifecycle including multi-disciplinary trials and TCO analysis.
- **Lite**: Rapid assessment for low-cost, low-risk (Class I) replacement items.

## Tool Requirements

- `~~health/artg-lookup` - For AU regulatory verification.
- `~~finance/tco-calculator` - For lifecycle costing.
- `~~legal/contract-templates` - For healthcare-specific terms.
- `~~project tracker` - For workflow tracking.

## Success Indicators

You've applied this skill well when:
- [ ] Regulatory registration (TGA/FDA) is verified and documented.
- [ ] Total Cost of Ownership includes all hidden costs (maintenance, consumables).
- [ ] Infrastructure and IT compatibility is confirmed.
- [ ] Cybersecurity risk assessment (MDS2) is complete.
- [ ] Clinical and operational stakeholders have endorsed the selection.

## Related Skills

- `~~health/business-case` - For drafting the investment justification.
- `~~legal/contract-review` - For the final analysis of purchase terms.
- `~~health/incident-reporting` - For monitoring device safety post-procurement.
