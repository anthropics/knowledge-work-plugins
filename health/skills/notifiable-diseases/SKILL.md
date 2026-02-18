---
name: health/notifiable-diseases
description: This skill should be used when managing notifiable disease reporting obligations, including identifying reportable conditions, understanding notification timelines, completing reporting forms, and coordinating public health responses. Applies to clinical and laboratory staff, infection control practitioners, and public health officials.
version: 1.0.0
---

# Notifiable Diseases

Guidance for healthcare providers on identifying, documenting, and reporting notifiable diseases according to jurisdictional requirements. This skill supports compliance with mandatory reporting obligations across Australia, New Zealand, and international jurisdictions.

**Critical**: Failure to report notifiable diseases can result in regulatory penalties and compromises public health surveillance. Always verify current disease lists as they are updated regularly.

## When to Use This Skill

Invoke this skill when:
- Diagnosing or suspecting a notifiable disease in a patient.
- Determining if a condition requires mandatory reporting.
- Completing notification forms for public health authorities.
- Coordinating contact tracing or outbreak investigations.
- Understanding notification timeframes by jurisdiction.
- Managing laboratory reporting obligations.
- Responding to public health authority requests for information.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Classic presentation of notifiable disease with laboratory confirmation | High | Proceed with notification; document thoroughly |
| Suspected notifiable disease pending laboratory confirmation | Medium | Initiate notification process; flag as preliminary |
| Unclear diagnosis with overlapping symptoms | Low | Consult infectious diseases or public health; document uncertainty |
| Novel or emerging pathogen not on standard lists | Low | Report immediately to public health; await guidance |

## Security & Privacy Considerations

### PHI/PII Handling
- **Never** include patient identifiers in unencrypted communications
- Use approved secure notification portals only
- De-identify data for internal quality reviews
- Maintain separate confidential records with identifiers

### Minimum Necessary Principle
- Report only data fields required by the notification form
- Do not include unrelated clinical information
- Limit distribution to those with legitimate public health need

## Regulatory Context

### Australia & New Zealand (Default)

#### Australian Notifiable Diseases

| Disease Category | Examples | Notification Timeline | Authority |
|-----------------|----------|---------------------|-----------|
| **Blood-borne** | Hepatitis B, C, HIV | 5 days | State/Territory Health Dept |
| **Vaccine-preventable** | Measles, pertussis, meningococcal | Immediate (24h) | State/Territory Health Dept |
| **Food-borne** | Salmonellosis, listeriosis | Immediate (24h) | State/Territory Health Dept |
| **Sexually transmitted** | Syphilis, gonorrhoea | 5 days | State/Territory Health Dept |
| **Vector-borne** | Dengue, Ross River virus | Immediate (24h) | State/Territory Health Dept |
| **Zoonotic** | Q fever, psittacosis | 5 days | State/Territory Health Dept |
| **Healthcare-associated** | CRE, MRSA outbreaks | Immediate | State/Territory Health Dept |

#### New Zealand Notifiable Diseases

| Disease Category | Examples | Notification Timeline | Authority |
|-----------------|----------|---------------------|-----------|
| **Urgent** | Cholera, plague, viral haemorrhagic fever | Immediate | Medical Officer of Health |
| **Priority** | Measles, meningococcal, pertussis | Immediate | Medical Officer of Health |
| **Standard** | Hepatitis, STIs, food-borne | 3 days | Medical Officer of Health |

### US/EU-lite Fallback

| Jurisdiction | Reporting System | Key Difference |
|--------------|-----------------|----------------|
| **United States** | CDC NNDSS + State systems | Varies by state; some conditions federally notifiable only |
| **European Union** | ECDC TESSy | Standardized EU case definitions; 24-48 hour reporting |

### Jurisdiction Matrix

| Jurisdiction | Authority | Reporting Trigger | Timeframe | Required Artifacts | Escalation Point |
|--------------|-----------|-------------------|-----------|-------------------|------------------|
| **AU - National** | DoH + State/Territory | Laboratory confirmation or clinical suspicion | Immediate-5 days | Notification form; laboratory report | Public Health Unit Director |
| **NZ - National** | Te Whatu Ora | Laboratory confirmation or clinical suspicion | Immediate-3 days | EpiSurv notification | Medical Officer of Health |
| **US - Federal** | CDC NNDSS | Laboratory confirmation | State-dependent (usually 24h-7d) | State notification form | State Epidemiologist |
| **EU** | ECDC TESSy | Laboratory confirmation | 24-48 hours | TESSy case report form | National Focal Point |

## Quick Reference

1. **Identify**: Confirm disease is on notifiable list for your jurisdiction
2. **Notify**: Report within required timeframe (immediate for urgent conditions)
3. **Document**: Complete all required fields accurately
4. **Laboratory**: Ensure lab has also submitted notification
5. **Follow-up**: Respond to public health authority requests promptly
6. **Contact Tracing**: Cooperate with contact identification when requested
7. **Outbreaks**: Any outbreak/cluster is notifiable regardless of specific disease

## Operating Modes

### Standard Mode
Complete notifiable disease management including identification of reportable conditions, understanding of notification timeframes, completion of detailed notification forms, coordination with public health authorities, and participation in contact tracing and outbreak investigations.

### Lite Mode
Quick reference for urgent notifications - confirms disease is notifiable, identifies correct authority, and provides immediate reporting pathway. Assumes user will complete full documentation later. Does not suppress mandatory immediate reporting requirements.

