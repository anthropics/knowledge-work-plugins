---
name: Intelligent Lookup Wizard
description: "Master fuzzy matching and intelligent lookup configuration for data harmonization and record matching. Use this when you need to match company names across sources, reconcile customer addresses, match product descriptions, deduplicate data, or harmonize master data from multiple systems. Essential for data quality improvement, MDM implementation, and data integration workflows."
---

# Intelligent Lookup Wizard Skill

## Overview

The Intelligent Lookup Wizard guides you through creating intelligent lookups in SAP Datasphere. Intelligent lookups use fuzzy matching algorithms to find similar records across datasets, enabling data harmonization, deduplication, and master data management without requiring exact matches.

## What Are Intelligent Lookups?

### Definition
An intelligent lookup is a data matching tool that:
- Compares text values using fuzzy matching algorithms
- Finds similar records across two datasets (input and lookup entities)
- Assigns match scores indicating confidence level
- Enables data enrichment, harmonization, and deduplication
- Includes review workflow for manual confirmation of matches

### When to Use Intelligent Lookups

**Use intelligent lookups for:**
- **Company name matching** — "ACME Corp", "Acme Corporation", "ACME Inc" → Match
- **Address reconciliation** — Handling abbreviations, spelling variations, format differences
- **Product description matching** — "Widget Pro" vs "Professional Widget" → Same product
- **Customer deduplication** — Finding duplicate customer records within dataset
- **Master data harmonization** — Matching vendor IDs across multiple procurement systems
- **Data quality improvement** — Identifying and merging incomplete/duplicate records
- **Cross-system reconciliation** — Matching accounts between ERP and CRM systems

**DO NOT use intelligent lookups for:**
- Exact match lookups (use standard SQL join)
- Numeric lookups (use hash or checksum matching)
- High-speed real-time lookups (use reference tables/caches)
- Data that must match perfectly (use data quality tools instead)

### When Intelligent Lookups Add Value

```
Scenario 1: Company Name Matching
Input data has: "ACME Corporations Inc"
Lookup table has: "Acme Corp"
Standard lookup: NO MATCH ✗
Intelligent lookup: MATCH ✓ (score: 0.92)

Scenario 2: Product Matching
Input: "Professional Grade Widget with Advanced Features"
Lookup: "Widget Pro - Advanced"
Standard lookup: NO MATCH ✗
Intelligent lookup: MATCH ✓ (score: 0.85)

Scenario 3: Address Matching
Input: "123 Main St, New York, NY 10001"
Lookup: "123 Main Street, New York, New York 10001"
Standard lookup: NO MATCH ✗
Intelligent lookup: MATCH ✓ (score: 0.95)
```

## Use Cases by Industry

### Finance and Procurement
- **Vendor deduplication:** Find duplicate vendor records from multiple divisions
- **Invoice matching:** Reconcile invoices with PO line items despite data entry variations
- **Bank account reconciliation:** Match transactions across GL accounts with slight format variations
- **Payment matching:** Find matching payment records in different systems

### Sales and CRM
- **Customer deduplication:** Identify duplicate customer records from different sources
- **Account consolidation:** Merge similar account names from prospect databases
- **Contact matching:** Harmonize contact information across sales regions
- **Lead matching:** Identify duplicate leads across marketing automation systems

### Supply Chain
- **Supplier matching:** Match supplier names across procurement systems
- **Product catalogue harmonization:** Link products with similar descriptions across brands
- **Site/location matching:** Find duplicate warehouse/store locations by address
- **SKU matching:** Match products by description when SKU numbers differ

### Healthcare
- **Patient matching:** Identify patient records with slight name/date variations
- **Provider matching:** Link healthcare providers by practice name and address
- **Drug matching:** Match pharmaceutical products by description and strength
- **Facility matching:** Identify duplicate hospital/clinic locations

### Retail
- **Store location matching:** Find duplicate store records by address and postal code
- **Product matching:** Link products across multiple vendor systems by description
- **Customer matching:** Identify duplicate customer loyalty accounts
- **Price matching:** Find comparable products for price comparison

## Setting Up an Intelligent Lookup

### Step 1: Define Input Entity

