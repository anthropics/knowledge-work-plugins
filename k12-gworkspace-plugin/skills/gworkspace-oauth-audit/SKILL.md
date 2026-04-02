---
name: gworkspace-oauth-audit
description: >
  Audit all third-party apps and OAuth permissions granted access to your
  Google Workspace accounts. Use when checking which apps have been granted
  access to school data, finding apps with overly broad permissions, identifying
  apps that staff approved without IT review, removing suspicious or unused app
  permissions, or running an app consent audit before a compliance review.
  Triggers on: "GWorkspace OAuth audit", "Google app permissions", "third-party
  Google apps", "what apps can access our Google data", "app consent Google",
  "Google Workspace app audit", "which apps are connected to Google",
  "remove Google app access", "FERPA Google apps".
---

# Google Workspace OAuth App Audit

## Purpose
Identify all third-party applications that have been granted OAuth access
to your Google Workspace accounts. FERPA compliance requires knowing exactly
which external apps can read student or staff data.

## Authentication
- **Key file:** `~/path/to/your/google_service_account.json`
- **Admin impersonation:** `admin@yourdomain.org`
- **Scopes:** `admin.reports.audit.readonly`

See [CONNECTORS.md](../../CONNECTORS.md) for full setup instructions.

## ⚠️ FERPA Note
Apps granted scopes like `drive.readonly`, `gmail.readonly`, `contacts.readonly`,
or `calendar` can access student data. These require review for FERPA compliance.

## Report Output
`~/path/to/your/reports/YYYYMMDD_GWorkspace_OAuth_Audit.xlsx`

## Steps

### Step 1 — Pull OAuth Token Grant Events
Query the admin audit log for token authorization events:

```python
#!/usr/bin/env python3
"""GWorkspace OAuth App Audit"""
import os, datetime, openpyxl
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE    = os.path.expanduser("~/path/to/your/google_service_account.json")
ADMIN_EMAIL = "admin@yourdomain.org"
REPORT_DIR  = os.path.expanduser("~/path/to/your/reports")
SCOPES = ["https://www.googleapis.com/auth/admin.reports.audit.readonly"]

# High-risk OAuth scopes
HIGH_RISK_SCOPES = {
    "https://mail.google.com/",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/contacts",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/admin.directory.user",
    "https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.rosters",
}

creds = service_account.Credentials.from_service_account_file(
    KEY_FILE, scopes=SCOPES
).with_subject(ADMIN_EMAIL)
svc = build("admin", "reports_v1", credentials=creds)

today = datetime.date.today()
start = (today - datetime.timedelta(days=180)).strftime("%Y-%m-%dT00:00:00Z")

grants = []
token = None
while True:
    resp = svc.activities().list(
        userKey="all",
        applicationName="token",
        startTime=start,
        maxResults=1000,
        pageToken=token,
    ).execute()

    for act in resp.get("items", []):
        actor = act.get("actor", {}).get("email", "Unknown")
        time  = act.get("id", {}).get("time", "")[:10]
        for event in act.get("events", []):
            name = event.get("name", "")
            if name != "authorize":
                continue
            params    = {p["name"]: p.get("value", "") for p in event.get("parameters", [])}
            app_name  = params.get("app_name", "Unknown App")
            scopes    = params.get("scope", "")
            client_id = params.get("client_id", "")

            # Determine risk
            scope_list = [s.strip() for s in scopes.split()]
            high_risk  = any(s in HIGH_RISK_SCOPES for s in scope_list)
            risk = "HIGH" if high_risk else "MEDIUM" if scopes else "LOW"

            grants.append({
                "time":      time,
                "user":      actor,
                "app":       app_name,
                "client_id": client_id,
                "scopes":    scopes,
                "risk":      risk,
            })

    token = resp.get("nextPageToken")
    if not token:
        break

# Deduplicate by (app, user, scopes)
seen = set()
unique_grants = []
for g in grants:
    key = (g["app"], g["user"], g["scopes"])
    if key not in seen:
        seen.add(key)
        unique_grants.append(g)

# Sort: HIGH first
unique_grants.sort(key=lambda x: (0 if x["risk"] == "HIGH" else 1 if x["risk"] == "MEDIUM" else 2))

os.makedirs(REPORT_DIR, exist_ok=True)
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "OAuth Grants"
header = ["Date", "User", "App Name", "Client ID", "Scopes", "Risk Level"]
for col, h in enumerate(header, 1):
    ws.cell(row=1, column=col, value=h)
for row, g in enumerate(unique_grants, 2):
    ws.cell(row=row, column=1, value=g["time"])
    ws.cell(row=row, column=2, value=g["user"])
    ws.cell(row=row, column=3, value=g["app"])
    ws.cell(row=row, column=4, value=g["client_id"])
    ws.cell(row=row, column=5, value=g["scopes"])
    ws.cell(row=row, column=6, value=g["risk"])

date_str = today.strftime("%Y%m%d")
out = os.path.join(REPORT_DIR, f"{date_str}_GWorkspace_OAuth_Audit.xlsx")
wb.save(out)
high = sum(1 for g in unique_grants if g["risk"] == "HIGH")
print(f"✅ Report saved: {out}")
print(f"   Unique OAuth grants (180d): {len(unique_grants)}")
print(f"   HIGH-risk grants: {high}")
```

### Step 2 — Review High-Risk Apps
Focus on HIGH-risk grants (access to Drive, Gmail, Contacts, Classroom):
- Is this a vendor-approved ed-tech tool?
- Did staff authorize it themselves without IT review?
- Does it need access to student data? Is it FERPA-compliant?

### Step 3 — Revoke Suspicious Grants
To revoke an app's access for a specific user:
1. Go to **Google Admin Console** → Security → API Controls → App Access Control
2. Find the app → click to manage → revoke access
3. Or instruct the user to go to **myaccount.google.com** → Security → Third-party apps

For domain-wide revocation:
- Admin Console → Security → API Controls → Block untrusted apps

### Step 4 — Document Decisions
For each HIGH-risk app, document in the report:
- **Approved:** Authorized ed-tech tool (e.g., Google Classroom integrations)
- **Pending Review:** Needs FERPA assessment
- **Revoked:** Access removed

## Common Apps to Watch
| App | Risk | Notes |
|-----|------|-------|
| ChatGPT/OpenAI | HIGH | FERPA concern — potential student data exposure |
| Zapier | HIGH | Automation — depends on what's connected |
| Grammarly | MEDIUM | Gmail access — review permissions |
| Canva | LOW | Typically Drive read — usually OK |
| LMS integrations | VARIES | Canvas, Schoology, etc. — usually pre-approved |

## Important Notes
- Token audit log covers ~180 days via the Reports API
- The token log captures grant events, not the current complete list of authorized apps
- For a definitive current inventory: Admin Console → Security → API Controls → App Access Control
- Student accounts authorizing non-approved apps is a policy violation even if low-risk
