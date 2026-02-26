---
name: Analytic Model Creator
description: "Build Analytic Models for SAP Analytics Cloud consumption. Use this skill when you need to create reporting dimensions, define sophisticated measures (calculated, restricted, count distinct), configure currency/unit conversions, set up exception aggregation, or prepare data for SAC dashboards. Essential for analytics layer design, KPI definition, and self-service BI enablement."
---

# Analytic Model Creator Skill

## Overview

The Analytic Model Creator skill guides you through designing and implementing Analytic Models in SAP Datasphere. Analytic Models are semantic objects that present data to analytics tools like SAP Analytics Cloud (SAC) in a consumable, pre-aggregated format. They sit above Fact and Dimension views, providing a polished interface for end users to create reports and dashboards.

## What Are Analytic Models?

### Definition
An Analytic Model is a semantic object that combines:
- **One Fact source** — Contains quantitative measures and primary grain
- **Multiple Dimensions** — Provide context and analysis dimensions
- **Measures** — Simple, calculated, or restricted aggregations
- **Variables** — Optional parameters for dynamic filtering
- **Attributes** — Dimension properties and drill-down paths
- **Aggregations** — Exception rules for special measure handling

### Role in the Consumption Layer
```
Raw Data (Databases)
        ↓
    Data Builder (Cleanse, Join)
        ↓
 Semantic Views (Graphical/SQL)
        ↓
 Analytic Models (Aggregated, Structured) ← YOU ARE HERE
        ↓
SAC Dashboards, Reports, Exploration
```

### When to Use Analytic Models

**Create an Analytic Model when:**
- Building SAC dashboards and reports
- End users need self-service analytics
- You need to define sophisticated aggregation rules
- Measures require conditional aggregation or currency conversion
- Multiple consumption patterns are needed from one data source
- Data governance requires controlled access to metrics

**DO NOT use Analytic Models for:**
- Pure data integration or distribution
- Direct operational reporting (use Relational Datasets)
- Real-time transaction querying (use transaction views)
- Data that rarely needs aggregation

## Creating an Analytic Model: Step-by-Step

### Step 1: Select a Fact Source

Choose the fact table that contains your measurable events or transactions.

**Fact source selection criteria:**
- Must be a view with semantic usage = "Fact"
- Contains quantitative measures (amounts, counts, quantities)
- Has appropriate grain for analysis (transaction, daily, order level)
- Includes necessary dimensional keys
- Consider data volume and refresh frequency

**Query fact source schema:**
```
Use MCP tool: get_table_schema(fact_view_name)
Returns: column list, data types, key indicators
```

**Fact source example:**
```
SalesOrders Fact View
├── OrderID (Key)
├── OrderDate (Time dimension)
├── CustomerID (Customer dimension key)
├── ProductID (Product dimension key)
├── Amount (Measure)
├── Quantity (Measure)
├── OrderStatus (Attribute)
└── CurrencyCode (Attribute)
```

### Step 2: Add Dimensions

Attach dimensional views that provide analysis context.

**Dimension selection:**
- Customer Dimension → Analyze sales by customer attributes
- Product Dimension → Analyze by product category, brand
- Date Dimension → Analyze over time (month, quarter, year)
- Geography Dimension → Analyze by region, country
- Organization Dimension → Analyze by cost center, department

**Association mapping:**
Each dimension is linked via a foreign key association:
```
SalesOrders.CustomerID → Customer.CustomerID
SalesOrders.ProductID → Product.ProductID
SalesOrders.OrderDate → Date.DateKey
```

**Best practices:**
- Include all business-relevant dimensions
- Verify foreign key relationships exist
- Document dimension hierarchy levels
- Include dimension keys and attributes
- Use search_catalog to discover available dimensions

**Dimension example:**
```
Customer Dimension
├── CustomerID (Key)
├── CustomerName (Attribute)
├── IndustryCode (Attribute)
├── Region (Attribute, drill-down to Country)
├── SalesTerritory (Attribute)
└── CreditLimit (Attribute)
```

### Step 3: Define Measures

Measures are the quantifiable metrics users analyze.

**Measure types:**

#### Simple Measures
Direct aggregation of a fact table column.

**Example:**
```
Measure: Total Sales Amount
Source Column: Amount
Aggregation: SUM
```