The input entity is the dataset containing values you want to match.

**Input entity selection criteria:**
- Should contain the "new" or "dirty" data that needs matching
- Columns must include text fields for matching (company names, addresses, descriptions)
- Can be a view, table, or query result
- May have multiple rows to match (matching many-to-one or many-to-many)

**Input entity example (Vendor Data to Harmonize):**
```
VendorInputID | VendorName              | Address                  | City      | State | ZIP
1             | ACME Corporation Inc    | 123 Main Street         | New York  | NY    | 10001
2             | Acme Corp              | 123 Main St             | NY        | NY    | 10001
3             | ACME Inc               | 123 Main Str            | NewYork   | NY    | 10001
4             | Best Widgets LLC       | 456 Oak Avenue          | Boston    | MA    | 02101
5             | Best Widget Industries | 456 Oak Ave             | Boston    | MA    | 02101
```

**Prepare input data:**
1. Remove leading/trailing whitespace
2. Standardize case (upper, lower, or title)
3. Remove special characters if not meaningful
4. Verify data completeness in key matching columns
5. Use `search_catalog` to locate input tables

### Step 2: Define Lookup Entity

The lookup entity is the reference dataset containing "correct" or master values.

**Lookup entity selection criteria:**
- Should be authoritative source of truth (master data)
- Contains the target values you want to match to
- Can be smaller than input (for efficiency)
- Should have unique key identifier for lookup results
- May contain additional attributes for enrichment

**Lookup entity example (Vendor Master):**
```
VendorID | VendorMasterName      | Address            | City     | State | ZIP    | VendorStatus
V-001    | Acme Corporation      | 123 Main Street   | New York | NY    | 10001  | Active
V-002    | Best Widgets Co.      | 456 Oak Avenue    | Boston   | MA    | 02101  | Active
V-003    | Global Supply Inc     | 789 Pine Road     | Chicago  | IL    | 60601  | Active
V-004    | Premier Components    | 321 Elm Street    | Denver   | CO    | 80202  | Inactive
```

**Lookup data quality considerations:**
- Master data should be clean and standardized
- Remove duplicates in lookup entity first
- Ensure key columns have no nulls
- Verify foreign key consistency
- Use `get_table_schema` to understand lookup structure

### Step 3: Select Matching Columns

Choose which columns from input and lookup entities to compare.

**Column selection strategy:**
- **Primary column:** Most important for matching (company name, main address)
- **Secondary columns:** Support matching logic (city, state, postal code)
- **Avoid noise:** Don't include columns that vary naturally (phone, email, website)

**Single column matching (Simple):**
```
Input Column: CompanyName
Lookup Column: VendorMasterName
Matching Strategy: Fuzzy text match
Example:
- "ACME Corp Inc" → Match to "Acme Corporation"
```

**Multi-column matching (Stronger):**
```
Column 1 (Weight: 60%):
Input: CompanyName
Lookup: VendorMasterName

Column 2 (Weight: 30%):
Input: City
Lookup: City

Column 3 (Weight: 10%):
Input: PostalCode
Lookup: ZIP

Scoring: Weighted combination of individual column scores
```

**Column preparation:**
- Standardize text case before matching
- Remove special characters (punctuation, symbols)
- Trim whitespace
- Expand abbreviations if possible (St → Street, Inc → Incorporated)
- Use `analyze_column_distribution` to understand data patterns

### Step 4: Configure Matching Strategies

Choose matching algorithms appropriate for your data.

**Matching strategy options:**

#### Exact Matching
**When to use:** When matches must be perfect but case-insensitive

**Algorithm:** Character-by-character comparison after normalization

**Configuration:**
```
Strategy: Exact (Case-Insensitive)
Normalization:
├── Convert to uppercase
├── Trim whitespace
├── Remove punctuation (optional)
└── Handle accents (ä → a)

Example:
Input: "acme corp."
Lookup: "ACME CORP"
Result: MATCH ✓
```

**Use case:** SKU matching, postal code matching, account numbers

#### Fuzzy Text Matching
**When to use:** When input data has typos, abbreviations, or minor variations

**Algorithm:** Levenshtein distance, Jaro-Winkler, or Soundex-based matching

