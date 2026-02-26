# Health Economics Track Specification

## Overview

Health economic evaluation workflows including cost-effectiveness analysis, cost-utility analysis, HTA submissions, and multi-perspective evaluations (PBAC, MSAC, NICE, CADTH).

## Scope

### Economic Evaluation Types
- Cost-effectiveness analysis (CEA)
- Cost-utility analysis (CUA)
- Cost-benefit analysis (CBA)
- Budget impact analysis (BIA)

### HTA Submissions
- PBAC (Australia - Pharmaceutical Benefits)
- MSAC (Australia - Medical Services)
- NICE (UK)
- CADTH (Canada)
- PHARMAC (NZ)

### Decision Modeling
- Decision tree models
- Markov models
- Microsimulation
- Sensitivity analyses (deterministic, probabilistic)

## Deliverables

### Skills
- `health-econ-eval` - Economic evaluation methodology
- `hta-submission` - HTA submission preparation

### Commands
- `/economic-evaluation` - Initiate economic evaluation

## Dependencies

- `health-core` (plugin structure)
- `health-evidence` (for clinical effectiveness inputs)

## Adapts From

- `data/statistical-analysis` - Analytical methods
- `finance/financial-statements` - Reporting structure

## Frameworks

- PBAC Guidelines (Australia)
- MSAC Guidelines (Australia)
- NICE Reference Case (UK)
- CADTH Guidelines (Canada)

## Success Criteria

- [ ] Guides economic evaluation by type
- [ ] Supports HTA submission preparation
- [ ] Includes decision modeling frameworks
- [ ] Provides sensitivity analysis guidance
- [ ] Encodes reference case requirements
