# Health Plugin

Healthcare organization workflows for compliance, quality, and clinical operations.

## Overview

This plugin provides specialized skills and commands for healthcare professionals working in:

- Complaints management
- Incident reporting
- Risk management
- Information governance
- Clinical coding
- Governance and policy
- Credentialing
- Procurement
- Quality improvement
- Financial operations
- Evidence review
- Data analysis
- Ethics
- Health economics
- Manuscript preparation
- Document co-authoring
- Grants
- Medicolegal
- Public health reporting and surveillance

## Jurisdiction Profile

- Default: Australia and New Zealand
- Portable variants: US/EU-lite when explicitly requested

## Installation

```bash
claude plugin install ./health
```

## Available Skills

Skills are organized by domain and will be added by individual track implementations.

| Domain | Skills | Status |
|--------|--------|--------|
| complaints | complaint-analysis, response-drafting | Planned |
| incidents | root-cause-analysis, cap-writing | Planned |
| risk | clinical-risk-assessment, worker-risk-assessment, enterprise-risk-assessment | Planned |
| information-governance | release-of-information, consent-management | Planned |
| coding | clinical-coding | Planned |
| governance | policy-development, procedure-development, guideline-development | Planned |
| credentialing | credentialing, privileging | Planned |
| procurement | device-procurement, business-case | Planned |
| quality | quality-improvement, accreditation-prep | Planned |
| financial | payer-contracts, charge-capture | Planned |
| evidence | systematic-review, evidence-synthesis | Planned |
| data-analysis | health-data-report | Planned |
| ethics | research-ethics, clinical-ethics | Planned |
| health-economics | health-econ-eval, hta-submission | Planned |
| manuscripts | manuscript-prep | Planned |
| document-coauthoring | clinical-doc-coauthoring | Planned |
| grants | grant-writer | Planned |
| medicolegal | child-protection, affidavits, medicolegal-reports | Planned |
| public-health | notifiable-diseases, public-health-surveillance | Planned |

## Implementation Status

- Planned tracks: 20 implementation tracks plus 1 infrastructure track
- Implemented skills: 2 (`complaints-management`, `incident-reporting`)
- Implemented commands: 2 (`submit-complaint`, `report-incident`)

## Configuration

### Connectors

See [CONNECTORS.md](./CONNECTORS.md) for connector setup instructions.

### Customization

Configure your organization's connectors in `.mcp.json`. Enable the connectors you need and set the required environment variables.

## Dependencies

- Claude Code >= 0.1.0
- Appropriate MCP connectors for your organization's tools

## License

MIT
