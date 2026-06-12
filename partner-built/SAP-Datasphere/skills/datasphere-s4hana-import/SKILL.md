---
name: S/4HANA Import Assistant
description: "Specialized assistant for importing entities from SAP S/4HANA and BW/4HANA into Datasphere. Use this when connecting to SAP systems, selecting CDS views, configuring ODP extraction, setting up Cloud Connector, or enabling real-time delta loads."
---

# S/4HANA Import Assistant

## Overview

This skill provides comprehensive guidance for successfully importing data from SAP S/4HANA and BW/4HANA systems into SAP Datasphere. It covers the entire workflow from understanding available source objects to configuring extraction methods and monitoring data flows.

## When to Use This Skill

- **Initial S/4HANA connection**: Setting up Cloud Connector and DP Agent
- **Exploring available objects**: Finding the right CDS views, InfoProviders, or tables
- **Selecting semantically rich data**: Choosing extraction-enabled views over raw tables
- **Configuring delta extraction**: Setting up ODP for real-time or near-real-time data
- **Handling BW/4HANA objects**: Importing InfoProviders and CompositeProviders
- **Troubleshooting connectivity**: Resolving Cloud Connector or DP Agent issues
- **Managing delta queues**: Monitoring and recovering from extraction issues
- **Optimizing extraction performance**: Choosing the right extraction methods

## The Import Entities Wizard Workflow

The Import Entities wizard guides you through a structured process for bringing SAP source objects into Datasphere:

### Step 1: Create or Select a Connection

```
Datasphere UI → Data Integrations → Connections
→ Create New or Select Existing S/4HANA Connection
```

**Required Information:**
- Connection Name (e.g., "SAP_S4H_PROD")
- Source System Type (S/4HANA, BW/4HANA, ECC, etc.)
- Host and Port
- Client Number
- Authentication Method (Basic, Certificate, OAuth)
- Cloud Connector Location ID (for on-premise systems)

**Example Connection Configuration:**
- Source: SAP S/4HANA 2023
- Host: s4h-prod.example.com
- Port: 443
- Client: 100
- Cloud Connector: CC_PROD_001

### Step 2: Create a New Replication or Data Integration Task

```
Data Integrations → New Task
→ Select Source System (from connections)
→ Choose Task Type (Replication Flow, Data Flow, or Transformation Flow)
```

### Step 3: Search and Select Source Objects

The system searches for available objects in the SAP source system:

**Search Criteria:**
- Object Type (CDS View, InfoProvider, ODP Extractor, Query)
- Business Area (Financial, Sales, Procurement, HR, Supply Chain)
- Object Name or Pattern
- Extraction Method (ODP, Database, Query)

**Search Example:**
```
Search: "C_*"
Filter by: CDS Views, Extraction-enabled only
Results: C_CUSTOMER, C_SALES_ORDER, C_INVOICE, ...
```

### Step 4: Configure Extraction Method

Choose how data will be extracted:

```
Object: C_CUSTOMER (CDS View)
Available Extraction Methods:
  ✓ ODP (Operational Data Provisioning) - Real-time, Delta support
  ✓ Database Access - Direct SQL, Full only
  ✓ API - If exposed as API
  → Select ODP for Delta capability
```

### Step 5: Map Source to Target

```
Source CDS View: C_CUSTOMER
Fields: CUSTOMER_ID, CUSTOMER_NAME, EMAIL, PHONE, CREATED_DATE
↓
Target Table (auto-created or manual selection)
CUSTOMER_MASTER (new table in Datasphere)
```

### Step 6: Configure Load Settings

```
Initial Load:
  - Full Load: Yes, load all historical data
  - Parallel Threads: 4 (for performance)
  - Package Size: 10000 rows

Delta Load:
  - Delta Enabled: Yes
  - Delta Type: ODP Change Data Capture
  - Extraction Frequency: Every 15 minutes
  - Watermark Field: CHANGENUMBER (from ODP)
```

### Step 7: Review and Activate

```
Review:
  - Source: C_CUSTOMER (S/4HANA)
  - Target: CUSTOMER_MASTER (Datasphere)
  - Method: ODP with Delta
  - Schedule: Automatic every 15 minutes

Status: Ready to Activate
```

## Identifying Extraction-Enabled CDS Views in S/4HANA

Not all CDS views are extraction-enabled. You must use views explicitly marked for extraction:

### Characteristics of Extraction-Enabled CDS Views

**Naming Convention:**
- Prefix `C_` : Consumer views, extraction-enabled (e.g., C_CUSTOMER, C_SALES_ORDER)
- Prefix `I_` : Internal views, not for extraction
- Prefix `P_` : Projection views
- Prefix `DD_` : Domain-specific views

