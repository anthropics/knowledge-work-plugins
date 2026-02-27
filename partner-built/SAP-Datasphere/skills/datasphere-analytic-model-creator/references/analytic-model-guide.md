# Analytic Model Reference Guide

## Measure Types - Syntax and Examples

### Simple Measures

Simple measures are straightforward aggregations of a single column with a standard aggregation function.

#### SUM Aggregation
```sql
Measure Name: Total Sales Revenue
Source Column: Amount (numeric)
Aggregation: SUM
Syntax: SUM(Amount)
Result: Sums all amount values across selected dimensions

Example Values:
- All Data: $5,234,500
- By Region: North=$1,200,000, South=$2,100,000, Europe=$1,934,500
- By Month: Jan=$425,000, Feb=$398,000, Mar=$456,000
```

#### COUNT Aggregation
```sql
Measure Name: Number of Orders
Source Column: OrderID
Aggregation: COUNT
Syntax: COUNT(OrderID)
Result: Counts non-null order IDs

Example:
- Total Orders: 12,456
- Orders by Customer: Acme=245, Beta=189, Gamma=512
- Orders by Month: Jan=1050, Feb=967, Mar=1123
```

#### COUNT DISTINCT Aggregation
```sql
Measure Name: Unique Customers
Source Column: CustomerID
Aggregation: COUNT(DISTINCT CustomerID)
Syntax: COUNT(DISTINCT CustomerID)
Result: Number of unique customer IDs

Example:
- Total Unique Customers: 3,456
- Unique Customers by Region: North=890, South=1,200, Europe=1,366
- Unique Customers by Product: ProductA=1,234, ProductB=2,100

Performance Note: COUNT DISTINCT can be slow on high-cardinality columns
```

#### AVG Aggregation
```sql
Measure Name: Average Order Value
Source Column: Amount
Aggregation: AVG
Syntax: AVG(Amount)
Result: Average of all amount values

Example:
- Overall Average: $419.42
- Average by Customer Segment: Premium=$892.34, Standard=$305.67, Basic=$187.23
- Average by Product Category: Electronics=$756.89, Clothing=$245.67

Formula: SUM(Amount) / COUNT(OrderID)
Interpretation: Users understand "typical order value"
```

#### MIN/MAX Aggregation
```sql
Measure Name: Minimum Order Value
Source Column: Amount
Aggregation: MIN
Syntax: MIN(Amount)
Result: Smallest order amount

Example:
- Minimum Order: $5.00
- Minimum by Region: North=$10.00, South=$5.00, Europe=$8.50

Measure Name: Maximum Order Value
Source Column: Amount
Aggregation: MAX
Syntax: MAX(Amount)
Result: Largest order amount

Example:
- Maximum Order: $125,400.00
- Maximum by Month: Jan=$95,600, Feb=$125,400, Mar=$87,300
```

---

### Calculated Measures

Calculated measures derive from expressions combining other measures, columns, or functions.

#### Ratio and Percentage Measures
```sql
Measure Name: Profit Margin Percentage
Formula: (NetProfit / Revenue) * 100
Source Measures: NetProfit, Revenue
Syntax: (NetProfit / Revenue) * 100
Result: Percentage profit relative to revenue

Example Calculation:
- NetProfit = $1,000,000
- Revenue = $5,000,000
- Result = (1,000,000 / 5,000,000) * 100 = 20%

Usage: Monitor profitability
Insight: "For every $100 of revenue, we keep $20 as profit"

---

Measure Name: Gross Margin Percentage
Formula: ((Revenue - COGS) / Revenue) * 100
Source Columns: Revenue, COGS (Cost of Goods Sold)
Syntax: ((Revenue - COGS) / Revenue) * 100
Result: Percentage of revenue above product cost

Example:
- Revenue = $100,000
- COGS = $60,000
- Result = ((100,000 - 60,000) / 100,000) * 100 = 40%

Variance Detection:
- Manufacturing: 35% (below target of 40%)
- Retail: 42% (above target of 40%)
```

