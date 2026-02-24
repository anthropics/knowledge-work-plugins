---
name: health/payer-contracts
description: This skill should be used when reviewing, analyzing, or negotiating healthcare payer contracts including private health insurance agreements, Medicare/DVA schedules, and managed care contracts. Use for rate analysis, term identification, renewal tracking, and compliance verification.
version: 1.0.0
---

# Payer Contract Review

A specialized framework for reviewing healthcare payer contracts, supporting finance and contracting teams in analyzing insurance agreements, government schedules, and managed care arrangements. This skill addresses healthcare-specific financial terms, regulatory requirements, and revenue cycle implications.

**Important**: This skill assists with contract analysis workflows but does not provide legal advice or definitive financial guidance. All contract reviews must be validated by qualified legal counsel and finance professionals before execution.

## When to Use This Skill

Invoke this skill when:
- Reviewing proposed payer contracts or contract amendments.
- Analyzing fee schedules and reimbursement rates against benchmarks.
- Preparing for contract renewals or renegotiations.
- Evaluating value-based care or risk-sharing arrangements.
- Assessing contract terms for medical necessity and prior authorization requirements.
- Reviewing timely filing limitations and claims submission requirements.
- Identifying compliance obligations for government payer contracts.
- Tracking contract expiration dates and renewal notice periods.
- Comparing multiple payer contracts for standardization opportunities.
- Responding to payer contract termination or non-renewal notices.
- Analyzing out-of-network provisions and balance billing restrictions.
- Evaluating capitation, bundled payment, or other alternative payment models.

## Regulatory Context

### Australia & New Zealand (Default)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **Private Health Insurance Act** (AU) | PHI contracts | Prostheses List pricing; benefit limitation periods; waiting periods |
| **National Health Act** (AU) | Medicare benefits | Schedule fees; bulk billing; patient gap payments |
| **DVA Schedule** (AU) | Veterans care | Department of Veterans' Affairs fee schedule requirements |
| **Accident Compensation Act** (NZ) | ACC contracts | No-fault scheme; regulated fee schedules; provider enrollment |
| **Health and Disability Services** (NZ) | Service contracts | Ministry of Health funding agreements; outcome requirements |
| **State Funding Arrangements** | State-specific | Activity-based funding (ABF); block grants; service agreements |

### US/EU-lite Fallback

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **CMS Conditions of Participation** (US) | Medicare/Medicaid | Enrollment requirements; compliance obligations; payment rules |
| **No Surprises Act** (US) | Balance billing | Out-of-network emergency and air ambulance protections |
| **Affordable Care Act** (US) | Market reforms | Medical loss ratio; essential health benefits; network adequacy |
| **State Prompt Pay Laws** (US) | Payment timing | Maximum days to pay clean claims; interest penalties |
| **GDPR** (EU) | Data protection | Patient data handling in claims processing |

### Jurisdiction Matrix

| Jurisdiction | Applicable Regulator | Reporting Trigger | Timeframe | Required Artifacts | Escalation Point |
|--------------|---------------------|-------------------|-----------|-------------------|------------------|
| **AU - Federal** | DoHAC (PHI/Medicare) | Contract execution | 30 days notification | Signed agreement; fee schedule; compliance attestation | Chief Financial Officer |
| **AU - State** | State Health Dept | Service agreement renewal | Annual cycle | Performance report; activity data; budget reconciliation | Director of Revenue Cycle |
| **NZ - National** | Health NZ/Te Whatu Ora | Service level agreement | As specified | Contract variation requests; performance metrics | Finance Manager |
| **US - Federal** | CMS | Medicare enrollment changes | 30-60 days | CMS-855 forms; compliance documentation | Compliance Officer |
| **US - State** | State Medicaid Agency | Medicaid contract renewal | Annual/biennial | Encounter data; quality metrics; financial reports | VP Payer Relations |

## Quick Reference

