# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool you connect in that category.

This plugin is **script-based** — all Google Workspace API calls run as Python scripts using a service account with domain-wide delegation. This means you configure credentials once and every skill runs without browser token extraction.

## Connectors for this plugin

| Category | Placeholder | Included servers | Notes |
|----------|-------------|-----------------|-------|
| Dashboard / Wiki | `~~dashboard` | Notion | Optional — update your security dashboard after each audit |
| Chat / Notifications | `~~chat` | Slack | Optional — post audit summaries to a channel |

## Authentication Model

All skills in this plugin use a **Google Cloud service account with domain-wide delegation**. This means:

- **One-time setup** — configure the service account once; all skills use it automatically
- **No browser token required** — runs fully headless, suitable for scheduling
- **Read-only by default** — all required scopes are audit/read-only; no destructive permissions
- **Requires Super Admin** — the impersonation account must have Super Admin privileges in Google Workspace Admin Console

## Setup Steps

### 1. Create a Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (e.g., `your-org-it-automation`)
3. Enable the **Admin SDK API** and **Google Drive API**

### 2. Create a Service Account

1. In your project → IAM & Admin → Service Accounts → Create Service Account
2. Name it (e.g., `gworkspace-automation`)
3. Create and download a JSON key file
4. Save the key file to a secure path (e.g., `~/path/to/your/google_service_account.json`)

### 3. Grant Domain-Wide Delegation

1. Note the service account's **Client ID** (numeric, from the JSON key)
2. Go to [admin.google.com](https://admin.google.com) → Security → Access and Data Control → API Controls → Domain-Wide Delegation
3. Add a new entry with the Client ID and the following scopes:

```
https://www.googleapis.com/auth/admin.reports.audit.readonly
https://www.googleapis.com/auth/admin.reports.usage.readonly
https://www.googleapis.com/auth/admin.directory.user.readonly
```

### 4. Update Each Skill

In each SKILL.md, update two constants at the top of the Python script:

```python
KEY_FILE    = os.path.expanduser("~/path/to/your/google_service_account.json")
ADMIN_EMAIL = "admin@yourdomain.org"   # Super Admin account for impersonation
```

### 5. Install Dependencies

```bash
pip install google-auth google-auth-httplib2 google-api-python-client openpyxl
```

## Required OAuth Scopes Summary

| Scope | Skills that use it |
|-------|-------------------|
| `admin.reports.audit.readonly` | threat-scan, external-share-audit, admin-audit, oauth-audit, meet-audit |
| `admin.reports.usage.readonly` | inactive-accounts, storage-report, meet-audit |
| `admin.directory.user.readonly` | threat-scan, inactive-accounts, admin-audit, storage-report |

## Optional: Scheduling

All scripts are suitable for scheduled execution (cron, Task Scheduler, or Claude scheduled tasks). Recommended schedule:

| Skill | Suggested cadence |
|-------|------------------|
| `gworkspace-threat-scan` | Weekly |
| `gworkspace-inactive-accounts` | Monthly |
| `gworkspace-external-share-audit` | Monthly |
| `gworkspace-admin-audit` | Monthly |
| `gworkspace-oauth-audit` | Quarterly |
| `gworkspace-storage-report` | Monthly |
| `gworkspace-meet-audit` | Monthly or on-demand |
