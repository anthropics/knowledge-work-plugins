# Security Architect Reference Guide

## Table of Contents

1. DAC Creation Patterns with SQL Examples
2. Authorization Migration Mapping
3. Audit Policy Templates
4. Identity Provider Configuration Checklists
5. Security Review Pre-Go-Live Checklist
6. Common Security Anti-Patterns and Fixes
7. Emergency Access Procedures

---

## 1. DAC Creation Patterns with SQL Examples

### Pattern 1: Simple Value-Based DAC

**Use Case:** Sales reps restricted to their assigned region.

**DAC Definition:**
```sql
CREATE DATA ACCESS CONTROL DAC_SALES_BY_REGION
FOR TABLE T_SALES
WHERE SALES_REGION = :USER_ASSIGNED_REGION;

-- Parameters:
-- :USER_ASSIGNED_REGION - User attribute from IdP
--   Example: john.smith has attribute ASSIGNED_REGION = 'Americas'
```

**User Attribute Setup:**
```sql
-- In IdP (Azure AD, Okta, etc.) or Datasphere User Management:
User: john.smith
Custom Attributes:
  ASSIGNED_REGION = 'Americas'

User: jane.doe
Custom Attributes:
  ASSIGNED_REGION = 'EMEA'

User: mary.johnson
Custom Attributes:
  ASSIGNED_REGION = 'APAC'
```

**Testing:**
```sql
-- Test as john.smith
SELECT DISTINCT SALES_REGION FROM T_SALES;
-- Expected: ['Americas']

-- Test as jane.doe
SELECT DISTINCT SALES_REGION FROM T_SALES;
-- Expected: ['EMEA']

-- Test as mary.johnson
SELECT DISTINCT SALES_REGION FROM T_SALES;
-- Expected: ['APAC']
```

---

### Pattern 2: Multi-Value DAC (IN List)

**Use Case:** Manager sees multiple assigned cost centers.

**DAC Definition:**
```sql
CREATE DATA ACCESS CONTROL DAC_COST_CENTER_MULTI
FOR TABLE T_FINANCIALS
WHERE COST_CENTER IN :USER_ASSIGNED_COST_CENTERS;

-- Parameters:
-- :USER_ASSIGNED_COST_CENTERS - User attribute (array/list)
--   Example: john.smith has attribute ASSIGNED_COST_CENTERS = ['CC001', 'CC002', 'CC003']
```

**User Attribute Setup:**
```sql
-- In IdP:
User: john.smith
Custom Attributes:
  ASSIGNED_COST_CENTERS = ['CC001', 'CC002', 'CC003']

User: jane.doe
Custom Attributes:
  ASSIGNED_COST_CENTERS = ['CC010']
```

**Testing:**
```sql
-- Test as john.smith
SELECT DISTINCT COST_CENTER FROM T_FINANCIALS;
-- Expected: ['CC001', 'CC002', 'CC003']

SELECT COUNT(*) FROM T_FINANCIALS WHERE COST_CENTER = 'CC010';
-- Expected: 0 (not in assigned list)

-- Test as jane.doe
SELECT DISTINCT COST_CENTER FROM T_FINANCIALS;
-- Expected: ['CC010']
```

---

### Pattern 3: Compound Key DAC

**Use Case:** Restrict by company AND subsidiary.

**DAC Definition:**
```sql
CREATE DATA ACCESS CONTROL DAC_COMPANY_SUBSIDIARY
FOR TABLE T_GENERAL_LEDGER
WHERE COMPANY_CODE = :USER_COMPANY
  AND SUBSIDIARY_CODE IN :USER_ASSIGNED_SUBSIDIARIES;

-- Parameters:
-- :USER_COMPANY - Single value
-- :USER_ASSIGNED_SUBSIDIARIES - Array value
```

**User Attribute Setup:**
```sql
-- In IdP:
User: john.smith
Custom Attributes:
  COMPANY = 'CORP001'
  ASSIGNED_SUBSIDIARIES = ['SUB_USA', 'SUB_CANADA', 'SUB_MEXICO']

User: jane.doe
Custom Attributes:
  COMPANY = 'CORP002'
  ASSIGNED_SUBSIDIARIES = ['SUB_UK', 'SUB_DE', 'SUB_FR']
```

**Testing:**
```sql
-- Test as john.smith
SELECT DISTINCT COMPANY_CODE FROM T_GENERAL_LEDGER;
-- Expected: ['CORP001']

SELECT DISTINCT SUBSIDIARY_CODE FROM T_GENERAL_LEDGER
WHERE COMPANY_CODE = 'CORP001';
-- Expected: ['SUB_USA', 'SUB_CANADA', 'SUB_MEXICO']

SELECT COUNT(*) FROM T_GENERAL_LEDGER
WHERE COMPANY_CODE = 'CORP002';
-- Expected: 0 (different company, hidden)
```

---

### Pattern 4: Hierarchy-Based DAC

**Use Case:** Users see their department and subordinates in org hierarchy.

**Hierarchy Table Structure:**
```sql
CREATE TABLE T_ORG_HIERARCHY (
  NODE_ID VARCHAR(20) PRIMARY KEY,
  PARENT_NODE_ID VARCHAR(20),
  NODE_NAME VARCHAR(100),
  NODE_LEVEL INTEGER,
  EFFECTIVE_FROM DATE,
  EFFECTIVE_TO DATE
);

INSERT INTO T_ORG_HIERARCHY VALUES
  ('CORP', NULL, 'Corporation', 1, '2024-01-01', NULL),
  ('DIV_ENG', 'CORP', 'Engineering', 2, '2024-01-01', NULL),
  ('DIV_SALES', 'CORP', 'Sales', 2, '2024-01-01', NULL),
  ('DEPT_SWE', 'DIV_ENG', 'Software Engineering', 3, '2024-01-01', NULL),
  ('DEPT_QA', 'DIV_ENG', 'QA', 3, '2024-01-01', NULL),
  ('DEPT_FIELD', 'DIV_SALES', 'Field Sales', 3, '2024-01-01', NULL),
  ('DEPT_INSIDE', 'DIV_SALES', 'Inside Sales', 3, '2024-01-01', NULL),
  ('TEAM_PYTHON', 'DEPT_SWE', 'Python Team', 4, '2024-01-01', NULL),
  ('TEAM_JAVA', 'DEPT_SWE', 'Java Team', 4, '2024-01-01', NULL);
```

