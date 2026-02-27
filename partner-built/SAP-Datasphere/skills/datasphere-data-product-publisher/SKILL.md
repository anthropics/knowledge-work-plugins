---
name: Data Product Publisher
description: "Publish and monetize data products through Datasphere's Data Sharing Cockpit. Use when preparing data for external consumers, setting up marketplace listings, managing access control, or licensing data assets. Keywords: data sharing, data product, marketplace, consumer, license, access control, data provider, visibility, quality."
---

# Data Product Publisher Skill

## Overview

The Data Product Publisher skill guides you through the complete lifecycle of publishing, managing, and monetizing data products in SAP Datasphere. From preparing high-quality data to creating marketplace listings, managing consumer subscriptions, and defining access policies, this skill provides best practices for successful data sharing.

## When to Use This Skill

Trigger this skill when you need to:
- Prepare data for sharing with external consumers
- Create a data product listing in the Data Sharing Cockpit
- Define access policies and license terms
- Publish data products to the Datasphere marketplace
- Onboard data consumers and manage access
- Update or deprecate existing data products
- Monitor data product quality and performance
- Manage subscription and licensing compliance
- Establish data governance for shared assets
- Generate insights from data product usage

## What Are Data Products in Datasphere?

### Business Value of Data Products

Data products are curated, managed, business-ready datasets packaged for consumption by external parties. They transform raw data into valuable strategic assets.

**Strategic Benefits:**
- **Revenue Generation**: Monetize internal data assets through data marketplace
- **Partner Enablement**: Share curated data with partners for joint business initiatives
- **Ecosystem Growth**: Build data ecosystem attracting new consumers and use cases
- **Competitive Advantage**: Leverage industry expertise through proprietary datasets
- **Operational Efficiency**: Enable self-service analytics reducing internal support burden

**Business Use Cases:**
- Financial services: Credit risk models, market data, transaction datasets
- Retail: Customer demographics, inventory insights, demand forecasting data
- Healthcare: Clinical outcomes, patient cohorts, treatment effectiveness
- Manufacturing: Supply chain data, quality metrics, equipment diagnostics
- Transportation: Route optimization data, fleet analytics, logistics insights

### Data Product Characteristics

**Well-Designed Data Products:**
1. **Clear Business Context**: Explain what the data represents and business relevance
2. **High Quality**: Completeness, accuracy, timeliness verified and documented
3. **Well-Documented**: Metadata, lineage, refresh frequency, known limitations
4. **Governed**: Clear ownership, access policies, data classification
5. **Maintained**: Actively updated, version-controlled, deprecation path defined
6. **Accessible**: Multiple consumption formats, clear usage examples
7. **Discoverable**: Proper categorization, tags, searchable descriptions

## Data Sharing Cockpit Overview

The Data Sharing Cockpit is Datasphere's central hub for managing all data sharing activities.

### Cockpit Sections

**Data Provider Features:**
- **My Products**: Create and manage your published data products
- **Pending Requests**: Review and approve consumer access requests
- **Subscriptions**: Monitor active data product subscriptions
- **Analytics**: View usage metrics, consumer engagement, quality stats
- **Settings**: Configure data product defaults, policies, and governance

**Navigation Path:**
```
Datasphere Main Menu → Data Sharing Cockpit → Data Provider
```

### Key Capabilities

| Capability | Purpose | Frequency |
|------------|---------|-----------|
| Create Product Listing | Define new data product | Once during setup |
| Set Access Policy | Control who can consume | Monthly review |
| Manage Terms & Conditions | Define license terms | During product launch |
| Review Requests | Approve/deny access | Daily/Weekly |
| Monitor Subscriptions | Track active consumers | Weekly |
| Publish Updates | Version data product | As needed |
| Manage Consumer Access | Grant/revoke permissions | As needed |
| View Analytics | Track usage and engagement | Weekly/Monthly |

## Data Provider Workflow: Preparing Data

### Step 1: Select Source Data

**Evaluation Criteria:**
- **Business Value**: Does the data address real consumer needs?
- **Quality Readiness**: Is data accurate, complete, and timely?
- **Regulatory Compliance**: Does sharing comply with privacy and regulations?
- **Ownership Clarity**: Does business own the rights to share?
- **Refresh Frequency**: Can we maintain timeliness cost-effectively?

