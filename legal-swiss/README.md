# Legal Productivity Plugin — Swiss Edition (nDSG / OR / ZGB)

An AI-powered productivity plugin for in-house legal teams operating under **Swiss law**. Designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — and works in Claude Code. Automates contract review, NDA triage, compliance workflows, legal briefings, and templated responses, all calibrated to Swiss mandatory law, Swiss court practice, and the FDPIC/EDÖB supervisory framework.

**Swiss law foundation:**
- **OR** (Obligationenrecht / Code des obligations) — primary contract law
- **nDSG** (Bundesgesetz über den Datenschutz, in force 1 September 2023) — data protection
- **ZGB** (Zivilgesetzbuch) — civil law, entity and capacity matters
- **ZPO** (Zivilprozessordnung) — civil procedure, evidence holds, injunctions
- **IPRG** — private international law, choice of law analysis
- **URG** (Urheberrechtsgesetz) — Swiss copyright; creator retains rights by default
- **FINMA** — financial market regulation (outsourcing: Circular 2023/1)
- **WEKO / KG** — Swiss Competition Commission; cartel law Art. 5, 7
- **VVG** (Versicherungsvertragsgesetz) — Swiss insurance; VVG Art. 38 prompt notification

**Three-language environment supported:** German (DE) · French (FR) · Italian (IT) · English (EN)

> **Disclaimer:** This plugin assists with legal workflows but does not provide legal advice. All outputs should be reviewed by a qualified Swiss attorney (*Rechtsanwalt / avocat / avvocato*, SAV/FSA admitted) before being relied upon. In-house counsel communications are **not** protected by Anwaltsgeheimnis — route sensitive regulatory matters through external Swiss counsel.

---

## Target Personas

- **Commercial Counsel** — Contract negotiation, vendor management, OR-based deal support
- **Product Counsel** — Product reviews, AGB, privacy notices under nDSG/GDPR, IP matters
- **Privacy / Compliance** — nDSG/GDPR compliance, AV-Vereinbarung reviews, Auskunftsbegehren (DSR), FDPIC monitoring
- **Litigation Support** — ZPO Beweissicherung, document holds, cantonal court briefings

---

## Installation

```
claude plugins add knowledge-work-plugins/legal-swiss
```

---

## Quick Start

### 1. Install the plugin

```
claude plugins add knowledge-work-plugins/legal-swiss
```

### 2. Configure your Swiss playbook

Create a local settings file to encode your team's Swiss-law negotiation positions and risk tolerances.

In your project's `.claude/` directory, create `legal.local.md`:

