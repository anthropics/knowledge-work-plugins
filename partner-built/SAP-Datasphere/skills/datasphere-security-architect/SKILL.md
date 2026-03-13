---
name: Security Architect
description: "Design and enforce row-level security, Data Access Controls (DACs), Analysis Authorization imports from BW/4HANA, and audit policies. Use when implementing data governance, protecting sensitive information, migrating BW authorizations, configuring compliance auditing (SOX, GDPR), or establishing segregation of duties. Critical for regulated industries."
---

# Security Architect Skill

## Overview

This skill guides you through designing and implementing comprehensive security controls in SAP Datasphere. Security architecture is foundational to enterprise data governance, ensuring users see only appropriate data while maintaining audit trails for compliance.

### When to Use This Skill

- **Authorization Migration**: Converting SAP BW/4HANA Analysis Authorizations to Datasphere Data Access Controls
- **Row-Level Security**: Restricting data visibility by user attributes, organizational hierarchy, or business rules
- **Compliance Requirements**: Implementing SOX, GDPR, HIPAA, or industry-specific audit requirements
- **Data Governance**: Establishing data access policies and enforcing them across organization
- **Sensitive Data Protection**: Masking or restricting access to PII, financial data, or proprietary information
- **Segregation of Duties**: Preventing unauthorized combinations of access
- **Audit Trail Management**: Logging and monitoring data access for investigation and reporting

### Security Architecture Overview

Datasphere provides layered security controls:

```
┌──────────────────────────────────────────────────────────┐
│           Data Consumer (BI Tool, App)                   │
└───────────────────────┬──────────────────────────────────┘
                        │
                   ┌────▼─────────────────┐
                   │  Identity & Access   │
                   │  Management (IdP)    │
                   │  - SAML, OIDC        │
                   │  - User Attributes   │
                   │  - Group Membership  │
                   └────┬─────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
   │ Space    │    │ Object  │    │ Row-    │
   │ Level    │    │ Level   │    │ Level   │
   │ Access   │    │ Access  │    │ Access  │
   └────┬────┘    └────┬────┘    └────┬────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
            ┌──────────▼────────────┐
            │  Data Access Controls │
            │  (DAC) - Row Filters  │
            │                       │
            │ - Operator/Values DAC │
            │ - Hierarchy DAC       │
            │ - Combined DACs       │
            └──────────┬───────────┘
                       │
        ┌──────────────▼──────────────┐
        │  Data (Tables, Views)       │
        │                             │
        │  User sees filtered rows    │
        └─────────────────────────────┘

        ┌──────────────────────────────┐
        │ Audit Trail (Logging)        │
        │ - Read operations logged     │
        │ - Changes logged             │
        │ - Access violations logged   │
        └──────────────────────────────┘
```

---

## Part 1: Data Access Controls (DAC) — Row-Level Security

Data Access Controls are Datasphere's primary mechanism for row-level security (RLS). DACs filter rows based on user context.

### DAC Architecture

**Core Concept:**

```sql
-- Without DAC: User sees all rows
SELECT * FROM T_SALES WHERE 1=1

-- Result: 1,000,000 rows

-- With DAC applied: User sees filtered rows
SELECT * FROM T_SALES WHERE COMPANY_CODE = CURRENT_USER_COMPANY

-- Result: 50,000 rows (only their company)
```

### DAC Types

#### Type 1: Operator and Values DAC

Filters rows by comparing a table column to a user attribute or fixed list.

**Use Cases:**
- Restrict sales reps to their assigned region
- Show finance staff only their cost center
- Limit product managers to their category
- Prevent cross-subsidiary data access

**Architecture:**

```yaml
DAC Type: Operator and Values
Name: DAC_SALES_BY_REGION

Filter Logic:
  Table Column: SALES_REGION
  Condition Type: IN
  Condition Values: [User Attribute: USER_ASSIGNED_REGIONS]

Result:
  - User with attribute REGIONS = ['Americas', 'EMEA']
  - Sees only rows where SALES_REGION IN ('Americas', 'EMEA')
  - Other regions hidden (Europe, APAC if not in attribute)
```

**Implementation Steps:**

1. **Create Custom User Attribute**
   ```sql
   -- In your Identity Provider (IdP) or Datasphere User Management
   User: john.smith@company.com
   Custom Attributes:
     - ASSIGNED_REGIONS: ['Americas', 'EMEA']
     - ASSIGNED_COST_CENTERS: ['CC001', 'CC002']
     - ASSIGNED_PLANTS: ['PLANT_USA', 'PLANT_MEXICO']
   ```

2. **Create DAC in Datasphere**
   - Navigate: Data Access Controls → New
   - Name: `DAC_SALES_BY_REGION`
   - Filter Column: `SALES_REGION` (from T_SALES table)
   - Operator: `IN`
   - Value Source: `User Attribute: ASSIGNED_REGIONS`

3. **Apply DAC to Table/View**
   - Open table: `T_SALES`
   - Add Data Access Control: `DAC_SALES_BY_REGION`
   - Scope: All users (or specific role)
   - Save and activate

4. **Test DAC Behavior**
   ```sql
   -- As user john.smith (ASSIGNED_REGIONS = ['Americas', 'EMEA'])
   SELECT COUNT(*) FROM T_SALES
   -- Expected: Only Americas & EMEA rows (e.g., 50K of 100K total)

   -- As user jane.doe (ASSIGNED_REGIONS = ['APAC'])
   SELECT COUNT(*) FROM T_SALES
   -- Expected: Only APAC rows (e.g., 30K of 100K total)
   ```

**SQL Expression DACs (Advanced):**

For complex logic, use SQL expressions:

```yaml
DAC Name: DAC_COMPLEX_SALES_ACCESS
Filter Expression: |
  (SALES_REGION IN :USER_REGIONS
   AND SALES_ORG = :USER_PRIMARY_ORG)
  OR (USER_ROLE = 'GLOBAL_MANAGER' AND 1=1)  -- Bypass for managers

Parameters:
  - :USER_REGIONS (from custom attribute)
  - :USER_PRIMARY_ORG (from custom attribute)
  - :USER_ROLE (from IdP role)
```

**Operator Choices:**

| Operator | Use Case | Example |
|---|---|---|
| `=` | Exact match | `COMPANY_CODE = USER_COMPANY` |
| `<>` | Not equal | `STATUS <> 'RESTRICTED'` |
| `IN` | Multiple values | `REGION IN (USER_REGIONS)` |
| `NOT IN` | Exclude values | `CATEGORY NOT IN (USER_EXCLUDED)` |
| `>`, `<`, `>=`, `<=` | Range filtering | `AMOUNT >= USER_MIN_THRESHOLD` |
| `LIKE` | Pattern matching | `CUSTOMER_NAME LIKE USER_NAME_PATTERN` |
| `BETWEEN` | Range (inclusive) | `POSTING_DATE BETWEEN START_DATE AND END_DATE` |

---

#### Type 2: Hierarchy DAC

Filters rows by organizational or master data hierarchies.

**Use Cases:**
- Restrict users to their department and sub-departments (org hierarchy)
- Show sales data by customer hierarchy (top → bottom levels)
- Limit access by product category hierarchy
- Enable drill-down while preventing sibling access

**Architecture:**