## Detailed Guidance

### 1. Disease Identification

#### Step 1: Check Notifiable Disease List
- Access current list from your jurisdiction's health department website
- Lists are updated regularly - verify you have latest version
- Some conditions have subcategories (e.g., invasive vs. non-invasive meningococcal)

#### Step 2: Apply Case Definitions

| Component | Definition |
|-----------|------------|
| **Clinical Criteria** | Signs and symptoms required |
| **Laboratory Criteria** | Confirmatory or supportive tests |
| **Epidemiological Link** | Exposure or contact history |
| **Case Classification** | Suspected, probable, confirmed |

**Example - Measles Case Definition:**
- **Suspected**: Fever + rash + cough/coryza/conjunctivitis
- **Probable**: Suspected case + epidemiological link
- **Confirmed**: Suspected case + laboratory confirmation

### 2. Notification Process

#### Who Must Notify

| Role | Obligation |
|------|------------|
| **Medical Practitioner** | Primary responsibility for clinical notifications |
| **Laboratory Director** | Mandatory for laboratory-confirmed results |
| **Nurse/Midwife** | In some jurisdictions for specific conditions |
| **Hospital Administration** | Ensure systems support compliance |

#### Notification Methods

**Australia:**
- Online: State/Territory surveillance systems (e.g., PAEDS, NetEpi)
- Phone: For urgent conditions outside hours
- Form: PDF/paper backup when systems unavailable

**New Zealand:**
- Online: EpiSurv (via ESR)
- Phone: Medical Officer of Health for urgent cases
- Form: Manual forms as backup

### 3. Notification Form Completion

#### Required Fields (Standard)

| Field | Rationale | Common Errors |
|-------|-----------|---------------|
| **Patient demographics** | Case identification | Incomplete addresses |
| **Disease/Condition** | Classification | Wrong code used |
| **Onset date** | Epidemiological timeline | Admission date instead |
| **Diagnosis basis** | Case classification | Omitting laboratory details |
| **Risk factors** | Public health action | Missing travel history |
| **Healthcare facility** | Outbreak investigation | Wrong facility code |

#### Example: Complete Notification Flow

**Scenario**: 5-year-old with confirmed pertussis

1. **Day 0 (Diagnosis)**:
   - PCR positive for Bordetella pertussis
   - Clinical: Paroxysmal cough + post-tussive vomiting
   - Determine: URGENT notification required (within 24 hours)

2. **Immediate Actions**:
   - Complete online notification form
   - Include laboratory report reference
   - Document household contacts (for contact tracing)
   - Flag recent vaccination status

3. **Public Health Response**:
   - Contact tracing initiated
   - Prophylaxis offered to contacts
   - Outbreak assessment if multiple cases
   - 5-day exclusion for case from school/childcare

### 4. Special Circumstances

#### Outbreaks and Clusters

Any unusual clustering of disease is notifiable:
- Two or more linked cases of same condition
- Increased incidence above baseline
- Novel or emerging pathogen

**Immediate Actions for Suspected Outbreak:**
1. Notify public health immediately (phone)
2. Do not wait for laboratory confirmation
3. Begin line list of cases
4. Preserve potential exposure sources

#### Laboratory Reporting

Laboratories have independent notification obligations:
- Ensure lab knows which tests are ordered
- Verify positive results have been reported by lab
- Follow up if no confirmation received within expected timeframe

## Common Mistakes

1. **Reporting Delay**: Waiting for all test results instead of reporting on clinical suspicion
2. **Wrong Authority**: Notifying federal instead of state/local public health
3. **Incomplete Forms**: Omitting epidemiological risk factors
4. **Missing Outbreaks**: Failing to recognize and report unusual clusters
5. **Jurisdiction Confusion**: Applying wrong case definitions or timeframes
6. **Privacy Breach**: Including PHI in unsecured communications
7. **Follow-up Failure**: Not responding to public health requests for additional information
8. **Outdated Lists**: Using old notifiable disease lists missing new conditions

## Tool Requirements

- **Jurisdiction Database**: Access to current notifiable disease lists
- **Notification Portal**: Secure online reporting system
- **Laboratory Interface**: Verification of lab reporting status
- **Contact Registry**: System for documenting exposed contacts

## Success Indicators

A successful notifiable disease management workflow:
- [ ] Disease correctly identified as notifiable
- [ ] Notification submitted within required timeframe
- [ ] Complete and accurate information provided
- [ ] Laboratory has also reported (or confirmed)
- [ ] Public health authority has acknowledged receipt
- [ ] Contact tracing information provided when requested
- [ ] Patient/family informed of public health requirements
- [ ] Documentation maintained for audit purposes

## Cross-References

- **health-coding**: Disease classification and coding
- **health-data-analysis**: Epidemiological analysis of surveillance data
- **health-incidents**: Outbreak investigation coordination
- **health-ethics**: Research ethics for surveillance data use

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-14 | Initial release with AU/NZ focus |

## References

- [Australian National Notifiable Diseases Surveillance System](https://www.health.gov.au/resources/publications/australian-national-notifiable-diseases-surveillance-system)
- [New Zealand Health Act 1956 - Notifiable Diseases](https://www.legislation.govt.nz/act/public/1956/0065/latest/whole.html)
- [CDC NNDSS Notifiable Conditions](https://ndc.services.cdc.gov/)
- [ECDC Surveillance Atlas of Infectious Diseases](https://atlas.ecdc.europa.eu/public/index.aspx)
