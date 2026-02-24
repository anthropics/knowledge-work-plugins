# Health Financial Track Specification

## Overview

Charge capture review, payer contract management, grant management, and revenue cycle support.

## Scope

### Payer Contracts
- Contract review (healthcare-specific terms)
- Rate analysis
- Renewal tracking
- Negotiation support

### Charge Capture
- Charge description master (CDM) review
- Coding validation
- Charge reconciliation
- Compliance monitoring

### Grant Management
- Grant application support
- Budget tracking
- Reporting requirements
- Closeout procedures

### Revenue Cycle
- Denial management
- Appeals process
- AR follow-up

## Deliverables

### Skills
- `payer-contracts` - Healthcare payer contract review and management
- `charge-capture` - Charge capture review and validation

### Commands
- `/review-payer-contract` - Payer contract analysis

## Dependencies

- `health-core` (plugin structure)

## Adapts From

- `legal/contract-review` - Contract analysis methodology
- `finance/reconciliation` - Reconciliation workflows
- `finance/audit-support` - Payer audit preparation

## Success Criteria

- [ ] Reviews payer contracts for healthcare-specific terms
- [ ] Supports charge capture validation
- [ ] Tracks contract renewal timelines
- [ ] Guides denial appeal process
