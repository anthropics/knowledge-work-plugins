---
name: Flow Doctor
description: "Diagnose and resolve errors in Data Flows, Replication Flows, Transformation Flows, and Task Chains. Use this when flows fail, to read error logs, identify root causes, and implement fixes. Critical for debugging data pipeline issues."
---

# Flow Doctor

## Overview

The Flow Doctor skill guides you through systematic troubleshooting of SAP Datasphere flows. When a flow fails, this skill helps you read error messages, understand root causes, and implement targeted solutions.

## When to Use This Skill

- **Flow execution failed**: Red status in monitor, need to identify why
- **Partial data loading**: Only some records loaded, others rejected
- **Performance degradation**: Flow taking longer than expected
- **Connectivity issues**: Cannot reach source or target system
- **Memory errors**: Out-of-memory or resource constraints
- **Data mismatches**: Unexpected differences between source and target
- **Schema changes**: Source structure changed, flow now incompatible
- **Task chain failures**: Dependent tasks failing or not executing

## Systematic Troubleshooting Workflow

### Step 1: Check Overall Flow Status

```
Datasphere → Data Integrations → Monitor
└─ Find failing flow
├─ Note last run time and status
├─ Check error indicator (red icon)
└─ Count failed runs vs total runs
```

**Status Indicators:**

| Status | Meaning | Action |
|--------|---------|--------|
| GREEN | Running successfully | Check logs for warnings |
| YELLOW | Running but with warnings | Review warning messages |
| RED | Failed | Read error log immediately |
| GRAY | Not running | Check scheduling or manual trigger |
| BLUE | Running (in progress) | Wait for completion |

**Example Status Review:**
```
Flow: REP_CUSTOMER_DAILY
Status: RED (Failed)
Last Run: 2024-01-16 23:45:00
Duration: 12 minutes (usually 5 minutes - 2.4x longer!)
Records: 45,000 / 1,000,000 loaded
Error Count: 1
```

### Step 2: Access and Read Error Logs

**Location:** Data Integrations → Monitor → [Flow Name]
```
Error Log Details:
├─ Timestamp: 2024-01-16 23:45:45
├─ Severity: ERROR
├─ Message: "Memory limit exceeded"
├─ Step: "LOAD_DATA_TRANSFORM"
└─ Context: "Processing batch 3 of 10"
```

**Log Types by Flow Type:**

**Replication Flow Logs:**
```
[2024-01-16 23:45:12] INFO  | Initializing replication from S/4HANA
[2024-01-16 23:45:30] INFO  | Connected to source system
[2024-01-16 23:45:31] INFO  | Extracting C_CUSTOMER (1M rows)
[2024-01-16 23:46:00] WARN  | Extraction slow: 20K rows/min (target: 50K rows/min)
[2024-01-16 23:46:45] ERROR | Authorization error: User missing RFC_READ_TABLE
[2024-01-16 23:46:45] INFO  | Replication failed - 0 rows loaded
```

**Data Flow Logs:**
```
[2024-01-16 23:45:00] INFO  | Starting data flow
[2024-01-16 23:45:05] INFO  | Reading source: 100,000 rows
[2024-01-16 23:45:10] INFO  | Python operator: Transform started
[2024-01-16 23:45:25] ERROR | Python operator: TypeError in line 42
[2024-01-16 23:45:25] ERROR | Stack trace: ...
[2024-01-16 23:45:25] INFO  | Data flow failed
```

**Transformation Flow Logs:**
```
[2024-01-16 23:45:00] INFO  | Executing transformation procedure
[2024-01-16 23:45:10] INFO  | Creating temporary tables
[2024-01-16 23:45:12] ERROR | SQL Error [327]: Column "AMOUNT" not found
[2024-01-16 23:45:12] INFO  | Rollback executed
[2024-01-16 23:45:12] INFO  | Transformation failed
```

### Step 3: Identify Root Cause Category

Use the decision tree to narrow down the issue:

```
Flow Failed
│
├─ Connection Error?
│  ├─ Cannot reach source system
│  ├─ Cloud Connector offline
│  └─ Network timeout
│
├─ Authorization Error?
│  ├─ User lacks role
│  ├─ RFC function not authorized
│  └─ Table access denied
│
├─ Schema Error?
│  ├─ Column not found
│  ├─ Data type mismatch
│  └─ Table structure changed
│
├─ Data Quality Error?
│  ├─ Invalid data values
│  ├─ NULL where NOT NULL
│  └─ Type conversion failed
│
├─ Resource Error?
│  ├─ Memory exhausted
│  ├─ CPU limit exceeded
│  └─ Disk full
│
├─ Logic Error?
│  ├─ SQL syntax error
│  ├─ Python operator crash
│  └─ Transformation logic bug
│
└─ Configuration Error?
   ├─ Wrong mapping
   ├─ Invalid parameters
   └─ Missing prerequisites
```

