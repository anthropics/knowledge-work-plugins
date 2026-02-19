# Connectors — Swiss Legal Plugin

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~cloud storage` might mean SharePoint, Box, or any storage provider with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

---

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Chat | `~~chat` | Slack | Microsoft Teams |
| Cloud storage | `~~cloud storage` | SharePoint, Box | Egnyte, Dropbox, Google Drive |
| CLM | `~~CLM` | — | Ironclad, Agiloft, Juro |
| CRM | `~~CRM` | — | Salesforce, HubSpot |
| E-signature | `~~e-signature` | — | DocuSign, Adobe Sign, PrivaSphere (Swiss-qualified) |
| Office suite | `~~office suite` | Microsoft 365 | Google Workspace |
| Project tracker | `~~project tracker` | Atlassian (Jira/Confluence) | Linear, Asana |

---

## Swiss-specific integrations

These integrations are relevant for Swiss legal workflows and are referenced in plugin commands and skills.

| Service | Purpose | Access |
|---------|---------|--------|
| **zefix.ch** (Swiss Federal Commercial Registry) | Handelsregister entity lookup; Kollektivunterschrift / signing authority verification; UID number check | Public web; no MCP required — use WebFetch |
| **shab.ch** (Schweizerisches Handelsamtsblatt / SOGC) | Bundesblatt-equivalent official gazette; company announcements; liquidation notices | Public web; no MCP required |
| **edoeb.admin.ch** (FDPIC / EDÖB) | FDPIC guidance, adequacy list, complaint register | Public web; no MCP required |
| **finma.ch** | FINMA circulars, outsourcing register, supervised entity lookup | Public web; no MCP required |
| **bger.ch / bvger.ch** | BGer (Federal Supreme Court) and BVGer (Federal Administrative Court) decisions | Public web; no MCP required |
| **eur-lex.europa.eu** | GDPR text, EU adequacy decisions, SCCs (June 2021) | Public web; no MCP required |

---

## Connector usage in workflows

### Contract review (`/review-contract`)
- `~~cloud storage`: Retrieve contract files and precedent library
- `~~CLM`: Look up existing agreements with the same counterparty
- `~~e-signature`: Route executed redlines for signature
- zefix.ch: Verify counterparty Handelsregister entry and signing authority (Kollektivunterschrift)

### Vendor check (`/vendor-check`)
- `~~CLM`: Primary source for existing agreement status
- `~~cloud storage`: Retrieve agreement copies and certificates
- zefix.ch: UID/entity verification; current Handelsregister status

### Daily brief (`/brief daily`)
- `~~office suite`: Calendar items requiring legal prep; incoming email flagged for legal
- `~~chat`: Overnight requests in legal Slack channels
- `~~project tracker`: Open matters, upcoming deadlines, DSR tracker
- shab.ch / bger.ch / edoeb.admin.ch: Regulatory monitoring (fetched directly)

### Incident brief (`/brief incident`)
- `~~chat`: Incident channel context (Slack #security, #legal)
- `~~office suite`: Incident emails, board notification drafts
- edoeb.admin.ch: FDPIC notification portal reference
- finma.ch: FINMA outsourcing notification requirement (if FINMA-supervised)

### DSR / Auskunftsbegehren response (`/respond dsr`)
- `~~project tracker`: DSR intake register; deadline tracking
- `~~office suite`: Response letter drafting and delivery
- `~~cloud storage`: Data map / Verarbeitungsverzeichnis for data categories

### FDPIC inquiry response (`/respond fdpic`)
- **Always escalate to outside Swiss counsel** — templates are orientation only
- `~~cloud storage`: AV-Vereinbarungen, Datenschutzerklärung, processing records
- `~~project tracker`: FDPIC matter docket (Aktenzeichen tracking)

---

## Graceful degradation

When MCP connections are unavailable, the plugin will:
1. Note which tool category is missing
2. Describe what the tool would have provided
3. Ask the user to supply the information manually or check the relevant Swiss registry/authority website directly
4. Continue the workflow with available information

The zefix.ch Handelsregister check is always flagged as a manual step since it requires real-time verification before contract execution.