**Configuration:**
```
Strategy: Fuzzy (Token-based)
Algorithm: Jaro-Winkler
Threshold: 0.85 (matches scoring 0.85+ are considered matches)

Example Matches (Score shown):
"ACME Corp" vs "Acme Corporation" = 0.89 ✓
"Smith Company" vs "Smyth Co" = 0.82 ✗ (below threshold)
"John Smith" vs "Jon Smyth" = 0.87 ✓
```

**Use case:** Company names, person names, product descriptions

#### Phonetic Matching
**When to use:** When spelling variations sound similar

**Algorithm:** Soundex, Metaphone, or Double Metaphone encoding

**Configuration:**
```
Strategy: Phonetic
Algorithm: Metaphone
Process:
├── Convert both strings to phonetic codes
├── Compare phonetic codes
└── Score based on code similarity

Example Matches:
"Smith" Metaphone: SM0
"Smyth" Metaphone: SM0
Result: MATCH ✓ (sounds identical)

"Catherine" Metaphone: K0RN
"Katherine" Metaphone: K0RN
Result: MATCH ✓
```

**Use case:** Person names, location names with spelling variations

#### Token-Based Matching
**When to use:** When columns contain multiple words/tokens that can be in different order

**Algorithm:** Break text into tokens; compare token sets

**Configuration:**
```
Strategy: Token-Based
Process:
├── Split text into words: "123 Main Street" → [123, Main, Street]
├── Match tokens between input and lookup
├── Score based on percentage of matching tokens
└── Consider token order (optional)

Example Matches:
"New York City" vs "City of New York" = 0.87 ✓
"Smith John" vs "John Smith" = 1.0 ✓ (all tokens match)
"Acme Inc" vs "Acme International" = 0.67 (2 of 3 tokens match)
```

**Use case:** Address matching, product names, company names with variable word order

#### Composite/Hybrid Matching
**When to use:** When combining multiple matching strategies for best results

**Configuration:**
```
Rule 1: Try exact match first (fastest)
├── If found: Return match immediately
└── If not found: Continue to Rule 2

Rule 2: Try phonetic match (for name variations)
├── If found with score > 0.90: Return match
└── If not found: Continue to Rule 3

Rule 3: Try fuzzy text match (for typos/abbreviations)
├── If found with score > 0.85: Return match
└── If not found: No match

Example:
"John Smyth" → Try exact (no match)
           → Try phonetic (match with Smith)
           → Return match
```

**Use case:** High-precision matching scenarios

## Matching Strategies Deep Dive

### Levenshtein Distance (Edit Distance)

**What it measures:** Minimum number of single-character edits needed to transform one string to another.

**Edits allowed:** Insert, delete, replace character

**Example calculation:**
```
String 1: "ACME"
String 2: "ACE"
Edits: Delete 'M' = 1 edit
Distance: 1

String 1: "kitten"
String 2: "sitting"
Edits:
1. k → s: "sitten"
2. e → i: "sittin"
3. Insert g: "sitting"
Distance: 3
```

**Normalized score (0-1):**
```
Similarity = 1 - (Distance / Max_Length)

Example: "Smith" vs "Smyth"
Distance: 1 (replace i with y)
Max Length: 5
Similarity: 1 - (1/5) = 0.80

Threshold typically: 0.80+ for match
```

### Jaro-Winkler Distance

**What it measures:** Similarity based on matching characters and their order, with bonus for matching prefix.

**Characteristics:**
- Ranges from 0 (no match) to 1.0 (perfect match)
- Rewards matching characters in same position
- Gives bonus for matching prefix (first 4 characters)
- Better for short strings than Levenshtein

**Example:**
```
String 1: "ACME CORP"
String 2: "ACME CORPORATION"

Jaro-Winkler: 0.9167
- Matching characters: A, C, M, E (prefix bonus)
- Order preserved for beginning of string
- Good score despite length difference
```

**Typical thresholds:**
- Strict: 0.90+
- Standard: 0.85-0.89
- Permissive: 0.80-0.84

### Soundex

**What it measures:** Phonetic encoding of how text sounds when spoken.