### Step 4: Extract Key Error Information

From the error log, extract:

1. **Exact Error Message**
   ```
   Raw: "ERROR [327]: Column 'REVENUE_AMOUNT' not found in table 'C_INVOICE'"
   Key: Column REVENUE_AMOUNT is missing
   ```

2. **Component Where It Failed**
   ```
   Step: "MERGE_DATA" (not in initial load, in merge phase)
   Line/Position: 23 in transformation procedure
   ```

3. **Severity Level**
   ```
   FATAL - Flow stops immediately
   ERROR - Flow stops after current step
   WARN - Flow continues but with issues
   INFO - Informational only
   ```

4. **Affected Data**
   ```
   Records processed: 45,000
   Records failed: 1,000
   Failed %: 2.2%
   ```

### Step 5: Implement Targeted Fix

Based on root cause category, apply the appropriate solution (see sections below).

### Step 6: Test and Validate

Before restarting in production:

```
Test Strategy:
1. Run on sample data (LIMIT 1000)
2. Verify output matches expected schema
3. Check row counts and data quality
4. Execute once before scheduling
```

**Validation Query:**
```sql
SELECT
    COUNT(*) AS TOTAL_ROWS,
    COUNT(DISTINCT KEY_COLUMN) AS UNIQUE_KEYS,
    COUNT(CASE WHEN AMOUNT IS NULL THEN 1 END) AS NULL_AMOUNTS,
    MIN(AMOUNT) AS MIN_AMOUNT,
    MAX(AMOUNT) AS MAX_AMOUNT
FROM TARGET_TABLE
WHERE LOAD_DATE = CURRENT_DATE;
```

## Common Replication Flow Failures

### Error Type 1: Authorization Errors

**Symptoms:**
```
ERROR: User [DATASPH_USER] does not have authorization for RFC_READ_TABLE
ERROR: Access denied to table [C_CUSTOMER]
ERROR: Missing role SAP_BC_ANALYTICS_EXTRACTOR
```

**Root Causes:**
- User missing required role in S/4HANA
- RFC function not authorized for user
- CDS view not marked as extraction-enabled
- Security policy restricts table access

**Diagnosis:**
```
1. Check user roles in S/4HANA (PFCG transaction)
2. Verify RFC authorizations (SM59 → ODP settings)
3. Confirm CDS view has @Analytics.dataExtraction.enabled = true
4. Review data security policies (RSECADMIN)
```

**Solution Steps:**

```
S/4HANA System Administration:
1. Go to PFCG transaction
2. Search for user: DATASPH_USER
3. Assign role: SAP_BC_ANALYTICS_EXTRACTOR
4. Add to role: S_ODP_* objects
5. Save and activate

Verify:
SM59 → ODP_BACKEND
Test Connection → Should succeed
```

**Prevention:**
```
Create dedicated technical user for extraction:
- User: DATASPH_EXTRACT
- Role: Custom role with minimum permissions
  ├─ RFC: RFC_READ_TABLE (for fallback)
  ├─ RFC: /ODSO/* (for ODP)
  ├─ Table: C_* (CDS views only)
  └─ Authorization level: VIEW only

Apply principle of least privilege.
```

### Error Type 2: Connection Timeouts

**Symptoms:**
```
ERROR: Connection timeout after 300 seconds
ERROR: Read timed out: no further information
ERROR: Unable to connect to host [s4h-prod.example.com:443]
WARN: Slow network response (5 min for 100K rows)
```

**Root Causes:**
- Network latency or packet loss
- Cloud Connector offline or overloaded
- Source system busy/unresponsive
- Large data volume causing slow extraction
- Firewall blocking connection

**Diagnosis Steps:**

```
1. Check Cloud Connector Status:
   Datasphere → Administration → Connections
   → S/4HANA_PROD → Status
   Expected: GREEN - Connected

2. Verify Network Connectivity:
   From DP Agent or Cloud Connector:
   ping s4h-prod.example.com
   telnet s4h-prod.example.com 443

3. Check Source System Load:
   S/4HANA → SM50 (Work Process Overview)
   Look for: CPU > 80%, Memory > 90%, Queued requests
```

**Solution:**

**Increase Timeout:**
```
Data Integrations → Connection Settings
→ S/4HANA_PROD
→ Advanced → Connection Timeout
   Current: 300 seconds
   Change to: 600 seconds

Save and retest
```