**Data Selection Process:**
```
1. Identify candidate datasets (brainstorm with business stakeholders)
2. Evaluate business value proposition
3. Assess data quality maturity
4. Review legal/compliance implications
5. Calculate maintenance cost vs. expected revenue
6. Prioritize by strategic importance and readiness
7. Select top 3-5 for pilot
```

### Step 2: Validate Data Quality

**Quality Dimensions to Assess:**

**Completeness:**
- No missing required fields
- Expected row count matches reality
- Historical coverage sufficient for analysis
- Example: "Product table has 100K SKUs with complete descriptions"

**Accuracy:**
- Spot-check sample data against source
- Verify calculations and aggregations
- Validate against known benchmarks
- Example: "Revenue totals within 0.1% of source system"

**Consistency:**
- Joins to related tables successful
- Foreign keys valid
- No conflicting values in related fields
- Example: "Every order.customer_id matches a customer record"

**Timeliness:**
- Refresh frequency documented
- Refresh SLA achievable and tested
- Latest data available within committed timeframe
- Example: "Daily refresh by 6am UTC, 99.5% on-time"

**Uniqueness:**
- Primary keys non-duplicated
- Grain consistent with documentation
- No unexpected duplicates in fact data
- Example: "Each transaction_id appears exactly once"

### Step 3: Prepare Metadata Documentation

**Essential Metadata:**

```
Dataset: Sales Transactions

DESCRIPTION:
  Daily transaction-level sales data across all retail locations.
  Includes order details, item-level quantities and prices.

BUSINESS CONTEXT:
  Enables analysis of sales patterns, product performance,
  customer spending behavior, and regional trends.

GRAIN:
  One row per item per order (transactional detail)
  Example: Order 12345 with 3 items = 3 rows

REFRESH FREQUENCY:
  Daily, 5am UTC. 99.5% on-time SLA.

ROW COUNT:
  Current: 50M rows (last 12 months)
  Growth: +50% annually

SIZE:
  Current: 25 GB compressed
  Growth: +2 GB monthly

KEY COLUMNS:
  - transaction_id (Primary Key)
  - transaction_date (Partition Key)
  - customer_id (Foreign Key)
  - product_id (Foreign Key)
  - quantity (Fact)
  - unit_price (Fact)
  - total_amount (Fact)

KNOWN LIMITATIONS:
  - Data includes 5 major retailers only (not all locations)
  - Web sales excluded (retail store sales only)
  - Pricing excludes regional discounts applied post-transaction
  - Returns recorded as separate negative transactions

DATA LINEAGE:
  Source: Enterprise ERP (SAP S/4HANA)
  ETL: Nightly Replication Flow (Datasphere)
  Transformations: None (raw transaction copy)
  Last Validated: 2024-01-15

CONTACT:
  Owner: sales@company.com
  Support: datasupport@company.com
```

### Step 4: Create View or Table for Sharing

Create a dedicated view/table for the data product (not the raw source):

**Why Create a View:**
- Isolates consumer access from production tables
- Enables selective column exposure (hide sensitive columns)
- Allows computed columns (e.g., profit margin calculation)
- Simplifies access revocation
- Enables data transformation/cleansing for consumers

**Example View Creation:**

```sql
CREATE VIEW product_sales_for_sharing AS
SELECT
  transaction_id,
  transaction_date,
  customer_id,
  product_id,
  ROUND(unit_price, 2) as unit_price,
  quantity,
  ROUND(total_amount, 2) as total_amount,
  CASE
    WHEN EXTRACT(MONTH FROM transaction_date) <= 6 THEN 'H1'
    ELSE 'H2'
  END as fiscal_half
FROM sales_transactions
WHERE transaction_date >= DATEADD(YEAR, -2, CURRENT_DATE)
  AND customer_id IS NOT NULL
-- Exclude internal sales and test transactions
  AND business_unit != 'INTERNAL'
  AND customer_id NOT BETWEEN 999990 AND 999999;

-- Column-level security: can be applied per consumer
ALTER VIEW product_sales_for_sharing SET COLUMN SECURITY
  (unit_price = 'SENSITIVE', total_amount = 'SENSITIVE');
```

**Best Practices:**
- Use descriptive view names
- Include computed/derived columns valuable for consumers
- Exclude columns with sensitive information
- Document all transformations
- Version your view definitions
- Use consistent naming conventions

## Creating a Data Product Listing

### Step 1: Access Data Sharing Cockpit

```
Datasphere Home → Data Sharing Cockpit → My Products → Create New Product
```

