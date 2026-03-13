---
name: View Architect
description: "Expert guide for designing Graphical and SQL Views in SAP Datasphere's Data Builder. Use this when you need to create views, define semantic models, set up associations, configure data access controls, or optimize view performance. Essential for building semantic layers, implementing star schemas, and preparing data for analytics."
---

# View Architect Skill

## Overview

The View Architect skill guides you through creating and designing views in SAP Datasphere's Data Builder. Views are fundamental semantic objects that organize raw data into meaningful business concepts. Whether you're building a graphical view through the intuitive UI or writing custom SQL, this skill covers the complete workflow from source selection through deployment and optimization.

## When to Use This Skill

- Creating new Graphical or SQL Views
- Designing semantic data models (Fact, Dimension, Hierarchy tables)
- Setting up associations between entities
- Implementing complex business logic through calculated columns and filters
- Configuring data access controls and security
- Optimizing view performance and push-down behavior
- Deploying views to development and production environments

## Graphical Views vs SQL Views

### Graphical Views
**When to use:**
- Building views through visual, drag-and-drop interface
- Team members need low-code/no-code approach
- Rapid prototyping and iteration
- Complex join logic with multiple tables
- Need version control and change tracking built-in

**Advantages:**
- Visual representation of logic
- Built-in validation and constraint checking
- Easier maintenance and documentation
- Collaborative design capabilities
- Automatic dependency tracking

**Limitations:**
- Cannot express certain complex SQL patterns
- May have slight performance overhead compared to hand-optimized SQL
- Limited to Datasphere's graphical expression capabilities

### SQL Views
**When to use:**
- Implementing complex analytical logic
- Requiring specific SQL functions or window operations
- Performance-critical transformations
- Migrating from existing SQL systems
- Need for advanced SQL patterns (CTEs, recursive queries, etc.)

**Advantages:**
- Maximum flexibility and control
- Hand-optimized for performance
- Access to all SQL functions available in SAP HANA
- Familiar to SQL developers
- Direct control over execution plans

**Limitations:**
- Requires SQL expertise
- Harder to maintain without proper documentation
- Less visual feedback during design
- Version control less integrated

## Semantic Usage Types

Semantic usage defines how Datasphere interprets and uses your view data. Choosing the correct semantic usage is crucial for reporting, aggregation, and filtering behavior.

### Fact
**Use when:** Your view represents transactional data, events, or measurements that you want to aggregate and analyze across dimensions.

**Characteristics:**
- Contains quantitative measures (amounts, counts, durations)
- Typically has grain at the transaction or event level
- Often used as the source for Analytic Models
- Supports multiple measures and aggregation rules
- Can reference multiple dimensions through associations

**Example:** Sales transactions (Order ID, Amount, Date, Quantity)

### Dimension
**Use when:** Your view represents descriptive attributes that provide context to facts.

**Characteristics:**
- Contains hierarchical or categorical data
- Typically slower-changing than fact data
- Used to filter, group, and drill down in analytics
- Should have a unique key (business key)
- Often associated with text entities for translations

**Example:** Product catalog (Product ID, Category, Subcategory, Supplier)

### Text
**Use when:** Your view contains multi-language descriptions or attributes for other entities.

**Characteristics:**
- Supports language-specific text and descriptions
- Associated with a main entity (Dimension or Fact)
- Language key and text element key structure
- Used for translation and localization

**Example:** Product descriptions in English, German, French

### Hierarchy
**Use when:** Your view defines parent-child relationships for drill-down and roll-up analysis.

**Characteristics:**
- Represents hierarchical structures (Organization charts, Product hierarchies)
- Contains hierarchy key, parent key, and order fields
- Supports multiple hierarchies in a single entity
- Used for drill-down/roll-up in SAC and reporting tools

**Example:** Organizational structure (Manager ID, Employee ID, Level)

### Relational Dataset
**Use when:** Your view is purely for data distribution, data integration, or non-analytical purposes.

**Characteristics:**
- Not used for analytical aggregation
- Used for operational reporting or data export
- Cannot be the source of an Analytic Model
- Useful for intermediate transformations
- Supports full-outer-join semantics

**Example:** Transaction audit log, data export view

## View Creation Workflow

### Step 1: Select Source Tables
Start by identifying which source tables contain the data you need.

**Best practices:**
- Use the Data Catalog to understand table structures: `search_catalog` with table keywords
- Retrieve detailed schema information: `get_table_schema` for your source tables
- Document your source dependencies
- Consider whether you're building on raw data or existing views
- Verify data quality and completeness of source tables

### Step 2: Define Joins
Create relationships between source tables using appropriate join types.

**Join types:**

- **INNER JOIN:** Returns rows matching in both tables. Use when you want only matched records (e.g., Orders with Customers).
- **LEFT OUTER JOIN:** Returns all rows from left table + matched rows from right. Use when left table is primary (e.g., All Customers and their Orders, if any).
- **RIGHT OUTER JOIN:** Returns all rows from right table + matched rows from left. Use when right table is primary.
- **FULL OUTER JOIN:** Returns all rows from both tables. Use when you need all records from both sources (e.g., reconciliation).
- **CROSS JOIN:** Cartesian product of both tables. Use cautiously; creates many rows. Example: creating combinations of dimensions.

