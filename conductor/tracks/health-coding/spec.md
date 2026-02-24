# Health Clinical Coding Track Specification

## Overview

Clinical coding and classification support including ICD-10, ICD-11, SNOMED-CT, ACHI mapping, and coding validation for research datasets and clinical documentation.

## Scope

### Classification Systems
- **ICD-10-AM** (Australian Modification)
- **ICD-11** (WHO)
- **SNOMED-CT** (Clinical terminology)
- **ACHI** (Australian Classification of Health Interventions)
- **DRG** (Diagnosis Related Groups)

### Use Cases
- Research dataset coding
- Clinical documentation improvement
- Classification mapping/conversion
- Coding audit support
- Population health data

### Workflow
- Code lookup and selection
- Multi-system mapping
- Validation checking
- Documentation requirements
- Common errors avoidance

## Deliverables

### Skills
- `clinical-coding` - Clinical coding guidance and validation

### Commands
- `/validate-coding` - Validate coding accuracy

## Dependencies

- `health-core` (plugin structure)

## Adapts From

- `data/data-validation` - Validation patterns

## MCP Connectors

- ICD-10 Codes MCP (existing)
- SNOMED CT Browser (potential)

## Success Criteria

- [ ] Supports ICD-10-AM coding
- [ ] Provides classification mapping guidance
- [ ] Validates code selection
- [ ] Documents coding rationale
- [ ] Identifies common coding errors