### Step 2: Complete Product Details

**Product Information Section:**

| Field | Required | Guidance |
|-------|----------|----------|
| Product Name | Yes | Concise, business-friendly (50 chars max) |
| Product ID | Auto-generated | System identifier (immutable) |
| Category | Yes | Pick from predefined (Finance, Sales, Operations, etc.) |
| Short Description | Yes | One-liner explaining value (100 chars max) |
| Long Description | Yes | Detailed explanation of contents (500 chars) |
| Owner Name | Yes | Name of data owner/steward |
| Owner Email | Yes | Contact for access requests |
| Support Email | Yes | Technical support contact |

**Example Listing:**

```
Product Name: Retail Sales Transactions
Short Description: Daily transaction-level sales across 5 major retailers
Long Description: Comprehensive view of retail transaction activity including
  order details, item quantities, pricing, and temporal attributes. Enables
  analysis of sales patterns, product performance, customer behavior, and
  regional trends. Updated daily with 12-month rolling window.
Category: Sales & Marketing
Owner: Sarah Johnson (sarah.johnson@company.com)
Support: data.support@company.com
```

### Step 3: Define Data Source

**Selection Options:**
- Tables (Raw data tables in your space)
- Views (Logical views, recommended)
- Replicated Objects (Data from integrated systems)
- Materialized Views (Pre-calculated/optimized data)

**Selection Criteria:**
- Use Views to enable secure column filtering
- Use Materialized Views for large frequently-accessed datasets
- Avoid exposing raw tables directly (limit consumer access)
- Select only necessary columns (principle of least privilege)

### Step 4: Configure Visibility and Sharing

**Visibility Options:**

| Setting | Scope | Best For |
|---------|-------|----------|
| **Private** | Only explicitly approved consumers | Proprietary data, partners, pilot |
| **Internal Only** | All employees within organization | General internal data sharing |
| **Public** | Visible to all Datasphere tenants | Open industry data, benchmarks |

**Recommendation:**
- Start with Private (explicit approval control)
- Move to Internal Only after stabilization
- Publish to Public only after extensive validation

### Step 5: Set Initial Access Control

**Access Control Mechanisms:**

```
1. Visibility (can user see the listing?)
   → Private: Explicit allow list
   → Internal: All internal users
   → Public: All users

2. Access Request (can user request access?)
   → Manual Approval: You review requests
   → Auto-Approval: Immediate access
   → Restricted: No requests accepted

3. Consumer Context (data consumer isolation)
   → Shared Context: Shared with other consumers
   → Private Context: Isolated per consumer
```

**Recommended Settings for Pilot:**
```
Visibility: Private
Access Request: Manual Approval (review each consumer)
Consumer Context: Private Context (isolate early)
```

## Writing Effective Product Descriptions

### Compelling Value Proposition

**Structure: Problem → Solution → Benefit**

```
WEAK:
"Sales data from our company"

STRONG:
"Gain competitive insight into retail sales patterns across 5 major markets.
Analyze product performance, customer spending trends, and seasonal demand
to optimize inventory and pricing strategies. Updated daily with 2 years
of historical transaction detail enabling time-series analysis and
forecasting model development."
```

### Key Information to Include

**What the data contains:**
- Specific data elements (transactions, products, customers)
- Time period covered (last 12 months, 5-year history)
- Geographic scope (global, regions, countries)
- Industry/segment coverage

**How to use it:**
- Top 3-5 common analytical use cases
- Example questions it can answer
- Recommended analysis approaches

**Who should use it:**
- Target consumer roles (analyst, data scientist, business intelligence)
- Industry segments with most value
- Business functions (sales, marketing, operations)

**Refresh and currency:**
- Update frequency (daily, weekly, monthly)
- Data lag (same-day reporting, 1-day lag)
- Historical period available

### Example Product Descriptions

**Customer Analytics Data Product:**

```
TITLE: Customer Master & Behavioral Analytics

DATA INCLUDED:
• Customer demographics (50M customers, 200+ attributes)
• Purchase history (transactions last 3 years)
• Online engagement metrics (website clicks, session data)
• Customer lifetime value calculations
• Churn risk scores

ANALYTICAL USE CASES:
1. Customer segmentation and targeting for marketing campaigns
2. Lifetime value prediction for pricing/acquisition optimization
3. Churn risk identification for retention programs
4. Product affinity analysis for cross-sell recommendations
5. Geographic expansion opportunity assessment

REFRESH FREQUENCY: Daily at 6am UTC
HISTORICAL DEPTH: 3 years rolling window
DATA QUALITY: 99.8% completeness, deduplicated, validated

TARGET AUDIENCE: Marketing teams, customer analytics, product managers

KNOWN LIMITATIONS:
• Online data excludes mobile app interactions (web-only)
• Excludes B2B customers (B2C retail only)
• Regional data available for 8 primary markets only
```

