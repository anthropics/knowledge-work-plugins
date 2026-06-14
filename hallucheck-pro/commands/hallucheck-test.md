---
name: hallucheck-test
description: Run a connectivity health check on all halluurl API types (CrossRef, OpenLibrary, Google Books fallback, bare URL). Use this before running /hallucheck on a real document to confirm which external APIs are reachable.
---

# /hallucheck-test

Run a quick API connectivity test for the halluurl phase of Hallucheck Pro.

**Run this immediately after installing the plugin** to know which APIs are reachable in your environment before running `/hallucheck` on a real document.

---

## Step 1 — Network Domain Reachability

Before testing the APIs, verify that each required domain is reachable. For each domain, attempt a basic HTTP request and report success or failure.

| # | Domain | Used for | Required? |
|---|--------|----------|-----------|
| A | `api.crossref.org` | DOI verification (CrossRef) | Yes — DOIs unverifiable if blocked |
| B | `openlibrary.org` | ISBN verification (primary) | No — Google Books is the fallback |
| C | `www.googleapis.com` | ISBN verification (Google Books fallback) | No — OpenLibrary is the primary |
| D | `hbr.org` | Bare URL example (HBR) | No — only needed for HBR-cited articles |

At least one of B or C must be reachable for ISBN verification to work.

Output this section first:

```
## Network Domain Check

| Domain               | Status      | Note                              |
|----------------------|-------------|-----------------------------------|
| api.crossref.org     | ✅ Reachable | DOI verification available        |
| openlibrary.org      | ❌ Blocked   | ISBN primary unavailable          |
| www.googleapis.com   | ✅ Reachable | Google Books fallback available   |
| hbr.org              | ✅ Reachable | Bare URL checks available         |

ISBN resolution: Google Books (fallback active — OpenLibrary blocked)
```

---

## Step 2 — API Fixture Tests

After the domain check, test each API type against a fixed, known-stable fixture reference:

| # | API type | Fixture reference |
|---|----------|------------------|
| 1 | CrossRef (DOI) | Hsee et al. (2010). *Psychological Science* 21(7). DOI: `10.1177/0956797610374738` |
| 2a | OpenLibrary (ISBN — primary) | Piaget (1950/2001). *The Psychology of Intelligence*. Routledge. ISBN: `978-0415254014` |
| 2b | Google Books (ISBN — fallback) | Same ISBN: `978-0415254014` via `googleapis.com/books/v1/volumes?q=isbn=...` |
| 3 | Bare URL (HBR) | Argyris (1977). *Harvard Business Review*. `hbr.org/1977/09/double-loop-learning-in-organizations` |

**Instructions:**
1. For each fixture, fetch the API endpoint and compare returned metadata to the expected values below.
2. For ISBN: test OpenLibrary (2a) first; if it fails, test Google Books (2b) as fallback.
3. Report PASS or FAIL per test. For ISBN, report the source that succeeded (or both failures).
4. Do NOT save a report file — output results directly in chat.

---

## Expected values (ground truth)

### Fixture 1 — CrossRef DOI
- **URL:** `https://api.crossref.org/works/10.1177/0956797610374738`
- **Expected title:** "Idleness Aversion and the Need for Justifiable Busyness" (case-insensitive)
- **Expected authors:** Hsee, Yang, Wang (3 authors)
- **Expected journal:** Psychological Science
- **Expected year:** 2010
- **Expected vol/issue/pages:** 21 / 7 / 926-930

### Fixture 2a — OpenLibrary ISBN (primary)
- **URL:** `https://openlibrary.org/isbn/9780415254014.json`
- **Expected title:** "The psychology of intelligence" (case-insensitive)
- **Expected author:** Piaget
- **Expected publisher:** Routledge
- **Note:** Year will show as 2001 (Routledge reissue) — correct for this edition. Not a failure.

