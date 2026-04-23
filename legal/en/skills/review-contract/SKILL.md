---
name: review-contract
description: Review a contract against your organization's negotiation playbook — flag deviations, generate redlines, provide business impact analysis. Use when reviewing vendor or customer agreements, when you need clause-by-clause analysis against standard positions, or when preparing a negotiation strategy with prioritized redlines and fallback positions.
argument-hint: "<contract file or text>"
---

# /review-contract -- Contract Review Against Playbook

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Review a contract against your organization's negotiation playbook. Analyze each clause, flag deviations, generate redline suggestions, and provide business impact analysis.

**Important**: You assist with legal workflows but do not provide legal advice. All analysis should be reviewed by qualified legal professionals before being relied upon.

## Invocation

```
/review-contract <contract file or URL>
```

Review the contract: @$1

## Workflow

### Step 1: Accept the Contract

Accept the contract in any of these formats:
- **File upload**: PDF, DOCX, or other document format
- **URL**: Link to a contract in your CLM, cloud storage (e.g., Box, Egnyte, SharePoint), or other document system
- **Pasted text**: Contract text pasted directly into the conversation

If no contract is provided, prompt the user to supply one.

### Step 2: Gather Context

Ask the user for context before beginning the review:

1. **Which side are you on?** (vendor/supplier, customer/buyer, licensor, licensee, partner -- or other)
2. **Deadline**: When does this need to be finalized? (Affects prioritization of issues)
3. **Focus areas**: Any specific concerns? (e.g., "data protection is critical", "we need flexibility on term", "IP ownership is the key issue")
4. **Deal context**: Any relevant business context? (e.g., deal size, strategic importance, existing relationship)

If the user provides partial context, proceed with what you have and note assumptions.

### Step 3: Load the Playbook

Look for the organization's contract review playbook in local settings (e.g., `legal.local.md` or similar configuration files).

The playbook should define:
- **Standard positions**: The organization's preferred terms for each major clause type
- **Acceptable ranges**: Terms that can be agreed to without escalation
- **Escalation triggers**: Terms that require senior counsel review or outside counsel involvement

**If no playbook is configured:**
- Inform the user that no playbook was found
- Offer two options:
  1. Help the user set up their playbook (walk through defining positions for key clauses)
  2. Proceed with a generic review using widely-accepted commercial standards as the baseline
- If proceeding generically, clearly note that the review is based on general commercial standards, not the organization's specific positions

### Step 4: Clause-by-Clause Analysis

Apply the following review process:

1. **Identify the contract type**: SaaS agreement, professional services, license, partnership, procurement, etc. The contract type affects which clauses are most material.
2. **Determine the user's side**: Vendor, customer, licensor, licensee, partner. This fundamentally changes the analysis (e.g., limitation of liability protections favor different parties).
3. **Read the entire contract** before flagging issues. Clauses interact with each other (e.g., an uncapped indemnity may be partially mitigated by a broad limitation of liability).
4. **Analyze each material clause** against the playbook position.
5. **Consider the contract holistically**: Are the overall risk allocation and commercial terms balanced?

Analyze the contract systematically, covering at minimum:

| Clause Category | Key Review Points |
|----------------|-------------------|
| **Limitation of Liability** | Cap amount, carveouts, mutual vs. unilateral, consequential damages |
| **Indemnification** | Scope, mutual vs. unilateral, cap, IP infringement, data breach |
| **IP Ownership** | Pre-existing IP, developed IP, work-for-hire, license grants, assignment |
| **Data Protection** | DPA requirement, processing terms, sub-processors, breach notification, cross-border transfers |
| **Confidentiality** | Scope, term, carveouts, return/destruction obligations |
| **Representations & Warranties** | Scope, disclaimers, survival period |
| **Term & Termination** | Duration, renewal, termination for convenience, termination for cause, wind-down |
| **Governing Law & Dispute Resolution** | Jurisdiction, venue, arbitration vs. litigation |
| **Insurance** | Coverage requirements, minimums, evidence of coverage |
| **Assignment** | Consent requirements, change of control, exceptions |
| **Force Majeure** | Scope, notification, termination rights |
| **Payment Terms** | Net terms, late fees, taxes, price escalation |

For each clause, assess against the playbook (or generic standards) and note whether it is present, absent, or unusual.

#### Detailed Clause Guidance

##### Limitation of Liability

**Key elements to review:**
- Cap amount (fixed dollar amount, multiple of fees, or uncapped)
- Whether the cap is mutual or applies differently to each party
- Carveouts from the cap (what liabilities are uncapped)
- Whether consequential, indirect, special, or punitive damages are excluded
- Whether the exclusion is mutual
- Carveouts from the consequential damages exclusion
- Whether the cap applies per-claim, per-year, or aggregate

