---
name: ingestion
description: Extract atomic facts from documents following the Fact Protocol. Use when processing source materials (code, manuals, transcripts, configs) into structured knowledge.
---

# Fact Extraction

You extract atomic facts from documents. Each fact is a single, self-contained factual
statement with full source provenance.

Your only job: "What factual statements does this document make?"

You do not decide entity types, relationships, or graph structure. That is the graph
builder's job. You extract raw facts.

## Critical: Writing Facts

You MUST write facts using the Write tool to the path
`.magellan/domains/<domain>/facts/<source_slug>.json`.

The `<source_slug>` is derived from the source document filename: take the filename stem
(without extension), replace path separators and spaces with underscores, and remove any
characters that are not alphanumeric, underscores, hyphens, or dots.

Each fact file follows this JSON structure:

```json
{
  "source_document": "path/to/original/source/document",
  "domain": "lowercase_domain_name",
  "extracted_at": "2024-01-15T10:30:00+00:00",
  "fact_count": 3,
  "facts": [ ... array of atomic facts ... ]
}
```

Generate a unique `fact_id` for each fact using the format `f_` followed by 8 random
hex characters (e.g., `f_3a8b2c1d`). Every fact must have a unique `fact_id`.

Facts MUST be organized by domain: one file per source document at
`domains/<domain>/facts/<source_slug>.json`. Do NOT create batch files like
`facts/batch1.json`.

## The Fact Protocol

Every fact you extract must follow this exact structure:

```json
{
  "fact_id": "f_3a8b2c1d",
  "statement": "Natural language summary of the fact",
  "subject": "The entity or concept this fact is about",
  "subject_domain": "lowercase_domain_name",
  "predicate": "The relationship or property being stated",
  "object": "The value, target, or detail",
  "source": {
    "document": "path/to/source/document",
    "location": "page 12, section 'Exception Handling'",
    "quote": "Exact quote from the source document (max 500 chars)"
  },
  "confidence": 0.85,
  "tags": ["business_rule", "exception_handling"]
}
```

## Rules

1. One fact per statement. If a paragraph contains three claims, extract three facts.
2. Every fact must have a direct quote from the source. No invented content.
3. The quote must be verbatim from the document. Do not paraphrase in the quote field.
4. The statement field IS your summary — make it clear and complete.
5. subject_domain must be lowercase with underscores only (e.g., `billing`, `title_processing`).
6. Confidence reflects how clearly the source states this fact:
   - 0.9-1.0: Explicitly stated, unambiguous
   - 0.7-0.89: Clearly implied or stated with minor ambiguity
   - 0.5-0.69: Inferred from context, needs validation
   - 0.3-0.49: Weak evidence, speculative
   - 0.0-0.29: Contradicted by other evidence in the same document

## Tags

Apply one or more of these tags to each fact:

- `business_rule` — a rule governing business logic or decisions
- `data_flow` — how data moves between systems or components
- `integration` — connection between systems, APIs, protocols
- `system_behavior` — how a system operates, processes, or responds
- `data_model` — entities, fields, relationships in data structures
- `operational` — how systems are operated, maintained, monitored
- `security` — authentication, authorization, encryption, access control
- `performance` — SLAs, throughput, latency, batch timing
- `exception_handling` — error paths, edge cases, workarounds
- `organizational` — teams, ownership, responsibilities
- `constraint` — limitations, restrictions, compliance requirements
- `tribal_knowledge` — undocumented knowledge from interviews or transcripts

## Examples

### Example 1: From a QA Manual (business document)

Source: "Dealer Master Manual 4.3.19.docx", page 5

> "When setting up a new dealership, the Floor Plan Bank must be assigned before
> any vehicles can be entered into inventory."

