---
description: Add materials or corrections to the Magellan knowledge graph
---

# Add Materials

Add a file, directory, correction, or resolution to the knowledge graph.

## Usage

```
/magellan:add <path>                        Add a file or directory
/magellan:add --correction "..."            Record a verbal correction
/magellan:add --resolve <id> "..."          Resolve a contradiction or answer a question
```

## Pre-Flight Check

Verify `.magellan/` exists. If not, initialize the workspace:
1. `mkdir -p .magellan/domains .magellan/diagrams .magellan/language_guides`
2. Write `.magellan/state.json` with `{"initialized_at": "<ISO timestamp>"}`.
3. Copy starter language guides from skills directory if available.

## Adding Files

When a file path is provided:

1. Read the file with the Read tool.
2. If it's a code file, check `.magellan/language_guides/` for a matching language
   guide. Read the guide for context before extracting facts.
3. Apply the ingestion skill to extract atomic facts.
4. Write facts to `.magellan/domains/<domain>/facts/<source_slug>.json`
   following the fact schema in file-conventions.
5. Update `.magellan/processed_files.json` with the file's disposition.
6. Report: facts extracted, domain, any issues.

When a directory path is provided:

1. List all files using Glob.
2. Read `.magellan/processed_files.json` to find already-processed files.
3. Skip unchanged files. Display: "Processing N new files (M skipped)."
4. Process each file using the single-file workflow above.
5. Update processed_files.json after each file.
6. Report: total processed, facts per file, skipped count.

## Adding Corrections

When `--correction` is provided with a quoted string:

1. Create a correction fact:
   - Parse the text to identify the subject and claim
   - Set `source.document` to `_corrections/<timestamp>.json`
   - Set `source.location` to "verbal correction"
   - Set `source.quote` to the exact text provided
   - Set `confidence` to 0.95
   - Set tags to `["correction"]`

2. Write to `.magellan/domains/<domain>/facts/_corrections/<timestamp>.json`.

3. Report what was recorded. The graph builder will detect contradictions
   on the next pipeline run.

## Resolving Contradictions and Answering Questions

When `--resolve <id>` is provided with a resolution note:

The `<id>` can be a contradiction ID (e.g., `c_001`) or a question ID (e.g., `oq_001`).

**For contradictions (c_xxx):**

1. Search for the contradiction across all domains:
   - Use Glob to find `domains/*/contradictions.json`.
   - Read each file and find the entry matching the ID in the `active` array.
2. Move the contradiction from `active` to `resolved`:
   - Remove it from the `active` array.
   - Add `resolution_note` (the quoted text), `resolved_at` (current ISO timestamp),
     and set `status` to `"resolved"`.
   - Append it to the `resolved` array in the same file.
3. Write the updated file back.
4. If the contradiction had `related_entities`, read each entity and remove the
   `contested: true` flag if no other active contradictions reference it.
5. Display:
   ```
   Resolved: c_001 (billing)
   Resolution: "Confirmed with John Smith: threshold changed to $15k in Q4"
   Affected entities updated: billing:manual_review_bypass
   ```

**For open questions (oq_xxx):**

1. Search across all domains:
   - Use Glob to find `domains/*/open_questions.json`.
   - Read each file and find the matching entry in the `active` array.
2. Move from `active` to `resolved`:
   - Remove from `active`.
   - Add `answer_source` (the quoted text), `answered_at` (current ISO timestamp),
     and set `status` to `"answered"`.
   - Append to the `resolved` array.
3. Write the updated file back.
4. Display:
   ```
   Answered: oq_003 (billing)
   Answer: "The $10k threshold is still active per Jane Doe (Finance)"
   ```

**If the ID is not found** in any domain, display:
```
Not found: <id>. Use /magellan:ask to list active contradictions and questions.
```

## Notes

- Every fact traces to a source document. Corrections create a record document.
- Follow the fact schema in file-conventions exactly.
- For large files, extract facts in batches of 10-15 to stay within output limits.
- Resolving a contradiction creates an audit trail — the dashboard shows both
  active and resolved items.
