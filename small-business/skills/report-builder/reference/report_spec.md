# Report Spec Format

Every report resolves to this structure before any data is pulled. The spec is what gets saved, and it's what makes a report repeatable.

---

## The format

```
Report name:  <short, owner-recognizable>
Cadence:      one-off | weekly | monthly | quarterly
Period:       <the window each run covers>
Comparison:   <prior period | same period last year | target | none>
Grouping:     <dimension, or none>

Metrics:
  <name>  =  <formula>  [source]
  <name>  =  <formula>  [source]

Sources:      <connectors used, or "uploaded file">
Notes:        <anything the owner clarified>
```

---

## Worked example 1 — the classic

**Owner said:** "Every Monday: sales by location vs last year, AR aging, labor percent."

```
Report name:  Monday operating pack
Cadence:      weekly, Monday
Period:       trailing 7 days
Comparison:   same 7 days last year
Grouping:     location

Metrics:
  Sales          =  sum of invoice totals, excluding tax   [QuickBooks]
  AR aging       =  open invoices bucketed 0-30 / 31-60 / 61+ days past due   [QuickBooks]
  Labor percent  =  payroll expense / net revenue          [QuickBooks]

Sources:      QuickBooks
Notes:        Labor measured against revenue, not total costs (confirmed).
              AR aging is company-wide, not split by location.
```

Note what was inferred and what was asked. Metric, grouping, and comparison came straight from the sentence. Only the labor denominator and the AR grouping needed a question.

---

## Worked example 2 — no connectors

**Owner said:** "I need a monthly report showing which products make the most money."

```
Report name:  Monthly product profitability
Cadence:      monthly, first business day
Period:       prior calendar month
Comparison:   prior month
Grouping:     product

Metrics:
  Revenue       =  sum of line totals by SKU        [uploaded sales CSV]
  Units         =  sum of quantity by SKU           [uploaded sales CSV]
  Gross margin  =  (revenue - COGS) / revenue       [uploaded sales CSV]

Sources:      uploaded file — monthly sales export
Notes:        COGS column must be present in the export. If absent, report
              revenue and units only and say margin is unavailable.
```

The no-connector path produces exactly the same shape of spec. Nothing about the report is degraded except where the data itself is missing.

---

## Worked example 3 — pipeline, cross-source

**Owner said:** "Show me every month how the pipeline is converting and what it's actually worth."

```
Report name:  Monthly pipeline conversion
Cadence:      monthly
Period:       prior calendar month
Comparison:   prior month
Grouping:     deal stage

Metrics:
  Deals entered     =  count of deals created in period       [HubSpot]
  Deals won         =  count of deals closed-won in period    [HubSpot]
  Win rate          =  deals won / deals resolved             [HubSpot]
  Weighted pipeline =  sum of (deal value x stage probability) [HubSpot]
  Revenue realized  =  invoices paid in period                [QuickBooks]

Sources:      HubSpot, QuickBooks
Notes:        Revenue realized is deliberately from the books, not the CRM.
              CRM deal values are forecasts; invoices are facts.
```

---

## Rules that keep specs honest

**Every metric names its source.** A metric without a source is a metric nobody can reproduce next month.

**Formulas are written out, not implied.** "Labor percent" means nothing on its own. "Payroll expense divided by net revenue" can be checked.

**Ambiguity gets recorded in Notes, not silently resolved.** When the owner clarifies something, write down what they said. Six months later that note is the only record of why the number is calculated the way it is.

**One report, one purpose.** If an owner describes eight unrelated metrics, that is probably two reports. Suggest the split rather than building one unreadable pack.