**Join strategy best practices:**
- Join on business keys (unique identifiers) when possible
- Avoid joining on descriptive fields
- Consider join cardinality (1:1, 1:N, N:N)
- N:N joins can create data explosion; validate results
- Filter early to reduce join volume
- Document join logic in calculated columns

### Step 3: Configure Projections
Select which columns to include and exclude from the view.

**Best practices:**
- Include only columns needed downstream
- Remove redundant columns (avoid duplicate keys from joined tables)
- Rename columns for clarity (Customer ID → CustomerID)
- Consider column ordering for readability
- Mark key columns appropriately
- Use semantic naming conventions

### Step 4: Add Calculated Columns
Create derived fields using expressions.

**Expression syntax examples:**
- **String concatenation:** `"Company: " || COMPANY_NAME`
- **Conditional logic:** `CASE WHEN AMOUNT > 1000 THEN 'Large' ELSE 'Small' END`
- **Date calculations:** `DATEDIFF(day, ORDER_DATE, DELIVERY_DATE)`
- **Aggregations (window functions):** `SUM(AMOUNT) OVER (PARTITION BY CUSTOMER_ID ORDER BY DATE)`
- **String functions:** `UPPER(PRODUCT_NAME)`, `SUBSTRING(CODE, 1, 3)`
- **Numeric functions:** `ROUND(PRICE, 2)`, `ABS(VARIANCE)`

**Calculated column best practices:**
- Use meaningful aliases
- Document complex formulas
- Test expressions with `execute_query` before deployment
- Avoid overly complex nested expressions; break into multiple columns
- Consider performance impact of calculations on large datasets

### Step 5: Add Filters
Define row-level filters to exclude unwanted data.

**Filter expression examples:**
- **Simple comparison:** `STATUS = 'ACTIVE'`
- **Date ranges:** `INVOICE_DATE >= '2024-01-01' AND INVOICE_DATE < '2024-02-01'`
- **IN lists:** `COUNTRY IN ('USA', 'Canada', 'Mexico')`
- **Null checks:** `CUSTOMER_EMAIL IS NOT NULL`
- **Complex logic:** `(STATUS = 'ACTIVE' AND AMOUNT > 0) OR (STATUS = 'ARCHIVED' AND APPROVAL_DATE > '2023-01-01')`

**Filter best practices:**
- Apply filters at the view level to prevent duplicate filtering logic
- Use meaningful filter names and descriptions
- Consider whether filters should be static (always applied) or dynamic (parameterized)
- Test filter performance on large datasets
- Document business logic behind filters

## Associations

Associations define relationships between entities without creating joins at the view level. They enable navigation and filtering in SAC and other analytics tools.

### Creating Associations

**Association types:**

- **To-One Association:** Links to a single dimension record. Example: Order → Customer (many orders to one customer)
- **To-Many Association:** Links to multiple records. Less common; use for navigational purposes

