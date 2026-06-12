---
name: Catalog Steward
description: Master your Datasphere catalog governance—enrich metadata, manage glossaries, define KPIs, control tags, and analyze impact. Use this when you need to improve data discoverability, ensure consistent terminology, prevent governance chaos, validate KPI definitions, or assess change impacts before modifications. Triggers include "organize our catalog," "standardize metadata," "define business glossaries," "link our KPIs," "what breaks if we change this," and "which models use this table."
---

# Catalog Steward Skill

## Overview

The Catalog Steward skill empowers you to take control of your SAP Datasphere's internal data governance. This skill focuses on **enriching metadata, managing business glossaries, defining KPIs, controlling tag taxonomies, and performing lineage-based impact analysis**—all essential for enabling self-service analytics and preventing governance chaos.

Unlike the Data Product Publisher skill (which publishes external marketplace products), the Catalog Steward skill is about making your *internal* Datasphere repository discoverable, understandable, and trustworthy. When users search your catalog, they should find well-named assets with clear descriptions, consistent business terminology, quality metrics, and transparent lineage.

### Why Catalog Governance Matters

- **Self-Service Analytics:** Business users can find and trust data without submitting tickets
- **Compliance & Auditability:** Clear lineage and ownership trails support regulatory requirements
- **Impact Analysis:** Understand change ripple effects before modifying critical assets
- **Terminology Alignment:** Glossaries ensure "Revenue" means the same thing across teams
- **Data Quality Transparency:** Quality scores help users select the right datasets
- **Governance at Scale:** Consistent metadata reduces technical debt and tribal knowledge

---

## Core Workflows

### 1. Metadata Enrichment

Metadata enrichment transforms technical asset names and sparse descriptions into discoverable, business-friendly documentation.

#### Workflow: Analyze and Suggest Business-Friendly Names

**When to use:** During onboarding, after importing source system tables, or during catalog cleanup sprints.

**Steps:**

1. **Search for undernamed assets:**
   - Use `search_catalog` to find tables/views with missing or cryptic names (e.g., "T_SALES_001")
   - Filter by asset type (Dimension, Fact, View, Model)
   - Identify candidates for enrichment

2. **Analyze content with column inspection:**
   - Use `get_asset_details` to inspect table/view structure
   - Review key columns to infer business meaning
   - Identify primary dimensions and measures
   - Example: "T_SALES_001" contains `CUST_ID`, `ORDER_DT`, `AMOUNT` → suggests "Customer Orders Fact"

3. **Suggest and apply business names:**
   - Map technical names to business-friendly alternatives
   - Follow naming conventions (see references for templates)
   - Apply updated names via catalog metadata endpoints
   - Document rationale in internal notes

**Best Practices:**

- Include plural nouns for fact tables, singular for dimensions
- Use business domain terminology (not IT jargon)
- Avoid ambiguity: "Sales" → "Monthly Sales Orders" or "Daily Sales Revenue"
- Create a naming convention document and version it

#### Workflow: Write Meaningful Descriptions

**When to use:** When onboarding new users, before publishing catalog assets, or during quality audits.

**Steps:**

1. **Gather context:**
   - Use `get_asset_details` to extract technical metadata
   - Review related objects (upstream sources, downstream consumers)
   - Identify responsible team or owner

2. **Write descriptions following a template:**
   - **What:** One-sentence summary of what the asset contains
   - **Why:** Business purpose or use case
   - **Key columns:** 2-3 most important dimensions/measures
   - **Refresh frequency:** How often is it updated
   - **Caveats:** Data quality issues, exclusions, or limitations
   - Example template (see references)

3. **Link to upstream sources:**
   - Document source systems or parent tables
   - Use `get_object_definition` to trace lineage
   - Include transformation logic (if relevant)

4. **Review and version:**
   - Have data owner approve descriptions
   - Track description changes in catalog versioning

**Best Practices:**

- Keep descriptions under 500 words; link to detailed documentation elsewhere
- Use plain language; assume audience is business analyst (not DBA)
- Include examples of typical queries or use cases
- Flag experimental or deprecated assets clearly
- Update descriptions when business meaning changes (not just when data structure changes)

#### Workflow: Auto-Suggest Tags Based on Content Analysis

**When to use:** During bulk catalog onboarding or when implementing a new tag taxonomy.

**Steps:**

1. **Analyze asset content:**
   - Use `get_asset_details` to inspect column names, types, and distributions
   - Use `analyze_column_distribution` to understand data characteristics
   - Identify data types (financial, HR, product, customer, operational)
   - Detect common patterns (dates, IDs, amounts)

2. **Match against tag taxonomy:**
   - Map identified characteristics to your tag taxonomy (see references)
   - Example: columns contain "SALARY", "EMPLOYEE_ID" → suggest tags: `hr`, `sensitive`, `employee-master`

3. **Propose tags with confidence scoring:**
   - High confidence: tags match multiple column patterns
   - Medium confidence: tags match domain or naming conventions
   - Low confidence: tags are contextual or require human review

4. **Review and apply:**
   - Present suggestions with reasoning
   - Allow manual override for edge cases
   - Batch-apply approved tags

**Best Practices:**

- Use a controlled vocabulary (see tag taxonomy in references)
- Combine multiple tag types (domain, sensitivity, cadence, owner)
- Review auto-suggestions; don't apply blindly
- Document why assets receive specific tags
- Update tags when asset usage patterns change

#### Workflow: Bulk Metadata Updates Across Multiple Assets

**When to use:** After organizational changes, standardization initiatives, or when implementing governance policies.

**Steps:**

1. **Identify batch scope:**
   - Use `list_catalog_assets` to find assets matching criteria (e.g., all tables from a source system, all models owned by a team)
   - Validate that batch scope is correct (test with small sample first)

2. **Define update template:**
   - Standardize naming patterns, tags, descriptions, or ownership
   - Create template for changes (see references)
   - Document change rationale and approval

3. **Execute updates in phases:**
   - Phase 1: Apply changes to test/sandbox catalogs
   - Phase 2: Validate against downstream consumers using lineage
   - Phase 3: Apply to production with versioning
   - Phase 4: Communicate changes to users

4. **Track and audit changes:**
   - Log all bulk changes with timestamp, author, and reason
   - Enable catalog versioning to support rollback if needed
   - Notify affected teams of changes

**Best Practices:**