```yaml
DAC Type: Hierarchy
Name: DAC_ORG_HIERARCHY_ACCESS

Hierarchy: ORG_STRUCTURE
  ├── Company
  │   ├── Division
  │   │   ├── Department
  │   │   └── Sub-Department
  │   └── Region
  │       ├── Country
  │       └── Territory

User Assignment:
  john.smith: Department "Engineering"
  Result: Can see Engineering + all sub-departments
  Cannot see: Other divisions, other departments

jane.doe: Division "Sales"
Result: Can see Sales division + all departments within Sales
Cannot see: Engineering division, other divisions
```

**Implementation Steps:**

1. **Create Hierarchy Table**
   ```sql
   CREATE TABLE T_ORG_HIERARCHY (
     NODE_ID VARCHAR(10) PRIMARY KEY,
     PARENT_NODE_ID VARCHAR(10),
     NODE_NAME VARCHAR(50),
     NODE_LEVEL INTEGER,  -- 1=Company, 2=Division, 3=Dept
     NODE_TYPE VARCHAR(20),
     EFFECTIVE_FROM DATE,
     EFFECTIVE_TO DATE
   );

   INSERT INTO T_ORG_HIERARCHY VALUES
     ('ROOT', NULL, 'Company', 1, 'COMPANY', '2024-01-01', NULL),
     ('DIV_ENG', 'ROOT', 'Engineering', 2, 'DIVISION', '2024-01-01', NULL),
     ('DIV_SALES', 'ROOT', 'Sales', 2, 'DIVISION', '2024-01-01', NULL),
     ('DEPT_DEV', 'DIV_ENG', 'Development', 3, 'DEPARTMENT', '2024-01-01', NULL),
     ('DEPT_QA', 'DIV_ENG', 'QA', 3, 'DEPARTMENT', '2024-01-01', NULL),
     ('DEPT_EMEA', 'DIV_SALES', 'EMEA Sales', 3, 'DEPARTMENT', '2024-01-01', NULL),
     ('DEPT_APAC', 'DIV_SALES', 'APAC Sales', 3, 'DEPARTMENT', '2024-01-01', NULL);
   ```

2. **Create User-to-Hierarchy Mapping**
   ```sql
   CREATE TABLE T_USER_ORG_MAPPING (
     USER_ID VARCHAR(12),
     ASSIGNED_NODE_ID VARCHAR(10),
     ASSIGNED_NODE_LEVEL INTEGER,
     EFFECTIVE_FROM DATE
   );

   INSERT INTO T_USER_ORG_MAPPING VALUES
     ('john.smith', 'DEPT_DEV', 3, '2024-01-01'),
     ('jane.doe', 'DIV_SALES', 2, '2024-01-01'),
     ('mary.johnson', 'ROOT', 1, '2024-01-01');  -- CEO sees all
   ```

3. **Create Hierarchy-Based DAC**
   - Create DAC: `DAC_ORG_HIERARCHY`
   - Type: Hierarchy
   - Hierarchy Table: `T_ORG_HIERARCHY`
   - Key Column: `NODE_ID`
   - User Mapping Table: `T_USER_ORG_MAPPING`
   - Mapping Key: `ASSIGNED_NODE_ID`
   - Include Sub-Hierarchy: Yes (allows drill-down)

4. **Apply DAC to Fact Tables**
   - Add DAC to any table with department/org column
   - Ensure table has matching key: `DEPARTMENT_ID`
   - Filter merges table column with user's hierarchy level

5. **Test Hierarchy Access**
   ```sql
   -- As john.smith (assigned DEPT_DEV, level 3)
   -- John can see data for:
   --   - DEPT_DEV (his department)
   --   - Any future sub-departments under DEPT_DEV (if any)
   --   - Sub-departments he gets reassigned to
   --
   -- John CANNOT see:
   --   - DEPT_QA (sibling department)
   --   - DIV_SALES (other division)
   --   - Other company divisions

   -- As jane.doe (assigned DIV_SALES, level 2)
   -- Jane can see data for:
   --   - DIV_SALES (her division)
   --   - DEPT_EMEA (child of DIV_SALES)
   --   - DEPT_APAC (child of DIV_SALES)
   --   - All sub-departments under EMEA/APAC
   --
   -- Jane CANNOT see:
   --   - DIV_ENG (other division)
   --   - DEPT_DEV, DEPT_QA (different division)
   ```

**Hierarchy Best Practices:**

- Maintain effective dates for organizational changes
- Test transitions when org structure changes
- Document hierarchy structure for audit purposes
- Keep hierarchy tables normalized to avoid anomalies
- Use version control if hierarchy evolves frequently

---

#### Type 3: Combined DACs

Chain multiple DACs together for complex scenarios.

**Use Case: Multi-Attribute Filtering**

```yaml
Scenario: Sales Manager needs:
  - Only their assigned regions (Operator DAC)
  - Only approved customer categories (Hierarchy DAC)
  - Only current fiscal year data (Date DAC)

Implementation:
  DAC 1 (Operator): SALES_REGION IN (:USER_REGIONS)
  DAC 2 (Hierarchy): CUSTOMER_CATEGORY hierarchy filter
  DAC 3 (Date): FISCAL_YEAR = CURRENT_FISCAL_YEAR

  Combination Logic: DAC1 AND DAC2 AND DAC3
  Result: User sees intersection of all three filters
```

**SQL Representation:**

```sql
-- Combined DAC logic (applied automatically by Datasphere)
SELECT * FROM T_SALES
WHERE SALES_REGION IN ('Americas', 'EMEA')           -- DAC 1
  AND CUSTOMER_CATEGORY IN ('A', 'B', 'C')           -- DAC 2
  AND FISCAL_YEAR = 2024                             -- DAC 3
```

---

### DAC Testing and Validation

**Test Framework:**

```yaml
Test Plan: DAC_SALES_BY_REGION

Test Case 1: User with Single Region
  User: john.smith (REGIONS = ['Americas'])
  Query: SELECT COUNT(*) FROM T_SALES
  Expected: Only Americas rows visible
  Verification:
    SELECT DISTINCT SALES_REGION FROM T_SALES
    Expected Result: ['Americas']

Test Case 2: User with Multiple Regions
  User: jane.doe (REGIONS = ['EMEA', 'APAC'])
  Query: SELECT COUNT(*) FROM T_SALES
  Expected: EMEA + APAC rows visible, Americas hidden
  Verification:
    SELECT DISTINCT SALES_REGION FROM T_SALES
    Expected Result: ['EMEA', 'APAC']

Test Case 3: User with No Assigned Regions
  User: alex.brown (REGIONS = [])
  Query: SELECT COUNT(*) FROM T_SALES
  Expected: 0 rows (empty result set)
  Verification: Row count = 0

Test Case 4: Admin Bypass (if applicable)
  User: admin.user (ROLE = 'GLOBAL_ADMIN')
  Query: SELECT COUNT(*) FROM T_SALES
  Expected: All rows visible (DAC bypassed)
  Verification: Row count = total all regions
```

**Validation SQL Queries:**

```sql
-- Query 1: Verify DAC is active on table
SELECT TABLE_NAME, DAC_NAME, DAC_TYPE, ACTIVE_FLAG
FROM DATASPHERE.DATA_ACCESS_CONTROLS
WHERE TABLE_NAME = 'T_SALES';

-- Expected: DAC_SALES_BY_REGION, Operator, Y

-- Query 2: List all DACs applied to table
SELECT DAC_NAME, FILTER_COLUMN, FILTER_OPERATOR, FILTER_VALUES
FROM DATASPHERE.DAC_DEFINITIONS
WHERE TABLE_NAME = 'T_SALES'
ORDER BY APPLY_SEQUENCE;

-- Query 3: Count rows per user per region (for validation)
-- Run as each test user and verify results match expectations
SELECT USER_ID, SALES_REGION, COUNT(*) as row_count
FROM T_SALES
GROUP BY USER_ID, SALES_REGION
ORDER BY USER_ID, SALES_REGION;
```

