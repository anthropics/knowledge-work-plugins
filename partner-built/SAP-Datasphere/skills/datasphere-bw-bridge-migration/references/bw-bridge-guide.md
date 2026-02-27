# BW Bridge Migration Reference Guide

## Table of Contents

1. Shell Conversion Step-by-Step Checklist
2. Remote Conversion Checklist
3. Object Compatibility Matrix
4. ADSO Type Comparison Details
5. Process Chain to Task Chain Mapping Patterns
6. STC01 Task List Error Codes
7. Migration Timeline Template
8. Rollback and Fallback Procedures

---

## 1. Shell Conversion Step-by-Step Checklist

### Pre-Conversion Phase (Days 1-3)

**Week Before Conversion:**
- [ ] Schedule conversion window (weekend or off-peak hours)
- [ ] Notify all users of downtime
- [ ] Disable dependent Process Chains
- [ ] Create database backup in source BW system
- [ ] Document current InfoCube structure (field list)
- [ ] Export object metadata to spreadsheet

**Day Before Conversion:**
- [ ] Run BW consistency check: **RSRV** transaction
- [ ] Fix any inconsistencies identified
- [ ] Verify BW Bridge system is accessible
- [ ] Test Datasphere connection from BW Bridge
- [ ] Confirm user has STC01 execution rights
- [ ] Review conversion task proposal

**Conversion Day - 2 Hours Before:**
- [ ] Stop all batch jobs accessing the InfoCube
- [ ] Verify no users logged into queries
- [ ] Final backup of metadata
- [ ] Confirm support team is available
- [ ] Have rollback plan ready

### Shell Conversion Execution Phase (Hours 1-2)

**Step 1: Access STC01 Transaction** (5 minutes)
```
Path: SAP GUI → /H /STC01
Authentication: Use BW administrator account
Location: BW Bridge system (not source BW)
```

**Step 2: Select Source Object** (10 minutes)
```
Transaction: STC01
Action: View Task List → Select "InfoCubes" or "ADSOs"
Selection:
  ☐ Object Name: [e.g., 0SALES_001]
  ☐ Verify object type matches expected
  ☐ Confirm object is not in use
  ☐ Note object size in GBs
```

**Step 3: Propose Conversion** (15 minutes)
```
Action: Click "Propose Conversion" button
System Response: Pre-conversion compatibility scan
Review Proposal Report:
  ☐ Number of characteristics identified
  ☐ Number of key figures identified
  ☐ Warnings (if any)
  ☐ Unsupported elements (if any)

Handling Warnings:
  ✓ Non-critical: can proceed
  ✓ Unsupported attributes: plan manual rebuild
  ✗ Critical: cancel and investigate

If Critical Issues:
  - Fix in source system
  - Re-run consistency check
  - Attempt conversion again
```

**Step 4: Validate Conversion Proposal** (15 minutes)
```
Review System-Generated Report:
  ☐ Field mapping completeness (100%?)
  ☐ Data type compatibility (all convertible?)
  ☐ Key field identification (correct?)
  ☐ Navigational attribute handling (mapped?)
  ☐ Hierarchy recognition (detected?)

Data Type Mapping Validation:
  BW Type          → Datasphere Type      ✓ Verify
  ─────────────────────────────────────────
  NUMC            → VARCHAR              [ ]
  DEC             → DECIMAL              [ ]
  DATS            → DATE                 [ ]
  TIMS            → TIME                 [ ]
  CHAR            → VARCHAR              [ ]
  CLNT            → VARCHAR              [ ]
```

**Step 5: Execute Conversion** (30 minutes)
```
Action: Click "Execute Conversion" button
Confirmation Dialog: "Confirm shell conversion of [OBJECT_NAME]?"
  ☐ Confirm by entering object name
  ☐ Click OK to proceed

System Process:
  1. Lock object in BW Bridge (prevent access)
  2. Read object metadata
  3. Generate Datasphere DDL scripts
  4. Create Datasphere tables/dimensions
  5. Create supporting objects (hierarchies, attributes)
  6. Validate object creation
  7. Update migration registry

Expected Duration: 15-45 minutes (depending on size)

Monitoring:
  ☐ Check batch job progress: SM37 (Job name: CONVERSION_xxxxx)
  ☐ Monitor temp tablespace usage: DB02
  ☐ If > 90% utilization, contact DBAs
```

### Post-Conversion Validation Phase (1-3 Hours)

**Step 6: Verify Object Creation** (30 minutes)
```
Location: Datasphere Repository Browser

Verification Checklist:
  ☐ Table exists with correct name
  ☐ Primary key fields present
  ☐ All characteristics converted to columns
  ☐ All key figures converted to measures
  ☐ Field count matches original (Count: ___)
  ☐ Data types are correct (spot-check 5 fields)
  ☐ Object marked as "Readable"
  ☐ Metadata populated (description, owner, etc.)

SQL Validation Query:
  SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE
  FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_NAME = 'T_[CONVERTED_NAME]'
  ORDER BY ORDINAL_POSITION;

  Expected Result: X rows (X = characteristic count + key figure count + system columns)
```

**Step 7: Data Transfer Configuration** (45 minutes)
```
Create Data Transfer Task:

Task Name: DT_LOAD_[OBJECTNAME]_FULL
Source:
  ☐ Connection: BW Bridge
  ☐ Source Object: [Original InfoCube/ADSO]
  ☐ Load Type: FULL_LOAD

Target:
  ☐ Datasphere Target Table: T_[OBJECTNAME]
  ☐ Load Behavior: TRUNCATE_AND_INSERT
  ☐ Error Handling: STOP_ON_ERROR

Scheduling:
  ☐ Frequency: One-time (initial load)
  ☐ Timing: Off-peak hours
```

