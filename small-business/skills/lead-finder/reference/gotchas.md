# Gotchas

Failure modes that produce a list nobody calls, or worse, one that damages the owner.

---

## Gotcha: asking the owner to describe their ideal customer

**Why it matters:** Owners describe who they wish they sold to. The data describes who actually pays. These differ in a way that matters, and the gap is usually the whole insight.

### Bad

```
Claude: "Who's your ideal customer?"
Owner:  "Mid-size commercial clients, really anyone who values quality."
```

That produces a search with no usable filters.

### Good

```
Claude: [reads 340 customers from QuickBooks, ranks by value, compares quartiles]
        "Your best customers are commercial property managers with 3 to 15
        buildings inside 25 miles, who came by referral. Your worst are
        residential emergency calls from search ads. Does that match?"
Owner:  "Yes — but over 15 buildings they go to the big regional firms."
```

The owner's job is to correct the profile, not to invent it.

---

## Gotcha: the five-hundred-row list

**Why it matters:** A huge list transfers the qualification work back to the owner, which is the work they were trying to hand off. They open it, cannot tell where to start, and never open it again.

### Bad

Scrape every company in the category within 50 miles. Deliver 512 rows.

### Good

Forty to sixty rows, each with a reason to call, sorted by score. Say what was cut and why:

```
47 companies met the bar; 61 more were found and cut for weak fit.
```

---

## Gotcha: a fabricated email address

**Why it matters:** This is the most damaging failure in the skill. Sending to guessed addresses at volume gets the owner's sending domain flagged. That hurts their real customer email for months, and they will not connect it to a prospect list from six weeks ago.

### Bad

```
Contact: dana.whitfield@ridgelinepg.com
```

Constructed from a naming pattern and presented as fact.

### Good

```
Contact: Dana Whitfield, Facilities Director
Route:   dana.whitfield@ridgelinepg.com
Confidence: inferred — pattern-matched from two other addresses at this
            company, not verified
```

The downstream outreach step treats inferred addresses differently. It can only do that if the confidence level is honest.

---

## Gotcha: an invented buying signal

**Why it matters:** The owner opens the call with the signal. If it is wrong, the call ends immediately and they stop trusting every row on the list.

### Bad

```
Why now: Likely expanding based on industry trends
```

That is a guess wearing the costume of a fact.

### Good

```
Why now: Filed a permit for a 7th building on Mar 14 (county records)
```

Or, honestly:

```
Why now: No specific trigger found — strong fit, cold approach
```

A row with no signal is fine. A row with a fictional one is not.

---

## Gotcha: writing to the CRM without approval

**Why it matters:** A bulk import of 47 companies and 39 contacts into a live CRM is hours to unwind if the owner did not want it, and there is no undo button they can reach.

### Bad

Create the records, then mention it.

### Good

State exactly what will be created, including the tag and the confirmation that nothing existing changes. Wait for a yes.

---

## Gotcha: dead companies on the list

**Why it matters:** Directories go stale. Three bounced calls in a row and the owner abandons the list, regardless of how good rows 4 through 47 are.

### Bad

Take the association roster at face value.

### Good

Confirm each company still exists and still looks active before it goes on the list. It is quick, and it protects the first ten rows — the only ones that get a chance to earn trust.

---

## Gotcha: treating missing Apollo as a blocker

**Why it matters:** Most owners in this segment have no data provider connected and never will. If the skill stalls without one, it does not work for the majority of its audience.

### Bad

```
"I need Apollo connected to build a prospect list."
```

### Good

```
"Apollo isn't connected, so I'll build this from public sources — permit
filings, the property association roster, and review sites. Expect a shorter
list than a data provider would give, but every row will be one I actually
checked."
```

Web-sourced lists are often better per row. Say that plainly rather than apologizing for the path.