```json
{
  "fact_id": "f_3a8b2c1d",
  "statement": "A Floor Plan Bank must be assigned to a dealership before vehicles can be entered into inventory",
  "subject": "Dealership Setup",
  "subject_domain": "dealer_management",
  "predicate": "has prerequisite",
  "object": "Floor Plan Bank assignment required before vehicle inventory entry",
  "source": {
    "document": "QA Manuals/Dealer Master Manual 4.3.19.docx",
    "location": "page 5, 'Setting Up a New Dealership'",
    "quote": "When setting up a new dealership, the Floor Plan Bank must be assigned before any vehicles can be entered into inventory."
  },
  "confidence": 0.95,
  "tags": ["business_rule", "constraint"]
}
```

### Example 2: From COBOL source code

Source: "CBBLKBOOK.cblle", lines 142-198

> `IF WS-INV-AMT > 10000 PERFORM 3200-MANUAL-REVIEW`

```json
{
  "fact_id": "f_d4e5f6a7",
  "statement": "Invoices exceeding $10,000 trigger a manual review process via paragraph 3200-MANUAL-REVIEW",
  "subject": "Invoice Processing",
  "subject_domain": "billing",
  "predicate": "has threshold trigger",
  "object": "Manual review triggered for invoice amounts over $10,000",
  "source": {
    "document": "Code/AS400 Artifacts/BLKBOOKV/QBLKBOOK/CBBLKBOOK.cblle",
    "location": "lines 142-198",
    "quote": "IF WS-INV-AMT > 10000 PERFORM 3200-MANUAL-REVIEW"
  },
  "confidence": 0.95,
  "tags": ["business_rule", "exception_handling"]
}
```

### Example 3: From a meeting transcript

Source: "ASI Demo for Slalom.vtt", timestamp 00:12:34

> "we actually moved the entire auction access module to AWS about two years ago
> but the core billing still runs on the AS/400"

```json
{
  "fact_id": "f_b8c9d0e1",
  "statement": "The Auction Access module was migrated to AWS approximately two years ago, while core billing remains on the AS/400",
  "subject": "Auction Access",
  "subject_domain": "infrastructure",
  "predicate": "runs on platform",
  "object": "AWS (migrated ~2 years ago), while core billing remains on AS/400",
  "source": {
    "document": "Meetings/ASI Demo for Slalom.vtt",
    "location": "timestamp 00:12:34",
    "quote": "we actually moved the entire auction access module to AWS about two years ago but the core billing still runs on the AS/400"
  },
  "confidence": 0.80,
  "tags": ["system_behavior", "integration"]
}
```

### Example 4: From a database config or data file

Source: "Current Domain Mapping.csv", row 3

> `billing, invoicing, INVLIB, CBINV001`

```json
{
  "fact_id": "f_f2a3b4c5",
  "statement": "The invoicing sub-domain in billing uses library INVLIB with source program CBINV001",
  "subject": "Invoicing",
  "subject_domain": "billing",
  "predicate": "has source program",
  "object": "CBINV001 in library INVLIB",
  "source": {
    "document": "Domain Information/Current Domain Mapping.csv",
    "location": "row 3",
    "quote": "billing, invoicing, INVLIB, CBINV001"
  },
  "confidence": 0.90,
  "tags": ["data_model", "system_behavior"]
}
```

## Domain Assignment

Assign the `subject_domain` based on the primary business area the fact relates to.

Common domains: `billing`, `title_processing`, `transportation`, `dealer_management`,
`vehicle_inventory`, `auction_operations`, `infrastructure`, `security`, `integration`.

If unsure which domain a fact belongs to, use `general`. The cross-domain linking pass
will reclassify later if needed.

## Language Reference Guides

After classifying a file, check whether a language reference guide exists for the
file's language. The guide provides context about the programming language — syntax,
patterns, naming conventions, and common misinterpretations — that significantly improves
fact extraction quality for niche or legacy languages.

1. Determine the `language_guide_key` from your classification (e.g., `rpg` for RPG ILE,
   `cobol` for COBOL, `cl` for CL programs, `dds` for DDS files).
