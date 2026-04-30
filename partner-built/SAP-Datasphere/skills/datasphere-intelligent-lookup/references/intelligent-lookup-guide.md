# Intelligent Lookup Reference Guide

## Matching Strategy Details and Algorithms

### Fuzzy Matching (Token-Based)

**How it works:**
- Breaks text into words/tokens
- Compares sets of tokens between input and lookup
- Assigns score based on matching token percentage
- Optionally considers token order

**Strengths:**
- Good for variable word order: "New York City" vs "City of New York"
- Handles added/missing words: "Smith Inc" vs "Smith Inc Corporation"
- Robust to word reordering

**Limitations:**
- Single-word fields don't benefit from tokenization
- Doesn't handle within-word typos well: "Smyth" vs "Smith"
- May miss partial matches

**Example:**
```
Input: "Professional Widget Manufacturing"
Tokens: [Professional, Widget, Manufacturing]

Lookup 1: "Widget Manufacturing Professional"
Tokens: [Widget, Manufacturing, Professional]
Match: 100% (same tokens, different order)
Score: 0.99 ✓

Lookup 2: "Professional Widget"
Tokens: [Professional, Widget]
Match: 66% (2 of 3 tokens)
Score: 0.66 ✗ (below typical 0.85 threshold)

Lookup 3: "Professional Widget Manufacturing Inc"
Tokens: [Professional, Widget, Manufacturing, Inc]
Match: 75% (3 of 4 tokens)
Score: 0.75 ✗
```

**Configuration options:**
```
Word Order Sensitivity:
├── Ignore order (order=false): More matches, less strict
│   Example: "Smith John" matches "John Smith"
└── Respect order (order=true): Fewer matches, more strict
    Example: "Smith John" does NOT match "John Smith"

Min Token Length:
├── 1: Count all tokens including single characters
├── 2: Ignore single-letter words (A, B, I)
└── 3: Ignore short words (And, The, For)
    Example: "The Smith Corporation" vs "Smith Corp"
    With min=3: Effectively matches on Smith, Corporation (ignores The)
```

---

### Levenshtein Distance

**How it works:**
- Counts minimum number of single-character edits needed
- Edits: insert, delete, or replace a character
- Distance of 0 = identical, higher = more different
- Normalized to 0-1 scale: similarity = 1 - (distance / max_length)

**Strengths:**
- Handles typos well: "Smith" vs "Smth"
- Works for single words
- Mathematically precise

**Limitations:**
- Expensive for long strings
- Doesn't recognize phonetically similar words: "Smith" vs "Smyth"
- Word order matters: "John Smith" ≠ "Smith John"
- Sensitive to letter position changes

**Example calculation:**
```
String 1: "ACME"
String 2: "ACNE"

Edit sequence:
1. ACME → ACNE (replace M with N)
Distance: 1

Normalized Score:
Max length: 4
Similarity: 1 - (1/4) = 0.75

Result: 0.75 score (below 0.85 threshold, no match)

---

String 1: "kitten"
String 2: "sitting"

Edit sequence:
1. kitten → sitten (replace k with s)
2. sitten → sittin (replace e with i)
3. sittin → sitting (insert g)
Distance: 3

Normalized Score:
Max length: 7
Similarity: 1 - (3/7) = 0.57

Result: No match
```

**When to use:**
- Detecting typos and minor spelling variations
- Matching codes with single-character errors
- Comparing short strings (names, codes)

---

### Jaro-Winkler Distance

**How it works:**
1. Calculate base Jaro score (character match and order)
2. Apply Winkler bonus if strings share common prefix
3. Jaro-Winkler = Jaro + (prefix_length × prefix_weight × (1 - Jaro))
   - prefix_weight typically 0.1
   - prefix_length max 4 characters

**Formula:**
```
Jaro = (1/3) × [(matches_in_str1 / len_str1) +
                (matches_in_str2 / len_str2) +
                ((matches - transpositions) / matches)]

Jaro-Winkler = Jaro + (l × p × (1 - Jaro))
where:
- l = common prefix length (max 4)
- p = prefix weight (typically 0.1)
```

**Strengths:**
- Better than Levenshtein for shorter strings
- Rewards matching prefix: ACME vs ACNE scores higher
- Considers character position and order
- Industry standard for name matching

**Limitations:**
- More complex computation
- Still doesn't handle phonetic variations
- Length difference still impacts score