**Regression Testing (Ongoing):**

After any DAC changes:
- Re-run all test cases
- Validate no unintended data exposure
- Check performance impact (DAC filters add overhead)
- Document any behavioral changes

---

## Part 2: Analysis Authorization Import (BW → Datasphere)

BW/4HANA Analysis Authorizations define who can see which InfoCubes and which rows. Datasphere uses a similar model but requires mapping.

### Understanding BW Analysis Authorizations

**BW Authorization Objects:**

```
Authorization:
├── Object: 0_RF_BOA
│   └── InfoCube: 0SALES_001
│       ├── Authorization Type: Value-based
│       ├── Auth Fields:
│       │   ├── COMPANY_CODE: ['0010', '0020']
│       │   ├── SALES_ORG: ['1000']
│       │   ├── CUSTOMER: ['*'] (All)
│       │   └── PRODUCT_CATEGORY: ['CARS', 'BIKES']
│       └── Result: User can access 0SALES_001 with those filters

└── Object: 0_USER
    └── Authorization Values:
        ├── User: john.smith
        ├── Company Code: '0010', '0020'
        ├── Role: Sales Manager
        └── Reports Allowed: [SALES001, SALES002]
```

**BW Authorization Types:**

| Type | Scope | Datasphere Mapping |
|---|---|---|
| Value-Based | Specific field values | Operator DAC |
| Hierarchy-Based | Organizational structure | Hierarchy DAC |
| Derived | Based on other authorizations | Computed DAC |
| Role-Based | User role determines access | Space/Object roles |

---

### BW to Datasphere Authorization Mapping

#### Step 1: Extract BW Authorizations

```
Transaction: SU01 (User Maintenance) in source BW system

For Each User:
  1. Select User ID
  2. View "Roles" tab
  3. For each role, note authorizations
  4. Document authorization fields and values:

User: JOHN.SMITH
├── Role: ZSD_REGIONAL_SALES_MGR
│   ├── Authorization 0_RF_BOA (InfoCube Access)
│   │   ├── COMPANY_CODE: 0010, 0020
│   │   ├── SALES_ORG: 1000
│   │   ├── SALES_DISTRICT: 10, 20, 30
│   │   └── REGION: EUR, AMER
│   ├── Authorization 0_AUDIT (Report Access)
│   │   └── Reports: SALES001, SALES002, SALES003
│   └── Authorization S_DEVELOP (Development Access)
│       └── Programs: ZSD_*
│
└── Role: ZFI_COST_CENTER_MGR
    ├── Authorization 0_RF_BOA
    │   ├── COMPANY_CODE: 0010
    │   ├── COST_CENTER: 1000, 1100, 1200
    │   └── PLANT: 1001, 1002
    └── Authorization 0_F_LEDGER
        └── Ledger access: All
```

**Export Steps:**

1. Use transaction **URAM** (Analysis Authorization Report)
2. Select user range (or all users)
3. Run report to extract authorization details
4. Export to Excel/CSV with columns:
   - USER_ID
   - AUTH_OBJECT
   - AUTH_FIELD_1
   - AUTH_FIELD_1_VALUES
   - AUTH_FIELD_2
   - AUTH_FIELD_2_VALUES
   - ... (repeat for all fields)
   - INFOCUBE_ID (for 0_RF_BOA)

**Example Export Format:**

```
USER_ID,AUTH_OBJECT,FIELD_1,VALUE_1,FIELD_2,VALUE_2,FIELD_3,VALUE_3,INFOCUBE
john.smith,0_RF_BOA,COMPANY_CODE,"0010;0020",SALES_ORG,"1000",SALES_DISTRICT,"10;20;30",0SALES_001
john.smith,0_RF_BOA,COMPANY_CODE,"0010;0020",SALES_ORG,"1000",REGION,"EUR;AMER",0SALES_001
jane.doe,0_RF_BOA,COMPANY_CODE,"0010",COST_CENTER,"1000;1100;1200",PLANT,"1001;1002",0COST_001
mary.johnson,0_RF_BOA,COMPANY_CODE,"*",SALES_ORG,"*",REGION,"*",0SALES_001
```

---

#### Step 2: Map BW Fields to Datasphere Columns

Create mapping table:

```sql
CREATE TABLE T_AUTH_FIELD_MAPPING (
  BW_INFOCUBE_ID VARCHAR(30),
  BW_AUTH_FIELD VARCHAR(30),
  DS_TABLE_NAME VARCHAR(60),
  DS_COLUMN_NAME VARCHAR(60),
  MAPPING_TYPE VARCHAR(20),  -- VALUES, HIERARCHY, FORMULA
  NOTES VARCHAR(500)
);

INSERT INTO T_AUTH_FIELD_MAPPING VALUES
  ('0SALES_001', 'COMPANY_CODE', 'T_SALES', 'COMPANY_CODE', 'VALUES',
   'Direct column match'),
  ('0SALES_001', 'SALES_ORG', 'T_SALES', 'SALES_ORG', 'VALUES',
   'Direct column match'),
  ('0SALES_001', 'SALES_DISTRICT', 'T_SALES', 'DISTRICT_ID', 'VALUES',
   'Maps to DISTRICT_ID column'),
  ('0SALES_001', 'REGION', 'T_SALES', 'SALES_REGION', 'HIERARCHY',
   'Use org hierarchy for filtering'),
  ('0COST_001', 'COST_CENTER', 'T_FINANCIALS', 'COST_CENTER', 'HIERARCHY',
   'Use cost center hierarchy'),
  ('0COST_001', 'PLANT', 'T_FINANCIALS', 'PLANT_ID', 'VALUES',
   'Direct column match');
```

**Mapping Challenges:**

| BW Field | Datasphere Challenge | Solution |
|---|---|---|
| Wildcard (*) | Means "all values" | Remove filter (no DAC needed) |
| Compound key | Multiple fields required | Create composite key DAC |
| User-exit logic | Custom ABAP code | Rebuild logic in transformation |
| Time-dependent | Fields change per period | Use date-scoped DAC |
| Hierarchies with wildcards | "REGION: EUR*" | Hierarchy DAC with pattern matching |

---

#### Step 3: Create Datasphere DACs from BW Authorizations

```
For Each BW Authorization:
  1. Parse all fields and values
  2. Create corresponding Datasphere DAC
  3. Link DAC to appropriate table/view
  4. Assign to user/role
```

**Example Conversion:**

```
BW Authorization:
User: john.smith
AuthObject: 0_RF_BOA
InfoCube: 0SALES_001
Fields:
  - COMPANY_CODE = 0010, 0020
  - SALES_ORG = 1000
  - SALES_DISTRICT = 10, 20, 30

Datasphere Implementation:
  DAC Name: DAC_SALES_JOHN_SMITH
  Type: Operator and Values
  Filter Expression:
    COMPANY_CODE IN ('0010', '0020')
    AND SALES_ORG = '1000'
    AND DISTRICT_ID IN ('10', '20', '30')

  Applied To: T_SALES (table), V_SALES_QUERY (view)
  Assigned To: john.smith
  Active: Yes
```

**Batch DAC Creation Script Template:**

