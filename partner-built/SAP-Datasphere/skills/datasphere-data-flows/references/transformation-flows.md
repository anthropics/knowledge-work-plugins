# Transformation Flows Reference

## Delta Staging Architecture

### Multi-Layer Pattern
```
[Source System]
      ↓ (Replication Flow)
[Raw Layer - Delta Table]
      ↓ (Transformation Flow)
[Cleansed Layer - Delta Table]
      ↓ (Transformation Flow)
[Curated Layer - Delta Table]
      ↓ (View)
[Consumption Layer]
```

### Delta Operations
| Operation | Symbol | Behavior |
|-----------|--------|----------|
| INSERT | I | New record created |
| UPDATE | U | Existing record modified |
| DELETE | D | Record marked for deletion |

## Prerequisites

### Source Table Requirements
- Must be a Local Table
- Must have **Delta Capture** enabled
- Contains delta records from Replication Flow

### Target Table Requirements
- Must be a Local Table
- Must have **Delta Capture** enabled
- Schema compatible with source + transformations

## SQL Transformations

### Supported Operations
```sql
-- Projections
SELECT column1, column2 FROM source

-- Filters
SELECT * FROM source WHERE status = 'ACTIVE'

-- Calculations
SELECT amount * quantity AS total FROM source

-- CASE statements
SELECT
  CASE WHEN amount > 1000 THEN 'HIGH' ELSE 'LOW' END AS priority
FROM source

-- Date functions
SELECT
  YEAR(created_date) AS year,
  MONTH(created_date) AS month
FROM source
```

### Limitations
- No complex multi-table joins (use Data Flow instead)
- No Python scripting
- Limited to SQL syntax

## Execution Modes

### Run on Delta
- Processes only changed records since last run
- Most efficient for incremental processing
- Maintains delta log for downstream flows

### Run Full
- Processes all records
- Use after schema changes
- Resets delta state

## Best Practices

### Naming Convention
```
TF_<SourceLayer>_TO_<TargetLayer>_<Description>
Example: TF_RAW_TO_CLEANSED_SALES
```

### Error Handling
- Monitor for failed delta propagation
- Check data type compatibility
- Validate NULL handling

### Performance
- Filter early in the pipeline
- Minimize transformations per flow
- Use appropriate scheduling frequency