**Extraction Capability Indicators:**

1. **@Analytics Annotation**
```abap
@Analytics.dataCategory: #FACT
@Analytics.dataExtraction.enabled: true
define view C_SALES_ORDER as
  select from vbak {
    vbak.vbeln as SalesOrderNumber,
    vbak.erdat as CreatedDate,
    vbak.netwr as NetAmount
  }
```

2. **@Semantics Annotation**
```abap
@Semantics.amount.currencyCode: 'CurrencyCode'
@ObjectModel.Composition.RefreshingElement: true
```

### Finding CDS Views in S/4HANA

**Via Transaction SE11 (ABAP Dictionary):**
```
SE11 → CDS View → Search for C_*
Filter: "Author = SAP" AND "Extraction Enabled = X"
```

**Via Search in Datasphere:**
```
Data Integrations → Search Catalog
Source: S/4HANA_PROD
Type: CDS View
Search Text: "customer" OR "sales" OR "invoice"
```

**Common Extraction-Enabled Views by Module:**

| Module | View Name | Purpose |
|--------|-----------|---------|
| Finance | C_GENERALLEDGER | General Ledger transactions |
| Finance | C_CUSTOMER_INVOICE | Customer invoices |
| Finance | C_SUPPLIER_INVOICE | Supplier invoices |
| Sales | C_CUSTOMER | Customer master |
| Sales | C_SALES_ORDER | Sales orders |
| Sales | C_SALES_ORDER_ITEM | Sales order line items |
| Procurement | C_SUPPLIER | Supplier master |
| Procurement | C_PURCHASE_ORDER | Purchase orders |
| Procurement | C_PURCHASE_ORDER_ITEM | Purchase order lines |
| Inventory | C_MATERIAL | Material master |
| Inventory | C_MATERIAL_STOCK | Inventory balances |
| HR | C_EMPLOYEE | Employee master |
| HR | C_EMPLOYEE_SALARY | Salary information |

### Verify Extraction Capability

Use the `search_catalog` MCP tool:

```
search_catalog(
    source="S/4HANA_PROD",
    object_type="CDS_VIEW",
    search_term="C_CUSTOMER",
    extraction_enabled=True
)
```

Expected output includes extraction metadata:
```json
{
    "object_name": "C_CUSTOMER",
    "extraction_enabled": true,
    "extraction_types": ["ODP", "DATABASE"],
    "delta_capable": true,
    "fields": [
        {
            "name": "CUSTOMER_ID",
            "type": "STRING",
            "key": true,
            "changeable": false
        },
        {
            "name": "CUSTOMER_NAME",
            "type": "STRING",
            "changeable": true
        }
    ]
}
```

## Understanding CDS View Annotations

Annotations in CDS views control behavior and extraction characteristics:

### @Analytics Annotations

```abap
@Analytics.dataCategory: #FACT              -- Type: FACT, DIMENSION, CUBE, QUERY
@Analytics.dataExtraction.enabled: true     -- Enable extraction
@Analytics.dataExtraction.deltaSupported: true  -- Support delta extractions
```

### @ObjectModel Annotations

```abap
@ObjectModel.readOnly: true                 -- View is read-only
@ObjectModel.transactional: false           -- Not transactional
@ObjectModel.usageType: #FACT                -- Usage classification
@ObjectModel.Composition.RefreshingElement: true  -- Refresh semantics
```

### @Semantics Annotations

```abap
@Semantics.amount.currencyCode: 'CurrencyCode'    -- Currency field
@Semantics.quantity.unitOfMeasure: 'UnitOfMeasure' -- UOM field
@Semantics.calendar.date: true              -- Date field
@Semantics.businessKey: true                -- Business key
```

### @EndUserText Annotations

```abap
@EndUserText.label: 'Customer Master'
@EndUserText.description: 'Extraction-enabled customer master data'
@EndUserText.quickInfo: 'All customers from KNVP and KNVV tables'
```

## ODP (Operational Data Provisioning) Extractors

ODP is SAP's modern extraction framework, replacing older RFC-based methods:

### ODP Architecture

```
S/4HANA System
├── ODP Provider (e.g., CDS View C_CUSTOMER)
├── ODP Context (e.g., ABAP:CDS_VIEWS)
├── Change Log Table
├── Delta Queue (Pending changes)
└── Watermark (Last extracted position)
```

### ODP Extractor Types

