# CockroachDB Plugin for Claude Code

[![Release Please](https://github.com/cockroachdb/claude-plugin/actions/workflows/release-please.yml/badge.svg)](https://github.com/cockroachdb/claude-plugin/actions/workflows/release-please.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

The CockroachDB plugin for [Claude Code](https://code.claude.com/) gives your AI coding agent direct access to CockroachDB databases — explore schemas, write optimized SQL, debug queries, and manage distributed clusters.

## Installation

Install from the [Claude Marketplace](https://claude.com/plugins/cockroachdb), or in Claude Code run:

```
/install-plugin cockroachdb
```

### Local development

```bash
claude --plugin-dir /path/to/claude-plugin
```

### Prerequisites

This plugin connects to CockroachDB via MCP (Model Context Protocol) using [MCP Toolbox for Databases](https://github.com/googleapis/genai-toolbox) (v0.27.0+):

```bash
brew install mcp-toolbox
```

## Configuration

Set environment variables for your CockroachDB connection:

```bash
export COCKROACHDB_HOST="your-cluster-host"
export COCKROACHDB_PORT="26257"
export COCKROACHDB_USER="your-user"
export COCKROACHDB_PASSWORD="your-password"
export COCKROACHDB_DATABASE="your-database"
export COCKROACHDB_SSLMODE="verify-full"
```

For CockroachDB Cloud, find connection details in the [Cloud Console](https://cockroachlabs.cloud/).

### Alternative MCP Backends

The plugin ships with the **MCP Toolbox** (stdio) backend active by default. To use a different backend, replace the contents of `.mcp.json`:

<details>
<summary><strong>MCP Toolbox via HTTP</strong> (remote/multi-user)</summary>

```json
{
  "mcpServers": {
    "cockroachdb-toolbox-http": {
      "type": "http",
      "url": "http://your-toolbox-host:5000/mcp"
    }
  }
}
```

Run Toolbox in HTTP mode: `toolbox --tools-file tools.yaml --address 0.0.0.0:5000`
</details>

<details>
<summary><strong>ccloud CLI</strong> (cluster lifecycle, backups, DR, networking)</summary>

The [`ccloud` CLI](https://www.cockroachlabs.com/blog/cockroachdb-ai-agents-cli-database-automation/) is an agent-ready command-line tool for full cluster lifecycle management. AI agents call ccloud directly via shell commands (not MCP protocol) -- every command supports `-o json` for structured output.

**Install:** `brew install cockroachdb/tap/ccloud`

**Authenticate (interactive):** `ccloud auth login` (opens browser; supports SSO via OIDC/SAMLv2)

**Authenticate (org-scoped):** `ccloud auth login --org {organization-label}`

**Authenticate (headless/CI):** `ccloud auth login --no-redirect` or use a service account API key as a bearer token.

**Example agent commands:**
```bash
# Provision
ccloud cluster create serverless my-cluster us-east-1 --cloud AWS -o json
ccloud cluster database create my-cluster myapp -o json

# Connect
ccloud cluster connection-string my-cluster --database myapp --sql-user maxroach -o json
# Composable: pipe into jq + psql
ccloud cluster connection-string my-cluster --database myapp --sql-user maxroach -o json \
  | jq -r '.connection_url' | xargs -I{} psql {} -c "SELECT count(*) FROM users"

# Operate
ccloud cluster list -o json
ccloud cluster info my-cluster -o json
ccloud cluster backup config update my-cluster --frequency 60 --retention 60

# Observe
ccloud audit list --limit 10 -o json
ccloud cluster versions -o json
ccloud cluster cmek get my-cluster -o json

# Scale & DR
ccloud replication create --primary-cluster prod-east --standby-cluster dr-west
ccloud cluster networking allowlist list <cluster-id> -o json

# Organize
ccloud folder create Production -o json
ccloud folder contents <folder-id> -o json

# Test resilience
ccloud cluster disruption set my-cluster --region us-east-1 --whole-region
```

**Coverage:** Provision, Connect, Operate, Observe, Scale & DR, Organize, Test resilience. See the [ccloud reference](https://www.cockroachlabs.com/docs/cockroachcloud/ccloud-reference) for full command list.
</details>

<details>
<summary><strong>CockroachDB Cloud MCP Server</strong> (OAuth/API key)</summary>

The official [managed MCP server](https://www.cockroachlabs.com/blog/cockroachdb-ai-agents-managed-mcp-server/) is hosted by Cockroach Labs and requires no infrastructure setup. Authenticate via OAuth 2.1 (PKCE) or a service account API key. Read-only by default; write access requires explicit consent.

**OAuth (recommended — opens browser for consent, scopes: `mcp:read`, `mcp:write`):**
```json
{
  "mcpServers": {
    "cockroachdb-cloud": {
      "type": "http",
      "url": "https://cockroachlabs.cloud/mcp",
      "headers": {
        "mcp-cluster-id": "{your-cluster-id}"
      }
    }
  }
}
```

**API Key (headless/autonomous agents):**
```json
{
  "mcpServers": {
    "cockroachdb-cloud": {
      "type": "http",
      "url": "https://cockroachlabs.cloud/mcp",
      "headers": {
        "mcp-cluster-id": "{your-cluster-id}",
        "Authorization": "Bearer {your-service-account-api-key}"
      }
    }
  }
}
```

Or via CLI: `claude mcp add cockroachdb-cloud https://cockroachlabs.cloud/mcp --transport http --header "mcp-cluster-id: {your-cluster-id}"`

See the [quickstart guide](https://www.cockroachlabs.com/docs/cockroachcloud/connect-to-the-cockroachdb-cloud-mcp-server) for detailed setup.
</details>

## What's Included

### MCP Backends

| Backend                    | Status      | Transport       | Use Case                                                                                                                          |
|----------------------------|-------------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------|
| `cockroachdb-toolbox`      | Active      | stdio           | Any CockroachDB cluster via [MCP Toolbox](https://github.com/googleapis/genai-toolbox)                                            |
| `cockroachdb-cloud`        | Active      | Streamable HTTP | [Managed MCP Server](https://www.cockroachlabs.com/blog/cockroachdb-ai-agents-managed-mcp-server/) — CockroachDB Cloud (OAuth/API key) |
| `cockroachdb-toolbox-http` | Available   | Streamable HTTP | MCP Toolbox remote/multi-user via HTTP                                                                                            |

### CLI Tools

| Tool              | Status | Use Case                                                                                                                                           |
|-------------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `ccloud`          | Active | [Agent-ready CLI](https://www.cockroachlabs.com/blog/cockroachdb-ai-agents-cli-database-automation/) — cluster lifecycle, backups, DR, networking, audit. Agents call directly via shell. |

### Tools

**MCP Toolbox** (self-hosted, any cluster):

| Tool                       | Description                                      |
|----------------------------|--------------------------------------------------|
| `cockroachdb-execute-sql`  | Execute SQL statements (SELECT, DDL, DML)        |
| `cockroachdb-list-schemas` | List all schemas in the database                 |
| `cockroachdb-list-tables`  | List tables with columns, types, and constraints |

**CockroachDB Cloud MCP** (managed, read tools):

| Tool                    | Description                                 |
|-------------------------|---------------------------------------------|
| `list_clusters`         | List all accessible clusters                |
| `get_cluster`           | Get detailed cluster information            |
| `list_databases`        | List databases in the cluster               |
| `list_tables`           | List tables in a database                   |
| `get_table_schema`      | Get detailed schema for a table             |
| `select_query`          | Execute a SELECT statement                  |
| `explain_query`         | Execute an EXPLAIN statement                |
| `show_running_queries`  | List currently executing queries            |

**CockroachDB Cloud MCP** (managed, write tools — requires write consent):

| Tool                    | Description                                 |
|-------------------------|---------------------------------------------|
| `create_database`       | Create a new database                       |
| `create_table`          | Create a new table                          |
| `insert_rows`           | Insert rows into a table                    |

### Skills

Skills are sourced from the [`cockroachdb-skills`](https://github.com/cockroachlabs/cockroachdb-skills) submodule via symlinks — a single source of truth shared across CockroachDB agent integrations. A [weekly CI workflow](.github/workflows/update-skills.yml) auto-detects upstream changes and opens a PR to update.

| Domain                             | Examples                                                     |
|------------------------------------|--------------------------------------------------------------|
| **Query & Schema Design**          | cockroachdb-sql                                              |
| **Observability & Diagnostics**    | profiling-statement-fingerprints, triaging-live-sql-activity |
| **Security & Governance**          | auditing-cloud-cluster-security, hardening-user-privileges   |
| **Onboarding & Migrations**        | molt-fetch, molt-verify, molt-replicator                     |
| **Operations & Lifecycle**         | managing-cluster-capacity, upgrading-cluster-version         |

### Agents

| Agent                    | Description                                                                          |
|--------------------------|--------------------------------------------------------------------------------------|
| `cockroachdb-dba`        | CockroachDB DBA expert — performance tuning, schema review, cluster diagnostics      |
| `cockroachdb-developer`  | Application developer expert — ORM config, retry logic, transaction patterns         |
| `cockroachdb-operator`   | Operator/SRE expert — cluster operations, monitoring, backups, scaling, incidents    |

Agents are auto-discovered from the `agents/` directory. Claude invokes them automatically based on task context, or you can reference them directly (e.g., "ask the cockroachdb-dba agent to review this schema").

### Hooks

| Hook              | Trigger               | What It Does                                                                         |
|-------------------|-----------------------|--------------------------------------------------------------------------------------|
| `validate-sql`    | Before SQL execution  | Blocks DROP DATABASE, TRUNCATE; warns on SERIAL, multi-DDL transactions              |
| `check-sql-files` | After file Write/Edit | Scans SQL/code files for CockroachDB anti-patterns (SERIAL, SELECT *, missing retry) |

Hooks run as Python scripts (Python 3, no external dependencies) and provide automated safety guardrails.

## Development

Clone the repository:

```bash
git clone --recurse-submodules https://github.com/cockroachdb/claude-plugin.git
cd claude-plugin
```

Test locally:

```bash
claude --plugin-dir .
```

Validate the plugin:

```bash
claude plugin validate .
```

### Project Structure

```
.claude-plugin/
  plugin.json                  # Plugin manifest with component declarations
  marketplace.json             # Marketplace catalog for distribution
.mcp.json                      # MCP server configuration
tools.yaml                     # Toolbox source & tool definitions
agents/
  cockroachdb-dba.md           # DBA agent
  cockroachdb-developer.md     # Developer agent
  cockroachdb-operator.md      # Operator agent
hooks/
  hooks.json                   # Hook configuration
scripts/
  validate-sql.py              # SQL validation hook
  check-sql-files.py           # Anti-pattern linter hook
skills/                        # Skills copied from cockroachdb-skills submodule
submodules/
  cockroachdb-skills/          # Shared skills submodule
assets/
  logo.svg                     # Plugin logo
```

## Releasing

This repo uses [Release Please](https://github.com/googleapis/release-please) for automated releases.

1. Use [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`) on `main`
2. Release Please opens a Release PR with version bump and changelog
3. Merge the Release PR to publish

## Links

- [CockroachDB Documentation](https://www.cockroachlabs.com/docs/)
- [CockroachDB Cloud Console](https://cockroachlabs.cloud/)
- [Managed MCP Server Blog Post](https://www.cockroachlabs.com/blog/cockroachdb-ai-agents-managed-mcp-server/)
- [Cloud MCP Quickstart Guide](https://www.cockroachlabs.com/docs/cockroachcloud/connect-to-the-cockroachdb-cloud-mcp-server)
- [ccloud CLI for AI Agents Blog Post](https://www.cockroachlabs.com/blog/cockroachdb-ai-agents-cli-database-automation/)
- [Claude Code Plugin Docs](https://code.claude.com/docs/en/plugins)
- [Plugin Marketplace Docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [ccloud CLI](https://www.cockroachlabs.com/docs/cockroachcloud/ccloud-get-started)
- [MCP Toolbox for Databases](https://github.com/googleapis/genai-toolbox)
- [Report Issues](https://github.com/cockroachdb/claude-plugin/issues)

## License

[Apache-2.0](LICENSE)
