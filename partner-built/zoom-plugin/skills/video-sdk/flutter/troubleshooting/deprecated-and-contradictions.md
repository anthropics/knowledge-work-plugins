# Deprecated and Contradictions

Observed from freshly crawled docs/reference plus local package archive:

## 1. Prompt reference was missing/invalid

- Input prompt had `reference: o`.
- Effective Flutter reference source was discovered from docs links and crawled from `sdk/custom/flutter/index.html`.

## 2. Version metadata mismatch in package archive

- Archive filename indicates `2.4.0`.
- `pubspec.yaml` and changelog content show `2.3.10` references.

Action: treat archive naming and package metadata independently; verify actual package version fields before rollout.

## 3. Docs/package age drift indicators

- Some docs mention package versions and setup patterns that may lag current wrappers.
- API reference is very large and highly version-sensitive (helpers, enums, errors).

Action: pin tested versions and maintain an internal compatibility matrix.

## 4. Crawl completeness note

- Reference crawl completed with one page-level error among a very large set.
- Use targeted recrawl for missing pages if a specific symbol cannot be found.
