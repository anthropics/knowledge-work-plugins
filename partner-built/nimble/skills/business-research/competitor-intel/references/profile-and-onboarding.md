# Profile & Onboarding

The business profile at `~/.nimble/business-profile.json` and first-run setup flow.

---

## Profile Schema

```json
{
  "company": {
    "name": "Acme Corp",
    "domain": "acme.com",
    "description": "Enterprise SaaS platform for project management"
  },
  "industry_keywords": ["project management software", "team collaboration SaaS"],
  "competitors": [
    { "name": "WidgetCo", "domain": "widgetco.com", "category": "project-mgmt" },
    { "name": "GizmoTech", "domain": "gizmotech.io", "category": "project-mgmt" }
  ],
  "preferences": {
    "skip_competitors": [],
    "output_format": "bullet-points"
  },
  "integrations": {
    "notion": { "reports_page_id": "" },
    "slack": { "channel": "" }
  },
  "sales_context": {
    "key_differentiators": [
      "Only platform with real-time web data access",
      "Sub-second API response times"
    ],
    "integration_partners": [
      { "name": "DataStack", "type": "data warehouse" },
      { "name": "CRMHub", "type": "CRM" }
    ],
    "case_studies": [
      { "customer": "Large enterprise retailer", "industry": "retail", "outcome": "3x faster competitive intel" }
    ],
    "common_objections": [
      { "objection": "We already use [competitor]", "response": "Our real-time data is fresher — most competitors cache for 24h+" }
    ]
  },
  "last_runs": {
    "competitor-intel": "2026-03-20T14:30:00Z",
    "meeting-prep": "2026-03-22T09:00:00Z"
  },
  "setup_completed": true
}
```

## Reading the Profile

At the start of every skill run:

```bash
cat ~/.nimble/business-profile.json 2>/dev/null
```

If missing or empty → trigger onboarding (see below).

Key fields:
- `company.name` / `company.domain` — the user's company
- `competitors` — tracked competitors with domains and categories
- `industry_keywords` — for industry-level searches
- `preferences.skip_competitors` — competitors to exclude
- `last_runs.{skill-name}` — timestamp for time-aware searches
- `sales_context` — value positioning data (differentiators, integrations, case studies, objections)
- `integrations` — Notion/Slack config for report distribution

## Updating the Profile

**After every skill run** — update `last_runs`:

```python
import json, datetime, os
path = os.path.expanduser("~/.nimble/business-profile.json")
with open(path, "r") as f:
    profile = json.load(f)
profile["last_runs"]["skill-name"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
with open(path, "w") as f:
    json.dump(profile, f, indent=2)
```

**On user correction** — apply immediately:

| User says | Action |
|-----------|--------|
| "Don't include CompanyX" | Add to `preferences.skip_competitors` |
| "Also track CompanyY" | Add to `competitors` (with domain + category) |
| "I moved to NewCompany" | Update `company` |
| "Show me more detail" | Update `preferences.output_format` |

Always confirm: "Got it — removed CompanyX from tracking."

**Rules:**
- Never overwrite the whole file. Read → modify → write.
- Preserve unknown fields.
- Handle missing file gracefully → trigger onboarding.
- JSON only, always valid.

---

## First-Run Onboarding

### Prerequisite Checks

The preflight pattern in `nimble-playbook.md` runs `nimble --version`. Parse its
output to check three things: installed, minimum version, and API key.

**Minimum CLI version: 0.8.0**

#### CLI missing (command not found)

Don't just tell the user to install — guide them through it:

1. Check if npm is available: `npm --version`
2. If npm exists:
   > "The Nimble CLI is required. I'll install it now."
   >
   > Run: `npm install -g @nimbleway/cli`
3. If npm is not available:
   > "The Nimble CLI requires Node.js/npm. Install Node.js first from
   > [nodejs.org](https://nodejs.org), then run: `npm install -g @nimbleway/cli`"
4. After install, verify: `nimble --version`
5. If verification fails, stop and ask the user to check their PATH.

#### CLI outdated (version < 0.8.0)

Parse the version from `nimble --version` output. If below 0.8.0:

> "Your Nimble CLI is version **[current]** — version **0.8.0+** is required
> for these skills. Upgrading now..."
>
> Run: `npm update -g @nimbleway/cli`

Verify after upgrade: `nimble --version`. If still outdated, suggest:
`npm uninstall -g @nimbleway/cli && npm install -g @nimbleway/cli`

#### API key not set

> You need a Nimble API key.
> 1. Go to [app.nimbleway.com](https://app.nimbleway.com) → API Keys
> 2. Generate a new key
> 3. Run: `export NIMBLE_API_KEY=your_key_here`
> 4. Add to `~/.zshrc` or `~/.bashrc` to make permanent.

After the user sets it, verify: `echo "NIMBLE_API_KEY=${NIMBLE_API_KEY:+set}"`

#### API key expired (401)

> Your key may have expired (72h TTL). Regenerate at app.nimbleway.com > API Keys.

#### All prerequisites met

Only proceed to Company Setup once CLI is installed, version is >= 0.8.0, and API key
is set. Don't silently skip any check.

### Company Setup (2 prompts max)

**Prompt 1** — ask in plain text (NOT AskUserQuestion with options):

> "What's your company's website domain? (e.g., acme.com)"

Verify — make two Bash calls simultaneously:
- `nimble search --query "[domain]" --include-domain '["[domain]"]' --max-results 3 --search-depth lite`
- `nimble search --query "[domain] company" --max-results 5 --search-depth lite`

Present what you found and confirm: "I found that **[Company]** ([domain]) is
[brief description]. Is this the right company?"

**Prompt 2** — skill-specific setup:

- **competitor-intel:** Offer choice via `AskUserQuestion`:
  - **Find for me** — search and suggest competitors
  - **I'll list them** — user provides names

  If "Find for me", make three Bash calls simultaneously:
  - `nimble search --query "[Company] competitors" --max-results 10 --search-depth lite`
  - `nimble search --query "[Company] vs" --max-results 10 --search-depth lite`
  - `nimble search --query "[Company] alternatives" --max-results 5 --search-depth lite`

- **meeting-prep:** No extra setup — context comes per-meeting
- **company-deep-dive:** No extra setup — target company comes per-request

### Create Profile

```bash
mkdir -p ~/.nimble/memory/{competitors,people,companies,reports,positioning,synthesis}
```

Write `~/.nimble/business-profile.json` using the schema above.

When setting up competitors, infer or ask for each competitor's domain and category.
Also infer industry keywords from the company description.

### Profile Exists

Skip onboarding. Greet with context:
"Running competitor intel for **Acme Corp** — tracking **WidgetCo**, **GizmoTech**."

---

## Error Recovery

If any step fails:
1. Tell the user what went wrong in plain language
2. Provide the exact command to fix it
3. Offer to retry

Never silently skip setup steps.
