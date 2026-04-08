# Zoom Meetings API

Authoritative endpoint inventory for Meetings. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/meetings/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 183 |
| Path templates | 128 |
| Tags | 19 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Archiving | 6 |
| Cloud Recording | 17 |
| Devices | 13 |
| H323 Devices | 4 |
| In-Meeting Apps | 2 |
| In-Meeting Features | 5 |
| Invitation & Registration | 10 |
| Live streaming | 4 |
| Meetings | 13 |
| PAC | 1 |
| Polls | 7 |
| Reports | 23 |
| SIP Phone | 4 |
| Summaries | 3 |
| Surveys | 3 |
| Templates | 2 |
| Tracking Field | 5 |
| TSP | 8 |
| Webinars | 53 |

## Endpoints by Tag

### Archiving

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/archive_files` | List archived files | `listArchivedFiles` |
| GET | `/archive_files/statistics` | Get archived file statistics | `getArchivedFileStatistics` |
| PATCH | `/archive_files/{fileId}` | Update an archived file's auto-delete status | `updateArchivedFile` |
| GET | `/meetings/{meetingId}/jointoken/local_archiving` | Get a meeting's archive token for local archiving | `meetingLocalArchivingArchiveToken` |
| DELETE | `/past_meetings/{meetingUUID}/archive_files` | Delete a meeting's archived files | `deleteArchivedFiles` |
| GET | `/past_meetings/{meetingUUID}/archive_files` | Get a meeting's archived files | `getArchivedFiles` |

### Cloud Recording

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/meetings/{meetingId}/recordings` | Delete meeting or webinar recordings | `recordingDelete` |
| GET | `/meetings/{meetingId}/recordings` | Get meeting recordings | `recordingGet` |
| GET | `/meetings/{meetingId}/recordings/analytics_details` | Get a meeting or webinar recording's analytics details | `analytics_details` |
| GET | `/meetings/{meetingId}/recordings/analytics_summary` | Get a meeting or webinar recording's analytics summary | `analytics_summary` |
| GET | `/meetings/{meetingId}/recordings/registrants` | List recording registrants | `meetingRecordingRegistrants` |
| POST | `/meetings/{meetingId}/recordings/registrants` | Create a recording registrant | `meetingRecordingRegistrantCreate` |
| GET | `/meetings/{meetingId}/recordings/registrants/questions` | Get registration questions | `recordingRegistrantsQuestionsGet` |
| PATCH | `/meetings/{meetingId}/recordings/registrants/questions` | Update registration questions | `recordingRegistrantQuestionUpdate` |
| PUT | `/meetings/{meetingId}/recordings/registrants/status` | Update a registrant's status | `meetingRecordingRegistrantStatus` |
| GET | `/meetings/{meetingId}/recordings/settings` | Get meeting recording settings | `recordingSettingUpdate` |
| PATCH | `/meetings/{meetingId}/recordings/settings` | Update meeting recording settings | `recordingSettingsUpdate` |
| DELETE | `/meetings/{meetingId}/recordings/{recordingId}` | Delete a recording file for a meeting or webinar | `recordingDeleteOne` |
| PUT | `/meetings/{meetingId}/recordings/{recordingId}/status` | Recover a single recording | `recordingStatusUpdateOne` |
| DELETE | `/meetings/{meetingId}/transcript` | Delete a meeting or webinar transcript | `DeleteMeetingTranscript` |
| GET | `/meetings/{meetingId}/transcript` | Get a meeting transcript | `GetMeetingTranscript` |
| PUT | `/meetings/{meetingUUID}/recordings/status` | Recover meeting recordings | `recordingStatusUpdate` |
| GET | `/users/{userId}/recordings` | List all recordings | `recordingsList` |

