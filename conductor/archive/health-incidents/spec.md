# Health Incidents Track Specification

## Overview

Serious adverse events (SAEs) and incident reporting, investigation, and escalation workflows. Distinct from complaints - these are safety events that may or may not involve patient/family complaints.

## Scope

### Incident Types
- Patient safety incidents
- Near misses
- Sentinel events
- Adverse drug reactions
- Device-related incidents
- Healthcare-associated infections

### Key Workflows

1. **Detection** - Identification and immediate reporting
2. **Classification** - Severity (SAC 1-4 or equivalent)
3. **Investigation** - Root cause analysis, RCA methodology
4. **Reporting** - Regulatory notifications, internal escalations
5. **Prevention** - Action items, system improvements

### Regulatory Context
- Mandatory reporting requirements
- Sentinel event protocols
- Quality improvement protections

## Deliverables

### Skills
- `incident-reporting` - Incident detection, classification, investigation workflow

### Commands
- `/report-incident` - Incident intake and routing

## Dependencies

- `health-core` (plugin structure)

## Success Criteria

- [ ] Classifies incident severity appropriately
- [ ] Identifies mandatory reporting triggers
- [ ] Supports RCA methodology
- [ ] Links to quality improvement tracking
- [ ] Maintains privilege protections where applicable