1. **Rate Analysis**: Compare proposed rates to fee schedule benchmarks and cost data.
2. **Term Length**: Note initial term, renewal periods, and termination provisions.
3. **Notice Periods**: Track renewal notice deadlines (typically 60-180 days).
4. **Claims Timeliness**: Identify timely filing limits (often 90-365 days).
5. **Prior Auth**: Document services requiring prior authorization and turnaround times.
6. **Medical Necessity**: Understand payer's medical necessity criteria and appeal rights.
7. **Reimbursement Method**: Clarify fee-for-service, capitation, or bundled payment.
8. **Value-Based Terms**: Identify quality metrics, risk-sharing, and bonus/penalty structures.
9. **Single Case Agreements**: Know when out-of-network single case rates apply.
10. **Audit Rights**: Understand payer audit provisions and documentation requirements.

## Operating Modes

### Standard Mode
Comprehensive contract review including full rate analysis, regulatory compliance check, risk assessment, and negotiation strategy development. Use for major contracts, new payer relationships, or significant renewals.

### Lite Mode
Streamlined review focusing on critical terms (rates, key dates, major compliance obligations) for contract extensions or low-value agreements. Maintains identification of high-risk provisions requiring escalation.

## Detailed Guidance

### 1. Contract Review Framework

#### Phase 1: Initial Assessment
- **Contract Type**: Identify if HMO, PPO, EPO, POS, or government program.
- **Payer Profile**: Research payer's market position, reputation, and financial stability.
- **Strategic Importance**: Assess volume potential and network adequacy impact.
- **Precedent Review**: Check existing contracts with same payer at other sites.

#### Phase 2: Financial Terms Analysis

**Fee Schedule Review**:
- Compare rates to current Medicare/MBS schedule (percent of benchmark).
- Calculate conversion factors and fee schedule updates (CPI, market baskets).
- Identify services with particularly favorable or unfavorable rates.
- Assess outlier and stop-loss provisions for high-cost cases.

**Payment Methodology**:
- **Fee-for-Service**: Specific fee schedule or percentage of charges.
- **Capitation**: Per member per month (PMPM) rates; risk adjustment; withholds.
- **Bundled Payments**: Episode definitions; quality gates; gainsharing.
- **Value-Based**: Quality metrics; shared savings/losses; risk tiers.

**Cost Considerations**:
- Calculate cost-to-charge ratios for key services.
- Factor in administrative burden (prior auth, documentation requirements).
- Assess technology and infrastructure requirements.
- Consider bad debt and denial risk under proposed terms.

#### Phase 3: Operational Terms Review

**Claims Processing**:
- **Timely Filing**: Submission deadlines (typically 90-180 days from service).
- **Clean Claim Definition**: Requirements for first-pass payment.
- **Payment Timeframes**: Prompt pay requirements; interest on late payments.
- **Electronic Claims**: Required formats (837I/P); companion guides.
- **Claim Corrections**: Process for resubmissions and corrected claims.

**Prior Authorization Requirements**:
- List of services requiring pre-authorization.
- Turnaround time commitments (urgent vs. standard).
- Retrospective authorization provisions (emergencies).
- Peer-to-peer review process for denials.
- Appeals process and timeframes.

**Medical Necessity & Clinical Policies**:
- Reference to payer's medical necessity criteria.
- Utilization management and case management requirements.
- Clinical pathways or care management programs.
- Experimental/investigational treatment exclusions.

**Documentation Requirements**:
- Specific coding and documentation standards.
- Supporting documentation for claims.
- Audit and medical record review provisions.

#### Phase 4: Network & Access Requirements

**Network Participation**:
- Exclusive vs. non-exclusive participation.
- Network adequacy and access standards.
- Continuity of care provisions for terminations.
- Tiered network implications (if applicable).

**Out-of-Network Provisions**:
- Emergency service protections (No Surprises Act in US).
- Balance billing restrictions and patient protections.
- Single case agreement (SCA) procedures.
- Out-of-network reimbursement rates.

#### Phase 5: Risk & Compliance Terms

**Audit & Compliance**:
- Payer audit rights and notification requirements.
- Documentation retention periods (typically 6-10 years).
- Overpayment recovery provisions.
- Fraud and abuse compliance requirements.
- OIG/Sanctions screening obligations.

**Insurance & Indemnification**:
- Professional liability insurance requirements.
- Indemnification provisions.
- Cyber liability for data breaches.

**Termination Provisions**:
- Termination for convenience vs. cause.
- Notice periods (typically 90-180 days).
- Immediate termination triggers.
- Post-termination claims processing (run-out periods).
- Patient notification requirements.

