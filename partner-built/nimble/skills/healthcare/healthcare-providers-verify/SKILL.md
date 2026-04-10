---
name: healthcare-providers-verify
description: |
  Validates practitioner credentials and license status against the NPI registry.
  Cross-references specialties, credentials, and practice addresses against
  official records. Returns Verified / Partially Verified / Unverified / Flagged
  per practitioner with mismatch details and source URLs.

  Triggers: "verify these doctors", "check provider credentials", "validate
  licenses", "verify NPI numbers", "cross-check credentials against NPI",
  "compliance audit on providers", "are these practitioners still licensed",
  "validate my provider list". Accepts CSV, Google Sheet URL, or pasted data.

  Do NOT use for extracting providers from practice URLs — use healthcare-providers-extract instead.
  Do NOT use for filling data gaps — use healthcare-providers-enrich instead.
  Do NOT use for discovering practices — use market-finder or local-places instead.
  Do NOT use for general extraction — use nimble-web-expert instead.
allowed-tools:
  - Bash(nimble:*)
  - Bash(date:*)
  - Bash(cat:*)
  - Bash(mkdir:*)
  - Bash(python3:*)
  - Bash(echo:*)
  - Bash(jq:*)
  - Bash(ls:*)
  - Bash(wc:*)
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
metadata:
  author: Nimbleway
  version: 0.17.0
---

# Healthcare Providers Verify

Validate practitioner credentials against the NPI registry and authoritative
sources, powered by Nimble's web data APIs.

User request: $ARGUMENTS

**Before running any commands**, read `references/nimble-playbook.md` for Claude Code
constraints (no shell state, no `&`/`wait`, sub-agent permissions, communication style).

---

## Instructions

### Step 0: Preflight + WSA Discovery

**Sibling handoff check:** Before running full preflight, check if
`healthcare-providers-extract` or `healthcare-providers-enrich` ran earlier in this
session by following the Sibling Handoff pattern from `references/nimble-playbook.md`.
If same-day output exists, skip CLI check and profile load, and reuse WSA Layer 1/3
inventory. Only re-run Layer 2 if the verification focus changed.

**Otherwise, run full preflight** from `references/nimble-playbook.md` (5 simultaneous
Bash calls: date calc, today, CLI check, profile load, index.md load).

**Also simultaneously** — run WSA discovery and setup:
- `mkdir -p ~/.nimble/memory/{reports,healthcare-providers-verify/checkpoints}`
- `ls ~/.nimble/memory/healthcare-providers-verify/checkpoints/ 2>/dev/null`
- Run Layer 1 (vertical) and Layer 3 (general tools) WSA discovery from
  `references/wsa-reference.md`. Layer 2 (session-specific) runs after Step 1 when
  you know the user's specialty and verification focus.

Classify discovered agents into verification categories and validate with
`nimble agent get` per `references/wsa-reference.md`.

From the preflight results:
- CLI missing or API key unset -> `references/profile-and-onboarding.md`, stop
- Profile exists -> note it for context. Determine mode using smart date windowing
  from `references/nimble-playbook.md`:
  - **Full mode:** first run OR last run > 14 days ago
  - **Quick refresh:** last run < 14 days ago (re-verify only previously
    Unverified/Flagged practitioners)
  - **Same-day repeat:** if `last_runs.healthcare-providers-verify` is today, check
    for existing report at `~/.nimble/memory/reports/healthcare-providers-verify-*[today].md`.
    If found, ask: "Already ran today. Run again for fresh data?"
- No profile -> that's fine. This skill doesn't require onboarding. Proceed to Step 1.

### Step 1: Parse Input + Starting Questions

**Chained-from-sibling shortcut:** Check for same-day extract or enrich output:
```bash
ls ~/.nimble/memory/reports/healthcare-providers-extract-*$(date +%Y-%m-%d).md 2>/dev/null
ls ~/.nimble/memory/reports/healthcare-providers-enrich-*$(date +%Y-%m-%d).md 2>/dev/null
```
If a same-day report exists, parse the `{slug}` and load the provider data
(`providers.json` or `enriched.json`). This gives you names, credentials, specialties,
and locations — skip parsing and go directly to Step 2.