**Common simple measures:**
- `SUM(Amount)` → Total revenue, total costs
- `SUM(Quantity)` → Total units sold
- `COUNT(*)` → Number of transactions
- `AVG(Price)` → Average unit price
- `MIN(Discount)` → Minimum discount applied
- `MAX(OrderValue)` → Largest order

#### Calculated Measures
Derived from other measures or columns using expressions.

**Example:**
```
Measure: Average Order Value
Formula: Total Sales Amount / Number of Orders

Measure: Gross Margin
Formula: (Revenue - COGS) / Revenue

Measure: Days to Delivery
Formula: DATEDIFF(day, OrderDate, DeliveryDate)
```

**Expression examples:**
```
# Percentage calculations
Profit_Margin = Net_Profit / Revenue * 100

# Unit economics
Cost_Per_Unit = Total_Cost / Quantity

# Time-based metrics
Days_In_Inventory = 365 / Inventory_Turnover

# Ratio analysis
Debt_To_Equity = Total_Debt / Total_Equity
```

#### Restricted Measures
Aggregation with specific filter conditions.

**Example:**
```
Measure: High-Value Orders
Source: Total Sales Amount
Filter: Amount > 10,000

Measure: On-Time Deliveries
Source: COUNT(OrderID)
Filter: ShipDate <= DueDate

Measure: Completed Orders
Source: COUNT(OrderID)
Filter: Status = 'Completed'
```

**Use cases:**
- Key performance indicators with thresholds
- Subset metrics (Premium customers only)
- Conformance counts (Quality metrics)
- Compliance tracking (Orders meeting SLA)

#### Count Distinct Measures
Count unique values of a dimension key.

**Example:**
```
Measure: Number of Customers
Type: Count Distinct
Column: CustomerID
Result: Unique customer count

Measure: Product Variety
Type: Count Distinct
Column: ProductID
Result: Number of distinct products sold
```

**Performance consideration:**
- Count distinct is expensive on large datasets
- Consider materialization if used frequently
- Avoid combining with many other dimensions in filters

**Measure definition best practices:**
- Use clear, business-friendly names
- Document calculation logic and filters
- Verify aggregation type (SUM vs AVG vs COUNT)
- Test measures with `execute_query` on sample data
- Consider currency and unit attributes
- Define decimal places and formatting

### Step 4: Configure Measure Aggregation Types

Specify how measures combine across dimensions.

**Aggregation types:**

| Type | Behavior | Example |
|------|----------|---------|
| **SUM** | Add values across dimension | Sum of all order amounts = Total revenue |
| **AVG** | Average across dimension | Average order value by customer |
| **MIN** | Minimum value in dimension | Lowest price per product |
| **MAX** | Highest value in dimension | Highest discount offered |
| **COUNT** | Count non-null values | Number of orders |
| **COUNT DISTINCT** | Unique values in dimension | Unique customers |
| **NONE** | No aggregation (detail level) | Exception cases |

**Context-specific aggregation:**
```
Measure: Headcount
SUM by Company (add departments)
AVG by Department (doesn't make sense)
Should use NONE or formula-based

Measure: Salary
AVG by Department (makes sense)
SUM by Department (total payroll)
```

### Step 5: Add Attributes

Attributes provide drill-down paths and detail information for dimensions.

**Attribute examples:**
```
From Customer Dimension:
- CustomerName (detail attribute)
- Industry (classification attribute)
- Region (hierarchy attribute)
- SalesRep (responsibility attribute)

From Product Dimension:
- ProductName (detail)
- Category (classification)
- Brand (classification)
- SkuNumber (identifier)
```

**Hierarchy attributes:**
```
Date Dimension
├── Year (top level)
├── Quarter (drill-down)
├── Month (drill-down)
└── Day (detail level)

Geography Dimension
├── Region (top level)
├── Country (drill-down)
├── Province/State (drill-down)
└── City (detail level)
```

**Best practices:**
- Include all user-facing attributes
- Order logically (hierarchical top-to-bottom)
- Document attribute meanings
- Consider user search/discovery

### Step 6: Define Variables and Input Parameters

Add dynamic filtering for user interaction.

**Variable types:**

#### Prompt Variables
Users select value(s) before executing queries.

**Example:**
```
Variable: FiscalYear
Type: Single-select Prompt
Values: 2022, 2023, 2024
Usage in Measure:
  COUNT(Orders) WHERE FiscalYear = :FiscalYear
```

**Multi-select prompt:**
```
Variable: SelectRegions
Type: Multi-select Prompt
Values: North, South, East, West, Europe
Filter: WHERE Region IN (:SelectRegions)
```

