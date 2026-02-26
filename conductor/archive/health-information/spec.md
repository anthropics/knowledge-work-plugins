# Health Information Management Track Specification

## Overview

Release of information (ROI), consent management, medical records retention, and privacy compliance.

## Scope

### Release of Information (ROI)
- Authorization validation
- Request processing workflow
- Minimum necessary standard
- Accounting of disclosures

### Consent Management
- Treatment consent
- Research consent
- Advance directives
- Proxy/representative documentation

### Records Management
- Retention schedules
- Destruction protocols
- Legal hold management
- Format requirements

### Privacy
- Breach assessment
- Patient rights requests
- Notice of privacy practices

## Deliverables

### Skills
- `release-of-information` - ROI processing workflow
- `consent-management` - Consent types and documentation

### Commands
- `/process-roi` - Process release of information request

## Dependencies

- `health-core` (plugin structure)

## Adapts From

- `legal/compliance` - Privacy regulations
- `customer-support/response-drafting` - Patient communications

## Success Criteria

- [ ] Validates authorization requirements
- [ ] Guides ROI processing with minimum necessary
- [ ] Tracks consent documentation
- [ ] Applies retention schedules correctly
