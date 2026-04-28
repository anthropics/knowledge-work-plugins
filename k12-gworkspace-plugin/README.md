# K-12 Google Workspace Plugin

A Google Workspace security auditing plugin built for K-12 IT administrators. Seven skills covering the most critical security and FERPA compliance gaps in school Google Workspace tenants — no expensive third-party tools, no complex setup, no admin portal clicking required. Configure a service account once and run comprehensive audits in minutes.

Built for [Claude Cowork](https://claude.com/product/cowork) and [Claude Code](https://claude.com/product/claude-code).

---

## Why This Plugin Exists

K-12 IT teams are small, under-resourced, and responsible for protecting student data under FERPA. Most security tooling is priced for enterprise. This plugin gives any IT admin with a Google Workspace Super Admin account the ability to run a complete Google Workspace security posture audit — for free, using the built-in Admin SDK Reports API.

---

## Installation

### Cowork

Install from [claude.com/plugins](https://claude.com/plugins/).

### Claude Code

```bash
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install k12-gworkspace@knowledge-work-plugins
```

---

## Skills

Skills fire automatically when relevant. Describe what you need in plain language.

| Skill | Trigger phrases | What it does |
|-------|----------------|--------------|
| `gworkspace-threat-scan` | "GWorkspace threat scan", "check for compromised Google accounts", "suspicious Google logins" | Analyzes login audit logs for credential stuffing, geographic anomalies, and compromised accounts |
| `gworkspace-inactive-accounts` | "inactive Google accounts", "who hasn't logged into Google", "stale Google accounts" | Finds accounts with no login activity in 30/60/90+ days; flags never-logged-in accounts |
| `gworkspace-external-share-audit` | "external Drive sharing", "Google Drive FERPA audit", "files shared outside school" | Identifies Drive files shared publicly or with external accounts — the #1 FERPA risk in Google Workspace |
| `gworkspace-admin-audit` | "GWorkspace admin audit", "who has Google admin access", "suspicious admin actions" | Reviews 90 days of admin activity — privilege changes, user deletions, setting changes |
| `gworkspace-oauth-audit` | "GWorkspace OAuth audit", "Google app permissions", "what apps can access our Google data" | Audits third-party OAuth app grants; flags apps with access to Drive, Gmail, Contacts, or Classroom |
| `gworkspace-storage-report` | "Google storage report", "Drive capacity report", "who has big Drive" | Per-user Drive + Gmail storage breakdown; identifies heavy users for capacity planning |
| `gworkspace-meet-audit` | "Google Meet audit", "Meet recordings", "external Meet participants" | Reviews Meet activity, recording events, and external participant joins for compliance |

---

## Commands

Explicit workflows you invoke with a slash command:

| Command | Description |
|---------|-------------|
| `/gw-threat-scan` | Scan for compromised and at-risk Google accounts |
| `/gw-inactive-accounts` | Find dormant accounts by inactivity threshold |
| `/gw-external-share-audit` | Audit Drive files shared outside your domain |
| `/gw-admin-audit` | Review admin activity and privilege changes |
| `/gw-oauth-audit` | Audit third-party OAuth app permissions |
| `/gw-storage-report` | Generate per-user storage usage report |
| `/gw-meet-audit` | Review Meet activity and recording compliance |

---

## Authentication

All skills use a **Google Cloud service account with domain-wide delegation**. One-time setup, then every skill runs without any additional authentication steps.

See [CONNECTORS.md](./CONNECTORS.md) for full setup instructions.

**Quick summary:**
1. Create a Google Cloud project and service account
2. Download the JSON key file
3. Grant domain-wide delegation in your Google Workspace Admin Console
4. Update `KEY_FILE` and `ADMIN_EMAIL` in each skill's script

---

## Output

Each skill generates a color-coded Excel report (`.xlsx`) saved to your configured output directory. Reports include:

- Summary statistics and risk counts
- Per-account detail with risk level flags
- Recommended remediation actions
- (Optional) Security dashboard update via Notion MCP

---

## Customizing for Your School

These skills work on any Google Workspace for Education tenant. To customize:

- **Update `KEY_FILE`** in each skill to point to your service account JSON key
- **Update `ADMIN_EMAIL`** to your Super Admin email address
- **Update `REPORT_DIR`** to your preferred reports folder
- **Connect Notion** if you maintain a security dashboard and want auto-updates after each audit
- **Adjust thresholds** — the inactive accounts skill defaults to 30/60/90 days; update `THRESHOLDS` to match your policy
- **Adjust lookback windows** — most skills default to 90 days; adjust `timedelta(days=90)` as needed

---

## Requirements

- Google Workspace for Education (any edition) or Google Workspace Business/Enterprise
- Super Admin account (required for domain-wide delegation impersonation)
- Google Cloud project with Admin SDK API enabled
- Python 3.8+ (available in Claude's sandbox; pre-installed on most systems)
- Python packages: `google-auth`, `google-auth-httplib2`, `google-api-python-client`, `openpyxl`

```bash
pip install google-auth google-auth-httplib2 google-api-python-client openpyxl
```

> **Note:** Google Admin SDK logs have a ~2-day lag. Very recent events (past 24–48 hours) may not appear in audit reports. This is a Google API limitation, not a plugin limitation.

---

## FERPA Considerations

Several skills are specifically designed around FERPA compliance in K-12 environments:

- **external-share-audit** — Drive files shared publicly or with external accounts can expose student records
- **oauth-audit** — Third-party apps with access to Drive, Gmail, or Classroom may process student data and require FERPA review
- **meet-audit** — Recordings of minors require parental consent consideration; external participant access to student meetings should be documented

---

## About

Built by Steve Mojica, IT Director and K-12 ed-tech consultant. Part of a suite of free Claude plugins for K-12 IT administrators.

- [k12-it-admin](https://github.com/stevemojica/Claude-Plugins/tree/main/k12-it-admin-plugin) — Companion plugin for Microsoft 365 / Entra ID security auditing
- [GitHub](https://github.com/stevemojica/Claude-Plugins)

---

## Contributing

Found a bug? Have a skill to add? PRs welcome. See the [contributing guide](https://github.com/anthropics/knowledge-work-plugins/blob/main/CONTRIBUTING.md).
