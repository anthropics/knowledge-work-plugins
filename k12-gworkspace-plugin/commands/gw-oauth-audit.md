---
description: Audit third-party OAuth app permissions granted to Google Workspace accounts
argument-hint: "[optional: focus area, e.g. 'high risk only' or 'last 180 days']"
---

# /gw-oauth-audit

Identify all third-party applications that have been granted OAuth access to your Google Workspace accounts. Flags apps with access to Drive, Gmail, Contacts, or Classroom for FERPA review.

## Usage

```
/gw-oauth-audit
/gw-oauth-audit high risk only
/gw-oauth-audit check for student data access
```

## What it does

- Queries the Admin SDK token audit log for OAuth `authorize` events (last 180 days)
- Flags HIGH-risk apps: those with access to Drive, Gmail, Contacts, Calendar, or Classroom
- Deduplicates grants by app + user + scopes
- Generates an Excel report with app name, client ID, granted scopes, and risk level
- Provides step-by-step instructions to revoke access via Admin Console or per-user settings
