# Zoom Team Chat API

Authoritative endpoint inventory for Team Chat. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/team-chat/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 107 |
| Path templates | 69 |
| Tags | 16 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Chat Channel Mention Group | 7 |
| Chat Channels | 16 |
| Chat Channels (Account-level) | 16 |
| Chat Emoji | 3 |
| Chat Files | 4 |
| Chat Messages | 15 |
| Chat Migration | 7 |
| Chat Reminder | 3 |
| Chat Sessions | 2 |
| Contacts | 3 |
| IM Chat | 1 |
| IM Groups | 8 |
| Invitations | 1 |
| Legal Hold | 6 |
| Reports | 2 |
| Shared Spaces | 13 |

## Endpoints by Tag

### Chat Channel Mention Group

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/chat/channels/{channelId}/mention_group` | List channel mention groups | `getChannelMentionGroup` |
| POST | `/chat/channels/{channelId}/mention_group` | Create a channel mention group | `createChannelMentionGroup` |
| DELETE | `/chat/channels/{channelId}/mention_group/{mentionGroupId}` | Delete a channel mention group | `deleteAChannelMentionGroup` |
| PATCH | `/chat/channels/{channelId}/mention_group/{mentionGroupId}` | Update a channel mention group information | `updateChannelMentionGroup` |
| DELETE | `/chat/channels/{channelId}/mention_group/{mentionGroupId}/members` | Remove channel mention group members | `removeChannelMentionGroupMembers` |
| GET | `/chat/channels/{channelId}/mention_group/{mentionGroupId}/members` | List the members of a mention group | `listTheMembersOfMentionGroup` |
| POST | `/chat/channels/{channelId}/mention_group/{mentionGroupId}/members` | Add channel members to a mention group | `addAChannelMembersToMentionGroup` |

### Chat Channels

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/chat/activities/channels` | List channel activity logs | `listAllChannelActivityLogs` |
| PATCH | `/chat/channels/events` | Perform operations on channels | `PerformOperationsOnChannels` |
| DELETE | `/chat/channels/{channelId}` | Delete a channel | `deleteUserLevelChannel` |
| GET | `/chat/channels/{channelId}` | Get a channel | `getUserLevelChannel` |
| PATCH | `/chat/channels/{channelId}` | Update a channel | `updateUserLevelChannel` |
| DELETE | `/chat/channels/{channelId}/members` | Batch remove members from a channel | `batchRemoveChannelMembers` |
| GET | `/chat/channels/{channelId}/members` | List channel members | `listUserLevelChannelMembers` |
| POST | `/chat/channels/{channelId}/members` | Invite channel members | `InviteUserLevelChannelMembers` |
| GET | `/chat/channels/{channelId}/members/groups` | List channel members (Groups) | `listChannelMembersGroups` |
| POST | `/chat/channels/{channelId}/members/groups` | Invite channel members (Groups) | `inviteChannelMembersGroups` |
| DELETE | `/chat/channels/{channelId}/members/groups/{groupId}` | Remove a member (group) | `removeAMemberGroup` |
| DELETE | `/chat/channels/{channelId}/members/me` | Leave a channel | `leaveChannel` |
| POST | `/chat/channels/{channelId}/members/me` | Join a channel | `joinChannel` |
| DELETE | `/chat/channels/{channelId}/members/{identifier}` | Remove a member | `removeAUserLevelChannelMember` |
| GET | `/chat/users/{userId}/channels` | List user's channels | `getChannels` |
| POST | `/chat/users/{userId}/channels` | Create a channel | `createChannel` |

