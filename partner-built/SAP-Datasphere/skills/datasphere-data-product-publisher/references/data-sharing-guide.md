# Data Sharing Guide Reference

## Data Product Listing Template

Use this template when creating a new data product listing in the Data Sharing Cockpit.

### Required Fields

```
PRODUCT IDENTIFICATION
====================
Product Name: [Business-friendly name, max 100 chars]
  Example: "Customer Master Data with Behavioral Analytics"

Product ID: [System-generated, read-only]
  Example: "prod_customer_master_001"

Category: [Select from dropdown]
  Options: Financial, Sales & Marketing, Operations, HR, Supply Chain, Other
  Selection: Sales & Marketing

Owner Information
=================
Data Owner Name: [Full name]
Data Owner Email: [Email address]
Data Owner Phone: [Optional, phone number]
Support Contact: [Email for consumer support]
Support Hours: [Optional, e.g., "Mon-Fri 8am-5pm EST"]

Business Context
================
Short Description: [One-liner value prop, max 150 chars]
  Example: "Complete customer profiles with 3-year purchase history and engagement metrics"

Long Description: [Detailed explanation, max 2000 chars]
  Include:
  - What data is included
  - Who should use it
  - Key analytical use cases
  - Time period covered
  - Refresh frequency

Data Source Configuration
=========================
Data Source Type: [Table | View | Materialized View | Replicated Object]
  Recommendation: Use View for consumer-friendly schema

Source Object: [Select from your space]
  Example: "vw_customer_analytics_publish"

Columns Included: [Auto-populated from source]
  Verify:
  - No sensitive columns exposed
  - All necessary columns included
  - Column names are business-friendly

Row Count: [Current record count]
  Example: "50,000,000 rows"

Data Size: [Current storage size]
  Example: "25 GB compressed"

Data Grain: [Explain level of detail]
  Example: "One row per customer, with aggregated metrics"

Refresh Frequency: [How often data updates]
  Options: Real-time | Hourly | Daily | Weekly | Monthly | Quarterly | Annual
  Selection: Daily
  Refresh Time (UTC): 06:00

Refresh SLA: [Service level agreement for timeliness]
  Example: "99.5% on-time delivery (5 min tolerance)"

Historical Depth: [How much historical data]
  Example: "3 years rolling window (36 months)"

Data Quality
============
Completeness: [% non-null for key columns]
  Example: "99.8% (5 out of 2.5M customer records have customer_id)"

Accuracy Validation: [How accuracy is verified]
  Example: "Daily reconciliation to ERP system, <0.5% variance tolerance"

Known Limitations: [Document any data gaps or caveats]
  Example:
  - "Excludes B2B customers (B2C retail only)"
  - "Online data limited to web (excludes mobile app)"
  - "Regional data available for 12 primary markets"
  - "Regional discounts excluded (list price only)"

Data Quality Score: [Overall quality rating]
  Options: Excellent (95%+) | Good (85-95%) | Acceptable (75-85%) | Poor (<75%)
  Selection: Excellent (98%)

Accessibility & Sharing
======================
Data Lineage: [Where data originates]
  Example: "Source: SAP S/4HANA ERP
           Transform: Nightly replication + view transformation
           Updated: 2024-01-15"

Visibility: [Who can see this product]
  Options: Private | Internal Only | Public
  Selection: Private
  Rationale: "Initial pilot with selected partners"

Access Approval: [How consumers request access]
  Options: Manual Approval | Auto-Approval
  Selection: Manual Approval
  Rationale: "Want to control initial consumer access"

Consumer Context: [Data isolation per consumer]
  Options: Shared Context | Private Context
  Selection: Private Context
  Rationale: "Each consumer gets isolated data environment"

Licensing & Terms
=================
License Type: [How data is licensed]
  Options: Free | Subscription | Pay-Per-Query | Custom
  Selection: Subscription

License Fee: [Cost structure if applicable]
  Example: "$500/month for subscription"

License Terms: [Attach or reference T&C document]
  Include:
  - Non-exclusive access rights
  - Permitted use cases
  - Restrictions (no redistribution, commercial use)
  - Confidentiality obligations
  - Data retention requirements

Sample License Terms:
  "Non-exclusive access for internal business intelligence use.
   Licensee may not re-distribute, re-sell, or share with third parties.
   Data is confidential and provided as-is without warranty.
   Data retention: No longer than 1 year after subscription ends."

Pricing Model Details: [If applicable]
  Subscription: $500/month, billed monthly, 30-day cancellation
  Pay-Per-Query: $0.50 per GB queried, billed monthly
  Volume Discounts: 20% off at 10+ subscriptions

Marketplace
===========
Marketplace Tags: [Keywords for discoverability]
  Examples: customer, sales, marketing, analytics, 3-year, behavioral

Target Industry: [Industries that would benefit]
  Examples: Retail, E-commerce, Consumer Goods, Financial Services

Use Case Examples: [2-3 concrete examples]
  Example 1: "Customer segmentation for targeted marketing campaigns"
  Example 2: "Lifetime value prediction for acquisition ROI optimization"
  Example 3: "Churn risk identification for retention programs"

Rating & Reviews: [Enable consumer feedback]
  Option: Enabled

Documentation Link: [URL to extended documentation]
  Example: "https://knowledge.company.com/data-products/customer-master"

Support Contacts
================
Primary Support Contact: [Name and email]
Support Email: [Monitored email for requests]
Support SLA: [Response time commitment]
  Example: "24-hour response during business hours"

Documentation Contacts: [Who updates metadata]
```

