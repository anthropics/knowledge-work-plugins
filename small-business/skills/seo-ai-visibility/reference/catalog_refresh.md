# Catalog Refresh

The bulk product pass for stores. Score every product, rewrite the worst, apply in approved batches.

Shopify and Wix are the connected paths. Wix exposes a full read/write site API, so a bulk
catalog and site refresh applies directly there the same way it does on Shopify — the
scoring, the revenue ordering, and the batch gates below are identical on both.

Without either, work from a product CSV export and hand back a corrected CSV for import —
the scoring and the rewriting are identical again.

---

## What gets scored

Four fields per product, each pass or fail with a reason.

| Field | Passes when |
|---|---|
| Title | Says what the product is in plain terms. Not a bare SKU, not a keyword pile. Under about 70 characters |
| Description | Answers what it is, what it fits, what is included, and what makes it different. At least a few real sentences |
| Image alt text | Present on every image and describes the image. Not the product title copied in |
| SEO title and description | Present, unique, under the length limits, distinct from the product title |

A fifth check worth running: **duplicate descriptions**. Stores routinely have the same paragraph on forty products. Flag the clusters.

---

## The scoring pass

Run across the whole catalog first, before writing anything. The owner needs to see the size of the problem.

```
Catalog scan — 412 products

Missing SEO description        318   77%
Missing or duplicate alt text  287   70%
Description under 40 words     201   49%
Duplicate description text      94   23%  (11 clusters)
Title is a bare SKU             38    9%

Fully complete                  41   10%

Worst 25 by revenue: 19 have no SEO fields and 22 have no alt text. Those
are the ones losing money, so they go first.
```

**Order by revenue, not by score.** Fixing a product that sells one unit a year is a waste of the owner's approval attention. Sort by units sold or revenue over the last 90 days and start at the top. Say that this is what you are doing.

---

## Rewriting

Read [the shared voice profile](../../../shared/voice-profile.md). Product copy carries the store's voice as much as email does.

**Titles.** What it is, then the distinguishing detail. Brand, model, size, and material where they matter to a buyer.

```
Bad:   HVAC-FLT-2025-B
Bad:   Best Premium High Quality Air Filter Furnace AC HVAC MERV 13 Cheap
Good:  MERV 13 Pleated Furnace Filter — 20x25x1, 6-Pack
```

**Descriptions.** First sentence says what it is and who it is for. Then specifics — dimensions, compatibility, what is in the box, how long it lasts. Then anything genuinely distinguishing.

```
MERV 13 pleated filter for standard 20x25x1 furnace and AC returns. Catches
pollen, dust, pet dander, and smoke particles down to 0.3 microns — the
grade most allergy sufferers want. Six filters, about a year of coverage
at the recommended 60-day change. Fits most residential systems built
after 1995; measure your existing filter before ordering.
```

**Alt text.** Describe the image, for someone who cannot see it. This is an accessibility requirement first and a search benefit second.

```
Bad:   MERV 13 filter buy online best price
Good:  White pleated furnace filter, front view, showing the 20x25x1 size
       printed on the cardboard frame
```

**Never invent product facts.** Dimensions, materials, compatibility, certifications, and country of origin come from the existing product data or from the owner. When they are missing, write around them and flag it — "compatibility list needed for 14 products" — rather than guessing. A wrong compatibility claim generates returns.

---

## Batch approval

**Batches of 20 to 25. Every batch gets its own yes.** A rewrite pattern that looked fine on three samples and is wrong across 400 products is a very long afternoon of undo.

Before the first batch, show three full before-and-after examples and get agreement on the pattern. Fixing the approach on three products costs nothing.

```
Batch 3 of 17 — products 51-75, ranked by 90-day revenue

Changing:  25 titles, 25 descriptions, 61 alt texts, 25 SEO descriptions
Sample:    <3 full before-and-after pairs>
Not touching: prices, inventory, variants, collections, publish status
Reversible: Yes — original values saved to catalog-backup-2026-07-27.csv

Apply these 25?
```

Rules that keep this safe:

- **Save the originals before the first write.** A CSV of the current values, always, no exception.
- **Never touch price, inventory, variants, or publish status.** This skill edits how products are described. Nothing else.
- **Stop on the first surprise.** If a write errors or a field comes back different from what was sent, stop the run and report rather than continuing through the remaining batches.
- **Report per batch.** Applied, skipped, failed, with product names.

---

## Structured data for products

Once descriptions are clean, add `Product` schema with `Offer`. Most store platforms generate it — check what is already there before adding a second, conflicting block.

Only mark up what is true and visible: price, availability, brand, SKU, and ratings that come from real reviews on the page.

---

## Without Shopify or Wix

Ask for the product export — most platforms have one — and return a corrected file for import.

Say the path plainly: "Export your products to CSV, send me the file, and I'll send back a version with the titles, descriptions, alt text, and SEO fields rewritten. You import it and check the first few before letting it run."

Same scoring, same revenue ordering, same batching in the review. The only difference is the owner clicks import.