```sql
-- Pseudo-code for bulk DAC creation
FOR EACH row in T_BW_AUTH_EXPORT:
  SET @user_id = row.USER_ID
  SET @infocube = row.INFOCUBE_ID
  SET @field_1 = row.FIELD_1
  SET @values_1 = row.VALUES_1
  SET @field_2 = row.FIELD_2
  SET @values_2 = row.VALUES_2

  -- Map BW fields to Datasphere columns
  SET @ds_table = (SELECT DS_TABLE_NAME
                   FROM T_AUTH_FIELD_MAPPING
                   WHERE BW_INFOCUBE_ID = @infocube)

  SET @ds_column_1 = (SELECT DS_COLUMN_NAME
                      FROM T_AUTH_FIELD_MAPPING
                      WHERE BW_INFOCUBE_ID = @infocube
                        AND BW_AUTH_FIELD = @field_1)

  -- Build filter expression
  SET @filter_expr = CONCAT(
    @ds_column_1, ' IN (', @values_1, ')'
  )

  -- Create DAC in Datasphere
  CREATE DATA ACCESS CONTROL AS (CONCAT('DAC_', @user_id, '_', @infocube))
  FOR TABLE (CONCAT('T_', @infocube))
  WHERE (@filter_expr)

  -- Assign to user
  GRANT DATA ACCESS CONTROL (CONCAT('DAC_', @user_id, '_', @infocube))
  TO USER @user_id
END FOR

-- After creation, validate
SELECT USER_ID, COUNT(*) as dac_count
FROM DATASPHERE.DATA_ACCESS_CONTROLS
GROUP BY USER_ID
HAVING dac_count > 0
ORDER BY dac_count DESC;
```

---

#### Step 4: Validate Authorization Migration

**Reconciliation Steps:**

1. **Verify all BW users have corresponding DACs**
   ```sql
   -- Compare user count
   SELECT COUNT(DISTINCT USER_ID) as bw_users
   FROM T_BW_AUTH_EXPORT;

   SELECT COUNT(DISTINCT USER_ID) as ds_users
   FROM DATASPHERE.DATA_ACCESS_CONTROLS;

   -- Expected: Both counts equal (or very close)
   ```

2. **Verify all BW fields are mapped**
   ```sql
   -- Check for unmapped fields
   SELECT DISTINCT BW_AUTH_FIELD
   FROM T_BW_AUTH_EXPORT bw
   WHERE NOT EXISTS (
     SELECT 1 FROM T_AUTH_FIELD_MAPPING m
     WHERE m.BW_AUTH_FIELD = bw.BW_AUTH_FIELD
   );

   -- Expected: Empty result set (no unmapped fields)
   ```

3. **Test sample authorizations**
   ```sql
   -- For test user john.smith:
   -- 1. Log in as john.smith in Datasphere
   -- 2. Execute query: SELECT DISTINCT COMPANY_CODE FROM T_SALES
   -- 3. Expected result: ['0010', '0020'] (from BW auth)
   -- 4. Execute: SELECT COUNT(*) FROM T_SALES WHERE SALES_ORG = '1000'
   -- 5. Expected: 150,000 records (only his sales org)
   ```

4. **Compare row counts (BW vs. Datasphere)**
   ```sql
   -- BW System:
   SELECT USER, COUNT(*) as row_count
   FROM 0SALES_001
   WHERE COMPANY_CODE IN ('0010', '0020')
     AND SALES_ORG = '1000'
   GROUP BY USER;

   -- Datasphere:
   SELECT CURRENT_USER as USER, COUNT(*) as row_count
   FROM T_SALES
   WHERE 1=1  -- DAC filter applied automatically
   GROUP BY CURRENT_USER;

   -- Expected: Row counts match ±0.1%
   ```

---

## Part 3: Audit Policy Configuration

Audit logging tracks who accessed what data and when, essential for compliance.

### Audit Logging Architecture

```
┌─────────────────┐
│   User Query    │
│  SELECT ...     │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────┐
│  Datasphere Query Engine     │
│  Applies Row-Level Security  │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  Audit Policy Evaluator      │
│  Is this query auditable?    │
│  - Table in audit scope?     │
│  - Operation type logged?    │
│  - User role triggers audit? │
└────────┬─────────────────────┘
         │
      ┌──┴───┬────────┐
      │      │        │
   Yes│      │No      │No Log
      │      │        │
      ▼      ▼        ▼
   ┌─────────────┐   Query
   │Log to Audit │   Continues
   │Table        │   Normally
   └────┬────────┘
        │
        ▼
   ┌──────────────────────┐
   │ T_AUDIT_LOG (Table)  │
   │ - USER_ID            │
   │ - OPERATION          │
   │ - TABLE_NAME         │
   │ - RECORD_COUNT       │
   │ - TIMESTAMP          │
   │ - IP_ADDRESS         │
   └──────────────────────┘
```

### Audit Policy Configuration Steps

#### Step 1: Define Audit Scope

Decide which tables, operations, and users to audit:

```yaml
Audit Scope Decision:

High Priority (Audit All Operations):
  ├── T_CUSTOMER_PII (Personal Identifiable Information)
  │   ├── Operations: Read, Insert, Update, Delete
  │   ├── Users: All
  │   └── Retention: 3 years (GDPR)
  ├── T_PAYROLL (Sensitive HR Data)
  │   ├── Operations: Read, Update, Delete
  │   ├── Users: All (especially non-HR)
  │   └── Retention: 7 years (Labor Laws)
  └── T_FINANCIAL_TRANSACTIONS (Compliance)
      ├── Operations: Read, Insert, Update, Delete
      ├── Users: All
      └── Retention: 10 years (SOX)

Medium Priority (Audit Changes Only):
  ├── T_PRODUCT_MASTER
  │   ├── Operations: Insert, Update, Delete (not Read)
  │   ├── Users: All
  │   └── Retention: 1 year
  ├── T_SALES
  │   ├── Operations: Insert, Update (not Read)
  │   ├── Users: Only non-sales users (exception access)
  │   └── Retention: 6 months
  └── T_CUSTOMER_ATTRIBUTES
      ├── Operations: Update, Delete
      ├── Users: All
      └── Retention: 1 year

Low Priority (Sample/Spot-Check):
  ├── T_REFERENCE_DATA
  │   ├── Operations: Reads (random sampling)
  │   ├── Users: All
  │   └── Retention: 3 months
```

#### Step 2: Create Audit Log Table

```sql
CREATE TABLE T_AUDIT_LOG (
  AUDIT_ID BIGINT PRIMARY KEY AUTO_INCREMENT,
  AUDIT_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  DATASPHERE_USER VARCHAR(256) NOT NULL,  -- Logged-in user
  IP_ADDRESS VARCHAR(45),                   -- IPv4 or IPv6
  SESSION_ID VARCHAR(64),                   -- Unique session identifier
  OBJECT_NAME VARCHAR(256) NOT NULL,        -- Table or view name
  OBJECT_TYPE VARCHAR(20),                  -- TABLE, VIEW, ANALYTICAL_MODEL
  OPERATION VARCHAR(20) NOT NULL,           -- READ, INSERT, UPDATE, DELETE
  ROW_COUNT_AFFECTED INTEGER,               -- Rows read/modified
  EXECUTION_TIME_MS INTEGER,                -- Query duration
  SQL_HASH VARCHAR(64),                     -- Hash of SQL (for uniqueness, not visibility)
  FILTER_APPLIED CHAR(1),                   -- Y/N - was DAC applied?
  DAC_FILTERS_APPLIED VARCHAR(500),         -- Which DACs filtered data?
  RESULT_STATUS VARCHAR(20),                -- SUCCESS, FAILED, DENIED
  ERROR_MESSAGE VARCHAR(1000),              -- If failed
  SENSITIVE_DATA_ACCESSED CHAR(1),          -- Y/N - flagged by policy?
  SUSPICIOUS_ACTIVITY_FLAG CHAR(1),         -- Y/N - triggered alert?
  COMPLIANCE_RELEVANT CHAR(1),              -- Y/N - required for audit trail?
  CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  RETAINED_UNTIL DATE,                      -- When to archive/delete

  INDEX idx_timestamp (AUDIT_TIMESTAMP),
  INDEX idx_user_timestamp (DATASPHERE_USER, AUDIT_TIMESTAMP),
  INDEX idx_object_name (OBJECT_NAME, OPERATION),
  INDEX idx_sensitivity (SENSITIVE_DATA_ACCESSED),
  INDEX idx_retention (RETAINED_UNTIL)
);
```

