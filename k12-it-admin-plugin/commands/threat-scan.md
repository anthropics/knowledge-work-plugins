---
description: Scan Microsoft 365 for active security threats and compromised accounts
argument-hint: "[optional: focus area, e.g. 'staff only' or 'check for phishing']"
---

# /threat-scan

Run a full M365 threat scan using Entra Identity Protection and the Microsoft Graph API.

## Usage

```
/threat-scan
/threat-scan staff only
/threat-scan check for active phishing
```

## What it does

- Pulls all risky users and risk detections from Entra Identity Protection
- Identifies accounts with active `atRisk` or `confirmedCompromised` status
- Analyzes attack patterns (countries, IP ranges, attack types)
- Verifies SSPR access for affected users
- Generates a color-coded Excel report
- Drafts password reset emails for affected users
- Dismisses risk flags after confirmed password resets