## License Term Options and Templates

### License 1: Internal Free Access

**Use Case:** Sharing within organization, building adoption

```
LICENSE AGREEMENT: INTERNAL FREE ACCESS

1. GRANT
   Company grants employees of its organization non-exclusive,
   royalty-free right to access and use the Data Product for
   business purposes only.

2. PERMITTED USE
   Licensee may:
   - Query and analyze the Data Product
   - Use analysis results internally for business decisions
   - Share insights (not raw data) with colleagues

3. RESTRICTIONS
   Licensee may NOT:
   - Share raw data with external parties
   - Attempt to identify individuals
   - Reverse-engineer data structures
   - Distribute data commercially

4. CONFIDENTIALITY
   Licensee acknowledges Data is confidential and maintains
   appropriate security controls.

5. NO WARRANTY
   Data provided AS-IS without warranty of accuracy, completeness,
   or fitness for particular purpose.

6. TERMINATION
   License terminates when employment ends or upon 30 days notice.

TERM: Effective upon grant, continues until termination
NO COST: No license fees
```

### License 2: Partner Subscription

**Use Case:** Premium data sharing with external partners

```
LICENSE AGREEMENT: PARTNER SUBSCRIPTION DATA

1. GRANT
   Provider grants Licensee non-exclusive right to access
   and use Data Product under terms of this Agreement.

2. PERMITTED USE
   Licensee may:
   - Query and analyze Data Product
   - Incorporate insights into business processes
   - Use for [SPECIFIC USE CASE: "customer analytics", "market analysis"]
   - Support [NUMBER] internal users

3. RESTRICTIONS
   Licensee may NOT:
   - Redistribute, re-sell, or share Data with third parties
   - Disclose Data to competitors
   - Create derivative products for external sale
   - Attempt to identify individuals from data
   - Use Data for purposes other than above

4. DATA QUALITY
   Provider provides Data "AS-IS" without warranties regarding:
   - Accuracy, timeliness, or completeness
   - Fitness for specific purposes
   - Non-infringement of third-party rights

5. REFRESH TERMS
   - Data updated: [FREQUENCY: "Daily by 6am UTC"]
   - Provider not liable for refresh delays
   - Maximum 48-hour delay without penalty

6. PAYMENT
   - Fee: $[AMOUNT]/[PERIOD] (e.g., "$1,000/month")
   - Payment: Due net 30 days from invoice
   - Late payment: 1.5% monthly interest
   - Annual discount available: [%]

7. TERM & TERMINATION
   - Initial Term: [PERIOD: "12 months"]
   - Renewal: Automatic unless 30-day notice given
   - Termination for Cause: Immediate if material breach
   - Termination for Convenience: 30 days notice, no refund
   - Upon termination: Licensee ceases all access immediately

8. CONFIDENTIALITY
   Licensee treats Data as confidential and implements reasonable
   security measures to prevent unauthorized access.

9. LIABILITY LIMIT
   Provider's total liability limited to fees paid in prior 12 months.
   In no event liable for indirect, consequential, lost profits, or
   data corruption damages.

10. DATA RESIDENCY
    Data remains in [REGION: "US East"] data centers only.
    Licensee not permitted to export or copy to other regions.

EXECUTION: Executed and effective as of [DATE]
```

