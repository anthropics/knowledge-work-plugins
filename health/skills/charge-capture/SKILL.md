---
name: health/charge-capture
description: This skill should be used when reviewing charge capture processes, validating the Charge Description Master (CDM), reconciling services provided to charges billed, or identifying compliance risks in healthcare revenue capture. Use for CDM maintenance, charge audits, and revenue integrity reviews.
version: 1.0.0
---

# Charge Capture Review

A specialized framework for reviewing healthcare charge capture processes and the Charge Description Master (CDM), supporting revenue cycle and compliance teams in ensuring accurate, complete, and compliant billing. This skill addresses the intersection of clinical documentation, coding standards, and revenue integrity.

**Important**: This skill assists with charge capture workflows but does not provide clinical coding certification or definitive billing guidance. All coding and billing decisions must be validated by certified coding professionals and compliance officers.

## When to Use This Skill

Invoke this skill when:
- Conducting periodic CDM reviews and maintenance.
- Validating that services provided are accurately captured and billed.
- Identifying missing charges or compliance risks in charge capture workflows.
- Reconciling clinical documentation to charges billed.
- Auditing charge accuracy against medical records.
- Reviewing new service implementations for charge capture setup.
- Investigating revenue leakage or charge capture gaps.
- Preparing for payer audits or compliance reviews.
- Training clinical staff on proper charge capture procedures.
- Validating modifier usage and medical necessity linkage.
- Reviewing charge master pricing against cost and market benchmarks.
- Addressing charge lag or delays in charge posting.
- Reconciling pharmacy, supply, and implant charges.

## Regulatory Context

### Australia & New Zealand (Default)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **Medicare Benefits Schedule** (AU) | Billing compliance | Accurate item numbers; correct claiming; bulk billing requirements |
| **Private Health Insurance Act** (AU) | Prostheses List | Correct prosthesis billing; benefit limitation periods |
| **DVA Fee Schedule** (AU) | Veterans billing | White/Gold card distinctions; approved provider requirements |
| **ACC Schedule** (NZ) | Injury billing | Correct classification codes; prior approval requirements |
| **Health and Disability Services** (NZ) | Funding compliance | National Pricing Framework; compliance with service specifications |
| **State Funding Agreements** | Activity-based funding | Correct DRG/AR-DRG assignment; ICD-10-AM/ACHI coding |

### US/EU-lite Fallback

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **CMS Conditions of Participation** (US) | Medicare compliance | Accurate charge description; timely billing; overpayment reporting |
| **False Claims Act** (US) | Fraud prevention | Knowing submission of false claims; whistleblower provisions |
| **Stark Law** (US) | Physician relationships | Prohibition on self-referrals; fair market value requirements |
| **Anti-Kickback Statute** (US) | Fraud prevention | Prohibition on remuneration for referrals |
| **Chargemaster Guidelines** (US) | Pricing transparency | Hospital price transparency rule; good faith estimates |
| **GDPR** (EU) | Data protection | PHI handling in billing processes |

### Jurisdiction Matrix

| Jurisdiction | Applicable Regulator | Reporting Trigger | Timeframe | Required Artifacts | Escalation Point |
|--------------|---------------------|-------------------|-----------|-------------------|------------------|
| **AU - Federal** | Services Australia | Overpayment identification | 90 days refund | Adjustment claims; refund documentation | Revenue Cycle Director |
| **AU - State** | State Health Dept | Funding variance >threshold | Monthly reporting | Activity data; variance explanations | Finance Manager |
| **NZ - National** | ACC/Te Whatu Ora | Coding error affecting funding | As specified | Corrected claims; root cause analysis | Health Information Manager |
| **US - Federal** | CMS/OIG | Self-disclosure of errors | 60 days (60-day rule) | Self-disclosure protocol (SDP) | Compliance Officer |
| **US - State** | State Medicaid | Billing error notification | Varies by state | Corrected claims; overpayment refunds | VP Revenue Cycle |

## Quick Reference

1. **Documentation First**: Charges require supporting clinical documentation.
2. **Code Accuracy**: Verify correct item codes/HCPCS/CPT codes are used.
3. **Modifier Validity**: Ensure modifiers are appropriate and supported.
4. **Medical Necessity**: Link charges to documented medical necessity.
5. **CDM Maintenance**: Review and update CDM at least annually.
6. **Charge Lag**: Minimize time between service and charge posting.
7. **Reconciliation**: Match clinical volumes to charges regularly.
8. **Compliance Screens**: Automated checks for high-risk scenarios.
9. **Staff Training**: Clinical staff must understand charge capture requirements.
10. **Audit Trail**: Maintain documentation supporting all charges.

