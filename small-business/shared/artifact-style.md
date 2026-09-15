# Artifact style — the house look

**Shared across the plugin.** One visual system so every page a skill produces
reads as the same product, not forty-six different ones. Read this before
building any HTML artifact; do not invent a new palette per skill.

**The point is not decoration.** These are back-office tools for a small
business owner — a call sheet, a cash snapshot, a reorder list. Polished and
legible beats flashy. No hero banners, no marketing gradients, no giant
mission statements. A ledger, not a landing page.

**Amounts follow the owner's currency.** Every figure a page shows carries
the business's ISO currency code (`GBP 1,240`, `AUD 18,400`), read from the
`## Business context` block per `shared/currency-and-locale.md`. The `USD`
figures in the examples below are illustrations of shape, not a default.

---

## When to use an artifact at all

Not every skill run needs one. Reach for a page when the output is something
the owner will **refer back to, print, hand to someone else, or paste from** —
a dashboard, a call sheet, a checklist, a set of recommendations with text to
copy. Skip it for a single number or a one-line answer; the chat reply is
the deliverable and a page around one sentence is noise.

**The artifact is additive, never a replacement.** The owner still gets the
short answer in chat. The page is where they go for the full picture.

**The owner's stored preference overrides the default.** Check the
`## Business context` block for an `Output preference` line (captured during
`smb-onboard`). Six values:

- `visual artifacts` (or absent) — the house-style artifact, the default.
- `docx` — deliver a DOCX document instead of the page, and say that is why.
- `md` — deliver a markdown file instead of the page, and say that is why.
- `notion` — create the deliverable as a Notion page via the Notion
  connector, in the owner's chosen workspace location, and say that is why.
  Page creation is a write: name the destination before creating, and never
  overwrite an existing page. If Notion is not connected this run, say so
  and fall back to the visual artifact — do not block the deliverable.
- `canva` — create the deliverable as a Canva Doc via the Canva connector.
  The path is two calls: `generate-design` with design type `doc`, verbatim
  on, and the full content in the query (it returns candidates, not a
  design), then `create-design-from-candidate` on the first candidate, which
  returns the design id and link that get handed back. Where the connector
  offers `create-design`, use it in place of that pair. The policy is always
  a new design, never an edit of one that exists. To name it, open a
  transaction with `read-design`, apply one `update_title` operation in
  `edit-design` (page title, business, date), and commit, so runs never
  collide. A Canva Doc takes headings, paragraphs, bold, italics, and lists
  only — turn each table into a list with one line per row, and leave charts,
  images, and links out. Brand kit: the first time a skill delivers to Canva,
  run `list-brand-kits`, ask once which kit to apply (or none), and record
  the kit's name and id as the `Canva brand kit` line of the profile; later
  runs pass that id as `brand_kit_id` without asking. If Canva is not
  connected this run, say so and fall back to the visual artifact — do not
  block the deliverable.
- `best for skill` — the skill decides per deliverable: a dashboard or
  screen renders as an artifact; anything that gets submitted, printed, or
  edited elsewhere (a proposal, an application narrative, a redline) ships
  as the document format the skill already names.

A one-off request ("give me this as a Word doc") always wins over the stored
preference, for that run only.

**One page, one deliverable — never hand over the HTML twice.** Building the
artifact may involve writing an HTML file first; that file is scaffolding, not
a deliverable. Publish the artifact and stop. Do not also surface the .html as
a downloadable file, attach it, or offer it alongside the page — an owner
handed both an artifact and an identical HTML download has to work out which
one is real, and the answer is always the artifact. The only file that ships
next to an artifact is a genuinely different format the skill already promises
(an XLSX workbook, a DOCX redline, a PDF packet). A second copy of the same
page in a different wrapper is not that.

---

## Brand tokens — house default, swappable per business

Every color and font below is a CSS custom property. **When the business's
own brand is known** — colors and logo pulled from their website during
`smb-onboard` and stored in the session memory's `## Business context` block
(its Website / Brand colors / Logo fields) — override the color tokens with
theirs. **When it is not known,** the house default applies as-is. Either
way, the component patterns below never change; only the token values do.

**Stored brand applies to every artifact, automatically.** Once the
`## Business context` block carries Brand colors (and optionally a Logo),
every page any skill renders uses them — the owner customizes once at
onboarding and never per page. Capturing that brand is `smb-onboard`'s job
and it must stay frictionless: a pasted website link or a plain-words
description ("forest green and cream"), never a hex code, color picker, or
upload.

