# Website research

Read this before fetching the owner's site. The goal is to replace interview
questions the site already answers, not to add a research phase on top of the
interview — onboarding should still finish in 15–20 minutes.

---

## What to fetch

The homepage plus whichever of these exist and are linked from it: about,
services or products, pricing, locations, contact. Three or four pages total
is enough — this is not a full site crawl.

## What to extract

| Field | What it feeds |
|---|---|
| What they actually sell | Business context; sharper than a one-line owner description alone |
| Who they sell to (consumer, business, both; specific niche) | Every skill that drafts customer-facing copy |
| Service area or locations | Local-service and retail skills |
| Team size signals (staff photos, "our team," locations count) | A cross-check on the interview answer, never a replacement for it |
| Price positioning (premium, budget, mid-market — inferred, not guessed as a number) | Proposal and marketing skills |
| The words they use for their own work | Feeds `shared/voice-profile.md` directly — this is real copy in the owner's own hand, even before any email is read |
| Brand colors (dominant background/accent from the site's own CSS) | The welcome artifact and every artifact after it, per `shared/artifact-style.md` |
| A declared font-family, if one is easy to find | Same — applied only if it resolves on Google Fonts; otherwise skip it, never fight the CSP |

**Do not infer anything the site doesn't actually say.** "Looks premium" from
a photo is a guess; "prices start at USD 200" printed on a pricing page is a
fact. Keep the two separate in what gets shown back — say when something is
inferred rather than read.

---

## Showing what was found

Always show it before storing anything, and keep it short — a wall of
extracted facts is worse than the interview it was meant to replace.

```
Read your site. Looks like: commercial HVAC repair and maintenance, Denver
metro, same-day service is a big deal to you — it's on every page. Found a
deep green and a slab serif in your branding.

Anything off, or should I use that for your reports too?
```

**Treat a correction as expected, not a failure.** Sites go stale, and an
owner catching one wrong detail in ten seconds is the whole point of showing
the draft rather than silently storing it.

---

## Brand token extraction

Pull the two or three colors that actually recur across the site — usually
visible in a header, a button, or a logo background — and any font-family
declared in the page's own stylesheet. Do not invent a palette from a single
photo; only extract what's structurally present in the site's own CSS or
repeated markup.

**Apply only on a yes.** Show the finding in the same message as the business
summary (see above), and only wire the colors and font into the welcome
artifact's tokens (`shared/artifact-style.md`) if the owner confirms. If the
site's declared font doesn't resolve on Google Fonts, keep the house default
silently — never show a broken font as if it worked.

Store the resolved values — not the raw scrape — in the `## Business context`
block's Brand colors and Logo fields (format in [onboard-checklist.md](onboard-checklist.md)), so
every later skill's artifact reads the same finished tokens without
re-deriving them.

---

## When there is no website, or the owner skips it

Say nothing lost — move straight to the interview. This step is a shortcut
when it exists, never a requirement:

```
No problem — I'll just ask a few questions instead.
```
