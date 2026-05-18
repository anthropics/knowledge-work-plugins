---
name: canva-creator
description: >
  Takes an approved content brief and executes a campaign end-to-end: builds
  the posting calendar, generates Canva designs for social posts, drafts
  caption and email copy, and stages social sends in HubSpot. Canva is used
  for social posts only (Instagram, Facebook, X, LinkedIn) — email content
  is drafted as plain text and surfaced inline for the owner to send from
  their own tool. Every step requires explicit owner approval. Use when the
  user says "make the content," "generate the posts," "create the assets,"
  "turn this into a campaign," or hands off an approved brief for execution.
---

# Canva Creator

## Scope

This skill handles a campaign in five sequential stages, each gated by owner
approval:

```
brief → calendar → asset inventory → Canva designs → copy → HubSpot staging
```

| Path | Channels | What this skill produces |
|------|----------|--------------------------|
| Canva (social) | Instagram, Facebook, X/Twitter, LinkedIn | Canva design + caption + scheduled HubSpot post |
| Text-only | Email (newsletter, marketing, drip) | Subject + preheader + body, surfaced inline for the owner to send |

**Canva is not used for email rows under any circumstance** — no templates,
no autofill, no design copies, no asset uploads, no exports. The owner
explicitly descoped Canva from the email path because email-template
autofill produces placeholder graphics when image slots exceed available
photos, and variation thumbnails fail to render in chat previews. If the
owner asks for a Canva email design, see `reference/gotchas.md` for the
redirect language.

---

## Pre-flight

Before Stage 1, confirm:

1. **Brief.** The user has referenced or pasted an approved brief. If not:
   "I'll need the content brief before I can build the campaign. Do you
   have one from the content-strategy skill, or would you like to write
   one now?"

2. **Canva tier.** Pro/Teams require manual template selection from the
   user's library (no autofill API). Enterprise can autofill from brand
   templates.

3. **HubSpot tier.** Social staging requires Marketing Hub Professional.
   Starter or Free → skip Stage 5 and export a CSV instead
   (see [reference/hubspot-staging.md](reference/hubspot-staging.md)).

4. **Brand assets.** Confirm the path to product photos on disk or that
   the brand kit is live in Canva.

5. **Generation budget.** Estimate the campaign's Canva volume and surface
   it before Stage 1 begins. Default is 3 candidates per Canva-bound row;
   each design costs ~5 API calls (autofill + export + polling).

   ```
   Generation budget for this campaign:
     Canva (social) rows: 8
     Candidates per row:  3   (default — say "single candidate" to use 1)
     Total designs:       24
     API calls (approx):  ~120  (autofill + export + polling)

   Canva limit: 100 requests/minute. This will take ~2-3 minutes of
   generation, well within your tier limits. Proceed?
   ```

   If the projected total designs exceeds 30, recommend single-candidate
   mode upfront — large campaigns run out of headroom fast. The owner can
   override the default to 1, 2, or 3 candidates per row before Stage 1
   starts. Lock the chosen value for the entire session.

---

## Workflow

### Stage 1 — Posting calendar

Pull from the brief: content themes, channels, cadence, hard dates
(launches, sales, holidays).

Build a calendar table with a `Path` column that routes every row to either
Canva or text-only drafting:

| Date | Channel | Path | Theme | Asset type | Caption/Subject angle |
|------|---------|------|-------|------------|-----------------------|
| Jun 2 | Instagram feed | Canva (social) | Linen launch | Square post | "finally, a dress…" |
| Jun 5 | Email | Text-only | Linen launch | Email body | "Linen that actually breathes" |

Tag every email-channel row as `Text-only` before presenting. Cap at 30
days unless the brief specifies otherwise. Flag scheduling conflicts (two
posts same day for the same product) up front.

**Checkpoint 1.** Present the calendar. Ask: "Does this match the plan?
Any dates to shift, channels to add, or themes to swap?" Iterate until
approved, then restate the split out loud — "N rows go through Canva, M
rows go through text-only drafting" — before moving on. Catching a
miscategorization here is free; catching it after generating designs
isn't.

---