**Step 8: Execute Full Data Load** (Variable - 30 min to 4 hours)
```
Action: Manually trigger data transfer task

Pre-Load Validation:
  ☐ Source object accessible
  ☐ Target table writable
  ☐ Network connectivity confirmed
  ☐ Estimated load time communicated to stakeholders

During Load Monitoring:
  Task: DT_LOAD_[OBJECTNAME]_FULL

  Check Progress Every 10 Minutes:
    ☐ Records processed: ___ / total
    ☐ Data transferred: ___ GB
    ☐ Error count: ___
    ☐ Estimated time remaining: ___
    ☐ CPU/Memory utilization: ___ / ___ %

Load Performance Metrics:
  Metric                        Target        Actual
  ─────────────────────────────────────────────────
  Records/Sec                   > 100K        ___
  GB/Sec                        > 1 GB        ___
  Network Utilization           < 80%         ___
  Datasphere CPU                < 75%         ___
```

**Step 9: Validate Loaded Data** (60 minutes)
```
Data Quality Checks (Run in Datasphere):

1. Row Count Validation
   Source Query:
     SELECT COUNT(*) FROM [BW_SOURCE_TABLE]
   Target Query:
     SELECT COUNT(*) FROM T_[OBJECTNAME]

   Expected: Match exactly (or ±0.1% if incremental flagging)
   ☐ PASS: ___,___ records in both
   ☐ FAIL: Source ___, Target ___ (Variance: __%)

2. Key Uniqueness Validation
   Query:
     SELECT COUNT(*), COUNT(DISTINCT [KEY_FIELDS])
     FROM T_[OBJECTNAME]

   Expected: Both counts equal (no duplicate keys)
   ☐ PASS: No duplicates detected
   ☐ FAIL: ___ duplicate keys found

3. NOT NULL Constraint Validation
   Query:
     SELECT COUNT(*) FROM T_[OBJECTNAME]
     WHERE [REQUIRED_FIELD] IS NULL

   Expected: 0 records
   ☐ PASS: No NULL values
   ☐ FAIL: ___ NULL values found in [FIELD]

4. Measure Aggregation Validation
   BW Query:
     SELECT SUM([KEY_FIGURE_1]) FROM 0SALES_001
     WHERE [FILTER_1] = 'VALUE'

   Datasphere Query:
     SELECT SUM([MEASURE_1]) FROM T_SALES_001
     WHERE [FILTER_1] = 'VALUE'

   Expected: Numeric match (same decimals)
   ☐ PASS: Both = ___,___,___.__
   ☐ FAIL: Source __, Target __ (Variance: __%)

5. Dimension Value Distribution Check
   Query:
     SELECT DIMENSION_FIELD, COUNT(*)
     FROM T_[OBJECTNAME]
     GROUP BY DIMENSION_FIELD
     ORDER BY COUNT(*) DESC

   Expected: Distribution matches source
   ☐ PASS: Top 10 values match source
   ☐ FAIL: Top value mismatch - [VALUE] source vs [VALUE] target

6. Date Range Validation
   Query:
     SELECT MIN(POSTING_DATE), MAX(POSTING_DATE), COUNT(DISTINCT POSTING_DATE)
     FROM T_[OBJECTNAME]

   Expected: Full date range covered (no gaps)
   ☐ PASS: Min ____, Max ____, ___ unique dates
   ☐ FAIL: Gap detected: ____

7. Data Type Spot Check (Sample 5 Fields)
   ☐ Field [NAME] - Type [VARCHAR] - Sample: '[value]'
   ☐ Field [NAME] - Type [DECIMAL] - Sample: [123.45]
   ☐ Field [NAME] - Type [DATE] - Sample: [2024-01-15]
   ☐ Field [NAME] - Type [INTEGER] - Sample: [999]
   ☐ Field [NAME] - Type [VARCHAR] - Sample: '[value]'
```

**Step 10: Create Dependent Objects** (30 minutes)
```
Hierarchies (if applicable):
  ☐ Create dimension hierarchies matching BW
  ☐ Test hierarchy navigation in Datasphere
  ☐ Validate parent-child relationships
  ☐ Confirm all nodes present

Analytical Models:
  ☐ Create analytical model on converted table
  ☐ Map dimensions and measures
  ☐ Configure filters/variables if needed
  ☐ Test query execution

Materialized Views (for aggregate tables):
  ☐ Create MV for pre-aggregated reporting
  ☐ Define refresh schedule
  ☐ Test query performance
```

**Step 11: User Acceptance Testing (Days 1-7 Post-Conversion)**
```
UAT Activities:

Day 1: System Orientation
  ☐ Open sample query in Datasphere
  ☐ Review result set (compare with BW)
  ☐ Train users on new interface
  ☐ Gather initial feedback

Day 2-3: Functional Testing
  ☐ Execute 5-10 key reports from converted object
  ☐ Verify results match BW reports
  ☐ Test filtering and drill-down
  ☐ Validate calculations and aggregations

Day 4-5: Performance Testing
  ☐ Compare query execution time (BW vs. Datasphere)
  ☐ Document baseline metrics
  ☐ Verify performance meets expectations (goal: 3-10x faster)
  ☐ If slower, escalate for optimization

Day 6-7: User Acceptance
  ☐ Collect sign-off from business owner
  ☐ Document any issues or enhancement requests
  ☐ Archive UAT results
  ☐ Schedule production cutover

UAT Sign-Off Template:
  Object: [NAME]
  Tester: [NAME]
  Date: [DATE]
  Result: ☐ APPROVED ☐ APPROVED WITH ISSUES ☐ REJECTED
  Issues Found: [List any defects]
  Performance: [Baseline vs. Datasphere metrics]
  Notes: [Additional comments]
```

