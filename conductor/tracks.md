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

- [~] **Track: health-complaints** (./tracks/health-complaints/)
  - Description: Patient complaints
  - Phase: 2
  - Adapts From: customer-support/ticket-triage
- [ ] **Track: health-incidents** (./tracks/health-incidents/)
  - Description: Serious adverse events
  - Phase: 2
  - Adapts From: customer-support/escalation
- [ ] **Track: health-risk** (./tracks/health-risk/)
  - Description: Multi-domain risk
  - Phase: 2
  - Adapts From: legal/legal-risk-assessment
- [ ] **Track: health-information** (./tracks/health-information/)
  - Description: ROI, consent, records
  - Phase: 2
  - Adapts From: legal/compliance
- [ ] **Track: health-coding** (./tracks/health-coding/)
  - Description: Clinical coding
  - Phase: 2
  - Adapts From: data/data-validation
- [ ] **Track: health-governance** (./tracks/health-governance/)
  - Description: Policies, procedures
  - Phase: 3
  - Adapts From: legal/compliance
- [ ] **Track: health-credentialing** (./tracks/health-credentialing/)
  - Description: Provider credentialing
  - Phase: 3
  - Adapts From: productivity/memory-management
- [ ] **Track: health-procurement** (./tracks/health-procurement/)
  - Description: Devices, business cases
  - Phase: 3
  - Adapts From: legal/contract-review
- [ ] **Track: health-quality** (./tracks/health-quality/)
  - Description: QI, accreditation
  - Phase: 3
  - Adapts From: product-management
- [ ] **Track: health-financial** (./tracks/health-financial/)
  - Description: Payer contracts
  - Phase: 3
  - Adapts From: finance
- [ ] **Track: health-evidence** (./tracks/health-evidence/)
  - Description: Systematic reviews
  - Phase: 3
  - Adapts From: bio-research
- [ ] **Track: health-data-analysis** (./tracks/health-data-analysis/)
  - Description: Epidemiological reports
  - Phase: 3
  - Adapts From: data
- [ ] **Track: health-public-health** (./tracks/health-public-health/)
  - Description: Notifiable disease reporting and surveillance
  - Phase: 3
  - Adapts From: legal/compliance
- [ ] **Track: health-ethics** (./tracks/health-ethics/)
  - Description: Research/clinical ethics
  - Phase: 4
  - Adapts From: bio-research
- [ ] **Track: health-economics** (./tracks/health-economics/)
  - Description: HTA, cost-effectiveness
  - Phase: 4
  - Adapts From: data, finance
- [ ] **Track: health-manuscripts** (./tracks/health-manuscripts/)
  - Description: Journal preparation
  - Phase: 4
  - Adapts From: bio-research
- [ ] **Track: health-doc-coauthoring** (./tracks/health-doc-coauthoring/)
  - Description: Three-stage collaborative clinical document development
  - Phase: 4
  - Adapts From: document-skills/docx
- [ ] **Track: health-grants** (./tracks/health-grants/)
  - Description: Grant applications
  - Phase: 4
  - Adapts From: bio-research
- [ ] **Track: health-medicolegal** (./tracks/health-medicolegal/)
  - Description: Child protection, affidavits, medico-legal
  - Phase: 4
  - Adapts From: legal
- [ ] **Track: skill-quality** (./tracks/skill-quality/)
  - Description: Quality standards for health plugin skills (30 skills)
  - Phase: Infrastructure
  - Adapts From: health-core

### Summary

- **21 tracks** total (1 meta + 19 implementation + 1 infrastructure)
- **33 planned skills** across all tracks
- **16 planned commands** for key workflows
- **0 implemented skills** in `health/skills/` currently
- **0 implemented commands** in `health/commands/` currently
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
