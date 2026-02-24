# Health Procurement Specification

## Overview

Healthcare procurement workflows including medical device procurement, value analysis, business case development, and capital equipment planning. Ensures cost-effective, clinically appropriate acquisitions.

## Scope

### Procurement Types
- Medical devices and equipment
- Capital equipment
- Consumables and supplies
- IT systems and software
- Services and contracts

### Value Analysis
- Clinical evidence review
- Cost-effectiveness analysis
- Total cost of ownership
- Safety and risk assessment
- Supplier evaluation

### Business Case Development
- Needs assessment
- Options analysis
- Financial modeling
- Implementation planning
- Risk assessment
- Benefits realization

### Contract Management
- Specification development
- Tender/RFQ processes
- Contract negotiation
- Vendor management
- Performance monitoring

## Deliverables

### Skills
- `device-procurement` - Medical device acquisition
- `business-case` - Business case development

### Commands
- `/procurement-request` - Initiate procurement
- `/business-case` - Create business case

## Dependencies

- `health-core` (plugin structure)
- `health-governance` (for policy alignment)
- `health-economics` (for value analysis)

## Adapts From

- `legal/contract-review` - Contract frameworks
- `finance/financial-statements` - Financial analysis

## Success Criteria

- [ ] Documents clinical need and evidence
- [ ] Evaluates multiple options
- [ ] Analyzes total cost of ownership
- [ ] Assesses safety and compliance
- [ ] Develops robust business cases
- [ ] Manages vendor relationships

## Regulatory Context

### Standards
- TGA (AU) / Medsafe (NZ) device registration
- ISO 13485 (Quality Management)
- ISO 14971 (Risk Management)

### Australia
- Therapeutic Goods Act
- ARTG inclusion requirements
- State/Territory procurement policies
- National Health Reform Agreement

### New Zealand
- Medicines Act
- WAND (Web-Assisted Notification of Devices)
- DHB Shared Services procurement
- Government Procurement Rules

### Approval Thresholds
- Delegated authority limits vary by organization
- Board approval typically required for >$1M capital
- Clinical governance sign-off required for clinical equipment