**Example calculation:**
```
String 1: "Smith"
String 2: "Smyth"

Character Analysis:
Position: 1=S, 2=m, 3=i/y, 4=t, 5=h
Matches: S, m, t, h (4 matches)
Transposition: i/y are different, not counted as match

Jaro = (1/3) × [(4/5) + (4/5) + ((4-0)/4)]
     = (1/3) × [0.8 + 0.8 + 1.0]
     = 0.867

Jaro-Winkler = 0.867 + (4 × 0.1 × (1 - 0.867))
             = 0.867 + (4 × 0.1 × 0.133)
             = 0.867 + 0.053
             = 0.920

Result: 0.92 score (matches at 0.85 threshold)
```

**When to use:**
- Person name matching
- Company name matching
- Comparing short strings where word order is fixed

---

### Soundex

**How it works:**
1. Keep first letter as is
2. Replace letters with numbers:
   - 1: B, F, P, V
   - 2: C, G, J, K, Q, S, X, Z
   - 3: D, T
   - 4: L
   - 5: M, N
   - 6: R
   - (Remove vowels, H, W, Y)
3. Remove consecutive duplicates
4. Pad/truncate to 4 characters

**Strengths:**
- Very fast computation
- Handles phonetic variations
- Works well for surnames
- English pronunciation-based

**Limitations:**
- Significant information loss (4 characters only)
- English-centric
- Can produce many false positives
- Doesn't work well for names < 4 characters

**Example encoding:**
```
"Robert"
R-o-b-e-r-t

Step 1: Keep R
Step 2: o(vowel-remove), b(1), e(vowel-remove), r(6), t(3)
        → R163

Step 3: Remove consecutive duplicates
        → R163 (no duplicates)

Step 4: Pad to 4 characters
        → R163 (already 4)

---

"Rupert"
R-u-p-e-r-t

Step 1: Keep R
Step 2: u(vowel-remove), p(1), e(vowel-remove), r(6), t(3)
        → R163

Result: "Robert" and "Rupert" both encode to R163 = MATCH ✓

---

"Lloyd"
L-l-o-y-d

Step 1: Keep L
Step 2: l(4), o(vowel-remove), y(remove), d(3)
        → L43

Step 3: Remove consecutive duplicates
        (no consecutive duplicates)
        → L43

Step 4: Pad to 4 characters
        → L430

---

"Lloyd" vs "Laude"
Lloyd = L430
Laude = L300

DIFFERENT CODES = NO MATCH ✗ (even though phonetically similar)
```

**Soundex encoding table:**
```
Letter Digit  | Examples
1      B F P V| "Baker" → B260, "Baker" vs "Barker" = B620 ✗
2      C G J K| "Carter" → C630, "Carter" vs "Karter" = K630 ✓
3      D T    | "Davis" → D120, "Davis" vs "Tavis" = T120 ✓
4      L      | "Lewis" → L200
5      M N    | "Morris" → M620, "Morris" vs "Norris" = N620 ✓
6      R      | "Roy" → R000
(vowels removed)
```

**When to use:**
- Surname matching
- Name matching in general
- As initial filter before more expensive algorithms

---

### Metaphone and Double Metaphone

**How it works:**
Similar to Soundex but with more sophisticated phonetic rules:
- More rules than Soundex
- Handles English pronunciation better
- Can produce primary and secondary codes (Double Metaphone)
- Keeps more letters than Soundex

**Strengths:**
- Better than Soundex for English names
- Handles consonant clusters
- Fewer false matches than Soundex

**Limitations:**
- Still English-centric
- Information loss (typically 4-5 characters)
- More complex rules to implement

**Example encoding:**
```
"Smith"     → SM0
"Smyth"     → SM0
Match: ✓

"Katherine" → K0RN
"Catherine" → K0RN
Match: ✓

"Johnson"   → JNSN
"Jonson"    → JNSN
Match: ✓

"Phillip"   → FL (first P is silent)
"Philip"    → FL
Match: ✓
```

**When to use:**
- Surname/name matching (better than Soundex)
- Phonetic variations of English names
- More accurate than Soundex while still fast

---

### Composite/Custom Matching Rules

**When single algorithm not sufficient:**

