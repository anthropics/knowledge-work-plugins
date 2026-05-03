---
description: Audit all privileged administrator roles in Entra ID
argument-hint: "[optional: focus area, e.g. 'global admins only']"
---

# /admin-role-audit

Enumerate every privileged role assignment and flag role sprawl, disabled admins, and vendor accounts.

## Usage

```
/admin-role-audit
/admin-role-audit global admins only
```

## What it does

- Lists all activated directory roles and their members
- Identifies high-privilege role holders (Global Admin, Security Admin, etc.)
- Flags disabled accounts still holding admin roles
- Flags guest accounts with admin roles
- Flags role sprawl (accounts with 3+ high-privilege roles)
- Generates a color-coded Excel report with a flagged accounts tab
