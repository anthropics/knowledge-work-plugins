# Provider Extraction Patterns

Skill-specific patterns for extracting practitioner data from healthcare practice
websites. For general extraction and site mapping rules, see `nimble-playbook.md`.

---

## Page URL Scoring

After `nimble map` discovers a site's pages, score each URL by path keywords to
identify provider-relevant pages. See Site Mapping Pattern in `nimble-playbook.md`
for the generic discover/score/filter/fallback flow.

### Keyword Weight Table

| Weight | Path Segments | Examples |
|--------|--------------|----------|
| **High** | `/providers`, `/doctors`, `/physicians`, `/our-team`, `/staff`, `/our-providers`, `/our-doctors`, `/our-physicians`, `/surgeons`, `/specialists` | `/our-providers`, `/meet-our-doctors` |
| **High** | `/dr-*`, `/doctor-*` (individual provider pages) | `/dr-jane-smith`, `/doctor-john-doe` |
| **Medium** | `/team`, `/about`, `/people`, `/about-us`, `/meet-the-team`, `/faculty`, `/clinicians` | `/about-us/team`, `/our-people` |
| **Low** | Homepage (`/`), `/services`, `/locations` | `/`, `/services/cataract-surgery` |
| **Skip** | `/blog`, `/news`, `/careers`, `/jobs`, `/privacy`, `/terms`, `/patient-portal`, `/pay-bill`, `/faq`, `/testimonials`, `/reviews`, `/gallery`, `/media` | `/blog/eye-health-tips` |

### Scoring Rules

- Cap at **15 pages** per practice site
- Always include at least one High-weight page (or homepage as fallback)
- Individual provider pages (`/dr-*`) are high value but cap at 10 per site to
  avoid over-extraction on large multi-provider practices
- If `nimble map` returns < 3 scored candidates, fall back to:
  ```bash
  nimble search --query "site:{domain} doctors OR providers OR team" --max-results 10 --search-depth lite
  ```

---

## Core Extraction Fields (5 Fields)

Every provider record targets these 5 fields. Confidence scoring uses this as the
N-field list (see Entity Confidence Scoring in `nimble-playbook.md`).

| # | Field | Key | Detection Patterns |
|---|-------|-----|-------------------|
| 1 | **Full Name** | `name` | `Dr.` prefix, `<h2>`/`<h3>` heading patterns, bold text near credential suffixes, structured bio sections |
| 2 | **Credentials** | `credentials` | Regex patterns (see below) found adjacent to names |
| 3 | **Specialty** | `specialty` | Keywords per vertical (see below), often near name or in bio paragraph |
| 4 | **Contact / Scheduling** | `contact` | Phone regex `\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}`, appointment URLs (`/book`, `/schedule`, `/request-appointment`), email addresses |
| 5 | **Education / Training** | `education` | "Residency", "Fellowship", "Medical School", "Board Certified", university names, graduation years |

### Confidence Scoring (from shared pattern)

- **High** -- 5/5 fields found + confirmed by 2+ pages or sources
- **Medium** -- 3-4/5 fields found
- **Low** -- 1-2/5 fields found

Display as: `High`, `Medium`, `Low`

---

## Credential Regex Patterns

Match these suffixes adjacent to provider names. Case-insensitive. Allow comma,
space, or period separators between multiple credentials.

### Medical Doctors
```
MD|M\.D\.|DO|D\.O\.
```

### Eye Care
```
OD|O\.D\.|FAAO
```

### Dental
```
DDS|D\.D\.S\.|DMD|D\.M\.D\.
```

### Advanced Practice
```
NP|PA|PA-C|ARNP|APRN|CNS|CRNA|DNP|D\.N\.P\.
```

### Therapy & Allied Health
```
PT|DPT|OT|OTR|SLP|CCC-SLP|RD|RDN|LCSW|LPC|PhD|Ph\.D\.|PsyD|Psy\.D\.
```

### Board Certifications (commonly listed)
```
FACS|FACP|FACC|FACOG|FAAP|FACEP|FAAOS|FASRS|FRCSC
```

### Combined Pattern

When scanning extracted markdown, look for names followed by credential clusters:

```
[Name],?\s*((?:MD|DO|OD|DDS|DMD|NP|PA|PA-C|ARNP|APRN|PT|DPT|PhD|FACS|FAAO|FACP|FACC|FACOG|FAAP|FAAOS|FASRS)[,.\s]*)+
```

---

## Specialty Keywords by Healthcare Vertical

### Ophthalmology
```
ophthalmology, ophthalmologist, retina, retinal, cataract, glaucoma, cornea,
corneal, LASIK, refractive surgery, oculoplastics, neuro-ophthalmology,
pediatric ophthalmology, vitreoretinal, anterior segment, posterior segment,
strabismus, ocular oncology, uveitis
```

### Dental
```
dentist, dentistry, general dentistry, cosmetic dentistry, orthodontics,
orthodontist, periodontics, periodontist, endodontics, endodontist,
oral surgery, oral surgeon, prosthodontics, prosthodontist, pediatric
dentistry, implants, dental implants, TMJ, sedation dentistry
```

### Dermatology
```
dermatology, dermatologist, Mohs surgery, cosmetic dermatology, skin cancer,
melanoma, psoriasis, eczema, acne, rosacea, laser treatment, botox,
fillers, chemical peel, phototherapy, patch testing
```

### General / Primary Care
```
family medicine, internal medicine, primary care, general practice,
preventive medicine, geriatrics, urgent care, walk-in clinic,
physical exam, wellness, annual checkup
```

### Orthopedics
```
orthopedics, orthopedic surgery, sports medicine, joint replacement,
spine surgery, hand surgery, foot and ankle, shoulder, knee,
arthroscopy, fracture care, physical therapy, rehabilitation
```

---

## Entity Deduplication (Skill-Specific)

Apply the shared 3-layer dedup pattern from `nimble-playbook.md` with these
skill-specific rules:

1. **Exact match** -- Same name + same practice domain = same provider
2. **Credential match** -- Same name + same credentials + same city = likely same
   provider (even across different practice sites)
3. **Fuzzy match** -- Normalize names (strip "Dr.", middle initials, suffixes),
   compare with Levenshtein distance <= 2 + same specialty = possible match,
   flag for review rather than auto-merging

### Cross-source name normalization

Different sources format provider names very differently. Exact string matching
across sources produces near-zero matches. Always normalize before comparing:

| Source | Raw format | After normalization |
|--------|-----------|-------------------|
| Google Maps | "Dr. Jane A. Smith, MD - Retina Specialist" | "jane smith" |
| Yelp | "Jane Smith" | "jane smith" |
| BBB | "Smith Eye Care LLC" | "smith eye care" |
| Practice website | "Jane A. Smith, M.D., F.A.C.S." | "jane smith" |

Normalization steps (apply in order):
1. Strip titles: `Dr.`, `Mr.`, `Ms.`, `Prof.`
2. Strip credentials: all patterns from the Credential Regex section above
3. Strip business suffixes: `LLC`, `Inc`, `Corp`, `PC`, `PLLC`, `PA`, `Associates`
4. Strip specialty descriptors: "- Retina Specialist", "- Ophthalmologist"
5. Strip middle initials (single letters with optional period)
6. Lowercase, collapse whitespace, strip remaining punctuation

After normalization, match with location context (same city or same zip code).
For **practice-level** dedup (not provider-level), also try matching the practice
name against provider last names ("Smith Eye Care" → likely matches "Dr. Smith").

Track `source_count` -- providers found across multiple sources are higher
confidence than those from a single source.
