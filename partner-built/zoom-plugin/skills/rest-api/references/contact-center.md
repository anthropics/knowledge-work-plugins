# Zoom Contact Center API

Authoritative endpoint inventory for Contact Center. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/contact-center/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 278 |
| Path templates | 157 |
| Tags | 25 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Address Books | 21 |
| Agent Statuses | 5 |
| Asset Library | 12 |
| Call Control | 3 |
| Campaigns | 21 |
| Dispositions | 10 |
| Engagements | 8 |
| Flows | 11 |
| Inboxes | 18 |
| Logs | 5 |
| Messaging | 1 |
| Notes | 4 |
| Operating Hours | 14 |
| Queues | 35 |
| Recordings | 4 |
| Regions | 7 |
| Reports V2(CX Analytics) | 11 |
| Reports(Legacy Reports) | 7 |
| Roles | 10 |
| Routing Profiles | 10 |
| Skills | 11 |
| SMS | 1 |
| Teams | 14 |
| Users | 22 |
| Variables | 13 |

## Endpoints by Tag

### Address Books

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/address_books` | List address books | `listAddressBooks` |
| POST | `/contact_center/address_books` | Create an address book | `createAddressBook` |
| GET | `/contact_center/address_books/contacts/{contactId}/custom_fields` | List a contact's custom fields | `ListContactCustomFields` |
| GET | `/contact_center/address_books/custom_fields` | List an address book's custom fields | `Listaddressbookcustomfields` |
| POST | `/contact_center/address_books/custom_fields` | Create an address book custom field | `Createacustomfield` |
| DELETE | `/contact_center/address_books/custom_fields/{customFieldId}` | Delete an address book custom field | `Deleteancustomfield` |
| GET | `/contact_center/address_books/custom_fields/{customFieldId}` | Get an address book's custom field | `Getaaddressbookcustomfield` |
| PATCH | `/contact_center/address_books/custom_fields/{customFieldId}` | Update an address book custom field | `Updateacustomfield` |
| GET | `/contact_center/address_books/units` | List address book units | `listUnits` |
| POST | `/contact_center/address_books/units` | Create an address book unit | `createUnit` |
| DELETE | `/contact_center/address_books/units/{unitId}` | Delete an address book unit | `deleteUnit` |
| GET | `/contact_center/address_books/units/{unitId}` | Get an address book unit | `getUnit` |
| PATCH | `/contact_center/address_books/units/{unitId}` | Update an address book unit | `updateUnit` |
| DELETE | `/contact_center/address_books/{addressBookId}` | Delete an address book | `deleteAddressBook` |
| GET | `/contact_center/address_books/{addressBookId}` | Get an address book | `getAddressBook` |
| PATCH | `/contact_center/address_books/{addressBookId}` | Update an address book | `updateAddressBook` |
| GET | `/contact_center/address_books/{addressBookId}/contacts` | List address book contacts | `listContacts` |
| POST | `/contact_center/address_books/{addressBookId}/contacts` | Create an address book contact | `createContact` |
| DELETE | `/contact_center/address_books/{addressBookId}/contacts/{contactId}` | Delete an address book contact | `contactDelete` |
| GET | `/contact_center/address_books/{addressBookId}/contacts/{contactId}` | Get an address book contact | `getContact` |
| PATCH | `/contact_center/address_books/{addressBookId}/contacts/{contactId}` | Update an address book contact | `updateContact` |

### Agent Statuses

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/system_statuses` | List system statuses | `listSystemStatus` |
| POST | `/contact_center/system_statuses` | Create a system status | `createSystemStatus` |
| DELETE | `/contact_center/system_statuses/{statusId}` | Delete a system status | `deleteSystemStatus` |
| GET | `/contact_center/system_statuses/{statusId}` | Get a system status | `getAStatus` |
| PATCH | `/contact_center/system_statuses/{statusId}` | Update a system status | `updateSystemStatus` |

