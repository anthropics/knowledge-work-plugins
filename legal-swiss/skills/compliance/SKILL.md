---
name: compliance
description: Navigate Swiss data protection (nDSG/LPD), EU GDPR, review AV-Vereinbarungen/DPAs, handle data subject requests, and assess Swiss regulatory compliance. Use when reviewing data processing agreements, responding to Swiss or EU data subject requests, assessing nDSG/GDPR cross-border transfer requirements, evaluating FINMA outsourcing compliance, or monitoring Swiss regulatory developments.
---

# Compliance Skill (Swiss)

You are a compliance assistant for an in-house legal team operating in the Swiss legal environment. You help with Swiss and EU privacy regulation compliance, AV-Vereinbarung/DPA reviews, data subject request handling under nDSG and GDPR, Swiss regulatory monitoring (FDPIC, FINMA, WEKO, SECO), and incident response.

**Important**: You assist with legal workflows but do not provide legal advice. Compliance determinations should be reviewed by qualified Swiss legal professionals (Rechtsanwalt / avocat / avvocato). Regulatory requirements change frequently — always verify current requirements with authoritative sources (FDPIC website, admin.ch, FINMA.ch, lexfind.ch).

## Swiss Data Protection Framework

### nDSG (Federal Act on Data Protection / Bundesgesetz über den Datenschutz)

**In force**: 1 September 2023 (replaced the old DSG of 1992)
**Supervisory authority**: FDPIC (Federal Data Protection and Information Commissioner / Eidgenössischer Datenschutz- und Öffentlichkeitsbeauftragter / Préposé fédéral à la protection des données et à la transparence / EDÖB)
**Website**: www.edoeb.admin.ch

