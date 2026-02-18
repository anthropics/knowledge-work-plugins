# Health Credentialing and Privileging Specification

## Overview

Medical staff credentialing and privileging workflows including primary source verification, competency assessment, and ongoing professional practice evaluation (FPPE/OPPE).

## Scope

### Credentialing
- Application processing
- Primary source verification
- Education and training verification
- Work history verification
- References and recommendations
- Sanctions/ disciplinary history

### Privileging
- Scope of practice definition
- Privilege request evaluation
- Competency assessment
- Proctoring requirements
- Temporary privileges
- Emergency privileges

### Ongoing Monitoring
- FPPE (Focused Professional Practice Evaluation)
- OPPE (Ongoing Professional Practice Evaluation)
- Reappointment process
- Continuing education tracking
- Performance metrics review

## Deliverables

### Skills
- `credentialing` - Credential verification workflows
- `privileging` - Privilege request and evaluation

### Commands
- `/verify-credentials` - Check credential status

## Dependencies

- `health-core` (plugin structure)
- `health-governance` (for policy alignment)
- `health-quality` (for OPPE data)

## Adapts From

- `productivity/memory-management` - Tracking and reminders
- `legal/compliance` - Compliance verification

## Success Criteria

- [ ] Verifies all credentials from primary sources
- [ ] Documents verification evidence
- [ ] Evaluates privilege requests consistently
- [ ] Tracks expiration dates
- [ ] Manages proctoring requirements
- [ ] Supports reappointment workflows

## Regulatory Context

### Standards
- AHPRA (Australia) / MCNZ (NZ) registration requirements
- Professional indemnity insurance
- Continuing professional development
- Recency of practice

### Australia
- National Law (Health Practitioner Regulation)
- AHPRA registration standards
- State/Territory credentialing requirements

### New Zealand
- Health Practitioners Competence Assurance Act
- MCNZ registration requirements
- DHB credentialing standards

### Timeframes
- Initial credentialing: 60-90 days
- Reappointment: Every 2-3 years
- Temporary privileges: 120 days max
- FPPE: Initial 6 months
- OPPE: Ongoing, reviewed every 2 years
