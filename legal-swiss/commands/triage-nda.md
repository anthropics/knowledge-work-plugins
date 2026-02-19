---
description: Rapidly triage an incoming NDA — classify as standard approval, counsel review, or full legal review
argument-hint: "<NDA file or text>"
---

# /triage-nda -- NDA Pre-Screening (Swiss)

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Rapidly triage incoming NDAs (Geheimhaltungsvereinbarungen / NDA / accord de confidentialité) against standard Swiss-law screening criteria. Classify the NDA for routing: standard approval, counsel review, or full legal review.

**Swiss legal context**: Swiss NDAs are typically governed by the Swiss Code of Obligations (OR/CO). Key considerations include:
- Confidentiality obligations for employees are mandatory under OR Art. 321a regardless of any NDA
- Non-solicitation and non-compete provisions embedded in NDAs are governed by OR Art. 340-340c if they affect employees, and are strictly limited
- Swiss courts generally enforce reasonable NDAs but will not enforce unreasonably broad or perpetual obligations
- The Vienna Convention (CISG) does not apply to NDA-type agreements; Swiss OR governs
- Injunctive relief (superprovisorische Massnahme / vorsorgliche Massnahme) is available under ZPO Art. 261ff. for NDA breaches
- Swiss arbitration (SCAI / Swiss Chambers' Arbitration Institution, or ICC with Swiss seat) is preferred over cantonal courts for international NDAs

**Important**: This command assists with legal workflows but does not provide legal advice. All analysis should be reviewed by qualified Swiss legal professionals before being relied upon.

## Invocation

```
/triage-nda
```

## Workflow

### Step 1: Accept the NDA

Accept the NDA in any format:
- **File upload**: PDF, DOCX, or other document format
- **URL**: Link to the NDA in a document system
- **Pasted text**: NDA text pasted directly

If no NDA is provided, prompt the user to supply one.

Also collect:
- **Counterparty jurisdiction**: Swiss entity (AG/GmbH/other)? EU entity? Other?
- **Business purpose**: What is the information to be shared for?
- **Data involved**: Does the NDA cover personal data (Personendaten under nDSG Art. 5(a))? If so, note that nDSG obligations apply in addition to the NDA

### Step 2: Load NDA Playbook

Look for NDA screening criteria in local settings (e.g., `legal.local.md`).

The NDA playbook should define:
- Mutual vs. unilateral requirements
- Acceptable term lengths under Swiss practice
- Required carveouts (per Swiss OR and commercial practice)
- Prohibited provisions (particularly competition clauses)
- Swiss law and jurisdiction requirements
- Approval thresholds and signing authority (per Handelsregister / Zeichnungsberechtigung)

**If no NDA playbook is configured:**
- Proceed with Swiss market-standard defaults (described below)
- Note clearly that defaults are being used
- **Swiss defaults applied**:
  - Mutual obligations required (unless the organization is only disclosing)
  - Term: 2-3 years standard; trade secrets (Geschäftsgeheimnisse) may warrant longer but not perpetual
  - Standard Swiss-law carveouts required (see Step 3)
  - No non-solicitation or non-compete provisions (governed by OR Art. 340-340c for employment context; out of place in a commercial NDA)
  - No residuals clause (or narrowly scoped to unaided memory only)
  - Governing law: Swiss OR (Canton of [Zurich / Geneva / other as appropriate])
  - Dispute resolution: Swiss cantonal courts or SCAI arbitration
  - Language: German, French, or English as appropriate

### Step 3: Quick Screen

Evaluate the NDA against each Swiss-law screening criterion:

| Criterion | Swiss-Law Check |
|-----------|-----------------|
| **Mutual vs. Unilateral** | Are obligations mutual? If unilateral, is that appropriate for the relationship and does the disclosing party have legitimate interests? |
| **Definition of Confidential Information** | Reasonable scope under Swiss commercial practice? Not so broad as to capture publicly available information? |
| **Term** | Within acceptable Swiss range? Reasonable for the type of information? (2-3 years for general commercial info; longer for technical trade secrets) |
| **Standard Carveouts** | All required Swiss carveouts present? (independent development, public knowledge, prior possession, third-party receipt, legal compulsion) |
| **Permitted Disclosures** | Can share with employees (note OR Art. 321a employees already have statutory confidentiality duties), advisors, contractors with need to know? |
| **Return/Destruction** | Reasonable obligations on termination? Allows retention of copies required by law, compliance, or backup policy? |
| **Residuals** | If present, limited to unaided memory only? Does not apply to trade secrets or technical information? |
| **Non-Solicitation** | Any non-solicit provisions? — Flag for Swiss OR Art. 340-340c analysis (employment-specific rules) |
| **Non-Compete** | Any non-compete provisions? — Flag: governed by OR Art. 340-340c if employee involved; in commercial NDAs, non-competes should not appear |
| **Injunctive Relief** | Mutual? Swiss ZPO Art. 261ff. already provides for vorsorgliche Massnahmen — contractual acknowledgment is standard |
| **Governing Law** | Swiss OR preferred for Swiss parties; for international NDAs, Swiss law is favorable; flag if highly unfavorable foreign law |
| **Jurisdiction / Arbitration** | Swiss cantonal courts or SCAI/ICC arbitration? Flag mandatory conciliation (Schlichtungsverfahren) requirement under ZPO Art. 197ff. if litigation track |
| **Unusual Provisions** | Any non-standard clauses: exclusivity, audit rights, IP assignment, liquidated damages, penalty clauses (Konventionalstrafe under OR Art. 160)? |
| **nDSG / Data Protection** | If personal data is to be shared under the NDA, does the NDA address nDSG obligations? (A standalone DPA/AV-Vereinbarung may be needed) |

### Step 4: Classify

Based on the screening results, assign a classification:

#### GREEN -- Standard Approval
All criteria met. NDA is Swiss-market-standard with no unusual provisions.
- **Route**: Can be approved and signed via standard process per Unterschriftenregelung (signing authority matrix)
- **Action**: Proceed to signature; ensure Handelsregister authority is confirmed for signatories on both sides
- **Note**: File executed copy in CLM with expiry reminder set

#### YELLOW -- Counsel Review Needed
One or more criteria have minor deviations that need review but are potentially acceptable:
- Definition of confidential information is broader than ideal but not unreasonable under Swiss practice
- Term is longer than standard (4-5 years) but within Swiss market range for the information type
- Residuals clause present but limited to unaided memory with explicit trade secret carveout
- Minor jurisdiction preference issue (e.g., Geneva vs. Zurich — both acceptable Swiss forums)
- Missing one standard carveout that can easily be added
- Governing law is foreign (EU/UK) but the NDA is for a European counterparty (acceptable but needs review)
- **Route**: Flag specific issues for counsel review
- **Action**: Counsel can likely resolve in a single review pass; typical turnaround 1-2 business days

#### RED -- Significant Issues
One or more criteria have material deviations that pose risk under Swiss law:
- Unilateral obligations when mutual is required
- Missing critical carveouts (especially independent development or legal compulsion)
- Non-solicitation or non-compete provisions embedded without OR Art. 340-340c compliance
- Unreasonable term (10+ years) or perpetual obligations beyond trade secret scope
- Overbroad definition that could capture public information or independently developed materials
- Broad residuals clause effectively licensing confidential information
- Liquidated damages / Konventionalstrafe clause that is unreasonably high (OR Art. 163 court may reduce)
- Audit rights without reasonable scope or notice
- IP assignment or license grant hidden in the NDA
- Highly unfavorable foreign jurisdiction with mandatory arbitration in an inconvenient seat
- **The document is not actually a standalone NDA** (contains commercial terms, exclusivity, IP, payment, or other substantive obligations)
- nDSG-sensitive data (besonders schützenswerte Personendaten) will be shared but the NDA has no data protection provisions
- **Route**: Full legal review required
- **Action**: Do not sign; requires negotiation, Swiss-law counterproposal, or rejection

### Step 5: Generate Triage Report

Output a structured report:

```
## NDA Triage Report / NDA-Prüfungsbericht

**Classification / Klassifikation**: [GREEN / YELLOW / RED]
**Parties / Parteien**: [party names, legal forms (AG/GmbH), cantons/jurisdictions]
**Type / Typ**: [Mutual / Unilateral (disclosing) / Unilateral (receiving)]
**Term / Dauer**: [agreement term] / [confidentiality survival period]
**Governing Law / Anwendbares Recht**: [Swiss OR / Canton X / Foreign law]
**Dispute Resolution / Streitbeilegung**: [Cantonal courts / SCAI arbitration / ICC / other]
**Contract Language / Vertragssprache**: [German / French / Italian / English]
**Review Basis**: [Playbook / Swiss Market-Standard Defaults]

## Screening Results / Prüfungsresultate

| Criterion / Kriterium | Status | Notes / Anmerkungen |
|-----------|--------|-------|
| Mutual Obligations | [PASS/FLAG/FAIL] | [details] |
| Definition Scope | [PASS/FLAG/FAIL] | [details] |
| Term / Dauer | [PASS/FLAG/FAIL] | [details] |
| Standard Carveouts | [PASS/FLAG/FAIL] | [details] |
| Non-Compete / Non-Solicit | [PASS/FLAG/FAIL] | [details + OR Art. reference if flagged] |
| Governing Law | [PASS/FLAG/FAIL] | [details] |
| nDSG / Data Protection | [PASS/FLAG/FAIL] | [details] |
| [etc.] | | |

## Issues Found / Festgestellte Probleme

### [Issue 1 -- YELLOW/RED]
**What / Was**: [description]
**Swiss Law Risk / Schweizer Rechtsrisiko**: [what could go wrong; applicable OR/nDSG provision]
**Suggested Fix / Empfohlene Lösung**: [specific language or approach]

[Repeat for each issue]

## Recommendation / Empfehlung

[Specific next step: approve, send for review with specific notes, or reject/counter]
[If RED: recommend sending organization's Swiss-law standard form NDA as counterproposal]

## Signature Authority Check / Zeichnungsberechtigungsprüfung

[Confirm that counterparty signatories have authority per Handelsregister / commercial register]
[Note if Kollektivunterschrift (joint signature) is required]

## Next Steps / Nächste Schritte

1. [Action item 1]
2. [Action item 2]
```

### Step 6: Routing Suggestion

Based on the classification:
- **GREEN**: Proceed to signature per Unterschriftenregelung; confirm Handelsregister authority; file in CLM with expiry reminder
- **YELLOW**: Send to designated reviewer with specific issues flagged; include suggested redlines in the contract language; typical timeline 1-2 business days
- **RED**: Engage Swiss counsel for full review; prepare counterproposal using the organization's Swiss-law standard NDA form; do not sign until resolved

## Notes

- If the document is not actually a standalone NDA (contains exclusivity, pricing, IP rights, or other commercial terms), flag as RED and recommend full contract review under /review-contract
- For NDAs that are part of a larger Swiss law agreement (e.g., Vertraulichkeitsklausel in an MSA), note that the broader agreement context and OR provisions affect the analysis
- For M&A / Unternehmenskauf context: NDAs should include standstill provisions and may be subject to special regulatory considerations (e.g., FINMA prior approval if financial institutions involved)
- Always note that this is a screening tool and qualified Swiss counsel should review any items the user is uncertain about
- Swiss tip: File the executed NDA in the Handelsregister-verified counterparty's folder and set calendar reminders for (a) the end of the NDA term, (b) any auto-renewal dates, and (c) the confidentiality survival period expiry