2. Check if `.magellan/language_guides/<language_guide_key>.md` exists (use the Read tool).
3. If it exists, read the guide and use it as context when extracting facts from this file.
   The guide tells you:
   - How to read the code (syntax, structure, control flow)
   - What patterns carry business logic vs. boilerplate
   - Client-specific naming conventions
   - Common misinterpretations to avoid
4. If no guide exists for this language, proceed normally (no change to behavior).

**Caching**: Read each guide once per language per pipeline run, not once per file. If you
have already read the RPG guide for a previous file, do not re-read it for subsequent RPG
files in the same run — it is already in your context.

**Example**: When processing an RPG ILE file, your classification identifies
`language_guide_key: "rpg"`. You read `.magellan/language_guides/rpg.md` which explains
that `CHAIN` is a keyed read operation, indicators 01-99 are conditional flags, and
`PFDEALRMST` follows the client's PF-prefix naming convention for physical files. With
this context, you extract "the program reads the dealer master file (PFDEALRMST) using
a keyed CHAIN operation with key list KYDLR" instead of "the program reads a file."

## What NOT to Extract

These patterns inflate fact counts with noise. Skip them aggressively:

- Table of contents entries, section headers repeated as content, index pages
- Lines that are just "Chapter N", "Section N.N", or page numbers
- Dotted leader lines (e.g., "Settings ........................... 3")
- Formatting artifacts: page headers, footers, watermarks, copyright notices
- Repeated boilerplate that appears in every document (e.g., "Auction Edge confidential")
- Opinions or editorial commentary (unless quoting a specific named person)
- Generic instructions like "Click OK to continue" or "See screenshot below"
- Empty or stub sections with no substantive content
- Metadata lines like "Last updated:", "Version:", "Author:" (unless the date/version
  is itself a useful fact about the system)

If you're unsure whether something is a real fact or document noise, apply this test:
would an architect preparing for a client meeting need to know this? If not, skip it.

## Fact Density Expectations

Use these benchmarks to gauge whether you're extracting thoroughly. If your yield
falls well below these targets, re-read the document more carefully before moving on.

| Document Type | Expected Facts (per unit) | Notes |
|---------------|---------------------------|-------|
| QA / Ops Manual (per 10 pages) | 15-30 | Business rules, procedures, thresholds |
| COBOL / RPG program (per 500 lines) | 8-15 | File dependencies, business rules, call chains |
| CL program | 5-10 | Job scheduling, file overrides, call chains |
| Meeting transcript (per 30 min) | 10-20 | Decisions, contradictions, tribal knowledge |
| Architecture document (per 10 pages) | 15-25 | System descriptions, integrations, constraints |
| CSV / data file | 3-8 | Schema, field meanings, relationships |
| DDS file | 3-8 | Record format, key fields, field descriptions |

If a file yields fewer than 3 facts, flag it in the progress display:
"Low yield: filename (N facts — expected M+ for this file type)"

These are guidelines, not hard minimums. A boilerplate README genuinely has 0
extractable facts. But a 200-page QA manual with 5 facts means you are skimming
and need to go deeper.

## Reading Large Documents

Not all documents can be processed in a single read. Long documents suffer from
attention degradation — facts from the middle and end of a long file get thinner
coverage than facts from the beginning.

**Determine the reading strategy before you start extracting:**

**Small documents (under ~5,000 lines or ~50 pages):**
Read the entire file in one pass. Extract facts normally.

**Large documents (over ~5,000 lines or ~50 pages):**
Read and extract in sections. Do NOT read the entire file at once.

1. **First pass — structure scan.** Read the first 200 lines with the Read tool
   (use `offset: 0, limit: 200`) to understand the document structure: table of
   contents, section headers, chapter boundaries, or natural break points.

2. **Plan sections.** Divide the document into sections of ~2,000-3,000 lines
   (~30-40 pages) based on the structure you found. Use natural boundaries
   (chapters, sections, modules) when possible. If none exist (e.g., a flat
   CSV or continuous log), use fixed-size chunks with 100-line overlap.

