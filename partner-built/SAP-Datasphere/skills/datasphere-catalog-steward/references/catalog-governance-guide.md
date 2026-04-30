# Catalog Governance Reference Guide

## Table of Contents
1. [Metadata Enrichment Templates](#metadata-enrichment-templates)
2. [Glossary Term Template](#glossary-term-template)
3. [KPI Definition Template](#kpi-definition-template)
4. [Tag Taxonomy Design Patterns](#tag-taxonomy-design-patterns)
5. [Impact Analysis Report Template](#impact-analysis-report-template)
6. [Data Quality Scorecard](#data-quality-scorecard)
7. [Catalog Review Schedule Template](#catalog-review-schedule-template)
8. [Governance RACI Matrix](#governance-raci-matrix)
9. [Common Anti-Patterns](#common-anti-patterns)

---

## Metadata Enrichment Templates

### Asset Naming Convention

Use these patterns to create consistent, discoverable asset names.

#### Dimension Table Naming
```
[Domain]_[Entity]_Dim

Examples:
- Customer_Dim (core customer master)
- Product_Dim (product catalog)
- Date_Dim (date dimension for time-series analysis)
- Employee_Dim (employee master)
- Geography_Dim (geographic locations/regions)
```

#### Fact Table Naming
```
[Domain]_[Verb]_Fact

Examples:
- Sales_Order_Fact (individual sales transactions)
- Finance_GL_Posting_Fact (general ledger postings)
- HR_Attendance_Fact (employee attendance records)
- Marketing_Campaign_Response_Fact (campaign responses)
```

#### View Naming
```
[Domain]_[Entity]_View_[Purpose]

Examples:
- Sales_Order_View_Current (current active orders)
- Customer_View_Enriched (customer with demographics)
- Finance_GL_View_Monthly (monthly GL aggregation)
- Product_View_with_Pricing (products with price hierarchy)
```

#### Model Naming
```
[Domain]_[Topic]_Model

Examples:
- Sales_Pipeline_Model
- Customer_Churn_Model
- Finance_Cash_Flow_Model
- HR_Headcount_Model
```

#### Measure Naming
```
[Entity]_[Aggregation]_[Domain]

Examples:
- Order_Count_Sales
- Revenue_Sum_Sales
- Cost_Avg_Finance
- Headcount_Current_HR
```

### Asset Description Template

Use this template for all asset descriptions:

```markdown
## [Asset Name]

### What This Asset Contains
[One-sentence summary describing the primary data contents]

Example: This table contains daily sales order transactions, including order details,
customer information, and order amounts for all regions.

### Business Purpose
[Why this asset exists; what business problems does it solve?]

Example: Enables sales analysis, revenue forecasting, and customer purchasing patterns
analysis for monthly business reviews and quarterly forecasting.

### Key Entities and Measures
- **Dimension [X]:** [Brief description] (Example value: "Customer ID, unique per customer")
- **Dimension [Y]:** [Brief description] (Example value: "Order date, YYYY-MM-DD format")
- **Measure [A]:** [Brief description] (Example value: "Order amount in USD, excluding tax")
- **Measure [B]:** [Brief description] (Example value: "Item quantity ordered")

### Data Refresh
- **Frequency:** [Daily/Weekly/Monthly] at [time, timezone]
- **Latency:** Data typically available within [X hours] of transaction
- **Last Updated:** [Auto-populated timestamp]

### Data Lineage
- **Source:** [List source systems or parent tables]
- **Transformations:** [Summarize key business logic or transformations applied]
- **Consumers:** [List primary consuming models or reports]

### Known Limitations or Caveats
[Document any data quality issues, exclusions, or approximations. This is critical.]

Examples:
- Excludes returns and cancellations; see Sales_Return_Fact for returns
- Historical data available from Jan 2020 forward only
- International orders excluded; see Global_Sales_Order_Fact
- Prices are list prices; do not include negotiated discounts

### Owner and Contact
- **Business Owner:** [Name, Title, Email]
- **Technical Owner:** [Name, Title, Email]
- **Last Review Date:** [YYYY-MM-DD]

### Related Assets
- [Related Dimension: Customer_Dim]
- [Related Fact: Sales_Order_Detail_Fact]
- [Related Model: Sales_Pipeline_Model]

### Certification Status
[Certified / Trusted / Monitor / Issue]
- Quality Score: [XX%]
- Last Quality Review: [YYYY-MM-DD]
```

### Description Writing Guidelines

**DO:**
- Use plain business language (assume audience is analyst, not DBA)
- Include concrete examples (helps readers understand scope)
- Document caveats and limitations (critical for users to know)
- Keep main description under 300 words (link to detailed docs)
- Use consistent tense (present tense, descriptive)
- Be specific (not "customer info" but "customer name, email, phone, address")

**DON'T:**
- Use technical jargon without explanation (no "SCD Type 2 dimension")
- Hide important limitations (users will find out later at cost)
- Write essays (use "see detailed documentation" link instead)
- Assume readers know source system (explain SAP, Salesforce, etc.)
- Change descriptions without notifying users (impacts trust)

### Examples

#### Good Description
```
Sales Order Fact

What This Asset Contains:
This table contains 250M+ daily sales order transactions from 2020-present,
including order header details (order ID, customer, date, amount) and detail
lines (product, quantity, unit price).

Business Purpose:
Enables revenue reporting, sales forecasting, and customer purchasing analysis.
Used in 40+ dashboards and 3 major KPIs (Monthly Revenue, Customer Lifetime Value,
Sales Pipeline).

Key Entities:
- Order ID (unique per order)
- Customer ID (links to Customer_Dim)
- Order Date (YYYY-MM-DD)
- Total Amount (USD, including tax)
- Product ID (links to Product_Dim)

Data Refresh:
- Frequency: Daily at 2 AM UTC
- Latency: Data available within 6 hours of order creation in SAP
- Last Updated: 2024-02-08

Limitations:
- Returns and cancellations excluded (see Sales_Return_Fact)
- International orders before 2023 not available (system migration)
- Negotiated discounts not shown; uses list prices
- Test orders included; filter by Customer ID >= 100000 to exclude

Owner: Sarah Chen, Sales Analytics Manager (s.chen@company.com)
Quality Score: 97% (certified)
```

#### Poor Description
```
Order Table

Contains order data. Updated daily. Links to customer table.
Has order amount and product info. See SQL for details.
```

---

## Glossary Term Template

Use this template for all glossary terms.

### Glossary Term Definition

```markdown
## [Term Name]

### Synonyms
[List alternative names for this concept]
- Alternative name 1
- Alternative name 2
- [Note: "Turnover" is NOT a synonym for US-based companies; document regional differences]

### Plain Language Definition
[Define the business concept in language a business analyst would use.
Assume no technical background. 1-2 sentences.]

Example: "The total income a company receives from selling products and services
to customers during a specific time period, before deducting expenses."

### Technical Definition
[How is this calculated in data systems? Include formula if applicable.]

Example: "Sum of all order amounts (order header TOTAL_AMOUNT field) for orders
with order status = 'Completed' during the reporting period, excluding canceled
and returned orders. Calculated in Sales_Summary model using TOTAL_REVENUE measure."

### Calculation Method
[Detailed step-by-step calculation, including any business logic or exclusions]

Example:
1. Identify all orders in SAP (table ORDERS) with status = 'Completed'
2. Exclude orders with flag CANCELLED_FLAG = 'Y'
3. Exclude order detail lines with return quantities > 0 (see RETURN_QTY column)
4. Sum TOTAL_AMOUNT field across all qualifying order detail lines
5. Convert to reporting currency using daily exchange rates (CURRENCY_CONVERSION table)
6. Apply any negotiated discounts recorded in CUSTOMER_DISCOUNT table

### Dimensions / Slicing
[How is this metric sliced in analysis?]

Typical Dimensions:
- By Customer Segment (Enterprise, Mid-Market, SMB)
- By Product Category (Physical Products, Services, Digital)
- By Geography (North America, Europe, Asia-Pacific)
- By Time Period (Daily, Weekly, Monthly, Year-to-Date)
- By Sales Channel (Direct, Partner, Online)

### Examples
[Provide concrete examples to clarify the definition]

**What Increases Revenue:**
- Customer places new order: Order Amount is added to Revenue
- Volume discount removed: Revenue increases (less discount)
- Price increase applied: Revenue increases for same quantities

**What Decreases Revenue:**
- Order canceled: Order Amount is removed from Revenue
- Product returned: Return amount is deducted from Revenue
- Negotiated discount applied: Revenue decreases

**Edge Cases:**
- Revenue from free trials: Generally excluded (zero price)
- Multi-year contracts: Recognized monthly/quarterly (not all at once)
- Accrued vs. received: Reported on accrual basis (not cash received)

### Related Terms
[Link to related glossary terms]

- **Parent Term:** [Term this is derived from]
- **Related Terms:** [Terms used in conjunction with this one]
- **Complement Terms:** [Terms that measure the inverse or opposite]

Examples:
- Parent: Total Revenue
- Related: Product Revenue, Service Revenue, Recurring Revenue
- Complement: Expenses, Cost of Revenue

### Calculation Logic / Formula
[For metrics, include detailed formula with field references]

Example SQL:
```sql
SELECT
  SUM(o.TOTAL_AMOUNT) as REVENUE
FROM ORDERS o
WHERE o.ORDER_STATUS = 'Completed'
  AND o.CANCELLED_FLAG = 'N'
  AND NOT EXISTS (SELECT 1 FROM ORDER_DETAIL od
                  WHERE od.ORDER_ID = o.ORDER_ID
                  AND od.RETURN_QTY > 0)
```

### Data Sources
[Which systems/tables implement this term?]

- Primary Source: SAP ERP (ORDERS, ORDER_DETAIL tables)
- Transformation: Sales_Summary model in Datasphere
- Calculation: TOTAL_REVENUE measure
- Reporting: All Sales dashboards

### Applicable Business Domains
[Which teams use this term?]

- Sales (daily/weekly tracking)
- Finance (monthly closing, forecasting)
- Executive Leadership (strategic KPIs)
- Marketing (ROI analysis)

### Owner and Approval
- **Business Owner:** [Name, Title]
- **Technical Owner:** [Name, Title]
- **Approved By:** [Name, Title, Governance Committee]
- **Approval Date:** [YYYY-MM-DD]
- **Last Review Date:** [YYYY-MM-DD]
- **Next Review Date:** [YYYY-MM-DD]

### Version History
| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.2 | 2024-02-01 | J. Smith | Added international revenue; updated definition |
| 1.1 | 2023-10-15 | M. Johnson | Clarified discount treatment |
| 1.0 | 2023-06-01 | S. Chen | Initial definition |

### Change Requests
[Link to any pending change requests or disputes about this definition]

- [Change Request #001: Should revenue include multi-year contracts? In review...]
- [Change Request #002: Should we exclude certain customer segments? Pending domain owner review...]

---

## KPI Definition Template

Use this template for all Key Performance Indicators.

```markdown
## [KPI Name]

### KPI Code
[Unique identifier for tracking]
Example: KPI-SALES-001, KPI-FIN-MARGIN-001

### Strategic Objective
[Which business goal does this KPI support?]

Example: "Increase annual recurring revenue (ARR) by 25% in 2024"
Example: "Improve customer retention from 92% to 95% by Q4 2024"

### Business Definition
[Plain-language definition suitable for executives]

Example: "The percentage of customers who renew their subscription with us
at the end of the contract period, measured monthly and tracked as trailing
12-month average."

### Technical Definition / Calculation
[Detailed calculation formula with field references]

Example:
1. Identify all customers with contract renewal dates in reporting month
2. Count customers who renewed contracts (RENEWAL_FLAG = 'Y')
3. Count total eligible customers (all with renewal date in month)
4. Calculate: Churn Rate = (Total - Renewed) / Total * 100%
5. Calculate: Retention = 100% - Churn Rate
6. Apply trailing 12-month moving average

### Formula
```
Retention Rate (%) = (Renewed Customers in Period / Eligible Customers) * 100
Trailing 12-Month Retention = Average of last 12 monthly rates
```

### Detailed Calculation Steps
[Step-by-step walkthrough for implementation]

```
Step 1: Identify eligible customers
- Customer must have active contract during reporting period
- Customer must have reached renewal date
- Exclude test customers (CUSTOMER_ID < 100000)

Step 2: Count renewals
- FROM Contracts c
- JOIN Renewals r ON c.CONTRACT_ID = r.CONTRACT_ID
- WHERE c.RENEWAL_DATE >= start_of_month
-   AND c.RENEWAL_DATE < end_of_month
-   AND r.RENEWAL_FLAG = 'Y'

Step 3: Calculate monthly rate
- Monthly Retention = Count(Renewals) / Count(Eligible) * 100

Step 4: Calculate trailing 12-month average
- T12M Retention = AVG(monthly rates for last 12 months)
```

### Dimensions (Slicing)
[How is this KPI analyzed by different attributes?]

- **Customer Segment:** Enterprise, Mid-Market, SMB
- **Product:** Core Product, Premium Add-on, Professional Services
- **Geography:** North America, EMEA, Asia-Pacific
- **Sales Channel:** Direct Sales, Partner, Self-Serve
- **Cohort:** By contract start date (vintage analysis)

### Data Sources
[Which tables and models provide this KPI?]

- **Source Table 1:** CONTRACTS (contract details)
- **Source Table 2:** RENEWALS (renewal transactions)
- **Transformation Model:** Customer_Success_Model
- **KPI Measure:** RETENTION_RATE_T12M
- **Dashboard:** Executive Revenue Dashboard, CS Team Dashboard

### Refresh Frequency and Timing
- **Frequency:** Monthly (on the 3rd business day)
- **Latency:** Data available 1 business day after month-end
- **Granularity:** Monthly, trended

### Thresholds and Targets
[What is "good" performance?]

| Threshold | Performance | Action |
|-----------|-------------|--------|
| ≥ 95% | Target Met | Monitor for changes |
| 92-95% | Yellow | Investigate; develop improvement plan |
| 88-92% | Orange | Escalate; assign improvement task force |
| < 88% | Red | Executive escalation; emergency action plan |

Target (2024): 95%

### KPI Owner and Accountability
- **KPI Owner (Accountable):** [Name, Title, Email] - Sets target, reviews monthly
- **Business Owner:** [Name, Title, Email] - Interprets results, defines initiatives
- **Data Owner:** [Name, Title, Email] - Ensures data quality, troubleshoots issues
- **Dashboard Owner:** [Name, Title, Email] - Maintains dashboard infrastructure
- **Escalation Path:** [Name, Title] if KPI misses target

### Related KPIs
[KPIs that work together or have dependencies]

- **Parent KPI:** Annual Recurring Revenue (ARR)
- **Child KPI:** Renewal Rate by Segment
- **Companion KPI:** Churn Rate, Net Revenue Retention
- **Prerequisite:** Customer Acquisition Rate (must have customers to retain)

### Historical Performance
[Track KPI performance over time]

| Period | Value | Trend | Notes |
|--------|-------|-------|-------|
| 2024-02 | 94.2% | ↑ 0.3% | Improvements in onboarding |
| 2024-01 | 93.9% | ↓ 0.2% | Competitor pressure in SMB |
| 2023-12 | 94.1% | ↑ 0.1% | Holiday season stable |

### Known Issues or Caveats
[Data quality issues, approximations, or limitations]

- "Multi-year contracts treated as annual renewal; not ideal for trend analysis"
- "Excludes customers with <6 months tenure (insufficient history)"
- "Data from SAP available with 2-day delay; projections based on partial month"

### Validation Results
[Was this KPI validated against data?]

- **Validation Date:** 2024-01-15
- **Status:** CERTIFIED
- **Data Quality Score:** 98%
- **Issues Found:** None
- **Validated By:** [Name, Data Quality Team]

### KPI Change History
| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.2 | 2024-01-01 | Changed to T12M avg; was monthly snap | CEO, CFO |
| 1.1 | 2023-10-01 | Added customer segment dimension | Sales VP |
| 1.0 | 2023-06-01 | Initial definition | Executive Team |

### Related Documentation
- [Detailed calculation logic](link-to-detailed-doc)
- [Data dictionary for source tables](link-to-data-dictionary)
- [Customer Success Dashboard](link-to-dashboard)
- [CS Team Review Meeting Notes](link-to-meeting-notes)

---
```

---

## Tag Taxonomy Design Patterns

### Pattern 1: Simple Flat Taxonomy (Good for <100 Assets)

```
Domain Tags:
- domain:sales
- domain:finance
- domain:hr
- domain:operations
- domain:marketing
- domain:product

Sensitivity Tags:
- sensitivity:public
- sensitivity:internal
- sensitivity:confidential
- sensitivity:pii
- sensitivity:financial

Cadence Tags:
- cadence:real-time
- cadence:daily
- cadence:weekly
- cadence:monthly
- cadence:quarterly

Quality Tags:
- quality:certified
- quality:trusted
- quality:monitor
- quality:issue

Usage Tags:
- usage:kpi
- usage:reporting
- usage:analysis
- usage:ml-model
- usage:regulatory
```

### Pattern 2: Hierarchical Taxonomy (Good for >500 Assets)

```
domain:finance
  ├── domain:finance:accounting
  ├── domain:finance:revenue
  ├── domain:finance:expense
  └── domain:finance:planning

domain:sales
  ├── domain:sales:pipeline
  ├── domain:sales:forecast
  ├── domain:sales:commission
  └── domain:sales:customer

domain:hr
  ├── domain:hr:payroll
  ├── domain:hr:recruiting
  ├── domain:hr:performance
  └── domain:hr:learning

sensitivity:data-protection
  ├── sensitivity:pii (Personally Identifiable Information)
  ├── sensitivity:financial (Salary, bank accounts)
  ├── sensitivity:health (Medical records)
  └── sensitivity:behavioral (Personal preferences)

cadence:update-frequency
  ├── cadence:real-time (updated <1 minute)
  ├── cadence:daily (updated 1x per day)
  ├── cadence:weekly (updated 1x per week)
  ├── cadence:monthly (updated 1x per month)
  └── cadence:static (not updated)
```

### Pattern 3: Multi-Dimensional Tagging (Best Practice)

Combine multiple tag types on each asset (3-5 tags typical):

```
Asset: Sales_Summary_Model
Tags Applied:
- domain:sales (which business area)
- cadence:daily (update frequency)
- quality:certified (data quality)
- usage:reporting (how it's used)

Asset: Customer_Financial_Data_View
Tags Applied:
- domain:finance (business area)
- sensitivity:pii (sensitive data)
- quality:trusted (quality status)
- cadence:weekly (refresh freq)
```

### Industry-Specific Tag Examples

#### Financial Services
```
Domain:
  ├── domain:banking
  ├── domain:insurance
  ├── domain:trading
  ├── domain:compliance
  ├── domain:risk

Regulatory:
  ├── regulatory:sox (Sarbanes-Oxley)
  ├── regulatory:gdpr (GDPR compliance)
  ├── regulatory:ccpa (California privacy)
  ├── regulatory:pci (Payment Card Industry)
  └── regulatory:hipaa (Healthcare)
```

#### Healthcare
```
Domain:
  ├── domain:clinical
  ├── domain:billing
  ├── domain:pharmacy
  ├── domain:radiology

Compliance:
  ├── compliance:hipaa
  ├── compliance:phi (Protected Health Info)
  ├── compliance:audit-trail
  └── compliance:consent-required
```

#### Retail/E-commerce
```
Domain:
  ├── domain:products
  ├── domain:orders
  ├── domain:inventory
  ├── domain:pricing
  ├── domain:customer-service

Business-Focus:
  ├── focus:inventory-mgmt
  ├── focus:demand-forecasting
  ├── focus:customer-lifetime-value
  ├── focus:promotional-analysis
```

### Tag Governance Rules

```
Tag Creation Rules:
- Only governance team can create new tags
- New tags require business justification
- New tags must fit within established taxonomy
- Tags reviewed and approved within 5 business days

Tag Application Rules:
- All assets must have at least 1 domain tag
- All assets with PII/sensitive data must be tagged
- Do not apply >5 tags per asset (creates noise)
- Tag changes must be logged in audit trail

Tag Deprecation:
- Tags with <5 assets tagged are candidates for deprecation
- Deprecated tags sunset over 30-day period
- Assets using deprecated tags must be re-tagged
- Deprecation announced 2 weeks in advance
```

---

## Impact Analysis Report Template

Use this template when assessing change impacts.

```markdown
# Impact Analysis Report

## Executive Summary

**Asset:** [Name of asset being changed]
**Change Type:** [Modification / Deletion / Renaming / Deprecation]
**Estimated Impact Scope:** [Low / Medium / High]
**Required Approvals:** [List stakeholders who must approve]
**Recommended Action:** [Proceed / Proceed with caution / Block until conditions met]

---

## Change Summary

### What is Being Changed
[Detailed description of the change]

Example: "Dropping column HISTORICAL_PRICE from Sales_Order_Fact table
(unused since 2022; replaced by dynamic price lookup)"

### Why is This Change Needed
[Business or technical justification]

Example: "Column is deprecated; all downstream models already migrated to
use Price_Dim table. Dropping will improve query performance by 3% and
reduce table size by 2.5 GB."

### Implementation Timeline
- **Analysis Date:** [When this impact analysis was completed]
- **Proposed Change Date:** [When change will be applied]
- **Approval Needed By:** [When approval must be complete]
- **Rollback Capability Until:** [Latest point rollback is possible]

---

## Downstream Impact Analysis

### Direct Consumers (Immediately Impacted)

| Consumer Asset | Type | Impact | Owner | Risk Level |
|---|---|---|---|---|
| Model: Sales_Analysis | Model | Column no longer available; breaking change | Sarah Chen | HIGH |
| Dashboard: Daily Sales Report | Dashboard | Will display NULL; visuals affected | John Smith | HIGH |
| Report: Monthly Sales Forecast | Report | Source data changed; recalculation needed | Jane Doe | MEDIUM |

**Summary:** 3 direct consumers identified. 2 require code changes; 1 requires testing.

### Indirect Consumers (Second-Level Impact)

| Asset Path | Type | Impact Depth | Owner | Risk Level |
|---|---|---|---|---|
| Table → Model: Sales_Analysis → Dashboard: Executive Dashboard | Dashboard | Breaking change will cascade; fixes required in model first | Sarah Chen | HIGH |
| Table → View: Sales_Summary_View → Report: Sales Trend Analysis | Report | Dependent on intermediate view; will propagate change | Bob Wilson | MEDIUM |

**Summary:** 2 indirect consumers via 2-step lineage. Impact depends on fix to Model: Sales_Analysis.

### KPI Consumers

| KPI Name | Related Measures | Impact | Owner |
|---|---|---|---|
| Monthly Revenue | TOTAL_REVENUE (uses Sales_Order_Fact) | Will break if not handled; recalculation required | C-Level |
| Customer Lifetime Value | CUSTOMER_SPEND (uses Sales_Order_Fact) | Will break; business user impact | Sales VP |

**Summary:** 2 KPIs directly impacted. CEO/CFO awareness required due to strategic importance.

### Total Impact Scope

```
Impact Pyramid:
┌─────────────────────────────────────┐
│  5 Executive Dashboards (users: 200+)│ ← Highest user impact
├─────────────────────────────────────┤
│ 12 Analyst Reports (users: 50+)     │
├─────────────────────────────────────┤
│ 3 Internal Models                    │
├─────────────────────────────────────┤
│ 1 Direct Consumer (Sales_Analysis)  │ ← Direct impact
└─────────────────────────────────────┘
```

---

## Impact Classification

### Risk Assessment Matrix

| Impact Type | Severity | Detectability | Blast Radius | Overall Risk |
|---|---|---|---|---|
| Executive Dashboard breaks | High | Easy (immediate user notices) | 200+ users | CRITICAL |
| Model calculation breaks | High | Medium (appears wrong after delay) | 50+ users | HIGH |
| Report shows NULL | Medium | Easy (report owner notices) | 10+ users | MEDIUM |
| Performance degrades | Low | Hard (gradual degradation) | All users | MEDIUM |

### Critical Assets at Risk
- **Executive Dashboard:** "Daily Sales Report" - CEO/CFO use this daily
- **KPI:** "Monthly Revenue" - Used in board reporting and compensation calc
- **Regulatory Report:** "Sales Tax Report" - Audit trail required

---

## Stakeholder Assessment

| Stakeholder | Role | Impact | Approval? |
|---|---|---|---|
| Sarah Chen (Sales Analyst) | Owner: Sales_Analysis Model | Must update model code | YES |
| John Smith (BI Team) | Owner: Executive Dashboard | Dashboard will break; requires fixes | YES |
| Jane Doe (Report Owner) | Owner: Sales Forecast Report | Dependent asset affected | YES |
| CFO | Executive User | KPI impacted; board report affected | YES |
| Data Governance Team | Oversight | Must track change impact | YES |

---

## Mitigation Strategy

### Option 1: No-Impact Approach (Recommended)
- Keep HISTORICAL_PRICE column in table
- Mark column as deprecated (add tag)
- Plan formal removal in 6-month sunset window
- Notify downstream owners of deprecation
- **Pros:** Zero breaking changes; minimal risk
- **Cons:** Technical debt remains; column not removed

### Option 2: Backward-Compatible Migration
- Create view Sales_Order_Fact_V2 without deprecated column
- Migrate downstream consumers to new view gradually
- Keep original table for 90-day compatibility window
- Provide mapping documentation
- **Pros:** Clean break with transition path; reduces technical debt
- **Cons:** Requires downstream testing; coordination needed

### Option 3: Breaking Change with Immediate Fix
- Remove column; notify all owners immediately
- Provide SQL fix for all downstream models
- Test fixes in dev/UAT before production
- Apply changes in coordinated rollout
- **Pros:** Complete cleanup; forces modernization
- **Cons:** High risk if any downstream consumers missed; potential user impact

### Recommendation
Use **Option 2 (Backward-Compatible Migration)**:
- Lower risk than breaking change
- Cleaner outcome than indefinite deprecation
- Provides transition time for downstream teams
- Demonstrates governance responsibility

---

## Testing and Validation Plan

### Testing Phases

**Phase 1: Development Testing (Week 1)**
- [ ] Apply change to development environment
- [ ] Test all 3 direct consumer models
- [ ] Validate KPI calculations still correct
- [ ] Run performance benchmarks
- [ ] Documentation: Test results, any issues found

**Phase 2: Stakeholder Validation (Week 2)**
- [ ] Notify stakeholders; provide test access
- [ ] Sarah Chen (Model Owner): Validate model still produces correct results
- [ ] John Smith (Dashboard Owner): Validate dashboard visuals correct
- [ ] CFO (KPI User): Confirm KPI numbers still trusted
- [ ] Documentation: Stakeholder sign-offs, any requirements identified

**Phase 3: UAT Testing (Week 3)**
- [ ] Deploy change to UAT environment
- [ ] Full regression testing of all downstream assets
- [ ] Performance testing under realistic load
- [ ] Data quality validation
- [ ] Documentation: UAT results, go/no-go decision

**Phase 4: Production Rollout (Week 4)**
- [ ] Deploy to production during low-traffic window
- [ ] Monitor dashboards/reports for issues
- [ ] Track data quality metrics
- [ ] Have rollback plan ready
- [ ] Post-change review 7 days after deployment

---

## Approval Sign-Offs

### Required Approvals (All must approve before proceeding)

- [ ] **Sarah Chen** (Sales_Analysis Model Owner)
  - Signature: _________________ Date: _______
  - Comments: _______________________________

- [ ] **John Smith** (Executive Dashboard Owner)
  - Signature: _________________ Date: _______
  - Comments: _______________________________

- [ ] **CFO** (Executive Stakeholder - KPI User)
  - Signature: _________________ Date: _______
  - Comments: _______________________________

- [ ] **Data Governance Lead** (Oversight)
  - Signature: _________________ Date: _______
  - Comments: _______________________________

---

## Communication Plan

### Stakeholder Notifications

**Immediate Notification (upon impact analysis completion):**
- Email to all direct consumer owners
- Summary of change, why needed, timeline
- Invite to review impact analysis
- Request any missing impacts be reported

**Pre-Approval Notification (1 week before change):**
- Final impact summary
- Testing plan and timeline
- Approval request with sign-off deadline
- Q&A call offered

**Post-Approval Notification (day before change):**
- Confirmed change date and time window
- Rollback plan and contact info
- Request to monitor their assets
- Escalation path if issues found

**Post-Change Notification (day after change):**
- Confirmation change deployed successfully
- Request for any issues to be reported
- Summary of validation results
- Thank you for support

### Training (if needed)
- [ ] Model: Sales_Analysis - 30-min working session with Sarah Chen
- [ ] Dashboard: Executive Dashboard - 15-min review with John Smith
- [ ] KPI: Monthly Revenue - Email summary to CFO

---

## Rollback Plan

**If issues discovered post-deployment:**

1. **Detection (Within 24 hours):**
   - Monitor dashboards for incorrect values
   - Monitor model calculations
   - Monitor data quality metrics
   - Alert triggers: NULL values, 5%+ change in key metrics

2. **Assessment (Within 1 hour of alert):**
   - Confirm issue is real (not expected change)
   - Assess severity (user impact, data correctness)
   - Decide: Fix forward vs. rollback

3. **Rollback (If necessary):**
   - Restore table from backup (retain last 48 hours)
   - Revert downstream model changes
   - Notify stakeholders
   - Root cause analysis

4. **Prevention:**
   - Post-mortem meeting to understand what was missed
   - Enhanced testing added to process
   - Documentation updated

**Rollback Window:** 48 hours after production deployment
**Decision Authority:** Data Governance Lead + CFO

---

## Post-Change Review

**Schedule:** 7 days after deployment

- [ ] All dashboards functioning normally
- [ ] All reports showing expected data
- [ ] KPIs within expected ranges
- [ ] Performance metrics improved as expected
- [ ] No user complaints or escalations
- [ ] Stakeholder feedback gathered
- [ ] Documentation updated with lessons learned
- [ ] Governance team signoff

---
```

---

## Data Quality Scorecard Template

```markdown
# Data Quality Scorecard

## Asset: [Asset Name]
**Date:** [YYYY-MM-DD]
**Owner:** [Name]
**Overall Score:** [XX%] | Status: [Certified / Trusted / Monitor / Issue]

---

## Quality Dimensions

### Dimension 1: Completeness
**Definition:** Percentage of non-null values in required fields

| Field | Total Rows | Null Count | Null % | Score | Status |
|---|---|---|---|---|---|
| CUSTOMER_ID | 10,000,000 | 0 | 0% | 100 | ✓ |
| ORDER_DATE | 10,000,000 | 150 | 0.0015% | 99.8 | ✓ |
| AMOUNT | 10,000,000 | 500 | 0.005% | 99.9 | ✓ |
| DISCOUNT | 10,000,000 | 500,000 | 5% | 95 | ✓ |

**Overall Completeness Score:** 98.7%
**Threshold:** ≥95% (PASS)
**Trend:** Stable (↔)

---

### Dimension 2: Timeliness
**Definition:** How fresh is the data? How long since last update?

| Metric | Target | Actual | Score | Status |
|---|---|---|---|---|
| Last Data Update | <6 hours | 2 hours ago | 100 | ✓ |
| Data Latency | <1 hour | 45 minutes | 100 | ✓ |
| Expected Next Update | >24 hours | 18 hours | 80 | ⚠ |
| Monthly Uptime | ≥99% | 99.7% | 100 | ✓ |

**Overall Timeliness Score:** 95%
**Threshold:** ≥90% (PASS)
**Trend:** Improving (↑)

---

### Dimension 3: Accuracy
**Definition:** Do values match source of truth or business rules?

| Validation Rule | Test Type | Records Tested | Failed | Pass Rate | Status |
|---|---|---|---|---|---|
| AMOUNT ≥ 0 | Range Check | 10M | 5 | 99.99999% | ✓ |
| CUSTOMER_ID exists in Customer_Dim | Referential Integrity | 10M | 1,250 | 99.9875% | ✓ |
| ORDER_DATE ≤ TODAY | Logic Check | 10M | 0 | 100% | ✓ |
| AMOUNT sums correctly by Order | Aggregation Check | 500K | 2 | 99.9996% | ✓ |

**Issues Found & Remediation:**
- 1,250 orders with missing customer ID (0.0125%)
  - Root Cause: Source system data issue
  - Remediation: Pending with source team
  - Status: Escalated to IT; ETA fix = 2024-02-15

**Overall Accuracy Score:** 99.99%
**Threshold:** ≥95% (PASS)
**Trend:** Stable (↔)

---

### Dimension 4: Consistency
**Definition:** Do related values align? No contradictions?

| Consistency Check | Test | Result | Status |
|---|---|---|---|
| Product Prices | List price ≤ extended price | 99.98% consistent | ✓ |
| Customer Hierarchy | Parent-child relationships valid | 100% consistent | ✓ |
| Date Fields | ORDER_DATE ≤ SHIP_DATE ≤ DELIVERY_DATE | 99.95% consistent | ✓ |
| Currency Conversion | Exchange rates consistent | 100% consistent | ✓ |

**Issues Found & Remediation:**
- 200 orders with extended price < list price (duplicate discount applied)
  - Root Cause: Discount logic in source system
  - Remediation: In progress; fix scheduled for 2024-02-12
  - Temporary Workaround: Ignore orders with this pattern in analysis

**Overall Consistency Score:** 99.98%
**Threshold:** ≥95% (PASS)
**Trend:** Stable (↔)

---

### Dimension 5: Uniqueness (Duplicate Detection)
**Definition:** Are there unintended duplicates?

| Check | Count Total | Count Unique | Duplicates | Duplicate % | Status |
|---|---|---|---|---|---|
| ORDER_ID | 10,000,000 | 9,999,500 | 500 | 0.005% | ✓ |
| (CUSTOMER_ID, ORDER_DATE, AMOUNT) | 10,000,000 | 9,999,800 | 200 | 0.002% | ✓ |

**Duplicates Found & Remediation:**
- 500 orders appear 2x in table (exact duplicate rows)
  - Root Cause: ETL bug causing double-load on 2024-01-15
  - Remediation: Duplicates deleted; ETL fixed
  - Status: Resolved 2024-01-16

**Overall Uniqueness Score:** 99.997%
**Threshold:** ≥99.9% (PASS)
**Trend:** Improving after cleanup (↑)

---

### Dimension 6: Validity
**Definition:** Do values match expected format, type, and range?

| Validation | Rule | Violations | Valid % | Status |
|---|---|---|---|---|
| AMOUNT Data Type | Numeric only | 0 | 100% | ✓ |
| AMOUNT Range | 0 ≤ AMOUNT ≤ 999,999,999 | 0 | 100% | ✓ |
| ORDER_DATE Format | YYYY-MM-DD | 0 | 100% | ✓ |
| ORDER_DATE Range | Valid calendar date | 0 | 100% | ✓ |
| CUSTOMER_ID Format | 8-digit numeric | 0 | 100% | ✓ |

**Overall Validity Score:** 100%
**Threshold:** ≥95% (PASS)
**Trend:** Stable (↔)

---

## Overall Quality Score Calculation

```
Overall Score = (Completeness*30% + Accuracy*30% + Timeliness*25% + Consistency*15%)

Calculation:
= (98.7 * 0.30) + (99.99 * 0.30) + (95 * 0.25) + (99.98 * 0.15)
= 29.61 + 29.997 + 23.75 + 14.997
= 98.364%

Overall Score: 98.4% → Status: CERTIFIED
```

---

## Quality Tier Assignment

| Score Range | Tier | Meaning | Action |
|---|---|---|---|
| ≥95% | **Certified** | Production-ready; low risk | Use freely; promote for publishing |
| 85-94% | **Trusted** | Generally reliable; monitor | Use with awareness; plan improvements |
| 75-84% | **Monitor** | Known issues; high touch | Use only if necessary; implement fixes |
| <75% | **Issue** | Significant problems | Do not use; escalate immediately |

**This Asset:** **Certified** (98.4% → Excellent quality)

---

## Data Quality Issues & Remediation

### Open Issues

| Issue | Severity | Root Cause | Remediation | Owner | ETA | Status |
|---|---|---|---|---|---|---|
| Missing Customer IDs (1,250 rows) | High | Source system bug | IT investigating data quality issue in SAP | IT Team | 2024-02-15 | In Progress |
| Duplicate orders (500) | Medium | ETL double-load bug | ETL logic fixed; duplicates removed | Data Team | 2024-01-16 | Resolved |
| Price discrepancies (200) | Low | Discount logic issue | Source system owner reviewing | Finance Team | 2024-02-12 | In Progress |

### Resolved Issues (Last 30 Days)

| Issue | Severity | Resolution | Date Resolved | Lessons Learned |
|---|---|---|---|---|
| Stale data (data not updated for 7 days) | High | Identified and restarted ETL process | 2024-02-01 | Added monitoring alerts |
| Null values in optional field spiked to 15% | Medium | Source system configuration issue fixed | 2024-01-28 | Increased validation in ETL |

---

## Quality Trends

### Historical Scores (Last 12 Months)

| Month | Completeness | Accuracy | Timeliness | Overall | Trend |
|---|---|---|---|---|---|
| 2024-02 | 98.7% | 99.99% | 95.0% | 98.4% | ↑ |
| 2024-01 | 98.0% | 99.95% | 94.0% | 97.8% | ↑ |
| 2023-12 | 97.5% | 99.50% | 92.0% | 97.1% | ↑ |
| 2023-11 | 97.0% | 99.20% | 90.0% | 96.2% | ↓ |
| ... | ... | ... | ... | ... | ... |

**Trend:** Improving overall; especially strong improvement in timeliness

---

## Improvement Opportunities

| Opportunity | Effort | Impact | Owner | Timeline |
|---|---|---|---|---|
| Fix missing Customer IDs in source | Medium | High (reduces accuracy gap) | IT | 2024-02-15 |
| Reduce timeliness to <1 hour (vs. current 2h) | High | Medium (improves for KPI users) | Data Team | Q1 2024 |
| Add duplicate detection in ETL | Low | Medium (prevents future duplicates) | Data Team | 2024-02-28 |
| Improve source data validation | Medium | High (reduces accuracy issues) | Finance Team | Q2 2024 |

---

## Data Quality Dashboard & Monitoring

**Public Dashboard:** [Link to Dashboard]
**Alert Thresholds:**
- Completeness <95% → Alert
- Accuracy <95% → Critical Alert
- Timeliness >6 hours → Alert
- Duplicate % >0.1% → Alert

**Monitoring Frequency:** Daily (automated checks)
**Review Frequency:** Weekly (governance team) / Monthly (stakeholder review)

---

## Owner Sign-Off

- **Data Owner:** [Name, Signature, Date]
- **Technical Owner:** [Name, Signature, Date]
- **Last Review Date:** [YYYY-MM-DD]
- **Next Review Date:** [YYYY-MM-DD]

---
```

---

## Catalog Review Schedule Template

```markdown
# Catalog Review Schedule & Tracking

## Review Cadence

| Asset Category | Frequency | Owners | Effort | Purpose |
|---|---|---|---|---|
| **Critical Assets** | Monthly | Asset Owner + Governance | 1 hour/asset | Ensure accuracy, quality, relevance |
| **Important Assets** | Quarterly | Asset Owner | 30 min/asset | Validate metadata, check usage |
| **Standard Assets** | Annual | Asset Owner | 15 min/asset | Confirm active, no cleanup needed |
| **Experimental** | N/A | Author | Ad hoc | Evaluate readiness for production |
| **Deprecated** | N/A | Retiring Team | One-time | Plan transition, archive |

---

## Critical Assets Review Schedule

Critical assets: KPIs, customer-facing models, regulatory data, high-volume dashboards

| Month | Assets to Review | Owner | Status | Notes |
|---|---|---|---|---|
| **2024-02** | Revenue KPI, Sales Pipeline Model | Sarah Chen | ✓ Complete | Quality improved to 98% |
| **2024-03** | Churn Rate KPI, Customer Segment Model | John Smith | → In Progress | Due 2024-03-15 |
| **2024-04** | Profit Margin KPI, Finance GL Model | Jane Doe | ⏳ Pending | Scheduled for 2024-04-01 |
| **2024-05** | Forecast Accuracy Model, Inventory Levels | Bob Wilson | ⏳ Pending | Scheduled for 2024-05-01 |

---

## Important Assets Quarterly Review Schedule

Important assets: Heavy-use dashboards, core measures, popular models

**Q1 2024 (Jan-Mar) Review Group:**
- Sales_Order_Fact (Table Owner: Sarah Chen) - Due 2024-02-15
- Sales_Summary_Model (Model Owner: John Smith) - Due 2024-02-15
- Executive Sales Dashboard (BI Owner: Jane Doe) - Due 2024-02-15
- Product_Category_Model (Data Owner: Bob Wilson) - Due 2024-03-15

**Q2 2024 (Apr-Jun) Review Group:**
- Finance_GL_Dim (Table Owner: Finance Team) - Due 2024-04-15
- Customer_Enriched_Model (Owner: Marketing Team) - Due 2024-04-15
- Monthly Report Suite (BI Team) - Due 2024-05-15

---

## Annual Review Scheduling

Standard assets: One comprehensive review per year, spread across months

| Month | Review Focus | # Assets | Assigned To | Status |
|---|---|---|---|---|
| Jan | Sales Domain | 25 | Sales Data Team | → In Progress |
| Feb | Finance Domain | 20 | Finance Data Team | ⏳ Starting |
| Mar | HR Domain | 15 | HR Data Team | ⏳ Not Started |
| Apr | Operations Domain | 30 | Ops Data Team | ⏳ Not Started |
| May | Marketing Domain | 18 | Marketing Team | ⏳ Not Started |
| Jun-Dec | Buffer + spillover | 20+ | Ad hoc | ⏳ Not Started |

---

## Review Checklist

Use this checklist for each asset review:

### Asset Metadata Review
- [ ] **Name:** Current and accurate? Business-friendly?
- [ ] **Description:** Up-to-date? Covers what/why/when/limitations?
- [ ] **Owner:** Current? Still in this role?
- [ ] **Tags:** Current and accurate?
- [ ] **Last Updated:** Metadata reflects current state?

### Business Relevance
- [ ] **Still Used?** Any recent usage? By whom?
- [ ] **Still Needed?** Does it still serve a business purpose?
- [ ] **Alignment:** Still aligned with current business priorities?
- [ ] **Deprecation Needed?** Is this asset becoming obsolete?

### Data Quality
- [ ] **Quality Score:** Current? Acceptable?
- [ ] **Known Issues:** Any data quality problems?
- [ ] **Freshness:** Data current? Update frequency still appropriate?
- [ ] **Accuracy Checks:** Still passing validation rules?

### Governance & Compliance
- [ ] **Ownership Clear:** Do we know who owns this?
- [ ] **Sensitive Data Tagged:** Is PII/confidential data properly tagged?
- [ ] **Lineage Current:** Data sources still accurate?
- [ ] **Approvals Current:** Owner and stakeholder approvals current?

### Action Items
- [ ] **Updates Needed:** Any metadata changes required?
- [ ] **Issues to Address:** Any problems identified?
- [ ] **Owners to Contact:** Anyone need to be notified?
- [ ] **Next Review:** Schedule next review date

---

## Stale Asset Identification

Automated process to identify candidate assets for cleanup:

```
Criteria for "Stale" Classification:
- No metadata updates in 24+ months
- No downstream consumers (per lineage)
- No recent queries (per query logs)
- Owner no longer in organization
- No associated KPIs or reports
```

**Current Stale Assets:**

| Asset | Last Updated | Owner Status | Consumers | Recommendation |
|---|---|---|---|---|
| Legacy_Sales_V1 | 2021-06-15 | Owner left org | 0 | Archive |
| Test_Customer_Model | 2022-03-01 | Still active | 0 | Delete |
| Old_GL_Reporting_View | 2021-12-31 | Still active | 2 (legacy reports) | Consolidate → New view |
| Experimental_Forecast | 2023-01-15 | Active | 0 | Deprecate (no adoption) |

---

## Review Completion Tracking

| Owner | Assets Assigned | Completed | In Progress | Pending | % Complete |
|---|---|---|---|---|---|
| Sarah Chen | 5 | 5 | 0 | 0 | 100% |
| John Smith | 6 | 4 | 2 | 0 | 67% |
| Jane Doe | 4 | 1 | 1 | 2 | 25% |
| Bob Wilson | 5 | 0 | 0 | 5 | 0% |
| **TOTAL** | **20** | **10** | **3** | **7** | **50%** |

**SLA:** 90% completion within review window

---

## Review Outcome Summary

### Issues Identified

| Category | Count | Examples |
|---|---|---|
| Metadata Updates Needed | 8 | Stale descriptions, outdated owners |
| Quality Issues Found | 4 | Data completeness declining, lag increasing |
| Deprecation Candidates | 3 | Legacy assets with no users |
| Owner Changes Needed | 5 | Owner left org, reassignment needed |

### Actions Taken

| Action | Count | Status |
|---|---|---|
| Metadata Updated | 8 | Completed |
| Quality Improvement Planned | 4 | Escalated to data team |
| Deprecation Initiated | 3 | In progress (30-day sunset) |
| Ownership Reassigned | 5 | Completed |

---
```

---

## Governance RACI Matrix Template

```markdown
# Governance RACI Matrix

## Legend
- **R (Responsible):** Does the work; executes the task
- **A (Accountable):** Final decision authority; answerable for outcome
- **C (Consulted):** Provides input; expertise needed
- **I (Informed):** Kept in the loop; notified of decisions

---

## Asset Metadata Management

| Activity | Data Owner | Business Owner | Governance Lead | BI Team | Compliance |
|---|---|---|---|---|---|
| Enrich asset descriptions | **R** | C | **A** | I | I |
| Create/update asset names | R | **A** | C | I | - |
| Assign asset ownership | **R** | **A** | C | - | I |
| Update quality scores | **R** | I | C | **A** | - |
| Apply quality tags | R | I | **A** | - | C |

---

## Glossary Management

| Activity | Business Owner | Governance Lead | Data Dictionary Owner | Finance (if $-related) | Compliance |
|---|---|---|---|---|---|
| Define glossary terms | **A** | R | C | C | C |
| Approve new terms | **A** | R | I | **C** (if financial) | I |
| Link terms to assets | R | **A** | I | - | I |
| Review/update terms | **A** | R | C | C | C |
| Deprecate terms | **A** | R | I | I | I |

---

## KPI Management

| Activity | Business Owner | Data Owner | Governance Lead | CFO/Finance | BI Owner |
|---|---|---|---|---|---|
| Define KPI | **A** | C | R | **A** | C |
| Calculate/implement | **C** | **R** | I | I | **A** |
| Validate KPI | **A** | **R** | C | I | I |
| Monitor KPI performance | **A** | I | I | **C** | **R** |
| Review/update KPI | **A** | **R** | C | **A** | I |
| Approve KPI changes | **A** | I | **R** | **A** (if strategic) | I |

---

## Data Quality Management

| Activity | Data Owner | Governance Lead | Quality Team | Business Owner | CIO |
|---|---|---|---|---|---|
| Define quality dimensions | I | **R** | **A** | C | I |
| Score assets | **R** | I | **A** | I | - |
| Track trends | **R** | I | **A** | I | - |
| Fix quality issues | **A** | I | **R** | C | I |
| Publish quality dashboard | **R** | I | **A** | I | I |
| Escalate critical issues | I | **R** | **A** | **A** | **C** |

---

## Change Management

| Activity | Data Owner | Business Owner | Governance Lead | BI Team | IT/Support |
|---|---|---|---|---|---|
| Propose change | **R** | I | **A** | I | - |
| Impact analysis | **R** | **A** | C | **A** | I |
| Stakeholder approval | I | **A** | **R** | **A** (if consumer) | I |
| Test/validate change | **A** | **C** | I | **R** | **R** |
| Deploy change | **A** | I | **R** | **R** | **A** |
| Monitor post-deployment | **R** | I | **A** | **R** | I |
| Incident response | **A** | **A** | **C** | **A** | **R** |

---

## Tag Management & Governance

| Activity | Data Owner | Governance Lead | Domain Owner | IT/Technical |
|---|---|---|---|---|
| Design tag taxonomy | I | **A** | **R** | C |
| Create new tags | I | **A** | **R** | I |
| Apply tags to assets | **R** | **A** | C | - |
| Review tag usage | **R** | **A** | I | - |
| Consolidate/deprecate tags | I | **A** | **R** | I |
| Enforce tag governance | **R** | **A** | C | I |

---

## Lineage & Impact Analysis

| Activity | Data Owner | Governance Lead | Analytics Team | Business Owner |
|---|---|---|---|---|
| Document lineage | **A** | **R** | I | I |
| Maintain lineage accuracy | **R** | I | **A** | I |
| Generate impact reports | **A** | **R** | C | **A** |
| Perform impact analysis | **R** | **A** | C | **A** |
| Communicate impacts | I | **R** | I | **A** |

---

## Catalog Review Process

| Activity | Asset Owner | Governance Lead | Data Owner | Domain Lead |
|---|---|---|---|---|
| Schedule reviews | I | **A** | - | **R** |
| Conduct reviews | **R** | I | **A** | I |
| Follow up on issues | **A** | **R** | **R** | I |
| Report results | I | **A** | I | **R** |
| Plan remediations | **A** | I | **R** | I |

---

## Approval Authority & Escalation

### By Impact Level

**Low Impact Changes** (e.g., description update)
- Authority: Data Owner
- Escalation: Governance Lead (if disputed)

**Medium Impact Changes** (e.g., column rename, tag change)
- Authority: Data Owner + Governance Lead
- Escalation: Domain Lead (if timeline critical)

**High Impact Changes** (e.g., delete column, deprecate KPI)
- Authority: Data Owner + Business Owner + Governance Lead
- Escalation: Executive Sponsor (if strategic impact)

**Critical Impact Changes** (e.g., break KPI, regulatory impact)
- Authority: Executive Sponsor + Governance Committee
- Escalation: CFO/CIO/Chief Data Officer

---

## Decision-Making Authority

| Decision | Authority | Consulted | Timeline | Escalation |
|---|---|---|---|---|
| Add new glossary term | Business Owner + Governance Lead | Data Owner | 5 business days | CFO (if finance term) |
| Define/approve KPI | CFO + Business Owner | Data Owner, BI Lead | 10 business days | CEO (if strategic) |
| Tag new asset | Data Owner | Governance Lead | 1 business day | Governance Lead |
| Score asset as "Issue" | Data Owner + Governance Lead | Business Owner | 3 business days | CIO (if urgent) |
| Deprecate critical asset | Business Owner + Governance Lead | All users | 30 days notice | Executive Sponsor |
| Change KPI calculation | Business Owner + Data Owner | Governance, BI, Users | 15 business days | CFO |

---

## Meeting Schedule & Attendees

### Monthly Data Governance Meeting
- **Attendees:** Governance Lead, Domain Leads, Data Owners (rotating)
- **Duration:** 1 hour
- **Agenda:** Review new issues, approve changes, discuss trends

### Quarterly KPI Steering Committee
- **Attendees:** CFO, Business Owners, Data Owner, Governance Lead
- **Duration:** 1.5 hours
- **Agenda:** KPI performance review, strategy alignment, new KPI approval

### Annual Governance Assessment
- **Attendees:** CIO, CFO, Governance Lead, Domain Leads, Business Owners
- **Duration:** Full day (possibly across 2 half-days)
- **Agenda:** Review program health, adjust policies, plan improvements

---
```

---

## Common Anti-Patterns and Solutions

### Anti-Pattern 1: "IT Metadata" Problem

**Symptom:** Descriptions use technical jargon ("SCD Type 2 dimension", "surrogate key join")

**Root Cause:** Data owners are IT/DBA staff writing for other technical people

**Impact:** Business analysts can't understand what data to use; self-service breaks

**Solution:**
1. Require business analyst to review descriptions
2. Rewrite using business language (customer, order, product)
3. Include examples: "This contains 500K+ customers with name, email, address, phone"
4. Remove technical implementation details
5. Add "For technical details, see data dictionary [link]"

---

### Anti-Pattern 2: "Tag Explosion"

**Symptom:** 200+ tags in system; no one knows what each one means; tags overlap heavily

**Root Cause:** Anyone can create tags; no governance; tags created ad-hoc for each use case

**Impact:** Tags become useless for discovery; searches return too many results; maintenance nightmare

**Solution:**
1. Consolidate to 20-50 core tags (ruthless deduplication)
2. Only governance team can create new tags
3. Design controlled vocabulary (see tag taxonomy template above)
4. Deprecate redundant tags over 30-day period
5. Regular quarterly reviews to keep taxonomy clean

---

### Anti-Pattern 3: "Silent KPI Changes"

**Symptom:** KPI calculation changed without notification; downstream users get wrong results; no audit trail

**Root Cause:** No governance around KPI changes; "just pushed change to production"

**Impact:** Users don't trust KPI numbers; regulatory audit risk; broken dashboards

**Solution:**
1. Version KPI definitions (v1.0, v1.1, v2.0)
2. Never silently change calculation (always bump version)
3. Impact analysis required before change
4. Stakeholder approval before deployment
5. Communicate change 2+ weeks in advance
6. Maintain old calculation alongside new (transition period)
7. Audit trail documents who changed what when

---

### Anti-Pattern 4: "Phantom Owner"

**Symptom:** Asset shows owner = "John Smith" but he left company 6 months ago; no one maintaining asset

**Root Cause:** Asset ownership not tracked; no process to reassign when people leave

**Impact:** Asset metadata stale; quality issues not fixed; governance ineffective

**Solution:**
1. Audit ownership quarterly; identify orphaned assets
2. When people leave: data owner notifies governance team
3. Automatically reassign to manager or team lead
4. Escalate if no clear owner identified
5. Regular reviews confirm ownership is current

---

### Anti-Pattern 5: "Quality Theater"

**Symptom:** System reports "100% quality" but users complain about bad data

**Root Cause:** Quality scoring ignores real issues; metrics disconnect from reality

**Impact:** Users don't trust quality scores; quality program loses credibility

**Solution:**
1. Focus on dimensions that matter (completeness, accuracy, timeliness)
2. Include business validation: "does data match reality?"
3. Document known issues (don't hide them in score)
4. Link quality scores to remediation projects (make it actionable)
5. Review scoring methodology with users (validate it matches their needs)

---

### Anti-Pattern 6: "Lost Lineage"

**Symptom:** Can't answer "where does this data come from?" or "what breaks if we change this table?"

**Root Cause:** Lineage not captured automatically; manually documented lineage becomes outdated

**Impact:** Impact analysis guesses at impacts; changes break downstream assets; scope creep

**Solution:**
1. Capture lineage automatically from data models (not manual docs)
2. Use lineage visualization tools (Datasphere provides this)
3. Update lineage when data models change (not manually)
4. Build impact analysis into change process
5. Generate impact reports before major changes

---

### Anti-Pattern 7: "Glossary Graveyard"

**Symptom:** 500-term glossary that no one uses; conflicts abound; terms obsolete and conflicting

**Root Cause:** Created terms once; never reviewed/maintained; no governance of conflicts

**Impact:** Glossary loses credibility; teams create their own terminology; governance broken

**Solution:**
1. Start with 20-30 high-impact terms (not 500)
2. Implement formal approval workflow
3. Version terms and track changes
4. Resolve conflicts through governance committee
5. Annual review; deprecate unused terms
6. Make glossary discoverable and always up-to-date

---

### Anti-Pattern 8: "Cargo Cult Metadata"

**Symptom:** Asset descriptions copied from template; generic/meaningless content ("Contains customer data")

**Root Cause:** Metadata required by process; no incentive for quality; no review

**Impact:** Descriptions not helpful for discovery; metadata burden without benefit

**Solution:**
1. Require meaningful descriptions (not boilerplate)
2. Review descriptions before publishing
3. Tie metadata quality to data product quality
4. Provide examples of good descriptions
5. Include specific field names and business context
6. Keep descriptions up-to-date (part of maintenance)

---

### Anti-Pattern 9: "Uncontrolled Sensitive Data"

**Symptom:** PII and financial data not properly tagged; discovered in unexpected places

**Root Cause:** No mandatory sensitivity tagging; no discovery mechanism for sensitive data

**Impact:** Compliance violations; audit findings; data breach risk

**Solution:**
1. Require `sensitivity` tag on ALL assets (mandatory)
2. Auto-suggest sensitivity tags based on content analysis
3. Prevent publishing assets without sensitivity tag
4. Build dashboard showing all sensitive data (inventory)
5. Regular audits for untagged sensitive data
6. Link sensitivity tags to access controls (if supported)

---

### Anti-Pattern 10: "Stale Asset Accumulation"

**Symptom:** Catalog full of unused tables, views, models; hard to find useful assets

**Root Cause:** No process to retire assets; "keep everything just in case"; no cleanup culture

**Impact:** Catalog becomes unmaintainable; users overwhelmed with choices; confusion about which asset to use

**Solution:**
1. Periodic cleanup sprints (quarterly)
2. Automated detection of stale assets (unused for 12+ months)
3. Archive (not delete) unused assets
4. Keep archived assets discoverable (for history)
5. Establish deprecation timeline (30-90 days notice)
6. Consolidate redundant implementations
7. Celebrate cleanup progress

---
