---
name: gworkspace-meet-audit
description: >
  Audit Google Meet usage and recording activity — find who is hosting meetings,
  identify external participants, locate recordings stored in Drive, and review
  Meet activity for compliance or usage reporting. Use when reviewing Meet
  activity, checking for external participants in sensitive meetings, locating
  recordings for discovery or compliance purposes, or reporting on video
  conferencing usage. Triggers on: "Google Meet audit", "Meet activity report",
  "who recorded a Google meeting", "Meet recordings", "external Meet
  participants", "Google video conferencing report", "Meet usage", "who joined
  our Google Meets", "Meet recording audit".
---

# Google Meet Activity Audit

## Purpose
Review Google Meet activity — meeting hosts, external participants, recording
activity, and usage patterns. Useful for compliance, incident investigation,
and usage reporting.

## Authentication
- **Key file:** `~/path/to/your/google_service_account.json`
- **Admin impersonation:** `admin@yourdomain.org`
- **Scopes:** `admin.reports.audit.readonly`, `admin.reports.usage.readonly`

See [CONNECTORS.md](../../CONNECTORS.md) for full setup instructions.

## Report Output
`~/path/to/your/reports/YYYYMMDD_GWorkspace_Meet_Audit.xlsx`

## Steps

### Step 1 — Pull Meet Audit Events
Query the Meet audit log for meeting and recording activity:

```python
#!/usr/bin/env python3
"""GWorkspace Google Meet Audit"""
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
start = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%dT00:00:00Z")

meetings       = []
recordings     = []
external_joins = []
token          = None

while True:
    resp = svc.activities().list(
        userKey="all",
        applicationName="meet",
        startTime=start,
        maxResults=1000,
        pageToken=token,
    ).execute()

    for act in resp.get("items", []):
        actor = act.get("actor", {}).get("email", "Unknown")
        time  = act.get("id", {}).get("time", "")[:10]
        for event in act.get("events", []):
            name         = event.get("name", "")
            params       = {p["name"]: p.get("value", "") for p in event.get("parameters", [])}
            meeting_code = params.get("meeting_code", "")
            display_name = params.get("display_name", "")

            if name == "call_ended":
                meetings.append({
                    "time":         time,
                    "host":         actor,
                    "meeting_code": meeting_code,
                    "duration_s":   params.get("duration_seconds", ""),
                    "participants": params.get("participant_count", ""),
                })
            elif name == "recording_started":
                recordings.append({
                    "time":         time,
                    "started_by":   actor,
                    "meeting_code": meeting_code,
                })
            elif name == "call_joined":
                # Flag external participants
                is_external = actor and "@" in actor and not actor.endswith(f"@{DOMAIN}")
                if is_external or (display_name and not actor.endswith(f"@{DOMAIN}")):
                    external_joins.append({
                        "time":         time,
                        "email":        actor,
                        "display_name": display_name,
                        "meeting_code": meeting_code,
                    })

    token = resp.get("nextPageToken")
    if not token:
        break

# Build workbook with 3 sheets
os.makedirs(REPORT_DIR, exist_ok=True)
wb = openpyxl.Workbook()

# Sheet 1: Meetings
ws1 = wb.active
ws1.title = "Meetings"
for col, h in enumerate(["Date", "Host", "Meeting Code", "Duration (s)", "Participants"], 1):
    ws1.cell(row=1, column=col, value=h)
for row, m in enumerate(meetings, 2):
    ws1.cell(row=row, column=1, value=m["time"])
    ws1.cell(row=row, column=2, value=m["host"])
    ws1.cell(row=row, column=3, value=m["meeting_code"])
    ws1.cell(row=row, column=4, value=m["duration_s"])
    ws1.cell(row=row, column=5, value=m["participants"])

# Sheet 2: Recordings
ws2 = wb.create_sheet("Recordings")
for col, h in enumerate(["Date", "Started By", "Meeting Code"], 1):
    ws2.cell(row=1, column=col, value=h)
for row, r in enumerate(recordings, 2):
    ws2.cell(row=row, column=1, value=r["time"])
    ws2.cell(row=row, column=2, value=r["started_by"])
    ws2.cell(row=row, column=3, value=r["meeting_code"])

# Sheet 3: External Participants
ws3 = wb.create_sheet("External Participants")
for col, h in enumerate(["Date", "External Email", "Display Name", "Meeting Code"], 1):
    ws3.cell(row=1, column=col, value=h)
for row, e in enumerate(external_joins, 2):
    ws3.cell(row=row, column=1, value=e["time"])
    ws3.cell(row=row, column=2, value=e["email"])
    ws3.cell(row=row, column=3, value=e["display_name"])
    ws3.cell(row=row, column=4, value=e["meeting_code"])

date_str = today.strftime("%Y%m%d")
out = os.path.join(REPORT_DIR, f"{date_str}_GWorkspace_Meet_Audit.xlsx")
wb.save(out)
print(f"✅ Report saved: {out}")
print(f"   Meetings completed (30d): {len(meetings)}")
print(f"   Recordings started: {len(recordings)}")
print(f"   External participant join events: {len(external_joins)}")
```

### Step 2 — Review the Three Sheets

**Meetings tab:** Overall meeting volume and hosts. Look for unusual patterns
(e.g., late-night meetings, high external participant counts).

**Recordings tab:** Every recording started in the last 30 days. Recordings
are stored in the host's Google Drive. For compliance or discovery, locate
the recording file in their Drive and note the share settings.

**External Participants tab:** Non-domain accounts who joined meetings.
- Known vendors or authorized external parties → expected; document for compliance
- Unknown external emails → investigate which meeting they joined and why
- Parents joining student support meetings → typically expected but should be documented

### Step 3 — Recording Compliance Check
Google Meet recordings stored in Drive may contain student audio/video.
FERPA implications:
- Recordings of minors require parental consent consideration
- Recordings should not be shared externally without review
- Check recording Drive files for external share settings (use the `gworkspace-external-share-audit` skill)

### Step 4 — Usage Summary for Leadership
If generating a usage report for administration:
- Total meetings hosted (30 days)
- Average participants per meeting
- Most active hosts
- Recording activity (count, hosts)

## Important Notes
- Meet audit log covers up to 90 days; this script defaults to 30 days — adjust `timedelta(days=30)` as needed
- Recording locations: Host's Google Drive → "Meet Recordings" folder
- The `call_joined` event may not capture all participant details for external/anonymous users
- Google Meet activity requires the Meet audit log to be enabled in Admin Console (enabled by default for Education)
- Usage reports and audit logs are separate API endpoints — this skill queries the audit log only
