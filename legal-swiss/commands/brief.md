---
description: Generate contextual briefings for legal work — daily summary, topic research, or incident response
argument-hint: "[daily | topic <query> | incident]"
---

# /brief -- Legal Team Briefing (Swiss)

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate contextual briefings for legal work in a Swiss legal environment. Supports three modes: daily brief, topic brief, and incident brief.

**Swiss legal context**: Swiss law is primarily governed by the Code of Obligations (OR/CO), the Civil Code (ZGB/CC), the Federal Act on Data Protection (nDSG/LPD, in force since 1 September 2023), and cantonal procedural law (ZPO/CPC). Regulatory oversight involves FDPIC/EDÖB (data protection), FINMA (financial markets), WEKO/COMCO (competition), and SECO.

**Important**: This command assists with legal workflows but does not provide legal advice. Briefings should be reviewed by qualified legal professionals (Swiss attorney / Rechtsanwalt / avocat / avvocato) before being relied upon.

## Invocation

```
/brief daily              # Morning brief of legal-relevant items
/brief topic [query]      # Research brief on a specific legal question
/brief incident [topic]   # Rapid brief on a developing situation
```

If no mode is specified, ask the user which type of brief they need.

## Modes

---

### Daily Brief

A morning summary of everything a Swiss legal team member needs to know to start their day.

#### Sources to Scan

Check each connected source for legal-relevant items:

**Email (if connected):**
- New contract requests or review requests
- Compliance questions or reports (nDSG, GDPR for EU-related matters)
- Responses from counterparties on active negotiations
- Flagged or urgent items from the legal team inbox
- External counsel communications
- Regulatory or legal update newsletters (FDPIC decisions, FINMA circulars, BGer rulings, Federal Gazette / Bundesblatt)
- Cantonal court or arbitration hearing notices

**Calendar (if connected):**
- Today's meetings that need legal prep (board meetings, deal reviews, vendor calls, Verwaltungsrat sessions)
- Upcoming deadlines this week:
  - Contract expirations and auto-renewal notice windows
  - Filing deadlines (Handelsregister, FDPIC, FINMA)
  - Court deadlines (Fristen under ZPO, including Schlichtungsverhandlung dates)
  - nDSG data breach notification follow-up obligations
- Recurring legal team syncs

**Chat (if connected):**
- Overnight messages in legal team channels
- Direct messages requesting legal input
- Mentions of legal-relevant topics (Vertrag, Compliance, Datenschutz, NDA, nDSG, DSGVO, Haftung)
- Escalations or urgent requests

**CLM (if connected):**
- Contracts awaiting review or signature
- Approaching expiration dates (next 30 days), especially those with auto-renewal (automatische Verlängerung) and short notice periods
- Newly executed agreements
- Contracts with CHF exposure above approval thresholds

**CRM (if connected):**
- Deals moving to stages that require legal involvement
- New opportunities flagged for legal review

#### Swiss-Specific Items to Check

- **Federal Gazette (Bundesblatt / Feuille fédérale)**: New ordinances, Federal Council decisions, and consultation procedures (Vernehmlassungen) relevant to the business
- **FDPIC guidance**: New opinions or enforcement actions from the Federal Data Protection and Information Commissioner
- **FINMA circulars** (if applicable to the industry): New or updated regulatory requirements
- **BGer decisions** (Federal Supreme Court / Bundesgericht): Recent rulings affecting contract law (OR), data protection, or relevant sector
- **WEKO/COMCO**: Competition law developments
- **Commercial Register (Handelsregister)**: Changes to counterparty entities (new directors, capital changes, dissolution)
- **Swiss financial calendar**: CHF payment obligations, currency clauses (Valoränderungsklauseln) approaching reset dates

#### Output Format

```
## Daily Legal Brief -- [Date]

### Urgent / Action Required
[Items needing immediate attention, sorted by urgency]

### Contract Pipeline
- **Awaiting Your Review**: [count and list]
- **Pending Counterparty Response**: [count and list]
- **Approaching Deadlines**: [items due this week, including auto-renewal notice windows]
- **CHF Exposure**: [contracts with material financial exposure]

### New Requests
[Contract review requests, NDA requests, compliance questions received since last brief]

### Calendar Today
[Meetings with legal relevance and what prep is needed; note language of meeting if multilingual]

### Regulatory / Compliance
[nDSG/GDPR items; FINMA/FDPIC updates; Federal Gazette items; WEKO developments]

### Team Activity
[Key messages or updates from legal team channels]

### This Week's Deadlines
[Upcoming deadlines, court dates, filing dates, notice periods under contracts]

### Sources Not Available
[Any sources that were not connected or returned errors]
```

---

### Topic Brief

Research and brief on a specific legal question or topic across available sources.

#### Workflow

1. Accept the topic query from the user
2. Search across connected sources:
   - **Documents**: Internal memos, prior analyses, playbooks, precedent, Swiss legal opinions (Rechtsgutachten)
   - **Email**: Prior communications on the topic
   - **Chat**: Team discussions about the topic
   - **CLM**: Related contracts or clauses
