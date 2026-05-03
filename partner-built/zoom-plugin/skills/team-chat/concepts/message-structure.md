# Message Card Structure (Chatbot API)

Chatbot messages use a card-like JSON structure (often called "message cards").

## High-Level Shape

- `content.head`: title + optional subhead
- `content.body`: array of blocks
  - `message` blocks for text
  - `fields` blocks for key/value rows
  - `actions` blocks for buttons
  - `attachments` blocks for images/links

## Where To Look

- Component reference: `../references/message-cards.md`

## Common Pitfalls

- Buttons must include a `value` you can route on when you receive an interaction webhook.
- Many issues that look like "Zoom didn't render my card" are just invalid JSON shape; validate your payload before sending.