**Optimize Extraction:**
```
Replication Flow Settings:
├─ Reduce batch size: 100,000 → 50,000 rows/batch
├─ Increase parallel threads: 1 → 4
├─ Add filter to source: WHERE load_date >= CURRENT_DATE - 7
└─ Schedule off-peak: 23:00 instead of 09:00
```

**Check Cloud Connector Performance:**
```
Admin Console → https://cc-prod.example.com:8443
→ Monitoring
├─ Check CPU usage (should be < 70%)
├─ Check throughput (should be > 50 MB/s)
├─ Check request queue (should be < 100)
└─ If overloaded: scale Cloud Connector or add standby
```

### Error Type 3: Schema Mismatches

**Symptoms:**
```
ERROR: Column 'REVENUE' not found in source table C_CUSTOMER
ERROR: Data type mismatch - Expected STRING, got DECIMAL
ERROR: Source table structure changed - table refresh required
```

**Root Causes:**
- Source CDS view fields changed in new S/4HANA patch
- Target table schema doesn't match source
- Column was deleted from source
- Data type definitions are incompatible

**Diagnosis:**

```
1. Get source schema:
   use MCP: get_table_schema(table_name="C_CUSTOMER", source="S/4HANA")

2. Get target schema:
   use MCP: get_table_schema(table_name="CUSTOMER_MASTER", source="DATASPHERE")

3. Compare field-by-field:
   Source: AMOUNT (DECIMAL 15,2), String length: 17
   Target: AMOUNT (DECIMAL 10,2), String length: 12
   Issue: Target too small for source values!
```

**Solution:**

**Refresh Source Schema:**
```
Data Integrations → Replication Flow → [Flow Name]
→ Source Definition
→ Refresh Schema
→ Review changes
→ Accept and Save
```

**Resize Target Columns:**
```sql
-- Identify columns needing expansion
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    NUMERIC_PRECISION,
    NUMERIC_SCALE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'CUSTOMER_MASTER'
    AND (
        CHARACTER_MAXIMUM_LENGTH < 255
        OR NUMERIC_PRECISION < 15
    );

-- Expand problem columns
ALTER TABLE CUSTOMER_MASTER
    MODIFY COLUMN REVENUE DECIMAL(19,4),
    MODIFY COLUMN CUSTOMER_NAME VARCHAR(500);
```

**Recreate Flow with Updated Schema:**
```
If structural changes are significant:
1. Backup existing data
2. Rename old table: CUSTOMER_MASTER → CUSTOMER_MASTER_OLD
3. Delete old flow
4. Create new flow (will auto-create table with current schema)
5. Perform full reload
6. Validate row counts match
7. Drop _OLD table
```

### Error Type 4: Delta Queue Issues

**Symptoms:**
```
ERROR: Change record (CN: 1500000) not found in delta queue
ERROR: Queue overflow - exceeds 4GB limit
WARN: Only 2 days of changes retained (retention < extraction frequency)
```

**Root Causes:**
- Delta queue purged before extraction (retention expired)
- Queue size exceeded, oldest records deleted
- Too much time between delta extractions
- Source system change log not maintained

**Diagnosis:**

```
Check Delta Queue Status:
use MCP: test_connection(
    source="S/4HANA_PROD",
    check_delta_queue=True
)

Expected output:
{
    "queue_size_gb": 1.2,
    "max_size_gb": 4.0,
    "oldest_record_days": 5,
    "retention_policy_days": 8,
    "health": "HEALTHY"
}
```

**Solution:**

**For Expired Queue (Records Deleted):**
```
1. The delta is lost, must do full reload
2. Stop the delta replication flow
3. Create new replication flow with full load
4. Set new watermark to current value
5. Resume delta from new watermark

SQL verification:
SELECT MAX(CHANGENUMBER) FROM C_CUSTOMER;
Store this value as new watermark.
```

**For Queue Overflow:**
```
Immediate: Perform full reload to reset

Preventive:
  a) Increase delta frequency:
     From: Every 30 minutes
     To: Every 5-10 minutes
     Rationale: Smaller batches prevent overflow

  b) Increase queue size in S/4HANA:
     SPRO → ODP Configuration
     Queue max size: 4GB → 8GB
     Retention: 8 days → 14 days

  c) Add source filter:
     Load only recent: WHERE changed_date >= CURRENT_DATE - 30
     Reduces volume extracted each run
```

## Common Data Flow Failures

### Error Type 1: Memory Limit Exceeded

**Symptoms:**
```
ERROR: Java heap space - Out of memory
ERROR: Insufficient memory for operator execution
WARN: Memory usage at 95% of limit
ERROR: Python operator crashed - memory allocation failed
```

