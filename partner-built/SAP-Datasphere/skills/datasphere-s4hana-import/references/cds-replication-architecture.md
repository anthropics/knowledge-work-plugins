# CDS View Replication Architecture: S/4HANA On-Premise to Datasphere

## End-to-End Architecture

### Datasphere Side (Target)
- Replication Flow UI/Services/Repository
- vFlow → VFlow-sub-abap → Replication Management Service (RMS)
- Axino/ABAP Pipeline Engine
- Replicated local table (target)

### Network Layer
- SAP Cloud Connector: Bridges cloud-to-on-premise connectivity

### S/4HANA Side (Source)
- CDS View with @Analytics.dataExtraction.enabled: true
- For Initial Only: Source table → RDB Buffer (direct)
- For Initial and Delta: Source table → Internal SQL View → CDC Engine (Master/Subscriber Logging Tables) → RDB Buffer

### Data Flow Summary

1. **Initial Only**: CDS View → RDB Buffer Tables → (Cloud Connector) → RMS → Local Table in Datasphere
2. **Initial and Delta**: CDS View → CDC Engine → Master Logging Table → Subscriber Logging Table → RDB Buffer → (Cloud Connector) → RMS → Local Table

## CDS View Requirements

### Mandatory Annotations

```
@Analytics:{
    dataExtraction: {
        enabled: true,
        delta.changeDataCapture.automatic: true  // for Initial and Delta
    }
}
```

- `dataExtraction.enabled: true` — Required for any replication
- `delta.changeDataCapture.automatic: true` — Required for delta capability (simple CDS views)
- `delta.changeDataCapture.mapping` — Alternative for complex CDS views with explicit field mapping
- See SAP Note 2890171 for complete CDS view requirements

### CDS View Validation

Use Transaction SDDLAR on source system with the following options:

- **Display DDL Source**: Review annotation correctness
- **Check DDL Source**: Validate syntax and consistency
- **Data Preview**: Confirm data is extractable
- **Show ROOT/COMPOSITION relations**: Check view hierarchy

## Setup Checklist

### Step 1: Cloud Connector

- Install and configure SAP Cloud Connector
- Add to Datasphere Configuration → Cloud Connector list
- Configure access paths for required services
- References: "Preparing Cloud Connector Connectivity", "Prepare Connectivity to SAP S/4HANA On-Premise"

### Step 2: Create S/4HANA On-Premise Connection

Connection Details:
- SAP Logon Connection Type (Application Server)
- Application Server
- System Number
- Client
- Language

Cloud Connector Configuration:
- Use Cloud Connector = true
- Location
- Virtual Host/Port

### Step 3: Validate Connection

Required validation result:
- Must show: "Replication flows are enabled"

Also verify:
- Data flows enabled
- Remote tables status
- Model Import status
- For validation errors: SAP KBA 3369433

### Step 4: Prepare CDS Views on Source

- Ensure required annotations are present
- Activate CDS views
- Verify in CDS_EXTRACTION container

### Step 5: Create Replication Flow in Datasphere

1. Data Builder → New Replication Flow
2. Select Source Connection (S/4HANA)
3. Select Source Container: CDS_EXTRACTION folder
4. Select Source Objects (CDS views)
5. Select Target Connection: SAP Datasphere
6. Set Load Type (Initial Only or Initial and Delta)
7. Save and Deploy before running

### Step 6: Run and Monitor

Monitor via Data Integration Monitor:
- Run Status
- Object Status
- Messages
- Metrics

**For Initial and Delta Replication**:
- Run Status = ACTIVE (RETRYING OBJECTS) between deltas is NORMAL
- Object Status cycles: INITIAL RUNNING → RETRYING → DELTA RUNNING → RETRYING
- Delta Load Interval configurable (Hours/Minutes)

## Source Container Notes

- Standard CDS views appear in CDS_EXTRACTION root folder
- If CDS view is not visible in CDS_EXTRACTION:
  1. Confirm `@Analytics.dataExtraction.enabled: true` annotation
  2. Confirm data can be extracted via RODPS_REPL_TEST
  3. Verify communication user has required authorizations
  4. Verify user has authorization to access the specific CDS view

## Troubleshooting Quick Reference

### Pre-Runtime Checks

1. All SAP Notes from SAP Note 2890171 applied on source system
2. CDS view validated with SDDLAR
3. Connection validates with "Replication flows are enabled"

### Runtime Error Investigation

1. Check Data Integration Monitor → Messages for error text
2. Check SLG1 on source system with objects DHAPE or DHCDC
3. Check DHRDBMON for buffer table status
4. Check DHCDCMON for delta/CDC status (Initial and Delta only)
5. Verify Observer and Transfer jobs are green in DHCDCMON Job Settings

### Performance Investigation

- System Monitor Dashboard in Datasphere
- HANA Cockpit for CPU and memory
- HANA indexserver log (access via SAP KBA 3476918)
- Check partitioning configuration

### Testing Outside Datasphere

- Report RODPS_REPL_TEST: Test extraction for the CDS view's corresponding SQL view
- Transaction ODQMON: Verify record count after test extraction