**Algorithm:**
1. Encode first letter
2. Encode remaining letters numerically:
   - 1: B, F, P, V
   - 2: C, G, J, K, Q, S, X, Z
   - 3: D, T
   - 4: L
   - 5: M, N
   - 6: R
   - (vowels and H, W, Y ignored)
3. Remove consecutive duplicates
4. Pad/truncate to 4 characters

**Examples:**
```
"Smith"  → S530
"Smyth"  → S530
Result: MATCH ✓

"John"   → J500
"Jean"   → J500
Result: MATCH ✓

"Robert" → R163
"Rupert" → R163
Result: MATCH ✓
```

**Limitations:**
- Only returns 4-character code
- Loss of information
- Works best for surname matching
- English names primarily

## Threshold Tuning

Match score thresholds determine which results are considered matches.

### Threshold Selection by Data Type

**Numeric/Postal Code (Exact or near-exact):**
```
Threshold: 0.98+
Reason: Small data, should be nearly identical
Example: "02101" vs "2101" (missing leading zero)
```

**Company Names (Moderate tolerance):**
```
Threshold: 0.85-0.90
Reason: May have legal entity type variations
Example: "Acme Corp" vs "Acme Corporation"
Typical Variation: Legal entity names, abbreviations
```

**Person Names (Higher tolerance):**
```
Threshold: 0.80-0.85
Reason: Common spelling variations, nickname matching
Example: "Johnson" vs "Jonson", "William" vs "Bill"
Typical Variation: Phonetic similarities, nickname/formal name
```

**Product Descriptions (Lower tolerance):**
```
Threshold: 0.75-0.85
Reason: May have significant description differences
Example: "Professional Widget" vs "Widget Pro"
Typical Variation: Word order, abbreviations, marketing language
```

**Address Matching (Moderate):**
```
Threshold: 0.80-0.90
Reason: Abbreviations (St/Street, Ave/Avenue) and format variations
Example: "123 Main St" vs "123 Main Street"
Typical Variation: Abbreviations, format, direction (N/S/E/W)
```

### Threshold Impact Matrix

| Threshold | Precision | Recall | Use Case |
|-----------|-----------|--------|----------|
| **0.95+** | Very High | Low | Only accept near-perfect matches (numeric, ID matching) |
| **0.90-0.94** | High | Moderate | Critical matching (master data, financial records) |
| **0.85-0.89** | Good | Good | Standard matching (company names, basic reconciliation) |
| **0.80-0.84** | Moderate | High | Permissive matching (descriptions, free-text fields) |
| **<0.80** | Low | Very High | Review all matches manually (high false positive rate) |

**Threshold adjustment strategy:**
```
Start with 0.85 (standard)
├── If too many false positives (incorrect matches):
│   └── Increase to 0.90 (tighter matching)
├── If too many false negatives (missed matches):
│   └── Decrease to 0.80 (looser matching)
└── Test with sample data before full run
```

## Review Workflow

### Match Review Interface

After intelligent lookup runs, review and approve matches.

**Review screen shows:**
```
Input Record:          | Lookup Match:        | Score:    | Status:
ACME Corp             | Acme Corporation     | 0.92      | [Approve/Reject/Skip]
Address: 123 Main St  | Address: 123 Main St | Details:  |
                      |                      | • Same street address
                      |                      | • City matches
                      |                      | • 8% name variation
```

**Match states:**
- **Approved:** Match confirmed, can be used for enrichment/deduplication
- **Rejected:** Not a valid match despite score
- **Skipped:** No decision made; requires manual review later
- **No Match:** Input record has no matching lookup record

### Batch Review Process

**For large result sets:**

```
Step 1: Filter by score range
├── Display high-confidence matches (0.95+) — Usually OK to auto-approve
├── Display moderate matches (0.85-0.94) — Manual review recommended
└── Display low matches (0.80-0.84) — Always review

Step 2: Review high-confidence matches
├── Spot-check 10% sample
├── Approve if valid
└── Batch-approve if consistent

Step 3: Manual review of moderate matches
├── Show side-by-side comparison
├── Display match reason (which fields matched)
├── Approve or reject individually

Step 4: Handle low-confidence matches
├── Review all or use alternative data source
└── Decide: Accept, reject, or request additional matching attempt
```

