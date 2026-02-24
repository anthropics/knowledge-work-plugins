# Health Credentialing Track Specification

## Overview

Provider credentialing, privileging, license verification, and clinical staff onboarding/offboarding workflows.

## Scope

### Credentialing
- Initial credentialing applications
- Primary source verification
- Background check coordination
- Credential committee preparation

### Privileging
- Delineation of privileges
- Competency verification
- Proctoring arrangements
- Privilege renewals

### License Management
- License tracking and expiration alerts
- DEA certification
- Board certifications
- Malpractice history

### Onboarding/Offboarding
- Orientation workflows
- Access provisioning
- Termination procedures

## Deliverables

### Skills
- `credentialing` - Credentialing workflow and verification
- `privileging` - Privilege delineation and management

### Commands
- `/verify-credentials` - Initiate credential verification

## Dependencies

- `health-core` (plugin structure)

## Adapts From

- `productivity/memory-management` - Tracking context and reminders

## Success Criteria

- [ ] Guides initial credentialing process
- [ ] Tracks verification requirements by provider type
- [ ] Supports privilege delineation
- [ ] Identifies re-credentialing timelines