**Root Causes:**
- Input dataset larger than available memory
- Python operator loading entire dataframe
- No pagination or chunking in code
- Memory-intensive aggregations

**Diagnosis:**

```
1. Check input row count:
   use MCP: execute_query("SELECT COUNT(*) FROM source_table")
   Example result: 50,000,000 rows (50M)

2. Estimate memory needed:
   50M rows × 1KB per row = 50GB (exceeds 32GB limit!)

3. Check operator code for memory issues:
   - Loading all data into memory at once
   - Creating large intermediate arrays
   - Not releasing memory between operations
```

**Solution:**

**Chunked Processing in Python:**
```python
def process_large_dataset_chunked(input_df, chunk_size=10000):
    """
    Process in chunks to avoid memory issues
    """
    result_chunks = []

    for i in range(0, len(input_df), chunk_size):
        chunk = input_df.iloc[i:i + chunk_size]

        # Process chunk
        processed_chunk = chunk.assign(
            revenue_category=chunk['revenue'].apply(categorize_revenue)
        )

        result_chunks.append(processed_chunk)

        # Explicitly free memory
        del chunk

    return pd.concat(result_chunks, ignore_index=True)

def process_via_partition(input_df, partition_column='YEAR_MONTH'):
    """
    Process by partitions instead of full load
    """
    result = []

    for partition_val in input_df[partition_column].unique():
        partition_data = input_df[input_df[partition_column] == partition_val]
        processed = partition_data.apply_transformations()
        result.append(processed)
        del partition_data

    return pd.concat(result, ignore_index=True)
```

**Add Source Filter:**
```
Data Flow Settings:
├─ Source: LARGE_TABLE (100M rows)
├─ Add WHERE clause:
│  WHERE TRANSACTION_DATE >= CURRENT_DATE - 90
│  (Reduces to 5M rows, fits in memory)
└─ Result: Incremental load instead of full
```

**Increase Memory Allocation:**
```
Data Flow → Advanced Settings
├─ Memory Limit: 16GB → 32GB
├─ Note: Requires larger execution environment
└─ Cost: Higher (check pricing)
```

### Error Type 2: Data Type Mismatch

**Symptoms:**
```
ERROR: TypeError: cannot convert from DECIMAL to STRING
ERROR: Cannot convert value "ABC123" to type INTEGER
ERROR: Date conversion error: invalid format "01/32/2024"
```

**Root Causes:**
- Source delivers unexpected data type
- Python operator assumes wrong type
- Implicit type conversion fails
- NULL values not handled

**Diagnosis:**

```python
# Check data types in Python operator
def diagnose_types(input_df):
    print(input_df.dtypes)
    print(input_df.head(10))
    print(input_df.describe())

    # Check for problematic values
    for col in input_df.columns:
        print(f"{col}: unique={input_df[col].nunique()}, nulls={input_df[col].isnull().sum()}")
```

**Solution:**

**Add Type Conversion:**
```python
def safe_transform(input_df):
    """
    Explicit type conversion with error handling
    """
    # String to number
    input_df['amount'] = pd.to_numeric(
        input_df['amount'],
        errors='coerce'  # Invalid values become NULL
    )

    # String to date
    input_df['transaction_date'] = pd.to_datetime(
        input_df['transaction_date'],
        format='%Y-%m-%d',
        errors='coerce'
    )

    # Handle NULLs from failed conversions
    input_df['amount'] = input_df['amount'].fillna(0)
    input_df['transaction_date'] = input_df['transaction_date'].fillna(
        pd.Timestamp('1900-01-01')
    )

    return input_df
```

**Add Validation Step:**
```python
def validate_before_transform(input_df):
    """
    Validate data quality before transformation
    """
    errors = []

    # Check nulls
    if input_df['amount'].isnull().any():
        errors.append(f"NULL amounts found: {input_df['amount'].isnull().sum()}")

    # Check type
    try:
        pd.to_numeric(input_df['amount'])
    except:
        errors.append("Amount contains non-numeric values")

    # Check value ranges
    if (input_df['amount'] < 0).any():
        errors.append(f"Negative amounts found: {(input_df['amount'] < 0).sum()}")

    if errors:
        raise ValueError("Data quality issues: " + "; ".join(errors))

    return input_df
```

### Error Type 3: Python Operator Crash

**Symptoms:**
```
ERROR: Python operator failure - execution terminated
ERROR: ImportError: No module named 'sklearn'
ERROR: NameError: name 'df' is not defined
TRACEBACK: File "operator.py", line 42, in process_data
```

**Root Causes:**
- Python syntax error in operator code
- Missing library import
- Variable name typo
- Incompatible library version

**Diagnosis:**

