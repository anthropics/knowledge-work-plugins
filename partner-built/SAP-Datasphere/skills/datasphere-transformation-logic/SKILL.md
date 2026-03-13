---
name: Transformation Logic Generator
description: "Generate and validate SQLScript and Python transformation logic for Data Flows and Transformation Flows. Use this when building complex transformations, optimizing performance, handling delta logic, or implementing SCD Type 2 slowly changing dimensions."
---

# Transformation Logic Generator

## Overview

This skill helps you design, write, and validate transformation logic for SAP Datasphere. Whether you're building a Transformation Flow with SQLScript or a Data Flow with Python operators, this skill provides patterns, best practices, and diagnostic tools to ensure your transformations are correct, performant, and maintainable.

## When to Use This Skill

- **Designing transformations** from scratch: Deciding which tool and language to use
- **Handling delta logic**: Implementing incremental loads with watermarks
- **Slowly Changing Dimensions (SCD Type 2)**: Tracking history of dimension changes
- **Complex data cleansing**: Deduplication, pivoting, date/time normalization
- **Performance optimization**: Dealing with large datasets or slow execution
- **Troubleshooting transformation failures**: SQL errors, type mismatches, operator crashes
- **Data type mapping**: Converting between source and target systems
- **Error handling**: Adding logging and validation to transformations

## SQLScript vs Python: Choosing Your Tool

### Use SQLScript for Transformation Flows When:
- Working with structured, tabular data from relational sources
- Needing high performance for large volumes (1M+ rows)
- Implementing delta loads with watermark patterns
- Performing set-based operations (MERGE, aggregations, window functions)
- Operating in the SAP HANA native database
- Team expertise is SQL-focused

### Use Python for Data Flows When:
- Requiring complex business logic that's hard to express in SQL
- Integrating with ML libraries (scikit-learn, pandas, numpy)
- Handling unstructured data (text, JSON, images)
- Needing pandas-like data manipulation
- Working with multiple input sources in flexible ways
- Team expertise is Python-focused

## SQLScript Transformations for Transformation Flows

### Delta Handling with Watermarks

Watermarks track the last extracted value to enable incremental loads. Common watermark types:

```sql
-- Timestamp watermark pattern
PROCEDURE TF_LOAD_CUSTOMER_DELTA (
    IN iv_last_watermark TIMESTAMP
)
LANGUAGE SQLSCRIPT
AS
BEGIN
    -- Get current watermark (typically max of changed timestamp)
    DECLARE v_current_watermark TIMESTAMP = CURRENT_TIMESTAMP();

    -- Load only changed records
    UPSERT TARGET_CUSTOMER
    SELECT
        CUSTOMER_ID,
        CUSTOMER_NAME,
        REVENUE,
        UPDATED_AT,
        'ACTIVE' AS RECORD_STATUS
    FROM SOURCE_CUSTOMER
    WHERE UPDATED_AT > :iv_last_watermark
        AND UPDATED_AT <= :v_current_watermark;

    -- Update watermark in control table
    UPSERT WATERMARK_CONTROL
    VALUES ('CUSTOMER', :v_current_watermark);
END;
```

### MERGE Operations for Upserts

MERGE is the most efficient way to handle inserts and updates:

```sql
-- Standard MERGE pattern
MERGE INTO TARGET_PRODUCT tp
USING SOURCE_PRODUCT sp
    ON tp.PRODUCT_ID = sp.PRODUCT_ID
WHEN MATCHED AND sp.IS_DELETED = 'X' THEN
    DELETE
WHEN MATCHED THEN
    UPDATE SET
        tp.PRODUCT_NAME = sp.PRODUCT_NAME,
        tp.PRICE = sp.PRICE,
        tp.UPDATED_AT = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
    INSERT (
        PRODUCT_ID,
        PRODUCT_NAME,
        PRICE,
        CREATED_AT,
        UPDATED_AT
    )
    VALUES (
        sp.PRODUCT_ID,
        sp.PRODUCT_NAME,
        sp.PRICE,
        CURRENT_TIMESTAMP(),
        CURRENT_TIMESTAMP()
    );
```

### Window Functions for Analytics

Window functions enable efficient ranking, running totals, and partition-based calculations:

