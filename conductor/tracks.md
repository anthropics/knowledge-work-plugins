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
└── health-data-analysis ────────────────────────────────┤
                                                          │
PHASE 4: Research/Academic (parallel, depends Phase 3)    │
├── health-ethics ───────────────────────────────────────┤
├── health-economics ────────────────────────────────────┤
├── health-manuscripts ──────────────────────────────────┤
├── health-grants ───────────────────────────────────────┤
└── health-medicolegal ──────────────────────────────────┘
```

### Track Registry

| Track | Description | Phase | Adapts From |
|-------|-------------|-------|-------------|
| [health-core](./tracks/health-core/) | Plugin foundation | 1 | - |
| [health-complaints](./tracks/health-complaints/) | Patient complaints | 2 | customer-support/ticket-triage |
| [health-incidents](./tracks/health-incidents/) | Serious adverse events | 2 | customer-support/escalation |
| [health-risk](./tracks/health-risk/) | Multi-domain risk | 2 | legal/legal-risk-assessment |
| [health-information](./tracks/health-information/) | ROI, consent, records | 2 | legal/compliance |
| [health-coding](./tracks/health-coding/) | Clinical coding | 2 | data/data-validation |
| [health-governance](./tracks/health-governance/) | Policies, procedures | 3 | legal/compliance |
| [health-credentialing](./tracks/health-credentialing/) | Provider credentialing | 3 | productivity/memory-management |
| [health-procurement](./tracks/health-procurement/) | Devices, business cases | 3 | legal/contract-review |
| [health-quality](./tracks/health-quality/) | QI, accreditation | 3 | product-management |
| [health-financial](./tracks/health-financial/) | Payer contracts | 3 | finance |
| [health-evidence](./tracks/health-evidence/) | Systematic reviews | 3 | bio-research |
| [health-data-analysis](./tracks/health-data-analysis/) | Epidemiological reports | 3 | data |
| [health-ethics](./tracks/health-ethics/) | Research/clinical ethics | 4 | bio-research |
| [health-economics](./tracks/health-economics/) | HTA, cost-effectiveness | 4 | data, finance |
| [health-manuscripts](./tracks/health-manuscripts/) | Journal preparation | 4 | bio-research |
| [health-grants](./tracks/health-grants/) | Grant applications | 4 | bio-research |
| [health-medicolegal](./tracks/health-medicolegal/) | Child protection, affidavits, medico-legal | 4 | legal |

### Summary

- **18 tracks** total (1 meta + 17 implementation)
- **30 skills** across all tracks
- **14 commands** for key workflows
- **4 phases** of execution

## Track Status

- `planning` - Specification in progress
- `active` - Implementation underway
- `paused` - Temporarily halted
- `complete` - Finished and verified
