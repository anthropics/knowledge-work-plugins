# Output Template

Two artifacts every run: a chat summary, then an XLSX workbook. The summary is the product. The workbook is the appendix.

---

## The chat summary

```
## <Report name> — <period>

<One sentence: the single most important thing this report says.>

**<Metric 1>** — <value>, <delta versus comparison>
**<Metric 2>** — <value>, <delta versus comparison>
**<Metric 3>** — <value>, <delta versus comparison>

### What stands out

- <Finding, naming the specific record or group and the number>
- <Finding>
- <Finding>

### Worth a look

- <Anything that needs a decision, with the suggested next step>

<Workbook attached. Tabs: summary, one per metric group, raw data.>
```

Three findings maximum. A summary with nine bullets is a table with extra steps.

---

## Worked example

```
## Monday operating pack — week of Jul 20

Portland is the only location below last year, and it's the reason total sales are flat.

**Sales** — USD 43,200, up 2% vs. same week last year
**AR past 30 days** — USD 18,400 across 6 invoices
**Labor** — 31% of revenue, up from 28%

### What stands out

- Portland did USD 6,100, down 22% year over year. Every other location is up.
- Labor crossed 30% for the first time in nine weeks, driven by overtime at Salem.
- Acme Corp is USD 4,200 and 47 days past due, with no payment since May 12.

### Worth a look

- Portland's drop is four weeks running now, not a one-week blip. Worth a look at
  staffing or local competition before it becomes the quarter's story.

Workbook attached. Tabs: summary, sales by location, AR aging, labor detail, raw data.
```

Notice what the summary does: it names the location, gives the number, states the trend length, and proposes a next step. "Sales were mixed" would have said nothing.

---

## The XLSX workbook

Tab order matters — owners open the first tab and often stop there.

1. **Summary** — the same metrics as the chat summary, as a clean table with comparisons
2. **One tab per metric group** — sales by location, AR aging, labor detail
3. **Raw data** — everything pulled, unmodified, so the owner or their accountant can check the math

Formatting rules that make a workbook usable:

- Header row bold and frozen
- Currency formatted as currency, percentages as percentages — not raw floats
- Deltas in their own column, not jammed into the value cell
- Negative numbers in parentheses or red, consistently
- A footer row on each tab naming the source and the pull timestamp

Build the workbook with a script rather than assembling cells by hand. It is faster, and it reruns identically next month.

---

## When data is missing

Never omit a metric silently. A missing row reads as a data problem the owner will go hunting for.

```
**Labor** — n/a (QuickBooks payroll accounts unavailable this run)
```

Then repeat every unavailable source once, at the bottom:

```
Not available this run: QuickBooks payroll accounts, Square (auth expired).
Everything else pulled clean.
```

---

## Partial periods

A month-to-date figure compared against a full prior month always looks like a collapse. Either compare like-for-like, or label it:

```
**Sales** — USD 21,400 month-to-date through Jul 27 (prior month same-day: USD 19,800, up 8%)
```

Never show a partial period against a full one without saying so. That single mistake has sent owners into a panic over a number that was fine.
