# Data Sources

Where the numbers come from, how to get them without a connector, and how to reconcile the two stories they tell.

---

## Connectors

| Source | Status | What to pull |
|---|---|---|
| Canva | Available | Creative asset generation from a written brief |
| TikTok Ads | The native connected path (TikTok MCP) | Spend, impressions, clicks, results, cost per result — at campaign, ad group, and ad level |
| Google Ads | No native connector — reached through a Zapier connection built with `build-connector`, offered once when the owner runs ads there | Whatever the connected Zapier actions expose. CSV export still works when no connection exists |
| HubSpot | Optional but high value | Leads by source, deals closed by source — the truth check on platform claims |
| QuickBooks, Shopify, Square | Optional | Revenue actually collected in the period |

**Check before assuming.** If a TikTok call or a Zapier action fails, do not retry in a loop and do not stall. Say the path is not available, switch to the export path, and keep going. Never call a platform with no native connector directly — it runs through a built Zapier connection or a CSV.

---

## The CSV export path

This is the common path. Treat it as the default, not the fallback.

### What to ask for, in the owner's words

- **Google Ads:** "In Google Ads, go to Campaigns, set the date range to last 30 days, click the download icon, choose CSV."
- **TikTok:** "Ads Manager, Campaign tab, Export, last 30 days."

Ask for 90 days too when the question is about trend rather than this month. Say why: "30 days tells us where we are, 90 tells us which way it's moving."

### Reading the file

Header names differ by platform and by export settings. Map, do not assume.

| What you need | Common column names |
|---|---|
| Spend | `Amount spent (USD)`, `Cost`, `Total spent` |
| Impressions | `Impressions`, `Impr.` |
| Clicks | `Clicks (all)`, `Link clicks`, `Clicks` |
| Results | `Results`, `Conversions`, `Leads`, `Purchases` |
| Cost per result | `Cost per result`, `Cost / conv.` — or compute it |
| Reach and frequency | `Reach`, `Frequency` |
| Date range | Usually in a header row above the table, not a column |

**Two traps in real exports.** First, `Results` can mean different things per campaign — one row's result is a lead form, another's is a page view. Check the `Result type` column if it exists; if it does not, say the results are not comparable across campaigns rather than summing them. Second, currency symbols and thousands separators arrive as text. Strip them before arithmetic.

If a column you need is absent, name it: "This export has spend and clicks but no conversion column, so I can tell you what traffic cost and nothing about what it produced." Then offer the export setting that would include it.

---

## Reconciling platform numbers against the CRM

The two will never match. The gap is information, not an error.

**Why platforms report more:**

- View-through conversions — someone saw the ad, did not click, bought later
- Cross-device attribution the CRM cannot see
- Attribution windows, often 7 days after a click and 1 day after a view
- Each platform claims the same conversion when a customer touched several ads

**Why the CRM reports fewer:**

- The source field is blank on records created by hand
- Phone calls and walk-ins carry no digital source at all
- Form fills that never became a CRM record

### The method

1. Pull platform-reported results per campaign
2. Pull CRM leads and closed deals with that source, over the same dates
3. Show both, side by side, labeled by who reported them
4. Give the owner one number to steer by — cost per closed job from the CRM — and label the platform figure as the optimistic bound

### Report it like this

```
Paid social — Spring Tune-Up
  Spend                      USD 1,840
  Platform says              34 conversions, USD 54 each
  CRM says                   19 leads tagged to it, 6 became jobs
  Cost per real job          USD 307
  The gap                    The platform counts people who saw the ad and called
                             later. The CRM only counts what got tagged.
                             Real number is probably between the two,
                             closer to the CRM.
```

Never publish one blended figure. Owners forward these numbers to partners and lenders.

---

## When there is no tracking at all

Plenty of small accounts run ads with no pixel and no conversion event. Clicks are the only signal.

Say it plainly: "There's no conversion tracking on this account, so nobody — not me, not the platform — can tell you what these ads produced. We can compare cost per click across campaigns, which tells you which creative got attention, and that is all it tells you."

Then offer the fix as the first recommendation, ahead of any budget change. Tracking before optimization; otherwise every later recommendation rests on nothing.