```markdown
# Swiss Legal Playbook Configuration

## Contract Review Positions (Swiss OR basis)

### Haftungsbeschränkung / Limitation of Liability
- Standard position: Mutual cap at 12 months of fees paid/payable
- Acceptable range: 6–24 months fees
- Escalation trigger: Exclusion of gross negligence or intent (void under OR Art. 100)
- OR Art. 100 note: Any clause excluding liability for Absicht or grobe Fahrlässigkeit
  is mandatory-law void — always require a savings clause

### Freistellung / Indemnification
- Standard position: Mutual indemnification for IP infringement and data breach
- Acceptable: Third-party claims only, proportionate to fault
- Escalation trigger: Unilateral indemnification; uncapped; includes own costs

### Geistiges Eigentum / IP Ownership
- Standard position: Each party retains pre-existing IP; customer owns deliverables
- Swiss note: URG default = creator retains copyright (no automatic work-for-hire)
- Escalation trigger: Broad IP assignment; reverse assignment of customer improvements;
  use of customer data for AI training without explicit nDSG-compliant consent

### Datenschutz / Data Protection
- Standard position: AV-Vereinbarung (nDSG Art. 9 / GDPR Art. 28) required for any
  personal data processing
- Requirements:
  - Sub-processor change notification right (not just general consent)
  - Breach notification ≤ 72 h to controller (enabling FDPIC and GDPR notification)
  - Data deletion within 30 days of contract termination
  - Audit rights including periodic on-site review
  - SCCs (June 2021 EU SCCs or Swiss addendum) for transfers to USA/India/non-adequate countries
- FDPIC adequacy list: EU/EEA + listed countries only; USA and India require SCCs
- Escalation trigger: No AV-Vereinbarung; blanket sub-processor consent; 14-day
  breach notification (prevents compliance); "internal policies" as transfer safeguard

### Vertragsdauer und Kündigung / Term and Termination
- Standard position: 1-year term; Kündigung für Convenience with 90-day notice
- Acceptable: Multi-year with termination for convenience after initial year
- Escalation trigger: Asymmetric termination rights; early termination fee = full
  remaining term; no termination for convenience for customer

### Anwendbares Recht und Gerichtsstand / Governing Law and Jurisdiction
- Preferred: Swiss law (OR); courts of Zürich (Handelsgericht ZH) or agreed canton
- Acceptable: SCAI arbitration (Swiss Rules of International Arbitration) for
  cross-border commercial disputes
- Escalation trigger: Non-Swiss governing law without IPRG analysis; mandatory
  arbitration in foreign seat; CISG not excluded

## NDA Defaults (Swiss OR basis)
- Mutual obligations required
- Term: 2–3 years standard; up to 5 years for trade secrets
- Required carveouts (OR-aligned):
  1. Independently developed without use of CI
  2. Already publicly available at disclosure
  3. Rightfully received from a third party
  4. Already known to recipient at disclosure date
  5. Required by law or court order (with prior notice obligation)
- Residuals clause: Generally NOT acceptable for Swiss operations
- Non-compete / non-solicit: Subject to OR Art. 340–340c limits (geographic, temporal,
  subject-matter scope; requires quid pro quo)
- Governing law: Swiss OR; venue Handelsgericht ZH/BE/GE or agreed canton
- Execution: Verify Kollektivunterschrift requirement in Handelsregister (zefix.ch)

## nDSG Breach Notification Positions
- FDPIC notification: "As soon as possible" (nDSG Art. 24) — no strict deadline,
  but target <72 h for GDPR parallel compliance
- GDPR Art. 33: 72-hour hard deadline from knowledge of breach (EU data subjects)
- Affected individuals: Notify if high risk; coordinate with FDPIC timing
- Pre-approved outside counsel: [Firm name and contact for breach response]
- Cyber insurer: [Policy number, breach notification hotline]

## Response Templates
- DSR acknowledgment deadline: 30 days from receipt (nDSG Art. 25 para. 6)
- FDPIC inquiry: Mandatory escalation to outside Swiss counsel — no exceptions
- Litigation hold: ZPO Art. 158; route through external counsel for Anwaltsgeheimnis
```

### 3. Connect your tools

Configure connections in `.mcp.json`. The plugin gracefully degrades when tools are unavailable. See [CONNECTORS.md](CONNECTORS.md) for supported integrations.

---

## Commands

### `/review-contract` — Swiss Contract Review

Review a contract against your Swiss-law playbook (OR mandatory rules + organizational positions). Flags deviations, identifies void clauses (OR Art. 100), generates bilingual redlines, and provides business impact analysis.

```
/review-contract
```

Accepts file upload, URL, or pasted contract text. Will ask for context (your side, deadline, focus areas) and review clause-by-clause. Key Swiss checks include:
- OR Art. 100 mandatory liability floor (gross negligence/intent exclusion = void)
- URG default IP ownership analysis
- CISG exclusion verification
- Handelsregister / Kollektivunterschrift execution checklist
- nDSG/GDPR AV-Vereinbarung adequacy

### `/triage-nda` — NDA Pre-Screening (Swiss OR)

Rapid triage of incoming NDAs. Classifies as GREEN (standard approval route), YELLOW (specific issues for counsel review), or RED (material issues requiring full counsel attention).

```
/triage-nda
```

Swiss-specific checks include OR Art. 340–340c non-compete/non-solicit analysis, carveout completeness, Konventionalstrafe review (OR Art. 160/163), and Kollektivunterschrift verification.

### `/vendor-check` — Swiss Vendor Agreement Status

Check the status of existing agreements with a vendor, including UID/Handelsregister verification.

```
/vendor-check [vendor name]
```

Reports on existing NDAs, MSAs, AV-Vereinbarungen, expiration dates, MWST/VAT treatment, and key Swiss-law terms. Includes FINMA outsourcing compliance flag for financial-sector vendors.

### `/brief` — Swiss Legal Team Briefing

Generate contextual briefings calibrated to Swiss law and regulatory sources.

```
/brief daily          # Morning brief: Bundesblatt, BGer/BVGer decisions, FDPIC, FINMA, WEKO updates
/brief topic [query]  # Research brief on a Swiss legal question
/brief incident       # Rapid brief on a developing situation (data breach, regulatory inquiry, etc.)
```

