# Hallucheck Pro

**Verify academic references via CrossRef and OpenLibrary APIs.**

A Claude Cowork plugin that extracts references from argument trees, validates them live against academic databases, and generates markdown hallucheck reports.

---

## What It Does

- **Reads** argument tree files from your vault (or wikilinks)
- **Extracts** all DOIs, ISBNs, and URLs
- **Verifies** each reference live via:
  - **CrossRef API** for journal articles (DOIs)
  - **OpenLibrary API** for books (ISBNs)
  - **Direct fetch** for bare URLs
- **Compares** returned metadata (title, authors, year, journal, volume, issue, pages) against what you cited
- **Generates** a markdown hallucheck report with four verification sections:
  1. **Inference** — Do sub-arguments back main arguments?
  2. **Claims** — Do cited insights match the actual works?
  3. **Reference plausibility** (knowledge-based)
  4. **Live URL verification** (API-based) — the critical addition

---

## Installation

1. Download `hallucheck-pro.plugin`
2. Install it in Cowork (drag-and-drop or via plugin manager)
3. Restart Cowork
4. The `/hallucheck` command becomes available
5. **Run `/hallucheck-test` immediately after installing** — this checks which APIs are reachable in your environment and tells you exactly what will and won't work before you run a real verification.

---

## Usage

### Basic Command

```
/hallucheck path/to/argument-tree.md
/hallucheck [[my-argument-tree]]
```

Both path and wikilink formats work.

### What Happens

1. File is read from your vault
2. All references (DOIs, ISBNs, URLs) are extracted
3. Each is verified live via API (30–60 seconds depending on count)
4. A markdown report is generated and saved to `x/AI_output/`

### Example Output

```markdown
# Hallucheck Report — power of slowness-argument tree

## Summary
- v Halluref (95%): Knowledge-based plausibility all checks pass
- v Halluclaim (100%): All insights match cited works
- v Halluinfer (100%): Argument chains solid
- ! Halluurl (88%): 1 DOI mismatch, 1 ISBN timeout

## Inference Status
- v Arg 1 ← 1.1 + 1.2 both support "speed as concealment"
- v Arg 2 ← 2.1 + 2.2 back "speed = info, slowness = understanding"
...

## Claim Status
- v 1.1 Hsee (2010) — "Idleness aversion" accurately represents the paper
- v 1.2 Hayes (1996) — Experiential avoidance concept accurate
...

## Reference Plausibility (Knowledge-Based)
- v 1.1 Hsee, C. K., Yang, A. X., & Wang, L. (2010) — Format/metadata all consistent
- v 1.2 Hayes et al. (1996) — Authors, journal, year all plausible
...

## Live URL Verification
- v 1.1 DOI resolves ✓ Title: "Idleness aversion and the need for justifiable busyness"
- v 1.2 DOI resolves ✓ Authors: Hayes, S.C., Wilson, K.G., Gifford, E.V., ...
- ! 4.2 Title mismatch — cited "NOMAD", returned "Novelty-related motivation..."
- ! 9.2 ISBN timeout — OpenLibrary API unreachable (retry later)
```

---

## Components

### Commands

- **`/hallucheck`** — Run verification on a file
- **`/hallucheck-test`** — API connectivity health check (run this first if you suspect network issues)

### Skills

- **`hallucheck-v4`** — Standalone skill documenting the hallucheck V4 methodology
  - Use to understand the framework
  - Reference for what each check does
  - Load anytime, not just via `/hallucheck`

### MCP Server

- **`hallucheck-verifier`** — Python server that calls CrossRef and OpenLibrary APIs
  - Runs automatically when `/hallucheck` is invoked
  - Returns structured JSON with verification results
  - Handles errors gracefully (continues even if one reference fails)

---

## Output Format

Reports are saved with versioning:
- First run: `hallucheck-{filename}-v1.md`
- Second run: `hallucheck-{filename}-v2.md`
- Etc.

All reports go to `x/AI_output/` in your vault.

---

## Network Requirements

The plugin requires internet access to:
- `api.crossref.org` (CrossRef)
- `doi.org` (DOI resolution)
- `openlibrary.org` (OpenLibrary)
- `googleapis.com` (Google Books fallback)
- Any bare URLs cited (e.g., `hbr.org`)

These are public, free APIs with no authentication required.

### Cowork Domain Allowlist

Claude's sandbox restricts outbound network access by default. You must add the required domains manually in:

**Settings → Capabilities → Additional allowed domains**

Add each of the following:

```
api.crossref.org
doi.org
openlibrary.org
googleapis.com
```

