---
name: BW Bridge Migration
description: "Migrate SAP BW/4HANA to Datasphere using BW Bridge Shell and Remote Conversion. Use when replacing legacy BW systems, converting Process Chains to Task Chains, handling ADSO inventory migrations, analyzing Task List compatibility (STC01), or transitioning from hybrid Bridge operations. Essential for BW→Datasphere modernization strategies."
---

# BW Bridge Migration Skill

## Overview

The SAP Datasphere BW Bridge provides a bridge environment for migrating from SAP BW/4HANA to Datasphere. This skill guides you through comprehensive migration strategies, architectural decisions, object conversion workflows, and operational transition patterns.

### When to Use This Skill

- **BW System Modernization**: Replacing legacy BW/4HANA systems with cloud-native Datasphere
- **Data Warehouse Migration**: Moving InfoCubes, DSOs, and Process Chains to native Datasphere
- **Hybrid Operations**: Running BW Bridge alongside native Datasphere during transition
- **Process Chain Migration**: Converting BW scheduling to Datasphere Task Chains
- **Inventory and Write-Interface ADSOs**: Handling specialized ADSO types in migration scenarios
- **Compatibility Assessment**: Determining which BW objects can be converted vs. rebuilt

### BW Bridge Architecture

The BW Bridge is a restricted instance of SAP BW/4HANA running **within** the Datasphere environment:

```
┌─────────────────────────────────────────────────────┐
│         Datasphere Tenant                           │
├─────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────┐   │
│ │ BW Bridge (Embedded BW/4HANA Instance)      │   │
│ │ - InfoCubes / Composite Providers           │   │
│ │ - DataStore Objects (ADSOs)                 │   │
│ │ - Process Chains                            │   │
│ │ - BW Authorizations & Hierarchies           │   │
│ └──────────────────────────────────────────────┘   │
│ ┌──────────────────────────────────────────────┐   │
│ │ Native Datasphere                           │   │
│ │ - Dimensions                                │   │
│ │ - Fact Tables & Analytical Datasets         │   │
│ │ - Task Chains                               │   │
│ │ - Data Access Controls (DACs)               │   │
│ └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**Key Characteristics:**
- BW Bridge is a **non-productive** restricted environment
- Cannot be used for production reporting
- Limited administrative capabilities compared to standalone BW/4HANA
- Intended for migration and modernization, not long-term operation

---

## Phase 1: Migration Assessment

### BW Object Inventory and Compatibility Analysis

Before conversion, analyze your entire BW landscape:

#### Step 1: Extract BW Object Inventory

Use transaction **STC01** (Task List Management) in the source BW system to:

1. Navigate to **STC01** in SAP GUI
2. Select **View Task List** to see all migration tasks
3. Export the full task list to a spreadsheet for documentation
4. Categorize objects by type:
   - InfoCubes / Composite Providers
   - DataStore Objects (Standard, Inventory, Write-Interface)
   - Master Data Objects (Characteristics, Key Figures)
   - Process Chains
   - Hierarchies and Authorization objects

#### Step 2: Compatibility Assessment

Create a compatibility matrix:

| Object Type | Convertible | Approach | Effort | Notes |
|---|---|---|---|---|
| InfoCube | Yes | Shell Conversion | Low | Direct mapping to Analytical Dataset |
| ADSO (Standard) | Yes | Shell Conversion | Low | Maps to native table |
| ADSO (Inventory) | Partial | Hybrid or Rebuild | Medium | Requires special DAC modeling |
| ADSO (Write-Interface) | Partial | Remote Conversion | High | Complex load process mapping |
| Composite Provider | Yes | Shell Conversion | Medium | May include non-convertible objects |
| Hierarchy | Yes | Both | Low | DAC hierarchy filtering available |
| Process Chain | Yes | Task Chain Rebuild | Medium | Manual mapping to Task Chain |
| BW Authorization | Yes | DAC Mapping | Medium | Migration via Analysis Authorization import |

#### Step 3: Risk Scoring

For each object, score migration risk:

```
Risk = (Complexity × Dependencies × Customization) ÷ Team Expertise

- Complexity: 1-5 (Simple BW objects = 1, complex logic = 5)
- Dependencies: 1-5 (Isolated = 1, many upstream consumers = 5)
- Customization: 1-5 (Standard = 1, heavily modified = 5)
- Team Expertise: 1-5 (Deep BW + Datasphere knowledge = 5)