**User-to-Hierarchy Mapping:**
```sql
CREATE TABLE T_USER_HIERARCHY_MAP (
  USER_ID VARCHAR(256),
  ASSIGNED_NODE_ID VARCHAR(20),
  EFFECTIVE_FROM DATE,
  EFFECTIVE_TO DATE
);

INSERT INTO T_USER_HIERARCHY_MAP VALUES
  ('john.smith@contoso.com', 'DEPT_SWE', '2024-01-01', NULL),    -- Dept head
  ('jane.doe@contoso.com', 'DIV_SALES', '2024-01-01', NULL),       -- Division head
  ('mary.johnson@contoso.com', 'CORP', '2024-01-01', NULL),        -- CEO
  ('alex.brown@contoso.com', 'TEAM_PYTHON', '2024-01-01', NULL),   -- Team lead
```

**DAC Definition:**
```sql
CREATE DATA ACCESS CONTROL DAC_ORG_HIERARCHY
FOR TABLE T_EMPLOYEE_DATA
WHERE DEPARTMENT_ID IN (
  SELECT NODE_ID FROM T_ORG_HIERARCHY h
  WHERE h.NODE_ID = :USER_ASSIGNED_NODE
     OR h.PARENT_NODE_ID = :USER_ASSIGNED_NODE
     OR h.PARENT_NODE_ID IN (
       SELECT NODE_ID FROM T_ORG_HIERARCHY
       WHERE PARENT_NODE_ID = :USER_ASSIGNED_NODE
     )
);

-- Simplified: Include assigned node + all descendants
```

**Testing:**
```sql
-- Test as john.smith (DEPT_SWE):
-- Can see: DEPT_SWE, TEAM_PYTHON, TEAM_JAVA
SELECT DISTINCT DEPARTMENT_ID FROM T_EMPLOYEE_DATA;
-- Expected: ['DEPT_SWE', 'TEAM_PYTHON', 'TEAM_JAVA']

-- Cannot see: DIV_SALES, DEPT_FIELD
SELECT COUNT(*) FROM T_EMPLOYEE_DATA WHERE DEPARTMENT_ID = 'DEPT_FIELD';
-- Expected: 0

-- Test as jane.doe (DIV_SALES):
-- Can see: DIV_SALES, DEPT_FIELD, DEPT_INSIDE
SELECT DISTINCT DEPARTMENT_ID FROM T_EMPLOYEE_DATA;
-- Expected: ['DIV_SALES', 'DEPT_FIELD', 'DEPT_INSIDE']

-- Test as mary.johnson (CORP):
-- Can see: Everything (all descendants)
SELECT COUNT(DISTINCT DEPARTMENT_ID) FROM T_EMPLOYEE_DATA;
-- Expected: 9 (all departments)
```

---

### Pattern 5: Time-Bounded DAC

**Use Case:** Users can only see current year's data (rolling window).

**DAC Definition:**
```sql
CREATE DATA ACCESS CONTROL DAC_CURRENT_YEAR
FOR TABLE T_SALES_TRANSACTIONS
WHERE POSTING_DATE >= DATE_TRUNC('year', CURRENT_DATE)
  AND POSTING_DATE < DATE_TRUNC('year', CURRENT_DATE) + INTERVAL 1 YEAR;

-- Alternative: Last 12 months
CREATE DATA ACCESS CONTROL DAC_TRAILING_12_MONTHS
FOR TABLE T_SALES_TRANSACTIONS
WHERE POSTING_DATE >= CURRENT_DATE - INTERVAL 1 YEAR
  AND POSTING_DATE < CURRENT_DATE + INTERVAL 1 DAY;
```

**Testing:**
```sql
-- Current date: 2024-02-08

-- Test: Current Year (2024)
SELECT MIN(POSTING_DATE), MAX(POSTING_DATE) FROM T_SALES_TRANSACTIONS;
-- Expected: '2024-01-01' to '2024-02-08'
-- Hidden: Any 2023 or prior dates

-- Test: Trailing 12 months
SELECT COUNT(*) FROM T_SALES_TRANSACTIONS
WHERE POSTING_DATE < '2023-02-08';
-- Expected: 0 (older than 12 months hidden)
```

---

### Pattern 6: Conditional DAC (IF/THEN)

**Use Case:** Different filters based on user role.

**DAC Definition:**
```sql
CREATE DATA ACCESS CONTROL DAC_CONDITIONAL_ROLE
FOR TABLE T_ORDERS
WHERE CASE
  WHEN :USER_ROLE = 'ADMIN' THEN 1 = 1  -- No filter for admins
  WHEN :USER_ROLE = 'MANAGER' THEN MANAGER_ID = :USER_ID
  WHEN :USER_ROLE = 'SALES_REP' THEN ASSIGNED_SALES_REP = :USER_ID
  ELSE 1 = 0  -- Deny all if role unknown
END;

-- Parameters:
-- :USER_ROLE - from IdP role mapping
-- :USER_ID - current user's ID
```

**Testing:**
```sql
-- Test as admin user (ROLE='ADMIN'):
SELECT COUNT(*) FROM T_ORDERS;
-- Expected: All orders

-- Test as manager (ROLE='MANAGER', USER_ID='MGR001'):
SELECT COUNT(*) FROM T_ORDERS;
-- Expected: Only orders where MANAGER_ID = 'MGR001'

-- Test as sales rep (ROLE='SALES_REP', USER_ID='SR001'):
SELECT COUNT(*) FROM T_ORDERS;
-- Expected: Only orders where ASSIGNED_SALES_REP = 'SR001'
```

---

### Pattern 7: Sensitive Column Masking (Advanced)

**Note:** Datasphere DACs filter rows, not columns. For column-level masking, use Transformation Rules:

```sql
-- Column-level masking: Redact PII in SELECT
SELECT
  CUSTOMER_ID,
  CUSTOMER_NAME,
  CASE
    WHEN CURRENT_USER NOT IN ('dpo@company.com', 'admin@company.com')
    THEN '***REDACTED***'
    ELSE CUSTOMER_EMAIL
  END as CUSTOMER_EMAIL,
  CASE
    WHEN CURRENT_USER NOT IN ('dpo@company.com', 'admin@company.com')
    THEN '***REDACTED***'
    ELSE CUSTOMER_PHONE
  END as CUSTOMER_PHONE
FROM T_CUSTOMER_SENSITIVE;

-- Result: Non-privileged users see redacted values
-- DPO and admin see actual PII
```

