# Tax Calculation Assumptions

This file documents the math and assumptions used in quarterly estimated tax calculations.
Always surface these assumptions in the output so the accountant can adjust.

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
                  Note: Social Security only applies up to the wage base ($176,100 for 2025)
Deductible half = SE tax ÷ 2   ← reduces taxable income
```

**Example:**
```
Net profit:      $80,000
SE tax base:     $80,000 × 92.35% = $73,880
SE tax:          $73,880 × 15.3%  = $11,304
Deductible half: $11,304 ÷ 2      = $5,652
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

### Federal income tax brackets (2025, single filer)

| Taxable income | Rate |
|---------------|------|
| $0 – $11,925 | 10% |
| $11,926 – $48,475 | 12% |
| $48,476 – $103,350 | 22% |
| $103,351 – $197,300 | 24% |
| $197,301 – $250,525 | 32% |
| $250,526 – $626,350 | 35% |
| Over $626,350 | 37% |

**For a rough estimate**, apply a single effective rate. Use 22% as the default for most SMB
owners unless the user gives you more info. Note this assumption explicitly.

**Adjusted net income** (for tax calculation):
```
Adjusted net = net profit − (SE tax ÷ 2) − QBI deduction (if applicable)
```
The QBI deduction (up to 20% of qualified business income) is significant for many SMBs —
note that it's not included in the base estimate and the accountant should apply it.

---

## Quarterly due dates (2025)

| Quarter | Period covered | Payment due |
|---------|---------------|-------------|
| Q1 | Jan 1 – Mar 31 | April 15, 2025 |
| Q2 | Apr 1 – May 31 | June 16, 2025 |
| Q3 | Jun 1 – Aug 31 | September 15, 2025 |
| Q4 | Sep 1 – Dec 31 | January 15, 2026 |

---

## Safe harbor rule

To avoid underpayment penalties, total estimated payments must be at least the lesser of:
- **100%** of prior year tax liability (or **110%** if prior year AGI exceeded $150,000)
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