Score > 12 = High Risk (prioritize for Shell Conversion)
Score 6-12 = Medium Risk (detailed design required)
Score < 6 = Low Risk (standard conversion path)
```

---

## Phase 2: Shell Conversion Workflow

Shell Conversion automatically converts BW objects to native Datasphere objects while preserving metadata and logic.

### When to Use Shell Conversion

- Standard InfoCubes → Analytical Datasets
- Standard ADSOs → Native Tables
- Simple hierarchies → Datasphere hierarchies
- Composite Providers with convertible objects

### Shell Conversion Step-by-Step

#### Pre-Conversion Validation (Steps 1-5)

1. **Verify BW System Health**
   - Run consistency checks: **RSRV** transaction
   - Ensure no orphaned objects
   - Validate all InfoCube aggregate tables are rebuilt
   - Check for active process chains and allow them to complete

2. **Extract Technical Metadata**
   - Document all InfoCube characteristics and key figures
   - List all navigational attributes
   - Export all hierarchies and custom hierarchies
   - Note all authorization-relevant fields
   - Document all calculated fields and restricted KFGs

3. **Analyze Data Volume**
   - Run query **STOM_INFOCUBE_SIZE** to get InfoCube sizes
   - Plan data transfer bandwidth and timeline
   - Identify incremental vs. full load requirements
   - Estimate network throughput: `Time = (Size in GB × 8) ÷ Network Mbps`

4. **Assess Custom Development**
   - Search for ABAP enhancements on InfoCube load processes
   - Document user-exits and BAdIs
   - Identify custom ABAP reports dependent on this InfoCube
   - Plan re-coding requirements for unsupported objects

5. **Create Migration Backlog**
   - Prioritize objects by:
     - Business criticality (P1: Core reporting, P2: Secondary, P3: Legacy)
     - Dependency chain (convert consumers before dependencies)
     - Data volume (small → large to validate approach)
   - Assign owners to each object conversion

#### Datasphere Preparation (Steps 6-10)

6. **Set Up Datasphere Space**
   - Create dedicated migration space: `BW_BRIDGE_MIGRATION`
   - Configure space members with appropriate roles
   - Enable audit logging for compliance tracking
   - Set up separate native Datasphere space: `NATIVE_TARGET`

7. **Prepare Source System Connections**
   - Create connection to source BW system with read-only user
   - Test connectivity and credential validation
   - Set up network routing if across different networks
   - Enable BW Bridge connector (licensed separately)

8. **Stage BW Bridge Instance**
   - BW Bridge provisioning (SAP handles infrastructure)
   - Validate Bridge system accessibility
   - Configure user accounts with BW Bridge access
   - Test STC01 access in Bridge environment

9. **Plan Object Naming Convention**
   - Establish naming prefix: `Z_`, `C_`, `_CONVERTED_`
   - Document version tracking: `v1`, `v2_refined`
   - Separate Bridge objects from native: `BRIDGE_*` vs `DS_*`
   - Create mapping spreadsheet: BW Name → Datasphere Name

10. **Set Up Data Transfer Infrastructure**
    - Configure batch data loads schedule
    - Plan full vs. incremental load strategy
    - Set up error logging and monitoring
    - Prepare rollback data snapshots

#### Object Conversion Execution (Steps 11-20)

11. **Initiate BW Bridge Shell Conversion**
    - In BW Bridge STC01, select source InfoCube/ADSO
    - Click **Propose Conversion** (automated pre-check)
    - Review conversion proposal report for warnings/errors
    - Resolve any compatibility issues identified

12. **Map Characteristic to Dimension**
    - For each characteristic in the InfoCube:
    - Determine if it becomes a Dimension or dimension column
    - Link to master data objects if they exist
    - Configure hierarchy support (if needed)
    - Validate attribute inheritance

13. **Map Key Figure to Measure**
    - Define aggregation type:
      - SUM (default) → Standard measure
      - MIN/MAX → Use in analytic models
      - NONE → Dimension-like field
    - Set decimal places and currency/unit links
    - Document any formula-based KFGs requiring recalculation

14. **Configure Advanced Mappings**
    - Map navigational attributes to dimension attributes
    - Convert restricted KFGs to calculated measures or materialized tables
    - Handle time characteristics (calendar years, months)
    - Map custom hierarchies to Datasphere hierarchies

15. **Validate Shell Conversion Preview**
    - Generate conversion impact report
    - Review object dependencies and impact analysis
    - Identify unsupported objects for manual rebuild
    - Validate field mappings and data type compatibility

16. **Execute Conversion**
    - Trigger shell conversion in STC01 (`Execute Conversion` button)
    - Monitor conversion logs for errors: `TL1-001`, `TL1-002`, etc.
    - Conversion typically completes in 15-60 minutes depending on size
    - Verify generated Datasphere objects in repository

17. **Post-Conversion Object Validation**
    - Verify Datasphere Analytical Dataset created with correct structure
    - Check dimension and measure count matches original
    - Validate field types: Integer, Decimal, String, Date
    - Test hierarchy loading if hierarchies were converted
    - Confirm object is marked as `Readable` in metadata

18. **Data Transfer Execution**
    - Create data transfer task from BW Bridge to native Datasphere
    - Initial full load: Extract all historical data
    - Validate row counts match source InfoCube
    - Implement incremental load for ongoing updates
    - Test data reconciliation: Source vs. Target row counts

19. **Query and View Conversion**
    - Convert dependent BW queries to Datasphere Analytical Models
    - Rewrite query formulas (not all BW calculations directly portable)
    - Test query performance - typically improve 3-10x
    - Validate query results against source system

20. **Sign-Off and Documentation**
    - Business owner approves converted object
    - Document conversion details: Object ID, conversion time, data volume
    - Update migration registry with conversion date
    - Archive pre-conversion metadata for audit trail

### Handling Unsupported Objects

Some BW constructs cannot be converted automatically:

| Unsupported Feature | Workaround |
|---|---|
| Account-Based Modeling | Rebuild as calculated measure in Analytical Model |
| Complex ABAP BAdIs in Load Process | Replicate logic in Datasphere Transformation rules |
| Time-Dependent Hierarchies | Use versioned Datasphere hierarchies with effective dates |
| Cell-Level Security (CLS) | Map to Data Access Controls (DACs) with column filtering |
| Query-Level Cascading | Model in Datasphere as dimensional filters |

### Shell Conversion Common Issues and Resolutions

| Issue | Root Cause | Resolution |
|---|---|---|
| Characteristic not converting | Non-standard attributes | Add missing attributes before conversion; retry |
| Data transfer timeout | Network latency | Increase timeout; split into smaller batches; check bandwidth |
| Hierarchies not loading | Circular hierarchy logic | Review and fix in source; convert simplified hierarchy |
| Permission errors on Bridge | User lacks Bridge access | Add user to BW Bridge roles in Datasphere |

---

## Phase 3: Remote Conversion Workflow

Remote Conversion is an alternative for complex scenarios where Shell Conversion is insufficient.

### When to Use Remote Conversion

- Composite Providers with heavy custom logic
- Write-Interface ADSOs with complex load processes
- Objects with extensive ABAP enhancements
- Scenarios requiring gradual cutover during transition
- Complex aggregation requirements

### Remote Conversion Architecture

```
┌────────────────────────────────────────┐
│    Source BW/4HANA System (Remote)    │
│    - InfoCubes, ADSOs, Queries        │
│    - Process Chains, Hierarchies      │
└────────────────┬───────────────────────┘
                 │ (Direct connection)
                 │
┌────────────────▼───────────────────────┐
│      Datasphere Remote Conversion      │
│   - BW Bridge (embedded read-only)    │
│   - Custom transformation logic        │
│   - Remote data federation             │
└────────────────┬───────────────────────┘
                 │ (Virtualization & ETL)
                 │