### Asset Library

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/asset_library/assets` | List assets | `listAssets` |
| POST | `/contact_center/asset_library/assets` | Create an asset | `createAnAsset` |
| DELETE | `/contact_center/asset_library/assets/{assetId}` | Delete an asset | `deleteAnAsset` |
| GET | `/contact_center/asset_library/assets/{assetId}` | Get an asset | `getAnAsset` |
| PATCH | `/contact_center/asset_library/assets/{assetId}` | Update an asset | `updateAnAsset` |
| POST | `/contact_center/asset_library/assets/{assetId}/duplicate` | Duplicate an asset | `duplicateAnAsset` |
| DELETE | `/contact_center/asset_library/assets/{assetId}/items` | Delete asset items | `Deleteassetitems` |
| GET | `/contact_center/asset_library/categories` | List asset categories | `listAssetCategories` |
| POST | `/contact_center/asset_library/categories` | Create an asset category | `createAnAssetCategory` |
| DELETE | `/contact_center/asset_library/categories/{categoryId}` | Delete an asset category | `deleteAnAssetCategory` |
| GET | `/contact_center/asset_library/categories/{categoryId}` | Get an asset category | `getAnAssetCategory` |
| PATCH | `/contact_center/asset_library/categories/{categoryId}` | Update an asset category | `updateAnAssetCategory` |

### Call Control

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| PUT | `/contact_center/engagements/{engagementId}/recording/{command}` | Control an engagement's recording | `engagementRecordingControl` |
| POST | `/contact_center/users/{userId}/commands` | Command control of a user | `userControl` |
| GET | `/contact_center/users/{userId}/devices` | List user's devices | `Listuserdevices` |

### Campaigns

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/outbound_campaign/campaigns` | List outbound campaigns | `listOutboundCampaigns` |
| POST | `/contact_center/outbound_campaign/campaigns` | Create an outbound campaign | `createOutboundCampaign` |
| DELETE | `/contact_center/outbound_campaign/campaigns/{campaignId}` | Delete an outbound campaign | `deleteOutboundCampaign` |
| GET | `/contact_center/outbound_campaign/campaigns/{campaignId}` | Get an outbound campaign | `getOutboundCampaign` |
| PATCH | `/contact_center/outbound_campaign/campaigns/{campaignId}` | Update an outbound campaign | `updateOutboundCampaign` |
| PATCH | `/contact_center/outbound_campaign/campaigns/{campaignId}/status` | Update an outbound campaign status | `Updateanoutboundcampaignstatus` |
| GET | `/contact_center/outbound_campaign/contact_lists` | List campaign contact lists | `listCampaignContactLists` |
| PATCH | `/contact_center/outbound_campaign/contact_lists` | Batch update campaign contact lists | `Batchupdatecampaigncontactlists` |
| POST | `/contact_center/outbound_campaign/contact_lists` | Create a campaign contact list | `createCampaignContactList` |
| DELETE | `/contact_center/outbound_campaign/contact_lists/{contactListId}` | Remove a campaign contact list | `deleteCampaignContactList` |
| GET | `/contact_center/outbound_campaign/contact_lists/{contactListId}` | Get a campaign contact list | `getCampaignContactList` |
| PATCH | `/contact_center/outbound_campaign/contact_lists/{contactListId}` | Update a campaign contact list | `updateCampaignContactList` |
| GET | `/contact_center/outbound_campaign/contact_lists/{contactListId}/contacts` | List a campaign contact list's contacts | `listCampaignContactListContacts` |
| PATCH | `/contact_center/outbound_campaign/contact_lists/{contactListId}/contacts` | Update a batch of contacts on a campaign contact list | `Updateabatchofcontactsonacampaigncontactlist` |
| POST | `/contact_center/outbound_campaign/contact_lists/{contactListId}/contacts` | Create a campaign contact list's contact | `createCampaignContactListContact` |
| DELETE | `/contact_center/outbound_campaign/contact_lists/{contactListId}/contacts/{contactId}` | Remove campaign contact list's contact | `deleteCampaigncontactListContact` |
| GET | `/contact_center/outbound_campaign/contact_lists/{contactListId}/contacts/{contactId}` | Get a campaign contact list's contact | `getCampaignContactListContact` |
| PATCH | `/contact_center/outbound_campaign/contact_lists/{contactListId}/contacts/{contactId}` | Update contact on a campaign contact list | `updateCampaignContactListContact` |
| DELETE | `/contact_center/outbound_campaign/dnc_lists/{dncListId}/phones` | Batch delete a campaign DNC list's phones | `batchDeleteCampaignDncListPhone` |
| GET | `/contact_center/outbound_campaign/dnc_lists/{dncListId}/phones` | List campaign DNC phone numbers | `listCampaignDncListPhones` |
| POST | `/contact_center/outbound_campaign/dnc_lists/{dncListId}/phones` | Batch create a campaign DNC list's phones | `batchCreateCampaignDncListPhones` |

