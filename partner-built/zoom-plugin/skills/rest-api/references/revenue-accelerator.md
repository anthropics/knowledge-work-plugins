# Zoom Revenue Accelerator API

Authoritative endpoint inventory for Revenue Accelerator. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/iq/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 75 |
| Path templates | 51 |
| Tags | 6 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Accounts | 2 |
| Conversations | 34 |
| CRM | 12 |
| Deals | 8 |
| ScheduleMeetings | 1 |
| Teams | 18 |

## Endpoints by Tag

### Accounts

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/iq/settings/indicators` | Get indicators settings [Deprecated] | `accountSettingsIndicatorsDeprecated` |
| GET | `/zra/settings/indicators` | Get indicators settings | `accountIndicatorsSettings` |

### Conversations

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/iq/conversations` | List conversations [Deprecated] | `listConversationsDeprecated` |
| POST | `/iq/conversations` | Add conversation by file id or download url. [Deprecated] | `AddConversationByFileIdOrDownloadUrlDeprecated` |
| DELETE | `/iq/conversations/{conversationId}` | Delete conversation by conversation ID [Deprecated] | `deleteConversationDeprecated` |
| GET | `/iq/conversations/{conversationId}` | Get conversation information [Deprecated] | `getConversationInfoDeprecated` |
| GET | `/iq/conversations/{conversationId}/comments` | Get conversation comments [Deprecated] | `getConversationCommentsDeprecated` |
| POST | `/iq/conversations/{conversationId}/comments` | Add new comments to the conversation [Deprecated] | `addConversationCommentDeprecated` |
| DELETE | `/iq/conversations/{conversationId}/comments/{commentId}` | Delete conversation's comment [Deprecated] | `deleteConversationCommentDeprecated` |
| PATCH | `/iq/conversations/{conversationId}/comments/{commentId}` | Edit conversation comment [Deprecated] | `editConversationCommentDeprecated` |
| GET | `/iq/conversations/{conversationId}/content_analysis` | Get conversation content analysis [Deprecated] | `getConversationContentAnalysisDeprecated` |
| GET | `/iq/conversations/{conversationId}/interactions` | Get conversation interactions [Deprecated] | `getConversationInteractionsDeprecated` |
| GET | `/iq/conversations/{conversationId}/scorecards` | Get conversation scorecards [Deprecated] | `getConversationScorecardsDeprecated` |
| PATCH | `/iq/conversations/{conversationId}/update_host` | Update conversation host id to new host id by conversation id [Deprecated] | `UpdateconversationhostidtonewhostidbyconversationidDeprecated` |
| POST | `/iq/files` | Upload IQ file [Deprecated] | `UploadIQFileDeprecated` |
| POST | `/iq/files/multipart` | Upload iq multipart file. [Deprecated] | `UploadIqMultipartFileDeprecated` |
| POST | `/iq/files/multipart/upload_events` | Initiate and complete a multipart upload. [Deprecated] | `InitiateAndCompleteAMultipartUpload. [Deprecated]` |
| POST | `/iq/users/{userId}/conversations` | Add conversation by meeting record url or meeting UUID. [Deprecated] | `addConversationDeprecated` |
| GET | `/iq/users/{userId}/conversations/playlists` | Get a user's playlist [Deprecated] | `getUserPlaylistDeprecated` |
| GET | `/zra/conversations` | List conversations | `listAllConversations` |
| POST | `/zra/conversations` | Add conversation by file id or download url. | `AddConversationByFileIdOrDownloadUrl` |
| DELETE | `/zra/conversations/{conversationId}` | Delete conversation by conversation ID | `deleteConversationById` |
| GET | `/zra/conversations/{conversationId}` | Get conversation information | `getConversationDetail` |
| GET | `/zra/conversations/{conversationId}/comments` | Get conversation comments | `getConversationCommentsById` |
| POST | `/zra/conversations/{conversationId}/comments` | Add new comments to the conversation | `addConversationComments` |
| DELETE | `/zra/conversations/{conversationId}/comments/{commentId}` | Delete conversation's comment | `deleteConversationCommentById` |
| PATCH | `/zra/conversations/{conversationId}/comments/{commentId}` | Edit conversation comment | `editConversationCommentById` |
| GET | `/zra/conversations/{conversationId}/content_analysis` | Get conversation content analysis | `getConversationContentAnalysisById` |
| GET | `/zra/conversations/{conversationId}/interactions` | Get conversation interactions | `getConversationInteraction` |
| GET | `/zra/conversations/{conversationId}/scorecards` | Get conversation scorecards | `getConversationScorecardsById` |
| PATCH | `/zra/conversations/{conversationId}/update_host` | Update conversation host id | `UpdateConversationhostid2NewHostidByConversationId` |
| POST | `/zra/files` | Upload IQ file | `UploadZraFile` |
| POST | `/zra/files/multipart` | Upload iq multipart file. | `UploadZraMultipartFile.` |
| POST | `/zra/files/multipart/upload_events` | Initiate and complete a multipart upload. | `InitiateAndCompleteAMultipartUpload` |
| POST | `/zra/users/{userId}/conversations` | Add conversation by meeting record url or meeting UUID. | `addConversationByRecord` |
| GET | `/zra/users/{userId}/conversations/playlists` | Get a user's playlist | `getUserPlaylists` |