### Devices

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/devices` | List devices | `listDevices` |
| POST | `/devices` | Add a new device | `addDevice` |
| GET | `/devices/groups` | Get ZDM group info | `Getzdmgroupinfo` |
| POST | `/devices/zpa/assignment` | Assign a device to a user or commonarea | `Assigndevicetoauser/commonarea` |
| GET | `/devices/zpa/settings` | Get Zoom Phone Appliance settings by user ID | `GetZpaDeviceListProfileSettingOfaUser` |
| POST | `/devices/zpa/upgrade` | Upgrade ZPA firmware or app | `UpgradeZpas/app` |
| DELETE | `/devices/zpa/vendors/{vendor}/mac_addresses/{macAddress}` | Delete ZPA device by vendor and mac address | `DeleteZpaDeviceByVendorAndMacAddress` |
| GET | `/devices/zpa/zdm_groups/{zdmGroupId}/versions` | Get ZPA version info | `GetZpaVersioninfo` |
| DELETE | `/devices/{deviceId}` | Delete device | `deleteDevice` |
| GET | `/devices/{deviceId}` | Get device detail | `getDevice` |
| PATCH | `/devices/{deviceId}` | Change device | `updateDevice` |
| PATCH | `/devices/{deviceId}/assign_group` | Assign a device to a group | `assginGroup` |
| PATCH | `/devices/{deviceId}/assignment` | Change device association | `changeDeviceAssociation` |

### H323 Devices

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/h323/devices` | List H.323/SIP devices | `deviceList` |
| POST | `/h323/devices` | Create a H.323/SIP device | `deviceCreate` |
| DELETE | `/h323/devices/{deviceId}` | Delete a H.323/SIP device | `deviceDelete` |
| PATCH | `/h323/devices/{deviceId}` | Update a H.323/SIP device | `deviceUpdate` |

### In-Meeting Apps

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/meetings/{meetingId}/open_apps` | Delete a meeting app | `meetingAppDelete` |
| POST | `/meetings/{meetingId}/open_apps` | Add a meeting app | `meetingAppAdd` |

### In-Meeting Features

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/live_meetings/{meetingId}/chat/messages/{messageId}` | Delete a live meeting message | `deleteMeetingChatMessageById` |
| PATCH | `/live_meetings/{meetingId}/chat/messages/{messageId}` | Update a live meeting message | `updateMeetingChatMessageById` |
| PATCH | `/live_meetings/{meetingId}/events` | In-meeting controls | `inMeetingControl` |
| GET | `/meetings/{meetingId}/jointoken/local_recording` | Get a meeting's join token for local recording | `meetingLocalRecordingJoinToken` |
| GET | `/meetings/{meetingId}/token` | Get meeting's token | `meetingToken` |

### Invitation & Registration

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/meetings/{meetingId}/batch_registrants` | Perform batch registration | `addBatchRegistrants` |
| GET | `/meetings/{meetingId}/invitation` | Get meeting invitation | `meetingInvitation` |
| POST | `/meetings/{meetingId}/invite_links` | Create a meeting's invite links | `meetingInviteLinksCreate` |
| GET | `/meetings/{meetingId}/registrants` | List meeting registrants | `meetingRegistrants` |
| POST | `/meetings/{meetingId}/registrants` | Add a meeting registrant | `meetingRegistrantCreate` |
| GET | `/meetings/{meetingId}/registrants/questions` | List registration questions | `meetingRegistrantsQuestionsGet` |
| PATCH | `/meetings/{meetingId}/registrants/questions` | Update registration questions | `meetingRegistrantQuestionUpdate` |
| PUT | `/meetings/{meetingId}/registrants/status` | Update registrant's status | `meetingRegistrantStatus` |
| DELETE | `/meetings/{meetingId}/registrants/{registrantId}` | Delete a meeting registrant | `meetingregistrantdelete` |
| GET | `/meetings/{meetingId}/registrants/{registrantId}` | Get a meeting registrant | `meetingRegistrantGet` |

### Live streaming

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/meetings/{meetingId}/jointoken/live_streaming` | Get a meeting's join token for live streaming | `meetingLiveStreamingJoinToken` |
| GET | `/meetings/{meetingId}/livestream` | Get livestream details | `getMeetingLiveStreamDetails` |
| PATCH | `/meetings/{meetingId}/livestream` | Update a livestream | `meetingLiveStreamUpdate` |
| PATCH | `/meetings/{meetingId}/livestream/status` | Update livestream status | `meetingLiveStreamStatusUpdate` |