```sql
-- Rank products by revenue within each category
SELECT
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    REVENUE,
    ROW_NUMBER() OVER (
        PARTITION BY CATEGORY
        ORDER BY REVENUE DESC
    ) AS REVENUE_RANK,
    SUM(REVENUE) OVER (
        PARTITION BY CATEGORY
        ORDER BY MONTH_ID
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS ROLLING_3M_REVENUE
FROM PRODUCT_SALES;
```

### Common Table Expressions (CTEs) for Readability

CTEs make complex logic more maintainable:

```sql
WITH customer_revenue AS (
    SELECT
        CUSTOMER_ID,
        SUM(ORDER_AMOUNT) AS TOTAL_REVENUE,
        COUNT(DISTINCT ORDER_ID) AS ORDER_COUNT
    FROM ORDERS
    GROUP BY CUSTOMER_ID
),
customer_segments AS (
    SELECT
        CUSTOMER_ID,
        TOTAL_REVENUE,
        CASE
            WHEN TOTAL_REVENUE >= 100000 THEN 'GOLD'
            WHEN TOTAL_REVENUE >= 50000 THEN 'SILVER'
            ELSE 'BRONZE'
        END AS SEGMENT
    FROM customer_revenue
)
SELECT *
FROM customer_segments
ORDER BY TOTAL_REVENUE DESC;
```

## Python Operators for Data Flows

### Pandas-like Operations

Python operators work with pandas DataFrames for flexible transformations:

```python
import pandas as pd

def process_orders(orders_df):
    """
    Transform and enrich orders with customer segments
    """
    # Group by customer and calculate metrics
    customer_stats = orders_df.groupby('customer_id').agg({
        'order_amount': ['sum', 'mean', 'count'],
        'order_date': 'max'
    }).reset_index()

    customer_stats.columns = ['customer_id', 'total_revenue',
                              'avg_order_value', 'order_count', 'last_order_date']

    # Calculate customer segment
    customer_stats['segment'] = pd.cut(
        customer_stats['total_revenue'],
        bins=[0, 50000, 100000, float('inf')],
        labels=['BRONZE', 'SILVER', 'GOLD']
    )

    return customer_stats
```

### Multi-input Fusion

Python operators can merge multiple inputs flexibly:

```python
def enrich_orders(orders_df, customers_df, products_df):
    """
    Join orders with customer and product dimensions
    """
    enriched = orders_df.merge(
        customers_df[['customer_id', 'segment', 'region']],
        on='customer_id',
        how='left'
    ).merge(
        products_df[['product_id', 'category', 'margin']],
        on='product_id',
        how='left'
    )

    enriched['revenue_contribution'] = (
        enriched['order_amount'] * enriched['margin']
    )

    return enriched[enriched['order_date'] >= '2024-01-01']
```

### Custom Business Logic

Implement domain-specific rules that are cumbersome in SQL:

```python
def apply_discount_rules(orders_df, rules_df):
    """
    Apply complex tiered discount rules based on customer and product
    """
    def calculate_discount(row):
        applicable_rules = rules_df[
            (rules_df['segment'] == row['segment']) &
            (rules_df['category'] == row['category'])
        ]

        if applicable_rules.empty:
            return 0.0

        max_discount = applicable_rules['discount_rate'].max()
        return min(max_discount, row['order_amount'] * 0.15)

    orders_df['discount'] = orders_df.apply(calculate_discount, axis=1)
    orders_df['net_amount'] = orders_df['order_amount'] - orders_df['discount']

    return orders_df
```

## Common Transformation Patterns

### SCD Type 2: Slowly Changing Dimensions

Track historical changes to dimension attributes:

```sql
-- Initialize dimension with SCD Type 2 structure
CREATE TABLE DIM_CUSTOMER (
    CUSTOMER_SK BIGINT,
    CUSTOMER_ID STRING,
    CUSTOMER_NAME STRING,
    REGION STRING,
    EFFECTIVE_DATE DATE,
    END_DATE DATE,
    IS_CURRENT CHAR(1),
    PRIMARY KEY (CUSTOMER_SK)
);

-- Load new and changed dimensions
PROCEDURE LOAD_DIM_CUSTOMER_SCD2 (
    IN iv_load_date DATE
)
LANGUAGE SQLSCRIPT
AS
BEGIN
    -- Close expired records
    UPDATE DIM_CUSTOMER
    SET END_DATE = :iv_load_date,
        IS_CURRENT = 'N'
    WHERE IS_CURRENT = 'Y'
        AND CUSTOMER_ID IN (
            SELECT CUSTOMER_ID
            FROM SOURCE_CUSTOMER sc
            WHERE EXISTS (
                SELECT 1 FROM DIM_CUSTOMER dc
                WHERE dc.CUSTOMER_ID = sc.CUSTOMER_ID
                  AND (dc.REGION <> sc.REGION
                       OR dc.CUSTOMER_NAME <> sc.CUSTOMER_NAME)
            )
        );

    -- Insert new records and changed dimensions
    INSERT INTO DIM_CUSTOMER
    SELECT
        NEXT VALUE FOR DIM_CUSTOMER_SK_SEQ,
        CUSTOMER_ID,
        CUSTOMER_NAME,
        REGION,
        :iv_load_date,
        NULL,
        'Y'
    FROM SOURCE_CUSTOMER
    WHERE CUSTOMER_ID NOT IN (
        SELECT DISTINCT CUSTOMER_ID FROM DIM_CUSTOMER WHERE IS_CURRENT = 'Y'
    )
    UNION ALL
    SELECT
        NEXT VALUE FOR DIM_CUSTOMER_SK_SEQ,
        sc.CUSTOMER_ID,
        sc.CUSTOMER_NAME,
        sc.REGION,
        :iv_load_date,
        NULL,
        'Y'
    FROM SOURCE_CUSTOMER sc
    JOIN DIM_CUSTOMER dc ON sc.CUSTOMER_ID = dc.CUSTOMER_ID
    WHERE dc.IS_CURRENT = 'Y'
        AND (
            dc.REGION <> sc.REGION
            OR dc.CUSTOMER_NAME <> sc.CUSTOMER_NAME
        );
END;
```

### Deduplication Pattern

Remove duplicate records, keeping the most recent or best version:

```sql
-- Keep only the most recent version of each record
WITH ranked_records AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY SOURCE_ID
            ORDER BY LOAD_DATE DESC, RECORD_ID DESC
        ) AS RN
    FROM SOURCE_DATA
)
SELECT *
FROM ranked_records
WHERE RN = 1;
```

### Pivoting/Unpivoting

Convert between row and column formats:

```sql
-- Pivot: Months as columns
SELECT
    CUSTOMER_ID,
    SUM(CASE WHEN MONTH = 1 THEN AMOUNT ELSE 0 END) AS JAN,
    SUM(CASE WHEN MONTH = 2 THEN AMOUNT ELSE 0 END) AS FEB,
    SUM(CASE WHEN MONTH = 3 THEN AMOUNT ELSE 0 END) AS MAR
FROM MONTHLY_SALES
GROUP BY CUSTOMER_ID;

-- Unpivot: Months as rows (using UNION)
SELECT CUSTOMER_ID, 1 AS MONTH, JAN_SALES AS AMOUNT FROM CUSTOMER_MONTHLY_SALES
UNION ALL
SELECT CUSTOMER_ID, 2 AS MONTH, FEB_SALES AS AMOUNT FROM CUSTOMER_MONTHLY_SALES
UNION ALL
SELECT CUSTOMER_ID, 3 AS MONTH, MAR_SALES AS AMOUNT FROM CUSTOMER_MONTHLY_SALES;
```

### Date/Time Handling

Common date transformations for business requirements:

```sql
-- Fiscal period calculation
SELECT
    DATE_FIELD,
    EXTRACT(YEAR FROM DATE_FIELD) AS CAL_YEAR,
    EXTRACT(MONTH FROM DATE_FIELD) AS CAL_MONTH,
    WEEKDAY(DATE_FIELD) AS DAY_OF_WEEK,
    CAST(TO_DECIMAL(DATE_FORMAT(DATE_FIELD, 'YYYYMM'), 7, 0) AS INTEGER) AS YYYYMM,
    -- Fiscal calendar (starts April)
    CASE
        WHEN MONTH(DATE_FIELD) >= 4 THEN YEAR(DATE_FIELD)
        ELSE YEAR(DATE_FIELD) - 1
    END AS FISCAL_YEAR,
    CASE
        WHEN MONTH(DATE_FIELD) >= 4 THEN MONTH(DATE_FIELD) - 3
        ELSE MONTH(DATE_FIELD) + 9
    END AS FISCAL_MONTH
FROM TRANSACTIONS;
```

## Data Type Mapping

Map source types to target types correctly to prevent runtime errors:

| Source Type | Target Type | Notes |
|-----------|-----------|-------|
| Source VARCHAR(255) | VARCHAR(255) or TEXT | Map size appropriately |
| Source DECIMAL(15,2) | DECIMAL(19,4) or FLOAT | Allow room for calculations |
| Source DATE | DATE or TIMESTAMP | Timestamp if time needed |
| Source NUMERIC(10) | INTEGER or BIGINT | Use BIGINT for IDs |
| Source BOOLEAN/CHAR(1) | CHAR(1) or INTEGER | Use 'Y'/'N' or 0/1 consistently |
| Source JSON | STRING | Parse in Python operator |
| Source NULL | Not applicable | Must handle explicitly |

Use `execute_query` to test type conversions:

```sql
SELECT
    CAST('2024-01-15' AS DATE) AS converted_date,
    CAST('123.45' AS DECIMAL(10,2)) AS converted_amount,
    CASE WHEN source_value IS NULL THEN 0 ELSE source_value END AS handled_null
FROM source_table LIMIT 10;
```

## Error Handling and Logging

Implement robust error handling in transformations:

### SQLScript Error Handling

```sql
PROCEDURE TRANSFORM_WITH_ERROR_HANDLING (
    IN iv_batch_id STRING
)
LANGUAGE SQLSCRIPT
WITH RESULT VIEW vv_load_result
AS
BEGIN
    DECLARE v_row_count INT;
    DECLARE v_error_message STRING;

    -- Create result logging table if needed
    CREATE LOCAL TEMPORARY TABLE lt_log (
        BATCH_ID STRING,
        OPERATION STRING,
        ROWS_AFFECTED INT,
        ERROR_FLAG CHAR(1),
        ERROR_MESSAGE STRING,
        TIMESTAMP TIMESTAMP
    );

    -- Wrap main operation in exception handler
    CALL DBMS_OUTPUT.PUT_LINE('Starting batch: ' || :iv_batch_id);

    BEGIN
        INSERT INTO TARGET_TABLE
        SELECT * FROM SOURCE_TABLE
        WHERE BATCH_ID = :iv_batch_id
            AND STATUS = 'VALID';

        v_row_count := ROWCOUNT;

        INSERT INTO lt_log VALUES (
            :iv_batch_id,
            'INSERT',
            :v_row_count,
            'N',
            NULL,
            CURRENT_TIMESTAMP()
        );

    EXCEPTION WHEN SQL_ERROR_CODE THEN
        v_error_message := CURRENT_TIMESTAMP() || ' - Error Code: ' ||
                          ::SQL_ERROR_CODE || ', Message: ' || ::SQL_ERROR_MESSAGE;

        INSERT INTO lt_log VALUES (
            :iv_batch_id,
            'INSERT',
            0,
            'Y',
            :v_error_message,
            CURRENT_TIMESTAMP()
        );
    END;

    -- Return log results
    vv_load_result = SELECT * FROM lt_log;
END;
```

### Python Operator Logging

```python
import logging
from datetime import datetime

def transform_with_logging(input_df):
    """
    Transform with comprehensive logging
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Processing {len(input_df)} input rows at {datetime.now()}")

    try:
        # Data validation
        if input_df.isnull().sum().sum() > 0:
            logger.warning(f"Found nulls: {input_df.isnull().sum().to_dict()}")
            input_df = input_df.fillna(0)

        # Transformation
        output_df = input_df.assign(
            processed_amount=input_df['amount'] * 1.1,
            processed_date=pd.to_datetime(input_df['date'])
        )

        logger.info(f"Successfully processed {len(output_df)} rows")
        return output_df

    except Exception as e:
        logger.error(f"Transformation failed: {str(e)}", exc_info=True)
        raise ValueError(f"Transformation error: {str(e)}")
```

## Testing Transformations

### Using execute_query for SQLScript Testing

Test your SQL logic incrementally before deploying:

```sql
-- Test 1: Data quality checks
EXECUTE QUERY '
SELECT
    COUNT(*) as total_rows,
    COUNT(DISTINCT customer_id) as distinct_customers,
    SUM(CASE WHEN amount < 0 THEN 1 ELSE 0 END) as negative_amounts
FROM source_orders
WHERE load_date = CURRENT_DATE
';

-- Test 2: Transformation validation
EXECUTE QUERY '
SELECT
    segment,
    COUNT(*) as count,
    AVG(revenue) as avg_revenue,
    MIN(revenue) as min_revenue,
    MAX(revenue) as max_revenue
FROM transformed_customers
GROUP BY segment
';

-- Test 3: Delta logic verification
EXECUTE QUERY '
SELECT
    operation,
    COUNT(*) as count
FROM (
    SELECT CASE
        WHEN old_value IS NULL THEN "INSERT"
        WHEN new_value IS NULL THEN "DELETE"
        ELSE "UPDATE"
    END as operation
    FROM merge_changes
)
GROUP BY operation
';
```