**Partitioning Strategy (for performance):**

```sql
-- Partition by month for easier archival
PARTITION BY RANGE (YEAR_MONTH(AUDIT_TIMESTAMP)) (
  PARTITION p_202401 VALUES LESS THAN ('202402'),
  PARTITION p_202402 VALUES LESS THAN ('202403'),
  -- ... monthly partitions
  PARTITION p_202412 VALUES LESS THAN ('202501'),
  PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Allows fast deletion: ALTER TABLE T_AUDIT_LOG DROP PARTITION p_202301;
-- Much faster than DELETE WHERE AUDIT_TIMESTAMP < '2023-02-01'
```

#### Step 3: Configure Audit Policies

In Datasphere:

1. Navigate: **Administration** → **Audit Management**
2. Create Audit Policy

```yaml
Audit Policy: POLICY_HIGH_SENSITIVITY_DATA

Name: POLICY_HIGH_SENSITIVITY_DATA
Description: "Audit all access to PII, financial, and compliance-relevant data"
Enabled: Yes

Tables in Scope:
  - T_CUSTOMER_PII
  - T_PAYROLL
  - T_FINANCIAL_TRANSACTIONS
  - T_EXECUTIVE_COMPENSATION

Operations to Audit:
  ☑ READ      (All read queries)
  ☑ INSERT    (New records added)
  ☑ UPDATE    (Existing records modified)
  ☑ DELETE    (Records removed)
  ☑ TRUNCATE  (Entire table cleared)

Users in Scope:
  ☐ All users (selected)
  ☐ Specific roles: [ADMIN, ANALYST]
  ☐ Specific users: []

Audit Destination:
  ☑ Central Audit Table: T_AUDIT_LOG
  ☐ External SIEM: siem.company.com:514
  ☐ File Export: /var/audit/datasphere/

Retention Settings:
  Retention Period: 3 years
  Retention Method: Keep in active storage for 1 year, then archive to cold storage
  Purge Schedule: Quarterly (automatic deletion after retention expires)

Alerting:
  ☑ Alert on suspicious activity
    ├─ > 100 rows accessed in single query: YES, Alert Level: MEDIUM
    ├─ DELETE operation on sensitive table: YES, Alert Level: HIGH
    ├─ Same user accessing multiple restricted tables in 10 min: YES, Alert Level: HIGH
    └─ Query from unusual IP address: YES, Alert Level: MEDIUM

Compliance Mapping:
  ☑ GDPR (General Data Protection Regulation)
    ├─ Personal Data Processing: YES
    ├─ Retention: 3 years minimum
    └─ Right to be Forgotten: Support deletion log
  ☑ SOX (Sarbanes-Oxley)
    ├─ Financial Data: YES
    ├─ Retention: 10 years minimum
    └─ Immutable Log: YES
  ☑ HIPAA (Health Insurance Portability)
    ├─ PHI (Protected Health Information): YES
    ├─ Retention: 6 years minimum
    └─ Breach Notification: Auto-trigger alert
```

#### Step 4: Configure Read/Change Audit Levels

**Read-Level Auditing (Detailed):**

```yaml
Audit Level: DETAILED_READ

When to Use:
  - Highly sensitive data (customer PII, health records, executive data)
  - Regulatory requirements (HIPAA, GDPR, SOX)
  - High-value business intelligence

Captured Information:
  ✓ Every SELECT query on audited table
  ✓ User ID and timestamp
  ✓ Number of rows accessed
  ✓ Filters applied (DAC information)
  ✓ Query execution time
  ✓ IP address and session ID
  ✓ Any exception/error conditions

Performance Impact:
  - Significant: ~5-15% query overhead
  - Storage: 1-3 bytes per row accessed
  - Example: 1 billion queries/day → 50-100 GB/month audit logs

Query Example (Detailed Read Audit):
  User: john.smith
  Query: SELECT * FROM T_CUSTOMER_PII WHERE STATE = 'CA'
  Audit Log Entry:
    - OPERATION: READ
    - ROW_COUNT_AFFECTED: 500,000
    - EXECUTION_TIME_MS: 2,345
    - DAC_FILTERS_APPLIED: [DAC_STATE_FILTER]
    - SENSITIVE_DATA_ACCESSED: Y
    - Timestamp: 2024-02-08 14:32:15
```

**Change-Level Auditing (Moderate):**

```yaml
Audit Level: CHANGES_ONLY

When to Use:
  - Standard operational tables (products, orders, inventory)
  - Security/compliance needs but not highest tier
  - Balance between audit trail and performance

Captured Information:
  ✓ INSERT operations (all new records)
  ✓ UPDATE operations (modified records)
  ✓ DELETE operations (removed records)
  ✗ READ operations (not logged)
  ✓ User, timestamp, row count
  ✓ Execution time, session ID

Performance Impact:
  - Low: ~1-2% query overhead (only changes logged)
  - Storage: 0.5-1 byte per modified row

Query Example (Change-Level Audit):
  User: jane.doe
  Query: UPDATE T_PRODUCT SET PRICE = 99.99 WHERE PRODUCT_ID = 'ABC123'
  Audit Log Entry:
    - OPERATION: UPDATE
    - ROW_COUNT_AFFECTED: 1
    - EXECUTION_TIME_MS: 145
    - Timestamp: 2024-02-08 14:35:22
```

**Space-Level Audit Scoping:**

```yaml
Scenario: Multiple Spaces with Different Sensitivity

Space: FINANCE (Highly Sensitive)
  Audit Policies: [POLICY_HIGH_SENSITIVITY_DATA, POLICY_SOX]
  Audit Level: DETAILED_READ + DETAILED_CHANGES
  Retention: 10 years

Space: SALES (Medium Sensitivity)
  Audit Policies: [POLICY_STANDARD, POLICY_PII_ONLY]
  Audit Level: CHANGES_ONLY
  Retention: 1 year

Space: REFERENCE (Low Sensitivity)
  Audit Policies: []
  Audit Level: NONE
  Retention: N/A

Result:
  - All spaces can use shared T_AUDIT_LOG table
  - Partition by AUDIT_TIMESTAMP for retention management
  - Query audit logs with WHERE clause:
    SELECT * FROM T_AUDIT_LOG
    WHERE OBJECT_NAME IN (SELECT TABLE_NAME FROM FINANCE.TABLES)
      AND AUDIT_TIMESTAMP >= DATE_SUB(CURRENT_DATE, INTERVAL 10 YEAR)
```

---

## Part 4: Identity Provider (IdP) Integration

