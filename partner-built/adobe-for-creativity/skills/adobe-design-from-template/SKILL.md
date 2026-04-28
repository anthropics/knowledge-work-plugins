---
name: adobe-design-from-template
description: >
  Create any visual design using Adobe Express templates — including flyers, posters, banners,
  social media posts (Instagram stories, Facebook posts, LinkedIn graphics), business cards,
  invitations, greeting cards, resumes, cover letters, brochures, newsletters, certificates,
  presentations, YouTube thumbnails, email headers, logos, menus, labels, and more.
  Use this skill whenever the user wants to make, design, create, or build any visual — even
  if they just say "make me a flyer", "design a poster", "I need something for Instagram",
  "create an event invite", "make a business card", or any similar request.
  Also handles requests to find or browse templates, edit text/copy, change background
  colors, or animate a design.
  Access: 🔐 Signed-In required | Gen AI: ❌
license: Apache-2.0
metadata:
  version: 1.0.0
  visibility: public
compatibility: "Requires Adobe for creativity MCP — search_design, fill_text, change_background_color, animate_design."
---

# Adobe Design from Template

Helps users find an Adobe Express template and customize it — updating text,
background color, and animation — producing a finished Express document ready
to share or open in Express for further editing.

---

## Step 0 - prereq: Initialize Adobe Tools
Call `adobe_mandatory_init` first. This returns file handling rules and tool routing guidance required for the rest of the workflow.

```json
{ "skill_name": "adobe-design-from-template", "skill_version": "1.0.0" }
```

---

## Workflow

### Step 0 — Build the search query (don't ask questions first)

Extract the design type from whatever the user said and go straight to Step 1.
Asking clarifying questions before showing templates creates friction; the picker
lets users course-correct visually, which is faster.

| User says                        | Query to use               |
| -------------------------------- | -------------------------- |
| "make me a flyer"                | `"flyer"`                  |
| "I need something for Instagram" | `"Instagram post"`         |
| "design a poster for my event"   | `"event poster"`           |
| "make a business card"           | `"business card"`          |
| "flyer for an ice cream social"  | `"ice cream social flyer"` |

---

### Step 1 — Search for a template

Call `search_design`:

```json
{
  "generalQuery": "<design type from user prompt>",
  "pageSize": 24
}
```

This renders an interactive picker in the chat. The user taps a template to select
it; the URN comes back automatically. If the user says "show more", call
`search_design` again with the same query and increment `startIndex` by `pageSize`.

---

### Step 2 — Confirm selection and offer edits

Once a template is selected, confirm what was picked and ask what to customize:

> "Got it — you've selected [template name]. What would you like to change?
>
> - ✏️ **Edit the text** — names, dates, headlines, copy
> - 🎨 **Change the background color**
> - ✨ **Animate it**
> - ✅ **I'm done** — just give me the link"

The user may choose one, several, or none. Apply each in sequence, then loop back
and ask if they want anything else before wrapping up.

---

### Step 3 — Apply edits

After each edit, ask: *"What else would you like to change, or does this look good?"*

#### Edit text / copy

Call `fill_text`:

```json
{
  "templateURN": "<URN>",
  "description": "<what to change and what to change it to>",
  "generalQuery": "<same, minus any PII>"
}
```

If the user hasn't specified what the text should say, ask before calling.

`fill_text` occasionally fails on the first attempt due to transient errors — if
it returns an error, retry once with identical parameters before reporting failure.

#### Change background color

Call `change_background_color`:

```json
{
  "templateOrDocumentURN": "<URN>",
  "backgroundColor": "<hex>",
  "description": "<e.g. change background to coral pink>",
  "generalQuery": "<same, minus any PII>"
}
```

If the user describes a color without a hex (e.g. "coral pink"), pick a
reasonable hex value using your judgment.

#### Animate

Call `animate_design`:

```json
{
  "templateOrDocumentURN": "<URN>",
  "description": "<animation style or intent>",
  "generalQuery": "<same, minus any PII>"
}
```

If `animate_design` returns a 403, the user's plan doesn't include animation.
Skip it and note in the delivery: *"Animation isn't available on your current Adobe plan — the rest of your design is ready."* Retrying does not resolve a 403 entitlement — continue without retry.

---

### Step 4 — Deliver

When the user is satisfied:

```
✅ Here's your finished design:

🎨 Template: [name]
[Edits applied, e.g. ✏️ Copy updated · 🎨 Background changed · ✨ Animated]

📎 Open in Express: [editor link]
```

Remind the user that the document is temporary (deleted after 12 hours) and
they should open it in Express to save.

---

## Coming soon

**ACPC asset picker** — a native picker for selecting images from Creative Cloud
Libraries is in development. This skill will be updated when it ships.

---

## Error handling

| Situation                           | Action                                                                                                      |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `fill_text` fails on first attempt  | Retry once with identical parameters                                                                        |
| `animate_design` returns 403        | Skip; note entitlement limit in delivery                                                                    |
| Any tool returns 401                | Ask user to re-authenticate via Adobe OAuth, then retry                                                     |
| No templates match query            | Try a broader query                                                                                         |
| User hasn't selected a template yet | Do not advance past the picker until a URN is returned; the URN is required for every subsequent tool call. |
| User skips all edits                | Fine — deliver the template link as-is                                                                      |

---

## Constraints

- The workflow always begins with the template picker before any edits.
- Template URNs come only from the picker — do not synthesise them.
- All edits are optional — don't assume the user wants any particular change