3. Synthesize findings into a structured brief
4. For Swiss law questions, note the applicable legal source (OR, ZGB, nDSG, sector-specific act) and whether cantonal or federal law applies

#### Output Format

```
## Topic Brief: [Topic]

### Summary
[2-3 sentence executive summary of findings]

### Swiss Legal Framework
[Applicable Swiss statutes (OR, ZGB, nDSG, FINMA regulations, etc.) and key provisions]
[Note if EU law (GDPR, EU directives) also applies due to cross-border activities]

### Background
[Context and history from internal sources]

### Current State
[What the organization's current position or approach is, based on available documents]

### Key Considerations
[Important factors, risks, or open questions; note any cantonal law variations]

### Internal Precedent
[Prior decisions, memos, or positions found in internal sources]

### Gaps
[What information is missing or what sources were not available]

### Recommended Next Steps
[What the user should do with this information; note when a Rechtsgutachten or outside counsel opinion is advisable]
```

#### Important Notes
- Topic briefs synthesize what is available in connected sources; they do not substitute for formal legal research
- For Swiss law questions, recommend consulting Swiss legal databases (Swisslex, Legalis, Klinika, Rechtsportal) or outside counsel
- For data protection topics, distinguish between Swiss nDSG (FDPIC oversight) and EU GDPR (relevant supervisory authority); both may apply
- Always note the limitations of the sources searched

---

### Incident Brief

Rapid briefing for developing situations that require immediate legal attention (data breaches, litigation threats, regulatory inquiries, IP disputes, competition investigations, etc.).

#### Workflow

1. Accept the incident topic or description
2. Rapidly scan all connected sources for relevant context:
   - **Email**: Communications about the incident
   - **Chat**: Real-time discussions and escalations
   - **Documents**: Relevant policies, response plans, insurance coverage, contractual indemnification
   - **Calendar**: Scheduled response meetings
   - **CLM**: Affected contracts, indemnification provisions, insurance requirements
3. Identify Swiss-specific notification and response obligations
4. Compile into an actionable incident brief

#### Output Format

```
## Incident Brief: [Topic]
**Prepared**: [timestamp]
**Classification**: [severity assessment if determinable]
**Privilege**: [Mark as "Anwaltsgeheimnis / Attorney-Client Privileged" if applicable]

### Situation Summary
[What is known about the incident]

### Timeline
[Chronological summary of events based on available sources]

### Immediate Swiss Legal Obligations
**Data Breach (nDSG Art. 24)**: Notify FDPIC "as soon as possible" if breach is likely to lead to high risk to data subjects; notify affected individuals without undue delay if required for their protection
**Data Breach (GDPR Art. 33)**: If EU data involved, notify relevant supervisory authority within 72 hours
**Regulatory Notifications**: FINMA (if financial institution), or other sector regulator
**Litigation Hold**: Preserve evidence relevant to potential ZPO proceedings
**Criminal referral**: Consider whether Strafanzeige is warranted or expected
**Board notification**: Assess Verwaltungsrat notification duty under CO Art. 717 (duty of care)

### Relevant Agreements
[Contracts, insurance policies (particularly D&O, cyber liability), or other agreements implicated]
[Note governing law and jurisdiction of each]

### Internal Response
[What response activity has already occurred based on email/chat]

### Key Contacts
[Relevant internal contacts, external Swiss counsel, FDPIC contact, applicable insurers]

### Recommended Immediate Actions
1. [Most urgent action — with Swiss law basis]
2. [Second priority]
3. [etc.]

### Information Gaps
[What is not yet known and needs to be determined]

### Sources Checked
[What was searched and what was not available]
```

#### Important Notes for Incident Briefs
- Speed matters. Produce the brief quickly with available information rather than waiting for complete information
- **Swiss privilege**: In Switzerland, attorney-client privilege (Anwaltsgeheimnis) applies to admitted attorneys (Rechtsanwälte). In-house counsel communications may not be privileged in Swiss law — flag this if privilege is a concern
- **nDSG breach notification**: No strict 72-hour deadline (unlike GDPR), but notification to FDPIC should be "as soon as possible" when the risk threshold is met
- **GDPR 72-hour rule** still applies when the incident involves personal data of EU/EEA residents
- For data incidents involving both Swiss and EU data, the stricter GDPR 72-hour deadline effectively governs the timeline
- Flag competition law angles if the incident could attract WEKO attention (e.g., data sharing, price coordination)
- Recommend outside counsel (Swiss attorney) engagement for any ORANGE or RED severity incident

## General Notes

- Briefs should be actionable: every item should have a clear next step or reason for inclusion
- Keep briefs concise. Link to source materials rather than reproducing them in full
- Note the language of key documents (German / French / Italian / English) — translation may be needed for Swiss court proceedings
- For daily briefs, learn the user's preferences over time (what they find useful, what they want filtered out)
- If sources are unavailable, note the gaps prominently so the user knows what was not checked
