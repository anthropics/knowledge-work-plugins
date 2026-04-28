# Replication Flow Error Patterns and Resolutions

## Architecture Context
Brief explanation: Replication Flows use RMS (Replication Management Service) collecting data from RDB (Resilient Data Buffer) tables via Cloud Connector. For "Initial and Delta" loads, the CDC Engine pushes changes through Master Logging Tables → Subscriber Logging Tables → RDB Buffer → RMS → Datasphere local table. Two load types: Initial Only (source table → RDB) and Initial and Delta (source table → CDC → RDB).

## Error Pattern 1: "Error occurred during execution of API activity; see application log" — Authorization
### Symptoms
- Error in Data Integration Monitor Messages tab
- SLG1 shows: "Not authorized to use operator 'internal.inport' (BADI_DHAPE_OPER_INPORT)" or "Not authorized to use operator 'com.sap.abap.operator_reader' (BADI_DHAPE_OPER_OPER_READER)"

### Root Cause
Missing security authorizations on the source ABAP system for the communication user

### Resolution
Apply SAP Note 3100673 — SAP Data Intelligence / SAP Datasphere - ABAP Integration - Security Settings. Assign required authorizations to the RFC communication user.

### Diagnostic Steps
1. Check SLG1 with Object DHAPE for detailed authorization error
2. Run SU53 for the communication user to see failed auth checks
3. Use STAUTHTRACE to trace the exact missing authorization objects

## Error Pattern 2: "Subscription interface error / Error while processing subscription of CDS view"
### Symptoms
- Deployment or initial run fails
- Run Log states CDS view definition is "complex or inconsistent"

### Root Cause
CDS view definition has issues — missing annotations, complex joins, unsupported features, or inconsistent metadata

### Resolution
1. Run SDDLAR on source system to validate CDS view (Check DDL Source, Data Preview)
2. Verify required annotations: @Analytics.dataExtraction.enabled: true
3. For delta: verify @Analytics.dataExtraction.delta.changeDataCapture annotation
4. Check SAP Note 2890171 for CDS view requirements in Replication Flow scenarios

### Diagnostic Steps
1. Open SLG1 with Object DHCDC for subscription errors
2. Test extraction independently with report RODPS_REPL_TEST
3. Validate CDS view in SDDLAR

## Error Pattern 3: "No source partition is available. Replication Flow will restart."
### Symptoms
- Data Integration Monitor shows State = "Partitioning Initial Load", Status = Active (Retrying)
- Flow keeps restarting without making progress

### Root Cause
Communication user lacks authorization to access the CDS view for subscriber RMS

### Resolution
1. Check SLG1 Object DHCDC for the specific authorization failure
2. Grant the required authorizations to the RFC user for the CDS view
3. Ensure S_SDSAUTH with ACTVT=16 (Execute) is assigned

### Diagnostic Steps
1. Check SLG1 for DHCDC entries at the time of the partitioning attempt
2. Run SU53 for the communication user immediately after the failure
3. Verify the user has S_SDSAUTH and SDDLVIEW authorization objects

## Error Pattern 4: "Failed because maximum number of deletions retries reached"
### Symptoms
- Multiple CDS views in a single Replication Flow
- Several views fail during replication
- Run Log states "CDS view definition is complex or inconsistent"

### Root Cause
When a Replication Flow contains many CDS views, failures in individual views can cascade. The deletion retry mechanism exhausts after repeated attempts.

### Resolution
1. Identify which specific CDS views are failing (check per-object status in Data Integration Monitor)
2. Validate each failing CDS view individually with SDDLAR and RODPS_REPL_TEST
3. Consider splitting large Replication Flows into smaller ones with fewer objects
4. Fix the "complex or inconsistent" CDS view definitions on the source system

## Error Pattern 5: "Cannot determine tables for CDS view"
### Symptoms
- Error during API activity execution
- SLG1 shows message DHCDC_CORE028 "Cannot determine tables for CDS view <name>"

### Root Cause
System cannot determine the underlying database tables for data extraction from the CDS view

