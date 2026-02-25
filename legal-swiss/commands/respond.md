---
description: Generate a response to a common legal inquiry using configured templates
argument-hint: "[inquiry-type]"
---

# /respond -- Generate Response from Templates (Swiss)

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate a response to a common legal inquiry using configured templates. Customizes the response with specific details and includes escalation triggers for situations that should not use a templated response.

**Swiss legal context**: Responses must comply with Swiss law defaults — nDSG for data protection matters, OR/ZGB for contract matters, and ZPO for procedural matters. Where EU individuals are involved, GDPR requirements may also apply in parallel. The supervisory authority for Swiss data protection is the FDPIC (Federal Data Protection and Information Commissioner / Eidgenössischer Datenschutz- und Öffentlichkeitsbeauftragter / Préposé fédéral à la protection des données et à la transparence).

**Important**: This command assists with legal workflows but does not provide legal advice. Generated responses should be reviewed by qualified Swiss legal professionals (Rechtsanwalt / avocat / avvocato) before being sent. Note that in-house counsel in Switzerland generally do not hold attorney-client privilege (Anwaltsgeheimnis) — privilege applies only to admitted attorneys.

## Invocation

```
/respond [inquiry-type]
```

Common inquiry types:
- `dsr` or `data-subject-request` -- Data subject access/deletion/correction requests (nDSG / GDPR)
- `hold` or `litigation-hold` -- Litigation hold / Beweissicherungsanordnung notices
- `vendor` or `vendor-question` -- Vendor legal questions
- `nda` or `nda-request` -- NDA requests from business teams
- `privacy` or `privacy-inquiry` -- Privacy-related questions (nDSG / GDPR)
- `subpoena` or `editionsverfügung` -- Court production orders / subpoenas (ZPO / IMAC)
- `insurance` -- Insurance claim notifications (cyber, D&O, general liability)
- `fdpic` -- Response to FDPIC inquiry or consultation
- `custom` -- Use a custom template

If no inquiry type is provided, ask the user what type of response they need and show available categories.

## Workflow

### Step 1: Identify Inquiry Type

Accept the inquiry type from the user. If the type is ambiguous, show available categories and ask for clarification.

### Step 2: Load Template

Look for templates in local settings (e.g., `legal.local.md` or a templates directory).

**If templates are configured:**
- Load the appropriate template for the inquiry type
- Identify required variables (recipient name, dates, specific details)
- Note the language requirement (German / French / Italian / English) based on the recipient's jurisdiction and the contract language clause

**If no templates are configured:**
- Inform the user that no templates were found for this inquiry type
- Offer to help create a template (see Step 6)
- Provide a reasonable default response structure based on the inquiry type and Swiss law

### Step 3: Check Escalation Triggers

Before generating the response, evaluate whether this situation has characteristics that should NOT use a templated response:

#### Data Subject Request Escalation Triggers (nDSG / GDPR)
- Request involves a minor's (Minderjährige) data
- Request is from the FDPIC, a cantonal supervisory authority, or other regulatory authority (not an individual data subject)
- Request involves data that is subject to a litigation hold (Beweissicherung)
- Requester is a current or former employee with an active dispute (HR matter, employment tribunal)
- Request scope is unusually broad or appears to be preparatory to litigation
- Request involves data processed in a jurisdiction with unique requirements (e.g., China PIPL, Russia)
- Request involves sensitive data (besonders schützenswerte Personendaten under nDSG Art. 5(c): health, religion, ethnicity, political opinions, criminal records, biometric, genetic data)
- Conflicting obligations: GDPR 30-day deadline vs. nDSG 30-day deadline both apply

#### Litigation Hold Escalation Triggers
- The matter involves potential criminal liability under Swiss Criminal Code (StGB) or special criminal statutes
- The preservation scope is unclear or potentially conflicts with nDSG/GDPR deletion obligations
- Prior holds for the same or related matter exist (risk of inconsistency)
- The hold may affect ongoing business operations significantly
- The matter involves a ZPO Vorsorgliche Massnahme (interim measure) or Beweissicherungsklage (evidence preservation action)
- Cross-border e-discovery with US litigation (Swiss bank secrecy / Bankgeheimnis or blocking statute concerns)

#### Vendor Question Escalation Triggers
- The question involves a dispute or potential breach under Swiss OR Art. 97ff.
- The vendor is threatening litigation or extraordinary termination (ausserordentliche Kündigung)
- The question involves FINMA regulatory compliance (if vendor is a financial institution or FINMA-supervised entity)
- The response could create a binding commitment (Vertragsangebot) under OR Art. 3ff. or a waiver
- The vendor holds sensitive personal data and the question touches on nDSG/GDPR compliance

#### NDA Request Escalation Triggers
- The counterparty is a competitor (WEKO/competition law implications of information sharing)
- The NDA is for a potential M&A / Unternehmensübernahme transaction
- The NDA involves government-classified or national security information
- The request involves unusual subject matter (AI training data, biometric data under nDSG Art. 5(c))
- The NDA purports to be governed by foreign law (review if Swiss mandatory provisions are displaced)

#### FDPIC / Regulatory Inquiry Escalation Triggers
- **Always escalate to outside counsel for FDPIC sachverhaltsabklärungen (fact-finding inquiries) or Empfehlungen (recommendations)**
- Any FINMA enforcement or supervisory correspondence
- Any WEKO/COMCO competition authority inquiry

**If an escalation trigger is detected:**
- Alert the user that this situation may not be appropriate for a templated response
- Explain which trigger was detected and why it matters under Swiss law
- Recommend the user consult with a senior team member or qualified Swiss outside counsel
- Offer to draft a preliminary response for counsel review rather than a final response
- Note if Anwaltsgeheimnis (attorney privilege) should be established by routing through outside counsel