**Example 1: Company Name Matching Rule**
```
Rule Set:
Step 1: Exact match (case-insensitive, no punctuation)
  "ACME Corporation" vs "acme corporation" → MATCH ✓

Step 2: If no exact, try fuzzy (0.90 threshold)
  "ACME Corp" vs "ACME Corporation" → Score 0.93 ✓

Step 3: If no fuzzy, try token-based
  "Acme Inc" vs "Inc Acme" → Tokens match ✓

Step 4: If still no match, try without legal entity type
  "ACME Manufacturing" vs "ACME Mfg Co" → Remove Co, match ✓

Implementation:
```sql
IF exact_match(input, lookup) THEN
  RETURN MATCH (score 1.0)
ELSE IF fuzzy_score(input, lookup) >= 0.90 THEN
  RETURN MATCH (score fuzzy_score)
ELSE IF token_match(input, lookup) >= 0.80 THEN
  RETURN MATCH (score token_match)
ELSE IF token_match(remove_legal_entity(input), lookup) >= 0.85 THEN
  RETURN MATCH (score adjusted)
ELSE
  RETURN NO_MATCH
END IF
```

**Example 2: Address Matching Rule**
```
Rule Set:
Column 1 (Weight 50%): Street Address
  Algorithm: Fuzzy (Jaro-Winkler 0.85)
  Preprocessing: Standardize abbreviations (St→Street)

Column 2 (Weight 30%): City
  Algorithm: Exact (case-insensitive)
  Preprocessing: None

Column 3 (Weight 20%): Postal Code
  Algorithm: Exact or prefix match
  Preprocessing: Remove dashes (12345-6789 → 12345)

Final Score: 50% × Street_Score + 30% × City_Score + 20% × Postal_Score

Example:
Input: "123 Main St, NewYork, NY 10001"
Lookup: "123 Main Street, New York, NY 10001"

Scoring:
├── Street: "Main St" vs "Main Street" = 0.95 → 0.95
├── City: "NewYork" vs "New York" = 1.0 (normalized) → 1.0
├── Postal: "10001" vs "10001" = 1.0 → 1.0

