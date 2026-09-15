# Worked Example: Year-End 1099 Prep

**Scenario:** Marcus owns a digital marketing agency. He asks: "I need to send out
my 1099s — can you pull together a list of who needs one?"

---

## Step 1: Pull contractor payments from all sources

**QuickBooks** (Jan 1 – Dec 31, 2024):

| Vendor | Total paid | 1099 eligible? | EIN/SSN on file? |
|--------|-----------|----------------|-----------------|
| Jenna Torres (copywriter) | USD 8,400 | Yes | Yes |
| Apex Web Solutions | USD 15,200 | Yes | Yes |
| Bob Nguyen | USD 550 | No | No |
| FedEx | USD 320 | No | No |
| Spark Digital Inc. | USD 6,000 | Yes | Yes |

**PayPal** (goods & services payments sent, 2024):

| Recipient | Total sent | Notes |
|-----------|-----------|-------|
| jenna.torres@email.com | USD 1,200 | Likely same as QuickBooks vendor |
| designbymike@gmail.com | USD 2,100 | Not in QuickBooks |
| Bob Nguyen | USD 480 | |

**Stripe** (not connected — skipped)

---

## Step 2: Aggregate and deduplicate

Cross-referencing QuickBooks and PayPal:

| Payee | QuickBooks | PayPal | Total | Notes |
|-------|-----------|--------|-------|-------|
| Jenna Torres | USD 8,400 | USD 1,200 | **USD 9,600** | Same person — email match |
| Apex Web Solutions | USD 15,200 | — | **USD 15,200** | |
| Spark Digital Inc. | USD 6,000 | — | **USD 6,000** | |
| Northwind Design (owner unknown) | — | USD 2,100 | **USD 2,100** | Not in QuickBooks; payee name unknown |
| Bob Nguyen | USD 550 | USD 480 | **USD 1,030** | Combined > USD 600; flagged |
| FedEx | USD 320 | — | USD 320 | Below threshold; goods/shipping — exempt |

---

## Step 3: Apply USD 600 threshold and W-9 check

- Jenna Torres: USD 9,600 ✅ → **1099-NEC required** · W-9 on file (EIN recorded in QB)
- Apex Web Solutions: USD 15,200 ✅ → **1099-NEC candidate** · W-9 on file · Note: may be a corp (confirm)
- Spark Digital Inc.: USD 6,000 ✅ → **1099-NEC candidate** · W-9 on file · "Inc." — likely corp exempt (confirm)
- Northwind Design: USD 2,100 ✅ → **1099-NEC required** · W-9 not on file — must collect
- Bob Nguyen: USD 1,030 ✅ → **1099-NEC required** · W-9 not on file — must collect
- FedEx: USD 320 → below threshold; goods/shipping — not required

---

## Step 4: Output delivered to Marcus

```
## 1099 prep list — 2024
Prepared January 10, 2025 · For review by your accountant · Not tax advice

### Summary
- Contractors paying: 5 candidates identified
- Require 1099-NEC (≥USD 600 for services): 5
- Missing W-9: 2 — action required before January 31
- Corporation exemption review needed: 2 (Apex, Spark)
- PayPal overlap: 2 contractors (Jenna Torres, Northwind Design) — see note below

### 1099-NEC candidates

| Payee | Total paid | Source(s) | W-9 status | Notes |
|-------|-----------|-----------|------------|-------|
| Jenna Torres | USD 9,600 | QB + PayPal | ✅ EIN on file | PayPal also paid USD 1,200 — confirm 1099-K handling |
| Apex Web Solutions | USD 15,200 | QuickBooks | ✅ EIN on file | "Solutions" — may be corp; confirm exemption with accountant |
| Spark Digital Inc. | USD 6,000 | QuickBooks | ✅ EIN on file | "Inc." — likely corp-exempt; confirm with accountant |
| Northwind Design | USD 2,100 | PayPal only | ⚠️ Missing W-9 | Full name unknown — obtain before filing |
| Bob Nguyen | USD 1,030 | QB + PayPal | ⚠️ Missing W-9 | Combined QB (USD 550) + PayPal (USD 480) = USD 1,030 |

### Missing W-9 action list
These contractors must provide a W-9 before you can file:

1. **Northwind Design** — paid USD 2,100 via PayPal. Obtain full legal name and W-9.
   IRS W-9 form: https://www.irs.gov/pub/irs-pdf/fw9.pdf
2. **Bob Nguyen** — paid USD 1,030 (QB + PayPal). W-9 not on file for either source.

### Payment processor note (PayPal)
Jenna Torres and Northwind Design received payments via PayPal. PayPal issues its own
1099-K to contractors receiving ≥USD 600 in goods & services payments. Your accountant
should confirm whether you still need to issue a 1099-NEC for these two, or whether
PayPal's 1099-K covers the reporting obligation.

### Next steps for your accountant
- [ ] Collect W-9 from Northwind Design (full legal name needed first)
- [ ] Collect W-9 from Bob Nguyen
- [ ] Confirm corporation exemption for Apex Web Solutions
- [ ] Confirm corporation exemption for Spark Digital Inc.
- [ ] Confirm 1099-K overlap handling for Jenna Torres and Northwind Design (PayPal)
- [ ] File 1099-NECs by January 31, 2025
- [ ] File 1096 transmittal with IRS by January 31, 2025
```