```
1. Read full traceback from logs
2. Identify line number causing issue
3. Check if syntax is valid
4. Verify all imports available

Example traceback:
  File "transform.py", line 42, in process_data
    revenue_category = categorize(df['revenue'])
                                  ^^
  NameError: name 'df' is not defined

Issue: DataFrame not created - likely parameter name wrong
```

**Solution:**

**Fix Syntax Errors:**
```python
# WRONG
def transform(input_df)
    # Missing colon
    result = input_df + 1  # Wrong
    reutrn result  # Typo

# RIGHT
def transform(input_df):
    result = input_df.assign(value=input_df['amount'] + 1)
    return result
```

**Add Missing Imports:**
```python
# Check what libraries are available
import sys
print(sys.version)

# Required imports for data flows
import pandas as pd
import numpy as np

# Optional (may not be available)
try:
    from sklearn import preprocessing
except ImportError:
    print("sklearn not available - using alternative")
    # Implement without sklearn
```

**Debug Print Statements:**
```python
def transform(input_df):
    print(f"Input shape: {input_df.shape}")
    print(f"Columns: {input_df.columns.tolist()}")

    result = input_df.assign(
        value=input_df['amount'] * 1.1
    )

    print(f"Output shape: {result.shape}")
    return result
```

## Common Transformation Flow Failures

### Error Type 1: SQL Syntax Errors

**Symptoms:**
```
ERROR SQL0104: Statement was not prepared - "CREATE TABLE" not recognized
ERROR SQL0207: Column 'REVENUE_AMOUNT' not found
ERROR SQL0289: Trigger or constraint violation
```

**Root Causes:**
- SQLScript syntax not valid
- Column name misspelled
- Reserved keyword used as identifier
- SQL dialect mismatch

**Diagnosis:**

```
1. Read error line number
2. Check syntax at that line
3. Verify all table/column names exist

Example:
Line 42: CREATE LOCAL TEMP TABLE temp_customer (
Line 43:     customer id INT,  // WRONG - missing underscore in column name
```

**Solution:**

**Test SQL Incrementally:**
```sql
-- Test step-by-step, not entire procedure at once

-- Step 1: Test table exists
EXECUTE QUERY 'SELECT * FROM SOURCE_CUSTOMER LIMIT 10';

-- Step 2: Test transformation
EXECUTE QUERY '
    SELECT
        CUSTOMER_ID,
        UPPER(CUSTOMER_NAME) as name_upper,
        CURRENT_TIMESTAMP as load_ts
    FROM SOURCE_CUSTOMER
    LIMIT 10
';

-- Step 3: If that works, test full transformation logic
EXECUTE QUERY '
    MERGE INTO TARGET_CUSTOMER tc
    USING SOURCE_CUSTOMER sc
        ON tc.CUSTOMER_ID = sc.CUSTOMER_ID
    WHEN MATCHED THEN
        UPDATE SET tc.NAME = sc.NAME
    WHEN NOT MATCHED THEN
        INSERT (CUSTOMER_ID, NAME)
        VALUES (sc.CUSTOMER_ID, sc.NAME)
';
```

**Quote Identifiers:**
```sql
-- If using reserved words or special characters:
SELECT
    "user",           -- reserved word - quote it
    "account-number", -- contains hyphen - quote it
    normal_column     -- no quotes needed
FROM table_name;
```

### Error Type 2: Delta Watermark Issues

**Symptoms:**
```
ERROR: Watermark value invalid - not found in source data
ERROR: Cannot compare TIMESTAMP and STRING types
WARN: Watermark not advancing - same value as last run
ERROR: Overlapping deltas - duplicate records loaded
```

**Root Causes:**
- Watermark field doesn't exist or changed type
- Watermark value outside valid range
- Source data older than watermark
- Timezone issues with timestamps

**Diagnosis:**

```
1. Check watermark field exists:
   use MCP: get_table_schema(table="C_CUSTOMER")
   Verify: LAST_CHANGED_AT field exists and is TIMESTAMP

2. Check watermark value:
   use MCP: execute_query("
       SELECT MAX(LAST_CHANGED_AT) FROM C_CUSTOMER
   ")
   Result: 2024-01-15 23:59:59
   Current watermark stored: 2024-01-16 00:00:00
   Issue: Watermark > max value means no data to extract!

3. Check for duplicates:
   use MCP: execute_query("
       SELECT CHANGENUMBER, COUNT(*) as cnt
       FROM delta_load_batch
       GROUP BY CHANGENUMBER
       HAVING COUNT(*) > 1
   ")
```

**Solution:**