- Always test bulk updates on a sample first
- Use lineage analysis to identify downstream impacts
- Batch updates by logical group (not random collections)
- Communicate timing and rationale to stakeholders
- Provide before/after comparisons for major changes

---

### 2. Glossary Term Management

A business glossary is the "source of truth" for terminology. It ensures that "Gross Margin," "EBITDA," and "Market Share" mean the same thing across all teams.

#### Workflow: Create and Maintain a Business Glossary

**When to use:** At governance program launch, when onboarding new business domains, or when terminology conflicts arise.

**Steps:**

1. **Identify core business concepts:**
   - Interview business owners and analysts
   - Review existing reports, dashboards, and analysis
   - Document terms with multiple definitions (conflicts to resolve)
   - Prioritize high-impact terms (used in multiple models, KPIs, or reports)

2. **Create glossary term entries:**
   - Use the glossary term template (see references)
   - Define each term with business meaning, not technical definition
   - Include approved synonyms and related terms
   - Document calculation methodology (for metrics)
   - Assign owner and approval authority
   - Set version and last-reviewed date

3. **Build glossary hierarchy:**
   - Group terms by business domain (Sales, Finance, HR, Operations)
   - Create parent-child relationships (e.g., "Revenue" → "Product Revenue", "Service Revenue")
   - Link related terms (see section on glossary relationships)

4. **Enable feedback and evolution:**
   - Publish draft glossary and collect feedback from stakeholders
   - Review conflicts and make approval decisions
   - Version published glossary (v1.0, v1.1, etc.)
   - Schedule annual reviews with business owners

**Best Practices:**

