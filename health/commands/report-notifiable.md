---
name: report-notifiable
description: Initiate a notifiable disease report to public health authorities. Guides selection of disease, jurisdiction requirements, and generates a notification checklist for compliance.
trigger: !health
color: red
---

# /report-notifiable Command

Initiate mandatory reporting of a notifiable disease to public health authorities.

## When to Use

Use this command when:
- Diagnosing or suspecting a notifiable disease
- Laboratory confirmation of a reportable condition
- Managing an outbreak or disease cluster
- Coordinating contact tracing activities
- Responding to a public health emergency

**Critical**: Many notifiable diseases require IMMEDIATE reporting (within 24 hours). Do not delay reporting pending all test results if clinical suspicion is high.

## Workflow

### 1. Disease Selection

Present the user with notifiable disease categories:

1. **Vaccine-Preventable Diseases**
   - Measles, mumps, rubella
   - Pertussis (whooping cough)
   - Diphtheria, tetanus
   - Varicella (chickenpox)
   - Invasive meningococcal disease

2. **Food-borne and Water-borne Diseases**
   - Salmonellosis, campylobacteriosis
   - Listeriosis
   - Hepatitis A
   - Typhoid/paratyphoid

3. **Blood-borne Diseases**
   - Hepatitis B, C
   - HIV (new diagnoses)

4. **Sexually Transmitted Infections**
   - Syphilis (infectious)
   - Gonorrhoea
   - Chlamydia (jurisdiction-dependent)

5. **Vector-borne Diseases**
   - Dengue, malaria
   - Ross River virus, Barmah Forest virus
   - Japanese encephalitis

6. **Other Notifiable Conditions**
   - Tuberculosis
   - Q fever
   - Psittacosis
   - Novel/emerging infections

### 2. Jurisdiction Selection

Determine applicable jurisdiction and authority:

| Jurisdiction | Primary Authority | Contact |
|--------------|------------------|---------|
| **Australia** | State/Territory Health Department | Public Health Unit |
| **New Zealand** | Medical Officer of Health | Local Public Health Service |
| **United States** | State Health Department + CDC | State Epidemiologist |
| **European Union** | National Focal Point + ECDC | Competent Authority |

### 3. Notification Checklist Generation

Based on disease and jurisdiction, generate a checklist:

#### Pre-Reporting Checklist

- [ ] Disease confirmed as notifiable in jurisdiction
- [ ] Case definition applied (suspected/probable/confirmed)
- [ ] Laboratory results available and attached
- [ ] Patient demographics complete
- [ ] Contact/exposure history documented
- [ ] Onset date and diagnosis date recorded
- [ ] Healthcare facility information included

#### Urgency Assessment

**IMMEDIATE (Phone + Online)**:
- Anthrax, botulism, plague
- Viral hemorrhagic fevers
- Novel/emerging pathogens
- Outbreaks/clusters

**URGENT (Within 24 hours)**:
- Measles, meningococcal, pertussis
- Food-borne diseases
- Vector-borne diseases

**ROUTINE (Within 5 days)**:
- Hepatitis B, C
- Most STIs
- Some zoonotic diseases

#### Required Information

**Patient Information**:
- Full name
- Date of birth
- Residential address
- Contact phone number
- Indigenous status (if applicable)
- Country of birth

**Clinical Information**:
- Disease/condition
- Date of onset
- Date of diagnosis
- Symptoms and signs
- Complications
- Outcome (if resolved/deceased)

**Laboratory Information**:
- Test type and result
- Laboratory name
- Date collected
- Specimen type

**Epidemiological Information**:
- Risk factors
- Travel history
- Occupation
- Contact with confirmed cases
- Institution/childcare attendance

## Example Session

**User:** `/report-notifiable`

**System:**
```
Notifiable Disease Reporting

Select the disease category:
1. Vaccine-Preventable Diseases
2. Food-borne and Water-borne Diseases
3. Blood-borne Diseases
4. Sexually Transmitted Infections
5. Vector-borne Diseases
6. Other Notifiable Conditions

Enter number or type disease name:
```

**User:** "1"

**System:**
```
Vaccine-Preventable Diseases

Select specific condition:
1. Measles
2. Mumps
3. Rubella
4. Pertussis (whooping cough)
5. Invasive meningococcal disease
6. Diphtheria
7. Tetanus
8. Varicella (chickenpox)

Enter number:
```

**User:** "1"

**System:**
```
MEASLES - URGENT NOTIFICATION REQUIRED

Measles requires immediate notification (within 24 hours) in all Australian states/territories and New Zealand.

Select jurisdiction:
1. Australian Capital Territory
2. New South Wales
3. Northern Territory
4. Queensland
5. South Australia
6. Tasmania
7. Victoria
8. Western Australia
9. New Zealand

Enter number:
```

**User:** "2" (NSW)

**System:**
```
NSW Health Measles Notification

⚠️ TIMEFRAME: Report within 24 hours
📞 URGENT (after hours): 1300 066 055
🌐 ONLINE: [NSW Health Notifiable Diseases](https://www.health.nsw.gov.au)

NOTIFICATION CHECKLIST:

Patient Information:
- [ ] Full name
- [ ] Date of birth
- [ ] Residential address and contact
- [ ] Indigenous status

Clinical Details:
- [ ] Date of symptom onset
- [ ] Date of rash onset
- [ ] Date of diagnosis
- [ ] Complications (if any)

Laboratory:
- [ ] Serology or PCR result attached
- [ ] Laboratory name and date

Epidemiological:
- [ ] Vaccination status
- [ ] Recent travel (last 3 weeks)
- [ ] Contact with known case
- [ ] School/childcare/workplace

Contacts for Tracing:
- [ ] Household contacts listed
- [ ] Healthcare contacts documented

Opening NSW notification portal...
Use /notifiable-diseases skill for detailed guidance on completion.
```

## Output

The command generates:
1. **Disease-specific guidance** - Timeframes and requirements
2. **Notification checklist** - Required information fields
3. **Authority contact** - Appropriate public health unit
4. **Urgency indicator** - Immediate vs routine reporting
5. **Skill reference** - Links to detailed guidance

## Integration Points

- **Input**: Clinical diagnosis, laboratory results, patient information
- **Process**: Uses `notifiable-diseases` skill for detailed methodology
- **Output**: Notification checklist, jurisdiction-specific requirements
- **Downstream**: Public health authority notification systems

## Error Handling

| Issue | Response |
|-------|----------|
| Disease not on notifiable list | Verify jurisdiction; may still be reportable as unusual cluster |
| Missing patient information | Flag required fields; defer to patient records |
| Out-of-hours urgent case | Provide after-hours emergency contact |
| Multi-jurisdictional case | Identify primary jurisdiction; coordinate reporting |

## MCP Connectors

```yaml
connectors:
  - jurisdiction database: ~~health_jurisdictions
  - notifiable diseases list: ~~notifiable_disease_registry
  - notification portal: ~~health_notification_systems
```

## Related Commands

- `/assess-risk` - Risk assessment for exposure incidents
- `/report-incident` - Healthcare incident reporting (different from notifiable diseases)