### Using smart_query for Intelligent Analysis

Let the system identify anomalies and patterns:

```
smart_query(
    dataset="transformed_customers",
    question="Are there any unexpected patterns or anomalies in the revenue by segment?"
)

smart_query(
    dataset="delta_loads",
    question="Is the distribution of inserted vs updated records normal for this load?"
)
```

## Performance Considerations for Large Datasets

### Indexing Strategy

```sql
-- Create indexes on join keys and filter conditions
CREATE INDEX IDX_ORDER_CUSTOMER ON ORDERS (CUSTOMER_ID);
CREATE INDEX IDX_PRODUCT_CATEGORY ON PRODUCTS (CATEGORY_ID);
CREATE INDEX IDX_DATE_PARTITION ON FACT_SALES (LOAD_DATE, CUSTOMER_ID);
```

### Partitioning for Scalability

```sql
-- Partition by month for faster filtering
CREATE TABLE FACT_SALES (
    TRANSACTION_ID BIGINT,
    CUSTOMER_ID INT,
    AMOUNT DECIMAL(15,2),
    TRANSACTION_DATE DATE,
    PRIMARY KEY (TRANSACTION_ID)
)
PARTITION BY RANGE (EXTRACT(YEAR_MONTH FROM TRANSACTION_DATE))
(
    PARTITION '202401' <= VALUES < '202402',
    PARTITION '202402' <= VALUES < '202403'
);
```

### Query Optimization

```sql
-- Use LIMIT for initial testing
SELECT * FROM large_table LIMIT 1000;

-- Filter early and often
SELECT *
FROM fact_table
WHERE load_date = CURRENT_DATE      -- Filter first
    AND customer_id IN (SELECT id FROM active_customers)
    AND amount > 0;

-- Aggregate before joining
SELECT
    c.customer_id,
    c.name,
    agg.total_revenue
FROM customers c
JOIN (
    SELECT customer_id, SUM(amount) as total_revenue
    FROM orders
    WHERE load_date >= CURRENT_DATE - 30
    GROUP BY customer_id
) agg ON c.customer_id = agg.customer_id;
```

### Memory Management in Python

```python
def process_large_file_chunked(input_df, chunk_size=10000):
    """
    Process large data in chunks to avoid memory issues
    """
    result_chunks = []

    for i in range(0, len(input_df), chunk_size):
        chunk = input_df.iloc[i:i + chunk_size]

        # Process chunk
        processed_chunk = chunk.assign(
            processed_value=chunk['value'] * 1.1
        )

        result_chunks.append(processed_chunk)

        # Explicitly free memory
        del chunk

    return pd.concat(result_chunks, ignore_index=True)
```

## MCP Tool References

### execute_query
Run and test SQL queries in your transformations. Use for validation and testing logic before deploying.

```
execute_query(
    query="SELECT * FROM source_table WHERE load_date = CURRENT_DATE LIMIT 100"
)
```

### smart_query
Ask intelligent questions about your data to identify patterns, anomalies, and quality issues.

```
smart_query(
    dataset="transformed_data",
    question="What are the top 5 anomalies in this dataset?"
)
```

### get_table_schema
Understand the structure of source and target tables before writing transformations.

```
get_table_schema(table_name="SOURCE_CUSTOMER")
```

### get_object_definition
View the complete definition of a Transformation Flow or Data Flow object.

```
get_object_definition(object_id="TF_CUSTOMER_TRANSFORM")
```

### analyze_column_distribution
Analyze data distribution to identify outliers and inform transformation logic.

```
analyze_column_distribution(
    table_name="CUSTOMER_REVENUE",
    column_name="ANNUAL_REVENUE"
)
```

## Next Steps

1. Identify your source and target structures using `get_table_schema`
2. Choose SQLScript for set-based operations or Python for custom logic
3. Draft your transformation logic using provided patterns
4. Test with `execute_query` or `smart_query` on sample data
5. Validate data types and mappings
6. Deploy to Transformation Flow or Data Flow
7. Monitor performance and adjust as needed