### Chat Channels (Account-level)

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/chat/channels` | List account's public channels | `getAccountChannels` |
| POST | `/chat/channels/search` | Search user's or account's channels | `searchChannels` |
| GET | `/chat/channels/{channelId}/activities` | List channel activity logs | `listChannelActivityLogs` |
| GET | `/chat/channels/{channelId}/retention` | Get retention policy of a channel | `getChannelRetention` |
| PATCH | `/chat/channels/{channelId}/retention` | Update retention policy of a channel | `updateChannelRetention` |
| DELETE | `/chat/users/{userId}/channels` | Batch delete channels | `batchDeleteChannelsAccountLevel` |
| DELETE | `/chat/users/{userId}/channels/{channelId}` | Delete a channel | `deleteChannel` |
| GET | `/chat/users/{userId}/channels/{channelId}` | Get a channel | `getChannel` |
| PATCH | `/chat/users/{userId}/channels/{channelId}` | Update a channel | `updateChannel` |
| DELETE | `/chat/users/{userId}/channels/{channelId}/admins` | Batch demote channel administrators | `batchDemoteChannelAdministrators` |
| GET | `/chat/users/{userId}/channels/{channelId}/admins` | List channel administrators | `listChannelAdministrators` |
| POST | `/chat/users/{userId}/channels/{channelId}/admins` | Promote channel members to administrators | `promoteChannelMembersAsAdmin` |
| DELETE | `/chat/users/{userId}/channels/{channelId}/members` | Batch remove members from a user's channel | `batchRemoveUserChannelMembers` |
| GET | `/chat/users/{userId}/channels/{channelId}/members` | List channel members | `listChannelMembers` |
| POST | `/chat/users/{userId}/channels/{channelId}/members` | Invite channel members | `inviteChannelMembers` |
| DELETE | `/chat/users/{userId}/channels/{channelId}/members/{identifier}` | Remove a member | `removeAChannelMember` |

### Chat Emoji

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/chat/emoji` | List custom emojis | `listCustomEmojis` |
| POST | `/chat/emoji/files` | Add a custom emoji | `addACustomEmoji` |
| DELETE | `/chat/emoji/{fileId}` | Delete a custom emoji | `DeleteCustomEmoji` |

### Chat Files

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/chat/files/{fileId}` | Delete a chat file | `deleteChatFile` |
| GET | `/chat/files/{fileId}` | Get file info | `getFileInfo` |
| POST | `/chat/users/{userId}/files` | Upload a chat file | `uploadAChatFile` |
| POST | `/chat/users/{userId}/messages/files` | Send a chat file | `sendChatFile` |

### Chat Messages

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| PATCH | `/chat/channel/message/events` | Perform operations on the message of channel | `PerformMessageOfChannel` |
| GET | `/chat/channels/{channelId}/pinned` | List pinned history messages of channel | `listChannelPinnedMessages` |
| GET | `/chat/forwarded_message/{forwardId}` | Get a forwarded message | `getForwardedMessage` |
| GET | `/chat/messages/bookmarks` | List bookmarks | `fetchBookmarks` |
| PATCH | `/chat/messages/bookmarks` | Add or remove a bookmark | `addOrRemoveABookmark` |
| GET | `/chat/messages/schedule` | List scheduled messages | `listScheduledMessages` |
| DELETE | `/chat/messages/schedule/{draftId}` | Delete a scheduled message | `deleteScheduleMessage` |
| GET | `/chat/users/{userId}/messages` | List user's chat messages | `getChatMessages` |
| POST | `/chat/users/{userId}/messages` | Send a chat message | `sendaChatMessage` |
| DELETE | `/chat/users/{userId}/messages/{messageId}` | Delete a message | `deleteChatMessage` |
| GET | `/chat/users/{userId}/messages/{messageId}` | Get a message | `getChatMessage` |
| PUT | `/chat/users/{userId}/messages/{messageId}` | Update a message | `editMessage` |
| PATCH | `/chat/users/{userId}/messages/{messageId}/emoji_reactions` | React to a chat message | `reactMessage` |
| PATCH | `/chat/users/{userId}/messages/{messageId}/status` | Mark message read or unread | `markMessage` |
| GET | `/chat/users/{userId}/messages/{messageId}/thread` | Retrieve a thread | `retrieveThread` |

### Chat Migration

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/chat/migration/channels/{channelId}/members` | Migrate channel members | `MigrateChannelMembers` |
| POST | `/chat/migration/emoji_reactions` | Migrate chat message reactions | `MigrateChatMessageReactions` |
| GET | `/chat/migration/mappings/channels` | Get migrated Zoom channel IDs | `getMigrationChannelsMapping` |
| GET | `/chat/migration/mappings/users` | Get migrated Zoom user IDs | `getMigrationUsersMapping` |
| POST | `/chat/migration/messages` | Migrate chat messages | `MigrateChatMessages` |
| POST | `/chat/migration/users/{identifier}/channels` | Migrate a chat channel | `MigrateAChatChannel` |
| POST | `/chat/migration/users/{identifier}/events` | Migrate 1:1 conversation or channel operations | `Migrate1:1ConversationOrChannelOperations` |

