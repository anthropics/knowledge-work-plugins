---
description: Audit all third-party OAuth app permissions in Microsoft 365
---

# /oauth-audit

Enumerate all third-party apps with access to your tenant and flag high-risk or unverified publishers.

## Usage

```
/oauth-audit
```

## What it does

- Lists all service principals (third-party apps) in the tenant
- Pulls delegated OAuth permission grants and application role assignments
- Flags apps with high-risk scopes (Mail.Read, Files.ReadWrite.All, Directory.ReadWrite.All, etc.)
- Flags unverified publishers with any data access
- Generates Excel report sorted by risk level
- Optionally: revokes specific app permissions or removes a service principal
