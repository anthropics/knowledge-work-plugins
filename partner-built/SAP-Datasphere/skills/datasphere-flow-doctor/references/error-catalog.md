# Error Catalog Reference

## Replication Flow Errors

### Connection and Authorization Errors

#### Error: Cannot reach SAP system
```
Code: CONN_001
Severity: CRITICAL
Message: Unable to establish connection to host [s4h-prod.example.com:443]

Causes:
1. Network unreachable
2. Cloud Connector offline
3. Firewall blocking connection
4. Wrong host/port configuration
5. Source system down

Diagnosis:
- Ping host: ping s4h-prod.example.com
- Check Cloud Connector: CC admin console → Status
- Check network: telnet s4h-prod.example.com 443
- Verify config: Data Integration → Connection → Check host/port

Solutions:
1. Verify network connectivity
2. Restart Cloud Connector if offline
3. Check firewall rules allow port 443
4. Verify connection credentials
5. Contact SAP system administrator
6. Increase timeout from 300s to 600s (if slow network)

Prevention:
- Redundant Cloud Connector instances (HA)
- Monitor Cloud Connector health continuously
- Document network/firewall requirements
- Test connection before scheduling
```

#### Error: Authorization failed - RFC_READ_TABLE denied
```
Code: AUTH_001
Severity: CRITICAL
Message: User [DATASPH_USER] not authorized for RFC_READ_TABLE

Causes:
1. User missing required role
2. RFC not enabled for user
3. Data security policy restricts access
4. Role missing specific authorization objects

Diagnosis:
- Check user roles: S/4HANA → PFCG → [USER] → Roles
- Check RFC auth: SM59 → ODP_BACKEND → Test
- Check security policy: RSECADMIN → Data access rules

Solutions:
1. Assign role SAP_BC_ANALYTICS_EXTRACTOR
2. Add RFC authorization: S_ODP_* objects
3. Grant table access via S_TABU_DIS
4. Review data security policies in RSECADMIN
5. Create custom role with minimum permissions

Prevention:
- Use dedicated technical user
- Apply principle of least privilege
- Regular access review
- Document required authorizations
```

#### Error: CDS view not marked for extraction
```
Code: EXTRACT_001
Severity: CRITICAL
Message: CDS view [I_CUSTOMER] not extraction-enabled

Causes:
1. Using internal view (I_*) instead of consumption (C_*)
2. Extraction not enabled in view annotations
3. View changed in new SAP patch
4. Custom view not properly configured

Diagnosis:
- Check view prefix: C_* (consumption) vs I_* (internal)
- Check annotations: SE11 → View → [Name]
  Look for: @Analytics.dataExtraction.enabled: true
- Search catalog: Datasphere → Search with extraction filter

Solutions:
1. Use SAP-provided consumption view (C_CUSTOMER not I_CUSTOMER)
2. Create custom view with extraction enabled:
   @Analytics.dataExtraction.enabled: true
   @Analytics.dataExtraction.deltaSupported: true
3. Request SAP to enable extraction if needed
4. Work with ABAP team to create extraction view

Prevention:
- Always use C_* views (consumption) when available
- Verify @Analytics annotation before using view
- Document which views are extraction-enabled
- Maintain list of approved CDS views for each module
```

### Data Extraction Errors

#### Error: Delta queue expired - must do full reload
```
Code: DELTA_001
Severity: CRITICAL
Message: Change number 1500000 not found in delta queue (queue retention < extraction frequency)

Causes:
1. Gap between delta extractions > queue retention (3-8 days)
2. Queue purged (automated cleanup older than retention)
3. Change records deleted by maintenance job
4. Extraction frequency too low (monthly vs daily requirements)

Diagnosis:
- Check delta queue: test_connection(check_delta_queue=True)
- Check queue retention: 3-8 days typical
- Check extraction frequency: Current vs required
- Calculate gap: Days since last successful delta

Solutions:
1. Accept delta loss, perform full reload:
   - Stop current delta flow
   - Create new replication with full load
   - Set new watermark to max(CHANGENUMBER)
   - Resume delta from new base

2. Increase extraction frequency:
   From: Weekly
   To: Daily
   Reduces gap, keeps within queue retention

3. Increase source system queue:
   SPRO → ODP → Increase max size (4GB → 8GB)
   Increase retention (8 days → 14 days)

Prevention:
- Schedule delta ≥2x per day if full reload possible
- Monitor queue health in advance
- Set alerts: Queue days retained < 5
- Document extraction frequency vs queue retention
```