---

## 2. Authorization Migration Mapping (BW → Datasphere)

### Mapping Table Structure

```sql
CREATE TABLE T_BW_DS_AUTH_MAPPING (
  MAPPING_ID INTEGER PRIMARY KEY AUTO_INCREMENT,
  BW_USER_ID VARCHAR(256),
  BW_AUTH_OBJECT VARCHAR(30),
  BW_AUTH_FIELD VARCHAR(30),
  BW_AUTH_VALUES VARCHAR(1000),
  DS_TABLE_NAME VARCHAR(256),
  DS_COLUMN_NAME VARCHAR(256),
  DS_DAC_NAME VARCHAR(256),
  MAPPING_STATUS VARCHAR(20),  -- PENDING, MAPPED, VALIDATED, ACTIVE
  VALIDATION_STATUS VARCHAR(20),  -- PASSED, FAILED, WARNING
  VALIDATION_NOTES VARCHAR(1000),
  CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ACTIVATED_AT TIMESTAMP,
  CREATED_BY VARCHAR(256),

  INDEX idx_bw_user (BW_USER_ID),
  INDEX idx_ds_table (DS_TABLE_NAME),
  INDEX idx_status (MAPPING_STATUS)
);
```

### Migration Workflow

```
Phase 1: EXTRACTION (BW System)
│
├─ Extract all users with active authorizations
├─ For each user, export:
│  ├─ BW_USER_ID
│  ├─ Authorization objects (0_RF_BOA, etc.)
│  ├─ Auth fields and values
│  └─ Assigned InfoCubes
│
└─ Output: T_BW_AUTH_EXTRACT (staging table)

Phase 2: MAPPING (Analysis & Planning)
│
├─ For each BW authorization:
│  ├─ Identify corresponding Datasphere table
│  ├─ Map BW field → Datasphere column
│  ├─ Determine DAC type (Operator, Hierarchy, etc.)
│  └─ Create DAC definition
│
└─ Output: T_BW_DS_AUTH_MAPPING (PENDING status)

Phase 3: CREATION (Datasphere)
│
├─ For each row in T_BW_DS_AUTH_MAPPING:
│  ├─ Create DAC in Datasphere
│  ├─ Assign to table/view
│  ├─ Assign to user
│  └─ Update status to MAPPED
│
└─ Output: Datasphere DACs created

Phase 4: VALIDATION
│
├─ For each DAC:
│  ├─ Test user access
│  ├─ Verify row filtering
│  ├─ Reconcile BW vs. DS row counts
│  └─ Update validation status
│
└─ Output: T_BW_DS_AUTH_MAPPING (VALIDATED status)

Phase 5: ACTIVATION
│
├─ Disable BW Bridge access
├─ Enable Datasphere access
├─ Monitor for access issues
├─ Update status to ACTIVE
│
└─ Output: Go-live complete
```

### Example Migration

```
BW Authorization Export:
┌────────────┬──────────────────────────────┐
│ USER_ID    │ Authorization Details        │
├────────────┼──────────────────────────────┤
│ JOHN.SMITH │ Object: 0_RF_BOA            │
│            │ InfoCube: 0SALES_001         │
│            │ COMPANY_CODE: 0010, 0020    │
│            │ SALES_ORG: 1000             │
│            │ REGION: EUR, AMER           │
└────────────┴──────────────────────────────┘

Datasphere Mapping:
┌──────────────────┬──────────────────────┬─────────────────────────┐
│ BW Field         │ DS Column            │ DAC Name               │
├──────────────────┼──────────────────────┼─────────────────────────┤
│ COMPANY_CODE     │ COMPANY_CODE         │ DAC_JOHN_COMPANY      │
│ SALES_ORG        │ SALES_ORG            │ DAC_JOHN_SALES_ORG    │
│ REGION           │ SALES_REGION         │ DAC_JOHN_REGION       │
└──────────────────┴──────────────────────┴─────────────────────────┘

DAC Creation:
DAC_JOHN_COMPANY:
  WHERE COMPANY_CODE IN ('0010', '0020')

DAC_JOHN_SALES_ORG:
  WHERE SALES_ORG = '1000'

DAC_JOHN_REGION:
  WHERE SALES_REGION IN ('EUR', 'AMER')

Combined Effect:
  SELECT * FROM T_SALES
  WHERE COMPANY_CODE IN ('0010', '0020')
    AND SALES_ORG = '1000'
    AND SALES_REGION IN ('EUR', 'AMER')
```

---

## 3. Audit Policy Templates for Compliance Frameworks

### Template 1: SOX (Sarbanes-Oxley) Compliance

**Applicable To:** Publicly traded companies, financial reporting.

```yaml
Audit Policy: SOX_COMPLIANCE_AUDIT

Scope:
  Tables:
    - T_GENERAL_LEDGER (all accounting entries)
    - T_JOURNAL_VOUCHERS (manual journal entries)
    - T_RECONCILIATIONS (bank/balance sheet reconciliations)
    - T_FIXED_ASSETS (asset management)
    - T_INTERCOMPANY_TRANSACTIONS (consolidation entries)

Operations:
  ☑ READ    (Financial data access)
  ☑ INSERT  (New transactions)
  ☑ UPDATE  (Changes to existing transactions)
  ☑ DELETE  (Deletion of transactions - should not occur)

Users:
  - All (especially non-Finance)
  - Priority: Non-accounting users accessing financial data

Logging Details:
  ├─ Timestamp (down to millisecond)
  ├─ User ID & session
  ├─ IP address & hostname
  ├─ Rows affected (count)
  ├─ Key field values (GL account, cost center)
  ├─ SQL hash (for deduplication)
  └─ Execution time

Retention:
  Duration: 10 years (SEC requirement)
  Storage: Primary database for 1 year, then archive
  Archival: Immutable (cannot be deleted)
  Retrieval: Must be queryable within 24 hours

Alerting:
  ☑ DELETE on T_JOURNAL_VOUCHERS: CRITICAL
  ☑ Bulk UPDATE on T_GENERAL_LEDGER: HIGH (> 100 rows)
  ☑ Access from unusual IP: MEDIUM
  ☑ Non-Finance user reading GL: MEDIUM

Reporting:
  ├─ Daily reconciliation: Transactions entered vs. approved
  ├─ Weekly: User access reports (who accessed what)
  ├─ Monthly: Exception report (DELETE/bulk updates)
  ├─ Quarterly: Compliance audit (coverage = 100%)
  └─ Annual: SOX Section 404 attestation data

Audit Review:
  Frequency: Continuous monitoring + Monthly deep-dive
  Owner: Internal Audit
  Scope: 100% of financial transactions
  Approval: CFO quarterly certification
```

