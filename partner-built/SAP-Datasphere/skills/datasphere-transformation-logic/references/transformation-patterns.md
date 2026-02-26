# Transformation Patterns Reference

## SQLScript Syntax Reference

### MERGE Statement Complete Syntax

```sql
MERGE INTO target_table AS tt
USING source_table AS st
    ON tt.key_column = st.key_column
WHEN MATCHED AND condition THEN
    UPDATE SET
        col1 = st.col1,
        col2 = st.col2
WHEN MATCHED THEN
    DELETE
WHEN NOT MATCHED THEN
    INSERT (col1, col2, col3)
    VALUES (st.col1, st.col2, st.col3);
```

#### MERGE Examples

**Basic Upsert (Insert or Update)**
```sql
MERGE INTO CUSTOMER_MASTER cm
USING CUSTOMER_STAGING cs
    ON cm.CUSTOMER_ID = cs.CUSTOMER_ID
WHEN MATCHED THEN
    UPDATE SET
        cm.CUSTOMER_NAME = cs.CUSTOMER_NAME,
        cm.EMAIL = cs.EMAIL,
        cm.UPDATED_AT = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
    INSERT (CUSTOMER_ID, CUSTOMER_NAME, EMAIL, CREATED_AT, UPDATED_AT)
    VALUES (cs.CUSTOMER_ID, cs.CUSTOMER_NAME, cs.EMAIL, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());
```

**Soft Delete Pattern**
```sql
MERGE INTO PRODUCT_DIM pd
USING PRODUCT_STAGING ps
    ON pd.PRODUCT_ID = ps.PRODUCT_ID
WHEN MATCHED AND ps.IS_ACTIVE = 0 THEN
    UPDATE SET
        pd.EFFECTIVE_END_DATE = CURRENT_DATE,
        pd.IS_CURRENT = 'N'
WHEN MATCHED AND ps.IS_ACTIVE = 1 THEN
    UPDATE SET
        pd.PRODUCT_NAME = ps.PRODUCT_NAME,
        pd.PRICE = ps.PRICE,
        pd.UPDATED_AT = CURRENT_TIMESTAMP()
WHEN NOT MATCHED AND ps.IS_ACTIVE = 1 THEN
    INSERT (PRODUCT_ID, PRODUCT_NAME, PRICE, EFFECTIVE_START_DATE, IS_CURRENT)
    VALUES (ps.PRODUCT_ID, ps.PRODUCT_NAME, ps.PRICE, CURRENT_DATE, 'Y');
```

**Three-Way Merge (Insert, Update, Delete)**
```sql
MERGE INTO EMPLOYEE e
USING EMPLOYEE_STAGING es
    ON e.EMP_ID = es.EMP_ID
WHEN MATCHED AND es.STATUS = 'TERMINATED' THEN
    DELETE
WHEN MATCHED THEN
    UPDATE SET
        e.EMP_NAME = es.EMP_NAME,
        e.SALARY = es.SALARY,
        e.DEPARTMENT = es.DEPARTMENT,
        e.MODIFIED_DATE = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
    INSERT (EMP_ID, EMP_NAME, SALARY, DEPARTMENT, CREATED_DATE)
    VALUES (es.EMP_ID, es.EMP_NAME, es.SALARY, es.DEPARTMENT, CURRENT_TIMESTAMP());
```

### Window Functions Reference

#### ROW_NUMBER() - Sequential numbering within partition

```sql
-- Get top 3 products by revenue in each category
SELECT
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    REVENUE,
    ROW_NUMBER() OVER (PARTITION BY CATEGORY ORDER BY REVENUE DESC) AS RN
FROM PRODUCTS
QUALIFY RN <= 3;
```

#### RANK() and DENSE_RANK() - Handle ties differently

```sql
-- RANK() skips numbers after ties, DENSE_RANK() doesn't
SELECT
    EMPLOYEE_ID,
    SALARY,
    RANK() OVER (ORDER BY SALARY DESC) AS RANK_NO,
    DENSE_RANK() OVER (ORDER BY SALARY DESC) AS DENSE_RANK_NO
FROM EMPLOYEES;

-- Output:
-- EMP1, 100000, 1, 1
-- EMP2, 100000, 1, 1
-- EMP3, 90000,  3, 2    <- RANK skips 2, DENSE_RANK doesn't
```

#### NTILE() - Divide into buckets

