# Health Information Governance Specification

## Overview

Health information governance including release of information (ROI), consent management, privacy compliance, and records management. Ensures compliant handling of patient health information.

## Scope

### Release of Information
- Third-party requests
- Patient access requests
- Legal/judicial requests
- Research access
- Insurance requests

### Consent Management
- Treatment consent
- Procedure-specific consent
- Research consent
- Release of information consent
- Withdrawal of consent

### Privacy Compliance
- Privacy Act (AU) / Privacy Act (NZ) compliance
- APP/IPP compliance
- Data breach response
- Privacy impact assessments

### Records Management
- Retention schedules
- Destruction protocols
- Archive management
- Legal hold procedures

## Deliverables

### Skills
- `release-of-information` - Process ROI requests
- `consent-management` - Handle consent workflows

### Commands
- `/process-roi` - Initiate ROI workflow

## Dependencies

- `health-core` (plugin structure)
- `health-governance` (for policy alignment)

## Adapts From

- `legal/compliance` - Compliance frameworks
- `document-skills/docx` - Document processing

## Success Criteria

- [ ] Validates authorization for information release
- [ ] Applies correct consent standards
- [ ] Maintains audit trails
- [ ] Ensures timely response to requests
- [ ] Protects against unauthorized disclosure
- [ ] Handles data breaches appropriately

## Regulatory Context

### Australia
- Privacy Act 1988 (Cth)
- Australian Privacy Principles (APPs)
- State/Territory health records legislation
- My Health Records Act

### New Zealand
- Privacy Act 2020
- Health Information Privacy Code
- Health (Retention of Health Information) Regulations

### Timeframes
- Patient access: 30 days (AU), 20 working days (NZ)
- Data breach notification: As soon as practicable
- Records retention: Minimum 7 years (adult), until age 25 (children)