| Type | Source | Use Case | Delta Support |
|------|--------|----------|----------------|
| CDS_VIEWS | Extraction-enabled CDS views | Modern standard objects | Yes (FULL) |
| FUNCTION | RFC function modules | Custom extraction logic | Yes |
| TABLE | Database tables | Direct table access | Yes |
| QUERY | ABAP query/report | Parameterized extraction | No |
| LOGICAL_LOG | Application log/changes | Event-based changes | Yes |

### Configuring ODP Delta Load

```
Source: C_SALES_ORDER (ODP Provider)
Delta Configuration:
  - Delta Type: FULL_THEN_DELTA
  - Semantics: Changed records only
  - Key Fields: SALES_ORDER_NUMBER (determines uniqueness)
  - Extraction Sequence: Change Number (internal counter)

Example Delta First Run:
1. Full load: all records
2. Store watermark: CHANGENUMBER = 1000000

Example Delta Second Run:
1. Query: CHANGENUMBER > 1000000
2. Delta load: only changed since last run
3. Update watermark: CHANGENUMBER = 1000050
```

### ODP Change Data Capture (CDC)

ODP tracks changes via change numbers and delta queues:

```
Change Number = Internal sequence counter
When a record changes:
  → ODP logs the change
  → Increments change number
  → Stores in delta queue
  → Available until queue is cleared (usually 3-8 days)

Delta Extraction Sequence:
  Initial Load (FULL): Get CHANGENUMBER = 500000
  Delta Load (Day 2): WHERE CHANGENUMBER > 500000
  Delta Load (Day 3): WHERE CHANGENUMBER > 500050
  ...
```

## ABAP CDS Views: Released APIs vs Custom Views

### SAP-Released CDS Views (Safe for Production)

**Characteristics:**
- Prefix: `C_` (consumption) or published by SAP
- Fully documented and supported by SAP
- Extraction-enabled with stable field lists
- Backward compatible across releases
- Published in SAP API Hub

**Example - C_GENERALLEDGER:**
```abap
@VDM.viewType: #CONSUMPTION
@ObjectModel.semanticKey: ['CompanyCode', 'DocumentNumber', 'FiscalYear']
@Analytics.dataCategory: #FACT
@Analytics.dataExtraction.enabled: true
define view C_GENERALLEDGER as
  select from fin_gl_posting as posting {
    posting.bukrs as CompanyCode,
    posting.belnr as DocumentNumber,
    posting.gjahr as FiscalYear,
    posting.dmbtr as Amount,
    posting.budat as DocumentDate
  }
  where posting.bukrs <> ''
    and posting.dmbtr <> 0;
```

### Custom CDS Views (Use with Caution)

**Risks:**
- No support guarantee from SAP
- Fields may change or disappear
- Not backward compatible
- May not have extraction enabled
- Performance not optimized for extraction

**When to use custom views:**
- SAP standard view doesn't exist
- Need to combine multiple tables
- Apply complex filtering/calculations
- Specific business requirements

**Creating a custom extraction-enabled view:**
```abap
@VDM.viewType: #CONSUMPTION
@Analytics.dataCategory: #FACT
@Analytics.dataExtraction.enabled: true
@Analytics.dataExtraction.deltaSupported: true
@EndUserText.label: 'Custom Sales Analysis'
define view Z_CUSTOM_SALES as
  select from vbak as orders
    inner join vbap as items on vbak.vbeln = vbap.vbeln
    left outer join vbrk as invoices on vbak.vbeln = vbrk.xblnr {
      vbak.vbeln as SalesOrder,
      vbap.posnr as LineNumber,
      vbak.erdat as CreatedDate,
      vbap.netwr as NetAmount
    };
```

## BW/4HANA Objects: InfoProviders and CompositeProviders

BW/4HANA uses InfoProviders as the primary data container for analytics:

### InfoProvider Types

**Standard InfoProvider (Cube):**
```
BW/4HANA → InfoProvider: /BIC/SALES (Facts and dimensions)
├── Fact Table: /BIC/FSALES00
├── Dimensions:
│   ├── 0CUSTOMER (Customer dimension)
│   ├── 0MATERIAL (Material dimension)
│   └── 0PLANT (Plant dimension)
└── Measures: Sales Value, Quantity, Margin
```

**CompositeProvider (Virtual Cube):**
```
CompositeProvider: /BIC/COMP_SALES
├── InfoProvider 1: /BIC/SALES (Current year)
├── InfoProvider 2: /BIC/SALES_ARCHIVE (Prior years)
└── Query logic: UNION with transformation rules
```

### Extraction from BW/4HANA

**Via ODP:**
```
BW System → ODP Provider (BW:INFOPROVIDER)
Source: /BIC/SALES
Type: InfoProvider
Delta: Change request number (BW concept)
Extraction: All cubes support ODP extraction
```