#### Per-Unit Economics
```sql
Measure Name: Cost Per Unit
Formula: TotalCost / TotalQuantity
Source Measures: TotalCost (SUM of Costs), TotalQuantity (SUM of Quantity)
Syntax: TotalCost / TotalQuantity
Result: Average cost per unit

Example:
- Total Cost = $150,000
- Total Quantity = 5,000 units
- Cost Per Unit = $30.00

Use Case: Track unit economics improvements
- Year 1: $35.00 per unit
- Year 2: $30.00 per unit (14% improvement)

---

Measure Name: Revenue Per Customer
Formula: TotalRevenue / UniqueCustomers
Source Measures: TotalRevenue (SUM), UniqueCustomers (COUNT DISTINCT)
Syntax: TotalRevenue / UniqueCustomers
Result: Average revenue per unique customer

Example:
- Total Revenue = $10,000,000
- Unique Customers = 2,500
- Revenue Per Customer = $4,000

Segment Analysis:
- Premium Customers: $8,500 per customer
- Standard Customers: $2,200 per customer
- Basic Customers: $400 per customer
```

#### Year-over-Year and Growth Measures
```sql
Measure Name: Revenue YoY Growth %
Formula: ((CurrentYear - PriorYear) / PriorYear) * 100
Calculated from: Two instances of Revenue measure with year filters
Syntax: ((RevenueCurrentYear - RevenuePriorYear) / RevenuePriorYear) * 100
Result: Percentage growth year-over-year

Example:
- 2024 Revenue = $12,500,000
- 2023 Revenue = $10,000,000
- YoY Growth = ((12,500,000 - 10,000,000) / 10,000,000) * 100 = 25%

Interpretation: Revenue grew 25% from 2023 to 2024

---

Measure Name: Quarter-over-Quarter Change
Formula: (CurrentQtr - PriorQtr) / PriorQtr
Calculated from: Two instances of Revenue with quarter filters
Example:
- Q2 2024 = $3,200,000
- Q1 2024 = $2,900,000
- QoQ = (3,200,000 - 2,900,000) / 2,900,000 = 10.3%
```

#### Conditional Calculations
```sql
Measure Name: Incentive Payment
Formula: CASE
         WHEN SalesAmount >= 1,000,000 THEN SalesAmount * 0.05
         WHEN SalesAmount >= 500,000 THEN SalesAmount * 0.03
         ELSE 0
         END
Source: SalesAmount measure
Result: Tiered commission/incentive

Example:
- Sales $1,500,000 → Incentive = $75,000 (5%)
- Sales $750,000 → Incentive = $22,500 (3%)
- Sales $250,000 → Incentive = $0

---

Measure Name: Performance Rating
Formula: CASE
         WHEN ActualSales >= TargetSales * 1.1 THEN 'Excellent'
         WHEN ActualSales >= TargetSales THEN 'On Track'
         WHEN ActualSales >= TargetSales * 0.8 THEN 'At Risk'
         ELSE 'Critical'
         END
Result: Categorical performance assessment

Example:
- Target = $1,000,000, Actual = $1,150,000 → 'Excellent' (15% above)
- Target = $1,000,000, Actual = $950,000 → 'On Track' (5% below, within tolerance)
- Target = $1,000,000, Actual = $750,000 → 'At Risk' (25% below)
```

#### Time-Based Calculations
```sql
Measure Name: Average Days to Delivery
Formula: AVG(DATEDIFF(day, OrderDate, DeliveryDate))
Source Columns: OrderDate, DeliveryDate
Result: Average delivery time in days

Example:
- Order Jan 15, Delivered Jan 18 = 3 days
- Order Jan 16, Delivered Jan 20 = 4 days
- Average = 3.5 days

Use Case: Service level tracking
- Target: 5 days
- Actual: 4.2 days (exceeding SLA)

---

Measure Name: Days Sales Outstanding (DSO)
Formula: (AvgAccountsReceivable / DailySales)
Approximation: (365 * AccountsReceivable) / Revenue
Interpretation: Average days to collect payment

Example Calculation:
- Annual Revenue = $10,000,000
- Average AR Balance = $1,500,000
- DSO = (365 * 1,500,000) / 10,000,000 = 54.75 days

Trend Analysis:
- Month 1: 60 days (slow collections)
- Month 2: 55 days (improving)
- Month 3: 50 days (on track)
```

