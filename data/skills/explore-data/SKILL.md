---
name: explore-data
description: Profile and explore a dataset to understand its shape, quality, and patterns. Use when encountering a new table or file, checking null rates and column distributions, spotting data quality issues like duplicates or suspicious values, or deciding which dimensions and metrics to analyze.
argument-hint: "<table or file>"
---

# /explore-data - Profile and Explore a Dataset

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Generate a comprehensive data profile for a table or uploaded file. Understand its shape, quality, and patterns before diving into analysis.

## Usage

```
/explore-data <table_name or file>
```

## Workflow

### 1. Access the Data

**If a data warehouse MCP server is connected:**

1. Resolve the table name (handle schema prefixes, suggest matches if ambiguous)
2. Query table metadata: column names, types, descriptions if available
3. Run profiling queries against the live data

**If a file is provided (CSV, Excel, Parquet, JSON):**

1. Read the file and load into a working dataset
2. Infer column types from the data

**If neither:**

1. Ask the user to provide a table name (with their warehouse connected) or upload a file
2. If they describe a table schema, provide guidance on what profiling queries to run

### 2. Understand Structure

Before analyzing any data, understand its structure:

**Table-level questions:**
- How many rows and columns?
- What is the grain (one row per what)?
- What is the primary key? Is it unique?
- When was the data last updated?
- How far back does the data go?

**Column classification** — categorize each column as one of:
- **Identifier**: Unique keys, foreign keys, entity IDs
- **Dimension**: Categorical attributes for grouping/filtering (status, type, region, category)
- **Metric**: Quantitative values for measurement (revenue, count, duration, score)
- **Temporal**: Dates and timestamps (created_at, updated_at, event_date)
- **Text**: Free-form text fields (description, notes, name)
- **Boolean**: True/false flags
- **Structural**: JSON, arrays, nested structures

### 3. Generate Data Profile

Run the following profiling checks:

**Table-level metrics:**
- Total row count
- Column count and types breakdown
- Approximate table size (if available from metadata)
- Date range coverage (min/max of date columns)

**All columns:**
- Null count and null rate
- Distinct count and cardinality ratio (distinct / total)
- Most common values (top 5-10 with frequencies)
- Least common values (bottom 5 to spot anomalies)

**Numeric columns (metrics):**
```
min, max, mean, median (p50)
standard deviation
percentiles: p1, p5, p25, p75, p95, p99
zero count
negative count (if unexpected)
```

**String columns (dimensions, text):**
```
min length, max length, avg length
empty string count
pattern analysis (do values follow a format?)
case consistency (all upper, all lower, mixed?)
leading/trailing whitespace count
```

**Date/timestamp columns:**
```
min date, max date
null dates
future dates (if unexpected)
distribution by month/week
gaps in time series
```

**Boolean columns:**
```
true count, false count, null count
true rate
```

**Present the profile as a clean summary table**, grouped by column type (dimensions, metrics, dates, IDs).

### 4. Identify Data Quality Issues

Apply the quality assessment framework below. Flag potential problems:

- **High null rates**: Columns with >5% nulls (warn), >20% nulls (alert)
- **Low cardinality surprises**: Columns that should be high-cardinality but aren't (e.g., a "user_id" with only 50 distinct values)
- **High cardinality surprises**: Columns that should be categorical but have too many distinct values
- **Suspicious values**: Negative amounts where only positive expected, future dates in historical data, obviously placeholder values (e.g., "N/A", "TBD", "test", "999999")
- **Duplicate detection**: Check if there's a natural key and whether it has duplicates
- **Distribution skew**: Extremely skewed numeric distributions that could affect averages
- **Encoding issues**: Mixed case in categorical fields, trailing whitespace, inconsistent formats

### 5. Discover Relationships and Patterns

After profiling individual columns:

- **Foreign key candidates**: ID columns that might link to other tables
- **Hierarchies**: Columns that form natural drill-down paths (country > state > city)
- **Correlations**: Numeric columns that move together
- **Derived columns**: Columns that appear to be computed from others
- **Redundant columns**: Columns with identical or near-identical information

### 6. Suggest Interesting Dimensions and Metrics

Based on the column profile, recommend:

- **Best dimension columns** for slicing data (categorical columns with reasonable cardinality, 3-50 values)
- **Key metric columns** for measurement (numeric columns with meaningful distributions)
- **Time columns** suitable for trend analysis
- **Natural groupings** or hierarchies apparent in the data
- **Potential join keys** linking to other tables (ID columns, foreign keys)

### 7. Recommend Follow-Up Analyses

Suggest 3-5 specific analyses the user could run next:

- "Trend analysis on [metric] by [time_column] grouped by [dimension]"
- "Distribution deep-dive on [skewed_column] to understand outliers"
- "Data quality investigation on [problematic_column]"
- "Correlation analysis between [metric_a] and [metric_b]"
- "Cohort analysis using [date_column] and [status_column]"

## Output Format

