# Persistence: The .telemetry/ Folder

Product tracking produces artifacts that must persist across sessions, engineers, and time. The `.telemetry/` folder in your repository is the canonical location for these artifacts.

## Folder Structure

```
.telemetry/
├── README.md               # Explains this folder's purpose (Phase 1)
├── product.md              # Product description — STATIC (Phase 1)
├── current-state.yaml      # Reverse-engineered tracking from codebase (Phase 2)
├── tracking-plan.yaml      # The canonical target tracking plan (Phase 3)
├── delta.md                # Diff: current state → target plan (Phase 3+)
├── instrument.md           # SDK-specific instrumentation guide (Phase 4)
├── changelog.md            # History of tracking plan changes (Phase 6)
├── audits/                 # Timestamped audit snapshots (Phase 2)
│   ├── 2026-01-15.md
│   ├── gap-analysis-2026-02-08.md
│   └── ...
```

## File Purposes — Keep Them Clean

### product.md — STATIC PRODUCT DESCRIPTION

**Purpose:** Captures what the product is, who uses it, and where value lives.

**Contains:**
- Product identity and one-liner
- Category classification
- Core value actions (ranked)
- Entity model (users, accounts, objects)
- Trait schemas
- Integration targets

**Does NOT contain:**
- Audit results or statistics
- Event counts or coverage percentages
- Working notes or progress
- Any output from Phase 2 (audit) or later

**When updated:**
- Initial discovery (Phase 1-2)
- Product pivot or major change (replay Phase 1-2)
- **Never updated during audits or routine maintenance**

### tracking-plan.yaml — THE PLAN

**Purpose:** Single source of truth for what events should exist.

**Contains:**
- Event definitions with properties
- Entity/trait schemas
- Naming conventions
- SDK target

**Updated by:** the **product-tracking-design-tracking-plan** and **product-tracking-instrument-new-feature** skills

### current-state.yaml — REVERSE-ENGINEERED TRACKING

**Purpose:** Machine-readable inventory of what's actually tracked in the codebase today.

**Contains:**
- Every event found in code (name, properties, location, LIVE/ORPHANED status)
- Identity management calls (identify, group)
- Observed patterns (naming style, centralization, error handling)

**Created by:** the **product-tracking-audit-current-tracking** skill

### delta.md — IMPLEMENTATION BACKLOG

**Purpose:** Explicit diff from current state to target plan — what to add, remove, rename, change.

**Created by:** the **product-tracking-design-tracking-plan** skill (initial), updated by the **product-tracking-instrument-new-feature** skill

### instrument.md — SDK-SPECIFIC GUIDE

**Purpose:** How-to guide for making identify, group, and track calls with the target SDK. Template code, API endpoints, constraints.

**Contains:**
- SDK call signatures and template code
- Architecture guidance (initialization, routing, shutdown)
- "Current Implementation" section (appended by the **product-tracking-audit-current-tracking** skill if present)

**Created by:** the **product-tracking-generate-implementation-guide** skill, with "Current Implementation" section from the **product-tracking-audit-current-tracking** skill

### audits/*.md — AUDIT RESULTS

**Purpose:** Historical record of implementation state. Each audit is a snapshot.

**Contains:**
- Gap analysis (ideal vs. current)
- Missing events, orphaned events, malformed events
- Coverage percentages
- Prioritized fix list

**Example files:**
- `audits/2026-02-08.md` — standard audit
- `audits/gap-analysis-2026-02-08.md` — detailed gap analysis

**Key principle:** Audit output goes HERE, not in product.md.

## File Initialization

When starting work on a product without a `.telemetry/` folder:

```bash
mkdir -p .telemetry/audits
```

Then:
1. **product-tracking-model-product** skill → creates `README.md` + `product.md`
2. **product-tracking-audit-current-tracking** skill → creates `current-state.yaml` + `audits/YYYY-MM-DD.md`
3. **product-tracking-design-tracking-plan** skill → creates `tracking-plan.yaml` + `delta.md`
4. Commit to version control

## Git Best Practices

**Do commit:**
- `README.md`
- `product.md`
- `current-state.yaml`
- `tracking-plan.yaml`
- `delta.md`
- `instrument.md`
- `changelog.md`
- `audits/*.md`

**Commit messages:**
- `telemetry: initial product discovery`
- `telemetry: add Content Exported event (v1.2.0)`
- `telemetry: audit 2026-02-01 (78% coverage)`

## Why Documentation Matters

Maintaining thorough documentation of your data schema and tracking plan is not optional -- it is essential infrastructure. Documentation serves multiple purposes:

- **Onboarding:** New team members can understand what is tracked and why without reading code
- **Troubleshooting:** Issues can be diagnosed against a known reference rather than requiring reverse engineering
- **Consistency:** Documentation prevents data strategy from drifting away from business goals
- **Collaboration:** Product, engineering, and data teams share a common reference point

The `.telemetry/` folder is this documentation. Keep it accurate and up to date as the plan evolves. Every event addition, modification, or deprecation should be reflected in both the tracking plan and the changelog.

## Anti-Patterns

Do not write audit stats to product.md.
The product description should stay clean. Audit results go to `audits/`.

Do not update product.md during every session.
It is a static description, not a working document.

Do not mix ideal plan with current state.
`tracking-plan.yaml` is the ideal. `audits/*.md` documents current state. Keep them separate.

Do not let documentation go stale.
If the tracking plan changes but documentation does not, the documentation becomes misleading -- worse than no documentation at all. Treat documentation updates as part of every tracking plan change.