### Handling Ambiguous Matches

When a record has multiple potential matches:

```
Input: "Smith Inc"

Possible Matches:
1. "Smith Corporation" — Score: 0.88
2. "Smith Industries" — Score: 0.87
3. "Smiths Inc" — Score: 0.91

Decision options:
├── Select highest score (Smiths Inc) — Automatic
├── Select all above threshold — All three
├── Manual review to disambiguate — Human decision
└── Reject all ambiguous matches — Conservative approach
```

**Disambiguation strategies:**
- Use secondary columns (address, industry, size) to differentiate
- Show additional context (historical data, relationships)
- Allow reviewer to select from list
- Escalate unclear matches for business owner review

## Best Practices for Match Quality

### Data Preparation (Before Matching)

**Standardization:**
```
Before Matching:
├── Remove extra whitespace (leading, trailing, internal)
├── Normalize case (UPPERCASE or Titlecase)
├── Expand common abbreviations (St→Street, Co→Company, Inc→Incorporated)
├── Remove special characters if not meaningful (@, #, $, etc.)
├── Convert accented characters (é→e, ñ→n) if language-neutral comparison needed
└── Fix obvious typos if known

Example Transformation:
Input: "ACME  corp., Inc."
Step 1 (Trim): "ACME corp., Inc."
Step 2 (Case): "ACME CORP., INC."
Step 3 (Expand): "ACME CORPORATION, INCORPORATED"
Step 4 (Clean): "ACME CORPORATION"
Result for matching: Much cleaner, higher match rate
```

**Use `analyze_column_distribution` to understand data before matching:**
```
Questions to answer:
├── What percentage of values are null/empty?
├── What's the length distribution (shortest, longest, average)?
├── Are there common prefixes or suffixes?
├── What characters are present (numbers, special chars)?
├── Are there obvious spelling variations?
└── What's the vocabulary size (unique values)?

Example output:
Column: Company Name
├── Null %: 2.3%
├── Length: Min=3, Max=150, Avg=35
├── Most common prefix: None
├── Special characters: ., &, -, ', ()
├── Unique values: 12,456 (high variety)
├── Top variations:
│   ├── "Inc" / "Inc." / "Incorporated" / "Inc,"
│   ├── "Corp" / "Corp." / "Corporation"
│   ├── "LLC" / "L.L.C." / "Ltd."
```

### Column Selection Strategy

**Primary vs Secondary columns:**
```
Primary Matching (weight: 70-80%):
├── Company Name (highest signal)
├── Product Code (if available)
└── Full Address (if detailed)

Secondary Matching (weight: 20-30%):
├── City
├── State/Province
├── Postal Code
├── Industry
└── Contact person
```

**Avoid unreliable columns:**
```
Don't use for matching:
├── Phone numbers (change frequently)
├── Email addresses (change frequently, privacy sensitive)
├── Website URLs (change, domain squatting)
├── Internal reference numbers (varies by system)
└── Timestamps (reflect data entry time, not content)

These vary too much; add noise rather than signal
```

### Iterative Refinement

**Matching process iteration:**
```
Iteration 1: Initial matching with 0.85 threshold
├── Results: 8,000 matches, 2,000 unmatched
├── Review high-confidence (>0.90): 95% accuracy
├── Review moderate (0.85-0.90): 75% accuracy
└── Finding: Moderate threshold needs tuning

Iteration 2: Adjust threshold to 0.88
├── Results: 7,200 matches (tighter), 2,800 unmatched
├── Review: 90% accuracy across all matches
├── Finding: Better precision, acceptable recall

Iteration 3: Manual review of unmatched
├── 500 unmatched actually have matches in reference data
├── Add domain-specific matching (e.g., subsidiary names)
└── Final: 99% of matching records identified

Lessons learned: Industry-specific variations required custom rules
```

### Handling Special Cases

**Company name variations:**
```
Input: "ABC Manufacturing"
Matches to find:
├── "ABC Manufacturing" (exact)
├── "ABC Manufacturing Corp" (legal name)
├── "ABC Mfg" (abbreviation)
├── "American Business Corp (ABC)" (full name with acronym)
├── "ABC Manufacturing Inc, subsidiary of XYZ" (nested relationship)

Strategy:
├── Use fuzzy matching with 0.85 threshold (catches first 3)
├── Add secondary matching on known abbreviation mappings
├── Include relationship data in review
```

