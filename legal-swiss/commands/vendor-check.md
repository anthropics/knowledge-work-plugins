---
description: Check the status of existing agreements with a vendor across all connected systems
argument-hint: "[vendor name]"
---

# /vendor-check -- Vendor Agreement Status (Swiss)

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Check the status of existing agreements with a vendor across all connected systems. Provides a consolidated view of the legal relationship under Swiss law.

**Swiss legal context**: Swiss vendor relationships involve:
- **Handelsregister (HR)**: Commercial register for verifying Swiss entity legal status, registered address, and authorized signatories (Zeichnungsberechtigte)
- **UID (Unternehmens-Identifikationsnummer)**: Swiss company number for legal entity verification
- **MWST (Mehrwertsteuer / TVA)**: Swiss VAT number and obligations under MWSTG
- **Swiss OR**: Governing contract law for Swiss-law agreements
- **nDSG**: Data protection compliance requirements for vendors who process personal data
- **FINMA**: Regulatory requirements for vendors to financial institutions (e.g., outsourcing under FINMA Circular 2023/1)
- **SIA / SFC norms**: Standard terms for construction, engineering, or other professional services if applicable

**Important**: This command assists with legal workflows but does not provide legal advice. Agreement status reports should be verified against original documents by qualified Swiss legal professionals.

## Invocation

```
/vendor-check [vendor name]
```

If no vendor name is provided, prompt the user to specify which vendor to check.

## Workflow

### Step 1: Identify the Vendor

Accept the vendor name from the user. Handle common variations:
- Full legal name vs. trade name (e.g., "UBS AG" vs. "UBS")
- Swiss entity designations (AG, GmbH, Genossenschaft, Kollektivgesellschaft, Kommanditgesellschaft, Stiftung, Verein)
- Parent/subsidiary relationships; note that Swiss group structures often use separate AG/GmbH entities per canton or function
- International entities with Swiss branches (Zweigniederlassung)
- UID (Unternehmens-Identifikationsnummer) if provided

Ask the user to clarify if the vendor name is ambiguous or if there are multiple entities in a group.

**Swiss tip**: Before proceeding, recommend checking the Handelsregister (zefix.ch) to confirm:
- Current legal name and registered address
- Legal form (AG, GmbH, etc.)
- Authorized signatories (Zeichnungsberechtigte) and their signing authority (Einzelunterschrift / Kollektivunterschrift)
- Whether any Konkurs (bankruptcy), Liquidation, or Nachlassverfahren (composition proceedings) are pending

### Step 2: Search Connected Systems

Search for the vendor across all available connected systems, in priority order:

#### CLM (Contract Lifecycle Management) -- If Connected
Search for all contracts involving the vendor:
- Active agreements (aktive Verträge)
- Expired agreements (last 3 years) — note: Swiss OR Art. 127 general limitation period is 10 years; some claims may survive expiry
- Agreements in negotiation or pending signature (Unterschrift)
- Amendments (Vertragsänderungen) and addenda
- Note CHF value and any value-added tax (MWST) provisions

#### CRM -- If Connected
Search for the vendor/account record:
- Account status and relationship type
- Associated opportunities or projects
- Contact information for vendor's legal/contracts/Einkauf team
- Payment history (relevant for assessing relationship health)

#### Email -- If Connected
Search for recent relevant correspondence:
- Contract-related emails (last 6 months)
- NDA, MSA, DPA attachments
- Negotiation threads
- Compliance certifications or audit reports shared by vendor

#### Documents (e.g., SharePoint, OneDrive) -- If Connected
Search for:
- Executed agreements (unterzeichnete Verträge)
- Redlines and drafts
- Due diligence materials
- Insurance certificates (Versicherungsbestätigungen)
- FINMA outsourcing documentation if applicable

#### Chat (e.g., Teams, Slack) -- If Connected
Search for recent mentions:
- Contract requests involving this vendor
- Legal or compliance questions about the vendor
- Relevant team discussions (last 3 months)
- Issues, disputes, or escalations involving the vendor

### Step 3: Compile Agreement Status

For each agreement found, report:

| Field | Details |
|-------|---------|
| **Agreement Type** | NDA/GhV, MSA/Rahmenvertrag, SOW/Auftrag, DPA/AV-Vereinbarung, SLA, License/Lizenzvertrag, Distribution/Vertriebsvertrag, etc. |
| **Status** | Active / Expired / In Negotiation / Pending Signature (Unterschrift ausstehend) |
| **Governing Law** | Swiss OR (which canton?) / Foreign law |
| **Contract Language** | German / French / Italian / English |
| **Effective Date** | When the agreement started (Vertragsbeginn) |
| **Expiration Date** | When it expires or renews (Vertragsende / Verlängerungsdatum) |
| **Auto-Renewal** | Yes/No; renewal term; notice period (Kündigungsfrist) — flag short notice windows |
| **CHF Value** | Contract value or annual fee in CHF; note any CHF/EUR/USD conversion clauses |
| **Key Terms** | Liability cap (in CHF); governing law; termination provisions; MWST treatment |
| **Amendments** | Any amendments (Nachträge) or addenda on file |
| **nDSG/GDPR Status** | Does vendor process personal data? AV-Vereinbarung / DPA in place? |
| **FINMA Status** | If regulated industry: outsourcing agreement per FINMA Circular 2023/1 requirements? |
| **Signature Authority** | Were the signatories authorized per Handelsregister at time of signing? |