**Step 12: Production Cutover** (4 hours)
```
Cutover Window: [Start Time] - [End Time] (Recommended: 03:00-07:00 UTC)

Pre-Cutover (T-30 min):
  ☐ Disable BW Bridge connections (read-only mode)
  ☐ Verify no active queries
  ☐ Final data sync (if incremental load pending)
  ☐ Confirm support team on call

Cutover Execution (T+0):
  ☐ Final validation query execution
  ☐ Update BI tool connections (point to Datasphere)
  ☐ Enable Datasphere object for production use
  ☐ Notify users of availability

Post-Cutover (T+2 hours):
  ☐ Monitor query execution
  ☐ Check system performance
  ☐ Respond to user issues
  ☐ Verify no Bridge access attempts

Post-Cutover (T+24 hours):
  ☐ Confirm reports are using Datasphere source
  ☐ Gather user feedback
  ☐ Document any issues
  ☐ Schedule follow-up optimization

Post-Cutover (T+7 days):
  ☐ Decommission BW Bridge connection (archive for 30 days)
  ☐ Archive legacy object definition
  ☐ Update data lineage documentation
  ☐ Complete migration registry entry
```

---

## 2. Remote Conversion Checklist

**Applicable For:** Composite Providers, Complex Scenarios, Gradual Cutover Requirements

### Pre-Remote Conversion Phase (Days 1-2)

- [ ] Assess if Shell Conversion is insufficient
- [ ] Document reasons for Remote Conversion choice
- [ ] Create RFC destination to source BW system
- [ ] Test network connectivity (latency, bandwidth)
- [ ] Identify custom transformation logic needed
- [ ] Plan staging table structure
- [ ] Estimate data volume and transfer time

### Remote Conversion Setup Phase (Days 3-5)

- [ ] Create External Data Source (connection to remote BW)
- [ ] Create Remote View in Datasphere
- [ ] Map BW fields to Datasphere columns
- [ ] Test remote table preview
- [ ] Create staging table (intermediate)
- [ ] Build Transformation rules for data logic
- [ ] Implement error handling and logging

### Data Replication Configuration (Days 6-7)

- [ ] Define full load strategy
- [ ] Define incremental load strategy
- [ ] Create Task Chain for scheduling
- [ ] Set up monitoring and alerts
- [ ] Test data transfer
- [ ] Validate data quality
- [ ] Document operational procedures

### Testing and Validation (Days 8-10)

- [ ] Execute full load test
- [ ] Run incremental load test
- [ ] Validate data reconciliation
- [ ] Test error scenarios
- [ ] Performance test
- [ ] User acceptance test
- [ ] Sign-off from business owner

---

## 3. Object Compatibility Matrix

### InfoCube / Composite Provider Convertibility

| Component | Convertible | Shell/Remote | Complexity | Notes |
|---|---|---|---|---|
| **Standard Characteristics** | Yes | Shell | Low | Direct mapping to dimension |
| Navigational Attributes | Partial | Shell | Low | Convert if exist; add if missing |
| Time Characteristics | Yes | Shell | Low | Special handling for fiscal periods |
| Number Range | Yes | Shell | Low | Becomes integer/decimal |
| **Standard Key Figures** | Yes | Shell | Low | Direct mapping to measure |
| Cumulated Key Figures | Yes | Shell | Low | Can be calculated in model |
| Restricted Key Figures | Yes | Shell | Medium | Becomes calculated measure |
| Calculated Key Figures | Partial | Both | Medium | May need recoding in Datasphere |
| **Hierarchies** | Yes | Shell | Low | Converted to dimension hierarchies |
| Custom Hierarchies | Yes | Shell | Medium | Requires node master data |
| Time-Dependent Hierarchies | Partial | Remote | High | Use versioned hierarchies |
| **Aggregate Tables** | Yes | Shell | Low | Converted to materialized views |
| Partitioned Aggregates | Yes | Shell | Medium | Maintain partition logic |
| **ABAP Enhancements** | No | Remote | High | Replicate logic in transformation |
| User-Exit Logic | No | Remote | High | Implement in Datasphere |
| BAdI Implementation | No | Remote | High | Convert ABAP to SQL |

### DataStore Object (ADSO) Convertibility

| ADSO Type | Convertible | Approach | Complexity | Target Object |
|---|---|---|---|---|
| **Standard ADSO** | Yes | Shell | Low | Fact Table |
| Inventory ADSO | Yes | Shell/Hybrid | Medium | Fact Table (Type-2 SCD) |
| Write-Interface ADSO | Partial | Remote | High | Dual Table (Staging + Production) |
| Hierarchical ADSO | Yes | Shell | Medium | Dimension Table |
| Multi-Dimensional ADSO | Yes | Shell | Medium | Star Schema (fact + dims) |

### Query and Analytics Convertibility

| Query Component | Convertible | Approach | Notes |
|---|---|---|---|
| **Query Filters** | Yes | Analytical Model | Parameterized filters work |
| Drill-Down Paths | Yes | Analytical Model | Configure hierarchy navigation |
| Calculated Columns | Partial | Analytical Model | Rewrite if complex ABAP |
| Sorting | Yes | Analytical Model | Standard SQL ORDER BY |
| Grouping/Subtotals | Yes | Analytical Model | SQL GROUP BY + WITH ROLLUP |
| Formatting | Partial | BI Tool | Move to reporting layer |
| Exceptions | Partial | Alerting | Use Datasphere alerts/rules |

