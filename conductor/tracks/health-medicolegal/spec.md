# Health Medicolegal Track Specification

## Overview

Medicolegal documentation workflows supporting child protection reporting, court documentation, expert witness statements, and statutory reporting obligations.

## Scope

### Document Types

| Type | Description | Regulatory Context |
|------|-------------|-------------------|
| **Child protection reports** | Mandatory reporting, risk assessments | State/territory child protection legislation |
| **Affidavits** | Court documentation, sworn statements | Court rules, evidence law |
| **Medico-legal reports** | Independent medical examinations, personal injury | Civil procedure rules |
| **Coroner's reports** | Reportable deaths, death certificates | Coroner's Act |
| **Workers compensation** | Work capacity, impairment assessments | Workers compensation legislation |
| **Capacity assessments** | Decision-making capacity, guardianship | Guardianship legislation |

### Workflow Elements

- Document structure requirements
- Legal admissibility considerations
- Confidentiality and privilege
- Mandatory reporting triggers
- Court formatting requirements
- Service and filing procedures

## Deliverables

### Skills
- `medicolegal-reports` - General medico-legal report structure
- `child-protection` - Child protection reporting workflow
- `affidavit-drafting` - Affidavit preparation and formatting

### Commands
- `/prepare-report` - Initiate medicolegal document

## Dependencies

- `health-core` (plugin structure)

## Adapts From

- `legal/canned-responses` - Template patterns
- `legal/contract-review` - Document review methodology

## Jurisdiction Considerations

Medicolegal requirements vary significantly by jurisdiction:
- Australian states/territories
- New Zealand
- Different court jurisdictions (Federal, State, Family)

Skills should parameterize by jurisdiction where requirements differ.

## Success Criteria

- [ ] Guides child protection report preparation
- [ ] Supports affidavit drafting with proper formatting
- [ ] Identifies mandatory reporting triggers
- [ ] Documents legal requirements by type
- [ ] Maintains appropriate tone and structure