---

### Restricted Measures

Restricted measures are aggregations with built-in filters, creating subset-specific metrics.

#### Threshold-Based Restrictions
```sql
Measure Name: High-Value Orders
Definition: COUNT of Orders where Amount >= $10,000
Source: OrderCount measure (COUNT(OrderID))
Filter: WHERE Amount >= 10000
Result: Count of orders above threshold

Example:
- Total Orders: 5,000
- High-Value Orders: 342
- Percentage: 6.84%

Use Case: Track premium transaction volume
Split by Sales Rep:
- Rep A: 45 high-value orders
- Rep B: 67 high-value orders
- Rep C: 28 high-value orders
```

#### Status-Based Restrictions
```sql
Measure Name: Completed Orders
Definition: SUM(Amount) where Status = 'Completed'
Source: Revenue measure (SUM(Amount))
Filter: WHERE OrderStatus = 'Completed'
Result: Revenue from only completed transactions

Example:
- Total Orders Revenue: $5,234,500 (includes pending, cancelled)
- Completed Orders: $4,987,234 (excludes non-completed)

Status Breakdown:
- Completed: $4,987,234 (95.3%)
- Pending: $189,456 (3.6%)
- Cancelled: $57,810 (1.1%)

---

Measure Name: On-Time Deliveries
Definition: COUNT(OrderID) where ShipDate <= DueDate
Filter: WHERE ShipDate <= DueDate
Result: Count of orders delivered on time

Example:
- Total Orders: 1,200
- On-Time: 1,050
- Late: 150
- On-Time Rate: 87.5%

Regional Performance:
- North: 91% on-time
- South: 85% on-time
- Europe: 83% on-time
```

#### Conformance and Compliance Restrictions
```sql
Measure Name: Approved Invoices
Definition: SUM(InvoiceAmount) where ApprovalStatus = 'Approved'
Filter: WHERE ApprovalStatus = 'Approved'
Result: Total amount of invoices meeting approval criteria

Example:
- Total Invoiced: $1,500,000
- Approved: $1,450,000 (96.7%)
- Pending Review: $35,000 (2.3%)
- Rejected: $15,000 (1.0%)

---

Measure Name: Quality Pass Rate
Definition: COUNT(InspectionID) where QualityScore >= 95
Filter: WHERE QualityScore >= 95
Result: Count of items passing quality threshold

Example:
- Total Items Inspected: 10,000
- Quality Pass: 9,750
- Quality Pass Rate: 97.5%

Quality Trend:
- Q1: 95.2%
- Q2: 96.8%
- Q3: 97.5% (improving)
```

#### Combination Restrictions
```sql
Measure Name: Large Orders from Key Customers
Definition: SUM(Amount) where Amount >= 50000 AND CustomerSegment = 'Key'
Filter: WHERE Amount >= 50000 AND CustomerSegment = 'Key'
Result: Revenue from large orders of key accounts

Example Calculation:
- Total Revenue: $10,000,000
- Large Orders (>$50K): $6,500,000
- Large Orders from Key Customers: $5,800,000 (89% of large orders)

Business Insight: Key customers represent significant large order volume
```

---

### Count Distinct Measures

Count distinct measures identify unique members of a dimension.