```css
:root {
  /* House default palette — override with brand colors when known */
  --ink: #17211F;        /* primary text, warm near-black */
  --paper: #F4F3EE;      /* page background, cool stone, not cream */
  --paper-raised: #FFFFFF; /* card surfaces sitting on --paper */
  --line: #DEDCD1;       /* hairline borders and rules */
  --accent: #0B6B5C;     /* primary accent — confident ledger-teal */
  --accent-soft: #E4EFEC; /* accent tint for pill backgrounds, highlights */
  --amber: #B9781F;      /* secondary accent — "review this" signal */
  --amber-soft: #F6EBDA;

  /* Semantic — separate from the accent, never repurposed for branding */
  --good: #2E7D4F;
  --good-soft: #E4F0E8;
  --warn: #B9781F;
  --warn-soft: #F6EBDA;
  --critical: #B3392C;
  --critical-soft: #FBEAE7;

  /* Type — override the family names when the business has its own */
  --font-display: 'Zilla Slab', Georgia, 'Times New Roman', serif;
  --font-body: 'Public Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'IBM Plex Mono', 'SF Mono', Consolas, monospace;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ink: #EDEAE2;
    --paper: #14201C;
    --paper-raised: #1B2A25;
    --line: #2C3A34;
    --accent: #4FBFA5;
    --accent-soft: #1E332C;
    --amber: #E0A559;
    --amber-soft: #362A16;
    --good: #6FCB94;
    --good-soft: #1D3226;
    --warn: #E0A559;
    --warn-soft: #362A16;
    --critical: #E37B6B;
    --critical-soft: #3A211C;
  }
}

:root[data-theme="dark"] {
  --ink: #EDEAE2;
  --paper: #14201C;
  --paper-raised: #1B2A25;
  --line: #2C3A34;
  --accent: #4FBFA5;
  --accent-soft: #1E332C;
  --amber: #E0A559;
  --amber-soft: #362A16;
  --good: #6FCB94;
  --good-soft: #1D3226;
  --warn: #E0A559;
  --warn-soft: #362A16;
  --critical: #E37B6B;
  --critical-soft: #3A211C;
}
```

**Fonts load from Google Fonts** — the one host the Artifact sandbox allows:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@500;600&family=Public+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
```

If the business's own brand font isn't on Google Fonts, keep the house
default rather than fighting the CSP — a close, working substitute beats a
font that silently fails to load.

**Extracting brand tokens during onboarding.** When `smb-onboard` reads the
business's website (see that skill's workflow), pull the dominant
background/accent colors and any font-family the site declares. Show the
owner what was found — *"Your site uses a deep green and a slab serif —
want your reports to match?"* — and only apply it on a yes. Store the
resolved values in the `## Business context` block (Brand colors / Logo
fields, adding a Brand font line when a usable font-family was found) so
every skill's artifact reads the same tokens without re-deriving them.

---

## Type

- **Display** (`--font-display`) for page titles and section headers only.
  Weight 600, `text-wrap: balance`, never for body copy.
- **Body** (`--font-body`) for everything read as prose.
- **Mono** (`--font-mono`) for every number that sits in a column — currency,
  counts, dates in a table. Pair with `font-variant-numeric: tabular-nums`.

Keep a type scale and stay on it:

```css
--text-xs: 0.75rem;   --text-sm: 0.875rem;  --text-base: 1rem;
--text-lg: 1.125rem;  --text-xl: 1.375rem;  --text-2xl: 1.75rem;
--text-3xl: 2.25rem;  /* the one big number on a dashboard, sparingly */
```

---

## Layout — the ledger-card pattern

Content sits in bordered panels (`--paper-raised` on `--paper`, `1px solid
var(--line)`, `border-radius: 6px` — a slight, deliberate radius, not
`rounded-lg` everywhere by default). Panels stack with `gap`, not margin.
Wide tables get their own `overflow-x: auto` wrapper so the page never
scrolls sideways.

```css
.panel {
  background: var(--paper-raised);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 1.5rem;
}
.page {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  max-width: 840px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}
```

---

## Components

### Header

Every artifact opens the same way: business name (or plugin name if none is
known yet), the page's job in one line, and when it was generated. No hero,
no illustration.

```html
<header class="page-header">
  <div class="brand-mark">RM</div>
  <div>
    <h1>Cash Flow Snapshot</h1>
    <p class="meta">Ridgeline Mechanical · Generated Aug 21, 2026</p>
  </div>
</header>
```

`.brand-mark` is a two-letter monogram in `--accent-soft` background,
`--accent` text, `--font-display` — the same shape on every page, initials
drawn from the business name.

### Stat tile

The one number that matters, large, with a plain-English line under it, not
just a label.