```sql
-- Divide customers into quartiles by revenue
SELECT
    CUSTOMER_ID,
    TOTAL_REVENUE,
    NTILE(4) OVER (ORDER BY TOTAL_REVENUE DESC) AS QUARTILE
FROM CUSTOMER_REVENUE
ORDER BY QUARTILE, TOTAL_REVENUE DESC;
```

#### LAG() and LEAD() - Look at adjacent rows

```sql
-- Calculate month-over-month revenue change
SELECT
    YEAR_MONTH,
    REVENUE,
    LAG(REVENUE) OVER (ORDER BY YEAR_MONTH) AS PREV_MONTH_REVENUE,
    REVENUE - LAG(REVENUE) OVER (ORDER BY YEAR_MONTH) AS MONTH_CHANGE,
    ROUND(
        100.0 * (REVENUE - LAG(REVENUE) OVER (ORDER BY YEAR_MONTH)) /
        LAG(REVENUE) OVER (ORDER BY YEAR_MONTH),
        2
    ) AS PERCENT_CHANGE
FROM MONTHLY_REVENUE
ORDER BY YEAR_MONTH;
```

#### Running Totals and Cumulative Sums

```sql
-- Calculate running revenue total
SELECT
    DATE_FIELD,
    DAILY_REVENUE,
    SUM(DAILY_REVENUE) OVER (
        ORDER BY DATE_FIELD
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS CUMULATIVE_REVENUE,
    AVG(DAILY_REVENUE) OVER (
        ORDER BY DATE_FIELD
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS ROLLING_7DAY_AVG
FROM DAILY_SALES
ORDER BY DATE_FIELD;
```

### Common Table Expressions (CTEs)

#### Multi-Level CTE with Dependencies

```sql
WITH monthly_sales AS (
    SELECT
        CUSTOMER_ID,
        EXTRACT(YEAR_MONTH FROM ORDER_DATE) AS YEAR_MONTH,
        SUM(ORDER_AMOUNT) AS MONTHLY_REVENUE
    FROM ORDERS
    GROUP BY CUSTOMER_ID, EXTRACT(YEAR_MONTH FROM ORDER_DATE)
),
customer_annual AS (
    SELECT
        CUSTOMER_ID,
        SUM(MONTHLY_REVENUE) AS ANNUAL_REVENUE,
        AVG(MONTHLY_REVENUE) AS AVG_MONTHLY_REVENUE,
        MAX(MONTHLY_REVENUE) AS MAX_MONTHLY_REVENUE,
        MIN(MONTHLY_REVENUE) AS MIN_MONTHLY_REVENUE
    FROM monthly_sales
    GROUP BY CUSTOMER_ID
),
customer_with_rank AS (
    SELECT
        CUSTOMER_ID,
        ANNUAL_REVENUE,
        RANK() OVER (ORDER BY ANNUAL_REVENUE DESC) AS REVENUE_RANK,
        CASE
            WHEN ANNUAL_REVENUE >= 500000 THEN 'PLATINUM'
            WHEN ANNUAL_REVENUE >= 250000 THEN 'GOLD'
            WHEN ANNUAL_REVENUE >= 100000 THEN 'SILVER'
            ELSE 'BRONZE'
        END AS CUSTOMER_SEGMENT
    FROM customer_annual
)
SELECT *
FROM customer_with_rank
WHERE REVENUE_RANK <= 100
ORDER BY REVENUE_RANK;
```

## Delta Load Patterns

### Timestamp-Based Delta Load

```sql
PROCEDURE LOAD_CUSTOMER_DELTA_TIMESTAMP (
    IN iv_last_load_timestamp TIMESTAMP
)
LANGUAGE SQLSCRIPT
AS
BEGIN
    -- Get the current maximum timestamp (becomes next watermark)
    DECLARE v_current_max_timestamp TIMESTAMP;

    SELECT MAX(LAST_MODIFIED_AT) INTO v_current_max_timestamp
    FROM SOURCE_CUSTOMER;

    -- Load only modified records
    UPSERT TARGET_CUSTOMER (
        CUSTOMER_ID,
        NAME,
        EMAIL,
        PHONE,
        LAST_MODIFIED_AT
    )
    SELECT
        CUSTOMER_ID,
        NAME,
        EMAIL,
        PHONE,
        LAST_MODIFIED_AT
    FROM SOURCE_CUSTOMER
    WHERE LAST_MODIFIED_AT > :iv_last_load_timestamp
        AND LAST_MODIFIED_AT <= :v_current_max_timestamp;

    -- Update the watermark
    UPDATE LOAD_WATERMARK
    SET LAST_LOAD_TIMESTAMP = :v_current_max_timestamp,
        LOAD_COUNT = LOAD_COUNT + 1,
        LAST_RUN_DATE = CURRENT_TIMESTAMP()
    WHERE TABLE_NAME = 'CUSTOMER';
END;
```