---

### Template 2: GDPR (General Data Protection Regulation)

**Applicable To:** European data subjects, personal data processing.

```yaml
Audit Policy: GDPR_PERSONAL_DATA_AUDIT

Scope:
  Tables:
    - T_CUSTOMER_PERSONAL (name, address, contact)
    - T_CUSTOMER_PAYMENT (credit cards, bank accounts)
    - T_EMPLOYEE_PERSONAL (HR records)
    - T_APPLICANT_DATA (job application info)
    - Any table containing PII

  Definition of PII: Name, Email, Phone, SSN, Address, Payment methods, etc.

Operations:
  ☑ READ    (Accessing personal data - DETAILED logging)
  ☑ INSERT  (Collecting personal data)
  ☑ UPDATE  (Modifying personal data)
  ☑ DELETE  (Right to be forgotten)

Users:
  - All (especially non-authorized business functions)
  - Flag: Non-Customer-Service users accessing customer PII

Logging Details:
  ├─ Timestamp
  ├─ User ID & session
  ├─ Purpose code (e.g., "BILLING", "SUPPORT", "MARKETING")
  ├─ Data subject ID (anonymized if possible)
  ├─ Rows accessed (count)
  ├─ Specific fields accessed (if column-level logging available)
  └─ Data export/download (flagged separately)

Retention:
  Duration: 3 years (GDPR Article 5.1.e - storage limitation)
  Storage: Encrypted at rest
  Archival: Delete on expiration (automatic)
  Legal Hold: Extended retention if litigation pending
  Data Subject Access: Must provide log extract within 30 days

Alerting:
  ☑ DELETE personal data: CRITICAL (log for audit trail)
  ☑ Bulk export: HIGH (> 100 records)
  ☑ Non-support user reading PII: HIGH
  ☑ International data transfer: CRITICAL
  ☑ Unauthorized processing: CRITICAL

Reporting:
  ├─ Data Subject Access Requests (SARs): 30-day reporting
  ├─ Breach notification: <72 hours to regulator
  ├─ Purpose justification: User must document legal basis
  ├─ Weekly: Users accessing PII without clear business need
  └─ Monthly: Compliance dashboard

Special Requirements:
  ├─ Data Minimization: Only collect/store minimum necessary
  ├─ Consent Tracking: Log consent dates/revocation
  ├─ Purpose Limitation: Can only use data for stated purpose
  ├─ Right to be Forgotten: Track deletion requests
  ├─ Legitimate Interest: Document basis for processing
  └─ Data Protection Impact Assessment (DPIA): Document high-risk processing

Audit Review:
  Frequency: Continuous + Quarterly DPA review
  Owner: Data Protection Officer (DPO)
  Scope: 100% of PII access
  Approval: DPO sign-off for compliance
```

---

### Template 3: HIPAA (Health Insurance Portability and Accountability Act)

**Applicable To:** Healthcare providers, health plans, covered entities.

```yaml
Audit Policy: HIPAA_PHI_AUDIT

Scope:
  Tables:
    - T_PATIENT_RECORDS (medical history)
    - T_DIAGNOSES (diagnosis codes)
    - T_MEDICATIONS (drug records)
    - T_CLAIMS (insurance claims with patient info)
    - T_GENETIC_DATA (DNA/genetic tests)
    - Any table with Protected Health Information (PHI)

  Definition of PHI: Medical records, diagnoses, medications, genetic info, etc.

Operations:
  ☑ READ    (Clinician access - requires authorization)
  ☑ INSERT  (New patient records)
  ☑ UPDATE  (Chart updates)
  ☑ DELETE  (Corrections - rare)

Users:
  - Clinicians (doctors, nurses, specialists)
  - Billing staff (claims processing)
  - QA/Auditors (compliance review)
  - Flag all others

Logging Details:
  ├─ Timestamp (down to second)
  ├─ User ID
  ├─ User role (Physician, Nurse, Billing, etc.)
  ├─ Patient identifier
  ├─ Access purpose (e.g., "Direct Care", "Treatment", "Billing")
  ├─ Rows accessed (patient record count)
  ├─ Unusual access patterns (e.g., accessing deceased patient)
  └─ Export/download of records

Retention:
  Duration: 6 years (HIPAA minimum)
  Storage: Encrypted, access-controlled
  Archival: Immutable after 1 year
  Retrieval: Audit logs available within 24 hours

Alerting:
  ☑ Unauthorized access attempt: CRITICAL
  ☑ Non-clinician accessing PHI: CRITICAL
  ☑ Bulk PHI export: CRITICAL
  ☑ After-hours access (unusual): HIGH
  ☑ Access to unassigned patient: MEDIUM

Reporting:
  ├─ Daily: Unauthorized access attempts
  ├─ Weekly: User access reports (by role)
  ├─ Monthly: Unusual access patterns (dead patients, bulk queries)
  ├─ Quarterly: Breach risk assessment
  └─ Annual: Compliance certification

Access Controls:
  ├─ Role-Based: Only clinicians caring for patient see records
  ├─ Time-Limited: Access expires at discharge
  ├─ Minimum Necessary: Show only relevant portions
  ├─ Emergency Access: Track and log all emergency overrides
  └─ Terminated Employee: Immediate revocation

Breach Notification:
  ├─ Detection: Unauthorized access → immediate alert
  ├─ Assessment: Within 24 hours (< 500 records = low risk)
  ├─ Notification: Patients (> 500 records = HHS/media notice)
  ├─ Documentation: Audit log required for investigation
  └─ Corrective Action: Preventive measures documented

Audit Review:
  Frequency: Continuous monitoring + Monthly deep-dive
  Owner: Chief Compliance Officer (CCO) & Privacy Officer
  Scope: 100% of PHI access
  Approval: Annual OCR (Office for Civil Rights) audit
```