### Resolution
See SAP KBA 3397020 — Check the @Analytics.dataExtraction annotation implementation and correct any errors or warnings. Restart extraction after fixing.

### Diagnostic Steps
1. Open SLG1, find entry with Object DHCDC, expand error details
2. Check long text for Message No. DHCDC_CORE028
3. In SDDLAR, verify CDS view can resolve to underlying tables
4. Check if annotation @Analytics.dataExtraction is correctly implemented

## Error Pattern 6: "Partitioning for object failed"
### Symptoms
- Random failures during replication, especially for larger datasets
- May work sometimes and fail other times

### Root Cause
Missing corrections in the source system

### Resolution
Apply SAP KBA 3465112 — Replication Flow of CDS views randomly fails with "Partitioning for Object failed". Implement the referenced SAP Notes on the source system.

## Error Pattern 7: DATA_NOT_READY — Buffer Table Empty or Low
### Symptoms
- Replication stalls, no data flowing
- DHRDBMON shows buffer table empty or very low record count
- No READY packages in Package Overview

### Root Cause (CDS views via CDC engine)
CDC Observer/Transfer jobs not running or not producing data

### Resolution
1. Check DHCDCMON → Job Settings → Verify Observer and Transfer jobs are green
2. If not green, click Dispatcher Job to reschedule
3. Check DHCDCMON → Application Log for errors
4. For performance issues with empty buffer: Increase transfer jobs per SAP Note 3669170 and SAP Note 3223735 (Transaction DHCDCSTG / Table DHCDC_JOBSTG parameters TRANSFER_MAX_JOBS and TRANSFER_MIN_JOBS)

## Error Pattern 8: DATA_NOT_READY — Buffer Table Full
### Symptoms
- DHRDBMON shows buffer table full or filling up
- Records not Assigned to Package is high (highlighted)
- READY packages accumulating but not being consumed

### Root Cause
RMS cannot collect data from the buffer — typically a Cloud Connector issue, network problem, or Datasphere-side bottleneck

### Resolution
1. Check Cloud Connector status and connectivity
2. Verify Datasphere connection is valid (Connection Management → Validate)
3. Check DHRDBMON Expert Functions to manually manage packages if needed
4. If packages are stuck, use "Change Status to Ready" or "Remove Records from Package" cautiously

## Error Pattern 9: ABAP Requests Completely Stuck
### Symptoms
- No progress in replication
- DHRDBMON shows no movement in buffer tables
- DHCDCMON logging tables may be growing

### Root Cause
Backend ABAP processing is blocked — jobs stuck, locks, or resource exhaustion

### Resolution
1. Check SM37 for Observer/Transfer job status
2. Check SM12 for locks on relevant tables
3. Check ST22 for ABAP short dumps related to /1DH/ programs
4. Verify no system-wide issues (SM21 system log, ST06 OS monitor)

## Component Ownership for SAP Support Cases
When opening an SAP support case, use these component assignments:
- RODPS_REPL_TEST returns error → Component: BW-WHM-DBA-ODA
- DHCDCMON Application Log shows "ACP daemon not start" → Component: BC-DB-CDC
- CDS extraction stuck → Check both BC-DB-CDC and DS-INT-RF (Datasphere Integration - Replication Flows)
- Cloud Connector issues → Component: BC-MID-SCC
- Datasphere-side pipeline issues → Component: DS-INT-RF

## Key SAP Notes Quick Reference
| SAP Note | Description |
|----------|-------------|
| 2890171 | ABAP Integration - CDS view requirements for Replication Flows |
| 3100673 | ABAP Integration - Security Settings |
| 3397020 | "Cannot determine tables for CDS view" resolution |
| 3465112 | "Partitioning for Object failed" random failures |
| 3669170 | How to improve replication performance - ABAP CDC Engine |
| 3223735 | SAP Data Intelligence - Transfer job tuning (DHCDC_JOBSTG) |
| 3369433 | Cloud Connector troubleshooting for Datasphere connections |
| 3365864 | Where does information in DHCDCMON come from? |
| 2930269 | ABAP CDS CDC common issues and troubleshooting |
| 3476918 | How to access HANA Cloud DB traces |
