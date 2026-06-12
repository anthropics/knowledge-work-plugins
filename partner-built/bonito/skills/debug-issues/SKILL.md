---
name: debug-issues
description: "Troubleshoot gateway errors, provider failures, agent issues, and routing problems. Check logs, verify connections, test endpoints, and diagnose root causes. Triggers on 'why is my agent failing', 'debug gateway', 'check provider status', 'something is broken', 'getting errors', or 'troubleshoot'."
---

# Debug Issues

Diagnose and fix problems with the Bonito gateway, providers, agents, and routing. Systematically check each layer, identify the root cause, and guide to a fix.

## Step 1: Understand the Problem

- Specific error message -> start with that component
- General "it's broken" -> run full diagnostic sweep
- Specific agent -> start with agent health
- Specific provider -> start with provider check
- Performance issue -> start with latency analysis

## Step 2: Check Each Layer

**Gateway:** Is the API reachable? Is auth valid? What's the latency?

**Providers:** For each connected provider:
- Is the API reachable? Are credentials valid?
- What's the error rate (last hour)?
- Are specific models affected, or all?

**Agents:** For affected agents:
- Is the config valid? Does the referenced model exist?
- Send a test message. Check response or error.
- If KB attached, test retrieval. If tools attached, test availability.

**Routing:** For affected policies:
- Are all referenced providers/models valid?
- Does failover trigger correctly?
- Any circular dependencies?

## Step 3: Pull Logs

Query ~~bonito for recent errors:
- Filter by time range and component
- Identify patterns: sudden spike (outage), gradual increase (rate limiting), intermittent (network)
- Count errors by type

## Step 4: Present Diagnosis and Fix

```
## Diagnostic Report

Issue: [User's reported problem]
Root Cause: [Brief description]

### System Health
| Component | Status | Details |
|-----------|--------|---------|
| Gateway | Healthy | 45ms |
| Provider: Bedrock | Down | 503 Service Unavailable |
| Agent: support-bot | Error | Upstream provider failure |

### What Happened
[Clear explanation of the issue chain]

### Fix
1. [Immediate action to resolve]
2. [Verification step]

### Prevention
1. [Step to prevent recurrence]
```

## Common Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| 401/403 errors | Expired API key | Regenerate key, update config |
| Timeouts (504) | Provider overloaded | Retry or failover to alt provider |
| Model not found (404) | Typo or model deprecated | Verify model name, use aliases |
| Rate limiting (429) | Too many requests | Spread across providers, upgrade tier |
| Agent not responding | Bad config or provider down | Check config, test provider health |