### Step 4: Gather Specific Details

Prompt the user for the details needed to customize the response:

**Data Subject Request (nDSG / GDPR):**
- Requester name, address, and identification
- Type of request: access (Auskunft, nDSG Art. 25), rectification (Berichtigung), deletion (Löschung), restriction of processing, portability, objection
- What data is involved and in which systems
- **Applicable regulation**: Swiss nDSG (if requester is in Switzerland), EU GDPR (if requester is EU/EEA resident), or both
- Response deadline:
  - nDSG: 30 days from receipt (extendable with justification, nDSG Art. 25 para. 7)
  - GDPR: 30 days from receipt (extendable by 60 days for complex requests with notice)
- FDPIC registration or prior inquiries on file?

**Litigation Hold:**
- Matter name and reference number (Geschäftsnummer)
- Custodians (Verwahrer) — who needs to preserve
- Scope of preservation: date range, data types, systems (email, chat, shared drives, devices)
- Outside counsel (externe Anwaltskanzlei) contact and privilege considerations
- Effective date and acknowledgment deadline
- Note: Swiss ZPO Art. 261ff. governs interim measures including evidence preservation; OR Art. 55 burden of proof considerations

**Vendor Question:**
- Vendor name and registered address (Handelsregister-Eintrag if available)
- Reference agreement (including governing law — Swiss OR vs. foreign law)
- Specific question being addressed
- Relevant contract provisions (cite article numbers if Swiss OR-governed)

**NDA Request:**
- Requesting business team and contact
- Counterparty name, legal form (AG/GmbH/etc.), and jurisdiction of incorporation
- Purpose of the NDA (Vertraulichkeitszweck)
- Mutual (gegenseitig) or unilateral (einseitig); if unilateral, which party discloses
- Proposed governing law (recommend Swiss OR if counterparty is Swiss)
- Any special requirements (trade secrets, regulatory data, pricing information)

### Step 5: Generate Response

Populate the template with the gathered details. Ensure the response:
- Uses appropriate language (German / French / Italian / English based on relationship and contract terms)
- Uses professional Swiss legal tone: formal, precise, and unambiguous
- Includes all required legal elements for the response type under Swiss law
- References specific dates, deadlines, and obligations with the correct statutory basis
- For data protection responses: cites nDSG provisions (and GDPR provisions if applicable)
- Provides clear next steps for the recipient
- Includes appropriate disclaimers or caveats
- Notes any Anwaltsgeheimnis considerations

Present the draft response to the user for review before sending.

### Step 6: Template Creation (If No Template Exists)

If the user wants to create a new template:

1. Ask what type of inquiry the template is for
2. Ask which language(s) the template will be used in (German / French / Italian / English)
3. Ask for key elements that should be included, including applicable Swiss law provisions
4. Ask for tone and audience (internal vs. external, business vs. legal, individual vs. regulatory authority)
5. Draft a template with variable placeholders (e.g., `{{empfaenger_name}}`, `{{frist_datum}}`, `{{aktenzeichen}}`)
6. Include escalation triggers appropriate for the category under Swiss law
7. Present the template for review
8. Suggest the user save the approved template to their local settings for future use

#### Swiss Template Format

```markdown
## Template: [Category Name] / [Vorlagename]

### Applicable Law
- [Swiss nDSG / OR / ZPO / etc.]
- [GDPR if EU data involved]

### Escalation Triggers
- [Trigger 1]
- [Trigger 2]

### Variables
- {{variable_1}}: [description / Beschreibung]
- {{variable_2}}: [description / Beschreibung]

### Subject Line / Betreff
[Subject template]

### Body / Text
[Response body with {{variables}}]

### Required Enclosures / Beilagen
[Any standard documents to include]

### Follow-Up / Folgenmassnahmen
[Standard follow-up actions after sending, including statutory tracking obligations]

### Statutory Basis / Rechtsgrundlage
[Cite specific articles: nDSG Art. X, OR Art. Y, etc.]
```

## Output Format

```
## Generated Response: [Inquiry Type]

**To / An**: [recipient / Empfänger]
**Subject / Betreff**: [subject line]
**Language / Sprache**: [German / French / Italian / English]
**Statutory Basis / Rechtsgrundlage**: [nDSG Art. X / OR Art. Y / etc.]

---

[Response body]

---

### Escalation Check / Eskalationsprüfung
[Confirmation that no escalation triggers were detected, OR flagged triggers with recommendations]

### Response Deadline / Frist
[Applicable statutory deadline with basis; calendar reminder recommended]

### Follow-Up Actions / Folgenmassnahmen
1. [Post-send actions]
2. [Calendar/Frist reminders to set — note Swiss Fristenberechnung rules under ZPO Art. 142ff.]
3. [Tracking or logging requirements, e.g., nDSG data subject request log]
```

## Notes

- Always present the draft response for user review before suggesting it be sent
- If connected to email via MCP, offer to create a draft email with the response
- For nDSG data subject requests: recommend maintaining a request log (Auskunftsbegehren-Register) for compliance documentation
- For regulated responses (DSRs, FDPIC inquiries, ZPO production orders), always note the applicable deadline and statutory requirements
- Templates should be maintained in the applicable official language(s) of Switzerland; if the organization operates in multiple language regions, maintain parallel German / French versions at minimum
- Swiss professional standard: responses to regulators (FDPIC, FINMA) should always be routed through qualified outside counsel (Rechtsanwalt / avocat) to ensure Anwaltsgeheimnis protection
