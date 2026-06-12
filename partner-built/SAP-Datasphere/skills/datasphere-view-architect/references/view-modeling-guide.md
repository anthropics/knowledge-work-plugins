# View Modeling Reference Guide

## Semantic Usage Types - Detailed Reference

### Fact Entity

**Definition:** Contains measures and quantitative data that is aggregated and analyzed across dimensions.

**Key characteristics:**
- Contains numeric measures (amounts, counts, weights, durations)
- Supports COUNT, SUM, AVG, MIN, MAX aggregations
- Typically at the grain of transactions or events
- Can have multiple fact tables with different grains
- Referenced by Analytic Models as primary source

**Data structure example:**
```
OrderID (Key)          | OrderDate | CustomerID | ProductID | Amount | Quantity | ShipDate
123                    | 2024-01-15| 456       | 789       | 1500   | 10       | 2024-01-18
124                    | 2024-01-15| 457       | 790       | 2300   | 15       | 2024-01-19
```

**When NOT to use:**
- Contains primarily text/descriptions (use Dimension or Text)
- Data doesn't change frequently enough for aggregation
- Only used for lookups (use Dimension instead)

---

### Dimension Entity

**Definition:** Provides descriptive context and attributes for analysis. Slower-changing reference data.

**Key characteristics:**
- Contains categorical and descriptive attributes
- Typically has a business key (unique identifier)
- Can be hierarchical (category → subcategory → product)
- Associated with one or more Fact tables
- Should be relatively stable (infrequent changes)

**Data structure example:**
```
ProductID (Key) | ProductName      | Category    | Subcategory | UnitPrice | Supplier
789            | Widget Pro       | Widgets     | Premium     | 150       | SuppCo A
790            | Widget Standard  | Widgets     | Standard    | 89        | SuppCo B
791            | Gadget Deluxe    | Gadgets     | Premium     | 299       | SuppCo A
```

**Associated Text Entity example:**
```
ProductID | Language | Description
789       | EN       | Professional-grade widget with advanced features
789       | DE       | Professionelles Widget mit erweiterten Funktionen
790       | EN       | Cost-effective widget for general use
790       | DE       | Kostengünstiges Widget für den allgemeinen Gebrauch
```

**Hierarchy example (Product Hierarchy):**
```
ProductHierarchyKey | ProductID | ParentProductID | HierarchyLevel | OrderNumber
PH-001             | 789       | 100            | 1              | 1
PH-002             | 100       | NULL           | 0              | 1
PH-003             | 790       | 100            | 1              | 2
```

---

### Text Entity

**Definition:** Contains language-specific translations and descriptions for other entities.

**Key characteristics:**
- Language-dependent content
- Associated with a parent entity (usually Dimension or Fact)
- Structure: Entity Key + Language Key + Text content
- Used for multi-language reporting
- Cannot have measures

**Data structure example:**
```
CustomerID | Language | CustomerName_Text       | AddressLine1_Text
456        | EN       | Acme Corporation       | 123 Main Street
456        | DE       | Acme Konzern           | Hauptstraße 123
456        | FR       | Société Acme           | 123 rue Principale
457        | EN       | Beta Industries        | 456 Oak Avenue
457        | DE       | Beta Industrien        | Eichenallee 456
```

**Usage in reporting:**
```
Users see:
EN: "Acme Corporation" → "123 Main Street"
DE: "Acme Konzern" → "Hauptstraße 123"
FR: "Société Acme" → "123 rue Principale"
```

---

### Hierarchy Entity

**Definition:** Defines parent-child relationships for drill-down and roll-up analysis.

**Key characteristics:**
- Represents organizational or categorical hierarchies
- Contains hierarchy key, member key, parent key
- Supports drill-down in analytics (Level 0 → Level 1 → Level 2)
- Can be recursive or balanced
- Includes order/sequence information

**Data structure example (Organizational Hierarchy):**
```
OrgHierarchyKey | EmployeeID | ParentEmployeeID | DepartmentName      | Level
1               | 100        | NULL            | Chief Executive     | 0
2               | 200        | 100             | Chief Financial     | 1
3               | 300        | 100             | Chief Operating     | 1
4               | 250        | 200             | Accounting Manager  | 2
5               | 260        | 200             | Finance Manager     | 2
6               | 251        | 250             | Accountant          | 3
```

**Drill-down path:** CEO → CFO → Finance Manager → Accountant