### Meetings

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| PATCH | `/live_meetings/{meetingId}/rtms_app/status` | Update participant Real-Time Media Streams (RTMS) app status | `meetingRTMSStatusUpdate` |
| DELETE | `/meetings/{meetingId}` | Delete a meeting | `meetingDelete` |
| GET | `/meetings/{meetingId}` | Get a meeting | `meeting` |
| PATCH | `/meetings/{meetingId}` | Update a meeting | `meetingUpdate` |
| POST | `/meetings/{meetingId}/sip_dialing` | Get a meeting SIP URI with passcode | `getSipDialingWithPasscode` |
| PUT | `/meetings/{meetingId}/status` | Update meeting status | `meetingStatus` |
| GET | `/past_meetings/{meetingId}` | Get past meeting details | `pastMeetingDetails` |
| GET | `/past_meetings/{meetingId}/instances` | List past meeting instances | `pastMeetings` |
| GET | `/past_meetings/{meetingId}/participants` | Get past meeting participants | `pastMeetingParticipants` |
| GET | `/past_meetings/{meetingId}/qa` | List past meetings' Q&A | `listPastMeetingQA` |
| GET | `/users/{userId}/meetings` | List meetings | `meetings` |
| POST | `/users/{userId}/meetings` | Create a meeting | `meetingCreate` |
| GET | `/users/{userId}/upcoming_meetings` | List upcoming meetings | `listUpcomingMeeting` |

### PAC

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/users/{userId}/pac` | List a user's PAC accounts | `userPACs` |

### Polls

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/meetings/{meetingId}/batch_polls` | Perform batch poll creation | `createBatchPolls` |
| GET | `/meetings/{meetingId}/polls` | List meeting polls | `meetingPolls` |
| POST | `/meetings/{meetingId}/polls` | Create a meeting poll | `meetingPollCreate` |
| DELETE | `/meetings/{meetingId}/polls/{pollId}` | Delete a meeting poll | `meetingPollDelete` |
| GET | `/meetings/{meetingId}/polls/{pollId}` | Get a meeting poll | `meetingPollGet` |
| PUT | `/meetings/{meetingId}/polls/{pollId}` | Update a meeting poll | `meetingPollUpdate` |
| GET | `/past_meetings/{meetingId}/polls` | List past meeting's poll results | `listPastMeetingPolls` |

### Reports

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/report/activities` | Get sign In / sign out activity report | `reportSignInSignOutActivities` |
| GET | `/report/billing` | Get billing reports | `getBillingReport` |
| GET | `/report/billing/invoices` | Get billing invoice reports | `getBillingInvoicesReports` |
| GET | `/report/cloud_recording` | Get cloud recording usage report | `reportCloudRecording` |
| GET | `/report/daily` | Get daily usage report | `reportDaily` |
| GET | `/report/history_meetings` | Get history meeting and webinar list | `Gethistorymeetingandwebinarlist` |
| GET | `/report/meeting_activities` | Get a meeting activities report | `reportMeetingactivitylogs` |
| GET | `/report/meetings/{meetingId}` | Get meeting detail reports | `reportMeetingDetails` |
| GET | `/report/meetings/{meetingId}/participants` | Get meeting participant reports | `reportMeetingParticipants` |
| GET | `/report/meetings/{meetingId}/polls` | Get meeting poll reports | `reportMeetingPolls` |
| GET | `/report/meetings/{meetingId}/qa` | Get meeting Q&A report | `reportMeetingQA` |
| GET | `/report/meetings/{meetingId}/survey` | Get meeting survey report | `reportMeetingSurvey` |
| GET | `/report/operationlogs` | Get operation logs report | `reportOperationLogs` |
| GET | `/report/remote_support` | Get remote support report | `Getremotesupportreport` |
| GET | `/report/telephone` | Get telephone reports | `reportTelephone` |
| GET | `/report/upcoming_events` | Get upcoming events report | `reportUpcomingEvents` |
| GET | `/report/users` | Get active or inactive host reports | `reportUsers` |
| GET | `/report/users/{userId}/meetings` | Get meeting reports | `reportMeetings` |
| GET | `/report/webinars/{webinarId}` | Get webinar detail reports | `reportWebinarDetails` |
| GET | `/report/webinars/{webinarId}/participants` | Get webinar participant reports | `reportWebinarParticipants` |
| GET | `/report/webinars/{webinarId}/polls` | Get webinar poll reports | `reportWebinarPolls` |
| GET | `/report/webinars/{webinarId}/qa` | Get webinar Q&A report | `reportWebinarQA` |
| GET | `/report/webinars/{webinarId}/survey` | Get webinar survey report | `reportWebinarSurvey` |

### SIP Phone

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/sip_phones/phones` | List SIP phones | `ListSIPPhonePhones` |
| POST | `/sip_phones/phones` | Enable SIP phone | `EnableSIPPhonePhones` |
| DELETE | `/sip_phones/phones/{phoneId}` | Delete SIP phone | `deleteSIPPhonePhones` |
| PATCH | `/sip_phones/phones/{phoneId}` | Update SIP phone | `UpdateSIPPhonePhones` |

