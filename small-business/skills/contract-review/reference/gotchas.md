# Gotchas

Edge cases in contract analysis. Good / Bad pairs.

---

## Gotcha: Flagging standard boilerplate as a red flag

**Why it matters:** Over-flagging trains the user to ignore the summary. If everything is a red flag, nothing is.

### ✗ Bad

```
Contract has a standard mutual NDA confidentiality clause, 2-year duration.
Claude: "🔴 Red flag: Confidentiality clause imposes obligations on both parties."
```

Standard mutual NDA is market-norm. Flagging it as a red flag destroys signal-to-noise ratio.

### ✓ Good

```
Contract has a standard mutual NDA confidentiality clause, 2-year duration.
Claude: [skips; does not flag]
```

Reserve red flags for genuinely non-standard terms. If a clause is boilerplate and fair, omit it.

---

## Gotcha: Missing clauses aren't missing from the analysis

**Why it matters:** For SMBs, the absence of standard protections (liability cap, change order process, consequential damages waiver) is often more dangerous than an unfavorable clause — the default legal position fills the gap, usually in the counterparty's favor.

### ✗ Bad

```
Contract has no liability cap.
Claude: [no mention; only analyzes clauses that are present]
```

User signs thinking liability is limited. It isn't.

### ✓ Good

```
Contract has no liability cap.
Claude: "🔴 Missing: No liability cap. This contract contains no limitation-of-liability
clause. Under default law, your exposure is uncapped. Standard practice is to cap at
fees paid in the prior 12 months. Suggest adding: 'Each party's total liability shall
not exceed the fees paid or payable in the 12 months preceding the claim.'"
```

Treat absent-but-standard clauses as red flags. Explicitly label them "Missing."

---

## Gotcha: Large PDFs truncated mid-analysis

**Why it matters:** Contracts over 20–30 pages often have the most dangerous terms in exhibits, schedules, or "Order Forms" at the back. If the PDF is read only up to page 15, key terms are silently missed.

### ✗ Bad

```
Skill reads pages 1–10 of a 40-page MSA. Schedules A–D (starting page 28) contain
the IP assignment and liability cap. Skill produces a "clean" summary.
```

### ✓ Good

```
Read the PDF in chunks: pages 1–10, 11–20, 21–40. Analyze all chunks before
producing the summary. If a section heading mentions "Schedule," "Exhibit," or
"Appendix," flag it explicitly and ensure it was read.
```

Always read the full document. Use the `pages` parameter to chunk large PDFs.

---

## Gotcha: Counterparty template vs. negotiated draft

**Why it matters:** Recommendations should match the negotiating context. Pushing back hard on a startup's first-draft agreement is different from pushing back on a Fortune 500 procurement template — the latter is often non-negotiable on 80% of its terms.

### ✗ Bad

```
Fortune 500 vendor agreement with standard procurement terms.
Claude: "🔴 This Net-60 payment term should be renegotiated to Net-30.
         Their legal team will likely accept the change."
```

Unrealistic recommendation wastes the user's political capital.

### ✓ Good

```
Claude: "🟡 Net-60 payment terms. This is longer than typical (Net-30 is standard),
         but common in large enterprise procurement templates. Worth asking for
         Net-45 as a compromise — they may accept it, especially for recurring work.
         Note: if this is a Fortune 500 template, payment terms are often non-negotiable
         in the first engagement."
```

Match the recommendation to the power dynamic. Label it yellow, not red. Acknowledge the reality.
