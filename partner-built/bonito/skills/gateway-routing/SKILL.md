---
name: gateway-routing
description: "Configure routing policies for the Bonito AI gateway. Failover chains, cost-optimized routing, A/B testing, model aliases, and cross-region inference. Triggers on 'set up failover', 'configure routing', 'add a fallback model', 'cross-region inference', 'create a model alias', or 'A/B test models'."
---

# Gateway Routing

Configure intelligent request routing across AI providers. Handles failover, cost optimization, A/B testing, model aliases, and cross-region inference.

## Step 1: Determine Strategy

- "Set up failover" -> failover chain
- "Route to cheapest" -> cost-optimized
- "A/B test Claude vs GPT" -> ab-test
- "Load balance" -> round-robin / weighted
- "Create alias 'fast'" -> model alias
- "Cross-region" -> geo-routing

## Step 2: Gather Requirements

**Failover:** Primary provider/model, fallback(s), failure detection criteria (timeout, error codes).

**Cost-optimized:** Quality threshold (minimum model tier), budget constraints, acceptable substitutes.

**A/B test:** Models A and B with providers, traffic split percentage, test duration.

**Model alias:** Alias name, target model and provider.

## Step 3: Validate and Create

1. List connected providers via ~~bonito
2. Verify requested models are available and healthy
3. Create the routing policy via ~~bonito
4. Set strategy, targets, priorities/weights, failover thresholds

## Step 4: Verify

1. Send test request -> confirm it routes to primary
2. For failover -> simulate failure -> confirm switch
3. For A/B -> send multiple requests -> confirm split ratio
4. Measure failover latency

## Output Format

```
## Routing Policy: [Name]

Strategy: [Failover / Cost-Optimized / A/B Test]
Status: Active

| Priority | Provider | Model | Status |
|----------|----------|-------|--------|
| Primary | AWS Bedrock | claude-sonnet | Healthy |
| Fallback | OpenAI | gpt-4o | Healthy |
| Last resort | Groq | llama-3-70b | Healthy |

Verification:
- Primary route: OK (85ms)
- Failover trigger: OK (<500ms switch)
```

## Strategies

**Failover:** Route to primary. If it fails, try the next. Use when uptime matters most.

**Cost-optimized:** Route to cheapest model meeting quality requirements. Tiers: budget (Groq Llama) -> standard (Claude Sonnet) -> premium (Claude Opus).

**A/B testing:** Split traffic between models for comparison. Set duration and metrics (latency, quality, cost).

**Round-robin / Weighted:** Distribute traffic across providers. Optional session affinity.

**Geo-routing:** Route to nearest or lowest-latency region. Requires multi-region provider setup.
