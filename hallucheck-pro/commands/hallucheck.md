---
name: hallucheck
description: Verify academic references in an argument tree file via CrossRef, OpenLibrary, and Google Books APIs. Extracts all DOIs, ISBNs, and URLs from the file, validates metadata live, and generates a markdown hallucheck report in x/AI_output/.
---

# /hallucheck

Verify academic references in an argument tree or reference document.

## Usage

```
/hallucheck path/to/argument-tree.md
/hallucheck [[power of slowness-argument tree]]
```

Accepts both:
- **Relative/absolute file paths**: `Luc25/Efforts/Works/Articles/my-tree.md`
- **Wikilink format**: `[[my-argument-tree]]`

## What it does

1. **Read** the file from your vault
2. **Extract** all references with DOIs, ISBNs, and bare URLs
3. **Verify** each reference live using the resolution chain below
4. **Compare** returned metadata (title, authors, year, journal, volume, issue, pages) against what's cited
5. **Generate** a markdown hallucheck report with four sections:
   - Summary (overall % clean)
   - Hallucheck V4 prompt (reference)
   - Inference status (do sub-arguments back main arguments?)
   - Claim status (do insights match cited works?)
   - Reference plausibility (knowledge-based check)
   - Live URL status (API verification results)
6. **Output** report to `x/AI_output/hallucheck-{filename}-v1.md` (increments versions if file exists)

## API resolution chain

| Reference type | Primary API | Fallback API |
|----------------|-------------|--------------|
| DOI | CrossRef (`api.crossref.org`) | — |
| ISBN | OpenLibrary (`openlibrary.org`) | **Google Books** (`googleapis.com`) |
| Bare URL | Direct HTTP check | — |

If OpenLibrary is blocked or unavailable, ISBNs are automatically retried via Google Books. The report records which source was used (`source: OpenLibrary` or `source: GoogleBooks (fallback)`). If both are unreachable, the reference is flagged `⚠ Unverifiable`.

## Example output

```
# Hallucheck Report — power of slowness-argument tree

## Summary
- v References (98%): All verified. 1 minor mismatch flagged.
- v Claims (100%): All accurate.
- v Inferences (100%): Argument chains solid.

## Live Verification Results
- v 1.1 Hsee 2010 — DOI resolves, metadata matches ✓
- v 2.2 Piaget 1950 — ISBN resolves via Google Books (fallback), title/publisher match ✓
- ! 9.1 Wilson 2014 — DOI resolves, author mismatch: "Ellsworth" → "Ellerbeck"
...
```

## Requirements

- File must be readable Markdown with structured references (DOI: URL, ISBN: number, or bare URLs)
- CrossRef must be accessible for DOI verification
- OpenLibrary **or** Google Books must be accessible for ISBN verification

## Notes

- Reports are versioned: first run creates `v1`, second creates `v2`, etc.
- If a reference cannot be verified (API timeout, invalid format), the report flags it with `⚠ Unverifiable`
- Run `/hallucheck-test` first to check which APIs are reachable in your environment
- The hallucheck methodology is documented in the **hallucheck-v4** skill (loadable separately)
