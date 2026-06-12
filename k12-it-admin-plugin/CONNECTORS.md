# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool you connect in that category.

This plugin is primarily **browser-based** — all Microsoft Graph API calls use a bearer token extracted from your active Entra admin session. No pre-configured API credentials are required.

## Connectors for this plugin

| Category | Placeholder | Included servers | Notes |
|----------|-------------|-----------------|-------|
| Microsoft 365 / Entra ID | `~~m365` | Microsoft 365 MCP | Bearer token via browser session (see each skill) |
| Dashboard / Wiki | `~~dashboard` | Notion | Optional — update your security dashboard after each audit |
| Chat / Notifications | `~~chat` | Slack | Optional — post audit summaries to a channel |

## Authentication Model

All skills in this plugin use a **browser session bearer token** rather than a registered app or service account. This means:

- **No app registration required** — works with any M365 tenant out of the box
- **No stored credentials** — token is extracted live from your Entra admin portal session
- **Tokens last 60–90 minutes** (session tokens can last up to 24 hours)
- **Requires Global Admin or appropriate role** — see each skill for the minimum required permissions

This approach was chosen for ease of adoption in K-12 environments where setting up service accounts and app registrations may require additional approval.

## Optional: App Registration (for Scheduled Scans)

If you want to run these audits on a schedule (e.g., weekly threat scans), set up an app registration in Entra ID with the following permissions:

| Permission | Type | Purpose |
|-----------|------|---------|
| `AuditLog.Read.All` | Application | Sign-in logs for threat scan |
| `Directory.Read.All` | Application | User and role data |
| `Policy.Read.All` | Application | Conditional Access policies |
| `Reports.Read.All` | Application | MFA registration data |
| `User.Read.All` | Application | User account details |
| `IdentityRiskyUser.Read.All` | Application | Risky user data (requires Entra P2) |