---

## 4. Identity Provider Configuration Checklist

### Azure AD SAML Configuration

```yaml
Prerequisites:
  ☐ Azure AD Premium subscription (or free tier)
  ☐ Datasphere tenant URL (e.g., https://datasphere.company.com)
  ☐ Domain administrator access
  ☐ User attribute mapping planned

Step 1: Register Application in Azure AD
  ☐ Sign in to Azure Portal (portal.azure.com)
  ☐ Navigate: Azure AD → App Registrations → New Registration
  ☐ Name: "SAP Datasphere"
  ☐ Supported account types: "Accounts in this organizational directory only"
  ☐ Redirect URI: Web - https://datasphere.company.com/saml/acs
  ☐ Click Register

Step 2: Configure SAML Single Sign-On
  ☐ In app overview, click "Single sign-on"
  ☐ Select "SAML"
  ☐ Upload or copy Datasphere SP metadata

Step 3: Basic SAML Configuration
  ☐ Identifier (Entity ID): https://datasphere.company.com/saml/entity
  ☐ Reply URL (ACS): https://datasphere.company.com/saml/acs
  ☐ Sign On URL: https://datasphere.company.com/login
  ☐ Logout URL: https://datasphere.company.com/logout

Step 4: Attributes & Claims
  ☐ NameID format: unspecified
  ☐ NameID value: user.userprincipalname
  ☐ Add custom claim:
      Name: http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress
      Value: user.mail
  ☐ Add custom claim for REGIONS:
      Name: REGIONS
      Value: user.extensionAttribute1

Step 5: SAML Signing Certificate
  ☐ Download signing certificate (Base64)
  ☐ Upload to Datasphere IdP configuration

Step 6: Azure AD Sign-In URL & Issuer
  ☐ Copy "Azure AD Sign-In URL" → Datasphere IdP Sign-On URL
  ☐ Copy "Azure AD Identifier" → Datasphere IdP Entity ID

Step 7: Configure User Attributes in Azure AD
  ☐ Go: Azure AD → Users → Select User (e.g., john.smith)
  ☐ Profile → Edit
  ☐ Extension attributes:
      extensionAttribute1 = Americas,EMEA  (for REGIONS)
      extensionAttribute2 = CC001,CC002    (for COST_CENTERS)

Step 8: Test Configuration
  ☐ In Datasphere Admin Console, click "Test SSO"
  ☐ Select test user (john.smith)
  ☐ Verify login succeeds
  ☐ Verify user attributes populated correctly

Step 9: Assign Users to Application
  ☐ In Azure AD, navigate to Users and groups
  ☐ Add users/groups to the Datasphere application
  ☐ (Alternative: Allow all users, manage via Datasphere roles)

Step 10: User Provisioning (Optional)
  ☐ If using automatic provisioning:
      ☑ Enable SCIM provisioning
      ☑ Copy SCIM URL from Azure
      ☑ Generate bearer token
      ☑ Enter in Datasphere IdP configuration
  ☐ If manual: Users created in Datasphere, authenticate via Azure AD

Verification:
  ☐ User can log in via SAML
  ☐ User attributes visible in Datasphere profile
  ☐ DACs apply based on user attributes
  ☐ Logout successful
  ☐ Session timeout works
```

### Okta SAML Configuration

```yaml
Prerequisites:
  ☐ Okta organization (org-xxxxx.okta.com)
  ☐ Admin access
  ☐ Datasphere SP metadata or details

Step 1: Create SAML 2.0 App in Okta
  ☐ Sign in to Okta Admin (okta.com/admin)
  ☐ Applications → Applications → Create New App
  ☐ Platform: Web
  ☐ Sign-On Method: SAML 2.0
  ☐ Click Create
  ☐ App Name: SAP Datasphere
  ☐ Click Next

Step 2: Configure SAML Settings
  ☐ Single Sign-On URL: https://datasphere.company.com/saml/acs
  ☐ Audience URI (SP Entity ID): https://datasphere.company.com/saml/entity
  ☐ Name ID Format: unspecified
  ☐ Name ID Value: user.login

Step 3: Configure Attributes & Claims
  ☐ Add Attribute Statements:
      Name: email, Value: user.email
      Name: firstName, Value: user.firstName
      Name: lastName, Value: user.lastName
  ☐ Add Custom Claims:
      Name: REGIONS, Value: user.regions (if custom attribute)
      Name: COST_CENTER, Value: user.costCenter

Step 4: Configure Group Claims (Optional)
  ☐ Add Group Claim:
      Name: groups
      Filter: Starts with = "*" (all groups)
      Value: group.name

Step 5: Download Metadata
  ☐ Scroll to "SAML Signing Certificates"
  ☐ Click "Download" to get certificate

Step 6: Provide Okta Details to Datasphere
  ☐ Sign-On URL: https://org-xxxxx.okta.com/app/123.../sso/saml
  ☐ Issuer ID: https://org-xxxxx.okta.com
  ☐ Certificate: [Downloaded certificate]
  ☐ Sign-Out URL: https://org-xxxxx.okta.com/login/signout

Step 7: Assign Users/Groups to App
  ☐ In Okta, go to Assignments tab
  ☐ Assign users or groups (e.g., "Datasphere Users" group)
  ☐ Set provisioning options if automated provisioning enabled

Step 8: Configure User Attributes (if custom)
  ☐ Profile Editor → Okta user profile
  ☐ Add custom attributes:
      regions: List (value: "Americas,EMEA")
      costCenter: String (value: "CC001")
  ☐ Populate attributes for test users

Step 9: Test SAML Login
  ☐ In Datasphere, click "Test SAML Configuration"
  ☐ User is redirected to Okta
  ☐ Okta login prompt appears
  ☐ User logs in
  ☐ Redirected back to Datasphere
  ☐ Session established

Step 10: Verify Attribute Flow
  ☐ Log in as test user
  ☐ Check Datasphere user profile
  ☐ Verify custom attributes present
  ☐ Verify DACs applied correctly

Troubleshooting:
  ☐ If "Assertion Consumer Service URL mismatch":
      Check ACS URL matches exactly in both Okta and Datasphere
  ☐ If "NameID not found":
      Verify NameID attribute matches IdP claim name
  ☐ If "Attributes not populated":
      Check Attribute Statements in Okta are correct
      Verify user has values for those attributes
```

