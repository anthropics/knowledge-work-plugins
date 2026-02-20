# Reference Sources

## How reference sources work

Skills in this plugin check against **authoritative documents** — brand guidelines, contract templates, compliance standards, test policies, and more. This file defines where the canonical versions of those documents live.

**Why this matters:** If a skill needs to check a deliverable against "the brand guidelines," it should fetch the one true version — not search across drives and find 6 conflicting copies. Configure your sources here so every skill uses the same reference.

## How to configure

Replace the placeholder values below with your team's actual locations. Use whatever URL format your document platform supports:

- **Google Drive:** `https://drive.google.com/drive/folders/<folder-id>` or `gdrive://<path>`
- **SharePoint:** `https://<tenant>.sharepoint.com/sites/<site>/Shared Documents/<path>`
- **Confluence:** `https://<instance>.atlassian.net/wiki/spaces/<space>/pages/<page-id>`
- **Local repo:** `repo://path/to/file.md` (relative to project root)
- **Figma:** `https://www.figma.com/file/<file-id>`
- **Notion:** `https://www.notion.so/<page-id>`

Leave rows you don't use. Add rows for domains specific to your team.

## Reference source table

<!-- Replace <PLACEHOLDER> values with your team's actual locations -->
<!-- Delete rows for domains you don't use -->
<!-- Add rows for any additional domains your team needs -->

| Domain | Reference Name | Location | Notes |
|--------|---------------|----------|-------|
| **Brand** | Brand Guidelines | `<BRAND_GUIDELINES_URL>` | Logo usage, color palette, typography, voice & tone |
| **Brand** | Visual Asset Library | `<VISUAL_ASSETS_URL>` | Approved logos, icons, photography |
| **Legal** | Contract Templates | `<CONTRACT_TEMPLATES_URL>` | Master service agreements, NDAs, SOWs |
| **Legal** | Privacy Policy Template | `<PRIVACY_POLICY_URL>` | GDPR/CCPA compliant template |
| **Compliance** | SOC 2 Control Matrix | `<SOC2_CONTROLS_URL>` | Current control descriptions and evidence |
| **Compliance** | Regulatory Requirements | `<REGULATORY_REQUIREMENTS_URL>` | Industry-specific compliance checklist |
| **Design** | Design System / Component Library | `<DESIGN_SYSTEM_URL>` | Approved components, spacing, interaction patterns |
| **Design** | Accessibility Standards | `<ACCESSIBILITY_STANDARDS_URL>` | WCAG level, testing requirements |
| **Code** | Testing Standards | `<TESTING_STANDARDS_URL>` | Coverage thresholds, test naming, CI/CD policies |
| **Code** | Architecture Decision Records | `<ADR_URL>` | Approved patterns, technology choices |
| **Product** | Product Requirements Template | `<PRD_TEMPLATE_URL>` | Standard format for specs and briefs |
| **Product** | Roadmap / Priorities | `<ROADMAP_URL>` | Current quarter priorities and OKRs |
| **Finance** | Report Template | `<FINANCE_TEMPLATE_URL>` | Standard format for financial reports |
| **Finance** | Chart of Accounts | `<CHART_OF_ACCOUNTS_URL>` | Account structure and naming conventions |
| **HR** | Policy Handbook | `<HR_POLICY_URL>` | Employee policies, org standards |
| **Marketing** | Campaign Brief Template | `<CAMPAIGN_TEMPLATE_URL>` | Standard format for campaign briefs |
| **Marketing** | Content Style Guide | `<CONTENT_STYLE_GUIDE_URL>` | Writing style, terminology, messaging |

## Instructions for skills

All skills in this plugin should follow this process:

1. **Before searching for reference documents**, check this table for a configured source in the relevant domain
2. **If a source is configured**, fetch the document from the specified location — this is the canonical version
3. **If a source is a placeholder** (contains `<` and `>`), skip it — the team hasn't configured this domain yet
4. **If no source is configured**, ask the user: "Do you have a reference document for [domain]? If so, share it or add it to REFERENCES.md for future runs."
5. **Never search independently** for a document that has a configured source — the configured version is authoritative