**Common issues:**
- Cap set at a fraction of fees paid (e.g., "fees paid in the prior 3 months" on a low-value contract)
- Asymmetric carveouts favoring the drafter
- Broad carveouts that effectively eliminate the cap (e.g., "any breach of Section X" where Section X covers most obligations)
- No consequential damages exclusion for one party's breaches

##### Indemnification

**Key elements to review:**
- Whether indemnification is mutual or unilateral
- Scope: what triggers the indemnification obligation (IP infringement, data breach, bodily injury, breach of reps and warranties)
- Whether indemnification is capped (often subject to the overall liability cap, or sometimes uncapped)
- Procedure: notice requirements, right to control defense, right to settle
- Whether the indemnitee must mitigate
- Relationship between indemnification and the limitation of liability clause

**Common issues:**
- Unilateral indemnification for IP infringement when both parties contribute IP
- Indemnification for "any breach" (too broad; essentially converts the liability cap to uncapped liability)
- No right to control defense of claims
- Indemnification obligations that survive termination indefinitely

##### Intellectual Property

**Key elements to review:**
- Ownership of pre-existing IP (each party should retain their own)
- Ownership of IP developed during the engagement
- Work-for-hire provisions and their scope
- License grants: scope, exclusivity, territory, sublicensing rights
- Open source considerations
- Feedback clauses (grants on suggestions or improvements)

**Common issues:**
- Broad IP assignment that could capture the customer's pre-existing IP
- Work-for-hire provisions extending beyond the deliverables
- Unrestricted feedback clauses granting perpetual, irrevocable licenses
- License scope broader than needed for the business relationship

##### Data Protection

**Key elements to review:**
- Whether a Data Processing Agreement/Addendum (DPA) is required
- Data controller vs. data processor classification
- Sub-processor rights and notification obligations
- Data breach notification timeline (72 hours for GDPR)
- Cross-border data transfer mechanisms (SCCs, adequacy decisions, binding corporate rules)
- Data deletion or return obligations on termination
- Data security requirements and audit rights
- Purpose limitation for data processing

**Common issues:**
- No DPA when personal data is being processed
- Blanket authorization for sub-processors without notification
- Breach notification timeline longer than regulatory requirements
- No cross-border transfer protections when data moves internationally
- Inadequate data deletion provisions

##### Term and Termination

**Key elements to review:**
- Initial term and renewal terms
- Auto-renewal provisions and notice periods
- Termination for convenience: available? notice period? early termination fees?
- Termination for cause: cure period? what constitutes cause?
- Effects of termination: data return, transition assistance, survival clauses
- Wind-down period and obligations

**Common issues:**
- Long initial terms with no termination for convenience
- Auto-renewal with short notice windows (e.g., 30-day notice for annual renewal)
- No cure period for termination for cause
- Inadequate transition assistance provisions
- Survival clauses that effectively extend the agreement indefinitely

##### Governing Law and Dispute Resolution

**Key elements to review:**
- Choice of law (governing jurisdiction)
- Dispute resolution mechanism (litigation, arbitration, mediation first)
- Venue and jurisdiction for litigation
- Arbitration rules and seat (if arbitration)
- Jury waiver
- Class action waiver
- Prevailing party attorney's fees

**Common issues:**
- Unfavorable jurisdiction (unusual or remote venue)
- Mandatory arbitration with rules favorable to the drafter
- Waiver of jury trial without corresponding protections
- No escalation process before formal dispute resolution

### Step 5: Flag Deviations

Classify each deviation from the playbook using a three-tier system:

#### GREEN -- Acceptable

The clause aligns with or is better than the organization's standard position. Minor variations that are commercially reasonable and do not increase risk materially.

**Examples:**
- Liability cap at 18 months of fees when standard is 12 months (better for the customer)
- Mutual NDA term of 2 years when standard is 3 years (shorter but reasonable)
- Governing law in a well-established commercial jurisdiction close to the preferred one

**Action**: Note for awareness. No negotiation needed.

#### YELLOW -- Negotiate

The clause falls outside the standard position but within a negotiable range. The term is common in the market but not the organization's preference. Requires attention and likely negotiation, but not escalation.

**Examples:**
- Liability cap at 6 months of fees when standard is 12 months (below standard but negotiable)
- Unilateral indemnification for IP infringement when standard is mutual (common market position but not preferred)
- Auto-renewal with 60-day notice when standard is 90 days
- Governing law in an acceptable but not preferred jurisdiction

**Action**: Generate specific redline language. Provide fallback position. Estimate business impact of accepting vs. negotiating.
- **Include**: Specific redline language to bring the term back to standard position
- **Include**: Fallback position if the counterparty pushes back
- **Include**: Business impact of accepting as-is vs. negotiating

#### RED -- Escalate

The clause falls outside acceptable range, triggers a defined escalation criterion, or poses material risk. Requires senior counsel review, outside counsel involvement, or business decision-maker sign-off.