### Dispositions

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/dispositions` | List dispositions | `listDispositions` |
| POST | `/contact_center/dispositions` | Create a disposition | `createDisposition` |
| GET | `/contact_center/dispositions/sets` | List disposition sets | `listSets` |
| POST | `/contact_center/dispositions/sets` | Create a disposition set | `createSet` |
| DELETE | `/contact_center/dispositions/sets/{dispositionSetId}` | Delete a disposition set | `deleteSet` |
| GET | `/contact_center/dispositions/sets/{dispositionSetId}` | Get a disposition set | `getSet` |
| PATCH | `/contact_center/dispositions/sets/{dispositionSetId}` | Update a disposition set | `updateSet` |
| DELETE | `/contact_center/dispositions/{dispositionId}` | Delete a disposition | `deleteDisposition` |
| GET | `/contact_center/dispositions/{dispositionId}` | Get a disposition | `getDisposition` |
| PATCH | `/contact_center/dispositions/{dispositionId}` | Update a disposition | `updateDisposition` |

### Engagements

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/contact_center/engagement` | Start an engagement | `Startworkitemengagement` |
| GET | `/contact_center/engagements` | List engagements | `listEngagements` |
| GET | `/contact_center/engagements/{engagementId}` | Get an engagement | `getEngagement` |
| PATCH | `/contact_center/engagements/{engagementId}` | Update an engagement | `updateEngagement` |
| GET | `/contact_center/engagements/{engagementId}/attachments` | Get an engagement's attachments | `ListAttachments` |
| GET | `/contact_center/engagements/{engagementId}/events` | Get an engagement's events | `getEngagementEvents` |
| GET | `/contact_center/engagements/{engagementId}/recordings/status` | Poll an engagement recording's status | `EngagementRecordingStatus` |
| GET | `/contact_center/engagements/{engagementId}/survey` | Get an engagement's survey | `getEngagementSurvey` |

### Flows

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/flows` | List flows | `listFlows` |
| POST | `/contact_center/flows` | Import a flow | `ImportFlow` |
| DELETE | `/contact_center/flows/{flowId}` | Delete a flow | `DeleteFlow` |
| GET | `/contact_center/flows/{flowId}` | Get a flow | `getAFlow` |
| PATCH | `/contact_center/flows/{flowId}` | Edit a flow | `EditFlow` |
| DELETE | `/contact_center/flows/{flowId}/entry_points` | Remove flow entry points | `RemoveFlowEntryPoints` |
| GET | `/contact_center/flows/{flowId}/entry_points` | List flow's entry points | `ListFlowEntryPoints` |
| POST | `/contact_center/flows/{flowId}/entry_points` | Add flow entry points | `AddFlowEntryPoints` |
| GET | `/contact_center/flows/{flowId}/export` | Export a flow | `ExportFlow` |
| PUT | `/contact_center/flows/{flowId}/publish` | Publish a flow | `PublishFlow` |
| GET | `/contact_center/flows_entry_points` | List entry points | `ListentryPoints` |

### Inboxes

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/contact_center/inboxes` | Delete inboxes | `inboxesDelete` |
| GET | `/contact_center/inboxes` | List inboxes | `listInbox` |
| POST | `/contact_center/inboxes` | Create an inbox | `inboxCreate` |
| DELETE | `/contact_center/inboxes/messages` | Delete inbox messages | `inboxesMessagesDelete` |
| GET | `/contact_center/inboxes/messages` | List an account's inbox messages | `listInboxesMessages` |
| GET | `/contact_center/inboxes/{inboxId}` | Get an inbox | `getInbox` |
| PATCH | `/contact_center/inboxes/{inboxId}` | Update an inbox | `inboxUpdate` |
| PATCH | `/contact_center/inboxes/{inboxId}/email_notification` | Update an inbox email notification | `Updateaninboxemailnotification` |
| GET | `/contact_center/inboxes/{inboxId}/email_notifications` | Get inbox email notification list | `Getinboxemailnotificationlist` |
| DELETE | `/contact_center/inboxes/{inboxId}/messages` | Delete an inbox's messages | `inboxMessagesDelete` |
| GET | `/contact_center/inboxes/{inboxId}/messages` | List an inbox's messages | `listInboxMessages` |
| DELETE | `/contact_center/inboxes/{inboxId}/messages/{messageId}` | Delete an inbox message | `inboxMessageDelete` |
| DELETE | `/contact_center/inboxes/{inboxId}/queues` | Remove inbox access queues | `unassignInboxQueues` |
| GET | `/contact_center/inboxes/{inboxId}/queues` | Get inbox access queues | `listInboxQueues` |
| POST | `/contact_center/inboxes/{inboxId}/queues` | Assign inbox access queues | `assignInboxQueues` |
| DELETE | `/contact_center/inboxes/{inboxId}/users` | Unassign inbox access users | `unassignInboxUsers` |
| GET | `/contact_center/inboxes/{inboxId}/users` | Get an inbox's users | `listInboxUsers` |
| POST | `/contact_center/inboxes/{inboxId}/users` | Assign inbox access users | `assignInboxUsers` |

