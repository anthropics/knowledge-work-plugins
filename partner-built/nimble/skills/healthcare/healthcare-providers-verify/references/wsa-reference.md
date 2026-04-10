# WSA Discovery for Healthcare Providers Verify

How to find and evaluate WSAs for validating practitioner credentials and license
status. The WSA catalog evolves constantly — this skill discovers relevant agents at
runtime rather than relying on a static list.

For general WSA execution rules (invocation, parsing, batch, fallback), see
`nimble-playbook.md`.

---

## Discovery Strategy

### Three search layers

Run these searches during preflight (Step 0) to build a session-specific WSA
inventory. Run all searches simultaneously:

**Layer 1 — Vertical search:**
```bash
nimble agent list --limit 100 --search "healthcare"
```
Returns all agents tagged with the Healthcare vertical (clinical trials, FDA,
regulatory, licensing, and any newly added healthcare agents).

**Layer 2 — Session-specific search:**
Search for terms derived from the user's input — their specialty, specific
registries, or data sources they mentioned:
```bash
# Registry and licensing searches:
nimble agent list --limit 50 --search "npi"
nimble agent list --limit 50 --search "license"
nimble agent list --limit 50 --search "board certification"

# If user mentioned specific registries:
nimble agent list --limit 50 --search "medical board"
nimble agent list --limit 50 --search "[state] license lookup"

# Specialty-specific:
nimble agent list --limit 50 --search "[user's specialty]"
```
Adapt search terms to whatever the user provided. Focus on regulatory and
verification-related agents.

**Layer 3 — General verification tools:**
These WSAs are useful across verticals for identity confirmation and practice
verification:
```bash
nimble agent list --limit 50 --search "google_maps"
nimble agent list --limit 50 --search "yelp"
nimble agent list --limit 50 --search "bbb"
```

### Evaluating discovered agents

For each discovered agent, read its `description` and `entity_type` to classify it
into a verification category:

| If the agent description mentions... | Assign to category |
|--------------------------------------|-------------------|
| NPI, license, credential, certification, registry | **Credential verification** — direct credential checks |
| Clinical trials, FDA, regulatory, compliance | **Regulatory verification** — regulatory activity confirmation |
| Reviews, ratings, patient feedback, active practice | **Practice confirmation** — confirms provider is actively practicing |
| Profile, directory, listing, search | **Identity confirmation** — confirms provider identity and web presence |

Validate each relevant agent's params before using it:
```bash
nimble agent get --template-name [agent_name]
```

**Skip agents that don't fit** — not every healthcare-tagged agent is useful for
verification. A drug interaction agent or a clinical trial search agent adds no
value to credential validation.

---

## Verification Phase Mapping

This skill has a narrower WSA focus than extract or enrich — the primary tool is
`nimble search` + `nimble extract` for NPI lookups. WSAs add value in two areas:

### Credential verification

**When:** Always — this is the core value of the skill.

**Primary tool:** `nimble search` + `nimble extract` (not WSA-dependent):
```bash
nimble search --query "[name] [credential] [state] NPI registry" --max-results 5 --search-depth lite
```
Then extract the NPI result page for structured data.

**WSA supplement:** If Layer 1/2 discovery found NPI or medical board agents, use
them for direct lookups — structured WSA output is higher quality than parsing
search results.

### Regulatory verification

**When:** User wants to confirm clinical trial activity, FDA associations, or
regulatory compliance beyond basic NPI lookup.

**Search terms for discovery:** `healthcare` vertical, `clinicaltrials`, `fda`,
`board`, `license`

**How to use:** Run discovered regulatory agents with the provider's name and
credentials. Cross-reference with NPI data to build a fuller verification picture.

**Fallback:**
```bash
nimble search --query "[provider-name] [credentials] clinical trials OR FDA OR board certification" --max-results 5 --search-depth lite
```

### Practice confirmation

**When:** Need to confirm a provider is actively practicing at a claimed location.

**Search terms for discovery:** `google_maps`, `yelp`, `bbb`

**How to use:** Run practice-level agents with the provider's practice name +
location. Confirm the practice exists and is active.

**Fallback:**
```bash
nimble search --query "[practice-name] [city] [state]" --max-results 5 --search-depth lite
```

---

## Scaling WSA Calls

Follow the Scaled Execution pattern from `nimble-playbook.md` — it covers
individual calls, batching, and the confirmation gate for large jobs.

For verification, the primary bottleneck is NPI lookups (one per practitioner).
WSA calls add supplementary verification and scale as:
`[practitioners requesting regulatory/practice verification] x [relevant WSA categories]`.

---

## Fallback Chain

If WSA discovery returns nothing useful for a category, fall back to `nimble search`
+ `nimble extract` (the core Nimble tools always work):

1. **Credential fallback:** `nimble search --query "[name] [state] NPI" --max-results 5 --search-depth lite` + extract NPI result
2. **Regulatory fallback:** `nimble search --query "[name] [credentials] clinical trials OR FDA" --max-results 5 --search-depth lite`
3. **Practice fallback:** `nimble search --query "[practice-name] [city] [state] reviews" --max-results 5 --search-depth lite`

The skill always produces verification results even if zero WSAs are found — WSAs
accelerate and enrich the verification, but NPI lookup via web search is the
foundation and never requires WSAs.