---

## 4. ADSO Type Comparison Details

### Standard ADSO

```
Purpose: Staging area for incremental data loads
Characteristics:
  - Requires activation after load
  - Not query-ready until activated
  - Optimized for ETL processes
  - Supports Insert, Update, Delete
  - Supports partitioning by time

Load Flow:
  1. Extract data from source
  2. Load into ADSO (inbound table)
  3. Activate ADSO (moves to active table)
  4. Available for queries

Datasphere Equivalent: Standard Fact Table
Design:
  CREATE TABLE T_STAGING (
    KEY_FIELD_1 VARCHAR(10) NOT NULL,
    KEY_FIELD_2 DATE NOT NULL,
    MEASURE_1 DECIMAL(15,2),
    MEASURE_2 INTEGER,
    _LOAD_ID INTEGER,
    PRIMARY KEY (KEY_FIELD_1, KEY_FIELD_2)
  );

  -- Separate production table (optional)
  CREATE TABLE T_PRODUCTION AS
  SELECT * FROM T_STAGING
  WHERE _LOAD_DATE = CURRENT_DATE;
```

### Inventory ADSO

```
Purpose: Track inventory balances at specific points in time
Characteristics:
  - Append-only (no updates to historical records)
  - Time-dimensioned (POSTING_DATE key field)
  - Can be queried directly
  - Efficient for balance sheet reporting
  - Supports balance carry-forward

Load Flow:
  1. Extract inventory snapshot as of date X
  2. Append to Inventory ADSO
  3. Query-ready immediately (no activation needed)
  4. Historical snapshots preserved forever

Datasphere Equivalent: Fact Table with Type-2 SCD
Design:
  CREATE TABLE T_INVENTORY (
    POSTING_DATE DATE NOT NULL,
    PRODUCT_ID VARCHAR(18) NOT NULL,
    WAREHOUSE_ID VARCHAR(10) NOT NULL,
    OPENING_BALANCE DECIMAL(15,2),
    RECEIPTS DECIMAL(15,2),
    ISSUES DECIMAL(15,2),
    CLOSING_BALANCE DECIMAL(15,2),
    LAST_MOVEMENT_DATE DATE,
    IS_CURRENT CHAR(1) DEFAULT 'X',
    _LOAD_DATE DATE,
    PRIMARY KEY (POSTING_DATE, PRODUCT_ID, WAREHOUSE_ID)
  );

  -- Query: Get current inventory (as of today)
  SELECT
    PRODUCT_ID,
    WAREHOUSE_ID,
    CLOSING_BALANCE,
    POSTING_DATE
  FROM T_INVENTORY
  WHERE POSTING_DATE = CURRENT_DATE
    AND IS_CURRENT = 'X';

  -- Query: Historical inventory (balance as of specific date)
  SELECT
    PRODUCT_ID,
    WAREHOUSE_ID,
    CLOSING_BALANCE,
    POSTING_DATE
  FROM T_INVENTORY
  WHERE POSTING_DATE = '2024-01-31'
    AND IS_CURRENT = 'X';
```

### Write-Interface ADSO

```
Purpose: Master data with direct user write capability
Characteristics:
  - Can be written to directly (bypassing ETL)
  - Query-ready immediately
  - Typically small (thousands of records)
  - Examples: Price lists, Discount tables, Exception rules
  - Supports versioning/effective dating

Load Flow:
  1. Users enter/modify data directly
  2. Data available immediately
  3. ETL can also load/update
  4. Queries can access latest version
  5. Historical tracking via effective dates

Datasphere Equivalent: Dual-Table Pattern

Design Approach 1: Simple Time-Versioned
  CREATE TABLE T_PRICE_MASTER (
    MATERIAL_ID VARCHAR(18) NOT NULL,
    CUSTOMER_ID VARCHAR(10),
    VALID_FROM DATE NOT NULL,
    VALID_TO DATE,
    UNIT_PRICE DECIMAL(13,2),
    CURRENCY VARCHAR(3),
    CREATED_BY VARCHAR(12),
    CREATED_AT TIMESTAMP,
    MODIFIED_BY VARCHAR(12),
    MODIFIED_AT TIMESTAMP,
    IS_CURRENT CHAR(1) DEFAULT 'X',
    PRIMARY KEY (MATERIAL_ID, CUSTOMER_ID, VALID_FROM)
  );

Design Approach 2: Dual-Table (Staging + Read)
  Staging Table (Write-enabled via app):
    T_PRICE_MASTER_STAGING
    - Used by data entry application
    - Direct INSERT/UPDATE operations
    - Not exposed to queries

  Production Table (Read-only):
    T_PRICE_MASTER
    - Refreshed hourly from staging
    - Exposed to BI queries
    - Maintains history

  Application Layer:
    - Users interact with Datasphere Data Marketplace
    - Custom approval workflow
    - Logs changes to T_PRICE_MASTER_AUDIT

  Refresh Job (hourly):
    -- Archive old current records
    UPDATE T_PRICE_MASTER
    SET IS_CURRENT = '', VALID_TO = CURRENT_DATE
    WHERE IS_CURRENT = 'X'
      AND (MATERIAL_ID, CUSTOMER_ID) IN (
        SELECT DISTINCT MATERIAL_ID, CUSTOMER_ID
        FROM T_PRICE_MASTER_STAGING
        WHERE MODIFIED_AT >= DATEADD(hour, -1, CURRENT_TIMESTAMP)
      );

    -- Insert new current records
    INSERT INTO T_PRICE_MASTER
    SELECT MATERIAL_ID, CUSTOMER_ID, VALID_FROM, NULL, UNIT_PRICE,
           CURRENCY, CREATED_BY, CREATED_AT, MODIFIED_BY, MODIFIED_AT,
           'X', CURRENT_DATE
    FROM T_PRICE_MASTER_STAGING
    WHERE MODIFIED_AT >= DATEADD(hour, -1, CURRENT_TIMESTAMP);
```

