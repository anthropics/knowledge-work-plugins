# S/4HANA Integration Reference Guide

## Common S/4HANA CDS Views by Functional Area

### Finance Module (FI/CO)

| View Name | Description | Key Fields | Delta Support | Typical Volume |
|-----------|-------------|-----------|---|---|
| C_GENERALLEDGER | General ledger transactions | Company Code, Account, Amount, Date | Yes | 100M-500M |
| C_ACCOUNT_MASTER | Chart of accounts | Company Code, Account, Type, Currency | No | 10K-100K |
| C_COSTCENTER | Cost center master | Cost Center, Name, Manager | No | 1K-10K |
| C_PROFITCENTER | Profit center master | Profit Center, Name, Controller | No | 100-1K |
| C_CUSTOMER_INVOICE | Customer invoices | Invoice#, Customer, Amount, Date | Yes | 10M-50M |
| C_SUPPLIER_INVOICE | Vendor invoices | Invoice#, Vendor, Amount, Date | Yes | 10M-50M |
| C_PAYMENT_HISTORY | Payment transactions | Payment#, Customer/Vendor, Date | Yes | 5M-20M |
| C_BANK_RECONCILIATION | Bank transactions | Bank Account, Transaction, Date | Yes | 1M-10M |

**Extraction Recommendation:**
- Use ODP for all transactions with delta enabled
- Full load for masters (daily or weekly)
- Delta frequency: 15 minutes for transactions

### Sales Module (SD)

| View Name | Description | Key Fields | Delta Support | Typical Volume |
|-----------|-------------|-----------|---|---|
| C_CUSTOMER | Customer master | Customer#, Name, Region, Currency | Yes | 10K-100K |
| C_SALES_ORDER | Sales orders | Order#, Customer, Date, Amount | Yes | 100K-1M |
| C_SALES_ORDER_ITEM | Order line items | Order#, Item#, Material, Qty, Price | Yes | 1M-10M |
| C_INVOICE | Customer invoices | Invoice#, Customer, Date, Amount | Yes | 100K-1M |
| C_CREDIT_MEMO | Credit memos | Memo#, Customer, Amount, Reason | Yes | 10K-100K |
| C_DELIVERY | Deliveries | Delivery#, Order#, Date, Status | Yes | 100K-1M |
| C_SALES_FORECAST | Sales forecasts | Customer, Material, Month, Qty | Yes | 100K-1M |

**Extraction Recommendation:**
- Delta enabled for all documents
- 5-minute frequency for real-time sales dashboards
- Use for sales analytics, AR aging, pipeline tracking

### Procurement Module (MM/PO)

| View Name | Description | Key Fields | Delta Support | Typical Volume |
|-----------|-------------|-----------|---|---|
| C_SUPPLIER | Supplier master | Supplier#, Name, Region, Currency | Yes | 1K-10K |
| C_PURCHASE_ORDER | Purchase orders | PO#, Supplier, Date, Amount | Yes | 100K-1M |
| C_PURCHASE_ORDER_ITEM | PO line items | PO#, Item#, Material, Qty, Price | Yes | 1M-10M |
| C_SUPPLIER_INVOICE | Vendor invoices | Invoice#, Supplier, Date, Amount | Yes | 10M-50M |
| C_MATERIAL | Material master | Material#, Description, Type, UOM | No | 10K-100K |
| C_MATERIAL_STOCK | Inventory balances | Plant, Material, Qty, Value | Yes | 100K-1M |
| C_PURCHASE_REQUISITION | Purchase requisitions | PR#, Date, Requester, Amount | Yes | 100K-1M |

**Extraction Recommendation:**
- Masters: Full load daily or weekly
- Transactions: Delta every 5-15 minutes
- Stock: Delta with high frequency (5 min) if needed for inventory management

### Human Resources (HR)

| View Name | Description | Key Fields | Delta Support | Typical Volume |
|-----------|-------------|-----------|---|---|
| C_EMPLOYEE | Employee master | Employee#, Name, Department, Manager | Yes | 1K-10K |
| C_EMPLOYEE_SALARY | Salary information | Employee#, Period, Amount, Currency | Yes | 100K-1M |
| C_EMPLOYEE_TIME | Time tracking | Employee#, Date, Hours, Activity | Yes | 1M-10M |
| C_ORGANIZATIONAL_UNIT | Org structure | Org Unit#, Name, Parent, Manager | No | 100-1K |
| C_EMPLOYEE_SKILL | Skill master | Employee#, Skill, Level, Date | Yes | 10K-100K |