### 2. Rate Analysis Methodology

#### Benchmark Comparison

**Primary Benchmarks**:
- **Australia**: Medicare Benefits Schedule (MBS) rates; Private Health Insurance Prostheses List.
- **New Zealand**: ACC regulated fee schedules; DHB/DHNZ service specifications.
- **United States**: Medicare Physician Fee Schedule (MPFS); Medicare Severity DRGs.

**Analysis Steps**:
1. Extract proposed rates for top 50-100 services by volume/revenue.
2. Compare to benchmark at item code level.
3. Calculate weighted average as percent of benchmark.
4. Identify services below cost or significantly below market.
5. Model revenue impact based on historical utilization.

#### Cost Analysis

**Cost-to-Charge Ratio Method**:
- Obtain hospital-specific cost-to-charge ratios by cost center.
- Apply to proposed rates to estimate margin.
- Identify services where proposed rate < cost.

**Activity-Based Costing** (if available):
- Time-driven activity-based costing (TDABC) for services.
- Compare to proposed reimbursement.
- Assess contribution margin by service line.

### 3. Key Contract Dates & Tracking

#### Critical Dates to Extract

| Date Type | Typical Range | Tracking Priority |
|-----------|---------------|-------------------|
| **Effective Date** | Contract start | Critical |
| **Initial Term End** | 1-3 years | Critical |
| **Renewal Notice Deadline** | 60-180 days before expiration | Critical |
| **Fee Schedule Updates** | Annual | High |
| **Quality Reporting Deadlines** | Quarterly/Annual | High |
| **Audit Rights Expiration** | Post-termination | Medium |

#### Renewal Management

**180 Days Before Expiration**:
- Initiate renewal discussions with payer.
- Prepare utilization and financial performance summary.
- Identify terms requiring modification.

**120 Days Before**:
- Submit formal renewal notice if required.
- Escalate if renewal terms not received.

**90 Days Before**:
- Finalize negotiation positions.
- Legal review of renewal documents.

**60 Days Before**:
- Execute renewal or implement termination plans.
- Communicate to affected departments.

### 4. Negotiation Strategy

#### Preparation

**Internal Alignment**:
- Confirm strategic priority of payer relationship.
- Identify must-have vs. nice-to-have terms.
- Establish walk-away position on rates.
- Secure executive sponsorship for negotiation.

**Leverage Assessment**:
- Market share of payer in service area.
- Competitor contracts with same payer.
- Must-have services provided by organization.
- Network adequacy implications for payer.

#### Common Negotiation Points

**Rates**:
- Request increases on services below benchmark.
- Negotiate annual rate escalators (CPI or higher).
- Secure stop-loss protections for high-cost cases.

**Operational Terms**:
- Reduce prior authorization burden.
- Improve timely filing windows.
- Secure prompt pay commitments with penalties.

**Risk Sharing**:
- Limit downside exposure in value-based arrangements.
- Ensure adequate risk adjustment.
- Clarify quality measure specifications.

## Documentation Requirements

### Contract Review File
- [ ] Contract summary with key terms
- [ ] Rate analysis spreadsheet with benchmark comparisons
- [ ] Risk assessment and compliance checklist
- [ ] Negotiation position document
- [ ] Internal approval documentation
- [ ] Signed contract with all amendments

### Ongoing Contract Management
- [ ] Contract database entry with key dates
- [ ] Fee schedule loaded into billing system
- [ ] Prior authorization requirements communicated to clinical staff
- [ ] Renewal tracking with calendar reminders
- [ ] Performance metrics dashboard (if value-based)

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **Accepting standard rates without analysis** | May result in significant underpayment | Always benchmark proposed rates against Medicare/MBS and cost data |
| **Missing renewal notice deadlines** | Automatic renewal or termination can occur without input | Track critical dates with 180-day advance reminders |
| **Not modeling revenue impact** | Unclear financial impact leads to poor decisions | Model revenue effect based on historical utilization |
| **Overlooking prior auth requirements** | Clinical staff unaware of requirements leading to denials | Document all prior auth requirements and educate staff |
| **Ignoring timely filing limits** | Lost revenue from late claim submissions | Set up claim submission workflows within contract timeframes |
| **Not understanding value-based terms** | Unexpected penalties or missed bonuses | Ensure clear understanding of quality metrics and risk arrangements |
| **Accepting broad audit rights** | Excessive administrative burden and overpayment risk | Negotiate reasonable audit limitations and timeframes |
| **Missing termination provisions** | Stuck in unfavorable contract without exit option | Understand all termination rights and notice periods |
| **Not checking for auto-renewal** | Unintended extension of unfavorable terms | Identify auto-renewal clauses and manage opt-out windows |
| **Failing to track amendments** | Operating under outdated terms | Maintain complete contract file with all amendments and rate updates |

