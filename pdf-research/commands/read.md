---
description: Open a PDF for reading and analysis
---

# Read PDF

Open a PDF document for interactive reading. Accepts local file paths,
arXiv URLs, or other academic paper URLs.

## Instructions

1. If the user provides a URL or file path, call `display_pdf` with that URL
2. If no URL given, call `list_pdfs` first to show available documents
3. After displaying, offer to summarize, extract key points, or answer questions

## Supported Sources

- Local files (drag-and-drop or file path)
- arXiv papers (arxiv.org/abs/... or arxiv.org/pdf/...)
- bioRxiv, medRxiv, chemRxiv preprints
- Zenodo, OSF, HAL, SSRN