┌────────────────▼───────────────────────┐
│   Native Datasphere Objects            │
│   - Dimensions, Fact Tables            │
│   - Analytical Models, Views           │
└────────────────────────────────────────┘
```

### Remote Conversion Step-by-Step

1. **Establish Remote BW Connection**
   - Set up read-only connection to source BW/4HANA
   - Validate network connectivity and firewall rules
   - Create dedicated RFC destination for Datasphere

2. **Create Remote View in Datasphere**
   - Create External Data Source pointing to BW remote query/provider
   - Define column mapping explicitly (no automatic detection)
   - Test remote table preview to validate connection

3. **Implement Custom Transformation**
   - Build Datasphere Transformation to apply business logic
   - Replicate ABAP BAdI logic if custom enhancements exist
   - Handle data type conversions (BW data types → SQL types)
   - Implement unit and currency handling

4. **Configure Staging Tables**
   - Create intermediate tables for transformation staging
   - Implement error handling for failed transformations
   - Add audit columns: `_LOAD_ID`, `_LOAD_TIMESTAMP`, `_SOURCE_SYSTEM`
   - Partition tables by loading period for performance

5. **Establish Data Replication Schedule**
   - Full load: Initial data population (typically 1-2x monthly)
   - Incremental load: Delta from last run (daily or hourly)
   - Monitor load performance and adjust timing
   - Implement automated failure notifications

6. **Testing and Validation**
   - Reconcile row counts: Source vs. Datasphere
   - Validate key metrics match (sum of measures by dimension)
   - Compare sample query results: BW vs. Datasphere
   - Document any data discrepancies and rationale

7. **Operationalize Remote Conversion**
   - Configure automated scheduling in Task Chains
   - Implement monitoring and alerting for load failures
   - Document runbook for manual recovery procedures
   - Plan cutover to native Datasphere (if applicable)

---

## Phase 4: Bridge-Specific Modeling

### DataStore Objects (ADSOs) in Datasphere

ADSOs in BW Bridge have special properties not found in standard tables. Understanding Bridge ADSO variants is critical.

#### ADSO Type Comparison

| Property | Standard ADSO | Inventory ADSO | Write-Interface ADSO |
|---|---|---|---|
| **Purpose** | Transactional staging | Periodic snapshots | Dimension/Master data |
| **Updates** | Full/Delta loads | Append-only (inventory) | Record management |
| **Activation** | Required after load | Incremental activation | Direct write capability |
| **Query-Ready** | Not directly queryable | Can be queried | Queryable immediately |
| **In Datasphere** | Standard Table | Fact Table (time-series) | Dimension Table |
| **Conversion Effort** | Low | Medium | High |

#### Standard ADSO Conversion

Standard ADSOs convert directly to Datasphere tables:

```yaml
BW Bridge ADSO:
  Name: 2_SALES_STAGING
  Key Fields:
    - COMPANY_CODE
    - SALES_ORG
    - PERIOD
  Data Fields:
    - AMOUNT
    - QUANTITY
    - CURRENCY

Converted to Datasphere Table:
  Name: T_SALES_STAGING
  Columns:
    - COMPANY_CODE (String, Key)
    - SALES_ORG (String, Key)
    - PERIOD (Date, Key)
    - AMOUNT (Decimal)
    - QUANTITY (Integer)
    - CURRENCY (String)
  Indexes:
    - Primary Key (COMPANY_CODE, SALES_ORG, PERIOD)
    - Index on PERIOD for time-series queries
```

#### Inventory ADSO Conversion

Inventory ADSOs maintain periodic snapshots. In Datasphere, these become fact tables with explicit time-dimensioning:

```sql
-- Inventory ADSO Structure in BW Bridge
-- Tracks balances as of specific dates
SELECT
  POSTING_DATE,
  PRODUCT_ID,
  WAREHOUSE_ID,
  OPENING_QUANTITY,
  INBOUND_QUANTITY,
  OUTBOUND_QUANTITY,
  CLOSING_QUANTITY,
  LAST_TRANSACTION_ID
FROM 3_INV_ADSO
WHERE POSTING_DATE >= '2024-01-01'
ORDER BY POSTING_DATE, PRODUCT_ID;

-- Equivalent Datasphere Fact Table
CREATE TABLE F_INVENTORY_SNAPSHOT (
  POSTING_DATE DATE NOT NULL,
  PRODUCT_ID VARCHAR(10) NOT NULL,
  WAREHOUSE_ID VARCHAR(10) NOT NULL,
  OPENING_QUANTITY DECIMAL(15,2),
  INBOUND_QUANTITY DECIMAL(15,2),
  OUTBOUND_QUANTITY DECIMAL(15,2),
  CLOSING_QUANTITY DECIMAL(15,2),
  LAST_TRANSACTION_ID VARCHAR(20),
  _LOAD_DATE DATE NOT NULL DEFAULT CURRENT_DATE,
  PRIMARY KEY (POSTING_DATE, PRODUCT_ID, WAREHOUSE_ID)
);

-- Data Access Control for inventory snapshots
-- Only allow users to see snapshots <= today
CREATE DATA ACCESS CONTROL DAC_INVENTORY_CURRENT
FOR TABLE F_INVENTORY_SNAPSHOT
FILTER BY
  POSTING_DATE <= CURRENT_DATE
AND WAREHOUSE_ID IN (SELECT ASSIGNED_WAREHOUSE FROM T_USER_WAREHOUSE_MAP
                     WHERE USER_ID = CURRENT_USER);
```

**Key Design Pattern for Inventory ADSOs:**
- Use surrogate key (`_LOAD_ID`) to track each snapshot load
- Include effective date range (`EFFECTIVE_FROM`, `EFFECTIVE_TO`) for historical queries
- Implement type-2 slowly-changing dimension for dimension tables
- Use partitioning by `POSTING_DATE` for query performance

#### Write-Interface ADSO Conversion

Write-Interface ADSOs enable direct data writing. These are complex in Datasphere as native tables are append-only. Implement a dual-table strategy:

```yaml
# BW Bridge Write-Interface ADSO
# Used for user-maintained master data (e.g., price lists)

BW Structure:
  ADSO: 4_PRICE_MASTER
  Key Fields:
    - MATERIAL_ID
    - CUSTOMER_ID
    - VALID_FROM (Date)
  Data Fields:
    - UNIT_PRICE (Decimal)
    - CURRENCY (String)
    - LAST_CHANGED (Timestamp)

