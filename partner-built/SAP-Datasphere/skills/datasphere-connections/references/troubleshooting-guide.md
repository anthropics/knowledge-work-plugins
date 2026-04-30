# Connection Troubleshooting Guide

## Cloud Connector Troubleshooting

### Required Access Paths for S/4HANA On-Premise
When configuring Cloud Connector for Datasphere, these paths must be allowed:

| Path | Access Type | Purpose |
|------|------------|---------|
| /sap/bw/ina | Path and all sub-paths | InA protocol for model transfer and metadata |
| /sap/opu/odata/sap/ESH_SEARCH_SRV/* | All sub-paths | Enterprise Search for entity discovery |
| /sap/opu/odata4/sap/csn_exposure_v4 | Path and all sub-paths | CSN Exposure for model import |
| /sap/bw4/v1/dwc/* | All sub-paths | BW/4HANA model transfer (if applicable) |

### Common Cloud Connector Issues
1. **Path not configured**: Connection validates but model import or replication fails — check that ALL required paths are added, not just the base URL
2. **Header configuration missing**: CORS requests fail — ensure proper header forwarding in Cloud Connector access control
3. **SSL/TLS certificate errors**: Certificate chain incomplete or expired — check trust store in Cloud Connector administration
4. **Authentication failures**: Verify backend user credentials in Cloud Connector, check password expiry
5. **Location ID mismatch**: If multiple Cloud Connectors exist, ensure Datasphere connection references the correct Location ID

### Validation Checklist
- Connection shows "Replication flows are enabled" ✓
- Connection shows "Data flows are enabled" ✓
- Model Import shows either enabled or disabled (not error) ✓
- Remote tables shows status ✓
- If validation fails: SAP KBA 3369433

## Data Provisioning Agent Troubleshooting

### Installation Prerequisites
- Version 2.6.3 or higher required for latest Datasphere features
- Java Runtime Environment (JRE) installed
- Network access from agent to both source system and Datasphere

### IP Allowlisting
- Agent machine's IPv4 address (public IP) must be added to Datasphere IP allowlist
- System → Configuration → IP Allowlist
- See SAP KBA 3276488 for allowlist configuration
- See SAP KBA 2894588 for IP allowlist details

### Agent Registration
1. Install agent on a machine with network access to source system
2. Configure agent connection to Datasphere
3. Register required adapters (SAP HANA, ABAP, etc.)
4. Verify registration in Datasphere → System → Configuration → Data Provisioning Agents

### Common DP Agent Issues
1. **Agent not visible in Datasphere**: Check IP allowlist, verify agent is running, check network connectivity
2. **Adapter registration fails**: Verify adapter compatibility, check agent logs
3. **JCO exceptions**: Enable JCO trace in DP Agent for detailed connection diagnostics (see SAP Note 2938870)
4. **Connection timeouts**: Check firewall rules between agent machine and source system
5. **Agent upgrade issues**: Stop agent before upgrade, verify Java compatibility after upgrade

### DP Agent Log Analysis
- Agent logs located in the agent installation directory
- Enable JCO trace for SAP system connectivity issues
- Check for connection pool exhaustion on high-throughput scenarios
- SAP Note 3196950 for comprehensive DP Agent troubleshooting

## CORS Configuration (for S/4HANA Backend)

### Temporary Enable (testing)
1. Transaction RZ11 → Parameter: icf/cors_enabled → Set to 1
2. Requires ABAP AS restart to take effect

### Permanent Enable (production)
1. Transaction rz10 → Profile: DEFAULT → Extended Maintenance
2. Create parameter: icf/cors_enabled = 1
3. Restart ABAP Application Server

### CORS Allowlist
1. Transaction UCONCOCKPIT
2. HTTP Allowlist Scenario
3. Add service path (e.g., /sap/bw/ina)
4. Configure allowed headers and methods

## S/4HANA CSN Exposure Service Prerequisites (BASIS >= 756)

### Required Software Components
- SAP_BASIS 756 or higher
- SAP_ABA
- SAP_BW (for BW/4HANA model transfer)
- Pre-requisite SAP Notes from SAP Note 3463326

### Required Search Connectors
Verify in transaction ESH_TEST_SEARCH (F4 on Connector ID, search "csn"):
- CSN_EXPOSURE_CDS_DEFAULT_FT
- CSN_EXPOSURE_CDS_DEFAULT_NFT
- SSCH_CMS_CDS_DESC_FT
- SSCH_CMS_CDS_DESC_NFT
- CSN_EXPOSURE_CDS

If missing, activate using report ESH_CDSABAP_ACTIVATION.

### Required Services
- CSN_EXPOSURE_V4: Check in /iwfnd/v4_admin → Published Services. If missing, use "Publish Service Groups"
- ESH_SEARCH_SRV: Check in /iwfnd/maint_service → Active Services. If missing, use "Add Service"

### Required Authorizations for Communication User
- SDDLVIEW: DDLSRCNAME = CSN_EXPOSURE_* entities, ACTVT = 03
- S_SERVICE: SRV_NAME = EF608938F3EB18256CE851763C2952, SRV_TYPE = HT
- S_START: AUTHPGMID = R3TR, AUTHOBJTYP = G4BA, AUTHOBJNAM = CSN_EXPOSURE_V4
- S_SDSAUTH: ACTVT = 16 (Execute)

## OData API Troubleshooting

### Authentication Errors
- Verify OAuth client configuration in Datasphere
- Check token endpoint URL format
- Confirm client ID and secret
- SAP KBA 3318090 for authentication error resolution

### Common OData Issues
1. **404 Not Found**: Verify the exact entity set name and URL path
2. **403 Forbidden**: Check user authorizations and Data Access Controls
3. **500 Internal Server Error**: Check Datasphere system logs, verify view deployment
4. **Timeout**: Reduce query scope, add filters, check view complexity

## ODBC Connection Issues

### Driver Installation
- Download HANA ODBC driver from SAP Development Tools
- Extract .SAR file using SAPCAR utility
- Configure ODBC DSN in Windows ODBC Administrator (64-bit)

### Common ODBC Issues
1. **Connection refused**: Verify hostname and port, check IP allowlist
2. **Authentication failed**: ODBC credentials are Database User credentials, NOT Datasphere login
3. **Schema not visible**: Verify Database User has required space schema access
4. **Multi-space access**: Requires Database User Group with cross-space grants

## Key SAP Notes
| Note | Description |
|------|-------------|
| 3369433 | Cloud Connector troubleshooting for Datasphere |
| 3276488 | IP Allowlist configuration |
| 2894588 | IP Allowlist details |
| 2938870 | DP Agent errors with Datasphere |
| 3196950 | DP Agent troubleshooting guide |
| 3463326 | S/4HANA CSN Exposure prerequisites |
| 3318090 | OData API authentication errors |
| 3383634 | BW/4HANA Model Import |
