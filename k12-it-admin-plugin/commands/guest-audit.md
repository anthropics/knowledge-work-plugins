---
description: Audit all external guest accounts in Microsoft 365
---

# /guest-audit

List all guest and external accounts, categorize by activity, and identify stale ones for removal.

## Usage

```
/guest-audit
```

## What it does

- Pulls all accounts with `userType = Guest`
- Categorizes: active (within 90 days), stale (90+ days inactive), pending invites, never signed in
- Shows domain summary (which organizations have the most external access)
- Generates Excel report with stale guests tabbed separately
- Optionally: disables or deletes specific guest accounts
