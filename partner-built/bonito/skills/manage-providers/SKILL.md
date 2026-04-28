---
name: manage-providers
description: "Connect, verify, and manage cloud AI providers through the Bonito gateway. Supports AWS Bedrock, Azure OpenAI, GCP Vertex AI, OpenAI, Anthropic, and Groq. Triggers on 'connect AWS Bedrock', 'add a provider', 'check my providers', 'list my providers', 'set up Azure OpenAI', or 'manage my AI providers'."
---

# Manage Providers

Connect and manage cloud AI providers from one place. Handles adding providers, verifying credentials, listing available models, checking health, and removing unused connections.

## Step 1: Identify the Action

- "Connect AWS Bedrock" / "Add OpenAI" -> create provider
- "List my providers" / "Check my providers" -> list all
- "Is Bedrock healthy?" / "Check provider status" -> health check
- "Remove Groq" -> delete provider
- "Rotate my Anthropic key" -> update credentials

## Step 2: Gather Credentials (for create)

Collect required credentials based on provider type:

| Provider | Required |
|----------|----------|
| AWS Bedrock | Access Key ID, Secret Access Key, Region |
| Azure OpenAI | API Key, Endpoint URL, API Version |
| GCP Vertex AI | Project ID, Region, Service Account JSON |
| OpenAI | API Key |
| Anthropic | API Key |
| Groq | API Key |

Never log or display raw credentials. Prompt the user to provide via environment variables when possible.

## Step 3: Create and Verify

1. Call ~~bonito to create the provider with type and credentials
2. Test API authentication (valid credentials?)
3. Test API reachability (can we reach the endpoint?)
4. List available models on the provider
5. Measure baseline latency

## Step 4: Present Results

**For create:**

```
## Provider Connected: [Name]

| Field | Value |
|-------|-------|
| Type | [AWS Bedrock / Azure OpenAI / etc.] |
| Region | [Region] |
| Status | Connected |
| Models | [Count] available |
| Latency | [X]ms |
```

**For list:**

```
| Provider | Type | Region | Status | Models | Latency |
|----------|------|--------|--------|--------|---------|
| [Name] | AWS Bedrock | us-east-1 | Healthy | 12 | 85ms |
| [Name] | OpenAI | — | Healthy | 8 | 120ms |
```

## Provider Notes

- **AWS Bedrock:** Requires IAM permissions for `bedrock:InvokeModel` and `bedrock:ListFoundationModels`. Some models need explicit access grants. Cross-region inference available.
- **Azure OpenAI:** Models are deployed as named deployments. You need deployment names, not just model names.
- **GCP Vertex AI:** Service account needs `aiplatform.endpoints.predict`. Supports Gemini and Claude via Model Garden.
- **OpenAI/Anthropic:** Direct API access. Simplest setup.
- **Groq:** Optimized for fast inference with open-source models (Llama, Mixtral).
