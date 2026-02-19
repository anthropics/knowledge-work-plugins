---
description: Review a contract against your organization's negotiation playbook — flag deviations, generate redlines, provide business impact analysis
argument-hint: "<contract file or text>"
---

# /review-contract -- Contract Review Against Playbook (Swiss)

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Review a contract against your organization's negotiation playbook. Analyze each clause, flag deviations, generate redline suggestions, and provide business impact analysis.

**Swiss legal framework**: Swiss contracts are primarily governed by the Code of Obligations (Obligationenrecht / OR / CO), the Civil Code (ZGB/CC), and sector-specific statutes. Key mandatory provisions that cannot be contracted away include:
- **OR Art. 100**: Cannot exclude liability for gross negligence (grobe Fahrlässigkeit) or intentional acts (Absicht); Art. 100 para. 2 allows exclusion of simple negligence only for non-regulated employment-type relationships
- **OR Art. 101**: Liability for auxiliary persons (Hilfspersonen) cannot be pre-excluded for intentional acts/gross negligence
- **OR Art. 19/20**: Contracts contrary to Swiss law, public policy (öffentliche Ordnung), or morality (Sittlichkeit) are void
- **nDSG**: Data protection obligations cannot be waived by contract

**Important**: This command assists with legal workflows but does not provide legal advice. All analysis should be reviewed by qualified Swiss legal professionals (Rechtsanwalt / avocat / avvocato) before being relied upon.

## Invocation

```
/review-contract
```

## Workflow

### Step 1: Accept the Contract

Accept the contract in any of these formats:
- **File upload**: PDF, DOCX, or other document format
- **URL**: Link to a contract in your CLM, cloud storage (e.g., SharePoint, OneDrive), or document system
- **Pasted text**: Contract text pasted directly into the conversation

If no contract is provided, prompt the user to supply one.

### Step 2: Gather Context

Ask the user for context before beginning the review:

1. **Which side are you on?** (Verkäufer/Lieferant, Käufer/Kunde, Lizenzgeber, Lizenznehmer, Partner — or other)
2. **Governing law**: Is this Swiss OR? Foreign law? Or unclear? (If foreign law, flag early — different mandatory provisions may apply)
3. **Contract language**: German / French / Italian / English? If not in the user's primary working language, translation may be needed for court proceedings
4. **Deadline**: When does this need to be finalized? (Affects prioritization)
5. **Focus areas**: Any specific concerns? (e.g., "data protection under nDSG is critical", "liability cap under OR Art. 100 concerns", "IP ownership under URG")
6. **Deal context**: CHF value, strategic importance, existing relationship, counterparty location (Switzerland / EU / other)
7. **Entity type**: Is the counterparty a Swiss AG/GmbH/other? Check Handelsregister entry for authority to sign

If the user provides partial context, proceed with what you have and note assumptions.

### Step 3: Load the Playbook

Look for the organization's contract review playbook in local settings (e.g., `legal.local.md`).

The playbook should define:
- **Standard positions**: The organization's preferred terms for each major clause type under Swiss law
- **Acceptable ranges**: Terms that can be agreed to without escalation
- **Escalation triggers**: Terms that require senior counsel review or outside Swiss counsel involvement
- **CHF thresholds**: Deal values that trigger different approval requirements

**If no playbook is configured:**
- Inform the user that no playbook was found
- Offer two options:
  1. Help set up a Swiss-law playbook
  2. Proceed with Swiss commercial market standards as the baseline
- If proceeding generically, clearly note the review is based on Swiss commercial practice, not organizational positions

### Step 4: Clause-by-Clause Analysis

Analyze the contract systematically, covering at minimum:

| Clause Category | Key Review Points (Swiss Law) |
|----------------|-------------------------------|
| **Limitation of Liability** | Cap amount (in CHF); OR Art. 100 mandatory floor (cannot exclude gross negligence/intent); mutual vs. unilateral; consequential damages exclusion validity under Swiss law |
| **Indemnification** | Scope; Swiss OR framework for indemnification (Schadloshaltung / garantie); cap; relation to OR Art. 101; procedure |
| **IP Ownership** | Pre-existing IP; work-for-hire (Swiss law: URG default is creator owns, not employer); license grants under URG; software: whether source code escrow needed |
| **Data Protection** | nDSG compliance; DPA/AV-Vereinbarung required if processor relationship; GDPR applicability (EU data subjects); FDPIC notification obligations; cross-border transfer mechanisms |
| **Confidentiality** | Scope; duration (Swiss courts enforce reasonable terms); standard carveouts; return/destruction; Note: Swiss employees have confidentiality duties under OR Art. 321a regardless |
| **Representations & Warranties** | Scope; Swiss warranty (Gewährleistung) rules under OR Art. 197ff. (sale) or Art. 367ff. (works contracts); contractual modification permitted within OR framework |
| **Term & Termination** | Duration; auto-renewal (automatische Verlängerung); notice periods (Kündigungsfristen); termination for cause (ausserordentliche Kündigung) under OR Art. 97; wind-down |
| **Governing Law & Dispute Resolution** | Swiss OR preferred; arbitration under Swiss Rules (SCAI) or ICC (Swiss seat) vs. cantonal courts; mandatory conciliation (Schlichtungsverfahren) under ZPO Art. 197ff. if litigation |
| **Insurance** | Coverage requirements; Swiss market norms; CHF minimums; evidence of coverage (Versicherungsbestätigung) |
| **Assignment** | Consent requirements; change of control; OR Art. 164ff. (assignment of claims); Note: Swiss law requires counterparty consent for assignment of contractual position unless otherwise agreed |
| **Force Majeure** | Scope; OR Art. 119 (Nachträgliche Unmöglichkeit); Swiss courts apply narrowly; COVID/supply chain precedents |
| **Payment Terms** | CHF or multi-currency; Swiss late payment interest (OR Art. 104: statutory 5% p.a.); MWST/VAT clause; MWST number (UID) references |
| **Competition / Non-Compete** | Swiss competition law (KG/LCart); WEKO implications; employee non-competes strictly regulated under OR Art. 340-340c |
| **Swiss-Specific Clauses** | AGB (General Terms) incorporation validity (OR Art. 1/8); entire agreement (Vollständigkeitsklausel); amendment formalities; signature authority (Handelsregister / Zeichnungsberechtigung) |

For each clause, assess against the playbook (or Swiss market standards) and note whether it is present, absent, or unusual.

### Step 5: Flag Deviations

Classify each deviation from the playbook using a three-tier system:

#### GREEN -- Acceptable
- Aligns with or is better than the organization's standard position under Swiss law
- Minor variations that are commercially reasonable
- No action needed; note for awareness

#### YELLOW -- Negotiate
- Falls outside standard position but within negotiable range under Swiss practice
- Common in the Swiss market but not the organization's preference
- Requires attention but not escalation
- **Include**: Specific redline language to bring the term back to standard position (in the contract language)
- **Include**: Fallback position if counterparty pushes back
- **Include**: Business impact of accepting as-is vs. negotiating

#### RED -- Escalate
- Falls outside acceptable range or conflicts with Swiss mandatory law (OR Art. 100, nDSG mandatory provisions, etc.)
- Unusual or aggressive terms that pose material risk under Swiss law
- Requires senior counsel review, outside Swiss counsel involvement, or business decision-maker sign-off
- **Include**: Why this is a RED flag (specific Swiss law risk)
- **Include**: Market-standard Swiss position
- **Include**: Business impact and potential CHF exposure
- **Include**: Recommended escalation path

### Step 6: Generate Redline Suggestions

