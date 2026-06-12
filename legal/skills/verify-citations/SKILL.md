---
name: verify-citations
description: Verify the legal authorities cited in a brief, memo, or filing — checking that each case, statute, or regulation exists, says what it is cited for, and binds in the relevant jurisdiction. Use when reviewing a draft brief or motion before filing, when checking AI-assisted or outside-counsel work product, or when you need a citation-by-citation diagnostic rather than a pass/fail lookup. Surfaces fabricated cites, misattributed holdings, wrong-jurisdiction authority, hallucinated details, and unverifiable coverage gaps.
argument-hint: "<brief, memo, or list of citations to verify>"
---

# /verify-citations -- Citation Verification

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Verify the legal authorities cited in a brief, memo, motion, or filing — case by case — before it is filed or relied upon.

**Important**: This skill assists with verification workflows but does not provide legal advice and is not a substitute for reading the cited authority. Citation verification supports, and does not replace, the filer's independent duty (e.g., Fed. R. Civ. P. 11) to confirm that every authority is real, accurately characterized, and properly applied. Automated lookups can be incomplete or out of date; always confirm against an authoritative reporter or court database before filing.

## Usage

```
/verify-citations $ARGUMENTS
```

Accepts: an uploaded brief or memo, a URL, pasted text, or a plain list of citations. If a connected research database (Westlaw, Lexis, court PACER/CourtListener) is available via MCP, it will be used; otherwise the skill notes which citations it could not independently confirm and tells you exactly what to check by hand.

## What I Need From You

To verify accurately I need, at minimum, the citations and the propositions they are offered for. The more of the following you provide, the deeper the check:

- **The document** (or the citation list) — so I can extract each authority and the claim it supports.
- **The filing jurisdiction and court** — required for the binding-authority check. "N.D. Cal." and "Tennessee Court of Appeals" produce different verdicts for the same case.
- **Which side you are on / the proposition** — so I can judge whether the cite actually supports the sentence it follows.
- **Access to the cited text** (a research connector, or the opinions themselves) — without it, I can confirm existence and metadata but cannot fully verify the holding.

## Output

```markdown
## Citation Verification Report: [Document]

**Filing jurisdiction**: [Court / circuit]
**Citations checked**: [N]   **Verified**: [N]   **Flagged**: [N]   **Unverifiable**: [N]

### Summary
[One line: Safe to proceed / Proceed after fixing flagged items / Do not file — fabricated or misattributed authority present]

### Citation-by-Citation

| # | Citation | Cited For | Verdict | Failure Mode | Confidence | What's Wrong / Fix |
|---|----------|-----------|---------|--------------|-----------|--------------------|
| 1 | [Caption, reporter, court, year] | [Proposition] | [Verified / Flagged / Unverifiable] | [None / Fabricated / Misattributed / Wrong Jurisdiction / Hallucinated Detail / Coverage Gap] | [High/Med/Low] | [Specifics + corrective action] |

### Flagged Items (detail)

#### [Citation]
- **Failure mode**: [category]
- **What the brief claims**: [proposition as written]
- **What the authority actually says / status**: [finding, with the relevant passage if available]
- **Why it matters**: [binding effect, credibility, sanction exposure]
- **Recommended fix**: [replace, re-characterize, add pincite, pull and read, remove]

### Could Not Verify
[Citations where existence or holding could not be independently confirmed — with the specific manual check required. "Unverifiable" is NOT "fabricated"; it means confirm by hand before relying on it.]

### Recommended Actions
1. [Highest-priority fix — typically any Fabricated or Misattributed item]
2. [Next]
3. [Next]
```

## The Five Ways a Citation Fails

Most citation tools return a binary answer: the case exists, or it doesn't. That is the wrong model. "Exists" does not mean "supports your argument," and "not found" does not mean "fabricated." A citation can fail in five distinct ways, and each demands a different response.

**1. Fabricated** — The authority does not exist at all. No docket, no opinion, no parties — an invention that merely looks like a citation. Caught only by an existence check against an authoritative source. *Response: remove it and find real authority for the proposition.*

**2. Misattributed Holding** — The case is real and looks up cleanly, but it does not say what the brief claims. It addresses a different issue, or stands for a related-but-distinct point. **This is the most dangerous mode because it passes a simple existence check** — the case is real, the claim about it is not. *Response: read the opinion, re-characterize the proposition or replace the cite.*

