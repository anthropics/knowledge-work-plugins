---
name: review-payer-contract
description: Analyze and review healthcare payer contracts to identify key financial terms, compliance requirements, and negotiation opportunities.
arguments:
  - name: payer_name
    description: "Name of the payer/insurance company (e.g., 'Blue Cross', 'Medicare', 'Bupa')."
    required: true
  - name: contract_type
    description: "Type of contract (e.g., 'Fee-for-Service', 'Capitation', 'Bundled Payment', 'Value-Based Care')."
    required: true
  - name: effective_date
    description: "Contract effective date in YYYY-MM-DD format."
    required: true
  - name: key_concerns
    description: "Optional: Specific concerns or focus areas for the review (e.g., 'low rates on cardiac services', 'strict prior auth requirements')."
    required: false
---

# Review Payer Contract

Use this command to conduct a structured analysis of a payer contract, identifying critical financial terms, operational requirements, compliance obligations, and negotiation opportunities.

## 1. Validate Input

- Verify `payer_name` is a recognized healthcare payer in your market.
- Confirm `contract_type` matches standard categories (Fee-for-Service, Capitation, Bundled Payment, Value-Based Care, Medicare/Medicaid).
- Ensure `effective_date` is in valid YYYY-MM-DD format.
- If `key_concerns` provided, categorize into: Financial (rates/cost), Operational (workflow/administrative), Compliance (regulatory/risk), or Strategic (network/exclusivity).

## 2. Invoke Skill

Use `~~health/payer-contracts` to:
1. Apply the contract review framework based on contract type.
2. Extract and analyze critical contract dates (effective date, term length, renewal notice deadlines).
3. Identify key operational terms (prior auth requirements, timely filing limits, medical necessity criteria).
4. Assess rate structure against benchmarks.
5. Evaluate risk and compliance obligations.
6. Generate negotiation priorities based on identified concerns.

## 3. Generate Structured Output

Produce:

### CONTRACT ANALYSIS REPORT: {{payer_name}}
- **Contract Type**: {{contract_type}}
- **Effective Date**: {{effective_date}}
- **Reference**: [Generate unique ID: PAYER-YYYY-NNN]
- **Analysis Date**: {{current_timestamp}}
- **Status**: ANALYSIS DRAFT

---

### 1. EXECUTIVE SUMMARY

**Payer Profile**: [Market position, volume potential, strategic importance]

**Overall Risk Assessment**: [High/Medium/Low]

**Key Findings**:
- [Primary financial concern]
- [Primary operational concern]
- [Primary compliance concern]