---

## 5. Security Review Pre-Go-Live Checklist

### 30-Day Pre-Go-Live Security Review

```yaml
Timeline: T-30 days to Go-Live

Week 1 (T-30 to T-23):
  Access Control Review:
    ☐ List all users with Datasphere access
    ☐ For each user, verify:
        ☑ Authorized to access Datasphere
        ☑ Has appropriate roles assigned
        ☑ No excessive privileges
        ☑ Segregation of duties maintained

  DAC Validation:
    ☐ All DACs created from authorization migration
    ☐ All DACs active and applied to tables
    ☐ Sample test: 5 users, verify data filtering works
    ☐ High-risk users tested (admins, global access)

  IdP Integration Testing:
    ☐ SAML/OIDC configuration verified
    ☐ User attributes populate correctly
    ☐ Custom attributes flowing through
    ☐ Single sign-out works
    ☐ Session timeout enforced

Week 2 (T-23 to T-16):
  Audit Policy Validation:
    ☐ All sensitive tables have audit policies
    ☐ Audit logging working (test with sample queries)
    ☐ Audit table receiving records
    ☐ Retention policies configured
    ☐ Alert thresholds set appropriately

  Compliance Mapping:
    ☐ All compliance requirements identified
    ☐ Applicable audit policies assigned (SOX, GDPR, HIPAA)
    ☐ Retention periods configured per regulation
    ☐ Breach notification procedures documented
    ☐ Data protection impact assessment (DPIA) completed if required

  Network & Encryption:
    ☐ TLS 1.2+ required for all connections
    ☐ Certificate installed and valid
    ☐ VPN/Firewall rules in place
    ☐ IP whitelisting configured (if applicable)
    ☐ Disable weak ciphers

Week 3 (T-16 to T-9):
  Stress Testing:
    ☐ High-volume query test (100 concurrent users)
    ☐ DAC performance impact measured (< 5% overhead acceptable)
    ☐ Audit logging performance (not slowing queries > 10%)
    ☐ Large data transfer test (10 GB table load)

  Disaster Recovery:
    ☐ Backup procedure tested
    ☐ Restore from backup tested
    ☐ Audit log backup separate from data
    ☐ RTO (Recovery Time Objective) documented
    ☐ RPO (Recovery Point Objective) documented

  Incident Response Planning:
    ☐ Incident response team assigned
    ☐ Escalation procedures defined
    ☐ On-call rotation established
    ☐ Communication templates prepared
    ☐ Contact information for all key personnel

Week 4 (T-9 to Go-Live):
  Final Security Audit:
    ☐ External security assessment (if required)
    ☐ Vulnerability scanning completed
    ☐ Penetration testing completed
    ☐ Security findings remediated
    ☐ Risk sign-off from CISO/Security Team

  User Readiness:
    ☐ Security awareness training completed by all users
    ☐ Password change required on first login
    ☐ MFA enabled (if applicable)
    ☐ Support team trained on security procedures
    ☐ User documentation reviewed

  Go-Live Prep:
    ☐ Cutover plan reviewed with security team
    ☐ Rollback procedures tested
    ☐ Emergency access procedures documented
    ☐ On-call team briefed
    ☐ Final security sign-off obtained

Approval Gates:
  ☐ Week 1: Access Control Review PASS
  ☐ Week 2: Audit Policy & Compliance Review PASS
  ☐ Week 3: Stress Test & DR Test PASS
  ☐ Week 4: Final Security Audit PASS + CISO Sign-Off
  ☐ Go-Live: Authorized by Security & Business Leadership
```

---

## 6. Common Security Anti-Patterns and Fixes

### Anti-Pattern 1: DAC Not Applied to All Tables

**Problem:**
```
User has DAC on T_SALES but not on V_SALES_SUMMARY
(View defined as: SELECT * FROM T_SALES)

Result: User can access T_SALES → filtered by DAC
        User can access V_SALES_SUMMARY → NO DAC applied → sees all data!
```

**Fix:**
```sql
-- Apply DAC to both base table AND views
CREATE DATA ACCESS CONTROL DAC_SALES_BY_REGION FOR TABLE T_SALES
  WHERE SALES_REGION = :USER_REGION;

CREATE DATA ACCESS CONTROL DAC_SALES_BY_REGION FOR VIEW V_SALES_SUMMARY
  WHERE SALES_REGION = :USER_REGION;

-- Verify:
SELECT TABLE_NAME, DAC_NAME FROM DATASPHERE.DAC_ASSIGNMENTS
WHERE DAC_NAME = 'DAC_SALES_BY_REGION'
ORDER BY TABLE_NAME;

-- Expected: Both T_SALES and V_SALES_SUMMARY listed
```

---

### Anti-Pattern 2: Admin User Sees All Data Despite DAC

**Problem:**
```
Admin user (ROLE='ADMIN') has DAC applied:
  DAC: SALES_REGION = :USER_REGION
  User's REGION attribute: 'Americas'

Result: Admin sees ALL regions (not just Americas)
        DAC bypass not documented
```

**Root Cause:**
- Admin role may have implicit bypass
- Configuration issue in DAC setup

**Fix:**
```sql
-- Option 1: Remove admin user from DAC filter
-- Explicitly exclude admins:
CREATE DATA ACCESS CONTROL DAC_SALES_BY_REGION FOR TABLE T_SALES
  WHERE CASE
    WHEN :USER_ROLE = 'ADMIN' THEN 1 = 1  -- Admins see all
    ELSE SALES_REGION = :USER_REGION       -- Others filtered
  END;

-- Option 2: Keep admin under same DAC (requires admin REGION attribute)
UPDATE T_USER_ATTRIBUTES
  SET ASSIGNED_REGION = 'ALL'
  WHERE USER_ID = 'admin.user';

-- Verify DAC behavior:
SELECT USER_ID, COUNT(*) as visible_rows, COUNT(DISTINCT SALES_REGION) as regions
FROM T_SALES
GROUP BY USER_ID
ORDER BY USER_ID;

-- Check for anomalies: Admin should see similar or more rows than expected
```

