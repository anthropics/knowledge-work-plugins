---
name: legal-response
description: Generate a response to a common legal inquiry using configured templates, with built-in escalation checks for situations that shouldn't use a templated reply. Use when responding to data subject requests, litigation hold notices, vendor legal questions, NDA requests from business teams, or subpoenas.
argument-hint: "[inquiry-type]"
---

# /legal-response -- Generate Response from Templates

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Generate a response to a common legal inquiry using configured templates. Customizes the response with specific details and includes escalation triggers for situations that should not use a templated response.

**Important**: This command assists with legal workflows but does not provide legal advice. Generated responses should be reviewed by qualified legal professionals before being sent, especially for regulated communications.

## Invocation

```
/legal-response [inquiry-type]
```

Common inquiry types:
- `dsr` or `data-subject-request` -- Data subject access/deletion/correction requests
- `hold` or `discovery-hold` -- Litigation hold notices
- `vendor` or `vendor-question` -- Vendor legal questions
- `nda` or `nda-request` -- NDA requests from business teams
- `privacy` or `privacy-inquiry` -- Privacy-related questions
- `subpoena` -- Subpoena or legal process responses
- `insurance` -- Insurance claim notifications
- `custom` -- Use a custom template

If no inquiry type is provided, ask the user what type of response they need and show available categories.

## Workflow

### Step 1: Identify Inquiry Type

Accept the inquiry type from the user. If the type is ambiguous, show available categories and ask for clarification.

### Step 2: Load Template

Look for templates in local settings (e.g., `legal.local.md` or a templates directory).

**If templates are configured:**
- Load the appropriate template for the inquiry type
- Identify required variables (recipient name, dates, specific details)

**If no templates are configured:**
- Inform the user that no templates were found for this inquiry type
- Offer to help create a template (see Template Creation Guide below)
- Provide a reasonable default response structure based on the inquiry type

### Step 3: Check Escalation Triggers

Before generating any response, evaluate whether this situation has characteristics that should NOT use a templated response.

#### Universal Escalation Triggers (Apply to All Categories)
- The matter involves potential litigation or regulatory investigation
- The inquiry is from a regulator, government agency, or law enforcement
- The response could create a binding legal commitment or waiver
- The matter involves potential criminal liability
- Media attention is involved or likely
- The situation is unprecedented (no prior handling by the team)
- Multiple jurisdictions are involved with conflicting requirements
- The matter involves executive leadership or board members

#### Data Subject Request Escalation Triggers
- Request involves a minor's data, or is from/on behalf of a minor
- Request is from a regulatory authority (not an individual)
- Request involves data that is subject to a litigation hold
- Requester is a current or former employee with an active dispute or HR matter
- Request scope is unusually broad or appears to be a fishing expedition
- Request involves data processed in a jurisdiction with unique requirements
- Request involves special category data (health, biometric, genetic)

#### Discovery Hold Escalation Triggers
- The matter involves potential criminal liability
- The preservation scope is unclear, disputed, or potentially overbroad
- There are questions about whether certain data is within scope
- Prior holds for the same or related matter exist
- The hold may affect ongoing business operations significantly
- Hold conflicts with regulatory deletion requirements
- Custodian objects to the hold scope

#### Vendor Question Escalation Triggers
- The question involves a dispute or potential breach
- The vendor is threatening litigation or termination
- The question involves regulatory compliance (not just contract terms)
- The response could create a binding commitment or waiver
- Response could affect ongoing negotiation

#### NDA Request Escalation Triggers
- The counterparty is a competitor
- The NDA involves government classified information
- The business context suggests the NDA is for a potential M&A transaction
- The request involves unusual subject matter (AI training data, biometric data, etc.)

#### Subpoena / Legal Process Escalation Triggers
- **ALWAYS requires counsel review** (templates are starting points only)
- Privilege issues identified
- Third-party data involved
- Cross-border production issues
- Unreasonable timeline

**When an escalation trigger is detected:**
1. **Stop**: Do not generate a templated response
2. **Alert**: Inform the user that an escalation trigger has been detected
3. **Explain**: Describe which trigger was detected and why it matters
4. **Recommend**: Suggest the appropriate escalation path (senior counsel, outside counsel, specific team member)
5. **Offer**: Provide a draft for counsel review (clearly marked as "DRAFT - FOR COUNSEL REVIEW ONLY") rather than a final response

### Step 4: Gather Specific Details

Prompt the user for the details needed to customize the response:

**Data Subject Request:**
- Requester name and contact information
- Type of request (access, deletion, correction, portability, opt-out)
- What data is involved
- Applicable regulation (GDPR, CCPA, CPRA, other)
- Response deadline