#### Error: Source table structure changed
```
Code: SCHEMA_001
Severity: HIGH
Message: Column [REVENUE_AMOUNT] not found in source table [C_CUSTOMER]

Causes:
1. CDS view updated in new S/4HANA patch
2. View field removed or renamed
3. Flow mapped to wrong source
4. Column metadata out of sync

Diagnosis:
- Compare source schema: get_table_schema("C_CUSTOMER", "S4H_PROD")
- Check target schema: get_table_schema("CUSTOMER_MASTER", "DATASPHERE")
- Verify flow mappings: Data Integration → Flow → Mappings
- Check S/4HANA version: Recent patch introduced changes?

Solutions:
1. Refresh source schema in flow
   → Right-click source → Refresh Schema
   → Review changes and accept

2. Adjust field mappings
   → Map source fields to target
   → Fill in missing fields with defaults or NULL
   → Remove obsolete target fields

3. Recreate target table
   → If structural changes significant
   → Delete old target table
   → Flow will recreate with current schema
   → Perform full reload

Prevention:
- Test after S/4HANA patches
- Maintain schema documentation
- Set up alerts for CDS view changes
- Use snapshot tables for archival
```

#### Error: No data extracted - query returns empty
```
Code: EXTRACT_002
Severity: MEDIUM
Message: Replication completed but 0 rows extracted from source

Causes:
1. Source table is empty
2. Filter condition too restrictive
3. Source system down but reports success
4. Incorrect table mapping
5. Valid scenario - no new data since last run

Diagnosis:
- Verify data exists: SELECT COUNT(*) FROM C_CUSTOMER
- Check filter: Is WHERE clause in extraction correct?
- Verify mapping: Table name, schema, connection
- Test connection directly: test_connection(check_objects=True)

Solutions:
1. If valid (expected): Status = WARNING, continue monitoring

2. If invalid (unexpected):
   - Check source data: SELECT * FROM C_CUSTOMER LIMIT 100
   - Remove/relax filters if too restrictive
   - Verify table name and schema
   - Check source system for data issues

3. If first run:
   - Expected behavior
   - Full load will extract all data
   - Subsequent delta runs will be non-empty
```

### Performance Errors

#### Error: Extraction slow - timeout approaching
```
Code: PERF_001
Severity: MEDIUM
Message: Extraction rate 10K rows/min, expected >50K rows/min; timeout in 5 min

Causes:
1. Large dataset (millions of rows)
2. Network congestion
3. Source system busy/overloaded
4. Batch size too large
5. Parallel threads too few

Diagnosis:
- Check source load: SM50 in S/4HANA
- Check network: latency, packet loss
- Check Cloud Connector: CPU/Memory usage
- Check Datasphere: Network throttling?
- Calculate expected time: rows / extraction_rate

Solutions:
1. Reduce batch size:
   From: 100,000 rows/batch
   To: 50,000 rows/batch
   Result: More batches but faster per batch

2. Increase parallel threads:
   From: 1 thread
   To: 4 threads
   Result: 4x faster (if resource available)

3. Add source filter:
   Load recent: WHERE changed_date >= CURRENT_DATE - 30
   Reduces volume, faster extraction

4. Increase timeout:
   From: 300 seconds
   To: 600 seconds
   Only if network genuinely slow

5. Schedule off-peak:
   From: 09:00 (business hours)
   To: 23:00 (off-peak)
   Less system contention

Prevention:
- Estimate initial load size: Rows × 1KB = Storage
- Test extraction with sample before scheduling
- Monitor trends over time
- Set thresholds for alerts
```

## Data Flow Errors

### Memory and Resource Errors

