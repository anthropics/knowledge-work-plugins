---
name: webhook-audit
description: Review and audit incoming Vault RE JSON payloads to trigger private actions.
arguments:
  - name: payload
    description: "The raw JSON payload from a Vault RE webhook."
    required: true
  - name: action_type
    description: "The type of event (e.g., contact.added, property.updated)."
    required: false
---

# /webhook-audit Command

Audit real-time CRM events and map them to your shadow workflow.

## When to Use

Use this command when:
- A new lead enters Vault RE and you want to "vet" it privately.
- A property status changes and you need to prep "Shadow Marketing" (OpenClaw).
- You want to verify the data integrity of a corporate system event.

## Workflow

### 1. JSON Parsing

Use `~~real-estate/shadow-workflow` to:
- Extract key entities (Contact Name, Property Address, User ID).
- Identify the specific trigger (e.g., "Signed via Secure Sign").

### 2. Strategy Mapping

Produce:
- **Shadow Event Summary**: Plain English explanation of the webhook.
- **Recommended Private Action**: (e.g., "Update Private Deal Sheet," "Draft Personal IG Story").
- **Priority Rating**: High/Medium/Low based on conversion potential.

## Example Session

**User:** `/webhook-audit payload: {"event": "property.updated", "id": 123, "status": "Listing"}`

**System:**
```
[~] PARSING VAULT RE PAYLOAD...
[~] MAPPING TO SHADOW WORKFLOW...

WEBHOOK AUDIT COMPLETE:

1. Event: Property '123 Petone St' moved from Appraisal to Listing.
2. Shadow Action:
   - Update 'Private Deal Tracker' (Google Sheet).
   - Trigger OpenClaw: Draft 'Just Listed' post for personal LinkedIn.
   - Task: Create 48-hour follow-up for all appraisal-stage leads.

Would you like to draft the OpenClaw teaser for this listing? [Y/n]
```

## Integration Points

- **Skill**: Uses `~~real-estate/shadow-workflow`.
- **Downstream**: Feeds into `/draft-listing`.