**Association setup:**
1. Define the foreign key (your view's column)
2. Define the target entity and its primary key
3. Set cardinality (1:1, N:1, 1:N)
4. Optionally set as "primary" for default navigation
5. Add descriptive label and documentation

**Association best practices:**
- Create associations to Dimension and Text entities
- Limit to business-meaningful relationships
- Avoid circular associations
- Document navigation paths for users
- Use consistent naming conventions (e.g., "To_Customer", "To_Date")

### Managed Associations vs Direct References
- **Managed associations:** Defined in the view, tracked in metadata
- **Direct references:** Column-based references without formal association

Use managed associations for navigational clarity and to enable SAC drill-down.

## Input Parameters and Data Access Controls

### Input Parameters
Add dynamic parameters to views for flexible filtering and analysis.

**Parameter types:**
- **Prompt (Single Value):** Users select one value before executing the view
- **Prompt (Multiple Values):** Users can select multiple values
- **Range:** Users define a start and end value (e.g., date range)
- **Variable:** Parametrized column value for runtime substitution

**Parameter usage example:**
```
INVOICE_DATE >= :StartDate AND INVOICE_DATE <= :EndDate
WHERE REGION = :SelectedRegion
```

**Input parameter best practices:**
- Provide meaningful default values
- Add descriptions and help text for end users
- Consider mandatory vs optional parameters
- Validate parameter ranges (e.g., EndDate > StartDate)
- Document which parameters are required for queries

### Data Access Controls (DAC)
Implement row-level security to restrict data based on user attributes.

**DAC setup:**
1. Define a Principal Hierarchy (user groups, departments, regions)
2. Create privilege assignments mapping users to hierarchy levels
3. Apply DAC filters at the view level

**DAC expression example:**
```
REGION IN (SELECT region FROM user_region_mapping WHERE user_id = CURRENT_USER)
```

**DAC best practices:**
- Align with organizational structure
- Review and audit access regularly
- Test with sample users to verify restrictions
- Document security policies in view descriptions
- Avoid hardcoding user-specific logic; use system variables

## Persistence Strategies

### Virtual Views
**When to use:**
- Data is frequently updated in source tables
- You need minimal storage overhead
- Underlying data changes daily/hourly
- Query latency is acceptable (seconds range)
- Data volume is moderate

**Characteristics:**
- No physical storage of view data
- Always reflects latest source data
- Query executed on-demand
- Lower storage costs
- Longer query times (joins and transformations happen at query time)

### Persisted Views
**When to use:**
- Data changes less frequently (daily or weekly)
- You need sub-second query performance
- Data volume is large and queries are heavy
- Multiple downstream views consume this view
- Aggregated or summarized data

**Characteristics:**
- Data physically stored in SAP HANA
- Refreshed on schedule (hourly, daily, etc.)
- Fast query performance
- Higher storage consumption
- Slightly stale data (between refresh intervals)
- Can be source for other persisted views

### Hybrid Approach
Persist heavily-used aggregates while virtualizing granular data:
```
Raw transactions (virtual)
  ↓ (source)
Daily summaries by customer (persisted, refreshed nightly)
  ↓ (source)
Monthly KPI reports (persisted, refreshed monthly)
```

## Performance Best Practices

### Push-Down Optimization
Enable Datasphere to push filters and projections down to the source database.

**Optimization rules:**
- Use columns from underlying tables directly when possible
- Place filters that operate on source columns at the view level
- Avoid complex calculated columns that prevent push-down
- Test execution plans to verify push-down behavior
- Use `execute_query` to analyze query performance

**Non-push-down scenarios:**
- Complex string manipulation
- Calculations requiring multiple source rows (window functions)
- Union operations
- Calculated columns combining multiple tables

### Avoiding Unnecessary Columns
- Include only columns needed by downstream objects
- Remove columns used only in intermediate joins
- Reduces memory and I/O
- Simplifies metadata for end users
- Speeds up view compilation

### Join Strategy Optimization
- Join dimension tables (small) after fact tables (large)
- Apply row filters before joins when possible
- Use inner joins where applicable (reduces rows)
- Monitor join cardinality; avoid N:N situations
- Consider materialization of intermediate steps

### Column Order and Indexing
- Place frequently filtered columns early in selection
- Logical grouping (keys, measures, attributes)
- No direct indexing control in views, but impacts source query

### Aggregation and Deduplication
- Use COUNT(DISTINCT column) carefully on large datasets
- Consider materializing lookups to avoid repeated joins
- Use aggregation functions efficiently (GROUP BY on necessary columns only)
- Test performance with realistic data volumes

## Deployment Workflow

### Pre-Deployment Validation
1. **Schema validation:** Run `get_table_schema` on all sources to confirm structure
2. **Query testing:** Use `execute_query` to test view with sample data
3. **Dependency review:** Use `get_object_definition` to check downstream dependencies
4. **Performance testing:** Analyze query time and execution plan
5. **Data validation:** Verify row counts and data ranges match expectations

### Deployment Steps
1. Save view and resolve any validation errors
2. Deploy to development environment for testing
3. Test with end users if applicable
4. Deploy to production environment
5. Monitor view execution performance
6. Document in change management system

### Post-Deployment
- Monitor query performance in production
- Collect metrics on refresh times (if persisted)
- Gather user feedback
- Adjust filters, associations, or persistence as needed
- Update documentation

## MCP Tools Reference

### get_table_schema
Retrieve detailed information about source table structure, data types, and constraints.
```
Use to understand available columns and their properties before designing joins
```

### search_catalog
Search for existing tables, views, and data assets in the catalog.
```
Use to find source data and understand the semantic data model landscape
```

### get_object_definition
Retrieve detailed metadata about views, dimensions, or other semantic objects.
```
Use to understand existing view structures, associations, and dependencies
```

### execute_query
Execute test queries against views to validate logic and performance.
```
Use to test calculated column expressions, filters, and join logic
```

## Key Takeaways

1. **Choose semantic usage carefully** — Fact, Dimension, Text, Hierarchy, or Relational Dataset determines behavior in analytics tools
2. **Design for performance** — Push-down optimization, efficient joins, and persistence strategies impact user experience
3. **Build associations for navigation** — Enable users to drill down and explore data across dimensions
4. **Validate before deployment** — Use MCP tools to test queries and understand dependencies
5. **Document comprehensively** — Clear descriptions help future maintainers and end users understand intent and usage patterns

## What's New (2026.05)

- **Partitioning Local Tables for Intelligent Applications**: If your Datasphere is part of an SAP Business Data Cloud formation, you can now create partitions for local tables installed via intelligent applications. This enables better management of read-only tables with large data volumes by breaking data into chunks.
- **Change Primary Key Index Type in Local Tables**: When a local table has multiple primary keys, you can now change the index type in the Local Table editor. This optimizes performance in very large volume scenarios where the default index type may not be optimal.
- **Review and Restore Transformation Flow Versions**: You can now review past versions of transformation flows, open them in read-only mode, download them as CSN/JSON files, and restore a past version to replace the current version. This provides version history and rollback capability for transformation logic.