### Chat Reminder

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/chat/messages/{messageId}/reminder` | Delete a reminder for a message | `deleteReminderForMessage` |
| POST | `/chat/messages/{messageId}/reminder` | Create a reminder message | `createReminderForMessage` |
| GET | `/chat/reminder` | List reminders | `listReminders` |

### Chat Sessions

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| PATCH | `/chat/users/{userId}/events` | Star or unstar a channel or contact user | `starUnstarChannelContact` |
| GET | `/chat/users/{userId}/sessions` | List a user's chat sessions | `getChatSessions` |

### Contacts

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/chat/users/me/contacts` | List user's contacts | `getUserContacts` |
| GET | `/chat/users/me/contacts/{identifier}` | Get user's contact details | `getUserContact` |
| GET | `/contacts` | Search company contacts | `searchCompanyContacts` |

### IM Chat

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/im/users/me/chat/messages` | Send IM messages | `sendimmessages` |

### IM Groups

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/im/groups` | List IM directory groups | `imGroups` |
| POST | `/im/groups` | Create an IM directory group | `imGroupCreate` |
| DELETE | `/im/groups/{groupId}` | Delete an IM directory group | `imGroupDelete` |
| GET | `/im/groups/{groupId}` | Retrieve an IM directory group | `imGroup` |
| PATCH | `/im/groups/{groupId}` | Update an IM directory group | `imGroupUpdate` |
| GET | `/im/groups/{groupId}/members` | List IM directory group members | `imGroupMembers` |
| POST | `/im/groups/{groupId}/members` | Add IM directory group members | `imGroupMembersCreate` |
| DELETE | `/im/groups/{groupId}/members/{memberId}` | Delete IM directory group member | `imGroupMembersDelete` |

### Invitations

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/chat/users/{userId}/invitations` | Send new contact invitation | `sendNewContactInvitation` |

### Legal Hold

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/chat/legalhold/matters` | List legal hold matters | `listLegalHoldMatters` |
| POST | `/chat/legalhold/matters` | Add a legal hold matter | `addLegalHoldMatter` |
| DELETE | `/chat/legalhold/matters/{matterId}` | Delete legal hold matters | `deleteLegalHoldMatters` |
| PATCH | `/chat/legalhold/matters/{matterId}` | Update legal hold matter | `updateLegalHoldMatter` |
| GET | `/chat/legalhold/matters/{matterId}/files` | List legal hold files by given matter | `listLegalHoldFiles` |
| GET | `/chat/legalhold/matters/{matterId}/files/download` | Download legal hold files for given matter | `downloadLegalHoldFiles` |

### Reports

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/report/chat/sessions` | Get chat sessions reports | `reportChatSessions` |
| GET | `/report/chat/sessions/{sessionId}` | Get chat message reports | `reportChatMessages` |

### Shared Spaces

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/chat/spaces` | List shared spaces | `listSharedSpaces` |
| POST | `/chat/spaces` | Create a shared space | `createSpace` |
| DELETE | `/chat/spaces/{spaceId}` | Delete a shared space | `deleteSpace` |
| GET | `/chat/spaces/{spaceId}` | Get a shared space | `getASharedSpace` |
| PATCH | `/chat/spaces/{spaceId}` | Update shared space settings | `updateSharedSpaceSettings` |
| DELETE | `/chat/spaces/{spaceId}/admins` | Demote shared space administrators to members | `demoteSpaceAdmins` |
| POST | `/chat/spaces/{spaceId}/admins` | Promote shared space members to administrators | `promoteSpaceMembers` |
| GET | `/chat/spaces/{spaceId}/channels` | List shared space channels | `listSharedSpaceChannels` |
| PATCH | `/chat/spaces/{spaceId}/channels` | Move shared space channels | `updateSharedSpaceChannels` |
| DELETE | `/chat/spaces/{spaceId}/members` | Remove members from a shared space | `deleteSpaceMembers` |
| GET | `/chat/spaces/{spaceId}/members` | List shared space members | `listSharedSpaceMembers` |
| POST | `/chat/spaces/{spaceId}/members` | Add members to a shared space | `addSpaceMembers` |
| PATCH | `/chat/spaces/{spaceId}/owner` | Transfer shared space ownership | `transferSpaceOwner` |