**Configuration:**
```
Source BW Object: /BIC/SALES
Characteristics (Dimensions):
  - 0CUSTOMER
  - 0MATERIAL
  - 0PLANT

Key Figures (Measures):
  - 0SALES_VALUE
  - 0QUANTITY
  - 0GROSS_MARGIN

Load Setting:
  - Initial Load: Full (all data)
  - Delta: Request-based (BW change request tracking)
```

### BW Query Extraction

**Query Option (Extract from OLAP Query):**
```
BW Query: Z_SALES_ANALYSIS
└── Extract directly as data source
├── Advantages: Complex logic defined in query, pre-calculated
├── Disadvantages: Delta not supported, slower than ODP
└── Use case: Aggregated reporting data
```

## Connection Prerequisites

### Cloud Connector Setup (On-Premise Systems)

The Cloud Connector acts as a reverse proxy tunnel between cloud and on-premise SAP systems:

**Installation Checklist:**

1. **Procurement**
   - [ ] Download Cloud Connector from SAP downloads
   - [ ] Obtain license key
   - [ ] Allocate VM or physical server (4GB RAM minimum)

2. **Installation**
   - [ ] Install on machine in SAP network
   - [ ] Configure JDK (Java 11+)
   - [ ] Set up HTTPS certificates
   - [ ] Configure administrative user

3. **Configuration**
   ```
   Administration UI: https://localhost:8443
   Add Backend System:
     - System Type: SAP System
     - Host: s4h-prod.example.com
     - Port: 443
     - Protocol: HTTPS
     - Virtual Host: s4h-prod (for cloud access)

   Resource Mapping:
     - URL Pattern: /sap/opu/odata/sap/*
     - URL Regex: ^/sap/opu/odata/sap/.*
     - Check: YES (enabled)
   ```

4. **Certificate Exchange**
   - [ ] Export Cloud Connector certificate
   - [ ] Import in S/4HANA trusted store
   - [ ] Exchange client certificate if using mutual TLS

5. **Testing**
   - [ ] Test from Datasphere → Cloud Connector → SAP system
   - [ ] Verify ODP availability
   - [ ] Check latency and throughput

**Cloud Connector Architecture:**
```
Datasphere (Cloud)
    ↓ HTTPS
Cloud Connector (DMZ/Internal Network)
    ↓ HTTPS/HTTP
S/4HANA System (On-Premise)
```

### DP Agent Setup (Alternative to Cloud Connector)

Data Provisioning Agent is used in some scenarios:

**When to use DP Agent:**
- Multi-tier network (requires agent in SAP network)
- Firewall restrictions prevent Cloud Connector
- Batch/scheduled extractions preferred

**Installation:**
```
Download: SAP Datasphere → Administration → DP Agent Download
Install on: Server in SAP network with access to source systems
Configure:
  - Datasphere tenant URL
  - OAuth credentials or certificate
  - Source system connections

Start Agent: .\dpsagent.exe start
Verify: Check "Agent Status" in Datasphere Administration
```

**DP Agent Communication:**
```
Datasphere → HTTPS → DP Agent (On-Premise)
           ← Data ← Source Systems
```

## Delta Extraction Patterns

### Pattern 1: Timestamp-Based Delta (Most Common)

**Setup:**
```
Source View: C_CUSTOMER
Delta Field: CHANGED_AT (timestamp)
ODP Configuration:
  - Track changes via timestamp
  - Load only records changed since last run
```

**Extraction Sequence:**
```
Day 1: Full load all customers (CHANGED_AT <= 2024-01-15)
       Save watermark: 2024-01-15 23:59:59

Day 2: Delta load where CHANGED_AT > 2024-01-15 23:59:59
       Changes: 150 new/updated records
       New watermark: 2024-01-16 23:59:59

Day 3: Delta load where CHANGED_AT > 2024-01-16 23:59:59
       Changes: 75 new/updated records
```

**Advantages:** Simple, reliable, handles late arrivals
**Disadvantages:** Requires timestamp maintenance

### Pattern 2: Change Number Sequence (ODP Native)

**Setup:**
```
Source: C_SALES_ORDER
ODP provides: Change Number (CHANGENUMBER field)
Automatic tracking by ODP
```

**Extraction Sequence:**
```
Day 1: Full load with CHANGENUMBER up to 5000000
Day 2: Delta where CHANGENUMBER > 5000000
       Extract: records 5000001 to 5000500
Day 3: Delta where CHANGENUMBER > 5000500
```

