# Granular OAuth Scopes

> Source: https://developers.zoom.us/docs/integrations/oauth-scopes-granular/


## Conference Room Connector (CRC)


### Account

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get Cisco/Polycom Room Account Setting](/docs/api/rest/reference/crc/methods/#operation/getCiscoPolycomRoomAccountSetting) | `crc:read:rooms_account_settings:admin` |
| [Get Cisco/Polycom Room Account Setting](/docs/api/rest/reference/crc/ma/#operation/getCiscoPolycomRoomAccountSetting) | `crc:read:rooms_account_settings:master` |
| [Update Cisco/Polycom Room Account Setting](/docs/api/rest/reference/crc/methods/#operation/UpdateCiscoPolycomRoomAccountSetting) | `crc:update:rooms_account_settings:admin` |
| [Update Cisco/Polycom Room Account Setting](/docs/api/rest/reference/crc/ma/#operation/UpdateCiscoPolycomRoomAccountSetting) | `crc:update:rooms_account_settings:master` |

### Api Connector

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get an API Connector's private key](/docs/api/rest/reference/crc/methods/#operation/GetanAPIConnector'sprivatekey) | `crc:read:apiconnector_private_key:admin` |
| [Get an API Connector's private key](/docs/api/rest/reference/crc/ma/#operation/GetanAPIConnector'sprivatekey) | `crc:read:apiconnector_private_key:master` |
| [Get an API Connector](/docs/api/rest/reference/crc/methods/#operation/GetAPIConnector) | `crc:read:apiconnector:admin` |
| [Get an API Connector](/docs/api/rest/reference/crc/ma/#operation/GetAPIConnector) | `crc:read:apiconnector:master` |
| [List API Connectors](/docs/api/rest/reference/crc/methods/#operation/GetListAPIConnectors) | `crc:read:list_apiconnectors:admin` |
| [List API Connectors](/docs/api/rest/reference/crc/ma/#operation/GetListAPIConnectors) | `crc:read:list_apiconnectors:master` |
| [Delete an API Connector](/docs/api/rest/reference/crc/methods/#operation/DeleteAPIConnector) | `crc:delete:apiconnector:admin` |
| [Delete an API Connector](/docs/api/rest/reference/crc/ma/#operation/DeleteAPIConnector) | `crc:delete:apiconnector:master` |
| [Create an API Connector](/docs/api/rest/reference/crc/methods/#operation/CreateAPIConnector) | `crc:write:apiconnector:admin` |
| [Create an API Connector](/docs/api/rest/reference/crc/ma/#operation/CreateAPIConnector) | `crc:write:apiconnector:master` |
| [Update an API Connector's private key](/docs/api/rest/reference/crc/methods/#operation/UpdateAPIConnectorPrivateKey) | `crc:update:apiconnector_private_key:admin` |
| [Update an API Connector's private key](/docs/api/rest/reference/crc/ma/#operation/UpdateAPIConnectorPrivateKey) | `crc:update:apiconnector_private_key:master` |
| [Update an API Connector](/docs/api/rest/reference/crc/methods/#operation/UpdateAPIConnector) | `crc:update:apiconnector:admin` |
| [Update an API Connector](/docs/api/rest/reference/crc/ma/#operation/UpdateAPIConnector) | `crc:update:apiconnector:master` |

### Cisco/Polycom Rooms

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a Managed Room](/docs/api/rest/reference/crc/methods/#operation/GetaManagedRoom) | `crc:read:room:admin` |
| [Get a Managed Room](/docs/api/rest/reference/crc/ma/#operation/GetaManagedRoom) | `crc:read:room:master` |
| [Delete a managed room](/docs/api/rest/reference/crc/methods/#operation/Deleteamanagedroom) | `crc:delete:room:admin` |
| [Delete a managed room](/docs/api/rest/reference/crc/ma/#operation/Deleteamanagedroom) | `crc:delete:room:master` |
| [List Managed Rooms](/docs/api/rest/reference/crc/methods/#operation/ListManagedRooms) | `crc:read:list_rooms:admin` |
| [List Managed Rooms](/docs/api/rest/reference/crc/ma/#operation/ListManagedRooms) | `crc:read:list_rooms:master` |
| [Update a Managed Room](/docs/api/rest/reference/crc/methods/#operation/UpdateaManagedRoom) | `crc:update:room:admin` |
| [Update a Managed Room](/docs/api/rest/reference/crc/ma/#operation/UpdateaManagedRoom) | `crc:update:room:master` |
| [Create a Managed Room](/docs/api/rest/reference/crc/methods/#operation/CreateaManagedRoom) | `crc:write:room:admin` |
| [Create a Managed Room](/docs/api/rest/reference/crc/ma/#operation/CreateaManagedRoom) | `crc:write:room:master` |

### Participant

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get participant identifier code](/docs/api/rest/reference/crc/methods/#operation/get_participant_identifier_code) | `crc:read:participant_identifier_code:admin`, `crc:read:participant_identifier_code:master` |

### Room Template

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete a room template](/docs/api/rest/reference/crc/methods/#operation/Deletearoomtemplate) | `crc:delete:rooms_template:admin` |
| [Delete a room template](/docs/api/rest/reference/crc/ma/#operation/Deletearoomtemplate) | `crc:delete:rooms_template:master` |
| [List Room Templates](/docs/api/rest/reference/crc/methods/#operation/ListRoomTemplates) | `crc:read:list_rooms_templates:admin` |
| [List Room Templates](/docs/api/rest/reference/crc/ma/#operation/ListRoomTemplates) | `crc:read:list_rooms_templates:master` |
| [Get a Room Template](/docs/api/rest/reference/crc/methods/#operation/GetaRoomTemplate) | `crc:read:rooms_template:admin` |
| [Get a Room Template](/docs/api/rest/reference/crc/ma/#operation/GetaRoomTemplate) | `crc:read:rooms_template:master` |
| [Create a Room Template](/docs/api/rest/reference/crc/methods/#operation/CreateaRoomTemplate) | `crc:write:rooms_template:admin` |
| [Create a Room Template](/docs/api/rest/reference/crc/ma/#operation/CreateaRoomTemplate) | `crc:write:rooms_template:master` |
| [Update a Room Template](/docs/api/rest/reference/crc/methods/#operation/UpdateaRoomTemplate) | `crc:update:rooms_template:admin` |
| [Update a Room Template](/docs/api/rest/reference/crc/ma/#operation/UpdateaRoomTemplate) | `crc:update:rooms_template:master` |

## Contact Center


### Address Books

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create an address book custom field](/docs/api/rest/reference/contact-center/methods/#operation/Createacustomfield) | `contact_center:write:address_book_custom_field:admin` |
| [Get an address book](/docs/api/rest/reference/contact-center/methods/#operation/getAddressBook) | `contact_center:read:address_book:admin` |
| [Create an address book](/docs/api/rest/reference/contact-center/methods/#operation/createAddressBook) | `contact_center:write:address_book:admin` |
| [Get an address book's custom field](/docs/api/rest/reference/contact-center/methods/#operation/Getaaddressbookcustomfield) | `contact_center:read:address_book_custom_field:admin` |
| [Update an address book](/docs/api/rest/reference/contact-center/methods/#operation/updateAddressBook) | `contact_center:update:address_book:admin` |
| [Get an address book unit](/docs/api/rest/reference/contact-center/methods/#operation/getUnit) | `contact_center:read:address_book_unit:admin` |
| [Delete an address book](/docs/api/rest/reference/contact-center/methods/#operation/deleteAddressBook) | `contact_center:delete:address_book:admin` |
| [Delete an address book unit](/docs/api/rest/reference/contact-center/methods/#operation/deleteUnit) | `contact_center:delete:address_book_unit:admin` |
| [Delete an address book custom field](/docs/api/rest/reference/contact-center/methods/#operation/Deleteancustomfield) | `contact_center:delete:address_book_custom_field:admin` |
| [List address book units](/docs/api/rest/reference/contact-center/methods/#operation/listUnits) | `contact_center:read:list_address_book_units:admin` |
| [Update an address book contact](/docs/api/rest/reference/contact-center/methods/#operation/updateContact) | `contact_center:update:address_book_contact:admin` |
| [List an address book's custom fields](/docs/api/rest/reference/contact-center/methods/#operation/Listaddressbookcustomfields) | `contact_center:read:address_book_custom_field:admin` |
| [Create an address book contact](/docs/api/rest/reference/contact-center/methods/#operation/createContact) | `contact_center:write:address_book_contact:admin` |
| [Update an address book unit](/docs/api/rest/reference/contact-center/methods/#operation/updateUnit) | `contact_center:update:address_book_unit:admin` |
| [Create an address book unit](/docs/api/rest/reference/contact-center/methods/#operation/createUnit) | `contact_center:write:address_book_unit:admin` |
| [List address book contacts](/docs/api/rest/reference/contact-center/methods/#operation/listContacts) | `contact_center:read:list_address_book_contacts:admin` |
| [Get an address book contact](/docs/api/rest/reference/contact-center/methods/#operation/getContact) | `contact_center:read:address_book_contact:admin` |
| [List address books](/docs/api/rest/reference/contact-center/methods/#operation/listAddressBooks) | `contact_center:read:list_address_books:admin` |
| [Update an address book custom field](/docs/api/rest/reference/contact-center/methods/#operation/Updateacustomfield) | `contact_center:update:address_book_custom_field:admin` |
| [Delete an address book contact](/docs/api/rest/reference/contact-center/methods/#operation/contactDelete) | `contact_center:delete:address_book_contact:admin` |
| [List a contact's custom fields](/docs/api/rest/reference/contact-center/methods/#operation/ListContactCustomFields) | `contact_center:read:address_book_custom_field:admin` |

### Agent Statuses

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a system status](/docs/api/rest/reference/contact-center/methods/#operation/getAStatus) | `contact_center:read:system_status:admin` |
| [Create a system status](/docs/api/rest/reference/contact-center/methods/#operation/createSystemStatus) | `contact_center:write:system_status:admin` |
| [Update a system status](/docs/api/rest/reference/contact-center/methods/#operation/updateSystemStatus) | `contact_center:update:system_status:admin` |
| [Delete a system status](/docs/api/rest/reference/contact-center/methods/#operation/deleteSystemStatus) | `contact_center:delete:system_status:admin` |
| [List system statuses](/docs/api/rest/reference/contact-center/methods/#operation/listSystemStatus) | `contact_center:read:list_system_statues:admin` |

### Asset Library

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List assets](/docs/api/rest/reference/contact-center/methods/#operation/listAssets) | `contact_center:read:asset_library:admin` |
| [Update an asset category](/docs/api/rest/reference/contact-center/methods/#operation/updateAnAssetCategory) | `contact_center:write:asset_library:admin` |
| [Create an asset](/docs/api/rest/reference/contact-center/methods/#operation/createAnAsset) | `contact_center:write:asset_library:admin` |
| [List asset categories](/docs/api/rest/reference/contact-center/methods/#operation/listAssetCategories) | `contact_center:read:asset_library:admin` |
| [Update an asset](/docs/api/rest/reference/contact-center/methods/#operation/updateAnAsset) | `contact_center:write:asset_library:admin` |
| [Delete an asset category](/docs/api/rest/reference/contact-center/methods/#operation/deleteAnAssetCategory) | `contact_center:delete:asset_library:admin` |
| [Delete an asset](/docs/api/rest/reference/contact-center/methods/#operation/deleteAnAsset) | `contact_center:delete:asset_library:admin` |
| [Get an asset](/docs/api/rest/reference/contact-center/methods/#operation/getAnAsset) | `contact_center:read:asset_library:admin` |
| [Create an asset category](/docs/api/rest/reference/contact-center/methods/#operation/createAnAssetCategory) | `contact_center:write:asset_library:admin` |
| [Duplicate an asset](/docs/api/rest/reference/contact-center/methods/#operation/duplicateAnAsset) | `contact_center:write:asset_library:admin` |
| [Delete asset items](/docs/api/rest/reference/contact-center/methods/#operation/Deleteassetitems) | `contact_center:write:asset_library:admin` |
| [Get an asset category](/docs/api/rest/reference/contact-center/methods/#operation/getAnAssetCategory) | `contact_center:read:asset_library:admin` |

### Call Control

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Command control of a user](/docs/api/rest/reference/contact-center/methods/#operation/userControl) | `contact_center:write:user_control:admin` |
| [List user's devices](/docs/api/rest/reference/contact-center/methods/#operation/Listuserdevices) | `contact_center:read:user_device:admin` |
| [Control an engagement's recording](/docs/api/rest/reference/contact-center/methods/#operation/engagementRecordingControl) | `contact_center:update:engagement_recording_control:admin` |

### Campaigns

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create an outbound campaign](/docs/api/rest/reference/contact-center/methods/#operation/createOutboundCampaign) | `contact_center:write:outbound_campaign:admin` |
| [List campaign contact list contacts](/docs/api/rest/reference/contact-center/methods/#operation/listCampaignContactListContacts) | `contact_center:read:outbound_campaign_contacts:admin` |
| [Get a campaign contact list](/docs/api/rest/reference/contact-center/methods/#operation/getCampaignContactList) | `contact_center:read:outbound_campaign_contactlist:admin` |
| [Delete an outbound campaign](/docs/api/rest/reference/contact-center/methods/#operation/deleteOutboundCampaign) | `contact_center:delete:outbound_campaign:admin` |
| [Create a campaign contact list's contact](/docs/api/rest/reference/contact-center/methods/#operation/createCampaignContactListContact) | `contact_center:write:outbound_campaign_contacts:admin` |
| [Update an outbound campaign status](/docs/api/rest/reference/contact-center/methods/#operation/Updateanoutboundcampaignstatus) | `contact_center:update:outbound_campaign:admin` |
| [Update a campaign contact list](/docs/api/rest/reference/contact-center/methods/#operation/updateCampaignContactList) | `contact_center:update:outbound_campaign_contactlist:admin` |
| [Get an outbound campaign](/docs/api/rest/reference/contact-center/methods/#operation/getOutboundCampaign) | `contact_center:read:outbound_campaign:admin` |
| [Get a campaign contact list's contact](/docs/api/rest/reference/contact-center/methods/#operation/getCampaignContactListContact) | `contact_center:read:outbound_campaign_contacts:admin` |
| [Create a campaign contact list](/docs/api/rest/reference/contact-center/methods/#operation/createCampaignContactList) | `contact_center:write:outbound_campaign_contactlist:admin` |
| [List campaign contact lists](/docs/api/rest/reference/contact-center/methods/#operation/listCampaignContactLists) | `contact_center:read:outbound_campaign_contactlist:admin` |
| [List outbound campaigns](/docs/api/rest/reference/contact-center/methods/#operation/listOutboundCampaigns) | `contact_center:read:outbound_campaign:admin` |
| [Update contact on a campaign contact list](/docs/api/rest/reference/contact-center/methods/#operation/updateCampaignContactListContact) | `contact_center:update:outbound_campaign_contacts:admin` |
| [Remove a campaign contact list](/docs/api/rest/reference/contact-center/methods/#operation/deleteCampaignContactList) | `contact_center:delete:outbound_campaign_contactlist:admin` |
| [Update an outbound campaign](/docs/api/rest/reference/contact-center/methods/#operation/updateOutboundCampaign) | `contact_center:update:outbound_campaign:admin` |
| [Remove campaign contact list's contact](/docs/api/rest/reference/contact-center/methods/#operation/deleteCampaigncontactListContact) | `contact_center:delete:outbound_campaign_contacts:admin` |

### Dispositions

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create a disposition set](/docs/api/rest/reference/contact-center/methods/#operation/createSet) | `contact_center:write:disposition_set:admin` |
| [List disposition sets](/docs/api/rest/reference/contact-center/methods/#operation/listSets) | `contact_center:read:list_disposition_sets:admin` |
| [Get a disposition set](/docs/api/rest/reference/contact-center/methods/#operation/getSet) | `contact_center:read:disposition_set:admin` |
| [Create a disposition](/docs/api/rest/reference/contact-center/methods/#operation/createDisposition) | `contact_center:write:disposition:admin` |
| [Delete a disposition](/docs/api/rest/reference/contact-center/methods/#operation/deleteDisposition) | `contact_center:delete:disposition:admin` |
| [Update a disposition set](/docs/api/rest/reference/contact-center/methods/#operation/updateSet) | `contact_center:update:disposition_set:admin` |
| [List dispositions](/docs/api/rest/reference/contact-center/methods/#operation/listDispositions) | `contact_center:read:list_dispositions:admin` |
| [Delete a disposition set](/docs/api/rest/reference/contact-center/methods/#operation/deleteSet) | `contact_center:delete:disposition_set:admin` |
| [Update a disposition](/docs/api/rest/reference/contact-center/methods/#operation/updateDisposition) | `contact_center:update:disposition:admin` |
| [Get a disposition](/docs/api/rest/reference/contact-center/methods/#operation/getDisposition) | `contact_center:read:disposition:admin` |

### Engagements

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Poll an engagement recording's status](/docs/api/rest/reference/contact-center/methods/#operation/EngagementRecordingStatus) | `contact_center:read:engagement_recording_status:admin` |
| [Update an engagement](/docs/api/rest/reference/contact-center/methods/#operation/updateEngagement) | `contact_center:update:engagement:admin` |
| [Get an engagement's events](/docs/api/rest/reference/contact-center/methods/#operation/getEngagementEvents) | `contact_center:read:engagement:admin` |
| [Start an engagement](/docs/api/rest/reference/contact-center/methods/#operation/Startworkitemengagement) | `contact_center:write:engagement:admin` |
| [List engagements](/docs/api/rest/reference/contact-center/methods/#operation/listEngagements) | `contact_center:read:list_engagements:admin` |
| [Get an engagement's survey](/docs/api/rest/reference/contact-center/methods/#operation/getEngagementSurvey) | `contact_center:read:engagement:admin` |
| [Get an engagement](/docs/api/rest/reference/contact-center/methods/#operation/getEngagement) | `contact_center:read:engagement:admin` |
| [Get an engagement's attachments](/docs/api/rest/reference/contact-center/methods/#operation/ListAttachments) | `contact_center:read:attachment:admin` |

### Flows

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Import a flow](/docs/api/rest/reference/contact-center/methods/#operation/ImportFlow) | `contact_center:write:flow:admin` |
| [Remove flow entry points](/docs/api/rest/reference/contact-center/methods/#operation/RemoveFlowEntryPoints) | `contact_center:delete:flow:admin` |
| [List flows](/docs/api/rest/reference/contact-center/methods/#operation/listFlows) | `contact_center:read:list_flows:admin` |
| [List flow's entry points](/docs/api/rest/reference/contact-center/methods/#operation/ListFlowEntryPoints) | `contact_center:read:flow:admin` |
| [List entry points](/docs/api/rest/reference/contact-center/methods/#operation/ListentryPoints) | `contact_center:read:flow:admin` |
| [Add flow entry points](/docs/api/rest/reference/contact-center/methods/#operation/AddFlowEntryPoints) | `contact_center:write:flow:admin` |
| [Edit a flow](/docs/api/rest/reference/contact-center/methods/#operation/EditFlow) | `contact_center:update:flow:admin` |
| [Get a flow](/docs/api/rest/reference/contact-center/methods/#operation/getAFlow) | `contact_center:read:flow:admin` |
| [Delete a flow](/docs/api/rest/reference/contact-center/methods/#operation/DeleteFlow) | `contact_center:delete:flow:admin` |
| [Publish a flow](/docs/api/rest/reference/contact-center/methods/#operation/PublishFlow) | `contact_center:update:flow:admin` |
| [Export a flow](/docs/api/rest/reference/contact-center/methods/#operation/ExportFlow) | `contact_center:read:flow:admin` |

### Inboxes

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create an inbox](/docs/api/rest/reference/contact-center/methods/#operation/inboxCreate) | `contact_center:write:inbox:admin` |
| [List an account's inbox messages](/docs/api/rest/reference/contact-center/methods/#operation/listInboxesMessages) | `contact_center:read:inbox_messages:admin` |
| [Unassign inbox access users](/docs/api/rest/reference/contact-center/methods/#operation/unassignInboxUsers) | `contact_center:delete:inbox_user:admin` |
| [Update an inbox](/docs/api/rest/reference/contact-center/methods/#operation/inboxUpdate) | `contact_center:update:inbox:admin` |
| [Delete inboxes](/docs/api/rest/reference/contact-center/methods/#operation/inboxesDelete) | `contact_center:delete:inbox:admin` |
| [Remove inbox access queues](/docs/api/rest/reference/contact-center/methods/#operation/unassignInboxQueues) | `contact_center:delete:inbox_queue:admin` |
| [Delete an inbox's messages](/docs/api/rest/reference/contact-center/methods/#operation/inboxMessagesDelete) | `contact_center:delete:inbox_messages:admin` |
| [Get inbox email notification list](/docs/api/rest/reference/contact-center/methods/#operation/Getinboxemailnotificationlist) | `contact_center:read:inbox:admin` |
| [Get an inbox's users](/docs/api/rest/reference/contact-center/methods/#operation/listInboxUsers) | `contact_center:read:inbox_user:admin` |
| [Delete inbox messages](/docs/api/rest/reference/contact-center/methods/#operation/inboxesMessagesDelete) | `contact_center:delete:inbox_messages:admin` |
| [Assign inbox access users](/docs/api/rest/reference/contact-center/methods/#operation/assignInboxUsers) | `contact_center:write:inbox_user:admin` |
| [List an inbox's messages](/docs/api/rest/reference/contact-center/methods/#operation/listInboxMessages) | `contact_center:read:inbox_messages:admin` |
| [Get inbox access queues](/docs/api/rest/reference/contact-center/methods/#operation/listInboxQueues) | `contact_center:read:list_inbox_queues:admin` |
| [Update an inbox email notification](/docs/api/rest/reference/contact-center/methods/#operation/Updateaninboxemailnotification) | `contact_center:update:inbox:admin` |
| [Assign inbox access queues](/docs/api/rest/reference/contact-center/methods/#operation/assignInboxQueues) | `contact_center:write:inbox_queue:admin` |
| [List inboxes](/docs/api/rest/reference/contact-center/methods/#operation/listInbox) | `contact_center:read:list_inboxes:admin` |
| [Delete an inbox message](/docs/api/rest/reference/contact-center/methods/#operation/inboxMessageDelete) | `contact_center:delete:inbox_message:admin` |
| [Get an inbox](/docs/api/rest/reference/contact-center/methods/#operation/getInbox) | `contact_center:read:inbox:admin` |

### Logs

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List message history](/docs/api/rest/reference/contact-center/methods/#operation/getMessageHistory) | `contact_center:read:messaging:admin` |
| [List work item message history](/docs/api/rest/reference/contact-center/methods/#operation/getWorkItemMessageHistory) | `contact_center:read:engagement_log:admin` |
| [List voice call logs](/docs/api/rest/reference/contact-center/methods/#operation/listVoiceCall) | `contact_center:read:voice_call_log:admin` |
| [List voice call logs](/docs/api/rest/reference/contact-center/ma/#operation/listVoiceCall) | `contact_center:read:voice_call_log:master` |
| [List email message history](/docs/api/rest/reference/contact-center/methods/#operation/getEmailMessageHistory) | `contact_center:read:engagement_log:admin` |
| [List SMS logs](/docs/api/rest/reference/contact-center/methods/#operation/listSMS) | `contact_center:read:sms_log:admin` |
| [List SMS logs](/docs/api/rest/reference/contact-center/ma/#operation/listSMS) | `contact_center:read:sms_log:master` |

### Messaging

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Send a message](/docs/api/rest/reference/contact-center/methods/#operation/SendaMessage) | `contact_center:write:messaging:admin` |

### Notes

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List notes](/docs/api/rest/reference/contact-center/methods/#operation/notes) | `contact_center:read:list_notes:admin` |
| [Get a note](/docs/api/rest/reference/contact-center/methods/#operation/getNote) | `contact_center:read:note:admin` |
| [Update a note](/docs/api/rest/reference/contact-center/methods/#operation/noteUpdate) | `contact_center:update:note` |
| [List engagement notes](/docs/api/rest/reference/contact-center/methods/#operation/engagementNotes) | `contact_center:read:list_notes:admin` |

### Operating Hours

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create business hours](/docs/api/rest/reference/contact-center/methods/#operation/businessHourCreate) | `contact_center:write:business_hour:admin` |
| [List the business hours' queues](/docs/api/rest/reference/contact-center/methods/#operation/listBusinessHourQueues) | `contact_center:read:business_hours_queue:admin` |
| [Update a closure set](/docs/api/rest/reference/contact-center/methods/#operation/closureSetUpdate) | `contact_center:update:closure_hour:admin` |
| [Create a closure set](/docs/api/rest/reference/contact-center/methods/#operation/closuresSetCreate) | `contact_center:write:closure_hour:admin` |
| [Update business hours](/docs/api/rest/reference/contact-center/methods/#operation/businessHourUpdate) | `contact_center:update:business_hour:admin` |
| [List business hours](/docs/api/rest/reference/contact-center/methods/#operation/listBusinessHours) | `contact_center:read:list_business_hours:admin` |
| [List the closures' queues](/docs/api/rest/reference/contact-center/methods/#operation/listClosureSetQueues) | `contact_center:read:closure_hour_queue:admin` |
| [Get a closure set](/docs/api/rest/reference/contact-center/methods/#operation/getAClosureSet) | `contact_center:read:closure_hour:admin` |
| [List the business hours' flows](/docs/api/rest/reference/contact-center/methods/#operation/listBusinessHourFlows) | `contact_center:read:business_hours_flow:admin` |
| [Delete business hours](/docs/api/rest/reference/contact-center/methods/#operation/businessHourDelete) | `contact_center:delete:business_hour:admin` |
| [Get business hours](/docs/api/rest/reference/contact-center/methods/#operation/getABusinessHour) | `contact_center:read:business_hour:admin` |
| [Delete a closure set](/docs/api/rest/reference/contact-center/methods/#operation/closureSetDelete) | `contact_center:delete:closure_hour:admin` |
| [List closures](/docs/api/rest/reference/contact-center/methods/#operation/listClosures) | `contact_center:read:list_closure_hours:admin` |
| [List the closures' flows](/docs/api/rest/reference/contact-center/methods/#operation/listClosureSetFlows) | `contact_center:read:clousre_hour_flow:admin` |

### Queues

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update a queue's operating hours](/docs/api/rest/reference/contact-center/methods/#operation/QueueOperatingHoursUpdate) | `contact_center:patch:queue_operating_hours:admin` |
| [Update a queue agent](/docs/api/rest/reference/contact-center/methods/#operation/updateQueueAgent) | `contact_center:update:queue_agent:admin` |
| [Unassign a queue agent](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueAgent) | `contact_center:delete:queue_agent:admin` |
| [Assign queue agents](/docs/api/rest/reference/contact-center/methods/#operation/assignQueueAgents) | `contact_center:write:queue_agent:admin` |
| [Delete a queue](/docs/api/rest/reference/contact-center/methods/#operation/queueDelete) | `contact_center:delete:queue:admin` |
| [Assign queue dispositions](/docs/api/rest/reference/contact-center/methods/#operation/assignQueueDispositions) | `contact_center:write:queue disposition:admin` |
| [Delete an attendee from a scheduled callback event](/docs/api/rest/reference/contact-center/methods/#operation/Deleteascheduledcallbackforanattendee) | `contact_center:delete:queue:admin` |
| [List queue dispositions](/docs/api/rest/reference/contact-center/methods/#operation/getQueueDispositions) | `contact_center:read:list_dispositions:admin` |
| [Batch delete queues](/docs/api/rest/reference/contact-center/methods/#operation/Batchdeletequeues) | `contact_center:delete:queue:admin` |
| [List queues](/docs/api/rest/reference/contact-center/methods/#operation/listQueues) | `contact_center:read:list_queues:admin` |
| [Update a queue's interrupt settings](/docs/api/rest/reference/contact-center/methods/#operation/updateQueueInterrupts) | `contact_center:update:queue:admin` |
| [Get a queue](/docs/api/rest/reference/contact-center/methods/#operation/getAQueue) | `contact_center:read:queue:admin` |
| [Unassign a queue disposition](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueDisposition) | `contact_center:delete:queue_disposition:admin` |
| [Assign queue teams](/docs/api/rest/reference/contact-center/methods/#operation/assignQueueTeams) | `contact_center:write:queue_team:admin` |
| [Unassign a queue team](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueTeam) | `contact_center:delete:queue_team:admin` |
| [Create a queue](/docs/api/rest/reference/contact-center/methods/#operation/queueCreate) | `contact_center:write:queue:admin` |
| [Delete a queue's interrupt menu configuration](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueInterruptMenu) | `contact_center:delete:queue:admin` |
| [Assign a queue menu based interrupt](/docs/api/rest/reference/contact-center/methods/#operation/assignQueueMenuBasedInterrupt) | `contact_center:update:queue:admin` |
| [Unassign a queue supervisor](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueSupervisor) | `contact_center:delete:queue_supervisor:admin` |
| [Update a queue](/docs/api/rest/reference/contact-center/methods/#operation/queueUpdate) | `contact_center:update:queue:admin` |
| [Unassign a queue disposition set](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueDispositionSet) | `contact_center:delete:queue_disposition_set:admin` |
| [List queue templates](/docs/api/rest/reference/contact-center/methods/#operation/Listqueuetemplates) | `contact_center:read:queue:admin` |
| [Unassign multiple teams in a queue](/docs/api/rest/reference/contact-center/methods/#operation/batchDeleteQueueTeams) | `contact_center:delete:queue_team:admin` |
| [List queue disposition sets](/docs/api/rest/reference/contact-center/methods/#operation/getQueueDispositionSets) | `contact_center:read:list_disposition_sets:admin` |
| [Batch create queues with a template](/docs/api/rest/reference/contact-center/methods/#operation/Batchcreatequeueswithatemplate) | `contact_center:write:queue:admin` |
| [Get a queue's operating hours](/docs/api/rest/reference/contact-center/methods/#operation/getAQueueOperatingHours) | `contact_center:read:queue_operating_hours:admin` |
| [List queue agents](/docs/api/rest/reference/contact-center/methods/#operation/getQueueAgents) | `contact_center:read:list_queue_agents:admin` |
| [Schedule a callback on a queue](/docs/api/rest/reference/contact-center/methods/#operation/Scheduleacallbackonaqueue) | `contact_center:write:queue:admin` |
| [Assign queue supervisors](/docs/api/rest/reference/contact-center/methods/#operation/assignQueueSupervisors) | `contact_center:delete:queue_supervisor:admin` |
| [Assign queue disposition sets](/docs/api/rest/reference/contact-center/methods/#operation/assignQueueDispositionSets) | `contact_center:write:queue_disposition_set:admin` |
| [List queue supervisors](/docs/api/rest/reference/contact-center/methods/#operation/getQueueSupervisors) | `contact_center:delete:queue_supervisor:admin` |
| [List a queue's scheduled callbacks availability](/docs/api/rest/reference/contact-center/methods/#operation/Listqueuescheduledcallbacksavailability) | `contact_center:read:queue:admin` |

### Recordings

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete engagement recordings](/docs/api/rest/reference/contact-center/methods/#operation/deleteEngagementRecordings) | `contact_center:delete:recording:admin` |
| [List a user's recordings](/docs/api/rest/reference/contact-center/methods/#operation/listUserRecordings) | `contact_center:read:list_recordings:admin`, `contact_center:read:list_recordings` |
| [Delete a recording](/docs/api/rest/reference/contact-center/methods/#operation/deleteRecording) | `contact_center:delete:recording:admin` |
| [List recordings](/docs/api/rest/reference/contact-center/methods/#operation/listRecordings) | `contact_center:read:list_recordings:admin` |
| [List engagement recordings](/docs/api/rest/reference/contact-center/methods/#operation/listEngagementRecordings) | `contact_center:read:list_recordings:admin` |
| [List queue recordings](/docs/api/rest/reference/contact-center/methods/#operation/listQueueRecordings) | `contact_center:read:list_recordings:admin`, `contact_center:read:list_recordings` |
| [Delete queue recordings](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueRecordings) | `contact_center:delete:recording:admin` |
| [Delete a user's recordings](/docs/api/rest/reference/contact-center/methods/#operation/deleteUserRecordings) | `contact_center:delete:recording:admin` |

### Regions

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List regions](/docs/api/rest/reference/contact-center/methods/#operation/ListRegions) | `contact_center:read:list_regions:admin` |
| [Update a region](/docs/api/rest/reference/contact-center/methods/#operation/UpdateARegion) | `contact_center:udpate:region:admin` |
| [Delete a region](/docs/api/rest/reference/contact-center/methods/#operation/DeleteARegion) | `contact_center:delete:region:admin` |
| [Assign users to a region](/docs/api/rest/reference/contact-center/methods/#operation/AssignUsersToARegion) | `contact_center:write:region_user:admin` |
| [Create a region](/docs/api/rest/reference/contact-center/methods/#operation/CreateARegion) | `contact_center:write:region:admin` |
| [Get a region](/docs/api/rest/reference/contact-center/methods/#operation/GetARegion) | `contact_center:read:region:admin` |
| [List a region's users](/docs/api/rest/reference/contact-center/methods/#operation/ListRegion'sUsers) | `contact_center:read:list_region_users:admin` |

### Reports V2(CX Analytics)

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List historical queue performance dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricalqueueperformancedatasetdata) | `contact_center:read:dataset_queue_performance:admin` |
| [List operation logs](/docs/api/rest/reference/contact-center/methods/#operation/listOperationLogs) | `contact_center:read:operation_logs:admin` |
| [List historical flow performance dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricalflowperformancedatasetdata) | `contact_center:read:dataset_flow_performance:admin` |
| [List historical disposition dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricaldispositiondatasetdata) | `contact_center:read:dataset_disposition:admin` |
| [List historical agent timecard dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricalagenttimecarddatasetdata) | `contact_center:read:dataset_agent_timecard:admin` |
| [List historical engagement dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listengagementdatasetdata) | `contact_center:read:dataset_engagement:admin` |
| [List historical Zoom Phone to Contact Center call journey data](/docs/api/rest/reference/contact-center/methods/#operation/ListhistoricalZoomphonetozcccalljourneydata) | `contact_center:read:call_journey_log:admin` |
| [List historical outbound dialer performance dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricaloutbounddialerperformancedatasetdata) | `contact_center:read:dataset_outbound_dialer_performance:admin` |
| [List historical engagement log data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricalengagementlogs) | `contact_center:read:engagement_log:admin` |
| [List historical agent performance dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricalagentperformancedatasetdata) | `contact_center:read:dataset_agent_performance:admin` |

### Reports(Legacy Reports)

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List historical queue's agents reports](/docs/api/rest/reference/contact-center/methods/#operation/listQueueAgentMetric) | `contact_center:read:agent_report:admin` |
| [List historical detail reports](/docs/api/rest/reference/contact-center/methods/#operation/listHistoricalDetailMetric) | `contact_center:read:engagement_report:admin` |
| [List agent leg reports](/docs/api/rest/reference/contact-center/methods/#operation/listAgentLegMetric) | `contact_center:read:agent_report:admin` |
| [List agent's status history reports](/docs/api/rest/reference/contact-center/methods/#operation/listAgentStatusHistory) | `contact_center:read:agent_status_report:admin` |
| [List agent's time sheet reports](/docs/api/rest/reference/contact-center/methods/#operation/listAgentTimeSheet) | `contact_center:read:agent_report:admin` |
| [List historical agent reports by queue](/docs/api/rest/reference/contact-center/methods/#operation/listQueueAgentsMetrics) | `contact_center:read:agent_report:admin` |
| [List historical queue reports](/docs/api/rest/reference/contact-center/methods/#operation/listHistoricalQueueMetric) | `contact_center:read:queue_report:admin` |

### Roles

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Unassign a role](/docs/api/rest/reference/contact-center/methods/#operation/deleteRoleUser) | `contact_center:delete:role_user:admin` |
| [Create a role](/docs/api/rest/reference/contact-center/methods/#operation/createRole) | `contact_center:write:role:admin` |
| [Delete a role](/docs/api/rest/reference/contact-center/methods/#operation/deleteRole) | `contact_center:delete:role:admin` |
| [Get a role](/docs/api/rest/reference/contact-center/methods/#operation/getRole) | `contact_center:read:role:admin` |
| [Update a role](/docs/api/rest/reference/contact-center/methods/#operation/updateRole) | `contact_center:update:role:admin` |
| [Delete role privileges](/docs/api/rest/reference/contact-center/methods/#operation/Deleteroleprivileges) | `contact_center:delete:role:admin` |
| [List users of a role](/docs/api/rest/reference/contact-center/methods/#operation/getRoleUsers) | `contact_center:read:list_role_users:admin` |
| [List roles](/docs/api/rest/reference/contact-center/methods/#operation/listRoles) | `contact_center:read:list_roles:admin` |
| [Assign a role](/docs/api/rest/reference/contact-center/methods/#operation/assignRoleUsers) | `contact_center:write:role_user:admin` |
| [Duplicate a role](/docs/api/rest/reference/contact-center/methods/#operation/Duplicatearole) | `contact_center:write:role:admin` |

### Routing Profiles

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a consumer routing profile](/docs/api/rest/reference/contact-center/methods/#operation/Getaconsumerroutingprofile) | `contact_center:read:consumer_routing_profile:admin` |
| [Update a consumer routing profile's details](/docs/api/rest/reference/contact-center/methods/#operation/Updateaconsumerroutingprofile'sdetails) | `contact_center:update:consumer_routing_profile:admin` |
| [List consumer routing profiles](/docs/api/rest/reference/contact-center/methods/#operation/Listconsumerroutingprofiles) | `contact_center:read:consumer_routing_profile:admin` |
| [Create a consumer routing profile](/docs/api/rest/reference/contact-center/methods/#operation/Createaconsumerroutingprofile) | `contact_center:write:consumer_routing_profile:admin` |
| [Get an agent routing profile](/docs/api/rest/reference/contact-center/methods/#operation/getAgentRoutingProfile) | `contact_center:read:agent_routing_profile:admin` |
| [List agent routing profiles](/docs/api/rest/reference/contact-center/methods/#operation/Listagentroutingprofiles) | `contact_center:read:agent_routing_profile:admin` |
| [Update an agent routing profile's details](/docs/api/rest/reference/contact-center/methods/#operation/Updateanagentroutingprofile'sdetails) | `contact_center:update:agent_routing_profile:admin` |
| [Delete a consumer routing profile](/docs/api/rest/reference/contact-center/methods/#operation/Deleteaconsumerroutingprofile) | `contact_center:delete:consumer_routing_profile:admin` |
| [Delete an agent routing profile](/docs/api/rest/reference/contact-center/methods/#operation/Deleteanagentroutingprofile) | `contact_center:delete:agent_routing_profile:admin` |
| [Create an agent routing profile](/docs/api/rest/reference/contact-center/methods/#operation/Createanagentroutingprofile) | `contact_center:write:agent_routing_profile:admin` |

### SMS

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Send an SMS](/docs/api/rest/reference/contact-center/methods/#operation/contactCenterSMS) | `contact_center:write:sms:admin` |

### Skills

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a skill category](/docs/api/rest/reference/contact-center/methods/#operation/getSkillCategory) | `contact_center:read:skill_category:admin` |
| [Create a skill](/docs/api/rest/reference/contact-center/methods/#operation/skillCreate) | `contact_center:write:skill:admin` |
| [Delete a skill](/docs/api/rest/reference/contact-center/methods/#operation/skillDelete) | `contact_center:delete:skill:admin` |
| [Update a skill](/docs/api/rest/reference/contact-center/methods/#operation/skillNameUpdate) | `contact_center:update:skill:admin` |
| [List users of a skill](/docs/api/rest/reference/contact-center/methods/#operation/listSkillUsers) | `contact_center:read:list_skill_users:admin` |
| [List skills](/docs/api/rest/reference/contact-center/methods/#operation/listSkills) | `contact_center:read:list_skills:admin` |
| [Create a skill category](/docs/api/rest/reference/contact-center/methods/#operation/SkillCategoryCreate) | `contact_center:write:skill_category:admin` |
| [Get a skill](/docs/api/rest/reference/contact-center/methods/#operation/getSkill) | `contact_center:read:skill:admin` |
| [Delete a skill category](/docs/api/rest/reference/contact-center/methods/#operation/SkillCategoryDelete) | `contact_center:delete:skill_category:admin` |
| [Update a skill category](/docs/api/rest/reference/contact-center/methods/#operation/SkillCategoryUpdate) | `contact_center:update:skill_category:admin` |
| [List skill categories](/docs/api/rest/reference/contact-center/methods/#operation/listSkillCategory) | `contact_center:read:list_skill_categories:admin` |

### Teams

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Unassign team supervisors](/docs/api/rest/reference/contact-center/methods/#operation/unassignTeamSupervisors) | `contact_center:delete:team:admin` |
| [Get a team](/docs/api/rest/reference/contact-center/methods/#operation/getTeamDetail) | `contact_center:read:team:admin` |
| [List teams](/docs/api/rest/reference/contact-center/methods/#operation/listTeams) | `contact_center:read:team:admin` |
| [List team's parent teams](/docs/api/rest/reference/contact-center/methods/#operation/getTeamParentTeams) | `contact_center:read:team:admin` |
| [List team agents](/docs/api/rest/reference/contact-center/methods/#operation/listTeamAgents) | `contact_center:read:team:admin` |
| [Create a team](/docs/api/rest/reference/contact-center/methods/#operation/CreateTeam) | `contact_center:write:team:admin` |
| [Move a team](/docs/api/rest/reference/contact-center/methods/#operation/moveTeam) | `contact_center:update:team:admin` |
| [Delete a team](/docs/api/rest/reference/contact-center/methods/#operation/deleteTeam) | `contact_center:delete:team:admin` |
| [List a team's child teams](/docs/api/rest/reference/contact-center/methods/#operation/getTeamChildTeams) | `contact_center:read:team:admin` |
| [Assign team agents](/docs/api/rest/reference/contact-center/methods/#operation/assignTeamAgents) | `contact_center:write:team:admin` |
| [Update a team](/docs/api/rest/reference/contact-center/methods/#operation/Updateateam) | `contact_center:update:team:admin` |
| [Assign team supervisors](/docs/api/rest/reference/contact-center/methods/#operation/assignTeamSupervisors) | `contact_center:write:team:admin` |
| [List team supervisors](/docs/api/rest/reference/contact-center/methods/#operation/listTeamSupervisors) | `contact_center:read:team:admin` |
| [Unassign team agents](/docs/api/rest/reference/contact-center/methods/#operation/unassignTeamAgents) | `contact_center:delete:team:admin` |

### Users

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Batch update user status](/docs/api/rest/reference/contact-center/methods/#operation/Batchupdateuserstatus) | `contact_center:write:batch_users:admin` |
| [Create a user's profile](/docs/api/rest/reference/contact-center/methods/#operation/createUser) | `contact_center:write:user:admin` |
| [Update a user's status](/docs/api/rest/reference/contact-center/methods/#operation/Updateauser'sstatus) | `contact_center:update:user:admin` |
| [Batch create user profiles](/docs/api/rest/reference/contact-center/methods/#operation/BatchCreateUsers) | `contact_center:write:batch_users:admin` |
| [Batch delete user profiles](/docs/api/rest/reference/contact-center/methods/#operation/batchDeleteUsers) | `contact_center:delete:batch_users:admin` |
| [Get a user template](/docs/api/rest/reference/contact-center/methods/#operation/Getanusertemplate) | `contact_center:read:user_templates:admin` |
| [List user templates](/docs/api/rest/reference/contact-center/methods/#operation/ListUserTemplates) | `contact_center:read:user_templates:admin` |
| [Delete a user template](/docs/api/rest/reference/contact-center/methods/#operation/deleteAUserTemplate) | `contact_center:delete:user_templates:admin` |
| [Unassign user's skill](/docs/api/rest/reference/contact-center/methods/#operation/deleteASkill) | `contact_center:delete:user_skill:admin` |
| [List user's queues](/docs/api/rest/reference/contact-center/methods/#operation/listUserQueues) | `contact_center:read:list_user_queues:admin` |
| [Assign user's skills](/docs/api/rest/reference/contact-center/methods/#operation/assignSkills) | `contact_center:write:user_skill:admin` |
| [Update a user template](/docs/api/rest/reference/contact-center/methods/#operation/updateAUserTemplate) | `contact_center:update:user_templates:admin` |
| [List user's skills](/docs/api/rest/reference/contact-center/methods/#operation/ListAUserSkills) | `contact_center:read:list_user_skills:admin` |
| [Create a user template](/docs/api/rest/reference/contact-center/methods/#operation/createAUserTemplate) | `contact_center:write:user_templates:admin` |
| [Update a user's profile](/docs/api/rest/reference/contact-center/methods/#operation/userUpdate) | `contact_center:update:user:admin` |
| [Delete a user's profile](/docs/api/rest/reference/contact-center/methods/#operation/userDelete) | `contact_center:delete:user:admin` |
| [Get a user's profile](/docs/api/rest/reference/contact-center/methods/#operation/userGet) | `contact_center:read:user:admin` |
| [Batch update user profiles](/docs/api/rest/reference/contact-center/methods/#operation/BatchUpdateUsers) | `contact_center:update:batch_users:admin` |
| [List users' profiles](/docs/api/rest/reference/contact-center/methods/#operation/users) | `contact_center:read:list_users:admin` |

### Variables

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete a variable](/docs/api/rest/reference/contact-center/methods/#operation/variableDelete) | `contact_center:delete:variable:admin` |
| [List variables](/docs/api/rest/reference/contact-center/methods/#operation/variables) | `contact_center:read:list_variables:admin` |
| [List variable groups](/docs/api/rest/reference/contact-center/methods/#operation/listVariableGroups) | `contact_center:read:list_variable_groups:admin` |
| [Get a variable log](/docs/api/rest/reference/contact-center/methods/#operation/getVariableLog) | `contact_center:read:variable_log:admin` |
| [Get a variable group](/docs/api/rest/reference/contact-center/methods/#operation/getAVariableGroup) | `contact_center:read:variable_group:admin` |
| [List variable logs](/docs/api/rest/reference/contact-center/methods/#operation/listVariableLogs) | `contact_center:read:list_variable_logs:admin` |
| [Create a variable](/docs/api/rest/reference/contact-center/methods/#operation/createVariable) | `contact_center:write:variable:admin` |
| [Delete a variable group](/docs/api/rest/reference/contact-center/methods/#operation/DeleteGroup) | `contact_center:delete:variable_group:admin` |
| [Delete a variable log](/docs/api/rest/reference/contact-center/methods/#operation/deleteVariableLog) | `contact_center:delete:variable_log:admin` |
| [Update a variable group](/docs/api/rest/reference/contact-center/methods/#operation/updateVariableGroup) | `contact_center:update:variable_group:admin` |
| [Get a variable](/docs/api/rest/reference/contact-center/methods/#operation/variableGet) | `contact_center:read:variable:admin` |
| [Create a variable group](/docs/api/rest/reference/contact-center/methods/#operation/createVariableGroup) | `contact_center:write:variable_group:admin` |
| [Update a variable](/docs/api/rest/reference/contact-center/methods/#operation/variableUpdate) | `contact_center:update:variable:admin` |

## Docs


### File Management

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create a new file](/docs/api/rest/reference/Docs/methods/#operation/CreateDoc) | `docs:write:file`, `docs:write:file:admin` |
| [Modify metadata of a file](/docs/api/rest/reference/Docs/methods/#operation/ModifyMetadata) | `docs:update:file`, `docs:update:file:admin` |
| [Get metadata of a file](/docs/api/rest/reference/Docs/methods/#operation/QueryFileMetadata) | `docs:read:file`, `docs:read:file:admin` |
| [List all children of a file](/docs/api/rest/reference/Docs/methods/#operation/ListAllChildren) | `docs:read:list_children`, `docs:read:list_children:admin` |
| [Delete a file](/docs/api/rest/reference/Docs/methods/#operation/DeleteFile) | `docs:delete:file`, `docs:delete:file:admin` |

### File Uploads

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create file upload for docs import or attachments](/docs/api/rest/reference/Docs/methods/#operation/Uploadfilefordocsimportorattachments) | `docs:write:file_uploads`, `docs:write:file_uploads:admin` |

### Import

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get file import status](/docs/api/rest/reference/Docs/methods/#operation/Getdocsfileimportstatus) | `docs:read:import`, `docs:read:import:admin` |
| [Create a new file by import](/docs/api/rest/reference/Docs/methods/#operation/Createanewfilebyimport) | `docs:write:import`, `docs:write:import:admin` |

## Marketplace


### App

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List apps](/docs/api/rest/reference/marketplace/methods/#operation/ListApps) | `marketplace:read:list_apps:admin` |
| [Get an app's user requests](/docs/api/rest/reference/marketplace/methods/#operation/getAppUserRequests) | `marketplace:read:app_request:admin` |
| [Update app's request status](/docs/api/rest/reference/marketplace/methods/#operation/updateAppRequestStatus) | `marketplace:update:app_request:admin` |
| [Update app pre approval setting](/docs/api/rest/reference/marketplace/methods/#operation/Updateapppreapprovalsetting) | `marketplace:write:app_pre_approve:admin` |
| [Generate Zoom App Deeplink](/docs/api/rest/reference/marketplace/methods/#operation/GenerateZoomAppDeeplink) | `marketplace:write:app_deeplink:admin` |
| [Get user's custom field values](/docs/api/rest/reference/marketplace/methods/#operation/getCustomFieldValues) | `marketplace:read:custom_fields:admin`, `marketplace:read:custom_fields` |
| [Get API call logs](/docs/api/rest/reference/marketplace/methods/#operation/Getapicalllogs) | `marketplace:read:list_api_logs:admin` |
| [Send app notifications](/docs/api/rest/reference/marketplace/methods/#operation/Sendappnotifications) | `marketplace:write:notifications` |
| [Create apps](/docs/api/rest/reference/marketplace/methods/#operation/CreateApps) | `marketplace:write:app`, `marketplace:write:app:admin` |
| [Create apps](/docs/api/rest/reference/marketplace/ma/#operation/CreateApps) | `marketplace:write:app:master` |
| [Get app user entitlements](/docs/api/rest/reference/marketplace/methods/#operation/getAppUserEntitlementRequests) | `marketplace:read:list_user_entitlements`, `marketplace:read:list_user_entitlements:admin` |
| [Get a user's entitlements](/docs/api/rest/reference/marketplace/methods/#operation/getUserEntitlementRequests) | `marketplace:read:list_user_entitlements`, `marketplace:read:list_user_entitlements:admin` |
| [Get information about an app](/docs/api/rest/reference/marketplace/methods/#operation/getAppInfo) | `marketplace:read:app`, `marketplace:read:app:admin` |
| [Add app allow requests for users](/docs/api/rest/reference/marketplace/methods/#operation/AddAppAllowRequestsForUsers) | `marketplace:write:app_request:admin` |
| [Rotate client secret](/docs/api/rest/reference/marketplace/methods/#operation/RotateClientSecret) | `marketplace:update:client_secret` |
| [Get a user's app requests](/docs/api/rest/reference/marketplace/methods/#operation/getUserAppRequests) | `marketplace:read:list_user_app_requests:admin`, `marketplace:read:list_user_app_requests` |
| [Enable or disable user app subscription](/docs/api/rest/reference/marketplace/methods/#operation/Enable/Disableuserappsubscription) | `marketplace:write:app:admin` |
| [Deletes an app](/docs/api/rest/reference/marketplace/methods/#operation/deleteApp) | `marketplace:write:app`, `marketplace:write:app:admin` |

### Manifest

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Export an app manifest from an existing app](/docs/api/rest/reference/marketplace/methods/#operation/getAppManifest) | `marketplace:read:app`, `marketplace:read:app:admin` |
| [Update an app by manifest](/docs/api/rest/reference/marketplace/methods/#operation/updateAppByManifest) | `marketplace:write:app`, `marketplace:write:app:admin` |
| [Validate an app manifest](/docs/api/rest/reference/marketplace/methods/#operation/validatingManifest) | `marketplace:read:app`, `marketplace:read:app:admin` |

## QSS


### Dashboards

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List meeting participants QoS Summary](/docs/api/rest/reference/qss/methods/#operation/dashboardMeetingParticipantsQOSSummary) | `dashboard:read:list_meeting_participants_qos:admin` |
| [List meeting participants QoS Summary](/docs/api/rest/reference/qss/ma/#operation/dashboardMeetingParticipantsQOSSummary) | `dashboard:read:list_meeting_participants_qos:master` |
| [List webinar participants QoS Summary](/docs/api/rest/reference/qss/methods/#operation/dashboardWebinarParticipantsQOSSummary) | `dashboard:read:list_webinar_participants_qos:admin` |
| [List webinar participants QoS Summary](/docs/api/rest/reference/qss/ma/#operation/dashboardWebinarParticipantsQOSSummary) | `dashboard:read:list_webinar_participants_qos:master` |

## SCIM


### Group

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create a group](/docs/api/rest/reference/scim-api/methods/#operation/groupScim2Create) | `scim2:admin` |
| [List groups](/docs/api/rest/reference/scim-api/methods/#operation/groupSCIM2List) | `scim2:admin` |
| [Delete a group](/docs/api/rest/reference/scim-api/methods/#operation/groupSCIM2Delete) | `scim2:admin` |
| [Get a group](/docs/api/rest/reference/scim-api/methods/#operation/groupSCIM2Get) | `scim2:admin` |
| [Update a group](/docs/api/rest/reference/scim-api/methods/#operation/groupSCIM2Update) | `scim2:admin` |

### User

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Deactivate a user](/docs/api/rest/reference/scim-api/methods/#operation/userADSCIM2Deactivate) | `scim2:admin` |
| [Delete a user](/docs/api/rest/reference/scim-api/methods/#operation/userSCIM2Delete) | `scim2:admin` |
| [Update a user](/docs/api/rest/reference/scim-api/methods/#operation/userSCIM2Update) | `scim2:admin` |
| [Get a user](/docs/api/rest/reference/scim-api/methods/#operation/userSCIM2Get) | `scim2:admin` |
| [Create a user](/docs/api/rest/reference/scim-api/methods/#operation/userScim2Create) | `scim2:admin` |
| [List users](/docs/api/rest/reference/scim-api/methods/#operation/userSCIM2List) | `scim2:admin` |

## Tasks


### Assignee

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Add assignees to a task](/docs/api/rest/reference/Tasks/methods/#operation/addTasksAssignees) | `tasks:write:assignees`, `tasks:write:assignees:admin` |
| [Get assignees of a task](/docs/api/rest/reference/Tasks/methods/#operation/GetAssigneesOfATask) | `tasks:read:assignees`, `tasks:read:assignees:admin` |
| [Remove Assignee from task](/docs/api/rest/reference/Tasks/methods/#operation/removeTaskAssignee) | `tasks:delete:assignees`, `tasks:delete:assignees:admin` |

### Collaborator

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Add collaborators to a task](/docs/api/rest/reference/Tasks/methods/#operation/addTasksCollaborators) | `tasks:write:collaborators`, `tasks:write:collaborators:admin` |
| [Remove collaborator from task](/docs/api/rest/reference/Tasks/methods/#operation/removeTaskCollaborator) | `tasks:delete:collaborator:admin`, `tasks:delete:collaborator` |
| [Get collaborators of a task](/docs/api/rest/reference/Tasks/methods/#operation/Getcollaboratorsofatask) | `tasks:read:list_collaborators`, `tasks:read:list_collaborators:admin` |

### Comment

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete a task's comment](/docs/api/rest/reference/Tasks/methods/#operation/DeleteTaskComment) | `tasks:delete:comment:admin`, `tasks:delete:comment` |
| [Get a task's comments](/docs/api/rest/reference/Tasks/methods/#operation/GetAV1TasksComment) | `tasks:read:comments`, `tasks:read:comments:admin` |
| [Add a comment to task](/docs/api/rest/reference/Tasks/methods/#operation/addComment) | `tasks:write:comment:admin`, `tasks:write:comment` |

### Tasks

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update task fields](/docs/api/rest/reference/Tasks/methods/#operation/updateTask) | `tasks:update:task`, `tasks:update:task:admin` |
| [Delete a task](/docs/api/rest/reference/Tasks/methods/#operation/deleteTask) | `tasks:delete:task:admin`, `tasks:delete:task` |
| [Create a new task](/docs/api/rest/reference/Tasks/methods/#operation/createTask) | `tasks:write:task` |
| [Get task details](/docs/api/rest/reference/Tasks/methods/#operation/getTaskDetail) | `tasks:read:task`, `tasks:read:task:admin` |
| [List tasks](/docs/api/rest/reference/Tasks/methods/#operation/getMyTasks) | `tasks:read:list_tasks:admin`, `tasks:read:list_tasks` |

## Team Chat


### Chat Channel Mention Group

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Add channel members to a mention group](/docs/api/rest/reference/chat/methods/#operation/addAChannelMembersToMentionGroup) | `team_chat:update:mention_group`, `team_chat:update:mention_group:admin` |
| [List channel mention groups](/docs/api/rest/reference/chat/methods/#operation/getChannelMentionGroup) | `team_chat:read:mention_group`, `team_chat:read:mention_group:admin` |
| [Remove channel mention group members](/docs/api/rest/reference/chat/methods/#operation/removeChannelMentionGroupMembers) | `team_chat:update:mention_group`, `team_chat:update:mention_group:admin` |
| [Update a channel mention group information](/docs/api/rest/reference/chat/methods/#operation/updateChannelMentionGroup) | `team_chat:update:mention_group`, `team_chat:update:mention_group:admin` |
| [Create a channel mention group](/docs/api/rest/reference/chat/methods/#operation/createChannelMentionGroup) | `team_chat:write:mention_group:admin`, `team_chat:write:mention_group` |
| [Delete a channel mention group](/docs/api/rest/reference/chat/methods/#operation/deleteAChannelMentionGroup) | `team_chat:delete:mention_group`, `team_chat:delete:mention_group:admin` |
| [List the members of a mention group](/docs/api/rest/reference/chat/methods/#operation/listTheMembersOfMentionGroup) | `team_chat:read:mention_group`, `team_chat:read:mention_group:admin` |

### Chat Channels

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List channel members](/docs/api/rest/reference/chat/methods/#operation/listUserLevelChannelMembers) | `team_chat:read:list_members`, `team_chat:read:list_members:admin` |
| [Create a channel](/docs/api/rest/reference/chat/methods/#operation/createChannel) | `team_chat:write:user_channel`, `team_chat:write:user_channel:admin` |
| [List channel members (Groups)](/docs/api/rest/reference/chat/methods/#operation/listChannelMembersGroups) | `team_chat:read:list_groups:admin` |
| [Update a channel](/docs/api/rest/reference/chat/methods/#operation/updateUserLevelChannel) | `team_chat:update:channel`, `team_chat:update:channel:admin` |
| [Remove a member (group)](/docs/api/rest/reference/chat/methods/#operation/removeAMemberGroup) | `team_chat:delete:group:admin` |
| [Remove a member](/docs/api/rest/reference/chat/methods/#operation/removeAUserLevelChannelMember) | `team_chat:delete:member`, `team_chat:delete:member:admin` |
| [List channel activity logs](/docs/api/rest/reference/chat/methods/#operation/listAllChannelActivityLogs) | `team_chat:read:list_channel_activity_logs:admin` |
| [Leave a channel](/docs/api/rest/reference/chat/methods/#operation/leaveChannel) | `team_chat:delete:member`, `team_chat:delete:member:admin` |
| [Perform operations on channels](/docs/api/rest/reference/chat/methods/#operation/PerformOperationsOnChannels) | `team_chat:update:archive_channels`, `team_chat:update:archive_channels:admin` |
| [List user's channels](/docs/api/rest/reference/chat/methods/#operation/getChannels) | `team_chat:read:list_user_channels`, `team_chat:read:list_user_channels:admin` |
| [Invite channel members (Groups)](/docs/api/rest/reference/chat/methods/#operation/inviteChannelMembersGroups) | `team_chat:write:groups:admin` |
| [Join a channel](/docs/api/rest/reference/chat/methods/#operation/joinChannel) | `team_chat:write:member` |
| [Invite channel members](/docs/api/rest/reference/chat/methods/#operation/InviteUserLevelChannelMembers) | `team_chat:write:members`, `team_chat:write:members:admin` |
| [Get a channel](/docs/api/rest/reference/chat/methods/#operation/getUserLevelChannel) | `team_chat:read:channel`, `team_chat:read:channel:admin` |
| [Delete a channel](/docs/api/rest/reference/chat/methods/#operation/deleteUserLevelChannel) | `team_chat:delete:channel`, `team_chat:delete:channel:admin` |
| [Batch remove members from a channel](/docs/api/rest/reference/chat/methods/#operation/batchRemoveChannelMembers) | `team_chat:delete:batch_members`, `team_chat:delete:batch_members:admin` |

### Chat Channels (Account-level)

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List channel administrators](/docs/api/rest/reference/chat/methods/#operation/listChannelAdministrators) | `team_chat:read:list_administrators:admin` |
| [Get a channel](/docs/api/rest/reference/chat/methods/#operation/getChannel) | `team_chat:read:user_channel`, `team_chat:read:user_channel:admin` |
| [Invite channel members](/docs/api/rest/reference/chat/methods/#operation/inviteChannelMembers) | `team_chat:write:members`, `team_chat:write:members:admin` |
| [Batch demote channel administrators](/docs/api/rest/reference/chat/methods/#operation/batchDemoteChannelAdministrators) | `team_chat:delete:batch_administrators:admin` |
| [Search user's or account's channels](/docs/api/rest/reference/chat/methods/#operation/searchChannels) | `team_chat:write:search_channels`, `team_chat:write:search_channels:admin` |
| [Promote channel members to administrators](/docs/api/rest/reference/chat/methods/#operation/promoteChannelMembersAsAdmin) | `team_chat:write:administrator:admin` |
| [Remove a member](/docs/api/rest/reference/chat/methods/#operation/removeAChannelMember) | `team_chat:delete:member:admin` |
| [Batch delete channels](/docs/api/rest/reference/chat/methods/#operation/batchDeleteChannelsAccountLevel) | `team_chat:delete:channels`, `team_chat:delete:channels:admin` |
| [List channel members](/docs/api/rest/reference/chat/methods/#operation/listChannelMembers) | `team_chat:read:list_members`, `team_chat:read:list_members:admin` |
| [Delete a channel](/docs/api/rest/reference/chat/methods/#operation/deleteChannel) | `team_chat:delete:user_channel`, `team_chat:delete:user_channel:admin` |
| [Update retention policy of a channel](/docs/api/rest/reference/chat/methods/#operation/updateChannelRetention) | `team_chat:update:retention:admin` |
| [Get retention policy of a channel](/docs/api/rest/reference/chat/methods/#operation/getChannelRetention) | `team_chat:read:retention:admin` |
| [List channel activity logs](/docs/api/rest/reference/chat/methods/#operation/listChannelActivityLogs) | `team_chat:read:list_channel_activity_logs:admin` |
| [List account's public channels](/docs/api/rest/reference/chat/methods/#operation/getAccountChannels) | `team_chat:read:list_channels:admin` |
| [Update a channel](/docs/api/rest/reference/chat/methods/#operation/updateChannel) | `team_chat:update:user_channel`, `team_chat:update:user_channel:admin` |
| [Batch remove members from a user's channel](/docs/api/rest/reference/chat/methods/#operation/batchRemoveUserChannelMembers) | `team_chat:delete:member:admin` |

### Chat Emoji

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Add a custom emoji](/docs/api/rest/reference/chat/methods/#operation/addACustomEmoji) | `team_chat:write:custom_emoji`, `team_chat:write:custom_emoji:admin` |
| [Delete a custom emoji](/docs/api/rest/reference/chat/methods/#operation/DeleteCustomEmoji) | `team_chat:delete:custom_emoji`, `team_chat:delete:custom_emoji:admin` |
| [List custom emojis](/docs/api/rest/reference/chat/methods/#operation/listCustomEmojis) | `team_chat:read:list_custom_emojis`, `team_chat:read:list_custom_emojis:admin` |

### Chat Files

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Send a chat file](/docs/api/rest/reference/chat/methods/#operation/sendChatFile) | `team_chat:write:message_files`, `team_chat:write:message_files:admin` |
| [Get file info](/docs/api/rest/reference/chat/methods/#operation/getFileInfo) | `team_chat:read:file`, `team_chat:read:file:admin` |
| [Upload a chat file](/docs/api/rest/reference/chat/methods/#operation/uploadAChatFile) | `team_chat:write:files`, `team_chat:write:files:admin` |
| [Delete a chat file](/docs/api/rest/reference/chat/methods/#operation/deleteChatFile) | `team_chat:delete:file`, `team_chat:delete:file:admin` |

### Chat Messages

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a message](/docs/api/rest/reference/chat/methods/#operation/getChatMessage) | `team_chat:read:user_message`, `team_chat:read:user_message:admin` |
| [Delete a scheduled message](/docs/api/rest/reference/chat/methods/#operation/deleteScheduleMessage) | `team_chat:delete:scheduled_message` |
| [List pinned history messages of channel](/docs/api/rest/reference/chat/methods/#operation/listChannelPinnedMessages) | `team_chat:read:list_pinned_messages` |
| [React to a chat message](/docs/api/rest/reference/chat/methods/#operation/reactMessage) | `team_chat:update:message_emoji`, `team_chat:update:message_emoji:admin` |
| [Delete a message](/docs/api/rest/reference/chat/methods/#operation/deleteChatMessage) | `team_chat:delete:user_message`, `team_chat:delete:user_message:admin` |
| [Perform operations on the message of channel](/docs/api/rest/reference/chat/methods/#operation/PerformMessageOfChannel) | `team_chat:update:pin_message` |
| [Update a message](/docs/api/rest/reference/chat/methods/#operation/editMessage) | `team_chat:update:user_message`, `team_chat:update:user_message:admin` |
| [List user's chat messages](/docs/api/rest/reference/chat/methods/#operation/getChatMessages) | `team_chat:read:list_user_messages`, `team_chat:read:list_user_messages:admin` |
| [Get a forwarded message](/docs/api/rest/reference/chat/methods/#operation/getForwardedMessage) | `team_chat:read:user_message`, `team_chat:read:user_message:admin` |
| [Add or remove a bookmark](/docs/api/rest/reference/chat/methods/#operation/addOrRemoveABookmark) | `team_chat:update:bookmark` |
| [List scheduled messages](/docs/api/rest/reference/chat/methods/#operation/listScheduledMessages) | `team_chat:read:list_scheduled_messages` |
| [Send a chat message](/docs/api/rest/reference/chat/methods/#operation/sendaChatMessage) | `team_chat:write:user_message`, `team_chat:write:user_message:admin` |
| [List bookmarks](/docs/api/rest/reference/chat/methods/#operation/fetchBookmarks) | `team_chat:read:list_bookmarks` |
| [Mark message read or unread](/docs/api/rest/reference/chat/methods/#operation/markMessage) | `team_chat:update:message_status`, `team_chat:update:message_status:admin` |
| [Retrieve a thread](/docs/api/rest/reference/chat/methods/#operation/retrieveThread) | `team_chat:read:thread_message`, `team_chat:read:thread_message:admin` |

### Chat Migration

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get migrated Zoom channel IDs](/docs/api/rest/reference/chat/methods/#operation/getMigrationChannelsMapping) | `team_chat:read:migrated_channels:admin` |
| [Migrate channel members](/docs/api/rest/reference/chat/methods/#operation/MigrateChannelMembers) | `team_chat:write:migrate_channel_members:admin` |
| [Get migrated Zoom user IDs](/docs/api/rest/reference/chat/methods/#operation/getMigrationUsersMapping) | `team_chat:read:migrated_users:admin` |
| [Migrate chat messages](/docs/api/rest/reference/chat/methods/#operation/MigrateChatMessages) | `team_chat:write:migrate_chat_messages:admin` |
| [Migrate a chat channel](/docs/api/rest/reference/chat/methods/#operation/MigrateAChatChannel) | `team_chat:write:migrate_a_chat_channel:admin` |
| [Migrate chat message reactions](/docs/api/rest/reference/chat/methods/#operation/MigrateChatMessageReactions) | `team_chat:write:migrate_chat_message_reactions:admin` |

### Chat Reminder

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List reminders](/docs/api/rest/reference/chat/methods/#operation/listReminders) | `team_chat:read:list_reminders` |
| [Create a reminder message](/docs/api/rest/reference/chat/methods/#operation/createReminderForMessage) | `team_chat:write:reminder` |
| [Delete a reminder for a message](/docs/api/rest/reference/chat/methods/#operation/deleteReminderForMessage) | `team_chat:delete:reminder` |

### Chat Sessions

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Star or unstar a channel or contact user](/docs/api/rest/reference/chat/methods/#operation/starUnstarChannelContact) | `team_chat:update:chat_control`, `team_chat:update:chat_control:admin` |
| [List a user's chat sessions](/docs/api/rest/reference/chat/methods/#operation/getChatSessions) | `team_chat:read:list_user_sessions`, `team_chat:read:list_user_sessions:admin` |

### Contacts

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get user's contact details](/docs/api/rest/reference/chat/methods/#operation/getUserContact) | `team_chat:read:contact` |
| [Search company contacts](/docs/api/rest/reference/chat/methods/#operation/searchCompanyContacts) | `contact:read:list_contacts`, `contact:read:list_contacts:admin` |
| [List user's contacts](/docs/api/rest/reference/chat/methods/#operation/getUserContacts) | `team_chat:read:list_contacts` |

### IM Groups

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update an IM directory group](/docs/api/rest/reference/chat/methods/#operation/imGroupUpdate) | `contact_group:update:group:admin` |
| [Update an IM directory group](/docs/api/rest/reference/chat/ma/#operation/imGroupUpdate) | `contact_group:update:group:master` |
| [Add IM directory group members](/docs/api/rest/reference/chat/methods/#operation/imGroupMembersCreate) | `contact_group:write:member:admin` |
| [Add IM directory group members](/docs/api/rest/reference/chat/ma/#operation/imGroupMembersCreate) | `contact_group:write:member:master` |
| [List IM directory groups](/docs/api/rest/reference/chat/methods/#operation/imGroups) | `contact_group:read:list_groups:admin` |
| [List IM directory groups](/docs/api/rest/reference/chat/ma/#operation/imGroups) | `contact_group:read:list_groups:master` |
| [Delete an IM directory group](/docs/api/rest/reference/chat/methods/#operation/imGroupDelete) | `contact_group:delete:group:admin` |
| [Delete an IM directory group](/docs/api/rest/reference/chat/ma/#operation/imGroupDelete) | `contact_group:delete:group:master` |
| [Retrieve an IM directory group](/docs/api/rest/reference/chat/methods/#operation/imGroup) | `contact_group:read:group:admin` |
| [Retrieve an IM directory group](/docs/api/rest/reference/chat/ma/#operation/imGroup) | `contact_group:read:group:master` |
| [Delete IM directory group member](/docs/api/rest/reference/chat/methods/#operation/imGroupMembersDelete) | `contact_group:delete:member:admin` |
| [Delete IM directory group member](/docs/api/rest/reference/chat/ma/#operation/imGroupMembersDelete) | `contact_group:delete:member:master` |
| [Create an IM directory group](/docs/api/rest/reference/chat/methods/#operation/imGroupCreate) | `contact_group:write:group:admin` |
| [Create an IM directory group](/docs/api/rest/reference/chat/ma/#operation/imGroupCreate) | `contact_group:write:group:master` |
| [List IM directory group members](/docs/api/rest/reference/chat/methods/#operation/imGroupMembers) | `contact_group:read:list_members:admin` |
| [List IM directory group members](/docs/api/rest/reference/chat/ma/#operation/imGroupMembers) | `contact_group:read:list_members:master` |

### Invitations

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Send new contact invitation](/docs/api/rest/reference/chat/methods/#operation/sendNewContactInvitation) | `team_chat:write:contact_information:admin`, `team_chat:write:contact_information` |

### Legal Hold

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Add a legal hold matter](/docs/api/rest/reference/chat/methods/#operation/addLegalHoldMatter) | `team_chat:write:legal_hold_matter:admin` |
| [Download legal hold files for given matter](/docs/api/rest/reference/chat/methods/#operation/downloadLegalHoldFiles) | `team_chat:read:legal_hold_matter_file:admin` |
| [List legal hold files by given matter](/docs/api/rest/reference/chat/methods/#operation/listLegalHoldFiles) | `team_chat:read:list_legal_hold_matter_files:admin` |
| [Update legal hold matter](/docs/api/rest/reference/chat/methods/#operation/updateLegalHoldMatter) | `team_chat:update:legal_hold_matter:admin` |
| [List legal hold matters](/docs/api/rest/reference/chat/methods/#operation/listLegalHoldMatters) | `team_chat:read:list_legal_hold_matters:admin` |
| [Delete legal hold matters](/docs/api/rest/reference/chat/methods/#operation/deleteLegalHoldMatters) | `team_chat:delete:legal_hold_matter:admin` |

### Reports

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get chat sessions reports](/docs/api/rest/reference/chat/methods/#operation/reportChatSessions) | `report:read:list_chat_sessions:admin` |
| [Get chat message reports](/docs/api/rest/reference/chat/methods/#operation/reportChatMessages) | `report:read:chat_session:admin` |

### Shared Spaces

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Remove members from a shared space](/docs/api/rest/reference/chat/methods/#operation/deleteSpaceMembers) | `team_chat:delete:shared_space_members`, `team_chat:delete:shared_space_members:admin` |
| [List shared spaces](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaces) | `team_chat:read:list_shared_spaces`, `team_chat:read:list_shared_spaces:admin` |
| [List shared space members](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaceMembers) | `team_chat:read:list_shared_space_members`, `team_chat:read:list_shared_space_members:admin` |
| [Delete a shared space](/docs/api/rest/reference/chat/methods/#operation/deleteSpace) | `team_chat:delete:shared_space`, `team_chat:delete:shared_space:admin` |
| [Get a shared space](/docs/api/rest/reference/chat/methods/#operation/getASharedSpace) | `team_chat:read:shared_space`, `team_chat:read:shared_space:admin` |
| [Update shared space settings](/docs/api/rest/reference/chat/methods/#operation/updateSharedSpaceSettings) | `team_chat:update:shared_space`, `team_chat:update:shared_space:admin` |
| [Promote shared space members to administrators](/docs/api/rest/reference/chat/methods/#operation/promoteSpaceMembers) | `team_chat:write:shared_space_administrators`, `team_chat:write:shared_space_administrators:admin` |
| [List shared space channels](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaceChannels) | `team_chat:read:list_shared_space_channels`, `team_chat:read:list_shared_space_channels:admin` |
| [Add members to a shared space](/docs/api/rest/reference/chat/methods/#operation/addSpaceMembers) | `team_chat:write:shared_space_members`, `team_chat:write:shared_space_members:admin` |
| [Demote shared space administrators to members](/docs/api/rest/reference/chat/methods/#operation/demoteSpaceAdmins) | `team_chat:delete:shared_space_administrators`, `team_chat:delete:shared_space_administrators:admin` |
| [Create a shared space](/docs/api/rest/reference/chat/methods/#operation/createSpace) | `team_chat:write:shared_space`, `team_chat:write:shared_space:admin` |
| [Move shared space channels](/docs/api/rest/reference/chat/methods/#operation/updateSharedSpaceChannels) | `team_chat:update:shared_space_channels` |
| [Transfer shared space ownership](/docs/api/rest/reference/chat/methods/#operation/transferSpaceOwner) | `team_chat:update:shared_space_owner`, `team_chat:update:shared_space_owner:admin` |

## Whiteboard


### Archiving

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List whiteboards sessions](/docs/api/rest/reference/Whiteboard/methods/#operation/Createwhiteboardsarchivefiles) | `whiteboard:read:list_sessions`, `whiteboard:read:list_sessions:admin` |
| [Download Whiteboards activity file](/docs/api/rest/reference/Whiteboard/methods/#operation/Downloadwhiteboardsactivityfile) | `whiteboard:read:archived_file`, `whiteboard:read:archived_file:admin` |
| [List whiteboard sessions activities](/docs/api/rest/reference/Whiteboard/methods/#operation/Listwhiteboardsessionsarchivedfiles) | `whiteboard:read:session`, `whiteboard:read:session:admin` |

### Collaborator

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Share a whiteboard to new users or team chat channels.](/docs/api/rest/reference/Whiteboard/methods/#operation/AddAWhiteboardCollaborator) | `whiteboard:write:collaborator:admin` |
| [Update whiteboard collaborators](/docs/api/rest/reference/Whiteboard/methods/#operation/UpdateAWhiteboardCollaborator) | `whiteboard:update:collaborator:admin` |
| [Get collaborators of a whiteboard](/docs/api/rest/reference/Whiteboard/methods/#operation/GetAWhiteboardCollaborator) | `whiteboard:read:list_collaborators:admin` |
| [Remove the collaborator from a whiteboard](/docs/api/rest/reference/Whiteboard/methods/#operation/DeleteAWhiteboardCollaborator) | `whiteboard:delete:collaborator:admin` |

### Document

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a whiteboard](/docs/api/rest/reference/Whiteboard/methods/#operation/GetAWhiteboard) | `whiteboard:read:whiteboard:admin`, `whiteboard:read:whiteboard` |
| [Update whiteboard basic information](/docs/api/rest/reference/Whiteboard/methods/#operation/UpdateAWhiteboardMetadata) | `whiteboard:update:whiteboard:admin` |
| [Create a new whiteboard](/docs/api/rest/reference/Whiteboard/methods/#operation/newWhiteboardCreate) | `whiteboard:write:whiteboard` |
| [Delete a whiteboard](/docs/api/rest/reference/Whiteboard/methods/#operation/DeleteAWhiteboard) | `whiteboard:delete:whiteboard:admin`, `whiteboard:delete:whiteboard` |
| [List all whiteboards](/docs/api/rest/reference/Whiteboard/methods/#operation/ListWhiteboards) | `whiteboard:read:list_whiteboards:admin`, `whiteboard:read:list_whiteboards` |

### Export

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Download whiteboard export](/docs/api/rest/reference/Whiteboard/methods/#operation/Downloadwhiteboardexport) | `whiteboard:read:export`, `whiteboard:read:export:admin` |
| [Get whiteboard export generation status](/docs/api/rest/reference/Whiteboard/methods/#operation/Getwhiteboardexportdatagenerationstatus) | `whiteboard:read:export`, `whiteboard:read:export:admin` |
| [Create whiteboard export](/docs/api/rest/reference/Whiteboard/methods/#operation/Createwhiteboardsexport) | `whiteboard:write:export`, `whiteboard:write:export:admin` |

### File

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Download Imported Whiteboard File](/docs/api/rest/reference/Whiteboard/methods/#operation/Downloadembeddedwhiteboardfile) | `whiteboard:read:file`, `whiteboard:read:file:admin` |
| [Upload file for whiteboard import](/docs/api/rest/reference/Whiteboard/methods/#operation/Uploadfileforwhiteboardimport) | `whiteboard:write:file`, `whiteboard:write:file:admin` |

### Import

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get whiteboard import status](/docs/api/rest/reference/Whiteboard/methods/#operation/GetWhiteboardimportstatus) | `whiteboard:read:import:admin`, `whiteboard:read:import` |
| [Create a new whiteboard by import](/docs/api/rest/reference/Whiteboard/methods/#operation/CreateWhiteboardImport) | `whiteboard:write:import`, `whiteboard:write:import:admin` |

### Project

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Share a project to new users](/docs/api/rest/reference/Whiteboard/methods/#operation/Shareaprojecttonewusers) | `whiteboard:write:project_collaborator`, `whiteboard:write:project_collaborator:admin` |
| [Move whiteboards to a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Movewhiteboardstoproject) | `whiteboard:write:project_whiteboard`, `whiteboard:write:project_whiteboard:admin` |
| [Create a new project](/docs/api/rest/reference/Whiteboard/methods/#operation/Createproject) | `whiteboard:write:project`, `whiteboard:write:project:admin` |
| [Remove whiteboards from a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Removewhiteboardsfromaproject) | `whiteboard:delete:project_whiteboard`, `whiteboard:delete:project_whiteboard:admin` |
| [Remove the collaborator from a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Removethecollaboratorfromaproject) | `whiteboard:delete:project_collaborator:admin`, `whiteboard:delete:project_collaborator` |
| [Delete a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Deleteproject) | `whiteboard:delete:project`, `whiteboard:delete:project:admin` |
| [Update project basic information](/docs/api/rest/reference/Whiteboard/methods/#operation/Updateproject) | `whiteboard:update:project:admin`, `whiteboard:update:project` |
| [List all projects](/docs/api/rest/reference/Whiteboard/methods/#operation/Listallprojects) | `whiteboard:read:list_projects:admin`, `whiteboard:read:list_projects` |
| [Get collaborators of a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Getcollaboratorsofaproject) | `whiteboard:read:project_collaborator`, `whiteboard:read:project_collaborator:admin` |
| [Update project collaborators](/docs/api/rest/reference/Whiteboard/methods/#operation/Updateprojectcollaborators) | `whiteboard:update:project_collaborator`, `whiteboard:update:project_collaborator:admin` |
| [Get a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Getaproject) | `whiteboard:read:project`, `whiteboard:read:project:admin` |

### Settings

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update whiteboard share setting](/docs/api/rest/reference/Whiteboard/methods/#operation/UpdateAWhiteboardShareSetting) | `whiteboard:update:share_setting:admin`, `whiteboard:update:share_setting` |

## Zoom Account


### Accounts

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Upload virtual background files](/docs/api/rest/reference/account/methods/#operation/uploadVB) | `account:write:virtual_background_files:master`, `account:write:virtual_background_files:admin` |
| [Upload virtual background files](/docs/api/rest/reference/account/ma/#operation/uploadVB) | `account:write:virtual_background_files:master` |
| [Update an account's webinar registration settings](/docs/api/rest/reference/account/methods/#operation/accountSettingsRegistrationUpdate) | `account:update:registration_settings:master` |
| [Update an account's webinar registration settings](/docs/api/rest/reference/account/ma/#operation/accountSettingsRegistrationUpdate) | `account:update:registration_settings:master` |
| [Get sub account details](/docs/api/rest/reference/account/ma/#operation/GetSubAccountDetails) | `account:read:sub_account:master`, `account:read:sub_account:admin` |
| [Delete virtual background files](/docs/api/rest/reference/account/methods/#operation/delVB) | `account:delete:virtual_background_files:master`, `account:delete:virtual_background_files:admin` |
| [Delete virtual background files](/docs/api/rest/reference/account/ma/#operation/delVB) | `account:delete:virtual_background_files:master` |
| [List sub accounts](/docs/api/rest/reference/account/ma/#operation/accounts) | `account:read:list_sub_accounts:master` |
| [Get account settings](/docs/api/rest/reference/account/methods/#operation/accountSettings) | `account:read:settings:admin`, `account:read:settings:master` |
| [Get account settings](/docs/api/rest/reference/account/ma/#operation/accountSettings) | `account:read:settings:master` |
| [Update account settings](/docs/api/rest/reference/account/methods/#operation/accountSettingsUpdate) | `account:update:settings:admin`, `account:update:settings:master` |
| [Update account settings](/docs/api/rest/reference/account/ma/#operation/accountSettingsUpdate) | `account:update:settings:master` |
| [Get an account's webinar registration settings](/docs/api/rest/reference/account/methods/#operation/accountSettingsRegistration) | `account:read:registration_settings:master` |
| [Get an account's webinar registration settings](/docs/api/rest/reference/account/ma/#operation/accountSettingsRegistration) | `account:read:registration_settings:master` |
| [Create a sub account](/docs/api/rest/reference/account/ma/#operation/accountCreate) | `account:write:sub_account:master` |
| [Update the account owner](/docs/api/rest/reference/account/methods/#operation/UpdateTheAccountOwner) | `account:update:owner:master`, `account:update:owner:admin` |
| [Update the account owner](/docs/api/rest/reference/account/ma/#operation/UpdateTheAccountOwner) | `account:update:owner:master` |
| [Update options](/docs/api/rest/reference/account/ma/#operation/UpdateOptions) | `account:update:options:master` |
| [Get account's managed domains](/docs/api/rest/reference/account/methods/#operation/accountManagedDomain) | `account:read:managed_domains:master` |
| [Get account's managed domains](/docs/api/rest/reference/account/ma/#operation/accountManagedDomain) | `account:read:managed_domains:master` |
| [Get account's trusted domains](/docs/api/rest/reference/account/methods/#operation/accountTrustedDomain) | `account:read:trusted_domains:master` |
| [Get account's trusted domains](/docs/api/rest/reference/account/ma/#operation/accountTrustedDomain) | `account:read:trusted_domains:master` |
| [Disassociate a sub account](/docs/api/rest/reference/account/ma/#operation/DisassociateASubAccount) | `account:delete:sub_account:master` |
| [Update locked settings](/docs/api/rest/reference/account/methods/#operation/UpdateLockedSettings) | `account:update:lock_settings:master`, `account:update:lock_settings:admin` |
| [Update locked settings](/docs/api/rest/reference/account/ma/#operation/UpdateLockedSettings) | `account:update:lock_settings:master` |
| [Get locked settings](/docs/api/rest/reference/account/methods/#operation/getAccountLockSettings) | `account:read:lock_settings:master` |
| [Get locked settings](/docs/api/rest/reference/account/ma/#operation/getAccountLockSettings) | `account:read:lock_settings:master` |

### Dashboards

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get top 25 issues of Zoom Rooms](/docs/api/rest/reference/account/methods/#operation/dashboardZoomRoomIssue) | `dashboard:read:issues_zoomroom:admin` |
| [Get top 25 issues of Zoom Rooms](/docs/api/rest/reference/account/ma/#operation/dashboardZoomRoomIssue) | `dashboard:read:issues_zoomroom:master` |
| [List client meeting satisfaction](/docs/api/rest/reference/account/methods/#operation/listMeetingSatisfaction) | `dashboard:read:meeting_survey:admin` |
| [List client meeting satisfaction](/docs/api/rest/reference/account/ma/#operation/listMeetingSatisfaction) | `dashboard:read:meeting_survey:master` |
| [Get webinar participant QoS](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarParticipantQOS) | `dashboard:read:webinar_participant_qos:admin` |
| [Get webinar participant QoS](/docs/api/rest/reference/account/ma/#operation/dashboardWebinarParticipantQOS) | `dashboard:read:webinar_participant_qos:master` |
| [Get issues of Zoom Rooms](/docs/api/rest/reference/account/methods/#operation/dashboardIssueDetailZoomRoom) | `dashboard:read:issues_zoomroom:admin` |
| [Get issues of Zoom Rooms](/docs/api/rest/reference/account/ma/#operation/dashboardIssueDetailZoomRoom) | `dashboard:read:issues_zoomroom:master` |
| [Get zoom meetings client feedback](/docs/api/rest/reference/account/methods/#operation/dashboardClientFeedbackDetail) | `dashboard:read:meeting_feedback:admin` |
| [Get zoom meetings client feedback](/docs/api/rest/reference/account/ma/#operation/dashboardClientFeedbackDetail) | `dashboard:read:meeting_feedback:master` |
| [Get post webinar feedback](/docs/api/rest/reference/account/methods/#operation/participantWebinarFeedback) | `dashboard:read:post_webinar_feedback:admin` |
| [Get post webinar feedback](/docs/api/rest/reference/account/ma/#operation/participantWebinarFeedback) | `dashboard:read:post_webinar_feedback:master` |
| [Get post meeting feedback](/docs/api/rest/reference/account/methods/#operation/participantFeedback) | `dashboard:read:post_meeting_feedback:admin` |
| [Get post meeting feedback](/docs/api/rest/reference/account/ma/#operation/participantFeedback) | `dashboard:read:post_meeting_feedback:master` |
| [List meetings](/docs/api/rest/reference/account/methods/#operation/dashboardMeetings) | `dashboard:read:list_meetings:admin` |
| [List meetings](/docs/api/rest/reference/account/ma/#operation/dashboardMeetings) | `dashboard:read:list_meetings:master` |
| [Get Zoom Rooms details](/docs/api/rest/reference/account/methods/#operation/dashboardZoomRoom) | `dashboard:read:zoomroom:admin` |
| [Get Zoom Rooms details](/docs/api/rest/reference/account/ma/#operation/dashboardZoomRoom) | `dashboard:read:zoomroom:master` |
| [Get webinar participants](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarParticipants) | `dashboard:read:list_webinar_participants:admin` |
| [Get webinar participants](/docs/api/rest/reference/account/ma/#operation/dashboardWebinarParticipants) | `dashboard:read:list_webinar_participants:master` |
| [Get top 25 Zoom Rooms with issues](/docs/api/rest/reference/account/methods/#operation/dashboardIssueZoomRoom) | `dashboard:read:list_zoomrooms:admin` |
| [Get top 25 Zoom Rooms with issues](/docs/api/rest/reference/account/ma/#operation/dashboardIssueZoomRoom) | `dashboard:read:list_zoomrooms:master` |
| [List Zoom Rooms](/docs/api/rest/reference/account/methods/#operation/dashboardZoomRooms) | `dashboard:read:list_zoomrooms:admin` |
| [List Zoom Rooms](/docs/api/rest/reference/account/ma/#operation/dashboardZoomRooms) | `dashboard:read:list_zoomrooms:master` |
| [Get webinar details](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarDetail) | `dashboard:read:webinar:admin` |
| [Get webinar details](/docs/api/rest/reference/account/ma/#operation/dashboardWebinarDetail) | `dashboard:read:webinar:master` |
| [List webinars](/docs/api/rest/reference/account/methods/#operation/dashboardWebinars) | `dashboard:read:list_webinars:admin` |
| [List webinars](/docs/api/rest/reference/account/ma/#operation/dashboardWebinars) | `dashboard:read:list_webinars:master` |
| [List Zoom meetings client feedback](/docs/api/rest/reference/account/methods/#operation/dashboardClientFeedback) | `dashboard:read:list_meetings_feedback:admin` |
| [List Zoom meetings client feedback](/docs/api/rest/reference/account/ma/#operation/dashboardClientFeedback) | `dashboard:read:list_meetings_feedback:master` |
| [Get meeting quality scores](/docs/api/rest/reference/account/methods/#operation/dashboardQuality) | `dashboard:read:meeting_quality_score:admin` |
| [Get meeting quality scores](/docs/api/rest/reference/account/ma/#operation/dashboardQuality) | `dashboard:read:meeting_quality_score:master` |
| [List webinar participant QoS](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarParticipantsQOS) | `dashboard:read:list_webinar_participants_qos:admin` |
| [List webinar participant QoS](/docs/api/rest/reference/account/ma/#operation/dashboardWebinarParticipantsQOS) | `dashboard:read:list_webinar_participants_qos:master` |
| [List meeting participants QoS](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingParticipantsQOS) | `dashboard:read:list_meeting_participants_qos:admin` |
| [List meeting participants QoS](/docs/api/rest/reference/account/ma/#operation/dashboardMeetingParticipantsQOS) | `dashboard:read:list_meeting_participants_qos:master` |
| [Get CRC port usage](/docs/api/rest/reference/account/methods/#operation/dashboardCRC) | `dashboard:read:crc_port_usage:admin` |
| [Get CRC port usage](/docs/api/rest/reference/account/ma/#operation/dashboardCRC) | `dashboard:read:crc_port_usage:master` |
| [List the client versions](/docs/api/rest/reference/account/methods/#operation/getClientVersions) | `dashboard:read:client_versions:admin` |
| [List the client versions](/docs/api/rest/reference/account/ma/#operation/getClientVersions) | `dashboard:read:client_versions:master` |
| [Get webinar sharing/recording details](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarParticipantShare) | `dashboard:read:webinar_sharing:admin` |
| [Get webinar sharing/recording details](/docs/api/rest/reference/account/ma/#operation/dashboardWebinarParticipantShare) | `dashboard:read:webinar_sharing:master` |
| [List meeting participants](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingParticipants) | `dashboard:read:list_meeting_participants:admin` |
| [List meeting participants](/docs/api/rest/reference/account/ma/#operation/dashboardMeetingParticipants) | `dashboard:read:list_meeting_participants:master` |
| [Get chat metrics](/docs/api/rest/reference/account/methods/#operation/dashboardChat) | `dashboard:read:chat:admin` |
| [Get chat metrics](/docs/api/rest/reference/account/ma/#operation/dashboardChat) | `dashboard:read:chat:master` |
| [Get meeting sharing/recording details](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingParticipantShare) | `dashboard:read:meeting_sharing:admin` |
| [Get meeting sharing/recording details](/docs/api/rest/reference/account/ma/#operation/dashboardMeetingParticipantShare) | `dashboard:read:meeting_sharing:master` |
| [Get meeting participant QoS](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingParticipantQOS) | `dashboard:read:meeting_participant_qos:admin` |
| [Get meeting participant QoS](/docs/api/rest/reference/account/ma/#operation/dashboardMeetingParticipantQOS) | `dashboard:read:meeting_participant_qos:master` |
| [Get meeting details](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingDetail) | `dashboard:read:meeting:admin` |
| [Get meeting details](/docs/api/rest/reference/account/ma/#operation/dashboardMeetingDetail) | `dashboard:read:meeting:master` |

### Data Requests

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get download link for data access request file](/docs/api/rest/reference/account/methods/#operation/DownloadfilesfromDataRequest) | `data_request:read:download:admin` |
| [Cancel data deletion request](/docs/api/rest/reference/account/methods/#operation/CancelDataRequest) | `data_request:delete:request:admin` |
| [List downloadable files for export data request](/docs/api/rest/reference/account/methods/#operation/GetDownloadableFilesforDataRequest) | `data_request:read:download:admin` |
| [List data request history](/docs/api/rest/reference/account/methods/#operation/GetDataRequestsHistory) | `data_request:read:history:admin` |
| [Create data (export/deletion) request](/docs/api/rest/reference/account/methods/#operation/CreateDataAccessRequest) | `data_request:write:request:admin` |

### Information Barriers

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Remove an Information Barrier policy](/docs/api/rest/reference/account/methods/#operation/InformationBarriersDelete) | `information_barrier:delete:policy:admin` |
| [Remove an Information Barrier policy](/docs/api/rest/reference/account/ma/#operation/InformationBarriersDelete) | `information_barrier:delete:policy:master` |
| [Update an Information Barriers policy](/docs/api/rest/reference/account/methods/#operation/InformationBarriersUpdate) | `information_barrier:update:policy:admin` |
| [Update an Information Barriers policy](/docs/api/rest/reference/account/ma/#operation/InformationBarriersUpdate) | `information_barrier:update:policy:master` |
| [Get an Information Barrier policy by ID](/docs/api/rest/reference/account/methods/#operation/InformationBarriersGet) | `information_barrier:read:policy:admin` |
| [Get an Information Barrier policy by ID](/docs/api/rest/reference/account/ma/#operation/InformationBarriersGet) | `information_barrier:read:policy:master` |
| [List information Barrier policies](/docs/api/rest/reference/account/methods/#operation/InformationBarriersList) | `information_barrier:read:list_policies:admin` |
| [List information Barrier policies](/docs/api/rest/reference/account/ma/#operation/InformationBarriersList) | `information_barrier:read:list_policies:master` |
| [Create an Information Barrier policy](/docs/api/rest/reference/account/methods/#operation/InformationBarriersCreate) | `information_barrier:write:policy:admin` |
| [Create an Information Barrier policy](/docs/api/rest/reference/account/ma/#operation/InformationBarriersCreate) | `information_barrier:write:policy:master` |

### Roles

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Unassign a role](/docs/api/rest/reference/account/methods/#operation/roleMemberDelete) | `role:delete:member`, `role:delete:member:admin` |
| [Unassign a role](/docs/api/rest/reference/account/ma/#operation/roleMemberDelete) | `role:delete:member:master` |
| [List roles](/docs/api/rest/reference/account/methods/#operation/roles) | `role:read:list_roles`, `role:read:list_roles:admin` |
| [List roles](/docs/api/rest/reference/account/ma/#operation/roles) | `role:read:list_roles:master` |
| [Update role information](/docs/api/rest/reference/account/methods/#operation/updateRole) | `role:update:role`, `role:update:role:admin` |
| [Update role information](/docs/api/rest/reference/account/ma/#operation/updateRole) | `role:update:role:master` |
| [Delete a role](/docs/api/rest/reference/account/methods/#operation/deleteRole) | `role:delete:role`, `role:delete:role:admin` |
| [Delete a role](/docs/api/rest/reference/account/ma/#operation/deleteRole) | `role:delete:role:master` |
| [Get role information](/docs/api/rest/reference/account/methods/#operation/getRoleInformation) | `role:read:role`, `role:read:role:admin` |
| [Get role information](/docs/api/rest/reference/account/ma/#operation/getRoleInformation) | `role:read:role:master` |
| [List members in a role](/docs/api/rest/reference/account/methods/#operation/roleMembers) | `role:read:list_members`, `role:read:list_members:admin` |
| [List members in a role](/docs/api/rest/reference/account/ma/#operation/roleMembers) | `role:read:list_members:master` |
| [Create a role](/docs/api/rest/reference/account/methods/#operation/createRole) | `role:write:role`, `role:write:role:admin` |
| [Create a role](/docs/api/rest/reference/account/ma/#operation/createRole) | `role:write:role:master` |
| [Assign a role](/docs/api/rest/reference/account/methods/#operation/AddRoleMembers) | `role:write:member`, `role:write:member:admin` |
| [Assign a role](/docs/api/rest/reference/account/ma/#operation/AddRoleMembers) | `role:write:member:master` |

### Survey Management

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get survey info](/docs/api/rest/reference/account/methods/#operation/getSurveyInfo) | `survey_management:read:survey:admin` |
| [Get survey info](/docs/api/rest/reference/account/ma/#operation/getSurveyInfo) | `survey_management:read:survey:master` |
| [Get survey instances](/docs/api/rest/reference/account/methods/#operation/getSurveyInstancesInfo) | `survey_management:read:list_survey_instances:admin` |
| [Get survey instances](/docs/api/rest/reference/account/ma/#operation/getSurveyInstancesInfo) | `survey_management:read:list_survey_instances:master` |
| [Get survey answers](/docs/api/rest/reference/account/methods/#operation/getSurveyAnswers) | `survey_management:read:list_survey_answers:admin` |
| [Get survey answers](/docs/api/rest/reference/account/ma/#operation/getSurveyAnswers) | `survey_management:read:list_survey_answers:master` |
| [Get surveys](/docs/api/rest/reference/account/methods/#operation/getAccountSurveys) | `survey_management:read:list_surveys:admin` |
| [Get surveys](/docs/api/rest/reference/account/ma/#operation/getAccountSurveys) | `survey_management:read:list_surveys:master` |

## Zoom Auto Dialer


### Prospect Management

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Next OAuth error messages](/docs/integrations/oauth-error-messages/) | `zoom_auto_dialer:update:prospects:admin` |

## Zoom Billing


### Billing

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Cancel a base plan](/docs/api/rest/reference/billing/ma/#operation/CancelABasePlan) | `billing:update:cancel_plan:master` |
| [Download subaccounts' billing invoice reports](/docs/api/rest/reference/billing/ma/#operation/downloadBillingInvoiceReport) | `billing:read:download_invoice_reports:master` |
| [Download an invoice file](/docs/api/rest/reference/billing/ma/#operation/downloadInvoicePDF) | `billing:read:download_invoice_file:master` |
| [Get account plan information](/docs/api/rest/reference/billing/ma/#operation/GetAccountPlanInformation) | `billing:read:plan_information:master`, `billing:read:plan_information:admin` |
| [Update billing information](/docs/api/rest/reference/billing/ma/#operation/UpdateBillingInformation) | `billing:update:billing_information:master` |
| [List upcoming renewal accounts](/docs/api/rest/reference/billing/ma/#operation/Getupcomingrenewalaccounts) | `billing:read:list_upcoming_renewal_accounts:master` |
| [Update a base plan](/docs/api/rest/reference/billing/ma/#operation/UpdateABasePlan) | `billing:update:plan:master` |
| [Get invoice details](/docs/api/rest/reference/billing/ma/#operation/GetInvoiceDetails) | `billing:read:invoice_details:master`, `billing:read:invoice_details:admin` |
| [Update an account's additional plan](/docs/api/rest/reference/billing/ma/#operation/UpdateAnAccount'sAdditionalPlan) | `billing:update:additional_plans:master` |
| [Get billing information](/docs/api/rest/reference/billing/ma/#operation/GetBillingInformation) | `billing:read:billing_information:master`, `billing:read:billing_information:admin` |
| [List billing invoices](/docs/api/rest/reference/billing/ma/#operation/ListBillingInvoices) | `billing:read:list_invoices:master`, `billing:read:list_invoices:admin` |
| [Get plan usage](/docs/api/rest/reference/billing/ma/#operation/GetPlanUsage) | `billing:read:plan_usage:master`, `billing:read:plan_usage:admin` |
| [Subscribe subaccount to an additional plan](/docs/api/rest/reference/billing/ma/#operation/SubscribeAccountToAnAdditionalPlan) | `billing:write:subscribe_additional_plans:master` |
| [Cancel additional plans](/docs/api/rest/reference/billing/ma/#operation/CancelAdditionalPlans) | `billing:update:cancel_additional_plans:master` |
| [Download an invoice file (v2)](/docs/api/rest/reference/billing/ma/#operation/downloadInvoicePDFFile) | `billing:read:download_invoice_file:master` |
| [Delete subaccounts' billing invoice report](/docs/api/rest/reference/billing/ma/#operation/deleteBillingInvoiceReport) | `billing:delete:invoice_report:master` |
| [Subscribe an account to a plan](/docs/api/rest/reference/billing/ma/#operation/SubscribeAccountToAPlan) | `billing:write:subscribe_plan:master` |

## Zoom Calendar


### acl

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create a new ACL rule](/docs/api/rest/reference/zoom-calendar/methods/#operation/Insertacl) | `calendar:write:acl`, `calendar:write:acl:admin` |
| [Delete an existing ACL rule](/docs/api/rest/reference/zoom-calendar/methods/#operation/Deleteacl) | `calendar:delete:acl`, `calendar:delete:acl:admin` |
| [Update the specified ACL rule](/docs/api/rest/reference/zoom-calendar/methods/#operation/Patchacl) | `calendar:update:acl`, `calendar:update:acl:admin` |
| [List ACL rules of specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Listacl) | `calendar:read:list_acl`, `calendar:read:list_acl:admin` |
| [Get the specified ACL rule](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getacl) | `calendar:read:acl`, `calendar:read:acl:admin` |

### calendar list

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Insert an existing calendar to the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/InsertcalendarList) | `calendar:write:calendar_list` |
| [Delete an existing calendar from the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/DeletecalendarList) | `calendar:delete:calendar_list` |
| [List the calendars in the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/ListcalendarList) | `calendar:read:list_calendar_lists` |
| [Update an existing calendar in the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/PatchcalendarList) | `calendar:update:calendar_list` |
| [Get a specified calendar from the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/GetcalendarList) | `calendar:read:calendar_list` |

### calendars

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getcalendar) | `calendar:read:calendar`, `calendar:read:calendar:admin` |
| [Delete a calendar owned by a user](/docs/api/rest/reference/zoom-calendar/methods/#operation/Deletecalendar) | `calendar:delete:calendar`, `calendar:delete:calendar:admin` |
| [Create a new secondary calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Insertcalendar) | `calendar:write:calendar`, `calendar:write:calendar:admin` |
| [Update the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Patchcalendar) | `calendar:update:calendar`, `calendar:update:calendar:admin` |

### colors

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get the color definitions for calendars and events](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getcolor) | `calendar:read:color`, `calendar:read:color:admin` |

### events

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Quick add an event to the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Quickaddevent) | `calendar:write:quick_add_event`, `calendar:write:quick_add_event:admin` |
| [Move the specified event from a calendar to another specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Moveevent) | `calendar:write:move_event`, `calendar:write:move_event:admin` |
| [Get the specified event on the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getevent) | `calendar:read:event`, `calendar:read:event:admin` |
| [Update the specified event on the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Patchevent) | `calendar:update:event`, `calendar:update:event:admin` |
| [Import event to the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Importevent) | `calendar:write:import_event`, `calendar:write:import_event:admin` |
| [List events on the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Listevent) | `calendar:read:list_events`, `calendar:read:list_events:admin` |
| [Insert a new event to the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Insertevent) | `calendar:write:event`, `calendar:write:event:admin` |
| [List all instances of the specified recurring event](/docs/api/rest/reference/zoom-calendar/methods/#operation/Instanceevent) | `calendar:read:instance_event`, `calendar:read:instance_event:admin` |
| [Delete an existing event from the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Deleteevent) | `calendar:delete:event`, `calendar:delete:event:admin` |

### freebusy

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Query freebusy information for a set of calendars](/docs/api/rest/reference/zoom-calendar/methods/#operation/Queryfreebusy) | `calendar:read:list_events`, `calendar:read:list_events:admin` |

### settings

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get the specified user calendar settings of the authenticated user](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getsetting) | `calendar:read:setting` |
| [List all user calendar settings of the authenticated user](/docs/api/rest/reference/zoom-calendar/methods/#operation/Listsettings) | `calendar:read:list_settings` |
| [Patch the specified user calendar settings of the authenticated user](/docs/api/rest/reference/zoom-calendar/methods/#operation/Patchsetting) | `calendar:update:setting`, `calendar:update:setting:admin` |

## Zoom Clips


### Clips

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List all clips](/docs/api/rest/reference/clips/methods/#operation/GetUserClips) | `clips:read:list_user_clips`, `clips:read:list_user_clips:admin` |
| [List all clips](/docs/api/rest/reference/clips/ma/#operation/GetUserClips) | `clips:read:list_user_clips:master` |

### Collaborator

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Remove the collaborator from a clip](/docs/api/rest/reference/clips/methods/#operation/DeleteCollaborator) | `clips:delete:collaborators`, `clips:delete:collaborators:admin` |
| [Get collaborators of a clip](/docs/api/rest/reference/clips/methods/#operation/GetClipCollaborators) | `clips:read:list_collaborator`, `clips:read:list_collaborator:admin` |

### Comment

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List clip comments](/docs/api/rest/reference/clips/methods/#operation/Listclipcomments) | `clips:read:list_comments`, `clips:read:list_comments:admin` |
| [Delete a comment](/docs/api/rest/reference/clips/methods/#operation/Deleteacomment) | `clips:delete:comment`, `clips:delete:comment:admin` |

### Download

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Download a clip](/docs/api/rest/reference/clips/methods/#operation/downloadClip) | `clips:read:download_clip`, `clips:read:download_clip:admin` |

### Single

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete a clip(soft delete)](/docs/api/rest/reference/clips/methods/#operation/DeleteClip) | `clips:delete:clip`, `clips:delete:clip:admin` |
| [Get a clip](/docs/api/rest/reference/clips/methods/#operation/GetClipById) | `clips:read:clip`, `clips:read:clip:admin` |

### Transfer

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Transfer task status check](/docs/api/rest/reference/clips/methods/#operation/Transfertaskstatuscheck) | `clips:read:transfer_task_status:admin` |
| [Transfer clips owner](/docs/api/rest/reference/clips/methods/#operation/Transferclipsowner) | `clips:write:transfer_owner:admin` |

## Zoom Commerce


### Account Management

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get the list of all accounts associated with a Zoom Partner/Sub-Reseller, by the account type](/docs/api/rest/reference/commerce/methods/#operation/getAllAccounts) | `zoom_commerce:read:account:admin` |
| [Get the account details for a Zoom Partner/Subreseller/End Customer](/docs/api/rest/reference/commerce/methods/#operation/getAccountDetails) | `zoom_commerce:read:account:admin` |
| [Create an end customer account](/docs/api/rest/reference/commerce/methods/#operation/createAccount) | `zoom_commerce:write:sub_account:admin` |
| [Add contacts to an existing end customer or your own account.](/docs/api/rest/reference/commerce/methods/#operation/addAccountContact) | `zoom_commerce:update:account:admin` |

### Billing

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Gets the PDF document for the billing document ID](/docs/api/rest/reference/commerce/methods/#operation/downloadBillingDoc) | `zoom_commerce:read:billing_documents:admin` |
| [Gets all billing documents for a distributor or a reseller](/docs/api/rest/reference/commerce/methods/#operation/getAllBillingDocs) | `zoom_commerce:read:billing_documents:admin` |
| [Get detailed information about a specific invoice for a distributor or a reseller](/docs/api/rest/reference/commerce/methods/#operation/getInvoiceDetail) | `zoom_commerce:read:billing_documents:admin` |

### Deal Registration

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Gets details of a deal registration by the deal registration](/docs/api/rest/reference/commerce/methods/#operation/getDealRegDetails) | `zoom_commerce:read:deal_registration:admin` |
| [Retrieves all valid Zoom Campaigns which a deal registration can be associated with.](/docs/api/rest/reference/commerce/methods/#operation/getCampaigns) | `zoom_commerce:read:deal_registration:admin` |
| [Creates a new deal registration for a partner](/docs/api/rest/reference/commerce/methods/#operation/createDealReg) | `zoom_commerce:write:deal_registration:admin` |
| [Updates an existing deal registration](/docs/api/rest/reference/commerce/methods/#operation/Updatesanexistingdealregistration) | `zoom_commerce:write:deal_registration:admin` |
| [Gets all valid Deal Registrations for a partner](/docs/api/rest/reference/commerce/methods/#operation/getAllDealRegs) | `zoom_commerce:read:deal_registration:admin` |

### Order

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Preview delta order metrics and subscriptions in an order](/docs/api/rest/reference/commerce/methods/#operation/createOrderPreview) | `zoom_commerce:write:order:admin` |
| [Get order details by order reference ID](/docs/api/rest/reference/commerce/methods/#operation/getOrderDetails) | `zoom_commerce:read:order:admin` |
| [Create a subscription order for a Zoom partner](/docs/api/rest/reference/commerce/methods/#operation/createOrder) | `zoom_commerce:write:order:admin` |
| [Gets all orders for a Zoom partner.](/docs/api/rest/reference/commerce/methods/#operation/getAllOrders) | `zoom_commerce:read:order:admin` |

### Platform

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Gets details of all files associated with a quote or deal registration](/docs/api/rest/reference/commerce/methods/#operation/allFileDetails) | `zoom_commerce:read:file:admin` |
| [Download a file associated with a quote or deal registration.](/docs/api/rest/reference/commerce/methods/#operation/downloadFile.) | `zoom_commerce:read:file:admin` |
| [Upload an attachment pdf file in context of a deal registration or quote](/docs/api/rest/reference/commerce/methods/#operation/uploadFile) | `zoom_commerce:write:file:admin` |

### Product Catalog

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Gets the details for a Zoom product or offer.](/docs/api/rest/reference/commerce/methods/#operation/getOfferDetail) | `zoom_commerce:read:product_catalog:admin` |
| [Gets the pricebook in a downloadable file](/docs/api/rest/reference/commerce/methods/#operation/downloadPricebook) | `zoom_commerce:read:product_catalog:admin` |
| [Gets Zoom Product Catalog for a Zoom Partner](/docs/api/rest/reference/commerce/methods/#operation/getOffers) | `zoom_commerce:read:product_catalog:admin` |

### Quote

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Gets all quotes for a Zoom partner](/docs/api/rest/reference/commerce/methods/#operation/getAllQuotes) | `zoom_commerce:read:quote:admin` |
| [Preview delta quote metrics and subscriptions in a quote](/docs/api/rest/reference/commerce/methods/#operation/createQuotePreview) | `zoom_commerce:write:quote:admin` |
| [Submits a subscription quote for provisioning](/docs/api/rest/reference/commerce/methods/#operation/provisionQuote) | `zoom_commerce:write:quote:admin` |
| [Update a subscription quote for a Zoom partner](/docs/api/rest/reference/commerce/methods/#operation/updateQuote) | `zoom_commerce:write:quote:admin` |
| [Create a subscription quote for a Zoom Partner](/docs/api/rest/reference/commerce/methods/#operation/createQuote) | `zoom_commerce:write:quote:admin` |
| [Get quote details by quote reference ID](/docs/api/rest/reference/commerce/methods/#operation/getQuoteDetails) | `zoom_commerce:read:quote:admin` |

### Subscription

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Gets subscription details for a given subscription number](/docs/api/rest/reference/commerce/methods/#operation/getSubscriptionDetails) | `zoom_commerce:read:subscription:admin` |
| [Get trial details for an end customer by their Zoom account number or the trial ID](/docs/api/rest/reference/commerce/methods/#operation/getTrialDetails) | `zoom_commerce:read:subscription:admin` |
| [Gets paid subscriptions for a Zoom partner.](/docs/api/rest/reference/commerce/methods/#operation/getAllSubscriptions) | `zoom_commerce:read:subscription:admin` |
| [Get trial subscriptions for a Zoom partner](/docs/api/rest/reference/commerce/methods/#operation/getAllTrialSubscriptions) | `zoom_commerce:read:subscription:admin` |
| [Gets subscription changes/versions for a given subscription number.](/docs/api/rest/reference/commerce/methods/#operation/getSubscriptionVersions) | `zoom_commerce:read:subscription:admin` |

## Zoom Events


### Attendee Actions

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update event attendee actions](/docs/api/rest/reference/event/methods/#operation/UpdateEventAttendeeActions) | `zoom_events:update:batch_attendee_actions`, `zoom_events:update:batch_attendee_actions:admin` |
| [List event attendee actions](/docs/api/rest/reference/event/methods/#operation/ListEventAttendeeActions) | `zoom_events:read:list_attendee_actions`, `zoom_events:read:list_attendee_actions:admin` |
| [List session attendee actions](/docs/api/rest/reference/event/methods/#operation/ListSessionAttendeeActions) | `zoom_events:read:list_session_attendee_actions`, `zoom_events:read:list_session_attendee_actions:admin` |
| [Update session attendee actions](/docs/api/rest/reference/event/methods/#operation/UpdateSessionAttendeeActions) | `zoom_events:update:batch_session_attendee_actions`, `zoom_events:update:batch_session_attendee_actions:admin` |

### Co Editors

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Add or remove event co-editors](/docs/api/rest/reference/event/methods/#operation/coeditoractions) | `zoom_events:write:coeditor`, `zoom_events:write:coeditor:admin` |
| [List coeditors](/docs/api/rest/reference/event/methods/#operation/getCoEditors) | `zoom_events:read:list_coeditors`, `zoom_events:read:list_coeditors:admin` |

### Emails

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List event emails sent status](/docs/api/rest/reference/event/methods/#operation/listEmailSentStatuses) | `zoom_events:read:list_emails_status`, `zoom_events:read:list_emails_status:admin` |
| [List event email types](/docs/api/rest/reference/event/methods/#operation/listEmailTypes) | `zoom_events:read:list_email_types`, `zoom_events:read:list_email_types:admin` |

### Event Access

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List event access links](/docs/api/rest/reference/event/methods/#operation/getEventAccessLinks) | `zoom_events:read:list_access_links`, `zoom_events:read:list_access_links:admin` |
| [Get event access link](/docs/api/rest/reference/event/methods/#operation/GetEventAccessLink) | `zoom_events:read:access_links`, `zoom_events:read:access_links:admin` |
| [Update event access](/docs/api/rest/reference/event/methods/#operation/updateEventAccess) | `zoom_events:update:access_links`, `zoom_events:update:access_links:admin` |
| [Delete event access link](/docs/api/rest/reference/event/methods/#operation/deleteEventAccessLink) | `zoom_events:delete:access_links`, `zoom_events:delete:access_links:admin` |
| [Create event access link](/docs/api/rest/reference/event/methods/#operation/createEventAccessLink) | `zoom_events:write:access_links`, `zoom_events:write:access_links:admin` |

### Events

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List events](/docs/api/rest/reference/event/methods/#operation/getEvents) | `zoom_events:read:list_events`, `zoom_events:read:list_events:admin` |
| [Get an event](/docs/api/rest/reference/event/methods/#operation/getEventInfo) | `zoom_events:read:event`, `zoom_events:read:event:admin` |
| [Delete an event](/docs/api/rest/reference/event/methods/#operation/deleteEvent) | `zoom_events:delete:event`, `zoom_events:delete:event:admin` |
| [Event actions](/docs/api/rest/reference/event/methods/#operation/EventActions) | `zoom_events:write:event`, `zoom_events:write:event:admin` |
| [Update an event](/docs/api/rest/reference/event/methods/#operation/updateEvent) | `zoom_events:update:event`, `zoom_events:update:event:admin` |
| [Create an event](/docs/api/rest/reference/event/methods/#operation/createEvent) | `zoom_events:write:event`, `zoom_events:write:event:admin` |

### Exhibitors

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create an exhibitor](/docs/api/rest/reference/event/methods/#operation/createExhibitor) | `zoom_events:write:exhibitor`, `zoom_events:write:exhibitor:admin` |
| [List exhibitors](/docs/api/rest/reference/event/methods/#operation/getExhibitors) | `zoom_events:read:list_exhibitors`, `zoom_events:read:list_exhibitors:admin` |
| [Update exhibitor for an event](/docs/api/rest/reference/event/methods/#operation/updateExhibitor) | `zoom_events:update:exhibitor`, `zoom_events:update:exhibitor:admin` |
| [Delete an exhibitor](/docs/api/rest/reference/event/methods/#operation/deleteExhibitor) | `zoom_events:delete:exhibitor`, `zoom_events:delete:exhibitor:admin` |
| [List sponsor tiers](/docs/api/rest/reference/event/methods/#operation/ListSponsorTiers) | `zoom_events:read:list_sponsor_tiers`, `zoom_events:read:list_sponsor_tiers:admin` |
| [Get an exhibitor](/docs/api/rest/reference/event/methods/#operation/getExhibitorInfo) | `zoom_events:read:exhibitor`, `zoom_events:read:exhibitor:admin` |

### Files

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Initiate and complete the multipart file upload](/docs/api/rest/reference/event/methods/#operation/initiateAndCompleteAEventMultipartUpload.) | `zoom_events:write:file_upload`, `zoom_events:write:file_upload:admin` |
| [Upload events multipart files](/docs/api/rest/reference/event/methods/#operation/uploadMultipartEventFile) | `zoom_events:write:file_upload`, `zoom_events:write:file_upload:admin` |
| [Upload events file](/docs/api/rest/reference/event/methods/#operation/uploadEventFile) | `zoom_events:write:file_upload`, `zoom_events:write:file_upload:admin` |

### Hubs

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Creates a new hub host](/docs/api/rest/reference/event/methods/#operation/createHubHost) | `zoom_events:write:hub_host`, `zoom_events:write:hub_host:admin` |
| [List hub Hosts](/docs/api/rest/reference/event/methods/#operation/gethubhostList) | `zoom_events:read:list_hub_hosts`, `zoom_events:read:list_hub_hosts:admin` |
| [List hub videos](/docs/api/rest/reference/event/methods/#operation/ListHubVideos) | `zoom_events:read:list_hub_videos`, `zoom_events:read:list_hub_videos:admin` |
| [Remove hub host](/docs/api/rest/reference/event/methods/#operation/deleteHubHost) | `zoom_events:delete:hub_host`, `zoom_events:delete:hub_host:admin` |
| [List hubs](/docs/api/rest/reference/event/methods/#operation/getHubList) | `zoom_events:read:list_hubs`, `zoom_events:read:list_hubs:admin` |

### Registrants

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List registrants](/docs/api/rest/reference/event/methods/#operation/getRegistrants) | `zoom_events:read:list_registrants`, `zoom_events:read:list_registrants:admin` |
| [List session attendees](/docs/api/rest/reference/event/methods/#operation/getSessionAttendeeList) | `zoom_events:read:list_session_attendees`, `zoom_events:read:list_session_attendees:admin` |

### Reports

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get VOD channel registration report](/docs/api/rest/reference/event/methods/#operation/VodChannelReigistration) | `zoom_events:read:vod_registrations`, `zoom_events:read:vod_registrations:admin` |
| [Get event survey report](/docs/api/rest/reference/event/methods/#operation/EventSurveyReportApi) | `zoom_events:read:list_session_surveys`, `zoom_events:read:list_session_surveys:admin` |
| [Get session attendance report](/docs/api/rest/reference/event/methods/#operation/SessionAttendanceReport) | `zoom_events:read:session_attendance`, `zoom_events:read:session_attendance:admin` |
| [Get chat transcripts report](/docs/api/rest/reference/event/methods/#operation/ChatTranscriptsReport) | `zoom_events:read:chat_transcripts`, `zoom_events:read:chat_transcripts:admin` |
| [Get custom report](/docs/api/rest/reference/event/methods/#operation/getCustomEventReport) | `zoom_events:read:custom_report`, `zoom_events:read:custom_report:admin` |
| [Get event registrations report](/docs/api/rest/reference/event/methods/#operation/EventRegistrationsReport) | `zoom_events:read:event_registration`, `zoom_events:read:event_registration:admin` |
| [Get event attendance (Live or Lobby) report](/docs/api/rest/reference/event/methods/#operation/EventAttendanceReport) | `zoom_events:read:event_attendance`, `zoom_events:read:event_attendance:admin` |

### Sessions

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List sessions](/docs/api/rest/reference/event/methods/#operation/getEventSessionList) | `zoom_events:read:list_sessions`, `zoom_events:read:list_sessions:admin` |
| [List session reservations](/docs/api/rest/reference/event/methods/#operation/ListSessionReservations) | `zoom_events:read:list_session_reservations`, `zoom_events:read:list_session_reservations:admin` |
| [Add session reservations](/docs/api/rest/reference/event/methods/#operation/AddSessionReservations) | `zoom_events:write:session_reservations`, `zoom_events:write:session_reservations:admin` |
| [Update a session](/docs/api/rest/reference/event/methods/#operation/updateEventSession) | `zoom_events:update:session`, `zoom_events:update:session:admin` |
| [Get the session information](/docs/api/rest/reference/event/methods/#operation/getEventSessionInfo) | `zoom_events:read:session`, `zoom_events:read:session:admin` |
| [Create a session](/docs/api/rest/reference/event/methods/#operation/createEventSession) | `zoom_events:write:session`, `zoom_events:write:session:admin` |
| [List session polls](/docs/api/rest/reference/event/methods/#operation/getSessionPolls) | `zoom_events:read:list_session_polls`, `zoom_events:read:list_session_polls:admin` |
| [Get session livestream configuration](/docs/api/rest/reference/event/methods/#operation/getSessionLivestreamConfiguration) | `zoom_events:read:session_livestream_config`, `zoom_events:read:session_livestream_config:admin` |
| [Delete session reservations](/docs/api/rest/reference/event/methods/#operation/DeleteSessionReservations) | `zoom_events:delete:session_reservations`, `zoom_events:delete:session_reservations:admin` |
| [Update session livestream configuration](/docs/api/rest/reference/event/methods/#operation/UpdateSessionLivestreamConfiguration) | `zoom_events:update:session_livestream_config`, `zoom_events:update:session_livestream_config:admin` |
| [List session interpreters](/docs/api/rest/reference/event/methods/#operation/getSessionInterpreterList) | `zoom_events:read:list_session_interpreters`, `zoom_events:read:list_session_interpreters:admin` |
| [Delete a session](/docs/api/rest/reference/event/methods/#operation/deleteEventSession) | `zoom_events:delete:session`, `zoom_events:delete:session:admin` |
| [Create or update session polls](/docs/api/rest/reference/event/methods/#operation/updateSessionPolls) | `zoom_events:update:session_poll`, `zoom_events:update:session_poll:admin` |
| [Get ticket session join token by Event ID and Session ID](/docs/api/rest/reference/event/methods/#operation/getSessionJoinToken) | `zoom_events:read:session_token`, `zoom_events:read:session_token:admin` |
| [Create or update session interpreters](/docs/api/rest/reference/event/methods/#operation/updateSessionInterpreters) | `zoom_events:update:session_interpreter`, `zoom_events:update:session_interpreter:admin` |

### Speakers

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List speakers](/docs/api/rest/reference/event/methods/#operation/getSpeakers) | `zoom_events:read:list_speakers`, `zoom_events:read:list_speakers:admin` |
| [Get a speaker](/docs/api/rest/reference/event/methods/#operation/getSpeaker) | `zoom_events:read:speaker`, `zoom_events:read:speaker:admin` |
| [Create a speaker](/docs/api/rest/reference/event/methods/#operation/createSpeaker) | `zoom_events:write:speaker`, `zoom_events:write:speaker:admin` |
| [Delete a speaker](/docs/api/rest/reference/event/methods/#operation/deleteSpeaker) | `zoom_events:delete:speaker`, `zoom_events:delete:speaker:admin` |
| [Update a speaker](/docs/api/rest/reference/event/methods/#operation/updateSpeaker) | `zoom_events:update:speaker`, `zoom_events:update:speaker:admin` |

### Ticket Types

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List ticket types](/docs/api/rest/reference/event/methods/#operation/getEventTicketTypes) | `zoom_events:read:list_ticket_types`, `zoom_events:read:list_ticket_types:admin` |
| [Update registration questions for ticket type](/docs/api/rest/reference/event/methods/#operation/updateRegistrationQuestionsForTicketType) | `zoom_events:update:registraion_question`, `zoom_events:update:registraion_question:admin` |
| [Delete a ticket type](/docs/api/rest/reference/event/methods/#operation/deleteEventTicketType) | `zoom_events:delete:ticket_type`, `zoom_events:delete:ticket_type:admin` |
| [Update ticket type for an event](/docs/api/rest/reference/event/methods/#operation/updateTicketType) | `zoom_events:update:ticket_type`, `zoom_events:update:ticket_type:admin` |
| [List registration questions for ticket type](/docs/api/rest/reference/event/methods/#operation/getRegistrationQuestionsForTicketType) | `zoom_events:read:list_registration_questions`, `zoom_events:read:list_registration_questions:admin` |
| [Create an event ticket type](/docs/api/rest/reference/event/methods/#operation/createTicketType) | `zoom_events:write:ticket_type`, `zoom_events:write:ticket_type:admin` |
| [Update registration questions for an event](/docs/api/rest/reference/event/methods/#operation/updateRegistrationQuestionsForEvent) | `zoom_events:update:registraion_question`, `zoom_events:update:registraion_question:admin` |
| [List registration questions for an event](/docs/api/rest/reference/event/methods/#operation/getRegistrationQuestionsForEvent) | `zoom_events:read:list_registration_questions`, `zoom_events:read:list_registration_questions:admin` |

### Tickets

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update ticket](/docs/api/rest/reference/event/methods/#operation/Updateticket) | `zoom_events:write:ticket`, `zoom_events:write:ticket:admin` |
| [Create tickets](/docs/api/rest/reference/event/methods/#operation/createTickets) | `zoom_events:write:ticket`, `zoom_events:write:ticket:admin` |
| [Get a ticket](/docs/api/rest/reference/event/methods/#operation/getTicketDetails) | `zoom_events:read:ticket`, `zoom_events:read:ticket:admin` |
| [Delete a ticket](/docs/api/rest/reference/event/methods/#operation/deleteTicket) | `zoom_events:delete:ticket`, `zoom_events:delete:ticket:admin` |
| [List tickets](/docs/api/rest/reference/event/methods/#operation/getTickets) | `zoom_events:read:list_tickets`, `zoom_events:read:list_tickets:admin` |

### Video On-Demand

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [VOD channel actions](/docs/api/rest/reference/event/methods/#operation/vodChannelActions) | `zoom_events:update:vod_channel`, `zoom_events:update:vod_channel:admin` |
| [List VOD channel videos](/docs/api/rest/reference/event/methods/#operation/ListVODChannelVideos) | `zoom_events:read:list_vod_channel_videos`, `zoom_events:read:list_vod_channel_videos:admin` |
| [Delete VOD Channel](/docs/api/rest/reference/event/methods/#operation/DeleteVODChannel) | `zoom_events:delete:vod_channel`, `zoom_events:delete:vod_channel:admin` |
| [Create VOD channel](/docs/api/rest/reference/event/methods/#operation/createVodChannel) | `zoom_events:write:vod_channel`, `zoom_events:write:vod_channel:admin` |
| [Delete VOD channel video](/docs/api/rest/reference/event/methods/#operation/DeleteVODChannelVideo) | `zoom_events:delete:vod_channel_videos`, `zoom_events:delete:vod_channel_videos:admin` |
| [Update VOD channel](/docs/api/rest/reference/event/methods/#operation/UpdateVideoChannel) | `zoom_events:update:vod_channel`, `zoom_events:update:vod_channel:admin` |
| [Get VOD channel details](/docs/api/rest/reference/event/methods/#operation/getVODChannelDetail) | `zoom_events:read:vod_channel`, `zoom_events:read:vod_channel:admin` |
| [List channels](/docs/api/rest/reference/event/methods/#operation/getVODChannels) | `zoom_events:read:list_all_vod_channels`, `zoom_events:read:list_all_vod_channels:admin` |
| [Add VOD channel videos](/docs/api/rest/reference/event/methods/#operation/AddVODChannelVideos) | `zoom_events:write:vod_channel_videos`, `zoom_events:write:vod_channel_videos:admin` |

### Video On-Demand Registrations

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List VOD Registration](/docs/api/rest/reference/event/methods/#operation/ListVODRegistration) | `zoom_events:read:vod_registrations`, `zoom_events:read:vod_registrations:admin` |
| [Get VOD Registration Questions](/docs/api/rest/reference/event/methods/#operation/getRegistrationQuestionsForVODChannel) | `zoom_events:read:vod_registration_questions`, `zoom_events:read:vod_registration_questions:admin` |
| [update VOD channel registration questions](/docs/api/rest/reference/event/methods/#operation/updateRegistrationQuestionsForVODchannel) | `zoom_events:update:vod_registration_questions`, `zoom_events:update:vod_registration_questions:admin` |
| [VOD channel registration](/docs/api/rest/reference/event/methods/#operation/VODTicketRegistration) | `zoom_events:write:vod_registration`, `zoom_events:write:vod_registration:admin` |

## Zoom Mail


### Drafts

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update the specified draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/update_draft_email) | `email:update:draft`, `email:update:draft:admin` |
| [List emails from draft folder](/docs/api/rest/reference/zoom-mail/methods/#operation/list_draft_emails) | `email:read:list_drafts`, `email:read:list_drafts:admin` |
| [Get the specified draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/get_draft_email) | `email:read:draft`, `email:read:draft:admin` |
| [Send out a draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/send_draft_email) | `email:write:send_draft`, `email:write:send_draft:admin` |
| [Delete an existing draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_draft_email) | `email:delete:draft`, `email:delete:draft:admin` |
| [Create a new draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/create_draft_email) | `email:write:draft`, `email:write:draft:admin` |

### History

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List history of events for mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_mailbox_history) | `email:read:history`, `email:read:history:admin` |

### Labels

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get the specified label in mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/get_label_in_mailbox) | `email:read:label`, `email:read:label:admin` |
| [Update the specified label in mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/update_label_in_mailbox) | `email:update:label`, `email:update:label:admin` |
| [List labels in the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_labels_in_mailbox) | `email:read:list_labels`, `email:read:list_labels:admin` |
| [Create a new label in mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/create_label_in_mailbox) | `email:write:label`, `email:write:label:admin` |
| [Delete an existing label from mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_label_from_mailbox) | `email:delete:label`, `email:delete:label:admin` |
| [Patch the specified label in mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/patch_label_in_mailbox) | `email:update:label`, `email:update:label:admin` |

### Mailbox

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get the mailbox profile](/docs/api/rest/reference/zoom-mail/methods/#operation/get_mailbox_profile) | `email:read:profile`, `email:read:profile:admin` |

### Messages

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete an existing email](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_email) | `email:delete:msg`, `email:delete:msg:admin` |
| [Move the specified email to TRASH folder](/docs/api/rest/reference/zoom-mail/methods/#operation/trash_email) | `email:write:trash_msg`, `email:write:trash_msg:admin` |
| [Move the specified email out of TRASH folder](/docs/api/rest/reference/zoom-mail/methods/#operation/untrash_email) | `email:write:untrash_msg`, `email:write:untrash_msg:admin` |
| [Update the specified email](/docs/api/rest/reference/zoom-mail/methods/#operation/update_email) | `email:write:modify_msg`, `email:write:modify_msg:admin` |
| [List emails from the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_emails) | `email:read:list_msgs`, `email:read:list_msgs:admin` |
| [Send out an email](/docs/api/rest/reference/zoom-mail/methods/#operation/send_email) | `email:write:send_msg`, `email:write:send_msg:admin` |
| [Batch delete the specified emails](/docs/api/rest/reference/zoom-mail/methods/#operation/batch_delete_emails) | `email:write:batch_delete_msgs`, `email:write:batch_delete_msgs:admin` |
| [Batch modify the specified emails](/docs/api/rest/reference/zoom-mail/methods/#operation/batch_modify_emails) | `email:write:batch_modify_msgs`, `email:write:batch_modify_msgs:admin` |
| [Create a new email](/docs/api/rest/reference/zoom-mail/methods/#operation/create_email) | `email:write:msg`, `email:write:msg:admin` |
| [Get the specified email](/docs/api/rest/reference/zoom-mail/methods/#operation/get_email) | `email:read:msg`, `email:read:msg:admin` |

### Messages.Attachments

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get the specified attachment for an email](/docs/api/rest/reference/zoom-mail/methods/#operation/get_email_attachment) | `email:read:attachment`, `email:read:attachment:admin` |

### Settings

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update mailbox vacation response setting](/docs/api/rest/reference/zoom-mail/methods/#operation/update_mailbox_vacation_response_setting) | `email:update:setting_vacation`, `email:update:setting_vacation:admin` |
| [Get mailbox vacation response setting](/docs/api/rest/reference/zoom-mail/methods/#operation/get_mail_vacation_response_setting) | `email:read:setting_vacation`, `email:read:setting_vacation:admin` |

### Settings.Delegates

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Revoke an existing delegate access from the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/revoke_mailbox_delegate) | `email:delete:setting_delegate`, `email:delete:setting_delegate:admin` |
| [List delegates on the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_mailbox_delegates) | `email:read:list_setting_delegates`, `email:read:list_setting_delegates:admin` |
| [Grant a new delegate access on the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/grant_mailbox_delegate) | `email:write:setting_delegate`, `email:write:setting_delegate:admin` |
| [Get the specified delegate on the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/get_mailbox_delegate) | `email:read:setting_delegate`, `email:read:setting_delegate:admin` |

### Settings.Filters

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get the specified email filter](/docs/api/rest/reference/zoom-mail/methods/#operation/get_email_filter) | `email:read:setting_filter`, `email:read:setting_filter:admin` |
| [Delete the specified email filter](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_email_filter) | `email:delete:setting_filter`, `email:delete:setting_filter:admin` |
| [Create an email filter](/docs/api/rest/reference/zoom-mail/methods/#operation/create_email_filter) | `email:write:setting_filter`, `email:write:setting_filter:admin` |
| [List email filters](/docs/api/rest/reference/zoom-mail/methods/#operation/list_email_filters) | `email:read:list_setting_filters`, `email:read:list_setting_filters:admin` |

### Threads

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete an existing email thread](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_email_thread) | `email:delete:thread`, `email:delete:thread:admin` |
| [Get the specified email thread](/docs/api/rest/reference/zoom-mail/methods/#operation/get_email_thread) | `email:read:thread`, `email:read:thread:admin` |
| [Move the specified thread out of TRASH folder](/docs/api/rest/reference/zoom-mail/methods/#operation/untrash_email_thread) | `email:write:untrash_thread`, `email:write:untrash_thread:admin` |
| [Move the specified thread to TRASH folder](/docs/api/rest/reference/zoom-mail/methods/#operation/trash_email_thread) | `email:write:trash_thread`, `email:write:trash_thread:admin` |
| [List email threads from the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_email_threads) | `email:read:list_threads`, `email:read:list_threads:admin` |
| [Update the specified thread](/docs/api/rest/reference/zoom-mail/methods/#operation/update_email_thread) | `email:write:thread`, `email:write:thread:admin` |

## Zoom Meeting


### Archiving

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a meeting's archived files](/docs/api/rest/reference/zoom-api/methods/#operation/getArchivedFiles) | `archiving:read:archived_files:admin`, `archiving:read:archived_files` |
| [List archived files](/docs/api/rest/reference/zoom-api/methods/#operation/listArchivedFiles) | `archiving:read:list_archived_files:admin`, `archiving:read:list_archived_files:master` |
| [List archived files](/docs/api/rest/reference/zoom-api/ma/#operation/listArchivedFiles) | `archiving:read:list_archived_files:master` |
| [Get archived file statistics](/docs/api/rest/reference/zoom-api/methods/#operation/getArchivedFileStatistics) | `archiving:read:archived_file_statistics:admin` |
| [Get a meeting's archive token for local archiving](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLocalArchivingArchiveToken) | `meeting:read:local_archiving_token:admin` |
| [Update an archived file's auto-delete status](/docs/api/rest/reference/zoom-api/methods/#operation/updateArchivedFile) | `archiving:update:archived_file_auto_delete_status`, `archiving:update:archived_file_auto_delete_status:admin` |
| [Delete a meeting's archived files](/docs/api/rest/reference/zoom-api/methods/#operation/deleteArchivedFiles) | `archiving:delete:archived_files:admin` |

### Cloud Recording

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a meeting or webinar recording's analytics details](/docs/api/rest/reference/zoom-api/methods/#operation/analytics_details) | `cloud_recording:read:recording_analytics_details`, `cloud_recording:read:recording_analytics_details:master`, `cloud_recording:read:recording_analytics_details:admin` |
| [Get a meeting or webinar recording's analytics details](/docs/api/rest/reference/zoom-api/ma/#operation/analytics_details) | `cloud_recording:read:recording_analytics_details:master` |
| [Get a meeting transcript](/docs/api/rest/reference/zoom-api/methods/#operation/GetMeetingTranscript) | `cloud_recording:read:meeting_transcript`, `cloud_recording:read:meeting_transcript:admin` |
| [Recover meeting recordings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingStatusUpdate) | `cloud_recording:update:recover_meeting_recordings`, `cloud_recording:update:recover_meeting_recordings:master`, `cloud_recording:update:recover_meeting_recordings:admin` |
| [Recover meeting recordings](/docs/api/rest/reference/zoom-api/ma/#operation/recordingStatusUpdate) | `cloud_recording:update:recover_meeting_recordings:master` |
| [Get meeting recording settings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingSettingUpdate) | `cloud_recording:read:recording_settings`, `cloud_recording:read:recording_settings:admin`, `cloud_recording:read:recording_settings:master` |
| [Get meeting recording settings](/docs/api/rest/reference/zoom-api/ma/#operation/recordingSettingUpdate) | `cloud_recording:read:recording_settings:master` |
| [Get registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/recordingRegistrantsQuestionsGet) | `cloud_recording:read:registration_questions`, `cloud_recording:read:registration_questions:master`, `cloud_recording:read:registration_questions:admin` |
| [Get registration questions](/docs/api/rest/reference/zoom-api/ma/#operation/recordingRegistrantsQuestionsGet) | `cloud_recording:read:registration_questions:master` |
| [Create a recording registrant](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRecordingRegistrantCreate) | `cloud_recording:write:recording_registrant`, `cloud_recording:write:recording_registrant:master`, `cloud_recording:write:recording_registrant:admin` |
| [Create a recording registrant](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRecordingRegistrantCreate) | `cloud_recording:write:recording_registrant:master` |
| [List an account's recordings](/docs/api/rest/reference/zoom-api/ma/#operation/ListRecordingsOfAnAccount) | `cloud_recording:read:list_account_recordings:master`, `cloud_recording:read:list_account_recordings:admin` |
| [List all recordings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingsList) | `cloud_recording:read:list_user_recordings`, `cloud_recording:read:list_user_recordings:master`, `cloud_recording:read:list_user_recordings:admin` |
| [List all recordings](/docs/api/rest/reference/zoom-api/ma/#operation/recordingsList) | `cloud_recording:read:list_user_recordings:master` |
| [Update a registrant's status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRecordingRegistrantStatus) | `cloud_recording:update:registrant_status`, `cloud_recording:update:registrant_status:master`, `cloud_recording:update:registrant_status:admin` |
| [Update a registrant's status](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRecordingRegistrantStatus) | `cloud_recording:update:registrant_status:master` |
| [Get a meeting or webinar recording's analytics summary](/docs/api/rest/reference/zoom-api/methods/#operation/analytics_summary) | `cloud_recording:read:recording_analytics_summary`, `cloud_recording:read:recording_analytics_summary:master`, `cloud_recording:read:recording_analytics_summary:admin` |
| [Get a meeting or webinar recording's analytics summary](/docs/api/rest/reference/zoom-api/ma/#operation/analytics_summary) | `cloud_recording:read:recording_analytics_summary:master` |
| [Recover a single recording](/docs/api/rest/reference/zoom-api/methods/#operation/recordingStatusUpdateOne) | `cloud_recording:update:recover_single_recording`, `cloud_recording:update:recover_single_recording:master`, `cloud_recording:update:recover_single_recording:admin` |
| [Recover a single recording](/docs/api/rest/reference/zoom-api/ma/#operation/recordingStatusUpdateOne) | `cloud_recording:update:recover_single_recording:master` |
| [List recording registrants](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRecordingRegistrants) | `cloud_recording:read:list_recording_registrants`, `cloud_recording:read:list_recording_registrants:admin`, `cloud_recording:read:list_recording_registrants:master` |
| [List recording registrants](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRecordingRegistrants) | `cloud_recording:read:list_recording_registrants:master` |
| [Delete a recording file for a meeting or webinar](/docs/api/rest/reference/zoom-api/methods/#operation/recordingDeleteOne) | `cloud_recording:delete:recording_file`, `cloud_recording:delete:recording_file:admin`, `cloud_recording:delete:recording_file:master` |
| [Delete a recording file for a meeting or webinar](/docs/api/rest/reference/zoom-api/ma/#operation/recordingDeleteOne) | `cloud_recording:delete:recording_file:master` |
| [Delete meeting or webinar recordings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingDelete) | `cloud_recording:delete:meeting_recording`, `cloud_recording:delete:meeting_recording:admin`, `cloud_recording:delete:meeting_recording:master` |
| [Delete meeting or webinar recordings](/docs/api/rest/reference/zoom-api/ma/#operation/recordingDelete) | `cloud_recording:delete:meeting_recording:master` |
| [Update meeting recording settings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingSettingsUpdate) | `cloud_recording:update:recording_settings`, `cloud_recording:update:recording_settings:master`, `cloud_recording:update:recording_settings:admin` |
| [Update meeting recording settings](/docs/api/rest/reference/zoom-api/ma/#operation/recordingSettingsUpdate) | `cloud_recording:update:recording_settings:master` |
| [Get meeting recordings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingGet) | `cloud_recording:read:list_recording_files:admin`, `cloud_recording:read:list_recording_files`, `cloud_recording:read:list_recording_files:master` |
| [Get meeting recordings](/docs/api/rest/reference/zoom-api/ma/#operation/recordingGet) | `cloud_recording:read:list_recording_files:master` |
| [Update registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/recordingRegistrantQuestionUpdate) | `cloud_recording:update:registration_questions:admin`, `cloud_recording:update:registration_questions`, `cloud_recording:update:registration_questions:master` |
| [Update registration questions](/docs/api/rest/reference/zoom-api/ma/#operation/recordingRegistrantQuestionUpdate) | `cloud_recording:update:registration_questions:master` |
| [Delete a meeting or webinar transcript](/docs/api/rest/reference/zoom-api/methods/#operation/DeleteMeetingTranscript) | `cloud_recording:delete:meeting_transcript`, `cloud_recording:delete:meeting_transcript:admin` |

### Devices

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Upgrade ZPA firmware or app](/docs/api/rest/reference/zoom-api/methods/#operation/UpgradeZpas/app) | `device:write:zpa_os_app:admin`, `device:write:zpa_os_app:master` |
| [Get ZPA version info](/docs/api/rest/reference/zoom-api/methods/#operation/GetZpaVersioninfo) | `device:read:list_zpa_versions:admin`, `device:read:list_zpa_versions:master` |
| [Assign a device to a user or commonarea](/docs/api/rest/reference/zoom-api/methods/#operation/Assigndevicetoauser/commonarea) | `device:write:zpa_device:admin`, `device:write:zpa_device:master` |
| [Delete ZPA device by vendor and mac address](/docs/api/rest/reference/zoom-api/methods/#operation/DeleteZpaDeviceByVendorAndMacAddress) | `device:delete:zpa_device:admin`, `device:delete:zpa_device:master` |
| [Get ZDM group info](/docs/api/rest/reference/zoom-api/methods/#operation/Getzdmgroupinfo) | `device:read:list_groups:admin`, `device:read:list_groups:master` |
| [Assign a device to a group](/docs/api/rest/reference/zoom-api/methods/#operation/assginGroup) | `device:write:group:admin`, `device:write:group:master` |
| [Get Zoom Phone Appliance settings by user ID](/docs/api/rest/reference/zoom-api/methods/#operation/GetZpaDeviceListProfileSettingOfaUser) | `device:read:user_setting:admin`, `device:read:user_setting:master` |
| [Change device association](/docs/api/rest/reference/zoom-api/methods/#operation/changeDeviceAssociation) | `device:update:zdm_device_assignment:admin` |

### H323 Devices

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create a H.323/SIP device](/docs/api/rest/reference/zoom-api/methods/#operation/deviceCreate) | `h323_device:write:device:admin` |
| [Delete a H.323/SIP device](/docs/api/rest/reference/zoom-api/methods/#operation/deviceDelete) | `h323_device:delete:device:admin` |
| [Update a H.323/SIP device](/docs/api/rest/reference/zoom-api/methods/#operation/deviceUpdate) | `h323_device:update:device:admin` |
| [List all H.323/SIP devices](/docs/api/rest/reference/zoom-api/methods/#operation/deviceList) | `h323_device:read:list_devices:admin` |

### In-Meeting Apps

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Add a meeting app](/docs/api/rest/reference/zoom-api/methods/#operation/meetingAppAdd) | `meeting:write:open_app`, `meeting:write:open_app:admin` |
| [Delete a meeting app](/docs/api/rest/reference/zoom-api/methods/#operation/meetingAppDelete) | `meeting:delete:open_app`, `meeting:delete:open_app:admin` |

### In-Meeting Features

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a meeting's join token for local recording](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLocalRecordingJoinToken) | `meeting:read:local_recording_token`, `meeting:read:local_recording_token:admin` |
| [Use in-meeting controls](/docs/api/rest/reference/zoom-api/methods/#operation/inMeetingControl) | `meeting:update:in_meeting_controls`, `meeting:update:in_meeting_controls:admin` |
| [Use in-meeting controls](/docs/api/rest/reference/zoom-api/ma/#operation/inMeetingControl) | `meeting:update:in_meeting_controls:master` |
| [Update a live meeting message](/docs/api/rest/reference/zoom-api/methods/#operation/updateMeetingChatMessageById) | `meeting:update:live_meeting_chat_message`, `meeting:update:live_meeting_chat_message:admin` |
| [Get meeting's token](/docs/api/rest/reference/zoom-api/methods/#operation/meetingToken) | `meeting:read:token`, `meeting:read:token:admin` |
| [Get meeting's token](/docs/api/rest/reference/zoom-api/ma/#operation/meetingToken) | `meeting:read:token:master` |
| [Delete a live meeting message](/docs/api/rest/reference/zoom-api/methods/#operation/deleteMeetingChatMessageById) | `meeting:delete:live_meeting_chat_message`, `meeting:delete:live_meeting_chat_message:admin` |

### Invitation & Registration

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete a meeting registrant](/docs/api/rest/reference/zoom-api/methods/#operation/meetingregistrantdelete) | `meeting:delete:registrant`, `meeting:delete:registrant:admin` |
| [Delete a meeting registrant](/docs/api/rest/reference/zoom-api/ma/#operation/meetingregistrantdelete) | `meeting:delete:registrant:master` |
| [Perform batch registration](/docs/api/rest/reference/zoom-api/methods/#operation/addBatchRegistrants) | `meeting:write:batch_registrants`, `meeting:write:batch_registrants:admin` |
| [Perform batch registration](/docs/api/rest/reference/zoom-api/ma/#operation/addBatchRegistrants) | `meeting:write:batch_registrants:master` |
| [Get meeting invitation](/docs/api/rest/reference/zoom-api/methods/#operation/meetingInvitation) | `meeting:read:invitation`, `meeting:read:invitation:admin` |
| [Get meeting invitation](/docs/api/rest/reference/zoom-api/ma/#operation/meetingInvitation) | `meeting:read:invitation:master` |
| [Add a meeting registrant](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantCreate) | `meeting:write:registrant`, `meeting:write:registrant:admin` |
| [Add a meeting registrant](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRegistrantCreate) | `meeting:write:registrant:master` |
| [Update registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantQuestionUpdate) | `meeting:update:registration_question`, `meeting:update:registration_question:admin` |
| [Update registration questions](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRegistrantQuestionUpdate) | `meeting:update:registration_question:master` |
| [Update registrant's status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantStatus) | `meeting:update:registrant_status`, `meeting:update:registrant_status:admin` |
| [Update registrant's status](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRegistrantStatus) | `meeting:update:registrant_status:master` |
| [Create a meeting's invite links](/docs/api/rest/reference/zoom-api/methods/#operation/meetingInviteLinksCreate) | `meeting:write:invite_links`, `meeting:write:invite_links:admin` |
| [Create a meeting's invite links](/docs/api/rest/reference/zoom-api/ma/#operation/meetingInviteLinksCreate) | `meeting:write:invite_links:master` |
| [List meeting registrants](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrants) | `meeting:read:list_registrants`, `meeting:read:list_registrants:admin` |
| [List meeting registrants](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRegistrants) | `meeting:read:list_registrants:master` |
| [List registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantsQuestionsGet) | `meeting:read:list_registration_questions`, `meeting:read:list_registration_questions:admin` |
| [Get a meeting registrant](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantGet) | `meeting:read:registrant`, `meeting:read:registrant:admin` |
| [Get a meeting registrant](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRegistrantGet) | `meeting:read:registrant:master` |

### Live streaming

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update a livestream](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLiveStreamUpdate) | `meeting:update:livestream`, `meeting:update:livestream:admin` |
| [Update a livestream](/docs/api/rest/reference/zoom-api/ma/#operation/meetingLiveStreamUpdate) | `meeting:update:livestream:master` |
| [Update livestream status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLiveStreamStatusUpdate) | `meeting:update:livestream_status`, `meeting:update:livestream_status:admin` |
| [Update livestream status](/docs/api/rest/reference/zoom-api/ma/#operation/meetingLiveStreamStatusUpdate) | `meeting:update:livestream_status:master` |
| [Get livestream details](/docs/api/rest/reference/zoom-api/methods/#operation/getMeetingLiveStreamDetails) | `meeting:read:livestream`, `meeting:read:livestream:admin` |
| [Get livestream details](/docs/api/rest/reference/zoom-api/ma/#operation/getMeetingLiveStreamDetails) | `meeting:read:livestream:master` |
| [Get a meeting's join token for live streaming](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLiveStreamingJoinToken) | `meeting:read:live_streaming_token`, `meeting:read:live_streaming_token:admin` |

### Meetings

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List past meeting instances](/docs/api/rest/reference/zoom-api/methods/#operation/pastMeetings) | `meeting:read:list_past_instances`, `meeting:read:list_past_instances:admin` |
| [List past meeting instances](/docs/api/rest/reference/zoom-api/ma/#operation/pastMeetings) | `meeting:read:list_past_instances:master` |
| [Get past meeting participants](/docs/api/rest/reference/zoom-api/methods/#operation/pastMeetingParticipants) | `meeting:read:list_past_participants`, `meeting:read:list_past_participants:admin` |
| [Get a meeting SIP URI with passcode](/docs/api/rest/reference/zoom-api/methods/#operation/getSipDialingWithPasscode) | `meeting:write:sip_dialing`, `meeting:write:sip_dialing:admin` |
| [Create a meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meetingCreate) | `meeting:write:meeting`, `meeting:write:meeting:admin` |
| [Create a meeting](/docs/api/rest/reference/zoom-api/ma/#operation/meetingCreate) | `meeting:write:meeting:master` |
| [Update meeting status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingStatus) | `meeting:update:status`, `meeting:update:status:admin` |
| [Update meeting status](/docs/api/rest/reference/zoom-api/ma/#operation/meetingStatus) | `meeting:update:status:master` |
| [Get past meeting details](/docs/api/rest/reference/zoom-api/methods/#operation/pastMeetingDetails) | `meeting:read:past_meeting`, `meeting:read:past_meeting:admin` |
| [List meetings](/docs/api/rest/reference/zoom-api/methods/#operation/meetings) | `meeting:read:list_meetings`, `meeting:read:list_meetings:admin` |
| [List meetings](/docs/api/rest/reference/zoom-api/ma/#operation/meetings) | `meeting:read:list_meetings:master` |
| [Update a meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meetingUpdate) | `meeting:update:meeting:admin`, `meeting:update:meeting` |
| [Update a meeting](/docs/api/rest/reference/zoom-api/ma/#operation/meetingUpdate) | `meeting:update:meeting:master` |
| [Delete a meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meetingDelete) | `meeting:delete:meeting`, `meeting:delete:meeting:admin` |
| [Delete a meeting](/docs/api/rest/reference/zoom-api/ma/#operation/meetingDelete) | `meeting:delete:meeting:master` |
| [Update participant Real-Time Media Streams (RTMS) app status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRTMSStatusUpdate) | `meeting:update:participant_rtms_app_status`, `meeting:update:participant_rtms_app_status:admin` |
| [Get a meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meeting) | `meeting:read:meeting`, `meeting:read:meeting:admin` |
| [Get a meeting](/docs/api/rest/reference/zoom-api/ma/#operation/meeting) | `meeting:read:meeting:master` |
| [List upcoming meetings](/docs/api/rest/reference/zoom-api/methods/#operation/listUpcomingMeeting) | `meeting:read:list_upcoming_meetings`, `meeting:read:list_upcoming_meetings:admin` |
| [List past meetings' Q&A](/docs/api/rest/reference/zoom-api/methods/#operation/listPastMeetingQA) | `meeting:read:past_qa`, `meeting:read:past_qa:admin` |

### PAC

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List a user's PAC accounts](/docs/api/rest/reference/zoom-api/methods/#operation/userPACs) | `pac:read:list_pac_accounts`, `pac:read:list_pac_accounts:admin` |
| [List a user's PAC accounts](/docs/api/rest/reference/zoom-api/ma/#operation/userPACs) | `pac:read:list_pac_accounts:master` |

### Polls

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete a meeting poll](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollDelete) | `meeting:delete:poll`, `meeting:delete:poll:admin` |
| [Delete a meeting poll](/docs/api/rest/reference/zoom-api/ma/#operation/meetingPollDelete) | `meeting:delete:poll:master` |
| [List meeting polls](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPolls) | `meeting:read:list_polls`, `meeting:read:list_polls:admin` |
| [List meeting polls](/docs/api/rest/reference/zoom-api/ma/#operation/meetingPolls) | `meeting:read:list_polls:master` |
| [List past meeting's poll results](/docs/api/rest/reference/zoom-api/methods/#operation/listPastMeetingPolls) | `meeting:read:list_poll_results`, `meeting:read:list_poll_results:admin` |
| [Perform batch poll creation](/docs/api/rest/reference/zoom-api/methods/#operation/createBatchPolls) | `meeting:write:batch_polls`, `meeting:write:batch_polls:admin` |
| [Perform batch poll creation](/docs/api/rest/reference/zoom-api/ma/#operation/createBatchPolls) | `meeting:write:batch_polls:master` |
| [Create a meeting poll](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollCreate) | `meeting:write:poll`, `meeting:write:poll:admin` |
| [Create a meeting poll](/docs/api/rest/reference/zoom-api/ma/#operation/meetingPollCreate) | `meeting:write:poll:master` |
| [Get a meeting poll](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollGet) | `meeting:read:poll`, `meeting:read:poll:admin` |
| [Get a meeting poll](/docs/api/rest/reference/zoom-api/ma/#operation/meetingPollGet) | `meeting:read:poll:master` |
| [Update a meeting poll](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollUpdate) | `meeting:update:poll`, `meeting:update:poll:admin` |
| [Update a meeting poll](/docs/api/rest/reference/zoom-api/ma/#operation/meetingPollUpdate) | `meeting:update:poll:master` |

### Reports

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a meeting activities report](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetingactivitylogs) | `report:read:meeting_activity_log:admin` |
| [Get a meeting activities report](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetingactivitylogs) | `report:read:meeting_activity_log:master` |
| [Get telephone reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportTelephone) | `report:read:telephone:admin` |
| [Get telephone reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportTelephone) | `report:read:telephone:master` |
| [Get meeting detail reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetingDetails) | `report:read:meeting:admin` |
| [Get meeting detail reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetingDetails) | `report:read:meeting:master` |
| [Get operation logs report](/docs/api/rest/reference/zoom-api/methods/#operation/reportOperationLogs) | `report:read:operation_logs:admin` |
| [Get operation logs report](/docs/api/rest/reference/zoom-api/ma/#operation/reportOperationLogs) | `report:read:operation_logs:master` |
| [Get meeting Q&A report](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetingQA) | `report:read:meeting_qna:admin` |
| [Get meeting Q&A report](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetingQA) | `report:read:meeting_qna:master` |
| [Get history meeting and webinar list](/docs/api/rest/reference/zoom-api/methods/#operation/Gethistorymeetingandwebinarlist) | `report:read:list_history_meetings:admin` |
| [Get history meeting and webinar list](/docs/api/rest/reference/zoom-api/ma/#operation/Gethistorymeetingandwebinarlist) | `report:read:list_history_meetings:master` |
| [Get remote support report](/docs/api/rest/reference/zoom-api/methods/#operation/Getremotesupportreport) | `report:read:remote_support:admin` |
| [Get remote support report](/docs/api/rest/reference/zoom-api/ma/#operation/Getremotesupportreport) | `report:read:remote_support:master` |
| [Get webinar poll reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportWebinarPolls) | `report:read:list_webinar_polls:admin` |
| [Get webinar poll reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportWebinarPolls) | `report:read:list_webinar_polls:master` |
| [Get webinar Q&A report](/docs/api/rest/reference/zoom-api/methods/#operation/reportWebinarQA) | `report:read:webinar_qna:admin` |
| [Get webinar Q&A report](/docs/api/rest/reference/zoom-api/ma/#operation/reportWebinarQA) | `report:read:webinar_qna:master` |
| [Get sign In / sign out activity report](/docs/api/rest/reference/zoom-api/methods/#operation/reportSignInSignOutActivities) | `report:read:user_activities:admin` |
| [Get sign In / sign out activity report](/docs/api/rest/reference/zoom-api/ma/#operation/reportSignInSignOutActivities) | `report:read:user_activities:master` |
| [Get meeting poll reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetingPolls) | `report:read:list_meeting_polls:admin` |
| [Get meeting poll reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetingPolls) | `report:read:list_meeting_polls:master` |
| [Get meeting reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetings) | `report:read:user:admin` |
| [Get meeting reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetings) | `report:read:user:master` |
| [Get active or inactive host reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportUsers) | `report:read:list_users:admin` |
| [Get active or inactive host reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportUsers) | `report:read:list_users:master` |
| [Get webinar participant reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportWebinarParticipants) | `report:read:list_webinar_participants:admin` |
| [Get webinar participant reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportWebinarParticipants) | `report:read:list_webinar_participants:master` |
| [Get upcoming events reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportUpcomingEvents) | `report:read:upcoming_meetings_webinars:admin` |
| [Get upcoming events reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportUpcomingEvents) | `report:read:upcoming_meetings_webinars:master` |
| [Get webinar survey report](/docs/api/rest/reference/zoom-api/methods/#operation/reportWebinarSurvey) | `report:read:webinar_survey:admin` |
| [Get webinar survey report](/docs/api/rest/reference/zoom-api/ma/#operation/reportWebinarSurvey) | `report:read:webinar_survey:master` |
| [Get meeting participant reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetingParticipants) | `report:read:list_meeting_participants:admin` |
| [Get meeting participant reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetingParticipants) | `report:read:list_meeting_participants:master` |
| [Get billing reports](/docs/api/rest/reference/zoom-api/methods/#operation/getBillingReport) | `report:read:billing:admin` |
| [Get billing reports](/docs/api/rest/reference/zoom-api/ma/#operation/getBillingReport) | `report:read:billing:master` |
| [Get webinar detail reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportWebinarDetails) | `report:read:webinar:admin` |
| [Get webinar detail reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportWebinarDetails) | `report:read:webinar:master` |
| [Get billing invoice reports](/docs/api/rest/reference/zoom-api/methods/#operation/getBillingInvoicesReports) | `report:read:billing_invoice:admin` |
| [Get billing invoice reports](/docs/api/rest/reference/zoom-api/ma/#operation/getBillingInvoicesReports) | `report:read:billing_invoice:master` |
| [Get meeting survey report](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetingSurvey) | `report:read:meeting_survey:admin` |
| [Get meeting survey report](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetingSurvey) | `report:read:meeting_survey:master` |

### SIP Connected Audio

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List internal call-out countries](/docs/api/rest/reference/zoom-api/ma/#operation/ListInternalCall-outCountries) | `sip_connected_audio:read:callout_countries:master`, `sip_connected_audio:read:callout_countries:admin` |
| [List internal numbers](/docs/api/rest/reference/zoom-api/ma/#operation/ListInternalNumbers) | `sip_connected_audio:read:internal_numbers:master`, `sip_connected_audio:read:internal_numbers:admin` |
| [Add internal call-out countries](/docs/api/rest/reference/zoom-api/ma/#operation/AddInternalCall-outCountries) | `sip_connected_audio:write:callout_countries:admin`, `sip_connected_audio:write:callout_countries:master` |
| [Assign SIP trunk configuration](/docs/api/rest/reference/zoom-api/ma/#operation/AssignSIPTrunkConfiguration) | `sip_connected_audio:update:settings:master`, `sip_connected_audio:update:settings:admin` |
| [Add internal numbers](/docs/api/rest/reference/zoom-api/ma/#operation/AddInternalNumbers) | `sip_connected_audio:write:internal_numbers:admin`, `sip_connected_audio:write:internal_numbers:master` |
| [Get SIP trunk configuration](/docs/api/rest/reference/zoom-api/ma/#operation/GetSIPTrunkConfiguration) | `sip_connected_audio:read:settings:master`, `sip_connected_audio:read:settings:admin` |
| [List SIP trunks](/docs/api/rest/reference/zoom-api/ma/#operation/ListSIPTrunks) | `sip_connected_audio:read:trunks:master`, `sip_connected_audio:read:trunks:admin` |
| [Assign SIP trunks](/docs/api/rest/reference/zoom-api/ma/#operation/AssignSIPTrunks) | `sip_connected_audio:write:trunks:master` |
| [Delete a SIP trunk](/docs/api/rest/reference/zoom-api/ma/#operation/DeleteASIPTrunk) | `sip_connected_audio:delete:trunks:master` |
| [Delete all numbers](/docs/api/rest/reference/zoom-api/ma/#operation/DeleteAllNumbers) | `sip_connected_audio:delete:numbers:master` |
| [Assign numbers](/docs/api/rest/reference/zoom-api/ma/#operation/AssignNumbers) | `sip_connected_audio:write:numbers:master` |
| [Delete an internal number](/docs/api/rest/reference/zoom-api/ma/#operation/DeleteAnInternalNumber) | `sip_connected_audio:delete:internal_numbers:admin`, `sip_connected_audio:delete:internal_numbers:master` |
| [List SIP trunk numbers](/docs/api/rest/reference/zoom-api/ma/#operation/listSipTrunkNumbers) | `sip_connected_audio:read:numbers:master` |
| [Update an internal number](/docs/api/rest/reference/zoom-api/ma/#operation/UpdateAnInternalNumber) | `sip_connected_audio:update:internal_numbers:master`, `sip_connected_audio:update:internal_numbers:admin` |
| [Delete internal call-out country](/docs/api/rest/reference/zoom-api/ma/#operation/DeleteInternalCall-outCountry) | `sip_connected_audio:delete:callout_countries:master`, `sip_connected_audio:delete:callout_countries:admin` |

### SIP Phone

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Enable SIP phone](/docs/api/rest/reference/zoom-api/methods/#operation/EnableSIPPhonePhones) | `sip_phone:write:sip_phone:admin` |
| [Enable SIP phone](/docs/api/rest/reference/zoom-api/ma/#operation/EnableSIPPhonePhones) | `sip_phone:write:sip_phone:master` |
| [Update SIP phone](/docs/api/rest/reference/zoom-api/methods/#operation/UpdateSIPPhonePhones) | `sip_phone:update:sip_phone:admin` |
| [Update SIP phone](/docs/api/rest/reference/zoom-api/ma/#operation/UpdateSIPPhonePhones) | `sip_phone:update:sip_phone:master` |
| [List SIP phones](/docs/api/rest/reference/zoom-api/methods/#operation/ListSIPPhonePhones) | `sip_phone:read:list_sip_phones:admin` |
| [List SIP phones](/docs/api/rest/reference/zoom-api/ma/#operation/ListSIPPhonePhones) | `sip_phone:read:list_sip_phones:master` |
| [Delete SIP phone](/docs/api/rest/reference/zoom-api/methods/#operation/deleteSIPPhonePhones) | `sip_phone:delete:sip_phone:admin` |
| [Delete SIP phone](/docs/api/rest/reference/zoom-api/ma/#operation/deleteSIPPhonePhones) | `sip_phone:delete:sip_phone:master` |

### Summaries

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List an account's meeting or webinar summaries](/docs/api/rest/reference/zoom-api/methods/#operation/Listmeetingsummaries) | `meeting:read:list_summaries:admin` |
| [List an account's meeting or webinar summaries](/docs/api/rest/reference/zoom-api/ma/#operation/Listmeetingsummaries) | `meeting:read:list_summaries:master` |
| [Delete a meeting or webinar summary](/docs/api/rest/reference/zoom-api/methods/#operation/Deletemeetingorwebinarsummary) | `meeting:delete:summary`, `meeting:delete:summary:admin` |
| [Delete a meeting or webinar summary](/docs/api/rest/reference/zoom-api/ma/#operation/Deletemeetingorwebinarsummary) | `meeting:delete:summary:master` |
| [Get a meeting or webinar summary](/docs/api/rest/reference/zoom-api/methods/#operation/Getameetingsummary) | `meeting:read:summary`, `meeting:read:summary:admin` |
| [Get a meeting or webinar summary](/docs/api/rest/reference/zoom-api/ma/#operation/Getameetingsummary) | `meeting:read:summary:master` |

### Surveys

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update a meeting survey](/docs/api/rest/reference/zoom-api/methods/#operation/meetingSurveyUpdate) | `meeting:update:survey`, `meeting:update:survey:admin` |
| [Update a meeting survey](/docs/api/rest/reference/zoom-api/ma/#operation/meetingSurveyUpdate) | `meeting:update:survey:master` |
| [Get a meeting survey](/docs/api/rest/reference/zoom-api/methods/#operation/meetingSurveyGet) | `meeting:read:survey`, `meeting:read:survey:admin` |
| [Get a meeting survey](/docs/api/rest/reference/zoom-api/ma/#operation/meetingSurveyGet) | `meeting:read:survey:master` |
| [Delete a meeting survey](/docs/api/rest/reference/zoom-api/methods/#operation/meetingSurveyDelete) | `meeting:delete:survey`, `meeting:delete:survey:admin` |
| [Delete a meeting survey](/docs/api/rest/reference/zoom-api/ma/#operation/meetingSurveyDelete) | `meeting:delete:survey:master` |

### TSP

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Add a user's TSP account](/docs/api/rest/reference/zoom-api/methods/#operation/userTSPCreate) | `tsp:write:tsp_account`, `tsp:write:tsp_account:admin` |
| [Add a user's TSP account](/docs/api/rest/reference/zoom-api/ma/#operation/userTSPCreate) | `tsp:write:tsp_account:master` |
| [Get account's TSP information](/docs/api/rest/reference/zoom-api/methods/#operation/tsp) | `tsp:read:tsp:admin` |
| [Get account's TSP information](/docs/api/rest/reference/zoom-api/ma/#operation/tsp) | `tsp:read:tsp:master` |
| [Update a TSP account](/docs/api/rest/reference/zoom-api/methods/#operation/userTSPUpdate) | `tsp:update:tsp_account`, `tsp:update:tsp_account:admin` |
| [Update a TSP account](/docs/api/rest/reference/zoom-api/ma/#operation/userTSPUpdate) | `tsp:update:tsp_account:master` |
| [Delete a user's TSP account](/docs/api/rest/reference/zoom-api/methods/#operation/userTSPDelete) | `tsp:delete:tsp_account`, `tsp:delete:tsp_account:admin` |
| [Delete a user's TSP account](/docs/api/rest/reference/zoom-api/ma/#operation/userTSPDelete) | `tsp:delete:tsp_account:master` |
| [Set global dial-in URL for a TSP user](/docs/api/rest/reference/zoom-api/methods/#operation/tspUrlUpdate) | `tsp:update:tsp_settings`, `tsp:update:tsp_settings:admin` |
| [Set global dial-in URL for a TSP user](/docs/api/rest/reference/zoom-api/ma/#operation/tspUrlUpdate) | `tsp:update:tsp_settings:master` |
| [Get a user's TSP account](/docs/api/rest/reference/zoom-api/methods/#operation/userTSP) | `tsp:read:tsp_account`, `tsp:read:tsp_account:admin` |
| [Get a user's TSP account](/docs/api/rest/reference/zoom-api/ma/#operation/userTSP) | `tsp:read:tsp_account:master` |
| [Update an account's TSP information](/docs/api/rest/reference/zoom-api/methods/#operation/tspUpdate) | `tsp:update:tsp:admin` |
| [Update an account's TSP information](/docs/api/rest/reference/zoom-api/ma/#operation/tspUpdate) | `tsp:update:tsp:master` |
| [List user's TSP accounts](/docs/api/rest/reference/zoom-api/methods/#operation/userTSPs) | `tsp:read:list_tsp_accounts`, `tsp:read:list_tsp_accounts:admin` |
| [List user's TSP accounts](/docs/api/rest/reference/zoom-api/ma/#operation/userTSPs) | `tsp:read:list_tsp_accounts:master` |

### Templates

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List meeting templates](/docs/api/rest/reference/zoom-api/methods/#operation/listMeetingTemplates) | `meeting:read:list_templates`, `meeting:read:list_templates:admin` |
| [List meeting templates](/docs/api/rest/reference/zoom-api/ma/#operation/listMeetingTemplates) | `meeting:read:list_templates:master` |
| [Create a meeting template from an existing meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meetingTemplateCreate) | `meeting:write:template`, `meeting:write:template:admin` |
| [Create a meeting template from an existing meeting](/docs/api/rest/reference/zoom-api/ma/#operation/meetingTemplateCreate) | `meeting:write:template:master` |

### Tracking Field

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a tracking field](/docs/api/rest/reference/zoom-api/methods/#operation/trackingfieldGet) | `tracking_field:read:tracking_field:admin` |
| [Get a tracking field](/docs/api/rest/reference/zoom-api/ma/#operation/trackingfieldGet) | `tracking_field:read:tracking_field:master` |
| [Delete a tracking field](/docs/api/rest/reference/zoom-api/methods/#operation/trackingfieldDelete) | `tracking_field:delete:tracking_field:admin` |
| [Delete a tracking field](/docs/api/rest/reference/zoom-api/ma/#operation/trackingfieldDelete) | `tracking_field:delete:tracking_field:master` |
| [List tracking fields](/docs/api/rest/reference/zoom-api/methods/#operation/trackingfieldList) | `tracking_field:read:list_tracking_fields:admin` |
| [List tracking fields](/docs/api/rest/reference/zoom-api/ma/#operation/trackingfieldList) | `tracking_field:read:list_tracking_fields:master` |
| [Create a tracking field](/docs/api/rest/reference/zoom-api/methods/#operation/trackingfieldCreate) | `tracking_field:write:tracking_field:admin` |
| [Create a tracking field](/docs/api/rest/reference/zoom-api/ma/#operation/trackingfieldCreate) | `tracking_field:write:tracking_field:master` |
| [Update a tracking field](/docs/api/rest/reference/zoom-api/methods/#operation/trackingfieldUpdate) | `tracking_field:update:tracking_field:admin` |
| [Update a tracking field](/docs/api/rest/reference/zoom-api/ma/#operation/trackingfieldUpdate) | `tracking_field:update:tracking_field:master` |

### Webinars

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete a webinar](/docs/api/rest/reference/zoom-api/methods/#operation/webinarDelete) | `webinar:delete:webinar`, `webinar:delete:webinar:admin` |
| [Delete a webinar](/docs/api/rest/reference/zoom-api/ma/#operation/webinarDelete) | `webinar:delete:webinar:master` |
| [List registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantsQuestionsGet) | `webinar:read:list_registration_questions`, `webinar:read:list_registration_questions:admin` |
| [List registration questions](/docs/api/rest/reference/zoom-api/ma/#operation/webinarRegistrantsQuestionsGet) | `webinar:read:list_registration_questions:master` |
| [Get a webinar's join token for local recording](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLocalRecordingJoinToken) | `webinar:read:local_recording_token`, `webinar:read:local_recording_token:admin` |
| [Create a webinar's poll](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPollCreate) | `webinar:write:poll`, `webinar:write:poll:admin` |
| [Create a webinar's poll](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPollCreate) | `webinar:write:poll:master` |
| [Upload a webinar's branding virtual background](/docs/api/rest/reference/zoom-api/methods/#operation/uploadWebinarBrandingVB) | `webinar:write:branding_virtual_background`, `webinar:write:branding_virtual_background:admin` |
| [Upload a webinar's branding virtual background](/docs/api/rest/reference/zoom-api/ma/#operation/uploadWebinarBrandingVB) | `webinar:write:branding_virtual_background:master` |
| [List a webinar's polls](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPolls) | `webinar:read:list_polls`, `webinar:read:list_polls:admin` |
| [List a webinar's polls](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPolls) | `webinar:read:list_polls:master` |
| [Update registrant's status](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantStatus) | `webinar:update:registrant_status`, `webinar:update:registrant_status:admin` |
| [Update registrant's status](/docs/api/rest/reference/zoom-api/ma/#operation/webinarRegistrantStatus) | `webinar:update:registrant_status:master` |
| [Update a live stream](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLiveStreamUpdate) | `webinar:update:livestream`, `webinar:update:livestream:admin` |
| [Update a live stream](/docs/api/rest/reference/zoom-api/ma/#operation/webinarLiveStreamUpdate) | `webinar:update:livestream:master` |
| [Remove all panelists](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelistsDelete) | `webinar:delete:panelist`, `webinar:delete:panelist:admin` |
| [Remove all panelists](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPanelistsDelete) | `webinar:delete:panelist:master` |
| [Update registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantQuestionUpdate) | `webinar:update:registration_question`, `webinar:update:registration_question:admin` |
| [Update registration questions](/docs/api/rest/reference/zoom-api/ma/#operation/webinarRegistrantQuestionUpdate) | `webinar:update:registration_question:master` |
| [Delete a webinar survey](/docs/api/rest/reference/zoom-api/methods/#operation/webinarSurveyDelete) | `webinar:delete:survey`, `webinar:delete:survey:admin` |
| [Delete a webinar survey](/docs/api/rest/reference/zoom-api/ma/#operation/webinarSurveyDelete) | `webinar:delete:survey:master` |
| [Create a webinar template](/docs/api/rest/reference/zoom-api/methods/#operation/webinarTemplateCreate) | `webinar:write:template`, `webinar:write:template:admin` |
| [Create a webinar template](/docs/api/rest/reference/zoom-api/ma/#operation/webinarTemplateCreate) | `webinar:write:template:master` |
| [List webinar templates](/docs/api/rest/reference/zoom-api/methods/#operation/listWebinarTemplates) | `webinar:read:list_templates`, `webinar:read:list_templates:admin` |
| [List webinar templates](/docs/api/rest/reference/zoom-api/ma/#operation/listWebinarTemplates) | `webinar:read:list_templates:master` |
| [Get a webinar](/docs/api/rest/reference/zoom-api/methods/#operation/webinar) | `webinar:read:webinar`, `webinar:read:webinar:admin` |
| [Get a webinar](/docs/api/rest/reference/zoom-api/ma/#operation/webinar) | `webinar:read:webinar:master` |
| [Get live stream details](/docs/api/rest/reference/zoom-api/methods/#operation/getWebinarLiveStreamDetails) | `webinar:read:livestream`, `webinar:read:livestream:admin` |
| [Get live stream details](/docs/api/rest/reference/zoom-api/ma/#operation/getWebinarLiveStreamDetails) | `webinar:read:livestream:master` |
| [Upload a webinar's branding wallpaper](/docs/api/rest/reference/zoom-api/methods/#operation/uploadWebinarBrandingWallpaper) | `webinar:write:branding_wallpaper`, `webinar:write:branding_wallpaper:admin` |
| [Upload a webinar's branding wallpaper](/docs/api/rest/reference/zoom-api/ma/#operation/uploadWebinarBrandingWallpaper) | `webinar:write:branding_wallpaper:master` |
| [Get a webinar poll](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPollGet) | `webinar:read:poll`, `webinar:read:poll:admin` |
| [Get a webinar poll](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPollGet) | `webinar:read:poll:master` |
| [Get a webinar survey](/docs/api/rest/reference/zoom-api/methods/#operation/webinarSurveyGet) | `webinar:read:survey`, `webinar:read:survey:admin` |
| [Get a webinar survey](/docs/api/rest/reference/zoom-api/ma/#operation/webinarSurveyGet) | `webinar:read:survey:master` |
| [Update a webinar poll](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPollUpdate) | `webinar:update:poll`, `webinar:update:poll:admin` |
| [Update a webinar poll](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPollUpdate) | `webinar:update:poll:master` |
| [List past webinar poll results](/docs/api/rest/reference/zoom-api/methods/#operation/listPastWebinarPollResults) | `webinar:read:list_past_polls`, `webinar:read:list_past_polls:admin` |
| [Get a webinar's archive token for local archiving](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLocalArchivingArchiveToken) | `webinar:read:local_archiving_token:admin` |
| [Create a webinar](/docs/api/rest/reference/zoom-api/methods/#operation/webinarCreate) | `webinar:write:webinar`, `webinar:write:webinar:admin` |
| [Create a webinar](/docs/api/rest/reference/zoom-api/ma/#operation/webinarCreate) | `webinar:write:webinar:master` |
| [List webinars](/docs/api/rest/reference/zoom-api/methods/#operation/webinars) | `webinar:read:list_webinars`, `webinar:read:list_webinars:admin` |
| [List webinars](/docs/api/rest/reference/zoom-api/ma/#operation/webinars) | `webinar:read:list_webinars:master` |
| [Set webinar's default branding virtual background](/docs/api/rest/reference/zoom-api/methods/#operation/setWebinarBrandingVB) | `webinar:update:branding_virtual_background`, `webinar:update:branding_virtual_background:admin` |
| [Set webinar's default branding virtual background](/docs/api/rest/reference/zoom-api/ma/#operation/setWebinarBrandingVB) | `webinar:update:branding_virtual_background:master` |
| [Get webinar's session branding](/docs/api/rest/reference/zoom-api/methods/#operation/getWebinarBranding) | `webinar:read:branding`, `webinar:read:branding:admin` |
| [Get webinar's session branding](/docs/api/rest/reference/zoom-api/ma/#operation/getWebinarBranding) | `webinar:read:branding:master` |
| [Get a webinar's join token for live streaming](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLiveStreamingJoinToken) | `webinar:read:live_streaming_token`, `webinar:read:live_streaming_token:admin` |
| [Delete a webinar's branding wallpaper](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarBrandingWallpaper) | `webinar:delete:branding_wallpaper`, `webinar:delete:branding_wallpaper:admin` |
| [Delete a webinar's branding wallpaper](/docs/api/rest/reference/zoom-api/ma/#operation/deleteWebinarBrandingWallpaper) | `webinar:delete:branding_wallpaper:master` |
| [Get a webinar SIP URI with passcode](/docs/api/rest/reference/zoom-api/methods/#operation/getWebinarSipDialingWithPasscode) | `webinar:write:sip_dialing`, `webinar:write:sip_dialing:admin` |
| [Perform batch registration](/docs/api/rest/reference/zoom-api/methods/#operation/addBatchWebinarRegistrants) | `webinar:write:batch_registrants`, `webinar:write:batch_registrants:admin` |
| [Perform batch registration](/docs/api/rest/reference/zoom-api/ma/#operation/addBatchWebinarRegistrants) | `webinar:write:batch_registrants:master` |
| [Update a webinar](/docs/api/rest/reference/zoom-api/methods/#operation/webinarUpdate) | `webinar:update:webinar`, `webinar:update:webinar:admin` |
| [Update a webinar](/docs/api/rest/reference/zoom-api/ma/#operation/webinarUpdate) | `webinar:update:webinar:master` |
| [Update webinar status](/docs/api/rest/reference/zoom-api/methods/#operation/webinarStatus) | `webinar:update:status`, `webinar:update:status:admin` |
| [Update webinar status](/docs/api/rest/reference/zoom-api/ma/#operation/webinarStatus) | `webinar:update:status:master` |
| [Delete a webinar's branding virtual backgrounds](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarBrandingVB) | `webinar:delete:branding_virtual_background`, `webinar:delete:branding_virtual_background:admin` |
| [Delete a webinar's branding virtual backgrounds](/docs/api/rest/reference/zoom-api/ma/#operation/deleteWebinarBrandingVB) | `webinar:delete:branding_virtual_background:master` |
| [List panelists](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelists) | `webinar:read:list_panelists`, `webinar:read:list_panelists:admin` |
| [List panelists](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPanelists) | `webinar:read:list_panelists:master` |
| [Get webinar absentees](/docs/api/rest/reference/zoom-api/methods/#operation/webinarAbsentees) | `webinar:read:list_absentees`, `webinar:read:list_absentees:admin` |
| [Get webinar absentees](/docs/api/rest/reference/zoom-api/ma/#operation/webinarAbsentees) | `webinar:read:list_absentees:master` |
| [Add a webinar registrant](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantCreate) | `webinar:write:registrant`, `webinar:write:registrant:admin` |
| [Add a webinar registrant](/docs/api/rest/reference/zoom-api/ma/#operation/webinarRegistrantCreate) | `webinar:write:registrant:master` |
| [Get webinar tracking sources](/docs/api/rest/reference/zoom-api/methods/#operation/getTrackingSources) | `webinar:read:list_tracking_sources`, `webinar:read:list_tracking_sources:admin` |
| [Get webinar tracking sources](/docs/api/rest/reference/zoom-api/ma/#operation/getTrackingSources) | `webinar:read:list_tracking_sources:master` |
| [Delete a webinar poll](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPollDelete) | `webinar:delete:poll`, `webinar:delete:poll:admin` |
| [Delete a webinar poll](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPollDelete) | `webinar:delete:poll:master` |
| [Get webinar's token](/docs/api/rest/reference/zoom-api/methods/#operation/webinarToken) | `webinar:read:token`, `webinar:read:token:admin` |
| [Get webinar's token](/docs/api/rest/reference/zoom-api/ma/#operation/webinarToken) | `webinar:read:token:master` |
| [Get a webinar registrant](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantGet) | `webinar:read:registrant`, `webinar:read:registrant:admin` |
| [Get a webinar registrant](/docs/api/rest/reference/zoom-api/ma/#operation/webinarRegistrantGet) | `webinar:read:registrant:master` |
| [Remove a panelist](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelistDelete) | `webinar:delete:panelist`, `webinar:delete:panelist:admin` |
| [Remove a panelist](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPanelistDelete) | `webinar:delete:panelist:master` |
| [Delete a webinar's branding name tag](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarBrandingNameTag) | `webinar:delete:branding_name_tag`, `webinar:delete:branding_name_tag:admin` |
| [Delete a webinar's branding name tag](/docs/api/rest/reference/zoom-api/ma/#operation/deleteWebinarBrandingNameTag) | `webinar:delete:branding_name_tag:master` |
| [Update a webinar's branding name tag](/docs/api/rest/reference/zoom-api/methods/#operation/updateWebinarBrandingNameTag) | `webinar:update:branding_name_tag`, `webinar:update:branding_name_tag:admin` |
| [Update a webinar's branding name tag](/docs/api/rest/reference/zoom-api/ma/#operation/updateWebinarBrandingNameTag) | `webinar:update:branding_name_tag:master` |
| [List Q&As of a past webinar](/docs/api/rest/reference/zoom-api/methods/#operation/listPastWebinarQA) | `webinar:read:past_qa`, `webinar:read:past_qa:admin` |
| [Add panelists](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelistCreate) | `webinar:write:panelist`, `webinar:write:panelist:admin` |
| [Add panelists](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPanelistCreate) | `webinar:write:panelist:master` |
| [List past webinar instances](/docs/api/rest/reference/zoom-api/methods/#operation/pastWebinars) | `webinar:read:list_past_instances`, `webinar:read:list_past_instances:admin` |
| [List past webinar instances](/docs/api/rest/reference/zoom-api/ma/#operation/pastWebinars) | `webinar:read:list_past_instances:master` |
| [Create webinar's invite links](/docs/api/rest/reference/zoom-api/methods/#operation/webinarInviteLinksCreate) | `webinar:write:invite_links`, `webinar:write:invite_links:admin` |
| [Create webinar's invite links](/docs/api/rest/reference/zoom-api/ma/#operation/webinarInviteLinksCreate) | `webinar:write:invite_links:master` |
| [Update live stream status](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLiveStreamStatusUpdate) | `webinar:update:livestream_status`, `webinar:update:livestream_status:admin` |
| [Update live stream status](/docs/api/rest/reference/zoom-api/ma/#operation/webinarLiveStreamStatusUpdate) | `webinar:update:livestream_status:master` |
| [Update a webinar survey](/docs/api/rest/reference/zoom-api/methods/#operation/webinarSurveyUpdate) | `webinar:update:survey`, `webinar:update:survey:admin` |
| [Update a webinar survey](/docs/api/rest/reference/zoom-api/ma/#operation/webinarSurveyUpdate) | `webinar:update:survey:master` |
| [Delete a webinar registrant](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarRegistrant) | `webinar:delete:registrant`, `webinar:delete:registrant:admin` |
| [Delete a webinar registrant](/docs/api/rest/reference/zoom-api/ma/#operation/deleteWebinarRegistrant) | `webinar:delete:registrant:master` |
| [List webinar participants](/docs/api/rest/reference/zoom-api/methods/#operation/listWebinarParticipants) | `webinar:read:list_past_participants:admin`, `webinar:read:list_past_participants` |
| [Create a webinar's branding name tag](/docs/api/rest/reference/zoom-api/methods/#operation/createWebinarBrandingNameTag) | `webinar:write:branding_name_tag`, `webinar:write:branding_name_tag:admin` |
| [Create a webinar's branding name tag](/docs/api/rest/reference/zoom-api/ma/#operation/createWebinarBrandingNameTag) | `webinar:write:branding_name_tag:master` |
| [List webinar registrants](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrants) | `webinar:read:list_registrants`, `webinar:read:list_registrants:admin` |
| [List webinar registrants](/docs/api/rest/reference/zoom-api/ma/#operation/webinarRegistrants) | `webinar:read:list_registrants:master` |
| [Delete a live webinar message](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarChatMessageById) | `webinar:delete:live_webinar_chat_message`, `webinar:delete:live_webinar_chat_message:admin` |

## Zoom Phone


### Accounts

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete phone numbers for an account's customized outbound caller ID](/docs/api/rest/reference/phone/methods/#operation/deleteOutboundCallerNumbers) | `phone:delete:customized_number:admin` |
| [Delete phone numbers for an account's customized outbound caller ID](/docs/api/rest/reference/phone/ma/#operation/deleteOutboundCallerNumbers) | `phone:delete:customized_number:master` |
| [Add phone numbers for an account's customized outbound caller ID](/docs/api/rest/reference/phone/methods/#operation/addOutboundCallerNumbers) | `phone:write:customized_number:admin` |
| [Add phone numbers for an account's customized outbound caller ID](/docs/api/rest/reference/phone/ma/#operation/addOutboundCallerNumbers) | `phone:write:customized_number:master` |
| [List an account's customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/methods/#operation/listCustomizeOutboundCallerNumbers) | `phone:read:list_customized_number:admin` |
| [List an account's customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/ma/#operation/listCustomizeOutboundCallerNumbers) | `phone:read:list_customized_number:master` |
| [List an account's Zoom Phone settings](/docs/api/rest/reference/phone/methods/#operation/listZoomPhoneAccountSettings) | `phone:read:list_account_settings:admin` |
| [List an account's Zoom Phone settings](/docs/api/rest/reference/phone/ma/#operation/listZoomPhoneAccountSettings) | `phone:read:list_account_settings:master` |

### Alerts

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete an alert setting](/docs/api/rest/reference/phone/methods/#operation/DeleteAnAlertSetting) | `phone:delete:alert_setting:admin` |
| [Delete an alert setting](/docs/api/rest/reference/phone/ma/#operation/DeleteAnAlertSetting) | `phone:delete:alert_setting:master` |
| [Get alert setting details](/docs/api/rest/reference/phone/methods/#operation/GetAlertSettingDetails) | `phone:read:alert_setting:admin` |
| [Get alert setting details](/docs/api/rest/reference/phone/ma/#operation/GetAlertSettingDetails) | `phone:read:alert_setting:master` |
| [List alert settings with paging query](/docs/api/rest/reference/phone/methods/#operation/ListAlertSettingsWithPagingQuery) | `phone:read:list_alert_settings:admin` |
| [List alert settings with paging query](/docs/api/rest/reference/phone/ma/#operation/ListAlertSettingsWithPagingQuery) | `phone:read:list_alert_settings:master` |
| [Add an alert setting](/docs/api/rest/reference/phone/methods/#operation/AddAnAlertSetting) | `phone:write:alert_setting:admin` |
| [Add an alert setting](/docs/api/rest/reference/phone/ma/#operation/AddAnAlertSetting) | `phone:write:alert_setting:master` |
| [Update an alert setting](/docs/api/rest/reference/phone/methods/#operation/UpdateAnAlertSetting) | `phone:patch:alert_setting:admin` |
| [Update an alert setting](/docs/api/rest/reference/phone/ma/#operation/UpdateAnAlertSetting) | `phone:patch:alert_setting:master` |

### Audio Library

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete an audio item](/docs/api/rest/reference/phone/methods/#operation/DeleteAudioItem) | `phone:delete:audio`, `phone:delete:audio:admin` |
| [Delete an audio item](/docs/api/rest/reference/phone/ma/#operation/DeleteAudioItem) | `phone:delete:audio:master` |
| [Add audio items](/docs/api/rest/reference/phone/methods/#operation/AddAudioItem) | `phone:write:batch_audios`, `phone:write:batch_audios:admin` |
| [Add audio items](/docs/api/rest/reference/phone/ma/#operation/AddAudioItem) | `phone:write:batch_audios:master` |
| [Update an audio item](/docs/api/rest/reference/phone/methods/#operation/UpdateAudioItem) | `phone:update:audio`, `phone:update:audio:admin` |
| [Update an audio item](/docs/api/rest/reference/phone/ma/#operation/UpdateAudioItem) | `phone:update:audio:master` |
| [Add an audio item for text-to-speech conversion](/docs/api/rest/reference/phone/methods/#operation/AddAnAudio) | `phone:write:audio`, `phone:write:audio:admin` |
| [Add an audio item for text-to-speech conversion](/docs/api/rest/reference/phone/ma/#operation/AddAnAudio) | `phone:write:audio:master` |
| [Get an audio item](/docs/api/rest/reference/phone/methods/#operation/GetAudioItem) | `phone:read:audio`, `phone:read:audio:admin` |
| [Get an audio item](/docs/api/rest/reference/phone/ma/#operation/GetAudioItem) | `phone:read:audio:master` |
| [List audio items](/docs/api/rest/reference/phone/methods/#operation/ListAudioItems) | `phone:read:list_audios`, `phone:read:list_audios:admin` |
| [List audio items](/docs/api/rest/reference/phone/ma/#operation/ListAudioItems) | `phone:read:list_audios:master` |

### Auto Receptionists

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete a non-primary auto receptionist](/docs/api/rest/reference/phone/methods/#operation/deleteAutoReceptionist) | `phone:delete:auto_receptionist:admin` |
| [Delete a non-primary auto receptionist](/docs/api/rest/reference/phone/ma/#operation/deleteAutoReceptionist) | `phone:delete:auto_receptionist:master` |
| [Unassign all phone numbers](/docs/api/rest/reference/phone/methods/#operation/unassignAllPhoneNumsAutoReceptionist) | `phone:delete:auto_receptionist_number:admin` |
| [Unassign all phone numbers](/docs/api/rest/reference/phone/ma/#operation/unassignAllPhoneNumsAutoReceptionist) | `phone:delete:auto_receptionist_number:master` |
| [Get an auto receptionist](/docs/api/rest/reference/phone/methods/#operation/getAutoReceptionistDetail) | `phone:read:auto_receptionist:admin` |
| [Get an auto receptionist](/docs/api/rest/reference/phone/ma/#operation/getAutoReceptionistDetail) | `phone:read:auto_receptionist:master` |
| [Unassign a phone number](/docs/api/rest/reference/phone/methods/#operation/unassignAPhoneNumAutoReceptionist) | `phone:delete:auto_receptionist_number:admin` |
| [Unassign a phone number](/docs/api/rest/reference/phone/ma/#operation/unassignAPhoneNumAutoReceptionist) | `phone:delete:auto_receptionist_number:master` |
| [Update an auto receptionist policy](/docs/api/rest/reference/phone/methods/#operation/updateAutoReceptionistPolicy) | `phone:update:auto_receptionist_policy:admin` |
| [Update an auto receptionist policy](/docs/api/rest/reference/phone/ma/#operation/updateAutoReceptionistPolicy) | `phone:update:auto_receptionist_policy:master` |
| [Update an auto receptionist](/docs/api/rest/reference/phone/methods/#operation/updateAutoReceptionist) | `phone:update:auto_receptionist:admin` |
| [Update an auto receptionist](/docs/api/rest/reference/phone/ma/#operation/updateAutoReceptionist) | `phone:update:auto_receptionist:master` |
| [Add a policy subsetting](/docs/api/rest/reference/phone/methods/#operation/AddPolicy) | `phone:write:auto_receptionist_policy:admin` |
| [Add a policy subsetting](/docs/api/rest/reference/phone/ma/#operation/AddPolicy) | `phone:write:auto_receptionist_policy:master` |
| [List auto receptionists](/docs/api/rest/reference/phone/methods/#operation/listAutoReceptionists) | `phone:read:list_auto_receptionists:admin` |
| [List auto receptionists](/docs/api/rest/reference/phone/ma/#operation/listAutoReceptionists) | `phone:read:list_auto_receptionists:master` |
| [Add an auto receptionist](/docs/api/rest/reference/phone/methods/#operation/addAutoReceptionist) | `phone:write:auto_receptionist:admin` |
| [Add an auto receptionist](/docs/api/rest/reference/phone/ma/#operation/addAutoReceptionist) | `phone:write:auto_receptionist:master` |
| [Delete a policy subsetting](/docs/api/rest/reference/phone/methods/#operation/DeletePolicy) | `phone:delete:auto_receptionist_policy:admin` |
| [Delete a policy subsetting](/docs/api/rest/reference/phone/ma/#operation/DeletePolicy) | `phone:delete:auto_receptionist_policy:master` |
| [Assign phone numbers](/docs/api/rest/reference/phone/methods/#operation/assignPhoneNumbersAutoReceptionist) | `phone:write:auto_receptionist_number:admin` |
| [Assign phone numbers](/docs/api/rest/reference/phone/ma/#operation/assignPhoneNumbersAutoReceptionist) | `phone:write:auto_receptionist_number:master` |
| [Get an auto receptionist policy](/docs/api/rest/reference/phone/methods/#operation/getAutoReceptionistsPolicy) | `phone:read:auto_receptionist_policy:admin` |
| [Get an auto receptionist policy](/docs/api/rest/reference/phone/ma/#operation/getAutoReceptionistsPolicy) | `phone:read:auto_receptionist_policy:master` |
| [Update a policy subsetting](/docs/api/rest/reference/phone/methods/#operation/updatePolicy) | `phone:update:auto_receptionist_policy:admin` |
| [Update a policy subsetting](/docs/api/rest/reference/phone/ma/#operation/updatePolicy) | `phone:update:auto_receptionist_policy:master` |

### Billing Account

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get billing account details](/docs/api/rest/reference/phone/methods/#operation/GetABillingAccount) | `phone:read:billing_account:admin` |
| [Get billing account details](/docs/api/rest/reference/phone/ma/#operation/GetABillingAccount) | `phone:read:billing_account:master` |
| [List billing accounts](/docs/api/rest/reference/phone/methods/#operation/listBillingAccount) | `phone:read:list_billing_accounts:admin` |
| [List billing accounts](/docs/api/rest/reference/phone/ma/#operation/listBillingAccount) | `phone:read:list_billing_accounts:master` |

### Blocked List

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update a blocked list](/docs/api/rest/reference/phone/methods/#operation/updateBlockedList) | `phone:update:blocked_list:admin` |
| [Update a blocked list](/docs/api/rest/reference/phone/ma/#operation/updateBlockedList) | `phone:update:blocked_list:master` |
| [List blocked lists](/docs/api/rest/reference/phone/methods/#operation/listBlockedList) | `phone:read:list_blocked_lists:admin` |
| [List blocked lists](/docs/api/rest/reference/phone/ma/#operation/listBlockedList) | `phone:read:list_blocked_lists:master` |
| [Create a blocked list](/docs/api/rest/reference/phone/methods/#operation/addAnumberToBlockedList) | `phone:write:blocked_list:admin` |
| [Create a blocked list](/docs/api/rest/reference/phone/ma/#operation/addAnumberToBlockedList) | `phone:write:blocked_list:master` |
| [Get blocked list details](/docs/api/rest/reference/phone/methods/#operation/getABlockedList) | `phone:read:blocked_list:admin` |
| [Get blocked list details](/docs/api/rest/reference/phone/ma/#operation/getABlockedList) | `phone:read:blocked_list:master` |
| [Delete a blocked list](/docs/api/rest/reference/phone/methods/#operation/deleteABlockedList) | `phone:delete:blocked_list:admin` |
| [Delete a blocked list](/docs/api/rest/reference/phone/ma/#operation/deleteABlockedList) | `phone:delete:blocked_list:master` |

### Call Handling

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update a call handling setting](/docs/api/rest/reference/phone/methods/#operation/updateCallHandling) | `phone:update:call_handling_setting:admin` |
| [Update a call handling setting](/docs/api/rest/reference/phone/ma/#operation/updateCallHandling) | `phone:update:call_handling_setting:master` |
| [Add a call handling setting](/docs/api/rest/reference/phone/methods/#operation/addCallHandling) | `phone:write:call_handling_setting:admin` |
| [Add a call handling setting](/docs/api/rest/reference/phone/ma/#operation/addCallHandling) | `phone:write:call_handling_setting:master` |
| [Delete a call handling setting](/docs/api/rest/reference/phone/methods/#operation/deleteCallHandling) | `phone:delete:call_handling_setting:admin` |
| [Delete a call handling setting](/docs/api/rest/reference/phone/ma/#operation/deleteCallHandling) | `phone:delete:call_handling_setting:master` |
| [Get call handling settings](/docs/api/rest/reference/phone/methods/#operation/getCallHandling) | `phone:read:list_call_handling_settings:admin` |
| [Get call handling settings](/docs/api/rest/reference/phone/ma/#operation/getCallHandling) | `phone:read:list_call_handling_settings:master` |

### Call Logs

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get call log details](/docs/api/rest/reference/phone/methods/#operation/getCallLogDetails) | `phone:read:call_log:admin` |
| [Get call log details](/docs/api/rest/reference/phone/ma/#operation/getCallLogDetails) | `phone:read:call_log:master` |
| [Get account's call history](/docs/api/rest/reference/phone/methods/#operation/accountCallHistory) | `phone:read:list_call_logs:admin` |
| [Get account's call history](/docs/api/rest/reference/phone/ma/#operation/accountCallHistory) | `phone:read:list_call_logs:master` |
| [Get call history](/docs/api/rest/reference/phone/methods/#operation/getCallPath) | `phone:read:call_log:admin` |
| [Get call history](/docs/api/rest/reference/phone/ma/#operation/getCallPath) | `phone:read:call_log:master` |
| [Get call history detail](/docs/api/rest/reference/phone/methods/#operation/getCallHistoryDetail) | `phone:read:call_log:admin` |
| [Get call history detail](/docs/api/rest/reference/phone/ma/#operation/getCallHistoryDetail) | `phone:read:call_log:master` |
| [Delete a user's call log](/docs/api/rest/reference/phone/methods/#operation/deleteCallLog) | `phone:delete:call_log`, `phone:delete:call_log:admin` |
| [Delete a user's call log](/docs/api/rest/reference/phone/ma/#operation/deleteCallLog) | `phone:delete:call_log:master` |
| [Get User AI Call Summary Detail](/docs/api/rest/reference/phone/methods/#operation/getUserAICallSummary) | `phone:read:ai_call_summary`, `phone:read:ai_call_summary:admin` |
| [Get User AI Call Summary Detail](/docs/api/rest/reference/phone/ma/#operation/getUserAICallSummary) | `phone:read:ai_call_summary:master` |
| [Get user's call history](/docs/api/rest/reference/phone/methods/#operation/phoneUserCallHistory) | `phone:read:list_call_logs:admin`, `phone:read:list_call_logs` |
| [Get user's call history](/docs/api/rest/reference/phone/ma/#operation/phoneUserCallHistory) | `phone:read:list_call_logs:master` |
| [Delete a user's call history](/docs/api/rest/reference/phone/methods/#operation/deleteUserCallHistory) | `phone:delete:call_log`, `phone:delete:call_log:admin` |
| [Delete a user's call history](/docs/api/rest/reference/phone/ma/#operation/deleteUserCallHistory) | `phone:delete:call_log:master` |
| [Get account's call logs](/docs/api/rest/reference/phone/methods/#operation/accountCallLogs) | `phone:read:list_call_logs:admin` |
| [Get account's call logs](/docs/api/rest/reference/phone/ma/#operation/accountCallLogs) | `phone:read:list_call_logs:master` |
| [Sync user's call history](/docs/api/rest/reference/phone/methods/#operation/syncUserCallHistory) | `phone:read:list_call_logs`, `phone:read:list_call_logs:admin` |
| [Sync user's call history](/docs/api/rest/reference/phone/ma/#operation/syncUserCallHistory) | `phone:read:list_call_logs:master` |
| [Add a client code to a call history](/docs/api/rest/reference/phone/methods/#operation/addClientCodeToCallHistory) | `phone:update:call_log:admin` |
| [Add a client code to a call history](/docs/api/rest/reference/phone/ma/#operation/addClientCodeToCallHistory) | `phone:update:call_log:master` |
| [Sync user's call logs](/docs/api/rest/reference/phone/methods/#operation/syncUserCallLogs) | `phone:read:list_call_logs`, `phone:read:list_call_logs:admin` |
| [Sync user's call logs](/docs/api/rest/reference/phone/ma/#operation/syncUserCallLogs) | `phone:read:list_call_logs:master` |
| [Get user's call logs](/docs/api/rest/reference/phone/methods/#operation/phoneUserCallLogs) | `phone:read:list_call_logs`, `phone:read:list_call_logs:admin` |
| [Get user's call logs](/docs/api/rest/reference/phone/ma/#operation/phoneUserCallLogs) | `phone:read:list_call_logs:master` |
| [Get call element](/docs/api/rest/reference/phone/methods/#operation/getCallElement) | `phone:read:call_log:admin` |
| [Get call element](/docs/api/rest/reference/phone/ma/#operation/getCallElement) | `phone:read:call_log:master` |
| [Add a client code to a call log](/docs/api/rest/reference/phone/methods/#operation/addClientCodeToCallLog) | `phone:update:call_log:admin` |
| [Add a client code to a call log](/docs/api/rest/reference/phone/ma/#operation/addClientCodeToCallLog) | `phone:update:call_log:master` |

### Call Queues

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update a call queue's policy subsetting](/docs/api/rest/reference/phone/methods/#operation/updateCQPolicySubSetting) | `phone:update:call_queue_policy:admin` |
| [Update a call queue's policy subsetting](/docs/api/rest/reference/phone/ma/#operation/updateCQPolicySubSetting) | `phone:update:call_queue_policy:master` |
| [Get call queue recordings](/docs/api/rest/reference/phone/methods/#operation/getCallQueueRecordings) | `phone:read:list_call_queue_recordings:admin` |
| [Get call queue recordings](/docs/api/rest/reference/phone/ma/#operation/getCallQueueRecordings) | `phone:read:list_call_queue_recordings:master` |
| [Assign numbers to a call queue](/docs/api/rest/reference/phone/methods/#operation/assignPhoneToCallQueue) | `phone:write:call_queue_number:admin` |
| [Assign numbers to a call queue](/docs/api/rest/reference/phone/ma/#operation/assignPhoneToCallQueue) | `phone:write:call_queue_number:master` |
| [List call queue members](/docs/api/rest/reference/phone/methods/#operation/listCallQueueMembers) | `phone:read:list_call_queue_members:admin` |
| [List call queue members](/docs/api/rest/reference/phone/ma/#operation/listCallQueueMembers) | `phone:read:list_call_queue_members:master` |
| [Unassign a member](/docs/api/rest/reference/phone/methods/#operation/unassignMemberFromCallQueue) | `phone:delete:call_queue_member:admin` |
| [Unassign a member](/docs/api/rest/reference/phone/ma/#operation/unassignMemberFromCallQueue) | `phone:delete:call_queue_member:master` |
| [List call queues](/docs/api/rest/reference/phone/methods/#operation/listCallQueues) | `phone:read:list_call_queues:admin` |
| [List call queues](/docs/api/rest/reference/phone/ma/#operation/listCallQueues) | `phone:read:list_call_queues:master` |
| [List call queue analytics](/docs/api/rest/reference/phone/methods/#operation/callqueueanalytics) | `phone:read:list_call_queues:admin` |
| [List call queue analytics](/docs/api/rest/reference/phone/ma/#operation/callqueueanalytics) | `phone:read:list_call_queues:master` |
| [Create a call queue](/docs/api/rest/reference/phone/methods/#operation/createCallQueue) | `phone:write:call_queue:admin` |
| [Create a call queue](/docs/api/rest/reference/phone/ma/#operation/createCallQueue) | `phone:write:call_queue:master` |
| [Unassign all members](/docs/api/rest/reference/phone/methods/#operation/unassignAllMembers) | `phone:delete:call_queue_member:admin` |
| [Unassign all members](/docs/api/rest/reference/phone/ma/#operation/unassignAllMembers) | `phone:delete:call_queue_member:master` |
| [Add a policy subsetting to a call queue](/docs/api/rest/reference/phone/methods/#operation/addCQPolicySubSetting) | `phone:write:call_queue_policy:admin` |
| [Add a policy subsetting to a call queue](/docs/api/rest/reference/phone/ma/#operation/addCQPolicySubSetting) | `phone:write:call_queue_policy:master` |
| [Add members to a call queue](/docs/api/rest/reference/phone/methods/#operation/addMembersToCallQueue) | `phone:write:call_queue_member:admin` |
| [Add members to a call queue](/docs/api/rest/reference/phone/ma/#operation/addMembersToCallQueue) | `phone:write:call_queue_member:master` |
| [Delete a call queue](/docs/api/rest/reference/phone/methods/#operation/deleteACallQueue) | `phone:delete:call_queue:admin` |
| [Delete a call queue](/docs/api/rest/reference/phone/ma/#operation/deleteACallQueue) | `phone:delete:call_queue:master` |
| [Unassign a phone number](/docs/api/rest/reference/phone/methods/#operation/unAssignPhoneNumCallQueue) | `phone:delete:call_queue_number:admin` |
| [Unassign a phone number](/docs/api/rest/reference/phone/ma/#operation/unAssignPhoneNumCallQueue) | `phone:delete:call_queue_number:master` |
| [Get call queue details](/docs/api/rest/reference/phone/methods/#operation/getACallQueue) | `phone:read:call_queue:admin` |
| [Get call queue details](/docs/api/rest/reference/phone/ma/#operation/getACallQueue) | `phone:read:call_queue:master` |
| [Update call queue details](/docs/api/rest/reference/phone/methods/#operation/updateCallQueue) | `phone:update:call_queue:admin` |
| [Unassign all phone numbers](/docs/api/rest/reference/phone/methods/#operation/unassignAPhoneNumCallQueue) | `phone:delete:call_queue_number:admin` |
| [Unassign all phone numbers](/docs/api/rest/reference/phone/ma/#operation/unassignAPhoneNumCallQueue) | `phone:delete:call_queue_number:master` |
| [Delete a CQ policy setting](/docs/api/rest/reference/phone/methods/#operation/removeCQPolicySubSetting) | `phone:delete:call_queue_policy:admin` |
| [Delete a CQ policy setting](/docs/api/rest/reference/phone/ma/#operation/removeCQPolicySubSetting) | `phone:delete:call_queue_policy:master` |

### Carrier Reseller

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List phone numbers](/docs/api/rest/reference/phone/methods/#operation/listCRPhoneNumbers) | `phone:read:list_carrier_numbers:admin` |
| [List phone numbers](/docs/api/rest/reference/phone/ma/#operation/listCRPhoneNumbers) | `phone:read:list_carrier_numbers:master` |
| [Delete a phone number](/docs/api/rest/reference/phone/methods/#operation/deleteCRPhoneNumber) | `phone:delete:carrier_number:admin` |
| [Delete a phone number](/docs/api/rest/reference/phone/ma/#operation/deleteCRPhoneNumber) | `phone:delete:carrier_number:master` |
| [Create phone numbers](/docs/api/rest/reference/phone/methods/#operation/createCRPhoneNumbers) | `phone:write:carrier_number:admin` |
| [Create phone numbers](/docs/api/rest/reference/phone/ma/#operation/createCRPhoneNumbers) | `phone:write:carrier_number:master` |
| [Activate phone numbers](/docs/api/rest/reference/phone/methods/#operation/activeCRPhoneNumbers) | `phone:update:carrier_number:admin` |
| [Activate phone numbers](/docs/api/rest/reference/phone/ma/#operation/activeCRPhoneNumbers) | `phone:update:carrier_number:master` |

### Common Areas

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Assign phone numbers to a common area](/docs/api/rest/reference/phone/methods/#operation/assignPhoneNumbersToCommonArea) | `phone:write:common_area_number:admin` |
| [Assign phone numbers to a common area](/docs/api/rest/reference/phone/ma/#operation/assignPhoneNumbersToCommonArea) | `phone:write:common_area_number:master` |
| [Add a common area](/docs/api/rest/reference/phone/methods/#operation/addCommonArea) | `phone:write:common_area:admin` |
| [Add a common area](/docs/api/rest/reference/phone/ma/#operation/addCommonArea) | `phone:write:common_area:master` |
| [Assign calling plans to a common area](/docs/api/rest/reference/phone/methods/#operation/assignCallingPlansToCommonArea) | `phone:write:common_area_calling_plan:admin` |
| [Assign calling plans to a common area](/docs/api/rest/reference/phone/ma/#operation/assignCallingPlansToCommonArea) | `phone:write:common_area_calling_plan:master` |
| [List common areas](/docs/api/rest/reference/phone/methods/#operation/listCommonAreas) | `phone:read:common_area:admin` |
| [List common areas](/docs/api/rest/reference/phone/ma/#operation/listCommonAreas) | `phone:read:common_area:master` |
| [Delete common area setting](/docs/api/rest/reference/phone/methods/#operation/deleteCommonAreaSetting) | `phone:delete:common_area_setting:admin` |
| [Delete common area setting](/docs/api/rest/reference/phone/ma/#operation/deleteCommonAreaSetting) | `phone:delete:common_area_setting:master` |
| [Apply template to common areas](/docs/api/rest/reference/phone/methods/#operation/ApplyTemplatetoCommonAreas) | `phone:write:apply_template_to_common_areas:admin` |
| [Apply template to common areas](/docs/api/rest/reference/phone/ma/#operation/ApplyTemplatetoCommonAreas) | `phone:write:apply_template_to_common_areas:master` |
| [Delete a common area](/docs/api/rest/reference/phone/methods/#operation/deleteCommonArea) | `phone:delete:common_area:admin` |
| [Delete a common area](/docs/api/rest/reference/phone/ma/#operation/deleteCommonArea) | `phone:delete:common_area:master` |
| [Get common area details](/docs/api/rest/reference/phone/methods/#operation/getACommonArea) | `phone:read:common_area:admin` |
| [Get common area details](/docs/api/rest/reference/phone/ma/#operation/getACommonArea) | `phone:read:common_area:master` |
| [Get common area settings](/docs/api/rest/reference/phone/methods/#operation/getCommonAreaSettings) | `phone:read:list_common_area_settings:admin` |
| [Get common area settings](/docs/api/rest/reference/phone/ma/#operation/getCommonAreaSettings) | `phone:read:list_common_area_settings:master` |
| [Unassign a calling plan from the common area](/docs/api/rest/reference/phone/methods/#operation/unassignCallingPlansFromCommonArea) | `phone:delete:common_area_calling_plan:admin` |
| [Unassign a calling plan from the common area](/docs/api/rest/reference/phone/ma/#operation/unassignCallingPlansFromCommonArea) | `phone:delete:common_area_calling_plan:master` |
| [Add common area setting](/docs/api/rest/reference/phone/methods/#operation/AddCommonAreaSetting) | `phone:write:common_area_setting:admin` |
| [Add common area setting](/docs/api/rest/reference/phone/ma/#operation/AddCommonAreaSetting) | `phone:write:common_area_setting:master` |
| [List activation codes](/docs/api/rest/reference/phone/methods/#operation/listActivationCodes) | `phone:read:list_common_area_activation_codes:admin` |
| [List activation codes](/docs/api/rest/reference/phone/ma/#operation/listActivationCodes) | `phone:read:list_common_area_activation_codes:master` |
| [Generate activation codes for common areas](/docs/api/rest/reference/phone/methods/#operation/Generateactivationcodesforcommonareas) | `phone:write:common_area:admin` |
| [Generate activation codes for common areas](/docs/api/rest/reference/phone/ma/#operation/Generateactivationcodesforcommonareas) | `phone:write:common_area:master` |
| [Unassign phone numbers from common area](/docs/api/rest/reference/phone/methods/#operation/unassignPhoneNumbersFromCommonArea) | `phone:delete:common_area_number:admin` |
| [Unassign phone numbers from common area](/docs/api/rest/reference/phone/ma/#operation/unassignPhoneNumbersFromCommonArea) | `phone:delete:common_area_number:master` |
| [Update common area](/docs/api/rest/reference/phone/methods/#operation/updateCommonArea) | `phone:update:common_area:admin` |
| [Update common area](/docs/api/rest/reference/phone/ma/#operation/updateCommonArea) | `phone:update:common_area:master` |
| [Update common area pin code](/docs/api/rest/reference/phone/methods/#operation/UpdateCommonAreaPinCode) | `phone:update:common_area:admin` |
| [Update common area pin code](/docs/api/rest/reference/phone/ma/#operation/UpdateCommonAreaPinCode) | `phone:update:common_area:master` |
| [Update common area setting](/docs/api/rest/reference/phone/methods/#operation/UpdateCommonAreaSetting) | `phone:update:common_area_setting:admin` |
| [Update common area setting](/docs/api/rest/reference/phone/ma/#operation/UpdateCommonAreaSetting) | `phone:update:common_area_setting:master` |

### Dashboard

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List detectable personal location users](/docs/api/rest/reference/phone/methods/#operation/listUserDetectablePersonalLocation) | `phone:read:detectable_personal_location:admin` |
| [List detectable personal location users](/docs/api/rest/reference/phone/ma/#operation/listUserDetectablePersonalLocation) | `phone:read:detectable_personal_location:master` |
| [List real time location for users](/docs/api/rest/reference/phone/methods/#operation/listUserRealtimeLocation) | `phone:read:realtime_location_users:admin` |
| [List real time location for users](/docs/api/rest/reference/phone/ma/#operation/listUserRealtimeLocation) | `phone:read:realtime_location_users:master` |
| [List real time location for IP phones](/docs/api/rest/reference/phone/methods/#operation/listPhoneRealtimelocation) | `phone:read:realtime_location_devices:admin` |
| [List real time location for IP phones](/docs/api/rest/reference/phone/ma/#operation/listPhoneRealtimelocation) | `phone:read:realtime_location_devices:master` |
| [List default emergency address users](/docs/api/rest/reference/phone/methods/#operation/listUserDefaultEmergencyAddress) | `phone:read:default_emergency_address:admin` |
| [List default emergency address users](/docs/api/rest/reference/phone/ma/#operation/listUserDefaultEmergencyAddress) | `phone:read:default_emergency_address:master` |
| [List users permission for location sharing](/docs/api/rest/reference/phone/methods/#operation/listUserLocationSharingPermission) | `phone:read:location_sharing_permission:admin` |
| [List users permission for location sharing](/docs/api/rest/reference/phone/ma/#operation/listUserLocationSharingPermission) | `phone:read:location_sharing_permission:master` |
| [List nomadic emergency services users](/docs/api/rest/reference/phone/methods/#operation/listUserNomadicEmergencyServices) | `phone:read:nomadic_emergency_services:admin` |
| [List nomadic emergency services users](/docs/api/rest/reference/phone/ma/#operation/listUserNomadicEmergencyServices) | `phone:read:nomadic_emergency_services:master` |
| [Get call QoS](/docs/api/rest/reference/phone/methods/#operation/getCallQoS) | `phone:read:call_qos:admin` |
| [Get call QoS](/docs/api/rest/reference/phone/ma/#operation/getCallQoS) | `phone:read:call_qos:master` |
| [Get call details from call log](/docs/api/rest/reference/phone/methods/#operation/getCallLogMetricsDetails) | `phone:read:call_log:admin` |
| [Get call details from call log](/docs/api/rest/reference/phone/ma/#operation/getCallLogMetricsDetails) | `phone:read:call_log:master` |
| [List past call metrics](/docs/api/rest/reference/phone/methods/#operation/listPastCallMetrics) | `phone:read:list_call_logs:admin` |
| [List past call metrics](/docs/api/rest/reference/phone/ma/#operation/listPastCallMetrics) | `phone:read:list_call_logs:master` |
| [List call logs](/docs/api/rest/reference/phone/methods/#operation/listCallLogsMetrics) | `phone:read:list_call_logs:admin` |
| [List call logs](/docs/api/rest/reference/phone/ma/#operation/listCallLogsMetrics) | `phone:read:list_call_logs:master` |
| [List tracked locations](/docs/api/rest/reference/phone/methods/#operation/listTrackedLocations) | `phone:read:list_tracked_locations:admin` |
| [List tracked locations](/docs/api/rest/reference/phone/ma/#operation/listTrackedLocations) | `phone:read:list_tracked_locations:master` |

### Device Line Keys

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get device line keys information](/docs/api/rest/reference/phone/methods/#operation/listDeviceLineKeySetting) | `phone:read:device_line_keys`, `phone:read:device_line_keys:admin` |
| [Get device line keys information](/docs/api/rest/reference/phone/ma/#operation/listDeviceLineKeySetting) | `phone:read:device_line_keys:master` |
| [Batch update device line key position](/docs/api/rest/reference/phone/methods/#operation/batchUpdateDeviceLineKeySetting) | `phone:update:device_line_keys`, `phone:update:device_line_keys:admin` |
| [Batch update device line key position](/docs/api/rest/reference/phone/ma/#operation/batchUpdateDeviceLineKeySetting) | `phone:update:device_line_keys:master` |

### Dial by Name Directory

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete users from a directory](/docs/api/rest/reference/phone/methods/#operation/DeleteUsersFromDirectory) | `phone:delete:directory:admin` |
| [Delete users from a directory](/docs/api/rest/reference/phone/ma/#operation/DeleteUsersFromDirectory) | `phone:delete:directory:master` |
| [Delete users from a directory of a site](/docs/api/rest/reference/phone/methods/#operation/DeleteUsersFromDirectoryBySite) | `phone:delete:directory:admin` |
| [Delete users from a directory of a site](/docs/api/rest/reference/phone/ma/#operation/DeleteUsersFromDirectoryBySite) | `phone:delete:directory:master` |
| [List users in directory](/docs/api/rest/reference/phone/methods/#operation/ListUsersFromDirectory) | `phone:read:directory:admin` |
| [List users in directory](/docs/api/rest/reference/phone/ma/#operation/ListUsersFromDirectory) | `phone:read:directory:master` |
| [List users in a directory by site](/docs/api/rest/reference/phone/methods/#operation/ListUsersFromDirectoryBySite) | `phone:read:directory:admin` |
| [List users in a directory by site](/docs/api/rest/reference/phone/ma/#operation/ListUsersFromDirectoryBySite) | `phone:read:directory:master` |
| [Add users to a directory](/docs/api/rest/reference/phone/methods/#operation/AddUsersToDirectory) | `phone:write:directory:admin` |
| [Add users to a directory](/docs/api/rest/reference/phone/ma/#operation/AddUsersToDirectory) | `phone:write:directory:master` |
| [Add users to a directory of a site](/docs/api/rest/reference/phone/methods/#operation/AddUsersToDirectoryBySite) | `phone:write:directory:admin` |
| [Add users to a directory of a site](/docs/api/rest/reference/phone/ma/#operation/AddUsersToDirectoryBySite) | `phone:write:directory:master` |

### Emergency Addresses

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update an emergency address](/docs/api/rest/reference/phone/methods/#operation/updateEmergencyAddress) | `phone:update:emergency_address:admin` |
| [Update an emergency address](/docs/api/rest/reference/phone/ma/#operation/updateEmergencyAddress) | `phone:update:emergency_address:master` |
| [Delete an emergency address](/docs/api/rest/reference/phone/methods/#operation/deleteEmergencyAddress) | `phone:delete:emergency_address:admin` |
| [Delete an emergency address](/docs/api/rest/reference/phone/ma/#operation/deleteEmergencyAddress) | `phone:delete:emergency_address:master` |
| [List emergency addresses](/docs/api/rest/reference/phone/methods/#operation/listEmergencyAddresses) | `phone:read:list_emergency_addresses:admin` |
| [List emergency addresses](/docs/api/rest/reference/phone/ma/#operation/listEmergencyAddresses) | `phone:read:list_emergency_addresses:master` |
| [Add an emergency address](/docs/api/rest/reference/phone/methods/#operation/addEmergencyAddress) | `phone:write:emergency_address:admin` |
| [Add an emergency address](/docs/api/rest/reference/phone/ma/#operation/addEmergencyAddress) | `phone:write:emergency_address:master` |
| [Get emergency address details](/docs/api/rest/reference/phone/methods/#operation/getEmergencyAddress) | `phone:read:emergency_address:admin` |
| [Get emergency address details](/docs/api/rest/reference/phone/ma/#operation/getEmergencyAddress) | `phone:read:emergency_address:master` |

### Emergency Service Locations

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List emergency service locations](/docs/api/rest/reference/phone/methods/#operation/listLocations) | `phone:read:list_emergency_locations:admin` |
| [List emergency service locations](/docs/api/rest/reference/phone/ma/#operation/listLocations) | `phone:read:list_emergency_locations:master` |
| [Delete an emergency location](/docs/api/rest/reference/phone/methods/#operation/deleteLocation) | `phone:delete:emergency_location:admin` |
| [Delete an emergency location](/docs/api/rest/reference/phone/ma/#operation/deleteLocation) | `phone:delete:emergency_location:master` |
| [Batch add emergency service locations](/docs/api/rest/reference/phone/methods/#operation/batchAddLocations) | `phone:write:batch_emergency_locations:admin` |
| [Batch add emergency service locations](/docs/api/rest/reference/phone/ma/#operation/batchAddLocations) | `phone:write:batch_emergency_locations:master` |
| [Update emergency service location](/docs/api/rest/reference/phone/methods/#operation/updateLocation) | `phone:update:emergency_location:admin` |
| [Update emergency service location](/docs/api/rest/reference/phone/ma/#operation/updateLocation) | `phone:update:emergency_location:master` |
| [Add an emergency service location](/docs/api/rest/reference/phone/methods/#operation/addLocation) | `phone:write:emergency_location:admin` |
| [Add an emergency service location](/docs/api/rest/reference/phone/ma/#operation/addLocation) | `phone:write:emergency_location:master` |
| [Get emergency service location details](/docs/api/rest/reference/phone/methods/#operation/getLocation) | `phone:read:emergency_location:admin` |
| [Get emergency service location details](/docs/api/rest/reference/phone/ma/#operation/getLocation) | `phone:read:emergency_location:master` |

### External Contacts

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List external contacts](/docs/api/rest/reference/phone/methods/#operation/listExternalContacts) | `phone:read:list_external_contacts:admin` |
| [List external contacts](/docs/api/rest/reference/phone/ma/#operation/listExternalContacts) | `phone:read:list_external_contacts:master` |
| [Add an external contact](/docs/api/rest/reference/phone/methods/#operation/addExternalContact) | `phone:write:external_contact:admin` |
| [Add an external contact](/docs/api/rest/reference/phone/ma/#operation/addExternalContact) | `phone:write:external_contact:master` |
| [Update external contact](/docs/api/rest/reference/phone/methods/#operation/updateExternalContact) | `phone:update:external_contact:admin` |
| [Update external contact](/docs/api/rest/reference/phone/ma/#operation/updateExternalContact) | `phone:update:external_contact:master` |
| [Delete an external contact](/docs/api/rest/reference/phone/methods/#operation/deleteAExternalContact) | `phone:delete:external_contact:admin` |
| [Delete an external contact](/docs/api/rest/reference/phone/ma/#operation/deleteAExternalContact) | `phone:delete:external_contact:master` |
| [Get external contact details](/docs/api/rest/reference/phone/methods/#operation/getAExternalContact) | `phone:read:external_contact:admin` |
| [Get external contact details](/docs/api/rest/reference/phone/ma/#operation/getAExternalContact) | `phone:read:external_contact:master` |

### Fax

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get extension's fax logs](/docs/api/rest/reference/phone/methods/#operation/Getuser'sfaxlogs) | `phone:read:list_fax_log`, `phone:read:list_fax_log:admin` |
| [Get extension's fax logs](/docs/api/rest/reference/phone/ma/#operation/Getuser'sfaxlogs) | `phone:read:list_fax_log:master` |
| [Download fax file](/docs/api/rest/reference/phone/methods/#operation/Downloadfaxfile) | `phone:read:fax_log`, `phone:read:fax_log:admin` |
| [Download fax file](/docs/api/rest/reference/phone/ma/#operation/Downloadfaxfile) | `phone:read:fax_log:master` |
| [Get account's fax logs](/docs/api/rest/reference/phone/methods/#operation/GetAccount'sFaxLogs) | `phone:read:list_fax_log:admin` |
| [Get account's fax logs](/docs/api/rest/reference/phone/ma/#operation/GetAccount'sFaxLogs) | `phone:read:list_fax_log:master` |
| [Get fax log details](/docs/api/rest/reference/phone/methods/#operation/GetFaxLogDetails) | `phone:read:list_fax_log:admin` |
| [Get fax log details](/docs/api/rest/reference/phone/ma/#operation/GetFaxLogDetails) | `phone:read:list_fax_log:master` |
| [Send fax](/docs/api/rest/reference/phone/methods/#operation/SendEFax) | `phone:write:send_fax`, `phone:write:send_fax:admin` |
| [Send fax](/docs/api/rest/reference/phone/ma/#operation/SendEFax) | `phone:write:send_fax:master` |
| [Upload fax file](/docs/api/rest/reference/phone/methods/#operation/UploadFaxFiles) | `phone:write:send_fax`, `phone:write:send_fax:admin` |
| [Upload fax file](/docs/api/rest/reference/phone/ma/#operation/UploadFaxFiles) | `phone:write:send_fax:master` |

### Firmware Update Rules

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get firmware update rule information](/docs/api/rest/reference/phone/methods/#operation/GetFirmwareRuleDetail) | `phone:read:firmware_update_rule:admin` |
| [Get firmware update rule information](/docs/api/rest/reference/phone/ma/#operation/GetFirmwareRuleDetail) | `phone:read:firmware_update_rule:master` |
| [Delete firmware update rule](/docs/api/rest/reference/phone/methods/#operation/DeleteFirmwareUpdateRule) | `phone:delete:firmware_update_rule:admin` |
| [Delete firmware update rule](/docs/api/rest/reference/phone/ma/#operation/DeleteFirmwareUpdateRule) | `phone:delete:firmware_update_rule:master` |
| [List firmware update rules](/docs/api/rest/reference/phone/methods/#operation/ListFirmwareRules) | `phone:read:list_firmware_update_rules:admin` |
| [List firmware update rules](/docs/api/rest/reference/phone/ma/#operation/ListFirmwareRules) | `phone:read:list_firmware_update_rules:master` |
| [Update firmware update rule](/docs/api/rest/reference/phone/methods/#operation/UpdateFirmwareRule) | `phone:update:firmware_update_rule:admin` |
| [Update firmware update rule](/docs/api/rest/reference/phone/ma/#operation/UpdateFirmwareRule) | `phone:update:firmware_update_rule:master` |
| [Add a firmware update rule](/docs/api/rest/reference/phone/methods/#operation/AddFirmwareRule) | `phone:write:firmware_update_rule:admin` |
| [Add a firmware update rule](/docs/api/rest/reference/phone/ma/#operation/AddFirmwareRule) | `phone:write:firmware_update_rule:master` |
| [List updatable firmwares](/docs/api/rest/reference/phone/methods/#operation/ListFirmwares) | `phone:read:list_firmwares:admin` |
| [List updatable firmwares](/docs/api/rest/reference/phone/ma/#operation/ListFirmwares) | `phone:read:list_firmwares:master` |

### Group Call Pickup

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update the group call pickup information](/docs/api/rest/reference/phone/methods/#operation/updateGCP) | `phone:update:call_pickup_group:admin` |
| [Update the group call pickup information](/docs/api/rest/reference/phone/ma/#operation/updateGCP) | `phone:update:call_pickup_group:master` |
| [List call pickup group members](/docs/api/rest/reference/phone/methods/#operation/listGCPMembers) | `phone:read:call_pickup_group_member:admin` |
| [List call pickup group members](/docs/api/rest/reference/phone/ma/#operation/listGCPMembers) | `phone:read:call_pickup_group_member:master` |
| [List group call pickup objects](/docs/api/rest/reference/phone/methods/#operation/listGCP) | `phone:read:list_call_pickup_groups:admin` |
| [List group call pickup objects](/docs/api/rest/reference/phone/ma/#operation/listGCP) | `phone:read:list_call_pickup_groups:master` |
| [Delete group call pickup objects](/docs/api/rest/reference/phone/methods/#operation/deleteGCP) | `phone:delete:call_pickup_group:admin` |
| [Delete group call pickup objects](/docs/api/rest/reference/phone/ma/#operation/deleteGCP) | `phone:delete:call_pickup_group:master` |
| [Add a group call pickup object](/docs/api/rest/reference/phone/methods/#operation/addGCP) | `phone:write:call_pickup_group:admin` |
| [Add a group call pickup object](/docs/api/rest/reference/phone/ma/#operation/addGCP) | `phone:write:call_pickup_group:master` |
| [Get call pickup group by ID](/docs/api/rest/reference/phone/methods/#operation/GetGCP) | `phone:read:call_pickup_group:admin` |
| [Get call pickup group by ID](/docs/api/rest/reference/phone/ma/#operation/GetGCP) | `phone:read:call_pickup_group:master` |
| [Add members to a call pickup group](/docs/api/rest/reference/phone/methods/#operation/addGCPMembers) | `phone:write:call_pickup_group_member:admin` |
| [Add members to a call pickup group](/docs/api/rest/reference/phone/ma/#operation/addGCPMembers) | `phone:write:call_pickup_group_member:master` |
| [Remove members from call pickup group](/docs/api/rest/reference/phone/methods/#operation/removeGCPMembers) | `phone:delete:call_pickup_group_member:admin` |
| [Remove members from call pickup group](/docs/api/rest/reference/phone/ma/#operation/removeGCPMembers) | `phone:delete:call_pickup_group_member:master` |

### Groups

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get group policy details](/docs/api/rest/reference/phone/methods/#operation/GetGroupPolicyDetails) | `phone:read:group_policy:admin` |
| [Get group policy details](/docs/api/rest/reference/phone/ma/#operation/GetGroupPolicyDetails) | `phone:read:group_policy:master` |
| [Get group phone settings](/docs/api/rest/reference/phone/methods/#operation/getGroupPhoneSettings) | `phone:read:group_setting:admin` |
| [Get group phone settings](/docs/api/rest/reference/phone/ma/#operation/getGroupPhoneSettings) | `phone:read:group_setting:master` |
| [Update group policy](/docs/api/rest/reference/phone/methods/#operation/updateGroupPolicy) | `phone:update:group_policy:admin` |
| [Update group policy](/docs/api/rest/reference/phone/ma/#operation/updateGroupPolicy) | `phone:update:group_policy:master` |

### IVR

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get auto receptionist IVR](/docs/api/rest/reference/phone/methods/#operation/getAutoReceptionistIVR) | `phone:read:auto_receptionist_ivr:admin` |
| [Get auto receptionist IVR](/docs/api/rest/reference/phone/ma/#operation/getAutoReceptionistIVR) | `phone:read:auto_receptionist_ivr:master` |
| [Update auto receptionist IVR](/docs/api/rest/reference/phone/methods/#operation/updateAutoReceptionistIVR) | `phone:update:auto_receptionist_ivr:admin` |
| [Update auto receptionist IVR](/docs/api/rest/reference/phone/ma/#operation/updateAutoReceptionistIVR) | `phone:update:auto_receptionist_ivr:master` |

### Inbound Blocked List

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete an extension's inbound block rule](/docs/api/rest/reference/phone/methods/#operation/DeleteExtensiontLevelInboundBlockRules) | `phone:delete:extension_inbound_block_rule:admin`, `phone:delete:extension_inbound_block_rule` |
| [Delete an extension's inbound block rule](/docs/api/rest/reference/phone/ma/#operation/DeleteExtensiontLevelInboundBlockRules) | `phone:delete:extension_inbound_block_rule:master` |
| [Add an account's inbound block rule](/docs/api/rest/reference/phone/methods/#operation/AddAccountLevelInboundBlockRules) | `phone:write:inbound_block_rule:admin` |
| [Add an account's inbound block rule](/docs/api/rest/reference/phone/ma/#operation/AddAccountLevelInboundBlockRules) | `phone:write:inbound_block_rule:master` |
| [Delete an account's inbound block rule](/docs/api/rest/reference/phone/methods/#operation/DeleteAccountLevelInboundBlockRules) | `phone:delete:inbound_block_rule:admin` |
| [Delete an account's inbound block rule](/docs/api/rest/reference/phone/ma/#operation/DeleteAccountLevelInboundBlockRules) | `phone:delete:inbound_block_rule:master` |
| [Mark a phone number as blocked for all extensions](/docs/api/rest/reference/phone/methods/#operation/MarkPhoneNumberAsBlockedForAllExtensions) | `phone:update:inbound_blocked_for_all:admin` |
| [Mark a phone number as blocked for all extensions](/docs/api/rest/reference/phone/ma/#operation/MarkPhoneNumberAsBlockedForAllExtensions) | `phone:update:inbound_blocked_for_all:master` |
| [List an account's inbound block rules](/docs/api/rest/reference/phone/methods/#operation/ListAccountLevelInboundBlockRules) | `phone:read:list_inbound_block_rules:admin` |
| [List an account's inbound block rules](/docs/api/rest/reference/phone/ma/#operation/ListAccountLevelInboundBlockRules) | `phone:read:list_inbound_block_rules:master` |
| [List an extension's inbound block rules](/docs/api/rest/reference/phone/methods/#operation/ListExtensionLevelInboundBlockRules) | `phone:read:list_extension_inbound_block_rules:admin`, `phone:read:list_extension_inbound_block_rules` |
| [List an extension's inbound block rules](/docs/api/rest/reference/phone/ma/#operation/ListExtensionLevelInboundBlockRules) | `phone:read:list_extension_inbound_block_rules:master` |
| [Delete an account's inbound blocked statistics](/docs/api/rest/reference/phone/methods/#operation/DeleteAccountLevelInboundBlockedStatistics) | `phone:delete:extension_inbound_block_rule_stat:admin` |
| [Delete an account's inbound blocked statistics](/docs/api/rest/reference/phone/ma/#operation/DeleteAccountLevelInboundBlockedStatistics) | `phone:delete:extension_inbound_block_rule_stat:master` |
| [Update an account's inbound block rule](/docs/api/rest/reference/phone/methods/#operation/UpdateAccountLevelInboundBlockRule) | `phone:update:inbound_block_rule:admin` |
| [Update an account's inbound block rule](/docs/api/rest/reference/phone/ma/#operation/UpdateAccountLevelInboundBlockRule) | `phone:update:inbound_block_rule:master` |
| [Add an extension's inbound block rule](/docs/api/rest/reference/phone/methods/#operation/AddExtensiontLevelInboundBlockRules) | `phone:write:extension_inbound_block_rule:admin`, `phone:write:extension_inbound_block_rule` |
| [Add an extension's inbound block rule](/docs/api/rest/reference/phone/ma/#operation/AddExtensiontLevelInboundBlockRules) | `phone:write:extension_inbound_block_rule:master` |
| [List an account's inbound blocked statistics](/docs/api/rest/reference/phone/methods/#operation/ListAccountLevelInboundBlockedStatistics) | `phone:read:list_extension_inbound_block_rules_stat:admin` |
| [List an account's inbound blocked statistics](/docs/api/rest/reference/phone/ma/#operation/ListAccountLevelInboundBlockedStatistics) | `phone:read:list_extension_inbound_block_rules_stat:master` |

### Line Keys

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get line key position and settings information](/docs/api/rest/reference/phone/methods/#operation/listLineKeySetting) | `phone:read:line_keys`, `phone:read:line_keys:admin` |
| [Get line key position and settings information](/docs/api/rest/reference/phone/ma/#operation/listLineKeySetting) | `phone:read:line_keys:master` |
| [Delete a line key setting.](/docs/api/rest/reference/phone/methods/#operation/DeleteLineKey) | `phone:delete:line_keys`, `phone:delete:line_keys:admin` |
| [Delete a line key setting.](/docs/api/rest/reference/phone/ma/#operation/DeleteLineKey) | `phone:delete:line_keys:master` |
| [Batch update line key position and settings information](/docs/api/rest/reference/phone/methods/#operation/BatchUpdateLineKeySetting) | `phone:update:line_keys`, `phone:update:line_keys:admin` |
| [Batch update line key position and settings information](/docs/api/rest/reference/phone/ma/#operation/BatchUpdateLineKeySetting) | `phone:update:line_keys:master` |

### Monitoring Groups

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Remove all monitors or monitored members from a monitoring group](/docs/api/rest/reference/phone/methods/#operation/removeMembers) | `phone:delete:monitoring_group_member:admin` |
| [Remove all monitors or monitored members from a monitoring group](/docs/api/rest/reference/phone/ma/#operation/removeMembers) | `phone:delete:monitoring_group_member:master` |
| [Get members of a monitoring group](/docs/api/rest/reference/phone/methods/#operation/listMembers) | `phone:read:list_monitoring_group_members:admin` |
| [Get members of a monitoring group](/docs/api/rest/reference/phone/ma/#operation/listMembers) | `phone:read:list_monitoring_group_members:master` |
| [Add members to a monitoring group](/docs/api/rest/reference/phone/methods/#operation/addMembers) | `phone:write:monitoring_group_member:admin` |
| [Add members to a monitoring group](/docs/api/rest/reference/phone/ma/#operation/addMembers) | `phone:write:monitoring_group_member:master` |
| [Delete a monitoring group](/docs/api/rest/reference/phone/methods/#operation/deleteMonitoringGroup) | `phone:delete:monitoring_group:admin` |
| [Delete a monitoring group](/docs/api/rest/reference/phone/ma/#operation/deleteMonitoringGroup) | `phone:delete:monitoring_group:master` |
| [Get monitoring group by ID](/docs/api/rest/reference/phone/methods/#operation/getMonitoringGroupById) | `phone:read:monitoring_group:admin` |
| [Get monitoring group by ID](/docs/api/rest/reference/phone/ma/#operation/getMonitoringGroupById) | `phone:read:monitoring_group:master` |
| [Create a monitoring group](/docs/api/rest/reference/phone/methods/#operation/createMonitoringGroup) | `phone:write:monitoring_group:admin` |
| [Create a monitoring group](/docs/api/rest/reference/phone/ma/#operation/createMonitoringGroup) | `phone:write:monitoring_group:master` |
| [Get a list of monitoring groups on an account](/docs/api/rest/reference/phone/methods/#operation/listMonitoringGroup) | `phone:read:list_monitoring_groups:admin` |
| [Get a list of monitoring groups on an account](/docs/api/rest/reference/phone/ma/#operation/listMonitoringGroup) | `phone:read:list_monitoring_groups:master` |
| [Remove a member from a monitoring group](/docs/api/rest/reference/phone/methods/#operation/removeMember) | `phone:delete:monitoring_group_member:admin` |
| [Remove a member from a monitoring group](/docs/api/rest/reference/phone/ma/#operation/removeMember) | `phone:delete:monitoring_group_member:master` |
| [Update a monitoring group](/docs/api/rest/reference/phone/methods/#operation/updateMonitoringGroup) | `phone:update:monitoring_group:admin` |
| [Update a monitoring group](/docs/api/rest/reference/phone/ma/#operation/updateMonitoringGroup) | `phone:update:monitoring_group:master` |

### Outbound Calling

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Add common area level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/AddCommonAreaOutboundCallingExceptionRule) | `phone:write:common_area_outbound_calling_rule:admin` |
| [Add common area level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/AddCommonAreaOutboundCallingExceptionRule) | `phone:write:common_area_outbound_calling_rule:master` |
| [Get site level outbound calling countries and regions](/docs/api/rest/reference/phone/methods/#operation/GetSiteOutboundCallingCountriesAndRegions) | `phone:read:site_outbound_calling_rule:admin` |
| [Get site level outbound calling countries and regions](/docs/api/rest/reference/phone/ma/#operation/GetSiteOutboundCallingCountriesAndRegions) | `phone:read:site_outbound_calling_rule:master` |
| [Get account level outbound calling countries and regions](/docs/api/rest/reference/phone/methods/#operation/GetAccountOutboundCallingCountriesAndRegions) | `phone:read:list_outbound_calling_rules:admin` |
| [Get account level outbound calling countries and regions](/docs/api/rest/reference/phone/ma/#operation/GetAccountOutboundCallingCountriesAndRegions) | `phone:read:list_outbound_calling_rules:master` |
| [Update user level outbound calling countries or regions](/docs/api/rest/reference/phone/methods/#operation/UpdateUserOutboundCallingCountriesOrRegions) | `phone:update:user_outbound_calling_rule:admin` |
| [Update user level outbound calling countries or regions](/docs/api/rest/reference/phone/ma/#operation/UpdateUserOutboundCallingCountriesOrRegions) | `phone:update:user_outbound_calling_rule:master` |
| [Add user level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/AddUserOutboundCallingExceptionRule) | `phone:write:user_outbound_calling_rule:admin` |
| [Add user level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/AddUserOutboundCallingExceptionRule) | `phone:write:user_outbound_calling_rule:master` |
| [Delete site level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/deleteSiteOutboundCallingExceptionRule) | `phone:delete:site_outbound_calling_rule:admin` |
| [Delete site level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/deleteSiteOutboundCallingExceptionRule) | `phone:delete:site_outbound_calling_rule:master` |
| [Update site level outbound calling countries or regions](/docs/api/rest/reference/phone/methods/#operation/UpdateSiteOutboundCallingCountriesOrRegions) | `phone:update:site_outbound_calling_rule:admin` |
| [Update site level outbound calling countries or regions](/docs/api/rest/reference/phone/ma/#operation/UpdateSiteOutboundCallingCountriesOrRegions) | `phone:update:site_outbound_calling_rule:master` |
| [Delete account level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/deleteAccountOutboundCallingExceptionRule) | `phone:delete:outbound_calling_rule:admin` |
| [Delete account level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/deleteAccountOutboundCallingExceptionRule) | `phone:delete:outbound_calling_rule:master` |
| [List site level outbound calling exception rules](/docs/api/rest/reference/phone/methods/#operation/listSiteOutboundCallingExceptionRule) | `phone:read:site_outbound_calling_rule:admin` |
| [List site level outbound calling exception rules](/docs/api/rest/reference/phone/ma/#operation/listSiteOutboundCallingExceptionRule) | `phone:read:site_outbound_calling_rule:master` |
| [Add site level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/AddSiteOutboundCallingExceptionRule) | `phone:write:site_outbound_calling_rule:admin` |
| [Add site level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/AddSiteOutboundCallingExceptionRule) | `phone:write:site_outbound_calling_rule:master` |
| [Update user level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/UpdateUserOutboundCallingExceptionRule) | `phone:update:user_outbound_calling_rule:admin` |
| [Update user level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/UpdateUserOutboundCallingExceptionRule) | `phone:update:user_outbound_calling_rule:master` |
| [Update common area level outbound calling countries or regions](/docs/api/rest/reference/phone/methods/#operation/UpdateCommonAreaOutboundCallingCountriesOrRegions) | `phone:update:common_area_outbound_calling_rule:admin` |
| [Update common area level outbound calling countries or regions](/docs/api/rest/reference/phone/ma/#operation/UpdateCommonAreaOutboundCallingCountriesOrRegions) | `phone:update:common_area_outbound_calling_rule:master` |
| [Update account level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/UpdateAccountOutboundCallingExceptionRule) | `phone:update:outbound_calling_rule:admin` |
| [Update account level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/UpdateAccountOutboundCallingExceptionRule) | `phone:update:outbound_calling_rule:master` |
| [Add account level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/AddAccountOutboundCallingExceptionRule) | `phone:write:outbound_calling_rule:admin` |
| [Add account level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/AddAccountOutboundCallingExceptionRule) | `phone:write:outbound_calling_rule:master` |
| [Update account level outbound calling countries or regions](/docs/api/rest/reference/phone/methods/#operation/UpdateAccountOutboundCallingCountriesOrRegions) | `phone:update:outbound_calling_rule:admin` |
| [Update account level outbound calling countries or regions](/docs/api/rest/reference/phone/ma/#operation/UpdateAccountOutboundCallingCountriesOrRegions) | `phone:update:outbound_calling_rule:master` |
| [Get user level outbound calling countries and regions](/docs/api/rest/reference/phone/methods/#operation/GetUserOutboundCallingCountriesAndRegions) | `phone:read:user_outbound_calling_rule:admin` |
| [Get user level outbound calling countries and regions](/docs/api/rest/reference/phone/ma/#operation/GetUserOutboundCallingCountriesAndRegions) | `phone:read:user_outbound_calling_rule:master` |
| [List account level outbound calling exception rules](/docs/api/rest/reference/phone/methods/#operation/listAccountOutboundCallingExceptionRule) | `phone:read:list_outbound_calling_rules:admin` |
| [List account level outbound calling exception rules](/docs/api/rest/reference/phone/ma/#operation/listAccountOutboundCallingExceptionRule) | `phone:read:list_outbound_calling_rules:master` |
| [Delete common area level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/deleteCommonAreaOutboundCallingExceptionRule) | `phone:delete:common_area_outbound_calling_rule:admin` |
| [Delete common area level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/deleteCommonAreaOutboundCallingExceptionRule) | `phone:delete:common_area_outbound_calling_rule:master` |
| [List common area level outbound calling exception rules](/docs/api/rest/reference/phone/methods/#operation/listCommonAreaOutboundCallingExceptionRule) | `phone:read:common_area_outbound_calling_rule:admin` |
| [List common area level outbound calling exception rules](/docs/api/rest/reference/phone/ma/#operation/listCommonAreaOutboundCallingExceptionRule) | `phone:read:common_area_outbound_calling_rule:master` |
| [Delete user level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/deleteUserOutboundCallingExceptionRule) | `phone:delete:user_outbound_calling_rule:admin` |
| [Delete user level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/deleteUserOutboundCallingExceptionRule) | `phone:delete:user_outbound_calling_rule:master` |
| [Update common area level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/UpdateCommonAreaOutboundCallingExceptionRule) | `phone:update:common_area_outbound_calling_rule:admin` |
| [Update common area level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/UpdateCommonAreaOutboundCallingExceptionRule) | `phone:update:common_area_outbound_calling_rule:master` |
| [Get common area level outbound calling countries and regions](/docs/api/rest/reference/phone/methods/#operation/GetCommonAreaOutboundCallingCountriesAndRegions) | `phone:read:common_area_outbound_calling_rule:admin` |
| [Get common area level outbound calling countries and regions](/docs/api/rest/reference/phone/ma/#operation/GetCommonAreaOutboundCallingCountriesAndRegions) | `phone:read:common_area_outbound_calling_rule:master` |
| [Update site level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/UpdateSiteOutboundCallingExceptionRule) | `phone:update:site_outbound_calling_rule:admin` |
| [Update site level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/UpdateSiteOutboundCallingExceptionRule) | `phone:update:site_outbound_calling_rule:master` |
| [List user level outbound calling exception rules](/docs/api/rest/reference/phone/methods/#operation/listUserOutboundCallingExceptionRule) | `phone:read:user_outbound_calling_rule:admin` |
| [List user level outbound calling exception rules](/docs/api/rest/reference/phone/ma/#operation/listUserOutboundCallingExceptionRule) | `phone:read:user_outbound_calling_rule:master` |

### Phone Devices

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List Smartphones](/docs/api/rest/reference/phone/methods/#operation/ListSmartphones) | `phone:read:list_devices:admin` |
| [List Smartphones](/docs/api/rest/reference/phone/ma/#operation/ListSmartphones) | `phone:read:list_devices:master` |
| [Assign an entity to a device](/docs/api/rest/reference/phone/methods/#operation/addExtensionsToADevice) | `phone:write:device_extension:admin` |
| [Assign an entity to a device](/docs/api/rest/reference/phone/ma/#operation/addExtensionsToADevice) | `phone:write:device_extension:master` |
| [Reboot a desk phone](/docs/api/rest/reference/phone/methods/#operation/rebootPhoneDevice) | `phone:write:reboot_device:admin` |
| [Reboot a desk phone](/docs/api/rest/reference/phone/ma/#operation/rebootPhoneDevice) | `phone:write:reboot_device:master` |
| [Delete a device](/docs/api/rest/reference/phone/methods/#operation/deleteADevice) | `phone:delete:device:admin` |
| [Delete a device](/docs/api/rest/reference/phone/ma/#operation/deleteADevice) | `phone:delete:device:master` |
| [Update provision template of a device](/docs/api/rest/reference/phone/methods/#operation/updateProvisionTemplateToDevice) | `phone:update:device_provision_template:admin` |
| [Update provision template of a device](/docs/api/rest/reference/phone/ma/#operation/updateProvisionTemplateToDevice) | `phone:update:device_provision_template:master` |
| [List devices](/docs/api/rest/reference/phone/methods/#operation/listPhoneDevices) | `phone:read:list_devices:admin` |
| [List devices](/docs/api/rest/reference/phone/ma/#operation/listPhoneDevices) | `phone:read:list_devices:master` |
| [Sync deskphones](/docs/api/rest/reference/phone/methods/#operation/syncPhoneDevice) | `phone:write:sync_device:admin` |
| [Sync deskphones](/docs/api/rest/reference/phone/ma/#operation/syncPhoneDevice) | `phone:write:sync_device:master` |
| [Add a device](/docs/api/rest/reference/phone/methods/#operation/addPhoneDevice) | `phone:write:device:admin` |
| [Add a device](/docs/api/rest/reference/phone/ma/#operation/addPhoneDevice) | `phone:write:device:master` |
| [Get device details](/docs/api/rest/reference/phone/methods/#operation/getADevice) | `phone:read:device:admin` |
| [Get device details](/docs/api/rest/reference/phone/ma/#operation/getADevice) | `phone:read:device:master` |
| [Update a device](/docs/api/rest/reference/phone/methods/#operation/updateADevice) | `phone:update:device:admin` |
| [Update a device](/docs/api/rest/reference/phone/ma/#operation/updateADevice) | `phone:update:device:master` |
| [Unassign an entity from the device](/docs/api/rest/reference/phone/methods/#operation/deleteExtensionFromADevice) | `phone:delete:device_extension:admin` |
| [Unassign an entity from the device](/docs/api/rest/reference/phone/ma/#operation/deleteExtensionFromADevice) | `phone:delete:device_extension:master` |

### Phone Numbers

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update a phone number](/docs/api/rest/reference/phone/methods/#operation/updatePhoneNumberDetails) | `phone:update:number:admin` |
| [Update a phone number](/docs/api/rest/reference/phone/ma/#operation/updatePhoneNumberDetails) | `phone:update:number:master` |
| [Update a site's unassigned phone numbers](/docs/api/rest/reference/phone/methods/#operation/updateSiteForUnassignedPhoneNumbers) | `phone:update:site_number:admin` |
| [Update a site's unassigned phone numbers](/docs/api/rest/reference/phone/ma/#operation/updateSiteForUnassignedPhoneNumbers) | `phone:update:site_number:master` |
| [Assign a phone number to a user](/docs/api/rest/reference/phone/methods/#operation/assignPhoneNumber) | `phone:write:user_number`, `phone:write:user_number:admin` |
| [Assign a phone number to a user](/docs/api/rest/reference/phone/ma/#operation/assignPhoneNumber) | `phone:write:user_number:master` |
| [Add BYOC phone numbers](/docs/api/rest/reference/phone/methods/#operation/addBYOCNumber) | `phone:write:byo_carrier_number:admin` |
| [Add BYOC phone numbers](/docs/api/rest/reference/phone/ma/#operation/addBYOCNumber) | `phone:write:byo_carrier_number:master` |
| [Delete unassigned phone numbers](/docs/api/rest/reference/phone/methods/#operation/deleteUnassignedPhoneNumbers) | `phone:delete:number:admin` |
| [Delete unassigned phone numbers](/docs/api/rest/reference/phone/ma/#operation/deleteUnassignedPhoneNumbers) | `phone:delete:number:master` |
| [Unassign a phone number](/docs/api/rest/reference/phone/methods/#operation/UnassignPhoneNumber) | `phone:delete:user_number`, `phone:delete:user_number:admin` |
| [Unassign a phone number](/docs/api/rest/reference/phone/ma/#operation/UnassignPhoneNumber) | `phone:delete:user_number:master` |
| [Get a phone number](/docs/api/rest/reference/phone/methods/#operation/getPhoneNumberDetails) | `phone:read:numbers:admin` |
| [Get a phone number](/docs/api/rest/reference/phone/ma/#operation/getPhoneNumberDetails) | `phone:read:numbers:master` |
| [List phone numbers](/docs/api/rest/reference/phone/methods/#operation/listAccountPhoneNumbers) | `phone:read:list_numbers:admin` |
| [List phone numbers](/docs/api/rest/reference/phone/ma/#operation/listAccountPhoneNumbers) | `phone:read:list_numbers:master` |

### Phone Plans

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List plan information](/docs/api/rest/reference/phone/methods/#operation/listPhonePlans) | `phone:read:list_calling_plans:admin` |
| [List plan information](/docs/api/rest/reference/phone/ma/#operation/listPhonePlans) | `phone:read:list_calling_plans:master` |
| [List calling plans](/docs/api/rest/reference/phone/methods/#operation/listCallingPlans) | `phone:read:list_calling_plans:admin` |
| [List calling plans](/docs/api/rest/reference/phone/ma/#operation/listCallingPlans) | `phone:read:list_calling_plans:master` |

### Phone Roles

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update a phone role](/docs/api/rest/reference/phone/methods/#operation/UpdatePhoneRole) | `phone:update:role:admin` |
| [Update a phone role](/docs/api/rest/reference/phone/ma/#operation/UpdatePhoneRole) | `phone:update:role:master` |
| [List phone roles](/docs/api/rest/reference/phone/methods/#operation/ListPhoneRoles) | `phone:read:list_roles:admin` |
| [List phone roles](/docs/api/rest/reference/phone/ma/#operation/ListPhoneRoles) | `phone:read:list_roles:master` |
| [Add members to roles](/docs/api/rest/reference/phone/methods/#operation/AddRoleMembers) | `phone:write:role_member:admin` |
| [Add members to roles](/docs/api/rest/reference/phone/ma/#operation/AddRoleMembers) | `phone:write:role_member:master` |
| [Add phone role targets](/docs/api/rest/reference/phone/methods/#operation/AddPhoneRoleTargets) | `phone:write:role:admin` |
| [Add phone role targets](/docs/api/rest/reference/phone/ma/#operation/AddPhoneRoleTargets) | `phone:write:role:master` |
| [Delete phone role targets](/docs/api/rest/reference/phone/methods/#operation/DeletePhoneRoleTargets) | `phone:delete:role:admin` |
| [Delete phone role targets](/docs/api/rest/reference/phone/ma/#operation/DeletePhoneRoleTargets) | `phone:delete:role:master` |
| [List phone role targets](/docs/api/rest/reference/phone/methods/#operation/ListPhoneRoleTargets) | `phone:read:list_roles:admin` |
| [List phone role targets](/docs/api/rest/reference/phone/ma/#operation/ListPhoneRoleTargets) | `phone:read:list_roles:master` |
| [Delete a phone role](/docs/api/rest/reference/phone/methods/#operation/DeletePhoneRole) | `phone:delete:role:admin` |
| [Delete a phone role](/docs/api/rest/reference/phone/ma/#operation/DeletePhoneRole) | `phone:delete:role:master` |
| [Duplicate a phone role](/docs/api/rest/reference/phone/methods/#operation/DuplicatePhoneRole) | `phone:write:role:admin` |
| [Duplicate a phone role](/docs/api/rest/reference/phone/ma/#operation/DuplicatePhoneRole) | `phone:write:role:master` |
| [Delete members in a role](/docs/api/rest/reference/phone/methods/#operation/DelRoleMembers) | `phone:delete:role_member:admin` |
| [Delete members in a role](/docs/api/rest/reference/phone/ma/#operation/DelRoleMembers) | `phone:delete:role_member:master` |
| [List members in a role](/docs/api/rest/reference/phone/methods/#operation/ListRoleMembers) | `phone:read:role_member:admin` |
| [List members in a role](/docs/api/rest/reference/phone/ma/#operation/ListRoleMembers) | `phone:read:role_member:master` |
| [Get role information](/docs/api/rest/reference/phone/methods/#operation/getRoleInformation) | `phone:read:role:admin` |
| [Get role information](/docs/api/rest/reference/phone/ma/#operation/getRoleInformation) | `phone:read:role:master` |

### Private Directory

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Remove a member from a private directory](/docs/api/rest/reference/phone/methods/#operation/removeAMemberFromAPrivateDirectory) | `phone:delete:private_directory_member:admin` |
| [Remove a member from a private directory](/docs/api/rest/reference/phone/ma/#operation/removeAMemberFromAPrivateDirectory) | `phone:delete:private_directory_member:master` |
| [Add members to a private directory](/docs/api/rest/reference/phone/methods/#operation/addMembersToAPrivateDirectory) | `phone:write:private_directory_member:admin` |
| [Add members to a private directory](/docs/api/rest/reference/phone/ma/#operation/addMembersToAPrivateDirectory) | `phone:write:private_directory_member:master` |
| [Update a private directory member](/docs/api/rest/reference/phone/methods/#operation/updateAPrivateDirectoryMember) | `phone:update:private_directory_member:admin` |
| [Update a private directory member](/docs/api/rest/reference/phone/ma/#operation/updateAPrivateDirectoryMember) | `phone:update:private_directory_member:master` |
| [List private directory members](/docs/api/rest/reference/phone/methods/#operation/listPrivateDirectoryMembers) | `phone:read:list_private_directory_members:admin` |
| [List private directory members](/docs/api/rest/reference/phone/ma/#operation/listPrivateDirectoryMembers) | `phone:read:list_private_directory_members:master` |

### Provider Exchange

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List carrier peering phone numbers.](/docs/api/rest/reference/phone/methods/#operation/listCarrierPeeringPhoneNumbers) | `phone:read:list_peering_numbers:admin` |
| [List carrier peering phone numbers.](/docs/api/rest/reference/phone/ma/#operation/listCarrierPeeringPhoneNumbers) | `phone:read:list_peering_numbers:master` |
| [Update peering phone numbers](/docs/api/rest/reference/phone/methods/#operation/updatePeeringPhoneNumbers) | `phone:update:peering_number:admin` |
| [Update peering phone numbers](/docs/api/rest/reference/phone/ma/#operation/updatePeeringPhoneNumbers) | `phone:update:peering_number:master` |
| [Add peering phone numbers](/docs/api/rest/reference/phone/methods/#operation/addPeeringPhoneNumbers) | `phone:write:peering_number:admin` |
| [Add peering phone numbers](/docs/api/rest/reference/phone/ma/#operation/addPeeringPhoneNumbers) | `phone:write:peering_number:master` |
| [List peering phone numbers](/docs/api/rest/reference/phone/methods/#operation/listPeeringPhoneNumbers) | `phone:read:list_peering_numbers:admin` |
| [List peering phone numbers](/docs/api/rest/reference/phone/ma/#operation/listPeeringPhoneNumbers) | `phone:read:list_peering_numbers:master` |
| [Remove peering phone numbers](/docs/api/rest/reference/phone/methods/#operation/deletePeeringPhoneNumbers) | `phone:delete:peering_number:admin` |
| [Remove peering phone numbers](/docs/api/rest/reference/phone/ma/#operation/deletePeeringPhoneNumbers) | `phone:delete:peering_number:master` |

### Provision Templates

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List provision templates](/docs/api/rest/reference/phone/methods/#operation/listAccountProvisionTemplate) | `phone:read:list_provision_templates:admin` |
| [List provision templates](/docs/api/rest/reference/phone/ma/#operation/listAccountProvisionTemplate) | `phone:read:list_provision_templates:master` |
| [Delete a provision template](/docs/api/rest/reference/phone/methods/#operation/deleteProvisionTemplate) | `phone:delete:provision_template:admin` |
| [Delete a provision template](/docs/api/rest/reference/phone/ma/#operation/deleteProvisionTemplate) | `phone:delete:provision_template:master` |
| [Update a provision template](/docs/api/rest/reference/phone/methods/#operation/updateProvisionTemplate) | `phone:update:provision_template:admin` |
| [Update a provision template](/docs/api/rest/reference/phone/ma/#operation/updateProvisionTemplate) | `phone:update:provision_template:master` |
| [Get a provision template](/docs/api/rest/reference/phone/methods/#operation/GetProvisionTemplate) | `phone:read:provision_template:admin` |
| [Get a provision template](/docs/api/rest/reference/phone/ma/#operation/GetProvisionTemplate) | `phone:read:provision_template:master` |
| [Add a provision template](/docs/api/rest/reference/phone/methods/#operation/addProvisionTemplate) | `phone:write:provision_template:admin` |
| [Add a provision template](/docs/api/rest/reference/phone/ma/#operation/addProvisionTemplate) | `phone:write:provision_template:master` |

### Recordings

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update Auto Delete Field](/docs/api/rest/reference/phone/methods/#operation/UpdateAutoDeleteField) | `phone:update:call_recording`, `phone:update:call_recording:admin` |
| [Update Auto Delete Field](/docs/api/rest/reference/phone/ma/#operation/UpdateAutoDeleteField) | `phone:update:call_recording:master` |
| [Update Recording Status](/docs/api/rest/reference/phone/methods/#operation/UpdateRecordingStatus) | `phone:update:call_recording`, `phone:update:call_recording:admin` |
| [Update Recording Status](/docs/api/rest/reference/phone/ma/#operation/UpdateRecordingStatus) | `phone:update:call_recording:master` |
| [Delete a call recording](/docs/api/rest/reference/phone/methods/#operation/deleteCallRecording) | `phone:delete:call_recording`, `phone:delete:call_recording:admin` |
| [Delete a call recording](/docs/api/rest/reference/phone/ma/#operation/deleteCallRecording) | `phone:delete:call_recording:master` |
| [Get recording by call ID](/docs/api/rest/reference/phone/methods/#operation/getPhoneRecordingsByCallIdOrCallLogId) | `phone:read:call_recording`, `phone:read:call_recording:admin` |
| [Get recording by call ID](/docs/api/rest/reference/phone/ma/#operation/getPhoneRecordingsByCallIdOrCallLogId) | `phone:read:call_recording:master` |
| [Get user's recordings](/docs/api/rest/reference/phone/methods/#operation/phoneUserRecordings) | `phone:read:list_recordings`, `phone:read:list_recordings:admin` |
| [Get user's recordings](/docs/api/rest/reference/phone/ma/#operation/phoneUserRecordings) | `phone:read:list_recordings:master` |
| [Download a phone recording transcript](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadRecordingTranscript) | `phone:read:recording_transcript`, `phone:read:recording_transcript:admin` |
| [Download a phone recording transcript](/docs/api/rest/reference/phone/ma/#operation/phoneDownloadRecordingTranscript) | `phone:read:recording_transcript:master` |
| [Download a phone recording](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadRecordingFile) | `phone:read:call_recording`, `phone:read:call_recording:admin` |
| [Download a phone recording](/docs/api/rest/reference/phone/ma/#operation/phoneDownloadRecordingFile) | `phone:read:call_recording:master` |
| [Get call recordings](/docs/api/rest/reference/phone/methods/#operation/getPhoneRecordings) | `phone:read:list_call_recordings:admin` |
| [Get call recordings](/docs/api/rest/reference/phone/ma/#operation/getPhoneRecordings) | `phone:read:list_call_recordings:master` |

### Reports

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get SMS/MMS charges usage report](/docs/api/rest/reference/phone/methods/#operation/GetSMSChargesUsageReport) | `phone:read:sms_charges:admin` |
| [Get SMS/MMS charges usage report](/docs/api/rest/reference/phone/ma/#operation/GetSMSChargesUsageReport) | `phone:read:sms_charges:master` |
| [Get fax charges usage report](/docs/api/rest/reference/phone/methods/#operation/Getfaxchargesusagereport) | `phone:read:fax_charges:admin` |
| [Get fax charges usage report](/docs/api/rest/reference/phone/ma/#operation/Getfaxchargesusagereport) | `phone:read:fax_charges:master` |
| [Get operation logs report](/docs/api/rest/reference/phone/methods/#operation/getPSOperationLogs) | `phone:read:operation_logs:admin` |
| [Get operation logs report](/docs/api/rest/reference/phone/ma/#operation/getPSOperationLogs) | `phone:read:operation_logs:master` |
| [Get call charges usage report](/docs/api/rest/reference/phone/methods/#operation/GetCallChargesUsageReport) | `phone:read:call_charges:admin` |
| [Get call charges usage report](/docs/api/rest/reference/phone/ma/#operation/GetCallChargesUsageReport) | `phone:read:call_charges:master` |

### Routing Rules

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update directory backup routing rule](/docs/api/rest/reference/phone/methods/#operation/updateRoutingRule) | `phone:update:routing_rule:admin` |
| [Update directory backup routing rule](/docs/api/rest/reference/phone/ma/#operation/updateRoutingRule) | `phone:update:routing_rule:master` |
| [List directory backup routing rules](/docs/api/rest/reference/phone/methods/#operation/listRoutingRule) | `phone:read:list_routing_rules:admin` |
| [List directory backup routing rules](/docs/api/rest/reference/phone/ma/#operation/listRoutingRule) | `phone:read:list_routing_rules:master` |
| [Add directory backup routing rule](/docs/api/rest/reference/phone/methods/#operation/addRoutingRule) | `phone:write:routing_rule:admin` |
| [Add directory backup routing rule](/docs/api/rest/reference/phone/ma/#operation/addRoutingRule) | `phone:write:routing_rule:master` |
| [Get directory backup routing rule](/docs/api/rest/reference/phone/methods/#operation/getRoutingRule) | `phone:read:routing_rule:admin` |
| [Get directory backup routing rule](/docs/api/rest/reference/phone/ma/#operation/getRoutingRule) | `phone:read:routing_rule:master` |
| [Delete directory backup routing rule](/docs/api/rest/reference/phone/methods/#operation/deleteRoutingRule) | `phone:delete:routing_rule:admin` |
| [Delete directory backup routing rule](/docs/api/rest/reference/phone/ma/#operation/deleteRoutingRule) | `phone:delete:routing_rule:master` |

### SMS

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List user's SMS sessions in descending order](/docs/api/rest/reference/phone/methods/#operation/GetSmsSessions) | `phone:read:sms_session`, `phone:read:sms_session:admin` |
| [List user's SMS sessions in descending order](/docs/api/rest/reference/phone/ma/#operation/GetSmsSessions) | `phone:read:sms_session:master` |
| [Sync SMS by session ID](/docs/api/rest/reference/phone/methods/#operation/smsSessionSync) | `phone:read:sms_session`, `phone:read:sms_session:admin` |
| [Sync SMS by session ID](/docs/api/rest/reference/phone/ma/#operation/smsSessionSync) | `phone:read:sms_session:master` |
| [Get SMS by message ID](/docs/api/rest/reference/phone/methods/#operation/smsByMessageId) | `phone:read:sms_message`, `phone:read:sms_message:admin` |
| [Get SMS by message ID](/docs/api/rest/reference/phone/ma/#operation/smsByMessageId) | `phone:read:sms_message:master` |
| [Get user's SMS sessions](/docs/api/rest/reference/phone/methods/#operation/userSmsSession) | `phone:read:list_sms_sessions`, `phone:read:list_sms_sessions:admin` |
| [Get user's SMS sessions](/docs/api/rest/reference/phone/ma/#operation/userSmsSession) | `phone:read:list_sms_sessions:master` |
| [Get SMS session details](/docs/api/rest/reference/phone/methods/#operation/smsSessionDetails) | `phone:read:sms_session`, `phone:read:sms_session:admin` |
| [Get SMS session details](/docs/api/rest/reference/phone/ma/#operation/smsSessionDetails) | `phone:read:sms_session:master` |
| [Post SMS message](/docs/api/rest/reference/phone/methods/#operation/postSmsMessage) | `phone:read:sms_message`, `phone:read:sms_message:admin` |
| [Get account's SMS sessions](/docs/api/rest/reference/phone/methods/#operation/accountSmsSession) | `phone:read:list_sms_sessions`, `phone:read:list_sms_sessions:admin` |
| [Get account's SMS sessions](/docs/api/rest/reference/phone/ma/#operation/accountSmsSession) | `phone:read:list_sms_sessions:master` |

### SMS Campaign

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Unassign a phone number](/docs/api/rest/reference/phone/methods/#operation/unassignCampaignPhoneNumber) | `phone:delete:sms_campaign_number:admin` |
| [Unassign a phone number](/docs/api/rest/reference/phone/ma/#operation/unassignCampaignPhoneNumber) | `phone:delete:sms_campaign_number:master` |
| [List user's opt statuses of phone numbers](/docs/api/rest/reference/phone/methods/#operation/getUserNumberCampaignOptStatus) | `phone:read:sms_campaign_number_opt_status`, `phone:read:sms_campaign_number_opt_status:admin` |
| [List user's opt statuses of phone numbers](/docs/api/rest/reference/phone/ma/#operation/getUserNumberCampaignOptStatus) | `phone:read:sms_campaign_number_opt_status:master` |
| [List opt statuses of phone numbers assigned to SMS campaign](/docs/api/rest/reference/phone/methods/#operation/getNumberCampaignOptStatus) | `phone:read:sms_campaign_number_opt_status:admin` |
| [List opt statuses of phone numbers assigned to SMS campaign](/docs/api/rest/reference/phone/ma/#operation/getNumberCampaignOptStatus) | `phone:read:sms_campaign_number_opt_status:master` |
| [Assign a phone number to SMS campaign](/docs/api/rest/reference/phone/methods/#operation/assignCampaignPhoneNumbers) | `phone:write:sms_campaign_number:admin` |
| [Assign a phone number to SMS campaign](/docs/api/rest/reference/phone/ma/#operation/assignCampaignPhoneNumbers) | `phone:write:sms_campaign_number:master` |
| [List SMS campaigns](/docs/api/rest/reference/phone/methods/#operation/listAccountSMSCampaigns) | `phone:read:list_sms_campaigns:admin` |
| [List SMS campaigns](/docs/api/rest/reference/phone/ma/#operation/listAccountSMSCampaigns) | `phone:read:list_sms_campaigns:master` |
| [Update opt statuses of phone numbers assigned to SMS campaign](/docs/api/rest/reference/phone/methods/#operation/updateNumberCampaignOptStatus) | `phone:update:sms_campaign_number_opt_status:admin` |
| [Update opt statuses of phone numbers assigned to SMS campaign](/docs/api/rest/reference/phone/ma/#operation/updateNumberCampaignOptStatus) | `phone:update:sms_campaign_number_opt_status:master` |
| [Get an SMS campaign](/docs/api/rest/reference/phone/methods/#operation/GetSMSCampaign) | `phone:read:sms_campaign:admin` |
| [Get an SMS campaign](/docs/api/rest/reference/phone/ma/#operation/GetSMSCampaign) | `phone:read:sms_campaign:master` |

### SMS Consent

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List opt statuses of phone numbers assigned to SMS consent](/docs/api/rest/reference/phone/methods/#operation/getNumberConsentOptStatus) | `phone:read:sms_consent_number_opt_status:admin` |
| [List opt statuses of phone numbers assigned to SMS consent](/docs/api/rest/reference/phone/ma/#operation/getNumberConsentOptStatus) | `phone:read:sms_consent_number_opt_status:master` |

### Setting Templates

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Add a setting template](/docs/api/rest/reference/phone/methods/#operation/addSettingTemplate) | `phone:write:setting_template:admin` |
| [Add a setting template](/docs/api/rest/reference/phone/ma/#operation/addSettingTemplate) | `phone:write:setting_template:master` |
| [Get setting template details](/docs/api/rest/reference/phone/methods/#operation/getSettingTemplate) | `phone:read:setting_template:admin` |
| [Get setting template details](/docs/api/rest/reference/phone/ma/#operation/getSettingTemplate) | `phone:read:setting_template:master` |
| [Update a setting template](/docs/api/rest/reference/phone/methods/#operation/updateSettingTemplate) | `phone:update:setting_template:admin` |
| [Update a setting template](/docs/api/rest/reference/phone/ma/#operation/updateSettingTemplate) | `phone:update:setting_template:master` |
| [List setting templates](/docs/api/rest/reference/phone/methods/#operation/listSettingTemplates) | `phone:read:list_setting_templates:admin` |
| [List setting templates](/docs/api/rest/reference/phone/ma/#operation/listSettingTemplates) | `phone:read:list_setting_templates:master` |

### Settings

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List ported numbers](/docs/api/rest/reference/phone/methods/#operation/listPortedNumbers) | `phone:read:list_ported_numbers:admin` |
| [List ported numbers](/docs/api/rest/reference/phone/ma/#operation/listPortedNumbers) | `phone:read:list_ported_numbers:master` |
| [Update account policy](/docs/api/rest/reference/phone/methods/#operation/updateAccountPolicy) | `phone:update:policy:admin` |
| [Update account policy](/docs/api/rest/reference/phone/ma/#operation/updateAccountPolicy) | `phone:update:policy:master` |
| [List SIP groups](/docs/api/rest/reference/phone/methods/#operation/listSipGroups) | `phone:read:list_sip_groups:admin` |
| [List SIP groups](/docs/api/rest/reference/phone/ma/#operation/listSipGroups) | `phone:read:list_sip_groups:master` |
| [Get ported numbers details](/docs/api/rest/reference/phone/methods/#operation/getPortedNumbersDetails) | `phone:read:ported_number:admin` |
| [Get ported numbers details](/docs/api/rest/reference/phone/ma/#operation/getPortedNumbersDetails) | `phone:read:ported_number:master` |
| [List BYOC SIP trunks](/docs/api/rest/reference/phone/methods/#operation/listBYOCSIPTrunk) | `phone:read:list_sip_trunks:admin` |
| [List BYOC SIP trunks](/docs/api/rest/reference/phone/ma/#operation/listBYOCSIPTrunk) | `phone:read:list_sip_trunks:master` |
| [Update phone account settings](/docs/api/rest/reference/phone/methods/#operation/updatePhoneSettings) | `phone:update:settings:admin` |
| [Update phone account settings](/docs/api/rest/reference/phone/ma/#operation/updatePhoneSettings) | `phone:update:settings:master` |
| [Get account policy details](/docs/api/rest/reference/phone/methods/#operation/GetAccountPolicyDetails) | `phone:read:policy:admin` |
| [Get account policy details](/docs/api/rest/reference/phone/ma/#operation/GetAccountPolicyDetails) | `phone:read:policy:master` |
| [Get phone account settings](/docs/api/rest/reference/phone/methods/#operation/phoneSetting) | `phone:read:settings:admin` |
| [Get phone account settings](/docs/api/rest/reference/phone/ma/#operation/phoneSetting) | `phone:read:settings:master` |

### Shared Line Appearance

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List shared line appearances](/docs/api/rest/reference/phone/methods/#operation/listSharedLineAppearances) | `phone:read:list_shared_line_appearances:admin` |
| [List shared line appearances](/docs/api/rest/reference/phone/ma/#operation/listSharedLineAppearances) | `phone:read:list_shared_line_appearances:master` |

### Shared Line Group

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Unassign a member from a shared line group](/docs/api/rest/reference/phone/methods/#operation/deleteAMemberSLG) | `phone:delete:shared_line_member:admin` |
| [Unassign a member from a shared line group](/docs/api/rest/reference/phone/ma/#operation/deleteAMemberSLG) | `phone:delete:shared_line_member:master` |
| [Assign phone numbers](/docs/api/rest/reference/phone/methods/#operation/assignPhoneNumbersSLG) | `phone:write:shared_line_group_number:admin` |
| [Assign phone numbers](/docs/api/rest/reference/phone/ma/#operation/assignPhoneNumbersSLG) | `phone:write:shared_line_group_number:master` |
| [Unassign members from a shared line group](/docs/api/rest/reference/phone/methods/#operation/deleteMembersOfSLG) | `phone:delete:shared_line_member:admin` |
| [Unassign members from a shared line group](/docs/api/rest/reference/phone/ma/#operation/deleteMembersOfSLG) | `phone:delete:shared_line_member:master` |
| [Unassign all phone numbers](/docs/api/rest/reference/phone/methods/#operation/deletePhoneNumbersSLG) | `phone:delete:shared_line_group_number:admin` |
| [Unassign all phone numbers](/docs/api/rest/reference/phone/ma/#operation/deletePhoneNumbersSLG) | `phone:delete:shared_line_group_number:master` |
| [Add a policy setting to a shared line group](/docs/api/rest/reference/phone/methods/#operation/addSLGPolicySubSetting) | `phone:write:shared_line_group_policy:admin` |
| [Add a policy setting to a shared line group](/docs/api/rest/reference/phone/ma/#operation/addSLGPolicySubSetting) | `phone:write:shared_line_group_policy:master` |
| [Add members to a shared line group](/docs/api/rest/reference/phone/methods/#operation/addMembersToSharedLineGroup) | `phone:write:shared_line_member:admin` |
| [Add members to a shared line group](/docs/api/rest/reference/phone/ma/#operation/addMembersToSharedLineGroup) | `phone:write:shared_line_member:master` |
| [Update a shared line group policy](/docs/api/rest/reference/phone/methods/#operation/updateSharedLineGroupPolicy) | `phone:update:shared_line_group_policy:admin` |
| [Update a shared line group policy](/docs/api/rest/reference/phone/ma/#operation/updateSharedLineGroupPolicy) | `phone:update:shared_line_group_policy:master` |
| [Update an SLG policy setting](/docs/api/rest/reference/phone/methods/#operation/updateSLGPolicySubSetting) | `phone:update:shared_line_group_policy:admin` |
| [Update an SLG policy setting](/docs/api/rest/reference/phone/ma/#operation/updateSLGPolicySubSetting) | `phone:update:shared_line_group_policy:master` |
| [Update a shared line group](/docs/api/rest/reference/phone/methods/#operation/updateASharedLineGroup) | `phone:update:shared_line_group:admin` |
| [Update a shared line group](/docs/api/rest/reference/phone/ma/#operation/updateASharedLineGroup) | `phone:update:shared_line_group:master` |
| [Unassign a phone number](/docs/api/rest/reference/phone/methods/#operation/deleteAPhoneNumberSLG) | `phone:delete:shared_line_group_number:admin` |
| [Unassign a phone number](/docs/api/rest/reference/phone/ma/#operation/deleteAPhoneNumberSLG) | `phone:delete:shared_line_group_number:master` |
| [Get a shared line group policy](/docs/api/rest/reference/phone/methods/#operation/getSharedLineGroupPolicy) | `phone:read:shared_line_group_policy:admin` |
| [Get a shared line group policy](/docs/api/rest/reference/phone/ma/#operation/getSharedLineGroupPolicy) | `phone:read:shared_line_group_policy:master` |
| [Get a shared line group](/docs/api/rest/reference/phone/methods/#operation/getASharedLineGroup) | `phone:read:shared_line_group:admin` |
| [Get a shared line group](/docs/api/rest/reference/phone/ma/#operation/getASharedLineGroup) | `phone:read:shared_line_group:master` |
| [The list of shared line groups](/docs/api/rest/reference/phone/methods/#operation/listSharedLineGroups) | `phone:read:list_shared_line_groups:admin` |
| [The list of shared line groups](/docs/api/rest/reference/phone/ma/#operation/listSharedLineGroups) | `phone:read:list_shared_line_groups:master` |
| [Delete a shared line group](/docs/api/rest/reference/phone/methods/#operation/deleteASharedLineGroup) | `phone:delete:shared_line_group:admin` |
| [Delete a shared line group](/docs/api/rest/reference/phone/ma/#operation/deleteASharedLineGroup) | `phone:delete:shared_line_group:master` |
| [Delete an SLG policy setting](/docs/api/rest/reference/phone/methods/#operation/removeSLGPolicySubSetting) | `phone:delete:shared_line_group_policy:admin` |
| [Delete an SLG policy setting](/docs/api/rest/reference/phone/ma/#operation/removeSLGPolicySubSetting) | `phone:delete:shared_line_group_policy:master` |
| [Create a shared line group](/docs/api/rest/reference/phone/methods/#operation/createASharedLineGroup) | `phone:write:shared_line_group:admin` |
| [Create a shared line group](/docs/api/rest/reference/phone/ma/#operation/createASharedLineGroup) | `phone:write:shared_line_group:master` |

### Sites

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a phone site setting](/docs/api/rest/reference/phone/methods/#operation/getSiteSettingForType) | `phone:read:site_setting:admin` |
| [Get a phone site setting](/docs/api/rest/reference/phone/ma/#operation/getSiteSettingForType) | `phone:read:site_setting:master` |
| [Add a site setting](/docs/api/rest/reference/phone/methods/#operation/addSiteSetting) | `phone:write:site_setting:admin` |
| [Add a site setting](/docs/api/rest/reference/phone/ma/#operation/addSiteSetting) | `phone:write:site_setting:master` |
| [Update the site setting](/docs/api/rest/reference/phone/methods/#operation/updateSiteSetting) | `phone:update:site_setting:admin` |
| [Update the site setting](/docs/api/rest/reference/phone/ma/#operation/updateSiteSetting) | `phone:update:site_setting:master` |
| [Delete a phone site](/docs/api/rest/reference/phone/methods/#operation/deletePhoneSite) | `phone:delete:site:admin` |
| [Delete a phone site](/docs/api/rest/reference/phone/ma/#operation/deletePhoneSite) | `phone:delete:site:master` |
| [Create a phone site](/docs/api/rest/reference/phone/methods/#operation/createPhoneSite) | `phone:write:site:admin` |
| [Create a phone site](/docs/api/rest/reference/phone/ma/#operation/createPhoneSite) | `phone:write:site:master` |
| [Add customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/methods/#operation/addSiteOutboundCallerNumbers) | `phone:write:site_customized_number:admin` |
| [Add customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/ma/#operation/addSiteOutboundCallerNumbers) | `phone:write:site_customized_number:master` |
| [Remove customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/methods/#operation/deleteSiteOutboundCallerNumbers) | `phone:delete:site_customized_number:admin` |
| [Remove customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/ma/#operation/deleteSiteOutboundCallerNumbers) | `phone:delete:site_customized_number:master` |
| [Get phone site details](/docs/api/rest/reference/phone/methods/#operation/getASite) | `phone:read:site:admin` |
| [Get phone site details](/docs/api/rest/reference/phone/ma/#operation/getASite) | `phone:read:site:master` |
| [Delete a site setting](/docs/api/rest/reference/phone/methods/#operation/deleteSiteSetting) | `phone:delete:site_setting:admin` |
| [Delete a site setting](/docs/api/rest/reference/phone/ma/#operation/deleteSiteSetting) | `phone:delete:site_setting:master` |
| [Update phone site details](/docs/api/rest/reference/phone/methods/#operation/updateSiteDetails) | `phone:update:site:admin` |
| [Update phone site details](/docs/api/rest/reference/phone/ma/#operation/updateSiteDetails) | `phone:update:site:master` |
| [List customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/methods/#operation/listSiteCustomizeOutboundCallerNumbers) | `phone:read:list_site_customized_number:admin` |
| [List customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/ma/#operation/listSiteCustomizeOutboundCallerNumbers) | `phone:read:list_site_customized_number:master` |
| [List phone sites](/docs/api/rest/reference/phone/methods/#operation/listPhoneSites) | `phone:read:list_sites:admin` |
| [List phone sites](/docs/api/rest/reference/phone/ma/#operation/listPhoneSites) | `phone:read:list_sites:master` |

### Users

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Unassign user's calling plan](/docs/api/rest/reference/phone/methods/#operation/unassignCallingPlan) | `phone:delete:users_calling_plan`, `phone:delete:users_calling_plan:admin` |
| [Unassign user's calling plan](/docs/api/rest/reference/phone/ma/#operation/unassignCallingPlan) | `phone:delete:users_calling_plan:master` |
| [Get a user's profile](/docs/api/rest/reference/phone/methods/#operation/phoneUser) | `phone:read:user`, `phone:read:user:admin` |
| [Get a user's profile](/docs/api/rest/reference/phone/ma/#operation/phoneUser) | `phone:read:user:master` |
| [List phone users](/docs/api/rest/reference/phone/methods/#operation/listPhoneUsers) | `phone:read:list_users:admin` |
| [List phone users](/docs/api/rest/reference/phone/ma/#operation/listPhoneUsers) | `phone:read:list_users:master` |
| [Update user's calling plan](/docs/api/rest/reference/phone/methods/#operation/updateCallingPlan) | `phone:update:calling_plan`, `phone:update:calling_plan:admin` |
| [Update user's calling plan](/docs/api/rest/reference/phone/ma/#operation/updateCallingPlan) | `phone:update:calling_plan:master` |
| [Update multiple users' properties in batch](/docs/api/rest/reference/phone/methods/#operation/updateUsersPropertiesInBatch) | `phone:update:batch_users:admin` |
| [Update multiple users' properties in batch](/docs/api/rest/reference/phone/ma/#operation/updateUsersPropertiesInBatch) | `phone:update:batch_users:master` |
| [Assign calling plan to a user](/docs/api/rest/reference/phone/methods/#operation/assignCallingPlan) | `phone:write:calling_plan`, `phone:write:calling_plan:admin` |
| [Assign calling plan to a user](/docs/api/rest/reference/phone/ma/#operation/assignCallingPlan) | `phone:write:calling_plan:master` |
| [Get user policy details](/docs/api/rest/reference/phone/methods/#operation/GetUserPolicyDetails) | `phone:read:user_policy:admin` |
| [Get user policy details](/docs/api/rest/reference/phone/ma/#operation/GetUserPolicyDetails) | `phone:read:user_policy:master` |
| [List users' phone numbers for a customized outbound caller ID](/docs/api/rest/reference/phone/methods/#operation/listUserCustomizeOutboundCallerNumbers) | `phone:read:list_user_customized_number`, `phone:read:list_user_customized_number:admin` |
| [List users' phone numbers for a customized outbound caller ID](/docs/api/rest/reference/phone/ma/#operation/listUserCustomizeOutboundCallerNumbers) | `phone:read:list_user_customized_number:master` |
| [Get a user's profile settings](/docs/api/rest/reference/phone/methods/#operation/phoneUserSettings) | `phone:read:user_setting:admin`, `phone:read:user_setting` |
| [Get a user's profile settings](/docs/api/rest/reference/phone/ma/#operation/phoneUserSettings) | `phone:read:user_setting:master` |
| [Update user policy](/docs/api/rest/reference/phone/methods/#operation/updateUserPolicy) | `phone:update:user_policy:admin` |
| [Update user policy](/docs/api/rest/reference/phone/ma/#operation/updateUserPolicy) | `phone:update:user_policy:master` |
| [Remove users' customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/methods/#operation/deleteUserOutboundCallerNumbers) | `phone:delete:user_customized_number`, `phone:delete:user_customized_number:admin` |
| [Remove users' customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/ma/#operation/deleteUserOutboundCallerNumbers) | `phone:delete:user_customized_number:master` |
| [Update a user's profile settings](/docs/api/rest/reference/phone/methods/#operation/updateUserSettings) | `phone:update:user_setting`, `phone:update:user_setting:admin` |
| [Update a user's profile settings](/docs/api/rest/reference/phone/ma/#operation/updateUserSettings) | `phone:update:user_setting:master` |
| [Add a user's shared access setting](/docs/api/rest/reference/phone/methods/#operation/addUserSetting) | `phone:write:shared_setting`, `phone:write:shared_setting:admin` |
| [Add a user's shared access setting](/docs/api/rest/reference/phone/ma/#operation/addUserSetting) | `phone:write:shared_setting:master` |
| [Batch add users](/docs/api/rest/reference/phone/methods/#operation/batchAddUsers) | `phone:write:batch_users:admin` |
| [Batch add users](/docs/api/rest/reference/phone/ma/#operation/batchAddUsers) | `phone:write:batch_users:master` |
| [Update a user's shared access setting](/docs/api/rest/reference/phone/methods/#operation/updateUserSetting) | `phone:update:shared_setting`, `phone:update:shared_setting:admin` |
| [Update a user's shared access setting](/docs/api/rest/reference/phone/ma/#operation/updateUserSetting) | `phone:update:shared_setting:master` |
| [Delete a user's shared access setting](/docs/api/rest/reference/phone/methods/#operation/deleteUserSetting) | `phone:delete:shared_setting`, `phone:delete:shared_setting:admin` |
| [Delete a user's shared access setting](/docs/api/rest/reference/phone/ma/#operation/deleteUserSetting) | `phone:delete:shared_setting:master` |
| [Update a user's profile](/docs/api/rest/reference/phone/methods/#operation/updateUserProfile) | `phone:update:user`, `phone:update:user:admin` |
| [Update a user's profile](/docs/api/rest/reference/phone/ma/#operation/updateUserProfile) | `phone:update:user:master` |
| [Add phone numbers for users' customized outbound caller ID](/docs/api/rest/reference/phone/methods/#operation/addUserOutboundCallerNumbers) | `phone:write:user_customized_number`, `phone:write:user_customized_number:admin` |
| [Add phone numbers for users' customized outbound caller ID](/docs/api/rest/reference/phone/ma/#operation/addUserOutboundCallerNumbers) | `phone:write:user_customized_number:master` |

### Voicemails

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get user's voicemails](/docs/api/rest/reference/phone/methods/#operation/phoneUserVoiceMails) | `phone:read:list_voicemails`, `phone:read:list_voicemails:admin` |
| [Get user's voicemails](/docs/api/rest/reference/phone/ma/#operation/phoneUserVoiceMails) | `phone:read:list_voicemails:master` |
| [Update Voicemail Read Status](/docs/api/rest/reference/phone/methods/#operation/updateVoicemailReadStatus) | `phone:update:voicemail`, `phone:update:voicemail:admin` |
| [Update Voicemail Read Status](/docs/api/rest/reference/phone/ma/#operation/updateVoicemailReadStatus) | `phone:update:voicemail:master` |
| [Get account voicemails](/docs/api/rest/reference/phone/methods/#operation/accountVoiceMails) | `phone:read:list_voicemails:admin` |
| [Get account voicemails](/docs/api/rest/reference/phone/ma/#operation/accountVoiceMails) | `phone:read:list_voicemails:master` |
| [Get user voicemail details from a call log](/docs/api/rest/reference/phone/methods/#operation/getVoicemailDetailsByCallIdOrCallLogId) | `phone:read:voicemail`, `phone:read:voicemail:admin` |
| [Get user voicemail details from a call log](/docs/api/rest/reference/phone/ma/#operation/getVoicemailDetailsByCallIdOrCallLogId) | `phone:read:voicemail:master` |
| [Get voicemail details](/docs/api/rest/reference/phone/methods/#operation/getVoicemailDetails) | `phone:read:voicemail`, `phone:read:voicemail:admin` |
| [Get voicemail details](/docs/api/rest/reference/phone/ma/#operation/getVoicemailDetails) | `phone:read:voicemail:master` |
| [Download a phone voicemail](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadVoicemailFile) | `phone:read:voicemail:admin`, `phone:read:voicemail` |
| [Download a phone voicemail](/docs/api/rest/reference/phone/ma/#operation/phoneDownloadVoicemailFile) | `phone:read:voicemail:master` |
| [Delete a voicemail](/docs/api/rest/reference/phone/methods/#operation/deleteVoicemail) | `phone:delete:voicemail`, `phone:delete:voicemail:admin` |
| [Delete a voicemail](/docs/api/rest/reference/phone/ma/#operation/deleteVoicemail) | `phone:delete:voicemail:master` |

### Zoom Rooms

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Remove a phone number from a Zoom Room](/docs/api/rest/reference/phone/methods/#operation/UnassignPhoneNumberFromZoomRoom) | `phone:delete:room_phone_number:admin` |
| [Remove a phone number from a Zoom Room](/docs/api/rest/reference/phone/ma/#operation/UnassignPhoneNumberFromZoomRoom) | `phone:delete:room_phone_number:master` |
| [Assign calling plans to a Zoom Room](/docs/api/rest/reference/phone/methods/#operation/assignCallingPlanToRoom) | `phone:write:room_calling_plan:admin` |
| [Assign calling plans to a Zoom Room](/docs/api/rest/reference/phone/ma/#operation/assignCallingPlanToRoom) | `phone:write:room_calling_plan:master` |
| [Add a Zoom Room to a Zoom Phone](/docs/api/rest/reference/phone/methods/#operation/addZoomRoom) | `phone:write:room:admin` |
| [Add a Zoom Room to a Zoom Phone](/docs/api/rest/reference/phone/ma/#operation/addZoomRoom) | `phone:write:room:master` |
| [Update a Zoom Room under Zoom Phone license](/docs/api/rest/reference/phone/methods/#operation/updateZoomRoom) | `phone:update:room:admin` |
| [Update a Zoom Room under Zoom Phone license](/docs/api/rest/reference/phone/ma/#operation/updateZoomRoom) | `phone:update:room:master` |
| [Assign phone numbers to a Zoom Room](/docs/api/rest/reference/phone/methods/#operation/assignPhoneNumberToZoomRoom) | `phone:write:room_phone_number:admin` |
| [Assign phone numbers to a Zoom Room](/docs/api/rest/reference/phone/ma/#operation/assignPhoneNumberToZoomRoom) | `phone:write:room_phone_number:master` |
| [Remove a calling plan from a Zoom Room](/docs/api/rest/reference/phone/methods/#operation/unassignCallingPlanFromRoom) | `phone:delete:room_calling_plan:admin` |
| [Remove a calling plan from a Zoom Room](/docs/api/rest/reference/phone/ma/#operation/unassignCallingPlanFromRoom) | `phone:delete:room_calling_plan:master` |
| [List Zoom Rooms without Zoom Phone assignment](/docs/api/rest/reference/phone/methods/#operation/listUnassignedZoomRooms) | `phone:read:list_rooms:admin` |
| [List Zoom Rooms without Zoom Phone assignment](/docs/api/rest/reference/phone/ma/#operation/listUnassignedZoomRooms) | `phone:read:list_rooms:master` |
| [Remove a Zoom Room from a ZP account](/docs/api/rest/reference/phone/methods/#operation/RemoveZoomRoom) | `phone:delete:room:admin` |
| [Remove a Zoom Room from a ZP account](/docs/api/rest/reference/phone/ma/#operation/RemoveZoomRoom) | `phone:delete:room:master` |
| [Get a Zoom Room under Zoom Phone license](/docs/api/rest/reference/phone/methods/#operation/getZoomRoom) | `phone:read:room:admin` |
| [Get a Zoom Room under Zoom Phone license](/docs/api/rest/reference/phone/ma/#operation/getZoomRoom) | `phone:read:room:master` |
| [List Zoom Rooms under Zoom Phone license](/docs/api/rest/reference/phone/methods/#operation/listZoomRooms) | `phone:read:list_rooms:admin` |
| [List Zoom Rooms under Zoom Phone license](/docs/api/rest/reference/phone/ma/#operation/listZoomRooms) | `phone:read:list_rooms:master` |

## Zoom Revenue Accelerator


### Accounts

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get indicators settings [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/accountSettingsIndicatorsDeprecated) | `zra:read:indicator`, `zra:read:indicator:admin` |
| [Get indicators settings](/docs/api/rest/reference/iq/methods/#operation/accountIndicatorsSettings) | `zra:read:indicator`, `zra:read:indicator:admin` |

### Conversations

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Upload iq multipart file.](/docs/api/rest/reference/iq/methods/#operation/UploadZraMultipartFile.) | `zra:write:file`, `zra:write:file:admin` |
| [Get conversation comments [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationCommentsDeprecated) | `zra:read:list_conversation_comments`, `zra:read:list_conversation_comments:admin` |
| [Delete conversation's comment [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/deleteConversationCommentDeprecated) | `zra:delete:conversation_comment`, `zra:delete:conversation_comment:admin` |
| [Add new comments to the conversation [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/addConversationCommentDeprecated) | `zra:write:conversation_comment`, `zra:write:conversation_comment:admin` |
| [Add new comments to the conversation](/docs/api/rest/reference/iq/methods/#operation/addConversationComments) | `zra:read:list_conversation_comments`, `zra:read:list_conversation_comments:admin` |
| [Get conversation content analysis [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationContentAnalysisDeprecated) | `zra:read:conversation_analysis`, `zra:read:conversation_analysis:admin` |
| [Get a user's playlist [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getUserPlaylistDeprecated) | `zra:read:list_conversation_playlists` |
| [Get conversation comments](/docs/api/rest/reference/iq/methods/#operation/getConversationCommentsById) | `zra:read:list_conversation_comments`, `zra:read:list_conversation_comments:admin` |
| [List conversations [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/listConversationsDeprecated) | `zra:read:list_conversations`, `zra:read:list_conversations:admin` |
| [Update conversation host id to new host id by conversation id [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/UpdateconversationhostidtonewhostidbyconversationidDeprecated) | `zra:update:conversation_host`, `zra:update:conversation_host:admin` |
| [Delete conversation by conversation ID [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/deleteConversationDeprecated) | `zra:delete:conversations`, `zra:delete:conversations:admin` |
| [Get conversation content analysis](/docs/api/rest/reference/iq/methods/#operation/getConversationContentAnalysisById) | `zra:read:conversation_analysis`, `zra:read:conversation_analysis:admin` |
| [Update conversation host id to new host id by conversation id](/docs/api/rest/reference/iq/methods/#operation/UpdateConversationhostid2NewHostidByConversationId) | `zra:update:conversation_host`, `zra:update:conversation_host:admin` |
| [Add conversation by file id or download url.](/docs/api/rest/reference/iq/methods/#operation/AddConversationByFileIdOrDownloadUrl) | `zra:write:conversation`, `zra:write:conversation:admin` |
| [Delete conversation's comment](/docs/api/rest/reference/iq/methods/#operation/deleteConversationCommentById) | `zra:delete:conversation_comment`, `zra:delete:conversation_comment:admin` |
| [Upload iq multipart file. [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/UploadIqMultipartFileDeprecated) | `zra:write:file`, `zra:write:file:admin` |
| [Get conversation information [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationInfoDeprecated) | `zra:read:conversations:admin`, `zra:read:conversations` |
| [Add conversation by meeting record url or meeting UUID.](/docs/api/rest/reference/iq/methods/#operation/addConversationByRecord) | `zra:write:conversation`, `zra:write:conversation:admin` |
| [Upload IQ file](/docs/api/rest/reference/iq/methods/#operation/UploadZraFile) | `zra:write:file`, `zra:write:file:admin` |
| [Add conversation by file id or download url. [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/AddConversationByFileIdOrDownloadUrlDeprecated) | `zra:write:conversation`, `zra:write:conversation:admin` |
| [Edit conversation comment [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/editConversationCommentDeprecated) | `zra:update:conversation_comment`, `zra:update:conversation_comment:admin` |
| [Get conversation scorecards [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationScorecardsDeprecated) | `zra:read:conversation_scorecards`, `zra:read:conversation_scorecards:admin` |
| [Upload IQ file [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/UploadIQFileDeprecated) | `zra:write:file`, `zra:write:file:admin` |
| [Initiate and complete a multipart upload.](/docs/api/rest/reference/iq/methods/#operation/InitiateAndCompleteAMultipartUpload) | `zra:write:file`, `zra:write:file:admin` |
| [Get a user's playlist](/docs/api/rest/reference/iq/methods/#operation/getUserPlaylists) | `zra:read:list_conversation_playlists` |
| [List conversations](/docs/api/rest/reference/iq/methods/#operation/listAllConversations) | `zra:read:list_conversations`, `zra:read:list_conversations:admin` |
| [Get conversation interactions](/docs/api/rest/reference/iq/methods/#operation/getConversationInteraction) | `zra:read:conversation_participants`, `zra:read:conversation_participants:admin` |
| [Get conversation information](/docs/api/rest/reference/iq/methods/#operation/getConversationDetail) | `zra:read:conversations:admin`, `zra:read:conversations` |
| [Edit conversation comment](/docs/api/rest/reference/iq/methods/#operation/editConversationCommentById) | `zra:update:conversation_comment`, `zra:update:conversation_comment:admin` |
| [Delete conversation by conversation ID](/docs/api/rest/reference/iq/methods/#operation/deleteConversationById) | `zra:delete:conversations`, `zra:delete:conversations:admin` |
| [Get conversation scorecards](/docs/api/rest/reference/iq/methods/#operation/getConversationScorecardsById) | `zra:read:conversation_scorecards`, `zra:read:conversation_scorecards:admin` |
| [Get conversation interactions [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationInteractionsDeprecated) | `zra:read:conversation_participants`, `zra:read:conversation_participants:admin` |
| [Add conversation by meeting record url or meeting UUID. [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/addConversationDeprecated) | `zra:write:conversation`, `zra:write:conversation:admin` |

### Deals

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List deals](/docs/api/rest/reference/iq/methods/#operation/listAllDeals) | `zra:read:list_deals`, `zra:read:list_deals:admin` |
| [Delete activity from the deal](/docs/api/rest/reference/iq/methods/#operation/DeleteActivityFromDeal) | `zra:delete:deal_activity`, `zra:delete:deal_activity:admin` |
| [Get deal information [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getDealInfoDeprecated) | `zra:read:deal`, `zra:read:deal:admin` |
| [Get deal activities](/docs/api/rest/reference/iq/methods/#operation/geAllActivitiesFromDeal) | `zra:read:list_deal_activities`, `zra:read:list_deal_activities:admin` |
| [Get deal activities [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getDealActivitiesDeprecated) | `zra:read:list_deal_activities`, `zra:read:list_deal_activities:admin` |
| [List deals [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/listDealsDeprecated) | `zra:read:list_deals`, `zra:read:list_deals:admin` |
| [Delete activity from the deal [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/DeleteActivityFromTheDealDeprecated) | `zra:delete:deal_activity`, `zra:delete:deal_activity:admin` |
| [Get deal information](/docs/api/rest/reference/iq/methods/#operation/getDealDetail) | `zra:read:deal`, `zra:read:deal:admin` |

### ScheduleMeetings

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List scheduled meetings](/docs/api/rest/reference/iq/methods/#operation/Listallscheduledmeetings) | `zra:read:list_conversations`, `zra:read:list_conversations:admin` |

### Teams

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete Team](/docs/api/rest/reference/iq/methods/#operation/DeleteTeam) | `zra:delete:team:admin` |
| [Get Team Detail](/docs/api/rest/reference/iq/methods/#operation/GetTeamDetail) | `zra:read:team:admin` |
| [Assign Team Managers](/docs/api/rest/reference/iq/methods/#operation/AssignTeamManagers) | `zra:write:team_manages:admin` |
| [Assign Team Members](/docs/api/rest/reference/iq/methods/#operation/AssignTeamMembers) | `zra:write:team_members:admin` |
| [List Unassigned Team Users](/docs/api/rest/reference/iq/methods/#operation/ListUnassignedTeamUsers) | `zra:read:unassigned_team_users:admin` |
| [Move team to new parent](/docs/api/rest/reference/iq/methods/#operation/MoveTeam) | `zra:update:team:admin` |
| [Remove additional access from current team](/docs/api/rest/reference/iq/methods/#operation/DeleteSharedFromTeams) | `zra:delete:team:admin` |
| [Update Team name](/docs/api/rest/reference/iq/methods/#operation/UpdateTeam) | `zra:update:team:admin` |
| [Unassign Team Members](/docs/api/rest/reference/iq/methods/#operation/UnassignTeamMembers) | `zra:delete:team_members:admin` |
| [List Team Managers](/docs/api/rest/reference/iq/methods/#operation/ListTeamManagers) | `zra:read:team_managers:admin` |
| [Create Team](/docs/api/rest/reference/iq/methods/#operation/CreateTeam) | `zra:write:team:admin` |
| [Grant additional access to current team](/docs/api/rest/reference/iq/methods/#operation/AddSharedFromTeams) | `zra:write:team:admin` |
| [List Account Teams](/docs/api/rest/reference/iq/methods/#operation/ListTeams) | `zra:read:team_list:admin` |
| [Remove additional access from target teams](/docs/api/rest/reference/iq/methods/#operation/DeleteSharedToTeams) | `zra:delete:team:admin` |
| [Unassign Team Managers](/docs/api/rest/reference/iq/methods/#operation/UnassignTeamManagers) | `zra:delete:team_managers:admin` |
| [List Team Members](/docs/api/rest/reference/iq/methods/#operation/ListTeamMembers) | `zra:read:team_members:admin` |
| [Grant additional access to target teams](/docs/api/rest/reference/iq/methods/#operation/AddSharedToTeams) | `zra:write:team:admin` |

## Zoom Rooms


### Room Apps

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Config Zoom Room Controller Apps](/docs/api/rest/reference/zoom-rooms/methods/#operation/ConfigZoomRoomControllerApps) | `zoom_rooms:write:zoom_apps:admin` |

### Visitor Management

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a list of visitors by location](/docs/api/rest/reference/zoom-rooms/methods/#operation/invitationList) | `visitor_management:read:list_invitations`, `visitor_management:read:list_invitations:admin` |
| [Invitation details by invitationID](/docs/api/rest/reference/zoom-rooms/methods/#operation/getInvitation) | `visitor_management:read:invitation_details`, `visitor_management:read:invitation_details:admin` |
| [Update an invitation](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateInvitation) | `visitor_management:update:invitation`, `visitor_management:update:invitation:admin` |
| [Send an invitation](/docs/api/rest/reference/zoom-rooms/methods/#operation/createInvitation) | `visitor_management:write:invitation`, `visitor_management:write:invitation:admin` |
| [Check in a visitor](/docs/api/rest/reference/zoom-rooms/methods/#operation/checkinVisitor) | `visitor_management:write:check_in`, `visitor_management:write:check_in:admin` |
| [Delete an Invitation](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteInvitation) | `visitor_management:delete:invitation`, `visitor_management:delete:invitation:admin` |

### Workspaces

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get a workspace's reservations](/docs/api/rest/reference/zoom-rooms/methods/#operation/listReservations) | `workspace:read:list_reservations`, `workspace:read:list_reservations:admin` |
| [Get a workspace](/docs/api/rest/reference/zoom-rooms/methods/#operation/getWorkspace) | `workspace:read:list_workspaces`, `workspace:read:list_workspaces:admin` |
| [Add or Update a Workspace floor map](/docs/api/rest/reference/zoom-rooms/methods/#operation/AddOrUpdateAWorkspaceFloorMap) | `workspace:write:location`, `workspace:write:location:admin` |
| [Update a reservation](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateReservation) | `workspace:update:reservation`, `workspace:update:reservation:admin` |
| [Edit a workspace asset](/docs/api/rest/reference/zoom-rooms/methods/#operation/PatchWorkspaceasset) | `workspace:update:asset:admin` |
| [Delete Workspace floor map](/docs/api/rest/reference/zoom-rooms/methods/#operation/DeleteWorkspaceFloorMap) | `workspace:write:location`, `workspace:write:location:admin` |
| [List workspace reservation questionnaires](/docs/api/rest/reference/zoom-rooms/methods/#operation/Listworkspacereservationquestionnaires) | `workspace:read:reservation:admin`, `workspace:read:reservation:master` |
| [Create a reservation](/docs/api/rest/reference/zoom-rooms/methods/#operation/createReservation) | `workspace:write:reservation`, `workspace:write:reservation:admin` |
| [List workspace additional information with time range](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getaworkspaceadditionalenhancements) | `workspace:read:list_workspaces`, `workspace:read:list_workspaces:admin` |
| [Update workspace settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateWorkspaceSettings) | `workspace:update:setting:admin`, `workspace:update:setting:master` |
| [Check in/out of a reservation](/docs/api/rest/reference/zoom-rooms/methods/#operation/reservationEvent) | `workspace:write:events`, `workspace:write:events:admin` |
| [Get all workspace assets](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getallworkspaceassets) | `workspace:read:asset:admin` |
| [Create a workspace asset](/docs/api/rest/reference/zoom-rooms/methods/#operation/AddaWorkspaceasset) | `workspace:write:asset:admin` |
| [Get a workspace reservation by reservationId](/docs/api/rest/reference/zoom-rooms/methods/#operation/GETGetaworkspacereservationbyreservationID) | `workspace:read:reservation`, `workspace:read:reservation:admin` |
| [List released workspaces by timeout](/docs/api/rest/reference/zoom-rooms/methods/#operation/getWorksapceReservationReleaseInof) | `zoom_rooms:read:list_release_infos:admin` |
| [Get Workspace Calendar Free/Busy Event](/docs/api/rest/reference/zoom-rooms/methods/#operation/GetWorkspaceCalendarFree/BusyEvent) | `workspace:read:workspace:admin` |
| [List workspaces](/docs/api/rest/reference/zoom-rooms/methods/#operation/listWorkspaces) | `workspace:read:list_workspaces`, `workspace:read:list_workspaces:admin` |
| [Create a workspace](/docs/api/rest/reference/zoom-rooms/methods/#operation/createWorkspace) | `workspace:write:workspace:admin` |
| [Delete a workspace](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteWorkspace) | `workspace:delete:workspace:admin` |
| [Update a workspace](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateWorkspace) | `workspace:update:workspace:admin` |
| [Get a workspace QR code](/docs/api/rest/reference/zoom-rooms/methods/#operation/getWorkspaceQRCode) | `workspace:read:qr:admin` |
| [Delete a reservation](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteReservation) | `workspace:delete:reservation`, `workspace:delete:reservation:admin` |
| [Get a location's hot desk usage](/docs/api/rest/reference/zoom-rooms/methods/#operation/getHotDeskUsage) | `workspace:read:usage`, `workspace:read:usage:admin` |
| [Get a user's workspace's reservations](/docs/api/rest/reference/zoom-rooms/methods/#operation/userListReservations) | `workspace:read:list_reservations:admin` |
| [Get a workspace asset](/docs/api/rest/reference/zoom-rooms/methods/#operation/get_workspace_asset) | `workspace:read:asset:admin` |
| [Set Workspace Calendar Free/Busy Event](/docs/api/rest/reference/zoom-rooms/methods/#operation/SetCalendarFree/BusyEvent) | `workspace:write:workspace:admin` |
| [Get a workspace location floor map](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getlocationfloormap) | `workspace:read:location`, `workspace:read:location:admin` |
| [Delete a workspace asset](/docs/api/rest/reference/zoom-rooms/methods/#operation/DeleteaWorkspaceasset) | `workspace:delete:asset:admin` |
| [Set a desk assignment](/docs/api/rest/reference/zoom-rooms/methods/#operation/setADeskAssignment) | `workspace:write:assignment:admin` |
| [Get a desk assignment](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getadeskassignment) | `workspace:read:assignment`, `workspace:read:assignment:admin` |
| [Delete a desk assignment](/docs/api/rest/reference/zoom-rooms/methods/#operation/Deleteadeskassignment) | `workspace:delete:assignment:admin` |

### Zoom Rooms

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get device information](/docs/api/rest/reference/zoom-rooms/methods/#operation/getRoomDevices) | `zoom_rooms:read:device_profile:admin` |
| [Get Zoom Room settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRSettings) | `zoom_rooms:read:room_settings:admin` |
| [Get Zoom Room settings](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRSettings) | `zoom_rooms:read:room_settings:master` |
| [List Zoom Rooms](/docs/api/rest/reference/zoom-rooms/methods/#operation/listZoomRooms) | `zoom_rooms:read:list_rooms:admin` |
| [List Zoom Rooms](/docs/api/rest/reference/zoom-rooms/ma/#operation/listZoomRooms) | `zoom_rooms:read:list_rooms:master` |
| [Delete a device profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteRoomProfile) | `zoom_rooms:delete:device_profile:admin` |
| [Delete a device profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/deleteRoomProfile) | `zoom_rooms:delete:device_profile:master` |
| [Use Zoom Room controls](/docs/api/rest/reference/zoom-rooms/methods/#operation/ZoomRoomsControls) | `zoom_rooms:update:room_control:admin` |
| [Use Zoom Room controls](/docs/api/rest/reference/zoom-rooms/ma/#operation/ZoomRoomsControls) | `zoom_rooms:update:room_control:master` |
| [Create a device profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/createRoomDeviceProfile) | `zoom_rooms:write:device_profile:admin` |
| [Create a device profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/createRoomDeviceProfile) | `zoom_rooms:write:device_profile:master` |
| [Update Zoom Room settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateZRSettings) | `zoom_rooms:update:room_settings:admin` |
| [Update Zoom Room settings](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateZRSettings) | `zoom_rooms:update:room_settings:master` |
| [List Zoom Room devices](/docs/api/rest/reference/zoom-rooms/methods/#operation/listZRDevices) | `zoom_rooms:read:list_devices:admin` |
| [List Zoom Room devices](/docs/api/rest/reference/zoom-rooms/ma/#operation/listZRDevices) | `zoom_rooms:read:list_devices:master` |
| [Update E911 digital signage](/docs/api/rest/reference/zoom-rooms/methods/#operation/manageE911signage) | `zoom_rooms:update:room_controls:admin` |
| [Update E911 digital signage](/docs/api/rest/reference/zoom-rooms/ma/#operation/manageE911signage) | `zoom_rooms:update:room_controls:master` |
| [Get Zoom Room profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRProfile) | `zoom_rooms:read:room:admin` |
| [Get Zoom Room profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRProfile) | `zoom_rooms:read:room:master` |
| [Delete a Zoom Room](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteAZoomRoom) | `zoom_rooms:delete:room:admin` |
| [Delete a Zoom Room](/docs/api/rest/reference/zoom-rooms/ma/#operation/deleteAZoomRoom) | `zoom_rooms:delete:room:master` |
| [Get Zoom Rooms virtual controller URL](/docs/api/rest/reference/zoom-rooms/methods/#operation/getWebzrcUrl) | `zoom_rooms:read:virtual_controller:admin` |
| [Get Zoom Rooms virtual controller URL](/docs/api/rest/reference/zoom-rooms/ma/#operation/getWebzrcUrl) | `zoom_rooms:read:virtual_controller:admin` |
| [Update a Zoom Room profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateRoomProfile) | `zoom_rooms:update:room:admin` |
| [Update a Zoom Room profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateRoomProfile) | `zoom_rooms:update:room:master` |
| [Change a Zoom Room's location](/docs/api/rest/reference/zoom-rooms/methods/#operation/changeZRLocation) | `zoom_rooms:update:room_location:admin` |
| [Change a Zoom Room's location](/docs/api/rest/reference/zoom-rooms/ma/#operation/changeZRLocation) | `zoom_rooms:update:room_location:master` |
| [List device profiles](/docs/api/rest/reference/zoom-rooms/methods/#operation/getRoomProfiles) | `zoom_rooms:read:list_device_profiles:admin` |
| [List device profiles](/docs/api/rest/reference/zoom-rooms/ma/#operation/getRoomProfiles) | `zoom_rooms:read:list_device_profiles:master` |
| [Add a Zoom Room](/docs/api/rest/reference/zoom-rooms/methods/#operation/addARoom) | `zoom_rooms:write:room:admin` |
| [Add a Zoom Room](/docs/api/rest/reference/zoom-rooms/ma/#operation/addARoom) | `zoom_rooms:write:room:master` |
| [Get Zoom Room sensor data](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRSensorData) | `zoom_rooms:read:sensor_data:admin` |
| [Update a device profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateDeviceProfile) | `zoom_rooms:update:device_profile:admin` |
| [Update a device profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateDeviceProfile) | `zoom_rooms:update:device_profile:master` |
| [Get a device profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/getRoomProfile) | `zoom_rooms:read:device_profile:admin` |
| [Get a device profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/getRoomProfile) | `zoom_rooms:read:device_profile:master` |

### Zoom Rooms Account

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get Zoom Room account profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRAccountProfile) | `zoom_rooms:read:account_profile:admin` |
| [Get Zoom Room account profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRAccountProfile) | `zoom_rooms:read:account_profile:master` |
| [Update Zoom Room account profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateZRAccProfile) | `zoom_rooms:update:account_profile:admin` |
| [Update Zoom Room account profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateZRAccProfile) | `zoom_rooms:update:account_profile:master` |
| [Get Zoom Room account settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRAccountSettings) | `zoom_rooms:read:account_settings:admin` |
| [Get Zoom Room account settings](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRAccountSettings) | `zoom_rooms:read:account_settings:master` |
| [Update Zoom Room account settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateZoomRoomAccSettings) | `zoom_rooms:update:account_settings:admin` |
| [Update Zoom Room account settings](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateZoomRoomAccSettings) | `zoom_rooms:update:account_settings:master` |

### Zoom Rooms Calendar

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Start calendar service sync process](/docs/api/rest/reference/zoom-rooms/methods/#operation/syncACalendarService) | `zoom_rooms:update:calendar_service:admin` |
| [List calendar services](/docs/api/rest/reference/zoom-rooms/methods/#operation/getCalendarServices) | `zoom_rooms:read:list_calendar_services:admin` |
| [List calendar resources by calendar service](/docs/api/rest/reference/zoom-rooms/methods/#operation/getCalendarResourcesByServiceId) | `zoom_rooms:read:list_calendar_resources:admin` |
| [Add a calendar resource to a calendar service](/docs/api/rest/reference/zoom-rooms/methods/#operation/addACalendarResourceToCalendarService) | `zoom_rooms:write:calendar_resource:admin` |
| [Delete a calendar resource](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteACalendarResource) | `zoom_rooms:delete:calendar_resource:admin` |
| [Get a calendar resource by ID](/docs/api/rest/reference/zoom-rooms/methods/#operation/getCalendarResourceById) | `zoom_rooms:read:calendar_resource:admin` |
| [Delete a calendar service](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteACalendarService) | `zoom_rooms:delete:calendar_service:admin` |

### Zoom Rooms Content

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List Digital Signage library playlist published rooms](/docs/api/rest/reference/zoom-rooms/methods/#operation/ListDigitalSignagelibraryplaylistpublishedrooms) | `zoom_rooms:read:digital_signage_library_playlists:admin` |
| [List Digital Signage library playlist published rooms](/docs/api/rest/reference/zoom-rooms/ma/#operation/ListDigitalSignagelibraryplaylistpublishedrooms) | `zoom_rooms:read:digital_signage_library_playlists:master` |
| [Add Zoom Rooms background image library content](/docs/api/rest/reference/zoom-rooms/methods/#operation/AddZoomRoomsBackgroundImageLibraryContent) | `zoom_rooms:write:background_library_content:admin` |
| [Update Zoom Rooms Background Image Library Folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/UpdateaZoomRoomsBackgroundLibraryFolderName) | `zoom_rooms:update:background_library_folder:admin` |
| [List default Zoom Rooms background image library contents](/docs/api/rest/reference/zoom-rooms/methods/#operation/ListDefaultZoomRoomsBackgroundImageLibrarycontents) | `zoom_rooms:read:background_library_content:admin` |
| [Add a digital signage URL](/docs/api/rest/reference/zoom-rooms/methods/#operation/AddadigitalsignageURL) | `zoom_rooms:write:digital_signage_library_contents:admin` |
| [Add a digital signage URL](/docs/api/rest/reference/zoom-rooms/ma/#operation/AddadigitalsignageURL) | `zoom_rooms:write:digital_signage_library_contents:master` |
| [Update Digital Signage library playlist published rooms](/docs/api/rest/reference/zoom-rooms/methods/#operation/UpdateDigitalSignagelibraryplaylistpublishedrooms) | `zoom_rooms:write:digital_signage_library_playlists:admin` |
| [Update Digital Signage library playlist published rooms](/docs/api/rest/reference/zoom-rooms/ma/#operation/UpdateDigitalSignagelibraryplaylistpublishedrooms) | `zoom_rooms:write:digital_signage_library_playlists:master` |
| [Add Zoom Rooms Background Image Library Folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/AddZoomRoomsBackgroundLibraryFolder) | `zoom_rooms:write:background_library_folder:admin` |
| [Delete Zoom Rooms Background Image Library Folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/DeleteZoomRoomsBackgroundLibraryFolder) | `zoom_rooms:delete:background_library_folder:admin` |
| [Add a Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/methods/#operation/AddaDigitalSignagelibraryplaylist) | `zoom_rooms:write:digital_signage_library_playlists:admin` |
| [Add a Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/ma/#operation/AddaDigitalSignagelibraryplaylist) | `zoom_rooms:write:digital_signage_library_playlists:master` |
| [Delete Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/methods/#operation/DeleteDigitalSignagelibraryplaylist) | `zoom_rooms:write:digital_signage_library_playlists:admin` |
| [Delete Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/ma/#operation/DeleteDigitalSignagelibraryplaylist) | `zoom_rooms:write:digital_signage_library_playlists:master` |
| [Update Digital Signage library playlist content items](/docs/api/rest/reference/zoom-rooms/methods/#operation/UpdateDigitalSignagelibraryplaylistcontentitems) | `zoom_rooms:write:digital_signage_library_playlists:admin` |
| [Update Digital Signage library playlist content items](/docs/api/rest/reference/zoom-rooms/ma/#operation/UpdateDigitalSignagelibraryplaylistcontentitems) | `zoom_rooms:write:digital_signage_library_playlists:master` |
| [Get Zoom Rooms Background Image Library Folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/GetZoomRoomsBackgroundLibraryFolder) | `zoom_rooms:read:background_library_folder:admin` |
| [Update a Digital Signage content item attributes](/docs/api/rest/reference/zoom-rooms/methods/#operation/Updateadigitalsignagecontentitemattributes) | `zoom_rooms:write:digital_signage_library_contents:admin` |
| [Update a Digital Signage content item attributes](/docs/api/rest/reference/zoom-rooms/ma/#operation/Updateadigitalsignagecontentitemattributes) | `zoom_rooms:write:digital_signage_library_contents:master` |
| [List Zoom Rooms Background Image Library Folders](/docs/api/rest/reference/zoom-rooms/methods/#operation/ListZoomRoomsBackgroundLibraryFolders) | `zoom_rooms:read:background_library_folder:admin` |
| [List Digital Signage library playlists](/docs/api/rest/reference/zoom-rooms/methods/#operation/ListDigitalSignagelibraryplaylists) | `zoom_rooms:read:digital_signage_library_playlists:admin` |
| [List Digital Signage library playlists](/docs/api/rest/reference/zoom-rooms/ma/#operation/ListDigitalSignagelibraryplaylists) | `zoom_rooms:read:digital_signage_library_playlists:master` |
| [Update a digital signage content folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/Updateadigitalsignagecontentfolder) | `zoom_rooms:write:digital_signage_library_contents:admin` |
| [Update a digital signage content folder](/docs/api/rest/reference/zoom-rooms/ma/#operation/Updateadigitalsignagecontentfolder) | `zoom_rooms:write:digital_signage_library_contents:master` |
| [Add a digital signage content folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/Addadigitalsignagecontentfolder) | `zoom_rooms:write:digital_signage_library_contents:admin` |
| [Add a digital signage content folder](/docs/api/rest/reference/zoom-rooms/ma/#operation/Addadigitalsignagecontentfolder) | `zoom_rooms:write:digital_signage_library_contents:master` |
| [Get Digital Signage content folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getdigitalsignagecontentfolderdetails) | `zoom_rooms:read:digital_signage_library_contents:admin` |
| [Get Digital Signage content folder](/docs/api/rest/reference/zoom-rooms/ma/#operation/Getdigitalsignagecontentfolderdetails) | `zoom_rooms:read:digital_signage_library_contents:master` |
| [Get Digital Signage library playlist content items](/docs/api/rest/reference/zoom-rooms/methods/#operation/GetDigitalSignagelibraryplaylistcontentitems) | `zoom_rooms:read:digital_signage_library_playlists:admin` |
| [Get Digital Signage library playlist content items](/docs/api/rest/reference/zoom-rooms/ma/#operation/GetDigitalSignagelibraryplaylistcontentitems) | `zoom_rooms:read:digital_signage_library_playlists:master` |
| [Get Digital Signage content item](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getdigitalsignagecontentitem) | `zoom_rooms:read:digital_signage_library_contents:admin` |
| [Get Digital Signage content item](/docs/api/rest/reference/zoom-rooms/ma/#operation/Getdigitalsignagecontentitem) | `zoom_rooms:read:digital_signage_library_contents:master` |
| [Get Zoom Rooms background image library content](/docs/api/rest/reference/zoom-rooms/methods/#operation/GetZoomRoomsBackgroundImageLibraryContent) | `zoom_rooms:read:background_library_content:admin` |
| [List Zoom Rooms background image library contents](/docs/api/rest/reference/zoom-rooms/methods/#operation/ListZoomRoomsbackgroundimagelibrarycontents) | `zoom_rooms:read:background_library_content:admin` |
| [Get Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/methods/#operation/GetDigitalSignagelibraryplaylist) | `zoom_rooms:read:digital_signage_library_playlists:admin` |
| [Get Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/ma/#operation/GetDigitalSignagelibraryplaylist) | `zoom_rooms:read:digital_signage_library_playlists:master` |
| [Delete a Digital Signage content item](/docs/api/rest/reference/zoom-rooms/methods/#operation/Deleteadigitalsignagecontentitem) | `zoom_rooms:write:digital_signage_library_contents:admin` |
| [Delete a Digital Signage content item](/docs/api/rest/reference/zoom-rooms/ma/#operation/Deleteadigitalsignagecontentitem) | `zoom_rooms:write:digital_signage_library_contents:master` |
| [Add a digital signage image or video](/docs/api/rest/reference/zoom-rooms/methods/#operation/Adddigitalsignageimageorvideo) | `zoom_rooms:write:digital_signage_library_contents:admin` |
| [Add a digital signage image or video](/docs/api/rest/reference/zoom-rooms/ma/#operation/Adddigitalsignageimageorvideo) | `zoom_rooms:write:digital_signage_library_contents:master` |
| [Delete a Digital Signage content folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/Deleteadigitalsignagecontentfolder) | `zoom_rooms:write:digital_signage_library_contents:admin` |
| [Delete a Digital Signage content folder](/docs/api/rest/reference/zoom-rooms/ma/#operation/Deleteadigitalsignagecontentfolder) | `zoom_rooms:write:digital_signage_library_contents:master` |
| [Update Zoom Rooms background image library content](/docs/api/rest/reference/zoom-rooms/methods/#operation/UpdateZoomRoomsBackgroundImageLibraryContent) | `zoom_rooms:update:background_library_content:admin` |
| [List Digital Signage content items](/docs/api/rest/reference/zoom-rooms/methods/#operation/GETListdigitalsignagecontentitems) | `zoom_rooms:read:digital_signage_library_contents:admin` |
| [List Digital Signage content items](/docs/api/rest/reference/zoom-rooms/ma/#operation/GETListdigitalsignagecontentitems) | `zoom_rooms:read:digital_signage_library_contents:master` |
| [Update a Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/methods/#operation/UpdateaDigitalSignagelibraryplaylist) | `zoom_rooms:write:digital_signage_library_playlists:admin` |
| [Update a Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/ma/#operation/UpdateaDigitalSignagelibraryplaylist) | `zoom_rooms:write:digital_signage_library_playlists:master` |
| [Update a Digital Signage image or video file](/docs/api/rest/reference/zoom-rooms/methods/#operation/Updateadigitalsignageimageorvideofile) | `zoom_rooms:write:digital_signage_library_contents:admin` |
| [Update a Digital Signage image or video file](/docs/api/rest/reference/zoom-rooms/ma/#operation/Updateadigitalsignageimageorvideofile) | `zoom_rooms:write:digital_signage_library_contents:master` |
| [Delete Zoom Rooms Background Image Library Content](/docs/api/rest/reference/zoom-rooms/methods/#operation/DeleteZoomRoomsBackgroundImageLibraryContent) | `zoom_rooms:delete:background_library_content:admin` |

### Zoom Rooms Devices

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Change Zoom Rooms app version](/docs/api/rest/reference/zoom-rooms/methods/#operation/changeZoomRoomsAppVersion) | `zoom_rooms:update:device_app_version:admin` |
| [Change Zoom Rooms app version](/docs/api/rest/reference/zoom-rooms/ma/#operation/changeZoomRoomsAppVersion) | `zoom_rooms:update:device_app_version:master` |
| [Delete a Zoom Room user device](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteDevice) | `zoom_rooms:delete:device:admin` |

### Zoom Rooms Location

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Add a location](/docs/api/rest/reference/zoom-rooms/methods/#operation/addAZRLocation) | `zoom_rooms:write:location:admin` |
| [Add a location](/docs/api/rest/reference/zoom-rooms/ma/#operation/addAZRLocation) | `zoom_rooms:write:location:master` |
| [Get Zoom Room location structure](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRLocationStructure) | `zoom_rooms:read:location_hierarchy:admin` |
| [Get Zoom Room location structure](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRLocationStructure) | `zoom_rooms:read:location_hierarchy:master` |
| [Update Zoom Rooms location structure](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateZoomRoomsLocationStructure) | `zoom_rooms:update:location_hierarchy:admin` |
| [Update Zoom Rooms location structure](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateZoomRoomsLocationStructure) | `zoom_rooms:update:location_hierarchy:master` |
| [Delete a location](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteAZRLocation) | `zoom_rooms:write:location:admin` |
| [Delete a location](/docs/api/rest/reference/zoom-rooms/ma/#operation/deleteAZRLocation) | `zoom_rooms:write:location:master` |
| [Change the assigned parent location](/docs/api/rest/reference/zoom-rooms/methods/#operation/changeParentLocation) | `zoom_rooms:update:location:admin` |
| [Change the assigned parent location](/docs/api/rest/reference/zoom-rooms/ma/#operation/changeParentLocation) | `zoom_rooms:update:location:master` |
| [List Zoom Room locations](/docs/api/rest/reference/zoom-rooms/methods/#operation/listZRLocations) | `zoom_rooms:read:list_locations:admin` |
| [List Zoom Room locations](/docs/api/rest/reference/zoom-rooms/ma/#operation/listZRLocations) | `zoom_rooms:read:list_locations:master` |
| [Update location settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateZRLocationSettings) | `zoom_rooms:update:location_settings:admin` |
| [Update location settings](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateZRLocationSettings) | `zoom_rooms:update:location_settings:master` |
| [Get location settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRLocationSettings) | `zoom_rooms:read:location_settings:admin` |
| [Get location settings](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRLocationSettings) | `zoom_rooms:read:location_settings:master` |
| [Update Zoom Room location profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateZRLocationProfile) | `zoom_rooms:update:location:admin` |
| [Update Zoom Room location profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateZRLocationProfile) | `zoom_rooms:update:location:master` |
| [Get Zoom Room location profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRLocationProfile) | `zoom_rooms:read:location:admin` |
| [Get Zoom Room location profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRLocationProfile) | `zoom_rooms:read:location:master` |

### Zoom Rooms Tags

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Assign Tags to Zoom Rooms By Location ID](/docs/api/rest/reference/zoom-rooms/methods/#operation/AssignTagsToZoomRoomsByLocationID) | `zoom_rooms:update:room_tag:admin` |
| [List all Zoom Room Tags](/docs/api/rest/reference/zoom-rooms/methods/#operation/listZoomRoomTags) | `zoom_rooms:read:list_tags:admin` |
| [Assign Tags to a Zoom Room](/docs/api/rest/reference/zoom-rooms/methods/#operation/AssignTagsToAZoomRoom) | `zoom_rooms:update:room_tag:admin` |
| [Create a new Zoom Rooms Tag](/docs/api/rest/reference/zoom-rooms/methods/#operation/createZoomRoomTag) | `zoom_rooms:write:tag:admin` |
| [Delete Tag](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteZoomRoomTag) | `zoom_rooms:delete:tag:admin` |
| [Un-assign Tags from a Zoom Room](/docs/api/rest/reference/zoom-rooms/methods/#operation/unassignZoomRoomTag) | `zoom_rooms:delete:room_tag:admin` |
| [Edit Tag](/docs/api/rest/reference/zoom-rooms/methods/#operation/editZoomRoomTag) | `zoom_rooms:update:tag:admin` |

## Zoom Scheduler


### Routing Forms

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [get routing response](/docs/api/rest/reference/phone/methods/#operation/Getroutingresponse) | `scheduler:read:routing`, `scheduler:read:routing:admin` |

### analytics

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Report analytics](/docs/api/rest/reference/phone/methods/#operation/report_analytics) | `scheduler:read:analytics`, `scheduler:read:analytics:admin` |

### availability

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get availability](/docs/api/rest/reference/phone/methods/#operation/get_availability) | `scheduler:read:availability`, `scheduler:read:availability:admin` |
| [Patch availability](/docs/api/rest/reference/phone/methods/#operation/patch_availability) | `scheduler:update:availability`, `scheduler:update:availability:admin` |
| [Insert availability](/docs/api/rest/reference/phone/methods/#operation/insert_availability) | `scheduler:write:availability`, `scheduler:write:availability:admin` |
| [Delete availability](/docs/api/rest/reference/phone/methods/#operation/delete_availability) | `scheduler:delete:availability`, `scheduler:delete:availability:admin` |
| [List availability](/docs/api/rest/reference/phone/methods/#operation/list_availability) | `scheduler:read:list_availability`, `scheduler:read:list_availability:admin` |

### scheduled events

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Patch scheduled events](/docs/api/rest/reference/phone/methods/#operation/patch_scheduled_events) | `scheduler:update:scheduled_event`, `scheduler:update:scheduled_event:admin` |
| [Get scheduled events](/docs/api/rest/reference/phone/methods/#operation/get_scheduled_events) | `scheduler:read:scheduled_event`, `scheduler:read:scheduled_event:admin` |
| [Get scheduled event attendee](/docs/api/rest/reference/phone/methods/#operation/get_scheduled_event_attendee) | `scheduler:read:scheduled_event_attendee`, `scheduler:read:scheduled_event_attendee:admin` |
| [List scheduled events](/docs/api/rest/reference/phone/methods/#operation/list_scheduled_events) | `scheduler:read:list_scheduled_events`, `scheduler:read:list_scheduled_events:admin` |
| [Delete scheduled events](/docs/api/rest/reference/phone/methods/#operation/delete_scheduled_events) | `scheduler:delete:scheduled_event`, `scheduler:delete:scheduled_event:admin` |

### schedules

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List schedules](/docs/api/rest/reference/phone/methods/#operation/list_schedules) | `scheduler:read:list_schedule`, `scheduler:read:list_schedule:admin` |
| [Patch schedules](/docs/api/rest/reference/phone/methods/#operation/patch_schedule) | `scheduler:update:patch_schedule`, `scheduler:update:patch_schedule:admin` |
| [Insert schedules](/docs/api/rest/reference/phone/methods/#operation/insert_schedule) | `scheduler:write:insert_schedule`, `scheduler:write:insert_schedule:admin` |
| [Get schedules](/docs/api/rest/reference/phone/methods/#operation/get_schedule) | `scheduler:read:get_schedule`, `scheduler:read:get_schedule:admin` |
| [Delete schedules](/docs/api/rest/reference/phone/methods/#operation/delete_schedules) | `scheduler:delete:delete_schedule`, `scheduler:delete:delete_schedule:admin` |

### scheduling links

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Single use link](/docs/api/rest/reference/phone/methods/#operation/single_use_link) | `scheduler:write:single_use_link`, `scheduler:write:single_use_link:admin` |

### shares

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create shares](/docs/api/rest/reference/phone/methods/#operation/create_shares) | `scheduler:write:share`, `scheduler:write:share:admin` |

### team

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List team](/docs/api/rest/reference/phone/methods/#operation/Listteam) | `scheduler:read:get_schedule`, `scheduler:read:get_schedule:admin` |

### users

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get user](/docs/api/rest/reference/phone/methods/#operation/get_user) | `scheduler:read:user`, `scheduler:read:user:admin` |

## Zoom User


### Divisions

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Create a division](/docs/api/rest/reference/user/methods/#operation/Createadivision) | `division:write:division:admin` |
| [Get a division](/docs/api/rest/reference/user/methods/#operation/Getdivision) | `division:read:division:admin` |
| [List divisions](/docs/api/rest/reference/user/methods/#operation/listDivisions) | `division:read:list_divisions:admin` |
| [List division members](/docs/api/rest/reference/user/methods/#operation/listDivisionMembers) | `division:read:member:admin` |
| [Delete a division](/docs/api/rest/reference/user/methods/#operation/Deletedivision) | `division:delete:division:admin` |
| [Assign a division](/docs/api/rest/reference/user/methods/#operation/assigndivisionMember) | `division:write:member:admin` |
| [Update a division](/docs/api/rest/reference/user/methods/#operation/Updateadivision) | `division:update:division:admin` |

### Groups

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete Virtual Background files](/docs/api/rest/reference/user/methods/#operation/delGroupVB) | `group:delete:virtual_background_files:admin` |
| [Delete Virtual Background files](/docs/api/rest/reference/user/ma/#operation/delGroupVB) | `group:delete:virtual_background_files:master` |
| [Upload Virtual Background files](/docs/api/rest/reference/user/methods/#operation/uploadGroupVB) | `group:write:virtual_background_files:admin` |
| [Upload Virtual Background files](/docs/api/rest/reference/user/ma/#operation/uploadGroupVB) | `group:write:virtual_background_files:master` |
| [List group channels](/docs/api/rest/reference/user/methods/#operation/groupChannels) | `group:read:list_channels:admin` |
| [List group channels](/docs/api/rest/reference/user/ma/#operation/groupChannels) | `group:read:list_channels:master` |
| [Add group members](/docs/api/rest/reference/user/methods/#operation/groupMembersCreate) | `group:write:member:admin` |
| [Add group members](/docs/api/rest/reference/user/ma/#operation/groupMembersCreate) | `group:write:member:master` |
| [Delete a group admin](/docs/api/rest/reference/user/methods/#operation/groupAdminsDelete) | `group:delete:administrator:admin` |
| [Delete a group admin](/docs/api/rest/reference/user/ma/#operation/groupAdminsDelete) | `group:delete:administrator:master` |
| [Update a group](/docs/api/rest/reference/user/methods/#operation/groupUpdate) | `group:update:group:admin` |
| [Update a group](/docs/api/rest/reference/user/ma/#operation/groupUpdate) | `group:update:group:master` |
| [Update locked settings](/docs/api/rest/reference/user/methods/#operation/groupLockedSettings) | `group:update:lock_settings:admin` |
| [Update locked settings](/docs/api/rest/reference/user/ma/#operation/groupLockedSettings) | `group:update:lock_settings:master` |
| [Create a group](/docs/api/rest/reference/user/methods/#operation/groupCreate) | `group:write:group:admin` |
| [Create a group](/docs/api/rest/reference/user/ma/#operation/groupCreate) | `group:write:group:master` |
| [Get locked settings](/docs/api/rest/reference/user/methods/#operation/getGroupLockSettings) | `group:read:lock_settings:admin` |
| [Get locked settings](/docs/api/rest/reference/user/ma/#operation/getGroupLockSettings) | `group:read:lock_settings:master` |
| [Update a group's settings](/docs/api/rest/reference/user/methods/#operation/updateGroupSettings) | `group:update:settings:admin` |
| [Update a group's settings](/docs/api/rest/reference/user/ma/#operation/updateGroupSettings) | `group:update:settings:master` |
| [Update a group's webinar registration settings](/docs/api/rest/reference/user/methods/#operation/groupSettingsRegistrationUpdate) | `group:update:registration_settings:admin` |
| [Update a group's webinar registration settings](/docs/api/rest/reference/user/ma/#operation/groupSettingsRegistrationUpdate) | `group:update:registration_settings:master` |
| [List group admins](/docs/api/rest/reference/user/methods/#operation/groupAdmins) | `group:read:administrator:admin` |
| [List group admins](/docs/api/rest/reference/user/ma/#operation/groupAdmins) | `group:read:administrator:master` |
| [Delete a group member](/docs/api/rest/reference/user/methods/#operation/groupMembersDelete) | `group:delete:member:admin` |
| [Delete a group member](/docs/api/rest/reference/user/ma/#operation/groupMembersDelete) | `group:delete:member:master` |
| [List groups](/docs/api/rest/reference/user/methods/#operation/groups) | `group:read:list_groups:admin` |
| [List groups](/docs/api/rest/reference/user/ma/#operation/groups) | `group:read:list_groups:master` |
| [Get a group](/docs/api/rest/reference/user/methods/#operation/group) | `group:read:group:admin` |
| [Get a group](/docs/api/rest/reference/user/ma/#operation/group) | `group:read:group:master` |
| [Get a group's settings](/docs/api/rest/reference/user/methods/#operation/getGroupSettings) | `group:read:settings:admin` |
| [Get a group's settings](/docs/api/rest/reference/user/ma/#operation/getGroupSettings) | `group:read:settings:master` |
| [Add group admins](/docs/api/rest/reference/user/methods/#operation/groupAdminsCreate) | `group:write:administrator:admin` |
| [List group members](/docs/api/rest/reference/user/methods/#operation/groupMembers) | `group:read:list_members:admin` |
| [List group members](/docs/api/rest/reference/user/ma/#operation/groupMembers) | `group:read:list_members:master` |
| [Update a group member](/docs/api/rest/reference/user/methods/#operation/updateAGroupMember) | `group:update:member:admin` |
| [Update a group member](/docs/api/rest/reference/user/ma/#operation/updateAGroupMember) | `group:update:member:master` |
| [Delete a group](/docs/api/rest/reference/user/methods/#operation/groupDelete) | `group:delete:group:admin` |
| [Delete a group](/docs/api/rest/reference/user/ma/#operation/groupDelete) | `group:delete:group:master` |
| [Get a group's webinar registration settings](/docs/api/rest/reference/user/methods/#operation/groupSettingsRegistration) | `group:read:registration_settings:admin` |
| [Get a group's webinar registration settings](/docs/api/rest/reference/user/ma/#operation/groupSettingsRegistration) | `group:read:registration_settings:master` |

### Users

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List a user's collaboration devices](/docs/api/rest/reference/user/methods/#operation/listCollaborationDevices) | `user:read:list_collaboration_devices`, `user:read:list_collaboration_devices:admin` |
| [Get meeting summary templates](/docs/api/rest/reference/user/methods/#operation/Getmeetingsummarytemplates) | `user:read:settings`, `user:read:settings:admin` |
| [Get user permissions](/docs/api/rest/reference/user/methods/#operation/userPermission) | `user:read:list_permissions`, `user:read:list_permissions:admin` |
| [Get user permissions](/docs/api/rest/reference/user/ma/#operation/userPermission) | `user:read:list_permissions:master` |
| [Delete a scheduler](/docs/api/rest/reference/user/methods/#operation/userSchedulerDelete) | `user:delete:scheduler`, `user:delete:scheduler:admin` |
| [Delete a scheduler](/docs/api/rest/reference/user/ma/#operation/userSchedulerDelete) | `user:delete:scheduler:master` |
| [Get user settings](/docs/api/rest/reference/user/methods/#operation/userSettings) | `user:read:settings`, `user:read:settings:admin` |
| [Get user settings](/docs/api/rest/reference/user/ma/#operation/userSettings) | `user:read:settings:master` |
| [Add assistants](/docs/api/rest/reference/user/methods/#operation/userAssistantCreate) | `user:write:assistant`, `user:write:assistant:admin` |
| [Add assistants](/docs/api/rest/reference/user/ma/#operation/userAssistantCreate) | `user:write:assistant:master` |
| [Update a user's presence status](/docs/api/rest/reference/user/methods/#operation/updatePresenceStatus) | `user:update:presence_status`, `user:update:presence_status:admin` |
| [Get a user](/docs/api/rest/reference/user/methods/#operation/user) | `user:read:user`, `user:read:user:admin` |
| [Get a user](/docs/api/rest/reference/user/ma/#operation/user) | `user:read:user:master` |
| [Upload a user's profile picture](/docs/api/rest/reference/user/methods/#operation/userPicture) | `user:write:profile_picture`, `user:write:profile_picture:admin` |
| [Upload a user's profile picture](/docs/api/rest/reference/user/ma/#operation/userPicture) | `user:write:profile_picture:master` |
| [Update user status](/docs/api/rest/reference/user/methods/#operation/userStatus) | `user:update:status`, `user:update:status:admin` |
| [Update user status](/docs/api/rest/reference/user/ma/#operation/userStatus) | `user:update:status:master` |
| [Get user summary](/docs/api/rest/reference/user/methods/#operation/userSummary) | `user:read:summary:admin` |
| [Get user summary](/docs/api/rest/reference/user/ma/#operation/userSummary) | `user:read:summary:master` |
| [Delete user schedulers](/docs/api/rest/reference/user/methods/#operation/userSchedulersDelete) | `user:delete:scheduler`, `user:delete:scheduler:admin` |
| [Delete user schedulers](/docs/api/rest/reference/user/ma/#operation/userSchedulersDelete) | `user:delete:scheduler:master` |
| [Get a user presence status](/docs/api/rest/reference/user/methods/#operation/getUserPresenceStatus) | `user:read:presence_status`, `user:read:presence_status:admin` |
| [List user schedulers](/docs/api/rest/reference/user/methods/#operation/userSchedulers) | `user:read:list_schedulers`, `user:read:list_schedulers:admin` |
| [List user schedulers](/docs/api/rest/reference/user/ma/#operation/userSchedulers) | `user:read:list_schedulers:master` |
| [Delete a user assistant](/docs/api/rest/reference/user/methods/#operation/userAssistantDelete) | `user:delete:assistant`, `user:delete:assistant:admin` |
| [Delete a user assistant](/docs/api/rest/reference/user/ma/#operation/userAssistantDelete) | `user:delete:assistant:master` |
| [Delete user assistants](/docs/api/rest/reference/user/methods/#operation/userAssistantsDelete) | `user:delete:assistant`, `user:delete:assistant:admin` |
| [Delete user assistants](/docs/api/rest/reference/user/ma/#operation/userAssistantsDelete) | `user:delete:assistant:master` |
| [List user assistants](/docs/api/rest/reference/user/methods/#operation/userAssistants) | `user:read:list_assistants`, `user:read:list_assistants:admin` |
| [List user assistants](/docs/api/rest/reference/user/ma/#operation/userAssistants) | `user:read:list_assistants:master` |
| [Delete a user](/docs/api/rest/reference/user/methods/#operation/userDelete) | `user:delete:user`, `user:delete:user:admin` |
| [Delete a user](/docs/api/rest/reference/user/ma/#operation/userDelete) | `user:delete:user:master` |
| [Get the user's ZAK](/docs/api/rest/reference/user/methods/#operation/userZak) | `user:read:zak`, `user:read:zak:admin` |
| [Update a user's email](/docs/api/rest/reference/user/methods/#operation/userEmailUpdate) | `user:update:email`, `user:update:email:admin` |
| [Update a user's email](/docs/api/rest/reference/user/ma/#operation/userEmailUpdate) | `user:update:email:master` |
| [List users](/docs/api/rest/reference/user/methods/#operation/users) | `user:read:list_users:admin` |
| [List users](/docs/api/rest/reference/user/ma/#operation/users) | `user:read:list_users:master` |
| [Revoke a user's SSO token](/docs/api/rest/reference/user/methods/#operation/userSSOTokenDelete) | `user:delete:token`, `user:delete:token:admin` |
| [Revoke a user's SSO token](/docs/api/rest/reference/user/ma/#operation/userSSOTokenDelete) | `user:delete:token:master` |
| [Update a user](/docs/api/rest/reference/user/methods/#operation/userUpdate) | `user:update:user`, `user:update:user:admin` |
| [Update a user](/docs/api/rest/reference/user/ma/#operation/userUpdate) | `user:update:user:master` |
| [Delete Virtual Background files](/docs/api/rest/reference/user/methods/#operation/delUserVB) | `user:delete:virtual_background_files`, `user:delete:virtual_background_files:admin` |
| [Delete Virtual Background files](/docs/api/rest/reference/user/ma/#operation/delUserVB) | `user:delete:virtual_background_files:master` |
| [Upload Virtual Background files](/docs/api/rest/reference/user/methods/#operation/uploadVBuser) | `user:write:virtual_background_files`, `user:write:virtual_background_files:admin` |
| [Upload Virtual Background files](/docs/api/rest/reference/user/ma/#operation/uploadVBuser) | `user:write:virtual_background_files:master` |
| [Get a user's token](/docs/api/rest/reference/user/methods/#operation/userToken) | `user:read:token`, `user:read:token:admin` |
| [Get a user's token](/docs/api/rest/reference/user/ma/#operation/userToken) | `user:read:token:master` |
| [Bulk update features for users](/docs/api/rest/reference/user/methods/#operation/bulkUpdateFeature) | `user:write:feature:admin` |
| [Bulk update features for users](/docs/api/rest/reference/user/ma/#operation/bulkUpdateFeature) | `user:write:feature:master` |
| [Update user settings](/docs/api/rest/reference/user/methods/#operation/userSettingsUpdate) | `user:update:settings`, `user:update:settings:admin` |
| [Update user settings](/docs/api/rest/reference/user/ma/#operation/userSettingsUpdate) | `user:update:settings:master` |
| [Create users](/docs/api/rest/reference/user/methods/#operation/userCreate) | `user:write:user:admin` |
| [Create users](/docs/api/rest/reference/user/ma/#operation/userCreate) | `user:write:user:master` |
| [Get collaboration device detail](/docs/api/rest/reference/user/methods/#operation/getCollaborationDevice) | `user:read:collaboration_device`, `user:read:collaboration_device:admin` |
| [Check a user's PM room](/docs/api/rest/reference/user/methods/#operation/userVanityName) | `user:read:pm_room`, `user:read:pm_room:admin` |
| [Update a user's password](/docs/api/rest/reference/user/methods/#operation/userPassword) | `user:update:password`, `user:update:password:admin` |
| [Update a user's password](/docs/api/rest/reference/user/ma/#operation/userPassword) | `user:update:password:master` |
| [Check a user email](/docs/api/rest/reference/user/methods/#operation/userEmail) | `user:read:email`, `user:read:email:admin` |

## Zoom Video Management


### Channels

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Update channel](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/UpdateVideoChannel) | `video_mgmt:update:channel`, `video_mgmt:update:channel:admin` |
| [List channels](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/listVideoChannels) | `video_mgmt:read:list_channels`, `video_mgmt:read:list_channels:admin` |
| [Get channel details](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/getChannelDetail) | `video_mgmt:read:channel`, `video_mgmt:read:channel:admin` |
| [Channel actions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/channelActions) | `video_mgmt:update:channel`, `video_mgmt:update:channel:admin` |
| [Create a channel](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/createChannel) | `video_mgmt:write:channel`, `video_mgmt:write:channel:admin` |
| [Delete channel](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeleteChannel) | `video_mgmt:delete:channel`, `video_mgmt:delete:channel:admin` |

### Permissions

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List channel permissions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/listChannelPermissions) | `video_mgmt:read:list_permissions`, `video_mgmt:read:list_permissions:admin` |
| [Update channel permissions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/updateChannelPermissions) | `video_mgmt:update:permissions`, `video_mgmt:update:permissions:admin` |
| [Create channel permissions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/createChannelPermissions) | `video_mgmt:write:permissions`, `video_mgmt:write:permissions:admin` |
| [Delete channel permissions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeleteChannelPermissions) | `video_mgmt:delete:permissions`, `video_mgmt:delete:permissions:admin` |

### Playlists

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Delete playlist](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeletePlaylist) | `video_mgmt:delete:playlist`, `video_mgmt:delete:playlist:admin` |
| [Add channel playlists](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/AddChannelPlaylists) | `video_mgmt:write:channel_playlists`, `video_mgmt:write:channel_playlists:admin` |
| [List playlists](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListPlaylists) | `video_mgmt:read:list_playlists`, `video_mgmt:read:list_playlists:admin` |
| [List channel playlists](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListChannelPlaylists) | `video_mgmt:read:list_channel_playlists`, `video_mgmt:read:list_channel_playlists:admin` |
| [Create a playlist](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/createPlaylist) | `video_mgmt:write:playlist`, `video_mgmt:write:playlist:admin` |
| [Delete channel playlists](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeleteChannelPlaylists) | `video_mgmt:delete:channel_playlists`, `video_mgmt:delete:channel_playlists:admin` |
| [Update playlist](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/UpdatePlaylist) | `video_mgmt:update:playlist`, `video_mgmt:update:playlist:admin` |

### Videos

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [List playlist videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListPlaylistVideos) | `video_mgmt:read:list_playlist_videos`, `video_mgmt:read:list_playlist_videos:admin` |
| [Delete playlist videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeletePlaylistVideos) | `video_mgmt:delete:playlist_videos`, `video_mgmt:delete:playlist_videos:admin` |
| [Add playlist videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/AddPlaylistVideos) | `video_mgmt:write:playlist_videos`, `video_mgmt:write:playlist_videos:admin` |
| [List all videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListAllVideos) | `video_mgmt:read:list_videos`, `video_mgmt:read:list_videos:admin` |
| [Add channel videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/AddChannelVideos) | `video_mgmt:write:channel_videos`, `video_mgmt:write:channel_videos:admin` |
| [List channel videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListChannelVideos) | `video_mgmt:read:list_channel_videos`, `video_mgmt:read:list_channel_videos:admin` |
| [Delete channel videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeleteChannelVideos) | `video_mgmt:delete:channel_videos`, `video_mgmt:delete:channel_videos:admin` |

### files

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Upload file for video management](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/uploadVODtFile) | `video_mgmt:write:file`, `video_mgmt:write:file:admin` |

## Zoom Virtual Agent


### Knowledge Management

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get articles](/docs/api/rest/reference/virtual-agent/methods/#operation/GetArticles) | `zva:read:list_km_articles`, `zva:read:list_km_articles:admin` |
| [Get sync](/docs/api/rest/reference/virtual-agent/methods/#operation/GetSync) | `zva:read:km_kb:admin` |
| [Get article](/docs/api/rest/reference/virtual-agent/methods/#operation/GetArticle) | `zva:read:km_article`, `zva:read:km_article:admin` |
| [Delete article](/docs/api/rest/reference/virtual-agent/methods/#operation/DeleteArticle) | `zva:delete:km_article`, `zva:delete:km_article:admin` |
| [Create sync request](/docs/api/rest/reference/virtual-agent/methods/#operation/CreateSyncRequest) | `zva:update:km_kb:admin` |
| [Update article](/docs/api/rest/reference/virtual-agent/methods/#operation/UpdateArticle) | `zva:update:km_article`, `zva:update:km_article:admin` |
| [Create article](/docs/api/rest/reference/virtual-agent/methods/#operation/CreateArticle) | `zva:write:km_article`, `zva:write:km_article:admin` |

### Report

| API Endpoint | Granular Scopes |
|--------------|-----------------|
| [Get ZVA engagements](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVAEngagements) | `zva:read:list_engagements:admin` |
| [Get ZVA query details](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVAQueryDetails) | `zva:read:list_queries:admin` |
| [Get ZVA Surveys](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVASurveys) | `zva:read:list_surveys:admin` |
| [Get ZVA variable details](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVAengagementvariabledetails) | `zva:read:list_variables:admin` |
| [Get ZVA transcripts](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVATranscripts) | `zva:read:list_transcripts:admin` |