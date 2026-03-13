# Health Risk Management Specification

## Overview

Comprehensive risk management for healthcare organizations including clinical risk, worker health and safety, and enterprise risk. Supports proactive identification, assessment, and mitigation of risks.

## Scope

### Risk Categories

**Clinical Risk**
- Patient safety hazards
- Clinical procedure risks
- Medication safety
- Infection control risks
- Diagnostic errors

**Worker Risk**
- Occupational violence
- Manual handling
- Sharps injuries
- Psychosocial hazards
- Exposure to hazardous substances

**Enterprise Risk**
- Financial risks
- Operational risks
- Strategic risks
- Compliance/regulatory risks
- Reputational risks

### Risk Management Process
1. Risk identification
2. Risk assessment (likelihood x consequence)
3. Risk evaluation and prioritization
4. Risk treatment (mitigation, transfer, acceptance)
5. Monitoring and review

## Deliverables

### Skills
- `clinical-risk` - Clinical risk assessment
- `worker-risk` - Worker safety risk assessment
- `enterprise-risk` - Enterprise risk management

### Commands
- `/assess-risk` - Initiate risk assessment

## Dependencies

- `health-core` (plugin structure)
- `health-incidents` (for incident linkage)
- `health-quality` (for QI alignment)

## Adapts From

- `legal/legal-risk-assessment` - Risk assessment frameworks
- `finance/financial-statements` - Financial risk analysis

## Success Criteria

- [ ] Identifies risks across all categories
- [ ] Assesses risks using standardized matrices
- [ ] Prioritizes risks by severity
- [ ] Develops treatment plans
- [ ] Links risks to incidents and QI
- [ ] Maintains risk register

## Regulatory Context

### Risk Matrix Standards
- Likelihood: Rare, Unlikely, Possible, Likely, Almost Certain
- Consequence: Insignificant, Minor, Moderate, Major, Catastrophic

### Australia
- Work Health and Safety Act
- NSQHS Standards
- Enterprise Risk Management Frameworks

### New Zealand
- Health and Safety at Work Act
- Health and Disability Services Standards