#### Error: Out of memory - Java heap space
```
Code: MEM_001
Severity: CRITICAL
Message: Java heap space - Out of memory exception in Python operator

Causes:
1. Input dataset larger than available memory
2. Python operator loading entire dataframe at once
3. Memory leak in operator code
4. No chunking/pagination in processing
5. Intermediate results not freed

Diagnosis:
- Check input row count: SELECT COUNT(*) FROM source
- Calculate memory: rows × ~1KB per row = GB needed
- Review operator code: Memory allocation patterns
- Check available memory: Data Flow → Resource Settings

Solutions:
1. Chunked processing:
   ```python
   for chunk in pd.read_csv(file, chunksize=10000):
       process_chunk(chunk)  # Process smaller pieces
   ```

2. Add source filter:
   WHERE load_date >= CURRENT_DATE - 90
   (Extract 3 months instead of 3 years)

3. Increase memory allocation:
   Data Flow → Advanced → Memory: 16GB → 32GB
   Cost: Higher (verify in pricing)

4. Streaming/iterator pattern:
   Don't load entire dataframe, process by partition

5. Reduce intermediate objects:
   ```python
   # Bad: Creates copies
   df2 = df1.assign(col=df1['x'] * 2)
   df3 = df2.groupby('y').sum()

   # Good: Chain operations
   result = df1.assign(col=df1['x'] * 2).groupby('y').sum()
   ```

Prevention:
- Test with sample data first (LIMIT 10000)
- Monitor memory during execution
- Set alerts for memory > 80%
- Document operator memory requirements
```

#### Error: CPU limit exceeded - operation timeout
```
Code: CPU_001
Severity: HIGH
Message: CPU usage exceeded 100% limit; operator terminated

Causes:
1. Complex calculations on large dataset
2. Inefficient algorithm (O(n²) instead of O(n))
3. String operations on huge text fields
4. Regex patterns too complex
5. No optimization in operator code

Diagnosis:
- Check operation complexity: Nested loops? String parsing?
- Profile code: Which lines consume most CPU?
- Check algorithm: Is there more efficient way?

Solutions:
1. Optimize algorithm:
   # Bad: O(n²)
   for i in data:
       for j in data:
           if i['id'] == j['id']: ...

   # Good: O(n) with dict lookup
   id_map = {row['id']: row for row in data}
   for i in data:
       j = id_map.get(i['id'])

2. Use vectorized operations (numpy/pandas):
   # Bad: Loop
   result = [x * 2 for x in values]

   # Good: Vectorized
   result = values * 2  # 100x faster

3. Move complex logic to database:
   # Bad: Python processing
   data = df[df['revenue'] > 1000].groupby('customer')

   # Good: SQL processing (in data source)
   SELECT * FROM C_SALES WHERE REVENUE > 1000 GROUP BY CUSTOMER

4. Reduce dataset:
   Add WHERE clause to extract fewer rows

Prevention:
- Test complexity on representative data
- Monitor CPU during execution
- Document operator CPU requirements
- Use profiling tools to identify bottlenecks
```

### Data Type and Conversion Errors

#### Error: Cannot convert STRING to DECIMAL
```
Code: TYPE_001
Severity: HIGH
Message: TypeError: cannot convert value 'ABC123' from type STRING to DECIMAL

Causes:
1. Source delivers unexpected data format
2. Python operator assumes wrong type
3. Locale-specific formatting (comma vs period)
4. Special characters in numeric fields
5. NULL values or empty strings

Diagnosis:
```python
# Check actual data
print(df['amount'].dtype)  # STRING instead of expected DECIMAL
print(df['amount'].head(10))  # See examples
print(df['amount'].unique()[:20])  # Check for non-numeric
```

Solutions:
1. Safe type conversion with error handling:
   ```python
   df['amount'] = pd.to_numeric(
       df['amount'],
       errors='coerce'  # Non-numeric become NULL
   )
   ```

2. Clean before conversion:
   ```python
   df['amount'] = (
       df['amount']
       .astype(str)
       .str.replace(',', '.')  # European format
       .str.replace('$', '')  # Currency symbol
       .str.strip()  # Whitespace
   )
   df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
   ```

3. Handle NULLs from failed conversions:
   ```python
   df['amount'] = df['amount'].fillna(0)  # or any default
   ```

4. Add validation:
   ```python
   invalid = df['amount'].isnull().sum()
   if invalid > 0:
       print(f"WARNING: {invalid} values failed conversion")
   ```

Prevention:
- Examine source data: SELECT * FROM source LIMIT 100
- Document expected formats
- Add type validation in first operator step
- Log/alert on conversion failures
```

#### Error: Date format invalid
```
Code: TYPE_002
Severity: HIGH
Message: ParserError: unable to parse string "01/32/2024" at position 0

Causes:
1. Date in unexpected format (MM/DD/YYYY vs DD/MM/YYYY)
2. Invalid date values (day > 31, month > 12)
3. Timezone issues
4. Locale-specific interpretation

Diagnosis:
```python
# Check samples
print(df['date'].head(10))
# Output: ['01/32/2024', '02/30/2024', ...]
# Issue: Impossible dates (day > number of days in month)

