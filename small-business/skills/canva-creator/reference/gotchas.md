# Gotchas

Common failure modes for the canva-creator skill.

---

## Gotcha: Generating ANY Canva design for an email row

**Why it matters:** The owner descoped Canva from the email path entirely.
Canva email-template autofill produces placeholder graphics (stock
landscapes, blank rectangles) in service-grid tiles, and variation
thumbnails fail to render in chat. The decision was: emails are text-only
from this skill, period. Generating a Canva email design — even one — is
a regression of an explicit descope.

### ✗ Bad

```
Calendar has 6 social rows + 2 email rows.
→ Stage 2 generates 6 social designs + 2 email designs.
→ Email designs ship with placeholder service tiles.
```

Or any variation: "I'll generate the email template just to give you a
visual reference," "I found an email template that might work, want to
preview it?", "Here's a Canva design for the Jun 5 email…" — all
forbidden.

### ✓ Good

```
Stage 1: Calendar built with Path column.
  - 6 rows tagged Canva (social)
  - 2 rows tagged Text-only (no Canva)
Stage 2: Generates exactly 6 Canva designs. Email rows are not passed
         to any Canva endpoint.
Stage 3: Drafts 6 social captions + 2 full emails (subject + preheader +
         body) as plain text.
Stage 4: Stages 6 social posts in HubSpot. Surfaces 2 emails inline for
         owner to copy into their email tool.
```

