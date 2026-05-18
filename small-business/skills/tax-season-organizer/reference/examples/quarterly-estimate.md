# Worked Example: Quarterly Estimated Tax

**Scenario:** Sarah runs a freelance graphic design business as a sole proprietor.
She asks: "How much should I pay in estimated taxes for Q2?"

---

## Step 1: Pull YTD P&L from QuickBooks

QuickBooks P&L — January 1 through March 31, 2025:
- Gross income: $48,000
- Operating expenses: $12,500 (software, equipment, marketing)
- Net ordinary income: **$35,500**

---

## Step 2: Ask about prior payments

> "Have you made any estimated tax payments so far this year?"

Sarah: "I paid $2,000 in April for Q1."

---

## Step 3: Calculate

```
YTD net profit (Q1):        $35,500
Annualized net profit:      $35,500 × 4 = $142,000  ← rough annualization

Self-employment tax:
  SE base:   $142,000 × 92.35%  = $131,137
  SE tax:    $131,137 × 15.3%   = $20,064
  (Soc. Sec. cap at $176,100 — not hit, full rate applies)
  Deductible half:              = $10,032

Federal income tax:
  Adjusted net: $142,000 − $10,032 = $131,968
  Bracket: 22% (estimated; actual may vary with household income)
  Federal tax:  $131,968 × 22%     = $29,033

Total estimated annual liability:
  SE tax + federal = $20,064 + $29,033 = $49,097

Quarterly breakdown:
  Annual liability:       $49,097
  Payments made (Q1):    −$2,000
  Remaining:              $47,097 ÷ 3 remaining quarters = $15,699 per quarter
  Q2 payment due June 16: ~$15,700
```

---

## Step 4: Output delivered to Sarah

```
## Estimated tax summary — Q2 2025
Prepared April 24, 2025 · For review by your accountant · Not tax advice

**YTD net profit (Jan 1 – Mar 31):** $35,500
**Estimated annual net profit:** $142,000 (annualized from Q1 actual)
**Business type assumed:** Sole proprietor (confirm with accountant)

### Self-employment tax
$142,000 × 92.35% × 15.3% = $20,064
Deductible SE half: $10,032

### Federal income tax estimate
Adjusted net income: $131,968
Assumed bracket: 22% (confirm with accountant — household income affects this)
Federal income tax estimate: $29,033

### Total estimated annual liability
$20,064 + $29,033 = **$49,097**

### Q2 payment
Annual liability:      $49,097
Less Q1 payment made: −$2,000
Remaining:             $47,097 ÷ 3 quarters = **~$15,700 due by June 16, 2025**

### Safe harbor note
To avoid underpayment penalty: ensure total 2025 payments ≥ 100% of your 2024
tax (or 110% if 2024 AGI > $150,000). Ask your accountant for that figure.

### Assumptions — review with your accountant
- Federal bracket: 22% (effective rate may differ)
- Business structure: sole proprietor (assumed)
- Annualization: Q1 × 4 — income may be seasonal
- State taxes: not included
- QBI deduction (up to 20%): not applied — could reduce federal tax significantly
- Retirement contributions, home office, vehicle: not applied
```
