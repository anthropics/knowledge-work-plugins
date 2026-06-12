---
description: Audit Conditional Access policies for gaps and misconfigurations
---

# /ca-audit

Pull all CA policies and analyze them for coverage holes — report-only mode, legacy auth, missing MFA enforcement.

## Usage

```
/ca-audit
```

## What it does

- Lists all Conditional Access policies with their current state
- Checks for policies stuck in report-only mode (not actually enforcing)
- Verifies an MFA policy covering all users exists and is enabled
- Checks for a legacy authentication block policy
- Checks for admin-specific CA protections
- Notes if sign-in risk policies are absent (requires Entra P2)
- Generates Excel report with a gaps and recommendations tab
- Optionally: enables report-only policies and creates legacy auth block policy