Datasphere Dual-Table Approach:
  Staging Table (write-enabled):
    T_PRICE_MASTER_STAGING
    - Used only for ETL/maintenance
    - Not exposed to business users

  Production Table (read-only):
    T_PRICE_MASTER
    - Fact table for queries
    - Refreshed nightly from staging
    - Enforces historical tracking

  UI Handler (if direct user input required):
    - Use Datasphere Data Marketplace app
    - Implement custom approval workflow
    - Maintain change log in T_PRICE_MASTER_AUDIT
```

**SQL Implementation Pattern:**

```sql
-- Write-Interface ADSO equivalent: Staging table
CREATE TABLE T_PRICE_MASTER_STAGING (
  MATERIAL_ID VARCHAR(18) NOT NULL,
  CUSTOMER_ID VARCHAR(10) NOT NULL,
  VALID_FROM DATE NOT NULL,
  UNIT_PRICE DECIMAL(13,2),
  CURRENCY VARCHAR(3),
  LAST_CHANGED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHANGED_BY VARCHAR(12) DEFAULT CURRENT_USER,
  PRIMARY KEY (MATERIAL_ID, CUSTOMER_ID, VALID_FROM)
);

-- Production table: Type-2 SCD
CREATE TABLE T_PRICE_MASTER (
  MATERIAL_ID VARCHAR(18) NOT NULL,
  CUSTOMER_ID VARCHAR(10) NOT NULL,
  VALID_FROM DATE NOT NULL,
  VALID_TO DATE,
  UNIT_PRICE DECIMAL(13,2),
  CURRENCY VARCHAR(3),
  IS_CURRENT CHAR(1) DEFAULT 'X',
  _LOAD_DATE DATE NOT NULL,
  PRIMARY KEY (MATERIAL_ID, CUSTOMER_ID, VALID_FROM)
);

-- Nightly refresh job pseudo-code
-- Step 1: Mark previous current records as history
UPDATE T_PRICE_MASTER
SET IS_CURRENT = '', VALID_TO = CURRENT_DATE - 1
WHERE IS_CURRENT = 'X'
  AND (MATERIAL_ID, CUSTOMER_ID) IN (
    SELECT DISTINCT MATERIAL_ID, CUSTOMER_ID FROM T_PRICE_MASTER_STAGING
    WHERE LAST_CHANGED >= CURRENT_DATE
  );

-- Step 2: Insert new current records
INSERT INTO T_PRICE_MASTER
  SELECT MATERIAL_ID, CUSTOMER_ID, VALID_FROM, NULL, UNIT_PRICE, CURRENCY, 'X', CURRENT_DATE
  FROM T_PRICE_MASTER_STAGING
  WHERE LAST_CHANGED >= CURRENT_DATE;
```

---

## Phase 5: Process Chain to Task Chain Mapping

Process Chains in BW are the scheduling and orchestration layer. Datasphere uses Task Chains, which require manual redesign.

### Architecture: BW Process Chain vs. Datasphere Task Chain

**BW Process Chain Components:**
- Variant Processor (Variable initialization)
- Data Load (ABAP batch jobs)
- BW Cubes, ADSOs (target objects)
- Process Chain Steps (Sequential execution)
- Check and Decision steps (Conditional logic)
- Wait/Event steps (Time/event-based triggers)

**Datasphere Task Chain Components:**
- Dimensions and Tables (source objects)
- Transformation rules (data logic)
- Data transfer tasks (load execution)
- Task sequences (dependencies)
- Conditions (IF/THEN logic)
- Schedules (Cron-based timing)

### Mapping BW Process Chain Elements

| BW Process Chain | Datasphere Mapping | Design Notes |
|---|---|---|
| Load InfoCube | Data Transfer Task or Transformation | Load from BW Bridge or external source |
| Process Chain Step | Task Sequence | Single task or complex sub-workflow |
| Check variant processor | Variables in Task Chain context | Parameterize tasks dynamically |
| Decision step (IF/THEN) | Conditional execution in Task Chain | Branch based on previous results |
| Parallel branches | Parallel execution flag in Task Chain | Improves performance, requires careful ordering |
| Post-load aggregation | Materialization Task | Pre-calculate aggregates for performance |
| Process chain event | Scheduled Trigger | Create external event-driven tasks if needed |

### Process Chain to Task Chain Step-by-Step

#### Step 1: Document Process Chain Structure

```
BW Process Chain: Z_DAILY_SALES_LOAD
├── Step 1: Load Sales Master [Transaction: RSBWP_LOAD_DATA, Variant: DEFAULT]
├── Step 2: Load Sales Transactions [Transaction: RSBWP_LOAD_DATAX, Variant: DAILY]
├── Step 3: Validate Load (Check) [Min Rec: 1000, Max Rec: 1000000]
├── Step 4a: Decision [IF success THEN → Step 5, ELSE → Step 6]
├── Step 5: Aggregate Sales (PARALLEL)
│   ├── 5a: Aggregate by Product [Time: 15 min]
│   ├── 5b: Aggregate by Region [Time: 12 min]
│   └── 5c: Aggregate by Customer [Time: 10 min]
├── Step 6: Send Email Notification [Email: admin@company.com]
└── Schedule: Daily at 03:00 UTC
```

#### Step 2: Design Task Chain Structure

Create equivalent Task Chain in Datasphere:

```yaml
Task Chain: TC_DAILY_SALES_LOAD
  Description: "Datasphere equivalent of Z_DAILY_SALES_LOAD"
  Schedule: CRON "0 3 * * ?" (Daily 03:00 UTC)

  Tasks:
    1. Task: DT_LOAD_SALES_MASTER
       Type: Data Transfer
       Source: BW Bridge InfoCube 0SALES_MASTER
       Target: T_SALES_MASTER
       Runtime: ~10 min
       ErrorHandling: STOP_ON_ERROR

    2. Task: DT_LOAD_SALES_TRANSACTIONS
       Type: Data Transfer
       Source: BW Bridge InfoCube 0SALES_001
       Target: T_SALES_TRANSACTIONS
       Runtime: ~25 min
       ErrorHandling: STOP_ON_ERROR
       Variables:
         - LOAD_TYPE = DELTA
         - LAST_LOAD_DATE = <previous run date>

    3. Task: TR_VALIDATE_LOAD
       Type: Transformation (Validation Logic)
       SQL: |
         SELECT COUNT(*) as record_count FROM T_SALES_TRANSACTIONS
         WHERE _LOAD_DATE = CURRENT_DATE
       Condition: record_count >= 1000 AND record_count <= 1000000
       OnError: LOG_WARNING_AND_CONTINUE

    4. Task: TC_AGGREGATION_TASKS (Parallel Sub-Task-Chain)
       Type: Task Chain (Parallel Execution)
       Runtime: ~15 min (parallelized)

       Sub-Tasks:
         4a. Task: TR_AGG_PRODUCT
             Type: Transformation
             Target: V_SALES_BY_PRODUCT (Materialized View)

         4b. Task: TR_AGG_REGION
             Type: Transformation
             Target: V_SALES_BY_REGION

         4c. Task: TR_AGG_CUSTOMER
             Type: Transformation
             Target: V_SALES_BY_CUSTOMER

    5. Task: NOTIFY_COMPLETION
       Type: Script (Send Email)
       On Success: Send email to admin@company.com
       Template: "Daily Sales Load Completed Successfully"

  Error Handling:
    OnTaskFailure: Retry up to 3 times with 10 min interval
    OnChainFailure: Send alert email and stop
    Rollback: Not automatic; requires manual intervention
