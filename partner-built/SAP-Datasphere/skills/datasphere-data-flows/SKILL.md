---
name: datasphere-data-flows
description: SAP Datasphere Data Integration expert skill covering Replication Flows, Data Flows, Transformation Flows, and Task Chains. Use for architecting, configuring, troubleshooting, and optimizing data movement pipelines including CDC/delta processing, ETL operations, and orchestration.
---

# SAP Datasphere Data Integration

Expert skill for SAP Datasphere Data Integration layer covering all flow types and orchestration patterns.

## Flow Type Decision Matrix

| Requirement | Recommended Flow | Reason |
|-------------|------------------|--------|
| Mass 1:1 data movement | **Replication Flow** | Optimized for bulk transfer, supports CDC |
| Real-time delta capture | **Replication Flow** | Only flow type supporting continuous CDC |
| Complex ETL (joins, unions) | **Data Flow** | Visual modeling + Python scripting |
| Delta propagation through layers | **Transformation Flow** | Reads/writes delta tables, SQL-based |
| Schedule & orchestrate | **Task Chain** | Dependency management, parallel execution |

## Navigation

### Accessing Data Builder
1. Click **Data Builder** in the left navigation menu (cube icon)
2. Select a **Space** to work in (required before creating objects)
3. Use the tabs to filter: All Files | Tables | Views | E/R Models | Analytic Models | **Flows** | Intelligent Lookups | Task Chains

### Creating Flows
From Data Builder, click one of the creation tiles at the top:
- **New Data Flow** - Opens Data Flow editor
- **New Replication Flow** - Opens Replication Flow wizard
- **New Transformation Flow** - Opens Transformation Flow editor
- **New Task Chain** - Opens Task Chain orchestrator

| Flow Type | Navigation Path | URL Fragment |
|-----------|----------------|--------------|
| Data Builder | Left Menu → Data Builder | `#/databuilder` |
| Flows List | Data Builder → Flows tab | `#/databuilder&/db/{SPACE}` (filtered) |
| Data Flow Editor | Data Builder → New Data Flow | `#/databuilder&/db/{SPACE}/-newDataFlow` |
| Replication Flow | Data Builder → New Replication Flow | `#/replicationflow` |
| Transformation Flow | Data Builder → New Transformation Flow | `#/transformationflow` |
| Task Chain | Data Builder → New Task Chain | `#/taskchain` |
| Monitor All | Data Integration Monitor | `#/dim` |

### Data Flow Editor Layout

**Left Panel - Repository/Sources:**
- **Repository Tab:** Lists local tables, views, and objects (85+ objects)
- **Sources Tab:** Lists external connections for bringing in data
  - Expand "Connections" to see available source systems
  - Supports cloud sources (AWS, Azure, etc.)

**Center - Canvas:**
- Drag-and-drop visual modeling area
- Nodes represent: Sources, Operators, Targets
- Lines represent data flow direction
- Node badges show column counts

**Operators Toolbar:**
| Icon | Operator | Purpose |
|------|----------|---------|
| Table | Source/Target | Add data source or target table |
| Chain | Join | Combine two inputs (INNER, LEFT, RIGHT, FULL) |
| Transform | Projection | Select/rename columns |
| Aggregate | Aggregation | GROUP BY with SUM, COUNT, AVG, etc. |
| Code | Script (Python) | Custom Python transformations |
| Filter | Filter | Row-level filtering |

**Right Panel - Properties:**
- **General:** Business Name, Technical Name, Status
- **Run Status:** Execution state, last run info
- **Input Parameters:** Runtime variables
- **Advanced Properties:** Memory allocation, restart options

---

## 1. Replication Flows

### Primary Use Case
**1:1 mass data replication** from supported sources to supported targets with minimal transformation (projection/filtering only). This is the successor to SLT for cloud-to-cloud scenarios.

### Capabilities
- **Initial Load:** Full data extraction
- **Delta Load (CDC):** Change Data Capture for incremental updates
- **Projections:** Column selection/filtering
- **Simple transformations:** Basic filtering only

### Delta Prerequisites
> **CRITICAL:** The source object must have CDC annotations enabled.

