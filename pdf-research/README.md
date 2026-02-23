# PDF Research Plugin

Read and analyze PDF documents using a local MCP server. Designed for
academic paper review, document analysis, and research workflows.

## What It Does

- **Open PDFs** from local files, arXiv, bioRxiv, and other academic sources
- **Interactive viewer** with search, navigation, and zoom
- **AI-powered analysis** -- summarize, extract key points, compare papers

## Commands

| Command | What it does |
|---------|-------------|
| `/pdf-research:read` | Open a PDF for reading |
| `/pdf-research:summarize` | Summarize a document |

## How It Works

This plugin uses a **local MCP server** (`@modelcontextprotocol/server-pdf`)
that runs on your machine via `npx`. No API keys or remote services needed --
the PDF server starts automatically when the plugin loads.

This is different from other knowledge-work plugins which use remote HTTP
connectors. The local server pattern enables offline PDF access and avoids
the need for a remote deployment.

## Requirements

- Node.js >= 18
- Internet for remote PDFs (arXiv, etc.)

## Supported PDF Sources

- Local files (file paths in your working directory)
- [arXiv](https://arxiv.org) papers
- [bioRxiv](https://biorxiv.org) / [medRxiv](https://medrxiv.org) preprints
- [chemRxiv](https://chemrxiv.org), [Zenodo](https://zenodo.org), [OSF](https://osf.io)
- [HAL Science](https://hal.science), [SSRN](https://ssrn.com)
