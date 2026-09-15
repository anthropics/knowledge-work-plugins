# Tax Calculation Assumptions — figures are for the 2025 tax year

This file documents the math and assumptions used in quarterly estimated tax calculations.
Always surface these assumptions in the output so the accountant can adjust.

> **Every rate, bracket, wage base, and due date below is a 2025 figure.** The math
> does not go stale; the numbers do. Before using any number from this file, check it
> against the tax year the owner is actually asking about.
>
> **If the tax year in question is not 2025:** do not quietly reuse these figures and
> do not invent replacements. Say so in the output, in the owner's own words:
>
> > "The bracket, wage base, and due dates I used are 2025 figures and you're asking
> > about <year>. Those change every year. Either give me the current numbers, or
> > treat everything below as a rough shape and let your accountant put the real
> > figures in."
>
> If a current-year figure can be fetched from an authoritative source (IRS.gov or a
> published IRS revenue procedure), use it and cite where it came from and the date
> fetched. Otherwise the fallback is asking the owner, never guessing. A bracket table
> invented from memory looks exactly like a real one on the page.

---

## Self-employment (SE) tax

SE tax applies to sole proprietors, single-member LLCs, and partners. It does **not** apply
to S-corp owners on their W-2 wages (only on distributions — and even that varies).

**Formula:**
```
SE tax base     = net profit × 92.35%
                  (the 7.65% reduction accounts for the employer-equivalent deduction)
SE tax          = SE tax base × 15.3%
                  (12.4% Social Security + 2.9% Medicare)
                  Note: Social Security only applies up to the wage base (USD 176,100 for 2025)
Deductible half = SE tax ÷ 2   ← reduces taxable income
```

**Example:**
```
Net profit:      USD 80,000
SE tax base:     USD 80,000 × 92.35% = USD 73,880
SE tax:          USD 73,880 × 15.3%  = USD 11,304
Deductible half: USD 11,304 ÷ 2      = USD 5,652
```

---

## Federal income tax estimate

### Business types and how they're taxed

| Business type | How income is taxed | SE tax applies? |
|--------------|---------------------|-----------------|
| Sole proprietor / single-member LLC | Schedule C → personal 1040 | Yes |
| Partnership / multi-member LLC | Schedule K-1 → personal 1040 | Yes (on earned income) |
| S-corporation | W-2 wages + K-1 distributions → 1040 | On wages only |
| C-corporation | Separate corporate return | No (payroll taxes instead) |

Default assumption: **sole proprietor** unless the user specifies otherwise. Always state this.

### Federal income tax brackets (2025 tax year, single filer)

| Taxable income | Rate |
|---------------|------|
| USD 0 – USD 11,925 | 10% |
| USD 11,926 – USD 48,475 | 12% |
| USD 48,476 – USD 103,350 | 22% |
| USD 103,351 – USD 197,300 | 24% |
| USD 197,301 – USD 250,525 | 32% |
| USD 250,526 – USD 626,350 | 35% |
| Over USD 626,350 | 37% |

**For a rough estimate**, apply a single effective rate. Use 22% as the default for most SMB
owners unless the user gives you more info. Note this assumption explicitly.

**Adjusted net income** (for tax calculation):
```
Adjusted net = net profit − (SE tax ÷ 2) − QBI deduction (if applicable)
```
The QBI deduction (up to 20% of qualified business income) is significant for many SMBs —
note that it's not included in the base estimate and the accountant should apply it.

---

## YTD net profit vs. annualized net profit

These are two different numbers and mixing them up is the easiest way to hand an
owner a wrong figure. Be explicit about which one each line uses.

- **YTD net profit** — what the books actually show from January 1 through the end
  of the last completed quarter. A fact.
- **Annualized net profit** — YTD net profit projected across the full year. An
  estimate, and only ever an estimate.

```
annualized_net = YTD_net ÷ months_elapsed × 12
```

**The tax math runs on the annualized figure**, because SE tax, the bracket, and the
wage base all apply to a full year of income. Run SE tax and federal income tax on
annualized net, then divide the resulting annual liability across quarters.

**Show both numbers, always labeled**, so the owner can see the projection for what
it is:

```
YTD net profit (Jan 1 – Jun 30):   USD 64,000   actual, from the books
Annualized net profit:            USD 128,000   projected, YTD ÷ 6 months × 12
```

Straight-line annualizing assumes the rest of the year looks like the part already
banked. For a seasonal business that is simply wrong. **Ask once** whether the year
runs evenly, and if it does not, use the owner's own sense of the full year and label
it "owner estimate, not projected from YTD."

---

## Quarterly due dates (2025 tax year)

| Quarter | Period covered | Payment due |
|---------|---------------|-------------|
| Q1 | Jan 1 – Mar 31 | April 15, 2025 |
| Q2 | Apr 1 – May 31 | June 16, 2025 |
| Q3 | Jun 1 – Aug 31 | September 15, 2025 |
| Q4 | Sep 1 – Dec 31 | January 15, 2026 |

Dates shift by a day or two each year around weekends and holidays. Confirm the
current year's dates rather than carrying these forward.

---

## When a quarter has already been missed

Today's date can land past a due date with nothing paid against it. Do not fold a
missed quarter silently into the remaining ones — say it out loud, because a late
payment accrues interest and penalty from its own due date, not from the next one.

Handle it in three parts:

1. **Name what was missed.** "Q2 was due June 16 and I don't see a payment against
   it." Amount and date, not a vague warning.
2. **Show the catch-up separately from the going-forward number.** One line for what
   is late, one line for the next scheduled payment. Two decisions, two figures.
3. **Send the penalty question to the accountant.** Underpayment penalty and interest
   are computed per quarter on Form 2210 and depend on prior-year figures this skill
   does not have. Flag that it applies; never estimate the amount.

The remaining-quarters division only covers quarters still ahead. If none are left,
say the balance is due with the return and note the filing deadline.

---

## Safe harbor rule

To avoid underpayment penalties, total estimated payments must be at least the lesser of:
- **100%** of prior year tax liability (or **110%** if prior year AGI exceeded USD 150,000)
- **90%** of current year tax liability

Always note this in output. The user's accountant should confirm prior-year tax figures.

---

## What the estimate does NOT include

Always list these exclusions in every output:
- State and local income taxes
- QBI deduction (Section 199A — can reduce federal tax by up to 20%)
- Home office deduction
- Vehicle deductions
- Depreciation / Section 179
- Retirement contributions (SEP-IRA, Solo 401k) — can significantly reduce SE tax base
- Health insurance deduction for self-employed
- Prior-year net operating loss carryforward

These can meaningfully reduce the final number. Flag them so the accountant applies them.