**Extraction Recommendation:**
- Masters: Weekly full load
- Transactions: Daily delta
- Use for HR analytics, headcount, skill gap analysis

### Supply Chain Module (SCM)

| View Name | Description | Key Fields | Delta Support | Typical Volume |
|-----------|-------------|-----------|---|---|
| C_DEMAND | Demand forecast | Product, Region, Month, Quantity | Yes | 100K-1M |
| C_SUPPLY | Supply availability | Plant, Material, Date, Quantity | Yes | 100K-1M |
| C_PURCHASE_REQUISITION | PR forecast | Date, Material, Quantity, Required Date | Yes | 100K-1M |

## CDS Annotation Reference

### Complete Annotation Examples

**Complete C_CUSTOMER Example:**
```abap
@VDM.viewType: #CONSUMPTION
@VDM.Datalake:true
@Analytics.dataCategory: #DIMENSION
@Analytics.dataExtraction.enabled: true
@Analytics.dataExtraction.deltaSupported: true

@ObjectModel.readOnly: true
@ObjectModel.usageType: #DOCUMENT
@ObjectModel.semanticKey: ['CustomerID']
@ObjectModel.Composition.RefreshingElement: true

@Semantics.businessKey: true
@Semantics.text: {element: ['CustomerName']}

@EndUserText.label: 'Customer Master'
@EndUserText.description: 'Extraction-enabled customer master data for analytics'
@EndUserText.quickInfo: 'Customer dimensions for sales and finance'

@UI.headerInfo: { typeName: 'Customer', typeNamePlural: 'Customers' }

define view C_CUSTOMER as
  select from kna1 {
      @Semantics.businessKey: true
      kna1.kunnr as CustomerID,

      @Semantics.text: true
      kna1.name1 as CustomerName,

      kna1.ort01 as City,

      @Semantics.location.longitude: true
      kna1.location_lon as Longitude,

      @Semantics.location.latitude: true
      kna1.location_lat as Latitude,

      @Semantics.amount.currencyCode: 'CurrencyCode'
      kna1.netwr as NetAnnualRevenue,

      kna1.waers as CurrencyCode,

      kna1.erdat as CreatedDate,

      @Semantics.systemDateTime.lastChangedAt: true
      kna1.aedat as LastChangedDate
  };
```

### Annotation Quick Reference Table

| Annotation | Purpose | Example |
|-----------|---------|---------|
| @VDM.viewType | Defines view layer | #CONSUMPTION (exposed), #INTERNAL, #DERIVED |
| @Analytics.dataCategory | Data role | #FACT, #DIMENSION, #CUBE, #QUERY |
| @Analytics.dataExtraction.enabled | Enable extraction | true/false |
| @Analytics.dataExtraction.deltaSupported | Delta capable | true/false |
| @ObjectModel.readOnly | Prevents writes | true/false |
| @ObjectModel.semanticKey | Unique identifier | ['Field1', 'Field2'] |
| @Semantics.businessKey | Business identifier | true/false |
| @Semantics.text | Description field | {element: ['FieldName']} |
| @Semantics.amount.currencyCode | Currency field | 'CurrencyField' |
| @Semantics.quantity.unitOfMeasure | Unit field | 'UOMField' |
| @Semantics.calendar.date | Date semantics | true/false |
| @EndUserText.label | User-friendly name | 'Customer Master' |
| @EndUserText.description | Detailed description | 'Customer master data...' |

## ODP Extractor Configuration

### ODP Context Types

```
ABAP:CDS_VIEWS
├── Source: ABAP CDS Views
├── Providers: All extraction-enabled views (C_*)
├── Delta: Yes, via ODP change log
└── Best For: Standard extraction

SAP_HANA:CALCULATION_VIEWS
├── Source: SAP HANA calculation views
├── Providers: Published views
├── Delta: Limited
└── Best For: Pre-calculated aggregates

BW:INFOPROVIDER
├── Source: BW InfoProviders
├── Providers: Cubes, DSO, InfoObjects
├── Delta: Yes, via BW requests
└── Best For: Integrated BW data

LOGICAL_LOG
├── Source: Application change logs
├── Providers: Business transactions
├── Delta: Event-based
└── Best For: Audit trail, compliance
```

### ODP Configuration Best Practices

**Enable Change Log in Source System:**
```
S/4HANA → SPRO → Source System Settings → ODP
└─ Activate change logging for CDS views:
   - Set retention period: 8 days
   - Set log size limit: 4GB
   - Set parallel write threads: 4
```