{{#key_concerns}}
**Specific Concerns Raised**: {{key_concerns}}
{{/key_concerns}}

---

### 2. CONTRACT TERMS ANALYSIS

#### Financial Structure
| Element | Status | Notes |
|---------|--------|-------|
| **Rate Benchmark** | [Percent of Medicare/MBS] | [Above/Below market] |
| **Payment Method** | {{contract_type}} | [Fee schedule details] |
| **Rate Escalator** | [CPI/Fixed/None] | [Annual adjustment mechanism] |
| **Outlier Provisions** | [Yes/No] | [Stop-loss thresholds if applicable] |

#### Critical Dates
| Date Type | Contract Value | Tracking Required |
|-----------|----------------|-------------------|
| **Effective Date** | {{effective_date}} | [Confirm implementation] |
| **Initial Term End** | [Calculate: +1-3 years] | **Critical** |
| **Renewal Notice Deadline** | [Calculate: -60-180 days] | **Critical** |
| **Fee Schedule Updates** | [Annual/As specified] | High |

---

### 3. OPERATIONAL REQUIREMENTS

#### Claims Processing
- **Timely Filing Limit**: [90/180/365 days from service]
- **Clean Claim Definition**: [Specific requirements]
- **Payment Timeframe**: [Prompt pay requirements]
- **Electronic Claims**: [Required format/Companion guides]

#### Prior Authorization Requirements
| Service Category | Pre-Auth Required | Turnaround Time |
|------------------|-------------------|-----------------|
| [Category 1] | [Yes/No] | [Urgent: 24h/Standard: 3-5d] |
| [Category 2] | [Yes/No] | [Urgent: 24h/Standard: 3-5d] |
| [Category 3] | [Yes/No] | [Urgent: 24h/Standard: 3-5d] |

#### Medical Necessity & Documentation
- **Criteria Reference**: [Payer medical necessity standards]
- **Appeals Process**: [First-level/Second-level/External review]
- **Documentation Requirements**: [Specific coding standards]
- **Audit Provisions**: [Rights/timeframes/retention]

---

### 4. COMPLIANCE & RISK ASSESSMENT

#### Regulatory Alignment
| Jurisdiction | Applicable Regulations | Compliance Actions |
|--------------|------------------------|--------------------|
| [AU Federal] | Private Health Insurance Act/Medicare | [Prostheses List/Bulk billing] |
| [AU State] | Activity-Based Funding | [Service agreements] |
| [NZ] | ACC/Health NZ | [Regulated fee schedules] |
| [US] | CMS/No Surprises Act | [Enrollment/Compliance] |

#### Risk Identification
| Risk Category | Risk Level | Description | Mitigation |
|---------------|------------|-------------|------------|
| **Financial** | [High/Med/Low] | [Rate/cost concerns] | [Strategy] |
| **Operational** | [High/Med/Low] | [Administrative burden] | [Strategy] |
| **Compliance** | [High/Med/Low] | [Regulatory exposure] | [Strategy] |
| **Strategic** | [High/Med/Low] | [Network/termination risks] | [Strategy] |

---

### 5. NEGOTIATION PRIORITIES

#### High Priority (Must Address)
1. [Critical financial or operational issue]
2. [Compliance concern requiring clarification]
3. [Risk mitigation requirement]

#### Medium Priority (Negotiate if Possible)
1. [Rate improvement opportunity]
2. [Operational efficiency gain]
3. [Term clarification needed]

#### Low Priority (Nice to Have)
1. [Minor rate adjustments]
2. [Process improvements]
3. [Documentation clarifications]

#### Negotiation Leverage
- **Market Position**: [Payer market share/Volume potential]
- **Network Impact**: [Adequacy implications]
- **Must-Have Services**: [Unique services provided]
- **Precedent**: [Existing contracts with this payer]

---

### 6. CONTRACT INTAKE WORKFLOW

#### Immediate Actions (This Week)
1. [ ] **Document Receipt**: Confirm all contract documents received
2. [ ] **Stakeholder Notification**: Alert Finance, Legal, Revenue Cycle teams
3. [ ] **Contract Database Entry**: Input key terms and dates into contract management system
4. [ ] **Calendar Reminders**: Set up renewal notice and critical date alerts

#### Short-Term Actions (Next 2 Weeks)
1. [ ] **Rate Analysis**: Complete detailed benchmark comparison for top services
2. [ ] **Revenue Impact Model**: Calculate financial impact based on historical utilization
3. [ ] **Operational Review**: Assess prior auth and documentation requirements with clinical teams
4. [ ] **Risk Assessment**: Complete compliance and legal review checklist

#### Medium-Term Actions (30-60 Days)
1. [ ] **Negotiation Preparation**: Develop position paper with must-haves and walk-away points
2. [ ] **Internal Approval**: Secure executive sign-off on negotiation strategy
3. [ ] **Counter-Proposal Draft**: Prepare formal response with requested modifications
4. [ ] **Stakeholder Alignment**: Brief affected departments on contract terms

---

### 7. DECISION MATRIX

| Scenario | Recommendation | Action |
|----------|----------------|--------|
| Rates acceptable, terms standard | **Proceed** | Execute after minor clarifications |
| Rates below benchmark but negotiable | **Negotiate** | Prepare counter-proposal with rate increases |
| Operational terms burdensome | **Negotiate** | Request prior auth simplification |
| Significant compliance risk | **Escalate** | Legal/Compliance review required |
| Below cost for major services | **Escalate** | CFO review; prepare walk-away position |
| Exclusive network requirements | **Escalate** | General Counsel/antitrust review |

---

### 8. APPROVAL CHECKLIST

Before contract execution:
- [ ] Rate analysis completed and reviewed by Finance
- [ ] Legal review completed (if required)
- [ ] Operational terms confirmed with affected departments
- [ ] Revenue impact modeled and approved
- [ ] Compliance obligations assigned to owners
- [ ] Renewal dates entered into tracking system
- [ ] Executive approval obtained
- [ ] Counter-proposal prepared (if applicable)

---

## 4. Execute Routing

- Save analysis report to `~~cloud storage` in Payer Contracts folder.
- Create contract tracker entry in `~~project tracker` with all critical dates.
- Update `~~finance/contract-database` with payer information and renewal timeline.
- Notify relevant stakeholders:
  - **Chief Financial Officer**: For material financial terms
  - **Director of Revenue Cycle**: For operational requirements
  - **Legal/Compliance**: For risk escalations
  - **Clinical Leadership**: For prior auth and documentation requirements
- Schedule renewal notice reminders (60-180 days before expiration).

## 5. Output Guardrails

- **Confidentiality**: Mark output as **Commercial-in-Confidence**. Do not share outside authorized personnel.
- **No Legal Advice**: This analysis supports decision-making but does not replace legal counsel. Flag items requiring legal review.
- **Financial Estimates**: All rate comparisons and revenue impacts are estimates. Validate with actual cost data before negotiation.
- **Regulatory Accuracy**: Verify all regulatory requirements against current legislation in your jurisdiction.
- **No PHI**: Ensure no patient-identifiable information is included in analysis or documentation.
- **Confidence Indicators**:
  - **High**: Standard commercial terms with acceptable rates
  - **Medium**: Government/regulated terms; verify compliance obligations
  - **Low**: Complex value-based arrangements or below-cost rates; escalate immediately

---

**Note**: This contract analysis provides a structured framework for payer contract review. All findings should be validated by qualified finance, legal, and revenue cycle professionals before making contract decisions or entering negotiations.
