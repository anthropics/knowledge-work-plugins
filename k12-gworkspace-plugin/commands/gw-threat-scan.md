---
description: Scan Google Workspace for active security threats and compromised accounts
argument-hint: "[optional: focus area, e.g. 'staff only' or 'check for phishing']"
---

# /gw-threat-scan

Scan Google Workspace login activity for credential stuffing, brute-force attacks, geographic anomalies, and compromised accounts using the Admin SDK Reports API.

## Usage

```
/gw-threat-scan
/gw-threat-scan staff only
/gw-threat-scan check for suspicious logins this week
```

## What it does

- Queries up to 90 days of login audit events from the Admin SDK Reports API
- Identifies accounts with failed login patterns across multiple countries
- Flags HIGH risk (≥5 failures from ≥3 countries), MEDIUM risk, and LOW risk accounts
- Generates a color-coded Excel report with flagged accounts and countries seen
- Sends an iMessage or Slack alert with the scan summary
- Provides remediation guidance for each risk level
