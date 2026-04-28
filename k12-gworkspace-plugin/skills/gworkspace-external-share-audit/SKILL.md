---
name: gworkspace-external-share-audit
description: >
  Audit Google Drive files shared outside your organization's domain —
  publicly accessible links, files shared with external email addresses, or
  folders accessible to anyone with a link. This is the highest-priority
  Google Workspace security and FERPA compliance check. Use when auditing
  external file sharing, checking for FERPA violations, reviewing Drive
  permissions before a compliance audit, or finding files shared with
  non-domain accounts. Triggers on: "external Drive sharing", "files shared
  outside school", "Google Drive FERPA audit", "who can see our Google files",
  "public Drive links", "Drive sharing audit", "external share report",
  "anyone with link", "files shared with parents or vendors".
---

# Google Drive External Share Audit

## Purpose
Identify Google Drive files and folders shared outside your organization's domain —
a critical FERPA compliance requirement for K-12 schools.

## Authentication
- **Key file:** `~/path/to/your/google_service_account.json`
- **Admin impersonation:** `admin@yourdomain.org`
- **Scopes:** `admin.reports.audit.readonly`

See [CONNECTORS.md](../../CONNECTORS.md) for full setup instructions.

## ⚠️ FERPA Priority
Drive external sharing is the #1 Google Workspace FERPA risk. Files shared:
- **Anyone with the link** (PUBLIC) — no authentication required
- **Specific external emails** — parents, vendors, former staff
- **External domains** — non-domain Google accounts

Any of these could expose student records, grades, or PII.

## Report Output
`~/path/to/your/reports/YYYYMMDD_GWorkspace_External_Share_Audit.xlsx`

## Steps

### Step 1 — Pull Drive Sharing Audit Events
Run the following script to query the Admin SDK Drive audit log:

```python
#!/usr/bin/env python3
"""GWorkspace External Share Audit"""
import os, datetime, openpyxl
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE    = os.path.expanduser("~/path/to/your/google_service_account.json")
ADMIN_EMAIL = "admin@yourdomain.org"
DOMAIN      = "yourdomain.org"
REPORT_DIR  = os.path.expanduser("~/path/to/your/reports")
SCOPES = ["https://www.googleapis.com/auth/admin.reports.audit.readonly"]

creds = service_account.Credentials.from_service_account_file(
    KEY_FILE, scopes=SCOPES
).with_subject(ADMIN_EMAIL)
svc = build("admin", "reports_v1", credentials=creds)

today = datetime.date.today()
start = (today - datetime.timedelta(days=90)).strftime("%Y-%m-%dT00:00:00Z")

findings = []
token = None
while True:
    resp = svc.activities().list(
        userKey="all",
        applicationName="drive",
        startTime=start,
        maxResults=1000,
        pageToken=token,
        eventName="change_user_access",
    ).execute()

    for act in resp.get("items", []):
        actor = act.get("actor", {}).get("email", "Unknown")
        for event in act.get("events", []):
            params = {p["name"]: p.get("value", "") for p in event.get("parameters", [])}
            target     = params.get("target_user", "")
            visibility = params.get("visibility", "")
            doc_title  = params.get("doc_title", "Unknown file")
            doc_type   = params.get("doc_type", "")
            owner      = params.get("owner", "")

            # Flag external shares
            is_public   = visibility in ("people_with_link", "public_on_the_web")
            is_external = target and "@" in target and not target.endswith(f"@{DOMAIN}")

            if is_public or is_external:
                findings.append({
                    "time":        act.get("id", {}).get("time", "")[:10],
                    "actor":       actor,
                    "doc_title":   doc_title,
                    "doc_type":    doc_type,
                    "owner":       owner,
                    "shared_with": target if is_external else "Anyone with link",
                    "visibility":  visibility,
                    "risk":        "HIGH" if is_public else "MEDIUM",
                })

    token = resp.get("nextPageToken")
    if not token:
        break

os.makedirs(REPORT_DIR, exist_ok=True)
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "External Shares"
header = ["Date", "Actor", "File Title", "File Type", "Owner",
          "Shared With", "Visibility", "Risk Level"]
for col, h in enumerate(header, 1):
    ws.cell(row=1, column=col, value=h)

for row, f in enumerate(sorted(findings, key=lambda x: x["risk"]), 2):
    ws.cell(row=row, column=1, value=f["time"])
    ws.cell(row=row, column=2, value=f["actor"])
    ws.cell(row=row, column=3, value=f["doc_title"])
    ws.cell(row=row, column=4, value=f["doc_type"])
    ws.cell(row=row, column=5, value=f["owner"])
    ws.cell(row=row, column=6, value=f["shared_with"])
    ws.cell(row=row, column=7, value=f["visibility"])
    ws.cell(row=row, column=8, value=f["risk"])

date_str = today.strftime("%Y%m%d")
out = os.path.join(REPORT_DIR, f"{date_str}_GWorkspace_External_Share_Audit.xlsx")
wb.save(out)
high = sum(1 for f in findings if f["risk"] == "HIGH")
med  = sum(1 for f in findings if f["risk"] == "MEDIUM")
print(f"✅ Report saved: {out}")
print(f"   Total external share events: {len(findings)}")
print(f"   HIGH (public/anyone-with-link): {high}")
print(f"   MEDIUM (specific external user): {med}")
```

### Step 2 — Triage the Findings
Open the Excel report. Sort by Risk Level:
- **HIGH (public links):** Review immediately — does this file contain student data?
- **MEDIUM (external users):** Verify the recipient is an authorized vendor or parent
- If student data is exposed: this may be a FERPA violation → notify administration

### Step 3 — Remediate
For each HIGH or MEDIUM finding:
1. Identify the file in Google Drive (search by title)
2. Open Share settings and remove the external access or change to "Restricted"
3. Notify the file owner of the policy violation
4. If student data was exposed: document in your Incident Reports folder

### Step 4 — Policy Reminder
After remediation, send a staff reminder that:
- Student records, grades, and PII must never be shared publicly or with non-school accounts
- FERPA violations can result in loss of federal funding
- All external sharing requires IT Director approval

## Important Notes
- The Admin SDK Drive audit log covers the last 90 days by default
- `change_user_access` events capture sharing changes, not the current state of all files
- For a full inventory of currently-shared files, a Google Drive API crawl is needed (beyond standard service account scope)
- Current scopes are read-only — remediation must be performed in the Drive UI or Admin Console
