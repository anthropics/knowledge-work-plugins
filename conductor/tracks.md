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
├── health-complaints ───────────────────────────────────┤
├── health-incidents ────────────────────────────────────┤
├── health-risk ─────────────────────────────────────────┤
├── health-information ──────────────────────────────────┤
└── health-coding ───────────────────────────────────────┤
                                                          │
PHASE 3: Extended Workflows (parallel)                    │
├── health-governance ───────────────────────────────────┤
├── health-credentialing ────────────────────────────────┤
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

## [ ] Track: health-governance - Policies, procedures
Folder: [./tracks/health-governance/](./tracks/health-governance/)
Phase: 3
Adapts From: legal/compliance

---
## [ ] Track: health-credentialing - Provider credentialing
Folder: [./tracks/health-credentialing/](./tracks/health-credentialing/)
Phase: 3
Adapts From: productivity/memory-management

---
## [ ] Track: health-procurement - Devices, business cases
Folder: [./tracks/health-procurement/](./tracks/health-procurement/)
Phase: 3
Adapts From: legal/contract-review

---
## [ ] Track: health-quality - QI, accreditation
Folder: [./tracks/health-quality/](./tracks/health-quality/)
Phase: 3
Adapts From: product-management

---
## [ ] Track: health-financial - Payer contracts
Folder: [./tracks/health-financial/](./tracks/health-financial/)
Phase: 3
Adapts From: finance

---
## [ ] Track: health-evidence - Systematic reviews
Folder: [./tracks/health-evidence/](./tracks/health-evidence/)
Phase: 3
Adapts From: bio-research

---
## [ ] Track: health-data-analysis - Epidemiological reports
Folder: [./tracks/health-data-analysis/](./tracks/health-data-analysis/)
Phase: 3
Adapts From: data

---
## [ ] Track: health-public-health - Notifiable disease reporting and surveillance
Folder: [./tracks/health-public-health/](./tracks/health-public-health/)
Phase: 3
Adapts From: legal/compliance

---
## [ ] Track: health-ethics - Research/clinical ethics
Folder: [./tracks/health-ethics/](./tracks/health-ethics/)
Phase: 4
Adapts From: bio-research

---
## [ ] Track: health-economics - HTA, cost-effectiveness
Folder: [./tracks/health-economics/](./tracks/health-economics/)
Phase: 4
Adapts From: data, finance

---
## [ ] Track: health-manuscripts - Journal preparation
Folder: [./tracks/health-manuscripts/](./tracks/health-manuscripts/)
Phase: 4
Adapts From: bio-research

---
## [ ] Track: health-doc-coauthoring - Three-stage collaborative clinical document development
Folder: [./tracks/health-doc-coauthoring/](./tracks/health-doc-coauthoring/)
Phase: 4
Adapts From: document-skills/docx

---
## [ ] Track: health-grants - Grant applications
Folder: [./tracks/health-grants/](./tracks/health-grants/)
Phase: 4
Adapts From: bio-research

---
## [ ] Track: health-medicolegal - Child protection, affidavits, medico-legal
Folder: [./tracks/health-medicolegal/](./tracks/health-medicolegal/)
Phase: 4
Adapts From: legal

---
## [ ] Track: skill-quality - Quality standards for health plugin skills (30 skills)
Folder: [./tracks/skill-quality/](./tracks/skill-quality/)
Phase: Infrastructure
Adapts From: health-core

### Summary

- **20 tracks** total (1 meta + 18 implementation + 1 infrastructure)
- **33 planned skills** across all tracks
- **16 planned commands** for key workflows
- **2 implemented skills** in `health/skills/` currently
- **2 implemented commands** in `health/commands/` currently
- **4 execution phases** plus an infrastructure track

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