```
## Data Profile: [table_name]

### Overview
- Rows: 2,340,891
- Columns: 23 (8 dimensions, 6 metrics, 4 dates, 5 IDs)
- Date range: 2021-03-15 to 2024-01-22

### Column Details
[summary table]

### Data Quality Issues
[flagged issues with severity]

### Recommended Explorations
[numbered list of suggested follow-up analyses]
```

---

## Quality Assessment Framework

### Completeness Score

Rate each column:
- **Complete** (>99% non-null): Green
- **Mostly complete** (95-99%): Yellow -- investigate the nulls
- **Incomplete** (80-95%): Orange -- understand why and whether it matters
- **Sparse** (<80%): Red -- may not be usable without imputation

### Consistency Checks

Look for:
- **Value format inconsistency**: Same concept represented differently ("USA", "US", "United States", "us")
- **Type inconsistency**: Numbers stored as strings, dates in various formats
- **Referential integrity**: Foreign keys that don't match any parent record
- **Business rule violations**: Negative quantities, end dates before start dates, percentages > 100
- **Cross-column consistency**: Status = "completed" but completed_at is null

### Accuracy Indicators

Red flags that suggest accuracy issues:
- **Placeholder values**: 0, -1, 999999, "N/A", "TBD", "test", "xxx"
- **Default values**: Suspiciously high frequency of a single value
- **Stale data**: Updated_at shows no recent changes in an active system
- **Impossible values**: Ages > 150, dates in the far future, negative durations
- **Round number bias**: All values ending in 0 or 5 (suggests estimation, not measurement)

### Timeliness Assessment

- When was the table last updated?
- What is the expected update frequency?
- Is there a lag between event time and load time?
- Are there gaps in the time series?

## Pattern Discovery Techniques

### Distribution Analysis

For numeric columns, characterize the distribution:
- **Normal**: Mean and median are close, bell-shaped
- **Skewed right**: Long tail of high values (common for revenue, session duration)
- **Skewed left**: Long tail of low values (less common)
- **Bimodal**: Two peaks (suggests two distinct populations)
- **Power law**: Few very large values, many small ones (common for user activity)
- **Uniform**: Roughly equal frequency across range (often synthetic or random)

### Temporal Patterns

For time series data, look for:
- **Trend**: Sustained upward or downward movement
- **Seasonality**: Repeating patterns (weekly, monthly, quarterly, annual)
- **Day-of-week effects**: Weekday vs. weekend differences
- **Holiday effects**: Drops or spikes around known holidays
- **Change points**: Sudden shifts in level or trend
- **Anomalies**: Individual data points that break the pattern

### Segmentation Discovery

Identify natural segments by:
- Finding categorical columns with 3-20 distinct values
- Comparing metric distributions across segment values
- Looking for segments with significantly different behavior
- Testing whether segments are homogeneous or contain sub-segments

### Correlation Exploration

Between numeric columns:
- Compute correlation matrix for all metric pairs
- Flag strong correlations (|r| > 0.7) for investigation
- Note: Correlation does not imply causation -- flag this explicitly
- Check for non-linear relationships (e.g., quadratic, logarithmic)

## Schema Understanding and Documentation

### Schema Documentation Template

When documenting a dataset for team use:

```markdown
## Table: [schema.table_name]

**Description**: [What this table represents]
**Grain**: [One row per...]
**Primary Key**: [column(s)]
**Row Count**: [approximate, with date]
**Update Frequency**: [real-time / hourly / daily / weekly]
**Owner**: [team or person responsible]

### Key Columns

| Column | Type | Description | Example Values | Notes |
|--------|------|-------------|----------------|-------|
| user_id | STRING | Unique user identifier | "usr_abc123" | FK to users.id |
| event_type | STRING | Type of event | "click", "view", "purchase" | 15 distinct values |
| revenue | DECIMAL | Transaction revenue in USD | 29.99, 149.00 | Null for non-purchase events |
| created_at | TIMESTAMP | When the event occurred | 2024-01-15 14:23:01 | Partitioned on this column |

### Relationships
- Joins to `users` on `user_id`
- Joins to `products` on `product_id`
- Parent of `event_details` (1:many on event_id)

### Known Issues
- [List any known data quality issues]
- [Note any gotchas for analysts]

### Common Query Patterns
- [Typical use cases for this table]
```

### Schema Exploration Queries

When connected to a data warehouse, use these patterns to discover schema:

```sql
-- List all tables in a schema (PostgreSQL)
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Column details (PostgreSQL)
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'my_table'
ORDER BY ordinal_position;

-- Table sizes (PostgreSQL)
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Row counts for all tables (general pattern)
-- Run per-table: SELECT COUNT(*) FROM table_name
```

### Lineage and Dependencies

When exploring an unfamiliar data environment:

1. Start with the "output" tables (what reports or dashboards consume)
2. Trace upstream: What tables feed into them?
3. Identify raw/staging/mart layers
4. Map the transformation chain from raw data to analytical tables
5. Note where data is enriched, filtered, or aggregated

## Tips

- For very large tables (100M+ rows), profiling queries use sampling by default -- mention if you need exact counts
- If exploring a new dataset for the first time, this command gives you the lay of the land before writing specific queries
- The quality flags are heuristic -- not every flag is a real problem, but each is worth a quick look
