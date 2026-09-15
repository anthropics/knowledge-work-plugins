# Worked example — Okonkwo Mechanical, July

Ray Okonkwo runs Okonkwo Mechanical, an HVAC company with four techs. Canva
Pro is connected. No Shopify (he is a service business, not retail). HubSpot
is on Starter, so social staging is not available and the CSV path is used.

Voice profile is already built and is the one in `../../../../shared/voice-profile.md`:
short sentences, contractions, "the work" not "solutions," never "reach out."

---

## Run 1 — the standing calendar

```
Owner: "We've gone quiet on Facebook. Can you get us posting again?"
```

Open the existing calendar. There isn't one yet, so say so and set a cadence
before drafting anything:

```
Nothing on file yet, so this is the first calendar.

You're a four-tech shop with an office manager, so three posts a week is
realistic and two is comfortable. I'd start at two and add the third once
it's sticking. Sound right?
```

Ray picks two a week for 30 days, Facebook and Instagram. Eight posts, plus
one email for service-plan renewals.

Calendar presented, with the Path column doing its job:

| Date | Channel | Path | Theme | Asset type | Angle |
|---|---|---|---|---|---|
| Jul 8 | Instagram feed | Canva (social) | Useful | Square post | "what that rattling noise means" |
| Jul 8 | Facebook | Repurpose of Jul 8 IG | Useful | 1200×630 | same |
| Jul 11 | Email | Text-only | Offer | Email body | "your plan renews Aug 1" |
| Jul 15 | Instagram feed | Canva (social) | Proof | Square post | Kirby Street install, before and after |
| Jul 18 | Instagram feed | Canva (social) | Offer | Square post | "July tune-up slots are open" |
| Jul 22 | Instagram feed | Canva (social) | People | Square post | Marcus joining the crew |
| Jul 25 | Instagram feed | Canva (social) | Useful | Square post | "why the upstairs is always hotter" |
| Jul 29 | Instagram feed | Canva (social) | Proof | Square post | Six-building commercial plan |

Restate the split before moving on:

```
Six rows go through Canva. One row is a repurpose of the Jul 8 design, so
it costs no generation. One row is text-only email. Good to lock this?
```

---

## The generation budget

```
Generation budget for this batch:
  Canva rows:          6
  Candidates per row:  3
  Total designs:       18
  API calls (approx):  ~90

Canva's limit is 100 requests a minute. Running one row at a time with a
30-second gap, this takes about 2 minutes. Proceed?
```

Ray says yes at the default. Locked at 3 for the session.

---

## Slot inventory — where the first problem showed up

The Jul 15 proof post uses a two-image before-and-after template. Ray sent one
photo.

```
The before-and-after template has 2 image slots — Before_Image and
After_Image. You sent me one photo (kirby_after.jpg). How should I fill
Before_Image?

  1. You send me the before photo
  2. Switch to a single-image template for this post
```

He finds the before shot. Both uploads poll to success, both asset IDs
recorded, and only then does generation start. Without this, slot two would
have rendered a stock landscape and the post would have looked finished.

---

## Generation, row at a time

Row 1 fires three candidates in parallel, exports all three to permanent PNGs,
and each one gets looked at. Candidate 2 comes back with the headline in
template-default lorem text — that one candidate is regenerated, not the row.
Three good options are presented as a single carousel, Ray picks one, then a
30-second pause before row 2.

At row 4, Canva returns a rate-limit error. First hit this session, so wait
60 seconds and retry that one candidate. It succeeds. Nothing is announced to
Ray for a transient spike; it costs a minute and no decision.

Had it hit a second time, the run would have stopped and asked:

```
Canva is rate-limiting us. Where things stand:
  Generated:  posts 1-4 (12 designs)
  Remaining:  posts 5-6 (6 designs not yet generated)

  1. Drop to one candidate each for the last two — finishes now
  2. Pause and resume in an hour when quota refills
  3. Stop here and move to captions with what we have
```

---

## Copy, in Ray's voice

Anchored on the profile before each caption, not just the first.

Jul 8, Instagram:

```
That rattling when the AC kicks on is usually the blower wheel, not the
compressor. Cheap fix if you catch it. Not cheap if you don't.

If yours is doing it, send us a video — we can usually tell from the sound.

#hvac #okonkwomechanical #homemaintenance
```

Short sentences, contractions, gets to the point in line two. What it does
not say: "reach out," "we're excited," "solutions." Those are on his never-do
list, and they are the first thing he would have flagged.

Jul 11, email, text only, no Canva anywhere near it:

```
Subject: Your service plan renews Aug 1
Preheader: Nothing to do unless you want to change it

Hi Dana,

Straight answer: your plan renews Aug 1 at the same rate as last year.
Nothing you need to do.

If you've added a unit or want to move to the commercial plan, tell me
before the 25th and I'll adjust it.

Thanks, Ray
```

---

## Staging

HubSpot Starter means no social staging, so the CSV path runs:

```
Your HubSpot plan doesn't include social scheduling, so here's a CSV you can
import into Buffer or Later — same dates, captions, and images:

  content-calendar-july.csv

Two things to know before you import:
  - The Jul 8 Facebook row reuses the Instagram image, cropped to 1200×630
  - Nothing publishes until you import it and hit schedule

The email for Jul 11 is above. Paste it into your email tool when you're
ready — I haven't queued it anywhere.
```

---

## Run 2 — three weeks later

The calendar is opened first, not rebuilt:

```
Since we last talked:
  Published:      6 posts (Jul 8 – Jul 25)
  Still queued:   2 posts (through Jul 29)
  Gap starting:   Jul 30

The Kirby Street before-and-after got the most comments by a distance.
Want me to extend from Jul 30 with more of the proof posts, same two a
week?
```

That is the difference between a campaign generator and a content operation.