## When to Escalate

Escalate to Chief Financial Officer, General Counsel, or Executive Team when:
- Proposed rates are below cost for significant service volume.
- Payer demands exclusive network participation.
- Contract includes unlimited audit rights or penalties.
- Value-based arrangement includes substantial downside risk (>10% revenue at risk).
- Termination provisions are unilateral or immediate without cause.
- Payer requires technology investments without compensation.
- Government payer contract includes compliance concerns or fraud risk.
- Contract conflicts with existing obligations or other payer agreements.
- Payer is in financial distress or has significant market complaints.
- Rate dispute involves material revenue impact (>5% of total revenue).

## Privacy Considerations

- **PHI Involved**: Yes - contracts may reference specific patient populations or utilization patterns.
- **Data Minimization**: Only share aggregate utilization data during negotiations, not individual patient information.
- **Breach Notification**: Understand contract provisions for data breach notification and liability.
- **Business Associate Agreements**: Ensure BAA is in place if payer will access PHI.
- **Data Security**: Verify payer meets organizational data security requirements.
- **Retention**: Maintain contracts and amendments per record retention policy (typically 7+ years post-termination).
- **No Persistence**: Do not store contract drafts with PHI in unsecured locations.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Standard commercial payer contract with standard terms | High | Proceed with standard review checklist |
| Rates within acceptable range of benchmarks | High | Recommend acceptance with minor operational clarifications |
| Government payer contract with regulated terms | Medium | Verify compliance requirements; escalate policy questions |
| Complex value-based arrangement with risk-sharing | Low | Require detailed financial modeling; involve actuarial resources |
| Exclusive network requirements or restrictive covenants | Low | **BLOCKER**: Escalate to General Counsel for antitrust/competition review |
| Proposed rates below cost for major service lines | Low | Escalate to CFO; prepare walk-away position or counter-proposal |
| Ambiguous prior authorization or medical necessity language | Medium | Request clarification; document assumptions |
| Payer in financial distress or market exit rumors | Low | Escalate to executive leadership; assess counterparty risk |

## Tool Requirements

- `~~cloud storage` - For contract documents and rate analysis files
- `~~project tracker` - For renewal tracking and negotiation milestones
- `~~finance/contract-database` - For contract repository and key date management
- `~~health/revenue-cycle` - For claims and reimbursement data integration
- `~~data analysis` - For rate modeling and financial impact analysis
- `~~legal/contract-review` - For general contract analysis and playbook alignment

## Success Indicators

You've applied this skill well when:
- [ ] All proposed rates analyzed against benchmarks and cost data
- [ ] Critical dates extracted and tracked in contract management system
- [ ] Key operational terms documented and communicated to affected departments
- [ ] Risk assessment identifies material issues for escalation
- [ ] Negotiation strategy based on leverage analysis and internal alignment
- [ ] Revenue impact modeled with sensitivity analysis
- [ ] Compliance obligations clearly understood and assigned to owners
- [ ] Prior authorization requirements communicated to clinical staff
- [ ] Renewal timeline established with advance notice reminders
- [ ] Contract file maintained with all amendments and correspondence

## Related Skills

- `~~legal/contract-review` - General contract analysis methodology and playbook alignment
- `~~finance/reconciliation` - For payment reconciliation and underpayment identification
- `~~health/charge-capture` - For CDM alignment with contract rates
- `~~health/clinical-coding` - For coding compliance under payer requirements
- `~~health/complaints-management` - For payer-related dispute resolution

---

**Note**: Payer contracting involves complex financial, legal, and operational considerations. This skill provides a structured approach but should be used in conjunction with qualified legal counsel, finance professionals, and revenue cycle expertise.