### Logs

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/email/messages` | List email message history | `getEmailMessageHistory` |
| GET | `/contact_center/messaging/messages` | List message history | `getMessageHistory` |
| GET | `/contact_center/sms` | List SMS logs | `listSMS` |
| GET | `/contact_center/voice_calls` | List voice call logs | `listVoiceCall` |
| GET | `/contact_center/work_item/messages` | List work item message history | `getWorkItemMessageHistory` |

### Messaging

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/contact_center/messages` | Send a message | `SendaMessage` |

### Notes

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/engagements/notes` | List notes | `notes` |
| GET | `/contact_center/engagements/{engagementId}/notes` | List engagement notes | `engagementNotes` |
| GET | `/contact_center/engagements/{engagementId}/notes/{noteId}` | Get a note | `getNote` |
| PATCH | `/contact_center/engagements/{engagementId}/notes/{noteId}` | Update a note | `noteUpdate` |

### Operating Hours

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/business_hours` | List business hours | `listBusinessHours` |
| POST | `/contact_center/business_hours` | Create business hours | `businessHourCreate` |
| DELETE | `/contact_center/business_hours/{businessHourId}` | Delete business hours | `businessHourDelete` |
| GET | `/contact_center/business_hours/{businessHourId}` | Get business hours | `getABusinessHour` |
| PATCH | `/contact_center/business_hours/{businessHourId}` | Update business hours | `businessHourUpdate` |
| GET | `/contact_center/business_hours/{businessHourId}/flows` | List the business hours' flows | `listBusinessHourFlows` |
| GET | `/contact_center/business_hours/{businessHourId}/queues` | List the business hours' queues | `listBusinessHourQueues` |
| GET | `/contact_center/closures` | List closures | `listClosures` |
| POST | `/contact_center/closures` | Create a closure set | `closuresSetCreate` |
| DELETE | `/contact_center/closures/{closureSetId}` | Delete a closure set | `closureSetDelete` |
| GET | `/contact_center/closures/{closureSetId}` | Get a closure set | `getAClosureSet` |
| PATCH | `/contact_center/closures/{closureSetId}` | Update a closure set | `closureSetUpdate` |
| GET | `/contact_center/closures/{closureSetId}/flows` | List the closures' flows | `listClosureSetFlows` |
| GET | `/contact_center/closures/{closureSetId}/queues` | List the closures' queues | `listClosureSetQueues` |

