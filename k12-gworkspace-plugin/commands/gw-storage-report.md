---
description: Generate a per-user Google Workspace storage usage report
argument-hint: "[optional: threshold, e.g. '>10GB only' or 'top 20 users']"
---

# /gw-storage-report

Generate a per-user storage breakdown across Google Drive and Gmail for all accounts in your organization. Supports capacity planning and quota management.

## Usage

```
/gw-storage-report
/gw-storage-report top 20 users
/gw-storage-report who is over 10GB
```

## What it does

- Queries the Admin SDK User Usage Report for Drive and Gmail storage metrics (as of yesterday)
- Calculates total storage (Drive + Gmail) per user in GB
- Flags users >10 GB for review and >5 GB for monitoring
- Generates an Excel report sorted by total storage descending
- Provides capacity planning guidance and actions for heavy users and departed staff