### Summaries

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/meetings/meeting_summaries` | List an account's meeting or webinar summaries | `Listmeetingsummaries` |
| DELETE | `/meetings/{meetingId}/meeting_summary` | Delete a meeting or webinar summary | `Deletemeetingorwebinarsummary` |
| GET | `/meetings/{meetingId}/meeting_summary` | Get a meeting or webinar summary | `Getameetingsummary` |

### Surveys

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/meetings/{meetingId}/survey` | Delete a meeting survey | `meetingSurveyDelete` |
| GET | `/meetings/{meetingId}/survey` | Get a meeting survey | `meetingSurveyGet` |
| PATCH | `/meetings/{meetingId}/survey` | Update a meeting survey | `meetingSurveyUpdate` |

### Templates

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/users/{userId}/meeting_templates` | List meeting templates | `listMeetingTemplates` |
| POST | `/users/{userId}/meeting_templates` | Create a meeting template from an existing meeting | `meetingTemplateCreate` |

### Tracking Field

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/tracking_fields` | List tracking fields | `trackingfieldList` |
| POST | `/tracking_fields` | Create a tracking field | `trackingfieldCreate` |
| DELETE | `/tracking_fields/{fieldId}` | Delete a tracking field | `trackingfieldDelete` |
| GET | `/tracking_fields/{fieldId}` | Get a tracking field | `trackingfieldGet` |
| PATCH | `/tracking_fields/{fieldId}` | Update a tracking field | `trackingfieldUpdate` |