**Discovery Hold:**
- Matter name and reference number
- Custodians (who needs to preserve)
- Scope of preservation (date range, data types, systems)
- Outside counsel contact
- Effective date

**Vendor Question:**
- Vendor name
- Reference agreement (if applicable)
- Specific question being addressed
- Relevant contract provisions

**NDA Request:**
- Requesting business team and contact
- Counterparty name
- Purpose of the NDA
- Mutual or unilateral
- Any special requirements

### Step 5: Generate Response

Populate the template with the gathered details. Ensure the response:
- Uses appropriate tone (professional, clear, not overly legalistic for business audiences)
- Includes all required legal elements for the response type
- References specific dates, deadlines, and obligations
- Provides clear next steps for the recipient
- Includes appropriate disclaimers or caveats

Present the draft response to the user for review before sending.

#### Customization Guidelines

**Required customization** — Every templated response MUST be customized with:
- Correct names, dates, and reference numbers
- Specific facts of the situation
- Applicable jurisdiction and regulation
- Correct response deadlines based on when the inquiry was received
- Appropriate signature block and contact information

**Tone adjustment** — Adjust tone based on:
- **Audience**: Internal vs. external, business vs. legal, individual vs. regulatory authority
- **Relationship**: New counterparty vs. existing partner vs. adversarial party
- **Sensitivity**: Routine inquiry vs. contentious matter vs. regulatory investigation
- **Urgency**: Standard timeline vs. expedited response needed

**Jurisdiction-specific adjustments:**
- Verify that cited regulations are correct for the requester's jurisdiction
- Adjust timelines to match applicable law
- Include jurisdiction-specific rights information
- Use jurisdiction-appropriate legal terminology

### Step 6: Template Creation (If No Template Exists)

If the user wants to create a new template, walk through the Template Creation Guide (see below) and present the finished template for review. Suggest the user save the approved template to their local settings for future use.

## Response Categories

### 1. Data Subject Requests (DSRs)

**Sub-categories**:
- Acknowledgment of receipt
- Identity verification request
- Fulfillment response (access, deletion, correction)
- Partial denial with explanation
- Full denial with explanation
- Extension notification

**Key template elements**:
- Reference to applicable regulation (GDPR, CCPA, etc.)
- Specific timeline for response
- Identity verification requirements
- Rights of the data subject (including right to complain to supervisory authority)
- Contact information for follow-up

**Example template structure**:
```
Subject: Your Data [Access/Deletion/Correction] Request - Reference {{request_id}}

Dear {{requester_name}},

We have received your request dated {{request_date}} to [access/delete/correct] your personal data under [applicable regulation].

[Acknowledgment / verification request / fulfillment details / denial basis]

We will respond substantively by {{response_deadline}}.

[Contact information]
[Rights information]
```

### 2. Discovery Holds (Litigation Holds)

**Sub-categories**:
- Initial hold notice to custodians
- Hold reminder / periodic reaffirmation
- Hold modification (scope change)
- Hold release

**Key template elements**:
- Matter name and reference number
- Clear preservation obligations
- Scope of preservation (date range, data types, systems, communication types)
- Prohibition on spoliation
- Contact for questions
- Acknowledgment requirement

**Example template structure**:
```
Subject: LEGAL HOLD NOTICE - {{matter_name}} - Action Required

PRIVILEGED AND CONFIDENTIAL
ATTORNEY-CLIENT COMMUNICATION

Dear {{custodian_name}},

You are receiving this notice because you may possess documents, communications, or data relevant to the matter referenced above.

PRESERVATION OBLIGATION:
Effective immediately, you must preserve all documents and electronically stored information (ESI) related to:
- Subject matter: {{hold_scope}}
- Date range: {{start_date}} to present
- Document types: {{document_types}}

DO NOT delete, destroy, modify, or discard any potentially relevant materials.

[Specific instructions for systems, email, chat, local files]

Please acknowledge receipt of this notice by {{acknowledgment_deadline}}.

Contact {{legal_contact}} with any questions.
```

### 3. Privacy Inquiries

**Sub-categories**:
- Cookie/tracking inquiry responses
- Privacy policy questions
- Data sharing practice inquiries
- Children's data inquiries
- Cross-border transfer questions

**Key template elements**:
- Reference to the organization's privacy notice
- Specific answers based on current practices
- Links to relevant privacy documentation
- Contact information for the privacy team

### 4. Vendor Legal Questions

**Sub-categories**:
- Contract status inquiry response
- Amendment request response
- Compliance certification requests
- Audit request responses
- Insurance certificate requests