### License 3: Marketplace - Pay-Per-Query

**Use Case:** Open marketplace model with usage-based pricing

```
LICENSE AGREEMENT: MARKETPLACE PAY-PER-QUERY

1. GRANT
   Provider grants Licensee non-exclusive right to query Data Product
   according to pricing model in Section 5.

2. PERMITTED USE
   Licensee may:
   - Query Data Product for business intelligence
   - Download query results for analysis
   - Use results for internal decision-making
   - Support up to [NUMBER] concurrent queries

3. RESTRICTIONS
   Licensee may NOT:
   - Redistribute raw data or query results
   - Use for commercial re-sale
   - Share Data with external parties
   - Attempt to identify individuals

4. QUERY TERMS
   - Query Limit: Unlimited
   - Concurrent Queries: [NUMBER, e.g., "5 concurrent"]
   - Result Size Limit: [e.g., "1M rows per query"]
   - Timeout: Queries > 1 hour auto-cancel

5. PRICING & PAYMENT
   Pricing Model: Pay-Per-Query (GB scanned)
   Rate: $[PRICE] per GB scanned (e.g., "$0.50 per GB")
   Minimum: None
   Billing: Monthly, based on actual usage
   Payment Due: Net 30 days from invoice
   Late Payment: 1.5% monthly interest

   Example Billing:
   - February Queries: 250 GB scanned
   - Rate: $0.50/GB
   - Invoice: 250 * $0.50 = $125.00

6. VOLUME DISCOUNTS
   - 100+ GB/month: 10% discount
   - 500+ GB/month: 25% discount
   - 1,000+ GB/month: 40% discount

7. USAGE MONITORING
   Provider monitors:
   - GB scanned per query (billed metric)
   - Query frequency
   - Data accessed
   Licensee receives weekly usage reports.

8. DATA QUALITY & DISCLAIMERS
   Data provided AS-IS without warranty.
   Provider not responsible for:
   - Accuracy or completeness
   - Timeliness relative to source systems
   - Fitness for particular purposes

9. TERM & TERMINATION
   - Effective: Upon account creation
   - Ongoing: Month-to-month auto-renewal
   - Termination: Either party may terminate with 30-day notice
   - Effect: Access revoked at end of notice period
   - Final Bill: Due on termination date

10. CONFIDENTIALITY
    Licensee maintains Data confidentiality per industry standards.

11. LIABILITY LIMITS
    Provider total liability capped at usage fees in prior 3 months.
    No liability for indirect or consequential damages.

ACCEPTANCE: Acceptance of terms required upon first query
```

## Access Policy Configuration Patterns

### Pattern 1: Consumer Role-Based Access

Implement different access policies based on consumer type.

**Sales Team (Internal)**
```sql
-- Full access to all columns, no filtering
CREATE VIEW vw_sales_data_internal AS
SELECT * FROM product_sales_fact
WHERE business_unit = 'SALES';

SECURITY POLICY: NONE (internal full access)
```