---

## 5. Process Chain to Task Chain Mapping Patterns

### Pattern 1: Sequential Load with Validation

**BW Process Chain:**
```
Start
  └─ Step 1: Load Master (InfoCube 0CUSTOMER)
     └─ Step 2: Load Transactions (InfoCube 0SALES)
        └─ Step 3: Check (Min: 100 records, Max: 10M records)
           ├─ If Success → Step 4: Aggregate
           └─ If Error → Step 5: Send Alert
```

**Datasphere Task Chain:**
```yaml
Task Chain: TC_SEQUENTIAL_LOAD_WITH_VALIDATION
  Tasks:
    1. DT_LOAD_CUSTOMER
       Type: Data Transfer
       Source: BW Bridge 0CUSTOMER
       Target: T_CUSTOMER
       Dependencies: None (Start)
       OnError: FAIL_ENTIRE_CHAIN

    2. DT_LOAD_SALES
       Type: Data Transfer
       Source: BW Bridge 0SALES
       Target: T_SALES
       Dependencies: Task 1 Success
       OnError: FAIL_ENTIRE_CHAIN

    3. TR_VALIDATE_LOAD
       Type: Transformation
       SQL: |
         SELECT COUNT(*) as load_count
         INTO @load_count
         FROM T_SALES
         WHERE _LOAD_DATE = CURRENT_DATE;

         IF @load_count < 100 OR @load_count > 10000000
           THEN SIGNAL SQLEXCEPTION;

       Dependencies: Task 2 Success
       OnError: GOTO Task 5

    4. TR_AGGREGATE_SALES
       Type: Transformation
       SQL: CREATE MATERIALIZED VIEW V_SALES_AGG AS ...
       Dependencies: Task 3 Success
       OnError: LOG_WARNING_CONTINUE

    5. SEND_ALERT
       Type: Script
       Action: Send email to admin@company.com
       Trigger: OnError from Task 3
```

### Pattern 2: Parallel Load with Synchronization Point

**BW Process Chain:**
```
Start
  ├─ Step 1: Load Regional Data (Americas, EMEA, APAC in parallel)
  ├─ Step 2: Load Reference Data (Rates, GL Accounts in parallel)
  └─ Sync Point (wait for all branches)
     └─ Step 3: Reconcile & Aggregate
```

**Datasphere Task Chain:**
```yaml
Task Chain: TC_PARALLEL_WITH_SYNC
  Tasks:
    # Regional Data Loads (Parallel)
    1. DT_LOAD_AMERICAS
       Type: Data Transfer
       Runtime: ~30 min
       NextTasks: [4] (Sync point)

    2. DT_LOAD_EMEA
       Type: Data Transfer
       Runtime: ~25 min
       NextTasks: [4] (Sync point)

    3. DT_LOAD_APAC
       Type: Data Transfer
       Runtime: ~20 min
       NextTasks: [4] (Sync point)

    # Reference Data Loads (Parallel)
    4. DT_LOAD_EXCHANGE_RATES
       Type: Data Transfer
       Runtime: ~5 min
       NextTasks: [7] (Sync point)

    5. DT_LOAD_GL_ACCOUNTS
       Type: Data Transfer
       Runtime: ~10 min
       NextTasks: [7] (Sync point)

    # Synchronization Point
    6. SYNC_POINT
       Type: Control (wait for tasks 1,2,3,4,5)
       WaitForTasks: [1, 2, 3, 4, 5]
       Timeout: 120 minutes
       NextTasks: [7]

    # Final Aggregation (after sync point)
    7. TR_FINAL_RECONCILE
       Type: Transformation
       Dependencies: Task 6 (SYNC_POINT)
       NextTasks: [END]

  Execution Order:
    - Tasks 1, 2, 3, 4, 5 start immediately (parallel)
    - Task 6 waits for ALL to complete
    - Task 7 starts after Task 6
```

### Pattern 3: Conditional Branching

**BW Process Chain:**
```
Start
  ├─ Step 1: Load Data
  ├─ Step 2: Check (IF record count > 0)
  │  ├─ Then → Step 3: Process Normal Path
  │  └─ Else → Step 4: Process Empty Load
  └─ Step 5: Send Notification
```

**Datasphere Task Chain:**
```yaml
Task Chain: TC_CONDITIONAL_BRANCHING
  Tasks:
    1. DT_LOAD_DATA
       Type: Data Transfer
       OutputVariables:
         - record_count (query result)
       NextTasks: [2]

    2. TR_CHECK_CONDITION
       Type: Transformation
       SQL: |
         SELECT COUNT(*) as record_count
         FROM T_LOADED_DATA
         WHERE _LOAD_DATE = CURRENT_DATE

       ConditionCheck: record_count > 0
       NextTaskIfTrue: Task 3
       NextTaskIfFalse: Task 4

    3. TR_PROCESS_NORMAL
       Type: Transformation (Normal processing logic)
       NextTasks: [5]

    4. TR_PROCESS_EMPTY
       Type: Transformation (Handle empty load)
       SQL: INSERT INTO T_AUDIT_LOG VALUES ('NO_DATA_LOADED', CURRENT_TIMESTAMP)
       NextTasks: [5]

    5. TR_SEND_NOTIFICATION
       Type: Script
       Action: Send email (content depends on path taken)
       FinalTask: Yes
```