**Key template elements**:
- Reference to the applicable agreement
- Specific response to the vendor's question
- Any required caveats or limitations
- Next steps and timeline

### 5. NDA Requests

**Sub-categories**:
- Sending the organization's standard form NDA
- Accepting a counterparty's NDA (with markup)
- Declining an NDA request with explanation
- NDA renewal or extension

**Key template elements**:
- Purpose of the NDA
- Standard terms summary
- Execution instructions
- Timeline expectations

### 6. Subpoena / Legal Process

**Sub-categories**:
- Acknowledgment of receipt
- Objection letter
- Request for extension
- Compliance cover letter

**Key template elements**:
- Case reference and jurisdiction
- Specific objections (if any)
- Preservation confirmation
- Timeline for compliance
- Privilege log reference (if applicable)

**Critical note**: Subpoena responses almost always require individualized counsel review. Templates serve as starting frameworks, not final responses.

### 7. Insurance Notifications

**Sub-categories**:
- Initial claim notification
- Supplemental information
- Reservation of rights response

**Key template elements**:
- Policy number and coverage period
- Description of the matter or incident
- Timeline of events
- Requested coverage confirmation

## Template Management Methodology

### Template Organization

Templates should be organized by category and maintained in the team's local settings. Each template should include:

1. **Category**: The type of inquiry the template addresses
2. **Template name**: A descriptive identifier
3. **Use case**: When this template is appropriate
4. **Escalation triggers**: When this template should NOT be used
5. **Required variables**: Information that must be customized for each use
6. **Template body**: The response text with variable placeholders
7. **Follow-up actions**: Standard steps after sending the response
8. **Last reviewed date**: When the template was last verified for accuracy

### Template Lifecycle

1. **Creation**: Draft template based on best practices and team input
2. **Review**: Legal team review and approval of template content
3. **Publication**: Add to template library with metadata
4. **Use**: Generate responses using the template
5. **Feedback**: Track when templates are modified during use to identify improvement opportunities
6. **Update**: Revise templates when laws, policies, or best practices change
7. **Retirement**: Archive templates that are no longer applicable

## Template Creation Guide

When helping users create new templates:

### 1. Define the Use Case
- What type of inquiry does this address?
- How frequently does this come up?
- Who is the typical audience?
- What is the typical urgency level?

### 2. Identify Required Elements
- What information must be included in every response?
- What regulatory requirements apply?
- What organizational policies govern this type of response?

### 3. Define Variables
- What changes with each use? (names, dates, specifics)
- What stays the same? (legal requirements, standard language)
- Use clear variable names: `{{requester_name}}`, `{{response_deadline}}`, `{{matter_reference}}`

### 4. Draft the Template
- Write in clear, professional language
- Avoid unnecessary legal jargon for business audiences
- Include all legally required elements
- Add placeholders for all variable content
- Include a subject line template if for email use

### 5. Define Escalation Triggers
- What situations should NOT use this template?
- What characteristics indicate the matter needs individualized attention?
- Be specific: vague triggers are not useful

### 6. Add Metadata
- Template name and category
- Version number and last reviewed date
- Author and approver
- Follow-up actions checklist

### Template Format

```markdown
## Template: {{template_name}}
**Category**: {{category}}
**Version**: {{version}} | **Last Reviewed**: {{date}}
**Approved By**: {{approver}}

### Use When
- [Condition 1]
- [Condition 2]

### Do NOT Use When (Escalation Triggers)
- [Trigger 1]
- [Trigger 2]

### Variables
| Variable | Description | Example |
|---|---|---|
| {{var1}} | [what it is] | [example value] |
| {{var2}} | [what it is] | [example value] |

### Subject Line
[Subject template with {{variables}}]

### Body
[Response body with {{variables}}]

### Follow-Up Actions
1. [Action 1]
2. [Action 2]

### Notes
[Any special instructions for users of this template]
```

## Output Format

```
## Generated Response: [Inquiry Type]

**To**: [recipient]
**Subject**: [subject line]

---

[Response body]

---

### Escalation Check
[Confirmation that no escalation triggers were detected, OR flagged triggers with recommendations]

### Follow-Up Actions
1. [Post-send actions]
2. [Calendar reminders to set]
3. [Tracking or logging requirements]
```

## Notes

- Always present the draft response for user review before suggesting it be sent
- If connected to email via MCP, offer to create a draft email with the response
- Track response deadlines and offer to set calendar reminders
- For regulated responses (DSRs, subpoenas), always note the applicable deadline and regulatory requirements
- Templates should be living documents; suggest updates when the user modifies a templated response, so the template can be improved over time