## Defining License Terms and Access Policies

### License Term Options

**Free Access:**
```
License Type: Community/Open Access
Cost: $0
Best For: Internal sharing, ecosystem growth, public datasets
Terms:
  - Non-exclusive access
  - Non-commercial use (internal only)
  - No warranty or support guarantee
  - Data provided as-is
```

**Subscription-Based:**
```
License Type: Monthly Subscription
Cost: $500-2,000/month (depends on data volume)
Best For: Premium proprietary data, commercial partners
Terms:
  - Exclusive access (single consumer)
  - Commercial use rights
  - Monthly refresh updates
  - Email support included
  - 30-day cancellation notice required
```

**Pay-Per-Query:**
```
License Type: Consumption-Based
Cost: $0.10-1.00 per GB queried
Best For: Large infrequent consumers, ad-hoc analysis
Terms:
  - Pay only for actual usage
  - Queries tracked and billed monthly
  - No minimum commitment
  - Real-time access control
```

### Access Control Patterns

**Pattern 1: Column-Level Security**

Expose different columns to different consumer types:

```
PARTNER A (Reseller):
  - product_id, product_name, category
  - quantity, revenue
  - transaction_date
  HIDE: unit_price, customer_id, cost_price

PARTNER B (Investor):
  - product_category, region
  - total_revenue, total_quantity
  - transaction_date
  HIDE: customer data, pricing details, individual transactions

INTERNAL SALES:
  - All columns including unit_price and cost_price
```

**Implementation in Datasphere:**
```sql
-- Create consumer-specific views
CREATE VIEW product_sales_for_resellers AS
SELECT transaction_id, product_id, product_name, category,
       quantity, revenue, transaction_date
FROM product_sales_for_sharing
WHERE authorized_partner = 'PARTNER_A';

CREATE VIEW product_sales_for_investors AS
SELECT product_category, region,
       SUM(revenue) as total_revenue, SUM(quantity) as total_quantity,
       transaction_date
FROM product_sales_for_sharing
GROUP BY product_category, region, transaction_date;
```

**Pattern 2: Row-Level Security (RLS)**

Restrict data visibility based on consumer attributes:

```
SALES REGION (APAC):
  - Access to APAC transactions only
  WHERE region IN ('Australia', 'Japan', 'Singapore', ...)

CUSTOMER (Small Retailer):
  - Access to own transactions only
  WHERE customer_id = AUTHENTICATED_CUSTOMER_ID

DISTRIBUTOR (Multi-region):
  - Access to 3 assigned regions only
  WHERE region IN ('EMEA', 'LATAM', 'APAC')
```

**Pattern 3: Time-Based Access**

Control which time periods consumers can access:

```
TIER: BASIC
  - Last 12 months only
  WHERE transaction_date >= DATEADD(YEAR, -1, CURRENT_DATE)

TIER: PREMIUM
  - Last 5 years
  WHERE transaction_date >= DATEADD(YEAR, -5, CURRENT_DATE)

TIER: ARCHIVE
  - All historical (7+ years)
  - No time restriction
```

### Terms and Conditions Template

```
DATA PRODUCT LICENSE AGREEMENT

1. GRANT OF LICENSE
   Provider grants Licensee non-exclusive right to access and use
   the Data Product for purposes outlined in this Agreement.

2. USAGE RESTRICTIONS
   Licensee agrees to:
   - Use Data Product only for authorized purposes
   - Not share Data with third parties without written consent
   - Not reverse-engineer or attempt to identify individuals
   - Maintain data confidentiality and security
   - Not re-distribute or re-sell Data

3. INTELLECTUAL PROPERTY
   Provider retains all intellectual property rights in Data Product.
   Licensee receives only limited usage rights under this Agreement.

4. DATA QUALITY & DISCLAIMERS
   Provider provides Data "AS-IS" without warranties:
   - Regarding accuracy or completeness
   - Of fitness for specific purposes
   - Against infringement or third-party claims

5. DATA REFRESH & UPDATES
   Data Product updated [daily/weekly/monthly] at [time] UTC.
   Provider not responsible for delays due to source system outages.

6. PAYMENT TERMS
   License Fee: [description and amount]
   Payment Due: [frequency and method]
   Late Payment: [interest rate and consequences]

7. TERMINATION
   Either party may terminate with [30] days written notice.
   Upon termination, Licensee must cease all use immediately.

8. CONFIDENTIALITY
   Licensee treats Data as confidential and not as public information.

9. LIMITATION OF LIABILITY
   Provider's total liability limited to fees paid in prior 12 months.
   Provider not liable for indirect, consequential, or lost profits.

10. GOVERNING LAW
    This Agreement governed by laws of [jurisdiction].
```

