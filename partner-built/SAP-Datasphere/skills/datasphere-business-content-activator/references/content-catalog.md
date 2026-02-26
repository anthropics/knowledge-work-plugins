# SAP Datasphere Business Content: Complete Catalog & Reference

## Table of Contents
1. [Complete Prerequisite Checklist](#complete-prerequisite-checklist)
2. [Time Dimension Population Guide](#time-dimension-population-guide)
3. [Currency Conversion Setup Guide](#currency-conversion-setup-guide)
4. [LSA++ Layer Mapping Reference](#lsa-layer-mapping-reference)
5. [Industry Content Packages Catalog](#industry-content-packages-catalog)
6. [Content Update Decision Matrix](#content-update-decision-matrix)
7. [Activation Troubleshooting Guide](#activation-troubleshooting-guide)
8. [Post-Activation Validation Checklist](#post-activation-validation-checklist)

---

## Complete Prerequisite Checklist

### By Content Type: What You Need Before Activation

#### Sales & Revenue Analytics Content

**Mandatory Prerequisites**:
- [ ] Time Dimension table created and populated
  - Date range covers: Current year -3 years to +1 year
  - Includes: Year, Quarter, Month, Week, Day of Week, Day of Month
  - Fiscal calendar (if non-Gregorian): Fiscal_Year, Fiscal_Quarter, Fiscal_Period

- [ ] Currency Conversion (TCURR, TCURV) available
  - Exchange rates populated for all base currencies to reporting currency
  - Historical rates available (for multi-currency transactions)
  - Rate update frequency: Daily or weekly

- [ ] Customer Master Data
  - Source: SAP S/4HANA connection or external file
  - Minimum fields: Customer_ID, Customer_Name, Industry, Country, Sales_District
  - Record count: All active and inactive customers

- [ ] Product Master Data
  - Product_ID, Product_Name, Product_Category, Product_Line
  - Product hierarchy for drill-down analysis
  - Pricing: Standard cost or list price per product

- [ ] Organization Hierarchy
  - Company_Code, Division, Region, Sales_Office
  - Cost Centers (for profitability analysis)
  - Sales Territory (if using territory-based sales model)

**Optional Prerequisites** (enhances content):
- [ ] Customer Attributes (Industry, Account Size, Customer Type)
- [ ] Product Attributes (Margin %, Warranty Terms, Product Lifecycle)
- [ ] Sales Employee Master (Sales Rep name, territory, manager)

**Typical Implementation Time**: 2-4 weeks
**Effort**: 2-3 data engineers + 1 business analyst

#### Supply Chain & Inventory Content

**Mandatory Prerequisites**:
- [ ] Time Dimension (as above)

- [ ] Product Master Data
  - Product_ID, Product_Name, Product_Category
  - Unit of Measure (UOM): Base unit, conversion factors
  - Procurement data: Lead time, Minimum order quantity, Supplier

- [ ] Supplier Master Data
  - Supplier_ID, Supplier_Name, Country, Shipping_Terms
  - Rating: Quality, On-time delivery, Cost competitiveness

- [ ] Location/Warehouse Master
  - Warehouse_ID, Warehouse_Name, Location, Capacity
  - Warehouse type (DC, Store, Plant)

- [ ] Storage Location Mapping
  - Product → Warehouse → Storage Location
  - Enables granular inventory tracking

**Optional Prerequisites**:
- [ ] Transportation master (shipping modes, carriers, costs)
- [ ] Commodity codes and tariff classification
- [ ] Seasonal adjustment factors (for demand planning)

**Typical Implementation Time**: 3-5 weeks

#### Finance & Profitability Content

**Mandatory Prerequisites**:
- [ ] Time Dimension (with fiscal calendar critical here)

- [ ] General Ledger Master
  - GL Account (from Chart of Accounts)
  - Account type (Asset, Liability, Revenue, Expense, Equity)
  - Company Code assignment

- [ ] Cost Element Master
  - Cost Element ID and description
  - Cost Element category (Material, Labor, Overhead)

- [ ] Cost Center Master
  - Cost Center ID, Name, Department
  - Cost Center hierarchy (for consolidation)

- [ ] Currency Conversion (critical for multi-company consolidation)

- [ ] Company/Legal Entity Master
  - Company Code, Company Name
  - Fiscal year definition
  - Inter-company elimination rules

**Optional Prerequisites**:
- [ ] Profit Center Master (for segment profitability)
- [ ] Internal Orders (for project costing)
- [ ] Real Estate/Asset location mapping

**Typical Implementation Time**: 4-6 weeks

#### HR & Compensation Content

**Mandatory Prerequisites**:
- [ ] Time Dimension (with payroll periods)

- [ ] Employee Master
  - Employee_ID, Employee_Name, Department, Cost_Center
  - Job Title, Job Grade, Employment Type (Full-time, Part-time, Contractor)
  - Hire Date, Termination Date (if applicable)

- [ ] Organization Structure
  - Department, Division, Company
  - Reporting hierarchy (Manager → Direct Reports)

- [ ] Compensation Master
  - Base Salary, Variable Pay components
  - Benefits allocation per employee

**Optional Prerequisites**:
- [ ] Time & Attendance data (hours worked, absences)
- [ ] Skills and Competency master
- [ ] Succession planning data

**Typical Implementation Time**: 2-3 weeks

#### Manufacturing & Quality Content

**Mandatory Prerequisites**:
- [ ] Time Dimension

- [ ] Product Master (including Bill of Materials)
  - Product_ID, Product_Name
  - Component hierarchy (for BOM)
  - Unit of Measure and conversion factors

- [ ] Work Center Master
  - Work Center ID, Name, Facility, Capacity
  - Standard time per operation

- [ ] Material Master
  - Material_ID, Description, Category
  - Cost (Standard cost per unit)
  - Supplier (for sourced materials)

- [ ] Quality Codes Master
  - Defect codes, Inspection results, Pass/Fail codes

**Optional Prerequisites**:
- [ ] Equipment / Asset master (for maintenance tracking)
- [ ] Routing master (sequential operations per product)
- [ ] Batch/Lot number master (for traceability)

**Typical Implementation Time**: 3-5 weeks

---

## Time Dimension Population Guide

The Time Dimension is foundational for all analytics. Proper setup ensures temporal calculations work correctly.

### Step 1: Create Time Dimension Table

If not auto-created by Business Content activation:

```sql
CREATE TABLE TIME_DIMENSION (
    DATE DATE NOT NULL,
    YEAR INTEGER,
    QUARTER INTEGER,
    QUARTER_NAME VARCHAR(10),
    MONTH INTEGER,
    MONTH_NAME VARCHAR(20),
    WEEK_OF_YEAR INTEGER,
    WEEK_OF_MONTH INTEGER,
    DAY_OF_WEEK INTEGER,
    DAY_NAME VARCHAR(20),
    DAY_OF_MONTH INTEGER,
    DAY_OF_YEAR INTEGER,
    FISCAL_YEAR INTEGER,
    FISCAL_QUARTER INTEGER,
    FISCAL_QUARTER_NAME VARCHAR(10),
    FISCAL_MONTH INTEGER,
    IS_HOLIDAY BOOLEAN,
    HOLIDAY_NAME VARCHAR(100),
    IS_WEEKEND BOOLEAN,
    WORKING_DAY BOOLEAN,
    PRIMARY KEY (DATE)
);
```

### Step 2: Generate Time Dimension Data

**Option A: Use SAP Datasphere Generator**

```
In Datasphere:
1. Go to Business Content > Administration > Time Dimension
2. Click Generate Data
3. Specify parameters:
   ├── Start Date: 2021-01-01
   ├── End Date: 2026-12-31
   ├── Fiscal Calendar: Custom Fiscal Year starts July 1
   ├── Holiday Calendar: Select your country (USA, Germany, Japan, etc.)
4. Download CSV file
```

**Option B: Generate Programmatically**

Python script to generate Time Dimension:

```python
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Parameters
start_date = pd.Timestamp('2021-01-01')
end_date = pd.Timestamp('2026-12-31')
fiscal_year_start_month = 7  # July

# Generate date range
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Build Time Dimension
time_dim = pd.DataFrame({
    'DATE': dates,
    'YEAR': dates.year,
    'QUARTER': dates.quarter,
    'QUARTER_NAME': 'Q' + dates.quarter.astype(str),
    'MONTH': dates.month,
    'MONTH_NAME': dates.strftime('%B'),
    'WEEK_OF_YEAR': dates.isocalendar().week,
    'WEEK_OF_MONTH': (dates.day // 7) + 1,
    'DAY_OF_WEEK': dates.weekday() + 1,  # 1=Monday, 7=Sunday
    'DAY_NAME': dates.strftime('%A'),
    'DAY_OF_MONTH': dates.day,
    'DAY_OF_YEAR': dates.dayofyear,
    'IS_WEEKEND': dates.weekday >= 5,  # Saturday, Sunday
    'WORKING_DAY': dates.weekday < 5,   # Monday-Friday
})

# Calculate Fiscal Year (starting July)
def get_fiscal_year(date, fiscal_start_month=7):
    if date.month >= fiscal_start_month:
        return date.year + 1
    else:
        return date.year

time_dim['FISCAL_YEAR'] = time_dim['DATE'].apply(
    lambda x: get_fiscal_year(x, fiscal_year_start_month)
)

# Calculate Fiscal Quarter
def get_fiscal_quarter(date, fiscal_start_month=7):
    month_in_fiscal = (date.month - fiscal_start_month) % 12
    return (month_in_fiscal // 3) + 1

time_dim['FISCAL_QUARTER'] = time_dim['DATE'].apply(
    lambda x: get_fiscal_quarter(x, fiscal_year_start_month)
)
time_dim['FISCAL_QUARTER_NAME'] = 'FY' + time_dim['FISCAL_YEAR'].astype(str) + \
                                  'Q' + time_dim['FISCAL_QUARTER'].astype(str)

# Add holidays (example: USA holidays)
holidays = {
    pd.Timestamp('2024-01-01'): 'New Year Day',
    pd.Timestamp('2024-07-04'): 'Independence Day',
    pd.Timestamp('2024-12-25'): 'Christmas',
}

time_dim['IS_HOLIDAY'] = time_dim['DATE'].isin(holidays.keys())
time_dim['HOLIDAY_NAME'] = time_dim['DATE'].map(holidays)

# Save to CSV
time_dim.to_csv('time_dimension.csv', index=False, date_format='%Y-%m-%d')
print(f"Generated Time Dimension: {len(time_dim)} rows")
print(time_dim.head())
```

### Step 3: Load into Datasphere

**Method 1: Direct CSV Upload**

```
In Datasphere:
1. Go to Data Integration > New Data Flow
2. Add source: Upload File (time_dimension.csv)
3. Add target: TIME_DIMENSION table
4. Map columns (ensure correct data types)
5. Execute load
```

**Method 2: Load via Data Integration Flow**

Create SQL INSERT or SAP S/4HANA extraction if your company has a time dimension there:

```
Data Flow Steps:
1. Extract from SAP S/4HANA table /BIC/DIMDATE (if available)
   → Or upload CSV as shown above
2. Transform:
   ├── Ensure DATE is primary key (unique, not null)
   ├── Convert all numeric fields to INTEGER
   ├── Convert all name fields to VARCHAR
3. Load into TIME_DIMENSION table
4. Create index on DATE column for performance
```

### Step 4: Verify Population

```sql
-- Check date coverage
SELECT MIN(DATE) as earliest_date, MAX(DATE) as latest_date, COUNT(*) as row_count
FROM TIME_DIMENSION;

Expected output:
earliest_date: 2021-01-01
latest_date: 2026-12-31
row_count: 2191  (6 years × 365 days average)

-- Check fiscal calendar
SELECT DISTINCT FISCAL_YEAR, MIN(DATE), MAX(DATE)
FROM TIME_DIMENSION
GROUP BY FISCAL_YEAR
ORDER BY FISCAL_YEAR;

Expected output (if FY starts July):
FISCAL_YEAR: 2021, MIN: 2020-07-01, MAX: 2021-06-30
FISCAL_YEAR: 2022, MIN: 2021-07-01, MAX: 2022-06-30
...

-- Check no missing dates
SELECT COUNT(*) FROM TIME_DIMENSION
WHERE DATE BETWEEN '2024-01-01' AND '2024-12-31';

Expected output: 366 (2024 is a leap year)
```

### Step 5: Update Frequency

Set up daily or weekly refresh to maintain current date:

```
In Datasphere Data Integration:
1. Create repeating task for Time Dimension refresh
2. Schedule: Daily at 23:59 UTC
3. Action: Insert new dates for next 1 year (rolling window)
4. Delete future dates beyond 3 years from today (keep 3-year rolling window)
```

---

## Currency Conversion Setup Guide

Multi-currency analytics require proper currency conversion configuration.

### Step 1: Source Currency Master Data

#### From SAP S/4HANA (Recommended)

Create data flow to extract exchange rates:

```
Source: SAP S/4HANA
Table: TCURR (Exchange Rates)

Fields:
├── FCURR (From Currency) — Source currency code
├── TCURR (To Currency) — Target currency code
├── GDATU (Valid From Date) — Rate validity start
├── GDATUV (Valid To Date) — Rate validity end
├── KURST (Exchange Rate Type) — M (Daily), B (Bond), etc.
├── KURSK (Exchange Rate) — Conversion factor

Target: Datasphere TCURR table
```

Data Flow SQL:

```sql
SELECT
    FCURR as source_currency,
    TCURR as target_currency,
    GDATU as valid_from_date,
    GDATUV as valid_to_date,
    KURST as rate_type,
    KURSK as exchange_rate
FROM TCURR@SAP_S4H
WHERE KURST = 'M'  -- Daily rates
  AND GDATU <= TODAY()
ORDER BY FCURR, TCURR, GDATU;
```

#### From External File

If not available in SAP:

```csv
source_currency,target_currency,valid_from_date,valid_to_date,exchange_rate
USD,EUR,2024-01-01,2024-12-31,0.92
USD,GBP,2024-01-01,2024-12-31,0.79
EUR,GBP,2024-01-01,2024-12-31,0.86
JPY,USD,2024-01-01,2024-12-31,0.0067
CNY,USD,2024-01-01,2024-12-31,0.138
```

### Step 2: Create Exchange Rate Lookup Table

```sql
CREATE TABLE TCURR (
    SOURCE_CURRENCY CHAR(3) NOT NULL,
    TARGET_CURRENCY CHAR(3) NOT NULL,
    VALID_FROM_DATE DATE NOT NULL,
    VALID_TO_DATE DATE NOT NULL,
    RATE_TYPE CHAR(1),
    EXCHANGE_RATE DECIMAL(20, 8),
    PRIMARY KEY (SOURCE_CURRENCY, TARGET_CURRENCY, VALID_FROM_DATE),
    INDEX idx_target_date (TARGET_CURRENCY, VALID_FROM_DATE)
);

-- Insert exchange rates
INSERT INTO TCURR VALUES
('USD', 'EUR', '2024-01-01', '2024-12-31', 'M', 0.92),
('USD', 'GBP', '2024-01-01', '2024-12-31', 'M', 0.79),
('EUR', 'USD', '2024-01-01', '2024-12-31', 'M', 1.0869),
('EUR', 'GBP', '2024-01-01', '2024-12-31', 'M', 0.86),
...;
```

### Step 3: Create Currency Conversion Calculation View

```sql
CREATE VIEW TCURV (
    source_currency,
    target_currency,
    conversion_date,
    exchange_rate
) AS
SELECT
    tcurr.source_currency,
    tcurr.target_currency,
    /* Get the most recent rate for the given date */
    MAX(tcurr.valid_from_date) as conversion_date,
    tcurr.exchange_rate
FROM TCURR tcurr
WHERE tcurr.valid_from_date <= CURRENT_DATE
  AND tcurr.valid_to_date >= CURRENT_DATE
GROUP BY
    tcurr.source_currency,
    tcurr.target_currency,
    tcurr.exchange_rate;
```

### Step 4: Use in Analytical Queries

**Example: Convert all sales to USD**

```sql
SELECT
    t.transaction_id,
    t.transaction_date,
    t.amount_original,
    t.currency_original,
    t.amount_original * COALESCE(c.exchange_rate, 1) as amount_usd,
    'USD' as currency_converted
FROM SALES t
LEFT JOIN TCURV c
    ON t.currency_original = c.source_currency
    AND c.target_currency = 'USD'
    AND c.conversion_date <= t.transaction_date
WHERE c.conversion_date = (
    SELECT MAX(conversion_date)
    FROM TCURV c2
    WHERE c2.source_currency = t.currency_original
      AND c2.target_currency = 'USD'
      AND c2.conversion_date <= t.transaction_date
);
```

### Step 5: Verify Configuration

```sql
-- Check exchange rates available
SELECT
    source_currency,
    target_currency,
    COUNT(*) as rate_count,
    MIN(valid_from_date) as earliest,
    MAX(valid_to_date) as latest
FROM TCURR
GROUP BY source_currency, target_currency
ORDER BY source_currency;

-- Check current rates
SELECT * FROM TCURV
WHERE conversion_date = TODAY()
ORDER BY source_currency, target_currency;

-- Test conversion
SELECT
    100 as amount,
    'EUR' as from_currency,
    'USD' as to_currency,
    100 * (SELECT exchange_rate FROM TCURV
           WHERE source_currency = 'EUR'
             AND target_currency = 'USD'
             AND conversion_date = TODAY()
          ) as amount_converted_usd;
```

### Step 6: Setup Refresh Schedule

Exchange rates typically change daily:

```
In Datasphere Data Integration:
1. Create task: "Update Exchange Rates Daily"
2. Source: External system or manual file upload
3. Target: TCURR table
4. Refresh frequency: Daily at 08:00 UTC
5. Retention: Keep rates for 3 years rolling
```

---

## LSA++ Layer Mapping Reference

Complete reference for how Business Content objects map to LSA++ layers.

### Layer 0: Inbound Layer - Source Extraction

**Purpose**: Raw data from source systems, minimal transformation.

**Characteristics**:
- Table structure mirrors source system
- Full detail level (no aggregation)
- Delta load frequency (daily, hourly)
- Field names may match source system language

**Example Objects from Business Content**:

```
Sales Analytics Package:
├── SALES_ORDER_INBOUND (mirrors S/4HANA VBAK)
├── SALES_ITEM_INBOUND (mirrors S/4HANA VBAP)
├── CUSTOMER_INBOUND (mirrors S/4HANA KNA1)
└── MATERIAL_INBOUND (mirrors S/4HANA MARA)

Supply Chain Package:
├── PURCHASE_ORDER_INBOUND (mirrors EKKO)
├── DELIVERY_INBOUND (mirrors LIKP)
├── GOODS_RECEIPT_INBOUND (mirrors EKET)
└── STOCK_INBOUND (mirrors MARD)
```

**Data Flow Pattern**:
```
Source System → Inbound Table (extract as-is)
```

**Access Control**: Data engineers only

---

### Layer 1: Propagation Layer - Document Level

**Purpose**: Document-level data with minimal business logic, ready to propagate.

**Characteristics**:
- One row per document or transaction
- Includes related master data attributes (not just IDs)
- Light transformation (decode values, convert units)
- Retains all detail (not aggregated)

**Example Objects**:

```
Sales Analytics:
├── SALES_ORDER_PROPAGATED
│   From: SALES_ORDER_INBOUND + CUSTOMER_INBOUND
│   Added: Customer_Name, Industry, Sales_Rep
│
├── INVOICE_PROPAGATED
│   From: BILLING_INBOUND + ORDER_INBOUND
│   Added: Order_ID, Customer reference, Terms
```

**Data Flow Pattern**:
```
Inbound (L0) → Enrich with Master Data → Propagation Table (L1)
```

**Transformations**:
```sql
-- Example transformation from L0 to L1
INSERT INTO SALES_ORDER_PROPAGATED
SELECT
    o.order_id,
    o.order_date,
    o.customer_id,
    c.customer_name,      -- Added from CUSTOMER master
    c.industry,           -- Added from CUSTOMER master
    o.amount,
    o.currency,
    o.sales_rep_id,
    sr.sales_rep_name,    -- Added from SALES_REP master
    CURRENT_TIMESTAMP as load_timestamp
FROM SALES_ORDER_INBOUND o
LEFT JOIN CUSTOMER_INBOUND c ON o.customer_id = c.customer_id
LEFT JOIN SALES_REP_INBOUND sr ON o.sales_rep_id = sr.sales_rep_id;
```

**Access Control**: Data engineers + architects

---

### Layer 2: Harmonization Layer - Unified Model

**Purpose**: Cleansed, standardized, deduplicated data. Single source of truth.

**Characteristics**:
- Business-friendly naming (not source system codes)
- Data quality checks and deduplication
- Cross-source consolidation (combine SAP + Salesforce + external systems)
- Slowly Changing Dimensions (SCD) logic
- Time-dimensioned snapshots for historical analysis

**Example Objects**:

```
Sales Analytics:
├── CUSTOMER_HARMONIZED
│   ├── Customer_ID (primary key)
│   ├── Customer_Name (standardized)
│   ├── Industry (from master, validated against industry list)
│   ├── Valid_From, Valid_To (SCD Type 2)
│   ├── Is_Active (calculated flag)
│   └── Last_Modified_Date

├── SALES_ORDER_HARMONIZED
│   ├── Order_ID
│   ├── Order_Date (standardized format)
│   ├── Customer_ID (foreign key to CUSTOMER_HARMONIZED)
│   ├── Amount_Local_Currency
│   ├── Amount_USD (converted using TCURV)
│   ├── Order_Status (standardized: NEW, CONFIRMED, SHIPPED, CLOSED)
│   ├── Margin_Amount (calculated)
│   └── Load_Date (when record was harmonized)

├── SALES_DAILY_SNAPSHOT
│   ├── Report_Date (grain)
│   ├── Customer_ID
│   ├── Orders_Count (aggregated)
│   ├── Revenue_Amount (summed, in USD)
│   └── Average_Order_Value (calculated)
```

**Data Quality Rules** (applied in L2):

```sql
-- Example: Deduplication
INSERT INTO CUSTOMER_HARMONIZED
SELECT DISTINCT
    customer_id,
    MAX(customer_name) as customer_name,  -- Pick most recent
    MAX(industry) as industry,
    CURRENT_DATE as valid_from,
    NULL as valid_to,
    1 as is_active,
    CURRENT_TIMESTAMP as last_modified
FROM SALES_ORDER_PROPAGATED
WHERE customer_id IS NOT NULL
  AND customer_name NOT LIKE '%TEST%'  -- Quality check
  AND customer_name NOT LIKE '%DUMMY%'
GROUP BY customer_id;

-- Example: SCD Type 2 (track history)
MERGE INTO CUSTOMER_HARMONIZED tgt
USING (SELECT * FROM CUSTOMER_INBOUND) src
ON tgt.customer_id = src.customer_id
WHEN MATCHED AND src.customer_name <> tgt.customer_name THEN
    UPDATE SET tgt.valid_to = CURRENT_DATE - 1
    THEN INSERT (customer_id, customer_name, valid_from, valid_to, is_active)
        VALUES (src.customer_id, src.customer_name, CURRENT_DATE, NULL, 1);
```

**Access Control**: Analysts (read), architects (write)

---

### Layer 3: Reporting Layer - Analytics

**Purpose**: Pre-aggregated, optimized analytical views for dashboards and reports.

**Characteristics**:
- Pre-aggregated (group by key dimensions)
- Optimized for dashboard performance
- Business metric naming (Revenue, Margin, %, Rank)
- Designed for end-user self-service
- Usually materialized (stored, not calculated on-demand)

**Example Objects**:

```
Sales Analytics:
├── REVENUE_BY_PRODUCT
│   ├── Report_Date (daily grain)
│   ├── Product_Category
│   ├── Product_Name
│   ├── Revenue_Amount (SUM of orders)
│   ├── Order_Count (COUNT of orders)
│   ├── Average_Order_Value (SUM / COUNT)
│   └── Margin_Percent (Margin / Revenue * 100)

├── CUSTOMER_METRICS
│   ├── Customer_ID
│   ├── Customer_Name
│   ├── Industry
│   ├── YTD_Revenue
│   ├── YTD_Order_Count
│   ├── YTD_Average_Order_Value
│   ├── Churn_Risk (calculated flag: no order in 90 days)
│   └── Customer_Lifetime_Value (all-time revenue)

├── REGIONAL_SALES_DASHBOARD
│   ├── Report_Date
│   ├── Region
│   ├── Sales_Office
│   ├── Revenue_Amount
│   ├── Revenue_YoY_Growth (Year-over-Year %)
│   ├── Target_Revenue
│   ├── Variance_to_Target
│   ├── Rank_in_Region
│   └── Status (On_Track, At_Risk, Off_Track)
```

**Aggregation Examples**:

```sql
-- Example L3 view: Revenue by Product
INSERT INTO REVENUE_BY_PRODUCT
SELECT
    DATE_TRUNC(o.order_date, DAY) as report_date,
    p.product_category,
    p.product_name,
    SUM(o.amount_usd) as revenue_amount,
    COUNT(DISTINCT o.order_id) as order_count,
    SUM(o.amount_usd) / COUNT(DISTINCT o.order_id) as average_order_value,
    SUM(o.margin_amount) / SUM(o.amount_usd) * 100 as margin_percent
FROM SALES_ORDER_HARMONIZED o
JOIN PRODUCT_HARMONIZED p ON o.product_id = p.product_id
WHERE o.order_date >= DATE_TRUNC(CURRENT_DATE, MONTH)
GROUP BY
    DATE_TRUNC(o.order_date, DAY),
    p.product_category,
    p.product_name;

-- Example L3 view: Customer Metrics (with complex calculations)
INSERT INTO CUSTOMER_METRICS
SELECT
    c.customer_id,
    c.customer_name,
    c.industry,
    SUM(o.amount_usd) as ytd_revenue,
    COUNT(DISTINCT o.order_id) as ytd_order_count,
    SUM(o.amount_usd) / NULLIF(COUNT(DISTINCT o.order_id), 0) as ytd_avg_order_value,
    CASE
        WHEN MAX(o.order_date) < CURRENT_DATE - 90 THEN 'High'
        WHEN MAX(o.order_date) < CURRENT_DATE - 30 THEN 'Medium'
        ELSE 'Low'
    END as churn_risk,
    SUM(o.amount_usd) as customer_lifetime_value
FROM CUSTOMER_HARMONIZED c
LEFT JOIN SALES_ORDER_HARMONIZED o
    ON c.customer_id = o.customer_id
    AND YEAR(o.order_date) = YEAR(CURRENT_DATE)
GROUP BY
    c.customer_id,
    c.customer_name,
    c.industry;
```

**Access Control**: All business users (read-only)

---

## Industry Content Packages Catalog

### Automotive Industry

#### Package: Automotive Sales & Service Analytics (ASA-SAL-001)
- **Version**: 2.3.1 (as of Feb 2024)
- **Size**: 45 tables, 28 views, 12 data flows
- **Industry Domains**: Sales, Service, Warranty, Spare Parts
- **Source Systems**: SAP S/4HANA, SAP CRM, SAP ERP
- **Key Analytical Areas**:
  - Vehicle sales by model, trim, color
  - Service revenue by service type and workshop
  - Warranty claim analysis
  - Spare parts inventory and turnover
- **Key Dimensions**: Vehicle_Model, Customer, Sales_Region, Workshop, Service_Type, Time
- **Key Metrics**:
  - Revenue_Sales, Revenue_Service, Revenue_Warranty
  - Units_Sold, Service_Orders_Count
  - Average_Selling_Price, Service_Margin_Percent
  - Warranty_Cost_Percent_of_Revenue
- **Prerequisites**:
  - Time Dimension (3-year history minimum)
  - Customer Master, Product Master (vehicles)
  - Sales Organization, Dealer Network
  - Currency Conversion (if multi-currency)
- **Typical Activation Time**: 4-6 weeks
- **Customization Needs**: Regional sales channel mapping

#### Package: Automotive Supply Chain & Inventory (ASA-SCM-001)
- **Version**: 1.8.0
- **Size**: 62 tables, 35 views, 18 data flows
- **Domains**: Procurement, Production Planning, Inventory, Logistics
- **Key Analytical Areas**:
  - Supplier performance (quality, on-time delivery, cost)
  - Production planning and scheduling
  - Inventory planning and optimization
  - Logistics cost and efficiency
- **Key Dimensions**: Supplier, Material, Plant, Warehouse, Logistics_Partner
- **Key Metrics**:
  - Supplier_Quality_Score, On_Time_Delivery_Rate
  - Inventory_Turnover, Days_Inventory_Outstanding
  - Procurement_Cost_Variance, Freight_Cost_per_Unit
  - Production_Yield, Equipment_Downtime
- **Prerequisites**:
  - Time Dimension (with production calendar)
  - Product Master (with BOM)
  - Supplier Master, Organization Hierarchy
  - Unit of Measure, Standard costs
- **Typical Activation Time**: 8-10 weeks
- **Customization Needs**: Multi-plant production planning rules

### Retail Industry

#### Package: Retail POS & Merchandise Analytics (RET-SAL-001)
- **Version**: 2.1.4
- **Size**: 38 tables, 31 views, 10 data flows
- **Domains**: Point of Sale, Merchandise Planning, Promotions
- **Key Analytical Areas**:
  - Sales by product category, store location
  - Merchandise margin and turnover
  - Promotion effectiveness and ROI
  - Customer traffic and conversion
- **Key Dimensions**: Store, Product_Category, Date, Cashier, Promotion
- **Key Metrics**:
  - Revenue, Units_Sold, Transactions_Count
  - Margin_Amount, Margin_Percent
  - Average_Transaction_Value
  - Promotion_Lift, Customer_Traffic
- **Prerequisites**:
  - Time Dimension (with fiscal calendar)
  - Product Master (UPC codes, categories)
  - Store Master (locations, formats)
  - Currency Conversion
- **Typical Activation Time**: 3-5 weeks
- **Customization Needs**: Store hierarchy alignment

#### Package: Retail Supply Chain & Inventory (RET-SCM-001)
- **Version**: 1.9.2
- **Size**: 55 tables, 40 views, 15 data flows
- **Domains**: Distribution, Inventory, Replenishment
- **Key Analytical Areas**:
  - Stock coverage and stockout analysis
  - Distribution center efficiency
  - Inventory aging and obsolescence
  - Replenishment effectiveness
- **Key Dimensions**: Store, Distribution_Center, Product, Supplier
- **Key Metrics**:
  - Stock_Coverage_Days, Stockout_Incidents
  - Inventory_Turnover, Days_Inventory_Outstanding
  - Distribution_Cost_per_Unit, Shrinkage_Rate
  - Replenishment_Accuracy
- **Prerequisites**:
  - Time Dimension
  - Product Master, Store Master, Distribution Network
  - Inventory transaction history (6+ months)
  - Unit of Measure
- **Typical Activation Time**: 6-8 weeks
- **Customization Needs**: Multi-tier distribution network

### Utilities Industry

#### Package: Energy & Water Distribution Analytics (UTI-OPS-001)
- **Version**: 1.6.0
- **Size**: 41 tables, 29 views, 12 data flows
- **Domains**: Grid Operations, Customer Billing, Asset Management
- **Key Analytical Areas**:
  - Energy/water consumption by customer segment
  - Outage frequency and duration (SAIDI/SAIFI)
  - Billing and revenue collection
  - Asset condition and maintenance
- **Key Dimensions**: Customer_Segment, Service_Area, Equipment, Date
- **Key Metrics**:
  - Consumption_Volume, Revenue_Billing
  - Outage_Frequency, Outage_Duration, Customer_Impact
  - Collection_Rate, Days_Sales_Outstanding
  - Asset_Age, Maintenance_Cost
- **Prerequisites**:
  - Time Dimension (hourly/daily)
  - Customer Master (by segment: residential, commercial, industrial)
  - Equipment Master, Service Territory
  - Meter readings and consumption data (historical 12 months)
- **Typical Activation Time**: 5-7 weeks
- **Customization Needs**: Regulatory reporting alignment

### Finance Industry

#### Package: General Ledger & Financial Reporting (FIN-GL-001)
- **Version**: 1.7.3
- **Size**: 34 tables, 26 views, 8 data flows
- **Domains**: Accounting, Profitability, Consolidation
- **Key Analytical Areas**:
  - Profitability analysis (P&L by segment)
  - Cash flow analysis
  - Receivables and payables aging
  - Consolidation and elimination
- **Key Dimensions**: Company_Code, GL_Account, Cost_Center, Time
- **Key Metrics**:
  - Revenue, Cost_of_Goods_Sold, Operating_Expense
  - Gross_Margin, Operating_Income, Net_Income
  - Accounts_Receivable_Aging, Days_Sales_Outstanding
  - Accounts_Payable_Aging, Days_Payable_Outstanding
- **Prerequisites**:
  - Time Dimension (with fiscal calendar critical)
  - GL Account Master with account type
  - Cost Center hierarchy
  - Currency Conversion (for consolidation)
  - Company/Legal Entity Master
- **Typical Activation Time**: 4-6 weeks
- **Customization Needs**: Chart of accounts mapping

#### Package: Banking Risk & Compliance (FIN-RISK-001)
- **Version**: 1.2.1
- **Size**: 48 tables, 35 views, 14 data flows
- **Domains**: Credit Risk, Market Risk, Regulatory Reporting
- **Key Analytical Areas**:
  - Credit risk assessment and monitoring
  - Portfolio composition and concentration
  - Non-performing loan (NPL) analysis
  - Regulatory ratio reporting (Basel III/IV)
- **Key Dimensions**: Borrower, Loan_Product, Rating, Collateral_Type
- **Key Metrics**:
  - Risk_Weighted_Assets, Capital_Ratio
  - Non_Performing_Loan_Ratio, Loss_Provisions
  - Interest_Rate_Risk_Exposure, Liquidity_Coverage_Ratio
- **Prerequisites**:
  - Time Dimension
  - Borrower Master, Loan Portfolio master
  - Risk classification master
  - Currency Conversion
  - Regulatory parameter tables (risk weights, LGD, PD)
- **Typical Activation Time**: 8-12 weeks
- **Customization Needs**: Regulatory framework alignment

### Manufacturing Industry

#### Package: Production & Cost Analysis (MFG-PROD-001)
- **Version**: 1.5.2
- **Size**: 52 tables, 38 views, 16 data flows
- **Domains**: Bill of Materials, Work Orders, Cost Accounting
- **Key Analytical Areas**:
  - Production cost analysis (standard vs. actual)
  - Variance analysis (material, labor, overhead)
  - Production efficiency and throughput
  - Order profitability
- **Key Dimensions**: Product, Work_Center, Cost_Element, Order, Plant
- **Key Metrics**:
  - Cost_per_Unit, Variance_Amount, Variance_Percent
  - Throughput, Cycle_Time, Equipment_Utilization
  - Scrap_Rate, Rework_Rate
  - Order_Profitability
- **Prerequisites**:
  - Time Dimension
  - Product Master (with BOM)
  - Cost Element Master, Cost Center hierarchy
  - Standard costs (historical)
  - Work Center/Equipment master
- **Typical Activation Time**: 7-9 weeks
- **Customization Needs**: Cost accounting method (actual vs. standard)

---

## Content Update Decision Matrix

When new versions of Business Content packages are released, decide whether to update:

### Decision Framework

```
Does content have                    Recommend
customizations?  |  Version Type    │ Action      │ Effort
─────────────────┼─────────────────────────────────────────
No               │ Patch (1.0→1.0.1)│ Overwrite   │ 1-2 hrs
No               │ Minor (1.0→1.1)  │ Overwrite   │ 2-4 hrs
No               │ Major (1.0→2.0)  │ Overwrite   │ 4-8 hrs
Yes, minor       │ Patch            │ Overwrite   │ 1-2 hrs
Yes, minor       │ Minor            │ Keep        │ 1 day
Yes, minor       │ Major            │ Keep        │ Separate project
Yes, major       │ Any type         │ Keep        │ Plan carefully
```

### Detailed Scenarios

| Scenario | Decision | Rationale | Steps |
|----------|----------|-----------|-------|
| **Patch: No customizations** | Overwrite immediately | Fixes bugs, improves stability | 1. Backup current version 2. Activate patch 3. Test dashboards |
| **Patch: Minor customizations** | Overwrite | Customizations usually preserved | 1. Verify custom fields not modified 2. Overwrite 3. Test |
| **Minor Version: No customizations** | Overwrite | New features valuable | 1. Review release notes 2. Test in dev 3. Activate |
| **Minor Version: Significant customizations** | Keep | Cost of re-customization outweighs benefit | 1. Document customizations 2. Evaluate new features 3. Plan migration for major version |
| **Major Version: Any customizations** | Keep (Plan separately) | Risk of breaking changes high | 1. Create project for migration 2. Analyze all changes 3. Rebuild customizations 4. Test thoroughly |
| **Production environment** | Keep + Test in Dev | Minimize production risk | 1. Update content in DEV 2. Thorough testing 3. Plan maintenance window 4. Update PROD |

### Update Testing Checklist

Before updating production content:

- [ ] Backup current version
  ```
  Export all objects: Business Content > Manage Content > Export
  ```

- [ ] Test in non-production space
  - [ ] Activate update version
  - [ ] Run all key analytical queries
  - [ ] Verify dashboard performance
  - [ ] Check custom field calculations
  - [ ] Test data flows

- [ ] Compare versions
  - [ ] List new tables/views
  - [ ] Check deprecated objects
  - [ ] Document breaking changes

- [ ] Merge customizations (if using Keep)
  - [ ] Identify modified fields in old version
  - [ ] Manually apply to new version
  - [ ] Test recalculations

- [ ] Communicate to stakeholders
  - [ ] Notify business users of new features
  - [ ] Schedule training if UI changed
  - [ ] Provide release notes

---

## Activation Troubleshooting Guide

### Symptoms and Solutions

#### Symptom: "Prerequisite not satisfied: Time Dimension"

**Root Cause**: Time Dimension table not populated or empty.

**Solution**:
```
1. Check if TIME_DIMENSION table exists
   → Go to Tables in space, search for "TIME_DIMENSION"

2. If exists but empty:
   → Go to Business Content > Administration > Time Dimension
   → Click "Generate Data"
   → Download CSV file
   → Create Data Flow: Upload CSV → TIME_DIMENSION table
   → Execute load

3. Verify population:
   → Query: SELECT COUNT(*) FROM TIME_DIMENSION
   → Should return thousands of rows (1+ year of data)
```

#### Symptom: "Currency Conversion view not available"

**Root Cause**: TCURR/TCURV not populated with exchange rates.

**Solution**:
```
1. Check if TCURR table exists and has data
   → SELECT COUNT(*) FROM TCURR
   → If 0 rows:

2. Load exchange rates:
   → Create Data Flow from SAP S/4HANA table TCURR
   → OR upload CSV with rates
   → Target: TCURR table

3. Create currency conversion view:
   → Use Datasphere's Calculation View template
   → Base on TCURR table
   → Publish as TCURV view

4. Verify:
   → SELECT * FROM TCURV WHERE CONVERSION_DATE = TODAY()
   → Should return rates for all currency pairs
```

#### Symptom: "Space quota exceeded" during activation

**Root Cause**: Insufficient memory, disk, or object quota in target space.

**Solution**:
```
1. Check space quota:
   → Go to Space > Settings
   → Review: Memory Used / Allocated, Disk Used / Allocated

2. Free up space:
   → Delete unused tables/views
   → Archive historical data flows
   → OR increase space allocation:
     └── Go to Space Settings > Upgrade Resources

3. Alternative: Activate to different space
   → Create new space with larger quota
   → Select as activation target
```

#### Symptom: "Connection test failed" during activation

**Root Cause**: Source system connection invalid or unreachable.

**Solution**:
```
1. Verify connection:
   → Go to Connections > [Connection Name]
   → Click Test Connection
   → Review error details

2. Common fixes:
   → Check credentials (username/password valid)
   → Verify hostname/IP reachable (ping, telnet)
   → Check firewall rules
   → Verify TLS certificate if using HTTPS

3. Update connection:
   → Edit connection with correct parameters
   → Retry test

4. Retry activation:
   → Business Content > Manage Content
   → Click Retry Activation
```

#### Symptom: "Permission denied" error

**Root Cause**: User lacks necessary roles for space.

**Solution**:
```
1. Check user role in target space:
   → Space Settings > Members
   → Look for current user

2. Assign space admin role:
   → Have space owner or admin assign:
     └── User Role: Space_Admin
     └── Or: Space_Editor (minimum for activation)

3. Retry activation with new permissions
```

#### Symptom: "Object conflicts: CUSTOMER table already exists"

**Root Cause**: Name collision with existing table.

**Solution**:
```
1. Choose conflict resolution:
   → In activation dialog, when conflict appears:
     ├── Overwrite (replace existing table)
     ├── Keep (skip this object)
     └── Rename (add _v2 suffix to new version)

2. If choosing Rename:
   → Update data flows to use new table names
   → Recalculate dependent views

3. If choosing Keep:
   → Manually merge old and new schema later
   → Document changes for future migration
```

#### Symptom: Activation hangs or times out

**Root Cause**: Large package, insufficient resources, or service slowness.

**Solution**:
```
1. Cancel activation:
   → If no progress > 30 mins, click Cancel
   → Activation rolls back automatically

2. Increase space resources:
   → Space Settings > Upgrade Memory / Disk
   → Increase to double current allocation

3. Retry activation:
   → Business Content > Manage Content > Retry
   → Monitor progress in real-time

4. Enable debug logging:
   → Go to settings > Logging Level = DEBUG
   → Activation logs will show detailed steps
```

---

## Post-Activation Validation Checklist

After successful activation, validate everything works:

### Data Completeness Checks

**Time Dimension**:
```sql
SELECT MIN(DATE), MAX(DATE), COUNT(*) FROM TIME_DIMENSION;
-- Verify: Covers at least 3-year rolling window
-- Verify: No gaps in dates
-- Verify: Fiscal calendar populated if used
```

**Master Data** (Customer, Product, Organization):
```sql
SELECT TABLE_NAME, COUNT(*) FROM [ACTIVATED_TABLES]
WHERE TABLE_NAME LIKE '%MASTER' OR TABLE_NAME LIKE '%REFERENCE'
GROUP BY TABLE_NAME;
-- Verify: All master data tables > 0 rows
```

**Exchange Rates** (if multi-currency):
```sql
SELECT COUNT(DISTINCT CURRENCY_PAIR) FROM TCURV
WHERE CONVERSION_DATE = TODAY();
-- Verify: All expected currency pairs have rates
```

### Analytical View Validation

**Test Key Views**:
```sql
-- For each key analytical view
SELECT COUNT(*) FROM REVENUE_ANALYSIS;
SELECT COUNT(*) FROM CUSTOMER_METRICS;
SELECT COUNT(*) FROM SALES_DASHBOARD;

-- Verify: Returns rows, no errors
-- Verify: Execution time < 5 seconds for < 1M rows
```

**Check Calculated Fields**:
```sql
SELECT MARGIN_PERCENT FROM REVENUE_ANALYSIS LIMIT 10;
-- Verify: No NULL, no error values
-- Verify: Percentages between 0-100 (if appropriate)

SELECT YTD_REVENUE, ORDERS_COUNT FROM CUSTOMER_METRICS LIMIT 10;
-- Verify: No negative numbers (if inappropriate)
-- Verify: Aggregations match manual calculation
```

### Performance Baseline

**Record Execution Times**:
```
Create_Date: [Today]
Query Performance Baseline:
├── REVENUE_ANALYSIS: 1.8 seconds
├── CUSTOMER_METRICS: 2.3 seconds
├── SALES_DASHBOARD: 1.2 seconds
├── MARGIN_ANALYSIS: 2.9 seconds
└── INVENTORY_STATUS: 3.1 seconds

Alert threshold: If any query > 5x baseline
```

### Dashboard & Report Testing

**For Each Pre-Built Dashboard**:
- [ ] Loads without errors
- [ ] All charts render with data
- [ ] Drill-down navigation works
- [ ] Filters apply and refresh correctly
- [ ] Dates display in correct format

**Example Test Case**:
```
Dashboard: Regional Sales Performance
├── Load dashboard: ✓ (< 3 seconds)
├── Chart 1 "Sales by Region": ✓ (shows 5 regions)
├── Chart 2 "YoY Growth": ✓ (shows comparison)
├── Filter by Date Range: ✓ (updates all charts)
└── Drill-down Region → Sales Office: ✓ (drills to detail)
```

### Access & Security

**Verify Access Control**:
```
Test user: analyst@company.com
Role: Datasphere_Analyst

Expected: Can read analytics views, cannot modify
├── Can SELECT from REVENUE_ANALYSIS: ✓
├── Can view dashboards: ✓
├── Cannot INSERT into tables: ✓
├── Cannot delete views: ✓
```

**Check Audit Logs**:
```
Go to Administration > Audit Logs
Filter: Last 24 hours, Action = Activation
Verify: All activation steps logged
```

### Business Validation

**Have Business Users Review**:
- [ ] KPIs match expected values (within 5%)
- [ ] Dimensions and hierarchies align to organization
- [ ] Data freshness is acceptable
- [ ] Report templates useful for their role

**Example Validation**:
```
Business Reviewer: Sales Director

Expected Revenue (from Finance System): $45.2M
Actual from REVENUE_ANALYSIS: $45.1M
Variance: 0.2% ✓ (acceptable)

Expected Orders (from operational system): 12,500
Actual from ORDERS_COUNT: 12,480
Variance: 0.2% ✓ (acceptable)
```

### Issue Logging

If issues found:
```
Log Template:
├── Date Found: [Date]
├── Component: [Table/View/Dashboard]
├── Issue: [Description]
├── Severity: Critical|High|Medium|Low
├── Resolution: [Fix applied]
└── Root Cause: [Why it happened]

Example:
├── Component: REVENUE_ANALYSIS view
├── Issue: Q1 2024 revenue 5% lower than expected
├── Root Cause: Missing transaction data from one sales office (data load failure)
├── Resolution: Re-ran data flow from source system, now correct
```

### Sign-Off

Get formal approval before opening to business users:

```
Activation Sign-Off Form:
├── Activated Package: SALES_ANALYTICS v2.1
├── Target Space: ANALYTICS_PROD
├── Activation Date: 2024-02-01
├── Data Validation: ✓ PASSED
├── Performance Baseline: ✓ PASSED
├── Dashboard Testing: ✓ PASSED
├── Business Review: ✓ PASSED
├── Go-Live Approval:
│   ├── Technical Lead: [Name] ✓ Approved
│   ├── Business Lead: [Name] ✓ Approved
│   └── Date: 2024-02-05
└── Available to Business Users: Yes (as of 2024-02-06)
```

---

## References and Support

- **Datasphere Documentation**: https://help.sap.com/datasphere
- **Business Content Network**: https://www.sap.com/datasphere/content-network
- **SAP Community**: https://community.sap.com/datasphere
- **SAP Support Portal**: https://support.sap.com

For questions on specific industry content, contact your SAP solution partner or Datasphere implementation team.
