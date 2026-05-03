# Zoom Mail API

Authoritative endpoint inventory for Mail. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/mail/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 41 |
| Path templates | 26 |
| Tags | 10 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Drafts | 6 |
| History | 1 |
| Labels | 6 |
| Mailbox | 1 |
| Messages | 10 |
| Messages.Attachments | 1 |
| Settings | 2 |
| Settings.Delegates | 4 |
| Settings.Filters | 4 |
| Threads | 6 |

## Endpoints by Tag

### Drafts

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/emails/mailboxes/{email}/drafts` | List emails from draft folder | `list_draft_emails` |
| POST | `/emails/mailboxes/{email}/drafts` | Create a new draft email | `create_draft_email` |
| POST | `/emails/mailboxes/{email}/drafts/send` | Send out a draft email | `send_draft_email` |
| DELETE | `/emails/mailboxes/{email}/drafts/{draftId}` | Delete an existing draft email | `delete_draft_email` |
| GET | `/emails/mailboxes/{email}/drafts/{draftId}` | Get the specified draft email | `get_draft_email` |
| PUT | `/emails/mailboxes/{email}/drafts/{draftId}` | Update the specified draft email | `update_draft_email` |

### History

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/emails/mailboxes/{email}/history` | List history of events for mailbox | `list_mailbox_history` |

### Labels

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/emails/mailboxes/{email}/labels` | List labels in the mailbox | `list_labels_in_mailbox` |
| POST | `/emails/mailboxes/{email}/labels` | Create a new label in mailbox | `create_label_in_mailbox` |
| DELETE | `/emails/mailboxes/{email}/labels/{labelId}` | Delete an existing label from mailbox | `delete_label_from_mailbox` |
| GET | `/emails/mailboxes/{email}/labels/{labelId}` | Get the specified label in mailbox | `get_label_in_mailbox` |
| PATCH | `/emails/mailboxes/{email}/labels/{labelId}` | Patch the specified label in mailbox | `patch_label_in_mailbox` |
| PUT | `/emails/mailboxes/{email}/labels/{labelId}` | Update the specified label in mailbox | `update_label_in_mailbox` |

### Mailbox

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/emails/mailboxes/{email}/profile` | Get the mailbox profile | `get_mailbox_profile` |

### Messages

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/emails/mailboxes/{email}/messages` | List emails from the mailbox | `list_emails` |
| POST | `/emails/mailboxes/{email}/messages` | Create a new email | `create_email` |
| POST | `/emails/mailboxes/{email}/messages/batchDelete` | Batch delete the specified emails | `batch_delete_emails` |
| POST | `/emails/mailboxes/{email}/messages/batchModify` | Batch modify the specified emails | `batch_modify_emails` |
| POST | `/emails/mailboxes/{email}/messages/send` | Send out an email | `send_email` |
| DELETE | `/emails/mailboxes/{email}/messages/{messageId}` | Delete an existing email | `delete_email` |
| GET | `/emails/mailboxes/{email}/messages/{messageId}` | Get the specified email | `get_email` |
| POST | `/emails/mailboxes/{email}/messages/{messageId}/modify` | Update the specified email | `update_email` |
| POST | `/emails/mailboxes/{email}/messages/{messageId}/trash` | Move the specified email to TRASH folder | `trash_email` |
| POST | `/emails/mailboxes/{email}/messages/{messageId}/untrash` | Move the specified email out of TRASH folder | `untrash_email` |

### Messages.Attachments

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/emails/mailboxes/{email}/messages/{messageId}/attachments/{attachmentId}` | Get the specified attachment for an email | `get_email_attachment` |

### Settings

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/emails/mailboxes/{email}/settings/vacation` | Get mailbox vacation response setting | `get_mail_vacation_response_setting` |
| PUT | `/emails/mailboxes/{email}/settings/vacation` | Update mailbox vacation response setting | `update_mailbox_vacation_response_setting` |

### Settings.Delegates

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/emails/mailboxes/{email}/settings/delegates` | List delegates on the mailbox | `list_mailbox_delegates` |
| POST | `/emails/mailboxes/{email}/settings/delegates` | Grant a new delegate access on the mailbox | `grant_mailbox_delegate` |
| DELETE | `/emails/mailboxes/{email}/settings/delegates/{delegateEmail}` | Revoke an existing delegate access from the mailbox | `revoke_mailbox_delegate` |
| GET | `/emails/mailboxes/{email}/settings/delegates/{delegateEmail}` | Get the specified delegate on the mailbox | `get_mailbox_delegate` |

### Settings.Filters

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/emails/mailboxes/{email}/settings/filters` | List email filters | `list_email_filters` |
| POST | `/emails/mailboxes/{email}/settings/filters` | Create an email filter | `create_email_filter` |
| DELETE | `/emails/mailboxes/{email}/settings/filters/{filterId}` | Delete the specified email filter | `delete_email_filter` |
| GET | `/emails/mailboxes/{email}/settings/filters/{filterId}` | Get the specified email filter | `get_email_filter` |

### Threads

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/emails/mailboxes/{email}/threads` | List email threads from the mailbox | `list_email_threads` |
| DELETE | `/emails/mailboxes/{email}/threads/{threadId}` | Delete an existing email thread | `delete_email_thread` |
| GET | `/emails/mailboxes/{email}/threads/{threadId}` | Get the specified email thread | `get_email_thread` |
| POST | `/emails/mailboxes/{email}/threads/{threadId}/modify` | Update the specified thread | `update_email_thread` |
| POST | `/emails/mailboxes/{email}/threads/{threadId}/trash` | Move the specified thread to TRASH folder | `trash_email_thread` |
| POST | `/emails/mailboxes/{email}/threads/{threadId}/untrash` | Move the specified thread out of TRASH folder | `untrash_email_thread` |