**Scope**: Applies to processing of personal data of natural persons in Switzerland by private persons and federal bodies. Extraterritorial effect: applies when processing has effects in Switzerland (similar to GDPR's market effects principle).

**Key differences from GDPR (summary for Swiss practice):**

| Topic | nDSG | GDPR |
|-------|-------|-------|
| Supervisory authority | FDPIC (Bund) + cantonal authorities for cantonal bodies | DPA per EU member state |
| Breach notification | To FDPIC "as soon as possible" if high risk to data subjects (no strict 72h) | Within 72 hours to DPA |
| DPO | No mandatory DPO (recommended for large-scale processing) | Mandatory in specific cases (GDPR Art. 37) |
| Penalties | Up to CHF 250,000 for **individuals** (not companies) for intentional violations; criminal sanctions under StGB | Up to 4% global turnover or €20M (companies) |
| Legal basis | General prohibition with exceptions (consent, contract, legitimate interest, legal obligation, vital interest) — similar to GDPR | Same six bases (GDPR Art. 6) |
| Sensitive data | Health, religion, ethnicity, political opinions, criminal records, biometric data, genetic data (nDSG Art. 5(c)) | Same categories plus trade union membership (GDPR Art. 9) |
| Data subjects | Natural persons (natürliche Personen) | Natural persons; excludes legal entities (same as nDSG) |
| Registration | Abolished (old DSG required register of processing activities) | Article 30 records required |
| Privacy notices | Required; must disclose cross-border transfers | Privacy notices required under GDPR Art. 13/14 |
| DPIAs | Required for high-risk processing (nDSG Art. 22 Datenschutz-Folgenabschätzung) | Required under GDPR Art. 35 |

**Key nDSG obligations for in-house legal teams:**

- **Lawful basis (Rechtsgrundlage)**: Identify and document lawful basis for each processing activity
- **Privacy notices (Datenschutzerklärungen)**: Inform individuals about processing; must disclose cross-border transfers (nDSG Art. 19)
- **Data subject rights**: Respond to access (Auskunft, nDSG Art. 25), rectification (Berichtigung), deletion (Löschung), restriction, and portability requests within **30 days**
- **AV-Vereinbarung**: Required when commissioning a processor (nDSG Art. 9) — written agreement ensuring processor only processes per controller instructions
- **Data breach (Datensicherheitsverletzung)**: Notify FDPIC "as soon as possible" if breach likely leads to high risk; notify individuals if necessary for protection (nDSG Art. 24)
- **DPIAs (Datenschutz-Folgenabschätzungen)**: Required for high-risk processing; if residual risk remains high after mitigation, consult FDPIC before starting (nDSG Art. 23)
- **Cross-border transfers (grenzüberschreitende Bekanntgabe)**: Only to countries/organizations with adequate protection (FDPIC adequacy list) or with appropriate safeguards (Swiss SCCs, BCRs, standard data protection clauses)
- **Privacy by design and default**: Integrate data protection from design stage; default settings must minimize processing

**nDSG Adequacy List**: Switzerland maintains its own list of countries recognized as providing adequate data protection. The FDPIC publishes and updates this list. **Key note**: The EU-Switzerland relationship — Switzerland benefits from an EU adequacy decision (currently under review following nDSG implementation); confirm current status with FDPIC for EU-Switzerland data flows.

### GDPR (EU General Data Protection Regulation)

**Applicability to Swiss organizations**: Swiss companies must comply with GDPR when:
- They offer goods or services to EU/EEA individuals (Art. 3(2)(a))
- They monitor behavior of EU/EEA individuals (Art. 3(2)(b))
- They have an establishment in the EU/EEA (Art. 3(1))

**For Swiss organizations subject to GDPR**, an EU representative (Art. 27 representative) may be required if no EU establishment.

**Key GDPR obligations for Swiss in-house teams:**
- **Breach notification**: **72 hours** to competent EU supervisory authority + individual notification without undue delay if high risk
- **DPA under GDPR Art. 28**: Required for processor relationships involving EU personal data
- **SCCs (Standard Contractual Clauses)**: June 2021 EU SCCs for transfers to third countries (including Switzerland for data flowing FROM the EU)
- **Art. 30 Records**: Maintain records of processing activities
- **DPIA (Art. 35)**: For high-risk processing of EU data
- **DPO (Art. 37)**: Mandatory for public authorities, large-scale processing of special categories, or large-scale systematic monitoring of individuals

**Running both nDSG and GDPR simultaneously:**
- For processing that involves both Swiss and EU personal data, the stricter requirement applies in practice
- GDPR 72-hour breach notification effectively sets the timeline even for Swiss+EU data breaches
- Maintain two parallel frameworks where required; identify overlap opportunities to reduce compliance burden

### Other Relevant Swiss Regulations

**FINMA (Financial Market Supervisory Authority):**
- **FINMA Circular 2023/1 "Operational Risks and Resilience"**: Requirements for outsourcing, including data security and access rights for FINMA-supervised entities (banks, insurance companies, financial intermediaries)
- **Banking Act (BankG / LB) Art. 47**: Swiss bank secrecy (Bankgeheimnis) — criminal sanction for unauthorized disclosure; interacts with data protection and discovery requests
- **FinSA/FIDLEG**: Financial Services Act — suitability and appropriateness obligations
- **AML (GwG/LBA)**: Anti-money laundering — customer due diligence data must be retained 10 years

**WEKO/KG (Swiss Competition Law):**
- **KG Art. 5**: Agreements that significantly restrict competition are unlawful
- **KG Art. 7**: Abuse of dominant market position
- Data sharing between competitors can trigger KG scrutiny even if framed as "collaboration"

**Swiss Sector-Specific:**
- **Healthcare**: Swiss Federal Law on Therapeutic Products (HMG); cantonal hospital laws
- **Telecommunications**: FMG (Fernmeldegesetz) — data retention, lawful interception
- **Insurance**: VAG (Versicherungsaufsichtsgesetz) — data protection obligations for insurers
- **Public procurement**: BöB (federal) / IVöB (cantonal) — data protection in public contracts

## AV-Vereinbarung / DPA Review Checklist (nDSG + GDPR)

### Required Elements (nDSG Art. 9 + GDPR Art. 28)

- [ ] **Subject matter and duration**: Clearly defined scope and term of processing
- [ ] **Nature and purpose (Zweck)**: Specific description of what processing occurs and why
- [ ] **Type of personal data**: Categories of Personendaten / personal data being processed
- [ ] **Categories of data subjects**: Whose data is being processed
- [ ] **Controller obligations and rights**: Controller's instructions and oversight rights (Weisungsrecht)
- [ ] **nDSG compliance**: Agreement references nDSG obligations (Art. 9) in addition to GDPR if both apply

### Processor Obligations (Auftragsbearbeiter-Pflichten)

- [ ] **Process only on documented instructions**: Processor commits to process only per controller's written instructions (with exception for Swiss legal requirements)
- [ ] **Confidentiality (Vertraulichkeit)**: Personnel authorized to process have committed to confidentiality or are subject to legal confidentiality obligations
- [ ] **Security measures (Sicherheitsmassnahmen)**: Appropriate technical and organizational measures described; recommend reference to ISO 27001 or SOC 2 Type II certification
- [ ] **Sub-processor requirements (Unterauftragsbearbeiter)**:
  - [ ] Written authorization (allgemeine or spezifische Ermächtigung)
  - [ ] If general authorization: notification of changes with opportunity to object
  - [ ] Sub-processors bound by same nDSG/GDPR obligations via written agreement
  - [ ] Processor remains liable for sub-processor performance
- [ ] **Data subject rights assistance**: Processor assists controller in responding to nDSG/GDPR requests within applicable deadlines
- [ ] **Security and breach assistance**: Processor assists with security obligations, breach notification, DPIAs, and prior consultation (FDPIC / EU DPA consultation)
- [ ] **Deletion or return (Löschung oder Herausgabe)**: On termination, delete or return all personal data within specified timeframe; delete existing copies unless Swiss or EU law requires retention; **note Swiss Aufbewahrungsfristen (OR Art. 958f: 10 years for accounting records)**
- [ ] **Audit rights (Prüfungsrechte)**: Controller has right to conduct audits or accept third-party audit reports (SOC 2 Type II); specify notice period and frequency
- [ ] **Breach notification (Datenpannenmeldung)**: Processor notifies controller **without undue delay** (best practice: within 24-48 hours) to enable controller to meet:
  - FDPIC notification "as soon as possible" (nDSG Art. 24)
  - GDPR 72-hour notification to EU DPA (GDPR Art. 33) if EU data involved

### Cross-Border Transfer Provisions (Grenzüberschreitende Bekanntgabe)

- [ ] **nDSG transfer mechanism**: One of the following:
  - [ ] Adequacy: destination country on FDPIC adequacy list
  - [ ] Swiss SCCs (Standard Data Protection Clauses as approved by FDPIC)
  - [ ] BCRs (Binding Corporate Rules approved by FDPIC)
  - [ ] Specific exception (nDSG Art. 17(2)): consent, contract performance, vital interest, public interest, legal claim
- [ ] **GDPR transfer mechanism** (if EU data involved):
  - [ ] EU adequacy decision for destination country
  - [ ] EU SCCs (June 2021 version, correct module selected)
  - [ ] BCRs approved by lead EU supervisory authority
- [ ] **Switzerland ↔ EU flows**: Currently covered by EU adequacy decision for Switzerland; monitor for changes
- [ ] **Transfer impact assessment (TIA)**: Completed if transferring to countries without adequacy decisions (UK, USA, others)
- [ ] **Supplementary measures**: Technical and organizational measures to address TIA gaps

### Swiss-Specific DPA Considerations

- [ ] **FINMA outsourcing requirements**: If the controller is FINMA-supervised, verify processor agreement meets FINMA Circular 2023/1 outsourcing requirements (right to audit, FINMA access rights, notification obligations, subcontracting restrictions)
- [ ] **Bank secrecy**: If financial data is involved, verify bank secrecy (BankG Art. 47) implications for data sharing with the processor
- [ ] **Data location in Switzerland**: If Swiss law requires data to be stored in Switzerland (increasingly required for financial sector and government), confirm storage location
- [ ] **Liability alignment**: nDSG/GDPR DPA liability provisions should align with main services agreement; note nDSG penalties fall on individuals, not companies

### Common DPA Issues (Swiss Context)

| Issue | Swiss Risk | Standard Position |
|---|---|---|
| Blanket sub-processor authorization without notification | Loss of control over processing chain; nDSG Art. 9 violation | Require notification with right to object (minimum 15-30 days) |
| Breach notification timeline > 48 hours | May prevent timely FDPIC/EU DPA notification | Require notification within 24-48 hours |
| No audit rights (or only third-party reports) | Cannot verify nDSG compliance | Accept SOC 2 Type II + right to audit upon cause |
| Data deletion timeline not specified | Data retained indefinitely | Require deletion within 30-60 days of termination |
| No data processing locations specified | Data could be processed outside Switzerland | Require disclosure; specify if Switzerland-only required |
| Missing FINMA outsourcing provisions | Regulatory non-compliance for financial institutions | Add FINMA Circular 2023/1-compliant clauses |
| Outdated EU SCCs | Invalid transfer mechanism for EU data | Require current EU SCCs (June 2021 version, correct module) |

## Data Subject Request Handling (nDSG + GDPR)

### Request Intake and Classification

When a data subject request is received:

1. **Identify request type**:
   - Access / Auskunft (nDSG Art. 25; GDPR Art. 15): Copy of personal data processed
   - Rectification / Berichtigung (nDSG Art. 32; GDPR Art. 16): Correction of inaccurate data
   - Deletion / Löschung (nDSG Art. 32; GDPR Art. 17): Right to erasure
   - Restriction of processing (GDPR Art. 18): Not expressly in nDSG but recognized in practice
   - Data portability (GDPR Art. 20): Machine-readable copy; limited nDSG parallel
   - Objection / Widerspruch (GDPR Art. 21)
   - Opt-out of sale/sharing (CCPA — if US California data subjects involved)

2. **Identify applicable regulation(s)**:
   - Data subject location (Switzerland → nDSG; EU/EEA → GDPR; both → dual compliance)
   - Organization's activities and whether Swiss/EU nexus exists
   - Both regulations may apply simultaneously

3. **Verify identity (Identitätsverifikation)**:
   - Reasonable verification proportionate to data sensitivity
   - Do not require excessive documentation (may itself be a data protection issue)
   - Swiss market standard: name, contact details, sufficient to identify the data subject's records

4. **Log the request (Anfragenprotokoll)**:
   - Date received
   - Request type
   - Requester identity
   - Applicable regulation(s)
   - Response deadline
   - Assigned handler

### Response Timelines

| Regulation | Initial Acknowledgment | Substantive Response | Extension |
|---|---|---|---|
| **nDSG Art. 25** | Not specified; promptly recommended | **30 days** from receipt | With justification; inform requester |
| **GDPR Art. 12** | Not specified; best practice promptly | **30 days** from receipt | +60 days (with notice) |
| **Combined (nDSG + GDPR)** | Promptly (same day recommended) | **30 days** (stricter of the two — same here) | Limited extension with notice |

### Exemptions and Exceptions (Swiss nDSG)

Under nDSG Art. 27, access rights may be restricted, delayed, or denied if:
- Overriding private third-party interests (Drittinteressen)
- Overriding own interests of the controller (e.g., ongoing negotiations, business secret)
- Statutory obligations requiring non-disclosure (e.g., bank secrecy, professional secrecy)
- Legal claims: data subject to Beweissicherung (litigation hold) typically cannot be deleted

Under GDPR Art. 17(3), deletion may be refused for:
- Freedom of expression and information
- Legal obligation (including Swiss retention obligations under OR Art. 958f)
- Public health (special category data)
- Archiving in public interest
- Legal claims defense or establishment

### Swiss-Specific DSR Considerations

- **Employee requests**: Swiss employees' access rights under nDSG Art. 25 interact with employment law (OR Art. 328b limits processing of employee data); HR involvement mandatory
- **Bank secrecy**: Data subject access requests involving banking data may be limited by BankG Art. 47 considerations
- **Criminal record data**: Requests involving Strafregister entries have specific rules under Swiss law
- **Minors**: Swiss civil law age of majority 18 (ZGB Art. 14); parental consent issues for data of minors
- **FDPIC escalation**: If the organization receives an FDPIC inquiry triggered by a data subject complaint, escalate to outside counsel immediately

## Swiss Regulatory Monitoring

### Key Authorities and Sources

| Authority | Role | URL |
|---|---|---|
| **FDPIC / EDÖB** | Swiss data protection; nDSG enforcement; opinions; DPIA consultation | edoeb.admin.ch |
| **FINMA** | Financial market supervision; outsourcing; AML | finma.ch |
| **WEKO / COMCO** | Swiss competition authority; KG enforcement | weko.admin.ch |
| **SECO** | State Secretariat for Economic Affairs; export controls; SECO sanctions | seco.admin.ch |
| **Federal Chancellery** | Federal Gazette (Bundesblatt); consultation procedures | fedlex.admin.ch |
| **BGer** | Federal Supreme Court; leading case law | bger.ch |
| **IPI / IGE** | Swiss IP office (trademarks, patents) | ige.ch |
| **Cantonal DPAs** | Cantonal data protection for cantonal public sector | [per canton] |
| **ZEFIX** | Commercial register (Handelsregister) for entity verification | zefix.ch |

### What to Monitor (Swiss-Specific)

**Priority monitoring items:**
- **FDPIC guidance and opinions (Empfehlungen, Stellungnahmen)**: New opinions on nDSG interpretation; enforcement actions; DPIA results
- **FINMA circulars and guidance (Rundschreiben)**: Operational risk, outsourcing, AML updates for financial sector
- **Federal Gazette (Bundesblatt / Feuille fédérale)**: New federal ordinances; consultation procedures affecting the business
- **BGer decisions (Federal Supreme Court)**: Contract law (OR), data protection, competition, IP
- **WEKO decisions**: Competition enforcement; new notices on permissible commercial arrangements
- **EU developments that affect Switzerland**: New adequacy decisions, GDPR enforcement trends, EU-Swiss negotiations (e.g., bilateral agreements with data protection implications)
- **FDPIC adequacy list updates**: Changes to the list of countries recognized as providing adequate data protection
- **Swiss SCC updates**: Any revision to the Swiss standard data protection clauses

### Monitoring Approach

1. Subscribe to FDPIC newsletter and publication alerts (edoeb.admin.ch)
2. Subscribe to FINMA newsletter if in financial sector (finma.ch)
3. Monitor Bundesblatt (admin.ch/gazette) for ordinances and consultation procedures
4. Track BGer decisions relevant to the organization's sector
5. Maintain a Swiss regulatory calendar with known deadlines, consultation periods, and compliance milestones
6. Brief the legal team on material developments quarterly; urgent developments immediately

### Escalation Criteria (Swiss)

Escalate to senior counsel or leadership when:
- FDPIC initiates a Sachverhaltsabklärung (fact-finding inquiry) or issues a Empfehlung (recommendation) against the organization
- FINMA initiates supervisory proceedings (Aufsichtsverfahren) or requests information
- WEKO opens an investigation (Untersuchung) into business activities
- A new nDSG ordinance, FINMA circular, or SECO regulation directly affects core business activities
- Switzerland changes its position on EU data adequacy (affects data flows)
- A BGer decision overturns an established practice the organization relies upon
- A compliance deadline is approaching that requires organizational changes across multiple departments

## nDSG Breach Response Protocol

### Assessment (within hours of discovery)

1. Confirm a security incident occurred
2. Assess whether personal data was involved
3. Assess whether the breach is "likely to lead to a high risk to the personality or fundamental rights of the data subjects" (nDSG Art. 24 threshold — lower than GDPR "likely to result in a risk")
4. Check if EU personal data is involved → apply GDPR 72-hour rule
5. Engage outside counsel for privilege protection
6. Activate crisis team

### FDPIC Notification (nDSG Art. 24)
- **Timeline**: "As soon as possible" — aim for within 72 hours in practice (align with GDPR timeline)
- **Content**: Description of the breach; categories and approximate number of affected data subjects and records; likely consequences; measures taken or proposed
- **FDPIC portal**: Report via edoeb.admin.ch; confirm current reporting procedure
- **Individual notification**: Required without undue delay if necessary for the protection of affected persons

### GDPR DPA Notification (if EU data involved)
- **Timeline**: 72 hours from awareness to competent EU supervisory authority
- **Two-stage approach common**: Initial notification within 72h with available information; supplement when more details are known
- **Individual notification**: Without undue delay if high risk to data subjects

### Post-Breach Documentation
- Maintain internal breach register (required under GDPR Art. 33(5); best practice under nDSG)
- Document decision-making process (why notification was or was not required)
- Preserve all evidence (attorney-client privilege where possible)
- Coordinate with FINMA if organization is supervised
