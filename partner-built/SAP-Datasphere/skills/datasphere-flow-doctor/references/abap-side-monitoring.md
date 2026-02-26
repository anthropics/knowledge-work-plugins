# ABAP-Side Monitoring for Replication Flows

## Overview

Replication Flows in SAP Datasphere depend on a distributed architecture spanning both the source SAP S/4HANA system and the Datasphere environment. The source system hosts three critical components:

- **CDC Engine** (Change Data Capture): Captures insert, update, and delete events from application tables using logging tables and the CDC framework
- **Resilient Data Buffer (RDB)**: A staging layer that stores captured changes temporarily before transmission
- **Replication Management Service (RMS)**: Coordinates data collection and transfer to Datasphere

Most runtime issues originate on the source system. While Datasphere's Data Integration Monitor shows replication status, the diagnostic root cause almost always requires investigation of ABAP-side components. This reference covers the transaction-based tools available in S/4HANA for monitoring and troubleshooting these components.

---

## Transaction DHCDCMON (CDC Monitor)

### Purpose

DHCDCMON provides real-time visibility into Change Data Capture (CDC) operations. It monitors the logging table infrastructure, view reconstruction, and data flow from application tables through the CDC framework. Use this transaction to diagnose issues with "Initial and Delta" replication flows where the CDC engine is actively capturing changes.

### Object Overview Tab

The Object Overview tab displays the core CDC state for each registered object:

**Registered Objects and CDC Status Section**
- **Object Name**: The CDS view being replicated (e.g., `I_Customer`)
- **Application Table**: The source S/4 table being monitored (e.g., `KNA1`)
- **Master LogTab (/1DH/ML\*)**: System-generated logging table receiving change events from the application
- **Subscriber LogTab (/1DH/SL\*)**: Derived logging table holding reconstructed view data
- **Record Counts**: Shows current row counts in both logging tables

**Key Diagnostic Rule: Logging Table Health Indicator**
- In a healthy state, both Master and Subscriber logging tables should contain 0 or minimal records (typically 1-10)
- Records accumulate temporarily as the CDC framework processes changes
- A **permanently rising record count** indicates the Observer or Transfer job is not consuming data
- High record counts (thousands+) signal a backlog and point to job failures or resource constraints

**Subscriber Worklist Section**
- Lists individual subscriber connections with their processing status
- **Status B** (Blocked): Subscriber processing is suspended; investigate job failures or authorization issues
- **Status E** (Failed): Subscriber encountered an error during processing; check Application Log
- Any records appearing in this section indicate active issues requiring immediate attention

**Subscriber Logging Table Sequence ID**
- Tracks the highest pointer value for each object's Subscriber logging table
- Increments each time a new change record is inserted into the logging table
- A static sequence ID (not changing over time) indicates no new changes are being captured or processed

**Observer Job Worklist**
- Shows which logging tables are currently being processed by the background Observer job
- Reflects real-time job activity; entries appear and disappear as processing completes
- Absence of activity for extended periods suggests the Observer job is not running

### Job Settings Tab

The Job Settings tab controls two critical background jobs that move data through the CDC pipeline:

**Observer Job (/1DH/OBSERVE_LOGTAB)**
- **SM37 Job Name**: `/1DH/OBSERVE_LOGTAB`
- **Underlying Report**: `DHCDCR_OBSERVE_LOGTAB`
- **Function**: Reads entries from the Master logging table, applies view reconstruction logic (executing CDS view definitions against captured deltas), and writes reconstructed results to the Subscriber logging table
- **Required Status**: Must show **green** status icon for healthy operation
- **Failure Impact**: If not green, view reconstruction halts, preventing delta data from propagating

**Transfer Job (/1DH/PUSH_CDS_DELTA)**
- **SM37 Job Name**: `/1DH/PUSH_CDS_DELTA`
- **Underlying Report**: `DHCDCR_PUSH_CDS_DELTA`
- **Function**: Extracts records from the Subscriber logging table and pushes them into the Resilient Data Buffer (RDB), preparing them for transmission to Datasphere
- **Required Status**: Must show **green** status icon
- **Failure Impact**: If not green, even though CDC is capturing and reconstructing data, it never reaches the buffer or Datasphere