- Start with 20-30 highest-impact terms, not the entire organization
- Involve business owners, not just IT, in definition
- Make glossary searchable and always discoverable (don't hide in PDFs)
- Include usage examples and anti-examples (what it is NOT)
- Document historical changes (why did definition change?)
- Link to actual data implementations (models, measures)

#### Workflow: Link Glossary Terms to Technical Assets

**When to use:** After glossary terms are approved, during model development, or during metadata enrichment sprints.

**Steps:**

1. **Identify linking opportunities:**
   - Use `search_catalog` to find assets matching glossary terms
   - Example: search for "revenue" → find all views, models, measures with revenue-related logic
   - Use `get_asset_details` to inspect calculated fields and measures

2. **Create term-to-asset mappings:**
   - Link glossary term "Revenue" to measure `TOTAL_REVENUE` in model `Sales_Summary`
   - Document how technical asset implements the glossary definition
   - Capture calculation logic or transformation rules
   - Note any deviations or approximations

3. **Enable bidirectional navigation:**
   - Users viewing glossary term should see which assets implement it
   - Users viewing assets should see which glossary terms apply
   - Create cross-reference views or dashboards

4. **Validate consistency:**
   - Check that all uses of the term apply the same definition
   - Flag deviations or variant calculations
   - Schedule reviews when definitions or implementations change

**Best Practices:**

- One glossary term can map to multiple technical assets (same concept, different contexts)
- Document if an asset implements the term exactly or is an approximation
- Include transformation rules or calculation logic in the mapping
- Update mappings when either glossary terms or asset definitions change
- Use mappings to detect duplicate or conflicting implementations

#### Workflow: Term Approval Workflows

**When to use:** When implementing formal governance, during terminology disputes, or when adding new glossary terms.

**Steps:**

1. **Define approval roles:**
   - **Proposer:** Business analyst or data owner
   - **Domain Owner:** Accountable for terms in their domain (Sales, Finance, etc.)
   - **Governance Lead:** Final approval authority
   - Use RACI matrix (see references) to clarify roles

2. **Create proposal-to-approval workflow:**
   - Proposer submits term with definition, calculation, and rationale
   - Domain owner reviews for alignment with business standards
   - Governance lead checks for conflicts, clarity, and compliance
   - Feedback is provided; proposer revises if needed
   - Final approval records who, when, and rationale

3. **Track approval status:**
   - Status: Draft → Proposed → Approved → Published
   - Escalation path for disputes (which executive resolves conflicts?)
   - SLA for reviews (e.g., 5 business days)

4. **Manage versioning:**
   - When a term definition changes, trigger re-approval
   - Previous versions remain available (audit trail)
   - Notify users when definitions change

**Best Practices:**

- Clarify approval authority upfront (don't create bottlenecks)
- Use lightweight workflow for low-risk terms, formal workflow for KPIs or financial terms
- Document why terms were rejected (helps future proposals)
- Include legal or compliance review for regulatory terms
- Set clear SLAs to prevent indefinite reviews

#### Workflow: Glossary Hierarchies and Relationships

**When to use:** As glossary grows beyond 30-50 terms, when standardizing across domains, or when implementing enterprise-wide terminology.

**Steps:**

1. **Design hierarchical structure:**
   - Create top-level categories (Business Domains: Finance, Sales, HR, etc.)
   - Create sub-categories (Finance → Revenue, Expenses, Assets)
   - Create specific terms (Revenue → Product Revenue, Service Revenue)
   - Support 2-3 levels of depth (too deep = hard to navigate)

2. **Define relationship types:**
   - **Synonym:** Alternative names for the same concept (e.g., "Gross Profit" = "Gross Margin")
   - **Related:** Conceptually connected but distinct (e.g., "Revenue" related to "Cost of Goods Sold")
   - **Parent-Child:** Hierarchical containment (e.g., "Revenue" ← "Product Revenue")
   - **Derived:** One term calculated from others (e.g., "Profit Margin" derived from "Profit" and "Revenue")

3. **Build navigation paths:**
   - Enable browsing by domain (discover all financial terms)
   - Enable searching across domains (find all revenue-related terms)
   - Create "Related Terms" suggestions on term detail pages
   - Build term dependency maps for KPI validation

4. **Maintain consistency:**
   - Review hierarchies during governance reviews
   - Consolidate synonyms and related terms to reduce duplication
   - Update relationships when definitions change

**Best Practices:**

- Don't create deep trees (3+ levels); use relationships instead
- Document relationship semantics (what makes two terms "related"?)
- Use hierarchies to organize domains, not to create arbitrary classification
- Enable free-text search as primary discovery mechanism
- Use term relationships to detect definition conflicts

#### Workflow: Ensure Consistent Terminology Across the Organization

**When to use:** During governance audits, when merging business units, or when enforcing standards.

**Steps:**

1. **Audit current terminology:**
   - Search catalog for variant names and definitions (e.g., "Revenue", "Sales", "Turnover", "Top Line")
   - Interview teams to understand why variants exist
   - Use `search_catalog` to find all objects using each variant
   - Document conflicts in a consolidation backlog

2. **Resolve conflicts through glossary:**
   - For each conflict, create a single approved glossary term
   - Declare one variant as canonical; others as synonyms
   - Document why this definition was chosen
   - Get stakeholder approval before enforcement

3. **Enforce consistency:**
   - Link all variant implementations to approved glossary term
   - Update descriptions/names in catalog to use approved terminology
   - Add metadata (tags) to identify which implementations are authoritative vs. legacy
   - Deprecate non-conforming implementations gradually

4. **Ongoing audits:**
   - Schedule quarterly reviews of new assets for terminology alignment
   - Audit popular models/views for consistent term usage
   - Include terminology checklist in data product publishing workflow

**Best Practices:**

- Enforce consistency gradually (phase out old terms over 6-12 months)
- Document migration path for teams using old terminology
- Recognize that business language evolves; update glossary annually
- Use glossary to enforce standards, not to restrict valid language
- Support common synonyms as alternate search terms

---

### 3. KPI (Key Performance Indicator) Definition

KPIs translate business objectives into measurable metrics. The catalog ensures KPIs are well-defined, validated against data, and linked to accountability.

#### Workflow: Define KPIs Within the Catalog

**When to use:** When launching new strategic initiatives, during business planning cycles, or when formalizing informal metrics.

**Steps:**

1. **Gather KPI requirements:**
   - Interview executive sponsors and business owners
   - Document strategic objective each KPI supports
   - Define calculation methodology (detailed formula)
   - Identify refresh cadence (daily, weekly, monthly)
   - Assign accountability (who owns this KPI?)
   - Define target/threshold values

2. **Create KPI definition using template (see references):**
   - **Name:** Business-friendly name (e.g., "Customer Lifetime Value")
   - **Code:** Unique identifier (e.g., "CLV_001")
   - **Strategic Objective:** Which business goal does this KPI support?
   - **Definition:** Plain-language description
   - **Calculation:** Detailed formula with logic
   - **Dimensions:** How is KPI sliced? (by customer segment, region, product, time)
   - **Data Sources:** Which tables/models feed this KPI?
   - **Owner:** Who is accountable?
   - **Review Frequency:** When is this KPI reviewed?
   - **Version:** Creation date and change log

3. **Validate against data landscape:**
   - Use `get_asset_details` to inspect source tables
   - Use `analyze_column_distribution` to check data availability and quality
   - Verify required dimensions/measures exist
   - Document any data gaps or approximations

4. **Publish and socialize:**
   - Create KPI detail page in catalog with calculation visible
   - Share KPI definition with stakeholders
   - Link to dashboards/reports that use this KPI
   - Establish governance (who approves changes?)

**Best Practices:**

- Keep KPI definitions simple; complexity breeds misunderstanding
- Include examples: "If X happened, would KPI increase or decrease?"
- Document known limitations and caveats (e.g., "excludes international operations")
- Version KPI definitions; don't silently change calculations
- Link KPI to glossary terms for consistency

#### Workflow: Link KPIs to Underlying Datasets and Measures

**When to use:** During KPI validation, when optimizing data models, or when documenting lineage.

**Steps:**

1. **Map KPI to source measures:**
   - Use `get_object_definition` to inspect model structure
   - Identify which measures feed each KPI calculation
   - Example: KPI "Profit Margin" uses measures `Total_Profit` and `Total_Revenue`
   - Document transformation logic (if any)

2. **Trace lineage to source systems:**
   - Use `list_catalog_assets` or lineage analysis to trace back to source tables
   - Document data flow: Source System → ETL → Model → Measure → KPI
   - Identify any data transformations or aggregations
   - Document refresh timing at each stage

3. **Create bidirectional links:**
   - KPI detail page shows source measures
   - Measure detail page shows which KPIs consume it
   - Enable impact analysis: "change this measure → affects these KPIs"

4. **Validate availability and completeness:**
   - Ensure all required source columns exist
   - Check that historical data is available for trending
   - Verify refresh frequency supports KPI review cycle
   - Document any data quality issues in lineage

**Best Practices:**

- Map each KPI to its smallest constituent measures (enables reuse)
- Document assumptions in data flow (e.g., "excludes canceled orders")
- Use lineage to identify shared dependencies (optimization opportunities)
- Automate lineage updates when data models change
- Create data dictionaries linking business metrics to technical measures

#### Workflow: KPI Ownership and Accountability

**When to use:** During KPI launch, during governance reviews, or when resolving KPI disputes.

**Steps:**

1. **Assign clear ownership:**
   - **KPI Owner:** Accountable for definition and business interpretation (executive)
   - **Data Owner:** Accountable for underlying data quality (data team)
   - **Dashboard Owner:** Accountable for reporting infrastructure (BI team)
   - Use RACI matrix (see references) to clarify secondary responsibilities

2. **Document ownership in catalog:**
   - Assign owner to KPI definition with contact information
   - Create KPI ownership matrix (spreadsheet or dashboard)
   - Link KPI to team or department
   - Document escalation path for KPI disputes

3. **Enable accountability:**
   - Schedule monthly KPI reviews with owners
   - Track KPI performance trends
   - Document explanations when KPIs miss targets
   - Use KPI dashboards to highlight performance issues early

4. **Rotate and transition ownership:**
   - When owner changes roles, assign replacement
   - Document transition in KPI versioning
   - Provide new owner with calculation documentation and historical context

**Best Practices:**

- Assign single accountable owner (not a committee)
- Ensure owner has authority to make decisions about KPI
- Connect KPI ownership to performance management/compensation (creates accountability)
- Review ownership quarterly; update when roles change
- Document succession plan for critical KPI owners

#### Workflow: KPI Validation

**When to use:** Before publishing KPIs, during data quality issues, or when results seem suspicious.

**Steps:**

1. **Validate calculation logic:**
   - Walk through calculation step-by-step
   - Check for logic errors (incorrect operators, filters, aggregations)
   - Verify dimensional alignment (are dimensions aggregated correctly?)
   - Test with known scenarios (e.g., "if all customers had 100 orders, KPI should be X")

2. **Validate data quality:**
   - Use `analyze_column_distribution` on source columns
   - Check for missing values, outliers, or data quality issues
   - Validate assumptions (e.g., "all dates are in YYYY-MM-DD format")
   - Review data freshness: is data current enough for KPI?

3. **Validate against reality:**
   - Compare KPI results to manual calculations (if available)
   - Run KPI on historical data; check for expected trends
   - Benchmark against external data if available (e.g., compare "Market Share" KPI to published reports)
   - Interview business owners: "does this number feel right?"

4. **Document validation results:**
   - Create validation report (see references)
   - Document any discrepancies and their root causes
   - Establish data quality requirements for KPI use
   - Define KPI confidence level (trusted, needs monitoring, experimental)

5. **Set up ongoing monitoring:**
   - Create KPI quality dashboard (shows data freshness, completeness, outliers)
   - Set up alerts for data quality issues
   - Schedule monthly validation checks
   - Document changes to source data that might affect KPI

**Best Practices:**

- Never publish KPI without validation
- Include data quality caveats in KPI definition
- Validate with business owners, not just data teams
- Document validation assumptions (so others can replicate)
- Schedule re-validation when source data changes significantly

#### Workflow: KPI Lifecycle Management

**When to use:** When KPIs become irrelevant, during business strategy reviews, or when merging business units.

**Steps:**

1. **Establish KPI lifecycle states:**
   - **Proposed:** New KPI being evaluated
   - **Active:** Currently tracked and reviewed
   - **Monitored:** Less critical but still watched
   - **Deprecated:** Phased out or replaced by newer KPI
   - **Archived:** Historically important, no longer used

2. **Transition KPIs through lifecycle:**
   - Proposed → Active: After validation and stakeholder approval
   - Active → Deprecated: When business objective changes or KPI becomes outdated
   - Deprecated → Archived: After 6-12 month sunset period
   - Document reason and date for each transition

3. **Manage sunset of deprecated KPIs:**
   - Communicate sunset date to stakeholders well in advance
   - Identify replacement KPI (if applicable)
   - Provide training on new KPI
   - Archive old dashboards/reports gradually
   - Keep historical data accessible for trend analysis

4. **Review and refresh KPI portfolio:**
   - Conduct annual KPI portfolio review
   - Assess each KPI: Still aligned with strategy? Still accurate? Still relevant?
   - Identify KPIs for deprecation
   - Identify new KPIs needed for emerging priorities

**Best Practices:**

- Document why KPIs were deprecated (important context for future teams)
- Don't delete KPI definitions; archive them with historical data
- Communicate KPI changes to all stakeholders early
- Link deprecated KPI to replacement (if applicable)
- Review KPI portfolio annually, not ad hoc

---

### 4. Tag Management

Tags are lightweight metadata that enable discovery and governance. A well-designed tag taxonomy makes the catalog navigable at scale.

#### Workflow: Design a Tag Taxonomy

**When to use:** At governance program launch or when current tagging scheme becomes unwieldy.

**Steps:**

1. **Define tag categories:**
   - **Domain Tags:** Business domain (Finance, Sales, HR, Operations, Product)
   - **Sensitivity Tags:** PII, Confidential, Internal, Public
   - **Cadence Tags:** Real-time, Daily, Weekly, Monthly, Ad-hoc
   - **Owner/Team Tags:** Owned_by_Finance, Owned_by_Sales, etc.
   - **Quality Tags:** Certified, Under_Review, Experimental, Legacy
   - **Use Case Tags:** KPI, Reporting, Analysis, AI/ML, Regulatory
   - See references for detailed taxonomy design patterns

2. **Create controlled vocabulary:**
   - Define each tag with clear definition
   - Document when to use each tag (vs. related tags)
   - Establish naming convention (lowercase, no spaces, hyphens for compound terms)
   - Example: Use `hr-employee-master` not `HR Employee Master` or `hr_emp_master`

3. **Design hierarchy (if needed):**
   - Flat hierarchy: Simple tag list, good for small catalogs (<100 assets)
   - Hierarchical: Parent/child relationships, good for large catalogs (>500 assets)
   - Example hierarchy: `domain:finance`, `domain:finance:accounting`, `domain:finance:revenue`

4. **Publish and train:**
   - Create tag guide with examples
   - Train data owners on tagging conventions
   - Publish tag definitions in easily searchable location
   - Include tag guide in onboarding documentation

**Best Practices:**

- Start simple; expand tags over time
- Limit tag count (20-50 active tags); too many defeats discovery
- Use domain category heavily; use other categories sparingly
- Don't use tags for information that should be in descriptions
- Review tags quarterly; consolidate if duplicates emerge
- See references for industry-specific tag examples

#### Workflow: Apply Tags Consistently Across Assets

**When to use:** During catalog onboarding, in metadata enrichment sprints, or during quality audits.

**Steps:**

1. **Define tagging standards:**
   - Which asset types get tagged? (tables, views, models, measures)
   - How many tags per asset? (typically 3-5)
   - Which tag categories are mandatory? (e.g., domain, sensitivity)
   - What approval is needed? (self-service vs. peer review)

2. **Apply tags systematically:**
   - Use `list_catalog_assets` to find untagged or under-tagged assets
   - Apply domain tag based on asset purpose
   - Apply sensitivity tag based on data content (PII, financial, health, etc.)
   - Apply cadence tag based on refresh frequency
   - Apply quality tag based on readiness level

3. **Document tagging decisions:**
   - For each asset, document why specific tags were applied
   - Include examples in tag definition (to ensure consistent interpretation)
   - Review tagging periodically; adjust tags if meanings change

4. **Enable peer review:**
   - Have data owner review proposed tags
   - Tag changes should be visible in audit trail
   - Create dashboard showing tagging coverage (% of assets with required tags)

**Best Practices:**

- Tag all new assets before publishing to catalog
- Use tags to enforce governance (e.g., all PII data must have `sensitivity:pii` tag)
- Don't over-tag; too many tags reduce usability
- Keep tag count consistent (don't tag one asset with 2 tags and another with 20)
- Review tags when asset purpose or data changes

#### Workflow: Tag-Based Search and Discovery

**When to use:** When enabling self-service analytics or building faceted search interfaces.

**Steps:**

1. **Enable tag-based filtering:**
   - Use `search_catalog` with tag filters
   - Support multi-tag searches (e.g., "show all assets tagged `domain:finance` AND `sensitivity:internal`")
   - Support tag hierarchies in search (search for `domain:finance` returns all finance sub-tags)

2. **Create tag-based browsing:**
   - Create tag clouds or faceted navigation in catalog UI
   - Enable "related tags" suggestions (if browsing `domain:sales`, suggest `cadence:daily`)
   - Show tag frequency (how many assets have each tag?)

3. **Enable self-service discovery:**
   - Train users to search by tag (simpler than writing complex queries)
   - Create tag guides for different personas (executives, analysts, engineers)
   - Build dashboards that link tags to data discovery metrics

4. **Track usage patterns:**
   - Monitor which tags are most searched
   - Identify unused tags (candidates for removal)
   - Use search analytics to refine tagging strategy

**Best Practices:**

- Make tag search as prominent as free-text search
- Enable "did you mean" suggestions for similar tags
- Show tag-based recommendations (users viewing asset with tag X also viewed assets with tag Y)
- Use tag search to validate tagging strategy (if tags aren't searched, reconsider their value)
- Create saved tag searches for common discovery patterns

#### Workflow: Tag Governance

**When to use:** When tagging decisions affect multiple teams, when enforcing compliance, or when implementing self-service governance.

**Steps:**

1. **Define tagging authority:**
   - Who can create new tags? (centralized: only governance team; decentralized: domain teams with approval)
   - Who can apply tags? (any asset owner; or only owners of sensitive assets)
   - Who can modify or delete tags? (governance team only)
   - Document process in governance policy

2. **Implement approval workflows (if needed):**
   - For sensitive tags (PII, Financial) or compliance tags, require approval
   - Asset owner proposes tags; governance team reviews and approves
   - Approval captures who approved and timestamp
   - Rejected tags include feedback for why

3. **Monitor tagging compliance:**
   - Create dashboard showing tagging coverage by domain/team
   - Flag assets missing required tags (domain, sensitivity)
   - Monthly tagging audit: review high-change assets
   - Identify teams with inconsistent tagging practices

4. **Enforce tagging standards:**
   - Prevent publishing of assets without required tags
   - Create alerts for untagged or mis-tagged sensitive assets
   - Include tagging checklist in data product publishing workflow
   - Tie tagging compliance to team scorecards (if appropriate)

**Best Practices:**

- Keep tagging lightweight; heavy approval workflows reduce adoption
- Tag sensitive assets with higher approval rigor
- Enable bulk tag application (don't require tagging each asset individually)
- Provide clear feedback when tagging violates standards
- Review tagging governance quarterly

---

### 5. Lineage and Impact Analysis

Understanding data lineage answers critical questions: "Where does this data come from?" "Which models consume this table?" "What breaks if I change this column?"

#### Workflow: Use Impact and Lineage Analysis to Trace Data Flows

**When to use:** Before modifying critical tables, during root cause analysis of data issues, or when documenting data flows.

**Steps:**

1. **Access lineage tools:**
   - Use `get_object_definition` to inspect asset structure
   - Use `list_catalog_assets` with lineage context to identify related assets
   - Access Datasphere lineage visualization (typically in asset detail page)
   - Filter lineage by direction (upstream, downstream, bidirectional)

2. **Trace upstream lineage:**
   - Start from asset of interest (e.g., a model or measure)
   - Follow lineage upstream to source tables
   - Identify transformations at each step
   - Document assumptions and business logic in transformations
   - Example: Model_Sales → View_Sales_Orders → Table_ORDERS (SAP source)

3. **Trace downstream lineage:**
   - Start from table or view
   - Follow lineage downstream to consuming models, measures, KPIs
   - Identify all downstream impacts (critical for change assessment)
   - Example: Table_CUSTOMERS → View_Customer_Enriched → Model_Customer_Analytics → KPI_Churn_Rate

4. **Analyze bidirectional flows:**
   - Identify circular dependencies (should be rare)
   - Find shared data flows (tables consumed by multiple models)
   - Identify choke points (tables with many downstream consumers)
   - Document data flow bottlenecks

5. **Document lineage:**
   - Create lineage diagram showing major data flows
   - Document business logic at each transformation
   - Include metadata about refresh timing
   - Publish documentation with visual lineage

**Best Practices:**

- Lineage should be automatically captured; manually document only complex logic
- Include transformation rationale (not just "what" but "why")
- Document data quality changes through lineage (where does quality degrade?)
- Review lineage when source systems change
- Use lineage to identify optimization opportunities (redundant transformations, etc.)

#### Workflow: Generate Impact Reports

**When to use:** Before making changes to critical assets, during root cause analysis, or during governance audits.

**Steps:**

1. **Define change scope:**
   - Identify specific table, column, model, or measure being changed
   - Document nature of change (delete column, rename, change calculation, deprecate table)
   - Estimate impact scope (how many downstream assets affected?)
   - Assess impact severity (internal tools only vs. customer-facing dashboards)

2. **Generate impact analysis:**
   - Use lineage tools to identify all downstream consumers
   - Classify consumers by impact type:
     - **Direct:** Assets directly consuming the changed object
     - **Indirect:** Assets consuming direct consumers
     - **KPI:** KPIs affected by change
     - **Reports/Dashboards:** BI artifacts consuming changed assets
   - Identify affected stakeholders (which teams will feel impact?)

3. **Assess impact severity:**
   - For each impacted asset, assess:
     - **Criticality:** Is this a critical KPI? Customer-facing? Regulatory?
     - **Detectability:** Would broken data be noticed immediately or silently wrong?
     - **Blast Radius:** How many end users affected?
   - Document each assessment with rationale

4. **Create impact report:**
   - **Change Summary:** What is being changed and why?
   - **Downstream Impacts:** List all affected assets with severity
   - **Mitigation Plans:** How to minimize impact? (e.g., phased rollout, temporary shadow calculation)
   - **Testing Plan:** How to validate change doesn't break downstream?
   - **Rollback Plan:** How to revert if issue discovered?
   - **Stakeholder Notifications:** Which teams need to be informed?

5. **Use report to gain approvals:**
   - Share impact report with affected stakeholders
   - Get sign-off from asset owners before proceeding
   - Document approval (who approved, when, any conditions)
   - Update report as approvals gathered

**Best Practices:**

- Always generate impact report before modifying critical assets
- Use impact reports to surface hidden downstream dependencies
- Include indirect impacts (sometimes more important than direct)
- Define severity thresholds (when is impact too high?)
- Use impact analysis to identify opportunities to consolidate redundant implementations

#### Workflow: Upstream Analysis

**When to use:** When investigating data quality issues, understanding data freshness, or documenting data sources.

**Steps:**

1. **Trace back to original sources:**
   - Start from asset with issue (model, measure, or dashboard)
   - Follow lineage upstream to source tables
   - Identify each transformation step
   - Document data quality at each stage

2. **Identify source systems:**
   - For each upstream table, identify source system (SAP, Salesforce, custom app, etc.)
   - Document extraction frequency (real-time, batch, delayed)
   - Identify data quality issues in source (missing values, duplicates, delays)

3. **Analyze data quality degradation:**
   - Identify where data quality issues are introduced
   - Example: "Missing Customer Names in source → not populated in enriched view → shows as blanks in dashboard"
   - Document which transformations impact quality

4. **Identify opportunities to improve:**
   - Use upstream analysis to fix quality issues at source (better than downstream workarounds)
   - Identify redundant transformations that could be consolidated
   - Propose moving transformations closer to source (for efficiency)

**Best Practices:**

- Document source system characteristics (reliability, update frequency)
- Use upstream analysis to identify data quality root causes
- Periodically review upstream dependencies; document changes
- Build dashboards tracking data freshness across lineage
- Work with source system owners to improve data quality upstream

#### Workflow: Downstream Analysis

**When to use:** When deprecating assets, understanding asset usage, or during data quality investigations.

**Steps:**

1. **Identify all downstream consumers:**
   - Start from table, view, or measure
   - Trace forward to consuming models, measures, KPIs
   - Continue tracing to dashboards, reports, or AI/ML models
   - Use `list_catalog_assets` to identify all references

2. **Categorize downstream usage:**
   - **Critical:** KPIs, customer-facing dashboards, regulatory reports
   - **Important:** Internal dashboards, analyst-used models, operational reports
   - **Experimental:** Prototype dashboards, one-time analyses
   - Assess what happens if asset becomes unavailable

3. **Understand consumption patterns:**
   - Which downstream assets are actively used?
   - Which downstream assets are stale/unused? (candidates for cleanup)
   - Which measures appear in multiple KPIs? (indicates high leverage)
   - Which dashboards have most users? (highest-risk to break)

4. **Plan changes safely:**
   - For deprecation: Provide replacement assets before turning off original
   - For modifications: Test changes against actual downstream consumers
   - Communicate changes early to downstream owners
   - Build deprecation timeline that allows downstream adjustment

**Best Practices:**

- Use downstream analysis to understand asset criticality
- Identify "hidden" downstream consumers (often forgotten dependencies)
- Use downstream usage patterns to prioritize data governance efforts
- Periodically clean up unused downstream assets (reduces technical debt)
- Track downstream usage to validate data product adoption

#### Workflow: Change Impact Assessment Before Modifications

**When to use:** Before modifying any production asset, during data quality fixes, or during optimization projects.

**Steps:**

1. **Plan change:**
   - Document what is being changed (table structure, calculation logic, assumptions)
   - Document why change is needed (bug fix, performance, business requirement)
   - Document expected benefits and risks

2. **Analyze downstream impacts:**
   - Use downstream analysis workflow (above) to identify all consumers
   - Generate impact report (see above workflow)
   - Identify critical vs. non-critical impacts
   - Document stakeholders who need notification

3. **Design safe change approach:**
   - **Option 1 (No-Impact Approach):** Add new column/table; don't modify existing ones
   - **Option 2 (Backward-Compatible):** Support old and new logic simultaneously during transition
   - **Option 3 (Phased Rollout):** Change in phases; monitor for issues at each phase
   - **Option 4 (Temporary Shadow):** Run new logic alongside old; validate before switching
   - Choose approach based on risk and downstream impact

4. **Build testing plan:**
   - Test change in development/test environment first
   - Test with actual data volumes and realistic downstream consumption patterns
   - Validate that downstream assets still produce correct results
   - Document test cases and results

5. **Execute with monitoring:**
   - Apply change (in phases if using phased rollout)
   - Monitor downstream dashboards/reports for unexpected changes
   - Monitor data quality metrics (completeness, accuracy, freshness)
   - Have rollback plan ready
   - Document any issues discovered during rollout

6. **Communicate and document:**
   - Notify downstream stakeholders of change and any impacts
   - Document change in asset versioning/changelog
   - Update lineage documentation if data flows changed
   - Conduct post-mortem if issues discovered

**Best Practices:**

- Always analyze impact before change; never assume "no one will notice"
- Use phased or shadow approaches for high-risk changes
- Build automated tests to validate downstream assets after changes
- Keep rollback capability for at least 24-48 hours after change
- Review impact assessment process regularly; improve based on incidents

---

### 6. Data Quality Scoring and Tracking

Data quality scores help users select trustworthy datasets and identify improvement opportunities.

#### Workflow: Define Quality Dimensions and Scoring

**When to use:** During governance program launch or when implementing data quality initiatives.

**Steps:**

1. **Identify quality dimensions:**
   - **Completeness:** Are all required values present? (inverse of missing/null rates)
   - **Accuracy:** Do values match source of truth or business rules?
   - **Timeliness:** Is data fresh? How long since last update?
   - **Consistency:** Do related values align? (e.g., sum of parts = total)
   - **Uniqueness:** Are there unintended duplicates?
   - **Validity:** Do values match expected format/range?
   - See references for detailed scoring templates

2. **Define scoring methodology:**
   - For each dimension, establish measurement logic
   - Example Completeness: "Score = 100 * (non-null rows / total rows)"
   - Example Timeliness: "Score = 100 if updated in last 24 hours; decreases 5 points per day stale"
   - Document assumptions and edge cases
   - Establish minimum thresholds (e.g., Completeness must be ≥95%)

3. **Aggregate scores:**
   - Calculate overall quality score from dimension scores
   - Use weighted average if some dimensions more important (see references for templates)
   - Example: Overall = (Completeness * 30% + Accuracy * 30% + Timeliness * 25% + Consistency * 15%)
   - Establish overall quality tiers: Certified (90+), Trusted (80-89), Monitor (70-79), Issue (<70)

4. **Establish scorecard template:**
   - Create quality scorecard showing all dimensions
   - Include trends over time (are we improving or degrading?)
   - Document current blockers to achieving higher scores
   - Set improvement targets

**Best Practices:**

- Start with simple dimensions (completeness, timeliness); add advanced dimensions over time
- Base scores on automated measurements when possible (avoid manual scoring)
- Review scoring methodology quarterly; update if dimensions/thresholds change
- Communicate quality scores to all data consumers
- Link quality issues to root causes (helps with remediation)

#### Workflow: Score Assets on Quality Metrics

**When to use:** During metadata enrichment, when onboarding new data sources, or in quality audits.

**Steps:**

1. **Measure quality dimensions:**
   - Use `analyze_column_distribution` to assess completeness (what % of rows have values?)
   - Check timeliness (when was data last refreshed?)
   - Run validation rules to assess accuracy (do values meet business rules?)
   - Compare with source to assess consistency

2. **Calculate quality scores:**
   - For each dimension, calculate score using methodology from above
   - Aggregate dimension scores into overall quality tier
   - Document any assumptions or manual overrides
   - Identify root causes of low scores

3. **Assign quality tags:**
   - Tag assets with quality tier (Certified, Trusted, Monitor, Issue)
   - Tag assets with specific quality issues (duplicate_data, stale_data, missing_values, etc.)
   - Use tags to surface quality issues in catalog search

4. **Publish quality metadata:**
   - Add quality score and dimensions to asset detail page
   - Create quality dashboard showing scores across portfolio
   - Enable sorting/filtering by quality score
   - Show trend charts (is quality improving over time?)

**Best Practices:**

- Automate quality scoring; don't rely on manual assessments
- Review quality scores weekly or monthly (not annually)
- Link quality issues to improvement projects (make it actionable)
- Highlight quick wins (easy-to-fix quality issues)
- Recognize teams that improve data quality

#### Workflow: Quality Dashboards and Trending

**When to use:** When establishing quality culture, during quality improvement programs, or for executive visibility.

**Steps:**

1. **Build quality scorecards:**
   - Create dashboard showing quality scores across all assets
   - Show breakdown by domain (Finance, Sales, HR, etc.)
   - Show breakdown by source system or team
   - Display as heatmap or scorecard format

2. **Visualize trends over time:**
   - Track quality score trends (improving or degrading?)
   - Identify tables with declining quality (investigate why)
   - Celebrate tables with improving quality (recognize teams)
   - Use trends to justify investment in quality initiatives

3. **Enable drill-down analysis:**
   - Click table to see detailed quality metrics (dimension scores)
   - See which columns are causing low quality
   - View quality issues identified in validation rules
   - Link to remediation projects or tickets

4. **Use for accountability:**
   - Assign quality scorecards to team owners
   - Monthly review of team's quality scorecard
   - Tie quality improvements to performance goals
   - Use quality metrics in hiring/promotion decisions (if appropriate)

**Best Practices:**

- Make quality visible to all users (public dashboard, not hidden)
- Set realistic improvement targets (don't expect 100% overnight)
- Celebrate improvements; don't just criticize poor quality
- Link quality metrics to business impact (show cost/risk of poor quality)
- Review quality dashboards at least monthly

---

### 7. Catalog Review Workflows

Regular catalog reviews prevent stale data, ensure accurate metadata, and maintain governance standards.

#### Workflow: Periodic Asset Review Scheduling

**When to use:** To establish ongoing governance cadence.

**Steps:**

1. **Define review schedule:**
   - **Critical Assets:** Monthly review (KPIs, customer-facing models, regulatory data)
   - **Important Assets:** Quarterly review (heavily-used dashboards, core measures)
   - **Standard Assets:** Annual review (everything else)
   - Establish review calendar with assigned owners

2. **Create review checklist:**
   - Does the asset meet current business needs?
   - Is metadata up-to-date (name, description, tags)?
   - Is quality acceptable? Any known issues?
   - Is asset actively used? By whom?
   - Is ownership clear and current?
   - Are there any deprecated or redundant assets to clean up?

3. **Conduct reviews:**
   - Send review request to asset owner with checklist
   - Owner reviews and confirms or updates metadata
   - Owner identifies any issues or improvement opportunities
   - Governance team follows up on unfinished reviews

4. **Track and report:**
   - Monitor review completion rates
   - Report on findings (common issues, needed improvements)
   - Create action items for improvements identified
   - Schedule follow-up reviews for problematic assets

**Best Practices:**

- Keep review lightweight; 5-minute checklist is better than hour-long review
- Automate notifications and tracking (don't rely on email)
- Make reviews part of team's regular cadence (e.g., first Friday of month)
- Recognize teams with high-quality catalogs
- Use review findings to improve governance processes

#### Workflow: Stale Asset Identification and Cleanup

**When to use:** During governance audits or when trying to reduce catalog clutter.

**Steps:**

1. **Identify stale assets:**
   - Use `list_catalog_assets` to find assets with:
     - No recent updates (e.g., not modified in 1+ year)
     - No recent usage (e.g., not consumed by any dashboards/models)
     - No owner or owner no longer in organization
   - Flag assets as potentially stale
   - Create stale asset inventory

2. **Investigate stale assets:**
   - For each stale asset, determine why it's not used
   - Is it truly unused? Or is usage not tracked?
   - Use downstream analysis to check for hidden dependencies
   - Interview potential users (is this asset still needed?)

3. **Plan consolidation or deprecation:**
   - **Option 1:** Consolidate with similar active asset (reduce duplication)
   - **Option 2:** Deprecate with migration path to replacement asset
   - **Option 3:** Archive with clear documentation (in case needed in future)
   - **Option 4:** Delete if truly redundant and no users identified
   - Get stakeholder approval before action

4. **Execute cleanup:**
   - For deprecation: Communicate timeline, provide replacement access
   - For consolidation: Migrate any remaining users to replacement asset
   - For archival: Move to archive location, keep documentation accessible
   - For deletion: Only after confirming no users/lineage dependencies

5. **Monitor and report:**
   - Track cleanup progress and completed actions
   - Report on amount of technical debt removed
   - Celebrate catalog cleanliness improvements
   - Establish policies to prevent stale assets from accumulating again

**Best Practices:**

- Don't delete without confirming no users (hidden dependencies surprise you)
- Keep archived assets documented; don't just disappear them
- Communicate deprecations early; give long lead time (6+ months)
- Use cleanup projects to establish ongoing maintenance culture
- Review and approve stale asset cleanup at governance committee level

#### Workflow: Ownership Assignment and Accountability

**When to use:** During onboarding, when ownership gaps identified, or during governance reviews.

**Steps:**

1. **Define ownership model:**
   - **Technical Owner:** Responsible for data model, refresh, quality
   - **Business Owner:** Responsible for business interpretation, accuracy
   - **Executive Sponsor:** Accountable for strategic alignment
   - Document roles and responsibilities in RACI matrix (see references)

2. **Identify ownership gaps:**
   - Use `list_catalog_assets` to find assets without assigned owner
   - Create ownership inventory (asset → assigned owner)
   - Identify teams with too much ownership (capacity issues)
   - Identify gaps where ownership unclear

3. **Assign ownership:**
   - Match assets to appropriate owners based on:
     - Team responsible for data model
     - Team most familiar with business context
     - Team consuming data most heavily
   - Get owner approval before assigning
   - Document escalation path if owner unavailable

4. **Enable accountability:**
   - Use ownership assignments to route review requests
   - Track owner response rates and quality of reviews
   - Recognize owners with high-quality asset governance
   - Provide support/training to struggling owners

5. **Maintain ownership:**
   - Review ownership quarterly
   - Update when owners change roles
   - Establish succession planning for critical asset owners
   - Document owner transitions with knowledge transfer

**Best Practices:**

- Assign single owner (not committees); clarifies accountability
- Ensure owner has time/authority to manage asset (avoid overloading)
- Rotate ownership periodically (prevents siloing of knowledge)
- Provide owners with tools and dashboards to manage their assets
- Tie ownership to performance reviews/compensation (creates accountability)

---

## MCP Tools Reference

This skill leverages these Datasphere MCP tools:

- **`search_catalog`** - Search catalog by name, description, or metadata; filter by type, domain, tag
- **`get_asset_details`** - Retrieve full metadata for table, view, model, or measure (structure, lineage, ownership)
- **`list_catalog_assets`** - List assets matching criteria (type, owner, status, tag); supports pagination
- **`search_repository`** - Search source system definitions and imported objects
- **`get_object_definition`** - Retrieve detailed definition of object (structure, calculations, lineage)
- **`get_deployed_objects`** - List deployed models/measures and their status
- **`analyze_column_distribution`** - Analyze column data types, cardinality, completeness, distributions

---

## Best Practices Summary

**Metadata Enrichment:**
- Use business terminology, not technical jargon
- Keep descriptions under 500 words; link to detailed docs
- Auto-suggest tags; require human review before applying
- Batch updates by logical group; test on samples first

**Glossary Management:**
- Start with 20-30 high-impact terms; grow over time
- Involve business owners in definitions
- Link glossary terms to actual technical implementations
- Version glossary; communicate changes to stakeholders
- Resolve terminology conflicts through formal approval process

**KPI Definition:**
- Define calculation logic clearly; include examples
- Validate KPI against underlying data before publishing
- Assign single owner; document accountability
- Review KPI portfolio annually for relevance
- Version KPI definitions; don't silently change calculations

**Tag Management:**
- Design controlled vocabulary; limit active tags to 20-50
- Apply tags consistently across all assets
- Use tags for governance enforcement (required tags for sensitive data)
- Review and consolidate tags quarterly

**Lineage & Impact:**
- Always analyze downstream impact before modifying critical assets
- Use impact reports to gain stakeholder approval for changes
- Identify and consolidate redundant implementations
- Build automated tests to validate changes against downstream consumers

**Data Quality:**
- Automate quality scoring; avoid manual assessments
- Make quality scores visible to all users
- Link quality issues to remediation projects
- Review quality metrics monthly; celebrate improvements

**Catalog Reviews:**
- Keep reviews lightweight (5-minute checklist)
- Conduct critical asset reviews monthly; standard assets annually
- Identify and clean up stale assets regularly
- Maintain ownership assignments; rotate periodically

---

## Common Anti-Patterns and Solutions

**Anti-Pattern:** Metadata written for IT, not business
- **Solution:** Use business analyst as template reviewer; remove jargon

**Anti-Pattern:** Too many tags; users can't navigate
- **Solution:** Consolidate to 20-30 core tags; deprecate duplicates

**Anti-Pattern:** KPI definitions silently change (breaks downstream calculations)
- **Solution:** Version KPI definitions; communicate changes; validate impact

**Anti-Pattern:** Assets with no owner; governance unenforceable
- **Solution:** Systematically assign owners; include ownership in publishing workflow

**Anti-Pattern:** Quality issues discovered downstream; no visibility upstream
- **Solution:** Build quality dashboards; surface issues early; tie to remediation projects

**Anti-Pattern:** Lineage not captured; impact analysis impossible
- **Solution:** Ensure lineage automatically captured from data models; manually document complex logic

**Anti-Pattern:** Glossary becomes unmaintainable; conflicting definitions
- **Solution:** Implement formal approval workflow; version terms; resolve conflicts through governance

---

## Integration with Data Product Publishing

The Catalog Steward skill complements the Data Product Publisher skill:

- **Catalog Steward:** Organizes internal repository (metadata, quality, lineage, governance)
- **Data Product Publisher:** Publishes curated products to external marketplace

Before publishing a data product, use Catalog Steward to:
- Ensure all source assets have clear ownership and quality certification
- Validate glossary terms and KPI definitions
- Verify lineage and impact analysis (understand ripple effects)
- Establish quality SLAs for published product
- Assign business/technical owners responsible for product quality

---

## Getting Started

1. **Audit Current State:**
   - Use `list_catalog_assets` to inventory all assets
   - Use `get_asset_details` to assess metadata quality
   - Identify highest-value governance improvements

2. **Design Your Governance Model:**
   - Define roles and responsibilities (RACI)
   - Design tag taxonomy and glossary structure
   - Establish quality scoring methodology

3. **Execute Pilot Project:**
   - Pick 1-2 business domains for pilot
   - Enrich metadata, add glossary terms, implement tagging
   - Build sample quality dashboard
   - Get stakeholder feedback and refine approach

4. **Scale Governance Program:**
   - Extend to additional domains
   - Build automation for metadata enrichment, quality scoring, lineage capture
   - Establish review cadences and ownership assignments
   - Train data owners and catalog curators

5. **Measure and Optimize:**
   - Track catalog usage metrics (searches, views, discovery patterns)
   - Monitor governance compliance (tagging, quality, ownership)
   - Conduct quarterly reviews; adjust policies based on feedback
   - Celebrate wins; recognize teams driving adoption