#### Customer Counting
```sql
Measure Name: Number of Unique Customers
Definition: COUNT(DISTINCT CustomerID)
Source Column: CustomerID
Result: Count of unique customers

Example:
- Total Transactions: 50,000
- Unique Customers: 3,200
- Avg Transactions per Customer: 15.6

Segmentation:
- Premium Customers: 120
- Standard Customers: 1,050
- Basic Customers: 2,030

Trend:
- Year 1: 2,500 unique customers
- Year 2: 3,200 unique customers (28% growth)
```

#### Product/SKU Counting
```sql
Measure Name: Product Variety Sold
Definition: COUNT(DISTINCT ProductID)
Source Column: ProductID
Result: Number of unique products sold

Example:
- Total Product Catalog: 5,000 SKUs
- Products Sold This Year: 1,200 (24% of catalog)
- Products Sold by Region: North=650, South=480, Europe=720

Use Case: Assortment analysis
- High-selling products: 50 SKUs (40% of revenue)
- Tail products: 1,150 SKUs (60% of revenue)
```

#### Unique Time Period Counting
```sql
Measure Name: Days with Sales Activity
Definition: COUNT(DISTINCT OrderDate)
Source Column: OrderDate
Result: Number of unique days with orders

Example:
- Total Days in Year: 365
- Days with Sales: 310 (85% of days)
- Average Orders per Day: 32.3

Use Case: Operational analysis
- Monday: 98% days with activity
- Friday: 92% days with activity
- Weekend: 15% days with activity
```

#### Supplier/Vendor Counting
```sql
Measure Name: Active Supplier Count
Definition: COUNT(DISTINCT SupplierID)
Source Column: SupplierID
Result: Number of active suppliers

Example:
- Total Registered Suppliers: 500
- Active Suppliers (has shipments this period): 180 (36%)
- Average Purchases per Supplier: 27.8

Risk Assessment:
- Primary suppliers (80% of value): 15 suppliers
- Secondary suppliers (20% of value): 165 suppliers
- Diversity is important for supply chain resilience
```

---

## Aggregation Types - Complete Reference

| Aggregation | Input | Output | When Used | Example |
|---|---|---|---|---|
| **SUM** | Numeric values | Total | Amounts, quantities, costs | SUM(InvoiceAmount) = $1,500,000 |
| **AVG** | Numeric values | Mean | Unit prices, rates, percentages | AVG(UnitPrice) = $45.50 |
| **COUNT** | Any column | Integer count | Number of transactions | COUNT(OrderID) = 5,432 |
| **COUNT DISTINCT** | Any column with duplicates | Unique count | Unique customers, products | COUNT(DISTINCT CustomerID) = 1,200 |
| **MIN** | Comparable values | Minimum | Lowest price, earliest date | MIN(OrderDate) = 2024-01-01 |
| **MAX** | Comparable values | Maximum | Highest discount, latest date | MAX(Amount) = $95,600 |
| **STDDEV** | Numeric values | Standard deviation | Variability, risk measurement | STDDEV(SalesAmount) = $12,450 |
| **VARIANCE** | Numeric values | Variance | Spread of data points | VARIANCE(Price) = 156.25 |

---

## Exception Aggregation Patterns

Exception aggregation rules define how specific measures behave when combined with certain dimensions.

### Pattern 1: Weighted Average Exception

**Scenario:** Unit prices should not be averaged across product categories.

```
Measure: Unit Price
Normal Aggregation: AVG(Price)

Exception Rule:
When dimension = ProductCategory
  Aggregate as: SUM(TotalAmount) / SUM(TotalQuantity)
  Instead of: AVG(Price)

Why: Taking an average of averages is mathematically incorrect
Example:
  Category A: 100 units at $10 (average) = $1,000 total
  Category B: 50 units at $20 (average) = $1,000 total

  Wrong: AVG(10, 20) = $15
  Correct: (1,000 + 1,000) / (100 + 50) = $13.33

Dashboard Impact:
  Without exception: Misleading $15 per unit price
  With exception: Correct $13.33 weighted unit price
```

### Pattern 2: Point-in-Time Exception