For S/4HANA CDS Views:
```abap
@Analytics.dataExtraction.enabled: true
@Analytics.dataExtraction.delta.changeDataCapture: true
```
If the source lacks CDC annotations, only "Initial Load" is supported.

### Supported Targets

#### Inbound Targets (SAP)
| Target | Delta Support | Notes |
|--------|---------------|-------|
| Local Table | Yes | Can be delta-capture enabled |
| Local Table (File) | Yes | HANA Data Lake Files (Object Store) |
| SAP HANA Cloud | Yes | Direct HANA connection |

#### Outbound Targets (Non-SAP) - Requires POI
| Target | Format | Notes |
|--------|--------|-------|
| Amazon S3 | Parquet/CSV | Premium Outbound required |
| Google Cloud Storage | Parquet/CSV | Premium Outbound required |
| Google BigQuery | Native | Premium Outbound required |
| Azure Data Lake Gen2 | Parquet/CSV | Premium Outbound required |
| Apache Kafka | Events | Premium Outbound required |

### Premium Outbound Integration (POI)

> **LICENSING ALERT:** Replicating to non-SAP targets incurs specific costs.

| Scenario | POI Required? |
|----------|---------------|
| Replicate to Datasphere Local Table | No |
| Replicate to HANA Cloud | No |
| Replicate to HDLF (Object Store) | No |
| Replicate to AWS S3 | **Yes** |
| Replicate to Azure ADLS Gen2 | **Yes** |
| Replicate to Kafka | **Yes** |

**POI Blocks:** Measured in 20GB increments. Plan capacity accordingly.

### Critical Constraints
- ❌ **No complex logic:** Cannot perform joins, unions, aggregations
- ❌ **No Python scripting:** Use Data Flows for custom code
- ✅ **Use for:** Data movement and simple filtering only

### Creating a Replication Flow

1. **Data Builder** → New → **Replication Flow**
2. **Add Source:**
   - Select connection (e.g., S/4HANA)
   - Choose source objects (CDS Views, tables)
3. **Configure Load Type:**
   - Initial Load Only
   - Initial + Delta (if CDC enabled)
4. **Add Target:**
   - Select target type (Local Table, Object Store, External)
5. **Map Columns:** Projection and filtering
6. **Deploy & Run**

---

## 2. Data Flows

### Primary Use Case
**Complex ETL operations** requiring joins, unions, aggregations, or custom Python scripting.

### Capabilities
- Visual drag-and-drop modeling
- Join multiple sources
- Union datasets
- Aggregations and calculations
- **Python Operator:** Custom transformations using Pandas-like operations

### Python Operator
```python
# Example: Rename columns and convert data types
def transform(data):
    df = data.copy()
    df.columns = [col.upper() for col in df.columns]
    df['AMOUNT'] = df['AMOUNT'].astype(float)
    return df
```

**Available libraries:** Standard Python data manipulation (Pandas-like dataframe operations)

### Critical Constraints

> **IMPORTANT:** Data Flows are **BATCH ONLY**

| Constraint | Impact |
|------------|--------|
| No CDC support | Cannot propagate delta changes continuously |
| Batch execution | Full reload each run (unless filtered) |
| No delta chaining | Cannot use Data Flow target as delta source for another flow |

### When NOT to Use Data Flows
- ❌ Real-time/streaming requirements → Use Replication Flow
- ❌ Delta propagation through layers → Use Transformation Flow
- ❌ Simple 1:1 data movement → Use Replication Flow (more efficient)

### When to Use Data Flows
- ✅ Complex joins between multiple sources
- ✅ Custom Python transformations
- ✅ Data quality operations
- ✅ One-time or scheduled batch loads

### Creating a Data Flow

> **Note:** A banner in the editor reminds you: "Replication and Transformation Flows are now the recommended approach... while Data Flows will continue to be supported for existing workflows."

**Step-by-Step:**

1. **Open Data Builder** → Select Space → Click **"New Data Flow"** tile
2. **Canvas Opens** with empty workspace showing:
   - Left panel: Repository (local objects) and Sources (external connections)
   - Properties panel: Auto-generates name like "Data Flow 1" / "Data_Flow_1"

