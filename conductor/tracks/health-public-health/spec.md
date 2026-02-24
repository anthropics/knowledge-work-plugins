# Health Public Health Track Specification

## Overview

Public health reporting workflows including notifiable disease reporting, surveillance notifications, and outbreak response coordination.

## Scope

### Notifiable Diseases
- Mandatory reporting requirements by jurisdiction
- Notification timelines (immediate vs. routine)
- Case definition criteria
- Laboratory confirmation requirements
- Contact tracing documentation

### Surveillance
- Population health monitoring
- Outbreak detection and response
- Epidemiological reporting
- Trend analysis

### Jurisdiction-Specific Requirements

**Australia**
- State/territory public health acts
- National Notifiable Diseases Surveillance System (NNDSS)
- CDNA surveillance guidelines

**New Zealand**
- Health Act 1956
- Notifiable Diseases Order
- ESR surveillance

### US/EU-lite Variant
- Provide lightweight US and EU adaptation notes only when explicitly requested.
- Keep AU/NZ as the default baseline.

## Deliverables

### Skills
- `notifiable-diseases` - Disease notification workflow
- `public-health-surveillance` - Surveillance and outbreak response

### Commands
- `/report-notifiable` - Initiate notifiable disease report

## Dependencies

- `health-core` (plugin structure)
- `health-coding` (ICD-10 coding for diseases)
- `health-data-analysis` (epidemiological analysis)

## Adapts From

- `legal/compliance` - Regulatory requirements

## Success Criteria

- [ ] Identifies notifiable disease triggers
- [ ] Guides notification by jurisdiction
- [ ] Documents case definitions
- [ ] Supports outbreak response coordination
- [ ] Tracks notification timelines