#### Range Variables
Users specify start and end values.

**Example:**
```
Variable: SalesDateRange
Type: Date Range
Filter: WHERE OrderDate BETWEEN :StartDate AND :EndDate
```

**Numeric range:**
```
Variable: OrderAmountRange
Type: Numeric Range
Filter: WHERE Amount >= :MinAmount AND Amount <= :MaxAmount
```

#### Fixed Variables
Predefined values for consistent calculations.

**Example:**
```
Variable: CurrentFiscalYear = YEAR(CURRENT_DATE())
Variable: PriorYear = CurrentFiscalYear - 1
Usage: In measures for year-over-year comparisons
```

**Variable best practices:**
- Provide meaningful default values
- Add descriptive labels and help text
- Consider mandatory vs optional
- Validate ranges (e.g., EndDate > StartDate)
- Document business context

### Step 7: Configure Currency Conversion

Handle multi-currency scenarios.

**Currency conversion setup:**

```
Define source currency column:
├── CurrencyCode (USD, EUR, GBP, etc.)

Define conversion rules:
├── Target currency (e.g., USD for all reporting)
├── Exchange rate source (lookup table, feed)
├── Effective date matching
└── Rounding rules
```

**Currency conversion configuration:**
```
Measure: Revenue (Converted)
Source: Amount
Original Currency: CurrencyCode column
Target Currency: USD
Exchange Rate Source: ExchangeRate.Lookup (SourceCurrency, TargetCurrency, Date)
Conversion Formula: Amount * ExchangeRate
```

**Multi-currency reporting:**
```
Report users can choose reporting currency:
- Filter: :ReportingCurrency = USD/EUR/GBP
- Measures automatically convert to selected currency
- Reconciliation occurs at transaction level
```

**Best practices:**
- Define conversion rules at measure definition time
- Document exchange rate sources
- Handle conversion date logic (transaction date, report date)
- Consider rounding and precision
- Test multi-currency calculations with sample data

### Step 8: Set Up Exception Aggregation Rules

Define special aggregation behavior for specific measures/dimensions.

**Exception aggregation examples:**

#### Measure Exception
Specific measure aggregates differently in certain dimension contexts.

```
Measure: UnitPrice
Normal Aggregation: AVG (average unit price)
Exception with ProductCategory:
- DO NOT average unit prices across product categories
- Use SUM(Amount) / SUM(Quantity) instead (weighted average)
- Prevents misleading aggregations
```

