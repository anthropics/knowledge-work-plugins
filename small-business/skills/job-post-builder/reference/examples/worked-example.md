# Worked Example: Senior Product Manager

## Input

User message:
> "We need to hire a Senior Product Manager for our payments team. They'll own
> the roadmap for our checkout experience. We want 5+ years of PM experience,
> ideally with a fintech or payments background. Remote-friendly, NYC preferred.
> Comp is $160–185k base. Three interview rounds: recruiter screen, hiring manager
> deep-dive, and a panel with two senior PMs. Send the offer via DocuSign when
> we get there."

---

## Phase 1 — What Claude extracts

| Field | Value |
|---|---|
| Role title | Senior Product Manager |
| Team / function | Payments team |
| Key responsibilities | Own roadmap for checkout experience |
| Must-haves | 5+ years PM experience |
| Nice-to-haves | Fintech or payments background |
| Location | Remote-friendly, NYC preferred |
| Compensation | $160–185k base |
| Interview process | 3 rounds: recruiter screen, HM deep-dive, senior PM panel (2 people) |
| Offer delivery | DocuSign |

Claude confirms and asks exactly one question:
> "Got it — hiring packet for a Senior PM on the payments team, $160–185k,
> remote-friendly NYC. One question before I start: do you have an existing job
> description or offer letter template I should use as the starting point, or
> should I build from scratch?"

---

## Expected output

### `Senior-PM-Job-Post.docx`

Structure follows `references/job-post-structure.md`:

1. **Opening hook** — Why this role exists now: the payments team is scaling the
   checkout experience and needs someone to own the roadmap end-to-end.
2. **About the company** — 3–4 sentences (Claude asks or infers from context).
3. **About the role** — What success looks like 12 months in: a faster, more
   reliable checkout with measurably higher conversion.
4. **What you'll do** — 5–6 bullets, action-verb led (e.g. "Own the checkout
   roadmap from discovery through launch…").
5. **What we're looking for** — Required: 5+ yrs PM exp, comfort with data,
   strong written communication. Preferred: fintech or payments domain experience.
6. **Compensation** — $160,000–$185,000 base salary.
7. **How to apply** — One sentence.

Length target: 500–650 words.

---

### `Senior-PM-Interview-Guide.docx`

Structure follows `references/interview-guide-structure.md`:

- **Role summary** — one paragraph reminding interviewers what they're assessing.
- **Stage map** — 3 stages, each interviewer, each competency.
- **Stage 1: Recruiter screen** — Communication, baseline fit, logistics.
  Questions focus on career narrative and logistics (comp, start date, remote setup).
- **Stage 2: HM deep-dive** — Roadmap ownership, payments context, prioritization
  under constraints. 5–6 behavioral questions; 2–3 follow-up probes each.
- **Stage 3: Senior PM panel** — Split between the two panelists. Panelist A owns
  product judgment (how they make tradeoffs); Panelist B owns cross-functional
  collaboration (how they work with engineering and design). Questions are pre-assigned
  so the candidate isn't asked the same thing twice.
- **Scoring rubric** — 1/3/5 anchors written specifically for a payments PM role
  (not generic). Example for "Ownership": 5 = proactively identified checkout
  failure mode no one asked them to track, drove fix, documented for team.
- **Debrief guide** — Interviewers share scores before discussion; focus debrief
  on divergent scores.

---

### `Senior-PM-Offer-Letter.docx`

Based on `references/offer-letter-template.md`. Pre-filled where data is available:

| Field | Value |
|---|---|
| `[JOB TITLE]` | Senior Product Manager |
| `[ANNUAL SALARY]` | `$160,000–$185,000 — confirm exact figure with HR before sending` |
| `[CANDIDATE FULL NAME]` | Left blank |
| `[PROPOSED START DATE]` | Left blank |
| `[OFFER EXPIRATION DATE]` | Left blank |
| At-will clause | Included |
| Legal review disclaimer | Included |

---

## Phase 6 — Expected browser flow

1. Claude navigates to `https://app.docusign.com` and confirms login state.
2. Clicks "Start → Send an Envelope".
3. Uploads `Senior-PM-Offer-Letter.docx`.
4. Asks: "What's the candidate's full name and email address?"
5. Adds candidate as Signer; adds user as CC if requested.
6. Sets subject: `Offer of Employment — Senior Product Manager at [Company Name]`.
7. Places Signature and Date Signed fields on the acceptance line.
8. Saves as draft — does NOT send.
9. Returns draft URL and tells the user to review before confirming Send.

**Pass criteria:** User opens the draft URL, sees correct signature placement,
and can send with one click. Envelope status is "Draft" until the user acts.
