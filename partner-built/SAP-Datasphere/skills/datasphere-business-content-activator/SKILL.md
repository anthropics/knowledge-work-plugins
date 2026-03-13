---
name: "SAP Datasphere Business Content Activator"
description: "Activate pre-built SAP Business Content packages in Datasphere! Use this skill when you need to deploy industry-specific data models, manage content updates, handle prerequisites (Time Dimension, Currency Conversion), and align content with LSA++ layered architecture. Essential for rapid analytics implementation, reducing customization, and accelerating time-to-value in retail, automotive, finance, utilities, and other verticals."
---

# SAP Datasphere Business Content Activator

## What is Business Content?

SAP Business Content is a collection of pre-built, production-ready data models, analytical views, and data flows designed for specific industries and business domains. Rather than building your entire analytics solution from scratch, Business Content gives you:

- **Pre-modeled Data Objects**: Tables, views, and dimensions aligned to industry best practices
- **Time and Currency Handling**: Built-in temporal and FX conversion logic
- **Industry-Specific Analytical Hierarchies**: Organized by sales channel, product lines, geographic regions, etc.
- **Data Flow Templates**: Extract-Transform-Load (ETL) patterns for common data integration scenarios
- **Reporting Views**: Pre-built analytics views ready for dashboards and reports
- **Documentation and Metadata**: Embedded business glossaries and lineage information

### Key Benefits

| Benefit | Impact |
|---------|--------|
| Time-to-Value | Deploy analytics in weeks vs. months |
| Best Practices | Industry-standard data modeling patterns |
| Reduced Customization | 70-80% of requirements covered by content |
| Consistency | Standardized KPIs across the organization |
| Maintainability | SAP updates content; you benefit from innovations |

---

## Content Network Overview

The SAP Datasphere Content Network is where you browse, preview, and select Business Content packages for activation.

### Accessing the Content Network

1. **Navigate to Content Network**:
   - In Datasphere, go to **Business Content > Content Network**
   - Or visit: `https://your-datasphere-instance/business-content/network`

2. **Search and Filter**:
   - Filter by **Industry** (Automotive, Utilities, Retail, Finance, Manufacturing, etc.)
   - Filter by **Domain** (Sales, Finance, Supply Chain, Human Resources, etc.)
   - Filter by **Data Source** (SAP S/4HANA, Salesforce, Workday, etc.)
   - Search by **Keyword** (e.g., "revenue analysis", "inventory management")

3. **Preview Package**:
   - View included data models and views
   - Check dependencies and prerequisites
   - Review object count and complexity
   - Read implementation guide

### Content Package Metadata

Each package displays:
- **Version**: Semantic versioning (e.g., 1.2.3) with release notes
- **Objects Count**: Number of tables, views, and flows included
- **Dependencies**: Packages this content requires
- **Prerequisites**: Time Dimension, Currency Conversion, other setup needs
- **Industries**: Which verticals this package serves
- **Last Updated**: SAP's latest modification date

---

## Pre-Activation Prerequisites Checklist

Before activating any Business Content, ensure these foundational elements are in place.

### Time Dimension Tables

Time Dimension is the backbone of temporal analytics. Business Content heavily relies on it for:
- Year-to-Date (YTD) analysis
- Period-over-Period (POP) comparisons
- Fiscal vs. calendar calendars
- Holidays and working day calculations

#### Check If Time Dimension Exists

```
In Datasphere:
1. Go to Business Content > Administration > Prerequisites
2. Look for "Time Dimension" table
3. Check: Status = "Populated" (with date range)
```

#### Populate Time Dimension (If Empty)

If the Time Dimension table exists but is empty:

1. **Download Time Dimension Data File**:
   - Go to **Administration > Time Dimension**
   - Click **Generate Data File** for your date range
   - Select fiscal period definition (Gregorian or custom)
   - Generate CSV with dates, quarters, years, etc.

2. **Load Data**:
   - Import CSV via **Data Integration > New Data Flow**
   - Select target: **Time Dimension** table
   - Map columns: date → DATE, year → YEAR, quarter → QUARTER, etc.
   - Execute load

3. **Verify Population**:
   - Query should return records for all periods:
     ```sql
     SELECT MIN(DATE), MAX(DATE), COUNT(*) FROM TIME_DIMENSION
     ```

#### Time Dimension Example Structure