### Pattern 4: Error Handling and Retry

**BW Process Chain:**
```
Start
  └─ Step 1: Load Data
     └─ Step 2: Check (If error, retry)
     │  └─ Retry up to 3 times
     │     └─ If success → Continue
     │     └─ If all retries fail → Error Handler
```

**Datasphere Task Chain:**
```yaml
Task Chain: TC_ERROR_HANDLING_RETRY
  Tasks:
    1. DT_LOAD_DATA_WITH_RETRY
       Type: Data Transfer
       ErrorHandling:
         RetryPolicy: EXPONENTIAL_BACKOFF
         MaxRetries: 3
         InitialRetryDelay: 5 minutes
         BackoffMultiplier: 2.0

       RetrierSchedule:
         Attempt 1: Immediate retry
         Attempt 2: Retry after 5 min
         Attempt 3: Retry after 10 min
         Attempt 4: Retry after 20 min

       OnAllRetriesFailed: GOTO Task 2

    2. TR_ERROR_HANDLER
       Type: Transformation
       SQL: |
         INSERT INTO T_ERROR_LOG
         VALUES ('LOAD_FAILED', 'Max retries exceeded', CURRENT_TIMESTAMP)

       NextTasks: [3]

    3. SEND_ESCALATION_ALERT
       Type: Script
       Action: Send alert to ops team
       FinalTask: Yes
```

---

## 6. STC01 Task List Error Codes and Resolutions

### Conversion Phase Errors

| Error Code | Message | Root Cause | Resolution |
|---|---|---|---|
| **TL1-001** | Object not found in BW Bridge | Object doesn't exist or wrong system | Verify object exists; check system connection |
| **TL1-002** | Insufficient authorization | User lacks conversion rights | Grant STC01_ADMIN role to user |
| **TL1-003** | Object already converted | Duplicate conversion attempt | Verify conversion completed; skip if already done |
| **TL1-004** | Unsupported object type | Object type not convertible (e.g., custom query) | Use Remote Conversion or manual rebuild |
| **TL1-005** | Metadata inconsistency detected | Orphaned fields or corrupt definition | Run BW consistency check (RSRV); fix and retry |
| **TL1-006** | Datasphere connection failed | Network issue or auth failure | Test connection; verify credentials; check firewall |
| **TL1-007** | Insufficient Datasphere space | No free storage | Clean up; compress old data; contact DBAs |
| **TL1-008** | Characteristic not recognized | Custom attribute not supported | Document attribute; plan manual handling |
| **TL1-009** | Key figure aggregation unsupported | Formula-based KFG not convertible | Implement as calculated measure in Analytical Model |
| **TL1-010** | Timeout during conversion | Process taking too long | Increase timeout setting; split large objects |

### Data Transfer Errors

| Error Code | Message | Root Cause | Resolution |
|---|---|---|---|
| **TL2-001** | Source table not accessible | Table doesn't exist or access denied | Verify source object; check user permissions |
| **TL2-002** | Target table locked | Another load in progress | Wait for completion; check Task Chain status |
| **TL2-003** | Data type mismatch | Field cannot be cast to target type | Adjust transformation; use CAST function |
| **TL2-004** | Primary key violation | Duplicate keys in source | Remove duplicates from source; use MERGE instead of INSERT |
| **TL2-005** | Foreign key violation | Referenced record not found | Load parent tables first; check referential integrity |
| **TL2-006** | NULL constraint violation | Required field is NULL | Apply transformation to populate; filter out nulls |
| **TL2-007** | Decimal precision loss | Number has more digits than target | Increase column precision; adjust data |
| **TL2-008** | String too long | VARCHAR exceeds max length | Increase column size; truncate/split data |
| **TL2-009** | Network timeout | Connection lost during transfer | Increase timeout; check bandwidth; retry |
| **TL2-010** | Disk space full | Target system out of space | Purge old data; add storage; reduce batch size |

### Post-Load Validation Errors

| Error Code | Message | Root Cause | Resolution |
|---|---|---|---|
| **TL3-001** | Row count mismatch | Source and target differ | Run data reconciliation; identify missing records |
| **TL3-002** | Aggregation mismatch | Sum of measures differs | Check for data type conversions; verify formulas |
| **TL3-003** | Key uniqueness violation | Duplicate keys found | Remove duplicates from source; investigate cause |
| **TL3-004** | Date range gap | Missing time periods | Re-run full load; check filtering logic |
| **TL3-005** | NULL values unexpected | More NULLs than source | Investigate transformation; check data quality |
| **TL3-006** | Data distribution skewed | Unusual grouping by dimension | Investigate source data; may be correct if expected |
| **TL3-007** | Hierarchy validation failed | Circular or orphaned nodes | Fix hierarchy in source; rebuild manually |
| **TL3-008** | Lookup failure | Referenced dimension record not found | Ensure dimension loaded first; add missing records |

---

## 7. Migration Timeline Template

### 4-Week Migration Timeline

