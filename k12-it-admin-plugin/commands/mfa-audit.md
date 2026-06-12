---
description: Run an MFA compliance audit for a Microsoft 365 security group
argument-hint: "<group name, e.g. 'All Faculty and Staff'>"
---

# /mfa-audit

Check MFA registration status for any security group and optionally enforce via Conditional Access.

## Usage

```
/mfa-audit All Faculty and Staff
/mfa-audit All Users
/mfa-audit Administrators
```

## What it does

- Searches for the named security group (handles fuzzy matching)
- Pulls MFA registration status for all group members
- Categorizes: registered, not registered, disabled accounts
- Exports CSV reports (all accounts + missing MFA list)
- Optionally: creates a shared-account MFA exclusion group
- Optionally: enables or updates a Conditional Access MFA enforcement policy
