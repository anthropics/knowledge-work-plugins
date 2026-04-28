---
name: deploy-stack
description: "Deploy AI infrastructure from a bonito.yaml configuration file. Creates providers, agents, knowledge bases, and routing policies in one shot. Triggers on 'deploy my AI stack', 'set up Bonito', 'deploy bonito.yaml', 'create my infrastructure', or 'deploy from config'."
---

# Deploy Stack

Deploy entire AI infrastructure from a single `bonito.yaml` config. Validates the schema, resolves dependencies, and creates all resources in the correct order.

## Step 1: Parse and Validate

Read bonito.yaml and extract:
- **Providers** (cloud AI services to connect)
- **Knowledge bases** (documents and embedding configs)
- **Agents** (BonBon agents and Bonobot orchestrators)
- **Routing** (policies, aliases, fallback chains)

Validate: required fields present, provider types supported, model references resolve, no circular dependencies.

## Step 2: Resolve Dependency Order

1. Providers first (everything depends on them)
2. Knowledge bases second (agents may reference them)
3. Agents third (depend on providers + KBs)
4. Routing policies last (reference providers and models)

## Step 3: Create Resources

For each resource in order:
1. Call ~~bonito to create it
2. Verify it's healthy (test connection, check response)
3. Record the ID for downstream references

If credentials are missing, prompt the user. Never store or log raw API keys.

## Step 4: Verify and Report

```
## Deployment Report

| Resource | Type | Status |
|----------|------|--------|
| [Name] | AWS Bedrock provider | Connected (12 models) |
| [Name] | Knowledge base | Indexed (42 chunks) |
| [Name] | BonBon agent | Deployed (85ms) |
| [Name] | Failover routing | Active |

Total: [X] providers, [X] KBs, [X] agents, [X] routing policies
```

## Config Reference

```yaml
# bonito.yaml
organization: my-company

providers:
  - name: aws-primary
    type: aws-bedrock
    region: us-east-1
  - name: openai-fallback
    type: openai

knowledge_bases:
  - name: support-faq
    documents: ./docs/faq/
    embedding_model: text-embedding-3-small

agents:
  - name: support-bot
    type: bonbon
    model: anthropic/claude-sonnet
    provider: aws-primary
    knowledge_base: support-faq
    system_prompt: "You are a helpful customer support agent."

routing:
  - name: production
    strategy: failover
    targets:
      - provider: aws-primary
        model: anthropic/claude-sonnet
        priority: 1
      - provider: openai-fallback
        model: gpt-4o
        priority: 2
```