If the owner explicitly asks for a Canva email design ("can you make me
a Canva version of the Jun 5 email?"), redirect: "This skill keeps emails
as text-only because the Canva email path produces placeholder graphics.
If you want a Canva-designed email, build it directly in Canva and I can
help you write the copy here."

---

## Gotcha: Generating without a budget plan

**Why it matters:** Canva caps API usage at 100 requests/minute per token,
and each design costs ~5 calls (autofill + export + polling). A 10-row
campaign with 4 candidates per row generates 40 designs and ~200 API
calls — and the math gets worse with parallelism. Without a pre-flight
budget, the owner hits quota mid-campaign with no clear recovery path
and four already-generated posts sitting unused.

### ✗ Bad

```
Calendar approved → immediately fire 4 candidates × 8 rows in parallel
→ ~160 API calls in 90 seconds → RATE_LIMIT_EXCEEDED on post 5 → loop
on retry → owner blocked.
```

### ✓ Good

```
Pre-flight: "8 Canva rows × 3 candidates = 24 designs, ~120 API calls.
Proceed at default 3 candidates per row?"

Stage 3: row 1's 3 candidates fire in parallel → 30s pause → row 2 →
30s pause → row 3 → … finishes at ~12 designs/minute, well under the
quota.

If quota does hit anyway: stop, surface progress, ask the owner
whether to drop to single candidates, pause an hour, or move to
captions with what's done.
```

---

## Gotcha: Skipping Checkpoint 1 (calendar approval) before generating assets

**Why it matters:** Generating 10+ Canva designs takes API calls, time, and
user attention. If the calendar has the wrong dates, wrong channels, or the
owner changes their mind about a theme, all that work is discarded. The
calendar checkpoint is the cheapest place to catch misalignment.

### ✗ Bad

Receive the brief → immediately start calling `POST /autofills` for all 12
posts → present designs before the owner has agreed on the schedule.

Owner: "Oh wait, I didn't want any posts the week of the 15th, I'm traveling."

### ✓ Good

Present the calendar table first. Wait for explicit "looks good" before opening
a single Canva API call.

---

## Gotcha: Template has more image slots than the brief provides photos for

**Why it matters:** Multi-image social templates (Instagram carousels,
product grids) can have 3+ image slots. When the brief gives you 1 photo
and the template demands 3, the unfilled slots silently render Canva's
stock landscape graphic — generic clouds and green hills where product
photos should be. The design looks "complete" until the owner opens it.

(Note: email rows skip Canva entirely in this skill — see SKILL.md Stage 3.
This gotcha applies only to social templates with multiple image slots.)

### ✗ Bad

Build manifest with one row per design ("Carousel — needs Hero_Image").
Upload the one photo. Generate. Carousel ships with slide 1 populated
and slides 2-3 both showing identical generic landscapes.

### ✓ Good

Build manifest slot-by-slot. Surface the gap explicitly:

```
The "3-product carousel" template has 3 image slots. The brief gave me
1 photo. How should I fill the other 2?

1. Reuse the same photo across all 3 slots
2. I'll send you 2 more photos
3. Pick a single-image template
```

Wait for the owner's choice before generating. Don't let placeholder
graphics ship.

---

## Gotcha: Trusting `status: success` without exporting and visually verifying

**Why it matters:** A successful autofill job means Canva accepted the
request and produced a design — not that the design contains the right
images. If an `asset_id` was empty, stale, or wrong-typed, the job still
returns `status: success` and the design renders with default placeholder
graphics. The only way to know is to look at the rendered output.

### ✗ Bad

```
Job status: success ✓
result.design.id: present ✓
→ Present to owner
```

Result: owner opens the carousel and sees stock landscape graphics in 3 of
4 designs.

### ✓ Good

After the job succeeds, export each design to a permanent PNG via
`POST /exports` (or `export-design` MCP). Look at each PNG and confirm it
contains real assets — not Canva's default landscape, not gray rectangles,
not lorem-ipsum text. Only present to the owner after visual verification
passes.

---

## Gotcha: One design in a batch fails to render

**Why it matters:** When 1 of 4 designs in a batch fails (job error, expired
preview URL, placeholder rendered) and you present the partial carousel
anyway, the owner sees three real designs and one "Show Image" gray
rectangle. They lose trust in the rest of the carousel even though it's
fine.

### ✗ Bad

```
Week 1 designs are ready:
[Option A — real preview]
[Option B — real preview]
[Option C — real preview]
[Option D — Show Image placeholder]
Which one should I use?
```

### ✓ Good

When you detect the broken design at Step 6 verification, regenerate just
that one design with the correct asset_id. Re-export, re-verify. Only
present once all four designs in the batch have permanent, verified
previews. If the second attempt also fails, ask the owner whether to skip,
swap template, or try a different photo.

---

## Gotcha: Generating assets without confirming all autofill fields have values

**Why it matters:** Canva autofill silently renders empty placeholders when a
field value is missing or the referenced `asset_id` doesn't exist. The result
is a professional-looking template with blank white rectangles where the
product photo and headline should be.

### ✗ Bad

Build calendar → immediately fire all `POST /autofills` in parallel → half
the designs come back with empty image placeholders because product photos
weren't uploaded first.

### ✓ Good

Build calendar → inventory every autofill field slot-by-slot → upload missing
product images → confirm all field values with owner → then generate designs
in parallel, with every field pre-populated.

---

## Gotcha: Passing invalid values to image autofill fields

**Why it matters:** When an autofill image field receives an empty string, a
file path, a URL, or a stale/invalid `asset_id`, Canva does not error — it
silently renders the template's default placeholder graphic (e.g., a generic
landscape with clouds and hills). The design looks "finished" but the hero
image is stock art, not the owner's product photo.

### ✗ Bad

Upload product photo → don't wait for the upload job to complete → pass the
`job_id` (not the `asset.id`) into the autofill data → design renders with
a placeholder landscape instead of the product photo.

### ✓ Good

Upload product photo via `POST /v1/asset-uploads` → poll
`GET /v1/asset-uploads/{job_id}` until `status == "success"` → extract
`asset.id` from the response → pass that exact ID into the autofill image
field. Verify every image field has a confirmed `asset.id` before calling
`POST /autofills`.

---

## Gotcha: Embedding Canva CDN thumbnail URLs in markdown

**Why it matters:** Canva's autofill response returns short-lived,
authenticated CDN URLs from `design.canva.ai`. These expire within minutes.
If Claude embeds them as markdown images (`![](design.canva.ai/...)`), they
render as broken "Show Image" placeholders by the time the message is shown.