**Partner - Reseller**
```sql
-- Limited columns, aggregate level
CREATE VIEW vw_sales_data_reseller AS
SELECT
  transaction_date,
  product_category,      -- Not product_id (too detailed)
  region,
  SUM(quantity) as total_quantity,      -- Aggregated
  SUM(revenue) as total_revenue,        -- Aggregated
  COUNT(DISTINCT customer_id) as customers  -- Hidden identities
FROM product_sales_fact
WHERE transaction_date >= DATEADD(MONTH, -12, CURRENT_DATE)
GROUP BY transaction_date, product_category, region;

SECURITY POLICY:
- Column restrictions: Hide unit_price, cost, customer_id
- Row restrictions: Current year only (12-month rolling)
```

**Partner - Investor**
```sql
-- Quarterly summaries only
CREATE VIEW vw_sales_data_investor AS
SELECT
  EXTRACT(QUARTER FROM transaction_date) as quarter,
  EXTRACT(YEAR FROM transaction_date) as year,
  SUM(revenue) as total_revenue,
  COUNT(DISTINCT customer_id) as customer_count,
  AVG(revenue / NULLIF(quantity, 0)) as avg_price,
  SUM(quantity) as total_units
FROM product_sales_fact
WHERE transaction_date >= DATEADD(YEAR, -3, CURRENT_DATE)
GROUP BY EXTRACT(QUARTER FROM transaction_date),
         EXTRACT(YEAR FROM transaction_date);

SECURITY POLICY:
- Column restrictions: Only aggregate metrics
- Row restrictions: Last 3 years quarterly summary
```

### Pattern 2: Data Masking by Consumer Sensitivity

Hide sensitive columns based on consumer classification.

**Configuration:**
```
CONSUMER CLASSIFICATION:
  - Internal (Full Access): All columns, all rows
  - Partner (Medium Access): 60% of columns, filtered rows
  - Public (Limited Access): 20% of columns, aggregate only

APPLICATION:
  Consumer: Acme Partners (Partner classification)
  Hide Columns: unit_cost, profit_margin, negotiated_discount
  Filter Rows: Last 12 months (not 5-year history)
  Mask Values: Customer names → hashed IDs
```

**Implementation:**
```sql
-- Base table (secure)
CREATE TABLE sales_transaction_secure (
  transaction_id INT,
  customer_name VARCHAR(100),  -- SENSITIVE
  customer_id INT,
  product_id INT,
  unit_cost DECIMAL(10,2),     -- SENSITIVE
  unit_price DECIMAL(10,2),
  quantity INT,
  revenue DECIMAL(10,2)
);

-- Secure column definitions
ALTER TABLE sales_transaction_secure
SET COLUMN SECURITY (
  customer_name = 'SENSITIVE',
  unit_cost = 'SENSITIVE'
);

-- Partner view (limited access)
CREATE VIEW vw_sales_for_partner AS
SELECT
  transaction_id,
  HASH(customer_name) as customer_hash,  -- Masked
  product_id,
  -- unit_cost hidden completely
  unit_price,
  quantity,
  revenue
FROM sales_transaction_secure
WHERE transaction_date >= DATEADD(MONTH, -12, CURRENT_DATE)
  AND customer_id NOT IN (SELECT customer_id FROM customer_vip_list);
  -- Exclude VIP customers from partner view

-- Grant permissions
GRANT SELECT ON vw_sales_for_partner TO 'acme_partners_consumer_context';
```

### Pattern 3: Time-Based Data Tiering

Provide different access horizons based on subscription level.

**Tier 1: Starter (Free)**
```
Access: Last 3 months only
Refresh: Weekly (not daily)
Latency Tolerance: 7 days (historical data only)
Rows Returned: Max 1M per query
Use Case: Ad-hoc exploration, small team
```

