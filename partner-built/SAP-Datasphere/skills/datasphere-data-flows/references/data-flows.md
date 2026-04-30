# Data Flows Reference Guide

## Overview

Data Flows are SAP Datasphere's batch ETL tool for complex transformations. They support graphical data transformation with operators including a Python operator for custom logic.

> **SAP Recommendation:** "Replication and Transformation Flows are now the recommended approach for loading and transforming data in SAP Datasphere. Data Flows will continue to be supported for existing workflows."

## Key Characteristics

| Characteristic | Value |
|---------------|-------|
| Execution Mode | **Batch only** |
| Delta Support | **No** (full load only) |
| CDC Support | **No** |
| Custom Code | Python operator available |
| Use Case | Complex transformations, aggregations |

## Data Flow Editor UI

### Toolbar Structure

**General Section:**
- Save icon
- Undo/Redo icons
- Deploy icon

**View Section:**
- View toggle buttons

**Edit Section:**
- Standard edit operations

**Tools Section:**
- Additional utilities

### Operators Toolbar Icons (left to right)
1. **Table** - Add source or target table
2. **Join** - Combine two data sources
3. **Projection** - Select/transform columns
4. **Aggregation** - GROUP BY operations
5. **Script** - Python custom code
6. **Filter** - Row filtering

### Canvas Node Elements
- **Source nodes:** Blue with grid icon, shows column count
- **Operator nodes:** Blue with operator-specific icon
- **Target nodes:** Blue with "Target" label, shows "New" if creating new table
- **Connection ports:** Circles on node edges for linking
- **Error badges:** Red indicators for validation issues

## CRITICAL CONSTRAINT

**Data Flows are BATCH ONLY** - They do NOT support:
- Delta/incremental loading
- Change Data Capture (CDC)
- Real-time processing

For delta requirements, use **Transformation Flows** instead.

## Operators

### Source Operators
- Table (local tables, views)
- SQL (custom SQL statements)

### Transformation Operators
- **Join** - Inner, left, right, full outer joins
- **Union** - Combine multiple sources
- **Filter** - Row-level filtering
- **Projection** - Column selection and renaming
- **Aggregation** - GROUP BY with SUM, COUNT, AVG, MIN, MAX
- **Script (Python)** - Custom Python transformations

### Target Operators
- Table (local tables)

## Python Operator

The Python operator enables custom transformation logic:

```python
# Example: Custom data cleansing
def transform(data):
    # data is a pandas DataFrame
    data['column'] = data['column'].str.upper()
    return data
```

**Capabilities**:
- Pandas DataFrame operations
- Custom business logic
- Data quality checks
- Complex calculations

**Limitations**:
- Performance overhead for large datasets
- No external library imports
- Memory constraints

## Navigation

**Access**: Data Builder → Data Flows

**Create**: Data Builder → New Data Flow → Drag operators → Connect sources to targets

## Execution

Data Flows can be:
- Run manually from Data Builder
- Scheduled via Task Chains
- Triggered by external events

## When to Use Data Flows

**Use Data Flows when**:
- Complex transformations are needed
- Python/custom logic is required
- Full refresh is acceptable
- One-time or batch processing

**Do NOT use Data Flows when**:
- Delta/CDC is required → Use Transformation Flows
- Simple 1:1 replication → Use Replication Flows
- Real-time processing needed → Use Replication Flows with CDC

## Best Practices

1. **Minimize Python Usage** - Use built-in operators when possible
2. **Filter Early** - Apply filters before joins to reduce data volume
3. **Test with Sample Data** - Validate logic before full runs
4. **Monitor Performance** - Check execution times in Data Integration Monitor
5. **Document Logic** - Add descriptions to operators for maintainability