3. **Process each section independently.** For each section:
   a. Read ONLY that section using `offset` and `limit` on the Read tool.
   b. Extract facts from that section.
   c. Write facts immediately (batch write to the fact file).
   d. Display: "Section N/M: extracted K facts (lines X-Y)"

4. **Track sections.** After all sections, verify total lines processed matches
   the document's total line count. If any range was skipped, go back and read it.
   Display: "Document complete: N facts from M sections (lines 1-total)"

**Why this matters:** A 200-page manual read in one pass might yield 30 facts,
heavily weighted toward the first 50 pages. The same manual read in 5 sections
of 40 pages each will yield 60-80 facts with even coverage. The section boundary
forces Claude to give full attention to every part of the document.

**Code files:** Most code files are under 5,000 lines and can be read in one pass.
For very large programs (e.g., 10,000+ line COBOL), split at paragraph/section
boundaries (COBOL) or subroutine boundaries (RPG) rather than arbitrary line counts.

## After Extraction

### Critical: Write in Batches to Avoid Output Limits

Do NOT accumulate all facts in your response and write them in one call at the end.
For large documents, this will exceed output token limits and lose all your work.

Instead, write facts in batches of 10-15 as you extract them:

1. Extract 10-15 facts from one section of the document.
2. **Pre-write checklist** — before writing, verify EVERY fact in the batch:
   - [ ] `fact_id` present (format: `f_` + 8 hex chars)
   - [ ] `statement` present and ≥ 10 characters
   - [ ] `subject` present and non-empty
   - [ ] `subject_domain` present, lowercase, matches `^[a-z][a-z0-9_]*$`
   - [ ] `predicate` present and non-empty
   - [ ] `object` present and non-empty
   - [ ] `source.document` present and non-empty
   - [ ] `source.location` present and non-empty
   - [ ] `source.quote` present, non-empty, ≤ 500 characters
   - [ ] `confidence` is a number between 0.0 and 1.0
   - [ ] `fact_count` in the wrapper matches the actual array length
3. Write the batch using the Write tool.
4. **Post-write verification** — immediately Read the file back and verify:
   - The file is valid JSON
   - `fact_count` matches the length of the `facts` array
   - No fact is missing `source.quote` (the most commonly dropped field)
   If verification fails, fix and rewrite before continuing.
5. **Quote verification** — for each fact in the batch, verify the quote
   actually exists in the source document:
   - Use the Grep tool to search for a distinctive substring of
     `source.quote` (at least 20 characters) in the original file.
   - If Grep finds a match: the quote is verified.
   - If Grep finds no match: the quote may be hallucinated. Re-read the
     relevant section of the source file, find the actual text, and correct
     the quote. If no matching content exists, delete the fact entirely.
   - You do NOT need to Grep every quote for short documents (under 50 lines)
     that you read in full — you can verify by memory. For large documents
     read in sections, always Grep-verify quotes from previous sections
     that are no longer in your immediate context.
   - Display any corrections: "Quote corrected: fact_id (original → fixed)"
   - Display any deletions: "Fact removed: fact_id (quote not found in source)"
6. Move to the next section and repeat.

When appending to an existing fact file, first Read the current file, merge the new
facts into the existing `facts` array, update `fact_count`, update `extracted_at`,
and Write the complete file back. This preserves earlier batches.

For small documents (under ~20 facts), a single Write call is fine — but still
run the pre-write checklist and post-write verification.

### Critical: Nothing Silently Skipped (Principle 3)

Every document you process must end with a recorded disposition. You MUST NOT
move to the next document without accounting for the current one.

- If you cannot read the file: record `unreadable` with the error.
- If you extract zero facts: record `no_facts_extracted` — this is not an error,
  but it must be recorded so the team knows the file was processed.
- If fact writing fails: fix the facts and retry.
  If still failing, record the error and the partial facts that did succeed.
- If any step throws an unexpected error: record `extraction_error` with the
  error message.

**Never silently skip a file, a section of a file, or a link in a file.**
If you encounter something you can't process, say so explicitly with a reason.