### CRM

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zra/crm/accounts` | Get CRM accounts | `getCrmAccounts` |
| POST | `/zra/crm/accounts` | Bulk import CRM accounts | `bulkImportAccounts` |
| GET | `/zra/crm/contacts` | Get CRM contacts | `getCrmContacts` |
| POST | `/zra/crm/contacts` | Bulk import CRM contacts | `bulkImportContacts` |
| GET | `/zra/crm/deals` | Get CRM deals | `getCrmDeals` |
| POST | `/zra/crm/deals` | Bulk import CRM deals | `bulkImportDeals` |
| GET | `/zra/crm/leads` | Get CRM leads | `getCrmLeads` |
| POST | `/zra/crm/leads` | Bulk import CRM leads | `bulkImportLeads` |
| DELETE | `/zra/crm/settings` | Unregister CRM API connection | `unregisterCrm` |
| GET | `/zra/crm/settings` | Get current CRM API registration | `getCrmRegistration` |
| POST | `/zra/crm/settings` | Register CRM API connection | `registerCrm` |
| GET | `/zra/crm/tasks/{taskId}` | Poll async task result | `getAsyncTask` |

### Deals

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/iq/deals` | List deals [Deprecated] | `listDealsDeprecated` |
| GET | `/iq/deals/{dealId}` | Get deal information [Deprecated] | `getDealInfoDeprecated` |
| DELETE | `/iq/deals/{dealId}/activities` | Delete activity from the deal [Deprecated] | `DeleteActivityFromTheDealDeprecated` |
| GET | `/iq/deals/{dealId}/activities` | Get deal activities [Deprecated] | `getDealActivitiesDeprecated` |
| GET | `/zra/deals` | List deals | `listAllDeals` |
| GET | `/zra/deals/{dealId}` | Get deal information | `getDealDetail` |
| DELETE | `/zra/deals/{dealId}/activities` | Delete activity from the deal | `DeleteActivityFromDeal` |
| GET | `/zra/deals/{dealId}/activities` | Get deal activities | `geAllActivitiesFromDeal` |

### ScheduleMeetings

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zra/scheduled` | List scheduled meetings | `Listallscheduledmeetings` |

### Teams

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/iq/teams` | List Account Teams [Deprecated] | `ListAccountTeamsDeprecated` |
| POST | `/zra/team` | Create Team | `CreateTeam` |
| GET | `/zra/team/unassigned_team_users` | List Unassigned Team Users | `ListUnassignedTeamUsers` |
| DELETE | `/zra/team/{teamId}` | Delete Team | `DeleteTeam` |
| GET | `/zra/team/{teamId}` | Get Team Detail | `GetTeamDetail` |
| PATCH | `/zra/team/{teamId}` | Update Team name | `UpdateTeam` |
| DELETE | `/zra/team/{teamId}/access/granted-from` | Remove additional access from current team | `DeleteSharedFromTeams` |
| POST | `/zra/team/{teamId}/access/granted-from` | Grant additional access to current team | `AddSharedFromTeams` |
| DELETE | `/zra/team/{teamId}/access/granted-to` | Remove additional access from target teams | `DeleteSharedToTeams` |
| POST | `/zra/team/{teamId}/access/granted-to` | Grant additional access to target teams | `AddSharedToTeams` |
| PATCH | `/zra/team/{teamId}/parent_team` | Move team to new parent | `MoveTeam` |
| DELETE | `/zra/team/{teamId}/team_managers` | Unassign Team Managers | `UnassignTeamManagers` |
| GET | `/zra/team/{teamId}/team_managers` | List Team Managers | `ListTeamManagers` |
| POST | `/zra/team/{teamId}/team_managers` | Assign Team Managers | `AssignTeamManagers` |
| DELETE | `/zra/team/{teamId}/team_members` | Unassign Team Members | `UnassignTeamMembers` |
| GET | `/zra/team/{teamId}/team_members` | List Team Members | `ListTeamMembers` |
| POST | `/zra/team/{teamId}/team_members` | Assign Team Members | `AssignTeamMembers` |
| GET | `/zra/teams` | List Account Teams | `ListTeams` |