## Operating Modes

### Standard Mode
Comprehensive charge capture review including CDM validation, clinical documentation audit, coding accuracy verification, compliance risk assessment, and process improvement recommendations. Use for annual reviews, pre-audit preparation, or significant revenue integrity concerns.

### Lite Mode
Focused review of high-risk charge capture areas or specific compliance concerns. Targets known problem areas, recent service changes, or specific payer requirements. Maintains core compliance checks while reducing scope.

## Detailed Guidance

### 1. Charge Description Master (CDM) Review

The CDM is the central repository of all billable services, supplies, and procedures. Accurate CDM maintenance is foundational to revenue integrity.

#### CDM Structure Elements

**Charge Code**:
- Unique identifier for each billable item
- Consistent formatting and logic
- No duplication or overlap

**Description**:
- Clear, accurate description of service/supply
- Patient-friendly language for price transparency (US requirement)
- Aligned with standard nomenclature (HCPCS, CPT, custom)

**Revenue Code** (US primarily):
- Correct UB-04 revenue code assignment
- Aligns with cost center mapping
- Supports proper cost reporting

**Pricing**:
- Standard charge amount
- Cost-to-charge ratio consideration
- Market benchmark alignment

**General Ledger Account**:
- Maps charges to appropriate GL accounts
- Supports accurate financial reporting
- Enables revenue analysis by service line

#### CDM Review Process

**Annual Comprehensive Review**:
1. **Inventory**: Export full CDM and categorize by service type.
2. **Code Validation**: Verify all procedure codes are current and valid.
3. **Pricing Analysis**: Compare prices to cost, benchmarks, and contracts.
4. **Duplicate Check**: Identify and eliminate duplicate or overlapping codes.
5. **Compliance Check**: Review for unbundling, upcoding, or other risks.
6. **Documentation**: Update CDM policies and review logs.

**Ongoing Maintenance**:
- Review new codes before implementation.
- Validate pricing for new services.
- Deactivate obsolete codes promptly.
- Update for annual coding changes (CPT, HCPCS updates).

### 2. Charge Capture Validation

#### Documentation-to-Charge Reconciliation

**Daily Reconciliation**:
- Compare clinical census/acuity to charges posted.
- Identify patients with services but no charges.
- Review high-value items for accuracy (OR, implants, procedures).

**Weekly Reconciliation**:
- Department-level charge volume vs. productivity metrics.
- Pharmacy dispensing to medication administration charges.
- Supply usage to supply charges.

**Monthly Reconciliation**:
- Financial volume to statistical volume (cases, visits, days).
- Missing charge reports by department.
- Charge lag analysis (time from service to charge posting).

#### Clinical Documentation Requirements

**Required Elements for Charge Capture**:
- Date and time of service
- Rendering provider identification
- Service description (procedure note, operative report)
- Medical necessity justification
- Supporting diagnoses

**Common Documentation Gaps**:
- Missing provider signatures
- Incomplete procedure descriptions
- Absent medical necessity statements
- Unclear start/stop times for time-based services

### 3. Coding Validation

#### Procedure Coding (CPT/HCPCS/Item Numbers)

**Code Selection Validation**:
- Code matches documented service exactly.
- No code splitting or unbundling.
- Correct code for site/location (facility vs. professional).

**Modifier Usage**:
- Modifier -25 (significant, separately identifiable E/M)
- Modifier -59 (distinct procedural service)
- Modifier -50 (bilateral procedure)
- Anesthesia modifiers (AA, QK, QX, etc.)

**Modifier Validation Checklist**:
- [ ] Modifier is appropriate for code pair.
- [ ] Documentation supports modifier use.
- [ ] No modifier overuse patterns.
- [ ] Payer-specific modifier requirements met.

#### Diagnosis Coding (ICD-10)

**Medical Necessity Linkage**:
- Primary diagnosis justifies primary procedure.
- Comorbidities documented for complexity/complications.
- Signs and symptoms coded when definitive diagnosis pending.

**Coding Specificity**:
- Laterality documented and coded.
- Severity/complexity captured.
- External cause codes when applicable.

### 4. High-Risk Charge Capture Areas