**Define ODP Extractor:**
```xml
ODP Provider Configuration:
  <ODPPROVIDER>
    <ContextID>ABAP:CDS_VIEWS</ContextID>
    <ObjectName>C_CUSTOMER</ObjectName>
    <Extraction>
      <Type>FULL_THEN_DELTA</Type>
      <InitialLoading>FULL</InitialLoading>
      <DeltaType>CHANGE_LOG</DeltaType>
      <SelectableFields>
        <Field Name="CUSTOMER_ID" Key="true" Changeable="false"/>
        <Field Name="CUSTOMER_NAME" Key="false" Changeable="true"/>
      </SelectableFields>
    </Extraction>
  </ODPPROVIDER>
```

**ODP Request Semantics:**
```
Request Concept in ODP:
  - Request = Batch of extractions for a run
  - Request ID = Uniquely identifies extraction batch
  - Watermark = Position within change log
  - Delta Request = Request for changes since last run

Full Load Request:
  SELECT_ALL = true
  FROM_CHANGENUMBER = 0
  Result: All records

Delta Request:
  SELECT_ALL = false
  FROM_CHANGENUMBER = 1000000
  Result: Only changes since change number 1000000
```

## Cloud Connector Setup Checklist

### Pre-Installation

- [ ] VM allocated: 4GB RAM minimum, 100GB storage
- [ ] Network: VM can reach S/4HANA system
- [ ] Java: JDK 11 or 17 installed and JAVA_HOME set
- [ ] SSL Certificate: Valid certificate for CC domain or self-signed accepted
- [ ] Firewall: Port 8443 (admin UI), port 443 (backend)
- [ ] User: Admin user for CC installation

### Installation Steps

```bash
# 1. Download Cloud Connector
cd /opt/sap
wget https://tools.hana.ondemand.com/additional/sapcc-latest.tar.gz
tar -xzf sapcc-latest.tar.gz

# 2. Set environment
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk
export PATH=$PATH:$JAVA_HOME/bin

# 3. Start Cloud Connector
cd /opt/sap/scc
./go.sh start

# 4. Access Admin UI
# https://localhost:8443/admin
# Default: Administrator / manage
```

### Configuration Steps

**1. Add Backend System:**
```
Admin Console → Cloud Connectors → Connector Group
→ Connected Backend Systems → +
Name: SAP_S4H_PROD
Type: SAP System
Host: s4h-prod.example.com
Port: 443
Principal Type: User Name/Password
User: DATASPH_TECH
Password: [encrypted in CC]
```

**2. Add Resource Mapping:**
```
Resource: /sap/opu/odata/sap/*
Check: YES (Allow)
Semantics: Access allowed
Protocol: HTTP/HTTPS

Resource: /sap/bc/odata/v4/*
Check: YES
Protocol: HTTP/HTTPS

Resource: /sap/bc/adt/*
Check: YES
Protocol: HTTP/HTTPS
```

**3. Configure High Availability:**
```
Multiple Cloud Connectors:
CC1: Primary (Active)
CC2: Standby (Passive)

Configure in Datasphere:
Connection Settings → Cloud Connector
Connector Group: SCC_GROUP_PROD
Connectors: CC1, CC2 (failover enabled)
```

**4. SSL Certificate:**
```bash
# Generate self-signed (development only)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /opt/sap/scc/server.key \
  -out /opt/sap/scc/server.crt

# Import in SAP system
STRUST transaction → Certificate
Import Cloud Connector certificate
```

### Cloud Connector Monitoring

**Performance Metrics:**
```
Admin Console → Monitoring
├── Requests/second: Target >100 req/s
├── Latency: Target <100ms average
├── Throughput: Target >50MB/s
└── Error Rate: Target <0.1%
```

**Health Check:**
```
Backend Connectivity:
  ✓ HTTPS port 443 reachable
  ✓ SSL handshake successful
  ✓ Authentication successful
  ✓ ODP availability confirmed
```

## DP Agent Installation and Configuration

### System Requirements

```
OS: Windows Server 2016+ or Linux (RHEL/SUSE)
CPU: 4 cores minimum
RAM: 8GB minimum (16GB recommended)
Storage: 50GB free space
Java: JDK 11+
Network: Direct access to S/4HANA and Datasphere
Firewall: Outbound HTTPS to Datasphere tenant
```

### Installation (Windows)