---

### Anti-Pattern 3: Audit Logs Not Retained Long Enough

**Problem:**
```
Audit policy configured with 1-year retention
GDPR requires 3-year retention
After 1 year, audit logs auto-deleted

Result: Cannot respond to GDPR data access request (beyond 1 year)
        Regulatory violation
```

**Fix:**
```sql
-- Update audit retention policy
ALTER AUDIT POLICY SOX_COMPLIANCE_AUDIT
  SET RETENTION_PERIOD = 10 YEARS;

ALTER AUDIT POLICY GDPR_COMPLIANCE_AUDIT
  SET RETENTION_PERIOD = 3 YEARS;

-- Archive strategy: Move to cold storage after 1 year
-- but keep for required duration
CREATE PARTITIONED TABLE T_AUDIT_LOG_ARCHIVE (
  PARTITION p_2023 PARTITION BY RANGE (YEAR(AUDIT_TIMESTAMP))
  PARTITION p_2024
  PARTITION p_2025
);

-- Archive job (quarterly):
INSERT INTO T_AUDIT_LOG_ARCHIVE
SELECT * FROM T_AUDIT_LOG
WHERE AUDIT_TIMESTAMP < DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR);

DELETE FROM T_AUDIT_LOG
WHERE AUDIT_TIMESTAMP < DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR);

-- Verify retention:
SELECT
  POLICY_NAME,
  RETENTION_PERIOD,
  PURGE_DATE
FROM DATASPHERE.AUDIT_POLICIES;

-- Expected: All policies meet regulatory requirements
```

---

### Anti-Pattern 4: User Attribute Not Synced with IdP

**Problem:**
```
IdP (Azure AD) has:
  john.smith: ASSIGNED_REGION = 'Americas'

Datasphere has:
  john.smith: ASSIGNED_REGION = 'EMEA'  (stale value)

Result: DAC filters to wrong region (old value)
        User sees unintended data
```

**Root Cause:**
- Manual attribute import → out of sync
- One-time sync → no ongoing updates
- SCIM provisioning not enabled

**Fix:**
```sql
-- Option 1: Enable SCIM (automated provisioning)
-- In IdP settings: Enable SCIM 2.0
-- In Datasphere: Configure SCIM token and endpoint
-- Result: Attributes sync every 15-60 minutes

-- Option 2: Scheduled attribute sync (if SCIM not available)
CREATE SCHEDULED TASK sync_user_attributes
  FREQUENCY: DAILY AT 02:00 UTC
  ACTION: Execute stored procedure;

CREATE PROCEDURE sync_user_attributes AS
  -- Extract from IdP LDAP/API
  DELETE FROM T_USER_ATTRIBUTES_STAGING;
  INSERT INTO T_USER_ATTRIBUTES_STAGING
    SELECT USER_ID, ASSIGNED_REGION, ASSIGNED_COST_CENTER
    FROM LDAP.USERS;  -- Query source IdP

  -- Upsert into Datasphere
  MERGE INTO T_USER_ATTRIBUTES target
  USING T_USER_ATTRIBUTES_STAGING source
  ON target.USER_ID = source.USER_ID
  WHEN MATCHED THEN UPDATE SET
    target.ASSIGNED_REGION = source.ASSIGNED_REGION,
    target.ASSIGNED_COST_CENTER = source.ASSIGNED_COST_CENTER,
    target.SYNC_TIMESTAMP = CURRENT_TIMESTAMP
  WHEN NOT MATCHED THEN INSERT
    VALUES (source.USER_ID, source.ASSIGNED_REGION, source.ASSIGNED_COST_CENTER, CURRENT_TIMESTAMP);

  -- Audit
  INSERT INTO T_ATTRIBUTE_SYNC_LOG
    VALUES (CURRENT_TIMESTAMP, 'SYNC_COMPLETE', @@AFFECTED_ROWS);
END;

-- Verify sync:
SELECT USER_ID, ASSIGNED_REGION, SYNC_TIMESTAMP
FROM T_USER_ATTRIBUTES
WHERE SYNC_TIMESTAMP > CURRENT_TIMESTAMP - INTERVAL 1 HOUR
ORDER BY SYNC_TIMESTAMP DESC;
```

---

### Anti-Pattern 5: No Segregation of Duties

**Problem:**
```
Same person (john.smith) assigned both:
  - Role: PURCHASE_REQUISITIONER (create POs)
  - Role: PAYMENT_APPROVER (approve payments)

Result: john.smith can requisition AND approve his own request
        Fraud control broken
```

**Fix:**
```sql
-- Define SoD rules
CREATE TABLE T_SEGREGATION_OF_DUTIES_RULES (
  RULE_ID INTEGER PRIMARY KEY,
  CONFLICT_ROLE_1 VARCHAR(100),
  CONFLICT_ROLE_2 VARCHAR(100),
  REASON VARCHAR(500),
  ENFORCEMENT VARCHAR(20)  -- PREVENT or MONITOR
);

INSERT INTO T_SEGREGATION_OF_DUTIES_RULES VALUES
  (1, 'PURCHASE_REQUISITIONER', 'PAYMENT_APPROVER',
   'Cannot request and approve own payment', 'PREVENT'),
  (2, 'TRANSACTION_CREATOR', 'TRANSACTION_AUDITOR',
   'Auditor must not create transactions they audit', 'PREVENT'),
  (3, 'USER_ADMIN', 'DATA_ADMIN',
   'User mgmt and data mgmt must be separate', 'MONITOR');

-- Validation: Check for SoD violations
SELECT u.USER_ID, COUNT(DISTINCT ur.ROLE_ID) as role_count
FROM T_USERS u
JOIN T_USER_ROLES ur ON u.USER_ID = ur.USER_ID
WHERE EXISTS (
  SELECT 1 FROM T_SEGREGATION_OF_DUTIES_RULES sod
  WHERE sod.CONFLICT_ROLE_1 IN (SELECT ur2.ROLE_ID
                                 FROM T_USER_ROLES ur2
                                 WHERE ur2.USER_ID = u.USER_ID)
    AND sod.CONFLICT_ROLE_2 IN (SELECT ur3.ROLE_ID
                                FROM T_USER_ROLES ur3
                                WHERE ur3.USER_ID = u.USER_ID)
    AND sod.ENFORCEMENT = 'PREVENT'
)
GROUP BY u.USER_ID;

-- If results found: Remove conflicting role assignments
-- Example: john.smith → remove PAYMENT_APPROVER role
```

