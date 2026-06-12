---
name: gworkspace-threat-scan
description: >
  Scan Google Workspace for active security threats, suspicious login activity,
  credential stuffing, and compromised accounts using the Admin SDK Reports API.
  Use when checking for hacked accounts, running a security threat check,
  investigating suspicious login activity, or generating a compromised accounts
  report. Triggers on: "GWorkspace threat scan", "Google threat scan", "check
  for compromised Google accounts", "suspicious Google logins", "GWorkspace
  security check", "run the Google scan".
---

# Google Workspace Threat Scan

## Purpose
Scan your Google Workspace domain for suspicious login activity including
credential stuffing, brute-force attacks, geographic anomalies, and compromised
accounts using the Admin SDK Reports API.

## Authentication
All GWorkspace skills use a service account with domain-wide delegation:
- **Key file:** `~/path/to/your/google_service_account.json`
- **Admin impersonation:** `admin@yourdomain.org`
- **Scopes:** `admin.reports.audit.readonly`, `admin.directory.user.readonly`

See [CONNECTORS.md](../../CONNECTORS.md) for full setup instructions.

## Script Location
Save the script below to a convenient path, for example:
`~/scripts/gworkspace_threat_scan.py`

## Report Output
`~/path/to/your/reports/YYYYMMDD_GWorkspace_Threat_Scan.xlsx`

## Steps

### Step 1 — Run the Threat Scan Script
Open Terminal and run the script below (or save it as a `.py` file and execute it):

```python
#!/usr/bin/env python3
"""GWorkspace Threat Scan — scans login audit logs for credential stuffing and anomalies."""
import os, json, datetime, collections, openpyxl
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

creds = service_account.Credentials.from_service_account_file(
    KEY_FILE, scopes=SCOPES
).with_subject(ADMIN_EMAIL)

rpt_svc = build("admin", "reports_v1", credentials=creds)

today = datetime.date.today()
start = (today - datetime.timedelta(days=90)).strftime("%Y-%m-%dT00:00:00Z")

# Collect login events per user
user_events = collections.defaultdict(lambda: {
    "failures": 0, "countries": set(), "ips": set(), "events": []
})

token = None
total_events = 0
while True:
    resp = rpt_svc.activities().list(
        userKey="all",
        applicationName="login",
        startTime=start,
        maxResults=1000,
        pageToken=token,
    ).execute()

    for act in resp.get("items", []):
        email = act.get("actor", {}).get("email", "unknown")
        time  = act.get("id", {}).get("time", "")[:10]
        for event in act.get("events", []):
            params = {p["name"]: p.get("value", "") for p in event.get("parameters", [])}
            is_failure = params.get("login_failure_type", "") != ""
            country    = params.get("country_code", "")
            ip         = act.get("ipAddress", "")
            if is_failure:
                user_events[email]["failures"] += 1
                if country:
                    user_events[email]["countries"].add(country)
                if ip:
                    user_events[email]["ips"].add(ip)
                user_events[email]["events"].append({
                    "time": time, "country": country, "ip": ip,
                    "type": params.get("login_failure_type", ""),
                })
        total_events += 1

    token = resp.get("nextPageToken")
    if not token:
        break

# Risk classification
def classify(data):
    f = data["failures"]
    c = len(data["countries"])
    if f >= 5 and c >= 3:
        return "HIGH"
    elif f >= 3 or c >= 2:
        return "MEDIUM"
    elif f >= 1:
        return "LOW"
    return "CLEAN"

findings = []
for email, data in user_events.items():
    risk = classify(data)
    if risk != "CLEAN":
        findings.append({
            "email": email,
            "failures": data["failures"],
            "countries": ", ".join(sorted(data["countries"])),
            "unique_ips": len(data["ips"]),
            "risk": risk,
        })

findings.sort(key=lambda x: ({"HIGH": 0, "MEDIUM": 1, "LOW": 2}[x["risk"]], -x["failures"]))

# Write Excel report
os.makedirs(REPORT_DIR, exist_ok=True)
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Threat Scan"
header = ["Email", "Failed Logins", "Countries Seen", "Unique IPs", "Risk Level"]
for col, h in enumerate(header, 1):
    ws.cell(row=1, column=col, value=h)
for row, f in enumerate(findings, 2):
    ws.cell(row=row, column=1, value=f["email"])
    ws.cell(row=row, column=2, value=f["failures"])
    ws.cell(row=row, column=3, value=f["countries"])
    ws.cell(row=row, column=4, value=f["unique_ips"])
    ws.cell(row=row, column=5, value=f["risk"])

date_str = today.strftime("%Y%m%d")
out = os.path.join(REPORT_DIR, f"{date_str}_GWorkspace_Threat_Scan.xlsx")
wb.save(out)

high   = sum(1 for f in findings if f["risk"] == "HIGH")
medium = sum(1 for f in findings if f["risk"] == "MEDIUM")
low    = sum(1 for f in findings if f["risk"] == "LOW")
countries_seen = set()
for f in findings:
    countries_seen.update(f["countries"].split(", "))

print(f"✅ Report saved: {out}")
print(f"   Total login events analyzed: {total_events}")
print(f"   HIGH risk users  : {high}")
print(f"   MEDIUM risk users: {medium}")
print(f"   LOW risk users   : {low}")
print(f"   Countries seen   : {', '.join(sorted(countries_seen))}")
print(f"   Flagged accounts : {', '.join(f['email'] for f in findings if f['risk'] in ('HIGH', 'MEDIUM'))}")

import sys
sys.exit(2 if high > 0 else 0)
```

Wait for completion. Note the exit code:
- **0** = No HIGH threats found (clean)
- **2** = HIGH threats found (action required)
- **other** = Script error

### Step 2 — Read the Terminal Summary
Look for these lines in the output:
```
     HIGH risk users  : <count>
     MEDIUM risk users: <count>
     LOW risk users   : <count>
     Countries seen   : <countries>
     Flagged accounts : <accounts>
```
Note the values — you will need them for Step 3.

### Step 3 — Update Your Security Dashboard (Optional)
If you maintain a Notion security dashboard, add a new row to your Security Scan
History database with today's date, scan type (Google Workspace), risk counts,
countries seen, and flagged accounts.

### Step 4 — Send Alert
Send yourself (or your team) a completion summary via Slack, iMessage, or email:

**If exit code 0 (clean):**
```
✅ GWorkspace Threat Scan complete — no HIGH threats found. Report saved.
```

**If exit code 2 (HIGH threats found):**
```
🚨 GWorkspace Threat Scan ALERT — HIGH risk accounts detected:
[list flagged accounts]
Countries: [countries seen]
⚠️ Immediate action required. Check your security dashboard and Excel report.
```

**If script error:**
```
⚠️ GWorkspace Threat Scan FAILED — script exited with error. Check Terminal output. Manual scan required.
```

## Important Notes
- ⚠️ Google Admin SDK logs have a ~2-day lag — very recent events may not appear
- The script analyzes up to 90 days of sign-in audit logs
- Risk levels: HIGH (≥5 failures from ≥3 countries), MEDIUM (≥3 failures or multi-country), LOW (anomalous patterns)
- Adjust `timedelta(days=90)` to change the lookback window

## Remediation Actions
- **HIGH risk:** Lock account immediately → force password reset → investigate
- **MEDIUM risk:** Monitor closely → notify user → consider password reset
- **LOW risk:** Log and monitor → no immediate action unless pattern worsens