| DATE | YEAR | QUARTER | MONTH | WEEK | DAY_OF_WEEK | FISCAL_YEAR | FISCAL_QUARTER | IS_HOLIDAY |
|------|------|---------|-------|------|-------------|-------------|-----------------|-----------|
| 2024-01-01 | 2024 | Q1 | 1 | 1 | Monday | 2024 | Q1 | true |
| 2024-01-02 | 2024 | Q1 | 1 | 1 | Tuesday | 2024 | Q1 | false |

### Currency Conversion Views (TCUR*)

Currency Conversion enables multi-currency reporting and harmonization. Business Content uses these views to convert transactional amounts to reporting currency.

#### Identify Required Currency Conversion Views

Business Content packages typically require:
- **TCURR** — Exchange rates master table
- **TCURN** — Currency conversion rules and settings
- **TCURV** — Currency conversion view (calculated)

#### Check If Currency Conversion is Available

```
In Datasphere:
1. Go to Business Content > Administration > Prerequisites
2. Look for "Currency Conversion" (TCUR*)
3. Check: Status = "Available" (with rates populated)
```

#### Set Up Currency Conversion (If Missing)

1. **Source Currency Master Data**:
   - **Option A**: Load from SAP S/4HANA connection
     - Table: TCURR (exchange rates)
     - Create data flow: SAP → Datasphere
   - **Option B**: Load from external system
     - Format: SOURCE_CURRENCY, TARGET_CURRENCY, RATE, VALID_FROM, VALID_TO
     - Example: USD → EUR, 0.92, 2024-01-01, 2024-12-31

2. **Create Currency Conversion View**:
   - Use Datasphere's **Currency Conversion Calculation View** template
   - Configure source as TCURR table
   - Specify conversion hierarchy (usually to reporting currency)

3. **Verify Exchange Rates**:
   - Query should return rates for all currency pairs:
     ```sql
     SELECT SOURCE_CURRENCY, TARGET_CURRENCY, RATE FROM TCURV
     WHERE VALID_FROM <= TODAY() AND VALID_TO >= TODAY()
     ```

### Unit of Measure Tables

Business Content often includes measurements (quantity, weight, volume). Unit of Measure (UOM) tables normalize these:

#### Check UOM Availability

```
In Datasphere:
1. Go to Business Content > Administration > Prerequisites
2. Look for "Unit of Measure" table
3. Check: Status = "Available"
```

#### UOM Table Structure

| UNIT_CODE | UNIT_NAME | CATEGORY | CONVERSION_FACTOR |
|-----------|-----------|----------|------------------|
| KG | Kilogram | Weight | 1.0 |
| LB | Pound | Weight | 0.453592 |
| MTR | Meter | Length | 1.0 |
| KM | Kilometer | Length | 1000.0 |

#### Populate UOM Table

```
Load standard UOM data:
1. Create data flow from SAP system → UOM table
2. Or upload CSV with standard UOM master data
3. Verify all conversion factors are populated
```

### Other Shared Dependencies

Depending on the Business Content package, also verify:

| Dependency | Purpose | Check |
|------------|---------|-------|
| Organizational Hierarchy | Drill-down by division, region, department | Table populated? |
| Customer Master | Customer dimensions and attributes | Source system connectivity? |
| Product Master | Product hierarchies and classifications | UPC/SKU mappings available? |
| General Ledger Accounts | Chart of Accounts for financial analysis | GL account mapping available? |

---

## Content Activation Workflow (Step-by-Step)

### Step 1: Select Business Content Package

1. Navigate to **Business Content > Content Network**
2. Browse or search for desired package
   - Example: "Sales Cloud Analytics" for retail
3. Click **Details** to review:
   - Objects included
   - Prerequisites
   - Industry applicability
   - Implementation time estimate

### Step 2: Review Included Objects

Packages typically include:

**Data Models** (tables for raw data ingestion):
- Sales orders, line items, fulfillment status
- Customer master, product master
- Daily snapshots for analytics

**Analytical Views** (pre-aggregated analytics):
- Revenue by product line (yearly, monthly)
- Customer acquisition and retention metrics
- Margin analysis by region

**Data Flows** (ETL templates):
- Extract data from SAP S/4HANA
- Transform and load into analytical tables
- Schedule frequency: daily, weekly, monthly

### Step 3: Choose Target Space

Decide where content will be activated:

**Option A: Single Space** (recommended for small teams)
- Create all content in one space (e.g., ANALYTICS)
- Simpler governance and discovery
- All users in space access all content