### Fixture 2b — Google Books ISBN (fallback)
- **URL:** `https://www.googleapis.com/books/v1/volumes?q=isbn:9780415254014`
- **Expected title:** contains "Psychology of Intelligence" (case-insensitive)
- **Expected author:** Piaget (in `volumeInfo.authors`)
- **Expected publisher:** Routledge (in `volumeInfo.publisher`)
- **Note:** Test 2b only if 2a fails. If 2b also fails, ISBN resolution is UNAVAILABLE.

### Fixture 3 — Bare URL (HBR)
- **URL:** `https://hbr.org/1977/09/double-loop-learning-in-organizations`
- **Expected:** HTTP 200 response

---

## Output format

Full output when all APIs pass:
```
# Hallucheck-Pro — API Connectivity Test

## Network Domain Check

| Domain               | Status       | Note                              |
|----------------------|--------------|-----------------------------------|
| api.crossref.org     | ✅ Reachable  | DOI verification available        |
| openlibrary.org      | ✅ Reachable  | ISBN primary available            |
| www.googleapis.com   | ✅ Reachable  | Google Books fallback available   |
| hbr.org              | ✅ Reachable  | Bare URL checks available         |

ISBN resolution: OpenLibrary (primary)

## API Fixture Tests

| # | Type                    | Endpoint                                       | Status  | Note                        |
|---|-------------------------|------------------------------------------------|---------|-----------------------------|
| 1 | CrossRef (DOI)          | api.crossref.org/works/10.1177/...             | ✅ PASS | All fields match            |
| 2 | OpenLibrary (ISBN)      | openlibrary.org/isbn/9780415254014.json        | ✅ PASS | Year 2001 expected          |
| 3 | Bare URL (HBR)          | hbr.org/1977/09/double-loop-learning-…         | ✅ PASS | HTTP 200                    |

Result: 3/3 APIs operational — halluurl phase FULLY OPERATIONAL ✅
```

When OpenLibrary is blocked but Google Books succeeds:
```
## Network Domain Check

| Domain               | Status       | Note                              |
|----------------------|--------------|-----------------------------------|
| api.crossref.org     | ✅ Reachable  | DOI verification available        |
| openlibrary.org      | ❌ Blocked    | ISBN primary unavailable          |
| www.googleapis.com   | ✅ Reachable  | Google Books fallback available   |
| hbr.org              | ✅ Reachable  | Bare URL checks available         |

ISBN resolution: Google Books (fallback active — OpenLibrary blocked)

## API Fixture Tests

| # | Type                       | Endpoint                                    | Status  | Note                        |
|---|----------------------------|---------------------------------------------|---------|-----------------------------|
| 1 | CrossRef (DOI)             | api.crossref.org/works/10.1177/...          | ✅ PASS | All fields match            |
| 2a | OpenLibrary (primary)     | openlibrary.org/isbn/9780415254014.json     | ❌ FAIL | EGRESS_BLOCKED              |
| 2b | Google Books (fallback)   | googleapis.com/books/v1/volumes?q=isbn:...  | ✅ PASS | Title and publisher match   |
| 3 | Bare URL (HBR)             | hbr.org/1977/09/double-loop-learning-…      | ✅ PASS | HTTP 200                    |

Result: 3/3 effective — halluurl phase OPERATIONAL (degraded) ⚠
OpenLibrary blocked — Google Books fallback ACTIVE. ISBNs will resolve via Google Books.
```

When both ISBN APIs fail:
```
| 2a | OpenLibrary (primary)     | openlibrary.org/isbn/...                    | ❌ FAIL | EGRESS_BLOCKED              |
| 2b | Google Books (fallback)   | googleapis.com/books/v1/volumes?q=isbn:...  | ❌ FAIL | EGRESS_BLOCKED              |

Result: 2/3 — halluurl phase DEGRADED ⚠
ISBN resolution UNAVAILABLE — both OpenLibrary and Google Books blocked. ISBN references will be flagged ⚠ Unverifiable.
```