**Scenario:** Headcount and inventory are point-in-time measures; don't sum across periods.

```
Measure: Employee Headcount
Normal Aggregation: SUM(EmployeeCount)

Exception Rule:
When dimension = Date or Time Period
  Aggregate as: NONE (show detail only)
  Instead of: SUM

Why: Summing headcount across months is meaningless
Example:
  Jan Headcount: 100 employees
  Feb Headcount: 105 employees
  Mar Headcount: 110 employees

  Wrong Sum: 315 (meaningless)
  Correct: Show each month separately, user interprets trend

---

Measure: Inventory On Hand
Normal Aggregation: SUM(Quantity)

Exception Rule:
When dimension = Date or Month
  Show: Last day of period balance only
  Not: Sum of all daily balances

Why: Inventory is measured at a point in time
Example:
  Month-end inventory is meaningful (stock available)
  Sum of daily inventory is meaningless (double-counting)
```

### Pattern 3: Ratio Exceptions

**Scenario:** Percentages and rates should not be averaged; recalculate from components.

```
Measure: Profit Margin %
Formula: (NetProfit / Revenue) * 100
Normal Aggregation: Uses formula components

Exception Rule:
When combining dimensions (e.g., Region and Product)
  Recalculate as: SUM(AllProfit) / SUM(AllRevenue) * 100
  Not: AVG(ProfitMarginByRegion)

Why: Averaging percentages loses context
Example:
  Region North: 50 units, $1,000 profit, 5% margin
  Region South: 100 units, $500 profit, 1% margin

  Wrong: AVG(5%, 1%) = 3%
  Correct: ($1,000 + $500) / ($20,000 + $50,000) = 1.75%

Dashboard Implementation:
  Raw measure: Use components (profit, revenue)
  Calculated measure: Apply formula
  Exception: Prevent aggregation of percentages
```

### Pattern 4: Subset Measure Exception

**Scenario:** When combining restricted and unrestricted measures.

```
Measure: Total Revenue
Source: SUM(Amount) with no filter

Measure: Online Revenue
Source: SUM(Amount) where SalesChannel = 'Online'

Exception Rule:
Cannot calculate: Online Revenue / Total Revenue at certain dimension levels
  Problem: Different denominator causes meaningless results
  Solution: Only calculate this ratio at specific dimension levels (e.g., by Product)

Dashboard Pattern:
  Show Total Revenue and Online Revenue side-by-side
  Calculate ratio only when both dimensions align
```

---

## Currency and Unit Conversion Configuration

### Multi-Currency Setup

**Configuration structure:**
```
Dimension: TransactionCurrency (from fact table)
Values: USD, EUR, GBP, JPY, CAD, AUD

Measure: Amount (in transaction currency)

Conversion Method:
1. Define exchange rate source
2. Apply conversion at query time
3. Display in target currency
```

**Exchange rate source example:**
```
ExchangeRates Table:
├── SourceCurrency (USD, EUR, GBP)
├── TargetCurrency (reporting currency)
├── ExchangeRate (conversion ratio)
├── EffectiveDate (when rate became valid)
└── SourceSystem (Reuters, ECB, Internal)

Example Data:
| SourceCurrency | TargetCurrency | ExchangeRate | EffectiveDate |
| USD            | EUR            | 0.92         | 2024-01-01    |
| GBP            | EUR            | 1.17         | 2024-01-01    |
| JPY            | EUR            | 0.0067       | 2024-01-01    |
```

**Conversion formula in measure:**
```
Measure: Revenue (EUR)
Formula: Amount * ExchangeRate
Lookup: ExchangeRates.ExchangeRate
  WHERE SourceCurrency = TransactionCurrency
  AND TargetCurrency = 'EUR'
  AND EffectiveDate <= TransactionDate
  ORDER BY EffectiveDate DESC
  LIMIT 1 (most recent rate)
```