Final Score: (50% × 0.95) + (30% × 1.0) + (20% × 1.0) = 0.975
Result: MATCH ✓
```

---

## Score Threshold Recommendations by Data Type

### Text Fields - Company Names

**Threshold: 0.85 (Standard)**

**Reasoning:**
- Often have legal entity types (Inc, Corp, Ltd)
- May be abbreviated (Acme vs Acme Corporation)
- Regional variations (American vs US)

**Match examples (Jaro-Winkler):**
```
"ACME Corp" vs "Acme Corporation" = 0.88 ✓
"ABC Manufacturing" vs "ABC Mfg" = 0.87 ✓
"Global Supply Inc" vs "Global Supplies Inc" = 0.84 ✗
"Smith Company" vs "Smiths Company" = 0.93 ✓
```

**Threshold tuning:**
- Too strict (0.95): Misses legitimate matches
- Too loose (0.75): Includes many false matches
- 0.85: Balanced precision/recall

---

### Text Fields - Person Names

**Threshold: 0.82 (Slightly lower)**

**Reasoning:**
- Many common phonetic variations
- Nicknames: Bill/William, Bob/Robert
- Spelling variations: Johnson/Jonson, Smith/Smyth
- Order variations: John Smith vs Smith, John

**Match examples (Jaro-Winkler):**
```
"John Smith" vs "Jon Smyth" = 0.84 ✓
"William Johnson" vs "Bill Johnson" = 0.79 ✗ (too different)
"Catherine" vs "Katherine" = 0.92 ✓
"Patricia" vs "Patrice" = 0.89 ✓
```

**Threshold tuning:**
- Use 0.82-0.85 for general matching
- Use 0.75 if you accept manual review
- Phonetic matching works better (use Soundex/Metaphone first)

---

### Addresses - Street Address

**Threshold: 0.88 (Stricter)**

**Reasoning:**
- Must match location accurately
- Abbreviations are standardizable
- Format variations are common (12 vs 12th)

**Match examples:**
```
"123 Main Street" vs "123 Main St" = 0.95 ✓
"456 Oak Ave" vs "456 Oak Avenue" = 0.93 ✓
"789 Pine Rd" vs "789 Pine Road" = 0.93 ✓
"100 First St" vs "100 First Street" = 0.95 ✓
"2 Second Ave" vs "200 Second Ave" = 0.88 ✓ (barely)
"250 Elm" vs "250 Oak" = 0.33 ✗ (wrong street)
```

**Threshold tuning:**
- 0.88-0.92: Recommended for address matching
- Pre-standardize abbreviations first (St, Ave, Rd, Blvd)
- Use postal code as secondary verification

---

### Addresses - Postal Code

**Threshold: 0.98 (Very strict)**

**Reasoning:**
- Must be nearly exact
- 5-10 digit number
- Variations are uncommon

**Match examples:**
```
"10001" vs "10001" = 1.0 ✓
"10001-1234" vs "10001" = 0.92 (different formats)
"02101" vs "2101" = 0.80 (missing leading 0)
```

**Threshold tuning:**
- Use exact match, not fuzzy
- Handle format variations programmatically
- Pre-clean before matching

---

### Numeric Fields - Product Codes

**Threshold: 0.99 (Almost exact)**

**Reasoning:**
- Must be nearly identical
- Small character set (digits)
- Any mismatch = wrong product

**Match examples:**
```
"SKU-12345" vs "SKU-12345" = 1.0 ✓
"SKU12345" vs "SKU-12345" = 0.97 (format difference)
"SKU-12345" vs "SKU-12346" = 0.88 ✗
```

**Threshold tuning:**
- 0.98+: Strict, recommended
- Only accept near-perfect matches
- Pre-standardize format

---

### Text Fields - Product Descriptions

**Threshold: 0.78-0.82 (More permissive)**

**Reasoning:**
- May use different marketing language
- Word order varies
- Abbreviations common (Pro, Max, Standard, etc.)
- Typos possible in descriptions

**Match examples:**
```
"Professional Widget" vs "Widget Pro" = 0.82 ✓
"Advanced Manufacturing Tool" vs "Advanced Tool" = 0.80 ✓
"Standard Gadget" vs "Basic Gadget" = 0.73 ✗
"Product XYZ-100" vs "XYZ 100 Product" = 0.78 ✓
```

**Threshold tuning:**
- Use 0.78-0.82 for description matching
- Token-based algorithm works better
- Be prepared for manual review

---

### Summary Table

| Data Type | Algorithm | Threshold | Note |
|-----------|-----------|-----------|------|
| Company Names | Jaro-Winkler | 0.85 | Good balance; handles legal entities |
| Person Names | Soundex/Metaphone* | 0.82 | Phonetic better; also try Jaro-Winkler |
| Street Address | Jaro-Winkler | 0.88 | Pre-standardize abbreviations |
| Postal Code | Exact | 0.99 | Nearly exact match required |
| Product Codes | Exact | 0.99 | Nearly exact; strict matching |
| Descriptions | Token-based | 0.80 | More permissive; manual review expected |
| Email Address | Exact | 0.99 | Nearly exact (domain case-insensitive) |
| Phone Number | Exact (digits only) | 0.99 | Remove formatting, match digits only |

*Soundex/Metaphone provides boolean match (same code = match), not scored

---

## Pre-Processing Tips - Data Standardization

### String Case Normalization

**Recommended approach:**
```
Normalize to UPPERCASE for matching
├── Avoids case sensitivity issues
├── Case inconsistency won't prevent matches
├── Standard practice for fuzzy matching

Example:
Input: "aCmE cOrP"
After: "ACME CORP"

Lookup: "acme corporation"
After: "ACME CORPORATION"
```

### Whitespace Handling

```
Step 1: Trim leading and trailing
├── " ACME " → "ACME"

Step 2: Standardize internal spaces (collapse multiple to single)
├── "ACME  CORP" → "ACME CORP"