```
WEEK 1: Planning & Assessment
┌─────────────────────────────────────────┐
│ Monday: Kick-off Meeting                │
│ ☐ Define scope & objectives             │
│ ☐ Review timeline                       │
│ ☐ Assign team roles                     │
│                                         │
│ Tuesday-Wednesday: Object Inventory     │
│ ☐ Export STC01 task list               │
│ ☐ Document BW object metadata           │
│ ☐ Assess complexity for each object    │
│                                         │
│ Thursday: Compatibility Assessment      │
│ ☐ Classify objects: High/Med/Low risk  │
│ ☐ Identify unsupported features        │
│ ☐ Create conversion roadmap            │
│                                         │
│ Friday: Infrastructure Setup            │
│ ☐ Provision Datasphere space           │
│ ☐ Configure BW Bridge access           │
│ ☐ Create user accounts & roles         │
│                                         │
│ Deliverable: Migration Plan Document   │
└─────────────────────────────────────────┘

WEEK 2: Pilot Conversion (1 object)
┌─────────────────────────────────────────┐
│ Monday: Pilot Object Selection          │
│ ☐ Choose low-risk test object          │
│ ☐ Size ~1-5 GB (manageable)           │
│ ☐ Some business value (validate value) │
│                                         │
│ Tuesday-Wednesday: Shell Conversion     │
│ ☐ Extract metadata                      │
│ ☐ Run compatibility check               │
│ ☐ Execute shell conversion              │
│ ☐ Validate object creation              │
│                                         │
│ Thursday: Data Transfer                 │
│ ☐ Execute full load                     │
│ ☐ Monitor progress                      │
│ ☐ Validate row counts                   │
│ ☐ Run reconciliation queries            │
│                                         │
│ Friday: Testing & Sign-Off              │
│ ☐ Basic UAT testing                     │
│ ☐ Performance validation                │
│ ☐ Business owner sign-off               │
│                                         │
│ Deliverable: Pilot Conversion Report   │
└─────────────────────────────────────────┘

WEEK 3: Wave 1 Conversion (5-10 objects)
┌─────────────────────────────────────────┐
│ Monday: Wave Planning                   │
│ ☐ Prioritize remaining objects         │
│ ☐ Define conversion sequence           │
│ ☐ Create conversion schedule           │
│                                         │
│ Tue-Thu: Parallel Conversions           │
│ ☐ Shell convert 5-10 objects (parallel)│
│ ☐ Load data for each                    │
│ ☐ Validate data quality                 │
│ ☐ Create analytics models/views        │
│                                         │
│ Friday: Consolidation                   │
│ ☐ Complete UAT for all objects         │
│ ☐ Address issues found                  │
│ ☐ Prepare for Wave 2                    │
│                                         │
│ Deliverable: Wave 1 Completion Report   │
└─────────────────────────────────────────┘

WEEK 4: Wave 2 + Go-Live Prep
┌─────────────────────────────────────────┐
│ Monday: Wave 2 Start                    │
│ ☐ Convert remaining objects             │
│ ☐ Complete data transfers               │
│                                         │
│ Tue-Wed: Go-Live Preparation            │
│ ☐ Final data reconciliation            │
│ ☐ Update BI tool connections            │
│ ☐ Create runbooks & documentation      │
│ ☐ Train support team                    │
│                                         │
│ Thursday: Readiness Check                │
│ ☐ All objects converted ✓               │
│ ☐ Data validated ✓                     │
│ ☐ Users trained ✓                      │
│ ☐ Runbooks ready ✓                     │
│ ☐ Support prepared ✓                   │
│                                         │
│ Friday: Go-Live Day                     │
│ ☐ Switch BI tool connections (03:00)  │
│ ☐ Monitor first 2 hours                │
│ ☐ Respond to issues                     │
│ ☐ Confirm success                       │
│                                         │
│ Deliverable: Go-Live Report             │
└─────────────────────────────────────────┘
```

### 8-Week Migration Timeline (Large-Scale)

```
WEEK 1-2: Planning & Assessment
  ☐ Form steering committee
  ☐ Conduct full system inventory
  ☐ Risk assessment & complexity scoring
  ☐ Resource planning

WEEK 3: Infrastructure & Pilot
  ☐ Provision Datasphere environment
  ☐ Configure connections
  ☐ Execute pilot conversion
  ☐ Validate pilot results

WEEK 4-5: Wave 1 (High Priority Objects)
  ☐ Convert top 20-30% of objects
  ☐ Data transfer & validation
  ☐ UAT phase 1

WEEK 6: Wave 2 (Medium Priority Objects)
  ☐ Convert 40-60% of objects
  ☐ Parallel testing continues
  ☐ Identify optimization opportunities

WEEK 7: Wave 3 (Remaining Objects)
  ☐ Convert final 10-20% of objects
  ☐ Complete UAT
  ☐ Go-live readiness assessment

WEEK 8: Go-Live & Stabilization
  ☐ Final cutover
  ☐ Production monitoring
  ☐ Issue resolution
  ☐ Decommission BW Bridge
```

---

## 8. Rollback and Fallback Procedures

### Scenario 1: Shell Conversion Fails (Before Data Transfer)

**Problem:** Conversion step fails; object not created in Datasphere

**Rollback Steps:**
1. [ ] Note conversion failure in log
2. [ ] Investigate error code (see Section 6)
3. [ ] Correct root cause in source system
4. [ ] Delete failed object from Datasphere
5. [ ] Retry shell conversion
6. [ ] Document lessons learned

**Fallback:** Defer object to Wave 2; use Remote Conversion instead

---

### Scenario 2: Data Transfer Fails (Partial Load)

**Problem:** Data load stops midway; target table has incomplete data

**Rollback Steps:**
1. [ ] Stop data transfer task immediately
2. [ ] Truncate target table (remove partial data)
3. [ ] Investigate error code (see Section 6)
4. [ ] Fix root cause (network, data quality, etc.)
5. [ ] Retry full data load
6. [ ] Run reconciliation to confirm completeness

