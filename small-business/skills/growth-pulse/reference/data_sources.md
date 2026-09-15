# Data Sources

Which connector answers which part of the pulse. Pull in one parallel batch.

---

## HubSpot — the funnel

The spine of this skill. Without it, funnel conversion is unavailable and the pulse leans on revenue trend instead.

| View | What to pull |
|---|---|
| Funnel conversion | Deals by stage, with create and close dates |
| Lead volume | Contacts created in period, with source property |
| Lead source mix | Contacts grouped by original source |
| Win rate | Deals closed-won divided by deals resolved |
| Cycle time | Median days from create to close, won deals only |
| Stalled deals | Deals with no activity in 14+ days, or close date in the past and still open |
| Response speed | Time from contact creation to first logged activity |

**Careful with deal value.** It is a forecast, not revenue. Never present weighted pipeline as money earned.

**Fallback:** a CRM deal export as CSV gives the same funnel views.

---

## Revenue sources

| Source | Best for |
|---|---|
| QuickBooks | Realized revenue — the number that ties to the books |
| Stripe, PayPal | Settlement timing, fees, refunds, subscription revenue |
| Square | In-person and per-location revenue |
| Shopify | Order counts, SKU-level revenue, repeat purchase rate |

**Pick one as the revenue source per pulse and say which.** When QuickBooks is connected, it wins — processors and storefronts then supply channel and product splits only. Summing across them double-counts, sometimes by more than double.

**Then guard against double-counting inside that one source.** The QuickBooks sales-by-customer summary emits a parent summary row and a separate total row for the same customer whenever sub-customers or jobs exist. Both carry the same amount, and the report's own top-customer list contains both. Filter rows whose metadata type marks them as a total before ranking customers or computing concentration; otherwise one customer occupies two slots in the ranking and the concentration figure is inflated.

---

## Ad platforms

| Source | What to pull |
|---|---|
| TikTok Ads | Native connector. `report_integrated_get` at campaign level for the last 7 days and the prior 7: spend, impressions, clicks, results, cost per result. `advertiser_info_get` first to confirm the account. Same reads and traps as `ad-manager` (`../../ad-manager/SKILL.md`); read there before the first call |
| Google Ads | Not wired into this skill — ask for a CSV export. The connector itself lives on `ad-manager` |

**Attribution honesty.** Ad platforms report conversions they claim. The CRM reports leads it received. These rarely agree, and the gap is not a bug. Report both and name the gap rather than picking the flattering one.

---

## Mailchimp — email as a channel

| View | What to pull |
|---|---|
| Campaign return | Campaign analytics with revenue attribution — opens, clicks, and attributed revenue per campaign |
| Channel trend | E-commerce analytics, for the email-attributed slice of revenue |
| Lead volume | Audience-growth analytics — subscribers added and lost in the period |

**Same attribution honesty applies.** Mailchimp's attributed revenue is Mailchimp's claim,
sitting next to the ad platform's claim and the CRM's record. Report it as the email
channel's own number and name the gap. Never fold it into a single blended figure.

**Mailchimp is read-and-draft only in this plugin.** It has no send path here, and its
campaign planner will refuse a single-campaign request — it produces multi-channel plans
only. Treat the audience list itself as unavailable for export unless a call actually
returns it.

**An auth or login error is connector health, not missing data.** If Mailchimp calls fail
with an expired login or authorization error, the appendix line should say "Mailchimp:
connection needs to be re-authorized — reconnect it in Connectors and rerun," not "no
email data." Name the fix, then continue the pulse without the email views. Before
writing that line, check the error did not come from the plugin's own registration
(`small-business:intuit-mailchimp`, the manifest key) while the owner's Mailchimp entry is live — if the owner's
entry works, use it and say nothing about reconnecting
(`../../../shared/connector-neutrality.md`, "One connector, two registrations").

---

## Sentiment

| Source | What to pull |
|---|---|
| Public reviews | Recent Google, Yelp, and industry-site reviews via web research |
| PayPal, Stripe | Dispute and chargeback counts and reasons |
| Gmail or Microsoft 365 | Inbound complaints, cancellation requests, refund asks |
| HubSpot | Ticket volume and themes, if support runs through the CRM |

Sentiment is the leading indicator in this pulse. It moves before revenue does, which is exactly what makes it worth including.

---

## The uploaded-file path

A first-class mode, not a degraded one. Many owners in this segment have no clean connector on the growth side at all.

What to ask for, in plain language:

- "Export your deals from the CRM" — funnel conversion
- "Export your sales report for the month" — channel and product performance
- "Download the campaign performance CSV from Ads Manager" — campaign return
- "Paste in your recent reviews" — sentiment

Read the header row, map the columns, and build the identical pulse. If a needed column is absent, name it — "there's no source column, so I can't break leads out by channel" — rather than quietly dropping the view.

---

## Parallel-pull rule

Every call goes out in one batch. This pulse routinely touches five or six systems.

Record failures internally and list them once in the appendix. Never surface a connector error in the middle of the brief — the owner asked about growth, not about integrations.