### Stage 2 — Asset inventory (Canva rows only)

Email rows skip this stage entirely. For each `Canva (social)` row, build
a manifest of what the template needs and what's already available.

1. **Enumerate every image slot by name.** Square Instagram posts usually
   have 1-2 image slots; carousels and product grids can have 5+. List
   them individually (`Header_Image`, `Product1_Image`, `Product2_Image`,
   …) — never roll them up as "product images."
   - Enterprise: read field names from `dataset[].label` on the brand
     template (`GET /v1/brand-templates/{id}`).
   - Pro/Teams: count every distinct image rectangle in the template.

2. **Inventory available assets.** Text content from the brief (product
   names, offer copy, taglines, pricing), product photos already uploaded
   to Canva (`GET /v1/assets`) or on the owner's disk, brand kit colors
   and fonts (Enterprise).

3. **Build the slot-by-slot gap table.** One row per slot per design — not
   per design.

   | Date | Slot name | Slot kind | Available asset | Status |
   |------|-----------|-----------|-----------------|--------|
   | Jun 2 | Hero_Image | image | bloom_summer.jpg → asset_id pending | upload |
   | Jun 2 | Headline | text | "Summer linen, finally" | ready |
   | Jun 9 | Product1_Image | image | — | **MISSING** |

4. **Resolve slot/asset mismatches with the owner.** If the template has
   more image slots than the brief provides photos, pause and ask:

   ```
   The "Summer Carousel" template has 5 image slots. The brief gave me 1
   photo (bloom_summer.jpg). How should I fill the other 4?

     1. Reuse the same photo across all 5 slots
     2. You send me 4 more photos (file paths)
     3. Pick a simpler template with fewer slots
   ```

   No generation calls until the owner picks. Generating with empty slots
   produces designs full of Canva's default landscape placeholders.

5. **Upload missing photos and capture verified asset IDs.** Upload via
   `POST /v1/asset-uploads`, then poll `GET /v1/asset-uploads/{job_id}`
   until `status == "success"`. Record `asset.id` from the response — this
   is the only value that works in an autofill image field. Passing an
   empty string, a URL, a file path, or a stale ID silently renders
   Canva's stock landscape graphic instead of the photo.

6. **Confirm the manifest.** Show the owner the completed slot-by-slot
   table with every slot resolved and every image `asset.id` confirmed.
   This is the last stop before Canva API calls.

---

### Stage 3 — Canva design generation

Before any Canva API call, re-read the calendar and drop any row whose
`Path` is not `Canva (social)`. Email rows do not pass through this
stage.

Generate designs **one calendar row at a time**, with 3 candidates per row
(or the value chosen at pre-flight). Each row follows the same loop:
generate candidates → verify → export → visually check → retry failures
→ present → wait for owner pick → next row. Pause 30 seconds between
rows. This caps the burst at 3 generations + 3 exports per ~30s — well
under Canva's 100 req/min rate limit. Do not parallelize multiple rows;
one row at a time is the protection that keeps the owner from hitting
quota mid-campaign.

**Polling cadence.** Poll job status every 3-5 seconds, not faster.
Tighter intervals burn quota without speeding up completion.

**Preview URLs — only one type is safe to embed.** Autofill responses
return `design.canva.ai` thumbnails that expire within minutes; embedding
them as markdown images produces broken "Show Image" placeholders.
Permanent export URLs (`export-download.canva.com` or the `export-design`
MCP tool) do not expire. Native Cowork carousels render the autofill
result directly using the connector's authenticated session — let them
render on their own, don't re-embed.

#### Row loop

1. **Resolve template.** (Once per session — same template across rows
   unless the calendar mixes asset types.)
   - Enterprise: `GET /v1/brand-templates` filtered by asset type.
   - Pro/Teams: `GET /v1/designs?ownership=any&query={template name}`,
     surface top 3 to the owner, confirm one before generating.

2. **Generate the row's candidates in parallel.** Fire the row's 3
   candidates simultaneously (or N from pre-flight).
   - Enterprise: `POST /v1/autofills` per candidate with the template ID
     and field values. Poll all jobs concurrently.
   - Pro/Teams: `POST /v1/designs` to create copies. Describe the text and
     image edits the owner applies in Canva; collect design IDs back.