**Job Recovery**
- If either job shows a non-green status (red, yellow, or stopped):
  - Click the **Dispatcher Job** button to trigger immediate rescheduling
  - The system will attempt to restart the job within seconds
  - Refresh the tab to verify the status icon returns to green
- If status does not recover after rescheduling, proceed to Application Log

**Application Log Integration**
- Click the **Application Log** button to jump to SLG1 (System Log)
- Displays detailed error messages from the most recent job execution
- Essential for understanding why a job failed to complete

### Key Parameters (from Job Settings)

The Job Settings tab also displays configuration parameters that control job behavior and performance:

**Observer Job Parallelism and Scheduling**
- **OBSERVER_MAX_JOBS / OBSERVER_MIN_JOBS**: Number of parallel Observer job instances (default typically 1-4)
- **OBSERVER_MIN_RUNTIME**: Minimum duration a job waits for new records before terminating
- **OBSERVER_PERIOD**: Time interval between job start attempts (controls scheduling frequency)

**Transfer Job Parallelism and Performance**
- **TRANSFER_MAX_JOBS / TRANSFER_MIN_JOBS**: Number of parallel Transfer job instances
- **Tuning Note**: SAP Note 3223735 recommends increasing `TRANSFER_MAX_JOBS` to 4-8 for high-volume scenarios to prevent RDB buffer overflow
- **TRANSFER_MAX_RUNTIME_MIN**: Maximum execution time per Transfer job instance (in minutes)

**Health Monitoring and Thresholds**
- **HEALTH_CHECK_PERIOD**: Interval (in seconds) between system health checks
- **LOGTAB_RECORDS_LIMIT**: Record count threshold at which the system raises a warning (e.g., 100,000)
- **LOGTAB_RECORDS_LIMIT_WARNING**: Alerts are triggered when actual record count exceeds this value

### Typical Error Symptoms

The following patterns in DHCDCMON indicate CDC problems requiring investigation:

1. **Subscriber Logging Table Permanently Growing**
   - Record count increases over time and does not decrease
   - Indicates the Transfer Job is not running or not consuming records
   - Check Job Status tab for Transfer Job status; if not green, reschedule via Dispatcher Job button

2. **Subscriber Worklist Shows Status B or E**
   - Status B (Blocked) suggests authorization failure or resource lock
   - Status E (Failed) indicates processing error; check Application Log for details
   - May indicate communication failure between source and Datasphere

3. **Repeating Errors in Application Log**
   - Same error message appearing across multiple job execution attempts
   - Systematic issue rather than transient failure; requires investigation of cause
   - Check SLG1 for more detailed error context

4. **Job Status Not Green (Red or Yellow)**
   - Job is inactive, failed, or in an error state
   - Reschedule via Dispatcher Job button
   - If status does not recover, review Application Log

5. **Authorization Failures**
   - Message: "User XXX is not authorized to use the dispatcher/observer process"
   - The background job user lacks necessary privileges
   - Check SU53 (Authorization Check) and review user role assignment
   - Ensure user has the `DHCDC` authorization object assigned

### Related SAP Notes

- **KBA 3365864**: "Where does information in DHCDCMON come from?" — Explains data sources and refresh behavior
- **KBA 2930269**: "ABAP CDS CDC common issues and troubleshooting" — Comprehensive CDC troubleshooting guide

---

## Transaction DHRDBMON (RDB Monitor / Data Buffer Monitor)

### Purpose

DHRDBMON provides visibility into the Resilient Data Buffer (RDB), which acts as a staging layer between the CDC Engine and Datasphere. The buffer temporarily stores captured changes, organizes them into packages, and waits for the Replication Management Service (RMS) to collect and transmit them. Use this transaction to diagnose issues where CDC is working but data is not reaching Datasphere, or when the buffer is accumulating records.

### Buffer Table Overview

The Buffer Table Overview section displays summary information for each object's buffer:

**Core Buffer Metadata**
- **Object Name**: The CDS view being replicated
- **Buffer Table Name**: Generated automatically when the object is subscribed from Datasphere; typically follows pattern `/1DH/BUF_*`
- **Producer ID**: Identifier corresponding to the Subscriber ID in DHCDCMON; useful for cross-referencing CDC and RDB state
- **Phase**: Maps to replication status in Datasphere's Replication Flow UI (e.g., "Initial", "Delta", "Complete")
- **Buffer Table Status**: Current operational state (Ready, Full, etc.)

