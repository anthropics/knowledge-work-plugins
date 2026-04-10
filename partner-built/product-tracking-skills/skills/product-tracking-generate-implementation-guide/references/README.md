# Integration References

This directory contains reference files for analytics destinations. Each file documents how to implement the core analytics calls — identify, group, track — using a specific tool's SDK and API.

The `product-tracking-generate-implementation-guide` skill reads the matching reference file before producing project-specific instrumentation guides. If a destination doesn't have a reference file here, the skill can't produce accurate guidance for it.

## Contributing a New Reference

### 1. Research the provider's current documentation

Every reference must be based on the provider's **current, live documentation** — not general knowledge. At a minimum, read:

- Getting started / quickstart page
- SDK reference (browser and Node.js if available)
- HTTP API reference
- User identification docs
- Group / account analytics docs (if the tool supports it)
- Rate limits and constraints

### 2. Follow the template

Use [destination-reference-template.md](destination-reference-template.md) as your starting point. It includes:

- A classification matrix to determine the tool's category and B2B fit
- A full research checklist covering auth, SDKs, method mapping, infrastructure, and debugging
- A skeleton markdown structure with all required sections
- Category-specific guidance (what to emphasize for web analytics vs product analytics vs error monitoring, etc.)

### 3. Conventions

**File naming:** lowercase, hyphenated. Examples: `segment.md`, `posthog.md`, `google-analytics.md`.

**Standard identifiers** — all code examples must use these consistently:

| Prefix | Entity |
|---|---|
| `usr_123` | User |
| `acc_456` | Account |
| `ws_789` | Workspace |
| `proj_123` | Project |
| `rpt_789` | Report |
| `task_456` | Task |

**Properties** use `snake_case` throughout.

**Code examples** must use the SDK's real API — correct imports, correct method signatures, correct authentication. No pseudocode.

### 4. Quality checklist

Before submitting:

- [ ] All code examples use real SDK calls from current documentation
- [ ] Standard B2B identifiers used throughout
- [ ] Properties use `snake_case`
- [ ] "Further Documentation" links point to real, working URLs
- [ ] At least 3 tool-specific Common Pitfalls
- [ ] Group context section present (for tools with Full or Partial B2B Fit)
- [ ] Overview clearly states the tool's category
- [ ] No marketing language — factual descriptions only

### 5. Update the skill

After adding a reference file, add it to the Reference Index in [`../SKILL.md`](../SKILL.md) under the appropriate category heading:

```markdown
- {Provider Name}: [references/{provider}.md](references/{provider}.md)
```

## Categories

| Category | B2B Fit | References |
|---|---|---|
| Product Analytics | Full | amplitude, mixpanel, posthog |
| CDPs | Full | segment, rudderstack |
| B2B Engagement | Full | accoil, journy |
| Full-Stack Analytics | Partial | google-analytics, usermaven |
| Web Analytics | Minimal | plausible, fathom, simple-analytics, beam-analytics, microanalytics, withcabin, cloudflare-web-analytics |
| Error / Performance | None | sentry, new-relic, azure-application-insights |
| Feature Flags | Partial | launchdarkly, statsig |
| Session / Behavior | Minimal | hotjar, userpilot |
| Tag Management | None | google-tag-manager |

**B2B Fit** indicates how well the tool maps to the standard identify → group → track model:
- **Full** — native users, accounts, and custom events with properties
- **Partial** — user identity supported, limited or no account-level grouping
- **Minimal** — session tagging only, no persistent identity model
- **None** — not designed for user/account analytics

## Supporting Files

| File | Purpose |
|---|---|
| `destination-reference-template.md` | Full template with research checklist and section skeleton |
| `behavioral-rules.md` | Quality rules for the implementation guide skill |
| `output-template.md` | Output structure for `.telemetry/instrument.md` |
| `forge-platform.md` | Forge platform architecture reference |
| `generic-http-architecture.md` | Generic HTTP POST architecture patterns |