### Step 4: Gap Analysis

Identify what agreements exist and what might be missing for a complete Swiss law relationship:

```
## Agreement Coverage / Vertragsdeckung

[✓/✗] NDA / Geheimhaltungsvereinbarung -- [status]
[✓/✗] MSA / Rahmenvertrag -- [status or "Not found"]
[✓/✗] DPA / AV-Vereinbarung (nDSG Art. 9) -- [status or "Not found — assess if required"]
[✓/✗] SOW / Auftrag or Werkvertrag -- [status or "Not found"]
[✓/✗] SLA / Service Level Agreement -- [status or "Not found"]
[✓/✗] Insurance Certificate / Versicherungsbestätigung -- [status or "Not found"]
[✓/✗] FINMA Outsourcing Agreement -- [status or "N/A — not regulated industry"]
[✓/✗] MWST / VAT clause in main agreement -- [present/absent]
```

Flag any gaps that may be needed based on the relationship type:
- If vendor handles personal data (Personendaten) → AV-Vereinbarung under nDSG Art. 9 required
- If vendor handles personal data of EU residents → GDPR-compliant DPA required
- If the organization is FINMA-supervised and vendor provides critical outsourced services → FINMA outsourcing compliance required
- If vendor provides services above CHF 230,000 (approximate public procurement threshold) → check whether public procurement rules (BöB/IVöB) apply

### Step 5: Generate Report

Output a consolidated report:

```
## Vendor Agreement Status / Lieferantenstatus: [Vendor Name]

**Search Date / Datum**: [today's date]
**Sources Checked / Geprüfte Quellen**: [list of systems searched]
**Sources Unavailable / Nicht verfügbare Quellen**: [list of systems not connected]

## Relationship Overview / Beziehungsübersicht

**Vendor / Lieferant**: [full legal name, legal form, UID if known]
**Handelsregister Status**: [active/dissolved/in liquidation — zefix.ch verification recommended]
**Registered Address / Domizil**: [registered canton and address]
**Relationship Type**: [vendor/partner/customer/outsourcing provider/etc.]
**CRM Status**: [if available]

## Agreement Summary / Vertragsübersicht

### [Agreement Type / Vertragstyp] -- [Status]
- **Effective / Beginn**: [date]
- **Expires / Ende**: [date] ([auto-renews / does not auto-renew])
- **Notice Period / Kündigungsfrist**: [period — flag if short]
- **Governing Law / Anwendbares Recht**: [Swiss OR / Canton X / Foreign law]
- **CHF Value**: [annual / total value]
- **Key Terms / Wesentliche Bedingungen**: [liability cap in CHF, key obligations]
- **Location / Ablageort**: [where the executed copy is stored]

### [Agreement Type 2] -- [Status]
[etc.]

## Gap Analysis / Lückenanalyse

[What's in place vs. what may be needed under Swiss law]
[Highlight: nDSG AV-Vereinbarung, FINMA outsourcing, insurance gaps]

## Upcoming Actions / Anstehende Massnahmen

- [Approaching expirations — with Kündigungsfrist notice dates]
- [Auto-renewal notice deadlines — flag any within 90 days]
- [Required agreements not yet in place — with Swiss law basis for requirement]
- [MWST / UID verification if applicable]
- [Handelsregister change notifications (e.g., new director, address change)]

## Compliance Status / Compliance-Status

[nDSG / GDPR data processing: AV-Vereinbarung status]
[FINMA outsourcing: compliance status if applicable]
[Insurance certificates: current or expired?]

## Notes / Anmerkungen

[Any relevant context from email/chat searches]
[Note any disputed matters, open negotiations, or relationship issues]
```

### Step 6: Handle Missing Sources

If key systems are not connected via MCP:

- **No CLM**: Note that no CLM is connected. Suggest the user check their CLM manually and verify via Handelsregister (zefix.ch) for any registered rights/charges. Report what was found in other systems.
- **No CRM**: Skip CRM context. Note the gap.
- **No Email**: Note that email was not searched. Suggest the user search for "[vendor name] Vertrag" or "[vendor name] NDA".
- **No Documents**: Note that document storage was not searched.

Always clearly state which sources were checked and which were not, so the user knows the completeness of the report.

## Notes

- If no agreements are found in any connected system, report that clearly and ask the user if they have agreements stored in physical files (Swiss practice still uses paper originals for some agreement types) or other document systems
- For vendor groups (e.g., Swiss holding company with operating subsidiaries), ask whether the user wants to check a specific entity or the entire group; note that Swiss holding/operating structures often require agreements to be with the specific contracting entity
- Flag any agreements that are expired but may still have surviving obligations under Swiss OR (confidentiality, indemnification, post-contractual obligations under OR Art. 97ff.)
- If an agreement is approaching expiration (within 90 days), or a Kündigungsfrist window is closing (within 90 days of notice deadline), highlight this prominently
- Swiss practical note: For significant vendor relationships, recommend conducting an annual Vertragsreview to catch expiring agreements, update AV-Vereinbarungen for nDSG compliance, and refresh insurance certificate requirements