### Buffer Table Details

Expanding a buffer table entry reveals detailed statistics:

**Capacity and Content Metrics**
- **Maximum Buffer Records**: Total record capacity the buffer can hold
- **Package Size**: Number of records grouped into each package for transmission
- **Current Number of Records**: Active records currently in the buffer
- **Records not Assigned to Package**: Count of records not yet grouped into a transmission package
  - Highlighted if this value is high relative to current records
  - Indicates data is accumulating without being organized for transmission
  - May signal RMS is not consuming packages or packages cannot form due to size constraints

**Package Processing Status**
- **Number of Packages Ready**: Packages completed and waiting for RMS to collect
  - Should appear and disappear as RMS transfers data to Datasphere
  - Accumulation indicates RMS collection failure or Cloud Connector issues
- **Number of Packages In Process**: Packages currently being transferred by RMS
  - Reflects real-time transfer activity
  - Should increase and decrease as RMS batches data

### Package Overview

The Package Overview section lists individual packages with detailed status:

**Package Information**
- **Package ID**: Unique identifier for this transmission batch
- **Status**: Current state (Ready, In Process, Transferred, etc.)
- **Number of Records**: Record count in this package
- **Last Status Change**: Timestamp of the most recent status update

**Package Accumulation Analysis**
- **Expected Behavior**: Packages should appear in READY status, then transition to IN_PROCESS, then be removed as RMS collects them
- **Accumulation Pattern**: If READY packages accumulate without being consumed (remaining in status Ready for minutes), indicates RMS or Cloud Connector is not polling or collecting
- **Performance Bottleneck**: If packages accumulate while in IN_PROCESS status, indicates slow network or Datasphere ingest capacity issue

### Expert Functions

The Package Overview tab includes action buttons for manual intervention:

- **Delete Package**: Removes a package and its records from the buffer (use cautiously; may lose data)
- **Change Status to Ready**: Forces a package back to Ready status for retransmission
- **Remove Records from Package**: Deletes specific records from a package

Use these sparingly; they are diagnostic aids rather than routine operations.

### Diagnostic Decision Tree

Use the following decision tree to isolate RDB-related issues:

**Are READY packages appearing in the Package Overview section?**

- **YES, but accumulating over time**
  - Packages are being created but not collected by RMS
  - Problem is downstream: RMS is not polling, Cloud Connector is disconnected, or Datasphere ingestion is blocked
  - Action: Check Cloud Connector status, verify RMS service health in Datasphere, review network connectivity
  - This is NOT an ABAP-side issue; focus troubleshooting on infrastructure and Datasphere

- **NO packages appearing, buffer table stays empty or has minimal records**
  - RDB is not receiving data from the CDC Engine
  - Problem is upstream: Transfer Job is not running, CDC is not capturing changes, or records are stuck in Subscriber logging table
  - Action: Check DHCDCMON Transfer Job status, verify CDC is capturing (check Subscriber logging table record count), review Application Log for errors

- **NO packages appearing, buffer table is full or filling up**
  - Data is arriving from CDC but packages are not forming or are not being marked as Ready
  - Problem is in the packaging logic or buffer is misconfigured
  - Action: Check buffer capacity settings, verify Package Size parameter, check for errors in DHRDBMON Application Log, consider manually changing package status to Ready to resume flow

---

## Transaction SLG1 (Application Log)

### Purpose

SLG1 (System Log) is the centralized application log for SAP systems. Replication Flow errors from the source S/4HANA system are logged with detailed messages, error codes, and resolution guidance. When DHCDCMON or DHRDBMON show failures, SLG1 provides the underlying cause.

### How to Use

**Step-by-Step Query Process**