**Option B: Separate Spaces by Layer** (recommended for large orgs using LSA++)
- **Inbound Layer Space**: Raw data tables
- **Harmonization Layer Space**: Data cleaning and transformation
- **Reporting Layer Space**: Analytical views for end users
- Enables fine-grained access control and performance isolation

### Step 4: Handle Conflicts with Existing Objects

If objects already exist in the target space:

| Scenario | Action |
|----------|--------|
| First activation | Proceed (no conflicts) |
| Re-activating same version | Skip (use existing objects) |
| Activating new version | Choose: **Overwrite** or **Keep** |
| Custom modifications exist | Choose: **Keep** (preserve changes) |

**Conflict Resolution Dialog**:
```
Existing Object: SALES_ORDERS
┌─────────────────────────────────┐
│ Overwrite (replace with new)    │
│ Keep (preserve customizations)  │
│ Rename new (add suffix _v2)     │
└─────────────────────────────────┘
```

### Step 5: Activate Package

1. Click **Activate** on the content package
2. Select target space(s)
3. Choose conflict resolution for each object
4. Review activation summary
5. Confirm activation

**Activation Progress**:
```
Creating objects: [████████░░] 80% (40/50 objects)
Estimated time remaining: 2 minutes
```

After activation, content objects appear in the target space.

---

## LSA++ (Layered Scalable Architecture) Alignment

LSA++ is SAP's recommended architecture for enterprise data warehouses. Business Content is designed to fit seamlessly into LSA++ layers.

### Understanding LSA++ Layers

```
┌─────────────────────────────────────────────────────────┐
│ REPORTING LAYER (L3)                                     │
│ Pre-aggregated analytics views for dashboards & reports │
│ Example: Revenue_Analysis, Customer_Metrics            │
└─────────────────────────────────────────────────────────┘
                           ↑
┌─────────────────────────────────────────────────────────┐
│ HARMONIZATION LAYER (L2)                                │
│ Cleansed, standardized, unified data model             │
│ Example: Sales_Order_Harmonized, Customer_Unified      │
└─────────────────────────────────────────────────────────┘
                           ↑
┌─────────────────────────────────────────────────────────┐
│ PROPAGATION LAYER (L1)                                  │
│ Document-level data, minimal transformation             │
│ Example: Sales_Order_Raw, Customer_Raw                 │
└─────────────────────────────────────────────────────────┘
                           ↑
┌─────────────────────────────────────────────────────────┐
│ INBOUND LAYER (L0)                                       │
│ Raw data extracted from source systems (as-is)         │
│ Example: SD_SALESDOCUMENT, MD_CUSTOMER                 │
└─────────────────────────────────────────────────────────┘
```

### How Business Content Maps to LSA++ Layers

**Inbound Layer Objects** (L0 - Source extraction):
- Tables with source system structure (e.g., SALESDOCUMENT copied from S/4HANA)
- Staging tables for daily delta loads
- Minimal transformation, full detail

**Propagation Layer Objects** (L1 - Document level):
- Document-level tables with line item detail
- Business fields added (e.g., sales document type descriptions)
- Ready for propagation to harmonization

**Harmonization Layer Objects** (L2 - Unified):
- Cleansed, deduplicated, standardized data
- Cross-source consolidation (combining from multiple SAP modules)
- Rich master data (customer, product with attributes)
- Time-dimensioned snapshots for historical analysis

**Reporting Layer Objects** (L3 - Analytics):
- Pre-aggregated cubes and analytical views
- Optimized for dashboard performance
- Business user language (e.g., "Revenue", "Gross Margin")
- Calculated fields and metrics

### Best Practices for Layering Imported Content

**1. Separate Spaces by Layer** (recommended):

```
Datasphere Spaces Structure:
├── INBOUND_LAYER (Space)
│   └── Raw data tables from source systems
│       └── Connections to SAP S/4HANA, Salesforce, etc.
├── HARMONIZATION_LAYER (Space)
│   └── Cleansed and standardized data
│       └── Data flows reading from INBOUND_LAYER
├── REPORTING_LAYER (Space)
│   └── Analytics views and dashboards
│       └── Analytical views reading from HARMONIZATION_LAYER
└── MASTERED_DATA (Space)
    └── Reference data (Customer, Product, Organization)
        └── Reusable by all layers
```

**Access Control by Layer**:
- **Inbound**: Only data engineers have access
- **Harmonization**: Data engineers + data architects
- **Reporting**: Business users (view only)
- **Mastered Data**: Read access for all layers

**2. Organize Within a Space** (alternative for smaller teams):