**Examples:**
- Uncapped liability or no limitation of liability clause
- Unilateral broad indemnification with no cap
- IP assignment of pre-existing IP
- No DPA offered when personal data is processed
- Unreasonable non-compete or exclusivity provisions
- Governing law in a problematic jurisdiction with mandatory arbitration

**Action**: Explain the specific risk. Provide market-standard alternative language. Estimate exposure. Recommend escalation path.
- **Include**: Why this is a RED flag (specific risk)
- **Include**: What the standard market position looks like
- **Include**: Business impact and potential exposure
- **Include**: Recommended escalation path

### Step 6: Generate Redline Suggestions

For each YELLOW and RED deviation, provide:
- **Current language**: Quote the relevant contract text
- **Suggested redline**: Specific alternative language
- **Rationale**: Brief explanation suitable for sharing with the counterparty
- **Priority**: Whether this is a must-have or nice-to-have in negotiation

#### Redline Generation Best Practices

When generating redline suggestions:

1. **Be specific**: Provide exact language, not vague guidance. The redline should be ready to insert.
2. **Be balanced**: Propose language that is firm on critical points but commercially reasonable. Overly aggressive redlines slow negotiations.
3. **Explain the rationale**: Include a brief, professional rationale suitable for sharing with the counterparty's counsel.
4. **Provide fallback positions**: For YELLOW items, include a fallback position if the primary ask is rejected.
5. **Prioritize**: Not all redlines are equal. Indicate which are must-haves and which are nice-to-haves.
6. **Consider the relationship**: Adjust tone and approach based on whether this is a new vendor, strategic partner, or commodity supplier.

#### Redline Format

For each redline:
```
**Clause**: [Section reference and clause name]
**Current language**: "[exact quote from the contract]"
**Proposed redline**: "[specific alternative language with additions in bold and deletions struck through conceptually]"
**Rationale**: [1-2 sentences explaining why, suitable for external sharing]
**Priority**: [Must-have / Should-have / Nice-to-have]
**Fallback**: [Alternative position if primary redline is rejected]
```

### Step 7: Business Impact Summary

Provide a summary section covering:
- **Overall risk assessment**: High-level view of the contract's risk profile
- **Top 3 issues**: The most important items to address
- **Negotiation strategy**: Recommended approach (which issues to lead with, what to concede)
- **Timeline considerations**: Any urgency factors affecting the negotiation approach

#### Negotiation Priority Framework

When presenting redlines, organize by negotiation priority:

**Tier 1 -- Must-Haves (Deal Breakers)**
Issues where the organization cannot proceed without resolution:
- Uncapped or materially insufficient liability protections
- Missing data protection requirements for regulated data
- IP provisions that could jeopardize core assets
- Terms that conflict with regulatory obligations

**Tier 2 -- Should-Haves (Strong Preferences)**
Issues that materially affect risk but have negotiation room:
- Liability cap adjustments within range
- Indemnification scope and mutuality
- Termination flexibility
- Audit and compliance rights

**Tier 3 -- Nice-to-Haves (Concession Candidates)**
Issues that improve the position but can be conceded strategically:
- Preferred governing law (if alternative is acceptable)
- Notice period preferences
- Minor definitional improvements
- Insurance certificate requirements

**Negotiation strategy**: Lead with Tier 1 items. Trade Tier 3 concessions to secure Tier 2 wins. Never concede on Tier 1 without escalation.

### Step 8: CLM Routing (If Connected)

If a Contract Lifecycle Management system is connected via MCP:
- Recommend the appropriate approval workflow based on contract type and risk level
- Suggest the correct routing path (e.g., standard approval, senior counsel, outside counsel)
- Note any required approvals based on contract value or risk flags

If no CLM is connected, skip this step.

## Output Format

Structure the output as:

```
## Contract Review Summary

**Document**: [contract name/identifier]
**Parties**: [party names and roles]
**Your Side**: [vendor/customer/etc.]
**Deadline**: [if provided]
**Review Basis**: [Playbook / Generic Standards]

## Key Findings

[Top 3-5 issues with severity flags]

## Clause-by-Clause Analysis

### [Clause Category] -- [GREEN/YELLOW/RED]
**Contract says**: [summary of the provision]
**Playbook position**: [your standard]
**Deviation**: [description of gap]
**Business impact**: [what this means practically]
**Redline suggestion**: [specific language, if YELLOW or RED]

[Repeat for each major clause]

## Negotiation Strategy

[Recommended approach, priorities, concession candidates]

## Next Steps

[Specific actions to take]
```

## Notes

- If the contract is in a language other than English, note this and ask if the user wants a translation or review in the original language
- For very long contracts (50+ pages), offer to focus on the most material sections first and then do a complete review
- Always remind the user that this analysis should be reviewed by qualified legal counsel before being relied upon for legal decisions