Step 3: Normalize line breaks and tabs
├── "ACME\nCORP" → "ACME CORP"
```

### Special Character Removal

**Decision: What to keep/remove**

```
Keep (meaningful):
├── Hyphens in compound words (New-York)
├── Apostrophes in names (O'Brien)
└── Numbers (Model 100, Version 2.0)

Remove (usually noise):
├── Punctuation at end (ACME, → ACME)
├── Extra symbols (@, #, $, %, &)
├── Parentheses and brackets (ACME (subsidiary) → ACME subsidiary)
└── Commas and periods

Partial removal:
├── Periods in abbreviations (U.S.A. → USA)
├── Dashes in codes (SKU-12345 → SKU12345 for matching)
```

**Examples:**
```
Input: "ACME, Inc."
Step 1 (case): "ACME, INC."
Step 2 (trim): "ACME, INC." (no leading/trailing)
Step 3 (special chars): "ACME INC"
Result: "ACME INC"

Input: "O'Brien & Associates (New York)"
Step 1 (case): "O'BRIEN & ASSOCIATES (NEW YORK)"
Step 2 (remove parens): "O'BRIEN & ASSOCIATES NEW YORK"
Step 3 (remove &): "O'BRIEN ASSOCIATES NEW YORK"
Result: "O'BRIEN ASSOCIATES NEW YORK"
```

### Abbreviation Standardization

**Common expansions:**

```
Company Legal Forms:
├── Inc → Incorporated
├── Corp → Corporation
├── Ltd → Limited
├── LLC → Limited Liability Company
├── Co → Company
├── Assoc → Association

Geographic:
├── St → Street
├── Ave → Avenue
├── Blvd → Boulevard
├── Rd → Road
├── Ln → Lane
├── Dr → Drive
├── Pl → Place
├── Ct → Court
├── N/S/E/W → North/South/East/West
├── NY → New York
├── PA → Pennsylvania
├── CA → California

Professional:
├── Ph.D. → Doctor
├── M.D. → Medical Doctor
├── Mr. → Mister
├── Mrs. → Missus
└── Ms. → Miss/Missus

Measurement:
├── Ft → Foot
├── Lbs → Pounds
├── Oz → Ounces
├── Qt → Quart
└── Gal → Gallon
```

**Implementation:**
```
Expansion strategy:
1. Create abbreviation mapping table
2. Apply during pre-processing
3. Or include both versions in matching

Example:
Input: "ACME Inc Street"
Option A (expand): "ACME Incorporated Street"
Option B (both): Match both "Inc" and "Incorporated" versions

Lookup: "ACME Corporation Street"
```

### Accents and Diacritics

**When to remove:**

```
Keep accents when:
├── Language-specific matching required (French, Spanish)
├── Name identity important (José vs Jose are different people)

Remove accents when:
├── Language-neutral matching
├── System doesn't support Unicode
├── Names used internationally
```

**Conversion table:**
```
À, Á, Â, Ã, Ä, Å → A
È, É, Ê, Ë → E
Ì, Í, Î, Ï → I
Ò, Ó, Ô, Õ, Ö → O
Ù, Ú, Û, Ü → U
Ñ → N
Ç → C
```

**Example:**
```
Input: "Société Générale"
After: "Societe Generale"

Lookup: "Societe Generale"
Result: MATCH ✓
```

### Number Formatting

```
Remove formatting for matching:
├── Phone: "(555) 123-4567" → "5551234567"
├── ZIP Code: "10001-1234" → "100011234" (for matching digits only)
├── Currency: "$1,234.56" → "1234.56"
├── Product code: "SKU-ABC-12345" → "SKUABC12345"

Consider context:
├── If dash is meaningful (model numbers): Keep
├── If just formatting: Remove
```

---

## Common Matching Patterns by Industry

### Finance/Accounting

**Pattern 1: Vendor Deduplication**
```
Columns to match: Vendor Name, Address, City
Primary: Vendor Name (fuzzy, 0.85)
Secondary: City (exact)
Threshold: 0.85

Example:
Input: "ACME Manufacturing Inc"
Match: "Acme Mfg Corporation"
Requires: Manual review despite score

Additional rule: If name matches but different city → Likely different vendor
```

**Pattern 2: Invoice Reconciliation**
```
Match: Invoice-to-PO line
Columns: Vendor, PO Number, Amount
Algorithm: Exact on Vendor + PO, fuzzy on amount (±5%)
Threshold: Vendor exact + PO fuzzy 0.95 + Amount within tolerance

Example:
Input PO: Amount $10,000
Invoice: Amount $9,987.50 (0.125% difference = match)
```

### Sales/CRM

**Pattern 1: Customer Deduplication**
```
Columns: Customer Name, Phone, Address
Algorithm 1: Exact match on phone (most reliable)
Algorithm 2: If no phone, fuzzy on name + city
Threshold: Phone exact, else name 0.82 + city exact

Example:
Phone Match: Always match regardless of name
No Phone: Require name match + postal code match
```

**Pattern 2: Lead Deduplication**
```
Columns: Email, Phone, First Name + Last Name
Algorithm: Exact email (if available), else phone, else fuzzy names
Threshold: Email/Phone exact, names 0.85

Priority:
1. Email address (nearly unique)
2. Phone number (high specificity)
3. First + Last Name fuzzy match
```

### Supply Chain

**Pattern 1: Supplier Master Consolidation**
```
Columns: Company, Address, Supplier Code
Algorithm: Fuzzy company (0.85) + address (0.88) + optional code
Threshold: Both address and company must match, code confirms

Example:
"ACME Mfg" + "123 Main" = potential match
"ACME Mfg" + "456 Oak" = different supplier (address doesn't match)
```

**Pattern 2: SKU Harmonization**
```
Columns: Product Code, Product Name, Supplier
Algorithm: Exact on code, fuzzy on name for fallback
Threshold: Code 0.99 (nearly exact), Name 0.85 if code missing

Example:
Code "SKU-12345" exact matches primary
Name match only if code not available
```

### Healthcare

**Pattern 1: Patient Record Matching**
```
Columns: First Name, Last Name, DOB, Phone
Algorithm:
  Rule 1: DOB + Last Name exact → MATCH
  Rule 2: First + Last Name + Phone → MATCH
  Rule 3: Fuzzy name (0.82) + DOB exact → MATCH
Threshold: At least 2 fields must strongly match

Caution: Medical matching requires high precision
```

**Pattern 2: Drug/Medication Matching**
```
Columns: Drug Name, Strength, Form
Algorithm: Fuzzy on name (0.88), exact on strength
Threshold: Name must match, strength must be exact

Example:
"Aspirin 100mg tablet" vs "ASA 100mg tablet" = 0.82 ✓ (close name, exact strength)
"Aspirin 100mg" vs "Aspirin 200mg" = NO MATCH ✗ (strength must match exactly)
```

### Retail

**Pattern 1: Product Catalog Harmonization**
```
Columns: UPC, Product Name, Brand
Algorithm: Exact on UPC, fuzzy on name for lookups
Threshold: UPC 0.99, Name 0.80 (descriptions vary)

Example:
UPC "012345678901" exact matches
Name match secondary if UPC unavailable
```

**Pattern 2: Store Location Matching**
```
Columns: Store Code, Street Address, City, State
Algorithm: Store code exact, address + city + state fuzzy
Threshold: Code 0.99, else address+city+state 0.88

Example:
Store "NYC-001" exact on code
If code missing: Address 0.90 + City 1.0 + State 1.0 = weighted match
```

---

## Troubleshooting Decision Tree

```
Start: Poor match results

├─ Too few matches found?
│  ├─ Check threshold
│  │  └─ Lower from 0.85 to 0.80, test
│  ├─ Check column selection
│  │  └─ Run analyze_column_distribution; verify data in columns
│  ├─ Check data quality
│  │  └─ Any nulls? Truncated values? Wrong data type?
│  └─ Check algorithm appropriateness
│     └─ Names: Use phonetic? Addresses: Use token-based?
│
├─ Too many false matches?
│  ├─ Check threshold
│  │  └─ Raise from 0.85 to 0.90, review quality
│  ├─ Check algorithm fit
│  │  └─ Example: Exact matching for codes, not fuzzy
│  ├─ Add secondary columns
│  │  └─ Single column matching too broad; add city, postal code
│  └─ Check lookup data
│     └─ Duplicates in master data? Clean first
│
├─ Specific records not matching?
│  ├─ Check for case sensitivity issues
│  │  └─ Normalize to uppercase
│  ├─ Check for special characters
│  │  └─ "Smith, Inc." vs "Smith Inc" (comma matters)
│  ├─ Check for abbreviation issues
│  │  └─ "St" vs "Street"; expand abbreviations
│  ├─ Check for extra whitespace
│  │  └─ "Smith  Inc" (double space) vs "Smith Inc"
│  └─ Try different algorithm
│     └─ If fuzzy fails, try phonetic or token-based
│
└─ Performance issues (slow matching)?
   ├─ Check data volume
   │  └─ Millions of rows? Consider batch processing
   ├─ Check algorithm complexity
   │  └─ Soundex (fast) vs Jaro-Winkler (slower)
   ├─ Check column cardinality
   │  └─ Matching on high-cardinality field? May be slow
   └─ Check for pre-processing
      └─ Can you pre-filter (exact matches first)?
```