## Visibility Settings: Public vs Private Contexts

### Context Model

**Private Context:**
- Isolated data environment per consumer
- Consumer cannot see other consumers' data
- Recommended for sensitive data sharing
- Higher operational overhead

**Shared Context:**
- Multiple authorized consumers in shared environment
- Reduces operational complexity
- Lower cost for provider
- Appropriate for non-sensitive, aggregate data

### Visibility Configuration

**Private Context Setup:**
```
1. Create Data Product listing
2. Set Visibility: Private
3. Set Access: Manual Approval only
4. For each approved consumer:
   a. Create consumer-specific context
   b. Assign data access policies
   c. Configure column/row-level security
   d. Notify consumer of access provisioning
5. Monitor usage per consumer
```

**Shared Context Setup:**
```
1. Create Data Product listing
2. Set Visibility: Private or Internal
3. Set Access: Auto-Approval (if homogeneous consumers)
4. Apply uniform security policies to all consumers
5. Monitor aggregate usage
```

## Consumer Perspective: Discovering and Requesting Access

### How Consumers Find Your Data Products

**Discovery Methods:**

1. **Data Marketplace Browse:**
   ```
   Datasphere → Data Sharing → Data Marketplace
   → Browse by Category (Sales, Marketing, Operations)
   → Search by keyword (sales, customer, revenue)
   ```

2. **Search Functionality:**
   ```
   Search: "product sales"
   Results: All public/accessible products with keyword match
   Sort By: Relevance, Recently Updated, Rating
   ```

3. **Provider Recommendations:**
   ```
   Follow favorite data providers
   → Receive notifications of new products
   → See curated product collections
   ```

### Consumer Access Request Process

**Step 1: Consumer Discovers Your Product**
- Finds listing in marketplace
- Reviews description and metadata
- Checks licensing terms

**Step 2: Consumer Submits Access Request**
```
Click: "Request Access" button
Form:
  - Use Case: Describes intended analysis/purpose
  - Expected Volume: How much data access needed
  - Timeline: When access needed
  - Company: Consumer organization
  - Team: Consumer department/team
```

**Step 3: You Review and Approve**
```
Data Sharing Cockpit → Pending Requests
Review:
  - Consumer organization and legitimacy
  - Use case alignment with your product intent
  - Any risk concerns or conflicts
Actions:
  - Approve: Grant access immediately
  - Conditional Approve: Grant with restrictions (e.g., time-limited)
  - Request Info: Ask clarifying questions
  - Deny: Reject request with explanation
```

**Step 4: Consumer Receives Access**
- Automated notification upon approval
- Access instructions and documentation
- Connection details if applicable
- Support contact information

## Data Marketplace: Publishing and Managing Subscribers

### Publishing to Marketplace

**Readiness Checklist Before Publishing:**
- Data quality validated (completeness, accuracy, timeliness)
- Metadata documented (business context, lineage, limitations)
- Security policies configured (column/row level)
- License terms finalized and reviewed by legal
- Support team trained on handling consumer questions
- SLA for refresh/updates defined
- Monitoring and alerting configured

**Publishing Steps:**

```
1. Data Sharing Cockpit → My Products → [Product Name]
2. Click "Publish to Marketplace"
3. Confirm:
   - Visibility: Public (marketplace listing)
   - Access Request: Manual or Auto-Approval
   - Pricing: Free, Subscription, or Pay-Per-Query
4. Add marketplace-specific metadata:
   - Product tags (sales, customer, financial, etc.)
   - Audience/industry tags
   - Use case examples
   - Rating and reviews enabled: Yes/No
5. Review marketplace preview
6. Confirm and publish
```

