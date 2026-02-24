# Health Incident Management Specification

## Overview

Clinical incident reporting and management including near-misses, adverse events, root cause analysis, and corrective action planning. Supports patient safety and continuous improvement.

## Scope

### Incident Types
- Clinical incidents (medication, procedure, diagnostic)
- Falls and injuries
- Infection control breaches
- Equipment failures
- Documentation errors
- Near-miss events

### Severity Classification
- Catastrophic/Sentinel events
- Major incidents
- Moderate incidents
- Minor incidents
- Near misses

### Workflows
- Immediate response and containment
- Incident reporting
- Root cause analysis (RCA)
- Corrective action planning (CAP)
- Implementation and monitoring
- Trend analysis and reporting

## Deliverables

### Skills
- `incident-reporting` - Complete incident reports
- `root-cause-analysis` - Conduct RCAs
- `cap-writing` - Draft corrective action plans

### Commands
- `/report-incident` - Initiate incident workflow

## Dependencies

- `health-core` (plugin structure)
- `health-quality` (for QI integration)
- `health-governance` (for policy alignment)

## Adapts From

- `customer-support/escalation` - Escalation patterns
- `product-management/roadmap-management` - Action planning

## Success Criteria

- [ ] Captures all required incident details
- [ ] Classifies severity correctly
- [ ] Guides RCA methodology (5 Whys, Fishbone, etc.)
- [ ] Develops SMART corrective actions
- [ ] Tracks CAP implementation
- [ ] Identifies trends for prevention

## Regulatory Context

### Australia
- NSQHS Standard 1: Governance
- State/Territory incident reporting requirements
- AHPRA notification requirements
- Aged Care Serious Incident Reporting

### New Zealand
- Health and Disability Services Standards
- Serious and Sentinel Events reporting (HQSC)

### Timeframes
- Immediate: Patient safety actions
- 24-72 hours: Initial report
- 30 days: Full investigation (serious incidents)
- 60 days: Corrective action plan submission