**Conversion date logic:**
```
Spot Rate Method (Transaction date):
- Convert using rate effective on transaction date
- Most accurate for financial reporting
- Requires historical rate table

Period-End Rate Method (Reporting date):
- Convert all transactions using month-end rate
- Simpler, used for P&L reporting
- May create volatility month-to-month
```

### Unit Conversion

**Unit conversion configuration:**
```
Measure: Quantity Sold (units)

Conversion Rules:
├── Base Unit: Pieces
├── Alternative Units: Dozen, Box, Pallet
├── Conversion Factors:
│   ├── 1 Dozen = 12 Pieces
│   ├── 1 Box = 24 Pieces
│   ├── 1 Pallet = 120 Boxes = 2,880 Pieces

Measure: Quantity (Dozens)
Formula: Quantity (units) / 12

Measure: Weight
├── Base Unit: Kilograms
├── Conversions:
│   ├── 1 Ton = 1,000 KG
│   ├── 1 Pound = 0.454 KG
│   ├── 1 Ounce = 0.0283 KG
```

**Mixed unit reporting:**
```
User selects reporting unit:
└─ [Dropdown: Pieces | Dozen | Box | Pallet]

System calculates:
- Formula-based conversion
- Display with appropriate unit label
- Rounding rules per unit type

Example:
Quantity = 500 Pieces
- In Pieces: 500
- In Dozen: 41.67 (rounded to 42)
- In Box: 20.83 (rounded to 21)
- In Pallet: 1.74 (rounded to 2)
```

---

## Variable Types and Usage Patterns

### Single Select Variable
```
Variable Definition:
├── Name: SelectedRegion
├── Label: Choose Region
├── Type: Single Select
├── Values: North, South, East, West, Europe
├── Default: North
└── Mandatory: Yes

Usage in Measure:
WHERE Region = :SelectedRegion

Dashboard Behavior:
- Dropdown with 5 options
- User selects one before query execution
- Entire dashboard filtered by selection
```

### Multi-Select Variable
```
Variable Definition:
├── Name: SelectedSalesReps
├── Label: Filter by Sales Representatives
├── Type: Multi-Select
├── Values: [List of 200+ reps]
├── Default: All
└── Mandatory: No

Usage in Measure:
WHERE SalesRepID IN (:SelectedSalesReps)

Dashboard Behavior:
- Multi-select list or checkbox group
- User selects multiple reps
- OR logic combines selections
- Empty selection = All reps
```

### Range Variable
```
Variable Definition (Numeric):
├── Name: SalesAmountRange
├── Label: Order Amount Range
├── Type: Range
├── Min Value: 0
├── Max Value: 1,000,000
├── Default Min: 0
├── Default Max: 100,000
└── Step: 1,000

Usage in Measure:
WHERE Amount >= :MinAmount AND Amount <= :MaxAmount

Variable Definition (Date):
├── Name: DateRange
├── Label: Order Date Range
├── Type: Date Range
├── Default Start: First day of current month
├── Default End: Last day of current month
└── Format: YYYY-MM-DD

Usage in Measure:
WHERE OrderDate >= :StartDate AND OrderDate <= :EndDate
```

### Hierarchical Variable
```
Variable Definition:
├── Name: OrganizationLevel
├── Label: Organization Hierarchy
├── Type: Hierarchical Select
├── Hierarchy: Company → Division → Department → Team
├── Default: Company level
└── Allow drill-down: Yes

Usage:
- User sees Company names
- On selection, displays Divisions
- On Division selection, displays Departments
- Drill-down continues through hierarchy
```

### Fixed Variable (Formula-Based)
```
Variable Definition:
├── Name: CurrentFiscalYear
├── Type: Fixed (Calculated)
├── Formula: YEAR(CURRENT_DATE())
├── Updated: Automatically daily

Usage in Measure:
WHERE FiscalYear = :CurrentFiscalYear

Example Calculations:
├── PriorYear = :CurrentFiscalYear - 1
├── CurrentMonthFirstDay = DATE_TRUNC('month', CURRENT_DATE())
├── LastDayOfMonth = LAST_DAY(CURRENT_DATE())
└── QuarterStart = DATE_TRUNC('quarter', CURRENT_DATE())
```