**Data structure example (Geography Hierarchy):**
```
GeoHierarchyKey | CountryCode | CountryName | RegionCode | RegionName | CityCode | CityName
1               | US         | United States| CA        | California | SF       | San Francisco
2               | US         | United States| CA        | California | LA       | Los Angeles
3               | US         | United States| NY        | New York   | NYC      | New York
4               | CA         | Canada      | ON        | Ontario    | TO       | Toronto
```

---

### Relational Dataset

**Definition:** Data used for distribution, integration, or operational purposes, not for analytical aggregation.

**Key characteristics:**
- No aggregation semantics
- Used for operational reporting or data export
- Cannot be source for Analytic Model
- Useful as intermediate transformation layer
- Supports full outer join semantics

**Use cases:**
- Customer contact lists for CRM exports
- Transaction audit logs for compliance
- Master data interfaces for upstream systems
- Data distribution feeds
- Non-analytical reporting views

---

## Join Types - Detailed Reference

### INNER JOIN

**Syntax:**
```sql
SELECT * FROM Orders o
INNER JOIN Customers c ON o.CustomerID = c.CustomerID
```

**Result visualization:**
```
Orders:        Customers:       Result:
O1-C1          C1-Acme          O1-C1-Acme
O2-C1          C2-Beta          O2-C1-Acme
O3-C2          C3-Gamma         O3-C2-Beta
                               (matches only)
```

**When to use:**
- Only want data where both tables match
- Filtering out unmatched records is acceptable
- Customer orders (exclude customers with no orders)
- Invoice line items (exclude invoices with no lines)

**Performance:** Generally fast, filters rows early

---

### LEFT OUTER JOIN

**Syntax:**
```sql
SELECT * FROM Customers c
LEFT OUTER JOIN Orders o ON c.CustomerID = o.CustomerID
```

**Result visualization:**
```
Customers:    Orders:          Result:
C1-Acme       O1-C1            C1-Acme-O1
C2-Beta       O2-C1            C1-Acme-O2
C3-Gamma      O3-C2            C2-Beta-O3
                               C3-Gamma-NULL
```

**When to use:**
- All records from left table are important
- Right table may not have matching records
- All customers, whether they have orders or not
- All products, whether they've been sold or not

**NULL handling:** Right table columns will be NULL where no match exists

---

### RIGHT OUTER JOIN

**Syntax:**
```sql
SELECT * FROM Customers c
RIGHT OUTER JOIN Orders o ON c.CustomerID = o.CustomerID
```

**Result visualization:**
```
Customers:    Orders:          Result:
C1-Acme       O1-C1            O1-C1-Acme
C2-Beta       O2-C1            O2-C1-Acme
C3-Gamma      O3-C2            O3-C2-Beta
              O4-C99           O4-C99-NULL
```

**When to use:**
- Right table records are the primary source
- Want all right table records, some left may not match
- Rare in data modeling; usually rewrite with LEFT JOIN and swap table order

---

### FULL OUTER JOIN

**Syntax:**
```sql
SELECT * FROM Customers c
FULL OUTER JOIN Orders o ON c.CustomerID = o.CustomerID
```

**Result visualization:**
```
Customers:    Orders:          Result:
C1-Acme       O1-C1            C1-Acme-O1
C2-Beta       O2-C1            C1-Acme-O2
C3-Gamma      O3-C2            C2-Beta-O3
              O4-C99           C3-Gamma-NULL
                               O4-C99-NULL
```

**When to use:**
- Reconciliation queries (all from both sides)
- Outer join of independent datasets
- Finding unmatched records in either table

**Performance:** Most expensive join type, retains all rows from both tables

---

### CROSS JOIN

**Syntax:**
```sql
SELECT * FROM DimDate d
CROSS JOIN DimProducts p
WHERE d.Year = 2024
```

**Result visualization:**
```
DimDate:      DimProducts:     Result (no join condition):
2024-01-01    Product A        2024-01-01-Product A
2024-01-02    Product B        2024-01-01-Product B
2024-01-03    Product C        2024-01-02-Product A
              Product D        2024-01-02-Product B
                               ... (many combinations)
```

**When to use:**
- Creating all possible combinations
- Generating complete date-product matrix
- Budget allocation across products
- Forecasting scenarios

**Warning:** Result size = left rows × right rows. Can create millions of rows!

---

## Calculated Column Expressions - Syntax Reference

### String Functions

