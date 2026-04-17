---
description: Open a PDF in the interactive viewer
argument-hint: "[path-or-url]"
---

> If you need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

# Open PDF

Display a PDF document in the live viewer. Use this when the user wants
to **see** a document — not just extract its text.

## Instructions

1. If the user provides a URL or file path, call `display_pdf` with it
2. If no path given, call `list_pdfs` first to show available documents
3. After displaying, offer next steps based on the document type:
   - **Contract / report** → "Want me to highlight key sections or add
     review notes?"
   - **Form** → "This has fillable fields — shall I help you fill it?"
   - **Academic paper** → "Shall I walk through and annotate the key
     findings?"

## Supported Sources

- Local files (paths or drag-and-drop into your working directory)
- arXiv (`arxiv.org/abs/...` auto-converts to PDF URL)
- Any direct HTTPS PDF URL (use the PDF link, not a landing page)

## When NOT to use this

If the user just wants a summary or text extraction, **do not** open
the viewer — use Claude's native Read tool on the PDF path instead.
The viewer is for interactive, visual workflows.