**International names:**
```
Company: "Société Générale"
Challenges:
├── Accented characters (é)
├── Legal form in French (Société)
├── May be registered as "Societe Generale" without accent

Strategy:
├── Normalize accents before matching
├── Include common language translations
├── Use phonetic matching as fallback
```

**Address variations:**
```
Input: "123 Oak Ave, Apt 4B, Springfield, IL 62701"
Match candidates:
├── "123 Oak Avenue, Suite 4B, Springfield, IL 62701" (abbreviation)
├── "123 Oak Ave, Springfield, IL 62701" (without unit)
├── "123 Oak Street, Springfield, IL 62701" (wrong street type)

Strategy:
├── Standardize street types (Ave→Avenue, St→Street)
├── Match at building/street level, not exact unit
├── Use postal code as secondary match
└── Accept lower score for address matching (0.80+)
```

## Troubleshooting Poor Match Rates

**Symptom: Very few matches found**

```
Diagnosis: Threshold too high
Solution:
├── Lower threshold from 0.85 to 0.80
├── Review matches at new threshold for false positives
└── Find acceptable balance point

Diagnosis: Data quality issues
Solution:
├── Run analyze_column_distribution on both input and lookup
├── Check for data type mismatches (numeric stored as text)
├── Look for null values in matching columns
├── Verify foreign key consistency
└── Standardize data before re-matching

Diagnosis: Column selection mismatch
Solution:
├── Verify input and lookup columns contain comparable data
├── Example: Matching ZIP code against City name won't work
├── Select columns with same semantic meaning
└── Test matching on subset first

Example Fix:
Before: Matching CompanyFullDescription (input) vs CompanyName (lookup)
After: Matching CompanyName (input) vs CompanyName (lookup)
Result: Match rate improves dramatically
```

**Symptom: Too many false positives (incorrect matches)**

```
Diagnosis: Threshold too low
Solution:
├── Increase threshold from 0.80 to 0.85 or higher
├── Review quality of now-excluded matches
└── Manually review borderline cases

Diagnosis: Algorithm not appropriate for data type
Solution:
├── "Smith" vs "Smyth" needs phonetic matching (not fuzzy)
├── Company names with acronyms need token-based (not exact)
├── Addresses need standardization first (not raw comparison)
└── Choose algorithm based on data characteristics

Diagnosis: Lookup data has duplicates or errors
Solution:
├── Find and merge duplicate lookup records first
├── Fix obvious errors in master data
├── Re-run matching against cleaned lookup
└── Clean input should match against clean reference
```

**Symptom: Unexpected matches missing from results**

```
Diagnosis: Match fell below threshold
Solution:
├── Lower threshold to capture similar results
├── Review those borderline matches
├── Decide if manual approval is acceptable

Diagnosis: Format mismatch between datasets
Solution:
├── Example: Input has "123 Main St", Lookup has "123 Main Street"
├── Standardize abbreviations before matching
├── Pre-process data consistently in both datasets
└── Test with sample matches first

Diagnosis: Matching algorithm doesn't handle data type
Solution:
├── Different algorithms for names, addresses, descriptions
├── Person names: Soundex, phonetic (catch nicknames)
├── Addresses: Token-based (word order varies)
├── Descriptions: Fuzzy (typos, abbreviations)
└── Test algorithm on known match pairs
```

## Key Takeaways

1. **Choose appropriate matching strategy** — Fuzzy for names/descriptions, exact for codes, phonetic for sound-alikes
2. **Prepare data thoroughly** — Standardization and cleansing improve match quality significantly
3. **Tune thresholds carefully** — Test different thresholds on sample data before full run
4. **Review results systematically** — High-confidence matches vs manual review vs rejection
5. **Iterate and refine** — Match quality improves with multiple passes and domain knowledge
6. **Document matching rules** — For reproducibility and future maintenance
7. **Consider false positives and negatives** — Choose threshold based on cost of each type of error