```sql
-- Concatenation
'Customer: ' || CUSTOMER_NAME || ' (' || COUNTRY || ')'
CONCAT(FIRST_NAME, ' ', LAST_NAME)

-- Case conversion
UPPER(PRODUCT_NAME)                    -- 'product' → 'PRODUCT'
LOWER(DESCRIPTION)                     -- 'UPPER' → 'upper'
INITCAP(CITY_NAME)                     -- 'new york' → 'New York'

-- String manipulation
SUBSTRING(SKU_CODE, 1, 3)              -- First 3 characters
LENGTH(PRODUCT_CODE)                   -- Number of characters
TRIM(CUSTOMER_NAME)                    -- Remove leading/trailing spaces
LTRIM(VALUE)                           -- Remove leading spaces
RTRIM(VALUE)                           -- Remove trailing spaces
REPLACE(DESCRIPTION, 'Old', 'New')     -- Find and replace

-- Pattern matching
POSITION('ABC' IN PRODUCT_CODE)        -- Find position of substring
INSTR(CUSTOMER_NAME, 'Inc')            -- Index of substring
LIKE '%Corp%'                          -- Pattern matching (use in WHERE)

-- String extraction
LEFT(ACCOUNT_CODE, 2)                  -- Leftmost n characters
RIGHT(ACCOUNT_CODE, 4)                 -- Rightmost n characters
MID(CODE, 2, 3)                        -- Extract n chars starting at position

-- Encoding/Decoding
HEX(DATA)                              -- Convert to hexadecimal
UNHEX(HEX_VALUE)                       -- Convert from hexadecimal
```

### Numeric Functions

```sql
-- Rounding
ROUND(PRICE, 2)                        -- Round to 2 decimals: 19.555 → 19.56
FLOOR(AMOUNT)                          -- Round down: 19.9 → 19
CEIL(AMOUNT)                           -- Round up: 19.1 → 20
TRUNCATE(VALUE, 1)                     -- Truncate to 1 decimal: 19.99 → 19.9

-- Sign and absolute value
ABS(VARIANCE)                          -- Absolute value: -150 → 150
SIGN(DIFFERENCE)                       -- Return -1, 0, or 1
SQRT(VARIANCE_SQUARED)                 -- Square root

-- Trigonometry
SIN(ANGLE), COS(ANGLE), TAN(ANGLE)    -- Trigonometric functions
ASIN(), ACOS(), ATAN()                 -- Inverse trigonometric

-- Logarithms
LOG(VALUE)                             -- Natural logarithm
LOG10(VALUE)                           -- Base-10 logarithm
EXP(POWER)                             -- e raised to power

-- Power and modulo
POWER(BASE, EXPONENT)                  -- 2 raised to power 3 = 8
MOD(17, 5)                             -- Remainder: 17 mod 5 = 2
GREATEST(10, 20, 5)                    -- Maximum of values: 20
LEAST(10, 20, 5)                       -- Minimum of values: 5

-- Random numbers
RAND()                                 -- Random decimal 0-1
RANDINT(1, 100)                        -- Random integer 1-100
```

### Date Functions

```sql
-- Current date/time
CURRENT_DATE                           -- Today: 2024-01-15
CURRENT_TIMESTAMP                      -- Now: 2024-01-15 14:30:45.123
CURRENT_TIME                           -- Time: 14:30:45

-- Date arithmetic
DATE_ADD(ORDER_DATE, INTERVAL 30 DAY)  -- Add 30 days
DATE_SUB(DELIVERY_DATE, INTERVAL 1 WEEK) -- Subtract 1 week
DATEDIFF(day, ORDER_DATE, DELIVERY_DATE) -- Days between dates: 5
DATEDIFF(month, START_DATE, END_DATE)  -- Months between dates

-- Date extraction
YEAR(INVOICE_DATE)                     -- Extract year: 2024
MONTH(INVOICE_DATE)                    -- Extract month: 6
DAY(INVOICE_DATE)                      -- Extract day: 15
QUARTER(INVOICE_DATE)                  -- Extract quarter: 2
WEEK(INVOICE_DATE)                     -- Week of year: 24
DAYNAME(ORDER_DATE)                    -- Day name: 'Monday'
MONTHNAME(ORDER_DATE)                  -- Month name: 'June'

-- Date formatting
TO_DATE(DATE_STRING, 'YYYY-MM-DD')     -- Parse string to date
TO_CHAR(ORDER_DATE, 'YYYY-MM-DD')      -- Format date as string

-- Quarter and fiscal calculations
'Q' || QUARTER(DATE_COLUMN)            -- 'Q1', 'Q2', etc.
YEAR(DATE_COLUMN) * 10000 + MONTH(DATE_COLUMN) * 100 + DAY(DATE_COLUMN) -- YYYYMMDD
```

### Conditional Functions

