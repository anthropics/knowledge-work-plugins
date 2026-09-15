# Shopify product data into content

When Shopify is connected, product photos, titles, descriptions, and prices
flow straight into design fields and captions. That removes the two steps
owners abandon on: hunting for a photo, and retyping a price they then get
wrong.

---

## What to pull

Read products and their variants. The fields that matter:

| Shopify field | Used for |
|---|---|
| `title` | Headline slot, caption subject |
| `body_html` | Source for the benefit line — strip tags, never paste raw HTML |
| `images[].src` | Design image slots |
| `variants[].price` | Price in the caption or a price slot |
| `variants[].compare_at_price` | Only source for a "was / now" claim |
| `variants[].inventory_quantity` | Whether to feature it at all |
| `tags`, `product_type` | Grouping products into a theme |

---

## Turning a product into a post

1. **Pick products worth posting.** Skip anything out of stock or with
   inventory too thin to survive the post working. A sold-out product
   featured on a Tuesday is a customer complaint on Wednesday.
2. **Get the image into Canva.** Upload from the Shopify image URL, poll the
   upload job to success, and record the returned asset ID. That ID is the
   only value an autofill image field accepts.
3. **Write the benefit line from the description, not with it.** Product
   descriptions are written for a product page, not a feed. Pull the one
   concrete thing and drop the rest.
4. **Carry the price through unchanged.** Copy the number from the API
   response. Do not round it, convert it, or infer a sale price.

---

## Price and claim rules

A wrong price in a public post is the most expensive error this skill can
make. The owner cannot quietly fix it after a hundred people have seen it.

- Only state a price the connector actually returned.
- Only say "was X, now Y" when `compare_at_price` exists and is higher than
  `price`. Never compute a discount percentage that Shopify did not imply.
- Never write "limited stock" or "almost gone" unless the inventory number
  supports it.
- If a price is missing, say so and ask. Do not fall back to the last price
  seen in an earlier session — prices change and the calendar is long-lived.

---

## Multiple products in one design

Product grids and carousels have one image slot per product. Enumerate them
individually and map each to a specific product before generating:

```
Slot Product1_Image → "18k BTU Mini-Split"  → asset_id confirmed
Slot Product2_Image → "Smart Thermostat"    → asset_id confirmed
Slot Product3_Image → —                     → MISSING, ask the owner
```

Never fill a slot with a repeated photo without asking. Three identical tiles
in a "three products" grid reads as a mistake, because it is one.

---

## Without Shopify

The fallback is the owner's photo folder plus whatever the brief states. It is
a complete path — it just costs an upload and a typed price, and the price
then needs confirming out loud before anything publishes.