```

#### Step 3: Handle Conditional Logic

BW Process Chains use decision steps; Datasphere Task Chains use conditional task execution:

```yaml
# BW Decision Step
Decision Step: CHECK_LOAD_SUCCESS
  If: Load Step was successful
    Then: Continue to Aggregation
  If: Load Step failed
    Then: Jump to Error Handler

# Datasphere Equivalent
Task Chain: TC_WITH_DECISION
  Tasks:
    1. DT_LOAD_DATA
       SuccessCondition: "record_count > 0"
       NextTaskOnSuccess: TC_AGGREGATION
       NextTaskOnFailure: SEND_ERROR_ALERT

    2. TC_AGGREGATION
       (Conditional execution only if Task 1 succeeds)

    3. SEND_ERROR_ALERT
       (Only executed if Task 1 fails)
```

#### Step 4: Handle Variable Processors

BW Process Chains initialize variables; Datasphere Task Chains use parameters:

```yaml
# BW Variant Processor
Variant Processor: VAR_SALES_LOAD
  Variables:
    - LOAD_DATE: today() - 1
    - LOAD_TYPE: DELTA
    - COMPANY_CODE: $COMP_CODE (User input)

# Datasphere Task Chain Parameters
Task Chain: TC_SALES_LOAD
  Parameters:
    - load_date (DateTime): default = <current_date - 1 day>
    - load_type (String): default = "DELTA"
    - company_code (String): required = true

  Usage in Transformation:
    WHERE POSTING_DATE = :load_date
      AND LOAD_TYPE = :load_type
      AND COMPANY_CODE = :company_code
```

#### Step 5: Configure Queued Task Manager (QTM) Runtime

The Queued Task Manager in Datasphere manages task execution:

**Task Chain Execution Policy:**

```yaml
Task Chain: TC_DAILY_SALES_LOAD
  Execution:
    MaxConcurrentRuns: 1        # Prevent concurrent execution
    Timeout: 1 hour              # Abort if running > 1 hour
    RetryPolicy:
      MaxRetries: 3
      RetryInterval: 10 minutes
      BackoffMultiplier: 1.5     # 10, 15, 22 minutes

    RuntimeQueueing:
      Priority: NORMAL           # Can be LOW, NORMAL, HIGH
      QueueBehavior: FIFO        # First-In-First-Out

    Notifications:
      OnStart: Log entry
      OnSuccess: Email notification
      OnFailure: Alert + Log + Email
      OnRetry: Log attempt number
```

#### Step 6: Map Aggregation and Post-Load Steps

BW typically includes aggregate table maintenance; Datasphere uses materialized views:

```sql
-- BW Post-Load Aggregation (in Process Chain)
-- Creates aggregate InfoCubes based on Dimension subsets

-- Datasphere Equivalent: Materialized View
CREATE MATERIALIZED VIEW V_SALES_BY_PRODUCT AS
SELECT
  PRODUCT_ID,
  SUM(SALES_AMOUNT) as total_sales,
  SUM(QUANTITY) as total_quantity,
  COUNT(DISTINCT CUSTOMER_ID) as unique_customers,
  CURRENT_DATE as view_date
FROM T_SALES_TRANSACTIONS
WHERE POSTING_DATE >= DATEADD(month, -12, CURRENT_DATE)
GROUP BY PRODUCT_ID;

-- Refresh Schedule (Task Chain)
Task: REFRESH_MATERIALIZED_VIEWS
  Type: Materialization Task
  Views: [V_SALES_BY_PRODUCT, V_SALES_BY_REGION, V_SALES_BY_CUSTOMER]
  Schedule: Daily at 04:00 UTC
  Parallelization: Yes (refresh all views in parallel)
```

#### Step 7: Test Task Chain Execution

Before production deployment:

1. **Functional Testing**: Execute Task Chain manually, verify all tasks complete
2. **Data Validation**: Compare output with legacy Process Chain results
3. **Performance Testing**: Validate runtime is acceptable (BW baseline +/- 20%)
4. **Error Scenario Testing**: Intentionally fail steps, verify error handling works
5. **Schedule Testing**: Run on actual schedule, verify no conflicts with other processes

### Handling Complex Process Chain Scenarios

**Parallel Execution in Task Chains:**

```yaml
# BW Process Chain with parallel branches
Process Chain: Z_COMPLEX_LOAD
  ├── Serial: Load Master Data (Step 1)
  ├── Parallel Branch 1: Load Regional Data (Steps 2-4)
  │   ├── 2: Americas Load
  │   ├── 3: EMEA Load
  │   └── 4: APAC Load
  ├── Parallel Branch 2: Load Reference Data (Steps 5-6)
  │   ├── 5: Exchange Rates
  │   └── 6: GL Accounts
  ├── Sync Point: After all parallel branches complete
  └── Serial: Run Aggregations (Step 7)