### TSP

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/tsp` | Get account's TSP information | `tsp` |
| PATCH | `/tsp` | Update an account's TSP information | `tspUpdate` |
| GET | `/users/{userId}/tsp` | List user's TSP accounts | `userTSPs` |
| POST | `/users/{userId}/tsp` | Add a user's TSP account | `userTSPCreate` |
| PATCH | `/users/{userId}/tsp/settings` | Set global dial-in URL for a TSP user | `tspUrlUpdate` |
| DELETE | `/users/{userId}/tsp/{tspId}` | Delete a user's TSP account | `userTSPDelete` |
| GET | `/users/{userId}/tsp/{tspId}` | Get a user's TSP account | `userTSP` |
| PATCH | `/users/{userId}/tsp/{tspId}` | Update a TSP account | `userTSPUpdate` |

### Webinars

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/live_webinars/{webinarId}/chat/messages/{messageId}` | Delete a live webinar message | `deleteWebinarChatMessageById` |
| GET | `/past_webinars/{webinarId}/absentees` | Get webinar absentees | `webinarAbsentees` |
| GET | `/past_webinars/{webinarId}/instances` | List past webinar instances | `pastWebinars` |
| GET | `/past_webinars/{webinarId}/participants` | List webinar participants | `listWebinarParticipants` |
| GET | `/past_webinars/{webinarId}/polls` | List past webinar poll results | `listPastWebinarPollResults` |
| GET | `/past_webinars/{webinarId}/qa` | List Q&As of a past webinar | `listPastWebinarQA` |
| GET | `/users/{userId}/webinar_templates` | List webinar templates | `listWebinarTemplates` |
| POST | `/users/{userId}/webinar_templates` | Create a webinar template | `webinarTemplateCreate` |
| GET | `/users/{userId}/webinars` | List webinars | `webinars` |
| POST | `/users/{userId}/webinars` | Create a webinar | `webinarCreate` |
| DELETE | `/webinars/{webinarId}` | Delete a webinar | `webinarDelete` |
| GET | `/webinars/{webinarId}` | Get a webinar | `webinar` |
| PATCH | `/webinars/{webinarId}` | Update a webinar | `webinarUpdate` |
| POST | `/webinars/{webinarId}/batch_registrants` | Perform batch registration | `addBatchWebinarRegistrants` |
| GET | `/webinars/{webinarId}/branding` | Get webinar's session branding | `getWebinarBranding` |
| DELETE | `/webinars/{webinarId}/branding/name_tags` | Delete a webinar's branding name tag | `deleteWebinarBrandingNameTag` |
| POST | `/webinars/{webinarId}/branding/name_tags` | Create a webinar's branding name tag | `createWebinarBrandingNameTag` |
| PATCH | `/webinars/{webinarId}/branding/name_tags/{nameTagId}` | Update a webinar's branding name tag | `updateWebinarBrandingNameTag` |
| DELETE | `/webinars/{webinarId}/branding/virtual_backgrounds` | Delete a webinar's branding virtual backgrounds | `deleteWebinarBrandingVB` |
| PATCH | `/webinars/{webinarId}/branding/virtual_backgrounds` | Set webinar's default branding virtual background | `setWebinarBrandingVB` |
| POST | `/webinars/{webinarId}/branding/virtual_backgrounds` | Upload a webinar's branding virtual background | `uploadWebinarBrandingVB` |
| DELETE | `/webinars/{webinarId}/branding/wallpaper` | Delete a webinar's branding wallpaper | `deleteWebinarBrandingWallpaper` |
| POST | `/webinars/{webinarId}/branding/wallpaper` | Upload a webinar's branding wallpaper | `uploadWebinarBrandingWallpaper` |
| POST | `/webinars/{webinarId}/invite_links` | Create webinar's invite links | `webinarInviteLinksCreate` |
| GET | `/webinars/{webinarId}/jointoken/live_streaming` | Get a webinar's join token for live streaming | `webinarLiveStreamingJoinToken` |
| GET | `/webinars/{webinarId}/jointoken/local_archiving` | Get a webinar's archive token for local archiving | `webinarLocalArchivingArchiveToken` |
| GET | `/webinars/{webinarId}/jointoken/local_recording` | Get a webinar's join token for local recording | `webinarLocalRecordingJoinToken` |
| GET | `/webinars/{webinarId}/livestream` | Get live stream details | `getWebinarLiveStreamDetails` |
| PATCH | `/webinars/{webinarId}/livestream` | Update a live stream | `webinarLiveStreamUpdate` |
| PATCH | `/webinars/{webinarId}/livestream/status` | Update live stream status | `webinarLiveStreamStatusUpdate` |
| DELETE | `/webinars/{webinarId}/panelists` | Remove all panelists | `webinarPanelistsDelete` |
| GET | `/webinars/{webinarId}/panelists` | List panelists | `webinarPanelists` |
| POST | `/webinars/{webinarId}/panelists` | Add panelists | `webinarPanelistCreate` |
| DELETE | `/webinars/{webinarId}/panelists/{panelistId}` | Remove a panelist | `webinarPanelistDelete` |
| GET | `/webinars/{webinarId}/polls` | List a webinar's polls | `webinarPolls` |
| POST | `/webinars/{webinarId}/polls` | Create a webinar's poll | `webinarPollCreate` |
| DELETE | `/webinars/{webinarId}/polls/{pollId}` | Delete a webinar poll | `webinarPollDelete` |
| GET | `/webinars/{webinarId}/polls/{pollId}` | Get a webinar poll | `webinarPollGet` |
| PUT | `/webinars/{webinarId}/polls/{pollId}` | Update a webinar poll | `webinarPollUpdate` |
| GET | `/webinars/{webinarId}/registrants` | List webinar registrants | `webinarRegistrants` |
| POST | `/webinars/{webinarId}/registrants` | Add a webinar registrant | `webinarRegistrantCreate` |
| GET | `/webinars/{webinarId}/registrants/questions` | List registration questions | `webinarRegistrantsQuestionsGet` |
| PATCH | `/webinars/{webinarId}/registrants/questions` | Update registration questions | `webinarRegistrantQuestionUpdate` |
| PUT | `/webinars/{webinarId}/registrants/status` | Update registrant's status | `webinarRegistrantStatus` |
| DELETE | `/webinars/{webinarId}/registrants/{registrantId}` | Delete a webinar registrant | `deleteWebinarRegistrant` |
| GET | `/webinars/{webinarId}/registrants/{registrantId}` | Get a webinar registrant | `webinarRegistrantGet` |
| POST | `/webinars/{webinarId}/sip_dialing` | Get a webinar SIP URI with passcode | `getWebinarSipDialingWithPasscode` |
| PUT | `/webinars/{webinarId}/status` | Update webinar status | `webinarStatus` |
| DELETE | `/webinars/{webinarId}/survey` | Delete a webinar survey | `webinarSurveyDelete` |
| GET | `/webinars/{webinarId}/survey` | Get a webinar survey | `webinarSurveyGet` |
| PATCH | `/webinars/{webinarId}/survey` | Update a webinar survey | `webinarSurveyUpdate` |
| GET | `/webinars/{webinarId}/token` | Get webinar's token | `webinarToken` |
| GET | `/webinars/{webinarId}/tracking_sources` | Get webinar tracking sources | `getTrackingSources` |
