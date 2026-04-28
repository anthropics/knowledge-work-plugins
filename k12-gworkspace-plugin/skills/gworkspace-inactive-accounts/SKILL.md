---
name: gworkspace-inactive-accounts
description: >
  Find stale, dormant, or inactive Google Workspace accounts — users who have
  not signed in for 30, 60, or 90+ days. Use when auditing inactive staff
  accounts, cleaning up dormant accounts before a compliance review, finding
  accounts that should be suspended after employee departures, or reducing the
  attack surface from unused logins. Triggers on: "inactive Google accounts",
  "who hasn't logged into Google", "stale Google accounts", "dormant Workspace
  users", "Google accounts to disable", "unused Google logins", "last Google
  sign-in audit", "Google offboarding cleanup".
---

# Google Workspace Inactive Accounts Audit

## Purpose
Identify Google Workspace accounts with no recent login activity.
Helps enforce least-privilege access, support offboarding, and reduce attack
surface from unused credentials.

## Authentication
- **Key file:** `~/path/to/your/google_service_account.json`
- **Admin impersonation:** `admin@yourdomain.org`
- **Scopes:** `admin.reports.usage.readonly`, `admin.directory.user.readonly`

See [CONNECTORS.md](../../CONNECTORS.md) for full setup instructions.

## Report Output
`~/path/to/your/reports/YYYYMMDD_GWorkspace_Inactive_Accounts.xlsx`

## Steps

### Step 1 — Generate the Report
Run the following Python script in Terminal (or save as a `.py` file and execute):

```python
#!/usr/bin/env python3
"""GWorkspace Inactive Accounts Audit"""
import os, json, datetime, openpyxl
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE    = os.path.expanduser("~/path/to/your/google_service_account.json")
ADMIN_EMAIL = "admin@yourdomain.org"
DOMAIN      = "yourdomain.org"
REPORT_DIR  = os.path.expanduser("~/path/to/your/reports")
SCOPES = [
    "https://www.googleapis.com/auth/admin.reports.usage.readonly",
    "https://www.googleapis.com/auth/admin.directory.user.readonly",
]
THRESHOLDS = [30, 60, 90]  # days

creds = service_account.Credentials.from_service_account_file(
    KEY_FILE, scopes=SCOPES
).with_subject(ADMIN_EMAIL)

dir_svc = build("admin", "directory_v1", credentials=creds)

today = datetime.date.today()
users = {}
token = None
while True:
    resp = dir_svc.users().list(
        domain=DOMAIN, maxResults=500, pageToken=token,
        orderBy="email", projection="full"
    ).execute()
    for u in resp.get("users", []):
        last = u.get("lastLoginTime", "")
        if last and last != "1970-01-01T00:00:00.000Z":
            try:
                dt = datetime.datetime.fromisoformat(last.replace("Z", "+00:00")).date()
                days = (today - dt).days
            except Exception:
                days = None
        elif last == "1970-01-01T00:00:00.000Z":
            days = 99999  # Never logged in
        else:
            days = None
        users[u["primaryEmail"]] = {
            "name": u.get("name", {}).get("fullName", ""),
            "ou": u.get("orgUnitPath", "/"),
            "suspended": u.get("suspended", False),
            "last_login": last[:10] if last else "Unknown",
            "days_inactive": days,
        }
    token = resp.get("nextPageToken")
    if not token:
        break

os.makedirs(REPORT_DIR, exist_ok=True)
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Inactive Accounts"

header = ["Email", "Full Name", "OU", "Last Login", "Days Inactive", "Suspended",
          "Flag 30d", "Flag 60d", "Flag 90d"]
for col, h in enumerate(header, 1):
    ws.cell(row=1, column=col, value=h)

for row, (email, d) in enumerate(sorted(users.items()), 2):
    di = d["days_inactive"]
    ws.cell(row=row, column=1, value=email)
    ws.cell(row=row, column=2, value=d["name"])
    ws.cell(row=row, column=3, value=d["ou"])
    ws.cell(row=row, column=4, value=d["last_login"])
    ws.cell(row=row, column=5, value=di if di != 99999 else "Never")
    ws.cell(row=row, column=6, value="Yes" if d["suspended"] else "No")
    ws.cell(row=row, column=7, value="YES" if di and di >= 30 else "")
    ws.cell(row=row, column=8, value="YES" if di and di >= 60 else "")
    ws.cell(row=row, column=9, value="YES" if di and di >= 90 else "")

date_str = today.strftime("%Y%m%d")
out = os.path.join(REPORT_DIR, f"{date_str}_GWorkspace_Inactive_Accounts.xlsx")
wb.save(out)
print(f"✅ Report saved: {out}")
print(f"   Total users: {len(users)}")
for t in THRESHOLDS:
    c = sum(1 for d in users.values() if d["days_inactive"] and d["days_inactive"] >= t)
    print(f"   Inactive {t}+d: {c}")
never = sum(1 for d in users.values() if d["days_inactive"] == 99999)
print(f"   Never logged in: {never}")
```

### Step 2 — Review the Report
Open the Excel file. Key columns:
- **Flag 90d = YES** → Priority for suspension or deletion (cross-ref with HR)
- **Flag 60d = YES** → Review with supervisor
- **Flag 30d = YES** → Monitor / notify user
- **Never logged in** → May be legacy migration accounts — bulk review recommended

### Step 3 — Cross-Reference with HR
Before suspending accounts, verify with HR that the employee is no longer active.
Suspend first rather than delete — deletions of synced accounts must happen at the
source (on-prem Active Directory if you are running a hybrid environment).

### Step 4 — Document Actions
Note which accounts were suspended and why. Add to your security dashboard in Notion
if running as part of a security review cycle.

## Important Notes
- In hybrid (on-prem AD + Google Workspace) environments, account deletions must occur at the source
- Suspended accounts retain data and can be reactivated
- Never-logged-in accounts may be legacy migration artifacts — verify before bulk suspending
- Student accounts follow a different lifecycle — coordinate with the registrar before actioning