# Datasphere Task Chain equivalent
Task Chain: TC_COMPLEX_LOAD
  Tasks:
    1. DT_LOAD_MASTER
       NextTask: [DT_LOAD_AMERICAS, DT_LOAD_REFDATA] (Parallel)

    2. DT_LOAD_AMERICAS (Parallel, execution starts after Task 1)
       NextTask: TC_REGIONAL_AGGREGATION (on completion)

    3. DT_LOAD_REFDATA (Parallel, execution starts after Task 1)
       NextTask: TC_REFERENCE_LOADING (on completion)

    4. TC_REGIONAL_AGGREGATION (waits for Task 2)
       NextTask: TC_FINAL_AGGREGATION (sync point)

    5. TC_REFERENCE_LOADING (waits for Task 3)
       NextTask: TC_FINAL_AGGREGATION (sync point)

    6. TC_FINAL_AGGREGATION (sync point: waits for Tasks 4 & 5)
       FinalTask: Yes
```

---

## Phase 6: Data Transfer Patterns

### Full vs. Incremental Load Strategy

**Full Load Pattern** (Initial migration):

```yaml
Full Load Strategy:
  Frequency: Once per object
  Timing: Off-peak hours (weekend or night)
  Data Volume: 100% of historical data
  Validation: Row count matching

  Steps:
    1. Extract all records from BW Bridge source
    2. Transform if needed (data type conversions, calculations)
    3. Load into Datasphere target table (TRUNCATE + INSERT)
    4. Validate: Record count, key uniqueness, NOT NULL constraints
    5. Confirm completion in migration registry

  Estimated Duration: Size(GB) / Bandwidth(Mbps/8) + Processing
  Example: 50 GB at 100 Mbps = ~1 hour + 15 min processing = 1.25 hours
```

**Incremental Load Pattern** (Ongoing updates):

```yaml
Incremental Load Strategy:
  Frequency: Daily, hourly, or real-time (depending on business need)
  Timing: Scheduled after source system completes load
  Data Volume: Only changes since last load
  Validation: Duplicate detection, referential integrity

  Steps:
    1. Determine load scope:
       - Timestamp-based: WHERE _CHANGED_AT >= :last_load_time
       - Sequence-based: WHERE _CHANGE_SEQ > :last_load_seq
       - Delta indicator: WHERE CHANGE_FLAG = 'X'

    2. Extract delta records from source
    3. Perform upsert in Datasphere:
       - For new records: INSERT
       - For updated records: UPDATE (or DELETE+INSERT for immutable tables)
       - For deleted records: Soft delete or remove depending on design

    4. Update watermark:
       - Store :last_load_time in metadata table
       - Increment :last_load_seq counter

    5. Validate: Row count in delta, uniqueness, referential integrity

  Metadata Tracking:
    Table: T_LOAD_WATERMARK
    Columns:
      - TABLE_NAME: Source table identifier
      - LAST_LOAD_TIMESTAMP: When last load occurred
      - LAST_LOAD_SEQUENCE: Sequence number if available
      - RECORD_COUNT_LOADED: Records in last load
      - STATUS: SUCCESS, FAILED, IN_PROGRESS
```

### Upsert (Insert + Update) Implementation

```sql
-- Technique 1: Merge Statement (Preferred)
MERGE INTO T_SALES_TRANSACTIONS tgt
USING T_SALES_TRANSACTIONS_DELTA src
ON (tgt.TRANSACTION_ID = src.TRANSACTION_ID
    AND tgt.LINE_ITEM_NUM = src.LINE_ITEM_NUM)
WHEN MATCHED AND src._OPERATION_FLAG = 'U'
  THEN UPDATE SET
    tgt.AMOUNT = src.AMOUNT,
    tgt.QUANTITY = src.QUANTITY,
    tgt.LAST_CHANGED = CURRENT_TIMESTAMP,
    tgt.CHANGED_BY = CURRENT_USER
WHEN MATCHED AND src._OPERATION_FLAG = 'D'
  THEN DELETE
WHEN NOT MATCHED AND src._OPERATION_FLAG IN ('I', 'U')
  THEN INSERT (TRANSACTION_ID, LINE_ITEM_NUM, AMOUNT, QUANTITY, LAST_CHANGED, CHANGED_BY)
  VALUES (src.TRANSACTION_ID, src.LINE_ITEM_NUM, src.AMOUNT, src.QUANTITY, CURRENT_TIMESTAMP, CURRENT_USER);

-- Technique 2: DELETE + INSERT (for immutable designs)
-- Delete all records from delta load period
DELETE FROM T_SALES_TRANSACTIONS
WHERE POSTING_DATE = CURRENT_DATE
  AND SOURCE_SYSTEM = 'BW_BRIDGE';

-- Insert all records from staging area
INSERT INTO T_SALES_TRANSACTIONS
SELECT * FROM T_SALES_TRANSACTIONS_STAGING
WHERE POSTING_DATE = CURRENT_DATE;

-- Technique 3: Type-2 SCD for dimension tables
-- Mark previous records as expired, insert new versions
UPDATE T_CUSTOMER_DIM
SET IS_CURRENT = '', VALID_TO = CURRENT_DATE - 1
WHERE IS_CURRENT = 'X'
  AND CUSTOMER_ID IN (SELECT CUSTOMER_ID FROM T_CUSTOMER_STAGING);

INSERT INTO T_CUSTOMER_DIM
SELECT *, 'X' as IS_CURRENT, CURRENT_DATE as VALID_FROM, NULL as VALID_TO
FROM T_CUSTOMER_STAGING;
```

### Data Reconciliation

After transfer, validate data integrity:

```sql
-- Reconciliation Query 1: Row Count Matching
SELECT
  'Row Count Check' as Check_Name,
  (SELECT COUNT(*) FROM T_BW_SOURCE) as Source_Count,
  (SELECT COUNT(*) FROM T_DATASPHERE_TARGET) as Target_Count,
  CASE WHEN (SELECT COUNT(*) FROM T_BW_SOURCE) =
            (SELECT COUNT(*) FROM T_DATASPHERE_TARGET)
       THEN 'PASS' ELSE 'FAIL' END as Status;