# Check source format
SELECT DISTINCT DATE_FIELD FROM SOURCE LIMIT 20;
```

Solutions:
1. Specify format:
   ```python
   df['date'] = pd.to_datetime(
       df['date'],
       format='%m/%d/%Y',  # Explicit format
       errors='coerce'  # Invalid → NULL
   )
   ```

2. Try multiple formats:
   ```python
   for fmt in ['%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d']:
       try:
           df['date'] = pd.to_datetime(df['date'], format=fmt)
           break
       except:
           continue
   ```

3. Clean invalid dates:
   ```python
   df['date'] = pd.to_datetime(
       df['date'],
       errors='coerce'  # Invalid → NaT (NULL)
   )
   df['date'] = df['date'].fillna(pd.Timestamp('1900-01-01'))
   ```

Prevention:
- Document source date format
- Request ISO format (YYYY-MM-DD) from source
- Validate samples before full extraction
- Test with known good dates
```

### Python Operator Errors

#### Error: ImportError - module not found
```
Code: IMPORT_001
Severity: CRITICAL
Message: ImportError: No module named 'sklearn'

Causes:
1. Library not available in Datasphere environment
2. Typo in import statement
3. Library version mismatch
4. Non-standard library not installed

Diagnosis:
```python
# Check available libraries
import sys
print(sys.version)

# Test import
try:
    import sklearn
    print("sklearn available")
except ImportError:
    print("sklearn NOT available")
```

Solutions:
1. Use only standard libraries:
   ✓ pandas, numpy, scipy
   ✓ statistics, math, datetime
   ? sklearn, tensorflow (may not be available)

2. Implement without library:
   ```python
   # Instead of sklearn.preprocessing.StandardScaler
   def standardize(values):
       mean = sum(values) / len(values)
       std = (sum((x - mean)**2 for x in values) / len(values))**0.5
       return [(x - mean) / std for x in values]
   ```

3. Contact support if critical library needed

Prevention:
- Test imports before deploying
- List available libraries in documentation
- Avoid exotic/non-standard libraries
- Implement fallback logic
```

#### Error: NameError - undefined variable
```
Code: NAME_001
Severity: HIGH
Message: NameError: name 'df' is not defined

Causes:
1. Variable name typo
2. Variable not created before use
3. Scope issue (variable local, not available)
4. Import statement failed silently

Diagnosis:
```python
# Check execution line by line
def transform(input_df):
    print(f"Input type: {type(input_df)}")
    print(f"Input shape: {input_df.shape}")
    # If input_df not available, input parameter name wrong

    dff = input_df.assign(col=1)  # Typo: dff vs df
    print(df)  # ERROR: df doesn't exist
```

Solutions:
1. Check parameter names match:
   ```python
   def transform(input_df):  # Parameter name
       # Use input_df, not df
       return input_df.assign(new_col=1)
   ```

2. Declare variables before use:
   ```python
   # Bad
   result = data + offset  # offset not defined!

   # Good
   offset = 100
   result = data + offset
   ```

3. Add debug output:
   ```python
   print(f"Available variables: {dir()}")
   print(f"Variable values: df={df}, offset={offset}")
   ```

Prevention:
- Use IDE with syntax checking
- Test on sample data first
- Add debug print statements
- Use consistent naming conventions
```

#### Error: SyntaxError in operator code
```
Code: SYNTAX_001
Severity: CRITICAL
Message: SyntaxError: invalid syntax (line 5)

Causes:
1. Missing colon or parenthesis
2. Indentation error
3. Invalid operator
4. Reserved keyword as variable name

Diagnosis:
```python
# Line 5 with error:
def transform(input_df)  # Missing colon!
    return input_df

# Fix:
def transform(input_df):
    return input_df
```

Solutions:
1. Check syntax:
   ```bash
   python -m py_compile operator.py
   ```

2. Use IDE with syntax highlighting

3. Common issues:
   - Missing colon after function/if/for
   - Indentation not consistent (tabs vs spaces)
   - Extra parenthesis
   - Invalid operator combination

Prevention:
- Use Python IDE with linting
- Test code locally before deploying
- Enable syntax checking in editor
```

