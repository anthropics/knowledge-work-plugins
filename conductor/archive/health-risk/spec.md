# Health Risk Assessment Track Specification

## Overview

Multi-domain risk assessment workflows for clinical risk, clinician and worker risk, enterprise risk, clinical services plan risk, and medicine standing orders risk.

## Scope

### Clinical Risk
- Patient safety event risk framing
- Severity and likelihood estimation
- Control selection and residual risk scoring

### Clinician and Worker Risk
- Workforce safety and occupational exposure risk
- Escalation criteria and immediate controls
- Documentation requirements

### Enterprise Risk
- Strategic and operational risk categorization
- Governance and accountability mapping
- Monitoring and review cadence

### Clinical Services Plan and Standing Orders Risk
- Service design risk checkpoints
- Standing orders risk controls and review triggers
- Regulatory and policy alignment checks

## Jurisdiction Defaults

- Default framing: Australia and New Zealand.
- Include US/EU-lite variant notes for portability when requested.

## Deliverables

### Skills
- `clinical-risk-assessment` - Clinical safety risk workflow
- `worker-risk-assessment` - Clinician and worker risk workflow
- `enterprise-risk-assessment` - Enterprise and governance risk workflow

### Commands
- `/assess-risk` - Structured risk assessment intake and recommendation flow

## Dependencies

- `health-core` (plugin structure)

## Adapts From

- `legal/legal-risk-assessment` - Risk taxonomy and control logic

## Success Criteria

- [ ] Supports consistent risk scoring across domains
- [ ] Captures controls and residual risk transparently
- [ ] Provides clear escalation and review triggers
- [ ] Produces auditable outputs for governance review
