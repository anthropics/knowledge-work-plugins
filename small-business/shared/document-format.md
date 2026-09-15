# Document format preference — plugin-wide default and override

**Scope:** skills that hand the owner a document meant to leave the
conversation — a proposal, a job post, a hiring packet. This is not about
dashboards, call sheets, or anything read once and acted on inside chat —
`shared/artifact-style.md`'s own delivery rule already covers those, and
this file does not change them.

---

## The preference

Set once during `smb-onboard`, stored in the Cowork session memory directory
as the `Output preference` line of the `## Business context` block (the block
format is in `skills/smb-onboard/reference/onboard-checklist.md`). The six
stored values are `visual artifacts`, `docx`, `md`, `notion`, `canva`, `best
for skill`; the six choices below map onto them in that order:

Six options, asked as multiple choice:

- **A styled page here (HTML artifact)** — the default, and what most owners
  want most of the time. Easy to view, easy to share a link to, nothing to
  download.
- **Word documents (.docx)** — for owners who print, email as attachments, or
  need to hand-edit in Word before sending.
- **Plain markdown or text files** — for owners pasting content into their
  own tools (a job board, an ATS, a CMS) rather than sending a file as-is.
- **Notion pages** — the document is created as a page via the Notion
  connector, in a destination the owner names, never overwriting an existing
  page. If Notion is not connected this run, say so and fall back to the HTML
  artifact; do not block the deliverable. The write rules are the same ones
  `shared/artifact-style.md` sets for the `notion` preference.
- **Canva Docs** — the document is created as a Canva Doc via the Canva
  connector, a new design each run, named with the date, content placed
  verbatim. If Canva is not connected this run, say so and fall back to the
  HTML artifact; do not block the deliverable. The write rules and the
  content limits (no tables, charts, or links in a Canva Doc) are the ones
  `shared/artifact-style.md` sets for the `canva` preference.
- **Whichever fits the moment** — the owner is fine leaving it to judgment
  call per document. Treat this the same as no preference at all.

## The default

**No stored preference, or "whichever fits the moment" → HTML artifact.**
Every skill this file governs defaults to rendering the document as a house-
style artifact and nothing else, unless the owner's stored preference says
otherwise, or a specific downstream mechanism requires a real file regardless
of preference (below).

## The override — when a real file is required regardless of preference

A stated preference for HTML never removes a file the *mechanism* requires,
it only removes files that existed purely as a courtesy format. Concretely:

- **E-signature routing** (DocuSign) needs an actual document to attach —
  produce it even if the preference is HTML-only, and say so in one line:
  *"This one still needs a real file for DocuSign — making the .docx for
  that, the page is still there to review first."*
- **A destination that only accepts a file** (a job board's upload field, a
  funder portal's submission format) works the same way — the destination's
  requirement wins, stated plainly, once.

This distinction is the whole point of this file: **preference decides the
courtesy copy; a genuine external requirement is never optional.**

## Skills this governs today

- `proposal-builder` — Step 5. DOCX and PDF are produced only when the
  preference calls for them; the HTML artifact is the default and always
  offered regardless.
- `job-post-builder` — the job post and interview guide follow the
  preference (both are typically pasted or read, not filed); the offer
  letter stays a real file by default because Phase 6 routes it to
  DocuSign — the override rule above, not an exception to it.

**Deliberately not touched:** `contract-review`'s redline DOCX (a lawyer
markup format the owner explicitly asks for, not a default), `report-builder`
/`report-pack`'s XLSX (a working data appendix, not a stylistic document
choice), and `grant-rfp-writer` (funder portals dictate the submission
format, not the owner). Applying a personal-taste preference to a file a
third party requires in a specific format would be the wrong fix.

## If the preference is unset when a skill runs

Ask once, briefly, the same way any other missing-context gap gets handled:
*"Quick one — want this as a page here, a Word doc, a Notion or Canva page,
or does it depend?"*
Store the answer as the `Output preference` line in the `## Business context`
block so it is never asked again. Do not
block the deliverable on the answer — default to HTML artifact for this run
if the owner is mid-task and would rather answer later.
