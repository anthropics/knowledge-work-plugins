# SAP Datasphere Plugin for Claude

The most comprehensive SAP Datasphere plugin for Claude. 18 specialized skills, 30 reference files, and 31,000+ lines of expert content covering every major Datasphere workflow — from data exploration and view design to BW Bridge migration, security architecture, CLI automation, and catalog governance. Powered by a production-grade MCP server with 45 tools, OAuth 2.0 authentication, and enterprise-level security including SQL sanitization and PII filtering.

## Skills

### Exploration & Discovery

| Skill | Description |
|-------|-------------|
| **datasphere-explorer** | Guided exploration and discovery — browse spaces, search the catalog, inspect schemas, profile data quality, trace lineage, and build queries interactively |

### Data Modeling

| Skill | Description |
|-------|-------------|
| **datasphere-view-architect** | Design Graphical and SQL views with proper semantic usage (Fact, Dimension, Text, Hierarchy), associations, persistence strategies, and performance optimization |
| **datasphere-analytic-model-creator** | Create Analytic Models for SAP Analytics Cloud with measures, dimensions, variables, currency conversion, and exception aggregation |
| **datasphere-intelligent-lookup** | Configure fuzzy matching and intelligent lookups for data harmonization across sources — matching strategies, threshold tuning, and review workflows |

### Data Integration

| Skill | Description |
|-------|-------------|
| **datasphere-data-flows** | Orchestrate replication flows (with CDC), data flows (visual ETL), transformation flows (SQL-based delta), and task chains |
| **datasphere-transformation-logic** | Generate and validate SQLScript and Python transformations — SCD Type 2, deduplication, pivoting, delta handling patterns |
| **datasphere-s4hana-import** | Import entities from SAP S/4HANA and BW/4HANA — CDS views, ODP extractors, Cloud Connector setup, and delta extraction |
| **datasphere-connections** | Create and manage 35+ connection types including SAP S/4HANA, BigQuery, Redshift, Kafka, and generic JDBC/OData connectors |

### Migration

| Skill | Description |
|-------|-------------|
| **datasphere-bw-bridge-migration** | Migrate from BW/4HANA using Shell and Remote Conversion — ADSO modeling, Process Chain to Task Chain mapping, hybrid operation, and decommissioning |

### Security

| Skill | Description |
|-------|-------------|
| **datasphere-security-architect** | Design row-level security with Data Access Controls (DAC), import BW Analysis Authorizations, configure audit policies, and integrate Identity Providers (SAML/OIDC) |

### Administration & Governance

| Skill | Description |
|-------|-------------|
| **datasphere-admin** | Space management, user and role administration, system monitoring, capacity planning, and transport operations |
| **datasphere-cli-automator** | Automate administration via CLI — generate JSON payloads for bulk space/user/connection provisioning, manage certificates, and build CI/CD pipelines |
| **datasphere-data-product-publisher** | Publish data products through the Data Sharing Cockpit — product descriptions, license terms, visibility settings, and marketplace management |
| **datasphere-transport-manager** | Manage CSN/JSON transport packages — dependency checking, export/import workflows, conflict resolution, and Content Network integration |
| **datasphere-business-content-activator** | Activate pre-built SAP Business Content packages — prerequisite checking (Time Dimensions, TCUR*), LSA++ alignment, and content update management |
| **datasphere-catalog-steward** | Internal data governance — metadata enrichment, glossary term management, KPI definitions, tag taxonomies, and lineage-based impact analysis |

### Monitoring & Troubleshooting

| Skill | Description |
|-------|-------------|
| **datasphere-flow-doctor** | Diagnose and resolve errors in Data Flows, Replication Flows, and Transformation Flows — error catalogs, root cause analysis, and fix recommendations |
| **datasphere-performance-optimizer** | Analyze and optimize performance — View Analyzer, Explain Plans, persistence strategies, partitioning, storage tiering, and query tuning |

## Reference Library (30 files)

Each skill includes detailed reference documentation for deep-dive guidance:

| Skill | Reference Files |
|-------|----------------|
| **explorer** | exploration-workflows.md |
| **view-architect** | view-modeling-guide.md |
| **analytic-model-creator** | analytic-model-guide.md |
| **intelligent-lookup** | intelligent-lookup-guide.md |
| **data-flows** | data-flows.md, replication-flows.md, transformation-flows.md, task-chains.md |
| **transformation-logic** | transformation-patterns.md |
| **s4hana-import** | s4hana-integration-guide.md, cds-replication-architecture.md |
| **connections** | authentication.md, connection-types.md, troubleshooting-guide.md |
| **bw-bridge-migration** | bw-bridge-guide.md |
| **security-architect** | security-patterns.md |
| **admin** | space-management.md, system-monitoring.md, security-governance.md, transport.md |
| **cli-automator** | cli-reference.md |
| **data-product-publisher** | data-sharing-guide.md |
| **transport-manager** | transport-operations.md |
| **business-content-activator** | content-catalog.md |
| **catalog-steward** | catalog-governance-guide.md |
| **flow-doctor** | error-catalog.md, abap-side-monitoring.md, replication-flow-error-patterns.md |
| **performance-optimizer** | optimization-techniques.md, diagnostic-procedures.md |

## Prerequisites

- [Claude Code](https://claude.com/claude-code) v1.0.33+ or Claude Desktop with Cowork mode
- An SAP Datasphere tenant with OAuth 2.0 client credentials
- Node.js 18+ (for the MCP server)

## Installation

Install from a marketplace or load directly:

```bash
claude --plugin-dir ./sap-datasphere-plugin-for-claude-cowork
```

## Configuration

After installation, configure your SAP Datasphere connection by setting the environment variables in `.mcp.json`:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATASPHERE_BASE_URL` | Your tenant URL | `https://mytenant.eu20.hcs.cloud.sap` |
| `DATASPHERE_CLIENT_ID` | OAuth client ID | From SAP BTP cockpit |
| `DATASPHERE_CLIENT_SECRET` | OAuth client secret | From SAP BTP cockpit |
| `DATASPHERE_TOKEN_URL` | OAuth token endpoint | `https://mytenant.authentication.eu20.hana.ondemand.com/oauth/token` |
| `DATASPHERE_AUTH_URL` | OAuth auth endpoint | `https://mytenant.authentication.eu20.hana.ondemand.com` |

### Setting up OAuth credentials in SAP BTP

1. Open the SAP BTP Cockpit for your subaccount
2. Navigate to **Security > Instances and Subscriptions**
3. Create a service instance for SAP Datasphere with the appropriate scopes
4. Create a service key to obtain your client ID and secret

## Usage

Once configured, just talk to Claude naturally:

- *"What spaces do we have in Datasphere?"*
- *"Help me design a star schema for customer analytics"*
- *"Create an analytic model with revenue measures"*
- *"Import CDS views from our S/4HANA system"*
- *"Migrate our BW Process Chains to Task Chains"*
- *"Set up row-level security on the sales data"*
- *"Bulk-create 50 users via CLI"*
- *"Activate the Automotive business content package"*
- *"My replication flow is failing — help me diagnose"*
- *"Optimize this slow-running view"*
- *"Set up a transport package for production deployment"*
- *"Enrich our catalog with business glossary terms"*
- *"Generate SCD Type 2 logic for the customer dimension"*

## MCP Server

This plugin uses the [`@mariodefe/sap-datasphere-mcp`](https://www.npmjs.com/package/@mariodefe/sap-datasphere-mcp) MCP server, which provides 45 tools covering:

- **Foundation**: Connection testing, user info, tenant config
- **Catalog & Discovery**: Space browsing, asset search, marketplace
- **Schema & Metadata**: Table schemas, OData metadata, analytical models
- **Data Query**: Smart queries, SQL execution, OData queries
- **Data Profiling**: Column distribution analysis, cross-asset column search
- **Repository & Lineage**: Object search, lineage tracing, deployment status
- **Database Users**: Full CRUD for space-level database users

## Security

The MCP server includes enterprise-grade security:

- OAuth 2.0 with automatic token refresh
- RBAC-based authorization enforcement
- SQL injection prevention and query sanitization
- PII redaction and credential masking
- Input validation on all tool parameters

## License

MIT