**Tier 2: Professional ($500/month)**
```
Access: Last 12 months
Refresh: Daily
Latency Tolerance: Same-day (updated by 6am next day)
Rows Returned: Max 100M per query
Use Case: Regular analysis, medium team
```

**Tier 3: Enterprise ($2,000+/month)**
```
Access: All historical (7+ years)
Refresh: Real-time (updated within 1 hour)
Latency Tolerance: 1 hour
Rows Returned: Unlimited
Concurrent Queries: 10+
Use Case: Deep analysis, large organization
```

**Implementation:**
```sql
-- Tiered view creation
CREATE VIEW vw_sales_tier_starter AS
SELECT * FROM sales_fact
WHERE transaction_date >= DATEADD(MONTH, -3, CURRENT_DATE);

CREATE VIEW vw_sales_tier_professional AS
SELECT * FROM sales_fact
WHERE transaction_date >= DATEADD(YEAR, -1, CURRENT_DATE);

CREATE VIEW vw_sales_tier_enterprise AS
SELECT * FROM sales_fact;  -- All data

-- Assign views based on subscription
CONSUMER: Consumer_A (Tier: Starter)
GRANT SELECT ON vw_sales_tier_starter TO 'consumer_a_context';

CONSUMER: Consumer_B (Tier: Professional)
GRANT SELECT ON vw_sales_tier_professional TO 'consumer_b_context';

CONSUMER: Consumer_C (Tier: Enterprise)
GRANT SELECT ON vw_sales_tier_enterprise TO 'consumer_c_context';
```

## Quality Checklist Before Publishing

Use this checklist to verify data product readiness.