```
Single Analytics Space with layering via naming:
├── L0_SALESDOCUMENT (Inbound)
├── L0_CUSTOMER (Inbound)
├── L1_SALESDOCUMENT_PROPAGATED (Propagation)
├── L2_SALESDOCUMENT_HARMONIZED (Harmonization)
├── L3_REVENUE_ANALYSIS (Reporting)
└── L3_CUSTOMER_METRICS (Reporting)
```

**3. Isolate Inbound from Harmonization**

Critical principle: Never have data flows directly from source system to Reporting Layer.

**Wrong** (anti-pattern):
```
Source System → Reporting View
(No data quality checks)
```

**Correct** (LSA++ compliant):
```
Source System → Inbound Tables → Harmonization Layer → Reporting View
                (staging)      (cleansing)          (optimization)
```

---

## Managing Content Updates

SAP regularly publishes new versions of Business Content. Decide whether to adopt updates.

### Understanding Update Types

**Patch Update** (e.g., 1.0.0 → 1.0.1):
- Bug fixes and data corrections
- No structural changes
- Recommended to apply: **Always**

**Minor Update** (e.g., 1.0 → 1.1):
- New fields, additional views
- Backward compatible
- Recommended to apply: **Usually** (assess customizations)

**Major Update** (e.g., 1.0 → 2.0):
- Significant restructuring, deprecated objects
- May break customizations
- Recommended to apply: **Plan carefully**

### Update Decision Matrix

| Scenario | Overwrite | Keep | Notes |
|----------|-----------|------|-------|
| Patch update, no customizations | **Overwrite** | | Apply immediately |
| Patch update, minor customizations | **Keep** → Merge | | Manual merge after update available |
| Minor update, no customizations | **Overwrite** | | Review new fields before updating |
| Minor update, significant customizations | **Keep** | | Evaluate if new features justify re-work |
| Major update, critical customizations | **Keep** | | Plan migration project separately |
| Production system, no customizations | **Overwrite** | | Update after testing in non-prod |
| Development space, any customizations | **Overwrite** | | Easier to re-customize than maintain drift |

### Update Workflow

**Step 1: Check for Updates**

```
In Datasphere:
1. Go to Business Content > Manage Content
2. Look for "Update Available" badges
3. Click to view release notes and changelog
```

**Step 2: Impact Analysis**

```
For each outdated object:
1. Check if customizations exist (custom fields, flows)
2. Check if dependent views use this object
3. Test update in non-production space first
```

**Step 3: Stage Update in Non-Prod**

```
1. Clone prod space to test space (if using separate spaces)
2. Or create separate test package version
3. Activate updated package version in test space
4. Run regression tests (SQL queries, dashboards)
5. Validate calculated fields and aggregations
```

**Step 4: Decide: Overwrite or Keep**

If testing passes and no customizations exist:
```
Click Overwrite → All objects replaced with new version
```

If customizations are critical or testing failed:
```
Click Keep → Old version retained, new version labeled _v2
```

After keeping old version:
- Manually migrate customizations to new version
- Gradually redirect data flows to _v2 objects
- Deprecate old version once migration complete

**Step 5: Update Production**

```
After non-prod validation:
1. Activate update in production space
2. Monitor performance and error logs
3. Validate dashboards and reports render correctly
4. Communicate update to business users
```

---

## Industry-Specific Content Packages

### Automotive Industry

**Package: Automotive Sales & Service Analytics**
- Objects: 45 tables, 28 views
- Domains: Sales, Service, Warranty, Spare Parts
- Key Measures: Vehicle sales by model, service revenue, parts availability
- Prerequisites: Time Dimension, Currency Conversion, Customer master
- Typical Activation Time: 4-6 weeks

**Package: Automotive Supply Chain**
- Objects: 62 tables, 35 views
- Domains: Procurement, Production Planning, Inventory, Logistics
- Key Measures: Supplier performance, production capacity, inventory turns
- Prerequisites: Time Dimension, Organization hierarchy, Product master
- Typical Activation Time: 8-10 weeks

### Retail Industry

**Package: Retail POS & Merchandise Analytics**
- Objects: 38 tables, 31 views
- Domains: Point of Sale, Merchandise Planning, Promotions
- Key Measures: Sales by product category, margin by location, promotion ROI
- Prerequisites: Time Dimension, Currency Conversion, Product hierarchy
- Typical Activation Time: 3-5 weeks

