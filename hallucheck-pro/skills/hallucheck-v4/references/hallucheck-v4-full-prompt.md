# Hallucheck V4 — Full Operational Prompt

## Core Checks

In the given input, verify the following assertions in order:

- **(halluref)** For each reference, assess whether the DOI / ISBN / URL and the cited metadata (author, title, journal or publisher, year) are mutually consistent — based on known literature and format plausibility.
- **(halluclaim)** For each reference, assess whether the insight or claim attached is actually present in or warranted by the cited work.
- **(halluinfer)** Retrace the inference stack: do the sub-arguments (x.1, x.2) back their main argument? Do the main arguments collectively back the thesis?
- **(halluurl)** Live-verify each reference identifier using the appropriate API or fetch:
  - **DOI** → fetch `https://api.crossref.org/works/{DOI}` and compare returned `title`, `author` (family + given), `container-title`, `published` date-parts, `volume`, `issue`, `page` against what is cited in the document.
  - **ISBN** → fetch `https://openlibrary.org/isbn/{ISBN}.json` and compare returned `title`, `authors`, `publishers` against what is cited.
  - **Bare URL** (e.g. HBR, Amazon) → fetch the page directly and confirm the article or book title and author are present and match.
  - For each field compared: flag any mismatch, even partial (e.g. year off, middle author missing, title truncated differently).

---

## Output Structure

**1 — Summary** (one line per check, with overall %)

Prefix `- v` if 100%, `- !` otherwise. Format: `- ! Halluurl (78%): [brief description of issues]`

**2 — Prompt** — spell this full prompt inside a fenced codeblock.

**3 — Inference status** — one line per main argument.
Prefix `- v` if sub-arguments back the main argument, `- !` with issue if not.

**4 — Claim status** — one line per sub-argument (x.1, x.2).
Prefix `- v` if insight matches the cited work, `- !` with issue if not.

**5 — Ref plausibility** (halluref, knowledge-based) — one line per reference.
Prefix `- v` if consistent, `- !` with specific field mismatch if not. Keep argument number.

**6 — Live URL status** (halluurl) — one line per reference.
- `- v {ref}` — DOI/ISBN/URL resolves, all compared fields match.
- `- ! {ref}` — (issue) state which fields mismatch or that the identifier does not resolve. Show the expected value vs the returned value. Keep argument number.

---

## CrossRef API Response Fields

```json
{
  "message": {
    "title": ["Article Title"],
    "author": [
      {"family": "Smith", "given": "John"},
      {"family": "Doe", "given": "Jane"}
    ],
    "container-title": ["Journal Name"],
    "published": {"date-parts": [[2010]]},
    "volume": "21",
    "issue": "7",
    "page": "926-930",
    "DOI": "10.1177/..."
  }
}
```

- A CrossRef 404 or empty response = DOI does not exist in the registry → flag as hallucinated.
- A response where `message.title` does not match → flag as wrong paper.

---

## OpenLibrary API Response Fields

```json
{
  "title": "Book Title",
  "authors": [{"name": "Author Name"}],
  "publishers": ["Publisher Name"],
  "publish_date": "2010"
}
```

- An OpenLibrary 404 or empty response = ISBN does not exist → flag as hallucinated.
- A response where `title` does not match → flag as wrong book.

---

*Hallucheck V4 — created 2026-02-28*