-- Reconciliation Query 2: Key Uniqueness
SELECT
  'Key Uniqueness' as Check_Name,
  CASE WHEN (SELECT COUNT(*) FROM T_DATASPHERE_TARGET) =
            (SELECT COUNT(DISTINCT KEY_FIELD_1, KEY_FIELD_2) FROM T_DATASPHERE_TARGET)
       THEN 'PASS' ELSE 'FAIL' END as Status,
  (SELECT COUNT(*) FROM T_DATASPHERE_TARGET) as Total_Records,
  (SELECT COUNT(DISTINCT KEY_FIELD_1, KEY_FIELD_2) FROM T_DATASPHERE_TARGET) as Unique_Keys;

-- Reconciliation Query 3: Key Aggregate Matching
SELECT
  DIMENSION_FIELD,
  COUNT(*) as Count_Source,
  SUM(AMOUNT) as Sum_Amount_Source
FROM T_BW_SOURCE
GROUP BY DIMENSION_FIELD
UNION ALL
SELECT
  DIMENSION_FIELD,
  COUNT(*) as Count_Target,
  SUM(AMOUNT) as Sum_Amount_Target
FROM T_DATASPHERE_TARGET
GROUP BY DIMENSION_FIELD;

-- Reconciliation Query 4: Data Quality Checks
SELECT
  'Data Quality' as Check_Category,
  'NULL values in Amount' as Issue,
  COUNT(*) as Record_Count
FROM T_DATASPHERE_TARGET
WHERE AMOUNT IS NULL
HAVING COUNT(*) > 0;

SELECT
  'Data Quality' as Check_Category,
  'Invalid Currency Code' as Issue,
  COUNT(*) as Record_Count
FROM T_DATASPHERE_TARGET
WHERE CURRENCY NOT IN ('USD', 'EUR', 'GBP', 'JPY')
HAVING COUNT(*) > 0;
```

---

## Phase 7: Hybrid Operations

During migration, BW Bridge and native Datasphere run in parallel.

### Parallel Reporting Architecture

```
┌──────────────────────────────────────────────────────┐
│           Unified Reporting Layer                    │
│ (BI Tools: SAC, Power BI, Tableau, Looker)          │
└──────────┬──────────────────────────────┬────────────┘
           │ (Dual queries)               │
    ┌──────▼──────────┐        ┌──────────▼─────┐
    │  BW Bridge      │        │  Native DS      │
    │  (Converted     │        │  (New objects)  │
    │   objects)      │        │                 │
    └─────────────────┘        └─────────────────┘

Migration Phase:
- Phase 1 (Weeks 1-4): Parallel testing
  - Reports pull from BOTH sources
  - Results reconciled nightly
  - Users provide feedback

- Phase 2 (Weeks 5-6): Gradual cutover
  - Critical reports → Native DS
  - Secondary reports → Still use Bridge

- Phase 3 (Week 7+): Complete cutover
  - All reports → Native DS
  - Bridge decommissioned
```

### Reporting Reconciliation During Migration

```yaml
Report Reconciliation Process:
  Daily Task:
    1. Extract report data from BW Bridge version
    2. Extract report data from Datasphere version
    3. Compare key metrics (with tolerance):
       - Row counts (tolerance: ±0.1%)
       - Sum of key measures (tolerance: ±0.01%)
    4. Flag discrepancies > tolerance
    5. Investigate root cause if discrepancies found

  Root Cause Analysis:
    - Data not transferred yet
    - Different filter logic in conversion
    - Rounding or aggregation differences
    - Incomplete incremental load

  Resolution:
    - Validate conversion logic
    - Adjust filters if needed
    - Re-run data transfer
    - Extend testing period if critical discrepancy
```

### Managing User Transition

```
Migration Communication Plan:

Week 1-2: Announcement
  - Explain BW → Datasphere transition
  - Highlight benefits (speed, cloud-native, lower TCO)
  - Share timeline

Week 3-4: Training
  - New Datasphere interface walkthrough
  - Differences from BW querying
  - Performance expectations
  - Support contact info

Week 5-6: Parallel Reporting
  - Users test Datasphere reports
  - Report issues to project team
  - Provide feedback on accuracy

Week 7: Cutover Window
  - BW Bridge reports become read-only (2-4 hours)
  - Verify final data sync
  - Switch all reports to Datasphere
  - Go-live validation

Post-Cutover: Support
  - Monitor query performance
  - Respond to user issues
  - Optimize slow queries
  - Track cost/performance metrics
```

---

## Phase 8: Decommissioning the Bridge

Once migration is complete and users are comfortable with native Datasphere, decommission the Bridge.

### Decommissioning Checklist

```
Pre-Decommissioning (2 weeks before):
☐ All critical reports migrated to Datasphere
☐ All historical data verified in Datasphere
☐ Users trained and comfortable
☐ Performance baseline established
☐ Backup/archival of BW metadata completed
☐ Legal/compliance sign-off obtained

Decommissioning (Final window):
☐ Final data sync: BW Bridge → Datasphere
☐ Verify no active Task Chains dependent on Bridge
☐ Disable BW Bridge connections
☐ Archive BW Bridge database
☐ Revoke user access to Bridge
☐ Update documentation: systems inventory, data lineage diagrams

Post-Decommissioning (30 days):
☐ Monitor for any Bridge connection attempts (should be zero)
☐ Monitor Datasphere performance (confirm no degradation)
☐ Archive BW Bridge infrastructure
☐ Document migration lessons learned
☐ Update training materials
☐ Schedule post-implementation review meeting

