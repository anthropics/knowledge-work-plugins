# NPI Verification Patterns

How to look up, interpret, and match NPI registry data against claimed practitioner
credentials. For credential regex and specialty keywords, see
`provider-extraction-patterns.md`. For general CLI patterns, see `nimble-playbook.md`.

---

## NPI Lookup Strategy

The NPI (National Provider Identifier) is the authoritative source for verifying
that a healthcare practitioner is registered, active, and practicing with the
credentials they claim. Every individual healthcare provider in the US has a unique
10-digit NPI number.

### Primary approach: NPPES API (1 call per provider)

The NPPES has a public API that returns structured JSON directly. This is faster
and more reliable than search + extract (2 calls). Build the query URL:

```bash
nimble extract --url "https://npiregistry.cms.hhs.gov/api/?version=2.1&first_name=[First]&last_name=[Last]&state=[ST]&limit=5" --format markdown
```

Add `&taxonomy_description=[Specialty]` if the specialty is known. The response
contains `results[]` with NPI number, status, credentials, taxonomy codes,
addresses, and enumeration dates.

**Parse the JSON response:** The API returns escaped JSON in the markdown field.
Parse it to extract the fields below. Match the correct result by comparing
`basic.first_name`, `basic.last_name`, and `taxonomies[].desc` against claimed data.

### Fallback approach: web search + extract (2 calls per provider)

If the NPPES API returns zero results or errors, fall back to web search:

```bash
nimble search --query "[Name] [Credential] [State] NPI registry" --max-results 5 --search-depth lite
```

Then extract from the top NPI source result:

```bash
nimble extract --url "[npi-result-url]" --format markdown
```

**Source priority:**
1. `npidb.org/doctors/` — clean structured data
2. `nppes.cms.hhs.gov` (provider-view pages) — official CMS source
3. Skip all others (healthline, hmedata, vitals, etc.) — inconsistent formatting

**Search refinement (if first search returns too many or zero results):**
- Too many results (common names) — add specialty:
  `"[Name] [Specialty] [City] [State] NPI"`
- No results — try without credentials:
  `"[Name] [State] NPI provider"`
- Still no results — try with practice name:
  `"[Name] [Practice Name] NPI"`

### Search budget

Max **3 search queries + 1 extraction** per practitioner. If no NPI match after
3 attempts, mark as Unverified and move on. The user can provide more context
later for unresolved providers. This prevents runaway agents from burning 10+
calls on a single ambiguous name.

### Key fields from NPI records
- **NPI Number** — 10-digit identifier
- **Entity Type** — Type 1 (individual) vs Type 2 (organization)
- **Provider Name** — legal name on record
- **Credential** — credential designation (MD, DO, OD, etc.)
- **Taxonomy Code + Description** — maps to specialty (see Taxonomy Matching below)
- **Enumeration Date** — when the NPI was first assigned
- **Last Updated** — most recent update to the record
- **Status** — Active or Deactivated (with deactivation date if applicable)
- **Practice Address** — primary practice location on file
- **Mailing Address** — may differ from practice address

---

## Taxonomy Matching

NPI records use Healthcare Provider Taxonomy Codes to classify specialties.
These are standardized codes maintained by the National Uniform Claim Committee (NUCC).
Rather than maintaining a static lookup table, use the taxonomy description from the
NPI record to match against the user's claimed specialty.

### Matching strategy

1. **Extract the taxonomy description** from the NPI record (e.g.,
   "Ophthalmology", "Optometrist", "Dentist - General Practice")
2. **Normalize both** the claimed specialty and NPI taxonomy description:
   lowercase, strip punctuation, expand abbreviations
3. **Match levels:**
   - **Exact** — normalized strings match or one contains the other
   - **Partial** — same broad category (e.g., claimed "retina specialist" vs
     NPI taxonomy "Ophthalmology" — same field, subspecialty detail differs)
   - **Mismatch** — different categories entirely (e.g., claimed "ophthalmologist"
     vs NPI taxonomy "Dentist")

### Common taxonomy categories by vertical

Use these to validate broad category matches when exact descriptions differ:

**Ophthalmology family:**
Ophthalmology, Retina Specialist, Cornea Specialist, Glaucoma Specialist,
Oculoplastics, Neuro-Ophthalmology, Pediatric Ophthalmology, Optometrist

**Dental family:**
General Dentistry, Orthodontics, Periodontics, Endodontics, Oral Surgery,
Prosthodontics, Pediatric Dentistry

**Primary Care family:**
Family Medicine, Internal Medicine, General Practice, Geriatric Medicine,
Preventive Medicine