### Queues

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/queue_templates` | List queue templates | `Listqueuetemplates` |
| GET | `/contact_center/queue_templates/{queueTemplateId}` | Get a queue template | `getQueueTemplate` |
| GET | `/contact_center/queues` | List queues | `listQueues` |
| POST | `/contact_center/queues` | Create a queue | `queueCreate` |
| DELETE | `/contact_center/queues/batch` | Batch delete queues | `Batchdeletequeues` |
| POST | `/contact_center/queues/batch` | Batch create queues with a template | `Batchcreatequeueswithatemplate` |
| DELETE | `/contact_center/queues/{queueId}` | Delete a queue | `queueDelete` |
| GET | `/contact_center/queues/{queueId}` | Get a queue | `getAQueue` |
| PATCH | `/contact_center/queues/{queueId}` | Update a queue | `queueUpdate` |
| GET | `/contact_center/queues/{queueId}/agents` | List queue agents | `getQueueAgents` |
| POST | `/contact_center/queues/{queueId}/agents` | Assign queue agents | `assignQueueAgents` |
| DELETE | `/contact_center/queues/{queueId}/agents/{userId}` | Unassign a queue agent | `deleteQueueAgent` |
| PATCH | `/contact_center/queues/{queueId}/agents/{userId}` | Update a queue agent | `updateQueueAgent` |
| GET | `/contact_center/queues/{queueId}/dispositions` | List queue dispositions | `getQueueDispositions` |
| POST | `/contact_center/queues/{queueId}/dispositions` | Assign queue dispositions | `assignQueueDispositions` |
| GET | `/contact_center/queues/{queueId}/dispositions/sets` | List queue disposition sets | `getQueueDispositionSets` |
| POST | `/contact_center/queues/{queueId}/dispositions/sets` | Assign queue disposition sets | `assignQueueDispositionSets` |
| DELETE | `/contact_center/queues/{queueId}/dispositions/sets/{dispositionSetId}` | Unassign a queue disposition set | `deleteQueueDispositionSet` |
| DELETE | `/contact_center/queues/{queueId}/dispositions/{dispositionId}` | Unassign a queue disposition | `deleteQueueDisposition` |
| PATCH | `/contact_center/queues/{queueId}/interrupt` | Update a queue's interrupt settings | `updateQueueInterrupts` |
| DELETE | `/contact_center/queues/{queueId}/interrupt_menu` | Delete a queue's interrupt menu configuration | `deleteQueueInterruptMenu` |
| POST | `/contact_center/queues/{queueId}/interrupt_menu` | Assign a queue menu based interrupt | `assignQueueMenuBasedInterrupt` |
| GET | `/contact_center/queues/{queueId}/operating_hours` | Get a queue's operating hours | `getAQueueOperatingHours` |
| PATCH | `/contact_center/queues/{queueId}/operating_hours` | Update a queue's operating hours | `QueueOperatingHoursUpdate` |
| DELETE | `/contact_center/queues/{queueId}/recordings` | Delete queue recordings | `deleteQueueRecordings` |
| GET | `/contact_center/queues/{queueId}/recordings` | List queue recordings | `listQueueRecordings` |
| DELETE | `/contact_center/queues/{queueId}/scheduled_callbacks/attendees/{attendeeId}` | Delete an attendee from a scheduled callback event | `Deleteascheduledcallbackforanattendee` |
| POST | `/contact_center/queues/{queueId}/scheduled_callbacks/events` | Schedule a callback on a queue | `Scheduleacallbackonaqueue` |
| GET | `/contact_center/queues/{queueId}/scheduled_callbacks/supportive_slots` | List a queue's scheduled callbacks availability | `Listqueuescheduledcallbacksavailability` |
| GET | `/contact_center/queues/{queueId}/supervisors` | List queue supervisors | `getQueueSupervisors` |
| POST | `/contact_center/queues/{queueId}/supervisors` | Assign queue supervisors | `assignQueueSupervisors` |
| DELETE | `/contact_center/queues/{queueId}/supervisors/{userId}` | Unassign a queue supervisor | `deleteQueueSupervisor` |
| DELETE | `/contact_center/queues/{queueId}/teams` | Unassign multiple teams in a queue | `batchDeleteQueueTeams` |
| POST | `/contact_center/queues/{queueId}/teams` | Assign queue teams | `assignQueueTeams` |
| DELETE | `/contact_center/queues/{queueId}/teams/{teamId}` | Unassign a queue team | `deleteQueueTeam` |

### Recordings

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/contact_center/engagements/{engagementId}/recordings` | Delete engagement recordings | `deleteEngagementRecordings` |
| GET | `/contact_center/engagements/{engagementId}/recordings` | List engagement recordings | `listEngagementRecordings` |
| GET | `/contact_center/recordings` | List recordings | `listRecordings` |
| DELETE | `/contact_center/recordings/{recordingId}` | Delete a recording | `deleteRecording` |