Datasphere integrates with SAML 2.0 and OIDC-compliant Identity Providers for authentication and user attribute mapping.

### Supported Identity Providers

| Provider | Protocol | User Attributes | Status |
|---|---|---|---|
| Azure AD | SAML 2.0, OIDC | Object ID, UPN, Groups | Supported |
| Okta | SAML 2.0, OIDC | Okta ID, Groups | Supported |
| Ping Identity | SAML 2.0, OIDC | User ID, Groups | Supported |
| SAP Cloud Identity | SAML 2.0 | Global User ID | Supported |
| Custom SAML | SAML 2.0 | Any custom attributes | Supported |

### IdP Configuration Steps

#### Step 1: Gather Identity Provider Metadata

From your IdP (Azure AD example):

```yaml
Identity Provider Details:

Azure AD Tenant: contoso.onmicrosoft.com
Application ID: 12345678-1234-1234-1234-123456789012
Client Secret: [SECRET]

SAML Endpoints:
  - Sign-On URL: https://login.microsoftonline.com/[TENANT_ID]/saml2
  - Sign-Out URL: https://login.microsoftonline.com/[TENANT_ID]/saml2/logout
  - Certificate (Signing): [X.509 Certificate]

Claim Mappings:
  - NameID (User Identifier): userPrincipalName (john.smith@contoso.com)
  - Email: mail (john.smith@contoso.com)
  - First Name: givenName (John)
  - Last Name: surname (Smith)
  - Custom Attributes:
    - REGIONS: extensionAttribute1 (list: ["Americas", "EMEA"])
    - COST_CENTER: extensionAttribute2 ("CC001")
    - SALES_ORG: extensionAttribute3 ("1000")
```

#### Step 2: Configure Datasphere as SAML Service Provider

In Datasphere Admin Console:

1. Navigate: **Administration** → **Security** → **Identity Providers**
2. Click **Add Identity Provider**

```yaml
Configuration:

Basic Settings:
  Provider Name: Azure_AD_Production
  Protocol: SAML 2.0
  Status: Active

Endpoint Configuration:
  IdP Sign-On URL: https://login.microsoftonline.com/[TENANT]/saml2
  IdP Sign-Out URL: https://login.microsoftonline.com/[TENANT]/saml2/logout
  IdP Signing Certificate: [Paste X.509 certificate content]

Service Provider Configuration:
  Assertion Consumer Service (ACS) URL:
    https://datasphere.company.com/saml/acs
  Entity ID:
    https://datasphere.company.com/saml/entity
  Signing Certificate: [Auto-generated]

Name ID Mapping:
  Source: SAML NameID
  Target: Datasphere User ID
  Format: urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified

Attribute Mappings:
  ┌─────────────────────┬──────────────────┬────────────────────┐
  │ Datasphere Field    │ SAML Claim Name  │ Example Value      │
  ├─────────────────────┼──────────────────┼────────────────────┤
  │ User ID             │ userPrincipalName│ john.smith@contoso │
  │ Email               │ mail             │ john.smith@contoso │
  │ First Name          │ givenName        │ John               │
  │ Last Name           │ surname          │ Smith              │
  │ REGIONS (Custom)    │ extensionAttribute1│["Americas","EMEA"]│
  │ COST_CENTER (Custom)│ extensionAttribute2│ CC001            │
  │ SALES_ORG (Custom)  │ extensionAttribute3│ 1000             │
  └─────────────────────┴──────────────────┴────────────────────┘

User Auto-Provisioning:
  ☑ Auto-Create User on First Login
  ☐ Auto-Assign to Space: [SALES_ANALYTICS]
  ☐ Auto-Assign Role: [ANALYTICS_VIEWER]

Session Settings:
  Single Sign-Out: Enabled
  Session Timeout: 60 minutes
  Remember Me: Disabled

Validation:
  [ ] Test Connection
  [ ] Download SP Metadata (for IdP registration)
```

#### Step 3: Map User Attributes to DACs

Create a mapping table to link IdP attributes to DAC filters:

```sql
CREATE TABLE T_USER_ATTRIBUTE_TO_DAC_MAPPING (
  USER_ID VARCHAR(256),
  ATTRIBUTE_NAME VARCHAR(50),
  ATTRIBUTE_VALUE VARCHAR(500),
  DAC_NAME VARCHAR(256),
  DAC_FILTER_VALUE VARCHAR(500),
  EFFECTIVE_FROM DATE,
  EFFECTIVE_TO DATE,
  MAPPING_STATUS VARCHAR(20)  -- ACTIVE, INACTIVE, PENDING
);

INSERT INTO T_USER_ATTRIBUTE_TO_DAC_MAPPING VALUES
  -- User: john.smith
  ('john.smith@contoso.com', 'REGIONS', 'Americas', 'DAC_SALES_BY_REGION', 'Americas', '2024-01-01', NULL, 'ACTIVE'),
  ('john.smith@contoso.com', 'REGIONS', 'EMEA', 'DAC_SALES_BY_REGION', 'EMEA', '2024-01-01', NULL, 'ACTIVE'),
  ('john.smith@contoso.com', 'COST_CENTER', 'CC001', 'DAC_FINANCE_BY_COST_CENTER', 'CC001', '2024-01-01', NULL, 'ACTIVE'),
  -- User: jane.doe
  ('jane.doe@contoso.com', 'REGIONS', 'EMEA', 'DAC_SALES_BY_REGION', 'EMEA', '2024-01-01', NULL, 'ACTIVE'),
  ('jane.doe@contoso.com', 'REGIONS', 'APAC', 'DAC_SALES_BY_REGION', 'APAC', '2024-01-01', NULL, 'ACTIVE'),
  ('jane.doe@contoso.com', 'SALES_ORG', '2000', 'DAC_SALES_BY_ORG', '2000', '2024-01-01', NULL, 'ACTIVE');
```

**Synchronization Process:**

```yaml
Flow: IdP Attribute → Datasphere User → DAC Application

1. User Logs In to Datasphere
   - SAML Request sent to Azure AD
   - Azure AD authenticates user
   - Azure AD returns SAML Response with:
     * User ID (john.smith@contoso.com)
     * Email (john.smith@contoso.com)
     * Custom Attributes (REGIONS: ['Americas', 'EMEA'])

2. Datasphere Processes SAML Response
   - Validates SAML signature
   - Extracts user ID and attributes
   - Creates/updates user in Datasphere
   - Stores attributes in user session context

3. User Executes Query
   SELECT * FROM T_SALES

4. Datasphere Applies Security Filters
   - Retrieves user's stored attributes
   - Looks up applicable DACs for T_SALES
   - Builds WHERE clause from DACs:
     WHERE SALES_REGION IN ('Americas', 'EMEA')

5. Query Returns Filtered Results
   - 500,000 rows (50% of total)
   - Other regions hidden

6. Audit Log Entry
   - USER_ID: john.smith@contoso.com
   - OPERATION: READ
   - FILTER_APPLIED: DAC_SALES_BY_REGION
   - ROW_COUNT_AFFECTED: 500,000
```

---

## Part 5: Privilege Escalation Prevention

Prevent users from gaining unauthorized access through configuration exploits.

### Principle of Least Privilege

**Core Concept:**

```
Each user gets MINIMUM permissions needed for their job.

Example: Sales Rep
├── NEED: Read sales data for their region
├── DON'T NEED: Edit master data, delete records, admin functions
└── ASSIGN: Viewer role on Sales space + DAC filtering by region

Example: Data Administrator
├── NEED: Create/modify objects, manage users, audit logs
├── DON'T NEED: View actual data, execute ad-hoc queries
└── ASSIGN: Admin role on Admin space + explicit DATA_READER removed
```