Fallback Procedure (if critical issues):
☐ Keep BW Bridge in read-only mode for 30 days
☐ Maintain daily backup exports from Bridge
☐ Document any queries that fail in Datasphere
☐ Have rollback plan ready (requires Bridge licensing extension)
```

---

## Common Migration Pitfalls

### Pitfall 1: Insufficient Data Validation

**Problem**: Proceed to cutover without reconciling source vs. target data.

**Prevention**:
- Implement automated reconciliation queries (see Phase 6)
- Require sign-off from business data steward
- Run parallel reports for 2+ weeks minimum
- Document tolerance levels for acceptable variance

### Pitfall 2: Complex Custom Logic Not Translated

**Problem**: BW custom calculations (BAdIs, user-exits) not replicated in Datasphere.

**Prevention**:
- Inventory all custom logic early (Phase 1)
- Document ABAP code and business purpose
- Rebuild logic as Datasphere transformation rules
- Validate calculated values match source

### Pitfall 3: Process Chain Dependencies Overlooked

**Problem**: Task Chains fail due to missing dependencies or incorrect sequencing.

**Prevention**:
- Document all Process Chain step dependencies (Phase 5)
- Test Task Chain execution thoroughly before go-live
- Implement error handling and notifications
- Have runbook for manual recovery

### Pitfall 4: Performance Regression After Migration

**Problem**: Datasphere reports run slower than expected.

**Prevention**:
- Establish BW baseline performance metrics
- Set Datasphere performance targets (goal: 3-10x faster)
- Implement indexes and partitioning
- Monitor query performance continuously
- Optimize slow queries identified in testing

### Pitfall 5: Authorization Loss During Migration

**Problem**: Data security lost when converting BW authorizations to DACs.

**Prevention**:
- Map BW Analysis Authorizations to DACs early (Phase 1)
- Test DAC filtering with diverse user groups
- Implement audit logging for sensitive data access
- Validate user can/cannot see appropriate rows
- Use Data Access Controls (covered in Security Architect skill)

### Pitfall 6: Incomplete Historical Data Transfer

**Problem**: Some time periods missing in Datasphere due to load failure.

**Prevention**:
- Implement data completeness checks by time period
- Run full load verification query:
  ```sql
  SELECT POSTING_DATE, COUNT(*) FROM T_DATASPHERE_TARGET
  GROUP BY POSTING_DATE ORDER BY POSTING_DATE;
  ```
- Identify and re-run failed loads
- Keep detailed load execution log

### Pitfall 7: Naming Conventions Create Confusion

**Problem**: Users cannot find converted objects due to renamed InfoCubes/ADSOs.

**Prevention**:
- Create naming convention mapping document
- Distribute to all users before cutover
- Create synonyms/aliases if tools support
- Add descriptive metadata/descriptions to objects
- Test report re-pointing before go-live

---

## Migration Runbook Template

```yaml
Migration Runbook: Z_SALES_MASTER_CUBE

Object Identification:
  Source: Z_SALES_MASTER (InfoCube)
  Size: 45 GB
  Record Count: 250 million transactions
  Key Fields: COMPANY, SALES_ORG, CUSTOMER, POSTING_DATE

Conversion Approach: Shell Conversion
Complexity Level: Medium
Risk Score: 8/25 (Medium-Low)

Execution Schedule:
  Phase: Wave 3 (Weeks 6-7)
  Shell Conversion Window: 2024-03-15 03:00-04:30 UTC (1.5 hours)
  Data Transfer: 2024-03-15 04:30-06:00 UTC (1.5 hours)
  Validation: 2024-03-15 06:00-08:00 UTC (2 hours)
  User Acceptance Testing: 2024-03-15 to 2024-03-20
  Production Cutover: 2024-03-22 03:00 UTC

Pre-Execution Steps:
  ☐ Verify backup of source InfoCube
  ☐ Confirm BW Bridge availability
  ☐ Disable dependent Process Chains
  ☐ Notify users of maintenance window
  ☐ Prepare rollback plan

Execution Steps:
  1. [03:00] Execute Shell Conversion
     Command: STC01 → Propose Conversion → Execute
     Expected Duration: 30 minutes
     Success Criteria: 0 errors, object created in Datasphere

  2. [03:35] Monitor Conversion Progress
     Transaction: SM37 (check batch job logs)
     Logs to Check: CONVERSION_Z_SALES_MASTER job

  3. [04:00] Validate Shell Conversion
     Verify: Object exists in Datasphere, field count matches
     SQL: SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'T_SALES_MASTER'

  4. [04:30] Initiate Full Data Load
     Task: DT_LOAD_SALES_MASTER
     Source: BW Bridge T_SALES_MASTER
     Target: Datasphere T_SALES_MASTER
     Options: Truncate existing, Full load

  5. [06:00] Monitor Data Load
     Check: Row count progress in both systems
     SQL: SELECT COUNT(*) FROM T_SALES_MASTER_STAGING, T_SALES_MASTER (target)

  6. [06:15] Data Load Completion
     Expected: All 250M records transferred
     Validation: Row count matching ±0.1%

  7. [06:30] Run Reconciliation Queries
     Query 1: Row count by COMPANY
     Query 2: Sum of SALES_AMOUNT by SALES_ORG
     Tolerance: ±0.01%

  8. [07:00] Create Datasphere Views
     Views: V_SALES_BY_PRODUCT, V_SALES_BY_REGION
     Type: Materialized
     Refresh: Daily at 04:00

  9. [08:00] Enable Reporting
     Update BI tool connections
     Point reports to Datasphere objects
     Enable read-only access for UAT

Post-Execution Steps:
  ☐ Verify no production queries against BW Bridge source
  ☐ Monitor Datasphere CPU/memory utilization
  ☐ Respond to UAT user issues
  ☐ Update documentation
  ☐ Schedule final cutover validation

Rollback Procedure (if issues detected):
  1. Disable Datasphere connections in BI tools
  2. Re-enable BW Bridge queries (kept as fallback)
  3. Halt incremental load Task Chain
  4. Delete failed Datasphere objects
  5. Investigate root cause
  6. Schedule retry within 48 hours

Escalation Contacts:
  Datasphere Admin: John Smith (john.smith@company.com)
  BW Bridge Specialist: Jane Doe (jane.doe@company.com)
  Data Quality Lead: Bob Johnson (bob.johnson@company.com)

Lessons Learned (Post-Cutover):
  <To be filled after execution>
```

---

## MCP Tool References

This skill integrates with these Claude MCP tools:

- **search_repository**: Find BW objects, transformations, and Task Chains by keyword
- **get_object_definition**: Retrieve complete object metadata, field definitions, and properties
- **list_repository_objects**: Browse all objects in a space, filter by type, see creation dates
- **get_task_status**: Check Task Chain execution progress, view logs, identify failures

**Example Usage:**

```
Assistant: "Let me search for your existing SALES InfoCubes in Datasphere."
Tool: search_repository(pattern: "SALES", object_type: "INFOCUBE")