---
name: pdf-reading
description: Read and navigate PDF documents using the local PDF server. Reference this when the user wants to open, read, search, or interact with any PDF file or academic paper.
---

# PDF Reading

You have access to a local PDF server that provides interactive document viewing.

## Available Tools

- **list_pdfs** -- Show available PDFs. Call with no arguments.
- **display_pdf** -- Open a PDF in the interactive viewer.
  - `url` (string): URL or local file path
  - `page` (number, optional): Starting page number

## How to Use

**When the user mentions a PDF, paper, or document:**
1. If they give a URL or path, call `display_pdf` directly
2. If they say "open the paper" without specifying, call `list_pdfs` to show options
3. After displaying, offer to summarize, extract data, answer questions

**arXiv shortcuts:**
- `arxiv.org/abs/2301.12345` is auto-converted to the PDF URL
- Users can just say "open arxiv 2301.12345"

**Supported remote sources:**
arXiv, bioRxiv, medRxiv, chemRxiv, Zenodo, OSF, HAL Science, SSRN

## Best Practices

- Always display the PDF before trying to analyze it
- For multi-page documents, ask which section the user cares about
- When comparing papers, display them one at a time and note key differences