For each YELLOW and RED deviation, provide:
- **Current language**: Quote the relevant contract text
- **Suggested redline**: Specific alternative language (in the contract's language — German / French / Italian / English)
- **Swiss law basis**: Cite the applicable OR/ZGB/nDSG provision if relevant
- **Rationale**: Brief explanation suitable for sharing with the counterparty's counsel
- **Priority**: Must-have / Should-have / Nice-to-have

### Step 7: Business Impact Summary

Provide a summary section covering:
- **Overall risk assessment**: High-level view of the contract's risk profile under Swiss law
- **OR Art. 100 compliance**: Confirm whether limitation of liability clauses comply with Swiss mandatory law
- **nDSG/GDPR compliance**: Confirm whether data protection provisions are adequate
- **Top 3 issues**: The most important items to address
- **Negotiation strategy**: Recommended approach for Swiss commercial negotiations (direct, precise, relationship-conscious)
- **CHF exposure**: Estimated maximum financial exposure under the contract
- **Timeline considerations**: Urgency factors; note any Verjährungsfristen (limitation periods) that may be running

### Step 8: Execution Checklist

Before signing, verify:
- [ ] Signatories have authority per Handelsregister (Zeichnungsberechtigung)
- [ ] Kollektivunterschrift (joint signature) requirements met if applicable
- [ ] Contract language agreed and any translation protocol established
- [ ] Stamped/dated originals required? (Swiss practice for certain contract types)
- [ ] MWST/VAT clauses correctly drafted if applicable
- [ ] nDSG AV-Vereinbarung (Data Processing Agreement) required and drafted?
- [ ] Insurance certificates obtained if required

### Step 9: CLM Routing (If Connected)

If a Contract Lifecycle Management system is connected via MCP:
- Recommend the appropriate approval workflow based on contract type, CHF value, and risk level
- Suggest the correct routing path per the organization's Unterschriftenregelung (signing authority matrix)
- Note any required approvals based on contract value or risk flags

## Output Format

```
## Contract Review Summary / Vertragsprüfung

**Document / Dokument**: [contract name/identifier]
**Parties / Parteien**: [party names, legal forms, and jurisdictions]
**Your Side / Ihre Position**: [vendor/customer/etc.]
**Governing Law / Anwendbares Recht**: [Swiss OR / Foreign law]
**Contract Language / Vertragssprache**: [German / French / Italian / English]
**Deadline / Frist**: [if provided]
**CHF Exposure**: [estimated maximum]
**Review Basis**: [Playbook / Swiss Commercial Standards]

## Key Findings / Hauptbefunde

[Top 3-5 issues with severity flags]

## OR Art. 100 / Liability Cap Compliance
[Explicit confirmation or issue with Swiss mandatory limitation of liability rules]

## Data Protection / Datenschutz
[nDSG and GDPR compliance assessment]

## Clause-by-Clause Analysis / Klauselanalyse

### [Clause Category] -- [GREEN/YELLOW/RED]
**Contract says / Vertragstext**: [summary of the provision]
**Swiss standard position**: [market standard or playbook position]
**Swiss law basis**: [OR Art. X / nDSG Art. Y / etc., if applicable]
**Deviation / Abweichung**: [description of gap]
**Business impact / Geschäftliche Auswirkung**: [what this means practically in CHF and operational terms]
**Redline suggestion**: [specific language, if YELLOW or RED]

[Repeat for each major clause]

## Negotiation Strategy / Verhandlungsstrategie

[Recommended approach; Swiss negotiation culture note: direct, written record preferred, focus on precision]

## Execution Checklist / Unterzeichnungsprüfung

[Handelsregister check, signature authority, MWST, nDSG AV-Vereinbarung, etc.]

## Next Steps / Nächste Schritte

[Specific actions to take]
```

## Notes

- If the contract is in German, French, or Italian, review in the original language; do not rely solely on unofficial translations
- For very long contracts (50+ pages), offer to focus on the most material sections first
- Always remind the user that this analysis should be reviewed by qualified Swiss legal counsel (Rechtsanwalt / avocat / avvocato) before being relied upon
- Swiss contract law tip: Oral modifications may be binding under OR Art. 115 unless the contract requires written amendments — flag if the contract lacks a written amendment clause
- For contracts with international counterparties, check whether the Vienna Convention on the International Sale of Goods (CISG / CISG) applies (Switzerland is a signatory) and whether it should be excluded