**3. Wrong Jurisdiction** — The authority is real and may even be on point, but it has no binding force where you are filing: an out-of-circuit opinion cited as controlling, or a sister-state decision presented as if it governed. *Response: relabel as persuasive, or substitute binding authority from the filing jurisdiction.*

**4. Hallucinated Detail** — The case exists and roughly supports the point, but a detail is wrong: the year, the deciding court, a party name, the disposition, or a fabricated pincite/quote. Close enough to pass a glance, wrong enough to damage credibility. *Response: correct the metadata; verify any quoted language verbatim against the opinion.*

**5. Coverage Gap** — The authority cannot be found in any available database. It may be an unreported decision, a sealed or restricted opinion, or from a jurisdiction that does not publish digitally. It is **not** fabricated — but it is unverifiable, which means the court cannot confirm it either. *Response: locate the primary source manually; do not rely on it until confirmed.*

## The Three-Layer Verification Process

Run every citation through all three layers, in order. If a layer fails, record the failure mode and proceed — later layers may surface additional problems, but a Layer 1 failure is dispositive.

### Layer 1 — Does this authority exist?
Cross-reference against an authoritative source (court database, official reporter, or a connected research tool). Match the **parties, docket/citation, court, and year** — not just the case name. A name match with a mismatched reporter or year is a signal, not a confirmation. If nothing matches: **Fabricated** — stop and flag.

### Layer 2 — Does it say what the brief claims?
Read the actual text of the opinion (or statute/regulation). Compare the holding to the proposition the citation supports in the brief. Confirm any quotation verbatim and confirm pincites point to the cited passage. **This is where most failures hide — behind real case names with wrong claims.** Mismatch: **Misattributed Holding** or **Hallucinated Detail**.

### Layer 3 — Does the authority bind?
Check that the deciding court sits in the filing jurisdiction and at a level that binds the court you are filing in. Confirm the authority is still good law (not reversed, vacated, superseded, or overruled). Distinguish binding from merely persuasive authority. Failure: **Wrong Jurisdiction** (or a currency problem — flag superseded authority explicitly).

> A tool that runs Layer 1 only gives a false sense of security. Confirming a case exists is necessary but not sufficient; a brief built on real cases with wrong holdings still fails in front of a judge.

## Confidence Scoring

Attach a confidence level to each verdict so the reviewer knows where to spend attention:

- **High** — Independently confirmed against an authoritative source (existence, text, and currency all checked).
- **Medium** — Existence confirmed, but the holding or currency could not be fully verified (e.g., no full-text access).
- **Low** — Could not independently confirm; verdict is inferential. Treat as **Unverifiable** and require a manual check.

Never report a fabricated-or-misattributed finding at Low confidence as if it were settled. Distinguish "I confirmed this is wrong" from "I could not confirm this is right."

## Verification Discipline

- **Unverifiable ≠ fabricated.** A coverage gap means *confirm by hand*, not *delete*. Conflating the two destroys good authority; ignoring it ships unconfirmed authority. Keep them in separate buckets in the report.
- **Quotes get verified verbatim.** A real case with an invented quotation is a Hallucinated Detail, not a pass. Match quoted language character-for-character and confirm the pincite.
- **Re-run after edits.** Citation fixes introduce new citations. Verify the replacements, not just the originals.
- **Graceful degradation.** When no research connector is available, do not guess. State plainly which citations could not be independently checked and what the human must do — listing an unconfirmed citation as "verified" is worse than listing it as unverifiable.
- **The duty stays with the filer.** This skill reduces the surface area a human must review; it does not discharge the Rule 11 (or equivalent) obligation to verify before filing.

## When to Escalate

Route to senior or outside counsel — and do not file — when:

- Any **Fabricated** or **Misattributed Holding** item survives into a draft intended for filing.
- A **substantial share of the citations cannot be verified** and no authoritative source is reachable.
- The document is **AI-assisted or from an unfamiliar source** and a material portion of its authority fails Layer 1 or Layer 2 (a pattern, not a single typo).
- A court in your jurisdiction has an **AI-use disclosure or certification requirement** and the filing relied on generative tools.

## Tips

1. **Give the proposition, not just the cite.** "Smith v. Jones, cited for the proposition that..." lets me run Layer 2; a bare citation only gets Layer 1.
2. **Name the court you are filing in.** Binding-authority verdicts depend on it.
3. **Verify the replacements too.** The cite you add to fix a flag is itself unverified until checked.
4. **Treat a clean existence check as the floor, not the finish.** The dangerous failures are real cases used wrongly.
