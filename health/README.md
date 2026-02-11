# Health Plugin

Healthcare organization workflows for compliance, quality, and clinical operations.

## Overview

This plugin provides specialized skills and commands for healthcare professionals working in:

- **Complaints Management** - Patient complaint handling and resolution
- **Incident Reporting** - Serious adverse event documentation and investigation
- **Risk Management** - Multi-domain risk assessment and mitigation
- **Information Governance** - ROI, consent management, records handling
- **Clinical Coding** - Medical coding validation and auditing
- **Governance** - Policy and procedure management
- **Credentialing** - Provider credential verification
- **Procurement** - Medical device evaluation and business cases
- **Quality Improvement** - QI projects and accreditation support
- **Financial Operations** - Payer contract analysis
- **Evidence Review** - Systematic reviews and evidence synthesis
- **Data Analysis** - Epidemiological reporting
- **Ethics** - Research and clinical ethics consultation
- **Health Economics** - HTA and cost-effectiveness analysis
- **Manuscript Preparation** - Journal article formatting
- **Grants** - Research grant applications
- **Medicolegal** - Child protection, affidavits, medico-legal reports

## Installation

```bash
claude plugin install ./health
```

## Available Skills

Skills are organized by domain and will be added by individual track implementations:

| Domain | Skills | Status |
|--------|--------|--------|
| complaints | complaint-analysis, response-drafting | Planned |
| incidents | root-cause-analysis, cap-writing | Planned |
| risk | risk-assessment, mitigation-planning | Planned |
| governance | policy-review, procedure-writing | Planned |
| ethics | ethics-consultation, irb-preparation | Planned |
| compliance | audit-preparation, gap-analysis | Planned |
| procurement | device-evaluation, business-case | Planned |

## Configuration

### Connectors

See [CONNECTORS.md](./CONNECTORS.md) for connector setup instructions.

### Customization

Configure your organization's connectors in the `.mcp.json` file. Enable the connectors you need and set the appropriate environment variables.

## Dependencies

- Claude Code >= 0.1.0
- Appropriate MCP connectors for your organization's tools

## License

MIT