Parse `$ARGUMENTS` for input type using the Input Parsing Pattern from
`references/nimble-playbook.md`. Key routing:
- **Sibling output detected** (providers.json/enriched.json) -> proceed to Step 2
- **CSV/Sheet/pasted data detected** -> proceed to Step 2
- **Unclear** -> ask (counts as 1 of max 2 prompts)

**If input is clear**, confirm and ask one shaping question (plain text, not
AskUserQuestion):

> "Found **N practitioners** to verify. Quick questions:
> 1. What should I verify? (credentials, specialty, active status, practice address — or all)
> 2. Healthcare vertical? (ophthalmology, dental, dermatology, general, or other)"

**If input is ambiguous**, use AskUserQuestion (counts as 1 of max 2 prompts):

> **What practitioner data should I verify?**
> - Paste provider data directly (name + credentials + location, one per line)
> - Provide a CSV file path or Google Sheet URL
> - Or describe what you have (e.g., "a list of 50 ophthalmologists I need to
>   verify against the NPI registry")

Skip questions the user already answered in their initial message.

### Step 2: Analyze Input Data

Parse the input into structured records. For each practitioner, identify:
- **Claimed fields** — name, credentials, specialty, state/city, practice name
- **Verification targets** — which claims to check based on user's focus

**Minimum required fields:** Name + at least one of (credentials, state, specialty).
If a practitioner has only a name with no other identifiers, flag it:
"Cannot verify [name] — need at least a state, credential, or specialty to search."

Build a verification plan summary:

> "Analyzing **N practitioners** for verification:
> - Names: N/N present
> - Credentials claimed: N/N
> - Specialty claimed: N/N
> - State/location: N/N
>
> Starting NPI verification..."

Run Layer 2 WSA discovery now that you know the specialty:
```bash
nimble agent list --limit 50 --search "[specialty]"
nimble agent list --limit 50 --search "[registry-user-mentioned]"
```

See `references/wsa-reference.md` for session-specific discovery.

### Step 3: NPI Registry Lookup

**Prefer the NPPES API** — it returns structured JSON in one call instead of
search + extract (two calls). Build the query URL from the practitioner's fields:

```bash
nimble extract --url "https://npiregistry.cms.hhs.gov/api/?version=2.1&first_name=[First]&last_name=[Last]&state=[ST]&limit=5" --format markdown
```

Add `&taxonomy_description=[Specialty]` if the specialty is known and specific
enough. The API returns NPI number, status, credentials, taxonomy codes, addresses,
and enumeration dates — everything needed for verification in a single call.

**Fallback to web search** if the NPPES API returns zero results or errors:

```bash
nimble search --query "[Name] [Credential] [State] NPI registry" --max-results 5 --search-depth lite
```

Then extract the top result from an NPI source (see source priority below).

**Source priority (enforce in sub-agent prompts):**
1. NPPES API (`npiregistry.cms.hhs.gov/api/`) — preferred, structured JSON
2. `npidb.org/doctors/` — clean structured data, good fallback
3. `nppes.cms.hhs.gov` (provider-view pages) — official CMS source
4. Skip all others (healthline, hmedata, vitals, etc.) — inconsistent formatting

Tell sub-agents: "Only extract from NPPES API, npidb.org, or nppes.cms.hhs.gov.
Ignore other NPI aggregator sites."

**Search budget per provider:** Max 3 search queries + 1 extraction per
practitioner. If no NPI match after 3 attempts, mark as Unverified and move on.
Tell sub-agents: "Do not run more than 4 nimble commands per provider. Mark as
Unverified if no match by then."

For 10+ practitioners, use sub-agents (see Sub-Agent Strategy below).

**Key fields from NPI records** — see `references/npi-verification-patterns.md`
for the full list: NPI number, status, credentials, taxonomy/specialty,
enumeration date, last updated, practice address.

**Checkpoint enforcement:** After each sub-agent returns its batch results, the
main context MUST write the checkpoint before spawning the next step or presenting
results:
1. Receive sub-agent results
2. Write checkpoint: `echo '[results]' > ~/.nimble/memory/healthcare-providers-verify/checkpoints/{slug}/batch-{n}.json`
3. Continue to next step

Do NOT skip this — if the run fails between steps, the user loses all progress.

### Step 4: Cross-Reference and Verify

For each practitioner, compare claimed data against extracted NPI data. Follow the
verification logic in `references/npi-verification-patterns.md`:

1. **Name matching** — normalize both names and determine match level (Strong,
   Likely, Weak, No Match) per the name matching rules in the reference
2. **Credential matching** — compare claimed credentials against NPI record
3. **Specialty matching** — compare claimed specialty against NPI taxonomy using
   the taxonomy matching strategy in the reference
4. **Address matching** — compare claimed state/city against NPI practice address
5. **Status check** — verify NPI status is Active

**Assign verification status** per practitioner based on the totality of evidence:
- **Verified** — all claims match NPI record
- **Partially Verified** — NPI found, minor discrepancies
- **Unverified** — no NPI match found or unable to disambiguate
- **Flagged** — active mismatches requiring human review

See `references/npi-verification-patterns.md` for the detailed criteria for each
status and the mismatch severity levels (Critical vs Warning).

### Step 5: WSA Supplementary Verification (Optional)

If the user requested regulatory verification beyond NPI lookup, or if Step 5
left practitioners as Unverified that might benefit from additional sources:

Run verification-phase WSAs discovered in Step 0. See `references/wsa-reference.md`
for the verification phase mapping, agent evaluation, and fallback chains.

**Practice confirmation:** For Unverified practitioners, try confirming their
practice exists via practice-level WSAs or web search:
```bash
nimble search --query "[practice-name] [city] [state]" --max-results 5 --search-depth lite
```

**Regulatory verification:** For practitioners the user wants regulatory checks on:
```bash
nimble search --query "[name] [credentials] clinical trials OR FDA OR board certification" --max-results 5 --search-depth lite
```

### Step 6: Deduplication & Confidence Scoring

Follow the Entity Deduplication pattern from `references/nimble-playbook.md`.
Skill-specific dedup rules are in `references/provider-extraction-patterns.md`.

**NPI dedup check:** After all sub-agents return, scan for duplicate NPI numbers
across batches. If two different providers mapped to the same NPI, flag both as
"Flagged — possible NPI collision, requires human review." This catches data entry
errors and name confusion in the source provider list.

**Verification-specific scoring:** The verification status (Verified / Partially
Verified / Unverified / Flagged) replaces confidence scoring for this skill.
Each status includes a confidence qualifier:
- **High confidence** — 2+ NPI sources corroborate, strong name match
- **Medium confidence** — single NPI source, likely name match
- **Low confidence** — weak name match, partial field matches

### Step 7: Output

Present results as a verification report — showing status per practitioner with
specific mismatch details. Group by verification status, include a "What This
Means" section at the end.

```markdown
# Provider Verification: [N] Practitioners Checked
*[Date] | [V] Verified, [PV] Partially Verified, [U] Unverified, [F] Flagged*

## TL;DR
Verified [V] of [T] practitioners against the NPI registry. [F] flagged for
review: [brief description of critical issues]. [U] could not be verified —
[common reason].

## Verification Results

| # | Name | Claimed | NPI Status | Verification | Issues | Source |
|---|------|---------|------------|-------------|--------|--------|
| 1 | Dr. Jane Smith | MD, Retinal Surgery, TX | Active (NPI 1234567890) | Verified | — | [NPI](url) |
| 2 | Dr. John Doe | OD, Ophthalmology, CA | Active (NPI 0987654321) | Partially Verified | Subspecialty differs | [NPI](url) |
| 3 | Dr. Alex Chen | MD, Dentistry, NY | Not Found | Unverified | No NPI match | [NPPES query](api-url) |
| 4 | Dr. Pat Lee | DO, Cardiology, FL | Deactivated | Flagged | NPI deactivated 2024-01 | [NPI](url) |

## Flagged Practitioners (Requires Human Review)

### Dr. Pat Lee
**Claimed:** DO, Cardiology, FL
**NPI Record:** NPI 1122334455 — **Deactivated** (01/15/2024)
**Issues:**
- CRITICAL: NPI status is Deactivated since January 2024
- Credential matches (DO confirmed)
- Specialty matches (Cardiovascular Disease taxonomy)
**Source:** [NPI Record](url)
**Action needed:** Confirm if provider has re-registered or if this is a
different individual.

[Repeat per flagged practitioner]

## Unverified Practitioners

[List practitioners where no NPI match was found, with search queries attempted]

## Verification Summary
- **Verified:** [V] practitioners — all claims confirmed
- **Partially Verified:** [PV] — minor discrepancies noted
- **Unverified:** [U] — no NPI match (common names, missing identifiers)
- **Flagged:** [F] — critical issues requiring review

## Sources
[Clickable URL for every NPI lookup page used, grouped by practitioner]

## What This Means
[Actionable interpretation: which practitioners are safe to include in your
directory, which need follow-up, what the verification rate tells you about
your data quality. Suggest next steps for unverified/flagged records.]
```

**Source links are mandatory.** Every verification finding must trace back to a
source URL.

### Step 8: Save to Memory

Make all Write calls simultaneously:

- Report -> `~/.nimble/memory/reports/healthcare-providers-verify-{slug}-{date}.md`
- Verification data -> `~/.nimble/memory/healthcare-providers-verify/{slug}/verified.json`
- Profile -> update `last_runs.healthcare-providers-verify` in
  `~/.nimble/business-profile.json` (only if profile exists)
- Follow the wiki update pattern from `references/memory-and-distribution.md`: update
  `index.md` rows for all affected entity files, append a `log.md` entry for this run.
- Clean up checkpoint (complete run) or keep (partial run)

**Update sibling artifacts:** If `providers.json` or `enriched.json` exists for this
slug under `~/.nimble/memory/`, merge NPI numbers and verification status into those
files. Generate a verified CSV export at
`~/.nimble/memory/healthcare-providers-verify/{slug}/verified-{date}.csv` with all
verification columns (NPI, NPI Status, NPI Taxonomy, Verification Status). Offer
this export path in Step 9 so the user can copy it where needed.

### Step 9: Share, Distribute & Follow-ups

**Always offer distribution — do not skip.** Follow
`references/memory-and-distribution.md` for connector detection and sharing flow.

Notion: full verification report as a dated subpage.
Slack: TL;DR with verification counts and flagged items only.

**Follow-ups:**

- **"Tell me more about Dr. X"** -> show full verification detail
- **"Export as CSV"** -> generate CSV with verification statuses
- **"Re-verify flagged only"** -> re-run NPI search for Flagged/Unverified only
- **"What should I do about the flagged ones?"** -> actionable next steps per issue

**Sibling skill suggestions:**

> **Next steps:**
> - Run `healthcare-providers-extract` on unverified providers' practice URLs
>   to get fresh data
> - Run `healthcare-providers-enrich` to fill gaps in verified providers' records
> - Run `market-finder` to find additional practices in this area

---

## Sub-Agent Strategy

For batch verification (10+ practitioners), use `nimble-researcher` agents
(`agents/nimble-researcher.md`) to parallelize NPI lookups and extraction.

Follow the sub-agent spawning rules from `references/nimble-playbook.md`
(bypassPermissions, batch max 4, explicit Bash instruction, fallback on failure).

**Spawn pattern:** One agent per batch of 5 practitioners. Each agent runs Steps 3-4
for its assigned practitioners and returns verification records. Tell each agent to
use `nimble extract-batch` for its NPI result URLs where possible — one batch call
per agent is faster than sequential calls.

**Small batch optimization:** If fewer than 10 practitioners, run directly from the
main context instead of spawning agents.

**Fallback:** If any agent fails, run those verifications directly from the main
context. Never leave gaps in the output.

---

## Error Handling

See `references/nimble-playbook.md` for the standard error table (missing API key,
429, 401, empty results, extraction garbage). Skill-specific errors:

- **No NPI results for practitioner:** "Couldn't find an NPI record for [name] in
  [state]. The name may be too common, or the provider may practice under a
  different name. Want me to try with additional context (practice name, NPI number)?"
- **Multiple NPI matches:** "Found multiple NPI records for [name] in [state].
  Can you confirm which one? [list top 3 with NPI numbers and specialties]"
- **NPI page extraction returned garbage:** "The NPI lookup page appears to be
  JavaScript-rendered. Retrying with browser rendering..." (auto-retry with
  `--render` per the shared pattern)
- **CSV/Sheet parse error:** "Couldn't parse the input file. Expected columns with
  practitioner names and at least one identifier (state, specialty, or credentials).
  Can you paste the data directly instead?"
- **Insufficient data for verification:** "Cannot verify [N] practitioners — they
  have only a name with no state, credential, or specialty. Add identifiers or
  remove them from the list."