**Reset Watermark to Valid Value:**
```sql
-- Check current maximum
SELECT MAX(LAST_CHANGED_AT) as current_max FROM C_CUSTOMER;

-- Update stored watermark
UPDATE WATERMARK_CONTROL
SET LAST_WATERMARK = (
    SELECT MAX(LAST_CHANGED_AT) - INTERVAL '1' HOUR
    FROM C_CUSTOMER
)
WHERE TABLE_NAME = 'CUSTOMER';

-- Next delta run will get last 1 hour of changes
```

**Fix Timestamp Timezone Issues:**
```sql
-- Problem: Timestamps stored in UTC but watermark in local time
-- Solution: Normalize to UTC

PROCEDURE LOAD_DELTA_NORMALIZED (
    IN iv_last_watermark TIMESTAMP
)
LANGUAGE SQLSCRIPT
AS
BEGIN
    DECLARE v_watermark_utc TIMESTAMP;

    -- Convert input to UTC if needed
    SET v_watermark_utc = TO_UTCTIMESTAMP(
        iv_last_watermark,
        'America/New_York'  -- source timezone
    );

    -- Load with UTC comparison
    MERGE INTO TARGET_DATA
    USING (
        SELECT *
        FROM SOURCE_DATA
        WHERE TO_UTCTIMESTAMP(CREATED_AT, 'America/New_York') > :v_watermark_utc
    ) delta
    ON TARGET_DATA.ID = delta.ID
    WHEN MATCHED THEN
        UPDATE SET TARGET_DATA.VALUE = delta.VALUE
    WHEN NOT MATCHED THEN
        INSERT VALUES (delta.ID, delta.VALUE);
END;
```

**Deduplicate if Overlaps Exist:**
```sql
-- Merge with deduplication on key fields
MERGE INTO TARGET_CUSTOMER tc
USING (
    SELECT *
    FROM SOURCE_DELTA
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY CUSTOMER_ID
        ORDER BY CHANGENUMBER DESC
    ) = 1  -- Keep only latest version
) delta
ON tc.CUSTOMER_ID = delta.CUSTOMER_ID
WHEN MATCHED THEN
    UPDATE SET tc.NAME = delta.NAME
WHEN NOT MATCHED THEN
    INSERT VALUES (delta.CUSTOMER_ID, delta.NAME);
```

### Error Type 3: Merge Conflicts

**Symptoms:**
```
ERROR: Merge violation - target record locked
ERROR: Constraint violation - duplicate key
ERROR: Cannot delete row referenced by foreign key
WARN: 500 rows failed to merge due to conflicts
```

**Root Causes:**
- Concurrent modifications (other process updating target)
- Key field contains duplicate values
- Foreign key constraint violated
- NOT NULL column has NULL value

**Diagnosis:**

```
1. Check for locks:
   CALL DBMS_LOCKS.CHECK_LOCKS();

2. Check for duplicate keys:
   SELECT CUSTOMER_ID, COUNT(*) as cnt
   FROM TARGET_CUSTOMER
   GROUP BY CUSTOMER_ID
   HAVING COUNT(*) > 1;

3. Check for orphaned records:
   SELECT *
   FROM TARGET_CUSTOMER tc
   WHERE NOT EXISTS (
       SELECT 1 FROM CUSTOMER_MASTER cm
       WHERE cm.CUSTOMER_ID = tc.CUSTOMER_ID
   );

4. Check for NULLs in NOT NULL columns:
   SELECT *
   FROM TARGET_CUSTOMER
   WHERE CUSTOMER_ID IS NULL
       OR CUSTOMER_NAME IS NULL;
```

**Solution:**

**Handle Duplicate Keys:**
```sql
-- Before merge, deduplicate
MERGE INTO TARGET_CUSTOMER tc
USING (
    -- Get only latest version of each key
    SELECT *
    FROM SOURCE_DELTA
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY CUSTOMER_ID
        ORDER BY SEQUENCE_NUM DESC
    ) = 1
) delta
ON tc.CUSTOMER_ID = delta.CUSTOMER_ID
WHEN MATCHED THEN
    UPDATE SET tc.CUSTOMER_NAME = delta.CUSTOMER_NAME
WHEN NOT MATCHED THEN
    INSERT VALUES (delta.CUSTOMER_ID, delta.CUSTOMER_NAME);
```

**Handle Foreign Key Violations:**
```sql
-- Insert only valid references
MERGE INTO ORDERS o
USING (
    SELECT *
    FROM ORDERS_STAGING os
    WHERE EXISTS (
        SELECT 1 FROM CUSTOMER_MASTER cm
        WHERE cm.CUSTOMER_ID = os.CUSTOMER_ID
    )
) delta
ON o.ORDER_ID = delta.ORDER_ID
WHEN MATCHED THEN
    UPDATE SET o.CUSTOMER_ID = delta.CUSTOMER_ID
WHEN NOT MATCHED THEN
    INSERT VALUES (delta.ORDER_ID, delta.CUSTOMER_ID);
```

