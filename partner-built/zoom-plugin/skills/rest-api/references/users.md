# Zoom Users API

Authoritative endpoint inventory for Users. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/users/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 71 |
| Path templates | 41 |
| Tags | 4 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Contact Groups | 8 |
| Divisions | 7 |
| Groups | 21 |
| Users | 35 |

## Endpoints by Tag

### Contact Groups

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/contacts/groups` | List contact groups | `contactGroups` |
| POST | `/contacts/groups` | Create a contact group | `contactGroupCreate` |
| DELETE | `/contacts/groups/{groupId}` | Delete a contact group | `contactGroupDelete` |
| GET | `/contacts/groups/{groupId}` | Get a contact group | `contactGroup` |
| PATCH | `/contacts/groups/{groupId}` | Update a contact group | `contactGroupUpdate` |
| DELETE | `/contacts/groups/{groupId}/members` | Remove members in a contact group | `contactGroupMemberRemove` |
| GET | `/contacts/groups/{groupId}/members` | List contact group members | `contactGroupMembers` |
| POST | `/contacts/groups/{groupId}/members` | Add contact group members | `contactGroupMemberAdd` |

### Divisions

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/divisions` | List divisions | `listDivisions` |
| POST | `/divisions` | Create a division | `Createadivision` |
| DELETE | `/divisions/{divisionId}` | Delete a division | `Deletedivision` |
| GET | `/divisions/{divisionId}` | Get a division | `Getdivision` |
| PATCH | `/divisions/{divisionId}` | Update a division | `Updateadivision` |
| GET | `/divisions/{divisionId}/users` | List division members | `listDivisionMembers` |
| POST | `/divisions/{divisionId}/users` | Assign a division | `assigndivisionMember` |

### Groups

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/groups` | List groups | `groups` |
| POST | `/groups` | Create a group | `groupCreate` |
| DELETE | `/groups/{groupId}` | Delete a group | `groupDelete` |
| GET | `/groups/{groupId}` | Get a group | `group` |
| PATCH | `/groups/{groupId}` | Update a group | `groupUpdate` |
| GET | `/groups/{groupId}/admins` | List group admins | `groupAdmins` |
| POST | `/groups/{groupId}/admins` | Add group admins | `groupAdminsCreate` |
| DELETE | `/groups/{groupId}/admins/{userId}` | Delete a group admin | `groupAdminsDelete` |
| GET | `/groups/{groupId}/channels` | List group channels | `groupChannels` |
| GET | `/groups/{groupId}/lock_settings` | Get locked settings | `getGroupLockSettings` |
| PATCH | `/groups/{groupId}/lock_settings` | Update locked settings | `groupLockedSettings` |
| GET | `/groups/{groupId}/members` | List group members | `groupMembers` |
| POST | `/groups/{groupId}/members` | Add group members | `groupMembersCreate` |
| DELETE | `/groups/{groupId}/members/{memberId}` | Delete a group member | `groupMembersDelete` |
| PATCH | `/groups/{groupId}/members/{memberId}` | Update a group member | `updateAGroupMember` |
| GET | `/groups/{groupId}/settings` | Get a group's settings | `getGroupSettings` |
| PATCH | `/groups/{groupId}/settings` | Update a group's settings | `updateGroupSettings` |
| GET | `/groups/{groupId}/settings/registration` | Get a group's webinar registration settings | `groupSettingsRegistration` |
| PATCH | `/groups/{groupId}/settings/registration` | Update a group's webinar registration settings | `groupSettingsRegistrationUpdate` |
| DELETE | `/groups/{groupId}/settings/virtual_backgrounds` | Delete Virtual Background files | `delGroupVB` |
| POST | `/groups/{groupId}/settings/virtual_backgrounds` | Upload Virtual Background files | `uploadGroupVB` |

### Users

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/users` | List users | `users` |
| POST | `/users` | Create users | `userCreate` |
| GET | `/users/email` | Check a user email | `userEmail` |
| POST | `/users/features` | Bulk update features for users | `bulkUpdateFeature` |
| GET | `/users/me/zak` | Get the user's ZAK | `userZak` |
| GET | `/users/summary` | Get user summary | `userSummary` |
| GET | `/users/vanity_name` | Check a user's PM room | `userVanityName` |
| DELETE | `/users/{userId}` | Delete a user | `userDelete` |
| GET | `/users/{userId}` | Get a user | `user` |
| PATCH | `/users/{userId}` | Update a user | `userUpdate` |
| DELETE | `/users/{userId}/assistants` | Delete user assistants | `userAssistantsDelete` |
| GET | `/users/{userId}/assistants` | List user assistants | `userAssistants` |
| POST | `/users/{userId}/assistants` | Add assistants | `userAssistantCreate` |
| DELETE | `/users/{userId}/assistants/{assistantId}` | Delete a user assistant | `userAssistantDelete` |
| GET | `/users/{userId}/collaboration_devices` | List a user's collaboration devices | `listCollaborationDevices` |
| GET | `/users/{userId}/collaboration_devices/{collaborationDeviceId}` | Get collaboration device detail | `getCollaborationDevice` |
| PUT | `/users/{userId}/email` | Update a user's email | `userEmailUpdate` |
| GET | `/users/{userId}/meeting_summary_templates` | Get meeting summary templates | `Getmeetingsummarytemplates` |
| GET | `/users/{userId}/meeting_templates/{meetingTemplateId}` | Get meeting template detail | `getUserMeetingTemplates` |
| PUT | `/users/{userId}/password` | Update a user's password | `userPassword` |
| GET | `/users/{userId}/permissions` | Get user permissions | `userPermission` |
| DELETE | `/users/{userId}/picture` | Delete a user's profile picture | `userPictureDelete` |
| POST | `/users/{userId}/picture` | Upload a user's profile picture | `userPicture` |
| GET | `/users/{userId}/presence_status` | Get a user presence status | `getUserPresenceStatus` |
| PUT | `/users/{userId}/presence_status` | Update a user's presence status | `updatePresenceStatus` |
| DELETE | `/users/{userId}/schedulers` | Delete user schedulers | `userSchedulersDelete` |
| GET | `/users/{userId}/schedulers` | List user schedulers | `userSchedulers` |
| DELETE | `/users/{userId}/schedulers/{schedulerId}` | Delete a scheduler | `userSchedulerDelete` |
| GET | `/users/{userId}/settings` | Get user settings | `userSettings` |
| PATCH | `/users/{userId}/settings` | Update user settings | `userSettingsUpdate` |
| DELETE | `/users/{userId}/settings/virtual_backgrounds` | Delete Virtual Background files | `delUserVB` |
| POST | `/users/{userId}/settings/virtual_backgrounds` | Upload Virtual Background files | `uploadVBuser` |
| PUT | `/users/{userId}/status` | Update user status | `userStatus` |
| DELETE | `/users/{userId}/token` | Revoke a user's SSO token | `userSSOTokenDelete` |
| GET | `/users/{userId}/token` | Get a user's token | `userToken` |