3. **Add Source Tables:**
   - From **Repository tab**: Click table, then click canvas area to add
   - Or click Operators toolbar → Table icon → click canvas
   - Source nodes show column count badge (e.g., "9" for 9 columns)

4. **Add Transformation Operators:**
   - Click operator icon in toolbar (Join, Projection, Aggregation, Script)
   - Click canvas to place
   - Connect nodes by clicking output port → dragging to input port

5. **Configure Join (if used):**
   - Select Join node → Properties panel shows:
     - Join Type: INNER (default), LEFT, RIGHT, FULL OUTER
     - Join Definition: Define key columns
   - Connect two source nodes to the join inputs

6. **Add Python Script (optional):**
   - Click Script operator in toolbar
   - Configure custom transformation logic in Properties panel

7. **Add Target Table:**
   - Click "+" icon on the last transformation node
   - Or: Operators → Table → place on canvas
   - Target shows "New" badge - creates new local table
   - Configure: Connection (Datasphere), Business Name, Technical Name

8. **Save & Deploy:**
   - Click Save icon (General toolbar)
   - Click Deploy to make executable
   - Status changes from "Not Deployed" → "Deployed"

9. **Run:**
   - From Run Status section → Click Run icon
   - Monitor in Data Integration Monitor

---

## 3. Transformation Flows

### Primary Use Case
**Delta propagation and multi-level staging** within Datasphere. The strategic successor to Data Flows for delta logic.

### Key Concept: Delta Waterfall
```
Replication Flow → [Delta Table A] → Transformation Flow → [Delta Table B] → Transformation Flow → [Delta Table C]
```
Each layer receives only **changed records** (Insert, Update, Delete).

### Capabilities
- Reads from Delta-enabled Local Table
- Writes to Delta-enabled Local Table
- **Delta Propagation:** Understands and propagates I/U/D operations
- **SQL-based transformations:** Powerful SQL logic

### Architecture Rule

> **CRITICAL DECISION:** If you need to:
> 1. Load data via Replication Flow (Inbound)
> 2. Process only the **changes** to a second layer
>
> → **Use Transformation Flow**, NOT Data Flow

### Delta Logic Support
| Operation | Propagated? |
|-----------|-------------|
| INSERT | ✅ Yes |
| UPDATE | ✅ Yes |
| DELETE | ✅ Yes |

### Creating a Transformation Flow

1. **Data Builder** → New → **Transformation Flow**
2. **Select Source:** Must be a Delta-enabled Local Table
3. **Add SQL Logic:**
   - Projections, filters
   - Calculations
   - CASE statements
4. **Select Target:** Delta-enabled Local Table
5. **Deploy & Run**

### Comparison: Data Flow vs Transformation Flow

| Aspect | Data Flow | Transformation Flow |
|--------|-----------|---------------------|
| Delta/CDC | ❌ No | ✅ Yes |
| Complex Joins | ✅ Yes | ⚠️ Limited |
| Python Scripts | ✅ Yes | ❌ No |
| Multi-level Staging | ❌ Not recommended | ✅ Designed for this |
| Performance | Batch reload | Incremental processing |

---

## 4. Task Chains

### Primary Use Case
**Scheduling and dependency management** for orchestrating multiple flows.

### Capabilities
- Trigger: Replication Flows, Data Flows, Transformation Flows
- Trigger: View Persistency, Intelligent Lookups
- **Execution Modes:** Serial (Linear) and Parallel
- **Gates:** AND (wait for all) and OR (wait for any)

### Execution Patterns

#### Serial Execution
```
[Flow A] → [Flow B] → [Flow C]
```
Each step waits for the previous to complete.

#### Parallel Execution with AND Gate
```
[Flow A] ─┐
          ├─ AND ─→ [Flow D]
[Flow B] ─┤
[Flow C] ─┘
```
Flow D runs only after A, B, AND C complete.

#### Parallel Execution with OR Gate
```
[Flow A] ─┐
          ├─ OR ─→ [Flow D]
[Flow B] ─┘
```
Flow D runs after A OR B completes (first one).

