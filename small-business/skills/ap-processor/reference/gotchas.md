# Gotchas

The failure modes that pay a bill twice, pay the wrong one, or quietly wreck the books. Every one of these has a dollar value attached.

---

## Gotcha: reading a total that isn't legible

**Why it matters:** The extracted total flows into the coded entry, the payment run, and the cash forecast. A confident wrong number is worse than a blank, because nobody checks a number that looks fine.

### Bad

```
Watsco, invoice 40218, total USD 1,847.00
```
(read from a glare-washed photo where only "1,84" was visible)

### Good

```
Watsco, invoice 40218 — total unreadable, glare across the amount block.
Vendor, date, and PO are clear. Send me the figure or a better photo and
this one's ready.
```

---

## Gotcha: the same invoice on the email and the statement

**Why it matters:** Duplicate payment is the most expensive thing that goes wrong in AP, and it is quiet. The vendor rarely calls to say you overpaid.

### Bad

Stage the emailed PDF as a bill. Later, stage the statement line as a second bill because it has a different reference. Pay both.

### Good

Match on vendor plus invoice number before coding anything. Flag the pair, name both sources, and let the owner confirm. Statements never create entries on their own.

---

## Gotcha: treating approval of coding as approval to pay

**Why it matters:** These are different decisions. An owner who agreed to file bills has not agreed to move USD 22,000. Getting this wrong once ends the trust relationship that makes the rest of the plugin useful.

### Bad

```
Staged 19 bills and scheduled the payment run for Thursday.
```

### Good

```
19 bills staged in QuickBooks, USD 41,208, all as unpaid.
Separately: 11 of them are due or discountable this week, USD 22,140.
Want me to build that payment run?
```

---

## Gotcha: auto-paying the recurring bill

**Why it matters:** Recurrence tells you the account code. It tells you nothing about whether the amount is right this month. Rate increases arrive inside recurring bills, and an auto-approved run is where they slip past.

### Bad

Insurance bill arrives, matches last month's vendor and account, goes straight into the run.

### Good

Code it automatically, include it in the proposal, and flag that it moved from USD 1,410 to USD 1,690 — up 20%. The owner may have agreed to that. Often they did not.

---

## Gotcha: splitting a job cost evenly because the split is unknown

**Why it matters:** An invented allocation is indistinguishable from a real one three months later, when the owner is trying to work out why the Maple St job lost money.

### Bad

USD 3,400 supply invoice, three jobs open, code USD 1,133 to each.

### Good

Code the whole thing to the most likely job, flag it as unsplit, and ask. A flagged single coding gets fixed. A tidy fake split never does.

---

## Gotcha: staging a Ramp or Expensify charge as a payable

**Why it matters:** It is already paid. Staging it creates a liability that does not exist and sets up a genuine double payment.

### Bad

Card feed and bill inbox both processed into the same payables list.

### Good

Card charges get coded, not staged for payment. Keep them in a separate bucket and say so in the summary.

---

## Gotcha: dropping an excluded bill silently

**Why it matters:** A bill held back for a good reason still has a vendor waiting on it. Silence turns a careful exclusion into a late payment.

### Bad

Present a clean run of 11 bills. Say nothing about the 3 that were held.

### Good

```
Held 3: Johnstone (billed 12, received 8), Grainger (no receiving record),
Watsco (total unreadable). None of these are late yet. Two need the vendor.
```

---

## Gotcha: creating a vendor record from a bad name read

**Why it matters:** "ACME SUPPLY #4412" as a new vendor splits the history that makes future coding automatic, and it makes the AP aging report wrong.

### Bad

New vendor created for every branch number and formatting variant.

### Good

Fuzzy-match against existing vendors first, propose the match, and only create a record when the owner confirms it is genuinely new.
