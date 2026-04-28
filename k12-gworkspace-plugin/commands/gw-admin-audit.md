---
description: Audit Google Workspace admin activity and privilege changes
argument-hint: "[optional: focus area, e.g. 'privilege changes only' or 'last 30 days']"
---

# /gw-admin-audit

Review 90 days of Google Workspace administrator activity — privilege grants, user deletions, account changes, and setting modifications. Flags high-risk events for investigation.

## Usage

```
/gw-admin-audit
/gw-admin-audit privilege changes only
/gw-admin-audit check for unauthorized actions
```

## What it does

- Queries the Admin SDK admin audit log for all admin activity (last 90 days)
- Flags HIGH-risk events: GRANT_ADMIN_PRIVILEGE, DELETE_USER, CHANGE_APPLICATION_SETTING, etc.
- Lists current Super Admin accounts via the Directory API
- Generates an Excel report sorted by risk level with actor, event, and target details
- Highlights patterns: after-hours actions, vendor activity, mass changes