**Package: Retail Supply Chain**
- Objects: 55 tables, 40 views
- Domains: Distribution, Inventory, Replenishment
- Key Measures: Stock coverage, distribution effectiveness, shrinkage
- Prerequisites: Time Dimension, Organization hierarchy, Product master
- Typical Activation Time: 6-8 weeks

### Utilities Industry

**Package: Energy & Water Distribution**
- Objects: 41 tables, 29 views
- Domains: Grid operations, Customer billing, Asset management
- Key Measures: Energy consumption by segment, outage frequency, billing accruals
- Prerequisites: Time Dimension, Currency Conversion, Equipment master
- Typical Activation Time: 5-7 weeks

### Finance Industry

**Package: General Ledger & Financial Reporting**
- Objects: 34 tables, 26 views
- Domains: Accounting, Profitability, Consolidation
- Key Measures: Revenue recognition, expense analysis, intercompany consolidation
- Prerequisites: Time Dimension, GL account master, Cost center hierarchy
- Typical Activation Time: 4-6 weeks

**Package: Banking Risk & Compliance**
- Objects: 48 tables, 35 views
- Domains: Credit risk, Market risk, Regulatory reporting
- Key Measures: Risk-weighted assets, non-performing loans, regulatory ratios
- Prerequisites: Time Dimension, Product master, Risk classification master
- Typical Activation Time: 8-12 weeks

### Manufacturing

**Package: Production & Costing**
- Objects: 52 tables, 38 views
- Domains: Bill of Materials, Work orders, Job costing
- Key Measures: Cost per unit, throughput, variance analysis
- Prerequisites: Time Dimension, Product master, Cost center hierarchy
- Typical Activation Time: 7-9 weeks

---

## Customizing Activated Content

After activation, content is often tailored for organization-specific needs.

### Safe Customization Patterns

**Pattern 1: Add Calculated Fields** (Non-breaking)

```
Existing View: REVENUE_ANALYSIS
├── Base fields: Sales_Amount, Product, Customer
└── Add calculated fields:
    ├── Margin_Percent = Gross_Margin / Sales_Amount * 100
    ├── Days_to_Payment = Invoice_Date - Payment_Date
    └── Customer_Segment = (custom logic based on revenue)
```

**Pattern 2: Create Extension Views** (Recommended)

Instead of modifying existing views, create new views that extend them:

```
Business Content View: REVENUE_ANALYSIS (DON'T MODIFY)
↓
New Extension View: REVENUE_ANALYSIS_EXTENDED (your custom logic)
├── Extends: REVENUE_ANALYSIS
├── Adds: Additional dimensions and calculated fields
└── Data flows and dashboards consume _EXTENDED view
```

**Benefits**:
- Original view unmodified (survives future updates)
- Your customizations clearly separated
- Easier to merge future updates

**Pattern 3: Create Custom Dimensions**

Extend master data tables with organization-specific attributes:

```
Content View: CUSTOMER_MASTER (standard SAP fields)
├── Customer_ID, Name, Industry, Region (standard)
└── Add via custom fields:
    ├── Account_Manager (org-specific)
    ├── Customer_Segment_Custom (org-specific classification)
    ├── Contract_Status (org-specific)
```

### Unsafe Customization (Avoid)

**Anti-Pattern 1: Modify Content Objects Directly**

```
❌ DON'T DO THIS:
1. Edit view REVENUE_ANALYSIS (from content)
2. Add custom fields directly
3. Problem: Update overwrites customizations
```

**Anti-Pattern 2: Hard-code Values**

```
❌ DON'T DO THIS:
Sales_Amount WHERE Country = 'USA'
^ Hard-coded country filter breaks for other regions
```

**Better**:
```
✓ DO THIS:
Create parameterized view with country input
Let business users select country via filter
```

### Common Customizations

**1. Add Company-Specific Hierarchies**

```
Extend Organization hierarchy:
├── Region (from content)
└── Add: Sales Territory, Account Team (your custom)

Extended View: SALES_REVENUE_BY_TERRITORY
├── Base: REVENUE_ANALYSIS
└── Joined with: Your Territory_Master table
```

**2. Align Chart of Accounts**

```
GL Account mapping table (YOUR custom):
├── Content_GL_Account → Your_GL_Account
├── 400000 (Sales) → 4000 (Sales Revenue)
├── 410000 (Returns) → 4100 (Sales Returns)

Use mapping in data flow:
GL_Details → Map GL Account → Store in HARMONIZED table
```