1. **Obtain the Error Timestamp from Datasphere**
   - Open the failing Replication Flow in Datasphere Data Integration Monitor
   - Navigate to the Messages tab
   - Note the error timestamp (typically displayed in user's local timezone)

2. **Adjust for Time Zone Difference**
   - S/4HANA system time and Datasphere user timezone may differ
   - Open SAP GUI transaction System > Status to check the source system's current date/time
   - Calculate the offset between source system time and the timestamp you recorded
   - Adjust the query timestamps accordingly

3. **Open SLG1 on the Source System**
   - Transaction SLG1 in SAP GUI
   - Defaults to showing logs from the past 24 hours

4. **Set Date/Time Range**
   - Enter **From Date** and **From Time** (adjusted for source system timezone)
   - Enter **To Date** and **To Time** (set slightly after the error timestamp to capture surrounding context)
   - Typical window: error timestamp ± 5 minutes

5. **Execute Query**
   - Press F8 to execute
   - SLG1 retrieves matching logs

6. **Review Results and Expand Logs**
   - Logs are displayed as collapsible entries
   - Click on an entry to expand and view detailed messages
   - Multiple messages may be grouped under one log

### Important Objects to Filter

SLG1 can return hundreds of logs across many SAP components. To reduce noise, focus on these object categories relevant to Replication Flows:

- **DHADM**: Administration components and system configuration
- **DHAMB**: ABAP Management (job scheduling, process control)
- **DHAPE**: ABAP Pipeline Engine (data transformation and extraction)
- **DHBAS**: Base Framework (core replication infrastructure)
- **DHCDC**: Change Data Capture (logging table operations, view reconstruction)
- **DHODP**: Operational Data Provisioning (legacy extraction framework)
- **DHRDB**: Resilient Data Buffer (packaging, transmission staging)

Filter by entering one of these object codes in the Object field to narrow results to Replication-specific logs.

### Reading Error Details

**Accessing Detailed Error Messages**
- Click the yellow question mark icon (?) or magnifying glass icon next to a log entry
- Opens a detailed message view with full error context

**Message Components**
- **Message Class (sy-msgid)**: Classification code (e.g., `DH`, `00`)
- **Message Number (sy-msgno)**: Specific error number within the class
- **Cause Description**: Explanation of what triggered the error
- **System Response**: What the system did in response
- **Resolution Instructions**: Suggested corrective actions
- **Searchable Keywords**: Tags for finding related documentation

**Long Text Reading**
- Some messages contain extensive long text with step-by-step instructions
- Scroll or expand the text area to view complete content
- Print or export messages if needed for analysis outside SAP

### Important Note: Search Limitations

- **Critical Limitation**: SLG1 does NOT support free-text search
- Filtering is based only on time ranges, object codes, and external identifiers
- To find errors related to a specific object (e.g., a CDS view name), you must:
  - Search within a narrow time window (reducing results manually)
  - Use object code filtering to limit to relevant components
  - Scan results manually or export to spreadsheet for offline analysis

**Time Zone Precision is Critical**
- Always adjust timestamps for source system timezone
- A ±10 minute error can result in missing relevant logs
- When unsure of exact time, query a wider window (±15 minutes) to avoid missing data

---

## Cross-Tool Diagnostic Workflow

For a failing Replication Flow, follow this systematic investigation sequence to isolate the component causing the issue:

**Step 1: Capture Initial Error Information**
- Open Datasphere Data Integration Monitor
- Navigate to the failing Replication Flow's Messages tab
- Record the error message text and timestamp
- Note the object name (CDS view being replicated)

**Step 2: Check RDB Status (Downstream of CDC)**
- Open DHRDBMON on the source system
- Search for the object by name
- Questions to answer:
  - Are READY packages accumulating? (indicates RMS/Cloud Connector issue)
  - Is the buffer table empty? (indicates CDC not pushing data)
  - Is the buffer table full? (indicates packaging or downstream bottleneck)

**Step 3: Check CDC Status (Data Capture)**
- Open DHCDCMON on the source system
- Search for the object
- Questions to answer:
  - Is the Subscriber logging table growing? (indicates Transfer Job not running)
  - Are any Subscriber Worklist entries in status B or E? (indicates job failure)
  - Are both Observer Job and Transfer Job showing green status?

**Step 4: Retrieve Detailed Error Context**
- Open SLG1 on the source system
- Enter adjusted timestamp range and filter by object code (DHCDC, DHRDB, DHAPE, or DHBAS)
- Find matching error log entries
- Expand entries to read the detailed error message with cause and resolution

**Step 5: Test CDC Outside of Datasphere (If CDC Issue Suspected)**
- If DHCDCMON shows logging table growth or job failures, test the CDS view independently
- Open RODPS_REPL_TEST on the source system
- Test the CDS view to confirm CDC replication works outside of Datasphere context
- If test fails, the issue is in the CDS view definition or CDC configuration, not in Datasphere

**Step 6: Check Operational Data Queue (If ODP Involved)**
- For some CDS views, Operational Data Provisioning (ODP) is the underlying extraction mechanism
- Open ODQMON on the source system
- Monitor queue status and extraction counters for the object
- Confirms whether ODP subscribers are receiving data

**Decision Logic**
- **Problem in steps 3-4 (DHCDCMON or SLG1)**: Issue is on the ABAP source system; fix CDC configuration, job scheduling, or authorization
- **Problem in step 2 (DHRDBMON)**: Issue is either upstream (CDC not pushing) or downstream (RMS not collecting)
  - Check step 3 to determine which
- **Problem passes steps 2-4 but fails in step 5 (RODPS_REPL_TEST)**: CDS view definition has an issue incompatible with Datasphere replication
- **All steps pass on source system**: Problem is in Datasphere, Cloud Connector, or network

---

## Additional Diagnostic Tools

Beyond the primary CDC and RDB transactions, several other tools provide complementary diagnostic information:

### SDDLAR (DDL Source Tool)
- **When to Use**: When CDC is failing due to CDS view definition issues
- **Capabilities**:
  - Display DDL Source: View the ABAP CDS definition syntax
  - Check DDL Source: Validate syntax without compilation
  - Data Preview: Execute the CDS view to test data retrieval
- **Diagnostic Value**: Confirms whether the CDS view itself is valid and executable

### RODPS_REPL_TEST (Replication Test Tool)
- **When to Use**: When CDC replication is failing in the context of Datasphere, but you want to isolate whether the CDC engine or CDS view is the problem
- **Function**: Tests CDS view replication outside of Datasphere context
- **Expected Behavior**: Successful test indicates the CDS view and CDC engine are healthy; failure points to CDS definition or CDC configuration issues

### ODQMON (Operational Data Queue Monitor)
- **When to Use**: For CDS views that use ODP (Operational Data Provisioning) as the underlying extraction mechanism
- **Visibility**: Queue status, subscriber count, extraction counters, and request history
- **Diagnostic Value**: Confirms whether ODP is successfully extracting and queuing data

### SM37 (Background Job Log)
- **When to Use**: When DHCDCMON shows job failures
- **Actions**:
  - Verify job status (completed, failed, running)
  - Review job logs and execution history
  - Check job scheduling parameters
  - Manually trigger job execution for testing

### SU53 (Authorization Check)
- **When to Use**: When errors mention "User XXX is not authorized"
- **Function**: Shows the last failed authorization check for the current user
- **Diagnostic Value**: Identifies missing authorization objects or role assignments

### STAUTHTRACE (Authorization Trace)
- **When to Use**: When SU53 does not provide sufficient detail
- **Function**: Enables detailed trace of authorization checks for a specific user or transaction
- **Diagnostic Value**: Shows every authorization check evaluated, which object failed, and why

---

## Summary Table: Transaction Reference

| Transaction | Component | Primary Use | Key Actions |
|---|---|---|---|
| DHCDCMON | CDC Engine | Monitor change capture | Check job status, review logging tables, reschedule jobs |
| DHRDBMON | RDB Buffer | Monitor data staging | Check package status, review buffer capacity |
| SLG1 | Logs | Find error details | Query by time range and object code |
| SDDLAR | CDS Metadata | Validate view definition | Display source, check syntax, preview data |
| RODPS_REPL_TEST | CDC Testing | Test outside Datasphere | Confirm CDC engine capability |
| ODQMON | ODP Queue | Monitor queue status | Check extraction count and queue depth |
| SM37 | Jobs | Monitor background jobs | Check Observer/Transfer job logs |
| SU53 | Authorization | Check failed permissions | Identify missing authorizations |
| STAUTHTRACE | Authorization | Trace permission checks | Debug authorization failures |