```
DATA QUALITY VALIDATION
=======================

COMPLETENESS CHECKS
[ ] No nulls in primary key columns
    Script: SELECT COUNT(*) FROM product WHERE product_id IS NULL
    Expected: 0 rows

[ ] Row count stable (within ±5% of expected daily volume)
    Script: SELECT COUNT(*) FROM sales WHERE DATE(load_date) = CURRENT_DATE
    Expected: Daily volume ±5%

[ ] All expected columns present
    Script: DESCRIBE product_sales_view
    Compare: Against documented schema

[ ] No orphaned records (foreign key integrity)
    Script: SELECT COUNT(*) FROM sales s
            WHERE NOT EXISTS (SELECT 1 FROM customers c WHERE c.id = s.customer_id)
    Expected: 0 rows

ACCURACY CHECKS
[ ] Sample spot-check against source system (10-20 records)
    Process: Compare 20 random transaction IDs
    Expected: 100% match

[ ] Monthly totals reconcile to GL (within 0.5%)
    Script: SELECT SUM(amount) FROM sales WHERE MONTH = CURRENT_MONTH
    Compare: Against GL Total from ERP
    Tolerance: ±0.5%

[ ] Aggregate metrics validate with known reports
    Process: Compare dashboard metrics with published reports
    Expected: Match within 0.1%

CONSISTENCY CHECKS
[ ] Foreign key relationships valid
    Script: Validate all product_ids exist in product_master
    Expected: 100% match

[ ] Grain/cardinality matches documentation
    Documentation: "One row per transaction, uniqueness on transaction_id"
    Validation: Count(Distinct transaction_id) = Count(*)
    Expected: Equals

[ ] No duplicate composite keys
    Script: SELECT transaction_id, customer_id, COUNT(*) FROM sales
            GROUP BY transaction_id, customer_id
            HAVING COUNT(*) > 1
    Expected: 0 rows

[ ] Data types consistent with schema
    Process: Review DESCRIBE output for column types
    Expected: All matches documented schema

TIMELINESS CHECKS
[ ] Last refresh timestamp recent (within SLA)
    Script: SELECT MAX(load_timestamp) FROM sales_fact
    Expected: Within last 24 hours

[ ] Refresh success rate meets SLA (99%+)
    Script: SELECT COUNT(*) FROM refresh_log
            WHERE success = TRUE AND load_date >= DATEADD(DAY, -30, CURRENT_DATE)
    Expected: ≥ 30 days / month * 0.99 = ≥29.7 successes

[ ] No stale partitions (gaps in date coverage)
    Script: SELECT DISTINCT transaction_date FROM sales
            ORDER BY transaction_date DESC
    Expected: No gaps in recent dates

CONFORMITY CHECKS
[ ] No schema drift (columns, types unchanged)
    Process: Compare current DDL to version-controlled schema
    Expected: Exact match

[ ] Column names business-friendly (no cryptic codes)
    Review: All column names understandable to business users
    Expected: All descriptive

[ ] All documentation current and accurate
    Review: Updated within last 30 days
    Expected: All sections current

SECURITY & PRIVACY CHECKS
[ ] No PII exposed unmasked
    Process: Review view definitions for customer names, SSN, etc.
    Expected: All sensitive data masked/removed

[ ] Access control policies in place
    Check: Row/column level security policies defined
    Expected: Policies for all consumer types

[ ] License terms final and reviewed by legal
    Review: With legal/compliance team
    Expected: Approved signature

PERFORMANCE CHECKS
[ ] Query performance meets expectations
    Test: Run 3 representative queries
    Expected: All complete within 30 seconds

[ ] Memory usage reasonable (no spills)
    Monitor: Check query logs for memory spill events
    Expected: Zero spill events

[ ] View dependencies documented
    List: All dependent views clearly identified
    Expected: Dependency tree documented

METADATA CHECKS
[ ] Business description complete and clear
    Review: Can external user understand purpose/content?
    Expected: Yes, without follow-up questions

[ ] Data lineage documented
    Document: Source → ETL → View → Consumer
    Expected: Full lineage documented

[ ] Refresh frequency and SLA clearly stated
    Document: "Daily by 6am UTC, 99.5% on-time SLA"
    Expected: Clear SLA statement

[ ] Known limitations documented
    Example: "Excludes web orders, includes retail only"
    Expected: Specific limitations listed

[ ] Contact information complete
    Check: Owner, support, escalation contacts
    Expected: All contacts identified and verified

INFRASTRUCTURE CHECKS
[ ] Monitoring & alerting configured
    Setup: Email alerts for refresh failures
    Expected: Alerts active and tested

[ ] Backup strategy in place
    Document: Recovery procedure and RTO/RPO
    Expected: Documented and tested

[ ] Capacity sufficient for growth
    Plan: 3-year growth projection
    Expected: Storage/compute adequate

SIGN-OFF
========
[ ] Business Owner Approves: _________________ Date: _______
[ ] Data Steward Approves: _________________ Date: _______
[ ] Quality Manager Approves: _________________ Date: _______
[ ] Technical Owner Approves: _________________ Date: _______

Ready for Publication: YES / NO
```

## Consumer Onboarding Workflow

Standard process for onboarding newly approved data product consumers.