**Use cases:**
- Weighted averages (don't average averages)
- Margin calculations (aggregate costs/revenue separately)
- Retention rates (don't average percentages)

#### Dimension Exception
Dimension behaves differently with certain measures.

```
Measure: Budget (allocated by department)
Normal behavior: SUM across all dimensions
Exception with Date dimension:
- DO NOT sum budgets across months
- Use only budget for the selected month
- Avoid double-counting

Measure: Headcount (point-in-time)
Exception with Organization:
- DO NOT sum headcount across levels
- Use only at lowest level (employees)
```

**Configuration syntax:**
```
Measure: Commission
Base Aggregation: SUM
Exception Rule:
  IF dimension = 'ProductCategory'
  THEN aggregate as NONE (show detail only)
  ELSE aggregate as SUM
```

**Best practices:**
- Document exceptions clearly
- Test aggregations in SAC
- Avoid overly complex rules
- Consider impact on user experience

## Attributes and Their Properties

### Attribute Types

#### Key Attributes
Unique identifiers for dimension members.

```
CustomerID (Key)
├── Used for dimension uniqueness
├── Not aggregated in reports
├── Used for filtering
└── Links to fact table
```

#### Classification Attributes
Categorical properties for grouping.

```
Product Category (Classification)
├── Values: Electronics, Clothing, Food
├── Used for drill-down and filtering
├── Typically aggregates with SUM
└── Creates different data segments
```

#### Hierarchy Attributes
Ordered levels for drill-down paths.

```
Organization Hierarchy:
├── Level 0: Company
├── Level 1: Division
├── Level 2: Department
├── Level 3: Team
└── Level 4: Individual
```

#### Text/Description Attributes
Longer text fields for context.

```
Product Description (Text)
├── Marketing description
├── Not aggregated
├── Read-only in most contexts
└── Useful for report context
```

### Attribute Properties

**Data type:**
- Text (string, variable length)
- Date (ISO format YYYY-MM-DD)
- Number (integer or decimal)
- Boolean (true/false)

**Attribute properties:**
```
Name: ProdCategory
Label: Product Category
Description: "High-level product grouping for analysis"
Data Type: Text
Semantic Role: Classification
Display Length: 50 characters
```

## Variables and Input Parameters

### Variable Definition Patterns

#### Financial Period Variables
```
Variable: SelectedMonth
Type: Single Select
Values: FROM calendar table
Usage: WHERE Month = :SelectedMonth

Variable: FiscalYearRange
Type: Range
Usage: WHERE FiscalYear BETWEEN :StartYear AND :EndYear
```

#### Geographic Variables
```
Variable: SelectedRegion
Type: Multi-Select
Values: North, South, East, West
Usage: WHERE Region IN (:SelectedRegion)

Variable: CountrySubset
Type: Multi-Select
Dynamic Values: FROM Country dimension
```

#### Customer Segment Variables
```
Variable: IndustryFilter
Type: Single Select
Values: Manufacturing, Retail, Service, Government
Usage: WHERE Industry = :IndustryFilter

Variable: MinAnnualRevenue
Type: Numeric
Default: 1000000
Usage: WHERE AnnualRevenue >= :MinAnnualRevenue
```

#### Performance Threshold Variables
```
Variable: TargetGrowthRate
Type: Numeric
Default: 0.10 (10%)
Usage in Measure: IF(GrowthRate >= :TargetGrowthRate, 'On Track', 'At Risk')
```

## SAC Consumption Considerations

### Dashboard Compatibility

**Layout and performance:**
- Keep analytic models focused (8-12 measures optimal)
- Include essential dimensions only
- Test dashboard responsiveness with typical filters
- Consider caching strategies for large datasets

**Filter interaction:**
- Dimension filters must have clear values
- Avoid excessive hierarchy levels (limit to 5)
- Test filter performance in SAC
- Document filter behavior for users

### Self-Service Analytics

**Naming conventions for clarity:**
```
GOOD:
- "Total Sales Revenue (USD)"
- "Customer Acquisition Cost"
- "On-Time Delivery Rate"

AVOID:
- "SAL_AMT"
- "CALC_COST"
- "OTD_PERC"
```

**Measure organization:**
```
Revenue Measures:
├── Total Sales Amount
├── Average Order Value
├── Revenue by Region
└── Year-over-Year Growth

Cost Measures:
├── Total COGS
├── Operating Expenses
└── Cost Per Unit
```

**Documentation for end users:**
```
For each measure, document:
- What it measures
- How it's calculated
- When to use it
- Any limitations or exceptions
- Currency or unit information
```

### Performance Optimization for SAC

**Query optimization:**
- Persist frequently-accessed analytic models
- Pre-aggregate common combinations
- Use SAC query caching
- Test with realistic user loads

**Dimension cardinality:**
```
Low cardinality (good for filters):
- Department (10-20 values)
- Region (5-10 values)

High cardinality (avoid for filtering):
- Customer ID (millions)
- Transaction ID (billions)
```

**Measure calculation placement:**
- Simple aggregations in Fact view
- Complex calculations in Analytic Model
- User-defined calculations in SAC (if acceptable)

## MCP Tools Reference

### get_analytical_metadata
Retrieve structure and properties of existing analytic models.
```
Use to understand existing measure definitions and dimension associations
Helps avoid duplicate measures across models
```

### query_analytical_data
Execute queries against analytic models to validate results.
```
Use to test measures, filters, and dimension combinations
Verify correct aggregation behavior before deployment
```

### search_catalog
Discover fact tables, dimensions, and existing analytic models.
```
Use to find suitable fact sources and dimension tables
Identify reusable components
```

### get_table_schema
Retrieve detailed column information for fact sources.
```
Use before creating measures to understand available data
Verify data types and column names
```

## Key Takeaways

1. **Choose fact sources carefully** — Correct grain and scope determines model usability
2. **Define comprehensive measures** — Simple, calculated, and restricted measures address diverse needs
3. **Include relevant dimensions** — Balance analysis richness with performance
4. **Handle exceptions explicitly** — Complex aggregation rules must be documented
5. **Consider currency and units** — Multi-currency models require explicit configuration
6. **Test in SAC early** — Validate filter behavior and dashboard performance
7. **Document for users** — Clear measure definitions enable self-service analytics
8. **Optimize for consumption** — Simplify complexity; performance matters in dashboards