---

## Best Practices for SAC Compatibility

### Measure Definition Best Practices

1. **Naming Convention**
   ```
   Good names:
   - "Total Sales Revenue"
   - "Customer Acquisition Cost"
   - "On-Time Delivery Rate"

   Avoid:
   - Acronyms without context (SAL_AMT, CAC, OTD)
   - Technical names (SUM_FACT_000123)
   - Vague names (VALUE, AMOUNT, DATA)
   ```

2. **Documentation**
   ```
   For each measure, document:
   - Definition: "Sum of all invoice amounts for completed orders"
   - Calculation: "SUM(InvoiceAmount) WHERE OrderStatus='Completed'"
   - Aggregation Type: "SUM"
   - Currency/Unit: "USD"
   - Limitations: "Excludes cancelled orders"
   - Last Updated: "2024-02-01"
   - Owner: "Finance Team"
   ```

3. **Aggregation Clarity**
   ```
   Specify default aggregation:

   Measure: Revenue
   ├── Default Agg: SUM (sum across regions, products)
   ├── Don't Sum: (leave as detail for certain dimensions)

   Measure: Unit Price
   ├── Default Agg: AVG
   ├── Exception: Use weighted average by product category
   ```

### Dimension and Attribute Organization

```
Dimension: ProductDimension
├── Keys and IDs
│   ├── ProductID
│   └── SKUNumber
├── Classification
│   ├── ProductCategory
│   ├── ProductSubcategory
│   └── Brand
├── Attributes
│   ├── ProductName
│   ├── Description
│   └── ListPrice
└── Hierarchy Levels
    ├── Category (Level 0)
    ├── Subcategory (Level 1)
    └── Product (Level 2)
```

### Performance Optimization

```
Measure Complexity Levels:

Level 1 (Simple, Fast):
- Simple aggregations (SUM, COUNT)
- Single column operations
- Expected query time: <1 second

Level 2 (Moderate, Acceptable):
- Calculated measures with 2-3 components
- Restricted measures with filters
- Expected query time: 1-5 seconds

Level 3 (Complex, Use Carefully):
- Multiple calculated components
- Complex window functions
- Count distinct on high-cardinality columns
- Expected query time: 5-30 seconds

Recommendation:
- Avoid Level 3 measures in interactive dashboards
- Use for scheduled reports only
- Consider materialization/persistence
```

---

## Troubleshooting Common Issues

### Aggregation Problems

**Issue: Measures don't add up correctly**
```
Symptom: Region A $100K + Region B $200K ≠ Total $300K

Cause: Unit price averaging issue
- Dimension level shows average unit prices
- But those aren't weighted by volume

Solution: Use exception aggregation rule
- Don't average prices across regions
- Recalculate from sum(amount) / sum(quantity)
```

**Issue: Data appears duplicated**
```
Symptom: Total $500K + Restricted measure $500K = $1M (should be $500K total)

Cause: N:N join cardinality explosion
- Join between fact and dimension creates duplicate rows
- Each duplicate counted separately

Solution: Verify join cardinality
- Should be N:1 (many orders to one customer)
- Not N:N (many orders to many dimension members)
- Check for incorrect join conditions
```

### Performance Issues

**Slow count distinct measures**
```
Cause: COUNT(DISTINCT CustomerID) on billions of rows

Solutions:
1. Create materialized view with daily customer counts
2. Pre-aggregate distinct counts at lower granularity
3. Archive old data before querying
4. Use approximate count algorithms
```

**Dashboard filter lag**
```
Cause: High-cardinality dimension with millions of values

Solutions:
1. Limit dimension values shown (top 100, not all)
2. Use hierarchical navigation instead of flat list
3. Implement search/autocomplete for selection
4. Create separate filtered dimension for dashboards
```