```
CONSUMER ONBOARDING WORKFLOW
=============================

PHASE 1: PRE-APPROVAL (1-2 days before approval)
═══════════════════════════════════════════════

Step 1: Verify Consumer Information
  □ Company name and industry
  □ Contact person and title
  □ Number of users who will access
  □ Expected use cases
  Review: Does request align with product intent?

Step 2: Assess Risk
  □ Is consumer a direct competitor?
  □ Are there geographic restrictions (data residency)?
  □ Are there industry restrictions?
  □ Check: Industry/risk matrix for approval

Step 3: Prepare Approval Response
  □ Draft approval email
  □ Include: Access instructions, support contact, T&Cs
  □ Schedule: Prepare welcome materials


PHASE 2: APPROVAL NOTIFICATION (Day 1)
═══════════════════════════════════════

Step 1: Send Approval Email
  Template:
  ───────────────────────────────────────────────
  Subject: Access Approved: [Product Name]

  Dear [Consumer Name],

  Your request to access [Product Name] has been APPROVED.

  QUICK START:
  1. Login to Datasphere with your credentials
  2. Navigate to Data Sharing → My Subscriptions
  3. Click [Product Name] to begin querying
  4. See documentation: [link]

  SUPPORT:
  Questions? Contact: [support email]
  Support hours: [hours]

  LICENSE TERMS:
  [Summary of key terms]
  Full terms: [link]

  DATA DESCRIPTION:
  [1-2 paragraph summary]

  IMPORTANT CONTACTS:
  Data Owner: [name, email]
  Technical Support: [email, hours]

  Welcome aboard!
  ───────────────────────────────────────────────

Step 2: Notify Internal Team
  To: Data owner, support team
  Content: New consumer approved, use case summary


PHASE 3: TECHNICAL PROVISIONING (1-3 days)
═══════════════════════════════════════════

Step 1: Create Consumer Context (if private context model)
  Action: Provision isolated data environment for consumer
  Includes: Network, storage, access controls
  Expected: 24 hours to completion

Step 2: Configure Access Policies
  Actions:
  □ Apply row-level security (if applicable)
  □ Apply column-level security (if applicable)
  □ Configure view permissions
  □ Test access with sample query
  Validation: Verify only authorized data visible

Step 3: Document Consumer-Specific Configuration
  Record:
  □ Consumer context ID
  □ Connection strings/endpoints
  □ Specific policies applied
  □ Data restrictions (time, volume, columns)
  File: [Documentation system]


PHASE 4: CONSUMER ENABLEMENT (3-5 days)
═══════════════════════════════════════

Step 1: Provide Detailed Documentation
  Send:
  □ Schema documentation (column descriptions, data types)
  □ Sample queries for common use cases
  □ Data dictionary
  □ Known limitations and data quality notes
  □ Refresh schedule and SLA

Step 2: Conduct Technical Walkthrough (if requested)
  Schedule: 30-minute video call
  Content:
  - Connection setup
  - Navigation in Datasphere
  - Query examples
  - Where to get help
  Attendees: Consumer tech lead + support person

Step 3: Monitor Initial Usage
  Week 1-2:
  □ Check for errors in consumer logs
  □ Verify expected data volume retrieved
  □ Proactively reach out if issues detected
  □ Gather initial feedback


PHASE 5: ONGOING SUPPORT (Continuous)
═════════════════════════════════════

Monthly Engagement:
  □ Review usage metrics
  □ Confirm SLA met (refresh timeliness, availability)
  □ Check for support requests (response time < 24h)
  □ Gather feedback (survey quarterly)

Quarterly Business Review:
  □ Usage trends
  □ ROI/value realized
  □ Product improvements based on feedback
  □ Upcoming product changes


PHASE 6: OFFBOARDING (Upon Termination)
═════════════════════════════════════════

Step 1: Termination Notice
  To: Consumer
  Timeline: 30-day notice
  Content: Specify termination date, offer grace period

Step 2: Final Access & Data Export
  Allow: Consumer to export final dataset (if applicable)
  Timeline: Until termination date
  Support: Help with export process if needed

Step 3: Revoke Access
  On Termination Date:
  □ Disable consumer context
  □ Revoke query permissions
  □ Remove from subscription list
  □ Archive access logs

Step 4: Feedback Collection
  Request: Post-termination survey
  Questions:
  - Was product valuable?
  - Why discontinued?
  - What would improve?
  Use: Guide product improvements
```

## Managing Data Product Lifecycle

Framework for versioning, updating, deprecating, and retiring data products.