## Transformation Flow Errors

### SQL Syntax Errors

#### Error: Column not found in table
```
Code: SQL_001
Severity: HIGH
Message: SQL Error [207]: Column 'REVENUE_AMOUNT' not found

Causes:
1. Column name typo
2. Column removed in schema update
3. Wrong table referenced
4. Case sensitivity issue (AMOUNT vs Amount)

Diagnosis:
- Check table schema: get_table_schema('C_CUSTOMER')
- Verify column in source: SELECT REVENUE_AMOUNT FROM C_CUSTOMER LIMIT 1
- Check flow mappings

Solutions:
1. Fix column name:
   # Bad
   SELECT REVENUE_AMOUNT FROM C_CUSTOMER

   # Good (correct name)
   SELECT REVENUE FROM C_CUSTOMER

2. Qualify table name:
   SELECT sc.REVENUE FROM SOURCE_CUSTOMER sc

3. Use schema-qualified name:
   SELECT REVENUE FROM SAP_SOURCE.C_CUSTOMER

Prevention:
- Refresh schema before writing SQL
- Test queries incrementally
- Use aliases for clarity
```

#### Error: Table not found
```
Code: SQL_002
Severity: HIGH
Message: SQL Error [261]: Table 'C_CUSTOMER' not found in schema

Causes:
1. Table doesn't exist
2. Schema not specified
3. Table name typo
4. Table in different schema/system

Diagnosis:
- Check table exists: SELECT * FROM C_CUSTOMER LIMIT 1
- Verify schema: SELECT * FROM SAP_SOURCE.C_CUSTOMER LIMIT 1
- Check source system connection

Solutions:
1. Specify schema:
   SELECT * FROM SAP_SOURCE.C_CUSTOMER

2. Create table first if missing:
   SELECT * FROM source_system.C_CUSTOMER

3. Verify table name
```

#### Error: Data type conversion impossible
```
Code: SQL_003
Severity: HIGH
Message: SQL Error [389]: CAST from [VARCHAR] to [INTEGER] not possible

Causes:
1. Column contains non-numeric characters
2. NULL values with no default
3. Precision loss (DECIMAL → INTEGER)

Diagnosis:
- Check data: SELECT AMOUNT, TYPEOF(AMOUNT) FROM source LIMIT 100
- Verify target type requirements

Solutions:
1. Use CAST with error handling:
   CAST(AMOUNT AS DECIMAL(19,2)) AS converted_amount
   Or use SAFE_CAST

2. Trim/clean before conversion:
   CAST(TRIM(REPLACE(AMOUNT, ',', '.')) AS DECIMAL)

3. Use COALESCE for NULLs:
   COALESCE(CAST(AMOUNT AS DECIMAL), 0) AS amount
```

### Delta and Watermark Errors

#### Error: Watermark value not in source data
```
Code: DELTA_002
Severity: HIGH
Message: Watermark timestamp '2024-01-15 23:59:59' exceeds maximum in source

Causes:
1. Watermark set to future date
2. Source data older than watermark
3. No new data since last extraction
4. Timezone mismatch

Diagnosis:
- Check current max: SELECT MAX(CHANGED_AT) FROM C_CUSTOMER
- Check stored watermark: SELECT * FROM WATERMARK_CONTROL
- Compare timestamps

Solutions:
1. Reset to valid value:
   UPDATE WATERMARK_CONTROL
   SET LAST_WATERMARK = (SELECT MAX(CHANGED_AT) FROM C_CUSTOMER)

2. Or set to past value:
   UPDATE WATERMARK_CONTROL
   SET LAST_WATERMARK = CURRENT_TIMESTAMP() - INTERVAL '1' HOUR

Prevention:
- Don't manually set watermark to future
- Validate watermark before loading
- Add check: watermark <= current_max_value
```

