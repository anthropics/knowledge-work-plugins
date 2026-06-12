---
name: gworkspace-storage-report
description: >
  Generate a Google Workspace Drive storage usage report — who is using the
  most storage, identify heavy users, find accounts approaching limits, and
  plan storage management before quotas are hit. Use when auditing storage
  consumption, preparing for a storage cleanup, identifying users who need
  storage limit adjustments, or generating a capacity planning report.
  Triggers on: "Google storage report", "who is using the most Drive space",
  "GWorkspace storage audit", "storage usage by user", "Drive capacity report",
  "Google Workspace storage", "storage quota report", "who has big Drive".
---

# Google Workspace Storage Usage Report

## Purpose
Generate a per-user storage breakdown across Google Drive and Gmail for all
accounts in your organization. Supports capacity planning and quota management.

## Authentication
- **Key file:** `~/path/to/your/google_service_account.json`
- **Admin impersonation:** `admin@yourdomain.org`
- **Scopes:** `admin.reports.usage.readonly`, `admin.directory.user.readonly`

See [CONNECTORS.md](../../CONNECTORS.md) for full setup instructions.

## Report Output
`~/path/to/your/reports/YYYYMMDD_GWorkspace_Storage_Report.xlsx`

## Steps

### Step 1 — Pull Usage Report
Run the following script to query per-user storage metrics:

```python
#!/usr/bin/env python3
"""GWorkspace Storage Usage Report"""
import os, datetime, openpyxl
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE    = os.path.expanduser("~/path/to/your/google_service_account.json")
ADMIN_EMAIL = "admin@yourdomain.org"
REPORT_DIR  = os.path.expanduser("~/path/to/your/reports")
SCOPES = [
    "https://www.googleapis.com/auth/admin.reports.usage.readonly",
    "https://www.googleapis.com/auth/admin.directory.user.readonly",
]

def gb(bytes_val):
    """Convert bytes to GB, rounded to 2 decimal places."""
    if bytes_val is None:
        return 0.0
    return round(int(bytes_val) / (1024 ** 3), 2)

creds = service_account.Credentials.from_service_account_file(
    KEY_FILE, scopes=SCOPES
).with_subject(ADMIN_EMAIL)
svc = build("admin", "reports_v1", credentials=creds)

# Usage reports use yesterday's date
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

usage = {}
token = None
while True:
    try:
        resp = svc.userUsageReport().get(
            userKey="all",
            date=yesterday,
            parameters="drive:num_items_created,drive:storage_used,gmail:storage_used,accounts:is_super_admin",
            maxResults=500,
            pageToken=token,
        ).execute()
    except Exception as e:
        print(f"⚠️  Usage report error: {e}")
        break

    for record in resp.get("usageReports", []):
        email  = record.get("entity", {}).get("userEmail", "")
        params = {p["name"]: p.get("intValue", p.get("boolValue", ""))
                  for p in record.get("parameters", [])}
        usage[email] = {
            "drive_gb":    gb(params.get("drive:storage_used")),
            "gmail_gb":    gb(params.get("gmail:storage_used")),
            "drive_items": params.get("drive:num_items_created", 0),
            "is_admin":    params.get("accounts:is_super_admin", False),
        }

    token = resp.get("nextPageToken")
    if not token:
        break

# Sort by total storage desc
sorted_users = sorted(usage.items(),
    key=lambda x: x[1]["drive_gb"] + x[1]["gmail_gb"], reverse=True)

os.makedirs(REPORT_DIR, exist_ok=True)
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Storage by User"
header = ["Email", "Drive (GB)", "Gmail (GB)", "Total (GB)",
          "Drive Items", "Admin", "Flag"]
for col, h in enumerate(header, 1):
    ws.cell(row=1, column=col, value=h)

for row, (email, d) in enumerate(sorted_users, 2):
    total = d["drive_gb"] + d["gmail_gb"]
    flag  = ""
    if total > 10:
        flag = "REVIEW (>10GB)"
    elif total > 5:
        flag = "MONITOR (>5GB)"
    ws.cell(row=row, column=1, value=email)
    ws.cell(row=row, column=2, value=d["drive_gb"])
    ws.cell(row=row, column=3, value=d["gmail_gb"])
    ws.cell(row=row, column=4, value=total)
    ws.cell(row=row, column=5, value=d["drive_items"])
    ws.cell(row=row, column=6, value="Yes" if d["is_admin"] else "No")
    ws.cell(row=row, column=7, value=flag)

date_str = datetime.date.today().strftime("%Y%m%d")
out = os.path.join(REPORT_DIR, f"{date_str}_GWorkspace_Storage_Report.xlsx")
wb.save(out)

total_drive  = sum(d["drive_gb"] for _, d in usage.items())
total_gmail  = sum(d["gmail_gb"] for _, d in usage.items())
flagged      = sum(1 for _, d in usage.items() if d["drive_gb"] + d["gmail_gb"] > 10)
print(f"✅ Report saved: {out}")
print(f"   Users analyzed: {len(usage)}")
print(f"   Total Drive usage: {total_drive:.1f} GB")
print(f"   Total Gmail usage: {total_gmail:.1f} GB")
print(f"   Users >10 GB (review): {flagged}")
```

### Step 2 — Review Top Consumers
Open the Excel report. The top users by storage are sorted first:
- **>10 GB flagged as REVIEW** — contact user to archive or delete large files
- **>5 GB flagged as MONITOR** — note for next quarter review
- Look for suspended or departed staff accounts still holding large amounts of storage — these can be exported then deleted

### Step 3 — Capacity Planning
With Education licenses, Google Workspace pools storage across the organization.
Key metrics:
- **Total pooled storage:** Check Admin Console → Reports → Storage
- **Top consumers:** Use this report to identify candidates for cleanup
- **Departed staff data:** Run alongside the Inactive Accounts audit and export valuable data before suspending accounts

### Step 4 — Actions
| Situation | Action |
|-----------|--------|
| Active user >10 GB | Email user to clean up Drive/Gmail; offer guidance |
| Departed user >5 GB | Review content → export if needed → delete account |
| Domain approaching limit | Identify top 10 users → target cleanup campaign |
| Student accounts growing | Review retention policy — purge graduated cohorts |

## Important Notes
- Usage reports are based on the previous day's snapshot — not real-time
- Google Workspace for Education pooled storage is shared across the domain
- Photos, Drive, and Gmail all consume from the same pool
- Shared drives (Team Drives) storage is attributed to the shared drive, not individual users
- Script uses `yesterday` as the report date; if run early in the morning and no data appears, try `yesterday - 1`
