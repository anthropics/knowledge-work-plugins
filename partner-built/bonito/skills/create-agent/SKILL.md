---
name: create-agent
description: "Create and configure BonBon agents or Bonobot orchestrators with system prompts, models, MCP tools, and RAG knowledge bases. Triggers on 'create an agent', 'deploy a chatbot', 'set up a support bot', 'build an orchestrator', 'make a BonBon', or 'create a Bonobot'."
---

# Create Agent

Create AI agents on the Bonito gateway. Handles both BonBon agents (single-model, task-focused) and Bonobot orchestrators (multi-agent, tool-using).

## Step 1: Determine Agent Type

- Simple task, single model, "chatbot", "support bot" -> **BonBon**
- Multi-step, coordination, "orchestrator", "multi-agent" -> **Bonobot**

If unclear, ask: "Do you need a single-purpose agent or a multi-agent orchestrator?"

## Step 2: Select Model and Provider

1. List available providers via ~~bonito
2. Recommend model based on use case:
   - Customer support -> Claude Sonnet (good balance)
   - Complex reasoning -> Claude Opus or GPT-4o
   - High volume, simple tasks -> Claude Haiku or Groq Llama
   - Code generation -> Claude Sonnet or GPT-4o
3. Confirm with user

## Step 3: Configure System Prompt

If user provides one, use it directly. If they describe the role:
1. Generate a draft (role, tone, boundaries, output format)
2. Present for approval
3. Iterate until satisfied

## Step 4: Attach Knowledge Base (Optional)

1. Check for existing KBs via ~~bonito
2. If new: create KB, upload documents, wait for indexing
3. Configure retrieval settings (top-K, similarity threshold)

## Step 5: Configure MCP Tools (Optional)

Select and attach relevant MCP tool servers for the agent's purpose.

## Step 6: Create, Deploy, and Test

1. Assemble config and call ~~bonito to create
2. Send a basic greeting -> verify response
3. Send a domain query -> verify relevance
4. If tools/KB attached -> test those too

## Output Format

```
## Agent Created: [Name]

| Field | Value |
|-------|-------|
| Type | [BonBon / Bonobot] |
| Model | [Model] via [Provider] |
| Agent ID | [ID] |
| Endpoint | /v1/agents/[id]/chat |
| Knowledge Base | [Name or None] |
| MCP Tools | [Count or None] |
| Status | Deployed |

### Test Results
| Test | Status |
|------|--------|
| Basic greeting | OK |
| Domain query | OK |

### Quick Start
curl -X POST https://api.getbonito.com/v1/agents/[id]/chat \
  -H "Authorization: Bearer $BONITO_API_KEY" \
  -d '{"message": "Hello!"}'
```

## Agent Types

**BonBon:** Single-model agent for focused tasks (support bots, Q&A, code review, content generation). One model, optional system prompt, optional KB, optional MCP tools.

**Bonobot:** Multi-agent orchestrator that delegates to specialized sub-agents. For complex workflows spanning multiple domains or requiring different models for different tasks.
