# Health Complaints Management Specification

## Overview

Complaint management for healthcare organizations including patient/family complaint triage, service recovery, and response drafting. Ensures timely, compassionate, and compliant resolution of concerns.

## Scope

### Complaint Types
- Clinical care concerns
- Communication issues
- Wait times and access
- Billing disputes
- Privacy breaches
- Visitor/staff interactions

### Workflows
- Initial complaint intake and triage
- Investigation and fact-finding
- Service recovery actions
- Response letter drafting
- Resolution tracking
- Trend analysis

### Stakeholders
- Patients and families
- Patient advocacy/relations
- Clinical staff
- Quality/safety teams
- Executive leadership
- External regulators (when required)

## Deliverables

### Skills
- `complaint-analysis` - Triage and categorize complaints
- `response-drafting` - Draft complaint responses

### Commands
- `/submit-complaint` - Initiate complaint workflow

## Dependencies

- `health-core` (plugin structure)
- `health-governance` (for policy alignment)

## Adapts From

- `customer-support/ticket-triage` - Triage patterns
- `customer-support/canned-responses` - Response templates

## Success Criteria

- [ ] Guides complaint categorization by severity/type
- [ ] Provides response templates by complaint category
- [ ] Tracks resolution timeframes
- [ ] Identifies systemic issues for QI
- [ ] Maintains regulatory compliance

## Regulatory Context

### Australia
- Australian Charter of Healthcare Rights
- State/Territory complaint handling legislation
- Aged Care Quality Standards (if applicable)

### New Zealand
- Health and Disability Commission Code
- Code of Health and Disability Services Consumers' Rights

### Escalation Thresholds
- Serious clinical harm
- Media involvement
- Legal action threatened
- Regulatory body contact
