# HubSpot fields and activity types

The specific HubSpot objects, properties, and activity types the `crm-maintenance` skill reads from and writes to. Only the fields listed here are in-scope for this skill — everything else in HubSpot is untouched.

## Contacts — write

| Field         | Usage                                                                                  |
|---------------|----------------------------------------------------------------------------------------|
| `email`       | Primary identifier for lookup + dedupe. Always set on creation.                        |
| `firstname`   | Set from email signature or calendar invite if available. Leave blank if unknown.      |
| `lastname`    | Set from email signature or calendar invite if available. Leave blank if unknown.      |
| `company`     | Set from email signature domain or calendar organization if available.                 |

Do not write any other contact properties. Owner, lifecycle stage, and lead source are user-managed fields — never overwrite.

## Contacts — read (for lookup)

| Field         | Usage                                                              |
|---------------|--------------------------------------------------------------------|
| `email`       | Search key. Case-insensitive exact match.                          |
| `firstname` · `lastname` · `company` | Displayed to the user during ambiguity resolution. |
| `hs_object_id`| Used for association with deals and activities.                    |

## Deals — read (all cleanup + resolution paths)

| Field                       | Usage                                                    |
|-----------------------------|----------------------------------------------------------|
| `dealname`                  | Displayed to the user; used for fuzzy match against email/meeting topic |
| `dealstage`                 | Read-only during cleanup — flag discrepancies, never change |
| `amount`                    | Read during cleanup; flag if recent email/meeting implies change |
| `closedate`                 | Read during cleanup; flag if outdated                    |
| `hs_next_step`              | Read + propose updates during cleanup                    |
| `hubspot_owner_id`          | Displayed to the user; never changed                     |
| `hs_lastactivitydate`       | Used to detect stale deals                               |
| Associated contacts         | Used to determine whether recent email/meeting participants are on the deal |

## Deals — write (cleanup path only, with approval)

| Field           | Rule                                                             |
|-----------------|------------------------------------------------------------------|
| `hs_next_step`  | Propose updates; write only with explicit user approval          |
| `closedate`     | Propose updates; write only with explicit user approval          |
| `amount`        | Propose updates; write only with explicit user approval          |
| Contact assoc.  | Propose adding missing deal participants; write only with approval |

**Never write** `dealstage`, `pipeline`, `hubspot_owner_id`, or any custom property during cleanup. Those are owner-managed.

## Activities — write

| Activity type                  | Used by        | Fields set                                                               |
|--------------------------------|----------------|--------------------------------------------------------------------------|
| Email engagement (`EMAIL`)     | Email path     | `hs_email_subject` (thread subject), `hs_email_text` (summary, not full thread), `hs_timestamp` (latest message time), associated contact(s) + deal |
| Call engagement (`CALL`)       | Call path      | `hs_call_title` (event title), `hs_call_body` (summary), `hs_call_duration` (from calendar), `hs_timestamp` (event start), associated contact(s) + deal |
| Note (`NOTE`)                  | Cleanup path   | `hs_note_body` (when flagging something for future review that doesn't fit a field update) |

Use HubSpot's standard engagement vocabulary. Do not invent custom activity types.

## Association rules

- Every activity must associate to the deal AND to at least one contact.
- If a contact is created on-the-fly during activity logging, associate it to the deal in the same operation so the activity shows up on both the contact and deal timelines.
- Do not associate a contact to a deal during an activity-logging flow unless the contact is actually a participant in that email thread or meeting.