**Marketplace Publishing Considerations:**
- Product becomes searchable to all Datasphere tenants
- Enable consumer reviews/ratings
- Respond to consumer questions publicly
- Monitor marketplace analytics for interest trends
- Consider SEO in product name and tags

### Managing Subscribers

**Subscriber Dashboard:**

```
View → Subscriptions

DISPLAY:
Consumer Company | Subscription Date | Status | Usage | Actions
─────────────────────────────────────────────────────────────────
Acme Corp       | 2024-01-15       | Active | High  | View Details
Beta Partners   | 2024-01-10       | Active | Low   | View Details
XYZ Industries  | 2024-01-05       | Active | Med   | Pause/Terminate
ABC Ventures    | 2023-12-20       | Inactive| None | Reactivate
```

**Subscriber Actions:**

| Action | Use Case | Impact |
|--------|----------|--------|
| View Details | Understand consumer usage patterns | Informational |
| Send Update | Notify of product changes/improvements | Engagement |
| Pause Access | Temporary suspension (technical issues) | Consumer blocked |
| Terminate | End subscription (license expired) | Consumer blocked |
| Adjust Limits | Change data volume/row limits | Access modified |

**Managing Inactive Subscribers:**

```
STEP 1: Monitor Inactivity
  - Alert after 30 days no queries
  - Alert after 90 days no usage

STEP 2: Outreach (if value-add)
  - Email consumer explaining new features
  - Offer training/support for adoption
  - Explore unmet needs

STEP 3: Decision
  - If consumer engaged: Continue service
  - If no response after outreach: Consider termination
  - Negotiate reduced pricing if volume concerns

STEP 4: Communicate Changes
  - Notify consumer of any adjustments
  - Update SLA/terms if applicable
```

## Data Access Control Considerations

### Sensitive Data Handling

**Identify Sensitive Elements:**
- Personal data (customer names, emails, IDs)
- Financial data (pricing, costs, revenue)
- Competitive information (market strategies)
- Proprietary methodologies

**Masking Strategies:**

| Data Type | Masking Approach | Example |
|-----------|-----------------|---------|
| **Customer Names** | Redact or hash | John Smith → CUST_12345 |
| **Email Addresses** | Partial redact | john@example.com → j***@example.com |
| **Phone Numbers** | Partial redact | 555-123-4567 → 555-***-**** |
| **Cost Data** | Hash or remove | $1.50 → [REDACTED] |
| **Revenue** | Aggregate only | Sum/Avg, not individual |
| **Personal IDs** | Hash with salt | 123-45-6789 → h7e2a9k4 |

**Column-Level Security Implementation:**

```sql
-- Define sensitivity levels
ALTER TABLE product_sales_for_sharing
SET COLUMN SECURITY
  (customer_id = 'HIGH', unit_price = 'MEDIUM', total_amount = 'MEDIUM');

-- Create role-specific views
CREATE VIEW sales_by_partner (customer_id = 'MASKED', unit_price = 'REMOVED')
AS SELECT ... FROM product_sales_for_sharing;
```

### Privacy Compliance

**Regulatory Considerations:**

| Regulation | Key Requirement | Implementation |
|------------|-----------------|-----------------|
| **GDPR** | Right to be forgotten | Support customer deletion requests |
| **CCPA** | Consumer data rights | Allow consumers to request/opt-out |
| **PII Rules** | Non-identification of individuals | Hash/mask personal identifiers |
| **Data Residency** | Geographic restrictions | Ensure data stays in authorized regions |

**Privacy Impact Assessment:**

```
BEFORE PUBLISHING:

Question 1: Does the data contain personally identifiable information?
  → Confirm PII is masked/redacted

Question 2: Can individuals be identified through data inference?
  → Test combinations of attributes
  → Ensure k-anonymity > 5 (minimum 5 individuals per cell)

Question 3: Is there compliance requirement for data geography?
  → Confirm data not crossing borders
  → Document jurisdiction alignment

Question 4: What is the data retention requirement?
  → Establish deletion schedule
  → Configure automated purge policies
```

## Quality Requirements for Publishable Data Products

### Quality Dimensions Framework

**COMPLETENESS (100% Rule)**
- Expected: No null values in key columns
- Validation: Row count matches expected daily volume ± 5%
- Example: "Daily customer updates expected 500K, actual 485K-515K"

**ACCURACY (Known Validation)**
- Expected: Spot-check sample matches source ± 0.5%
- Validation: Totals align with ERP reporting
- Example: "Monthly revenue reconciled to GL within 0.1%"