```
LIFECYCLE PHASES
════════════════

PHASE 1: LAUNCH (0-3 months)
─────────────────────────────
Status: Pilot / Limited Release
Consumers: Selected partners, internal teams
Focus: Quality validation, feedback collection
Actions:
  □ Monitor quality metrics daily
  □ Respond to questions within 24h
  □ Collect detailed feedback
  □ Prepare launch review
Output: Production readiness assessment

PHASE 2: GROWTH (3-12 months)
──────────────────────────────
Status: General Availability
Consumers: Increasing adoption
Focus: Scale, stability, improvements
Actions:
  □ Weekly quality/performance review
  □ Respond to feature requests
  □ Implement non-breaking improvements
  □ Monitor usage trends
  □ Add consumers as demand grows
Output: Stable, reliable product

PHASE 3: MATURITY (12+ months)
────────────────────────────────
Status: Stable
Consumers: Established user base
Focus: Optimization, efficiency
Actions:
  □ Monthly review of metrics
  □ Optimize performance/cost
  □ Plan enhancements based on roadmap
  □ Maintain high SLA
Output: Efficient, well-tuned service

PHASE 4: DECLINE (Product nearing end)
────────────────────────────────────────
Status: Limited Updates
Consumers: Stable or declining
Focus: Transition planning
Actions:
  □ Announce intended retirement date (12+ months notice)
  □ Reduce new feature development
  □ Prepare migration path for consumers
  □ Document replacement products
Output: Managed transition


VERSION MANAGEMENT
═══════════════════

Semantic Versioning: MAJOR.MINOR.PATCH

MAJOR (Breaking changes):
  Example: Removing a column
  Action: 60+ days notice to consumers
  Migration: Provide alternative view/product
  Version: 2.0 → 3.0

MINOR (Additive changes):
  Example: Adding new column, updating metrics
  Action: 15+ days notice
  Compatibility: Backward compatible
  Version: 2.0 → 2.1

PATCH (Bug fixes):
  Example: Correcting data quality issue
  Action: Immediate deployment
  Impact: Transparent to consumers
  Version: 2.0 → 2.0.1

Version Communication:
  Change Log: Document all changes
  Timeline: When deployed
  Impact: Who is affected
  Action Required: Yes/No


UPDATE PROCESS
═══════════════

Step 1: Plan Update
  □ Define what's changing
  □ Determine version number
  □ Calculate impact on consumers
  □ Set deployment date

Step 2: Communicate
  □ Notify consumers 15-60 days before
  □ Describe changes and benefits
  □ Explain any action required
  □ Provide migration guide if breaking

Step 3: Implement
  □ Deploy to staging environment
  □ Test with representative queries
  □ Validate consumer views still work
  □ Deploy to production

Step 4: Monitor
  □ Watch consumer query success rate
  □ Monitor performance impact
  □ Respond to issues immediately
  □ Collect feedback

Step 5: Document
  □ Update version history
  □ Update product documentation
  □ Update schema/lineage


DEPRECATION PROCESS
════════════════════

Timeline:
  Day 1: Announce deprecation (12 months notice)
  Month 6: Final warning
  Month 11: Final opportunity to migrate
  Month 12+1: Retirement


Deprecation Announcement (Day 1):
  To: All consumers
  Subject: [Product Name] Deprecation Announcement

  [Product Name] will be retired on [DATE], 12 months from now.

  REASON: [Explain business rationale]
  REPLACEMENT: [What to use instead]
  MIGRATION: [Steps to transition]
  SUPPORT: [Help available during transition]
  DEADLINE: [Final day for questions/assistance]

  Questions? Contact: [support contact]


Migration Support:
  □ Provide comparison of old vs. new product
  □ Supply migration guide with examples
  □ Offer technical assistance (calls, emails)
  □ Extend support during transition period
  □ Provide data export if needed


RETIREMENT PROCESS
════════════════════

30 Days Before:
  □ Final notice to all consumers
  □ Confirm all consumers migrated or confirmed termination
  □ Disable new access requests

On Retirement Date:
  □ Revoke all access permissions
  □ Archive product and documentation
  □ Remove from marketplace
  □ Retain backups for compliance

Post-Retirement:
  □ Monitor for questions/incidents
  □ Document lessons learned
  □ Update guidance for future products
```
