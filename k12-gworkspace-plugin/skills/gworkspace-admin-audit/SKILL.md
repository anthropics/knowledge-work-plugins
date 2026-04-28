---
name: gworkspace-admin-audit
description: >
  Audit Google Workspace administrator activity — flag suspicious admin actions,
  check who has admin privileges, review recent admin log events, and identify
  over-privileged or dormant admin accounts. Use when reviewing admin access,
  checking for unauthorized changes, performing a quarterly admin access review,
  or preparing for a compliance audit. Triggers on: "GWorkspace admin audit",
  "who has Google admin access", "Google admin activity", "suspicious admin
  actions", "GWorkspace admin review", "Google Workspace privilege audit",
  "check admin log", "what did admins do in Google".
---

# Google Workspace Admin Audit

## Purpose
Review admin-level activity on your Google Workspace domain — who did what, when,
and whether any actions look suspicious or unauthorized.

## Authentication
- **Key file:** `~/path/to/your/google_service_account.json`
- **Admin impersonation:** `admin@yourdomain.org`
- **Scopes:** `admin.reports.audit.readonly`, `admin.directory.user.readonly`

See [CONNECTORS.md](../../CONNECTORS.md) for full setup instructions.

## Report Output
`~/path/to/your/reports/YYYYMMDD_GWorkspace_Admin_Audit.xlsx`

## Steps

### Step 1 — Pull Admin Activity Log
Run the following script to query admin audit events:

```python
#!/usr/bin/env python3
"""GWorkspace Admin Activity Audit"""
import os, datetime, openpyxl
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE    = os.path.expanduser("~/path/to/your/google_service_account.json")
ADMIN_EMAIL = "admin@yourdomain.org"
DOMAIN      = "yourdomain.org"
REPORT_DIR  = os.path.expanduser("~/path/to/your/reports")
SCOPES = [
    "https://www.googleapis.com/auth/admin.reports.audit.readonly",
    "https://www.googleapis.com/auth/admin.directory.user.readonly",
]

# High-risk event names to flag
HIGH_RISK_EVENTS = {
    "GRANT_ADMIN_PRIVILEGE", "REVOKE_ADMIN_PRIVILEGE",
    "DELETE_USER", "SUSPEND_USER", "UNSUSPEND_USER",
    "CREATE_USER", "CHANGE_PASSWORD",
    "ADD_GROUP_MEMBER", "REMOVE_GROUP_MEMBER",
    "CHANGE_APPLICATION_SETTING", "TOGGLE_SERVICE_ENABLED",
    "CHANGE_DOMAIN_SETTING", "RENAME_USER",
}

creds = service_account.Credentials.from_service_account_file(
    KEY_FILE, scopes=SCOPES
).with_subject(ADMIN_EMAIL)
svc = build("admin", "reports_v1", credentials=creds)

today = datetime.date.today()
start = (today - datetime.timedelta(days=90)).strftime("%Y-%m-%dT00:00:00Z")

events = []
token = None
while True:
    resp = svc.activities().list(
        userKey="all",
        applicationName="admin",
        startTime=start,
        maxResults=1000,
        pageToken=token,
    ).execute()

    for act in resp.get("items", []):
        actor = act.get("actor", {}).get("email", "Unknown")
        time  = act.get("id", {}).get("time", "")[:10]
        for event in act.get("events", []):
            name   = event.get("name", "")
            params = {p["name"]: p.get("value", p.get("multiValue", ""))
                      for p in event.get("parameters", [])}
            risk = "HIGH" if name in HIGH_RISK_EVENTS else "LOW"
            events.append({
                "time":    time,
                "actor":   actor,
                "event":   name,
                "target":  params.get("USER_EMAIL", params.get("SETTING_NAME", "")),
                "details": str(params),
                "risk":    risk,
            })

    token = resp.get("nextPageToken")
    if not token:
        break

# Sort: HIGH first, then by date desc
events.sort(key=lambda x: (0 if x["risk"] == "HIGH" else 1, x["time"]), reverse=False)

os.makedirs(REPORT_DIR, exist_ok=True)
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Admin Activity"
header = ["Date", "Actor", "Event", "Target", "Risk Level", "Details"]
for col, h in enumerate(header, 1):
    ws.cell(row=1, column=col, value=h)
for row, e in enumerate(events, 2):
    ws.cell(row=row, column=1, value=e["time"])
    ws.cell(row=row, column=2, value=e["actor"])
    ws.cell(row=row, column=3, value=e["event"])
    ws.cell(row=row, column=4, value=e["target"])
    ws.cell(row=row, column=5, value=e["risk"])
    ws.cell(row=row, column=6, value=e["details"])

date_str = today.strftime("%Y%m%d")
out = os.path.join(REPORT_DIR, f"{date_str}_GWorkspace_Admin_Audit.xlsx")
wb.save(out)
high = sum(1 for e in events if e["risk"] == "HIGH")
print(f"✅ Report saved: {out}")
print(f"   Total admin events (90d): {len(events)}")
print(f"   HIGH-risk events: {high}")
```

### Step 2 — Review High-Risk Events
Focus on HIGH-risk events first:
- **GRANT_ADMIN_PRIVILEGE** — Was this authorized? Who was granted admin access?
- **DELETE_USER** — Were all deletions expected (offboarding)?
- **CHANGE_APPLICATION_SETTING** — Were security settings changed without IT approval?
- **CREATE_USER** — Was this a sanctioned new hire or IT action?

Look for patterns: actions taken outside business hours, actions by vendor accounts, or actions targeting sensitive accounts.

### Step 3 — Admin Privilege Inventory
Pull current admin accounts separately if needed:

```python
# Quick admin account listing (add to script or run standalone)
dir_svc = build("admin", "directory_v1", credentials=creds)
resp = dir_svc.users().list(
    domain=DOMAIN, query="isAdmin=true", maxResults=200
).execute()
for u in resp.get("users", []):
    print(u["primaryEmail"], u.get("name", {}).get("fullName", ""))
```

### Step 4 — Flag Suspicious Activity
Red flags to escalate immediately:
- Admin actions from unknown or external accounts
- Privilege grants or revocations not initiated by your authorized IT admin accounts
- Password changes on admin accounts
- Service toggles affecting all users
- Actions occurring in the middle of the night or on weekends

### Step 5 — Document and Remediate
- Unauthorized changes → revert immediately and investigate
- Excess admin accounts → revoke roles after verifying with account owners
- Findings → save in your incident reports folder

## Important Notes
- Admin audit log covers ~90 days via the Reports API
- Vendor admin accounts should be reviewed quarterly and removed when the engagement ends
- Any GRANT_ADMIN_PRIVILEGE event not initiated by your IT team requires investigation