#### Pharmacy Charges

**Common Issues**:
- Missing waste documentation (single-use vials).
- Incorrect units (mg vs. mL).
- Modifier -JW (drug waste) not applied.
- Compound medication billing errors.

**Validation Steps**:
- Verify MAR to pharmacy charges.
- Review high-cost drug administration.
- Check waste documentation compliance.

#### Implantable Devices

**Common Issues**:
- Device not documented as implanted.
- Incorrect device code selected.
- Pass-through device billing errors.
- Patient-owned device confusion.

**Validation Steps**:
- Match implant logs to charges.
- Verify operative report documentation.
- Check device identification stickers/reports.

#### Surgical Procedures

**Common Issues**:
- Procedure code doesn't match operative report.
- Incorrect site or laterality.
- Missing assistant surgeon documentation.
- Unbundled component codes.

**Validation Steps**:
- Code from operative report, not schedule.
- Verify correct CPT code selection.
- Check for NCCI edits before billing.

#### Evaluation & Management (E/M) Services

**Common Issues**:
- Level not supported by documentation.
- Modifier -25 overuse.
- Split/shared billing errors.
- Incident-to billing violations.

**Validation Steps**:
- Apply 2021/2023 E/M guidelines correctly.
- Verify medical decision-making or time-based coding.
- Check for duplicate E/M on same day.

### 5. Compliance Risk Assessment

#### Overpayment Risk Areas

**Upcoding**:
- Billing higher-level service than documented.
- Documentation doesn't support code selected.
- Pattern analysis for outlier coding profiles.

**Unbundling**:
- Billing component codes separately when comprehensive code exists.
- Breaking up procedures into multiple charges.
- NCCI edit violations.

**Insufficient Documentation**:
- Missing or illegible signatures.
- Incomplete procedure descriptions.
- Absent medical necessity statements.

#### Underpayment Risk Areas

**Downcoding**:
- Conservative coding results in lower reimbursement.
- Fear of audit leads to systematic under-coding.

**Missing Charges**:
- Services provided but not charged.
- Charge capture process failures.
- System interface errors.

**Modifier Underuse**:
- Legitimate modifiers not applied.
- Reduced reimbursement due to missing modifiers.

### 6. Charge Audit Process

#### Pre-Bill Audit (Front-End)

**Automated Edits**:
- Code validity checks.
- CCI/NCCI edit verification.
- Medical necessity screens (LCD/NCD).
- Duplicate charge detection.
- Age/sex edits.

**Manual Review Triggers**:
- High-dollar charges (>$ threshold).
- Complex surgical cases.
- Modifier usage requiring validation.
- New provider charges.

#### Post-Bill Audit (Back-End)

**Sample Selection**:
- Random sampling for general review.
- Targeted sampling for high-risk areas.
- Focused review for compliance concerns.

**Audit Documentation**:
- Medical record reviewed.
- Codes billed vs. codes supported.
- Discrepancies identified.
- Corrective actions taken.
- Education provided.

#### Audit Findings Response

**Error Rate Calculation**:
- Dollar value of errors / Total dollars audited.
- Track error rates by department, coder, provider.
- Trend over time.

**Corrective Actions**:
- Immediate claim corrections.
- Refund of overpayments.
- Provider/clinical staff education.
- Process improvements.
- System fixes.

## Documentation Requirements

### CDM Review Documentation
- [ ] CDM review schedule and policy
- [ ] Annual CDM review report
- [ ] New code implementation logs
- [ ] Pricing analysis and justification
- [ ] Deleted code archive

### Charge Capture Audit File
- [ ] Audit plan and sampling methodology
- [ ] Audit tool/checklist used
- [ ] Medical records reviewed
- [ ] Findings report with error rates
- [ ] Corrective action plan
- [ ] Education records
- [ ] Follow-up audit results