```powershell
# 1. Download DP Agent from Datasphere
# Administration → Data Provisioning → Download DP Agent

# 2. Extract and install
Expand-Archive -Path dpsagent-*.zip -DestinationPath C:\dpsagent
cd C:\dpsagent

# 3. Run installer
.\install.exe /path C:\dpsagent /user datasph_agent /password [pass]

# 4. Configure
notepad conf\agent.properties
# Set:
# DATASPHERE_TENANT=https://[tenant].datasphere.cloud.sap
# DATASPHERE_USER=dpsagent@company.com
# DATASPHERE_PASSWORD=[oauth_token]
# SAP_SYSTEM_HOST=s4h-prod.example.com
# SAP_SYSTEM_CLIENT=100

# 5. Start service
Start-Service dpsagent

# 6. Verify
.\dpsagent status
```

### Installation (Linux)

```bash
# 1. Download and extract
cd /opt/sap
unzip dpsagent-*.zip
cd dpsagent

# 2. Configure
nano conf/agent.properties
# Set properties as above

# 3. Create systemd service
sudo tee /etc/systemd/system/dpsagent.service > /dev/null <<EOF
[Unit]
Description=SAP Datasphere DP Agent
After=network.target

[Service]
Type=forking
User=sap
WorkingDirectory=/opt/sap/dpsagent
ExecStart=/opt/sap/dpsagent/bin/dpsagent.sh start
ExecStop=/opt/sap/dpsagent/bin/dpsagent.sh stop
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# 4. Start
sudo systemctl start dpsagent
sudo systemctl status dpsagent

# 5. Verify
./bin/dpsagent status
```

## Delta Queue Management

### Monitoring Delta Queue

**Check Queue Status:**
```sql
-- In S/4HANA, execute:
SELECT odp_context, odp_object, queue_size, oldest_record_date
FROM /ODSO/ODP_QUEUE_STATUS
WHERE odp_context = 'ABAP:CDS_VIEWS'
  AND odp_object = 'C_CUSTOMER';
```

**Expected Output:**
```
ODSO_OBJECT      QUEUE_SIZE   OLDEST_RECORD   DAYS_RETAINED
C_CUSTOMER       250MB        2024-01-15      8
C_SALES_ORDER    1.2GB        2024-01-14      7
C_INVOICE        800MB        2024-01-16      8
```

### Delta Queue Overflow Management

**Scenario: Queue exceeds size limit (4GB)**

```
Symptoms:
- Extraction fails with "Queue Full" error
- Older change records purged
- Must perform full reload

Recovery Steps:
1. Check queue status in source system
2. Perform full reload in Datasphere
3. Reset watermark to current value
4. Resume delta extractions
5. Monitor queue going forward
```

**Prevention:**
```
Datasphere Configuration:
- Increase delta frequency (5 min instead of 15 min)
- Reduce batch size if possible
- Monitor queue size weekly

Source System:
- Increase retention period to 10-14 days
- Increase log size limit to 8-10GB
- Add parallel threads for cleanup
```

### Delta Queue Cleanup

**Manual Cleanup (Caution: Data loss)**
```sql
-- Backup first!
EXEC RsSYS.sp_DeleteOdpQueueOlder(
  @ContextName = 'ABAP:CDS_VIEWS',
  @ObjectName = 'C_CUSTOMER',
  @DaysToKeep = 3
);
```

## Troubleshooting S/4HANA Connectivity

### Connection Test Failures

| Error | Cause | Solution |
|-------|-------|----------|
| "Host not reachable" | Network/firewall issue | Verify IP, port, firewall rules, Cloud Connector |
| "Authentication failed" | Invalid credentials | Check user/password, role authorization |
| "SSL certificate invalid" | Certificate issue | Update certificate, check chain |
| "ODP not available" | CDS view not extraction-enabled | Verify view prefix (C_*), check annotations |
| "Connection timeout" | System overload/network latency | Increase timeout, check system load |

### ODP Availability Verification

```
Datasphere → Connection → Test Connection
Expected Success:
  ✓ Backend System: Connected
  ✓ ODP: Available
  ✓ CDS Views: Accessible
  ✓ Latency: <500ms
```

### Delta Extraction Troubleshooting

**Symptom: Delta extraction fails with "Change number invalid"**
```
Cause: Change number > current max
Solution:
  1. Full reload to get current watermark
  2. Restart delta from new watermark
```

**Symptom: No delta records extracted**
```
Cause: No changes since last run
Solution:
  1. Verify source data actually changed
  2. Check watermark = previous max
  3. Query source directly for verification
```

**Symptom: Duplicate records in delta load**
```
Cause: Duplicate changes in log
Solution:
  1. Deduplicate on key fields
  2. Use SCD Type 2 for dimension tables
  3. Verify merge logic in target
```

