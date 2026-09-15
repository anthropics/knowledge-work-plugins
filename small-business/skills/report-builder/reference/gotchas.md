# Gotchas

Failure modes that produce a report that looks right and is quietly wrong. Those are the dangerous ones — owners forward these reports to banks, boards, and accountants.

---

## Gotcha: partial period compared against a full one

**Why it matters:** On July 27, month-to-date sales versus last full month looks like a 20% collapse. It isn't. Owners have made staffing decisions off this mistake.

### Bad

```
Sales — USD 21,400, down 19% vs. June
```

June was a full month. July is three days short. The comparison is meaningless and the owner reads it as a crisis.

### Good

```
Sales — USD 21,400 month-to-date through Jul 27
        (June through the 27th: USD 19,800, up 8%)
```

Same data, honest comparison, opposite conclusion.

---

## Gotcha: the same sale counted twice

**Why it matters:** A Shopify order settled through Stripe and recorded in QuickBooks exists in three systems. Summing across connected sources inflates revenue, sometimes by double.

### Bad

```
Pull revenue from QuickBooks + Shopify + Stripe, sum all three.
Report shows USD 129,000. Actual revenue was USD 43,000.
```

### Good

```
Pick one system as the revenue source. Say which:

Revenue — USD 43,000 (source: QuickBooks; Shopify and Stripe used for
          fulfillment and fee detail only)
```

Rule of thumb: the books are the revenue source when connected. Processors supply fees and timing. Storefronts supply product-level splits.

---

## Gotcha: a group disappears instead of showing zero

**Why it matters:** If Portland sold nothing this week and the row vanishes, the owner assumes the data is broken and goes looking. A zero is information; a missing row is noise.

### Bad

```
Sales by location:
  Salem      USD 18,200
  Eugene     USD 19,000
```

Portland existed last week. Where did it go?

### Good

```
Sales by location:
  Salem      USD 18,200
  Eugene     USD 19,000
  Portland   USD 0        (no sales recorded this period)
```

---

## Gotcha: grouped rows don't tie to the total

**Why it matters:** An owner who adds your columns and gets a different number stops trusting every report you produce after that.

### Bad

Publish the total and the breakdown without checking they agree.

### Good

Check the sum before delivering. If they genuinely don't tie, say why:

```
Sales by location sums to USD 41,900. Total sales is USD 43,200.
The USD 1,300 gap is unallocated invoices with no location set.
```

Naming the gap builds more trust than hiding it.

---

## Gotcha: re-interviewing about a saved report

**Why it matters:** The whole promise of this skill is "describe it once." Asking the same five questions every month breaks that promise and the owner stops using it.

### Bad

```
Owner: "Run the Monday report."
Claude: "Sure — which metrics would you like, and what period should it cover?"
```

### Good

```
Owner: "Run the Monday report."
Claude: [reads saved_reports.md, finds it, runs it]
        "Monday operating pack — week of Jul 20..."
```

Always read `saved_reports.md` first.

---

## Gotcha: a plausible number filled in for a missing one

**Why it matters:** This is the most serious failure in the skill. A report is a document owners act on and forward. An invented figure that looks reasonable can survive several hands before anyone catches it.

### Bad

```
Labor — approximately 30% of revenue
```

Where did that come from? Nowhere. Payroll accounts didn't return.

### Good

```
Labor — n/a (QuickBooks payroll accounts unavailable this run)
```

Never estimate, never round toward a guess, never carry last period's figure forward silently.

---

## Gotcha: leading with the table

**Why it matters:** Owners asked for a report because they want a decision. A wall of numbers hands the analysis back to them, which is the job they were trying to hand off.

### Bad

Open with a 40-row table, then a summary underneath it.

### Good

Open with the one sentence that matters, three headline metrics, three findings. Everything else goes in the workbook.