```sql
-- Simple CASE
CASE WHEN AMOUNT > 1000 THEN 'Large'
     WHEN AMOUNT > 100 THEN 'Medium'
     ELSE 'Small'
END

-- Searched CASE
CASE WHEN STATUS = 'ACTIVE' AND AMOUNT > 0 THEN 'Valid'
     WHEN STATUS = 'INACTIVE' THEN 'Closed'
     ELSE 'Unknown'
END

-- IF alternative
IF(QUANTITY > 0, AMOUNT / QUANTITY, 0)  -- Avoid division by zero

-- COALESCE (return first non-NULL)
COALESCE(UPDATED_DATE, CREATED_DATE, SYSTEM_DATE)  -- Use first available

-- NULL handling
IFNULL(COMMISSION, 0)                   -- Replace NULL with 0
NULLIF(VALUE1, VALUE2)                  -- Return NULL if equal, else VALUE1
```

### Aggregate Functions (Window Functions)

```sql
-- Running totals and averages
SUM(AMOUNT) OVER (PARTITION BY CUSTOMER_ID ORDER BY ORDER_DATE)
-- Running total of sales per customer

AVG(PRICE) OVER (PARTITION BY PRODUCT_CATEGORY)
-- Average price within each category

-- Ranking
ROW_NUMBER() OVER (PARTITION BY CUSTOMER_ID ORDER BY ORDER_DATE DESC)
-- Row number per customer, newest orders first

RANK() OVER (ORDER BY SALES_AMOUNT DESC)
-- Rank with gaps (1, 2, 2, 4)

DENSE_RANK() OVER (ORDER BY SALES_AMOUNT DESC)
-- Rank without gaps (1, 2, 2, 3)

-- Lead and lag
LAG(AMOUNT, 1) OVER (PARTITION BY CUSTOMER_ID ORDER BY DATE)
-- Previous order amount for each customer

LEAD(AMOUNT, 1) OVER (PARTITION BY CUSTOMER_ID ORDER BY DATE)
-- Next order amount for each customer

-- First and last values
FIRST_VALUE(AMOUNT) OVER (PARTITION BY CUSTOMER_ID ORDER BY DATE)
-- First purchase amount per customer

LAST_VALUE(AMOUNT) OVER (PARTITION BY CUSTOMER_ID ORDER BY DATE)
-- Last purchase amount per customer
```

---

## Filter Expressions - Reference

### Date Range Filters

```sql
-- Single month
INVOICE_DATE >= '2024-01-01' AND INVOICE_DATE < '2024-02-01'

-- Year to date
INVOICE_DATE >= '2024-01-01' AND INVOICE_DATE <= CURRENT_DATE

-- Last 90 days
INVOICE_DATE >= CURRENT_DATE - 90

-- Fiscal year (April-March)
CASE WHEN MONTH(ORDER_DATE) >= 4
     THEN YEAR(ORDER_DATE)
     ELSE YEAR(ORDER_DATE) - 1
END = 2024

-- Relative filters
ORDER_DATE >= DATE_ADD(CURRENT_DATE, INTERVAL -30 DAY)  -- Last 30 days
DELIVERY_DATE >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)  -- Last month
```

### Categorical Filters

```sql
-- Single value
STATUS = 'ACTIVE'
REGION = 'North America'

-- Multiple values
COUNTRY IN ('USA', 'Canada', 'Mexico')
PRODUCT_LINE IN (SELECT PRODUCT_LINE_ID FROM APPROVED_LINES)

-- Exclusions
DEPARTMENT NOT IN ('Discontinued', 'Testing')
STATUS <> 'INACTIVE'

-- Null/empty handling
CUSTOMER_EMAIL IS NOT NULL
MIDDLE_NAME IS NULL
DESCRIPTION <> ''
```

### Numeric Range Filters

```sql
-- Simple ranges
AMOUNT > 1000
QUANTITY BETWEEN 10 AND 100

-- Percentage-based
DISCOUNT_PERCENT <= 10

-- Variance tolerance
ABS(ACTUAL - FORECAST) <= 100

-- Top values
SALES_RANK <= 10  -- Top 10 products
PERCENTILE >= 0.75  -- Top quartile
```

### Complex Composite Filters

```sql
-- Multiple conditions (AND)
STATUS = 'ACTIVE'
AND ORDER_DATE >= '2024-01-01'
AND AMOUNT > 0
AND COUNTRY IN ('USA', 'Canada')

-- Alternative conditions (OR)
REGION IN ('North', 'South')
OR MANAGER_ID IS NULL
OR PERFORMANCE_RATING >= 4

-- Complex logic
(STATUS = 'ACTIVE' AND AMOUNT > 100)
OR (STATUS = 'PENDING' AND AMOUNT > 1000)
OR (STATUS = 'ARCHIVED' AND APPROVAL_DATE > '2023-01-01')

-- Excluding problematic records
AMOUNT > 0  -- No zero/negative sales
AND CREATED_DATE <= CURRENT_DATE  -- No future dates
AND CUSTOMER_ID <> 0  -- Valid customers only
AND LENGTH(TRIM(DESCRIPTION)) > 0  -- Non-empty descriptions
```

