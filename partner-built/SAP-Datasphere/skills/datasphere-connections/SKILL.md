---
name: datasphere-connections
description: SAP Datasphere connections skill for creating and managing data source connections. Use when configuring connections to SAP systems (S/4HANA, BW, ECC), cloud databases (BigQuery, Redshift, Azure SQL), or other data sources for use in views, data flows, and replication.
---

# SAP Datasphere Connections

Skill for creating and managing connections to data sources in SAP Datasphere. Connections enable access to SAP and non-SAP systems for data federation, replication, and ETL operations.

## Navigation Overview

**Path:** Left Menu → Connections → `#/connections`

Connections are space-scoped - you must select a space before viewing or creating connections.

## Connection Types (35 Available)

### SAP Sources
| Connection Type | Features | Use Case |
|----------------|----------|----------|
| SAP ABAP | Remote Tables, Replication, Data Flows | Connect to SAP ERP systems |
| SAP S/4HANA Cloud | Remote Tables, Replication, Data Flows | S/4HANA Cloud integration |
| SAP S/4HANA On-Premise | Remote Tables, Replication, Data Flows | On-prem S/4HANA systems |
| SAP BW | Remote Tables, Model Import | BW/4HANA integration |
| SAP BW/4HANA Model Transfer | Model Import | Import BW models |
| SAP ECC | Remote Tables, Replication | Legacy ECC systems |
| SAP HANA | Remote Tables, Replication, Data Flows | Direct HANA connectivity |
| SAP SuccessFactors | Data Flows | HR data integration |
| SAP Fieldglass | Data Flows | Vendor management data |
| SAP Marketing Cloud | Data Flows | Marketing data |
| SAP Signavio | Data Flows | Process mining data |
| Cloud Data Integration | Data Flows | SAP CDI sources |

### Cloud Databases
| Connection Type | Features | Use Case |
|----------------|----------|----------|
| Google BigQuery | Remote Tables, Data Flows | GCP analytics |
| Amazon Redshift | Remote Tables, Data Flows | AWS data warehouse |
| Amazon Athena | Remote Tables, Data Flows | S3 query service |
| Microsoft Azure SQL Database | Remote Tables, Data Flows | Azure SQL |
| Microsoft Azure Data Lake Gen2 | Data Flows | Azure storage |
| Microsoft Azure Blob Storage | Data Flows | Azure blobs |
| Microsoft OneLake | Data Flows | Fabric integration |
| Oracle | Remote Tables, Data Flows | Oracle databases |

### Storage & Streaming
| Connection Type | Features | Use Case |
|----------------|----------|----------|
| Amazon S3 | Data Flows | AWS object storage |
| Google Cloud Storage | Data Flows | GCP object storage |
| Generic SFTP | Data Flows | File transfers |
| Apache Kafka | Data Flows | Event streaming |
| Confluent | Data Flows | Managed Kafka |

### Generic Connectors
| Connection Type | Features | Use Case |
|----------------|----------|----------|
| Generic JDBC | Remote Tables, Data Flows | Any JDBC source |
| Generic OData | Remote Tables, Data Flows | OData services |
| Generic HTTP | API Tasks | REST APIs |
| Open Connectors | Data Flows | Third-party via SAP Open Connectors |

## Creating a Connection

### Step-by-Step Process

1. **Navigate to Connections**
   - Left Menu → Connections
   - Select target space from the space cards

2. **Start Connection Wizard**
   - Click **+** dropdown → **Create Connection**
   - Wizard opens with 3 steps

3. **Step 1: Choose Connection Type**
   - Use filters to narrow options:
     - Features: API Tasks, Data Flows, Model Import, Remote Tables, Replication Flows
     - Categories: Cloud, On-Premise
     - Sources: Non-SAP, Partner Tools, SAP
   - Click on desired connection type tile

4. **Step 2: Configure Connection Properties**
   - **Connection Details:**
     - Category (Cloud/On-Premise)
     - Host (server address)
     - Port (service port)
   - **Authentication:** Select method
     - User Name and Password
     - X.509 Client Certificate
     - OAuth 2.0
   - **Features:**
     - Remote Tables: Enable/disable virtual access
     - Data Provisioning: Direct or via DP Agent
     - Data Access: Remote, Replication, or both
   - Click **Next Step**

5. **Step 3: Enter Name and Description**
   - Business Name (display name)
   - Technical Name (system identifier)
   - Description (optional)
   - Click **Create**

### Authentication Methods

| Method | When to Use |
|--------|-------------|
| User Name and Password | Basic auth, service accounts |
| X.509 Client Certificate | Certificate-based, high security |
| OAuth 2.0 | Cloud services, SSO integration |
| SAP Assertion Ticket | SAP-to-SAP trusted communication |

## Managing Connections

### Connection Actions
| Action | Description |
|--------|-------------|
| Edit | Modify connection properties |
| Delete | Remove connection (requires no dependencies) |
| Validate | Test connection connectivity |
| Pause | Temporarily disable replication |
| Restart | Resume paused replication |

### Connection Status
- **Connected:** Active and working
- **Disconnected:** Configuration issue or source unavailable
- **Paused:** Manually paused replication

## Remote Tables

When a connection supports Remote Tables:

1. **In Data Builder:**
   - Open a space in Data Builder
   - Click **Sources** panel
   - Expand connection to see available tables
   - Drag table to canvas → creates Remote Table

2. **Remote Table Options:**
   - **Federation:** Virtual access (query on demand)
   - **Replication:** Copy data to local storage
   - **Snapshot:** Point-in-time copy

### Replication Settings
- **Real-Time:** Continuous change capture
- **Scheduled:** Periodic full/delta loads
- **Manual:** On-demand refresh

## SAP Open Connectors

For third-party data sources not directly supported:

1. Navigate to Connections → SAP Open Connectors tab
2. Click **Integrate your SAP Open Connectors Account**
3. Configure SAP Open Connectors instance
4. Access 150+ pre-built connectors

## Best Practices

### Connection Naming
- Use descriptive business names
- Include environment indicator (DEV, TEST, PROD)
- Example: "S4HANA_Finance_PROD"

### Security
- Use service accounts, not personal credentials
- Rotate credentials regularly
- Use certificates where supported
- Limit connection access via space membership

### Performance
- Enable replication for frequently accessed data
- Use federation for large, infrequently queried tables
- Consider data freshness requirements

## Troubleshooting

### Connection Fails to Validate
1. Verify host/port are correct
2. Check firewall rules (Cloud Connector if on-prem)
3. Validate credentials
4. Test network connectivity

### Replication Errors
1. Check Data Integration Monitor for details
2. Verify source system availability
3. Review space storage capacity
4. Check for schema changes in source

## Resources

See reference files for detailed procedures:
- `references/connection-types.md` - Detailed connection type configurations
- `references/authentication.md` - Authentication setup guides
- `references/troubleshooting-guide.md` - Cloud Connector path configuration, Data Provisioning Agent troubleshooting, CORS setup, CSN Exposure prerequisites, OData/ODBC diagnostics
