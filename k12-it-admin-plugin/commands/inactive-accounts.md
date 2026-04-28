---
description: Find dormant Microsoft 365 accounts by inactivity threshold
argument-hint: "[days: 30, 60, or 90 — defaults to 60]"
---

# /inactive-accounts

Find accounts with no sign-in activity beyond a configurable threshold.

## Usage

```
/inactive-accounts
/inactive-accounts 90
/inactive-accounts 30
```

## What it does

- Pulls all user accounts with sign-in activity data (beta Graph endpoint)
- Categorizes: inactive beyond threshold, never signed in, already disabled
- Sorts by most inactive first
- Generates Excel report with color-coded inactivity levels (30/60/90+ days)
- Recommends accounts to investigate with HR before disabling
- Optionally: disables specific accounts via Graph API
