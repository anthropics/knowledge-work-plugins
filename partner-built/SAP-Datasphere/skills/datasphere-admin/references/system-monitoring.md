# System Monitoring Reference

## Table of Contents
1. [Dashboard Overview](#dashboard-overview)
2. [Storage Monitoring](#storage-monitoring)
3. [Task Logs](#task-logs)
4. [Statement Logs](#statement-logs)
5. [Memory Management](#memory-management)
6. [Elastic Compute Nodes](#elastic-compute-nodes)
7. [Troubleshooting Guide](#troubleshooting-guide)

## Dashboard Overview

### Accessing System Monitor
Path: Left Menu → System Monitor → System Monitor

### Dashboard Layout
The dashboard displays real-time and historical metrics:

| Card | Metric | Time Range |
|------|--------|------------|
| Disk Storage Used | Pie chart breakdown | Now |
| Disk Used by Spaces | Usage vs quota | Now |
| Memory Used by Spaces | Usage vs quota | Now |
| Failed Tasks | Count | Last 24 Hours |
| Out-of-Memory Errors | Count | Last 24 Hours |
| Top 5 OOM by Space | Space breakdown | Last 7 Days |
| Admission Control Events | Rejection/Queuing | Last 24 Hours |

### Storage Categories
- **Other Data:** System and operational data
- **Data in Spaces:** User space data
- **Administrative Data:** Metadata and configurations
- **Audit Log Data:** Activity logging

## Storage Monitoring

### Disk Storage Metrics
- Total allocated vs used
- Breakdown by category
- Trend analysis available

### Memory Storage Metrics
- In-memory table usage
- Per-space breakdown
- Warm vs cold data

### Capacity Planning Indicators
- Red: >90% utilization (critical)
- Yellow: 70-90% utilization (warning)
- Green: <70% utilization (healthy)

## Task Logs

### Accessing Task Logs
1. System Monitor → System Monitor
2. Click **Task Logs** tab

### Task Types Logged
- Data Flow executions
- Replication Flow runs
- Transformation Flow operations
- View persistence tasks
- Task Chain executions

### Filtering Options
| Filter | Options |
|--------|---------|
| Space | All spaces or specific |
| Task Type | Flow type selection |
| Status | Running, Completed, Failed |
| Date Range | Custom date selection |

### Task Details View
Click on a task row to see:
- Start/end timestamps
- Duration
- Records processed
- Error messages (if failed)
- Step-by-step execution log

## Statement Logs

### Accessing Statement Logs
1. System Monitor → System Monitor
2. Click **Statement Logs** tab

### Logged Statements
- SQL queries
- DDL operations
- DML operations

### Analysis Capabilities
- Execution time analysis
- Resource consumption
- Query optimization hints

### Filtering Statements
- By user
- By statement type
- By execution time threshold
- By date range

## Memory Management

### Out-of-Memory (OOM) Errors
Dashboard shows:
- OOM count (last 24 hours)
- Top 5 spaces by OOM (last 7 days)
- MDS request failures

### Causes of OOM
- Large data loads
- Complex queries
- Insufficient memory quota
- Multiple concurrent operations

### Resolution Steps
1. Identify affected space from dashboard
2. Review Task Logs for failing operations
3. Options:
   - Increase space memory quota
   - Optimize query/model
   - Schedule during off-peak
   - Use Elastic Compute Nodes

## Elastic Compute Nodes

### Monitoring ECN
Path: System Monitor → Elastic Compute Nodes tab

### Metrics Available
- Active nodes
- Block-hours consumed
- Usage by space

### ECN Best Practices
- Use for burst workloads
- Monitor consumption trends
- Plan block-hour budgets

## Troubleshooting Guide

### Failed Task Investigation
1. System Monitor → Task Logs
2. Filter: Status = Failed
3. Click task for details
4. Review error message
5. Common resolutions:
   - Connection timeout: Check source availability
   - Memory error: Increase quota or optimize
   - Permission error: Verify user roles

### Slow Performance Investigation
1. System Monitor → Statement Logs
2. Sort by execution time
3. Identify slow queries
4. Options:
   - Add indexes
   - Optimize joins
   - Partition large tables
   - Persist frequently accessed views

### Storage Capacity Issues
1. Dashboard → Check utilization percentages
2. Identify top consumers by space
3. Options:
   - Archive old data
   - Delete unused objects
   - Increase storage quotas
   - Compress data

### Admission Control Events
Indicates resource contention:
- **Rejection Events:** Requests denied due to resource limits
- **Queuing Events:** Requests waiting for resources

Resolution:
- Stagger scheduled tasks
- Increase capacity
- Optimize resource-heavy operations
