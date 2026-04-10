# .telemetry/

This folder contains product telemetry artifacts — structured descriptions of what the product tracks, why, and how. It was created by **Product Tracking Skills**.

## What's in here

| File | Purpose | Created by |
|------|---------|------------|
| `README.md` | This file | **product-tracking-model-product** skill |
| `business-case.md` | Why add telemetry — stakeholder-ready business case | **product-tracking-business-case** skill |
| `product.md` | Product description — what it does, who uses it, how value flows | **product-tracking-model-product** skill |
| `current-state.yaml` | Reverse-engineered tracking from the codebase | **product-tracking-audit-current-tracking** skill |
| `tracking-plan.yaml` | Target tracking plan — what should be tracked | **product-tracking-design-tracking-plan** skill |
| `delta.md` | Diff from current state to target plan | **product-tracking-design-tracking-plan** skill |
| `instrument.md` | SDK-specific instrumentation guide | **product-tracking-generate-implementation-guide** skill |
| `changelog.md` | History of tracking plan changes | **product-tracking-instrument-new-feature** skill |
| `audits/` | Timestamped audit snapshots | **product-tracking-audit-current-tracking** skill |

## Workflow

These artifacts follow a seven-skill lifecycle:

```
product-tracking-business-case → product-tracking-model-product → product-tracking-audit-current-tracking → product-tracking-design-tracking-plan → product-tracking-generate-implementation-guide → product-tracking-implement-tracking ← product-tracking-instrument-new-feature
```

Each phase reads upstream artifacts and produces its own. Phases can be replayed as the product evolves.

## Version control

**Commit** everything in this folder except `.session-log.json` (ephemeral session data — add to `.gitignore`).

## Source

Product Tracking Skills — by Accoil.
https://github.com/accoil/product-tracking-skills