3. **Verify job status.** For each candidate, confirm
   `GET /autofills/{job_id}` returned `status == "success"` and
   `result.design.id` is present. Handle errors per-design:
   - `JOB_FAILED` → read `job.error.message`, fix the field values or
     asset IDs, retry once.
   - `RATE_LIMIT_EXCEEDED` (first hit this session) → wait 60s, retry
     that one candidate once. This handles transient spikes.
   - `RATE_LIMIT_EXCEEDED` (second hit this session) **or** any
     `quota_exceeded` / daily-cap error → stop generation immediately.
     Do not retry. Surface progress and ask:

     ```
     Canva is rate-limiting the campaign. Status so far:
       ✓ Generated:  Posts 1-4 (12 designs)
       ⏸ Remaining:  Posts 5-8 (12 designs not yet generated)

     How should I proceed?
       1. Switch to 1 candidate per remaining row (4 designs total) — finishes now
       2. Pause campaign — resume in 60 minutes when quota refills
       3. Stop generation — work with what we have, move to captions
     ```

     Wait for the owner's choice. Do not loop on retry.

4. **Export each successful candidate to a permanent PNG.** Fire the
   row's exports in parallel.
   - REST: `POST /v1/exports` with `format.type: "png"`, poll
     `GET /v1/exports/{job_id}` until success, capture `urls[0]`.
   - Canva MCP: `export-design` with the design ID.

   These permanent URLs are what get embedded in previews and attached to
   the HubSpot post later. The autofill response thumbnail is never used
   downstream.

5. **Visually verify each export.** Look at the image and reject any of
   these — they all indicate an unfilled slot or wrong asset:
   - Generic landscape with clouds and green hills (Canva's default
     placeholder)
   - Solid gray rectangles where a photo should be
   - Lorem-ipsum or template-default text
   - Subject that doesn't match the brief (wrong product, wrong brand)

   If a candidate fails verification: re-check the manifest for the
   affected slot, fix the `asset.id`, regenerate that single candidate,
   re-export, re-verify.

6. **Retry per-candidate on partial failure.** If 1 of N candidates in
   the row failed at Step 3 or 5, regenerate just that one — don't redo
   the whole row and don't present a partial broken carousel. If the
   second attempt also fails:

   ```
   The third candidate for the Jun 9 post keeps failing — Canva returned
   [error / rendered placeholder]. How should I proceed?

     1. Skip it — present the other 2 and move on
     2. Swap to a simpler template for just this candidate
     3. Try once more with a different photo
   ```

7. **Present the row's candidates.** Let the native Cowork carousel
   render the autofill tool result. Below it, add a text prompt:

   ```
   Jun 9 candidates are ready — scroll through the carousel above.
   Which one should I use for the Jun 9 post?
   ```

   If the carousel doesn't render or one position is broken, embed the
   permanent export PNG URLs from Step 4 instead. Final fallback: link to
   the design's Canva edit URL (`https://www.canva.com/d/{design_id}`).
   Never re-embed `design.canva.ai` URLs.

8. **Pause 30 seconds, then move to the next row.**

**Checkpoint 2.** Satisfied once the owner has picked one design per
calendar row. If they want a regenerate, regenerate only that one
candidate.

---

### Stage 4 — Copy drafting

For each calendar row, draft the copy. Social rows get a caption; email
rows get a full email.

**Social captions** — Instagram, Facebook, X, LinkedIn:

- Length: channel-appropriate (Instagram ≤ 2,200 chars; Facebook ≤ 500
  recommended; X ≤ 280).
- Structure: hook → one product benefit → CTA → 3-5 hashtags (not 30).
- Voice: match the brief's tone markers. If the brief says "casual and
  friendly," don't write corporate copy.
- No filler. No "Exciting news!" or "We're thrilled to announce." Open
  with the value.

**Email content** — Claude writes the entire email; no Canva:

- Subject: ≤ 50 chars, specific, no clickbait. "Spring projects are
  booking up" beats "Don't miss out!"
