---
name: contract-review
description: >
  Lightweight NDA, MSA, and vendor contract review for SMBs without legal on
  staff. Reads contracts from local files, Gmail attachments, or DocuSign
  envelopes; flags non-standard terms; explains risks in plain English; and
  outputs a marked-up redline as a separate DOCX. Use when the user says
  "review this contract," "what am I signing," "red flags," "flag any concerns,"
  "check the payment terms," or uploads/forwards a contract or legal agreement.
---

# Contract Review

## Quick start

Attach a contract file, forward the email containing it, or paste the text directly.

```
User: "Review this MSA and flag anything I should push back on."
→ Skill reads the document, identifies parties and contract type,
  analyzes 8 risk categories, returns a severity-tiered summary
  with a negotiation playbook, and exports a redlined DOCX.
```

## Workflow

1. **Get the contract** — Pull from one of three sources, in order of preference:
   - **Gmail**: Search for recent emails with contract attachments (see `reference/gmail-fetch.md`)
   - **DocuSign**: Fetch the envelope by ID or search recent drafts awaiting signature (see `reference/docusign-fetch.md`)
   - **Local file or paste**: Read the PDF (chunked via `pages` parameter for 10+ page files) or DOCX via Read tool. If the user pastes text directly, work with what's provided.

   Read the full document before analyzing. Dangerous clauses are frequently in exhibits and schedules at the back.

2. **Identify contract type and parties** — Determine agreement type (NDA, MSA, SOW, SaaS subscription, consulting, subcontractor, vendor) and which party is the user's company vs. the counterparty. Note if it looks like a counterparty template — these are typically one-sided and the counterparty expects pushback.

3. **Analyze across 8 risk categories** — Work through the contract from the ops/finance perspective of a small business owner without in-house legal. Categories are ordered by typical risk severity; use judgment for context.

   **Category 1: Payment terms and cash flow**
   - Payment timing: Net-30 is standard; Net-60+ is flaggable; Net-90/120 is a hard negotiation point
   - Payment triggers: acceptance periods that let the client slow-walk approvals indefinitely
   - Late payment penalties: absence is a gap worth noting
   - Invoicing requirements: rigid formats or PO numbers that can delay payment on technicalities
   - Expense reimbursement: pre-approval requirements and caps
   - Rate adjustments: annual increase mechanism for multi-year engagements

   **Category 2: Liability and indemnification**
   - Liability caps: uncapped liability is always a red flag
   - Mutual vs. one-sided indemnification
   - Indemnification scope: "any and all claims arising from the services" is not standard
   - Insurance requirements: E&O, cyber, general liability — achievability at the required limits
   - Consequential damages waiver: missing = flag prominently

   **Category 3: Termination and exit**
   - Termination for convenience: is it mutual? 30-day notice is typical
   - Termination for cause: cure period; vague "material breach" without definition
   - Wind-down: payment for in-progress work at termination
   - Transition assistance: paid vs. unpaid, time-limited vs. open-ended
   - Survival clauses: indefinite indemnification survival = flag

   **Category 4: Intellectual property**
   - IP assignment vs. license
   - Pre-existing IP and background tools carve-out — absence means inadvertent assignment
   - Work product definition breadth: drafts, notes, internal tools

   **Category 5: Scope and change management**
   - Scope definition clarity
   - Change order process: absence = scope creep without compensation
   - Acceptance criteria: subjective ("to client's satisfaction") vs. defined
   - Timeline asymmetry: user penalized for delays but client is not for slow feedback

   **Category 6: Non-compete and exclusivity**
   - Non-compete scope, definition of "competitor," duration
   - Exclusivity requirements on the user's company
   - Non-solicitation: employee poaching is normal; industry-broad restrictions are not

   **Category 7: Confidentiality and data**
   - Confidentiality scope: "all information shared" with no exceptions is overly broad
   - Duration: 2–3 years is typical; perpetual is aggressive
   - Data handling security requirements vs. company size and data sensitivity
   - Return/destruction requirements post-termination

   **Category 8: Operational concerns**
   - Governing law and dispute resolution; mandatory arbitration
   - Auto-renewal: opt-out window and notice period (missing a 60-day window is a common SMB mistake)
   - Assignment rights, especially if the client gets acquired
   - Most favored nation: constrains pricing across the entire client book
   - Audit rights: scope and frequency

4. **Present flagged summary** — Organize by severity:

   **🔴 Red flags (push back before signing)** — For each: quote the exact clause, explain the problem in plain language, suggest specific alternative language.

   **🟡 Yellow flags (negotiate, not deal-breakers)** — For each: quote the clause, explain the concern, describe what "better" looks like.

   **🟢 Key terms to note (awareness only)** — Payment schedules, notice periods, renewal dates, insurance requirements, key contacts.

   **📋 Contract summary** — Plain-language summary: who does what, for how much, over what timeframe, under what conditions.

   **💡 Negotiation playbook** — For each red and yellow flag: what to ask for, how to frame the ask, and what a reasonable compromise looks like.

5. **Export redline DOCX** — After presenting the summary, offer to export a redlined DOCX with the suggested changes marked up. Use the `docx` skill to generate a Word document that:
   - Preserves the original contract structure
   - Marks suggested deletions in strikethrough and additions in underline
   - Adds a cover page summarizing the changes

   Ask: "Want me to export a redlined DOCX you can send back to the counterparty?"

## Approval gates

- Never characterize the output as legal advice. Always recommend attorney review for red flags or binding decisions.
- Quote actual clause language, not paraphrases. The user needs the exact text for negotiation calls.
- Flag what's missing, not just what's there. A contract silent on liability caps or change orders is often more dangerous than one with unfavorable terms.
- Do not flag standard boilerplate. If a clause is fair and market-standard, skip it. The user wants signal, not a clause-by-clause restatement.
- Compare to market norms when flagging: "Net-90 is uncommon in professional services — Net-30 is standard."
- Adjust recommendations to the power dynamic. A Fortune 500 procurement MSA is a different negotiation than a small startup agreement.
- Never send the redlined DOCX to the counterparty without explicit user confirmation.

## Reference

- `reference/gotchas.md` — edge cases in contract analysis
- `reference/docusign-fetch.md` — pulling envelopes from DocuSign
- `reference/gmail-fetch.md` — finding contract attachments in Gmail
- `reference/examples/flagged-summary-saas.md` — worked example: SaaS agreement review output