**Prevention:**
- Set batch size to recoverable chunks (100K records)
- Log every 10K records processed
- Use restart checkpoints for large loads

---

### Scenario 3: Data Reconciliation Fails (Row Count Mismatch)

**Problem:** Source and target row counts don't match; data lost during transfer

**Investigation:**
1. [ ] Get exact row counts from both systems
2. [ ] Calculate variance: `(Target - Source) / Source * 100`
3. [ ] If variance < 0.1%: Acceptable; document variance
4. [ ] If variance >= 0.1%: Investigate
   - Check if source was modified during load
   - Verify load is complete (check timestamps)
   - Look for NULL value filtering
   - Check for duplicate key rejections

**Remediation:**
```sql
-- Find records in source not in target
SELECT * FROM T_BW_SOURCE s
WHERE NOT EXISTS (
  SELECT 1 FROM T_DATASPHERE_TARGET t
  WHERE t.KEY_FIELD_1 = s.KEY_FIELD_1
    AND t.KEY_FIELD_2 = s.KEY_FIELD_2
)
LIMIT 100;  -- Review first 100

-- If records found: Re-insert missing records
INSERT INTO T_DATASPHERE_TARGET
SELECT * FROM T_BW_SOURCE
WHERE KEY_FIELD_1 IN (
  -- List of missing keys from investigation above
);
```

**Fallback:** If unable to reconcile:
- Truncate target; re-run full load
- Extend reconciliation tolerance if variance < 0.5%
- Escalate to data quality team if > 0.5%

---

### Scenario 4: Production Cutover Issues (Post-Go-Live)

**Problem:** Datasphere queries failing; users cannot access reports

**Immediate Actions (First 30 minutes):**
1. [ ] Disable Datasphere connections in BI tools
2. [ ] Re-enable BW Bridge as fallback source
3. [ ] Notify users of temporary service degradation
4. [ ] Assemble troubleshooting team
5. [ ] Initiate incident call

**Investigation (30 minutes - 2 hours):**
- Check Datasphere system status
- Review query logs for errors
- Validate data transfer completion
- Check network connectivity

**Resolution Examples:**
- **Missing data**: Re-run data transfer, validate upload
- **Slow queries**: Missing indexes; optimize with EXPLAIN PLAN
- **Authorization denied**: User permissions; review DACs
- **Data quality issue**: Investigate source; re-convert object

**Escalation Criteria:**
- If issue unresolved within 2 hours: Escalate to Datasphere vendor
- If no resolution path identified: Proceed with permanent fallback

**Permanent Fallback (if unresolved):**
1. [ ] Keep BW Bridge in production (read-only mode)
2. [ ] Postpone Datasphere cutover by 1 week
3. [ ] Root cause analysis & fix
4. [ ] Schedule retry

---

### Scenario 5: BW Bridge Decommissioning Blocked

**Problem:** Cannot shutdown BW Bridge; still has active dependencies

**Investigation:**
```sql
-- Find active Task Chains using Bridge objects
SELECT TASK_CHAIN_ID, LAST_EXECUTION_DATE
FROM DATASPHERE.TASK_CHAINS
WHERE SOURCE_SYSTEM = 'BW_BRIDGE'
ORDER BY LAST_EXECUTION_DATE DESC;

-- Find BI tool connections to Bridge
SELECT TOOL_NAME, CONNECTION_STRING, LAST_USED
FROM BI_TOOL_CONNECTIONS
WHERE SYSTEM = 'BW_BRIDGE'
ORDER BY LAST_USED DESC;
```

**Remediation:**
1. [ ] Identify all Bridge dependencies
2. [ ] Migrate each to Datasphere equivalent
3. [ ] Update BI tool connections
4. [ ] Disable Bridge access for 30 days (read-only)
5. [ ] Monitor for orphaned connections
6. [ ] Retry decommissioning

---

### Emergency Rollback Procedure (Nuclear Option)

**Use ONLY if critical data corruption or security breach:**

```
Trigger Conditions:
  ☐ Multiple data integrity issues affecting > 10% of records
  ☐ Security breach with customer PII exposure
  ☐ Complete system failure without recovery option
  ☐ Executive decision to halt migration

Execution:
  1. [T+0] Activate incident response team
  2. [T+15] Notify all executives & legal
  3. [T+30] Take Datasphere objects offline
  4. [T+45] Full restoration from BW Bridge backups
  5. [T+60] Validate data integrity
  6. [T+90] Restore user access to BW Bridge
  7. [T+2h] Root cause analysis begins
  8. [T+24h] Communication to users

Communication:
  - "Migration paused due to [REASON]"
  - "BW reports temporarily restored"
  - "Datasphere access temporarily unavailable"
  - "Full investigation underway"

Recovery Timeline:
  - Week 1: Root cause analysis
  - Week 2: Fix root cause
  - Week 3-4: Retry migration with corrections
```

---

### Fallback Maintenance (Post-Fallback)

If you execute a fallback:

**Weekly Monitoring:**
- [ ] Monitor BW Bridge CPU/memory usage
- [ ] Check for any Bridge connection errors
- [ ] Validate data freshness

**Monthly Reviews:**
- [ ] Analyze root cause in detail
- [ ] Identify prevention measures
- [ ] Update runbooks

**Retry Planning:**
- Schedule retry within 2-4 weeks
- Communicate new target date to users
- Apply lessons learned from fallback
- Execute comprehensive retesting before go-live

---

End of Reference Guide

