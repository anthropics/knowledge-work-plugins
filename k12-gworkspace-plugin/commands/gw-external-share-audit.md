---
description: Audit Google Drive files shared outside your organization's domain
argument-hint: "[optional: time range, e.g. 'last 30 days' or 'last 90 days']"
---

# /gw-external-share-audit

Identify Drive files shared publicly or with external email addresses — the highest-priority FERPA compliance check for Google Workspace in K-12 schools.

## Usage

```
/gw-external-share-audit
/gw-external-share-audit last 30 days
/gw-external-share-audit check for student data exposure
```

## What it does

- Queries the Admin SDK Drive audit log for `change_user_access` events (last 90 days)
- Flags HIGH risk shares: "Anyone with the link" / public links
- Flags MEDIUM risk shares: files shared with specific external email addresses
- Generates an Excel report sorted by risk level with file titles, owners, and recipients
- Provides FERPA remediation guidance and step-by-step instructions to revoke access