**The test for taxonomy matching:** A "Partial" match within the same family is
acceptable — flag it as a note, not an error. A mismatch across families is a
verification failure that requires human review.

---

## Verification Status Determination

For each practitioner, assign one of four verification statuses based on the
totality of evidence:

### Verified
All of the following are true:
- NPI record found and status is Active
- Name matches (after normalization — see name matching below)
- Credential matches (claimed credential appears on NPI record)
- Specialty matches (Exact or Partial taxonomy match)
- Practice address is in the claimed state (if state was provided)

### Partially Verified
NPI record found but with minor discrepancies:
- Name matches but credential not listed on NPI (may use different designation)
- Specialty is a Partial match (same family, different subspecialty)
- Address is in a different city but same state
- NPI is active but hasn't been updated in 5+ years

### Unverified
Cannot confirm the practitioner's claims:
- No NPI record found for this name + state combination
- Multiple NPI matches, insufficient data to disambiguate
- NPI record found but name similarity is too low (possible different person)

### Flagged
Active discrepancies that require human review:
- NPI record exists but status is **Deactivated** (include deactivation date)
- Credential **mismatch** — claimed MD but NPI shows DO, or vice versa
- Specialty **mismatch** across families (claimed ophthalmologist, NPI says dentist)
- Address mismatch — claimed state differs from NPI practice state
- Name match is borderline (could be same person with name change, or different person)

### Recent Relocators

If the NPI address is in a different state but the provider's practice website
shows a recent join date (< 6 months), classify as **Verified with note** rather
than Partially Verified or Flagged. NPI address updates typically lag 3-6 months
after a provider changes practice locations. Note the discrepancy but don't
downgrade the verification status. Look for these signals:
- Practice website bio says "joined [practice] in [recent year]"
- Provider appears on the new practice's team page but NPI shows prior state
- LinkedIn or other sources confirm the relocation

---

## Name Matching

NPI records use legal names which may differ from how providers present themselves
on practice websites.

### Normalization steps (apply to both claimed name and NPI name)
1. Strip titles: Dr., Mr., Ms., Prof.
2. Strip credentials: all patterns from `provider-extraction-patterns.md`
3. Strip suffixes: Jr., Sr., III, IV
4. Lowercase everything
5. Collapse whitespace, strip remaining punctuation

### Match levels
- **Strong match** — normalized first + last name match exactly
- **Likely match** — last name matches, first name is a known variant
  (e.g., "William" / "Bill", "Robert" / "Bob", "James" / "Jim")
- **Weak match** — last name matches, first name differs (possible name change,
  or different person — flag for review)
- **No match** — last names differ after normalization

### Common name variant pairs
Rather than hardcoding a complete list, look for these patterns:
- Formal vs informal (William/Bill, Robert/Bob, James/Jim, Elizabeth/Beth)
- Hyphenated vs maiden name (provider may use married or maiden name differently
  across sources)
- Middle name as first name (some providers go by their middle name)

When a name is a "Weak match" or "No match" but other fields strongly match
(same specialty, same city, same practice name), upgrade to "Likely match" and
note the discrepancy rather than marking as Unverified.

---

## Mismatch Flagging

Every flagged mismatch must include:
1. **What was claimed** — the value from the user's input
2. **What was found** — the value from the NPI record
3. **Source URL** — clickable link to the NPI lookup page
4. **Severity** — Critical (deactivated NPI, credential mismatch) or
   Warning (address mismatch, stale record, name variant)

### Critical mismatches (always flag)
- Deactivated NPI status
- Credential type mismatch (MD claimed, DO found — or vice versa)
- Specialty mismatch across taxonomy families
- Entity type mismatch (individual claimed, organization NPI found)

### Warning mismatches (flag as notes)
- Address in different city but same state
- Subspecialty mismatch within same taxonomy family
- NPI record not updated in 5+ years (stale but not necessarily wrong)
- Name variant (informal vs formal name)

---

## Batch Verification Optimization

For large lists (20+ practitioners), optimize the search strategy:

### Group by state
Practitioners in the same state often appear in the same NPI lookup results.
Group searches by state to improve cache hits and reduce redundant searches.

### Prioritize by risk
If the user specified a verification focus (e.g., "check credentials only"),
optimize the pipeline:
- **Credentials only** — NPI lookup + credential match, skip address verification
- **Active status only** — NPI lookup + status check, skip taxonomy matching
- **Full verification** — all checks (default)

### Checkpoint strategy
Save verification progress after every 10 practitioners:
```bash
echo '{...}' > ~/.nimble/memory/healthcare-providers-verify/checkpoints/{slug}/verify.json
```
This allows resuming interrupted verification runs without re-searching already-verified practitioners.