### ✗ Bad

Generate 8 designs → manually embed each CDN thumbnail URL in the response
as `![Hero 1](https://design.canva.ai/xxx)` → all images show as broken
gray placeholders because the URLs expired before render.

### ✓ Good

Either let the native Cowork carousel render the tool result automatically,
or export each design via `POST /exports` and embed the **permanent** export
URL. As a final fallback, link to the design's permanent edit URL
(`https://www.canva.com/d/{design_id}`). Never re-embed `design.canva.ai`
URLs.

---

## Gotcha: Listing designs one-by-one as individual image blocks

**Why it matters:** When Claude lists each design as a separate block
("Hero 1 / [image] / Hero 2 / [image]"), the images render as broken
gray "Show Image" placeholders. Presenting all designs together in a
single grouped batch triggers Cowork's side-by-side carousel, which
renders correctly.

### ✗ Bad

```
Hero 1 — Multi-property portfolio
[Show Image]
View in Canva: https://canva.com/d/xxx

Hero 2 — Coastal market case study
[Show Image]
View in Canva: https://canva.com/d/yyy
```

### ✓ Good

Present all designs in one grouped response so they render as a
side-by-side carousel. Below the carousel, add a single prompt:

```
Here are 4 hero designs for Week 1. Scroll through the carousel
above and let me know which one to keep.
```

---

## Gotcha: Generating designs sequentially instead of in parallel

**Why it matters:** Generating designs one at a time means the owner waits
through N round trips instead of one. Fire all generation requests within a
batch at once and present selection after all jobs complete.

### ✗ Bad

Generate design 1 → wait → show it → generate design 2 → wait → show it →
… × 8 designs. Owner watches a slow drip for 10 minutes.

### ✓ Good

Fire all designs in the current batch at once → poll all jobs concurrently →
once all complete, export each → verify visually → then present.

---

## Gotcha: Auto-selecting a brand template for Pro/Teams users

**Why it matters:** Pro/Teams users have no brand-template API access. If
Claude guesses a template by name and generates with the wrong one, the owner
gets designs in the wrong colors/fonts and has to redo the work in Canva
manually.

### ✗ Bad

```
Found template "Square Post - Blue". Using this for all feed posts.
```
…followed by 8 designs in blue when the brand is green.

### ✓ Good

```
I found 3 templates in your Canva library that could work for feed posts:
1. Square Post - Blue  (last edited March 2026)
2. Summer Promo - Green  (last edited April 2026)
3. Product Feature Card  (last edited Jan 2026)

Which one should I use?
```

---

## Gotcha: Caption voice drift across a long calendar

**Why it matters:** When drafting 12–20 captions in one pass, the tone tends
to drift — early captions follow the brief's voice markers, later ones slip
into generic marketing copy. Owners notice immediately.

### ✗ Bad

Post 1: "Our handmade candles are the perfect summer gift 🌿" (matches brief: "warm, conversational")  
Post 10: "Elevate your ambiance with our artisanal fragrance collection." (corporate drift)

### ✓ Good

Before drafting, anchor on 2–3 voice markers from the brief (e.g., "casual,
friendly, uses light humor"). Re-read the first draft caption before writing
each new one. If the owner flags a voice mismatch on any caption, re-read that
caption and flag it as the recalibration point for the remaining drafts.

---

## Gotcha: Staging HubSpot posts without verifying `scheduledAt` is in the future

**Why it matters:** HubSpot rejects posts with `scheduledAt` in the past with
a validation error. If the calendar was built on an earlier date and the
owner is only now staging, some dates may have passed.

### ✗ Bad

Build calendar on April 1st for June posts → owner approves May 15th → try to
stage without checking → post for "April 30th 10:00 AM" returns 400.

### ✓ Good

Before calling `POST /social/posts`, compare each `scheduledAt` against the
current UTC time. If any post date has passed, surface it: "The post scheduled
for April 30th has already passed. Should I skip it, or reschedule it to next
week?"