**3. Add Company Fiscal Calendar**

```
If business uses non-Gregorian fiscal calendar:
1. Create custom fiscal calendar master
2. Extend Time Dimension joins with fiscal calendar
3. Reporting uses fiscal year / fiscal quarter
```

---

## Troubleshooting Failed Activations

### Common Activation Failures

| Error | Cause | Solution |
|-------|-------|----------|
| "Prerequisite not met: Time Dimension" | Time Dimension table empty | Populate Time Dimension with date data |
| "Space quota exceeded" | Not enough memory/disk | Increase space allocation or split across spaces |
| "Object name conflict" | Object exists, conflict resolution not specified | Choose Overwrite or Rename in conflict dialog |
| "Connection test failed" | Source system unreachable | Verify connection credentials and network |
| "Permission denied" | Insufficient space access | Ensure user has space_admin role |

### Activation Log Review

After failed activation, review logs:

```
In Datasphere:
1. Go to Business Content > Activation History
2. Find failed activation
3. Click View Logs
4. Search for ERROR lines
```

**Log Example**:
```
[2024-02-01 10:15:30] INFO: Activation started for package SALES_ANALYTICS v1.2
[2024-02-01 10:15:45] INFO: Creating objects...
[2024-02-01 10:16:02] ERROR: Failed to create object REVENUE_DAILY
[2024-02-01 10:16:02] ERROR: Reason: "Space SALES_ANALYTICS at capacity (1000 GB / 1000 GB)"
[2024-02-01 10:16:02] WARN: Rollback initiated. 12 objects created, 3 objects rolled back.
```

### Retry Failed Activation

After fixing the underlying issue:

```
1. Go to Business Content > Manage Content
2. Find the package with failed activation
3. Click Retry Activation
4. Review conflict resolution settings
5. Click Confirm
```

---

## Post-Activation Validation Checklist

After successful activation, verify everything is working:

### Data Verification

- [ ] Time Dimension table populated with correct date range
  ```sql
  SELECT MIN(DATE), MAX(DATE), COUNT(*) FROM TIME_DIMENSION
  ```

- [ ] Currency Conversion rates populated
  ```sql
  SELECT COUNT(*) FROM TCURV WHERE VALID_FROM <= TODAY()
  ```

- [ ] Master data tables have records
  ```sql
  SELECT TABLE_NAME, COUNT(*) FROM [ACTIVATED_OBJECTS] GROUP BY TABLE_NAME
  ```

- [ ] Data flow test load executed successfully
  - No error logs in data flow execution history
  - Row counts match expected volumes

### Analytical View Verification

- [ ] Key analytical views return data
  ```sql
  SELECT TOP 100 * FROM REVENUE_ANALYSIS
  -- Should return rows with expected columns
  ```

- [ ] Calculated fields compute without errors
  ```sql
  SELECT *, MARGIN_PERCENT FROM REVENUE_ANALYSIS
  -- No NULL or error values for MARGIN_PERCENT
  ```

- [ ] Aggregation views perform acceptably
  - Query execution time < 5 seconds
  - No memory errors in query trace

### Dashboard & Reporting

- [ ] Pre-built dashboards load without errors
- [ ] Charts render with expected data
- [ ] Drill-down by dimensions works
- [ ] Filter selections (date range, region) apply correctly

### Performance Baseline

- [ ] Document current query performance
  ```
  Create_Date Baseline:
  - REVENUE_ANALYSIS: 2.1 seconds
  - CUSTOMER_METRICS: 1.8 seconds
  - MARGIN_ANALYSIS: 3.2 seconds
  ```
- [ ] Monitor performance over 1-2 weeks
- [ ] Alert if degradation > 20%

### Access & Security

- [ ] Users can access content in appropriate spaces
- [ ] Row-level security rules apply (if configured)
- [ ] Audit logs track access to sensitive views

---

## Next Steps

1. **Identify Industry Packages**: Browse Content Network for your vertical
2. **Verify Prerequisites**: Ensure Time Dimension, Currency Conversion ready
3. **Plan LSA++ Layout**: Decide on space separation by layer
4. **Test in Non-Prod**: Activate in development space first
5. **Customize Thoughtfully**: Use extension views, not in-place modifications
6. **Monitor Post-Activation**: Validate data, performance, access
7. **Plan Updates**: Track new versions and plan upgrades quarterly

See **references/content-catalog.md** for complete prerequisite checklists, activation troubleshooting, industry-specific content listings, and post-activation validation templates.
