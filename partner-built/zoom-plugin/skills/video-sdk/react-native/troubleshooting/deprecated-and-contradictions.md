# Deprecated and Contradictions

Observed from crawled docs/reference and local package analysis:

## 1. Naming inconsistency in examples

- Some samples/docs use `username`; current typed wrappers often use `userName`.
- Action: normalize to the exact type definitions of the installed wrapper version.

## 2. README duplication/quality issues

- Package README includes duplicated `videoOptions` block in join example.
- Action: trust typed API references over README snippets when inconsistent.

## 3. Deprecated annotation helper surface in reference

- Crawled reference marks deprecation signals on annotation helper type/class pages.
- Action: treat annotation helper APIs as version-sensitive and verify current support before new feature adoption.

## 4. \"Not supported\" notes in share docs

- Crawled React Native share docs include explicit not-supported caveats for some share paths/features.
- Action: gate share features by runtime capability checks and fallback UI.

## 5. Large API surface drift risk

- React Native reference includes many helpers/enums/types that evolve over releases.
- Action: pin versions and keep app-level adapter boundaries around helper/event APIs.

## 6. External quickstart verification constraint

- Direct remote quickstart verification can fail in restricted DNS/network environments.
- Action: prioritize local package + crawled docs/reference as baseline and verify quickstart when network is available.
