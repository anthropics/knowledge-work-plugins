---
name: hallucheck-v4
description: Hallucheck V4 methodology for verifying academic references. Combines knowledge-based plausibility checks (halluref, halluclaim, halluinfer) with live API verification (halluurl) via CrossRef and OpenLibrary. Explains each section and output format. Use this skill to understand the hallucheck framework or as a reference guide.
---

# Hallucheck V4 Methodology

A systematic framework for verifying academic references in argument trees and reference lists.

## Core Concept

Hallucheck V4 extends hallucheck V3 with a **live verification layer** (`halluurl`). It checks references at four levels:

1. **halluref** (knowledge-based) — Does the DOI/ISBN format match the author, title, journal?
2. **halluclaim** (knowledge-based) — Does the cited insight actually appear in the work?
3. **halluinfer** (logical) — Do sub-arguments back the main argument? Is the reasoning chain sound?
4. **halluurl** (live) — Does the DOI/ISBN resolve? Do the returned metadata match what's cited?

---

## The Four Checks

### 1. Halluref (Reference Plausibility)

**Knowledge-based assessment** of whether the identifier (DOI, ISBN, URL) and cited metadata are mutually consistent.

- DOI format is correct for the journal (SAGE, Elsevier, APA, etc.)
- Author names match the journal/publisher typical patterns
- Year, volume, issue are plausible
- Title length and style match the work type (article, book, etc.)

**Output:** `- v {ref}` if consistent, `- ! {ref} (issue details)` if flagged.

### 2. Halluclaim (Insight Accuracy)

**Knowledge-based assessment** of whether the cited insight or claim is actually present in or warranted by the work.

- Does the paper/book actually discuss what the insight describes?
- Is the attribution accurate or is it a distortion/misrepresentation?
- Does the insight map onto the work's actual contribution?

**Output:** `- v` if accurate, `- !` with specific misalignment if not.

### 3. Halluinfer (Inference Chain)

**Logical assessment** of whether sub-arguments (x.1, x.2) actually back their main argument, and whether the argument chain supports the thesis.

- Do 1.1 + 1.2 together establish argument 1?
- Do arguments 1–10 collectively support the thesis?
- Are any inferences speculative or unsupported?

**Output:** `- v` if chain is sound, `- !` with the weak link identified.

### 4. Halluurl (Live Verification)

**API-based verification** that the identifier resolves and the metadata matches.

Uses:
- **CrossRef API** (`api.crossref.org/works/{DOI}`) for journal articles
- **OpenLibrary API** (`openlibrary.org/isbn/{ISBN}.json`) for books
- **Direct fetch** for bare URLs (HBR, Amazon, etc.)

**Compared fields:**
- Title (must match exactly or very closely)
- Authors (all author names present)
- Year (must match published year)
- Journal/Publisher (exact match)
- Volume, issue, pages (if cited, must match)

**Output:** `- v {ref}` if all fields match, `- ! {ref} (specific field mismatch: expected vs. returned)` if any field diverges.

---

## Output Format

### Summary
One line per check type:
```
- ! Halluref (95%): 1 minor format mismatch (Piaget book scope)
- v Halluclaim (100%): All insights accurate to cited works
- v Halluinfer (100%): Argument chains solid
- ! Halluurl (85%): 3 DOI mismatches, 1 ISBN timeout
```

### Section 1: Halluref Status
List every reference:
```
- v 1.1 Hsee (2010) — DOI format correct, authors/title/journal consistent
- ! 2.2 Piaget (1950) — Book scope mismatch (cited for concepts better in different work)
```

### Section 2: Halluclaim Status
List insights vs. works:
```
- v 1.1 — "Idleness aversion" insight accurately represents Hsee et al. (2010)
- ! 10.1 — "Mindfulness definition" more precisely sourced from 2003 academic paper, not 1994 popular book
```

### Section 3: Halluinfer Status
Argument chains:
```
- v Argument 1 ← 1.1 + 1.2 both support "speed as concealment"
- ! Argument 7 ← 7.1 is analogical (self-handicapping) not direct
```

### Section 4: Halluurl Status
Live verification:
```
- v 1.1 Hsee 2010 DOI resolves, title "Idleness aversion...", authors match, year 2010, journal Psychological Science ✓
- ! 4.2 Düzel 2010 DOI resolves but title mismatch: cited "NOMAD", returned "Novelty-related motivation of anticipation..."
- ! 5.2 Rogers ISBN timeout — OpenLibrary API unreachable
```

---

## When to Use Hallucheck V4

- **Finalizing argument trees** before publication
- **Verifying reference accuracy** in academic work
- **Catching hallucinated citations** (real DOIs pointing to wrong papers, non-existent ISBNs)
- **Building confidence in your reasoning** (do your backings actually support your claims?)

## When NOT to Use

- Early drafting phase (too rigid, slows exploration)
- Informal research notes (overkill)
- When references are intentionally vague or secondary

---

## Common Issues Caught by Hallucheck V4

| Issue | Detection | Example |
|-------|-----------|---------|
| Wrong DOI (resolves to different paper) | halluurl | Cited "Smith 2010 on X", DOI resolves to "Smith 2010 on Y" |
| Non-existent ISBN | halluurl | ISBN doesn't exist in OpenLibrary; 404 |
| Misquoted insight | halluclaim | Citation describes paper's finding, but paper actually argues the opposite |
| Weak inference | halluinfer | Sub-argument 2.1 doesn't actually support main argument 2 |
| Incorrect year/volume | halluurl | Cited "vol 5", CrossRef returns "vol 6" |

---

See `references/hallucheck-v4-full-prompt.md` for the complete operational prompt.