**Implementation Checklist:**

```yaml
Least Privilege Checklist:

☐ Identify Role Requirements
  For each job function:
    - List required access (tables, operations)
    - List forbidden access (data types, functions)
    - Document time-sensitive access (only during month-end)

☐ Create Custom Roles
  Instead of: Using standard Viewer/Editor/Admin roles
  Do This: Create specific roles:
    - SALES_ANALYST: Read sales only, no customers
    - FINANCE_REVIEWER: Read financial data only, no HR
    - ADMIN_DATAMODEL: Create objects, no data access

☐ Assign Minimum Permissions
  - Role: Finance Analyst
  - Space Access: FINANCE (Viewer)
  - Object Level: T_GENERAL_LEDGER (Read)
  - Row Level: DAC_COST_CENTER_FILTER (their CC)
  - Avoid: Admin rights, cross-space access, write permissions

☐ Regular Access Reviews
  - Quarterly: Review all user assignments
  - Question: "Does john.smith still need ADMIN role?"
  - Action: Remove if not actively used

☐ Segregation of Duties (SOD) Enforcement
  Prevent: Same person having conflicting roles
    - Cannot be: Approver AND Requester
    - Cannot be: Data Creator AND Auditor
    - Cannot be: Admin AND Data User
```

### Segregation of Duties (SoD) Patterns

**Pattern 1: Financial Controls (SOX Compliance)**

```yaml
Scenario: Accounts Payable Process

Segregation:
  ├── Purchase Requisition (Employee)
  │   └── Can: Create requisitions, view own POs
  │       Cannot: Approve own requisitions, access accounting
  ├── Approval (Manager)
  │   └── Can: Approve requisitions up to $10K
  │       Cannot: Create invoices, execute payments
  ├── Invoice Receipt (Accounts Payable)
  │   └── Can: Enter invoices, match to POs
  │       Cannot: Approve requisitions, execute payments
  ├── Payment Execution (Finance)
  │   └── Can: Execute payments to approved invoices
  │       Cannot: Approve, create invoices, change vendors
  └── Audit (Internal Audit)
      └── Can: View all, produce reports
          Cannot: Modify data, execute transactions

Implementation in Datasphere:
  Create 5 Spaces:
    - PROCUREMENT (for requisition creation)
    - APPROVAL (for managers)
    - ACCOUNTS_PAYABLE (for AP team)
    - FINANCE (for payment execution)
    - AUDIT (for compliance review)

  Create 5 Roles:
    - REQUISITIONER: Read/Write on PROCUREMENT tables
    - APPROVER: Read on PROCUREMENT, Write on APPROVAL tables
    - AP_STAFF: Read on PROCUREMENT/APPROVAL, Write on AP tables
    - FINANCE: Read on AP tables, Write on FINANCE tables
    - AUDITOR: Read all, no Write permissions

  DAC Controls:
    - Requisitioner: Only sees own requisitions
    - Approver: Sees requisitions below their limit
    - AP_Staff: Sees invoices matched to approved POs
    - Finance: Sees invoices ready for payment
    - Auditor: Sees all with audit trail
```

**Pattern 2: Data Governance (GDPR Compliance)**

```yaml
Scenario: Customer PII Access

Segregation:
  ├── Data Collection (Customer Service)
  │   └── Can: Create customer records with contact info
  │       Cannot: Delete records, access payment info
  ├── Analysis (Marketing)
  │   └── Can: View aggregated customer data (no PII)
  │       Cannot: Access individual customer records
  ├── Privacy (Data Protection Officer)
  │   └── Can: Access full customer records for privacy requests
  │       Cannot: Use data for marketing, audit customer queries
  └── Audit (Compliance)
      └── Can: View who accessed PII, when, what actions
          Cannot: Modify data, access actual PII

Implementation:
  Tables:
    - T_CUSTOMER_CONTACT (phone, email)
    - T_CUSTOMER_PAYMENT (CC, bank account)
    - T_CUSTOMER_AGGREGATE (summary, no PII)
    - T_CUSTOMER_AUDIT (access logs)

  Roles:
    - CUSTOMER_REPRESENTATIVE: Write CONTACT, cannot access PAYMENT
    - MARKETING_ANALYST: Read AGGREGATE only, CONTACT hidden
    - DATA_PROTECTION_OFFICER: Read all PII, Write audit logs
    - COMPLIANCE_AUDITOR: Read AUDIT, specific rows based on time-range DAC

  DACs:
    - MARKETING_ANALYST: No DAC on CONTACT (entire table hidden)
    - CUSTOMER_REP: DAC_ASSIGNED_CUSTOMERS (only their region's customers)
    - DPO: DAC_PRIVACY_REQUESTS (only records under active request)
```

**Pattern 3: System Administration (Separation from Data Use)**

```yaml
Scenario: Admin Role Compartmentalization

Segregation:
  ├── Object Administrator
  │   └── Can: Create tables, views, transformations
  │       Cannot: Access data, manage users, see audit logs
  ├── User/Security Administrator
  │   └── Can: Manage users, assign roles, configure DACs
  │       Cannot: Create objects, access data, modify audit settings
  ├── Audit Administrator
  │   └── Can: Configure audit policies, view audit logs
  │       Cannot: Modify users, create objects, access data
  └── System Administrator (limited)
      └── Can: Overall system settings, coordinate between other admins
          Cannot: Day-to-day object creation, user management

Implementation in Datasphere:
  Roles:
    - OBJECT_ADMIN: Roles SPACE_ADMIN on Tech space only
    - USER_ADMIN: User.Manage permission, cannot enter Data space
    - AUDIT_ADMIN: Audit.Manage permission, cannot create objects
    - SUPER_ADMIN: All three roles

  Space Segregation:
    - TECH_SPACE: Only OBJECT_ADMIN has access
    - MASTER_DATA: Only USER_ADMIN can modify access
    - DATA_SPACE: No admin role, only business users with DACs
    - AUDIT_SPACE: Only AUDIT_ADMIN, read-only for others
```

---

## Part 6: Security Testing and Validation Workflows

### Pre-Go-Live Security Checklist

```yaml
Security Validation - Pre-Production Checklist:

Identity & Access Management:
  ☐ IdP (SAML/OIDC) configuration tested
  ☐ User provisioning tested (new users created correctly)
  ☐ User attribute mapping verified (custom attributes populated)
  ☐ Single sign-out verified (logout clears session)
  ☐ Session timeout tested (idle users logged out)
  ☐ Concurrent session limits enforced

Data Access Controls:
  ☐ DACs active on all sensitive tables
  ☐ Each DAC tested with test users
  ☐ Row-level filtering verified (users see only assigned rows)
  ☐ Hierarchy DACs tested (managers see subordinate data)
  ☐ Combined DACs tested (multiple filters work together)
  ☐ Admin override tested (admin users bypass DACs if configured)
  ☐ DAC performance measured (< 5% query overhead)

Audit & Compliance:
  ☐ Audit policies active on sensitive tables
  ☐ Read operations logged for PII tables
  ☐ Change operations logged for all data
  ☐ Audit log table populated correctly
  ☐ Retention policies configured and tested
  ☐ Alert thresholds set and tested
  ☐ Compliance mapping configured

Authorization Migration (if from BW):
  ☐ All BW users have corresponding DACs
  ☐ All BW fields mapped to Datasphere columns
  ☐ Row count reconciliation completed (±0.1%)
  ☐ Authorization coverage tested (sample users)
  ☐ Audit trail shows migration timestamp

Privilege Segregation:
  ☐ No user has multiple conflicting roles
  ☐ Least privilege assignments verified
  ☐ Admin roles limited to necessary users
  ☐ Data access separated from admin functions
  ☐ Audit access separated from data access

Encryption & Network:
  ☐ TLS 1.2+ for all connections
  ☐ Data in transit encrypted
  ☐ Data at rest encrypted (if required)
  ☐ VPN/Firewall rules configured
  ☐ IP whitelisting tested (if applicable)

Disaster & Incident Response:
  ☐ Audit log backup/archival process defined
  ☐ Emergency access procedure documented
  ☐ Incident response runbook created
  ☐ Key person coverage confirmed
  ☐ Change management process implemented
```