**Incident brief** (`/brief incident`) is designed for data breach scenarios: computes FDPIC nDSG Art. 24 and GDPR Art. 33 parallel notification deadlines, flags personal criminal liability under nDSG Art. 60–62, identifies VR notification duty (OR Art. 716a), and establishes Anwaltsgeheimnis priority.

### `/respond` — Generate Swiss-Law Templated Response

Generate a response from configured Swiss-law templates for common inquiry types.

```
/respond [inquiry-type]
```

Supported types: `dsr` (nDSG Art. 25 Auskunftsbegehren), `fdpic` (EDÖB inquiry — always escalates), `hold` (ZPO Beweissicherung), `vendor` (vendor legal question), `nda` (NDA request), `insurance` (VVG claim notification). **FDPIC and ZPO court order response types always trigger mandatory escalation to outside Swiss counsel.**

---

## Skills

| Skill | Description | Key Swiss law |
|-------|-------------|---------------|
| `contract-review` | Playbook-based contract analysis, OR mandatory law checks, redlines | OR Art. 100, URG, CISG, IPRG |
| `nda-triage` | NDA screening, classification, OR carveout completeness | OR Art. 340–340c, Art. 160/163 |
| `compliance` | nDSG/GDPR dual framework, AV-Vereinbarung review, breach protocols | nDSG Art. 9, 24, 25, 60–62; GDPR Art. 28, 33 |
| `canned-responses` | Swiss-law template management, DSR/FDPIC responses, escalation logic | nDSG Art. 25, VVG Art. 38, ZPO Art. 158 |
| `legal-risk-assessment` | Risk severity framework in CHF; VR liability; regulatory exposure | OR Art. 754, nDSG Art. 60–62, KG Art. 5/7 |
| `meeting-briefing` | Swiss meeting prep, Verwaltungsrat briefings, ZPO deadline tracking | OR Art. 716a, ZPO Art. 197ff |

---

## Example Workflows

### Contract Review (MSA with vendor)

1. Receive a vendor MSA via email
2. Run `/review-contract` and upload the document
3. Provide context: "We are the customer, need to sign by end of quarter, focus on data protection and liability"
4. Receive clause-by-clause analysis with GREEN/YELLOW/RED flags
5. OR Art. 100 violations flagged as mandatory RED — non-negotiable Swiss law
6. Get specific bilingual redline language (German/English) for YELLOW and RED items
7. Verify counterparty signing authority at zefix.ch before execution

### NDA Triage

1. Sales team sends an NDA from a new prospect
2. Run `/triage-nda` and paste or upload the NDA
3. Get classification: GREEN (route for signature with Handelsregister check), YELLOW (specific issues), or RED (needs full counsel review with Swiss outside counsel)
4. For GREEN NDAs: verify Kollektivunterschrift at zefix.ch, then approve
5. For RED NDAs: engage SAV/FSA-admitted attorney

### Data Breach Incident Brief

1. SIEM alert fires — suspected data exfiltration
2. Run `/brief incident` and provide known facts
3. Receive immediate brief with:
   - GDPR Art. 33 countdown (72-hour hard deadline from knowledge)
   - FDPIC nDSG Art. 24 notification obligation ("as soon as possible")
   - nDSG Art. 60 personal criminal liability flags for responsible individuals
   - VR notification duty (OR Art. 716a)
   - Anwaltsgeheimnis establishment checklist
   - Parallel FDPIC + EU supervisory authority notification matrix
4. Use brief to brief CEO, General Counsel, and Verwaltungsrat

### FDPIC Inquiry Response

1. Receive FDPIC Sachverhaltsabklärung (Art. 49 nDSG)
2. Run `/respond fdpic` — plugin **immediately escalates** to outside Swiss counsel
3. Receive draft skeleton for counsel review only, marked "ENTWURF — NUR ZUR PRÜFUNG DURCH EXTERNEN RECHTSANWALT"
4. Route all further communications through external Rechtsanwalt to establish Anwaltsgeheimnis

### Daily Brief

1. Start morning with `/brief daily`
2. Receive: overnight Bundesblatt publications, new BGer/BVGer data protection decisions, FDPIC activity, FINMA circulars, WEKO press releases, upcoming contract/DSR/ZPO deadlines
3. Prioritize day based on Swiss-law statutory deadlines

---

## Swiss-Specific Configuration Notes

### Anwaltsgeheimnis (Swiss Attorney-Client Privilege)