**Advantages:** ODP handles completely, most reliable
**Disadvantages:** Limited history (3-8 days typically)

### Pattern 3: Logical Change Document (For Complex Changes)

**Setup:**
```
Source: BW InfoProvider
Tracking: Change request numbers
Each request = batch of changes
```

**Handling:**
```
Request 001: 1000 rows inserted
Request 002: 500 rows updated
Request 003: 100 rows deleted

Delta load pulls complete requests (no partial)
```

## Best Practices for S/4HANA Imports

### 1. Choose the Right Extraction Method

**Decision Tree:**
```
Need Real-time Data?
├─ YES → Use ODP if available
│        └─ Delta every 5-15 minutes
└─ NO → Can batch load suffice?
         ├─ YES → Use Database access or ODP batch
         └─ NO → Use ODP with frequent schedule
```

### 2. Identify Semantically Rich Objects

**Semantic Richness Hierarchy:**
```
1. SAP-provided consumption CDS view (C_*) ✓✓✓ (Use this)
2. SAP cluster/pooled table via CDS ✓✓
3. SAP standard table via CDS ✓
4. Custom CDS view ✓ (Use with caution)
5. Raw SAP table ✗ (Avoid if possible)
```

**Why it matters:**
- Consumption views have business logic applied
- Transformations and hierarchies built-in
- Data quality rules enforced
- Fields well-documented and stable

### 3. Handle Hierarchies Correctly

**Hierarchy Example (0CUSTOMER dimension):**
```
Hierarchy Structure:
Region
├── North America
│   ├── USA
│   │   ├── East Region
│   │   └── West Region
│   └── Canada
└── Europe
    ├── UK
    └── Germany

Extract with Hierarchy:
- Get all leaf customers
- Include parent relationships
- Track parent changes (SCD Type 2)
```

**Configuration:**
```
BW InfoProvider: /BIC/SALES
Dimension: 0CUSTOMER
Include: Hierarchy levels
  - CUSTHIER01 (Standard customer hierarchy)
  - With parent-child relationships
```

### 4. Manage Load Volumes

**Large Initial Loads:**
```
Source: C_GENERALLEDGER (500M rows)
Strategy:
  - Partition by date range
  - Load in parallel batches
  - Monitor memory and storage
  - Estimate: 500M rows ≈ 100GB compressed
```

**Configuration:**
```
Parallel Threads: 4-8 (for initial load)
Package Size: 100,000 rows per package
Estimated Duration: 8-12 hours
Monitor: Memory, CPU, Network
```

### 5. Monitor Delta Queue Health

**Check Delta Queue Status:**
```
Use MCP tool: test_connection(source="S/4HANA_PROD")
Verify:
  - Delta queue not overflowing
  - Change documents available
  - No extraction errors
```

**Delta Queue Limits:**
```
Typical retention: 3-8 days
Size limit: 2-4GB per table
If exceeded: Must do full reload

Monitor:
  - Days of changes retained
  - % of queue capacity used
  - Time since last cleanup
```

## MCP Tool References

### search_catalog
Find available objects in S/4HANA or BW/4HANA systems:

```
search_catalog(
    source="S/4HANA_PROD",
    object_type="CDS_VIEW",
    search_term="customer",
    extraction_enabled=True,
    module="SALES"
)
```

### get_space_assets
View existing objects imported into Datasphere spaces:

```
get_space_assets(
    space_name="FINANCE",
    asset_type="TABLE",
    source="S/4HANA_PROD"
)
```

### search_repository
Search Datasphere repository for specific objects:

```
search_repository(
    object_type="REPLICATION_FLOW",
    name_contains="CUSTOMER",
    source_system="S/4HANA"
)
```

### test_connection
Verify connectivity to SAP systems and ODP availability:

```
test_connection(
    connection_name="SAP_S4H_PROD",
    verify_odp=True,
    check_delta_queue=True
)
```

## Reference Materials

See reference files for detailed procedures:
- `references/s4hana-integration-guide.md` - CDS views by functional area, ODP configuration, Cloud Connector and DP Agent setup
- `references/cds-replication-architecture.md` - End-to-end architecture for CDS view replication (RMS, RDB, CDC Engine), setup checklist, CDS annotation requirements, and troubleshooting quick reference

## Next Steps

1. **Gather prerequisites** using test_connection
2. **Search for objects** using search_catalog
3. **Evaluate semantic richness** of available CDS views
4. **Plan extraction method** (ODP for delta, Database for full)
5. **Set up Cloud Connector** if on-premise system
6. **Create and activate** replication flow
7. **Monitor** initial load and subsequent deltas

