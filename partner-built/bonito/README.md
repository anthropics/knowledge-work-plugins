# Bonito Plugin

An AI infrastructure management plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. Helps you deploy and manage AI infrastructure across cloud providers, create agents, configure intelligent routing, analyze costs, and debug issues. Works with any team — standalone with the Bonito API, supercharged when you connect GitHub, Slack, and other tools.

## Installation

```bash
claude plugin install bonito
```

## Skills

Domain knowledge Claude uses automatically when relevant:

| Skill | Description |
|---|---|
| `deploy-stack` | Deploy AI infrastructure from a bonito.yaml config — create providers, agents, knowledge bases, and routing in one shot |
| `manage-providers` | Connect, verify, and manage cloud AI providers — AWS Bedrock, Azure OpenAI, GCP Vertex AI, OpenAI, Anthropic, Groq |
| `create-agent` | Create and configure BonBon agents or Bonobot orchestrators with system prompts, models, MCP tools, and RAG |
| `cost-analysis` | Analyze AI spending across providers, identify expensive models, recommend cheaper alternatives, optimize routing |
| `gateway-routing` | Configure routing policies — cost-optimized, failover, A/B testing, model aliases, and cross-region inference |
| `debug-issues` | Troubleshoot gateway errors, provider failures, and agent issues — check logs, verify connections, test endpoints |

## Example Workflows

### Deploying Your AI Stack

Just describe what you want:
```
Deploy my AI infrastructure from bonito.yaml
```

The `deploy-stack` skill reads your config file, creates providers, agents, knowledge bases, and routing policies — all in one shot. It validates each step and reports what was created.

### Connecting a New Provider

```
Connect my AWS Bedrock account as a provider
```

The `manage-providers` skill walks you through credential setup, creates the provider, verifies the connection, and lists available models. Works for any supported cloud provider.

### Building an Agent

```
Create a customer support agent using Claude on AWS Bedrock with our FAQ knowledge base
```

The `create-agent` skill configures a BonBon agent with your chosen model, system prompt, knowledge base, and MCP tools. It deploys the agent and gives you the endpoint.

### Optimizing Costs

```
What am I spending on AI across all providers?
```

The `cost-analysis` skill pulls usage data across all connected providers, breaks down costs by model and agent, identifies expensive patterns, and recommends cheaper alternatives or routing changes.

## Standalone + Supercharged

Every skill works without any additional integrations:

| What You Can Do | Standalone | Supercharged With |
|-----------------|------------|-------------------|
| Deploy infrastructure | bonito.yaml + Bonito API | GitHub (track configs in repos) |
| Manage providers | Bonito API | Monitoring (health dashboards) |
| Create agents | Bonito API | GitHub (version agent configs) |
| Analyze costs | Bonito API | Slack (cost threshold alerts) |
| Configure routing | Bonito API | Monitoring (traffic dashboards) |
| Debug issues | Bonito API logs | Slack (error notifications), Monitoring |

## MCP Integrations

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

Connect your tools for a richer experience:

| Category | Examples | What It Enables |
|---|---|---|
| **AI Gateway** | Bonito MCP | Provider management, agent creation, routing, cost analytics |
| **Version Control** | GitHub, GitLab | Infrastructure-as-code, config versioning, PR reviews |
| **Notifications** | Slack, Teams, Discord | Deployment alerts, cost warnings, provider status updates |
| **Monitoring** | Datadog, Grafana | Traffic dashboards, latency tracking, health monitoring |

See [CONNECTORS.md](CONNECTORS.md) for the full list of supported integrations.

## Settings

Create a `settings.local.json` file to personalize:

- **Cowork**: Save it in any folder you've shared with Cowork (via the folder picker). The plugin finds it automatically.
- **Claude Code**: Save it at `bonito/.claude/settings.local.json`.

```json
{
  "organization": "Your Company",
  "bonito_api_url": "https://api.getbonito.com",
  "default_model": "anthropic/claude-sonnet-4-20250514",
  "preferences": {
    "default_provider": "aws-bedrock",
    "cost_alert_threshold": 100,
    "routing_strategy": "cost-optimized",
    "region": "us-east-1"
  }
}
```

The plugin will ask you for this information interactively if it's not configured.