### Change Data Capture (CDC) Pattern

```sql
PROCEDURE LOAD_FROM_CDC_QUEUE (
    IN iv_queue_name STRING
)
LANGUAGE SQLSCRIPT
AS
BEGIN
    -- Process CDC log entries
    MERGE INTO FACT_ORDERS fo
    USING (
        SELECT
            ORDER_ID,
            CUSTOMER_ID,
            ORDER_AMOUNT,
            ORDER_DATE,
            OPERATION,
            OPERATION_TIMESTAMP
        FROM CDC_QUEUE
        WHERE QUEUE_NAME = :iv_queue_name
            AND PROCESSED_FLAG = 'N'
    ) cdc
        ON fo.ORDER_ID = cdc.ORDER_ID
    WHEN MATCHED AND cdc.OPERATION = 'D' THEN
        DELETE
    WHEN MATCHED AND cdc.OPERATION IN ('U', 'M') THEN
        UPDATE SET
            fo.CUSTOMER_ID = cdc.CUSTOMER_ID,
            fo.ORDER_AMOUNT = cdc.ORDER_AMOUNT,
            fo.ORDER_DATE = cdc.ORDER_DATE
    WHEN NOT MATCHED AND cdc.OPERATION IN ('I', 'M') THEN
        INSERT (ORDER_ID, CUSTOMER_ID, ORDER_AMOUNT, ORDER_DATE)
        VALUES (cdc.ORDER_ID, cdc.CUSTOMER_ID, cdc.ORDER_AMOUNT, cdc.ORDER_DATE);

    -- Mark CDC entries as processed
    UPDATE CDC_QUEUE
    SET PROCESSED_FLAG = 'Y',
        PROCESSED_TIMESTAMP = CURRENT_TIMESTAMP()
    WHERE QUEUE_NAME = :iv_queue_name
        AND PROCESSED_FLAG = 'N';
END;
```

### Numeric Sequence Delta Load

```sql
PROCEDURE LOAD_MATERIAL_DELTA_SEQUENCE (
    IN iv_last_sequence INT
)
LANGUAGE SQLSCRIPT
AS
BEGIN
    DECLARE v_current_max_sequence INT;

    -- Load only records with sequence > last_sequence
    SELECT MAX(CHANGE_SEQUENCE) INTO v_current_max_sequence
    FROM SOURCE_MATERIAL;

    UPSERT TARGET_MATERIAL
    SELECT
        MATERIAL_ID,
        MATERIAL_NAME,
        UNIT_PRICE,
        MATERIAL_GROUP,
        CHANGE_SEQUENCE
    FROM SOURCE_MATERIAL
    WHERE CHANGE_SEQUENCE > :iv_last_sequence
        AND CHANGE_SEQUENCE <= :v_current_max_sequence;

    -- Store the new sequence number
    UPDATE SEQUENCE_WATERMARK
    SET LAST_SEQUENCE = :v_current_max_sequence,
        LAST_LOAD_DATE = CURRENT_TIMESTAMP()
    WHERE TABLE_NAME = 'MATERIAL';
END;
```

## SCD Type 2 Implementation Templates

### Full SCD Type 2 Pattern with History

