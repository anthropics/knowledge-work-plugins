# Tracks Registry

Active development tracks for this project.

## How to Create a Track

1. Create directory: `conductor/tracks/<track-id>/`
2. Add files: `spec.md`, `plan.md`, `metadata.json`
3. Register track below with link

## Health Plugin Program

Meta-track: [health-plugin](./tracks/health-plugin/) - Program overview and coordination

### Execution Phases

```
PHASE 1: Foundation
└── health-core ─────────────────────────────────────────┐
                                                           │
PHASE 2: Core Workflows (parallel)                        │
├── health-coding ───────────────────────────────────────┤
└── health-governance ───────────────────────────────────┤
                                                           │
PHASE 3: Extended Workflows (parallel)                    │
├── health-procurement ──────────────────────────────────┤
├── health-quality ──────────────────────────────────────┤
├── health-financial ────────────────────────────────────┤
├── health-evidence ─────────────────────────────────────┤
├── health-data-analysis ────────────────────────────────┤
└── health-public-health ────────────────────────────────┤
                                                           │
PHASE 4: Research/Academic (parallel, depends Phase 3)    │
├── health-ethics ───────────────────────────────────────┤
├── health-economics ────────────────────────────────────┤
├── health-manuscripts ──────────────────────────────────┤
├── health-doc-coauthoring ──────────────────────────────┤
├── health-grants ───────────────────────────────────────┤
└── health-medicolegal ──────────────────────────────────┘
```

### Track Registry (Canonical)

- [x] **Track: health-procurement** (./archive/health-procurement/)
  - Phase: 3
  - Adapts From: legal/contract-review

- [x] **Track: health-quality** (./tracks/health-quality/)
  - Phase: 3
  - Adapts From: product-management

- [x] **Track: health-financial** (./tracks/health-financial/)
  - Phase: 3
  - Adapts From: finance

- [ ] **Track: health-evidence** (./tracks/health-evidence/)
  - Phase: 3
  - Adapts From: bio-research

- [x] **Track: health-data-analysis** (./tracks/health-data-analysis/)
  - Phase: 3
  - Adapts From: data

- [x] **Track: health-public-health** (./tracks/health-public-health/)
  - Phase: 3
  - Adapts From: legal/compliance

- [x] **Track: health-ethics** (./tracks/health-ethics/)
  - Phase: 4
  - Adapts From: bio-research

- [x] **Track: health-economics** (./tracks/health-economics/)
  - Phase: 4
  - Adapts From: data, finance

- [x] **Track: health-manuscripts** (./tracks/health-manuscripts/)
  - Phase: 4
  - Adapts From: bio-research

- [x] **Track: health-doc-coauthoring** (./tracks/health-doc-coauthoring/)
  - Phase: 4
  - Adapts From: document-skills/docx

- [x] **Track: health-grants** (./tracks/health-grants/)
  - Phase: 4
  - Adapts From: bio-research

- [x] **Track: health-medicolegal** (./tracks/health-medicolegal/)
  - Phase: 4
  - Adapts From: legal

- [x] **Track: skill-quality** (./tracks/skill-quality/)
  - Phase: Infrastructure
  - Adapts From: health-core

### Summary

- **14 tracks** total (1 meta + 12 implementation + 1 infrastructure)
- **33+ skills** implemented across all tracks
- **16+ commands** implemented for key workflows
- **29+ skills** in `health/skills/` currently
- **12+ commands** in `health/commands/` currently
- **4 execution phases** plus an infrastructure track
- **All tracks complete** ✓

## Track Status

- `planning` - Specification in progress
- `active` - Implementation underway
- `paused` - Temporarily halted
- `complete` - Finished and verified

## Execution Discipline

- `active` tracks must have exactly one task marked `IN PROGRESS` (or `[~]`) in `plan.md`.
- Tasks should include `Owner:` and `Updated:` context at section level for accountability.
- Tracks with no `IN PROGRESS` task should remain `planning`.
- Explicit blockers should be marked with `BLOCKER:` or `BLOCKED:` so status tooling can detect them.

---

- [x] **Track: Establish a Strategic Equalizer plugin for Ministers and Ministerial staffers to audit and challenge bureaucratic advice.** (./tracks/ministerial-audit_20260214/)