---

## 7. Emergency Access Procedures

### Emergency Access When Normal IdP Unavailable

**Scenario:** Azure AD outage, users cannot log in via SAML.

```yaml
Emergency Access Procedure (Break-Glass):

Trigger Conditions:
  ☐ IdP unavailable for > 15 minutes
  ☐ Critical business operations blocked
  ☐ Approval from CISO/Security Lead obtained

Pre-Requisites:
  ☐ Emergency access accounts created and secured
  ☐ Temporary credentials stored in secure vault (Vault, AWS Secrets Manager)
  ☐ Access log prepared for audit trail
  ☐ Rollback plan documented

Step 1: Declare Emergency (5 min)
  ☐ CISO/Security Lead confirms IdP issue
  ☐ Escalation email sent to incident response team
  ☐ Status page updated: "Emergency access enabled"
  ☐ Timer started: Document emergency duration

Step 2: Authenticate User via Emergency Account (5 min)
  ☐ User provides: Employee ID, Manager approval, Business justification
  ☐ Validate against employee database
  ☐ Call user's manager to verbally confirm (if possible)
  ☐ Issue temporary password (e.g., TempPass_2024_ABC123)
  ☐ Force password change on first login

Step 3: Grant Temporary Access (5 min)
  ☐ Assign minimal required roles (NOT admin roles)
  ☐ Apply restrictive DACs (if any changes to standard)
  ☐ Limit session duration: 4 hours max
  ☐ Enable IP whitelist if possible
  ☐ Log all assignments in T_EMERGENCY_ACCESS_LOG

Step 4: Audit & Monitoring (ongoing)
  ☐ Monitor user session closely
  ☐ Alert on: Data exports, schema changes, privilege escalation attempts
  ☐ Capture detailed audit logs: Every query, every data access
  ☐ Disable access immediately after business need satisfied (not waiting 4 hours)

Step 5: Revoke Emergency Access (at resolution)
  ☐ IdP restored and working
  ☐ Confirm all users can log in normally
  ☐ Disable all temporary accounts
  ☐ Force password change required on next IdP login
  ☐ Deactivate emergency session tokens

Step 6: Post-Emergency Audit (within 24 hours)
  ☐ Review audit log: T_EMERGENCY_ACCESS_LOG
  ☐ Verify all access was legitimate
  ☐ Check for data exfiltration or unauthorized changes
  ☐ Document findings in incident report
  ☐ Update incident management system (e.g., Jira, ServiceNow)

Template: Emergency Access Log Entry
  ┌────────────────────────────────────────┐
  │ Emergency Access Event Log             │
  ├────────────────────────────────────────┤
  │ Incident ID: INC-2024-0234            │
  │ User ID: john.smith@contoso.com       │
  │ Access Type: Temporary Login           │
  │ Reason: Azure AD outage (03:00-04:30 UTC) │
  │ Authorized By: CISO - Jane Doe         │
  │ Grant Time: 2024-02-08 03:15 UTC       │
  │ Revoke Time: 2024-02-08 04:45 UTC      │
  │ Duration: 1.5 hours                    │
  │ Roles Granted: VIEWER                  │
  │ DACs Applied: Standard                 │
  │ Queries Executed: 12                   │
  │ Data Accessed: T_SALES (4 rows)        │
  │ Audit: REVIEWED & APPROVED              │
  │ Reviewer: Internal Audit Team          │
  └────────────────────────────────────────┘

RTO (Recovery Time Objective): 15 minutes
  - Emergency access available within 15 min of IdP failure

Frequency Review:
  - Quarterly: Validate emergency accounts still work
  - Semi-annually: Update authorized personnel list
  - Annually: Run mock emergency access drill
```

---

### Permanent Account Deprovisioning

**When:** Employee termination, role change, access revocation.

```yaml
Deprovisioning Checklist:

T+0 (Termination Date):
  ☐ HR notifies IT/Security of termination
  ☐ Collect all devices (laptop, phone, badge)
  ☐ Take note of time (often end-of-business Friday)

T+1 hour (Immediate Actions):
  ☐ Disable IdP account (Azure AD, Okta, etc.)
  ☐ Revoke session tokens (logout all sessions)
  ☐ Disable Datasphere user account
  ☐ Remove user from all roles and spaces
  ☐ Revoke API tokens/credentials
  ☐ Log action: T_USER_DEPROVISIONING_LOG

T+1 day (Extended Access Cleanup):
  ☐ Check for shared passwords (vault) → change all
  ☐ Remove from security groups and mailing lists
  ☐ Transfer file ownership to manager
  ☐ Archive email (if required by retention policy)
  ☐ Document what data user created/owns

T+30 days (Archival):
  ☐ Review audit logs for any activity post-termination (should be zero)
  ☐ Archive all user session logs
  ☐ Delete audit events > 30 days old (unless regulatory hold)
  ☐ Confirm no data leakage occurred
  ☐ Final sign-off from Security/Compliance

Template: User Deprovisioning Checklist
  User: john.smith@contoso.com
  Termination Date: 2024-02-08
  Reason: Voluntary resignation

  Deprovisioning Steps:
    ☐ [02/08 17:00] HR notification received
    ☐ [02/08 17:15] Datasphere access disabled
    ☐ [02/08 17:30] Azure AD account disabled
    ☐ [02/08 17:45] All sessions terminated
    ☐ [02/09 09:00] Shared credentials changed
    ☐ [02/09 10:00] File access transferred to manager
    ☐ [02/09 11:00] Email archived
    ☐ [02/10] Audit log review completed (no suspicious activity)
    ☐ [02/10] Final approval: Security & Compliance sign-off

  Risk Assessment:
    Access Duration: 4 years
    Data Accessed: T_CUSTOMER_PII, T_FINANCIAL
    Export Capability: YES (standard role)
    Suspicious Activity: NONE detected
    Conclusion: LOW RISK - Clean deprovisioning
```

---

End of Security Architect Reference Guide