```sql
PROCEDURE LOAD_DIM_ACCOUNT_SCD2 (
    IN iv_effective_date DATE
)
LANGUAGE SQLSCRIPT
AS
BEGIN
    DECLARE EXIT HANDLER FOR SQL_ERROR
    BEGIN
        RESIGNAL;
    END;

    -- Step 1: Identify changed attributes in source
    WITH changed_accounts AS (
        SELECT
            sa.ACCOUNT_ID,
            sa.ACCOUNT_NAME,
            sa.ACCOUNT_TYPE,
            sa.REGION,
            sa.MANAGER_ID,
            da.ACCOUNT_SK,
            da.ACCOUNT_NAME AS OLD_NAME,
            da.ACCOUNT_TYPE AS OLD_TYPE,
            da.REGION AS OLD_REGION,
            da.MANAGER_ID AS OLD_MANAGER
        FROM SOURCE_ACCOUNT sa
        LEFT JOIN DIM_ACCOUNT da
            ON sa.ACCOUNT_ID = da.ACCOUNT_ID
            AND da.IS_CURRENT = 'Y'
        WHERE sa.ACCOUNT_ID NOT IN (
            SELECT DISTINCT ACCOUNT_ID FROM DIM_ACCOUNT WHERE IS_CURRENT = 'Y'
        )
        OR (
            da.ACCOUNT_NAME <> sa.ACCOUNT_NAME
            OR da.ACCOUNT_TYPE <> sa.ACCOUNT_TYPE
            OR da.REGION <> sa.REGION
            OR da.MANAGER_ID <> sa.MANAGER_ID
        )
    )
    -- Step 2: Close old records for changed attributes
    UPDATE DIM_ACCOUNT
    SET END_DATE = :iv_effective_date,
        IS_CURRENT = 'N'
    WHERE ACCOUNT_SK IN (SELECT ACCOUNT_SK FROM changed_accounts);

    -- Step 3: Insert new records (both new accounts and changed versions)
    INSERT INTO DIM_ACCOUNT (
        ACCOUNT_SK,
        ACCOUNT_ID,
        ACCOUNT_NAME,
        ACCOUNT_TYPE,
        REGION,
        MANAGER_ID,
        EFFECTIVE_DATE,
        END_DATE,
        IS_CURRENT
    )
    SELECT
        NEXT VALUE FOR SEQ_ACCOUNT_SK,
        ACCOUNT_ID,
        ACCOUNT_NAME,
        ACCOUNT_TYPE,
        REGION,
        MANAGER_ID,
        :iv_effective_date,
        NULL,
        'Y'
    FROM SOURCE_ACCOUNT;
END;
```

### Audit Trail for SCD Type 2

```sql
PROCEDURE AUDIT_SCD2_CHANGES (
    IN iv_table_name STRING,
    IN iv_effective_date DATE
)
LANGUAGE SQLSCRIPT
AS
BEGIN
    INSERT INTO DIM_AUDIT_TRAIL (
        TABLE_NAME,
        RECORD_ID,
        CHANGE_TYPE,
        CHANGED_COLUMNS,
        OLD_VALUES,
        NEW_VALUES,
        EFFECTIVE_DATE,
        AUDIT_TIMESTAMP
    )
    SELECT
        :iv_table_name,
        ACCOUNT_ID,
        CASE
            WHEN OLD_NAME IS NULL THEN 'NEW'
            ELSE 'CHANGED'
        END,
        CONCAT_STRING('|', NULL, cols),
        OLD_VALUES,
        NEW_VALUES,
        :iv_effective_date,
        CURRENT_TIMESTAMP()
    FROM (
        SELECT
            sa.ACCOUNT_ID,
            sa.ACCOUNT_NAME,
            da.ACCOUNT_NAME AS OLD_NAME,
            STRING_AGG(
                CASE
                    WHEN da.ACCOUNT_NAME <> sa.ACCOUNT_NAME THEN 'ACCOUNT_NAME'
                    WHEN da.REGION <> sa.REGION THEN 'REGION'
                    WHEN da.MANAGER_ID <> sa.MANAGER_ID THEN 'MANAGER_ID'
                END,
                '|'
            ) AS cols,
            CONCAT('OLD_NAME:', COALESCE(da.ACCOUNT_NAME, 'NULL'),
                   '|OLD_REGION:', COALESCE(da.REGION, 'NULL')) AS OLD_VALUES,
            CONCAT('NEW_NAME:', COALESCE(sa.ACCOUNT_NAME, 'NULL'),
                   '|NEW_REGION:', COALESCE(sa.REGION, 'NULL')) AS NEW_VALUES
        FROM SOURCE_ACCOUNT sa
        LEFT JOIN DIM_ACCOUNT da
            ON sa.ACCOUNT_ID = da.ACCOUNT_ID
            AND da.IS_CURRENT = 'Y'
        GROUP BY sa.ACCOUNT_ID, sa.ACCOUNT_NAME, da.ACCOUNT_NAME, da.REGION, da.MANAGER_ID
    );
END;
```

## Data Cleansing Transformation Recipes

### Remove Duplicates, Keep Latest

```sql
CREATE TABLE CUSTOMER_CLEANED AS
WITH ranked_records AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY EMAIL
            ORDER BY LAST_MODIFIED_AT DESC
        ) AS RN
    FROM CUSTOMER_RAW
    WHERE EMAIL IS NOT NULL
)
SELECT * FROM ranked_records WHERE RN = 1;
```

### Fix Common Data Quality Issues