Add any other domains your cited URLs reference (e.g. `hbr.org`, `pubmed.ncbi.nlm.nih.gov`).

> Without these entries, the `halluurl` phase will report all references as `⚠ Unverifiable (network)`. Run `/hallucheck-test` after adding the domains to confirm connectivity.

---

## Interpreting Results

### ✓ Green (Clean)

All checks pass for that reference. Use it with confidence.

### ! Orange (Flagged)

One or more checks found an issue:

| Flag | Meaning | Action |
|------|---------|--------|
| **Halluref issue** | DOI/ISBN format or metadata seems off (knowledge-based) | Review manually; might be an unusual format |
| **Halluclaim issue** | Cited insight may not match what the paper actually says | Check the paper; may need to revise the insight |
| **Halluinfer issue** | Sub-argument doesn't clearly support the main argument | Strengthen the logical chain |
| **Halluurl issue** | DOI/ISBN doesn't resolve OR metadata doesn't match | Critical: check if you cited the right paper |

---

## Testing

### /hallucheck-test

Before running `/hallucheck` on a real document, you can verify that all three external API types are reachable:

```
/hallucheck-test
```

This runs against three fixed fixture references — one per API type — and reports PASS/FAIL:

| # | API type | Fixture |
|---|----------|---------|
| 1 | CrossRef (DOI) | Hsee et al. (2010) — Psychological Science |
| 2a | OpenLibrary (ISBN — primary) | Piaget (1950) — The Psychology of Intelligence |
| 2b | Google Books (ISBN — fallback) | Same ISBN via googleapis.com (tested if 2a fails) |
| 3 | Bare URL (HBR) | Argyris (1977) — Double loop learning in organizations |

Expected output if all APIs are up:

```
Result: 3/3 APIs reachable — halluurl phase OPERATIONAL ✅
```

If you see `DEGRADED` or `FAIL`, your session network is blocking one or more external APIs. The main `/hallucheck` command will still run but will mark affected references as `Unverifiable (network)`.

**Why these fixtures?** They are well-established references in stable databases, unlikely to be removed or modified. The Düzel 4.2 mismatch discovered during testing (title truncation) is intentionally excluded — test fixtures should be clean references that return exact matches.

---

## Known Limitations

1. **API rate limits** — CrossRef and OpenLibrary have rate limits. If you run hallucheck on 100+ references, you may hit limits (waits 1 sec between calls to avoid this)

2. **Title matching is fuzzy** — If a title is truncated or abbreviated differently, it may flag as a mismatch even if it's the same paper. Manual review recommended.

3. **Special characters** — Some DOIs with encoded characters may not resolve. Test first.

4. **OpenLibrary ISBN gaps** — Not all ISBNs are in OpenLibrary. If a book is rare or very recent, it might timeout.

---

## Troubleshooting

### "DOI does not resolve"
- Check the DOI format (should be `10.xxxx/...`)
- Try the DOI manually: https://doi.org/10.1177/...
- Some DOIs may be temporarily unavailable

### "ISBN not found"
- Verify the ISBN is correct (13 digits)
- Check on Amazon or OpenLibrary manually
- Rare/old books may not be indexed

### "API unreachable"
- Check your internet connection
- If behind a corporate proxy, check network settings in Cowork
- CrossRef/OpenLibrary may be temporarily down

### Command not found
- Restart Cowork after installing the plugin
- Verify plugin is listed in plugin manager

---

## Building on This Plugin

Hallucheck Pro is designed to be extended. Future versions could add:

- Zotero integration (read references from Zotero library)
- Semantic Scholar API (additional verification source)
- PDF extraction (parse references from PDFs directly)
- Batch scheduling (hallucheck documents on a schedule)
- Report aggregation (summary across multiple documents)

---

## License & Attribution

**Hallucheck Pro** was created by Roland for personal use in verifying academic argument trees.

**Methodology**: Hallucheck V4 extends Hallucheck V3 (knowledge-based verification) with live API verification via CrossRef and OpenLibrary.

**APIs Used**:
- [CrossRef API](https://www.crossref.org/) — Journal article metadata
- [OpenLibrary API](https://openlibrary.org/developers/) — Book metadata (primary)
- [Google Books API](https://developers.google.com/books) — Book metadata (fallback, no auth required)

---

## Support

For issues or feature requests, open an issue on [GitHub](https://github.com/luctaesch/hallucheck-pro/issues). Contributions and PRs welcome.

---

*Plugin version: 0.3.0*
*Created: 2026-02-28*
