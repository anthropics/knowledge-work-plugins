# K-12 IT Admin Plugin

A Microsoft 365 security auditing plugin built for K-12 IT administrators. Seven skills covering the most common security gaps in school M365 tenants — no app registrations, no extra tooling, no admin portal clicking required. Just sign into Entra, extract a bearer token, and run.

Built for [Claude Cowork](https://claude.com/product/cowork) and [Claude Code](https://claude.com/product/claude-code).

---

## Why This Plugin Exists

K-12 IT teams are small, under-resourced, and responsible for protecting student data under FERPA. Most security tooling is priced for enterprise. This plugin gives any IT admin with a Global Admin account the ability to run a complete M365 security posture audit in under an hour — for free.

---

## Installation

### Cowork

Install from [claude.com/plugins](https://claude.com/plugins/).

### Claude Code

```bash
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install k12-it-admin@knowledge-work-plugins
```

---

## Skills

Skills fire automatically when relevant. Describe what you need in plain language.

| Skill | Trigger phrases | What it does |
|-------|----------------|--------------|
| `m365-threat-scan` | "threat scan", "compromised accounts", "who's been hacked" | Checks for risky users, credential stuffing, and active threats via Entra Identity Protection |
| `m365-admin-role-audit` | "admin role audit", "who has admin access", "over-privileged accounts" | Inventories all privileged role assignments, flags role sprawl and disabled admins |
| `m365-mfa-audit` | "MFA audit", "who doesn't have two-factor", "MFA compliance" | Checks MFA registration for any security group; optionally enforces via Conditional Access |
| `m365-ca-audit` | "Conditional Access audit", "CA policy review", "legacy auth" | Analyzes all CA policies for gaps — report-only, legacy auth, missing MFA coverage |
| `m365-oauth-audit` | "OAuth audit", "app permissions", "what apps can access our data" | Enumerates third-party app consent, flags high-risk scopes (Mail.Read, Files.ReadWrite.All, etc.) |
| `m365-guest-audit` | "guest accounts", "external users", "clean up guests" | Lists all external guest accounts, categorizes stale/pending/never-used |
| `m365-inactive-accounts` | "inactive accounts", "stale accounts", "who hasn't logged in" | Finds accounts with no sign-in activity in 30/60/90+ days |

---

## Commands

Explicit workflows you invoke with a slash command:

| Command | Description |
|---------|-------------|
| `/threat-scan` | Run a full M365 threat scan |
| `/admin-role-audit` | Audit all privileged role assignments |
| `/mfa-audit` | Run MFA compliance check for a security group |
| `/ca-audit` | Audit Conditional Access policy coverage |
| `/oauth-audit` | Review all third-party app permissions |
| `/guest-audit` | Audit all external guest accounts |
| `/inactive-accounts` | Find dormant accounts by inactivity threshold |

---

## Authentication

All skills use a **bearer token extracted from your active Entra admin session** — no app registration required. Each skill walks you through a one-time browser step:

1. Open [https://entra.microsoft.com](https://entra.microsoft.com) as Global Admin
2. Open DevTools → Console (F12)
3. Run a one-line JavaScript snippet (provided in each skill)
4. Paste the token into Claude

Tokens last 60–90 minutes. If you need longer-running or scheduled scans, see [CONNECTORS.md](./CONNECTORS.md) for app registration setup.

---

## Output

Each skill generates a color-coded Excel report (`.xlsx`) saved to your specified output directory. Reports include:

- Summary statistics and risk counts
- Per-account detail with color-coded risk levels
- Recommended actions
- (Optional) Security dashboard update via Notion MCP

---

## Customizing for Your School

These skills work out of the box on any M365 Education tenant. To customize:

- **Update the output path** in each skill's Excel export step to point to your preferred reports folder
- **Connect Notion** if you maintain a security dashboard and want auto-updates after each audit
- **Adjust thresholds** — the inactive accounts skill defaults to 60 days; adjust `THRESHOLD_DAYS` to match your policy

---

## Requirements

- Microsoft 365 Education (A1, A3, or A5) or any M365 tenant with Entra ID
- Global Admin account (or minimum roles noted in each skill)
- Python available in Claude's sandbox (pre-installed)
- `openpyxl` package (pre-installed in most environments; install with `pip install openpyxl` if needed)

> **Note:** The threat scan skill uses Entra Identity Protection endpoints. Some data (risky user detections) requires **Entra ID P1 or P2**. With M365 A1 (no P1/P2), the skill falls back to sign-in audit log analysis.

---

## Contributing

Found a bug? Have a skill to add? PRs welcome. See the [contributing guide](https://github.com/anthropics/knowledge-work-plugins/blob/main/CONTRIBUTING.md).
