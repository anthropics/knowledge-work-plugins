# Deriving the Ideal Customer Profile

The profile comes from customers who already pay, not from the owner's description. Owners describe aspiration; the data describes reality, and the two are usually different in an important way.

---

## The method

**1. Pull every customer with revenue attached.**

From QuickBooks: customer name, total revenue, first invoice date, average days to pay. From HubSpot: industry, size, source, deal cycle length. From an uploaded CSV: whatever columns exist.

**2. Rank by value, not by revenue alone.**

A customer worth having is one that pays well, pays on time, and stays. Rank on all three:

```
value = total revenue x tenure in years, discounted for slow payment
```

A USD 40,000 customer who takes 70 days to pay and left after a year is not better than a USD 22,000 customer in year four who pays in 12 days.

**3. Split top and bottom quartile.**

Take the top 25% and the bottom 25%. The middle tells you nothing.

**4. Find what separates them.**

Compare across every dimension available:

- Industry or trade
- Company size — employees, locations, revenue band
- Geography — distance from the owner, urban or rural
- How they arrived — referral, search, ads, walk-in
- What they bought first
- Season or month they arrived

The useful finding is a dimension where the two quartiles genuinely differ. If both quartiles are evenly spread across industries, industry is not part of the profile — say so rather than including it for completeness.

**5. State the profile in the owner's language.**

```
Best customers look like:
  <industry or trade>, <size band>, <geography>
  usually found via <channel>
  first purchase is typically <product or service>

Worst customers look like:
  <the counter-pattern, when it's clear>
```

The counter-pattern matters as much as the pattern. "Anyone under 10 employees churns inside a year" saves more money than any targeting criterion.

---

## Worked example

An HVAC contractor's customer export, 340 rows.

**Top quartile shared:** commercial property managers, 3 or more buildings, within 25 miles, arrived by referral, first job was a maintenance contract rather than a repair.

**Bottom quartile shared:** single-property residential, arrived from a search ad, first job was an emergency repair.

**Profile written back:**

```
Best customers look like:
  Commercial property managers with 3+ buildings, inside 25 miles.
  Usually arrive by referral.
  First job is a maintenance contract, not an emergency call.

Worst customers look like:
  Single-property residential from search ads calling for an emergency fix.
  They pay once and never come back.
```

The owner's correction: "Right, but property managers with more than about 15 buildings go to the big regional firms. Cap it."

That correction is worth more than the entire enrichment step, and it only surfaces when you show the profile back.

---

## When there's very little data

Some owners have twenty customers and no CRM. The method still works, it just runs by hand — read the twenty, ask which five they would clone, and find what those five share.

With fewer than about ten customers, the honest answer is that there is no statistical pattern yet. Say so, and build the profile from the owner's judgment instead. Do not dress up a hunch as analysis.

---

## What not to include in the profile

**Anything the owner can't act on.** "Companies with strong internal culture" is not a targeting criterion.

**Dimensions where top and bottom look the same.** Including them makes the profile look thorough and makes the search worse.

**More than five criteria.** Every additional filter shrinks the result set geometrically. Five is usually enough to find look-alikes; eight finds nobody.