**Handle Concurrent Updates:**
```sql
-- Add retry logic
PROCEDURE MERGE_WITH_RETRY (
    IN iv_max_retries INT DEFAULT 3
)
LANGUAGE SQLSCRIPT
AS
BEGIN
    DECLARE v_retry_count INT := 0;
    DECLARE v_success CHAR(1) := 'N';

    WHILE :v_retry_count < :iv_max_retries AND :v_success = 'N' DO
        BEGIN
            -- Attempt merge
            MERGE INTO TARGET_DATA td
            USING SOURCE_DELTA sd
                ON td.KEY = sd.KEY
            WHEN MATCHED THEN
                UPDATE SET td.VALUE = sd.VALUE
            WHEN NOT MATCHED THEN
                INSERT VALUES (sd.KEY, sd.VALUE);

            SET v_success = 'Y';

        EXCEPTION WHEN SQL_ERROR_CODE THEN
            SET v_retry_count = :v_retry_count + 1;
            IF :v_retry_count >= :iv_max_retries THEN
                RESIGNAL;  -- Give up after max retries
            END IF;
            -- Wait before retrying
            CALL SYS.DBMS_LOCK.SLEEP(5);
        END;
    END WHILE;
END;
```

## Task Chain Failures

### Error Type 1: Dependency Errors

**Symptoms:**
```
ERROR: Task [STEP_B] failed - dependency on STEP_A not satisfied
ERROR: Task [STEP_C] not executed - parent task STEP_B failed
WARN: Task chain halted at step 2 of 5
```

**Root Causes:**
- Parent task failed before child task could run
- Dependency graph has circular reference
- Task configuration specifies wrong predecessor
- Timing issue - child starts before parent finishes

**Diagnosis:**

```
1. View task chain graph:
   Task Chain → [Chain Name] → Design View
   Look for: Red nodes (failed), Blue nodes (waiting)

2. Check dependency configuration:
   Task [STEP_B] Dependencies:
   ├─ Require STEP_A success
   ├─ Start after STEP_A completion
   └─ If STEP_A fails, STEP_B: SKIP | FAIL | RETRY

3. Check task execution order:
   Logs show: STEP_A failed at 10:15:00
   Logs show: STEP_B started at 10:15:05 (shouldn't have!)
```

**Solution:**

**Check Dependency Graph:**
```
Task Chain: CUSTOMER_LOAD_CHAIN
├─ STEP_A: REP_CUSTOMER (Replication)
│  └─ Status: FAILED
├─ STEP_B: TF_CUSTOMER_TRANSFORM (Transformation)
│  └─ Depends on: STEP_A SUCCESS (blocked)
├─ STEP_C: TF_CUSTOMER_AGGREGATE (Aggregation)
│  └─ Depends on: STEP_B SUCCESS (blocked)
└─ STEP_D: TF_CUSTOMER_PUBLISH (Export)
   └─ Depends on: STEP_C SUCCESS (blocked)

Fix:
1. Investigate STEP_A failure (see Replication Flow errors)
2. Restart STEP_A
3. Task chain automatically continues through B → C → D
```

**Configure Error Handling:**
```
Task Dependency Settings:
├─ If predecessor fails:
│  ├─ Option 1: STOP (whole chain halts)
│  ├─ Option 2: SKIP (run anyway, may fail)
│  ├─ Option 3: RETRY (attempt predecessor again)
│  └─ Option 4: CONDITIONAL (run only if success)
│
└─ Example configuration:
   STEP_B depends on STEP_A
   If STEP_A fails: RETRY (up to 3 times)
   If all retries fail: STOP (don't waste resources)
```

### Error Type 2: Scheduling Conflicts

**Symptoms:**
```
WARN: Task scheduled to run 10:00 but previous run still executing at 10:15
ERROR: Task skipped - overlap with concurrent execution detected
WARN: Daily run scheduled but weekly run already in progress
```

**Root Causes:**
- Previous run took longer than expected
- Frequency too high (overlapping executions)
- Manual trigger conflicts with scheduled run
- System resources exhausted

**Diagnosis:**

```
Check execution timeline:
Run 1: Starts 10:00, ends 10:45 (45 min)
Run 2: Scheduled 10:30 (overlap with Run 1!)
Run 3: Scheduled 11:00 (may overlap with Run 2!)

Issue: Task takes 45 min but scheduled every 30 min.
Duration: 45 min
Frequency: 30 min
Fix: Change frequency to 60 min minimum
```

