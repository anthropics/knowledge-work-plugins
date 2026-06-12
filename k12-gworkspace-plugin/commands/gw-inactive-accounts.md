---
description: Find dormant Google Workspace accounts by inactivity threshold
argument-hint: "[optional: threshold in days, e.g. '90' or '60 days']"
---

# /gw-inactive-accounts

Identify Google Workspace accounts with no recent login activity across 30, 60, and 90-day thresholds. Supports offboarding, compliance reviews, and attack surface reduction.

## Usage

```
/gw-inactive-accounts
/gw-inactive-accounts 90 days
/gw-inactive-accounts staff accounts only
```

## What it does

- Queries the Admin SDK Directory API for all users and their last login timestamps
- Flags accounts inactive for 30+, 60+, and 90+ days
- Identifies never-logged-in accounts (common after domain migrations)
- Generates an Excel report with OU, suspension status, and inactivity flags
- Provides guidance on cross-referencing with HR before suspending accounts
