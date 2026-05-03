# Zoom Accounts API

Authoritative endpoint inventory for Accounts. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/accounts/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 59 |
| Path templates | 46 |
| Tags | 6 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Accounts | 11 |
| Dashboards | 26 |
| Data Requests | 5 |
| Information Barriers | 5 |
| Roles | 8 |
| Survey Management | 4 |

## Endpoints by Tag

### Accounts

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/accounts/{accountId}/lock_settings` | Get locked settings | `getAccountLockSettings` |
| PATCH | `/accounts/{accountId}/lock_settings` | Update locked settings | `UpdateLockedSettings` |
| GET | `/accounts/{accountId}/managed_domains` | Get account's managed domains | `accountManagedDomain` |
| PUT | `/accounts/{accountId}/owner` | Update the account owner | `UpdateTheAccountOwner` |
| GET | `/accounts/{accountId}/settings` | Get account settings | `accountSettings` |
| PATCH | `/accounts/{accountId}/settings` | Update account settings | `accountSettingsUpdate` |
| GET | `/accounts/{accountId}/settings/registration` | Get an account's webinar registration settings | `accountSettingsRegistration` |
| PATCH | `/accounts/{accountId}/settings/registration` | Update an account's webinar registration settings | `accountSettingsRegistrationUpdate` |
| DELETE | `/accounts/{accountId}/settings/virtual_backgrounds` | Delete virtual background files | `delVB` |
| POST | `/accounts/{accountId}/settings/virtual_backgrounds` | Upload virtual background files | `uploadVB` |
| GET | `/accounts/{accountId}/trusted_domains` | Get account's trusted domains | `accountTrustedDomain` |

### Dashboards

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/metrics/chat` | Get chat metrics | `dashboardChat` |
| GET | `/metrics/client/feedback` | List Zoom meetings client feedback | `dashboardClientFeedback` |
| GET | `/metrics/client/feedback/{feedbackId}` | Get zoom meetings client feedback | `dashboardClientFeedbackDetail` |
| GET | `/metrics/client/satisfaction` | List client meeting satisfaction | `listMeetingSatisfaction` |
| GET | `/metrics/client_versions` | List the client versions | `getClientVersions` |
| GET | `/metrics/crc` | Get CRC port usage | `dashboardCRC` |
| GET | `/metrics/issues/zoomrooms` | Get top 25 Zoom Rooms with issues | `dashboardIssueZoomRoom` |
| GET | `/metrics/issues/zoomrooms/{zoomroomId}` | Get issues of Zoom Rooms | `dashboardIssueDetailZoomRoom` |
| GET | `/metrics/meetings` | List meetings | `dashboardMeetings` |
| GET | `/metrics/meetings/{meetingId}` | Get meeting details | `dashboardMeetingDetail` |
| GET | `/metrics/meetings/{meetingId}/participants` | List meeting participants | `dashboardMeetingParticipants` |
| GET | `/metrics/meetings/{meetingId}/participants/qos` | List meeting participants QoS | `dashboardMeetingParticipantsQOS` |
| GET | `/metrics/meetings/{meetingId}/participants/satisfaction` | Get post meeting feedback | `participantFeedback` |
| GET | `/metrics/meetings/{meetingId}/participants/sharing` | Get meeting sharing/recording details | `dashboardMeetingParticipantShare` |
| GET | `/metrics/meetings/{meetingId}/participants/{participantId}/qos` | Get meeting participant QoS | `dashboardMeetingParticipantQOS` |
| GET | `/metrics/quality` | Get meeting quality scores | `dashboardQuality` |
| GET | `/metrics/webinars` | List webinars | `dashboardWebinars` |
| GET | `/metrics/webinars/{webinarId}` | Get webinar details | `dashboardWebinarDetail` |
| GET | `/metrics/webinars/{webinarId}/participants` | Get webinar participants | `dashboardWebinarParticipants` |
| GET | `/metrics/webinars/{webinarId}/participants/qos` | List webinar participant QoS | `dashboardWebinarParticipantsQOS` |
| GET | `/metrics/webinars/{webinarId}/participants/satisfaction` | Get post webinar feedback | `participantWebinarFeedback` |
| GET | `/metrics/webinars/{webinarId}/participants/sharing` | Get webinar sharing/recording details | `dashboardWebinarParticipantShare` |
| GET | `/metrics/webinars/{webinarId}/participants/{participantId}/qos` | Get webinar participant QoS | `dashboardWebinarParticipantQOS` |
| GET | `/metrics/zoomrooms` | List Zoom Rooms | `dashboardZoomRooms` |
| GET | `/metrics/zoomrooms/issues` | Get top 25 issues of Zoom Rooms | `dashboardZoomRoomIssue` |
| GET | `/metrics/zoomrooms/{zoomroomId}` | Get Zoom Rooms details | `dashboardZoomRoom` |

### Data Requests

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/data_requests/files/{fileId}/url` | Get download link for data access request file | `DownloadfilesfromDataRequest` |
| GET | `/data_requests/requests` | List data request history | `GetDataRequestsHistory` |
| POST | `/data_requests/requests` | Create data  (export/deletion) request | `CreateDataAccessRequest` |
| DELETE | `/data_requests/requests/{requestId}` | Cancel data deletion request | `CancelDataRequest` |
| GET | `/data_requests/requests/{requestId}` | List downloadable files for export data request | `GetDownloadableFilesforDataRequest` |

### Information Barriers

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/information_barriers/policies` | List information Barrier policies | `InformationBarriersList` |
| POST | `/information_barriers/policies` | Create an Information Barrier policy | `InformationBarriersCreate` |
| DELETE | `/information_barriers/policies/{policyId}` | Remove an Information Barrier policy | `InformationBarriersDelete` |
| GET | `/information_barriers/policies/{policyId}` | Get an Information Barrier policy by ID | `InformationBarriersGet` |
| PATCH | `/information_barriers/policies/{policyId}` | Update an Information Barriers policy | `InformationBarriersUpdate` |

### Roles

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/roles` | List roles | `roles` |
| POST | `/roles` | Create a role | `createRole` |
| DELETE | `/roles/{roleId}` | Delete a role | `deleteRole` |
| GET | `/roles/{roleId}` | Get role information | `getRoleInformation` |
| PATCH | `/roles/{roleId}` | Update role information | `updateRole` |
| GET | `/roles/{roleId}/members` | List members in a role | `roleMembers` |
| POST | `/roles/{roleId}/members` | Assign a role | `AddRoleMembers` |
| DELETE | `/roles/{roleId}/members/{memberId}` | Unassign a role | `roleMemberDelete` |

### Survey Management

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/surveys` | Get surveys | `getAccountSurveys` |
| GET | `/surveys/{surveyId}` | Get survey info | `getSurveyInfo` |
| GET | `/surveys/{surveyId}/answers` | Get survey answers | `getSurveyAnswers` |
| GET | `/surveys/{surveyId}/instances` | Get survey instances | `getSurveyInstancesInfo` |
