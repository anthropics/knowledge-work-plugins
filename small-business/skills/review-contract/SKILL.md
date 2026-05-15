---
name: review-contract
description: Reviews a contract in plain English, surfaces red flags with severity ratings, and produces a marked-up docx/PDF with suggested redlines. Accepts optional file path or DocuSign envelope ID.
allowed-tools: Read, WebFetch, Bash
---

Run the contract review. Read the document, explain what it says, flag anything risky, and produce marked-up redlines for the owner to use in negotiations.

Parse arguments:
- `FILE_PATH_OR_DOCUSIGN_ENVELOPE_ID` — path to a local PDF/docx file, or a DocuSign envelope ID; if omitted, check the most recent envelope awaiting signature in DocuSign

## Step 1 — Load the contract

Using the `contract-review` skill workflow:

1. If a file path is given: read the document from Files or Desktop.
2. If a DocuSign envelope ID is given: pull the document from DocuSign.
3. If neither: check DocuSign for the most recent envelope with status `waiting for signature` and confirm with the owner before proceeding.

## Step 2 — Plain-English summary

Produce a 3-paragraph summary:
1. **What this contract does** — the deal in plain terms (who, what, how much, how long)
2. **Key obligations** — what the owner must do and when
3. **Key rights** — what the owner gets and any termination or exit paths

## Step 3 — Red-flag list

For each risk, rate severity: 🔴 High / 🟡 Medium / 🟢 Low

Flag at minimum:
- Auto-renewal clauses with short cancellation windows
- Unilateral price change rights
- Broad IP ownership transfers
- Unlimited liability or missing liability cap
- Exclusivity clauses
- Non-compete or non-solicit provisions
- Ambiguous payment or deliverable terms

Format each flag as:
```
{Severity} {Clause name} — {what it says in plain English} — Suggested redline: {fix}
```

## Step 4 — Marked-up redlines

Generate a list of specific redline suggestions in legal markup format:
```
§{section}: DELETE "[original language]" / INSERT "[suggested replacement]"
Reason: {one sentence}
```

Offer to export this as a marked-up docx or PDF to Files or Desktop.

## Connector failures

If DocuSign is not connected and no file path was given, ask the owner to upload the contract as a PDF or docx. If DocuSign is connected but the envelope ID is invalid, report the error and ask the owner to check the ID. This command works fully offline with a local file — connectors are optional.

## Approval gates

- **Never sign, send, or modify the actual DocuSign envelope.** Present the review and wait for the owner to act.
- **Always caveat:** "This is not legal advice. Review with your attorney before signing."
- **Never delete or overwrite the original document.**

## Output

Present the plain-English summary, red-flag list, and redline suggestions. Ask the owner whether to export a marked-up copy and where to save it.