### Regions

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/regions` | List regions | `ListRegions` |
| POST | `/contact_center/regions` | Create a region | `CreateARegion` |
| DELETE | `/contact_center/regions/{regionId}` | Delete a region | `DeleteARegion` |
| GET | `/contact_center/regions/{regionId}` | Get a region | `GetARegion` |
| PATCH | `/contact_center/regions/{regionId}` | Update a region | `UpdateARegion` |
| GET | `/contact_center/regions/{regionId}/users` | List a region's users | `ListRegion'sUsers` |
| POST | `/contact_center/regions/{regionId}/users` | Assign users to a region | `AssignUsersToARegion` |

### Reports V2(CX Analytics)

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/analytics/dataset/historical/agent_performance` | List historical agent performance dataset data | `Listhistoricalagentperformancedatasetdata` |
| GET | `/contact_center/analytics/dataset/historical/agent_timecard` | List historical agent timecard dataset data | `Listhistoricalagenttimecarddatasetdata` |
| GET | `/contact_center/analytics/dataset/historical/disposition` | List historical disposition dataset data | `Listhistoricaldispositiondatasetdata` |
| GET | `/contact_center/analytics/dataset/historical/engagement` | List historical engagement dataset data | `Listengagementdatasetdata` |
| GET | `/contact_center/analytics/dataset/historical/expert_assist` | List historical expert assist dataset data | `Listexpertassistdatasetdata` |
| GET | `/contact_center/analytics/dataset/historical/flow_performance` | List historical flow performance dataset data | `Listhistoricalflowperformancedatasetdata` |
| GET | `/contact_center/analytics/dataset/historical/outbound_dialer_performance` | List historical outbound dialer performance dataset data | `Listhistoricaloutbounddialerperformancedatasetdata` |
| GET | `/contact_center/analytics/dataset/historical/queue_performance` | List historical queue performance dataset data | `Listhistoricalqueueperformancedatasetdata` |
| GET | `/contact_center/analytics/log/historical/engagement` | List historical engagement log data | `Listhistoricalengagementlogs` |
| GET | `/contact_center/analytics/log/historical/journey` | List historical Zoom Phone to Contact Center call journey data | `ListhistoricalZoomphonetozcccalljourneydata` |
| GET | `/contact_center/reports/operation_logs` | List operation logs | `listOperationLogs` |

### Reports(Legacy Reports)

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/analytics/agents/leg_metrics` | List agent leg reports | `listAgentLegMetric` |
| GET | `/contact_center/analytics/agents/status_history` | List agent's status history reports | `listAgentStatusHistory` |
| GET | `/contact_center/analytics/agents/time_sheets` | List agent's time sheet reports | `listAgentTimeSheet` |
| GET | `/contact_center/analytics/historical/details/metrics` | List historical detail reports | `listHistoricalDetailMetric` |
| GET | `/contact_center/analytics/historical/queues/agents/metrics` | List historical agent reports by queue | `listQueueAgentsMetrics` |
| GET | `/contact_center/analytics/historical/queues/metrics` | List historical queue reports | `listHistoricalQueueMetric` |
| GET | `/contact_center/analytics/historical/queues/{queueId}/agents/metrics` | List historical queue's agents reports | `listQueueAgentMetric` |