### BW Bridge Integration
Task Chains can trigger remote process chains in SAP BW Bridge, though Bridge chains are typically scheduled internally within the Bridge Cockpit.

### Creating a Task Chain

1. **Data Builder** → New → **Task Chain**
2. **Add Tasks:** Drag flows to canvas
3. **Configure Dependencies:**
   - Connect tasks with arrows
   - Set gate types (AND/OR)
4. **Set Schedule:**
   - One-time or recurring
   - Time-based or event-based
5. **Deploy & Activate**

---

## Integration Patterns

### SAP S/4HANA Integration

**Preferred Method:** CDS Views via ABAP connection (using Cloud Connector)

| Method | When to Use |
|--------|-------------|
| CDS Views | Preferred - semantic richness, CDC support |
| SLT (Trigger-based) | Legacy - supported but CDS preferred |

### Object Store (HANA Data Lake Files)

**Physical Storage:** Replication Flows can dump data to "Local Table (File)" in embedded HANA Data Lake.

| Characteristic | Value |
|----------------|-------|
| Performance | Slower than In-Memory HANA |
| Use Case | Warm/Cold data, staging |
| Data Products | Foundation for BDC Data Products |

### Databricks Integration

| Direction | Method | Cost Impact |
|-----------|--------|-------------|
| **Inbound** (Databricks → SAP) | JDBC connection or Data Import | Standard |
| **Outbound** (SAP → Databricks) Federation | Delta Sharing (Zero Copy) | No data movement |
| **Outbound** (SAP → Databricks) Mass | Replication Flow → ADLS Gen2 → Mount as Delta Table | **POI Required** |

---

## Troubleshooting Guide

### Replication Flow Failed

**Check these in order:**

1. **CDC Annotations:** Does source CDS view have:
   ```abap
   @Analytics.dataExtraction.enabled: true
   @Analytics.dataExtraction.delta.changeDataCapture: true
   ```

2. **Cloud Connector:** Is it running and connected?

3. **POI Blocks:** For non-SAP targets, are you out of Premium Outbound blocks?

4. **Execution Nodes:** Check thread limits for large tables (e.g., ACDOCA)

### Data Flow is Slow

**Optimization checklist:**

1. **Full loads every time?** → Switch to Replication Flow (for movement) or Transformation Flow (for delta logic)

2. **Large joins?** → Pre-aggregate or filter at source

3. **Python operator?** → Optimize DataFrame operations

### How to Move BW Data?

> **Do NOT rebuild manually!**

| Scenario | Solution |
|----------|----------|
| Legacy BW logic (ABAP) | Use **SAP BW Bridge** |
| BW/4HANA 2021+ or BW 7.5 SP24+ | Use **Data Product Generator** to push InfoProviders to Object Store |

### I Need Real-Time

**Only option:** Replication Flows

Data Flows and Transformation Flows are **batch only**.

---

## Best Practices

### Flow Selection
1. **Start with Replication Flow** for data ingestion
2. **Use Transformation Flows** for delta staging layers
3. **Reserve Data Flows** for complex one-time transformations
4. **Orchestrate with Task Chains**

### Cost Optimization
- Replicate to SAP targets (no POI cost)
- Use federation (Remote Tables) when real-time not required
- Size POI blocks based on 20GB increments

### Performance
- Enable CDC on source CDS views
- Use Object Store for warm/cold data
- Parallelize with Task Chains where possible

## Resources

See reference files for detailed procedures:
- `references/replication-flows.md` - Detailed replication configuration
- `references/transformation-flows.md` - Delta staging patterns
- `references/task-chains.md` - Orchestration patterns

## What's New (2026.05)

- **Improved Primary Key Order Handling in Replication Flows**: During table replication, the primary key order from the source is now preserved in the target. This prevents replication failures caused by key order mismatches between source and target tables. No configuration needed — this is automatic behavior.
- **Output Parameters in Task Chains**: Task chain objects now support output parameters. You can map output parameters from task objects to the parent task chain, enabling more flexible orchestration of nested task chains and conditional logic based on task results.
