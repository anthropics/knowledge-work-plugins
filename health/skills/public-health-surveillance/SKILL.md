---
name: health/public-health-surveillance
description: This skill should be used when designing, implementing, or analyzing public health surveillance systems. Supports epidemiologists, public health officers, and healthcare administrators in outbreak detection, surveillance methodology, and population health monitoring.
version: 1.0.0
---

# Public Health Surveillance

Comprehensive guidance for public health surveillance activities including outbreak detection, surveillance system design, data analysis for population health monitoring, and response coordination. This skill supports healthcare organizations and public health agencies in maintaining robust surveillance capabilities.

**Important**: Surveillance activities must balance public health benefit with privacy protection. Always ensure appropriate data governance and ethics approvals are in place.

## When to Use This Skill

Invoke this skill when:
- Designing or evaluating a surveillance system
- Analyzing surveillance data for outbreak detection
- Developing outbreak response protocols
- Conducting population health assessments
- Implementing syndromic surveillance
- Preparing surveillance reports for stakeholders
- Evaluating surveillance system performance
- Coordinating multi-jurisdictional surveillance activities

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Clear statistical threshold breach with confirmatory testing | High | Activate outbreak response protocol |
| Elevated rates approaching threshold with consistent pattern | Medium | Enhanced monitoring; prepare response |
| Isolated cluster with unclear transmission | Low | Investigate further; rule out data artifacts |
| Novel pattern without historical comparison | Low | Consult epidemiologist; flag for expert review |

## Security & Privacy Considerations

### Data Governance
- All surveillance data must have approved data governance framework
- Privacy Impact Assessments required for new surveillance systems
- Data retention limits defined and enforced
- Access controls based on legitimate public health need

### De-identification Standards
- Use approved statistical disclosure control methods
- Small cell suppression for rare conditions (<5 cases)
- Geographic aggregation to protect individual privacy
- Date shifting for enhanced privacy where appropriate

## Regulatory Context

### Australia & New Zealand (Default)

| System | Purpose | Agency |
|--------|---------|--------|
| **NNDSS** | National notifiable disease surveillance | DoH (AU) |
| **EpiSurv** | NZ notifiable disease surveillance | ESR (NZ) |
| **ASPREN** | GP sentinel surveillance | DoH/Universities |
| **PICNet** | Healthcare-associated infection surveillance | State Health Depts |
| **OzFoodNet** | Foodborne disease surveillance | State Health Depts |

### Surveillance Types

| Type | Definition | Use Case |
|------|------------|----------|
| **Passive** | Routine reporting by providers | Notifiable diseases, laboratory data |
| **Active** | Active case finding by surveillance staff | Enhanced surveillance for outbreaks |
| **Sentinel** | Representative site surveillance | GP networks, hospital EDs |
| **Syndromic** | Pre-diagnostic indicators | Early outbreak detection |
| **Event-based** | Unstructured data monitoring | Media scanning, social media |

## Quick Reference

1. **Define Objectives**: Clear surveillance goals and case definitions
2. **Data Sources**: Reliable, timely, and complete data streams
3. **Analysis Methods**: Appropriate statistical methods for detection
4. **Response Protocols**: Clear escalation and response procedures
5. **Quality Assurance**: Regular validation and data quality checks
6. **Reporting**: Timely dissemination to stakeholders
7. **Evaluation**: Periodic assessment of system performance
8. **Ethics**: Appropriate governance and privacy protections

## Operating Modes

### Standard Mode
Full surveillance system design and operation including system specification, data quality management, statistical analysis, outbreak detection algorithms, response coordination, and system evaluation.

### Lite Mode
Streamlined outbreak detection and response for urgent situations. Focuses on immediate detection criteria and essential response actions. Maintains mandatory reporting and escalation requirements.

## Detailed Guidance

### 1. Surveillance System Design

#### Step 1: Define Objectives

| Element | Consideration | Example |
|---------|--------------|---------|
| **Purpose** | Why is surveillance needed? | Detect influenza outbreaks early |
| **Conditions** | What health events? | ILI, confirmed influenza, complications |
| **Population** | Who is covered? | All ED presentations in region |
| **Setting** | Where is data collected? | Hospital emergency departments |
| **Timeframe** | How quickly needed? | Daily reporting for rapid detection |

#### Step 2: Select Surveillance Approach

**Passive Surveillance:**
- Pros: Low cost, sustainable
- Cons: Incomplete reporting, delays
- Best for: Notifiable diseases with mandatory reporting

**Active Surveillance:**
- Pros: Complete, accurate data
- Cons: Resource intensive
- Best for: Outbreak investigations, high-priority conditions

**Syndromic Surveillance:**
- Pros: Early detection, pre-diagnostic
- Cons: Lower specificity, false alarms
- Best for: Bioterrorism, pandemic preparedness

### 2. Outbreak Detection