### Roles

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/roles` | List roles | `listRoles` |
| POST | `/contact_center/roles` | Create a role | `createRole` |
| POST | `/contact_center/roles/duplicate` | Duplicate a role | `Duplicatearole` |
| DELETE | `/contact_center/roles/{roleId}` | Delete a role | `deleteRole` |
| GET | `/contact_center/roles/{roleId}` | Get a role | `getRole` |
| PATCH | `/contact_center/roles/{roleId}` | Update a role | `updateRole` |
| DELETE | `/contact_center/roles/{roleId}/privileges` | Delete role privileges | `Deleteroleprivileges` |
| GET | `/contact_center/roles/{roleId}/users` | List users of a role | `getRoleUsers` |
| POST | `/contact_center/roles/{roleId}/users` | Assign a role | `assignRoleUsers` |
| DELETE | `/contact_center/roles/{roleId}/users/{userId}` | Unassign a role | `deleteRoleUser` |

### Routing Profiles

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/agent_routing_profiles` | List agent routing profiles | `Listagentroutingprofiles` |
| POST | `/contact_center/agent_routing_profiles` | Create an agent routing profile | `Createanagentroutingprofile` |
| DELETE | `/contact_center/agent_routing_profiles/{agentRoutingProfileId}` | Delete an agent routing profile | `Deleteanagentroutingprofile` |
| GET | `/contact_center/agent_routing_profiles/{agentRoutingProfileId}` | Get an agent routing profile | `getAgentRoutingProfile` |
| PATCH | `/contact_center/agent_routing_profiles/{agentRoutingProfileId}` | Update an agent routing profile's details | `Updateanagentroutingprofile'sdetails` |
| GET | `/contact_center/consumer_routing_profiles` | List consumer routing profiles | `Listconsumerroutingprofiles` |
| POST | `/contact_center/consumer_routing_profiles` | Create a consumer routing profile | `Createaconsumerroutingprofile` |
| DELETE | `/contact_center/consumer_routing_profiles/{consumerRoutingProfileId}` | Delete a consumer routing profile | `Deleteaconsumerroutingprofile` |
| GET | `/contact_center/consumer_routing_profiles/{consumerRoutingProfileId}` | Get a consumer routing profile | `Getaconsumerroutingprofile` |
| PATCH | `/contact_center/consumer_routing_profiles/{consumerRoutingProfileId}` | Update a consumer routing profile's details | `Updateaconsumerroutingprofile'sdetails` |

### Skills

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/skills` | List skills | `listSkills` |
| POST | `/contact_center/skills` | Create a skill | `skillCreate` |
| GET | `/contact_center/skills/categories` | List skill categories | `listSkillCategory` |
| POST | `/contact_center/skills/categories` | Create a skill category | `SkillCategoryCreate` |
| DELETE | `/contact_center/skills/categories/{skillCategoryId}` | Delete a skill category | `SkillCategoryDelete` |
| GET | `/contact_center/skills/categories/{skillCategoryId}` | Get a skill category | `getSkillCategory` |
| PATCH | `/contact_center/skills/categories/{skillCategoryId}` | Update a skill category | `SkillCategoryUpdate` |
| DELETE | `/contact_center/skills/{skillId}` | Delete a skill | `skillDelete` |
| GET | `/contact_center/skills/{skillId}` | Get a skill | `getSkill` |
| PATCH | `/contact_center/skills/{skillId}` | Update a skill | `skillNameUpdate` |
| GET | `/contact_center/skills/{skillId}/users` | List users of a skill | `listSkillUsers` |

### SMS

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/contact_center/sms` | Send an SMS | `contactCenterSMS` |