---

## Data Access Control (DAC) Setup

### Principal Hierarchy Structure

```
Organization (Root)
├── Region
│   ├── Sales_East
│   ├── Sales_West
│   └── Sales_Europe
└── Department
    ├── Finance
    ├── Operations
    └── Executive
```

### User-to-Principal Mapping

```
UserID        | PrincipalValue | Level
john.smith    | Sales_East     | Region
jane.doe      | Sales_West     | Region
carlos.lopez  | Executive      | Department
maria.garcia  | Finance        | Department
```

### DAC Filter Expression Examples

```sql
-- Region-based access
SALES_REGION IN (
  SELECT principal_value
  FROM user_principals
  WHERE user_id = CURRENT_USER
  AND principal_type = 'Region'
)

-- Department-based access
COST_CENTER IN (
  SELECT cost_center_id
  FROM department_mapping
  WHERE department_name IN (
    SELECT principal_value
    FROM user_principals
    WHERE user_id = CURRENT_USER
  )
)

-- Hierarchical access (user sees their team and below)
MANAGER_ID IN (
  SELECT employee_id
  FROM org_hierarchy
  WHERE reporting_line LIKE CONCAT('%',
    (SELECT employee_id FROM employees WHERE user_id = CURRENT_USER), '%')
)

-- Multi-dimensional access
(REGION = (SELECT region FROM user_attributes WHERE user_id = CURRENT_USER))
AND (FISCAL_YEAR >= (SELECT start_year FROM user_fiscal_access WHERE user_id = CURRENT_USER))
```

---

## Common View Patterns

### Star Schema Pattern

```
Central Fact Table (Orders)
         ↙    ↓    ↓    ↖
    Customer  Date  Product  Warehouse
   (Dimension) Dimensions...
```

**Implementation:**
- Fact view contains transaction-level data with foreign keys
- Dimension views contain reference data
- Associations link Fact to Dimensions
- Supports drill-down and analysis across multiple dimensions

---

### Snowflake Schema Pattern

```
Fact Table (Orders)
    ↓
  Customer Dimension
    ↓
  Geography (nested hierarchy)
    ↓
  Region → Country → Continent
```

**Implementation:**
- Normalized dimension tables
- Dimension views reference sub-dimensions
- More storage efficient than star schema
- Slightly more complex join logic

---

### Denormalized Pattern

```
Single Fact View (Sales with all attributes)
- OrderID, CustomerID, CustomerName, Address
- ProductID, ProductName, Category
- Date, Region, Amount, Quantity
```

**Use when:**
- Data is read-heavy, rarely updated
- Performance is critical
- Query simplicity is important

**Caution:** Data redundancy, update anomalies possible

---

### Federated/Materialized View Pattern

```
Virtual View (combines virtual and persisted sources)
- Virtual customer orders (real-time)
- Persisted customer master (daily refresh)
- Persisted product catalog (weekly refresh)
```

**Implementation:**
- Mix persistent and virtual views
- Persist frequently-accessed aggregates
- Virtual where real-time is critical

---

## Association Best Practices

### Navigational Hierarchy
```
Fact: Orders
  → To_Customer (Customer Dimension)
      → To_Geography (Customer Geography)
          → To_Region (Region Master)
```

**Enable:** Drill-down from Order → Customer Region in analytics

### Bidirectional Reference
```
Customer (Dimension)
  ← Has_Orders (inverse association)

Order (Fact)
  → To_Customer (forward association)
```

**Note:** Explicitly model if needed for reverse navigation

### Avoiding Circular References
```
AVOID:
Product ← → Category ← → Brand

DO:
Product → Category
Product → Brand
(No circular dependency)
```

---

## Performance Tuning Reference

### Push-Down Eligible Operations
- ✓ Column selection (projection)
- ✓ Row filters on source columns
- ✓ Simple arithmetic operations
- ✓ String comparisons

### Push-Down NOT Possible
- ✗ Complex calculated columns
- ✗ Window functions
- ✗ Union operations
- ✗ Group-by aggregations in virtual views

### Storage Estimate Formula
```
View Size = Row Count × Average Row Width

Example:
100 million order rows × 80 bytes/row = 8 GB

Compressed (typical 3:1) = ~2.7 GB
```