**Solution:**

**Adjust Schedule Frequency:**
```
Current Schedule:
├─ Frequency: Every 30 minutes
├─ Avg Duration: 45 minutes
├─ Overlap Risk: HIGH

New Schedule:
├─ Frequency: Every 60 minutes (1 hour)
├─ Avg Duration: 45 minutes
├─ Buffer: 15 minutes
└─ Overlap Risk: LOW
```

**Prevent Overlapping Runs:**
```
Task Chain Settings:
├─ Allow Parallel Execution: NO
├─ Max Concurrent Runs: 1
├─ Queue Behavior: Skip if busy
└─ Description: Ensures one run at a time
```

### Error Type 3: Parallel Execution Issues

**Symptoms:**
```
ERROR: Race condition - two tasks writing same target table
WARN: Task 1 and Task 2 both running - resource contention
ERROR: Deadlock - Task A waiting for Task B, Task B waiting for Task A
```

**Root Causes:**
- Tasks configured to run in parallel but have shared resources
- No locking mechanism to prevent conflicts
- Circular dependencies in parallel tasks
- Memory/CPU constraints with parallel load

**Diagnosis:**

```
Check Parallel Configuration:
Task A: Loads TABLE_X
Task B: Loads TABLE_X (parallel)
Task C: Aggregates TABLE_X

Issue: Tasks A and B both write TABLE_X simultaneously!

Solution: Make A and B sequential OR
          Load to separate tables and union results
```

**Solution:**

**Sequential Instead of Parallel:**
```
Change from:
Task A → TABLE_X ┐
Task B → TABLE_X ├─ TABLE_RESULT
Task C ────────────→

To:
Task A → TABLE_X_A ┐
Task B → TABLE_X_B ├─ TABLE_RESULT
Task C ────────────→
(C does UNION of X_A and X_B)
```

**Add Locking:**
```sql
PROCEDURE LOAD_WITH_LOCK (
    IN iv_lock_name STRING DEFAULT 'CUSTOMER_LOAD'
)
LANGUAGE SQLSCRIPT
AS
BEGIN
    CALL DBMS_LOCK.REQUEST(iv_lock_name, 'X');  -- Exclusive lock

    BEGIN
        -- Load data (only one task executes at a time)
        MERGE INTO TARGET_CUSTOMER ...;

    EXCEPTION WHEN SQL_ERROR_CODE THEN
        CALL DBMS_LOCK.RELEASE(iv_lock_name);
        RESIGNAL;
    END;

    CALL DBMS_LOCK.RELEASE(iv_lock_name);
END;
```

## When to Restart vs Investigate Deeper

### Restart Only (Self-Resolving Issues)

```
Symptoms → Action:
├─ Temporary timeout → Restart flow
├─ One-time network hiccup → Restart flow
├─ Cloud Connector was briefly down → Restart flow
└─ Out of memory during spike → Restart flow (if single instance)

Expected Outcome: Successful on second attempt
No code/config changes needed
```

### Investigate Before Restarting (Persistent Issues)

```
Symptoms → Investigation Required:
├─ Authorization error → Fix user roles first
├─ Schema mismatch → Refresh schema and adjust mapping
├─ Duplicate rows → Add deduplication logic
├─ Memory consistently exceeded → Reduce batch size or add filter
├─ Dependency failure → Fix parent task first
└─ Data quality issues → Add validation/cleansing

Expected Outcome: Understand root cause, apply fix
Prevent same issue recurring
```

## MCP Tool References

### get_task_status
Check current and historical status of flows and tasks:

```
get_task_status(
    task_name="REP_CUSTOMER_DAILY",
    include_history=True,
    last_runs=10
)
```

### search_repository
Find flows and dependencies:

```
search_repository(
    object_type="REPLICATION_FLOW",
    name_contains="CUSTOMER",
    status="FAILED"
)
```

### get_object_definition
View complete flow configuration:

```
get_object_definition(object_id="REP_CUSTOMER_DAILY")
```

### execute_query
Run test queries to validate data and diagnose issues:

```
execute_query(
    query="SELECT COUNT(*) FROM TARGET_CUSTOMER WHERE LOAD_DATE = CURRENT_DATE"
)
```

## Reference Materials

See reference files for detailed procedures:
- `references/error-catalog.md` - Complete error code catalog with solutions
- `references/abap-side-monitoring.md` - ABAP-side monitoring tools (DHCDCMON, DHRDBMON, SLG1) for diagnosing Replication Flow issues on the source S/4HANA system
- `references/replication-flow-error-patterns.md` - 9 known Replication Flow error patterns with root causes, diagnostic steps, SAP Note references, and SAP support component assignments