```html
<div class="stat-tile">
  <div class="stat-figure">USD 18,240</div>
  <div class="stat-label">Cash on hand</div>
  <p class="stat-context">About 11 weeks of runway at current burn.</p>
</div>
```

`.stat-figure` uses `--font-mono`, `--text-3xl`, `tabular-nums`. The context
line is what makes it useful — a number alone is not an answer.

### Status pill

A small stamp-like tag, not a rounded pill-shaped badge — rectangular with a
slight radius, uppercase, letter-spaced. Semantic colors only.

```html
<span class="status status--good">On track</span>
<span class="status status--warn">Review</span>
<span class="status status--critical">Overdue</span>
```

```css
.status {
  display: inline-block;
  padding: 0.15rem 0.55rem;
  border-radius: 3px;
  font: 600 var(--text-xs) var(--font-body);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.status--good { background: var(--good-soft); color: var(--good); }
.status--warn { background: var(--warn-soft); color: var(--warn); }
.status--critical { background: var(--critical-soft); color: var(--critical); }
```

### Table

Hairline row dividers, no heavy grid. Numbers right-aligned in
`--font-mono`. Wrap in `.table-scroll` for width.

```html
<div class="table-scroll">
  <table>
    <thead><tr><th>Customer</th><th>Amount</th><th>Days overdue</th></tr></thead>
    <tbody>
      <tr><td>Corwin & Bay</td><td class="num">USD 1,240</td><td class="num">14</td></tr>
    </tbody>
  </table>
</div>
```

### Copy block

For text the owner is meant to paste elsewhere — an SEO fix, an email draft,
a job post. The button copies via the Clipboard API with a manual-select
fallback if the sandbox blocks it (test — do not assume it always works).

```html
<div class="copy-block">
  <button class="copy-btn" onclick="copyBlock(this)">Copy</button>
  <pre>Add this to your homepage title tag: "Ridgeline Mechanical — Same-Day HVAC Repair, Denver Metro"</pre>
</div>
<script>
function copyBlock(btn) {
  const text = btn.nextElementSibling.textContent;
  const done = () => { btn.textContent = 'Copied'; setTimeout(() => btn.textContent = 'Copy', 1500); };
  if (navigator.clipboard?.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(() => fallbackSelect(btn));
  } else {
    fallbackSelect(btn);
  }
}
function fallbackSelect(btn) {
  const range = document.createRange();
  range.selectNodeContents(btn.nextElementSibling);
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  btn.textContent = 'Selected — press Cmd/Ctrl+C';
}
</script>
```

### Checklist with progress

For a close process or an onboarding step list. Count derives from the
items, never hand-typed, so it can't drift out of sync.

```html
<div class="checklist">
  <p class="checklist-progress">3 of 9 done</p>
  <label><input type="checkbox" checked disabled> Bank feed reconciled</label>
  <label><input type="checkbox" disabled> Payroll posted</label>
</div>
```

### Footer

Every artifact ends the same way — quiet, small, `--text-xs`, `--line`
colored:

```html
<footer class="page-footer">Generated by <strong>Cash Flow Snapshot</strong> — Small Business</footer>
```

---

## Both themes, always

Follow the token structure above exactly: bare `:root` for light, the
`prefers-color-scheme` media query guarded by `:not([data-theme="light"])`,
and `:root[data-theme="dark"]` repeating the same values so an explicit
toggle wins either direction. Every component reads colors from the tokens —
never a literal hex in a component rule — so a single override point (brand
colors, or the dark-mode block) recolors the whole page correctly.

---

## What not to do

- **Do not deliver the page twice.** Publish the artifact; never also hand
  over the same content as a downloadable .html file. One page, one
  deliverable.
- **Do not invent a new palette per skill.** Every artifact uses these tokens.
  A one-off look defeats the entire point of a house style.
- **Do not add a hero, an illustration, or marketing copy.** These are
  operating tools, not pitches.
- **Do not skip dark mode.** Half the checklist above exists to prevent an
  unreadable page in the other theme.
- **Do not assume the clipboard API works.** The sandbox can block it —
  test, and ship the fallback.
- **Do not let this rule grow SKILL.md files.** A skill's delivery step is
  one line: "Render the result using the house artifact style
  (`../../shared/artifact-style.md`)," with the specific components named.
  All the CSS and component detail stays in this one file.

---

## Reference build

`reference/artifact-example.html` in this directory is a complete working
page using every component above, for copying structure from directly.
One caveat when copying: the example is a standalone file with a full
doctype/head/body skeleton so it opens in a browser. When the publishing
surface wraps content in its own document skeleton (the Artifact tool does),
copy only the styles and the body content — never the doctype, html, head,
or body tags themselves.