**CONSISTENCY (Relational Integrity)**
- Expected: All foreign keys resolve to valid parent records
- Validation: No orphaned records
- Example: "Every product_id in sales matches product_master"

**TIMELINESS (SLA-Based)**
- Expected: Data refreshed daily by 6am UTC
- Validation: 99.5% on-time delivery tracked
- Example: "30-day rolling SLA: 150/151 refreshes on-time = 99.3%"

**CONFORMITY (Schema Validation)**
- Expected: All columns present, correct data types
- Validation: Schema unchanged without notice
- Example: "Revenue always DECIMAL(10,2), never NULL, always > 0"

### Quality Scorecard

**Calculate Quality Score:**
```
Quality Score = (Completeness + Accuracy + Consistency + Timeliness + Conformity) / 5

SCORING:
  95-100% = Production Ready
  85-95%  = Acceptable (monitor closely)
  75-85%  = Conditional (fix issues before publishing)
  < 75%   = Not Ready (rework required)
```

**Example Quality Report:**

```
PRODUCT: Retail Sales Transactions
REPORTING PERIOD: January 2024

COMPLETENESS:
  Target: 100% non-null on transaction_id, customer_id, amount
  Result: 99.8% (5 orphaned records out of 2.5M)
  Status: PASS

ACCURACY:
  Target: Revenue within 0.5% of ERP GL
  Result: GL reconciliation: GL $50.2M vs Data $50.1M = 0.2% variance
  Status: PASS

CONSISTENCY:
  Target: All customer_ids in sales found in customer_master
  Result: 99.97% matching (750 orphaned sales found, corrected)
  Status: PASS WITH CORRECTION

TIMELINESS:
  Target: Daily refresh by 6am UTC, 99%+ on-time
  Result: 31/31 refreshes on-time in January = 100%
  Status: PASS

CONFORMITY:
  Target: All columns present, correct types, no schema drift
  Result: All 15 columns present, types correct, no changes detected
  Status: PASS

OVERALL SCORE: (99.8 + 100 + 99.97 + 100 + 100) / 5 = 99.95%
VERDICT: PRODUCTION READY ✓
```

## Using MCP Tools for Data Product Management

### browse_marketplace
Discover and analyze market opportunities:
```
browse_marketplace(category="Sales", sort_by="rating", limit=20)
```
Returns: Top products in category, enabling you to understand competitive positioning

### search_catalog
Find related data products and dependencies:
```
search_catalog(keyword="customer", consumer_type="public")
```
Returns: All products matching search, helping identify ecosystem opportunities

### get_asset_details
Retrieve complete product metadata:
```
get_asset_details(asset_id="retail_sales_transactions_001")
```
Returns: Full product definition, schemas, lineage, security policies

### get_space_info
Understand data space structure and capacity:
```
get_space_info(space_name="sales_analytics")
```
Returns: Space configuration, objects, sizing, security posture

## Data Product Publishing Workflow

1. **Evaluate**: Assess candidate datasets (business value, quality, compliance)
2. **Prepare**: Create views, validate metadata, ensure quality
3. **List**: Create product listing with compelling description
4. **License**: Define terms, access policies, pricing
5. **Publish**: Make product discoverable to target consumers
6. **Manage**: Review requests, approve consumers, monitor subscriptions
7. **Support**: Answer questions, resolve issues, handle updates
8. **Monitor**: Track usage, quality metrics, customer satisfaction
9. **Iterate**: Gather feedback, make improvements, version updates
10. **Retire**: Deprecate products, communicate sunset dates

## Best Practices

- Start with high-quality, high-value data (not everything is a data product)
- Create consumer-specific views (avoid direct table exposure)
- Document thoroughly including known limitations
- Test access controls with representative consumers before publishing
- Implement automated quality monitoring
- Respond to access requests within 24-48 hours
- Establish clear support SLA for subscribers
- Monitor marketplace analytics to understand demand
- Regularly collect consumer feedback and improve products
- Version data products and communicate changes
- Plan data retention and archival strategy upfront
- Consider privacy and compliance implications early

## What's New (2026.05)

- **Optimized Data Product Uninstallation**: Uninstalling data products is now significantly faster. All related artifacts — including replication flows — are automatically removed during uninstallation. Previously, orphaned replication flows could remain after uninstalling a data product, requiring manual cleanup.
