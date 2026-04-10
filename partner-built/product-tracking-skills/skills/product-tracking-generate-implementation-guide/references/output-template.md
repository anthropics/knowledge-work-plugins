# instrument.md Output Template

Write to `.telemetry/instrument.md` following this structure:

```markdown
# Instrumentation Guide

## Target: [SDK Name]

Generated from tracking-plan.yaml v[version] on [date].

## SDK Setup

### Dependencies
[Package names, install commands]

### Initialization
[Setup code, configuration]

### Environment Variables
| Variable | Purpose | Required |
[Table of env vars needed]

## Identity

### identify()

**Syntax:**
[SDK-specific call signature]

**User Traits:**
| Trait | Type | PII | Notes |
[Mapped from tracking plan entities]

**When to Call:**
[Trigger points]

**Template Code:**
[One real, working example with the plan's actual traits]

### group()

**Syntax:**
[SDK-specific call signature]

**Group Hierarchy:**
| Level | SDK Mapping | ID Source | Parent |
[How plan groups map to SDK]

**Group Traits:**
| Level | Trait | Type | Notes |
[Mapped from tracking plan groups]

**When to Call:**
[Trigger points]

**Template Code:**
[One real, working example per group level]

## Events

### track()

**Syntax:**
[SDK-specific call signature]

**SDK Constraints:**
[e.g., Accoil: no properties — encode in event names]

**Template Code:**
[1-2 representative examples showing the call pattern]

### Group-Level Attribution

[How to attribute events to different group levels in this SDK]
[Template code showing attribution at different levels]

## Complete Tracking Module

[Include the COMPLETE, copy-paste-ready tracking module code here. This should be a single block that a developer can drop into their codebase — not fragments requiring assembly. Include all imports, class/module definitions, event constants, identify/group/track functions, delivery infrastructure, and initialization. The developer should never need to mentally stitch pieces together.]

## Architecture

### Client vs Server
[Which calls go where]

### Queues and Batching
[SDK-specific batching/queue behavior]

### Shutdown / Flush
[How to handle graceful shutdown]

### Error Handling
[What to catch, retry behavior]

## Verification

### Confirming Delivery
[How to verify events are arriving — debug console, API response logs, destination dashboard]

### Expected Latency
[Real-time for direct API, batched interval for queue-based delivery]

### Success vs Failure
[HTTP status codes, error responses, what to look for in logs]

### Development Testing
[How to test without polluting production — separate API keys, environment flags, dry-run mode]

## Rollout Strategy (if requested)

1. **Development:** Enable verbose/debug logging. Verify event shape and delivery.
2. **Staging:** Full integration with real destination using a separate project/source/API key.
3. **Production — gradual:** Start with lifecycle events only. Verify in the destination dashboard. Then enable core value events.
4. **Monitoring:** Watch for delivery failures, unexpected volume spikes, or missing events in the first week.

## SDK-Specific Constraints
[Bullet list of gotchas, limitations, and things to watch for]

## Coverage Gaps
[Note any environments or SDK variants not covered by the reference files.
If the user's stack requires patterns not documented here, flag it.]
```