```sql
SELECT
    -- Trim and uppercase strings
    UPPER(TRIM(CUSTOMER_NAME)) AS CUSTOMER_NAME,
    -- Standardize phone format
    REPLACE(REPLACE(REPLACE(PHONE, ' ', ''), '-', ''), '(', ''), ')', '') AS PHONE_NORMALIZED,
    -- Handle null amounts
    COALESCE(SALES_AMOUNT, 0) AS SALES_AMOUNT,
    -- Fix dates
    CASE
        WHEN BIRTH_DATE > CURRENT_DATE THEN CURRENT_DATE - 1
        WHEN BIRTH_DATE < '1900-01-01' THEN NULL
        ELSE BIRTH_DATE
    END AS BIRTH_DATE_FIXED,
    -- Standardize boolean
    CASE WHEN IS_ACTIVE IN ('Y', 'true', 1, 'yes') THEN 'Y' ELSE 'N' END AS IS_ACTIVE
FROM CUSTOMER_RAW;
```

### Consolidate Duplicate Entries

```sql
SELECT
    CUSTOMER_ID,
    MAX(CUSTOMER_NAME) AS CUSTOMER_NAME,
    MAX(EMAIL) AS EMAIL,
    COUNT(*) AS OCCURRENCE_COUNT,
    MAX(LAST_MODIFIED_AT) AS LATEST_UPDATE,
    STRING_AGG(PHONE, '|' ORDER BY PHONE) AS ALL_PHONES
FROM CUSTOMER_RAW
WHERE CUSTOMER_ID IS NOT NULL
GROUP BY CUSTOMER_ID
HAVING COUNT(*) > 1;
```

### Classify Data Quality Issues

```sql
SELECT
    CUSTOMER_ID,
    CUSTOMER_NAME,
    EMAIL,
    PHONE,
    CASE
        WHEN CUSTOMER_NAME IS NULL THEN 'MISSING_NAME'
        WHEN LENGTH(TRIM(CUSTOMER_NAME)) < 3 THEN 'NAME_TOO_SHORT'
        WHEN EMAIL IS NULL THEN 'MISSING_EMAIL'
        WHEN NOT EMAIL LIKE '%@%.%' THEN 'INVALID_EMAIL'
        WHEN PHONE IS NULL THEN 'MISSING_PHONE'
        WHEN REGEXP_LIKE(PHONE, '^[0-9\-\(\) ]+$') = 0 THEN 'INVALID_PHONE'
        ELSE 'VALID'
    END AS DATA_QUALITY_FLAG
FROM CUSTOMER_RAW;
```

## Date/Time Manipulation Functions

### Fiscal Calendar Calculations

```sql
-- Return week number within fiscal year
SELECT
    CALENDAR_DATE,
    EXTRACT(YEAR FROM CALENDAR_DATE) AS CAL_YEAR,
    EXTRACT(MONTH FROM CALENDAR_DATE) AS CAL_MONTH,
    EXTRACT(WEEK FROM CALENDAR_DATE) AS CAL_WEEK,
    -- Fiscal year starting April 1
    CASE
        WHEN MONTH(CALENDAR_DATE) >= 4
        THEN YEAR(CALENDAR_DATE)
        ELSE YEAR(CALENDAR_DATE) - 1
    END AS FISCAL_YEAR,
    -- Fiscal month (1-12, starting April)
    CASE
        WHEN MONTH(CALENDAR_DATE) >= 4
        THEN MONTH(CALENDAR_DATE) - 3
        ELSE MONTH(CALENDAR_DATE) + 9
    END AS FISCAL_MONTH,
    -- Fiscal quarter
    CASE
        WHEN MONTH(CALENDAR_DATE) IN (4, 5, 6) THEN 1
        WHEN MONTH(CALENDAR_DATE) IN (7, 8, 9) THEN 2
        WHEN MONTH(CALENDAR_DATE) IN (10, 11, 12) THEN 3
        ELSE 4
    END AS FISCAL_QUARTER
FROM DATE_DIMENSION;
```

### Age and Duration Calculations

```sql
SELECT
    CUSTOMER_ID,
    BIRTH_DATE,
    -- Age in years
    DATEDIFF(YEAR, BIRTH_DATE, CURRENT_DATE) AS AGE_YEARS,
    -- Exact age including months and days
    ROUND(DATEDIFF(DAY, BIRTH_DATE, CURRENT_DATE) / 365.25, 2) AS AGE_YEARS_EXACT,
    -- Tenure in months
    DATEDIFF(MONTH, CUSTOMER_START_DATE, CURRENT_DATE) AS TENURE_MONTHS,
    -- Days since last activity
    DATEDIFF(DAY, LAST_ACTIVITY_DATE, CURRENT_DATE) AS DAYS_INACTIVE
FROM CUSTOMER;
```