#### Statistical Methods

| Method | Description | Threshold |
|--------|-------------|-----------|
| **Cumulative Sum (CUSUM)** | Detects small sustained changes | CUSUM statistic > h |
| **Exponentially Weighted** | Recent data weighted higher | EWMA > μ + 3σ |
| **Historical Limits** | Comparison to baseline | Current > 2σ above baseline |
| **Scan Statistics** | Spatial-temporal clustering | SaTScan p-value < 0.05 |
| **Regression Models** | Adjust for trends/seasonality | Standardized residual > 2 |

#### Example: Daily Syndrome Surveillance

**Setting**: Emergency department ILI surveillance

**Algorithm**:
1. Calculate daily ILI proportion (ILI cases / total ED visits)
2. Compare to 2-week baseline (same days of week, previous 2 weeks)
3. Calculate z-score: (current - baseline mean) / baseline SD
4. Alert if z-score > 2 for 2+ consecutive days

### 3. Response Coordination

#### Outbreak Response Levels

| Level | Criteria | Response |
|-------|----------|----------|
| **1 - Watch** | Statistical alert, no epidemiological link | Enhanced monitoring |
| **2 - Alert** | Confirmed cluster with transmission | Activate outbreak team |
| **3 - Response** | Sustained transmission, public health impact | Full outbreak response |
| **4 - Emergency** | Widespread transmission, severe illness | Emergency operations |

#### Response Actions by Level

**Level 1 (Watch)**:
- Review case details
- Verify data accuracy
- Enhanced monitoring
- Prepare response resources

**Level 2 (Alert)**:
- Activate outbreak team
- Initiate case interviews
- Begin contact tracing
- Implement control measures
- Notify stakeholders

**Level 3 (Response)**:
- Full outbreak investigation
- Laboratory confirmation
- Environmental assessment
- Enhanced control measures
- Public communication

**Level 4 (Emergency)**:
- Emergency operations center
- Multi-agency coordination
- Public health emergency declaration
- Resource mobilization
- Media management

### 4. Surveillance Evaluation

#### System Attributes (CDC Guidelines)

| Attribute | Definition | Target |
|-----------|-----------|--------|
| **Simplicity** | Ease of operation | Minimal training required |
| **Flexibility** | Adaptability to changes | Rapidly accommodate new conditions |
| **Data Quality** | Completeness and validity | >90% complete core fields |
| **Acceptability** | Willingness to participate | >80% provider compliance |
| **Sensitivity** | Proportion of cases detected | >80% case ascertainment |
| **Representativeness** | Generalizability | Matches population demographics |
| **Timeliness** | Speed of data availability | <24h from event to report |
| **Stability** | Reliability and availability | >95% uptime |

## Common Mistakes

1. **Poor Case Definitions**: Unclear or inconsistent definitions leading to misclassification
2. **Incomplete Data**: Missing fields compromising analysis validity
3. **Delayed Reporting**: Lags reducing timeliness and response effectiveness
4. **Algorithm Errors**: Inappropriate thresholds causing alert fatigue or missed outbreaks
5. **No Baseline**: Lack of historical data preventing trend detection
6. **Privacy Breaches**: Inadequate de-identification in reports
7. **Response Delays**: Bureaucratic hurdles slowing outbreak response
8. **Resource Gaps**: Insufficient capacity for surge response

## Tool Requirements

- **Surveillance Database**: Secure, scalable data repository
- **Statistical Software**: R, SAS, or equivalent for analysis
- **GIS Tools**: For spatial analysis and mapping
- **Alert System**: Automated notification of threshold breaches
- **Dashboard**: Real-time visualization of surveillance data
- **Secure Communication**: For outbreak response coordination

## Success Indicators

A successful surveillance system:
- [ ] Detects outbreaks within defined timeframe
- [ ] Maintains >90% data completeness
- [ ] Achieves >80% sensitivity for target conditions
- [ ] Provides data within 24 hours of event
- [ ] Supports timely public health action
- [ ] Maintains stakeholder engagement
- [ ] Meets privacy and governance requirements
- [ ] Regularly evaluated and improved

## Cross-References

- **notifiable-diseases**: Case identification and individual notifications
- **health-data-analysis**: Statistical methods for surveillance data
- **health-incidents**: Outbreak investigation and incident management
- **health-ethics**: Ethics of population health surveillance

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-14 | Initial release |

## References

- [CDC Surveillance Resource Center](https://www.cdc.gov/surveillance/)
- [WHO Global Health Observatory](https://www.who.int/data/gho)
- [European Centre for Disease Prevention and Control Surveillance Atlases](https://www.ecdc.europa.eu/en/all-topics-z/surveillance-and-disease-data)
- [Australian Institute of Health and Welfare Disease Surveillance](https://www.aihw.gov.au/reports/australias-health/disease-surveillance)
