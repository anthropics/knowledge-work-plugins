# ContextIQ Plugin for Cowork and Claude Code

Governed enterprise knowledge access — cited answers, entitlement-scoped retrieval, and audit-ready answer paths — powered by [ContextIQ](https://contextiq.us).

---

## What This Plugin Does

ContextIQ connects Cowork and Claude Desktop to your organization's knowledge sources through Model Context Protocol (MCP). It controls which sources each user can query, returns cited answers with source evidence, and keeps retrieval scoped to authorized entitlements.

| Skill | Description |
|---|---|
| **Governed Query** | Ask questions answered from authorized enterprise sources with cited evidence |
| **Source Discovery** | List available knowledge sources scoped to your entitlements |

---

## Requirements

- Python 3.10+
- Cognito username and password (provided by your admin)
- Setup link or config file (provided by your admin)
- No AWS CLI, AWS account, or backend access required — everything runs through the admin's deployment

**Admins** — ContextIQ must be deployed before users can connect. See the [Quickstart Guide](https://contextiq-releases.s3.us-west-2.amazonaws.com/essentials/latest/templates/README.md) for deployment, user creation, and distribution options.

---

## Setup

End users do not need AWS CLI, direct backend access, or any infrastructure setup. Your admin deploys ContextIQ and manages the knowledge bases — you just need a setup link or config file from your admin to connect.

### From a setup link (recommended)

Your admin will share a setup link via email, Slack, or your internal wiki.

```bash
./contextiq-setup --url "https://your-setup-link..."
```

Enter your username and password when prompted. Done.

### From a config file

If your admin sent a `contextiq-connection.json` file:

1. Save it to your Downloads folder
2. Run `./contextiq-setup`

The script auto-detects the config from these locations (checked in order):
- `~/.contextiq/contextiq-connection.json`
- `~/Downloads/contextiq-connection.json`
- Current directory
- Plugin directory

You can also point to the file explicitly:

```bash
./contextiq-setup --config /path/to/contextiq-connection.json
```

### Admin self-setup (fallback)

If you are the admin who deployed ContextIQ and have AWS CLI configured with access to the deployment account, you can skip the config file and connect directly via CloudFormation discovery:

```bash
./contextiq-setup --username your-email@company.com
```

The script discovers the deployment automatically from CloudFormation stack outputs. See the [Quickstart Guide](https://contextiq-releases.s3.us-west-2.amazonaws.com/essentials/latest/templates/README.md) for full admin setup and team distribution options.

### After setup

Restart Cowork or Claude Desktop. Start asking questions about your enterprise knowledge — the plugin activates automatically when relevant.

### Re-authentication

Access tokens refresh automatically for 30 days. When you see a "session expired" error, re-run the same setup command you used initially.

---

## Admin Guide

Admins deploy the ContextIQ backend, create user accounts, and distribute connection configs. All of this is covered in the Quickstart Guide:

**[Quickstart Guide — Deployment, User Management & Distribution](https://contextiq-releases.s3.us-west-2.amazonaws.com/essentials/latest/templates/README.md)**

The quickstart covers:
- CloudFormation deployment (~20-30 minutes)
- Cognito user creation (standalone user pools; contact hello@contextiq.us for Active Directory, SAML, or SSO integration via ContextIQ Enterprise)
- Team distribution via automated email (S3 + SES), shareable link, or config file attachment
- Admin command reference for `contextiq-setup`

Supported regions: us-east-1 or us-west-2. Requires Bedrock model access (Anthropic Claude + Amazon Titan Embed Text V2).

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| "No gateway URL configured" | Run `contextiq-setup` first |
| "Session expired" | Re-run `contextiq-setup` to refresh tokens |
| "No connection config found" | Save `contextiq-connection.json` to `~/Downloads/` or use `--config` / `--url` flag |
| "Authentication failed" | Check username and password; if first login, use the temporary password from your welcome email |
| Tools not appearing in Claude | Restart Cowork/Claude Desktop; verify `contextiq-mcp-proxy` is executable (`chmod +x`) |

For admin-side issues (CloudFormation, S3 publishing, SES), see the [Quickstart Guide troubleshooting section](https://contextiq-releases.s3.us-west-2.amazonaws.com/essentials/latest/templates/README.md).

---

## Resources

- **Quickstart guide:** [Deployment & setup instructions](https://contextiq-releases.s3.us-west-2.amazonaws.com/essentials/latest/templates/README.md)
- **Website:** [contextiq.us](https://contextiq.us)
- **Support:** hello@contextiq.us
- **Enterprise:** Contact us for broader source coverage, custom guardrails, domain-specific validation, and guided rollout

---

## License

MIT — see [LICENSE](LICENSE) for details.