### Period-Over-Period Comparisons

```sql
-- Compare current month to same month last year
SELECT
    curr.YEAR_MONTH,
    curr.REVENUE AS CURRENT_REVENUE,
    prev.REVENUE AS PRIOR_YEAR_REVENUE,
    curr.REVENUE - prev.REVENUE AS ABSOLUTE_CHANGE,
    ROUND(100.0 * (curr.REVENUE - prev.REVENUE) / prev.REVENUE, 2) AS PERCENT_CHANGE
FROM MONTHLY_REVENUE curr
LEFT JOIN MONTHLY_REVENUE prev
    ON curr.CUSTOMER_ID = prev.CUSTOMER_ID
    AND DATE_ADD(prev.YEAR_MONTH, INTERVAL 12 MONTH) = curr.YEAR_MONTH
ORDER BY curr.YEAR_MONTH;
```

### Rolling Window Periods

```sql
-- 13-week rolling average
SELECT
    WEEK_ENDING_DATE,
    WEEKLY_REVENUE,
    AVG(WEEKLY_REVENUE) OVER (
        ORDER BY WEEK_ENDING_DATE
        ROWS BETWEEN 12 PRECEDING AND CURRENT ROW
    ) AS ROLLING_13WEEK_AVG,
    -- YTD total
    SUM(WEEKLY_REVENUE) OVER (
        PARTITION BY EXTRACT(YEAR FROM WEEK_ENDING_DATE)
        ORDER BY WEEK_ENDING_DATE
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS YTD_REVENUE
FROM WEEKLY_REVENUE_TREND
ORDER BY WEEK_ENDING_DATE;
```

## Python Operator API Reference

### Basic DataFrame Operations

```python
import pandas as pd

def transform_data(input_df):
    """
    Common DataFrame operations
    """
    # Select columns
    subset = input_df[['customer_id', 'amount', 'date']]

    # Filter rows
    active = input_df[input_df['status'] == 'ACTIVE']

    # Add computed columns
    input_df['new_column'] = input_df['amount'] * 1.1

    # Rename columns
    renamed = input_df.rename(columns={'amount': 'sale_amount'})

    # Drop nulls in specific column
    no_nulls = input_df.dropna(subset=['amount'])

    return input_df
```

### Aggregation and Grouping

```python
def aggregate_by_segment(orders_df):
    """
    Group and aggregate operations
    """
    summary = orders_df.groupby('customer_segment').agg({
        'order_amount': ['sum', 'mean', 'count', 'std'],
        'order_date': ['min', 'max'],
        'customer_id': 'nunique'
    }).reset_index()

    # Multi-level grouping
    customer_segment = orders_df.groupby(['customer_id', 'segment']).agg(
        total_amount=('order_amount', 'sum'),
        order_count=('order_id', 'count'),
        avg_order_size=('order_amount', 'mean')
    ).reset_index()

    return summary
```

### Merging and Joining

```python
def join_dimensions(facts_df, customer_df, product_df):
    """
    Multi-input fusion with joins
    """
    # Inner join
    enriched = facts_df.merge(
        customer_df[['customer_id', 'segment', 'region']],
        on='customer_id',
        how='inner'
    )

    # Left join with product
    enriched = enriched.merge(
        product_df[['product_id', 'category', 'list_price']],
        on='product_id',
        how='left'
    )

    # Fill missing with defaults
    enriched['segment'] = enriched['segment'].fillna('UNKNOWN')
    enriched['category'] = enriched['category'].fillna('UNCATEGORIZED')

    return enriched
```

### Advanced Transformations

```python
def apply_business_rules(orders_df, rules_config):
    """
    Complex business logic
    """
    # Apply conditional transformations
    orders_df['discount_rate'] = orders_df.apply(
        lambda row: apply_discount_rule(
            row['order_amount'],
            row['customer_segment'],
            row['order_date']
        ),
        axis=1
    )

    # Pivot transformation
    monthly_summary = orders_df.pivot_table(
        index='customer_id',
        columns='order_month',
        values='order_amount',
        aggfunc='sum',
        fill_value=0
    )

    # String operations
    orders_df['normalized_name'] = orders_df['customer_name'].str.upper().str.strip()

    return orders_df
```