In Switzerland, attorney-client privilege (**Anwaltsgeheimnis**) applies **only** to admitted attorneys (*Rechtsanwälte/avocats/avvocati*, SAV/FSA members). In-house counsel communications are **not privileged** under Swiss law. This has several consequences for plugin use:

- All FDPIC inquiry responses must be coordinated with external Swiss counsel
- All ZPO court order responses require external Swiss counsel — no exceptions
- Litigation hold notices should be prepared with external counsel for maximum protection
- Sensitive internal legal analyses (nDSG breach assessments, regulatory exposure) should be routed through external counsel when litigation is foreseeable

### OR Art. 100 — Mandatory Liability Floor

Under OR Art. 100, it is **void** to contractually exclude liability for intentional acts (*Absicht*) or gross negligence (*grobe Fahrlässigkeit*). Any contract clause attempting to do so — even if signed by both parties — is legally ineffective. The plugin flags these clauses as mandatory RED and generates Swiss-law savings clause language.

### nDSG vs. GDPR Dual Compliance

Swiss organizations processing personal data of EU residents are subject to **both** nDSG and GDPR simultaneously. Key differences:

| Topic | nDSG | GDPR |
|-------|------|------|
| Breach notification to authority | "As soon as possible" (no strict deadline) | 72 hours (hard) |
| Breach notification to individuals | If high risk, without undue delay | If high risk, without undue delay |
| Penalty structure | CHF 250'000 per **individual** (not company) | Up to €20M / 4% global turnover |
| DPO mandatory | No (unless Canton/federal body) | Yes (for large-scale processing) |
| FDPIC adequacy list | Own list (see edoeb.admin.ch) | EU adequacy decisions |

The plugin applies the stricter of the two frameworks by default. For breach notification, the GDPR 72-hour clock effectively governs because FDPIC notification "as soon as possible" will always be ≤72 hours in practice.

---

## MCP Integration

The plugin connects to your tools through MCP servers. See [CONNECTORS.md](CONNECTORS.md) for the full list.

| Category | Examples | Purpose |
|----------|----------|---------|
| Chat | Slack, Teams | Team requests, incident coordination, triage |
| Cloud storage | Box, SharePoint | Playbooks, templates, contract repository |
| Office suite | Microsoft 365 | Email, calendar, documents |
| Project tracker | Atlassian (Jira/Confluence) | Matter tracking, DSR register, deadline calendar |
| Swiss registry | zefix.ch | Handelsregister / Kollektivunterschrift verification |

---

## Sample Test Files

The `samples/` directory contains realistic Swiss-law test documents for validating plugin behaviour:

| File | Tests | Key issues |
|------|-------|------------|
| `sample-msa-ch.md` | `/review-contract` | OR Art. 100 violation; IP assignment; AI training on customer data; asymmetric termination |
| `sample-av-vereinbarung-ch.md` | `compliance` skill | Blanket sub-processor consent; 14-day breach notification; USA/India transfers without SCCs; CHF 10k liability cap including intent (OR Art. 100 void) |
| `sample-fdpic-inquiry-ch.md` | `/respond fdpic` | EDÖB Sachverhaltsabklärung EDÖB-2026-0412-CH; Auskunftsrecht violation; cross-border transfer gaps |
| `sample-data-breach-incident.md` | `/brief incident` | SQL injection; 47'000 records; GDPR 72h + FDPIC parallel notification; nDSG Art. 60 personal liability flags |

---

## File Structure

```
legal-swiss/
├── .claude-plugin/plugin.json
├── .mcp.json
├── README.md
├── CONNECTORS.md
├── commands/
│   ├── brief.md           # /brief daily | topic | incident
│   ├── respond.md         # /respond dsr | fdpic | hold | vendor | nda | insurance
│   ├── review-contract.md # /review-contract
│   ├── triage-nda.md      # /triage-nda
│   └── vendor-check.md    # /vendor-check [vendor]
├── skills/
│   ├── contract-review/SKILL.md
│   ├── nda-triage/SKILL.md
│   ├── compliance/SKILL.md
│   ├── canned-responses/SKILL.md
│   ├── legal-risk-assessment/SKILL.md
│   └── meeting-briefing/SKILL.md
└── samples/
    ├── sample-msa-ch.md
    ├── sample-av-vereinbarung-ch.md
    ├── sample-fdpic-inquiry-ch.md
    └── sample-data-breach-incident.md
```