- Preheader: ≤ 90 chars, complements the subject without repeating it.
- Body: plain prose, 100-250 words. Opening line that earns the read →
  1-2 paragraphs of substance → single clear CTA → sign-off.
- Voice: same tone markers as social. Owners want their emails to sound
  like them, not like a templated newsletter.
- No image references. Don't write "see image above." If the owner wants
  visuals, they add them in their email tool.
- One CTA per email. Pick the most important action and lead with it.

Present captions inline below each social row. Present full emails
inline below each email row:

```
Subject: <subject line>
Preheader: <preheader text>

<body text>
```

For worked examples, see
[reference/examples/boutique-brief-campaign.md](reference/examples/boutique-brief-campaign.md).

**Checkpoint 3.** "Any captions or emails to rewrite? Flag the date and
what to change." Iterate until approved.

---

### Stage 5 — HubSpot staging + email handoff

Stage social posts in HubSpot. Email content is not staged — it's
surfaced inline for the owner to copy into their email tool. For API
field reference, see
[reference/hubspot-staging.md](reference/hubspot-staging.md).

1. **Create the campaign.** `POST /marketing/v3/campaigns` with the
   campaign name and start/end dates from the calendar.

2. **Stage each social post.** `POST` to the HubSpot Social API per
   `Canva (social)` row:
   - `channel`: map calendar channel to HubSpot account ID
   - `scheduledAt`: ISO 8601 datetime — confirm it's in the future before
     calling
   - `content.body`: approved caption
   - `attachments`: permanent Canva export PNG URL from Stage 3
   - `status`: `SCHEDULED` (never `PUBLISHED`)

3. **Confirm the queue.** Call
   `GET /marketing/v3/social/posts?status=SCHEDULED`, surface the list,
   provide a direct link to the HubSpot campaign view.

4. **Surface email content for handoff.** For each email row, present the
   approved subject + preheader + body inline, grouped by send date. The
   owner copies these into their email tool (HubSpot Marketing Email,
   Mailchimp, Gmail).

**Final checkpoint.**

```
Your social posts are scheduled in HubSpot: [link]
They'll go out as scheduled — you can cancel or edit any post in HubSpot.

Email content is drafted below — copy each into your email tool when
you're ready to send:

  Jun 5 — "Spring projects are booking up"
  Jul 15 — "Summer maintenance windows are filling"

Anything to change before we're done?
```

---

## Approval gates

- **No Canva calls for email rows.** Re-check the `Path` column before
  every API call.
- **No publishing.** Every HubSpot post is staged as `SCHEDULED`; the
  owner controls go-live.
- **Always surface the generation budget at pre-flight.** Owner sees the
  total design count and approves before Stage 1 begins.
- **One row at a time in Stage 3.** Candidates within a row fire in
  parallel, but rows are sequential with a 30s gap — this is the quota
  protection.
- **On the second quota error, pause and ask.** Never loop on retry.
- **Always export to a permanent PNG before presenting.** Job success
  doesn't mean the design rendered correctly.
- **Never embed `design.canva.ai` URLs in messages.** They expire.
- **Never regenerate the whole row when one candidate fails.**
  Per-candidate retry only.
- **Never auto-select a template for Pro/Teams users.** Always confirm.
- **Never skip slot-by-slot inventory.** Multi-slot templates render
  placeholder landscapes when any slot is empty.
- **Never skip Checkpoint 1.** Generating before the calendar is approved
  is the largest source of wasted work in this skill.

---

## Reference

- [reference/canva-api.md](reference/canva-api.md) — Canva Connect API
  endpoints, asset upload, export formats, MCP equivalents
- [reference/hubspot-staging.md](reference/hubspot-staging.md) — HubSpot
  Social API and CSV fallback for non-Pro tiers
- [reference/gotchas.md](reference/gotchas.md) — Good / Bad patterns for
  every failure mode this skill has hit in production
- [reference/examples/boutique-brief-campaign.md](reference/examples/boutique-brief-campaign.md)
  — full worked examples (single-slot social, multi-slot template)