#### Error: Overlapping delta loads - duplicate records
```
Code: DELTA_003
Severity: MEDIUM
Message: 1000 duplicate records loaded; watermark not advancing correctly

Causes:
1. Watermark not advancing between runs
2. Same change records selected multiple times
3. Overlap in extraction range

Diagnosis:
- Compare consecutive runs:
  Run 1: WHERE changed_at > 2024-01-15 12:00:00
  Run 2: WHERE changed_at > 2024-01-15 12:00:00 (same!)
- Check stored watermark

Solutions:
1. Advance watermark after successful load:
   ```sql
   UPDATE WATERMARK_CONTROL
   SET LAST_WATERMARK = CURRENT_TIMESTAMP()
   WHERE TABLE_NAME = 'CUSTOMER'
   ```

2. Deduplicate in merge:
   ```sql
   MERGE INTO TARGET_CUSTOMER tc
   USING (
       SELECT * FROM SOURCE_DELTA
       QUALIFY ROW_NUMBER() OVER (
           PARTITION BY CUSTOMER_ID
           ORDER BY CHANGENUMBER DESC
       ) = 1
   ) delta
   ON tc.CUSTOMER_ID = delta.CUSTOMER_ID
   ...
   ```

Prevention:
- Verify watermark advancement in logs
- Check stored value after each load
- Add validations
```

### Lock and Constraint Errors

#### Error: Table locked - cannot write
```
Code: LOCK_001
Severity: MEDIUM
Message: SQL Error [389]: Cannot acquire lock on table TARGET_CUSTOMER

Causes:
1. Other process writing to same table
2. Long-running transaction holding lock
3. Deadlock between processes
4. Manual lock not released

Diagnosis:
- Check locks: CALL DBMS_LOCKS.CHECK_LOCKS()
- Check processes: SELECT * FROM M_TRANSACTIONS
- Check blocking: SELECT * FROM M_BLOCKED_TRANSACTIONS

Solutions:
1. Wait and retry:
   Increase timeout, flow will retry

2. Kill blocking transaction:
   SELECT CONNECTION_ID FROM M_CONNECTIONS WHERE SESSION_ID = 'X'
   ALTER SYSTEM KILL SESSION 'X'

3. Run serially instead of parallel

Prevention:
- Use row-level locking (lock specific records)
- Keep transactions short
- Release locks promptly
```

#### Error: Foreign key constraint violated
```
Code: CONST_001
Severity: HIGH
Message: SQL Error [301]: Foreign key constraint violation in table ORDERS

Causes:
1. Order references non-existent customer
2. Parent record deleted while child exists
3. Wrong key value

Diagnosis:
- Check orphan records:
  SELECT * FROM ORDERS o
  WHERE NOT EXISTS (SELECT 1 FROM CUSTOMER c WHERE c.ID = o.CUSTOMER_ID)

Solutions:
1. Load only valid records:
   ```sql
   MERGE INTO ORDERS
   USING (
       SELECT * FROM ORDERS_STAGING os
       WHERE EXISTS (SELECT 1 FROM CUSTOMER c WHERE c.ID = os.CUSTOMER_ID)
   ) delta
   ...
   ```

2. Create missing parents first

Prevention:
- Validate before merge
- Load parents before children
- Use referential integrity constraints
```

## Performance Degradation Issues

### Diagnosis Workflow

```
Flow taking longer than expected
├─ Step 1: Compare to historical runs
│  ├─ Previous avg: 10 minutes
│  ├─ Current run: 25 minutes
│  └─ Degradation: 2.5x slower
│
├─ Step 2: Identify bottleneck
│  ├─ Source extraction: Slow
│  ├─ Transformation: Normal
│  └─ Target load: Normal
│  → Problem: Source slowdown
│
├─ Step 3: Investigate root cause
│  ├─ Source system load
│  ├─ Network latency
│  ├─ Data volume increase
│  └─ Cloud Connector resource
│
└─ Step 4: Apply solution
   ├─ Reduce batch size
   ├─ Add filters
   ├─ Increase parallelism
   └─ Schedule differently
```

### Common Performance Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Large data volume | Extraction takes 2h (was 30min) | Add WHERE filter, split into smaller batch |
| Network congestion | Latency 500ms (was 50ms) | Schedule off-peak, use compression |
| Source system busy | CPU/Memory high in SM50 | Schedule when less busy (23:00) |
| Cloud Connector overloaded | Low throughput (10MB/s vs 100MB/s) | Add standby CC, increase resources |
| Inefficient SQL | Slow aggregation | Add indexes, rewrite query, increase DB resources |
| Python operator inefficient | CPU 95% for simple operation | Optimize algorithm, use vectorization |
| Memory pressure | Swapping to disk | Reduce batch size, add filter |
| Unindexed tables | Table scan vs index seek | Add index on key columns, vacuum analyze |