### Compliance Documentation
- [ ] Charge capture policies and procedures
- [ ] Staff training records
- [ ] Audit results and trend reports
- [ ] Overpayment tracking and refunds
- [ ] Self-disclosure documentation (if applicable)

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **Charging from schedules rather than documentation** | Schedule may not reflect actual service performed | Always code from clinical documentation (operative reports, procedure notes) |
| **Missing time documentation** | Time-based codes require explicit time documentation | Ensure start/stop times documented for all time-based services |
| **Modifier overuse** | Pattern of inappropriate modifiers is compliance risk | Apply modifiers only when documentation clearly supports |
| **Incomplete procedure descriptions** | Insufficient detail to support code selection | Require detailed descriptions matching code nomenclature |
| **Not verifying implant documentation** | Implants must be documented as implanted in patient | Match implant logs to operative reports before charging |
| **Ignoring charge lag** | Delayed charges affect cash flow and timely filing | Monitor and minimize days from service to charge posting |
| **Failing to validate medical necessity** | Payers deny claims without documented necessity | Ensure diagnoses justify procedures in documentation |
| **Skipping NCCI edit checks** | Unbundling violations trigger audit scrutiny | Verify all code pairs against NCCI edits before billing |
| **Not updating CDM annually** | Outdated codes cause claim rejections | Conduct comprehensive annual CDM review |
| **Inadequate clinical staff training** | Staff don't understand charge capture requirements | Provide regular training on documentation and charge requirements |

## When to Escalate

Escalate to Revenue Cycle Director, Compliance Officer, or Chief Financial Officer when:
- Audit reveals systematic upcoding or unbundling patterns.
- Error rate exceeds organizational threshold (typically >5%).
- Potential overpayment exceeds materiality threshold (e.g., $10,000+).
- False Claims Act or fraud concerns identified.
- Charge capture process failures causing significant revenue leakage.
- Payer audit findings with extrapolation demands.
- Self-disclosure to government payers required.
- Clinical staff non-compliance with documentation requirements.
- System interface errors causing widespread charge failures.
- New service implementation lacks charge capture workflow.

## Privacy Considerations

- **PHI Involved**: Yes - charge audits require access to medical records with patient identifiers.
- **Minimum Necessary**: Auditors should only access records necessary for charge validation.
- **Access Controls**: Limit charge audit system access to revenue integrity staff.
- **Audit Trail**: Maintain logs of who accessed which records and when.
- **Retention**: Retain audit documentation per compliance requirements (typically 6-10 years).
- **No Persistence**: Do not store PHI in audit working papers longer than necessary.
- **De-identification**: Use de-identified data for aggregate reporting and trend analysis.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Standard charge capture with clear documentation | High | Proceed with routine billing |
| Complex procedure with detailed operative report | High | Code from documentation with confidence |
| Missing documentation for charged service | Low | **BLOCKER**: Hold charge pending documentation completion |
| Modifier usage unclear from documentation | Medium | Query provider for clarification |
| Pattern of coding errors identified in audit | Low | Escalate to compliance; halt similar billing pending review |
| High-cost implant without clear documentation | Low | Verify with surgical team before billing |
| Potential unbundling identified | Medium | Review against NCCI edits; consult coding guidelines |
| Charge lag exceeding timely filing limits | Low | **BLOCKER**: Escalate to revenue cycle leadership; assess ability to bill |
| Self-disclosure threshold potentially met | Low | Escalate to compliance officer and legal counsel immediately |

## Tool Requirements

- `~~health/clinical-systems` - For accessing medical records and clinical documentation
- `~~health/clinical-coding` - For coding validation and guidance
- `~~finance/reconciliation` - For charge-to-payment reconciliation
- `~~cloud storage` - For audit documentation and CDM files
- `~~project tracker` - For audit plans and corrective action tracking
- `~~data analysis` - For charge lag analysis and trend reporting

## Success Indicators

You've applied this skill well when:
- [ ] CDM is current with annual review completed
- [ ] Charge lag is minimized (target: <3 days from service)
- [ ] Documentation supports all charges billed
- [ ] Error rates remain below organizational threshold
- [ ] Compliance risks identified and remediated promptly
- [ ] Clinical staff trained on charge capture requirements
- [ ] Overpayments identified and refunded timely
- [ ] Revenue leakage minimized through process improvements
- [ ] Audit findings trend positive over time
- [ ] Payer audits result in minimal findings

## Related Skills

- `~~health/clinical-coding` - For detailed coding guidance and validation
- `~~health/payer-contracts` - For understanding reimbursement methodologies
- `~~health/complaints-management` - For handling billing disputes
- `~~finance/reconciliation` - For payment reconciliation and denial analysis
- `~~finance/audit-support` - For external audit preparation

---

**Note**: Charge capture and revenue integrity are complex domains requiring specialized expertise. This skill provides a structured approach but should be used in conjunction with certified coding professionals, compliance officers, and revenue cycle leadership.