### Security Testing Scenarios

#### Test 1: User Isolation (DAC Filtering)

```yaml
Scenario: Sales Reps Cannot See Each Other's Data

Setup:
  User 1: john.smith (ASSIGNED_REGION = 'Americas')
  User 2: jane.doe (ASSIGNED_REGION = 'EMEA')
  Table: T_SALES (100,000 rows: 50K Americas, 50K EMEA)

Test Execution:
  Step 1: Log in as john.smith
  Step 2: Execute: SELECT COUNT(*) FROM T_SALES
  Expected Result: 50,000 (Americas only)
  Actual Result: ___

  Step 3: Log in as jane.doe
  Step 4: Execute: SELECT COUNT(*) FROM T_SALES
  Expected Result: 50,000 (EMEA only)
  Actual Result: ___

  Step 5: Try to query: SELECT * FROM T_SALES WHERE REGION = 'EMEA' as john.smith
  Expected Result: 0 rows (filtered out by DAC)
  Actual Result: ___

Pass Criteria: Both users see only their region, cannot access other regions
```

#### Test 2: Admin Override (if configured)

```yaml
Scenario: Admin Can See All Data When Override Enabled

Setup:
  User: admin.user (ROLE = 'ADMIN', DAC bypass = enabled)
  Table: T_SALES (100,000 rows)

Test Execution:
  Step 1: Log in as admin.user
  Step 2: Execute: SELECT COUNT(*) FROM T_SALES
  Expected Result: 100,000 (all rows, DAC bypassed)
  Actual Result: ___

Pass Criteria: Admin sees complete dataset
```

#### Test 3: Audit Trail Completeness

```yaml
Scenario: All Sensitive Data Access Logged

Setup:
  User: john.smith
  Table: T_CUSTOMER_PII (sensitive)
  Audit Policy: Detailed READ logging enabled

Test Execution:
  Step 1: Execute SELECT COUNT(*) FROM T_CUSTOMER_PII
  Step 2: Check audit log: SELECT * FROM T_AUDIT_LOG
         WHERE DATASPHERE_USER = 'john.smith'
         AND OBJECT_NAME = 'T_CUSTOMER_PII'

  Expected Audit Entry:
    - AUDIT_TIMESTAMP: (within 1 second of query)
    - DATASPHERE_USER: john.smith
    - OPERATION: READ
    - ROW_COUNT_AFFECTED: (should match count)
    - FILTER_APPLIED: Y
    - DAC_FILTERS_APPLIED: [DAC_name]

Pass Criteria: Audit entry exists with complete information
```

#### Test 4: Hierarchy DAC Navigation

```yaml
Scenario: Manager Can See Team Data but Not Siblings

Setup:
  Organization Hierarchy:
    ├── Company
    │   ├── Sales Division
    │   │   ├── Americas Department
    │   │   │   ├── North Region
    │   │   │   └── South Region
    │   │   └── EMEA Department
    │   │       ├── North Europe
    │   │       └── South Europe
    │   └── Engineering Division

  User: john.smith (Assigned: Sales Division → Americas Department)
  Data: T_SALES_TRANSACTIONS (has DEPARTMENT_ID column)

Test Execution:
  Step 1: john.smith executes: SELECT DISTINCT DEPARTMENT_ID FROM T_SALES_TRANSACTIONS
  Expected Result: [Americas, North Region, South Region]
  Actual Result: ___

  Step 2: john.smith executes:
    SELECT COUNT(*) FROM T_SALES_TRANSACTIONS WHERE DEPARTMENT_ID = 'EMEA'
  Expected Result: 0 (EMEA is sibling, not subordinate)
  Actual Result: ___

  Step 3: john.smith executes:
    SELECT COUNT(*) FROM T_SALES_TRANSACTIONS WHERE DEPARTMENT_ID = 'North Region'
  Expected Result: Actual count (subordinate department visible)
  Actual Result: ___

Pass Criteria: john.smith sees Americas and its sub-departments,
not EMEA or other divisions
```

---

## Part 7: MCP Tool References

This skill integrates with these Claude MCP tools:

- **get_current_user**: Retrieve logged-in user's identity and attributes
- **get_available_scopes**: List user's accessible spaces and permissions
- **list_spaces**: Enumerate all spaces with access metadata
- **get_space_info**: Retrieve space security configuration, members, roles
- **search_repository**: Find security-relevant objects (DACs, audit policies)

**Example Usage:**

```
Assistant: "Let me check what spaces you have access to and your current permission level."
Tool: get_available_scopes()
Result: Scopes = [FINANCE (Viewer), SALES (Editor), AUDIT (Viewer)]
```

---

## MCP Tool Integration Examples

### Example 1: Review Current User Authorization

```
User Request: "What security controls apply to me?"

Assistant Actions:
1. get_current_user()
   → Returns: user_id=john.smith@contoso.com, roles=[SALES_ANALYST, VIEWER]

2. get_available_scopes()
   → Returns: spaces=[
       { space: 'SALES', role: 'EDITOR', tables: ['T_SALES', 'T_CUSTOMER'] },
       { space: 'FINANCE', role: 'VIEWER', tables: ['T_GL'] }
     ]

3. search_repository(query='DAC', filter='assigned_to:john.smith')
   → Returns: dacs=[
       { dac_name: 'DAC_SALES_BY_REGION', filter_column: 'REGION', values: ['Americas', 'EMEA'] }
     ]

Response: "You have access to SALES (editor) and FINANCE (viewer).
A data access control (DAC_SALES_BY_REGION) filters your SALES data to Americas and EMEA regions."
```

### Example 2: Audit Policy Impact Analysis

```
User Request: "Which tables have audit logging enabled?"

Assistant Actions:
1. search_repository(query='audit', filter='type:policy', status='active')
   → Returns list of active audit policies

2. For each policy, get_space_info() to see affected tables

3. Compile table list with audit levels and retention

Response: "These 12 tables have audit logging:
- T_CUSTOMER_PII: Detailed READ logging, 3-year retention
- T_FINANCIAL: Change-only logging, 10-year retention
- T_SALES: Change-only logging, 1-year retention"

## What's New (2026.05)

- **Visibility of Data Access Controls Applied to Sources**: When editing a Graphical or SQL View, you can now see data access controls (DACs) applied to the view's sources in a new subsection "Applied via Sources" under the Data Access Controls panel. This provides transparency into inherited security — you can see not just the DACs applied directly to your view, but also those applied upstream to the views and tables your view consumes. Critical for auditing and debugging access control behavior in complex view hierarchies.
```

---

End of SKILL.md