### Teams

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/teams` | List teams | `listTeams` |
| POST | `/contact_center/teams` | Create a team | `CreateTeam` |
| DELETE | `/contact_center/teams/{teamId}` | Delete a team | `deleteTeam` |
| GET | `/contact_center/teams/{teamId}` | Get a team | `getTeamDetail` |
| PATCH | `/contact_center/teams/{teamId}` | Update a team | `Updateateam` |
| DELETE | `/contact_center/teams/{teamId}/agents` | Unassign team agents | `unassignTeamAgents` |
| GET | `/contact_center/teams/{teamId}/agents` | List team agents | `listTeamAgents` |
| POST | `/contact_center/teams/{teamId}/agents` | Assign team agents | `assignTeamAgents` |
| GET | `/contact_center/teams/{teamId}/children` | List a team's child teams | `getTeamChildTeams` |
| PATCH | `/contact_center/teams/{teamId}/move` | Move a team | `moveTeam` |
| GET | `/contact_center/teams/{teamId}/parents` | List team's parent teams | `getTeamParentTeams` |
| DELETE | `/contact_center/teams/{teamId}/supervisors` | Unassign team supervisors | `unassignTeamSupervisors` |
| GET | `/contact_center/teams/{teamId}/supervisors` | List team supervisors | `listTeamSupervisors` |
| POST | `/contact_center/teams/{teamId}/supervisors` | Assign team supervisors | `assignTeamSupervisors` |

### Users

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/contact_center/users` | Batch delete user profiles | `batchDeleteUsers` |
| GET | `/contact_center/users` | List users' profiles | `users` |
| PATCH | `/contact_center/users` | Batch update user profiles | `BatchUpdateUsers` |
| POST | `/contact_center/users` | Create a user's profile | `createUser` |
| POST | `/contact_center/users/batch` | Batch create user profiles | `BatchCreateUsers` |
| PATCH | `/contact_center/users/status` | Batch update user status | `Batchupdateuserstatus` |
| GET | `/contact_center/users/templates` | List user templates | `ListUserTemplates` |
| POST | `/contact_center/users/templates` | Create a user template | `createAUserTemplate` |
| DELETE | `/contact_center/users/templates/{templateId}` | Delete a user template | `deleteAUserTemplate` |
| GET | `/contact_center/users/templates/{templateId}` | Get a user template | `Getanusertemplate` |
| PATCH | `/contact_center/users/templates/{templateId}` | Update a user template | `updateAUserTemplate` |
| DELETE | `/contact_center/users/{userId}` | Delete a user's profile | `userDelete` |
| GET | `/contact_center/users/{userId}` | Get a user's profile | `userGet` |
| PATCH | `/contact_center/users/{userId}` | Update a user's profile | `userUpdate` |
| PATCH | `/contact_center/users/{userId}/opt_in_out_queues` | Batch opt in or opt out a user's queues | `BatchOptInOrOutUserQueues` |
| GET | `/contact_center/users/{userId}/queues` | List user's queues | `listUserQueues` |
| DELETE | `/contact_center/users/{userId}/recordings` | Delete a user's recordings | `deleteUserRecordings` |
| GET | `/contact_center/users/{userId}/recordings` | List a user's recordings | `listUserRecordings` |
| GET | `/contact_center/users/{userId}/skills` | List user's skills | `ListAUserSkills` |
| POST | `/contact_center/users/{userId}/skills` | Assign user's skills | `assignSkills` |
| DELETE | `/contact_center/users/{userId}/skills/{skillId}` | Unassign user's skill | `deleteASkill` |
| PATCH | `/contact_center/users/{userId}/status` | Update a user's status | `Updateauser'sstatus` |

### Variables

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contact_center/variable_logs` | List variable logs | `listVariableLogs` |
| DELETE | `/contact_center/variable_logs/{variableLogId}` | Delete a variable log | `deleteVariableLog` |
| GET | `/contact_center/variable_logs/{variableLogId}` | Get a variable log | `getVariableLog` |
| GET | `/contact_center/variables` | List variables | `variables` |
| POST | `/contact_center/variables` | Create a variable | `createVariable` |
| GET | `/contact_center/variables/groups` | List variable groups | `listVariableGroups` |
| POST | `/contact_center/variables/groups` | Create a variable group | `createVariableGroup` |
| DELETE | `/contact_center/variables/groups/{variableGroupId}` | Delete a variable group | `DeleteGroup` |
| GET | `/contact_center/variables/groups/{variableGroupId}` | Get a variable group | `getAVariableGroup` |
| PATCH | `/contact_center/variables/groups/{variableGroupId}` | Update a variable group | `updateVariableGroup` |
| DELETE | `/contact_center/variables/{variableId}` | Delete a variable | `variableDelete` |
| GET | `/contact_center/variables/{variableId}` | Get a variable | `variableGet` |
| PATCH | `/contact_center/variables/{variableId}` | Update a variable | `variableUpdate` |
