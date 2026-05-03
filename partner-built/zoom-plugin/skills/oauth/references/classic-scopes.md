# Classic OAuth Scopes

> Source: https://developers.zoom.us/docs/integrations/oauth-scopes/

## Account

### account:master

View and manage sub accounts

**Associated APIs:**

- [Update the account owner](/docs/api/rest/reference/account/ma/#operation/UpdateTheAccountOwner)
- [Get sub account details](/docs/api/rest/reference/account/ma/#operation/GetSubAccountDetails)
- [Get account's managed domains](/docs/api/rest/reference/account/ma/#operation/accountManagedDomain)
- [List upcoming renewal accounts](/docs/api/rest/reference/billing/ma/#operation/Getupcomingrenewalaccounts)
- [Delete virtual background files](/docs/api/rest/reference/account/ma/#operation/delVB)
- [Create a sub account](/docs/api/rest/reference/account/ma/#operation/accountCreate)
- [Update options](/docs/api/rest/reference/account/ma/#operation/UpdateOptions)
- [Get plan usage](/docs/api/rest/reference/billing/ma/#operation/GetPlanUsage)
- [Get account's trusted domains](/docs/api/rest/reference/account/ma/#operation/accountTrustedDomain)
- [List sub accounts](/docs/api/rest/reference/account/ma/#operation/accounts)
- [Disassociate a sub account](/docs/api/rest/reference/account/ma/#operation/DisassociateASubAccount)
- [Upload virtual background files](/docs/api/rest/reference/account/ma/#operation/uploadVB)

### account:read:admin

View account info

**Associated APIs:**

- [Get locked settings](/docs/api/rest/reference/account/methods/#operation/getAccountLockSettings)
- [Get indicators settings](/docs/api/rest/reference/iq/methods/#operation/accountIndicatorsSettings)
- [Get an account's webinar registration settings](/docs/api/rest/reference/account/ma/#operation/accountSettingsRegistration)
- [Get account settings](/docs/api/rest/reference/account/ma/#operation/accountSettings)
- [Get account's managed domains](/docs/api/rest/reference/account/methods/#operation/accountManagedDomain)
- [Get account's trusted domains](/docs/api/rest/reference/account/methods/#operation/accountTrustedDomain)
- [Get indicators settings [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/accountSettingsIndicatorsDeprecated)

### account:write:admin

View and manage account info

**Associated APIs:**

- [Update locked settings](/docs/api/rest/reference/account/methods/#operation/UpdateLockedSettings)
- [Get locked settings](/docs/api/rest/reference/account/ma/#operation/getAccountLockSettings)
- [Get indicators settings](/docs/api/rest/reference/iq/methods/#operation/accountIndicatorsSettings)
- [Update the account owner](/docs/api/rest/reference/account/methods/#operation/UpdateTheAccountOwner)
- [Upload virtual background files](/docs/api/rest/reference/account/ma/#operation/uploadVB)
- [Update account settings](/docs/api/rest/reference/account/methods/#operation/accountSettingsUpdate)
- [Get indicators settings [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/accountSettingsIndicatorsDeprecated)
- [Get an account's webinar registration settings](/docs/api/rest/reference/account/ma/#operation/accountSettingsRegistration)
- [Delete virtual background files](/docs/api/rest/reference/account/ma/#operation/delVB)
- [Update an account's webinar registration settings](/docs/api/rest/reference/account/ma/#operation/accountSettingsRegistrationUpdate)
- [Get account settings](/docs/api/rest/reference/account/ma/#operation/accountSettings)

## Billing

### billing:master

View and manage sub account's billing info

**Associated APIs:**

- [Subscribe an account to a plan](/docs/api/rest/reference/billing/ma/#operation/SubscribeAccountToAPlan)
- [Get invoice details](/docs/api/rest/reference/billing/ma/#operation/GetInvoiceDetails)
- [Cancel additional plans](/docs/api/rest/reference/billing/ma/#operation/CancelAdditionalPlans)
- [Get account plan information](/docs/api/rest/reference/billing/ma/#operation/GetAccountPlanInformation)
- [Generate sub accounts' billing invoice reports](/docs/api/rest/reference/billing/ma/#operation/generateSubInvoiceReport)
- [Get billing information](/docs/api/rest/reference/billing/ma/#operation/GetBillingInformation)
- [Delete subaccounts' billing invoice report](/docs/api/rest/reference/billing/ma/#operation/deleteBillingInvoiceReport)
- [Subscribe subaccount to an additional plan](/docs/api/rest/reference/billing/ma/#operation/SubscribeAccountToAnAdditionalPlan)
- [Update an account's additional plan](/docs/api/rest/reference/billing/ma/#operation/UpdateAnAccount'sAdditionalPlan)
- [Download an invoice file](/docs/api/rest/reference/billing/ma/#operation/downloadInvoicePDF)
- [Update a base plan](/docs/api/rest/reference/billing/ma/#operation/UpdateABasePlan)
- [List upcoming renewal accounts](/docs/api/rest/reference/billing/ma/#operation/Getupcomingrenewalaccounts)
- [List billing invoices](/docs/api/rest/reference/billing/ma/#operation/ListBillingInvoices)
- [List sub accounts' billing invoice reports](/docs/api/rest/reference/billing/ma/#operation/listSubInvoiceReport)
- [Download subaccounts' billing invoice reports](/docs/api/rest/reference/billing/ma/#operation/downloadBillingInvoiceReport)
- [Download an invoice file (v2)](/docs/api/rest/reference/billing/ma/#operation/downloadInvoicePDFFile)
- [Cancel a base plan](/docs/api/rest/reference/billing/ma/#operation/CancelABasePlan)
- [Update billing information](/docs/api/rest/reference/billing/ma/#operation/UpdateBillingInformation)
- [Get plan usage](/docs/api/rest/reference/billing/ma/#operation/GetPlanUsage)

## Calendar

### calendar:read

View calendar

**Associated APIs:**

- [Get the specified user calendar settings of the authenticated user](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getsetting)
- [Get the color definitions for calendars and events](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getcolor)
- [Query freebusy information for a set of calendars](/docs/api/rest/reference/zoom-calendar/methods/#operation/Queryfreebusy)
- [List ACL rules of specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Listacl)
- [List all user calendar settings of the authenticated user](/docs/api/rest/reference/zoom-calendar/methods/#operation/Listsettings)
- [Get a specified calendar from the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/GetcalendarList)
- [Get the specified event on the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getevent)
- [List events on the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Listevent)
- [List the calendars in the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/ListcalendarList)
- [Get the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getcalendar)
- [List all instances of the specified recurring event](/docs/api/rest/reference/zoom-calendar/methods/#operation/Instanceevent)
- [Get the specified ACL rule](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getacl)

### calendar:read:admin

View calendar

**Associated APIs:**

- [Get the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getcalendar)
- [Get the specified event on the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getevent)
- [Query freebusy information for a set of calendars](/docs/api/rest/reference/zoom-calendar/methods/#operation/Queryfreebusy)
- [List ACL rules of specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Listacl)
- [Get the specified user calendar settings of the authenticated user](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getsetting)
- [List all user calendar settings of the authenticated user](/docs/api/rest/reference/zoom-calendar/methods/#operation/Listsettings)
- [List all instances of the specified recurring event](/docs/api/rest/reference/zoom-calendar/methods/#operation/Instanceevent)
- [Get the color definitions for calendars and events](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getcolor)
- [Get the specified ACL rule](/docs/api/rest/reference/zoom-calendar/methods/#operation/Getacl)
- [List events on the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Listevent)
- [Get a specified calendar from the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/GetcalendarList)
- [List the calendars in the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/ListcalendarList)

### calendar:write

Manage calendar

**Associated APIs:**

- [Insert an existing calendar to the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/InsertcalendarList)
- [Insert a new event to the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Insertevent)
- [Quick add an event to the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Quickaddevent)
- [Delete a calendar owned by a user](/docs/api/rest/reference/zoom-calendar/methods/#operation/Deletecalendar)
- [Move the specified event from a calendar to another specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Moveevent)
- [Update the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Patchcalendar)
- [Import event to the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Importevent)
- [Create a new secondary calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Insertcalendar)
- [Create a new ACL rule](/docs/api/rest/reference/zoom-calendar/methods/#operation/Insertacl)
- [Delete an existing ACL rule](/docs/api/rest/reference/zoom-calendar/methods/#operation/Deleteacl)
- [Delete an existing calendar from the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/DeletecalendarList)
- [Update the specified event on the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Patchevent)
- [Update the specified ACL rule](/docs/api/rest/reference/zoom-calendar/methods/#operation/Patchacl)
- [Update an existing calendar in the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/PatchcalendarList)
- [Patch the specified user calendar settings of the authenticated user](/docs/api/rest/reference/zoom-calendar/methods/#operation/Patchsetting)
- [Delete an existing event from the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Deleteevent)

### calendar:write:admin

Manage calendar

**Associated APIs:**

- [Delete an existing ACL rule](/docs/api/rest/reference/zoom-calendar/methods/#operation/Deleteacl)
- [Create a new ACL rule](/docs/api/rest/reference/zoom-calendar/methods/#operation/Insertacl)
- [Delete an existing event from the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Deleteevent)
- [Quick add an event to the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Quickaddevent)
- [Delete an existing calendar from the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/DeletecalendarList)
- [Update the specified event on the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Patchevent)
- [Insert an existing calendar to the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/InsertcalendarList)
- [Insert a new event to the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Insertevent)
- [Create a new secondary calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Insertcalendar)
- [Update an existing calendar in the user's own calendarList](/docs/api/rest/reference/zoom-calendar/methods/#operation/PatchcalendarList)
- [Patch the specified user calendar settings of the authenticated user](/docs/api/rest/reference/zoom-calendar/methods/#operation/Patchsetting)
- [Import event to the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Importevent)
- [Update the specified ACL rule](/docs/api/rest/reference/zoom-calendar/methods/#operation/Patchacl)
- [Update the specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Patchcalendar)
- [Delete a calendar owned by a user](/docs/api/rest/reference/zoom-calendar/methods/#operation/Deletecalendar)
- [Move the specified event from a calendar to another specified calendar](/docs/api/rest/reference/zoom-calendar/methods/#operation/Moveevent)

## Chat

### chat:read

View Chat Message Info

**Associated APIs:**

- [List shared space members](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaceMembers)
- [List shared spaces](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaces)
- [List custom emojis](/docs/api/rest/reference/chat/methods/#operation/listCustomEmojis)
- [Get file info](/docs/api/rest/reference/chat/methods/#operation/getFileInfo)
- [List pinned history messages of channel](/docs/api/rest/reference/chat/methods/#operation/listChannelPinnedMessages)
- [Get a shared space](/docs/api/rest/reference/chat/methods/#operation/getASharedSpace)
- [List shared space channels](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaceChannels)

### chat:read:admin

View Chat Message Info

**Associated APIs:**

- [List custom emojis](/docs/api/rest/reference/chat/methods/#operation/listCustomEmojis)
- [List shared space channels](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaceChannels)
- [Get a shared space](/docs/api/rest/reference/chat/methods/#operation/getASharedSpace)
- [List shared space members](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaceMembers)
- [List pinned history messages of channel](/docs/api/rest/reference/chat/methods/#operation/listChannelPinnedMessages)
- [List shared spaces](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaces)

### chat:write

Manage Chat Message Info

**Associated APIs:**

- [Delete a shared space](/docs/api/rest/reference/chat/methods/#operation/deleteSpace)
- [Create a shared space](/docs/api/rest/reference/chat/methods/#operation/createSpace)
- [List shared space members](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaceMembers)
- [Add a custom emoji](/docs/api/rest/reference/chat/methods/#operation/addACustomEmoji)
- [Demote shared space administrators to members](/docs/api/rest/reference/chat/methods/#operation/demoteSpaceAdmins)
- [List custom emojis](/docs/api/rest/reference/chat/methods/#operation/listCustomEmojis)
- [Promote shared space members to administrators](/docs/api/rest/reference/chat/methods/#operation/promoteSpaceMembers)
- [Remove members from a shared space](/docs/api/rest/reference/chat/methods/#operation/deleteSpaceMembers)
- [Delete a chat file](/docs/api/rest/reference/chat/methods/#operation/deleteChatFile)
- [Update shared space settings](/docs/api/rest/reference/chat/methods/#operation/updateSharedSpaceSettings)
- [Transfer shared space ownership](/docs/api/rest/reference/chat/methods/#operation/transferSpaceOwner)
- [Move shared space channels](/docs/api/rest/reference/chat/methods/#operation/updateSharedSpaceChannels)
- [List pinned history messages of channel](/docs/api/rest/reference/chat/methods/#operation/listChannelPinnedMessages)
- [Delete a custom emoji](/docs/api/rest/reference/chat/methods/#operation/DeleteCustomEmoji)
- [Get a shared space](/docs/api/rest/reference/chat/methods/#operation/getASharedSpace)
- [List shared space channels](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaceChannels)
- [Perform operations on the message of channel](/docs/api/rest/reference/chat/methods/#operation/PerformMessageOfChannel)
- [Add members to a shared space](/docs/api/rest/reference/chat/methods/#operation/addSpaceMembers)
- [List shared spaces](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaces)

### chat:write:admin

Manage Chat Message Info

**Associated APIs:**

- [List custom emojis](/docs/api/rest/reference/chat/methods/#operation/listCustomEmojis)
- [Create a shared space](/docs/api/rest/reference/chat/methods/#operation/createSpace)
- [Demote shared space administrators to members](/docs/api/rest/reference/chat/methods/#operation/demoteSpaceAdmins)
- [Add a custom emoji](/docs/api/rest/reference/chat/methods/#operation/addACustomEmoji)
- [List shared spaces](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaces)
- [Promote shared space members to administrators](/docs/api/rest/reference/chat/methods/#operation/promoteSpaceMembers)
- [Update shared space settings](/docs/api/rest/reference/chat/methods/#operation/updateSharedSpaceSettings)
- [Remove members from a shared space](/docs/api/rest/reference/chat/methods/#operation/deleteSpaceMembers)
- [Delete a custom emoji](/docs/api/rest/reference/chat/methods/#operation/DeleteCustomEmoji)
- [Add members to a shared space](/docs/api/rest/reference/chat/methods/#operation/addSpaceMembers)
- [Get a shared space](/docs/api/rest/reference/chat/methods/#operation/getASharedSpace)
- [List shared space channels](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaceChannels)
- [Delete a shared space](/docs/api/rest/reference/chat/methods/#operation/deleteSpace)
- [List shared space members](/docs/api/rest/reference/chat/methods/#operation/listSharedSpaceMembers)
- [Transfer shared space ownership](/docs/api/rest/reference/chat/methods/#operation/transferSpaceOwner)

### chat_channel:read

View current user's team chat channels

**Associated APIs:**

- [Get a channel](/docs/api/rest/reference/chat/methods/#operation/getUserLevelChannel)
- [List channel members](/docs/api/rest/reference/chat/methods/#operation/listChannelMembers)
- [List channel administrators](/docs/api/rest/reference/chat/methods/#operation/listChannelAdministrators)
- [List the members of a mention group](/docs/api/rest/reference/chat/methods/#operation/listTheMembersOfMentionGroup)
- [Search user's or account's channels](/docs/api/rest/reference/chat/methods/#operation/searchChannels)
- [List channel mention groups](/docs/api/rest/reference/chat/methods/#operation/getChannelMentionGroup)
- [List user's channels](/docs/api/rest/reference/chat/methods/#operation/getChannels)

### chat_channel:read:admin

View all users' team chat channels

**Associated APIs:**

- [List channel activity logs](/docs/api/rest/reference/chat/methods/#operation/listChannelActivityLogs)
- [List user's channels](/docs/api/rest/reference/chat/methods/#operation/getChannels)
- [List channel members (Groups)](/docs/api/rest/reference/chat/methods/#operation/listChannelMembersGroups)
- [Get a channel](/docs/api/rest/reference/chat/methods/#operation/getUserLevelChannel)
- [List channel mention groups](/docs/api/rest/reference/chat/methods/#operation/getChannelMentionGroup)
- [List channel members](/docs/api/rest/reference/chat/methods/#operation/listChannelMembers)
- [List channel administrators](/docs/api/rest/reference/chat/methods/#operation/listChannelAdministrators)
- [List account's public channels](/docs/api/rest/reference/chat/methods/#operation/getAccountChannels)
- [Search user's or account's channels](/docs/api/rest/reference/chat/methods/#operation/searchChannels)
- [Get retention policy of a channel](/docs/api/rest/reference/chat/methods/#operation/getChannelRetention)

### chat_channel:read:member

View team chat channels as a member

**Associated APIs:**

- [List the members of a mention group](/docs/api/rest/reference/chat/methods/#operation/listTheMembersOfMentionGroup)

### chat_channel:write

View and manage current user's team chat channels

**Associated APIs:**

- [List user's channels](/docs/api/rest/reference/chat/methods/#operation/getChannels)
- [Batch demote channel administrators](/docs/api/rest/reference/chat/methods/#operation/batchDemoteChannelAdministrators)
- [Leave a channel](/docs/api/rest/reference/chat/methods/#operation/leaveChannel)
- [Perform operations on channels](/docs/api/rest/reference/chat/methods/#operation/PerformOperationsOnChannels)
- [Join a channel](/docs/api/rest/reference/chat/methods/#operation/joinChannel)
- [Search user's or account's channels](/docs/api/rest/reference/chat/methods/#operation/searchChannels)
- [Add channel members to a mention group](/docs/api/rest/reference/chat/methods/#operation/addAChannelMembersToMentionGroup)
- [Update a channel](/docs/api/rest/reference/chat/methods/#operation/updateUserLevelChannel)
- [Delete a channel mention group](/docs/api/rest/reference/chat/methods/#operation/deleteAChannelMentionGroup)
- [List channel members](/docs/api/rest/reference/chat/methods/#operation/listChannelMembers)
- [Invite channel members](/docs/api/rest/reference/chat/methods/#operation/InviteUserLevelChannelMembers)
- [Batch delete channels](/docs/api/rest/reference/chat/methods/#operation/batchDeleteChannelsAccountLevel)
- [Update a channel mention group information](/docs/api/rest/reference/chat/methods/#operation/updateChannelMentionGroup)
- [Create a channel mention group](/docs/api/rest/reference/chat/methods/#operation/createChannelMentionGroup)
- [Promote channel members to administrators](/docs/api/rest/reference/chat/methods/#operation/promoteChannelMembersAsAdmin)
- [Batch remove members from a user's channel](/docs/api/rest/reference/chat/methods/#operation/batchRemoveUserChannelMembers)
- [Get a channel](/docs/api/rest/reference/chat/methods/#operation/getUserLevelChannel)
- [Delete a channel](/docs/api/rest/reference/chat/methods/#operation/deleteChannel)
- [Batch remove members from a channel](/docs/api/rest/reference/chat/methods/#operation/batchRemoveChannelMembers)
- [Remove a member](/docs/api/rest/reference/chat/methods/#operation/removeAUserLevelChannelMember)
- [Create a channel](/docs/api/rest/reference/chat/methods/#operation/createChannel)
- [Remove channel mention group members](/docs/api/rest/reference/chat/methods/#operation/removeChannelMentionGroupMembers)

### chat_channel:write:admin

View and manage all users' team chat channels

**Associated APIs:**

- [Get a channel](/docs/api/rest/reference/chat/methods/#operation/getChannel)
- [Update a channel](/docs/api/rest/reference/chat/methods/#operation/updateChannel)
- [Batch remove members from a channel](/docs/api/rest/reference/chat/methods/#operation/batchRemoveChannelMembers)
- [Delete a channel](/docs/api/rest/reference/chat/methods/#operation/deleteChannel)
- [List channel members](/docs/api/rest/reference/chat/methods/#operation/listUserLevelChannelMembers)
- [Get retention policy of a channel](/docs/api/rest/reference/chat/methods/#operation/getChannelRetention)
- [Remove a member](/docs/api/rest/reference/chat/methods/#operation/removeAChannelMember)
- [List the members of a mention group](/docs/api/rest/reference/chat/methods/#operation/listTheMembersOfMentionGroup)
- [Update retention policy of a channel](/docs/api/rest/reference/chat/methods/#operation/updateChannelRetention)
- [Create a channel](/docs/api/rest/reference/chat/methods/#operation/createChannel)
- [Join a channel](/docs/api/rest/reference/chat/methods/#operation/joinChannel)
- [Remove channel mention group members](/docs/api/rest/reference/chat/methods/#operation/removeChannelMentionGroupMembers)
- [Search user's or account's channels](/docs/api/rest/reference/chat/methods/#operation/searchChannels)
- [Invite channel members (Groups)](/docs/api/rest/reference/chat/methods/#operation/inviteChannelMembersGroups)
- [Invite channel members](/docs/api/rest/reference/chat/methods/#operation/InviteUserLevelChannelMembers)
- [Batch demote channel administrators](/docs/api/rest/reference/chat/methods/#operation/batchDemoteChannelAdministrators)
- [List channel members (Groups)](/docs/api/rest/reference/chat/methods/#operation/listChannelMembersGroups)
- [Leave a channel](/docs/api/rest/reference/chat/methods/#operation/leaveChannel)
- [Remove a member (group)](/docs/api/rest/reference/chat/methods/#operation/removeAMemberGroup)
- [Perform operations on channels](/docs/api/rest/reference/chat/methods/#operation/PerformOperationsOnChannels)
- [Add channel members to a mention group](/docs/api/rest/reference/chat/methods/#operation/addAChannelMembersToMentionGroup)
- [List user's channels](/docs/api/rest/reference/chat/methods/#operation/getChannels)
- [Delete a channel mention group](/docs/api/rest/reference/chat/methods/#operation/deleteAChannelMentionGroup)
- [List account's public channels](/docs/api/rest/reference/chat/methods/#operation/getAccountChannels)
- [Batch delete channels](/docs/api/rest/reference/chat/methods/#operation/batchDeleteChannelsAccountLevel)
- [Update a channel mention group information](/docs/api/rest/reference/chat/methods/#operation/updateChannelMentionGroup)
- [Promote channel members to administrators](/docs/api/rest/reference/chat/methods/#operation/promoteChannelMembersAsAdmin)
- [Create a channel mention group](/docs/api/rest/reference/chat/methods/#operation/createChannelMentionGroup)
- [Batch remove members from a user's channel](/docs/api/rest/reference/chat/methods/#operation/batchRemoveUserChannelMembers)

### chat_contact:read

View current user's team chat contact information

**Associated APIs:**

- [Get user's contact details](/docs/api/rest/reference/chat/methods/#operation/getUserContact)
- [List user's contacts](/docs/api/rest/reference/chat/methods/#operation/getUserContacts)

### chat_contact:write

Send Contact Invitation

**Associated APIs:**

- [Send new contact invitation](/docs/api/rest/reference/chat/methods/#operation/sendNewContactInvitation)

### chat_contact:write:admin

Send contact invitation

**Associated APIs:**

- [Send new contact invitation](/docs/api/rest/reference/chat/methods/#operation/sendNewContactInvitation)

### chat_event:write

Manage your chat event info

**Associated APIs:**

- [Star or unstar a channel or contact user](/docs/api/rest/reference/chat/methods/#operation/starUnstarChannelContact)

### chat_event:write:admin

Manage account's chat event info

**Associated APIs:**

- [Star or unstar a channel or contact user](/docs/api/rest/reference/chat/methods/#operation/starUnstarChannelContact)

### chat_history_legal_hold:read:admin

View Chat History Legal Hold Info

**Associated APIs:**

- [List legal hold files by given matter](/docs/api/rest/reference/chat/methods/#operation/listLegalHoldFiles)
- [Download legal hold files for given matter](/docs/api/rest/reference/chat/methods/#operation/downloadLegalHoldFiles)
- [List legal hold matters](/docs/api/rest/reference/chat/methods/#operation/listLegalHoldMatters)

### chat_history_legal_hold:write:admin

Manage Chat History Legal Hold Info

**Associated APIs:**

- [Update legal hold matter](/docs/api/rest/reference/chat/methods/#operation/updateLegalHoldMatter)
- [List legal hold files by given matter](/docs/api/rest/reference/chat/methods/#operation/listLegalHoldFiles)
- [Download legal hold files for given matter](/docs/api/rest/reference/chat/methods/#operation/downloadLegalHoldFiles)
- [List legal hold matters](/docs/api/rest/reference/chat/methods/#operation/listLegalHoldMatters)
- [Delete legal hold matters](/docs/api/rest/reference/chat/methods/#operation/deleteLegalHoldMatters)
- [Add a legal hold matter](/docs/api/rest/reference/chat/methods/#operation/addLegalHoldMatter)

### chat_message:read

View current user's team chat messages

**Associated APIs:**

- [Get a forwarded message](/docs/api/rest/reference/chat/methods/#operation/getForwardedMessage)
- [Retrieve a thread](/docs/api/rest/reference/chat/methods/#operation/retrieveThread)
- [Get a message](/docs/api/rest/reference/chat/methods/#operation/getChatMessage)
- [List reminders](/docs/api/rest/reference/chat/methods/#operation/listReminders)
- [List bookmarks](/docs/api/rest/reference/chat/methods/#operation/fetchBookmarks)
- [List a user's chat sessions](/docs/api/rest/reference/chat/methods/#operation/getChatSessions)
- [List scheduled messages](/docs/api/rest/reference/chat/methods/#operation/listScheduledMessages)
- [List user's chat messages](/docs/api/rest/reference/chat/methods/#operation/getChatMessages)

### chat_message:read:admin

View all users' team chat messages

**Associated APIs:**

- [Get a message](/docs/api/rest/reference/chat/methods/#operation/getChatMessage)
- [Retrieve a thread](/docs/api/rest/reference/chat/methods/#operation/retrieveThread)
- [List user's chat messages](/docs/api/rest/reference/chat/methods/#operation/getChatMessages)
- [Get a forwarded message](/docs/api/rest/reference/chat/methods/#operation/getForwardedMessage)
- [List a user's chat sessions](/docs/api/rest/reference/chat/methods/#operation/getChatSessions)

### chat_message:write

View and manage current user's team chat messages

**Associated APIs:**

- [Mark message read or unread](/docs/api/rest/reference/chat/methods/#operation/markMessage)
- [Create a reminder message](/docs/api/rest/reference/chat/methods/#operation/createReminderForMessage)
- [Send a chat file](/docs/api/rest/reference/chat/methods/#operation/sendChatFile)
- [Send a chat message](/docs/api/rest/reference/chat/methods/#operation/sendaChatMessage)
- [React to a chat message](/docs/api/rest/reference/chat/methods/#operation/reactMessage)
- [Get a message](/docs/api/rest/reference/chat/methods/#operation/getChatMessage)
- [List bookmarks](/docs/api/rest/reference/chat/methods/#operation/fetchBookmarks)
- [Add or remove a bookmark](/docs/api/rest/reference/chat/methods/#operation/addOrRemoveABookmark)
- [Update a message](/docs/api/rest/reference/chat/methods/#operation/editMessage)
- [Delete a reminder for a message](/docs/api/rest/reference/chat/methods/#operation/deleteReminderForMessage)
- [Delete a scheduled message](/docs/api/rest/reference/chat/methods/#operation/deleteScheduleMessage)
- [Delete a message](/docs/api/rest/reference/chat/methods/#operation/deleteChatMessage)
- [Upload a chat file](/docs/api/rest/reference/chat/methods/#operation/uploadAChatFile)
- [List scheduled messages](/docs/api/rest/reference/chat/methods/#operation/listScheduledMessages)
- [List user's chat messages](/docs/api/rest/reference/chat/methods/#operation/getChatMessages)
- [Get a forwarded message](/docs/api/rest/reference/chat/methods/#operation/getForwardedMessage)

### chat_message:write:admin

View and manage all users' team chat messages

**Associated APIs:**

- [Get a forwarded message](/docs/api/rest/reference/chat/methods/#operation/getForwardedMessage)
- [Mark message read or unread](/docs/api/rest/reference/chat/methods/#operation/markMessage)
- [React to a chat message](/docs/api/rest/reference/chat/methods/#operation/reactMessage)
- [Delete a message](/docs/api/rest/reference/chat/methods/#operation/deleteChatMessage)
- [Send a chat message](/docs/api/rest/reference/chat/methods/#operation/sendaChatMessage)
- [Update a message](/docs/api/rest/reference/chat/methods/#operation/editMessage)
- [Get a message](/docs/api/rest/reference/chat/methods/#operation/getChatMessage)
- [Send a chat file](/docs/api/rest/reference/chat/methods/#operation/sendChatFile)
- [List user's chat messages](/docs/api/rest/reference/chat/methods/#operation/getChatMessages)
- [Upload a chat file](/docs/api/rest/reference/chat/methods/#operation/uploadAChatFile)

### chat_migration:read:admin

View information about a chat history migration

**Associated APIs:**

- [Get migrated Zoom user IDs](/docs/api/rest/reference/chat/methods/#operation/getMigrationUsersMapping)
- [Get migrated Zoom channel IDs](/docs/api/rest/reference/chat/methods/#operation/getMigrationChannelsMapping)

### chat_migration:write:admin

Migrate chat history from another vendor

**Associated APIs:**

- [Migrate channel members](/docs/api/rest/reference/chat/methods/#operation/MigrateChannelMembers)
- [Migrate 1:1 conversation or channel operations](/docs/api/rest/reference/chat/methods/#operation/Migrate1:1ConversationOrChannelOperations)
- [Migrate a chat channel](/docs/api/rest/reference/chat/methods/#operation/MigrateAChatChannel)
- [Migrate chat message reactions](/docs/api/rest/reference/chat/methods/#operation/MigrateChatMessageReactions)
- [Migrate chat messages](/docs/api/rest/reference/chat/methods/#operation/MigrateChatMessages)

### imchat:bot

Enable Chatbot within Zoom Team Chat Client

**Associated APIs:**

- [Delete a Chatbot message](/docs/api/rest/reference/chatbot/methods/#operation/deleteAChatbotMessage)
- [Send Chatbot messages](/docs/api/rest/reference/chatbot/methods/#operation/sendChatbot)
- [Link Unfurls](/docs/api/rest/reference/chatbot/methods/#operation/unfurlingLink)
- [Edit a Chatbot message](/docs/api/rest/reference/chatbot/methods/#operation/editChatbotMessage)

### imchat:read:admin

View all users history and channels

**Associated APIs:**

- [Get chat message reports](/docs/api/rest/reference/chat/methods/#operation/reportChatMessages)
- [Get chat sessions reports](/docs/api/rest/reference/chat/methods/#operation/reportChatSessions)

### imchat:write

Send a team chat message to a Zoom Team Chat user or channel

**Associated APIs:**

- [Send IM messages](/docs/api/rest/reference/chat/methods/#operation/sendimmessages)

## Clips

### clips:read

View your clips information

**Associated APIs:**

- [List clip comments](/docs/api/rest/reference/clips/methods/#operation/Listclipcomments)
- [Get collaborators of a clip](/docs/api/rest/reference/clips/methods/#operation/GetClipCollaborators)
- [Download a clip](/docs/api/rest/reference/clips/methods/#operation/downloadClip)
- [Get a clip](/docs/api/rest/reference/clips/methods/#operation/GetClipById)
- [List all clips](/docs/api/rest/reference/clips/methods/#operation/GetUserClips)

### clips:read:admin

View your clips information

**Associated APIs:**

- [List clip comments](/docs/api/rest/reference/clips/methods/#operation/Listclipcomments)
- [Get collaborators of a clip](/docs/api/rest/reference/clips/methods/#operation/GetClipCollaborators)
- [Download a clip](/docs/api/rest/reference/clips/methods/#operation/downloadClip)
- [Transfer task status check](/docs/api/rest/reference/clips/methods/#operation/Transfertaskstatuscheck)
- [Get a clip](/docs/api/rest/reference/clips/methods/#operation/GetClipById)
- [List all clips](/docs/api/rest/reference/clips/methods/#operation/GetUserClips)

### clips:write

Manage your clips information

**Associated APIs:**

- [Delete a clip(soft delete)](/docs/api/rest/reference/clips/methods/#operation/DeleteClip)
- [Remove the collaborator from a clip](/docs/api/rest/reference/clips/methods/#operation/DeleteCollaborator)
- [Initiate and complete the multipart file upload for a clip](/docs/api/rest/reference/clips/methods/#operation/InitiateAndCompleteAClipMultipartUpload.)
- [Upload clip multipart files](/docs/api/rest/reference/clips/methods/#operation/UploadIqMultipartClipFile)
- [Delete a comment](/docs/api/rest/reference/clips/methods/#operation/Deleteacomment)
- [Upload clip file](/docs/api/rest/reference/clips/methods/#operation/UploadClipFile)

### clips:write:admin

Manage your clips information

**Associated APIs:**

- [Transfer clips owner](/docs/api/rest/reference/clips/methods/#operation/Transferclipsowner)
- [Remove the collaborator from a clip](/docs/api/rest/reference/clips/methods/#operation/DeleteCollaborator)
- [Initiate and complete the multipart file upload for a clip](/docs/api/rest/reference/clips/methods/#operation/InitiateAndCompleteAClipMultipartUpload.)
- [Upload clip file](/docs/api/rest/reference/clips/methods/#operation/UploadClipFile)
- [Delete a clip(soft delete)](/docs/api/rest/reference/clips/methods/#operation/DeleteClip)
- [Delete a comment](/docs/api/rest/reference/clips/methods/#operation/Deleteacomment)
- [Upload clip multipart files](/docs/api/rest/reference/clips/methods/#operation/UploadIqMultipartClipFile)

## Conference Room Connector (CRC)

### apiconnector:master

This scope allows an app to view and manage sub account’s API Connector information

**Associated APIs:**

- [List API Connectors](/docs/api/rest/reference/crc/ma/#operation/GetListAPIConnectors)
- [Get an API Connector](/docs/api/rest/reference/crc/ma/#operation/GetAPIConnector)
- [Update an API Connector](/docs/api/rest/reference/crc/ma/#operation/UpdateAPIConnector)
- [Create an API Connector](/docs/api/rest/reference/crc/ma/#operation/CreateAPIConnector)
- [Update an API Connector's private key](/docs/api/rest/reference/crc/ma/#operation/UpdateAPIConnectorPrivateKey)
- [Get an API Connector's private key](/docs/api/rest/reference/crc/ma/#operation/GetanAPIConnector'sprivatekey)
- [Delete an API Connector](/docs/api/rest/reference/crc/ma/#operation/DeleteAPIConnector)

### apiconnector:read:admin

This scope allow an app to view all API Connector information

**Associated APIs:**

- [Get an API Connector](/docs/api/rest/reference/crc/methods/#operation/GetAPIConnector)
- [List API Connectors](/docs/api/rest/reference/crc/methods/#operation/GetListAPIConnectors)
- [Get an API Connector's private key](/docs/api/rest/reference/crc/methods/#operation/GetanAPIConnector'sprivatekey)

### apiconnector:write:admin

This scope allow an app to view and manage all API Connector information

**Associated APIs:**

- [Update an API Connector](/docs/api/rest/reference/crc/methods/#operation/UpdateAPIConnector)
- [Delete an API Connector](/docs/api/rest/reference/crc/methods/#operation/DeleteAPIConnector)
- [Update an API Connector's private key](/docs/api/rest/reference/crc/methods/#operation/UpdateAPIConnectorPrivateKey)
- [Create an API Connector](/docs/api/rest/reference/crc/methods/#operation/CreateAPIConnector)

### crc:master

View and manage sub account's CRC configuration

**Associated APIs:**

- [Get participant identifier code](/docs/api/rest/reference/crc/methods/#operation/get_participant_identifier_code)

### crc:read:admin

View and manage CRC configuration

**Associated APIs:**

- [Get participant identifier code](/docs/api/rest/reference/crc/methods/#operation/get_participant_identifier_code)

### crc_account:master

View and manage all sub account's Cisco/Polycom room account setting

**Associated APIs:**

- [Get Cisco/Polycom Room Account Setting](/docs/api/rest/reference/crc/ma/#operation/getCiscoPolycomRoomAccountSetting)
- [Update Cisco/Polycom Room Account Setting](/docs/api/rest/reference/crc/ma/#operation/UpdateCiscoPolycomRoomAccountSetting)

### crc_account:read:admin

View Cisco/Polycom rooms account setting

**Associated APIs:**

- [Get Cisco/Polycom Room Account Setting](/docs/api/rest/reference/crc/methods/#operation/getCiscoPolycomRoomAccountSetting)

### crc_account:write:admin

View and manage Cisco/Polycom rooms account setting

**Associated APIs:**

- [Update Cisco/Polycom Room Account Setting](/docs/api/rest/reference/crc/methods/#operation/UpdateCiscoPolycomRoomAccountSetting)

### crc_rooms:master

View and manage sub account’s managed Cisco and Polycom rooms information

**Associated APIs:**

- [Delete a room template](/docs/api/rest/reference/crc/ma/#operation/Deletearoomtemplate)
- [Update a Managed Room](/docs/api/rest/reference/crc/ma/#operation/UpdateaManagedRoom)
- [Update a Room Template](/docs/api/rest/reference/crc/ma/#operation/UpdateaRoomTemplate)
- [Create a Managed Room](/docs/api/rest/reference/crc/ma/#operation/CreateaManagedRoom)
- [Get a Managed Room](/docs/api/rest/reference/crc/ma/#operation/GetaManagedRoom)
- [Get a Room Template](/docs/api/rest/reference/crc/ma/#operation/GetaRoomTemplate)
- [List Room Templates](/docs/api/rest/reference/crc/ma/#operation/ListRoomTemplates)
- [Delete a managed room](/docs/api/rest/reference/crc/ma/#operation/Deleteamanagedroom)
- [List Managed Rooms](/docs/api/rest/reference/crc/ma/#operation/ListManagedRooms)
- [Create a Room Template](/docs/api/rest/reference/crc/ma/#operation/CreateaRoomTemplate)

### crc_rooms:read:admin

View all managed Cisco and Polycom rooms information

**Associated APIs:**

- [Get a Room Template](/docs/api/rest/reference/crc/methods/#operation/GetaRoomTemplate)
- [List Managed Rooms](/docs/api/rest/reference/crc/methods/#operation/ListManagedRooms)
- [List Room Templates](/docs/api/rest/reference/crc/methods/#operation/ListRoomTemplates)
- [Get a Managed Room](/docs/api/rest/reference/crc/methods/#operation/GetaManagedRoom)

### crc_rooms:write:admin

View and manage all managed Cisco and Polycom rooms information

**Associated APIs:**

- [Delete a room template](/docs/api/rest/reference/crc/methods/#operation/Deletearoomtemplate)
- [Update a Room Template](/docs/api/rest/reference/crc/methods/#operation/UpdateaRoomTemplate)
- [Create a Room Template](/docs/api/rest/reference/crc/methods/#operation/CreateaRoomTemplate)
- [Create a Managed Room](/docs/api/rest/reference/crc/methods/#operation/CreateaManagedRoom)
- [Delete a managed room](/docs/api/rest/reference/crc/methods/#operation/Deleteamanagedroom)
- [Update a Managed Room](/docs/api/rest/reference/crc/methods/#operation/UpdateaManagedRoom)

## Contact Center

### contact_center_attachment:read:admin

View your contact center attachment information

**Associated APIs:**

- [Get an engagement's attachments](/docs/api/rest/reference/contact-center/methods/#operation/ListAttachments)

### contact_center_flow:write:admin

flow write

**Associated APIs:**

- [Delete a flow](/docs/api/rest/reference/contact-center/methods/#operation/DeleteFlow)
- [Edit a flow](/docs/api/rest/reference/contact-center/methods/#operation/EditFlow)
- [Publish a flow](/docs/api/rest/reference/contact-center/methods/#operation/PublishFlow)
- [Remove flow entry points](/docs/api/rest/reference/contact-center/methods/#operation/RemoveFlowEntryPoints)
- [Import a flow](/docs/api/rest/reference/contact-center/methods/#operation/ImportFlow)
- [Add flow entry points](/docs/api/rest/reference/contact-center/methods/#operation/AddFlowEntryPoints)

### contact_center_messaging:read:admin

Get message

**Associated APIs:**

- [List work item message history](/docs/api/rest/reference/contact-center/methods/#operation/getWorkItemMessageHistory)
- [List email message history](/docs/api/rest/reference/contact-center/methods/#operation/getEmailMessageHistory)
- [List message history](/docs/api/rest/reference/contact-center/methods/#operation/getMessageHistory)

### contact_center_messaging:write:admin

send message

**Associated APIs:**

- [Send a message](/docs/api/rest/reference/contact-center/methods/#operation/SendaMessage)

### contact_center_routing_profile:write:admin

Edit agent routing profile.

**Associated APIs:**

- [Update a consumer routing profile's details](/docs/api/rest/reference/contact-center/methods/#operation/Updateaconsumerroutingprofile'sdetails)
- [Delete an agent routing profile](/docs/api/rest/reference/contact-center/methods/#operation/Deleteanagentroutingprofile)
- [Create an agent routing profile](/docs/api/rest/reference/contact-center/methods/#operation/Createanagentroutingprofile)
- [Update an agent routing profile's details](/docs/api/rest/reference/contact-center/methods/#operation/Updateanagentroutingprofile'sdetails)
- [Delete a consumer routing profile](/docs/api/rest/reference/contact-center/methods/#operation/Deleteaconsumerroutingprofile)
- [Create a consumer routing profile](/docs/api/rest/reference/contact-center/methods/#operation/Createaconsumerroutingprofile)

### contact_center_team:read:admin

View your contact center team information

**Associated APIs:**

- [List teams](/docs/api/rest/reference/contact-center/methods/#operation/listTeams)
- [List team's parent teams](/docs/api/rest/reference/contact-center/methods/#operation/getTeamParentTeams)
- [Get a team](/docs/api/rest/reference/contact-center/methods/#operation/getTeamDetail)
- [List team supervisors](/docs/api/rest/reference/contact-center/methods/#operation/listTeamSupervisors)
- [List a team's child teams](/docs/api/rest/reference/contact-center/methods/#operation/getTeamChildTeams)
- [List team agents](/docs/api/rest/reference/contact-center/methods/#operation/listTeamAgents)

### contact_center_team:write:admin

Manage your contact center team information

**Associated APIs:**

- [Create a team](/docs/api/rest/reference/contact-center/methods/#operation/CreateTeam)
- [Assign team supervisors](/docs/api/rest/reference/contact-center/methods/#operation/assignTeamSupervisors)
- [Assign team agents](/docs/api/rest/reference/contact-center/methods/#operation/assignTeamAgents)
- [Delete a team](/docs/api/rest/reference/contact-center/methods/#operation/deleteTeam)
- [Unassign team agents](/docs/api/rest/reference/contact-center/methods/#operation/unassignTeamAgents)
- [Update a team](/docs/api/rest/reference/contact-center/methods/#operation/Updateateam)
- [Move a team](/docs/api/rest/reference/contact-center/methods/#operation/moveTeam)
- [Unassign team supervisors](/docs/api/rest/reference/contact-center/methods/#operation/unassignTeamSupervisors)

### contact_center_user_template:read:admin

View all contact center user template’s details.

**Associated APIs:**

- [Get a user template](/docs/api/rest/reference/contact-center/methods/#operation/Getanusertemplate)

### contact_center_user_template:write:admin

View and manage all contact center user template's details.

**Associated APIs:**

- [Update a user template](/docs/api/rest/reference/contact-center/methods/#operation/updateAUserTemplate)
- [Create a user template](/docs/api/rest/reference/contact-center/methods/#operation/createAUserTemplate)
- [Delete a user template](/docs/api/rest/reference/contact-center/methods/#operation/deleteAUserTemplate)

## ContactCenter

### contact_center_asset_library:read:admin

View your contact center asset library information

**Associated APIs:**

- [List assets](/docs/api/rest/reference/contact-center/methods/#operation/listAssets)
- [List asset categories](/docs/api/rest/reference/contact-center/methods/#operation/listAssetCategories)
- [Get an asset](/docs/api/rest/reference/contact-center/methods/#operation/getAnAsset)
- [Get an asset category](/docs/api/rest/reference/contact-center/methods/#operation/getAnAssetCategory)

### contact_center_asset_library:write:admin

Manage your contact center asset library information

**Associated APIs:**

- [Create an asset](/docs/api/rest/reference/contact-center/methods/#operation/createAnAsset)
- [Delete an asset](/docs/api/rest/reference/contact-center/methods/#operation/deleteAnAsset)
- [Update an asset](/docs/api/rest/reference/contact-center/methods/#operation/updateAnAsset)
- [Delete an asset category](/docs/api/rest/reference/contact-center/methods/#operation/deleteAnAssetCategory)
- [Create an asset category](/docs/api/rest/reference/contact-center/methods/#operation/createAnAssetCategory)
- [Update an asset category](/docs/api/rest/reference/contact-center/methods/#operation/updateAnAssetCategory)
- [Delete asset items](/docs/api/rest/reference/contact-center/methods/#operation/Deleteassetitems)
- [Duplicate an asset](/docs/api/rest/reference/contact-center/methods/#operation/duplicateAnAsset)

### contact_center_contact:read:admin

View address book information

**Associated APIs:**

- [List address books](/docs/api/rest/reference/contact-center/methods/#operation/listAddressBooks)
- [Get an address book unit](/docs/api/rest/reference/contact-center/methods/#operation/getUnit)
- [List address book units](/docs/api/rest/reference/contact-center/methods/#operation/listUnits)
- [List a contact's custom fields](/docs/api/rest/reference/contact-center/methods/#operation/ListContactCustomFields)
- [List an address book's custom fields](/docs/api/rest/reference/contact-center/methods/#operation/Listaddressbookcustomfields)
- [Get an address book](/docs/api/rest/reference/contact-center/methods/#operation/getAddressBook)
- [Get an address book contact](/docs/api/rest/reference/contact-center/methods/#operation/getContact)
- [List address book contacts](/docs/api/rest/reference/contact-center/methods/#operation/listContacts)
- [Get an address book's custom field](/docs/api/rest/reference/contact-center/methods/#operation/Getaaddressbookcustomfield)

### contact_center_contact:write:admin

Update address book information

**Associated APIs:**

- [Update an address book unit](/docs/api/rest/reference/contact-center/methods/#operation/updateUnit)
- [Update an address book contact](/docs/api/rest/reference/contact-center/methods/#operation/updateContact)
- [Update an address book custom field](/docs/api/rest/reference/contact-center/methods/#operation/Updateacustomfield)
- [Create an address book contact](/docs/api/rest/reference/contact-center/methods/#operation/createContact)
- [Create an address book unit](/docs/api/rest/reference/contact-center/methods/#operation/createUnit)
- [Create an address book custom field](/docs/api/rest/reference/contact-center/methods/#operation/Createacustomfield)
- [Delete an address book contact](/docs/api/rest/reference/contact-center/methods/#operation/contactDelete)
- [Delete an address book custom field](/docs/api/rest/reference/contact-center/methods/#operation/Deleteancustomfield)
- [Delete an address book unit](/docs/api/rest/reference/contact-center/methods/#operation/deleteUnit)
- [Delete an address book](/docs/api/rest/reference/contact-center/methods/#operation/deleteAddressBook)
- [Create an address book](/docs/api/rest/reference/contact-center/methods/#operation/createAddressBook)
- [Update an address book](/docs/api/rest/reference/contact-center/methods/#operation/updateAddressBook)

### contact_center_disposition:read:admin

View your contact center disposition information

**Associated APIs:**

- [Get a disposition set](/docs/api/rest/reference/contact-center/methods/#operation/getSet)
- [List disposition sets](/docs/api/rest/reference/contact-center/methods/#operation/listSets)
- [Get a disposition](/docs/api/rest/reference/contact-center/methods/#operation/getDisposition)
- [List dispositions](/docs/api/rest/reference/contact-center/methods/#operation/listDispositions)

### contact_center_disposition:write:admin

Manage your contact center disposition information

**Associated APIs:**

- [Create a disposition set](/docs/api/rest/reference/contact-center/methods/#operation/createSet)
- [Delete a disposition](/docs/api/rest/reference/contact-center/methods/#operation/deleteDisposition)
- [Update a disposition](/docs/api/rest/reference/contact-center/methods/#operation/updateDisposition)
- [Delete a disposition set](/docs/api/rest/reference/contact-center/methods/#operation/deleteSet)
- [Update a disposition set](/docs/api/rest/reference/contact-center/methods/#operation/updateSet)
- [Create a disposition](/docs/api/rest/reference/contact-center/methods/#operation/createDisposition)

### contact_center_engagement:read:admin

View all contact center engagement information

**Associated APIs:**

- [Poll an engagement recording's status](/docs/api/rest/reference/contact-center/methods/#operation/EngagementRecordingStatus)
- [Get an engagement's survey](/docs/api/rest/reference/contact-center/methods/#operation/getEngagementSurvey)

### contact_center_engagement:write:admin

Manage all contact center engagement information

**Associated APIs:**

- [Control an engagement's recording](/docs/api/rest/reference/contact-center/methods/#operation/engagementRecordingControl)
- [Update an engagement](/docs/api/rest/reference/contact-center/methods/#operation/updateEngagement)
- [Start an engagement](/docs/api/rest/reference/contact-center/methods/#operation/Startworkitemengagement)

### contact_center_flow:read:admin

View all contact center flow information

**Associated APIs:**

- [List the closures' flows](/docs/api/rest/reference/contact-center/methods/#operation/listClosureSetFlows)
- [List flows](/docs/api/rest/reference/contact-center/methods/#operation/listFlows)
- [Export a flow](/docs/api/rest/reference/contact-center/methods/#operation/ExportFlow)
- [List entry points](/docs/api/rest/reference/contact-center/methods/#operation/ListentryPoints)
- [List flow's entry points](/docs/api/rest/reference/contact-center/methods/#operation/ListFlowEntryPoints)
- [Get a flow](/docs/api/rest/reference/contact-center/methods/#operation/getAFlow)
- [List the business hours' flows](/docs/api/rest/reference/contact-center/methods/#operation/listBusinessHourFlows)

### contact_center_inbox:read:admin

View all contact center inbox information

**Associated APIs:**

- [List an inbox's messages](/docs/api/rest/reference/contact-center/methods/#operation/listInboxMessages)
- [Get an inbox](/docs/api/rest/reference/contact-center/methods/#operation/getInbox)
- [List inboxes](/docs/api/rest/reference/contact-center/methods/#operation/listInbox)
- [Get inbox email notification list](/docs/api/rest/reference/contact-center/methods/#operation/Getinboxemailnotificationlist)
- [List an account's inbox messages](/docs/api/rest/reference/contact-center/methods/#operation/listInboxesMessages)

### contact_center_inbox:write:admin

Manage all contact center inbox information

**Associated APIs:**

- [Update an inbox](/docs/api/rest/reference/contact-center/methods/#operation/inboxUpdate)
- [Delete an inbox's messages](/docs/api/rest/reference/contact-center/methods/#operation/inboxMessagesDelete)
- [Delete inboxes](/docs/api/rest/reference/contact-center/methods/#operation/inboxesDelete)
- [Update an inbox email notification](/docs/api/rest/reference/contact-center/methods/#operation/Updateaninboxemailnotification)
- [Create an inbox](/docs/api/rest/reference/contact-center/methods/#operation/inboxCreate)
- [Delete inbox messages](/docs/api/rest/reference/contact-center/methods/#operation/inboxesMessagesDelete)
- [Delete an inbox message](/docs/api/rest/reference/contact-center/methods/#operation/inboxMessageDelete)

### contact_center_note:read:admin

View all contact center note information

**Associated APIs:**

- [List notes](/docs/api/rest/reference/contact-center/methods/#operation/notes)
- [Get a note](/docs/api/rest/reference/contact-center/methods/#operation/getNote)
- [List engagement notes](/docs/api/rest/reference/contact-center/methods/#operation/engagementNotes)

### contact_center_note:write

Manage all contact center note information

**Associated APIs:**

- [Update a note](/docs/api/rest/reference/contact-center/methods/#operation/noteUpdate)

### contact_center_operating_hours:read:admin

View all contact center operating hours information

**Associated APIs:**

- [List business hours](/docs/api/rest/reference/contact-center/methods/#operation/listBusinessHours)
- [Get a closure set](/docs/api/rest/reference/contact-center/methods/#operation/getAClosureSet)
- [List closures](/docs/api/rest/reference/contact-center/methods/#operation/listClosures)
- [Get business hours](/docs/api/rest/reference/contact-center/methods/#operation/getABusinessHour)

### contact_center_operating_hours:write:admin

Manage all contact center operating hours information

**Associated APIs:**

- [Create business hours](/docs/api/rest/reference/contact-center/methods/#operation/businessHourCreate)
- [Delete business hours](/docs/api/rest/reference/contact-center/methods/#operation/businessHourDelete)
- [Update business hours](/docs/api/rest/reference/contact-center/methods/#operation/businessHourUpdate)
- [Create a closure set](/docs/api/rest/reference/contact-center/methods/#operation/closuresSetCreate)
- [Delete a closure set](/docs/api/rest/reference/contact-center/methods/#operation/closureSetDelete)
- [Update a closure set](/docs/api/rest/reference/contact-center/methods/#operation/closureSetUpdate)

### contact_center_operation_logs:read:admin

Read permission for Operation logs

**Associated APIs:**

- [List operation logs](/docs/api/rest/reference/contact-center/methods/#operation/listOperationLogs)

### contact_center_outbound_campaign:delete:admin

Delete an Outbound Campaign.

**Associated APIs:**

- [Delete an outbound campaign](/docs/api/rest/reference/contact-center/methods/#operation/deleteOutboundCampaign)

### contact_center_outbound_campaign:read:admin

View an Outbound Campaign.

**Associated APIs:**

- [List outbound campaigns](/docs/api/rest/reference/contact-center/methods/#operation/listOutboundCampaigns)
- [Get an outbound campaign](/docs/api/rest/reference/contact-center/methods/#operation/getOutboundCampaign)

### contact_center_outbound_campaign:update:admin

Update an Outbound Campaign

**Associated APIs:**

- [Update an outbound campaign](/docs/api/rest/reference/contact-center/methods/#operation/updateOutboundCampaign)

### contact_center_outbound_campaign:write:admin

Create an Outbound Campaign

**Associated APIs:**

- [Update an outbound campaign status](/docs/api/rest/reference/contact-center/methods/#operation/Updateanoutboundcampaignstatus)
- [Create an outbound campaign](/docs/api/rest/reference/contact-center/methods/#operation/createOutboundCampaign)

### contact_center_outbound_campaign_contactlist:read:admin

Get campaign contact list

**Associated APIs:**

- [Get a campaign contact list](/docs/api/rest/reference/contact-center/methods/#operation/getCampaignContactList)
- [List campaign contact lists](/docs/api/rest/reference/contact-center/methods/#operation/listCampaignContactLists)

### contact_center_outbound_campaign_contactlist:write:admin

Create campaign contact list

**Associated APIs:**

- [Create a campaign contact list](/docs/api/rest/reference/contact-center/methods/#operation/createCampaignContactList)
- [Update a campaign contact list](/docs/api/rest/reference/contact-center/methods/#operation/updateCampaignContactList)
- [Remove a campaign contact list](/docs/api/rest/reference/contact-center/methods/#operation/deleteCampaignContactList)

### contact_center_outbound_campaign_contacts:read:admin

Get campaign contact list contact

**Associated APIs:**

- [Get a campaign contact list's contact](/docs/api/rest/reference/contact-center/methods/#operation/getCampaignContactListContact)
- [List campaign contact list contacts](/docs/api/rest/reference/contact-center/methods/#operation/listCampaignContactListContacts)

### contact_center_outbound_campaign_contacts:write:admin

Create campaign contact list contact

**Associated APIs:**

- [Create a campaign contact list's contact](/docs/api/rest/reference/contact-center/methods/#operation/createCampaignContactListContact)
- [Update contact on a campaign contact list](/docs/api/rest/reference/contact-center/methods/#operation/updateCampaignContactListContact)
- [Remove campaign contact list's contact](/docs/api/rest/reference/contact-center/methods/#operation/deleteCampaigncontactListContact)

### contact_center_preference:read:admin

View your contact center preference information

**Associated APIs:**

- [List system statuses](/docs/api/rest/reference/contact-center/methods/#operation/listSystemStatus)
- [Get a system status](/docs/api/rest/reference/contact-center/methods/#operation/getAStatus)

### contact_center_preference:write:admin

Manage your contact center preference information

**Associated APIs:**

- [Update a system status](/docs/api/rest/reference/contact-center/methods/#operation/updateSystemStatus)
- [Create a system status](/docs/api/rest/reference/contact-center/methods/#operation/createSystemStatus)
- [Delete a system status](/docs/api/rest/reference/contact-center/methods/#operation/deleteSystemStatus)

### contact_center_queue:read:admin

View your contact center queue information

**Associated APIs:**

- [List a queue's scheduled callbacks availability](/docs/api/rest/reference/contact-center/methods/#operation/Listqueuescheduledcallbacksavailability)
- [List queue templates](/docs/api/rest/reference/contact-center/methods/#operation/Listqueuetemplates)
- [List queue disposition sets](/docs/api/rest/reference/contact-center/methods/#operation/getQueueDispositionSets)
- [Get a closure set](/docs/api/rest/reference/contact-center/methods/#operation/getAClosureSet)
- [List queue supervisors](/docs/api/rest/reference/contact-center/methods/#operation/getQueueSupervisors)
- [List closures](/docs/api/rest/reference/contact-center/methods/#operation/listClosures)
- [List queue dispositions](/docs/api/rest/reference/contact-center/methods/#operation/getQueueDispositions)
- [List business hours](/docs/api/rest/reference/contact-center/methods/#operation/listBusinessHours)
- [List queue agents](/docs/api/rest/reference/contact-center/methods/#operation/getQueueAgents)
- [Get inbox access queues](/docs/api/rest/reference/contact-center/methods/#operation/listInboxQueues)
- [List the business hours' queues](/docs/api/rest/reference/contact-center/methods/#operation/listBusinessHourQueues)
- [Get a queue](/docs/api/rest/reference/contact-center/methods/#operation/getAQueue)
- [List the closures' queues](/docs/api/rest/reference/contact-center/methods/#operation/listClosureSetQueues)
- [Get a queue's operating hours](/docs/api/rest/reference/contact-center/methods/#operation/getAQueueOperatingHours)
- [Get business hours](/docs/api/rest/reference/contact-center/methods/#operation/getABusinessHour)
- [List queues](/docs/api/rest/reference/contact-center/methods/#operation/listQueues)

### contact_center_queue:write:admin

Manage your contact center queue information

**Associated APIs:**

- [Unassign a queue team](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueTeam)
- [Delete a queue's interrupt menu configuration](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueInterruptMenu)
- [Unassign multiple teams in a queue](/docs/api/rest/reference/contact-center/methods/#operation/batchDeleteQueueTeams)
- [Assign queue dispositions](/docs/api/rest/reference/contact-center/methods/#operation/assignQueueDispositions)
- [Batch create queues with a template](/docs/api/rest/reference/contact-center/methods/#operation/Batchcreatequeueswithatemplate)
- [Unassign a queue agent](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueAgent)
- [Update a queue](/docs/api/rest/reference/contact-center/methods/#operation/queueUpdate)
- [Update a queue's operating hours](/docs/api/rest/reference/contact-center/methods/#operation/QueueOperatingHoursUpdate)
- [Create business hours](/docs/api/rest/reference/contact-center/methods/#operation/businessHourCreate)
- [Unassign a queue supervisor](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueSupervisor)
- [Batch delete queues](/docs/api/rest/reference/contact-center/methods/#operation/Batchdeletequeues)
- [Assign queue teams](/docs/api/rest/reference/contact-center/methods/#operation/assignQueueTeams)
- [Unassign a queue disposition set](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueDispositionSet)
- [Remove inbox access queues](/docs/api/rest/reference/contact-center/methods/#operation/unassignInboxQueues)
- [Update a queue's interrupt settings](/docs/api/rest/reference/contact-center/methods/#operation/updateQueueInterrupts)
- [Assign inbox access queues](/docs/api/rest/reference/contact-center/methods/#operation/assignInboxQueues)
- [Delete an attendee from a scheduled callback event](/docs/api/rest/reference/contact-center/methods/#operation/Deleteascheduledcallbackforanattendee)
- [Schedule a callback on a queue](/docs/api/rest/reference/contact-center/methods/#operation/Scheduleacallbackonaqueue)
- [Unassign a queue disposition](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueDisposition)
- [Update a queue agent](/docs/api/rest/reference/contact-center/methods/#operation/updateQueueAgent)
- [Delete a queue](/docs/api/rest/reference/contact-center/methods/#operation/queueDelete)
- [Create a closure set](/docs/api/rest/reference/contact-center/methods/#operation/closuresSetCreate)
- [Create a queue](/docs/api/rest/reference/contact-center/methods/#operation/queueCreate)
- [Assign queue disposition sets](/docs/api/rest/reference/contact-center/methods/#operation/assignQueueDispositionSets)
- [Assign queue agents](/docs/api/rest/reference/contact-center/methods/#operation/assignQueueAgents)
- [Assign a queue menu based interrupt](/docs/api/rest/reference/contact-center/methods/#operation/assignQueueMenuBasedInterrupt)
- [Assign queue supervisors](/docs/api/rest/reference/contact-center/methods/#operation/assignQueueSupervisors)

### contact_center_recording:read

View your contact center recording information.

**Associated APIs:**

- [List queue recordings](/docs/api/rest/reference/contact-center/methods/#operation/listQueueRecordings)
- [List a user's recordings](/docs/api/rest/reference/contact-center/methods/#operation/listUserRecordings)

### contact_center_recording:read:admin

View all contact center recording information

**Associated APIs:**

- [List recordings](/docs/api/rest/reference/contact-center/methods/#operation/listRecordings)
- [List a user's recordings](/docs/api/rest/reference/contact-center/methods/#operation/listUserRecordings)
- [List queue recordings](/docs/api/rest/reference/contact-center/methods/#operation/listQueueRecordings)
- [List engagement recordings](/docs/api/rest/reference/contact-center/methods/#operation/listEngagementRecordings)

### contact_center_recording:write:admin

Manage all contact center recording information

**Associated APIs:**

- [Delete a recording](/docs/api/rest/reference/contact-center/methods/#operation/deleteRecording)
- [Delete engagement recordings](/docs/api/rest/reference/contact-center/methods/#operation/deleteEngagementRecordings)
- [Delete queue recordings](/docs/api/rest/reference/contact-center/methods/#operation/deleteQueueRecordings)
- [Delete a user's recordings](/docs/api/rest/reference/contact-center/methods/#operation/deleteUserRecordings)

### contact_center_region:read:admin

View all contact center region information

**Associated APIs:**

- [Get a region](/docs/api/rest/reference/contact-center/methods/#operation/GetARegion)
- [List regions](/docs/api/rest/reference/contact-center/methods/#operation/ListRegions)
- [List a region's users](/docs/api/rest/reference/contact-center/methods/#operation/ListRegion'sUsers)

### contact_center_region:write:admin

Manage all contact center region information

**Associated APIs:**

- [Delete a region](/docs/api/rest/reference/contact-center/methods/#operation/DeleteARegion)
- [Update a region](/docs/api/rest/reference/contact-center/methods/#operation/UpdateARegion)
- [Create a region](/docs/api/rest/reference/contact-center/methods/#operation/CreateARegion)
- [Assign users to a region](/docs/api/rest/reference/contact-center/methods/#operation/AssignUsersToARegion)

### contact_center_report:read:admin

View all contact center report information

**Associated APIs:**

- [List historical queue's agents reports](/docs/api/rest/reference/contact-center/methods/#operation/listQueueAgentMetric)
- [List agent's status history reports](/docs/api/rest/reference/contact-center/methods/#operation/listAgentStatusHistory)
- [Get an engagement's events](/docs/api/rest/reference/contact-center/methods/#operation/getEngagementEvents)
- [List historical outbound dialer performance dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricaloutbounddialerperformancedatasetdata)
- [List historical disposition dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricaldispositiondatasetdata)
- [Get an engagement](/docs/api/rest/reference/contact-center/methods/#operation/getEngagement)
- [List historical queue reports](/docs/api/rest/reference/contact-center/methods/#operation/listHistoricalQueueMetric)
- [List historical engagement dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listengagementdatasetdata)
- [List historical detail reports](/docs/api/rest/reference/contact-center/methods/#operation/listHistoricalDetailMetric)
- [List historical queue performance dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricalqueueperformancedatasetdata)
- [List historical flow performance dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricalflowperformancedatasetdata)
- [List historical agent timecard dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricalagenttimecarddatasetdata)
- [List agent leg reports](/docs/api/rest/reference/contact-center/methods/#operation/listAgentLegMetric)
- [List agent's time sheet reports](/docs/api/rest/reference/contact-center/methods/#operation/listAgentTimeSheet)
- [List historical agent reports by queue](/docs/api/rest/reference/contact-center/methods/#operation/listQueueAgentsMetrics)
- [List engagements](/docs/api/rest/reference/contact-center/methods/#operation/listEngagements)
- [List historical Zoom Phone to Contact Center call journey data](/docs/api/rest/reference/contact-center/methods/#operation/ListhistoricalZoomphonetozcccalljourneydata)
- [List historical engagement log data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricalengagementlogs)
- [List historical agent performance dataset data](/docs/api/rest/reference/contact-center/methods/#operation/Listhistoricalagentperformancedatasetdata)

### contact_center_role:read:admin

View your contact center role information

**Associated APIs:**

- [Get a role](/docs/api/rest/reference/contact-center/methods/#operation/getRole)
- [List users of a role](/docs/api/rest/reference/contact-center/methods/#operation/getRoleUsers)
- [List roles](/docs/api/rest/reference/contact-center/methods/#operation/listRoles)

### contact_center_role:write:admin

Manage your contact center role information

**Associated APIs:**

- [Delete a role](/docs/api/rest/reference/contact-center/methods/#operation/deleteRole)
- [Assign a role](/docs/api/rest/reference/contact-center/methods/#operation/assignRoleUsers)
- [Delete role privileges](/docs/api/rest/reference/contact-center/methods/#operation/Deleteroleprivileges)
- [Update a role](/docs/api/rest/reference/contact-center/methods/#operation/updateRole)
- [Create a role](/docs/api/rest/reference/contact-center/methods/#operation/createRole)
- [Unassign a role](/docs/api/rest/reference/contact-center/methods/#operation/deleteRoleUser)
- [Duplicate a role](/docs/api/rest/reference/contact-center/methods/#operation/Duplicatearole)

### contact_center_routing_profile:read:admin

View routing profile information.

**Associated APIs:**

- [Get a consumer routing profile](/docs/api/rest/reference/contact-center/methods/#operation/Getaconsumerroutingprofile)
- [List agent routing profiles](/docs/api/rest/reference/contact-center/methods/#operation/Listagentroutingprofiles)
- [Get an agent routing profile](/docs/api/rest/reference/contact-center/methods/#operation/getAgentRoutingProfile)
- [List consumer routing profiles](/docs/api/rest/reference/contact-center/methods/#operation/Listconsumerroutingprofiles)

### contact_center_skill:read:admin

View all contact center skill information

**Associated APIs:**

- [List user's skills](/docs/api/rest/reference/contact-center/methods/#operation/ListAUserSkills)
- [Get a skill](/docs/api/rest/reference/contact-center/methods/#operation/getSkill)
- [Get a skill category](/docs/api/rest/reference/contact-center/methods/#operation/getSkillCategory)
- [List skills](/docs/api/rest/reference/contact-center/methods/#operation/listSkills)
- [List skill categories](/docs/api/rest/reference/contact-center/methods/#operation/listSkillCategory)

### contact_center_skill:write:admin

Manage all contact center skill information

**Associated APIs:**

- [Update a skill category](/docs/api/rest/reference/contact-center/methods/#operation/SkillCategoryUpdate)
- [Create a skill category](/docs/api/rest/reference/contact-center/methods/#operation/SkillCategoryCreate)
- [Delete a skill category](/docs/api/rest/reference/contact-center/methods/#operation/SkillCategoryDelete)
- [Update a skill](/docs/api/rest/reference/contact-center/methods/#operation/skillNameUpdate)
- [Assign user's skills](/docs/api/rest/reference/contact-center/methods/#operation/assignSkills)
- [Create a skill](/docs/api/rest/reference/contact-center/methods/#operation/skillCreate)
- [Delete a skill](/docs/api/rest/reference/contact-center/methods/#operation/skillDelete)
- [Unassign user's skill](/docs/api/rest/reference/contact-center/methods/#operation/deleteASkill)

### contact_center_sms:master

View sub account’s SMS log information

**Associated APIs:**

- [List SMS logs](/docs/api/rest/reference/contact-center/ma/#operation/listSMS)

### contact_center_sms:read:admin

View all contact center SMS log information

**Associated APIs:**

- [List SMS logs](/docs/api/rest/reference/contact-center/methods/#operation/listSMS)

### contact_center_user:read:admin

View all contact center user’s details

**Associated APIs:**

- [List users of a skill](/docs/api/rest/reference/contact-center/methods/#operation/listSkillUsers)
- [List user's devices](/docs/api/rest/reference/contact-center/methods/#operation/Listuserdevices)
- [List users' profiles](/docs/api/rest/reference/contact-center/methods/#operation/users)
- [Get a user's profile](/docs/api/rest/reference/contact-center/methods/#operation/userGet)
- [List user's queues](/docs/api/rest/reference/contact-center/methods/#operation/listUserQueues)
- [List user templates](/docs/api/rest/reference/contact-center/methods/#operation/ListUserTemplates)
- [Get an inbox's users](/docs/api/rest/reference/contact-center/methods/#operation/listInboxUsers)

### contact_center_user:write:admin

View and manage all contact center user's details

**Associated APIs:**

- [Update a user's profile](/docs/api/rest/reference/contact-center/methods/#operation/userUpdate)
- [Assign inbox access users](/docs/api/rest/reference/contact-center/methods/#operation/assignInboxUsers)
- [Batch update user status](/docs/api/rest/reference/contact-center/methods/#operation/Batchupdateuserstatus)
- [Unassign inbox access users](/docs/api/rest/reference/contact-center/methods/#operation/unassignInboxUsers)
- [Batch delete user profiles](/docs/api/rest/reference/contact-center/methods/#operation/batchDeleteUsers)
- [Create a user's profile](/docs/api/rest/reference/contact-center/methods/#operation/createUser)
- [Batch create user profiles](/docs/api/rest/reference/contact-center/methods/#operation/BatchCreateUsers)
- [Batch update user profiles](/docs/api/rest/reference/contact-center/methods/#operation/BatchUpdateUsers)
- [Update a user's status](/docs/api/rest/reference/contact-center/methods/#operation/Updateauser'sstatus)
- [Delete a user's profile](/docs/api/rest/reference/contact-center/methods/#operation/userDelete)
- [Command control of a user](/docs/api/rest/reference/contact-center/methods/#operation/userControl)

### contact_center_variable:read:admin

View all contact center variable information

**Associated APIs:**

- [Get a variable](/docs/api/rest/reference/contact-center/methods/#operation/variableGet)
- [Get a variable group](/docs/api/rest/reference/contact-center/methods/#operation/getAVariableGroup)
- [List variable groups](/docs/api/rest/reference/contact-center/methods/#operation/listVariableGroups)
- [List variables](/docs/api/rest/reference/contact-center/methods/#operation/variables)

### contact_center_variable:write:admin

Manage all contact center variable information

**Associated APIs:**

- [Create a variable](/docs/api/rest/reference/contact-center/methods/#operation/createVariable)
- [Create a variable group](/docs/api/rest/reference/contact-center/methods/#operation/createVariableGroup)
- [Update a variable](/docs/api/rest/reference/contact-center/methods/#operation/variableUpdate)
- [Update a variable group](/docs/api/rest/reference/contact-center/methods/#operation/updateVariableGroup)
- [Delete a variable](/docs/api/rest/reference/contact-center/methods/#operation/variableDelete)
- [Delete a variable group](/docs/api/rest/reference/contact-center/methods/#operation/DeleteGroup)

### contact_center_variable_log:read:admin

View variable log information

**Associated APIs:**

- [List variable logs](/docs/api/rest/reference/contact-center/methods/#operation/listVariableLogs)
- [Get a variable log](/docs/api/rest/reference/contact-center/methods/#operation/getVariableLog)

### contact_center_variable_log:write:admin

Manage variable log information

**Associated APIs:**

- [Delete a variable log](/docs/api/rest/reference/contact-center/methods/#operation/deleteVariableLog)

### contact_center_voice_call:master

View sub account’s voice call information

**Associated APIs:**

- [List voice call logs](/docs/api/rest/reference/contact-center/ma/#operation/listVoiceCall)

### contact_center_voice_call:read:admin

view voice call information

**Associated APIs:**

- [List voice call logs](/docs/api/rest/reference/contact-center/methods/#operation/listVoiceCall)

## Contacts

### contact:read

View current user's contacts

**Associated APIs:**

- [Search company contacts](/docs/api/rest/reference/chat/methods/#operation/searchCompanyContacts)

### contact:read:admin

View all users' contacts

**Associated APIs:**

- [Search company contacts](/docs/api/rest/reference/chat/methods/#operation/searchCompanyContacts)

## Dashboard

### dashboard:master

View sub account's Dashboard data

**Associated APIs:**

- [Get issues of Zoom Rooms](/docs/api/rest/reference/account/ma/#operation/dashboardIssueDetailZoomRoom)
- [List webinars](/docs/api/rest/reference/account/ma/#operation/dashboardWebinars)
- [Get meeting sharing/recording details](/docs/api/rest/reference/account/ma/#operation/dashboardMeetingParticipantShare)
- [Get meeting quality scores](/docs/api/rest/reference/account/ma/#operation/dashboardQuality)
- [List client meeting satisfaction](/docs/api/rest/reference/account/ma/#operation/listMeetingSatisfaction)
- [Get CRC port usage](/docs/api/rest/reference/account/ma/#operation/dashboardCRC)
- [List meeting participants](/docs/api/rest/reference/account/ma/#operation/dashboardMeetingParticipants)
- [Get post meeting feedback](/docs/api/rest/reference/account/ma/#operation/participantFeedback)
- [List meeting participants QoS Summary](/docs/api/rest/reference/qss/ma/#operation/dashboardMeetingParticipantsQOSSummary)
- [Get chat metrics](/docs/api/rest/reference/account/ma/#operation/dashboardChat)
- [Get webinar participant QoS](/docs/api/rest/reference/account/ma/#operation/dashboardWebinarParticipantQOS)
- [Get Zoom Rooms details](/docs/api/rest/reference/account/ma/#operation/dashboardZoomRoom)
- [Get webinar sharing/recording details](/docs/api/rest/reference/account/ma/#operation/dashboardWebinarParticipantShare)
- [Get zoom meetings client feedback](/docs/api/rest/reference/account/ma/#operation/dashboardClientFeedbackDetail)
- [List the client versions](/docs/api/rest/reference/account/ma/#operation/getClientVersions)
- [Get webinar details](/docs/api/rest/reference/account/ma/#operation/dashboardWebinarDetail)
- [Get webinar participants](/docs/api/rest/reference/account/ma/#operation/dashboardWebinarParticipants)
- [List webinar participant QoS](/docs/api/rest/reference/account/ma/#operation/dashboardWebinarParticipantsQOS)
- [List Zoom meetings client feedback](/docs/api/rest/reference/account/ma/#operation/dashboardClientFeedback)
- [List webinar participants QoS Summary](/docs/api/rest/reference/qss/ma/#operation/dashboardWebinarParticipantsQOSSummary)
- [List Zoom Rooms](/docs/api/rest/reference/account/ma/#operation/dashboardZoomRooms)
- [Get meeting participant QoS](/docs/api/rest/reference/account/ma/#operation/dashboardMeetingParticipantQOS)
- [Get meeting details](/docs/api/rest/reference/account/ma/#operation/dashboardMeetingDetail)
- [Get post webinar feedback](/docs/api/rest/reference/account/ma/#operation/participantWebinarFeedback)
- [Get top 25 issues of Zoom Rooms](/docs/api/rest/reference/account/ma/#operation/dashboardZoomRoomIssue)
- [List meeting participants QoS](/docs/api/rest/reference/account/ma/#operation/dashboardMeetingParticipantsQOS)
- [Get top 25 Zoom Rooms with issues](/docs/api/rest/reference/account/ma/#operation/dashboardIssueZoomRoom)

### dashboard:read:admin

View Dashboard data

**Associated APIs:**

- [Get issues of Zoom Rooms](/docs/api/rest/reference/account/methods/#operation/dashboardIssueDetailZoomRoom)
- [List webinars](/docs/api/rest/reference/account/methods/#operation/dashboardWebinars)
- [Get meeting sharing/recording details](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingParticipantShare)
- [Get meeting quality scores](/docs/api/rest/reference/account/methods/#operation/dashboardQuality)
- [Get webinar participant QoS](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarParticipantQOS)
- [Get chat metrics](/docs/api/rest/reference/account/methods/#operation/dashboardChat)
- [Get top 25 issues of Zoom Rooms](/docs/api/rest/reference/account/methods/#operation/dashboardZoomRoomIssue)
- [Get meeting participant QoS](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingParticipantQOS)
- [List Zoom Rooms](/docs/api/rest/reference/account/methods/#operation/dashboardZoomRooms)
- [List meeting participants QoS Summary](/docs/api/rest/reference/qss/methods/#operation/dashboardMeetingParticipantsQOSSummary)
- [List meeting participants](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingParticipants)
- [Get CRC port usage](/docs/api/rest/reference/account/methods/#operation/dashboardCRC)
- [List webinar participant QoS](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarParticipantsQOS)
- [List Zoom meetings client feedback](/docs/api/rest/reference/account/methods/#operation/dashboardClientFeedback)
- [List webinar participants QoS Summary](/docs/api/rest/reference/qss/methods/#operation/dashboardWebinarParticipantsQOSSummary)
- [List the client versions](/docs/api/rest/reference/account/methods/#operation/getClientVersions)
- [Get webinar details](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarDetail)
- [Get webinar participants](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarParticipants)
- [List meetings](/docs/api/rest/reference/account/methods/#operation/dashboardMeetings)
- [Get post webinar feedback](/docs/api/rest/reference/account/methods/#operation/participantWebinarFeedback)
- [Get meeting details](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingDetail)
- [Get Zoom Rooms details](/docs/api/rest/reference/account/methods/#operation/dashboardZoomRoom)
- [Get webinar sharing/recording details](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarParticipantShare)
- [Get zoom meetings client feedback](/docs/api/rest/reference/account/methods/#operation/dashboardClientFeedbackDetail)
- [List meeting participants QoS](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingParticipantsQOS)
- [Get top 25 Zoom Rooms with issues](/docs/api/rest/reference/account/methods/#operation/dashboardIssueZoomRoom)
- [Get post meeting feedback](/docs/api/rest/reference/account/methods/#operation/participantFeedback)
- [List client meeting satisfaction](/docs/api/rest/reference/account/methods/#operation/listMeetingSatisfaction)

### dashboard_crc:read:admin

View all users' usage statistics of CRC

**Associated APIs:**

- [Get CRC port usage](/docs/api/rest/reference/account/methods/#operation/dashboardCRC)

### dashboard_home:read:admin

View overview of usage statistics for Meetings and Zoom Rooms

**Associated APIs:**

- [Get issues of Zoom Rooms](/docs/api/rest/reference/account/methods/#operation/dashboardIssueDetailZoomRoom)
- [Get top 25 Zoom Rooms with issues](/docs/api/rest/reference/account/methods/#operation/dashboardIssueZoomRoom)
- [List client meeting satisfaction](/docs/api/rest/reference/account/methods/#operation/listMeetingSatisfaction)
- [List Zoom meetings client feedback](/docs/api/rest/reference/account/methods/#operation/dashboardClientFeedback)
- [Get zoom meetings client feedback](/docs/api/rest/reference/account/methods/#operation/dashboardClientFeedbackDetail)
- [Get meeting quality scores](/docs/api/rest/reference/account/methods/#operation/dashboardQuality)
- [List the client versions](/docs/api/rest/reference/account/methods/#operation/getClientVersions)

### dashboard_im:read:admin

View all users' usage statistics of team chat messages and message types

**Associated APIs:**

- [Get chat metrics](/docs/api/rest/reference/account/methods/#operation/dashboardChat)

### dashboard_meetings:read:admin

View all users' meetings information on Dashboard

**Associated APIs:**

- [List meeting participants QoS Summary](/docs/api/rest/reference/qss/methods/#operation/dashboardMeetingParticipantsQOSSummary)
- [List meeting participants QoS](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingParticipantsQOS)
- [List meeting participants](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingParticipants)
- [Get post meeting feedback](/docs/api/rest/reference/account/methods/#operation/participantFeedback)
- [Get meeting sharing/recording details](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingParticipantShare)
- [List meetings](/docs/api/rest/reference/account/methods/#operation/dashboardMeetings)
- [Get meeting details](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingDetail)
- [Get meeting participant QoS](/docs/api/rest/reference/account/methods/#operation/dashboardMeetingParticipantQOS)

### dashboard_webinars:read:admin

View all users' webinar information on Dashboard

**Associated APIs:**

- [Get webinar participants](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarParticipants)
- [Get webinar sharing/recording details](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarParticipantShare)
- [List webinars](/docs/api/rest/reference/account/methods/#operation/dashboardWebinars)
- [List webinar participant QoS](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarParticipantsQOS)
- [Get webinar participant QoS](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarParticipantQOS)
- [Get post webinar feedback](/docs/api/rest/reference/account/methods/#operation/participantWebinarFeedback)
- [List webinar participants QoS Summary](/docs/api/rest/reference/qss/methods/#operation/dashboardWebinarParticipantsQOSSummary)
- [Get webinar details](/docs/api/rest/reference/account/methods/#operation/dashboardWebinarDetail)

### dashboard_zr:read:admin

View all users' Zoom Room usage statistics and information

**Associated APIs:**

- [Get Zoom Rooms details](/docs/api/rest/reference/account/methods/#operation/dashboardZoomRoom)
- [List Zoom Rooms](/docs/api/rest/reference/account/methods/#operation/dashboardZoomRooms)
- [Get top 25 issues of Zoom Rooms](/docs/api/rest/reference/account/methods/#operation/dashboardZoomRoomIssue)

## Device

### device:read:admin

Manage device

**Associated APIs:**

- [Get Zoom Phone Appliance settings by user ID](/docs/api/rest/reference/zoom-api/methods/#operation/GetZpaDeviceListProfileSettingOfaUser)
- [Get device detail](/docs/api/rest/reference/zoom-api/methods/#operation/getDevice)
- [Get ZPA version info](/docs/api/rest/reference/zoom-api/methods/#operation/GetZpaVersioninfo)
- [Get ZDM group info](/docs/api/rest/reference/zoom-api/methods/#operation/Getzdmgroupinfo)
- [List devices](/docs/api/rest/reference/zoom-api/methods/#operation/listDevices)

### device:write:admin

View and manage device

**Associated APIs:**

- [Get device detail](/docs/api/rest/reference/zoom-api/methods/#operation/getDevice)
- [Assign a device to a user or commonarea](/docs/api/rest/reference/zoom-api/methods/#operation/Assigndevicetoauser/commonarea)
- [List devices](/docs/api/rest/reference/zoom-api/methods/#operation/listDevices)
- [Delete device](/docs/api/rest/reference/zoom-api/methods/#operation/deleteDevice)
- [Add new device](/docs/api/rest/reference/zoom-api/methods/#operation/addDevice)
- [Assign a device to a group](/docs/api/rest/reference/zoom-api/methods/#operation/assginGroup)
- [Change device](/docs/api/rest/reference/zoom-api/methods/#operation/updateDevice)
- [Upgrade ZPA firmware or app](/docs/api/rest/reference/zoom-api/methods/#operation/UpgradeZpas/app)
- [Delete ZPA device by vendor and mac address](/docs/api/rest/reference/zoom-api/methods/#operation/DeleteZpaDeviceByVendorAndMacAddress)
- [Change device association](/docs/api/rest/reference/zoom-api/methods/#operation/changeDeviceAssociation)

## Devices (H323)

### h323:master

View and manage sub account's H.323 devices

**Associated APIs:**

- [Delete a H.323/SIP device](/docs/api/rest/reference/zoom-api/ma/#operation/deviceDelete)
- [Update a H.323/SIP device](/docs/api/rest/reference/zoom-api/ma/#operation/deviceUpdate)
- [List all H.323/SIP devices](/docs/api/rest/reference/zoom-api/ma/#operation/deviceList)
- [Create a H.323/SIP device](/docs/api/rest/reference/zoom-api/ma/#operation/deviceCreate)

### h323:read:admin

View all users' H.323 devices

**Associated APIs:**

- [List all H.323/SIP devices](/docs/api/rest/reference/zoom-api/methods/#operation/deviceList)

### h323:write:admin

View and manage all users' H.323 devices

**Associated APIs:**

- [Update a H.323/SIP device](/docs/api/rest/reference/zoom-api/methods/#operation/deviceUpdate)
- [Delete a H.323/SIP device](/docs/api/rest/reference/zoom-api/methods/#operation/deviceDelete)
- [Create a H.323/SIP device](/docs/api/rest/reference/zoom-api/methods/#operation/deviceCreate)

## Docs

### docs:delete

Delete a file

**Associated APIs:**

- [Delete a file](/docs/api/rest/reference/Docs/methods/#operation/DeleteFile)

### docs:delete:admin

Delete a file

**Associated APIs:**

- [Delete a file](/docs/api/rest/reference/Docs/methods/#operation/DeleteFile)

### docs:read:admin

Get basic info of the file

**Associated APIs:**

- [List all children of a file](/docs/api/rest/reference/Docs/methods/#operation/ListAllChildren)
- [Get metadata of a file](/docs/api/rest/reference/Docs/methods/#operation/QueryFileMetadata)

### docs:write:admin

Edit basic info of a file

**Associated APIs:**

- [Create a new file](/docs/api/rest/reference/Docs/methods/#operation/CreateDoc)
- [Modify metadata of a file](/docs/api/rest/reference/Docs/methods/#operation/ModifyMetadata)

### docs_file_uploads:write

Create a file upload

**Associated APIs:**

- [Create file upload for docs import or attachments](/docs/api/rest/reference/Docs/methods/#operation/Uploadfilefordocsimportorattachments)

### docs_file_uploads:write:admin

Create a file upload

**Associated APIs:**

- [Create file upload for docs import or attachments](/docs/api/rest/reference/Docs/methods/#operation/Uploadfilefordocsimportorattachments)

### docs_import:read

Get import task status

**Associated APIs:**

- [Get file import status](/docs/api/rest/reference/Docs/methods/#operation/Getdocsfileimportstatus)

### docs_import:read:admin

Get import task status

**Associated APIs:**

- [Get file import status](/docs/api/rest/reference/Docs/methods/#operation/Getdocsfileimportstatus)

### docs_import:write

Create new file by import

**Associated APIs:**

- [Create a new file by import](/docs/api/rest/reference/Docs/methods/#operation/Createanewfilebyimport)

### docs_import:write:admin

Create new file by import

**Associated APIs:**

- [Create a new file by import](/docs/api/rest/reference/Docs/methods/#operation/Createanewfilebyimport)

## Group

### group:master

View and manage sub account's groups

**Associated APIs:**

- [Get locked settings](/docs/api/rest/reference/user/ma/#operation/getGroupLockSettings)
- [Get a group's webinar registration settings](/docs/api/rest/reference/user/ma/#operation/groupSettingsRegistration)
- [Update a group's webinar registration settings](/docs/api/rest/reference/user/ma/#operation/groupSettingsRegistrationUpdate)
- [Update locked settings](/docs/api/rest/reference/user/ma/#operation/groupLockedSettings)
- [List group members](/docs/api/rest/reference/user/ma/#operation/groupMembers)
- [Upload Virtual Background files](/docs/api/rest/reference/user/ma/#operation/uploadGroupVB)
- [Delete a group admin](/docs/api/rest/reference/user/ma/#operation/groupAdminsDelete)
- [Get a group](/docs/api/rest/reference/user/ma/#operation/group)
- [Get a group's settings](/docs/api/rest/reference/user/ma/#operation/getGroupSettings)
- [List group channels](/docs/api/rest/reference/user/ma/#operation/groupChannels)
- [Update a group member](/docs/api/rest/reference/user/ma/#operation/updateAGroupMember)
- [List groups](/docs/api/rest/reference/user/ma/#operation/groups)
- [Create a group](/docs/api/rest/reference/user/ma/#operation/groupCreate)
- [List group admins](/docs/api/rest/reference/user/ma/#operation/groupAdmins)
- [Update a group's settings](/docs/api/rest/reference/user/ma/#operation/updateGroupSettings)
- [Add group members](/docs/api/rest/reference/user/ma/#operation/groupMembersCreate)
- [Delete Virtual Background files](/docs/api/rest/reference/user/ma/#operation/delGroupVB)
- [Add group admins](/docs/api/rest/reference/user/ma/#operation/groupAdminsCreate)
- [Delete a group member](/docs/api/rest/reference/user/ma/#operation/groupMembersDelete)
- [Delete a group](/docs/api/rest/reference/user/ma/#operation/groupDelete)
- [Update a group](/docs/api/rest/reference/user/ma/#operation/groupUpdate)

### group:read:admin

View groups

**Associated APIs:**

- [List group members](/docs/api/rest/reference/user/methods/#operation/groupMembers)
- [List groups](/docs/api/rest/reference/user/methods/#operation/groups)
- [List group admins](/docs/api/rest/reference/user/methods/#operation/groupAdmins)
- [Get a group's webinar registration settings](/docs/api/rest/reference/user/methods/#operation/groupSettingsRegistration)
- [List group channels](/docs/api/rest/reference/user/methods/#operation/groupChannels)
- [Get locked settings](/docs/api/rest/reference/user/methods/#operation/getGroupLockSettings)
- [Get a group's settings](/docs/api/rest/reference/user/methods/#operation/getGroupSettings)
- [Get a group](/docs/api/rest/reference/user/methods/#operation/group)

### group:write:admin

View and manage groups

**Associated APIs:**

- [Get a group](/docs/api/rest/reference/user/methods/#operation/group)
- [Update a group](/docs/api/rest/reference/user/methods/#operation/groupUpdate)
- [List group members](/docs/api/rest/reference/user/methods/#operation/groupMembers)
- [Update a group's webinar registration settings](/docs/api/rest/reference/user/methods/#operation/groupSettingsRegistrationUpdate)
- [Add group members](/docs/api/rest/reference/user/methods/#operation/groupMembersCreate)
- [Delete a group admin](/docs/api/rest/reference/user/methods/#operation/groupAdminsDelete)
- [Get locked settings](/docs/api/rest/reference/user/methods/#operation/getGroupLockSettings)
- [List group admins](/docs/api/rest/reference/user/methods/#operation/groupAdmins)
- [Create a group](/docs/api/rest/reference/user/methods/#operation/groupCreate)
- [Update a group's settings](/docs/api/rest/reference/user/methods/#operation/updateGroupSettings)
- [List groups](/docs/api/rest/reference/user/methods/#operation/groups)
- [Get a group's settings](/docs/api/rest/reference/user/methods/#operation/getGroupSettings)
- [Delete a group](/docs/api/rest/reference/user/methods/#operation/groupDelete)
- [Delete Virtual Background files](/docs/api/rest/reference/user/methods/#operation/delGroupVB)
- [Add group admins](/docs/api/rest/reference/user/methods/#operation/groupAdminsCreate)
- [Upload Virtual Background files](/docs/api/rest/reference/user/methods/#operation/uploadGroupVB)
- [Get a group's webinar registration settings](/docs/api/rest/reference/user/methods/#operation/groupSettingsRegistration)
- [Delete a group member](/docs/api/rest/reference/user/methods/#operation/groupMembersDelete)
- [List group channels](/docs/api/rest/reference/user/methods/#operation/groupChannels)
- [Update a group member](/docs/api/rest/reference/user/methods/#operation/updateAGroupMember)
- [Update locked settings](/docs/api/rest/reference/user/methods/#operation/groupLockedSettings)

## IM Group

### contact_group:read:admin

View all contact group information

**Associated APIs:**

- [List contact groups](/docs/api/rest/reference/user/methods/#operation/contactGroups)
- [List contact group members](/docs/api/rest/reference/user/methods/#operation/contactGroupMembers)

### contact_group:write:admin

Manage all contact group information

**Associated APIs:**

- [Add contact group members](/docs/api/rest/reference/user/methods/#operation/contactGroupMemberAdd)
- [Remove members in a contact group](/docs/api/rest/reference/user/methods/#operation/contactGroupMemberRemove)
- [Get a contact group](/docs/api/rest/reference/user/methods/#operation/contactGroup)
- [Update a contact group](/docs/api/rest/reference/user/methods/#operation/contactGroupUpdate)
- [Delete a contact group](/docs/api/rest/reference/user/methods/#operation/contactGroupDelete)
- [Create a contact group](/docs/api/rest/reference/user/methods/#operation/contactGroupCreate)

### imgroup:master

View and manage sub account's Zoom Team Chat Groups

**Associated APIs:**

- [Retrieve an IM directory group](/docs/api/rest/reference/chat/ma/#operation/imGroup)
- [List IM directory groups](/docs/api/rest/reference/chat/ma/#operation/imGroups)
- [Add IM directory group members](/docs/api/rest/reference/chat/ma/#operation/imGroupMembersCreate)
- [Delete an IM directory group](/docs/api/rest/reference/chat/ma/#operation/imGroupDelete)
- [Update an IM directory group](/docs/api/rest/reference/chat/ma/#operation/imGroupUpdate)
- [Delete IM directory group member](/docs/api/rest/reference/chat/ma/#operation/imGroupMembersDelete)
- [List IM directory group members](/docs/api/rest/reference/chat/ma/#operation/imGroupMembers)
- [Create an IM directory group](/docs/api/rest/reference/chat/ma/#operation/imGroupCreate)

### imgroup:read:admin

View Zoom Team Chat Group information

**Associated APIs:**

- [List IM directory group members](/docs/api/rest/reference/chat/methods/#operation/imGroupMembers)
- [List IM directory groups](/docs/api/rest/reference/chat/methods/#operation/imGroups)
- [Retrieve an IM directory group](/docs/api/rest/reference/chat/methods/#operation/imGroup)

### imgroup:write:admin

View and manage Zoom Team Chat Groups

**Associated APIs:**

- [Delete an IM directory group](/docs/api/rest/reference/chat/methods/#operation/imGroupDelete)
- [Create an IM directory group](/docs/api/rest/reference/chat/methods/#operation/imGroupCreate)
- [Update an IM directory group](/docs/api/rest/reference/chat/methods/#operation/imGroupUpdate)
- [List IM directory group members](/docs/api/rest/reference/chat/methods/#operation/imGroupMembers)
- [List IM directory groups](/docs/api/rest/reference/chat/methods/#operation/imGroups)
- [Retrieve an IM directory group](/docs/api/rest/reference/chat/methods/#operation/imGroup)
- [Add IM directory group members](/docs/api/rest/reference/chat/methods/#operation/imGroupMembersCreate)
- [Delete IM directory group member](/docs/api/rest/reference/chat/methods/#operation/imGroupMembersDelete)

## Integration Healthcare

### clinical_note:read:admin

Read Clinical Notes

### clinical_note:update:admin

Update Clinical Notes

## Mail

### mail:read

Read user’s own mailbox content.

**Associated APIs:**

- [Get the specified attachment for an email](/docs/api/rest/reference/zoom-mail/methods/#operation/get_email_attachment)
- [List labels in the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_labels_in_mailbox)
- [Get the specified email thread](/docs/api/rest/reference/zoom-mail/methods/#operation/get_email_thread)
- [Get the mailbox profile](/docs/api/rest/reference/zoom-mail/methods/#operation/get_mailbox_profile)
- [List email threads from the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_email_threads)
- [Get the specified draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/get_draft_email)
- [List delegates on the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_mailbox_delegates)
- [Get the specified email](/docs/api/rest/reference/zoom-mail/methods/#operation/get_email)
- [List history of events for mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_mailbox_history)
- [List email filters](/docs/api/rest/reference/zoom-mail/methods/#operation/list_email_filters)
- [Get the specified email filter](/docs/api/rest/reference/zoom-mail/methods/#operation/get_email_filter)
- [Get the specified delegate on the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/get_mailbox_delegate)
- [Get mailbox vacation response setting](/docs/api/rest/reference/zoom-mail/methods/#operation/get_mail_vacation_response_setting)
- [List emails from draft folder](/docs/api/rest/reference/zoom-mail/methods/#operation/list_draft_emails)
- [Get the specified label in mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/get_label_in_mailbox)
- [List emails from the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_emails)

### mail:read:admin

Read all mailboxes' content under the account, and account level settings.

**Associated APIs:**

- [Get the mailbox profile](/docs/api/rest/reference/zoom-mail/methods/#operation/get_mailbox_profile)
- [Get the specified attachment for an email](/docs/api/rest/reference/zoom-mail/methods/#operation/get_email_attachment)
- [Get the specified email filter](/docs/api/rest/reference/zoom-mail/methods/#operation/get_email_filter)
- [Get the specified email](/docs/api/rest/reference/zoom-mail/methods/#operation/get_email)
- [Get the specified draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/get_draft_email)
- [Get mailbox vacation response setting](/docs/api/rest/reference/zoom-mail/methods/#operation/get_mail_vacation_response_setting)
- [Get the specified label in mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/get_label_in_mailbox)
- [List emails from draft folder](/docs/api/rest/reference/zoom-mail/methods/#operation/list_draft_emails)
- [Get the specified delegate on the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/get_mailbox_delegate)
- [List emails from the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_emails)
- [List labels in the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_labels_in_mailbox)
- [Get the specified email thread](/docs/api/rest/reference/zoom-mail/methods/#operation/get_email_thread)
- [List history of events for mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_mailbox_history)
- [List email filters](/docs/api/rest/reference/zoom-mail/methods/#operation/list_email_filters)
- [List email threads from the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_email_threads)
- [List delegates on the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/list_mailbox_delegates)

### mail:write

Read and write user’s own mailbox content.

**Associated APIs:**

- [Delete an existing email thread](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_email_thread)
- [Create a new draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/create_draft_email)
- [Create a new email](/docs/api/rest/reference/zoom-mail/methods/#operation/create_email)
- [Delete an existing label from mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_label_from_mailbox)
- [Grant a new delegate access on the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/grant_mailbox_delegate)
- [Send out a draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/send_draft_email)
- [Update mailbox vacation response setting](/docs/api/rest/reference/zoom-mail/methods/#operation/update_mailbox_vacation_response_setting)
- [Batch modify the specified emails](/docs/api/rest/reference/zoom-mail/methods/#operation/batch_modify_emails)
- [Delete an existing draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_draft_email)
- [Revoke an existing delegate access from the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/revoke_mailbox_delegate)
- [Update the specified draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/update_draft_email)
- [Create a new label in mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/create_label_in_mailbox)
- [Patch the specified label in mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/patch_label_in_mailbox)
- [Send out an email](/docs/api/rest/reference/zoom-mail/methods/#operation/send_email)
- [Move the specified thread out of TRASH folder](/docs/api/rest/reference/zoom-mail/methods/#operation/untrash_email_thread)
- [Delete an existing email](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_email)
- [Move the specified thread to TRASH folder](/docs/api/rest/reference/zoom-mail/methods/#operation/trash_email_thread)
- [Update the specified label in mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/update_label_in_mailbox)
- [Update the specified email](/docs/api/rest/reference/zoom-mail/methods/#operation/update_email)
- [Update the specified thread](/docs/api/rest/reference/zoom-mail/methods/#operation/update_email_thread)
- [Batch delete the specified emails](/docs/api/rest/reference/zoom-mail/methods/#operation/batch_delete_emails)
- [Move the specified email to TRASH folder](/docs/api/rest/reference/zoom-mail/methods/#operation/trash_email)
- [Move the specified email out of TRASH folder](/docs/api/rest/reference/zoom-mail/methods/#operation/untrash_email)
- [Create an email filter](/docs/api/rest/reference/zoom-mail/methods/#operation/create_email_filter)
- [Delete the specified email filter](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_email_filter)

### mail:write:admin

Read and write all mailboxes' content under the account, and account level settings.

**Associated APIs:**

- [Update mailbox vacation response setting](/docs/api/rest/reference/zoom-mail/methods/#operation/update_mailbox_vacation_response_setting)
- [Delete an existing label from mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_label_from_mailbox)
- [Move the specified thread to TRASH folder](/docs/api/rest/reference/zoom-mail/methods/#operation/trash_email_thread)
- [Update the specified thread](/docs/api/rest/reference/zoom-mail/methods/#operation/update_email_thread)
- [Revoke an existing delegate access from the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/revoke_mailbox_delegate)
- [Move the specified email out of TRASH folder](/docs/api/rest/reference/zoom-mail/methods/#operation/untrash_email)
- [Delete an existing email thread](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_email_thread)
- [Batch modify the specified emails](/docs/api/rest/reference/zoom-mail/methods/#operation/batch_modify_emails)
- [Create a new draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/create_draft_email)
- [Update the specified draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/update_draft_email)
- [Patch the specified label in mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/patch_label_in_mailbox)
- [Move the specified email to TRASH folder](/docs/api/rest/reference/zoom-mail/methods/#operation/trash_email)
- [Update the specified label in mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/update_label_in_mailbox)
- [Delete an existing draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_draft_email)
- [Send out a draft email](/docs/api/rest/reference/zoom-mail/methods/#operation/send_draft_email)
- [Update the specified email](/docs/api/rest/reference/zoom-mail/methods/#operation/update_email)
- [Send out an email](/docs/api/rest/reference/zoom-mail/methods/#operation/send_email)
- [Create a new email](/docs/api/rest/reference/zoom-mail/methods/#operation/create_email)
- [Create an email filter](/docs/api/rest/reference/zoom-mail/methods/#operation/create_email_filter)
- [Move the specified thread out of TRASH folder](/docs/api/rest/reference/zoom-mail/methods/#operation/untrash_email_thread)
- [Delete an existing email](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_email)
- [Delete the specified email filter](/docs/api/rest/reference/zoom-mail/methods/#operation/delete_email_filter)
- [Create a new label in mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/create_label_in_mailbox)
- [Grant a new delegate access on the mailbox](/docs/api/rest/reference/zoom-mail/methods/#operation/grant_mailbox_delegate)
- [Batch delete the specified emails](/docs/api/rest/reference/zoom-mail/methods/#operation/batch_delete_emails)

## Marketplace

### marketplace_app:master

View and manage sub accounts' marketplace app info

**Associated APIs:**

- [Create apps](/docs/api/rest/reference/marketplace/ma/#operation/CreateApps)

### marketplace_app:read

View your marketplace app information

**Associated APIs:**

- [Get information about an app](/docs/api/rest/reference/marketplace/methods/#operation/getAppInfo)
- [Get a user's app requests](/docs/api/rest/reference/marketplace/methods/#operation/getUserAppRequests)
- [Validate an app manifest](/docs/api/rest/reference/marketplace/methods/#operation/validatingManifest)
- [Export an app manifest from an existing app](/docs/api/rest/reference/marketplace/methods/#operation/getAppManifest)
- [Get webhook logs](/docs/api/rest/reference/marketplace/methods/#operation/getWebhookLogs)

### marketplace_app:read:admin

View marketplace app information for the account

**Associated APIs:**

- [Export an app manifest from an existing app](/docs/api/rest/reference/marketplace/methods/#operation/getAppManifest)
- [Get a user's app requests](/docs/api/rest/reference/marketplace/methods/#operation/getUserAppRequests)
- [Get an app's user requests](/docs/api/rest/reference/marketplace/methods/#operation/getAppUserRequests)
- [Get webhook logs](/docs/api/rest/reference/marketplace/methods/#operation/getWebhookLogs)
- [Validate an app manifest](/docs/api/rest/reference/marketplace/methods/#operation/validatingManifest)
- [Get information about an app](/docs/api/rest/reference/marketplace/methods/#operation/getAppInfo)
- [List apps](/docs/api/rest/reference/marketplace/methods/#operation/ListApps)

### marketplace_app:write

Edit marketplace app

**Associated APIs:**

- [Deletes an app](/docs/api/rest/reference/marketplace/methods/#operation/deleteApp)
- [Create apps](/docs/api/rest/reference/marketplace/methods/#operation/CreateApps)
- [Update an app by manifest](/docs/api/rest/reference/marketplace/methods/#operation/updateAppByManifest)

### marketplace_app:write:admin

View and Manage marketplace app information for the account

**Associated APIs:**

- [Enable or disable user app subscription](/docs/api/rest/reference/marketplace/methods/#operation/Enable/Disableuserappsubscription)
- [Update app pre approval setting](/docs/api/rest/reference/marketplace/methods/#operation/Updateapppreapprovalsetting)
- [Add app allow requests for users](/docs/api/rest/reference/marketplace/methods/#operation/AddAppAllowRequestsForUsers)
- [Generate Zoom App Deeplink](/docs/api/rest/reference/marketplace/methods/#operation/GenerateZoomAppDeeplink)
- [Update an app by manifest](/docs/api/rest/reference/marketplace/methods/#operation/updateAppByManifest)
- [Create apps](/docs/api/rest/reference/marketplace/methods/#operation/CreateApps)
- [Update app's request status](/docs/api/rest/reference/marketplace/methods/#operation/updateAppRequestStatus)
- [Deletes an app](/docs/api/rest/reference/marketplace/methods/#operation/deleteApp)

### marketplace_custom_fields:read

Read custom field values

**Associated APIs:**

- [Get user's custom field values](/docs/api/rest/reference/marketplace/methods/#operation/getCustomFieldValues)

### marketplace_custom_fields:read:admin

Read custom field values

**Associated APIs:**

- [Get user's custom field values](/docs/api/rest/reference/marketplace/methods/#operation/getCustomFieldValues)

### marketplace_entitlement:read

View entitlements

**Associated APIs:**

- [Get app user entitlements](/docs/api/rest/reference/marketplace/methods/#operation/getAppUserEntitlementRequests)
- [Get a user's entitlements](/docs/api/rest/reference/marketplace/methods/#operation/getUserEntitlementRequests)

### marketplace_entitlement:read:admin

View entitlements

**Associated APIs:**

- [Get app user entitlements](/docs/api/rest/reference/marketplace/methods/#operation/getAppUserEntitlementRequests)
- [Get a user's entitlements](/docs/api/rest/reference/marketplace/methods/#operation/getUserEntitlementRequests)

## Meeting

### information_barriers:read:admin

View information barriers

**Associated APIs:**

- [List information Barrier policies](/docs/api/rest/reference/account/methods/#operation/InformationBarriersList)
- [Get an Information Barrier policy by ID](/docs/api/rest/reference/account/methods/#operation/InformationBarriersGet)

### information_barriers:read:master

View information barriers

**Associated APIs:**

- [Get an Information Barrier policy by ID](/docs/api/rest/reference/account/ma/#operation/InformationBarriersGet)
- [List information Barrier policies](/docs/api/rest/reference/account/ma/#operation/InformationBarriersList)

### information_barriers:write:admin

View and manage information barriers

**Associated APIs:**

- [Remove an Information Barrier policy](/docs/api/rest/reference/account/methods/#operation/InformationBarriersDelete)
- [Create an Information Barrier policy](/docs/api/rest/reference/account/methods/#operation/InformationBarriersCreate)
- [Update an Information Barriers policy](/docs/api/rest/reference/account/methods/#operation/InformationBarriersUpdate)

### information_barriers:write:master

View and manage information barriers

**Associated APIs:**

- [Remove an Information Barrier policy](/docs/api/rest/reference/account/ma/#operation/InformationBarriersDelete)
- [Create an Information Barrier policy](/docs/api/rest/reference/account/ma/#operation/InformationBarriersCreate)
- [Update an Information Barriers policy](/docs/api/rest/reference/account/ma/#operation/InformationBarriersUpdate)

### meeting:master

View and manage sub account's user meetings

**Associated APIs:**

- [List meeting registrants](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRegistrants)
- [List meeting templates](/docs/api/rest/reference/zoom-api/ma/#operation/listMeetingTemplates)
- [Update livestream status](/docs/api/rest/reference/zoom-api/ma/#operation/meetingLiveStreamStatusUpdate)
- [List registration questions](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRegistrantsQuestionsGet)
- [Add a meeting registrant](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRegistrantCreate)
- [Create a meeting template from an existing meeting](/docs/api/rest/reference/zoom-api/ma/#operation/meetingTemplateCreate)
- [List past meeting instances](/docs/api/rest/reference/zoom-api/ma/#operation/pastMeetings)
- [List meetings](/docs/api/rest/reference/zoom-api/ma/#operation/meetings)
- [Use in-meeting controls](/docs/api/rest/reference/zoom-api/ma/#operation/inMeetingControl)
- [Create a meeting](/docs/api/rest/reference/zoom-api/ma/#operation/meetingCreate)
- [Get a meeting survey](/docs/api/rest/reference/zoom-api/ma/#operation/meetingSurveyGet)
- [Update a meeting](/docs/api/rest/reference/zoom-api/ma/#operation/meetingUpdate)
- [Update a meeting survey](/docs/api/rest/reference/zoom-api/ma/#operation/meetingSurveyUpdate)
- [Delete a meeting registrant](/docs/api/rest/reference/zoom-api/ma/#operation/meetingregistrantdelete)
- [List meeting polls](/docs/api/rest/reference/zoom-api/ma/#operation/meetingPolls)
- [Create a meeting's invite links](/docs/api/rest/reference/zoom-api/ma/#operation/meetingInviteLinksCreate)
- [Get livestream details](/docs/api/rest/reference/zoom-api/ma/#operation/getMeetingLiveStreamDetails)
- [Update registration questions](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRegistrantQuestionUpdate)
- [Get a meeting registrant](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRegistrantGet)
- [Update registrant's status](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRegistrantStatus)
- [Get meeting invitation](/docs/api/rest/reference/zoom-api/ma/#operation/meetingInvitation)
- [Perform batch registration](/docs/api/rest/reference/zoom-api/ma/#operation/addBatchRegistrants)
- [Update a meeting poll](/docs/api/rest/reference/zoom-api/ma/#operation/meetingPollUpdate)
- [Get a meeting](/docs/api/rest/reference/zoom-api/ma/#operation/meeting)
- [Get a meeting poll](/docs/api/rest/reference/zoom-api/ma/#operation/meetingPollGet)
- [Delete a meeting survey](/docs/api/rest/reference/zoom-api/ma/#operation/meetingSurveyDelete)
- [Delete a meeting poll](/docs/api/rest/reference/zoom-api/ma/#operation/meetingPollDelete)
- [Delete a meeting](/docs/api/rest/reference/zoom-api/ma/#operation/meetingDelete)
- [Update meeting status](/docs/api/rest/reference/zoom-api/ma/#operation/meetingStatus)
- [Update a livestream](/docs/api/rest/reference/zoom-api/ma/#operation/meetingLiveStreamUpdate)
- [Get meeting's token](/docs/api/rest/reference/zoom-api/ma/#operation/meetingToken)
- [Create a meeting poll](/docs/api/rest/reference/zoom-api/ma/#operation/meetingPollCreate)
- [Perform batch poll creation](/docs/api/rest/reference/zoom-api/ma/#operation/createBatchPolls)

### meeting:read

View your meetings

**Associated APIs:**

- [Get livestream details](/docs/api/rest/reference/zoom-api/methods/#operation/getMeetingLiveStreamDetails)
- [List past meeting instances](/docs/api/rest/reference/zoom-api/methods/#operation/pastMeetings)
- [Get a meeting survey](/docs/api/rest/reference/zoom-api/methods/#operation/meetingSurveyGet)
- [Get a meeting registrant](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantGet)
- [List meetings](/docs/api/rest/reference/zoom-api/methods/#operation/meetings)
- [Get a meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meeting)
- [List past meeting's poll results](/docs/api/rest/reference/zoom-api/methods/#operation/listPastMeetingPolls)
- [Get past meeting details](/docs/api/rest/reference/zoom-api/methods/#operation/pastMeetingDetails)
- [List past meetings' Q&A](/docs/api/rest/reference/zoom-api/methods/#operation/listPastMeetingQA)
- [List meeting templates](/docs/api/rest/reference/zoom-api/methods/#operation/listMeetingTemplates)
- [Get past meeting participants](/docs/api/rest/reference/zoom-api/methods/#operation/pastMeetingParticipants)
- [List registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantsQuestionsGet)
- [Get meeting invitation](/docs/api/rest/reference/zoom-api/methods/#operation/meetingInvitation)
- [List meeting registrants](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrants)
- [Get a meeting poll](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollGet)
- [List meeting polls](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPolls)
- [List upcoming meetings](/docs/api/rest/reference/zoom-api/methods/#operation/listUpcomingMeeting)
- [Get meeting's token](/docs/api/rest/reference/zoom-api/methods/#operation/meetingToken)

### meeting:read:admin

View all user meetings

**Associated APIs:**

- [Get livestream details](/docs/api/rest/reference/zoom-api/methods/#operation/getMeetingLiveStreamDetails)
- [List past meeting's poll results](/docs/api/rest/reference/zoom-api/methods/#operation/listPastMeetingPolls)
- [List meeting polls](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPolls)
- [Get a meeting survey](/docs/api/rest/reference/zoom-api/methods/#operation/meetingSurveyGet)
- [List past meetings' Q&A](/docs/api/rest/reference/zoom-api/methods/#operation/listPastMeetingQA)
- [List past meeting instances](/docs/api/rest/reference/zoom-api/methods/#operation/pastMeetings)
- [Get past meeting participants](/docs/api/rest/reference/zoom-api/methods/#operation/pastMeetingParticipants)
- [List meetings](/docs/api/rest/reference/zoom-api/methods/#operation/meetings)
- [Get a meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meeting)
- [Get past meeting details](/docs/api/rest/reference/zoom-api/methods/#operation/pastMeetingDetails)
- [List meeting templates](/docs/api/rest/reference/zoom-api/methods/#operation/listMeetingTemplates)
- [List meeting registrants](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrants)
- [List upcoming meetings](/docs/api/rest/reference/zoom-api/methods/#operation/listUpcomingMeeting)
- [List registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantsQuestionsGet)
- [Get meeting's token](/docs/api/rest/reference/zoom-api/methods/#operation/meetingToken)
- [Get meeting invitation](/docs/api/rest/reference/zoom-api/methods/#operation/meetingInvitation)
- [Get a meeting registrant](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantGet)
- [Get a meeting poll](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollGet)

### meeting:write

View and manage your meetings

**Associated APIs:**

- [Update registrant's status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantStatus)
- [Add a meeting app](/docs/api/rest/reference/zoom-api/methods/#operation/meetingAppAdd)
- [Update livestream status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLiveStreamStatusUpdate)
- [Add a meeting registrant](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantCreate)
- [Delete a meeting poll](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollDelete)
- [Update a meeting poll](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollUpdate)
- [Delete a meeting survey](/docs/api/rest/reference/zoom-api/methods/#operation/meetingSurveyDelete)
- [Delete a meeting registrant](/docs/api/rest/reference/zoom-api/methods/#operation/meetingregistrantdelete)
- [Delete a live meeting message](/docs/api/rest/reference/zoom-api/methods/#operation/deleteMeetingChatMessageById)
- [Update registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantQuestionUpdate)
- [Create a meeting poll](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollCreate)
- [Perform batch poll creation](/docs/api/rest/reference/zoom-api/methods/#operation/createBatchPolls)
- [Perform batch registration](/docs/api/rest/reference/zoom-api/methods/#operation/addBatchRegistrants)
- [Create a meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meetingCreate)
- [Delete a meeting app](/docs/api/rest/reference/zoom-api/methods/#operation/meetingAppDelete)
- [Update a meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meetingUpdate)
- [Create a meeting's invite links](/docs/api/rest/reference/zoom-api/methods/#operation/meetingInviteLinksCreate)
- [Update a livestream](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLiveStreamUpdate)
- [Update a meeting survey](/docs/api/rest/reference/zoom-api/methods/#operation/meetingSurveyUpdate)
- [Update meeting status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingStatus)
- [Delete a meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meetingDelete)
- [Create a meeting template from an existing meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meetingTemplateCreate)
- [Use in-meeting controls](/docs/api/rest/reference/zoom-api/methods/#operation/inMeetingControl)
- [Update participant Real-Time Media Streams (RTMS) app status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRTMSStatusUpdate)
- [Update a live meeting message](/docs/api/rest/reference/zoom-api/methods/#operation/updateMeetingChatMessageById)

### meeting:write:admin

View and manage all user meetings

**Associated APIs:**

- [Update a livestream](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLiveStreamUpdate)
- [Perform batch registration](/docs/api/rest/reference/zoom-api/methods/#operation/addBatchRegistrants)
- [Create a meeting template from an existing meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meetingTemplateCreate)
- [Delete a meeting app](/docs/api/rest/reference/zoom-api/methods/#operation/meetingAppDelete)
- [Create a meeting's invite links](/docs/api/rest/reference/zoom-api/methods/#operation/meetingInviteLinksCreate)
- [Update a meeting survey](/docs/api/rest/reference/zoom-api/methods/#operation/meetingSurveyUpdate)
- [Update meeting status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingStatus)
- [Delete a live meeting message](/docs/api/rest/reference/zoom-api/methods/#operation/deleteMeetingChatMessageById)
- [Update a live meeting message](/docs/api/rest/reference/zoom-api/methods/#operation/updateMeetingChatMessageById)
- [Use in-meeting controls](/docs/api/rest/reference/zoom-api/methods/#operation/inMeetingControl)
- [Update participant Real-Time Media Streams (RTMS) app status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRTMSStatusUpdate)
- [Delete a meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meetingDelete)
- [Create a meeting poll](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollCreate)
- [Delete a meeting survey](/docs/api/rest/reference/zoom-api/methods/#operation/meetingSurveyDelete)
- [Add a meeting app](/docs/api/rest/reference/zoom-api/methods/#operation/meetingAppAdd)
- [Update livestream status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLiveStreamStatusUpdate)
- [Add a meeting registrant](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantCreate)
- [Delete a meeting registrant](/docs/api/rest/reference/zoom-api/methods/#operation/meetingregistrantdelete)
- [Delete a meeting poll](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollDelete)
- [Perform batch poll creation](/docs/api/rest/reference/zoom-api/methods/#operation/createBatchPolls)
- [Create a meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meetingCreate)
- [Update a meeting](/docs/api/rest/reference/zoom-api/methods/#operation/meetingUpdate)
- [Update registrant's status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantStatus)
- [Update a meeting poll](/docs/api/rest/reference/zoom-api/methods/#operation/meetingPollUpdate)
- [Update registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRegistrantQuestionUpdate)

### meeting:write:admin:sip_dialing

Get CRC dial string with passcode

**Associated APIs:**

- [Get a meeting SIP URI with passcode](/docs/api/rest/reference/zoom-api/methods/#operation/getSipDialingWithPasscode)

### meeting:write:sip_dialing

Get CRC dial string with passcode

**Associated APIs:**

- [Get a meeting SIP URI with passcode](/docs/api/rest/reference/zoom-api/methods/#operation/getSipDialingWithPasscode)

### meeting_summary:master

View and manage sub account's user meeting summaries

**Associated APIs:**

- [Get a meeting or webinar summary](/docs/api/rest/reference/zoom-api/ma/#operation/Getameetingsummary)
- [List an account's meeting or webinar summaries](/docs/api/rest/reference/zoom-api/ma/#operation/Listmeetingsummaries)
- [Delete a meeting or webinar summary](/docs/api/rest/reference/zoom-api/ma/#operation/Deletemeetingorwebinarsummary)

### meeting_summary:read

View your meeting summaries

**Associated APIs:**

- [Get a meeting or webinar summary](/docs/api/rest/reference/zoom-api/methods/#operation/Getameetingsummary)

### meeting_summary:read:admin

View all user meeting summaries

**Associated APIs:**

- [List an account's meeting or webinar summaries](/docs/api/rest/reference/zoom-api/methods/#operation/Listmeetingsummaries)
- [Get a meeting or webinar summary](/docs/api/rest/reference/zoom-api/methods/#operation/Getameetingsummary)

### meeting_token:read:admin:live_streaming

View live streaming meeting token information

**Associated APIs:**

- [Get a meeting's join token for live streaming](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLiveStreamingJoinToken)

### meeting_token:read:admin:local_archiving

View local archiving meeting token information

**Associated APIs:**

- [Get a meeting's archive token for local archiving](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLocalArchivingArchiveToken)

### meeting_token:read:admin:local_recording

This scope allows an app to view an account's users' local recording meeting token information

**Associated APIs:**

- [Get a meeting's join token for local recording](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLocalRecordingJoinToken)

### meeting_token:read:live_streaming

View live streaming meeting token information

**Associated APIs:**

- [Get a meeting's join token for live streaming](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLiveStreamingJoinToken)

### meeting_token:read:local_recording

This scope allows an app to view a user's local recording meeting token information

**Associated APIs:**

- [Get a meeting's join token for local recording](/docs/api/rest/reference/zoom-api/methods/#operation/meetingLocalRecordingJoinToken)

## NumberManagement

### number_management_numbers:read:admin

View all phone number detail in "Number Management".

### number_management_numbers:read:master

View and manage sub account's phone number detail in "Number Management".

### number_management_numbers:write:admin

Manage phone number detail in "Number Management".

### number_management_numbers:write:master

Manage sub account's phone number detail in "Number Management".

## PAC

### pac:master

**Associated APIs:**

- [List a user's PAC accounts](/docs/api/rest/reference/zoom-api/ma/#operation/userPACs)

### pac:read

View your audio conference info

**Associated APIs:**

- [List a user's PAC accounts](/docs/api/rest/reference/zoom-api/methods/#operation/userPACs)

### pac:read:admin

View all users' audio conference info

**Associated APIs:**

- [List a user's PAC accounts](/docs/api/rest/reference/zoom-api/methods/#operation/userPACs)

## Phone

### phone:master

View and manage all sub accounts' Zoom Phone information

**Associated APIs:**

- [Delete an extension's inbound block rule](/docs/api/rest/reference/phone/ma/#operation/DeleteExtensiontLevelInboundBlockRules)
- [Delete users from a directory](/docs/api/rest/reference/phone/ma/#operation/DeleteUsersFromDirectory)
- [Get device details](/docs/api/rest/reference/phone/ma/#operation/getADevice)
- [Get a list of monitoring groups on an account](/docs/api/rest/reference/phone/ma/#operation/listMonitoringGroup)
- [Upload fax file](/docs/api/rest/reference/phone/ma/#operation/UploadFaxFiles)
- [Update a user's profile](/docs/api/rest/reference/phone/ma/#operation/updateUserProfile)
- [Unassign a member](/docs/api/rest/reference/phone/ma/#operation/unassignMemberFromCallQueue)
- [Add audio items](/docs/api/rest/reference/phone/ma/#operation/AddAudioItem)
- [Update user policy](/docs/api/rest/reference/phone/ma/#operation/updateUserPolicy)
- [Add a Zoom Room to a Zoom Phone](/docs/api/rest/reference/phone/ma/#operation/addZoomRoom)
- [Update user level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/UpdateUserOutboundCallingExceptionRule)
- [Update an emergency address](/docs/api/rest/reference/phone/ma/#operation/updateEmergencyAddress)
- [Get call log details](/docs/api/rest/reference/phone/ma/#operation/getCallLogDetails)
- [Update an SLG policy setting](/docs/api/rest/reference/phone/ma/#operation/updateSLGPolicySubSetting)
- [List call logs](/docs/api/rest/reference/phone/ma/#operation/listCallLogsMetrics)
- [Get an auto receptionist](/docs/api/rest/reference/phone/ma/#operation/getAutoReceptionistDetail)
- [Delete a blocked list](/docs/api/rest/reference/phone/ma/#operation/deleteABlockedList)
- [List auto receptionists](/docs/api/rest/reference/phone/ma/#operation/listAutoReceptionists)
- [Assign a phone number to a user](/docs/api/rest/reference/phone/ma/#operation/assignPhoneNumber)
- [Download a phone recording transcript](/docs/api/rest/reference/phone/ma/#operation/phoneDownloadRecordingTranscript)
- [Add a policy subsetting to a call queue](/docs/api/rest/reference/phone/ma/#operation/addCQPolicySubSetting)
- [Update account level outbound calling countries or regions](/docs/api/rest/reference/phone/ma/#operation/UpdateAccountOutboundCallingCountriesOrRegions)
- [Add a client code to a call history](/docs/api/rest/reference/phone/ma/#operation/addClientCodeToCallHistory)
- [Assign phone numbers to a common area](/docs/api/rest/reference/phone/ma/#operation/assignPhoneNumbersToCommonArea)
- [Unassign a calling plan from the common area](/docs/api/rest/reference/phone/ma/#operation/unassignCallingPlansFromCommonArea)
- [Get blocked list details](/docs/api/rest/reference/phone/ma/#operation/getABlockedList)
- [Remove a member from a private directory](/docs/api/rest/reference/phone/ma/#operation/removeAMemberFromAPrivateDirectory)
- [Add phone numbers for users' customized outbound caller ID](/docs/api/rest/reference/phone/ma/#operation/addUserOutboundCallerNumbers)
- [Delete a call queue](/docs/api/rest/reference/phone/ma/#operation/deleteACallQueue)
- [List real time location for IP phones](/docs/api/rest/reference/phone/ma/#operation/listPhoneRealtimelocation)
- [Delete a shared line group](/docs/api/rest/reference/phone/ma/#operation/deleteASharedLineGroup)
- [Create a call queue](/docs/api/rest/reference/phone/ma/#operation/createCallQueue)
- [List opt statuses of phone numbers assigned to SMS campaign](/docs/api/rest/reference/phone/ma/#operation/getNumberCampaignOptStatus)
- [Update the group call pickup information](/docs/api/rest/reference/phone/ma/#operation/updateGCP)
- [Add members to roles](/docs/api/rest/reference/phone/ma/#operation/AddRoleMembers)
- [Get common area settings](/docs/api/rest/reference/phone/ma/#operation/getCommonAreaSettings)
- [Sync user's call history](/docs/api/rest/reference/phone/ma/#operation/syncUserCallHistory)
- [List setting templates](/docs/api/rest/reference/phone/ma/#operation/listSettingTemplates)
- [Get call QoS](/docs/api/rest/reference/phone/ma/#operation/getCallQoS)
- [List customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/ma/#operation/listSiteCustomizeOutboundCallerNumbers)
- [List users' phone numbers for a customized outbound caller ID](/docs/api/rest/reference/phone/ma/#operation/listUserCustomizeOutboundCallerNumbers)
- [Get user voicemail details from a call log](/docs/api/rest/reference/phone/ma/#operation/getVoicemailDetailsByCallIdOrCallLogId)
- [Get group policy details](/docs/api/rest/reference/phone/ma/#operation/GetGroupPolicyDetails)
- [Delete an audio item](/docs/api/rest/reference/phone/ma/#operation/DeleteAudioItem)
- [Get user level outbound calling countries and regions](/docs/api/rest/reference/phone/ma/#operation/GetUserOutboundCallingCountriesAndRegions)
- [Update an alert setting](/docs/api/rest/reference/phone/ma/#operation/UpdateAnAlertSetting)
- [Delete a device](/docs/api/rest/reference/phone/ma/#operation/deleteADevice)
- [Create a blocked list](/docs/api/rest/reference/phone/ma/#operation/addAnumberToBlockedList)
- [Assign an entity to a device](/docs/api/rest/reference/phone/ma/#operation/addExtensionsToADevice)
- [Update Recording Status](/docs/api/rest/reference/phone/ma/#operation/UpdateRecordingStatus)
- [Update a user's shared access setting](/docs/api/rest/reference/phone/ma/#operation/updateUserSetting)
- [Remove a Zoom Room from a ZP account](/docs/api/rest/reference/phone/ma/#operation/RemoveZoomRoom)
- [Get account's call logs](/docs/api/rest/reference/phone/ma/#operation/accountCallLogs)
- [Delete an account's inbound blocked statistics](/docs/api/rest/reference/phone/ma/#operation/DeleteAccountLevelInboundBlockedStatistics)
- [Get fax charges usage report](/docs/api/rest/reference/phone/ma/#operation/Getfaxchargesusagereport)
- [List phone users](/docs/api/rest/reference/phone/ma/#operation/listPhoneUsers)
- [Update Voicemail Read Status](/docs/api/rest/reference/phone/ma/#operation/updateVoicemailReadStatus)
- [Update a shared line group policy](/docs/api/rest/reference/phone/ma/#operation/updateSharedLineGroupPolicy)
- [Update a provision template](/docs/api/rest/reference/phone/ma/#operation/updateProvisionTemplate)
- [Delete common area level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/deleteCommonAreaOutboundCallingExceptionRule)
- [Delete directory backup routing rule](/docs/api/rest/reference/phone/ma/#operation/deleteRoutingRule)
- [Assign numbers to a call queue](/docs/api/rest/reference/phone/ma/#operation/assignPhoneToCallQueue)
- [List call queues](/docs/api/rest/reference/phone/ma/#operation/listCallQueues)
- [Add a site setting](/docs/api/rest/reference/phone/ma/#operation/addSiteSetting)
- [Add a setting template](/docs/api/rest/reference/phone/ma/#operation/addSettingTemplate)
- [Get emergency address details](/docs/api/rest/reference/phone/ma/#operation/getEmergencyAddress)
- [List audio items](/docs/api/rest/reference/phone/ma/#operation/ListAudioItems)
- [Update an audio item](/docs/api/rest/reference/phone/ma/#operation/UpdateAudioItem)
- [Get call queue recordings](/docs/api/rest/reference/phone/ma/#operation/getCallQueueRecordings)
- [List Zoom Rooms without Zoom Phone assignment](/docs/api/rest/reference/phone/ma/#operation/listUnassignedZoomRooms)
- [Add peering phone numbers](/docs/api/rest/reference/phone/ma/#operation/addPeeringPhoneNumbers)
- [Apply template to common areas](/docs/api/rest/reference/phone/ma/#operation/ApplyTemplatetoCommonAreas)
- [Update phone account settings](/docs/api/rest/reference/phone/ma/#operation/updatePhoneSettings)
- [Generate activation codes for common areas](/docs/api/rest/reference/phone/ma/#operation/Generateactivationcodesforcommonareas)
- [Update a shared line group](/docs/api/rest/reference/phone/ma/#operation/updateASharedLineGroup)
- [Delete an emergency location](/docs/api/rest/reference/phone/ma/#operation/deleteLocation)
- [List an extension's inbound block rules](/docs/api/rest/reference/phone/ma/#operation/ListExtensionLevelInboundBlockRules)
- [Remove a calling plan from a Zoom Room](/docs/api/rest/reference/phone/ma/#operation/unassignCallingPlanFromRoom)
- [Get phone account settings](/docs/api/rest/reference/phone/ma/#operation/phoneSetting)
- [List plan information](/docs/api/rest/reference/phone/ma/#operation/listPhonePlans)
- [Remove members from call pickup group](/docs/api/rest/reference/phone/ma/#operation/removeGCPMembers)
- [Update common area level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/UpdateCommonAreaOutboundCallingExceptionRule)
- [Get a phone number](/docs/api/rest/reference/phone/ma/#operation/getPhoneNumberDetails)
- [Add BYOC phone numbers](/docs/api/rest/reference/phone/ma/#operation/addBYOCNumber)
- [Update account policy](/docs/api/rest/reference/phone/ma/#operation/updateAccountPolicy)
- [Update Auto Delete Field](/docs/api/rest/reference/phone/ma/#operation/UpdateAutoDeleteField)
- [List nomadic emergency services users](/docs/api/rest/reference/phone/ma/#operation/listUserNomadicEmergencyServices)
- [Get alert setting details](/docs/api/rest/reference/phone/ma/#operation/GetAlertSettingDetails)
- [Add members to a monitoring group](/docs/api/rest/reference/phone/ma/#operation/addMembers)
- [Add an external contact](/docs/api/rest/reference/phone/ma/#operation/addExternalContact)
- [Delete a user's call log](/docs/api/rest/reference/phone/ma/#operation/deleteCallLog)
- [Unassign all phone numbers](/docs/api/rest/reference/phone/ma/#operation/unassignAllPhoneNumsAutoReceptionist)
- [Get a Zoom Room under Zoom Phone license](/docs/api/rest/reference/phone/ma/#operation/getZoomRoom)
- [Delete site level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/deleteSiteOutboundCallingExceptionRule)
- [The list of shared line groups](/docs/api/rest/reference/phone/ma/#operation/listSharedLineGroups)
- [Delete an emergency address](/docs/api/rest/reference/phone/ma/#operation/deleteEmergencyAddress)
- [List activation codes](/docs/api/rest/reference/phone/ma/#operation/listActivationCodes)
- [Batch add emergency service locations](/docs/api/rest/reference/phone/ma/#operation/batchAddLocations)
- [List phone numbers](/docs/api/rest/reference/phone/ma/#operation/listCRPhoneNumbers)
- [Send fax](/docs/api/rest/reference/phone/ma/#operation/SendEFax)
- [List emergency addresses](/docs/api/rest/reference/phone/ma/#operation/listEmergencyAddresses)
- [List firmware update rules](/docs/api/rest/reference/phone/ma/#operation/ListFirmwareRules)
- [Get call recordings](/docs/api/rest/reference/phone/ma/#operation/getPhoneRecordings)
- [Update a phone number](/docs/api/rest/reference/phone/ma/#operation/updatePhoneNumberDetails)
- [Update user level outbound calling countries or regions](/docs/api/rest/reference/phone/ma/#operation/UpdateUserOutboundCallingCountriesOrRegions)
- [Update a device](/docs/api/rest/reference/phone/ma/#operation/updateADevice)
- [Unassign a member from a shared line group](/docs/api/rest/reference/phone/ma/#operation/deleteAMemberSLG)
- [Update an auto receptionist policy](/docs/api/rest/reference/phone/ma/#operation/updateAutoReceptionistPolicy)
- [Sync user's call logs](/docs/api/rest/reference/phone/ma/#operation/syncUserCallLogs)
- [Add an emergency address](/docs/api/rest/reference/phone/ma/#operation/addEmergencyAddress)
- [Add a policy setting to a shared line group](/docs/api/rest/reference/phone/ma/#operation/addSLGPolicySubSetting)
- [Get account policy details](/docs/api/rest/reference/phone/ma/#operation/GetAccountPolicyDetails)
- [List common areas](/docs/api/rest/reference/phone/ma/#operation/listCommonAreas)
- [Delete an external contact](/docs/api/rest/reference/phone/ma/#operation/deleteAExternalContact)
- [List ported numbers](/docs/api/rest/reference/phone/ma/#operation/listPortedNumbers)
- [Unassign members from a shared line group](/docs/api/rest/reference/phone/ma/#operation/deleteMembersOfSLG)
- [Get a provision template](/docs/api/rest/reference/phone/ma/#operation/GetProvisionTemplate)
- [Get user's recordings](/docs/api/rest/reference/phone/ma/#operation/phoneUserRecordings)
- [Delete a monitoring group](/docs/api/rest/reference/phone/ma/#operation/deleteMonitoringGroup)
- [Update a phone role](/docs/api/rest/reference/phone/ma/#operation/UpdatePhoneRole)
- [Delete a common area](/docs/api/rest/reference/phone/ma/#operation/deleteCommonArea)
- [Sync SMS by session ID](/docs/api/rest/reference/phone/ma/#operation/smsSessionSync)
- [Add common area level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/AddCommonAreaOutboundCallingExceptionRule)
- [Get members of a monitoring group](/docs/api/rest/reference/phone/ma/#operation/listMembers)
- [Get call details from call log](/docs/api/rest/reference/phone/ma/#operation/getCallLogMetricsDetails)
- [Add members to a call queue](/docs/api/rest/reference/phone/ma/#operation/addMembersToCallQueue)
- [List blocked lists](/docs/api/rest/reference/phone/ma/#operation/listBlockedList)
- [List tracked locations](/docs/api/rest/reference/phone/ma/#operation/listTrackedLocations)
- [Update common area pin code](/docs/api/rest/reference/phone/ma/#operation/UpdateCommonAreaPinCode)
- [Get a phone site setting](/docs/api/rest/reference/phone/ma/#operation/getSiteSettingForType)
- [Add phone numbers for an account's customized outbound caller ID](/docs/api/rest/reference/phone/ma/#operation/addOutboundCallerNumbers)
- [List BYOC SIP trunks](/docs/api/rest/reference/phone/ma/#operation/listBYOCSIPTrunk)
- [Get SMS session details](/docs/api/rest/reference/phone/ma/#operation/smsSessionDetails)
- [Get call queue details](/docs/api/rest/reference/phone/ma/#operation/getACallQueue)
- [List users in directory](/docs/api/rest/reference/phone/ma/#operation/ListUsersFromDirectory)
- [Reboot a desk phone](/docs/api/rest/reference/phone/ma/#operation/rebootPhoneDevice)
- [Update opt statuses of phone numbers assigned to SMS campaign](/docs/api/rest/reference/phone/ma/#operation/updateNumberCampaignOptStatus)
- [Get monitoring group by ID](/docs/api/rest/reference/phone/ma/#operation/getMonitoringGroupById)
- [Get user's SMS sessions](/docs/api/rest/reference/phone/ma/#operation/userSmsSession)
- [Get SMS/MMS charges usage report](/docs/api/rest/reference/phone/ma/#operation/GetSMSChargesUsageReport)
- [Batch update device line key position](/docs/api/rest/reference/phone/ma/#operation/batchUpdateDeviceLineKeySetting)
- [Delete a user's shared access setting](/docs/api/rest/reference/phone/ma/#operation/deleteUserSetting)
- [Unassign an entity from the device](/docs/api/rest/reference/phone/ma/#operation/deleteExtensionFromADevice)
- [Assign phone numbers](/docs/api/rest/reference/phone/ma/#operation/assignPhoneNumbersAutoReceptionist)
- [Update emergency service location](/docs/api/rest/reference/phone/ma/#operation/updateLocation)
- [Assign a phone number to SMS campaign](/docs/api/rest/reference/phone/ma/#operation/assignCampaignPhoneNumbers)
- [List an account's inbound blocked statistics](/docs/api/rest/reference/phone/ma/#operation/ListAccountLevelInboundBlockedStatistics)
- [Update common area](/docs/api/rest/reference/phone/ma/#operation/updateCommonArea)
- [Download a phone voicemail](/docs/api/rest/reference/phone/ma/#operation/phoneDownloadVoicemailFile)
- [Delete firmware update rule](/docs/api/rest/reference/phone/ma/#operation/DeleteFirmwareUpdateRule)
- [Get account's SMS sessions](/docs/api/rest/reference/phone/ma/#operation/accountSmsSession)
- [Download fax file](/docs/api/rest/reference/phone/ma/#operation/Downloadfaxfile)
- [Add directory backup routing rule](/docs/api/rest/reference/phone/ma/#operation/addRoutingRule)
- [Get a user's profile settings](/docs/api/rest/reference/phone/ma/#operation/phoneUserSettings)
- [Get ported numbers details](/docs/api/rest/reference/phone/ma/#operation/getPortedNumbersDetails)
- [Unassign a phone number](/docs/api/rest/reference/phone/ma/#operation/unAssignPhoneNumCallQueue)
- [Delete a call recording](/docs/api/rest/reference/phone/ma/#operation/deleteCallRecording)
- [Get account voicemails](/docs/api/rest/reference/phone/ma/#operation/accountVoiceMails)
- [Add a device](/docs/api/rest/reference/phone/ma/#operation/addPhoneDevice)
- [List real time location for users](/docs/api/rest/reference/phone/ma/#operation/listUserRealtimeLocation)
- [Add an audio item for text-to-speech conversion](/docs/api/rest/reference/phone/ma/#operation/AddAnAudio)
- [Activate phone numbers](/docs/api/rest/reference/phone/ma/#operation/activeCRPhoneNumbers)
- [Add a user's shared access setting](/docs/api/rest/reference/phone/ma/#operation/addUserSetting)
- [Update peering phone numbers](/docs/api/rest/reference/phone/ma/#operation/updatePeeringPhoneNumbers)
- [Add members to a shared line group](/docs/api/rest/reference/phone/ma/#operation/addMembersToSharedLineGroup)
- [Get extension's fax logs](/docs/api/rest/reference/phone/ma/#operation/Getuser'sfaxlogs)
- [Update group policy](/docs/api/rest/reference/phone/ma/#operation/updateGroupPolicy)
- [Get operation logs report](/docs/api/rest/reference/phone/ma/#operation/getPSOperationLogs)
- [List phone sites](/docs/api/rest/reference/phone/ma/#operation/listPhoneSites)
- [Unassign phone numbers from common area](/docs/api/rest/reference/phone/ma/#operation/unassignPhoneNumbersFromCommonArea)
- [Add a client code to a call log](/docs/api/rest/reference/phone/ma/#operation/addClientCodeToCallLog)
- [Get directory backup routing rule](/docs/api/rest/reference/phone/ma/#operation/getRoutingRule)
- [Add a call handling setting](/docs/api/rest/reference/phone/ma/#operation/addCallHandling)
- [List phone roles](/docs/api/rest/reference/phone/ma/#operation/ListPhoneRoles)
- [List billing accounts](/docs/api/rest/reference/phone/ma/#operation/listBillingAccount)
- [Get account level outbound calling countries and regions](/docs/api/rest/reference/phone/ma/#operation/GetAccountOutboundCallingCountriesAndRegions)
- [Delete account level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/deleteAccountOutboundCallingExceptionRule)
- [Delete phone numbers for an account's customized outbound caller ID](/docs/api/rest/reference/phone/ma/#operation/deleteOutboundCallerNumbers)
- [Delete a phone role](/docs/api/rest/reference/phone/ma/#operation/DeletePhoneRole)
- [Post SMS message](/docs/api/rest/reference/phone/ma/#operation/postSmsMessage)
- [Delete a voicemail](/docs/api/rest/reference/phone/ma/#operation/deleteVoicemail)
- [Batch add users](/docs/api/rest/reference/phone/ma/#operation/batchAddUsers)
- [Get line key position and settings information](/docs/api/rest/reference/phone/ma/#operation/listLineKeySetting)
- [Sync deskphones](/docs/api/rest/reference/phone/ma/#operation/syncPhoneDevice)
- [Update an auto receptionist](/docs/api/rest/reference/phone/ma/#operation/updateAutoReceptionist)
- [Update user's calling plan](/docs/api/rest/reference/phone/ma/#operation/updateCallingPlan)
- [List account level outbound calling exception rules](/docs/api/rest/reference/phone/ma/#operation/listAccountOutboundCallingExceptionRule)
- [Get role information](/docs/api/rest/reference/phone/ma/#operation/getRoleInformation)
- [Update phone site details](/docs/api/rest/reference/phone/ma/#operation/updateSiteDetails)
- [List emergency service locations](/docs/api/rest/reference/phone/ma/#operation/listLocations)
- [List an account's customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/ma/#operation/listCustomizeOutboundCallerNumbers)
- [Delete group call pickup objects](/docs/api/rest/reference/phone/ma/#operation/deleteGCP)
- [Get voicemail details](/docs/api/rest/reference/phone/ma/#operation/getVoicemailDetails)
- [Get emergency service location details](/docs/api/rest/reference/phone/ma/#operation/getLocation)
- [Add an emergency service location](/docs/api/rest/reference/phone/ma/#operation/addLocation)
- [Update auto receptionist IVR](/docs/api/rest/reference/phone/ma/#operation/updateAutoReceptionistIVR)
- [Update a user's profile settings](/docs/api/rest/reference/phone/ma/#operation/updateUserSettings)
- [Get auto receptionist IVR](/docs/api/rest/reference/phone/ma/#operation/getAutoReceptionistIVR)
- [List site level outbound calling exception rules](/docs/api/rest/reference/phone/ma/#operation/listSiteOutboundCallingExceptionRule)
- [Update a setting template](/docs/api/rest/reference/phone/ma/#operation/updateSettingTemplate)
- [Get group phone settings](/docs/api/rest/reference/phone/ma/#operation/getGroupPhoneSettings)
- [Add members to a private directory](/docs/api/rest/reference/phone/ma/#operation/addMembersToAPrivateDirectory)
- [List updatable firmwares](/docs/api/rest/reference/phone/ma/#operation/ListFirmwares)
- [Add a group call pickup object](/docs/api/rest/reference/phone/ma/#operation/addGCP)
- [Download a phone recording](/docs/api/rest/reference/phone/ma/#operation/phoneDownloadRecordingFile)
- [Get site level outbound calling countries and regions](/docs/api/rest/reference/phone/ma/#operation/GetSiteOutboundCallingCountriesAndRegions)
- [Mark a phone number as blocked for all extensions](/docs/api/rest/reference/phone/ma/#operation/MarkPhoneNumberAsBlockedForAllExtensions)
- [Delete a call handling setting](/docs/api/rest/reference/phone/ma/#operation/deleteCallHandling)
- [List common area level outbound calling exception rules](/docs/api/rest/reference/phone/ma/#operation/listCommonAreaOutboundCallingExceptionRule)
- [Delete a line key setting.](/docs/api/rest/reference/phone/ma/#operation/DeleteLineKey)
- [List opt statuses of phone numbers assigned to SMS consent](/docs/api/rest/reference/phone/ma/#operation/getNumberConsentOptStatus)
- [Create a monitoring group](/docs/api/rest/reference/phone/ma/#operation/createMonitoringGroup)
- [Remove all monitors or monitored members from a monitoring group](/docs/api/rest/reference/phone/ma/#operation/removeMembers)
- [Get setting template details](/docs/api/rest/reference/phone/ma/#operation/getSettingTemplate)
- [Delete a non-primary auto receptionist](/docs/api/rest/reference/phone/ma/#operation/deleteAutoReceptionist)
- [Update a call handling setting](/docs/api/rest/reference/phone/ma/#operation/updateCallHandling)
- [Create a phone site](/docs/api/rest/reference/phone/ma/#operation/createPhoneSite)
- [Update common area level outbound calling countries or regions](/docs/api/rest/reference/phone/ma/#operation/UpdateCommonAreaOutboundCallingCountriesOrRegions)
- [Get User AI Call Summary Detail](/docs/api/rest/reference/phone/ma/#operation/getUserAICallSummary)
- [Get common area details](/docs/api/rest/reference/phone/ma/#operation/getACommonArea)
- [List directory backup routing rules](/docs/api/rest/reference/phone/ma/#operation/listRoutingRule)
- [Update the site setting](/docs/api/rest/reference/phone/ma/#operation/updateSiteSetting)
- [Delete a site setting](/docs/api/rest/reference/phone/ma/#operation/deleteSiteSetting)
- [Delete unassigned phone numbers](/docs/api/rest/reference/phone/ma/#operation/deleteUnassignedPhoneNumbers)
- [Delete a phone site](/docs/api/rest/reference/phone/ma/#operation/deletePhoneSite)
- [List an account's Zoom Phone settings](/docs/api/rest/reference/phone/ma/#operation/listZoomPhoneAccountSettings)
- [Get fax log details](/docs/api/rest/reference/phone/ma/#operation/GetFaxLogDetails)
- [Get a shared line group policy](/docs/api/rest/reference/phone/ma/#operation/getSharedLineGroupPolicy)
- [Add customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/ma/#operation/addSiteOutboundCallerNumbers)
- [Get a user's profile](/docs/api/rest/reference/phone/ma/#operation/phoneUser)
- [Get call pickup group by ID](/docs/api/rest/reference/phone/ma/#operation/GetGCP)
- [List call queue members](/docs/api/rest/reference/phone/ma/#operation/listCallQueueMembers)
- [List call pickup group members](/docs/api/rest/reference/phone/ma/#operation/listGCPMembers)
- [Duplicate a phone role](/docs/api/rest/reference/phone/ma/#operation/DuplicatePhoneRole)
- [Update a blocked list](/docs/api/rest/reference/phone/ma/#operation/updateBlockedList)
- [List members in a role](/docs/api/rest/reference/phone/ma/#operation/ListRoleMembers)
- [List group call pickup objects](/docs/api/rest/reference/phone/ma/#operation/listGCP)
- [Add a provision template](/docs/api/rest/reference/phone/ma/#operation/addProvisionTemplate)
- [Update a policy subsetting](/docs/api/rest/reference/phone/ma/#operation/updatePolicy)
- [List carrier peering phone numbers.](/docs/api/rest/reference/phone/ma/#operation/listCarrierPeeringPhoneNumbers)
- [Assign calling plan to a user](/docs/api/rest/reference/phone/ma/#operation/assignCallingPlan)
- [Remove users' customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/ma/#operation/deleteUserOutboundCallerNumbers)
- [Delete a user's call history](/docs/api/rest/reference/phone/ma/#operation/deleteUserCallHistory)
- [List SMS campaigns](/docs/api/rest/reference/phone/ma/#operation/listAccountSMSCampaigns)
- [Delete common area setting](/docs/api/rest/reference/phone/ma/#operation/deleteCommonAreaSetting)
- [Add members to a call pickup group](/docs/api/rest/reference/phone/ma/#operation/addGCPMembers)
- [List devices](/docs/api/rest/reference/phone/ma/#operation/listPhoneDevices)
- [Update a monitoring group](/docs/api/rest/reference/phone/ma/#operation/updateMonitoringGroup)
- [List private directory members](/docs/api/rest/reference/phone/ma/#operation/listPrivateDirectoryMembers)
- [List user's SMS sessions in descending order](/docs/api/rest/reference/phone/ma/#operation/GetSmsSessions)
- [Remove a phone number from a Zoom Room](/docs/api/rest/reference/phone/ma/#operation/UnassignPhoneNumberFromZoomRoom)
- [List shared line appearances](/docs/api/rest/reference/phone/ma/#operation/listSharedLineAppearances)
- [Add users to a directory](/docs/api/rest/reference/phone/ma/#operation/AddUsersToDirectory)
- [Remove customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/ma/#operation/deleteSiteOutboundCallerNumbers)
- [Delete a phone number](/docs/api/rest/reference/phone/ma/#operation/deleteCRPhoneNumber)
- [Add an account's inbound block rule](/docs/api/rest/reference/phone/ma/#operation/AddAccountLevelInboundBlockRules)
- [Add common area setting](/docs/api/rest/reference/phone/ma/#operation/AddCommonAreaSetting)
- [Remove a member from a monitoring group](/docs/api/rest/reference/phone/ma/#operation/removeMember)
- [Delete an account's inbound block rule](/docs/api/rest/reference/phone/ma/#operation/DeleteAccountLevelInboundBlockRules)
- [List alert settings with paging query](/docs/api/rest/reference/phone/ma/#operation/ListAlertSettingsWithPagingQuery)
- [Get external contact details](/docs/api/rest/reference/phone/ma/#operation/getAExternalContact)
- [Update an account's inbound block rule](/docs/api/rest/reference/phone/ma/#operation/UpdateAccountLevelInboundBlockRule)
- [Assign phone numbers to a Zoom Room](/docs/api/rest/reference/phone/ma/#operation/assignPhoneNumberToZoomRoom)
- [List past call metrics](/docs/api/rest/reference/phone/ma/#operation/listPastCallMetrics)
- [List Smartphones](/docs/api/rest/reference/phone/ma/#operation/ListSmartphones)
- [Update external contact](/docs/api/rest/reference/phone/ma/#operation/updateExternalContact)
- [Add a common area](/docs/api/rest/reference/phone/ma/#operation/addCommonArea)
- [Create a shared line group](/docs/api/rest/reference/phone/ma/#operation/createASharedLineGroup)
- [Get an audio item](/docs/api/rest/reference/phone/ma/#operation/GetAudioItem)
- [List an account's inbound block rules](/docs/api/rest/reference/phone/ma/#operation/ListAccountLevelInboundBlockRules)
- [Add an alert setting](/docs/api/rest/reference/phone/ma/#operation/AddAnAlertSetting)
- [Delete user level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/deleteUserOutboundCallingExceptionRule)
- [Update site level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/UpdateSiteOutboundCallingExceptionRule)
- [Remove peering phone numbers](/docs/api/rest/reference/phone/ma/#operation/deletePeeringPhoneNumbers)
- [Add account level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/AddAccountOutboundCallingExceptionRule)
- [Delete members in a role](/docs/api/rest/reference/phone/ma/#operation/DelRoleMembers)
- [Update a call queue's policy subsetting](/docs/api/rest/reference/phone/ma/#operation/updateCQPolicySubSetting)
- [Update common area setting](/docs/api/rest/reference/phone/ma/#operation/UpdateCommonAreaSetting)
- [List user's opt statuses of phone numbers](/docs/api/rest/reference/phone/ma/#operation/getUserNumberCampaignOptStatus)
- [Update a Zoom Room under Zoom Phone license](/docs/api/rest/reference/phone/ma/#operation/updateZoomRoom)
- [Update multiple users' properties in batch](/docs/api/rest/reference/phone/ma/#operation/updateUsersPropertiesInBatch)
- [Update a private directory member](/docs/api/rest/reference/phone/ma/#operation/updateAPrivateDirectoryMember)
- [Add users to a directory of a site](/docs/api/rest/reference/phone/ma/#operation/AddUsersToDirectoryBySite)
- [Create phone numbers](/docs/api/rest/reference/phone/ma/#operation/createCRPhoneNumbers)
- [Update directory backup routing rule](/docs/api/rest/reference/phone/ma/#operation/updateRoutingRule)
- [List SIP groups](/docs/api/rest/reference/phone/ma/#operation/listSipGroups)
- [List users permission for location sharing](/docs/api/rest/reference/phone/ma/#operation/listUserLocationSharingPermission)
- [Get device line keys information](/docs/api/rest/reference/phone/ma/#operation/listDeviceLineKeySetting)
- [Update account level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/UpdateAccountOutboundCallingExceptionRule)
- [Update a site's unassigned phone numbers](/docs/api/rest/reference/phone/ma/#operation/updateSiteForUnassignedPhoneNumbers)
- [List peering phone numbers](/docs/api/rest/reference/phone/ma/#operation/listPeeringPhoneNumbers)
- [Get call charges usage report](/docs/api/rest/reference/phone/ma/#operation/GetCallChargesUsageReport)
- [Add a firmware update rule](/docs/api/rest/reference/phone/ma/#operation/AddFirmwareRule)
- [Update site level outbound calling countries or regions](/docs/api/rest/reference/phone/ma/#operation/UpdateSiteOutboundCallingCountriesOrRegions)
- [Get user policy details](/docs/api/rest/reference/phone/ma/#operation/GetUserPolicyDetails)
- [List calling plans](/docs/api/rest/reference/phone/ma/#operation/listCallingPlans)
- [Add an extension's inbound block rule](/docs/api/rest/reference/phone/ma/#operation/AddExtensiontLevelInboundBlockRules)
- [Get firmware update rule information](/docs/api/rest/reference/phone/ma/#operation/GetFirmwareRuleDetail)
- [Batch update line key position and settings information](/docs/api/rest/reference/phone/ma/#operation/BatchUpdateLineKeySetting)
- [Unassign all members](/docs/api/rest/reference/phone/ma/#operation/unassignAllMembers)
- [Get user's call logs](/docs/api/rest/reference/phone/ma/#operation/phoneUserCallLogs)
- [Update provision template of a device](/docs/api/rest/reference/phone/ma/#operation/updateProvisionTemplateToDevice)
- [Get account's fax logs](/docs/api/rest/reference/phone/ma/#operation/GetAccount'sFaxLogs)
- [Delete an alert setting](/docs/api/rest/reference/phone/ma/#operation/DeleteAnAlertSetting)
- [Unassign user's calling plan](/docs/api/rest/reference/phone/ma/#operation/unassignCallingPlan)
- [Get SMS by message ID](/docs/api/rest/reference/phone/ma/#operation/smsByMessageId)
- [Delete a policy subsetting](/docs/api/rest/reference/phone/ma/#operation/DeletePolicy)
- [Get recording by call ID](/docs/api/rest/reference/phone/ma/#operation/getPhoneRecordingsByCallIdOrCallLogId)
- [List detectable personal location users](/docs/api/rest/reference/phone/ma/#operation/listUserDetectablePersonalLocation)
- [List Zoom Rooms under Zoom Phone license](/docs/api/rest/reference/phone/ma/#operation/listZoomRooms)
- [Assign calling plans to a common area](/docs/api/rest/reference/phone/ma/#operation/assignCallingPlansToCommonArea)
- [Get common area level outbound calling countries and regions](/docs/api/rest/reference/phone/ma/#operation/GetCommonAreaOutboundCallingCountriesAndRegions)
- [List default emergency address users](/docs/api/rest/reference/phone/ma/#operation/listUserDefaultEmergencyAddress)
- [List provision templates](/docs/api/rest/reference/phone/ma/#operation/listAccountProvisionTemplate)
- [List external contacts](/docs/api/rest/reference/phone/ma/#operation/listExternalContacts)
- [Get an SMS campaign](/docs/api/rest/reference/phone/ma/#operation/GetSMSCampaign)
- [Delete an SLG policy setting](/docs/api/rest/reference/phone/ma/#operation/removeSLGPolicySubSetting)
- [Add an auto receptionist](/docs/api/rest/reference/phone/ma/#operation/addAutoReceptionist)
- [List users in a directory by site](/docs/api/rest/reference/phone/ma/#operation/ListUsersFromDirectoryBySite)
- [Get a shared line group](/docs/api/rest/reference/phone/ma/#operation/getASharedLineGroup)
- [Get phone site details](/docs/api/rest/reference/phone/ma/#operation/getASite)
- [Delete a CQ policy setting](/docs/api/rest/reference/phone/ma/#operation/removeCQPolicySubSetting)
- [Assign calling plans to a Zoom Room](/docs/api/rest/reference/phone/ma/#operation/assignCallingPlanToRoom)
- [Get call handling settings](/docs/api/rest/reference/phone/ma/#operation/getCallHandling)
- [Add a policy subsetting](/docs/api/rest/reference/phone/ma/#operation/AddPolicy)
- [Get billing account details](/docs/api/rest/reference/phone/ma/#operation/GetABillingAccount)
- [Delete users from a directory of a site](/docs/api/rest/reference/phone/ma/#operation/DeleteUsersFromDirectoryBySite)
- [List user level outbound calling exception rules](/docs/api/rest/reference/phone/ma/#operation/listUserOutboundCallingExceptionRule)
- [Add site level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/AddSiteOutboundCallingExceptionRule)
- [Get user's voicemails](/docs/api/rest/reference/phone/ma/#operation/phoneUserVoiceMails)
- [Update firmware update rule](/docs/api/rest/reference/phone/ma/#operation/UpdateFirmwareRule)
- [Delete a provision template](/docs/api/rest/reference/phone/ma/#operation/deleteProvisionTemplate)
- [Get an auto receptionist policy](/docs/api/rest/reference/phone/ma/#operation/getAutoReceptionistsPolicy)
- [Add user level outbound calling exception rule](/docs/api/rest/reference/phone/ma/#operation/AddUserOutboundCallingExceptionRule)

### phone:read

View your phone information

**Associated APIs:**

- [List user's opt statuses of phone numbers](/docs/api/rest/reference/phone/methods/#operation/getUserNumberCampaignOptStatus)
- [Download fax file](/docs/api/rest/reference/phone/methods/#operation/Downloadfaxfile)
- [Download a phone recording transcript](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadRecordingTranscript)
- [Get call element](/docs/api/rest/reference/phone/methods/#operation/getCallElement)
- [Get a user's profile settings](/docs/api/rest/reference/phone/methods/#operation/phoneUserSettings)
- [Sync user's call logs](/docs/api/rest/reference/phone/methods/#operation/syncUserCallLogs)
- [List user's SMS sessions in descending order](/docs/api/rest/reference/phone/methods/#operation/GetSmsSessions)
- [List an extension's inbound block rules](/docs/api/rest/reference/phone/methods/#operation/ListExtensionLevelInboundBlockRules)
- [Download a phone recording](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadRecordingFile)
- [Get user's recordings](/docs/api/rest/reference/phone/methods/#operation/phoneUserRecordings)
- [Get device line keys information](/docs/api/rest/reference/phone/methods/#operation/listDeviceLineKeySetting)
- [Sync user's call history](/docs/api/rest/reference/phone/methods/#operation/syncUserCallHistory)
- [Get user's voicemails](/docs/api/rest/reference/phone/methods/#operation/phoneUserVoiceMails)
- [Get User AI Call Summary Detail](/docs/api/rest/reference/phone/methods/#operation/getUserAICallSummary)
- [Get extension's fax logs](/docs/api/rest/reference/phone/methods/#operation/Getuser'sfaxlogs)
- [Get call history detail](/docs/api/rest/reference/phone/methods/#operation/getCallHistoryDetail)
- [List users' phone numbers for a customized outbound caller ID](/docs/api/rest/reference/phone/methods/#operation/listUserCustomizeOutboundCallerNumbers)
- [Get user voicemail details from a call log](/docs/api/rest/reference/phone/methods/#operation/getVoicemailDetailsByCallIdOrCallLogId)
- [List audio items](/docs/api/rest/reference/phone/methods/#operation/ListAudioItems)
- [Get user's call logs](/docs/api/rest/reference/phone/methods/#operation/phoneUserCallLogs)
- [Sync SMS by session ID](/docs/api/rest/reference/phone/methods/#operation/smsSessionSync)
- [Get SMS session details](/docs/api/rest/reference/phone/methods/#operation/smsSessionDetails)
- [Get voicemail details](/docs/api/rest/reference/phone/methods/#operation/getVoicemailDetails)
- [Get a user's profile](/docs/api/rest/reference/phone/methods/#operation/phoneUser)
- [Get call log details](/docs/api/rest/reference/phone/methods/#operation/getCallLogDetails)
- [Get line key position and settings information](/docs/api/rest/reference/phone/methods/#operation/listLineKeySetting)
- [Get an audio item](/docs/api/rest/reference/phone/methods/#operation/GetAudioItem)
- [Get user's SMS sessions](/docs/api/rest/reference/phone/methods/#operation/userSmsSession)
- [Get SMS by message ID](/docs/api/rest/reference/phone/methods/#operation/smsByMessageId)
- [Download a phone voicemail](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadVoicemailFile)

### phone:read:admin

View all users' phone information

**Associated APIs:**

- [Get directory backup routing rule](/docs/api/rest/reference/phone/methods/#operation/getRoutingRule)
- [List emergency addresses](/docs/api/rest/reference/phone/methods/#operation/listEmergencyAddresses)
- [Get call history detail](/docs/api/rest/reference/phone/ma/#operation/getCallHistoryDetail)
- [Get a phone number](/docs/api/rest/reference/phone/methods/#operation/getPhoneNumberDetails)
- [Get a provision template](/docs/api/rest/reference/phone/methods/#operation/GetProvisionTemplate)
- [Get call charges usage report](/docs/api/rest/reference/phone/methods/#operation/GetCallChargesUsageReport)
- [List user's SMS sessions in descending order](/docs/api/rest/reference/phone/methods/#operation/GetSmsSessions)
- [Get an audio item](/docs/api/rest/reference/phone/methods/#operation/GetAudioItem)
- [List alert settings with paging query](/docs/api/rest/reference/phone/methods/#operation/ListAlertSettingsWithPagingQuery)
- [List phone numbers](/docs/api/rest/reference/phone/methods/#operation/listCRPhoneNumbers)
- [List an account's inbound block rules](/docs/api/rest/reference/phone/methods/#operation/ListAccountLevelInboundBlockRules)
- [List phone role targets](/docs/api/rest/reference/phone/methods/#operation/ListPhoneRoleTargets)
- [List ported numbers](/docs/api/rest/reference/phone/methods/#operation/listPortedNumbers)
- [Get external contact details](/docs/api/rest/reference/phone/methods/#operation/getAExternalContact)
- [List firmware update rules](/docs/api/rest/reference/phone/methods/#operation/ListFirmwareRules)
- [List default emergency address users](/docs/api/rest/reference/phone/methods/#operation/listUserDefaultEmergencyAddress)
- [Get device line keys information](/docs/api/rest/reference/phone/methods/#operation/listDeviceLineKeySetting)
- [Get SMS by message ID](/docs/api/rest/reference/phone/methods/#operation/smsByMessageId)
- [List common areas](/docs/api/rest/reference/phone/methods/#operation/listCommonAreas)
- [Get user's SMS sessions](/docs/api/rest/reference/phone/methods/#operation/userSmsSession)
- [Get emergency address details](/docs/api/rest/reference/phone/methods/#operation/getEmergencyAddress)
- [List BYOC SIP trunks](/docs/api/rest/reference/phone/methods/#operation/listBYOCSIPTrunk)
- [Get call recordings](/docs/api/rest/reference/phone/methods/#operation/getPhoneRecordings)
- [List users permission for location sharing](/docs/api/rest/reference/phone/methods/#operation/listUserLocationSharingPermission)
- [List past call metrics](/docs/api/rest/reference/phone/methods/#operation/listPastCallMetrics)
- [Get account policy details](/docs/api/rest/reference/phone/methods/#operation/GetAccountPolicyDetails)
- [Get a shared line group policy](/docs/api/rest/reference/phone/methods/#operation/getSharedLineGroupPolicy)
- [Get user's call logs](/docs/api/rest/reference/phone/methods/#operation/phoneUserCallLogs)
- [Get a Zoom Room under Zoom Phone license](/docs/api/rest/reference/phone/methods/#operation/getZoomRoom)
- [The list of shared line groups](/docs/api/rest/reference/phone/methods/#operation/listSharedLineGroups)
- [List user's opt statuses of phone numbers](/docs/api/rest/reference/phone/methods/#operation/getUserNumberCampaignOptStatus)
- [Sync user's call logs](/docs/api/rest/reference/phone/methods/#operation/syncUserCallLogs)
- [List calling plans](/docs/api/rest/reference/phone/methods/#operation/listCallingPlans)
- [List blocked lists](/docs/api/rest/reference/phone/methods/#operation/listBlockedList)
- [Get call details from call log](/docs/api/rest/reference/phone/methods/#operation/getCallLogMetricsDetails)
- [Get firmware update rule information](/docs/api/rest/reference/phone/methods/#operation/GetFirmwareRuleDetail)
- [Get members of a monitoring group](/docs/api/rest/reference/phone/methods/#operation/listMembers)
- [List users in directory](/docs/api/rest/reference/phone/methods/#operation/ListUsersFromDirectory)
- [List peering phone numbers](/docs/api/rest/reference/phone/methods/#operation/listPeeringPhoneNumbers)
- [Get SMS/MMS charges usage report](/docs/api/rest/reference/phone/methods/#operation/GetSMSChargesUsageReport)
- [Get user's recordings](/docs/api/rest/reference/phone/methods/#operation/phoneUserRecordings)
- [List detectable personal location users](/docs/api/rest/reference/phone/methods/#operation/listUserDetectablePersonalLocation)
- [Get account's fax logs](/docs/api/rest/reference/phone/methods/#operation/GetAccount'sFaxLogs)
- [Get ported numbers details](/docs/api/rest/reference/phone/methods/#operation/getPortedNumbersDetails)
- [Get common area settings](/docs/api/rest/reference/phone/methods/#operation/getCommonAreaSettings)
- [List SIP groups](/docs/api/rest/reference/phone/methods/#operation/listSipGroups)
- [Get recording by call ID](/docs/api/rest/reference/phone/methods/#operation/getPhoneRecordingsByCallIdOrCallLogId)
- [Get SMS session details](/docs/api/rest/reference/phone/methods/#operation/smsSessionDetails)
- [Get call queue details](/docs/api/rest/reference/phone/methods/#operation/getACallQueue)
- [Download a phone recording transcript](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadRecordingTranscript)
- [Get an SMS campaign](/docs/api/rest/reference/phone/methods/#operation/GetSMSCampaign)
- [List tracked locations](/docs/api/rest/reference/phone/methods/#operation/listTrackedLocations)
- [List provision templates](/docs/api/rest/reference/phone/methods/#operation/listAccountProvisionTemplate)
- [Get common area level outbound calling countries and regions](/docs/api/rest/reference/phone/methods/#operation/GetCommonAreaOutboundCallingCountriesAndRegions)
- [List Zoom Rooms under Zoom Phone license](/docs/api/rest/reference/phone/methods/#operation/listZoomRooms)
- [List an account's inbound blocked statistics](/docs/api/rest/reference/phone/methods/#operation/ListAccountLevelInboundBlockedStatistics)
- [List external contacts](/docs/api/rest/reference/phone/methods/#operation/listExternalContacts)
- [Get user's voicemails](/docs/api/rest/reference/phone/methods/#operation/phoneUserVoiceMails)
- [Get call history](/docs/api/rest/reference/phone/methods/#operation/getCallPath)
- [Download a phone voicemail](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadVoicemailFile)
- [List an account's customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/methods/#operation/listCustomizeOutboundCallerNumbers)
- [Get account voicemails](/docs/api/rest/reference/phone/methods/#operation/accountVoiceMails)
- [Get call handling settings](/docs/api/rest/reference/phone/methods/#operation/getCallHandling)
- [List real time location for users](/docs/api/rest/reference/phone/methods/#operation/listUserRealtimeLocation)
- [Get monitoring group by ID](/docs/api/rest/reference/phone/methods/#operation/getMonitoringGroupById)
- [Get account's SMS sessions](/docs/api/rest/reference/phone/methods/#operation/accountSmsSession)
- [List user level outbound calling exception rules](/docs/api/rest/reference/phone/methods/#operation/listUserOutboundCallingExceptionRule)
- [Get an auto receptionist policy](/docs/api/rest/reference/phone/methods/#operation/getAutoReceptionistsPolicy)
- [Get billing account details](/docs/api/rest/reference/phone/methods/#operation/GetABillingAccount)
- [Download fax file](/docs/api/rest/reference/phone/methods/#operation/Downloadfaxfile)
- [List phone sites](/docs/api/rest/reference/phone/methods/#operation/listPhoneSites)
- [List users in a directory by site](/docs/api/rest/reference/phone/methods/#operation/ListUsersFromDirectoryBySite)
- [Get a shared line group](/docs/api/rest/reference/phone/methods/#operation/getASharedLineGroup)
- [Get a user's profile settings](/docs/api/rest/reference/phone/methods/#operation/phoneUserSettings)
- [Get a phone site setting](/docs/api/rest/reference/phone/methods/#operation/getSiteSettingForType)
- [Get operation logs report](/docs/api/rest/reference/phone/methods/#operation/getPSOperationLogs)
- [Get extension's fax logs](/docs/api/rest/reference/phone/methods/#operation/Getuser'sfaxlogs)
- [Get role information](/docs/api/rest/reference/phone/methods/#operation/getRoleInformation)
- [Get voicemail details](/docs/api/rest/reference/phone/methods/#operation/getVoicemailDetails)
- [List setting templates](/docs/api/rest/reference/phone/methods/#operation/listSettingTemplates)
- [Get an auto receptionist](/docs/api/rest/reference/phone/methods/#operation/getAutoReceptionistDetail)
- [Get call QoS](/docs/api/rest/reference/phone/methods/#operation/getCallQoS)
- [List opt statuses of phone numbers assigned to SMS campaign](/docs/api/rest/reference/phone/methods/#operation/getNumberCampaignOptStatus)
- [List emergency service locations](/docs/api/rest/reference/phone/methods/#operation/listLocations)
- [Get line key position and settings information](/docs/api/rest/reference/phone/methods/#operation/listLineKeySetting)
- [List updatable firmwares](/docs/api/rest/reference/phone/methods/#operation/ListFirmwares)
- [Get call log details](/docs/api/rest/reference/phone/methods/#operation/getCallLogDetails)
- [List account level outbound calling exception rules](/docs/api/rest/reference/phone/methods/#operation/listAccountOutboundCallingExceptionRule)
- [List real time location for IP phones](/docs/api/rest/reference/phone/methods/#operation/listPhoneRealtimelocation)
- [Get blocked list details](/docs/api/rest/reference/phone/methods/#operation/getABlockedList)
- [List call logs](/docs/api/rest/reference/phone/methods/#operation/listCallLogsMetrics)
- [Get call element](/docs/api/rest/reference/phone/ma/#operation/getCallElement)
- [Get group phone settings](/docs/api/rest/reference/phone/methods/#operation/getGroupPhoneSettings)
- [List auto receptionists](/docs/api/rest/reference/phone/methods/#operation/listAutoReceptionists)
- [Get phone site details](/docs/api/rest/reference/phone/methods/#operation/getASite)
- [List an extension's inbound block rules](/docs/api/rest/reference/phone/methods/#operation/ListExtensionLevelInboundBlockRules)
- [Get a list of monitoring groups on an account](/docs/api/rest/reference/phone/methods/#operation/listMonitoringGroup)
- [List phone roles](/docs/api/rest/reference/phone/methods/#operation/ListPhoneRoles)
- [Get group policy details](/docs/api/rest/reference/phone/methods/#operation/GetGroupPolicyDetails)
- [List call pickup group members](/docs/api/rest/reference/phone/methods/#operation/listGCPMembers)
- [List common area level outbound calling exception rules](/docs/api/rest/reference/phone/methods/#operation/listCommonAreaOutboundCallingExceptionRule)
- [Get common area details](/docs/api/rest/reference/phone/methods/#operation/getACommonArea)
- [Download a phone recording](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadRecordingFile)
- [Get site level outbound calling countries and regions](/docs/api/rest/reference/phone/methods/#operation/GetSiteOutboundCallingCountriesAndRegions)
- [Get User AI Call Summary Detail](/docs/api/rest/reference/phone/methods/#operation/getUserAICallSummary)
- [Get auto receptionist IVR](/docs/api/rest/reference/phone/methods/#operation/getAutoReceptionistIVR)
- [Get account level outbound calling countries and regions](/docs/api/rest/reference/phone/methods/#operation/GetAccountOutboundCallingCountriesAndRegions)
- [List billing accounts](/docs/api/rest/reference/phone/methods/#operation/listBillingAccount)
- [Get account's call history](/docs/api/rest/reference/phone/ma/#operation/accountCallHistory)
- [List site level outbound calling exception rules](/docs/api/rest/reference/phone/methods/#operation/listSiteOutboundCallingExceptionRule)
- [Get fax log details](/docs/api/rest/reference/phone/methods/#operation/GetFaxLogDetails)
- [List users' phone numbers for a customized outbound caller ID](/docs/api/rest/reference/phone/methods/#operation/listUserCustomizeOutboundCallerNumbers)
- [Get setting template details](/docs/api/rest/reference/phone/methods/#operation/getSettingTemplate)
- [Get device details](/docs/api/rest/reference/phone/methods/#operation/getADevice)
- [List customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/methods/#operation/listSiteCustomizeOutboundCallerNumbers)
- [Get user level outbound calling countries and regions](/docs/api/rest/reference/phone/methods/#operation/GetUserOutboundCallingCountriesAndRegions)
- [Get user voicemail details from a call log](/docs/api/rest/reference/phone/methods/#operation/getVoicemailDetailsByCallIdOrCallLogId)
- [List opt statuses of phone numbers assigned to SMS consent](/docs/api/rest/reference/phone/methods/#operation/getNumberConsentOptStatus)
- [List directory backup routing rules](/docs/api/rest/reference/phone/methods/#operation/listRoutingRule)
- [Get user policy details](/docs/api/rest/reference/phone/methods/#operation/GetUserPolicyDetails)
- [List carrier peering phone numbers.](/docs/api/rest/reference/phone/methods/#operation/listCarrierPeeringPhoneNumbers)
- [Sync SMS by session ID](/docs/api/rest/reference/phone/methods/#operation/smsSessionSync)
- [List members in a role](/docs/api/rest/reference/phone/methods/#operation/ListRoleMembers)
- [Sync user's call history](/docs/api/rest/reference/phone/methods/#operation/syncUserCallHistory)
- [Get user's call history](/docs/api/rest/reference/phone/methods/#operation/phoneUserCallHistory)
- [Get fax charges usage report](/docs/api/rest/reference/phone/methods/#operation/Getfaxchargesusagereport)
- [List call queue members](/docs/api/rest/reference/phone/methods/#operation/listCallQueueMembers)
- [Get a user's profile](/docs/api/rest/reference/phone/methods/#operation/phoneUser)
- [List private directory members](/docs/api/rest/reference/phone/methods/#operation/listPrivateDirectoryMembers)
- [List an account's Zoom Phone settings](/docs/api/rest/reference/phone/methods/#operation/listZoomPhoneAccountSettings)
- [List audio items](/docs/api/rest/reference/phone/methods/#operation/ListAudioItems)
- [List call queue analytics](/docs/api/rest/reference/phone/ma/#operation/callqueueanalytics)
- [List call queues](/docs/api/rest/reference/phone/methods/#operation/listCallQueues)
- [List group call pickup objects](/docs/api/rest/reference/phone/methods/#operation/listGCP)
- [List shared line appearances](/docs/api/rest/reference/phone/methods/#operation/listSharedLineAppearances)
- [Get emergency service location details](/docs/api/rest/reference/phone/methods/#operation/getLocation)
- [Get call pickup group by ID](/docs/api/rest/reference/phone/methods/#operation/GetGCP)
- [List activation codes](/docs/api/rest/reference/phone/methods/#operation/listActivationCodes)
- [List phone users](/docs/api/rest/reference/phone/methods/#operation/listPhoneUsers)
- [Get call queue recordings](/docs/api/rest/reference/phone/methods/#operation/getCallQueueRecordings)
- [List Zoom Rooms without Zoom Phone assignment](/docs/api/rest/reference/phone/methods/#operation/listUnassignedZoomRooms)
- [List Smartphones](/docs/api/rest/reference/phone/methods/#operation/ListSmartphones)
- [List nomadic emergency services users](/docs/api/rest/reference/phone/methods/#operation/listUserNomadicEmergencyServices)
- [Get phone account settings](/docs/api/rest/reference/phone/methods/#operation/phoneSetting)
- [List devices](/docs/api/rest/reference/phone/methods/#operation/listPhoneDevices)
- [List SMS campaigns](/docs/api/rest/reference/phone/methods/#operation/listAccountSMSCampaigns)
- [Get account's call logs](/docs/api/rest/reference/phone/methods/#operation/accountCallLogs)
- [List plan information](/docs/api/rest/reference/phone/methods/#operation/listPhonePlans)
- [Get alert setting details](/docs/api/rest/reference/phone/methods/#operation/GetAlertSettingDetails)

### phone:write

View and manage your phone information

**Associated APIs:**

- [Add an audio item for text-to-speech conversion](/docs/api/rest/reference/phone/methods/#operation/AddAnAudio)
- [Update user's calling plan](/docs/api/rest/reference/phone/methods/#operation/updateCallingPlan)
- [Unassign user's calling plan](/docs/api/rest/reference/phone/methods/#operation/unassignCallingPlan)
- [Delete a line key setting.](/docs/api/rest/reference/phone/methods/#operation/DeleteLineKey)
- [Batch update device line key position](/docs/api/rest/reference/phone/methods/#operation/batchUpdateDeviceLineKeySetting)
- [Update Voicemail Read Status](/docs/api/rest/reference/phone/methods/#operation/updateVoicemailReadStatus)
- [Delete a user's shared access setting](/docs/api/rest/reference/phone/methods/#operation/deleteUserSetting)
- [Add audio items](/docs/api/rest/reference/phone/methods/#operation/AddAudioItem)
- [Add phone numbers for users' customized outbound caller ID](/docs/api/rest/reference/phone/methods/#operation/addUserOutboundCallerNumbers)
- [Remove users' customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/methods/#operation/deleteUserOutboundCallerNumbers)
- [Delete a user's call history](/docs/api/rest/reference/phone/methods/#operation/deleteUserCallHistory)
- [Update Recording Status](/docs/api/rest/reference/phone/methods/#operation/UpdateRecordingStatus)
- [Delete a user's call log](/docs/api/rest/reference/phone/methods/#operation/deleteCallLog)
- [Update Auto Delete Field](/docs/api/rest/reference/phone/methods/#operation/UpdateAutoDeleteField)
- [Delete an audio item](/docs/api/rest/reference/phone/methods/#operation/DeleteAudioItem)
- [Add an extension's inbound block rule](/docs/api/rest/reference/phone/methods/#operation/AddExtensiontLevelInboundBlockRules)
- [Send fax](/docs/api/rest/reference/phone/methods/#operation/SendEFax)
- [Add a user's shared access setting](/docs/api/rest/reference/phone/methods/#operation/addUserSetting)
- [Post SMS message](/docs/api/rest/reference/phone/methods/#operation/postSmsMessage)
- [Unassign a phone number](/docs/api/rest/reference/phone/methods/#operation/UnassignPhoneNumber)
- [Delete a call recording](/docs/api/rest/reference/phone/methods/#operation/deleteCallRecording)
- [Update a user's shared access setting](/docs/api/rest/reference/phone/methods/#operation/updateUserSetting)
- [Delete a voicemail](/docs/api/rest/reference/phone/methods/#operation/deleteVoicemail)
- [Update a user's profile settings](/docs/api/rest/reference/phone/methods/#operation/updateUserSettings)
- [Upload fax file](/docs/api/rest/reference/phone/methods/#operation/UploadFaxFiles)
- [Delete an extension's inbound block rule](/docs/api/rest/reference/phone/methods/#operation/DeleteExtensiontLevelInboundBlockRules)
- [Batch update line key position and settings information](/docs/api/rest/reference/phone/methods/#operation/BatchUpdateLineKeySetting)
- [Update an audio item](/docs/api/rest/reference/phone/methods/#operation/UpdateAudioItem)
- [Update a user's profile](/docs/api/rest/reference/phone/methods/#operation/updateUserProfile)
- [Assign calling plan to a user](/docs/api/rest/reference/phone/methods/#operation/assignCallingPlan)
- [Assign a phone number to a user](/docs/api/rest/reference/phone/methods/#operation/assignPhoneNumber)

### phone:write:admin

View and manage all users' phone information

**Associated APIs:**

- [Unassign a phone number](/docs/api/rest/reference/phone/methods/#operation/UnassignPhoneNumber)
- [Create a shared line group](/docs/api/rest/reference/phone/methods/#operation/createASharedLineGroup)
- [Send fax](/docs/api/rest/reference/phone/methods/#operation/SendEFax)
- [Update site level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/UpdateSiteOutboundCallingExceptionRule)
- [Delete an emergency address](/docs/api/rest/reference/phone/methods/#operation/deleteEmergencyAddress)
- [Batch add emergency service locations](/docs/api/rest/reference/phone/methods/#operation/batchAddLocations)
- [Update site level outbound calling countries or regions](/docs/api/rest/reference/phone/methods/#operation/UpdateSiteOutboundCallingCountriesOrRegions)
- [Delete a phone number](/docs/api/rest/reference/phone/methods/#operation/deleteCRPhoneNumber)
- [Update Auto Delete Field](/docs/api/rest/reference/phone/methods/#operation/UpdateAutoDeleteField)
- [Remove users' customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/methods/#operation/deleteUserOutboundCallerNumbers)
- [Update a Zoom Room under Zoom Phone license](/docs/api/rest/reference/phone/methods/#operation/updateZoomRoom)
- [Delete a monitoring group](/docs/api/rest/reference/phone/methods/#operation/deleteMonitoringGroup)
- [Delete common area setting](/docs/api/rest/reference/phone/methods/#operation/deleteCommonAreaSetting)
- [Generate activation codes for common areas](/docs/api/rest/reference/phone/methods/#operation/Generateactivationcodesforcommonareas)
- [Batch update device line key position](/docs/api/rest/reference/phone/methods/#operation/batchUpdateDeviceLineKeySetting)
- [Add an account's inbound block rule](/docs/api/rest/reference/phone/methods/#operation/AddAccountLevelInboundBlockRules)
- [Unassign an entity from the device](/docs/api/rest/reference/phone/methods/#operation/deleteExtensionFromADevice)
- [Remove peering phone numbers](/docs/api/rest/reference/phone/methods/#operation/deletePeeringPhoneNumbers)
- [Add a setting template](/docs/api/rest/reference/phone/methods/#operation/addSettingTemplate)
- [Delete members in a role](/docs/api/rest/reference/phone/methods/#operation/DelRoleMembers)
- [Delete a user's shared access setting](/docs/api/rest/reference/phone/methods/#operation/deleteUserSetting)
- [Assign calling plans to a Zoom Room](/docs/api/rest/reference/phone/methods/#operation/assignCallingPlanToRoom)
- [Batch update line key position and settings information](/docs/api/rest/reference/phone/methods/#operation/BatchUpdateLineKeySetting)
- [Add a provision template](/docs/api/rest/reference/phone/methods/#operation/addProvisionTemplate)
- [Delete a device](/docs/api/rest/reference/phone/methods/#operation/deleteADevice)
- [Remove customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/methods/#operation/deleteSiteOutboundCallerNumbers)
- [Update an alert setting](/docs/api/rest/reference/phone/methods/#operation/UpdateAnAlertSetting)
- [Delete a policy subsetting](/docs/api/rest/reference/phone/methods/#operation/DeletePolicy)
- [Delete phone role targets](/docs/api/rest/reference/phone/ma/#operation/DeletePhoneRoleTargets)
- [Update opt statuses of phone numbers assigned to SMS campaign](/docs/api/rest/reference/phone/methods/#operation/updateNumberCampaignOptStatus)
- [Update a provision template](/docs/api/rest/reference/phone/methods/#operation/updateProvisionTemplate)
- [Add BYOC phone numbers](/docs/api/rest/reference/phone/methods/#operation/addBYOCNumber)
- [Update the site setting](/docs/api/rest/reference/phone/methods/#operation/updateSiteSetting)
- [Add members to a monitoring group](/docs/api/rest/reference/phone/methods/#operation/addMembers)
- [Add common area level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/AddCommonAreaOutboundCallingExceptionRule)
- [Update common area level outbound calling countries or regions](/docs/api/rest/reference/phone/methods/#operation/UpdateCommonAreaOutboundCallingCountriesOrRegions)
- [Update Recording Status](/docs/api/rest/reference/phone/methods/#operation/UpdateRecordingStatus)
- [Assign phone numbers](/docs/api/rest/reference/phone/methods/#operation/assignPhoneNumbersSLG)
- [Add members to a call pickup group](/docs/api/rest/reference/phone/methods/#operation/addGCPMembers)
- [Remove a member from a monitoring group](/docs/api/rest/reference/phone/methods/#operation/removeMember)
- [Delete an audio item](/docs/api/rest/reference/phone/methods/#operation/DeleteAudioItem)
- [Add members to a call queue](/docs/api/rest/reference/phone/methods/#operation/addMembersToCallQueue)
- [Delete an emergency location](/docs/api/rest/reference/phone/methods/#operation/deleteLocation)
- [Update a setting template](/docs/api/rest/reference/phone/methods/#operation/updateSettingTemplate)
- [Add peering phone numbers](/docs/api/rest/reference/phone/methods/#operation/addPeeringPhoneNumbers)
- [Update common area level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/UpdateCommonAreaOutboundCallingExceptionRule)
- [Delete an external contact](/docs/api/rest/reference/phone/methods/#operation/deleteAExternalContact)
- [Remove a phone number from a Zoom Room](/docs/api/rest/reference/phone/methods/#operation/UnassignPhoneNumberFromZoomRoom)
- [Update user level outbound calling countries or regions](/docs/api/rest/reference/phone/methods/#operation/UpdateUserOutboundCallingCountriesOrRegions)
- [Update Voicemail Read Status](/docs/api/rest/reference/phone/methods/#operation/updateVoicemailReadStatus)
- [Create a call queue](/docs/api/rest/reference/phone/methods/#operation/createCallQueue)
- [Unassign a member](/docs/api/rest/reference/phone/methods/#operation/unassignMemberFromCallQueue)
- [Update user level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/UpdateUserOutboundCallingExceptionRule)
- [Update a user's profile](/docs/api/rest/reference/phone/methods/#operation/updateUserProfile)
- [Create a monitoring group](/docs/api/rest/reference/phone/methods/#operation/createMonitoringGroup)
- [Add a user's shared access setting](/docs/api/rest/reference/phone/methods/#operation/addUserSetting)
- [Delete users from a directory](/docs/api/rest/reference/phone/methods/#operation/DeleteUsersFromDirectory)
- [Add members to a shared line group](/docs/api/rest/reference/phone/methods/#operation/addMembersToSharedLineGroup)
- [Add a call handling setting](/docs/api/rest/reference/phone/methods/#operation/addCallHandling)
- [Delete a voicemail](/docs/api/rest/reference/phone/methods/#operation/deleteVoicemail)
- [Update user policy](/docs/api/rest/reference/phone/methods/#operation/updateUserPolicy)
- [Unassign a calling plan from the common area](/docs/api/rest/reference/phone/methods/#operation/unassignCallingPlansFromCommonArea)
- [Mark a phone number as blocked for all extensions](/docs/api/rest/reference/phone/methods/#operation/MarkPhoneNumberAsBlockedForAllExtensions)
- [Update the group call pickup information](/docs/api/rest/reference/phone/methods/#operation/updateGCP)
- [Add an audio item for text-to-speech conversion](/docs/api/rest/reference/phone/methods/#operation/AddAnAudio)
- [Delete a site setting](/docs/api/rest/reference/phone/methods/#operation/deleteSiteSetting)
- [Update a shared line group](/docs/api/rest/reference/phone/methods/#operation/updateASharedLineGroup)
- [Update phone account settings](/docs/api/rest/reference/phone/methods/#operation/updatePhoneSettings)
- [Update account level outbound calling countries or regions](/docs/api/rest/reference/phone/methods/#operation/UpdateAccountOutboundCallingCountriesOrRegions)
- [Update phone site details](/docs/api/rest/reference/phone/methods/#operation/updateSiteDetails)
- [Update peering phone numbers](/docs/api/rest/reference/phone/methods/#operation/updatePeeringPhoneNumbers)
- [Delete a shared line group](/docs/api/rest/reference/phone/methods/#operation/deleteASharedLineGroup)
- [Update a blocked list](/docs/api/rest/reference/phone/methods/#operation/updateBlockedList)
- [Batch add users](/docs/api/rest/reference/phone/methods/#operation/batchAddUsers)
- [Add a policy subsetting to a call queue](/docs/api/rest/reference/phone/methods/#operation/addCQPolicySubSetting)
- [Update a policy subsetting](/docs/api/rest/reference/phone/methods/#operation/updatePolicy)
- [Delete firmware update rule](/docs/api/rest/reference/phone/methods/#operation/DeleteFirmwareUpdateRule)
- [Update an audio item](/docs/api/rest/reference/phone/methods/#operation/UpdateAudioItem)
- [Reboot a desk phone](/docs/api/rest/reference/phone/methods/#operation/rebootPhoneDevice)
- [Add phone numbers for an account's customized outbound caller ID](/docs/api/rest/reference/phone/methods/#operation/addOutboundCallerNumbers)
- [Delete a call recording](/docs/api/rest/reference/phone/methods/#operation/deleteCallRecording)
- [Remove a Zoom Room from a ZP account](/docs/api/rest/reference/phone/methods/#operation/RemoveZoomRoom)
- [Activate phone numbers](/docs/api/rest/reference/phone/methods/#operation/activeCRPhoneNumbers)
- [Add members to roles](/docs/api/rest/reference/phone/methods/#operation/AddRoleMembers)
- [Delete a common area](/docs/api/rest/reference/phone/methods/#operation/deleteCommonArea)
- [Add phone role targets](/docs/api/rest/reference/phone/methods/#operation/AddPhoneRoleTargets)
- [Add a client code to a call log](/docs/api/rest/reference/phone/methods/#operation/addClientCodeToCallLog)
- [Unassign phone numbers from common area](/docs/api/rest/reference/phone/methods/#operation/unassignPhoneNumbersFromCommonArea)
- [Update group policy](/docs/api/rest/reference/phone/methods/#operation/updateGroupPolicy)
- [Unassign a member from a shared line group](/docs/api/rest/reference/phone/methods/#operation/deleteAMemberSLG)
- [Update a phone number](/docs/api/rest/reference/phone/methods/#operation/updatePhoneNumberDetails)
- [Add a device](/docs/api/rest/reference/phone/methods/#operation/addPhoneDevice)
- [Unassign members from a shared line group](/docs/api/rest/reference/phone/methods/#operation/deleteMembersOfSLG)
- [Add audio items](/docs/api/rest/reference/phone/methods/#operation/AddAudioItem)
- [Remove a member from a private directory](/docs/api/rest/reference/phone/methods/#operation/removeAMemberFromAPrivateDirectory)
- [Delete phone numbers for an account's customized outbound caller ID](/docs/api/rest/reference/phone/methods/#operation/deleteOutboundCallerNumbers)
- [Assign a phone number to SMS campaign](/docs/api/rest/reference/phone/methods/#operation/assignCampaignPhoneNumbers)
- [Add an emergency address](/docs/api/rest/reference/phone/methods/#operation/addEmergencyAddress)
- [Add directory backup routing rule](/docs/api/rest/reference/phone/methods/#operation/addRoutingRule)
- [Unassign all phone numbers](/docs/api/rest/reference/phone/methods/#operation/unassignAPhoneNumCallQueue)
- [Update common area](/docs/api/rest/reference/phone/methods/#operation/updateCommonArea)
- [Update account level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/UpdateAccountOutboundCallingExceptionRule)
- [Delete site level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/deleteSiteOutboundCallingExceptionRule)
- [Update a site's unassigned phone numbers](/docs/api/rest/reference/phone/methods/#operation/updateSiteForUnassignedPhoneNumbers)
- [Update an account's inbound block rule](/docs/api/rest/reference/phone/methods/#operation/UpdateAccountLevelInboundBlockRule)
- [Delete a user's call log](/docs/api/rest/reference/phone/methods/#operation/deleteCallLog)
- [Delete a provision template](/docs/api/rest/reference/phone/methods/#operation/deleteProvisionTemplate)
- [Update directory backup routing rule](/docs/api/rest/reference/phone/methods/#operation/updateRoutingRule)
- [Add account level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/AddAccountOutboundCallingExceptionRule)
- [Add an external contact](/docs/api/rest/reference/phone/methods/#operation/addExternalContact)
- [Update an auto receptionist policy](/docs/api/rest/reference/phone/methods/#operation/updateAutoReceptionistPolicy)
- [Create phone numbers](/docs/api/rest/reference/phone/methods/#operation/createCRPhoneNumbers)
- [Assign numbers to a call queue](/docs/api/rest/reference/phone/methods/#operation/assignPhoneToCallQueue)
- [Update a shared line group policy](/docs/api/rest/reference/phone/methods/#operation/updateSharedLineGroupPolicy)
- [Add a policy setting to a shared line group](/docs/api/rest/reference/phone/methods/#operation/addSLGPolicySubSetting)
- [Update emergency service location](/docs/api/rest/reference/phone/methods/#operation/updateLocation)
- [Add a common area](/docs/api/rest/reference/phone/methods/#operation/addCommonArea)
- [Unassign user's calling plan](/docs/api/rest/reference/phone/methods/#operation/unassignCallingPlan)
- [Assign calling plan to a user](/docs/api/rest/reference/phone/methods/#operation/assignCallingPlan)
- [Update a user's shared access setting](/docs/api/rest/reference/phone/methods/#operation/updateUserSetting)
- [Delete an account's inbound blocked statistics](/docs/api/rest/reference/phone/methods/#operation/DeleteAccountLevelInboundBlockedStatistics)
- [Assign an entity to a device](/docs/api/rest/reference/phone/methods/#operation/addExtensionsToADevice)
- [Create a blocked list](/docs/api/rest/reference/phone/methods/#operation/addAnumberToBlockedList)
- [Update a phone role](/docs/api/rest/reference/phone/methods/#operation/UpdatePhoneRole)
- [Delete a phone site](/docs/api/rest/reference/phone/methods/#operation/deletePhoneSite)
- [Delete an alert setting](/docs/api/rest/reference/phone/methods/#operation/DeleteAnAlertSetting)
- [Add customized outbound caller ID phone numbers](/docs/api/rest/reference/phone/methods/#operation/addSiteOutboundCallerNumbers)
- [Delete an account's inbound block rule](/docs/api/rest/reference/phone/methods/#operation/DeleteAccountLevelInboundBlockRules)
- [Update a call handling setting](/docs/api/rest/reference/phone/methods/#operation/updateCallHandling)
- [Create a phone site](/docs/api/rest/reference/phone/methods/#operation/createPhoneSite)
- [Remove all monitors or monitored members from a monitoring group](/docs/api/rest/reference/phone/methods/#operation/removeMembers)
- [Remove members from call pickup group](/docs/api/rest/reference/phone/methods/#operation/removeGCPMembers)
- [Update a device](/docs/api/rest/reference/phone/methods/#operation/updateADevice)
- [Add a client code to a call history](/docs/api/rest/reference/phone/methods/#operation/addClientCodeToCallHistory)
- [Update common area pin code](/docs/api/rest/reference/phone/methods/#operation/UpdateCommonAreaPinCode)
- [Add an extension's inbound block rule](/docs/api/rest/reference/phone/methods/#operation/AddExtensiontLevelInboundBlockRules)
- [Add common area setting](/docs/api/rest/reference/phone/methods/#operation/AddCommonAreaSetting)
- [Add a site setting](/docs/api/rest/reference/phone/methods/#operation/addSiteSetting)
- [Add users to a directory](/docs/api/rest/reference/phone/methods/#operation/AddUsersToDirectory)
- [Remove a calling plan from a Zoom Room](/docs/api/rest/reference/phone/methods/#operation/unassignCallingPlanFromRoom)
- [Update multiple users' properties in batch](/docs/api/rest/reference/phone/methods/#operation/updateUsersPropertiesInBatch)
- [Update a monitoring group](/docs/api/rest/reference/phone/methods/#operation/updateMonitoringGroup)
- [Delete a blocked list](/docs/api/rest/reference/phone/methods/#operation/deleteABlockedList)
- [Add an alert setting](/docs/api/rest/reference/phone/methods/#operation/AddAnAlertSetting)
- [Assign phone numbers to a Zoom Room](/docs/api/rest/reference/phone/methods/#operation/assignPhoneNumberToZoomRoom)
- [Delete unassigned phone numbers](/docs/api/rest/reference/phone/methods/#operation/deleteUnassignedPhoneNumbers)
- [Update a private directory member](/docs/api/rest/reference/phone/methods/#operation/updateAPrivateDirectoryMember)
- [Delete directory backup routing rule](/docs/api/rest/reference/phone/methods/#operation/deleteRoutingRule)
- [Assign a phone number to a user](/docs/api/rest/reference/phone/methods/#operation/assignPhoneNumber)
- [Delete a phone role](/docs/api/rest/reference/phone/methods/#operation/DeletePhoneRole)
- [Post SMS message](/docs/api/rest/reference/phone/methods/#operation/postSmsMessage)
- [Delete an extension's inbound block rule](/docs/api/rest/reference/phone/methods/#operation/DeleteExtensiontLevelInboundBlockRules)
- [Delete a non-primary auto receptionist](/docs/api/rest/reference/phone/methods/#operation/deleteAutoReceptionist)
- [Sync deskphones](/docs/api/rest/reference/phone/methods/#operation/syncPhoneDevice)
- [Update an emergency address](/docs/api/rest/reference/phone/methods/#operation/updateEmergencyAddress)
- [Update an auto receptionist](/docs/api/rest/reference/phone/methods/#operation/updateAutoReceptionist)
- [Update an SLG policy setting](/docs/api/rest/reference/phone/methods/#operation/updateSLGPolicySubSetting)
- [Update account policy](/docs/api/rest/reference/phone/methods/#operation/updateAccountPolicy)
- [Add a policy subsetting](/docs/api/rest/reference/phone/methods/#operation/AddPolicy)
- [Delete a line key setting.](/docs/api/rest/reference/phone/methods/#operation/DeleteLineKey)
- [Delete account level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/deleteAccountOutboundCallingExceptionRule)
- [Add site level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/AddSiteOutboundCallingExceptionRule)
- [Delete a user's call history](/docs/api/rest/reference/phone/methods/#operation/deleteUserCallHistory)
- [Apply template to common areas](/docs/api/rest/reference/phone/methods/#operation/ApplyTemplatetoCommonAreas)
- [Delete group call pickup objects](/docs/api/rest/reference/phone/methods/#operation/deleteGCP)
- [Add an auto receptionist](/docs/api/rest/reference/phone/methods/#operation/addAutoReceptionist)
- [Duplicate a phone role](/docs/api/rest/reference/phone/methods/#operation/DuplicatePhoneRole)
- [Add phone numbers for users' customized outbound caller ID](/docs/api/rest/reference/phone/methods/#operation/addUserOutboundCallerNumbers)
- [Delete a call handling setting](/docs/api/rest/reference/phone/methods/#operation/deleteCallHandling)
- [Upload fax file](/docs/api/rest/reference/phone/methods/#operation/UploadFaxFiles)
- [Update provision template of a device](/docs/api/rest/reference/phone/methods/#operation/updateProvisionTemplateToDevice)
- [Delete common area level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/deleteCommonAreaOutboundCallingExceptionRule)
- [Assign calling plans to a common area](/docs/api/rest/reference/phone/methods/#operation/assignCallingPlansToCommonArea)
- [Delete users from a directory of a site](/docs/api/rest/reference/phone/methods/#operation/DeleteUsersFromDirectoryBySite)
- [Add a group call pickup object](/docs/api/rest/reference/phone/methods/#operation/addGCP)
- [Add members to a private directory](/docs/api/rest/reference/phone/methods/#operation/addMembersToAPrivateDirectory)
- [Unassign all members](/docs/api/rest/reference/phone/methods/#operation/unassignAllMembers)
- [Add users to a directory of a site](/docs/api/rest/reference/phone/methods/#operation/AddUsersToDirectoryBySite)
- [Update firmware update rule](/docs/api/rest/reference/phone/methods/#operation/UpdateFirmwareRule)
- [Add user level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/AddUserOutboundCallingExceptionRule)
- [Delete user level outbound calling exception rule](/docs/api/rest/reference/phone/methods/#operation/deleteUserOutboundCallingExceptionRule)
- [Assign phone numbers to a common area](/docs/api/rest/reference/phone/methods/#operation/assignPhoneNumbersToCommonArea)
- [Add a firmware update rule](/docs/api/rest/reference/phone/methods/#operation/AddFirmwareRule)
- [Update common area setting](/docs/api/rest/reference/phone/methods/#operation/UpdateCommonAreaSetting)
- [Update call queue details](/docs/api/rest/reference/phone/methods/#operation/updateCallQueue)
- [Add a Zoom Room to a Zoom Phone](/docs/api/rest/reference/phone/methods/#operation/addZoomRoom)
- [Update external contact](/docs/api/rest/reference/phone/methods/#operation/updateExternalContact)
- [Add an emergency service location](/docs/api/rest/reference/phone/methods/#operation/addLocation)
- [Delete a call queue](/docs/api/rest/reference/phone/methods/#operation/deleteACallQueue)
- [Delete a CQ policy setting](/docs/api/rest/reference/phone/methods/#operation/removeCQPolicySubSetting)
- [Update user's calling plan](/docs/api/rest/reference/phone/methods/#operation/updateCallingPlan)
- [Update a user's profile settings](/docs/api/rest/reference/phone/methods/#operation/updateUserSettings)
- [Update auto receptionist IVR](/docs/api/rest/reference/phone/methods/#operation/updateAutoReceptionistIVR)
- [Delete an SLG policy setting](/docs/api/rest/reference/phone/methods/#operation/removeSLGPolicySubSetting)
- [Update a call queue's policy subsetting](/docs/api/rest/reference/phone/methods/#operation/updateCQPolicySubSetting)

### phone_call_log:master

View and manage all subaccounts' call logs

**Associated APIs:**

- [Get user's call logs](/docs/api/rest/reference/phone/ma/#operation/phoneUserCallLogs)
- [Get account's call logs](/docs/api/rest/reference/phone/ma/#operation/accountCallLogs)
- [Get call log details](/docs/api/rest/reference/phone/ma/#operation/getCallLogDetails)
- [Delete a user's call log](/docs/api/rest/reference/phone/ma/#operation/deleteCallLog)
- [Delete a user's call history](/docs/api/rest/reference/phone/ma/#operation/deleteUserCallHistory)

### phone_call_log:read

View your call history information

**Associated APIs:**

- [Get user's call history](/docs/api/rest/reference/phone/ma/#operation/phoneUserCallHistory)
- [Get user's call logs](/docs/api/rest/reference/phone/methods/#operation/phoneUserCallLogs)
- [Get call element](/docs/api/rest/reference/phone/methods/#operation/getCallElement)
- [Get call history detail](/docs/api/rest/reference/phone/methods/#operation/getCallHistoryDetail)
- [Get call log details](/docs/api/rest/reference/phone/methods/#operation/getCallLogDetails)

### phone_call_log:read:admin

View all users' call history information

**Associated APIs:**

- [Get account's call history](/docs/api/rest/reference/phone/methods/#operation/accountCallHistory)
- [Get call log details](/docs/api/rest/reference/phone/methods/#operation/getCallLogDetails)
- [Get call history detail](/docs/api/rest/reference/phone/methods/#operation/getCallHistoryDetail)
- [Get user's call logs](/docs/api/rest/reference/phone/methods/#operation/phoneUserCallLogs)
- [Get call element](/docs/api/rest/reference/phone/ma/#operation/getCallElement)
- [Get account's call logs](/docs/api/rest/reference/phone/methods/#operation/accountCallLogs)
- [Get call history](/docs/api/rest/reference/phone/ma/#operation/getCallPath)

### phone_call_log:write

View and manage your call log information

**Associated APIs:**

- [Delete a user's call log](/docs/api/rest/reference/phone/methods/#operation/deleteCallLog)
- [Delete a user's call history](/docs/api/rest/reference/phone/methods/#operation/deleteUserCallHistory)

### phone_call_log:write:admin

View and manage all users' call log information

**Associated APIs:**

- [Delete a user's call log](/docs/api/rest/reference/phone/methods/#operation/deleteCallLog)
- [Delete a user's call history](/docs/api/rest/reference/phone/methods/#operation/deleteUserCallHistory)

### phone_peering:master

View and manage subaccounts' E164 numbers sent via peering API

**Associated APIs:**

- [List peering phone numbers](/docs/api/rest/reference/phone/ma/#operation/listPeeringPhoneNumbers)
- [Add peering phone numbers](/docs/api/rest/reference/phone/ma/#operation/addPeeringPhoneNumbers)
- [Remove peering phone numbers](/docs/api/rest/reference/phone/ma/#operation/deletePeeringPhoneNumbers)
- [Update peering phone numbers](/docs/api/rest/reference/phone/ma/#operation/updatePeeringPhoneNumbers)
- [List carrier peering phone numbers.](/docs/api/rest/reference/phone/ma/#operation/listCarrierPeeringPhoneNumbers)

### phone_peering:read:admin

View the E164 numbers sent via peering API

**Associated APIs:**

- [List ported numbers](/docs/api/rest/reference/phone/methods/#operation/listPortedNumbers)
- [Get ported numbers details](/docs/api/rest/reference/phone/methods/#operation/getPortedNumbersDetails)
- [List peering phone numbers](/docs/api/rest/reference/phone/methods/#operation/listPeeringPhoneNumbers)
- [List carrier peering phone numbers.](/docs/api/rest/reference/phone/methods/#operation/listCarrierPeeringPhoneNumbers)

### phone_peering:write:admin

View and manage the E164 numbers sent via peering API

**Associated APIs:**

- [Update peering phone numbers](/docs/api/rest/reference/phone/methods/#operation/updatePeeringPhoneNumbers)
- [Remove peering phone numbers](/docs/api/rest/reference/phone/methods/#operation/deletePeeringPhoneNumbers)
- [Add peering phone numbers](/docs/api/rest/reference/phone/methods/#operation/addPeeringPhoneNumbers)

### phone_recording:master

View and manage subaccounts' call recording information

**Associated APIs:**

- [Get user's recordings](/docs/api/rest/reference/phone/ma/#operation/phoneUserRecordings)
- [Download a phone recording transcript](/docs/api/rest/reference/phone/ma/#operation/phoneDownloadRecordingTranscript)
- [Get call recordings](/docs/api/rest/reference/phone/ma/#operation/getPhoneRecordings)
- [Get recording by call ID](/docs/api/rest/reference/phone/ma/#operation/getPhoneRecordingsByCallIdOrCallLogId)
- [Download a phone recording](/docs/api/rest/reference/phone/ma/#operation/phoneDownloadRecordingFile)

### phone_recording:read

View your call recording information

**Associated APIs:**

- [Get user's recordings](/docs/api/rest/reference/phone/methods/#operation/phoneUserRecordings)
- [Download a phone recording](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadRecordingFile)
- [Get recording by call ID](/docs/api/rest/reference/phone/methods/#operation/getPhoneRecordingsByCallIdOrCallLogId)
- [Download a phone recording transcript](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadRecordingTranscript)

### phone_recording:read:admin

View all users' recording information

**Associated APIs:**

- [Download a phone recording transcript](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadRecordingTranscript)
- [Get call recordings](/docs/api/rest/reference/phone/methods/#operation/getPhoneRecordings)
- [Get meeting recordings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingGet)
- [Download a phone recording](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadRecordingFile)
- [Get recording by call ID](/docs/api/rest/reference/phone/methods/#operation/getPhoneRecordingsByCallIdOrCallLogId)
- [Get user's recordings](/docs/api/rest/reference/phone/methods/#operation/phoneUserRecordings)

### phone_recording:write

View and manage your call recording information

**Associated APIs:**

- [Delete a call recording](/docs/api/rest/reference/phone/methods/#operation/deleteCallRecording)
- [Update Auto Delete Field](/docs/api/rest/reference/phone/methods/#operation/UpdateAutoDeleteField)
- [Update Recording Status](/docs/api/rest/reference/phone/methods/#operation/UpdateRecordingStatus)

### phone_recording:write:admin

View and manage all users' call recording information

**Associated APIs:**

- [Update Auto Delete Field](/docs/api/rest/reference/phone/methods/#operation/UpdateAutoDeleteField)
- [Delete a call recording](/docs/api/rest/reference/phone/methods/#operation/deleteCallRecording)
- [Update Recording Status](/docs/api/rest/reference/phone/methods/#operation/UpdateRecordingStatus)

### phone_sms:master

View and manage all sub accounts' Zoom Phone SMS information

**Associated APIs:**

- [Get user's SMS sessions](/docs/api/rest/reference/phone/ma/#operation/userSmsSession)
- [Get account's SMS sessions](/docs/api/rest/reference/phone/ma/#operation/accountSmsSession)
- [Get SMS by message ID](/docs/api/rest/reference/phone/ma/#operation/smsByMessageId)
- [Get SMS session details](/docs/api/rest/reference/phone/ma/#operation/smsSessionDetails)

### phone_sms:read

View your Zoom Phone SMS information

**Associated APIs:**

- [Get SMS by message ID](/docs/api/rest/reference/phone/methods/#operation/smsByMessageId)
- [Get user's SMS sessions](/docs/api/rest/reference/phone/methods/#operation/userSmsSession)
- [List user's SMS sessions in descending order](/docs/api/rest/reference/phone/methods/#operation/GetSmsSessions)
- [Sync SMS by session ID](/docs/api/rest/reference/phone/methods/#operation/smsSessionSync)
- [Get account's SMS sessions](/docs/api/rest/reference/phone/methods/#operation/accountSmsSession)
- [Get SMS session details](/docs/api/rest/reference/phone/methods/#operation/smsSessionDetails)

### phone_sms:read:admin

View all users' Zoom Phone SMS information

**Associated APIs:**

- [Get user's SMS sessions](/docs/api/rest/reference/phone/methods/#operation/userSmsSession)
- [Get account's SMS sessions](/docs/api/rest/reference/phone/methods/#operation/accountSmsSession)
- [Get SMS session details](/docs/api/rest/reference/phone/methods/#operation/smsSessionDetails)
- [Get SMS by message ID](/docs/api/rest/reference/phone/methods/#operation/smsByMessageId)
- [List user's SMS sessions in descending order](/docs/api/rest/reference/phone/methods/#operation/GetSmsSessions)
- [Sync SMS by session ID](/docs/api/rest/reference/phone/methods/#operation/smsSessionSync)

### phone_sms:write

View and manage your Zoom Phone SMS information

**Associated APIs:**

- [Post SMS message](/docs/api/rest/reference/phone/methods/#operation/postSmsMessage)

### phone_sms:write:admin

View and manage all users' Zoom Phone SMS information

**Associated APIs:**

- [Post SMS message](/docs/api/rest/reference/phone/methods/#operation/postSmsMessage)

### phone_voicemail:master

View and manage subaccounts' call voicemails

**Associated APIs:**

- [Download a phone voicemail](/docs/api/rest/reference/phone/ma/#operation/phoneDownloadVoicemailFile)
- [Delete a voicemail](/docs/api/rest/reference/phone/ma/#operation/deleteVoicemail)
- [Get user voicemail details from a call log](/docs/api/rest/reference/phone/ma/#operation/getVoicemailDetailsByCallIdOrCallLogId)
- [Get voicemail details](/docs/api/rest/reference/phone/ma/#operation/getVoicemailDetails)
- [Get account voicemails](/docs/api/rest/reference/phone/ma/#operation/accountVoiceMails)
- [Get user's voicemails](/docs/api/rest/reference/phone/ma/#operation/phoneUserVoiceMails)

### phone_voicemail:read

View your call voicemail information

**Associated APIs:**

- [Get voicemail details](/docs/api/rest/reference/phone/methods/#operation/getVoicemailDetails)
- [Get user voicemail details from a call log](/docs/api/rest/reference/phone/methods/#operation/getVoicemailDetailsByCallIdOrCallLogId)
- [Get user's voicemails](/docs/api/rest/reference/phone/methods/#operation/phoneUserVoiceMails)
- [Download a phone voicemail](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadVoicemailFile)

### phone_voicemail:read:admin

View all users' call voicemail information

**Associated APIs:**

- [Get account voicemails](/docs/api/rest/reference/phone/methods/#operation/accountVoiceMails)
- [Download a phone voicemail](/docs/api/rest/reference/phone/methods/#operation/phoneDownloadVoicemailFile)
- [Get voicemail details](/docs/api/rest/reference/phone/methods/#operation/getVoicemailDetails)
- [Get user's voicemails](/docs/api/rest/reference/phone/methods/#operation/phoneUserVoiceMails)
- [Get user voicemail details from a call log](/docs/api/rest/reference/phone/methods/#operation/getVoicemailDetailsByCallIdOrCallLogId)

### phone_voicemail:write

View and manage your call voicemail information

**Associated APIs:**

- [Delete a voicemail](/docs/api/rest/reference/phone/methods/#operation/deleteVoicemail)
- [Update Voicemail Read Status](/docs/api/rest/reference/phone/methods/#operation/updateVoicemailReadStatus)

### phone_voicemail:write:admin

View and manage all users' call voicemail information

**Associated APIs:**

- [Delete a voicemail](/docs/api/rest/reference/phone/methods/#operation/deleteVoicemail)
- [Update Voicemail Read Status](/docs/api/rest/reference/phone/methods/#operation/updateVoicemailReadStatus)

## QualityManagement

### qm_evaluations:read

Read evaluations

### qm_evaluations:read:admin

Read evaluations

### qm_interactions:read

View interactions

### qm_interactions:read:admin

View interactions

## Recording

### recording:master

View and manage sub account's user recordings

**Associated APIs:**

- [List all recordings](/docs/api/rest/reference/zoom-api/ma/#operation/recordingsList)
- [List archived files](/docs/api/rest/reference/zoom-api/ma/#operation/listArchivedFiles)
- [List an account's recordings](/docs/api/rest/reference/zoom-api/ma/#operation/ListRecordingsOfAnAccount)
- [Delete a recording file for a meeting or webinar](/docs/api/rest/reference/zoom-api/ma/#operation/recordingDeleteOne)
- [Recover meeting recordings](/docs/api/rest/reference/zoom-api/ma/#operation/recordingStatusUpdate)
- [Update registration questions](/docs/api/rest/reference/zoom-api/ma/#operation/recordingRegistrantQuestionUpdate)
- [Create a recording registrant](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRecordingRegistrantCreate)
- [Recover a single recording](/docs/api/rest/reference/zoom-api/ma/#operation/recordingStatusUpdateOne)
- [Get meeting recording settings](/docs/api/rest/reference/zoom-api/ma/#operation/recordingSettingUpdate)
- [Delete meeting or webinar recordings](/docs/api/rest/reference/zoom-api/ma/#operation/recordingDelete)
- [Update a registrant's status](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRecordingRegistrantStatus)
- [Update meeting recording settings](/docs/api/rest/reference/zoom-api/ma/#operation/recordingSettingsUpdate)
- [Get meeting recordings](/docs/api/rest/reference/zoom-api/ma/#operation/recordingGet)
- [List recording registrants](/docs/api/rest/reference/zoom-api/ma/#operation/meetingRecordingRegistrants)
- [Get registration questions](/docs/api/rest/reference/zoom-api/ma/#operation/recordingRegistrantsQuestionsGet)

### recording:read

View your recordings

**Associated APIs:**

- [Get a meeting transcript](/docs/api/rest/reference/zoom-api/methods/#operation/GetMeetingTranscript)
- [Get meeting recordings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingGet)
- [Get registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/recordingRegistrantsQuestionsGet)
- [List recording registrants](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRecordingRegistrants)
- [List all recordings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingsList)
- [Get a meeting's archived files](/docs/api/rest/reference/zoom-api/methods/#operation/getArchivedFiles)
- [Get meeting recording settings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingSettingUpdate)

### recording:read:admin

View all user recordings

**Associated APIs:**

- [Get a meeting transcript](/docs/api/rest/reference/zoom-api/methods/#operation/GetMeetingTranscript)
- [List recording registrants](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRecordingRegistrants)
- [Get meeting recording settings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingSettingUpdate)
- [List all recordings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingsList)
- [List archived files](/docs/api/rest/reference/zoom-api/methods/#operation/listArchivedFiles)
- [Get registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/recordingRegistrantsQuestionsGet)
- [Get archived file statistics](/docs/api/rest/reference/zoom-api/methods/#operation/getArchivedFileStatistics)

### recording:write

View and manage your recordings

**Associated APIs:**

- [Create a recording registrant](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRecordingRegistrantCreate)
- [Update a registrant's status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRecordingRegistrantStatus)
- [Delete a recording file for a meeting or webinar](/docs/api/rest/reference/zoom-api/methods/#operation/recordingDeleteOne)
- [Update an archived file's auto-delete status](/docs/api/rest/reference/zoom-api/methods/#operation/updateArchivedFile)
- [Recover meeting recordings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingStatusUpdate)
- [Update meeting recording settings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingSettingsUpdate)
- [Delete a meeting or webinar transcript](/docs/api/rest/reference/zoom-api/methods/#operation/DeleteMeetingTranscript)
- [Recover a single recording](/docs/api/rest/reference/zoom-api/methods/#operation/recordingStatusUpdateOne)
- [Get a meeting transcript](/docs/api/rest/reference/zoom-api/methods/#operation/GetMeetingTranscript)
- [Delete meeting or webinar recordings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingDelete)
- [Update registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/recordingRegistrantQuestionUpdate)

### recording:write:admin

View and manage all user recordings

**Associated APIs:**

- [Recover a single recording](/docs/api/rest/reference/zoom-api/methods/#operation/recordingStatusUpdateOne)
- [Delete meeting or webinar recordings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingDelete)
- [Update an archived file's auto-delete status](/docs/api/rest/reference/zoom-api/methods/#operation/updateArchivedFile)
- [Update registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/recordingRegistrantQuestionUpdate)
- [Create a recording registrant](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRecordingRegistrantCreate)
- [Update meeting recording settings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingSettingsUpdate)
- [Delete a meeting's archived files](/docs/api/rest/reference/zoom-api/methods/#operation/deleteArchivedFiles)
- [Update a registrant's status](/docs/api/rest/reference/zoom-api/methods/#operation/meetingRecordingRegistrantStatus)
- [Delete a recording file for a meeting or webinar](/docs/api/rest/reference/zoom-api/methods/#operation/recordingDeleteOne)
- [Recover meeting recordings](/docs/api/rest/reference/zoom-api/methods/#operation/recordingStatusUpdate)
- [Get a meeting transcript](/docs/api/rest/reference/zoom-api/methods/#operation/GetMeetingTranscript)
- [Delete a meeting or webinar transcript](/docs/api/rest/reference/zoom-api/methods/#operation/DeleteMeetingTranscript)

## Report

### report:master

View sub account's report data

**Associated APIs:**

- [Get webinar participant reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportWebinarParticipants)
- [Get meeting reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetings)
- [Get webinar Q&A report](/docs/api/rest/reference/zoom-api/ma/#operation/reportWebinarQA)
- [Get telephone reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportTelephone)
- [Get operation logs report](/docs/api/rest/reference/zoom-api/ma/#operation/reportOperationLogs)
- [Get remote support report](/docs/api/rest/reference/zoom-api/ma/#operation/Getremotesupportreport)
- [Get sign In / sign out activity report](/docs/api/rest/reference/zoom-api/ma/#operation/reportSignInSignOutActivities)
- [Get webinar poll reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportWebinarPolls)
- [Get upcoming events reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportUpcomingEvents)
- [Get a meeting activities report](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetingactivitylogs)
- [Get cloud recording usage report](/docs/api/rest/reference/zoom-api/ma/#operation/reportCloudRecording)
- [Get meeting Q&A report](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetingQA)
- [Get daily usage report](/docs/api/rest/reference/zoom-api/ma/#operation/reportDaily)
- [Get webinar detail reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportWebinarDetails)
- [Get billing invoice reports](/docs/api/rest/reference/zoom-api/ma/#operation/getBillingInvoicesReports)
- [Get meeting poll reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetingPolls)
- [Get meeting participant reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetingParticipants)
- [Get history meeting and webinar list](/docs/api/rest/reference/zoom-api/ma/#operation/Gethistorymeetingandwebinarlist)
- [Get billing reports](/docs/api/rest/reference/zoom-api/ma/#operation/getBillingReport)
- [Get meeting survey report](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetingSurvey)
- [Get meeting detail reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportMeetingDetails)
- [Get active or inactive host reports](/docs/api/rest/reference/zoom-api/ma/#operation/reportUsers)

### report:read:admin

View report data

**Associated APIs:**

- [Get upcoming events reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportUpcomingEvents)
- [Get meeting detail reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetingDetails)
- [Get sign In / sign out activity report](/docs/api/rest/reference/zoom-api/methods/#operation/reportSignInSignOutActivities)
- [Get remote support report](/docs/api/rest/reference/zoom-api/methods/#operation/Getremotesupportreport)
- [Get billing reports](/docs/api/rest/reference/zoom-api/methods/#operation/getBillingReport)
- [Get meeting survey report](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetingSurvey)
- [Get daily usage report](/docs/api/rest/reference/zoom-api/methods/#operation/reportDaily)
- [Get billing invoice reports](/docs/api/rest/reference/zoom-api/methods/#operation/getBillingInvoicesReports)
- [Get webinar Q&A report](/docs/api/rest/reference/zoom-api/methods/#operation/reportWebinarQA)
- [Get active or inactive host reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportUsers)
- [Get meeting participant reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetingParticipants)
- [Get meeting poll reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetingPolls)
- [Get webinar survey report](/docs/api/rest/reference/zoom-api/methods/#operation/reportWebinarSurvey)
- [Get webinar detail reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportWebinarDetails)
- [Get telephone reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportTelephone)
- [Get history meeting and webinar list](/docs/api/rest/reference/zoom-api/methods/#operation/Gethistorymeetingandwebinarlist)
- [Get meeting Q&A report](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetingQA)
- [Get webinar participant reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportWebinarParticipants)
- [Get cloud recording usage report](/docs/api/rest/reference/zoom-api/methods/#operation/reportCloudRecording)
- [Get meeting reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetings)
- [Get webinar poll reports](/docs/api/rest/reference/zoom-api/methods/#operation/reportWebinarPolls)
- [Get a meeting activities report](/docs/api/rest/reference/zoom-api/methods/#operation/reportMeetingactivitylogs)
- [Get operation logs report](/docs/api/rest/reference/zoom-api/methods/#operation/reportOperationLogs)

### report_chat:read:admin

View your team chat history report

**Associated APIs:**

- [Get chat message reports](/docs/api/rest/reference/chat/methods/#operation/reportChatMessages)
- [Get chat sessions reports](/docs/api/rest/reference/chat/methods/#operation/reportChatSessions)

### zva_report:read:admin

View zva engagements

**Associated APIs:**

- [Get ZVA transcripts](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVATranscripts)
- [Get ZVA variable details](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVAengagementvariabledetails)
- [Get ZVA query details](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVAQueryDetails)
- [Get ZVA Surveys](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVASurveys)
- [Get ZVA engagements](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVAEngagements)

## Role

### role:master

View and manage sub account user roles

**Associated APIs:**

- [Assign a role](/docs/api/rest/reference/account/ma/#operation/AddRoleMembers)
- [Get role information](/docs/api/rest/reference/account/ma/#operation/getRoleInformation)
- [Create a role](/docs/api/rest/reference/account/ma/#operation/createRole)
- [Update role information](/docs/api/rest/reference/account/ma/#operation/updateRole)
- [List members in a role](/docs/api/rest/reference/account/ma/#operation/roleMembers)
- [List roles](/docs/api/rest/reference/account/ma/#operation/roles)
- [Unassign a role](/docs/api/rest/reference/account/ma/#operation/roleMemberDelete)
- [Delete a role](/docs/api/rest/reference/account/ma/#operation/deleteRole)

### role:read:admin

View all user roles

**Associated APIs:**

- [List members in a role](/docs/api/rest/reference/account/methods/#operation/roleMembers)
- [List roles](/docs/api/rest/reference/account/methods/#operation/roles)
- [Get role information](/docs/api/rest/reference/account/methods/#operation/getRoleInformation)

### role:write:admin

View and manage all user roles

**Associated APIs:**

- [List roles](/docs/api/rest/reference/account/methods/#operation/roles)
- [Update role information](/docs/api/rest/reference/account/methods/#operation/updateRole)
- [Delete a role](/docs/api/rest/reference/account/methods/#operation/deleteRole)
- [Unassign a role](/docs/api/rest/reference/account/methods/#operation/roleMemberDelete)
- [Assign a role](/docs/api/rest/reference/account/methods/#operation/AddRoleMembers)
- [Get role information](/docs/api/rest/reference/account/methods/#operation/getRoleInformation)
- [Create a role](/docs/api/rest/reference/account/methods/#operation/createRole)
- [List members in a role](/docs/api/rest/reference/account/methods/#operation/roleMembers)

## Room

### room:master

View and manage sub account's Zoom Rooms information

**Associated APIs:**

- [Get Digital Signage content folder](/docs/api/rest/reference/zoom-rooms/ma/#operation/Getdigitalsignagecontentfolderdetails)
- [Get device information](/docs/api/rest/reference/zoom-rooms/ma/#operation/getRoomDevices)
- [Change a Zoom Room's location](/docs/api/rest/reference/zoom-rooms/ma/#operation/changeZRLocation)
- [List Digital Signage library playlists](/docs/api/rest/reference/zoom-rooms/ma/#operation/ListDigitalSignagelibraryplaylists)
- [Create a device profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/createRoomDeviceProfile)
- [Get Digital Signage library playlist content items](/docs/api/rest/reference/zoom-rooms/ma/#operation/GetDigitalSignagelibraryplaylistcontentitems)
- [Get Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/ma/#operation/GetDigitalSignagelibraryplaylist)
- [Get Zoom Room location profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRLocationProfile)
- [Update Zoom Room location profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateZRLocationProfile)
- [Get Zoom Room account profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRAccountProfile)
- [Delete a location](/docs/api/rest/reference/zoom-rooms/ma/#operation/deleteAZRLocation)
- [Get Digital Signage content item](/docs/api/rest/reference/zoom-rooms/ma/#operation/Getdigitalsignagecontentitem)
- [Get Zoom Room settings](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRSettings)
- [Delete a device profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/deleteRoomProfile)
- [List digital signage contents](/docs/api/rest/reference/zoom-rooms/ma/#operation/listDigitalSignageContent)
- [Get Zoom Rooms virtual controller URL](/docs/api/rest/reference/zoom-rooms/ma/#operation/getWebzrcUrl)
- [Add a digital signage URL](/docs/api/rest/reference/zoom-rooms/ma/#operation/AddadigitalsignageURL)
- [Get location settings](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRLocationSettings)
- [List Zoom Rooms](/docs/api/rest/reference/zoom-rooms/ma/#operation/listZoomRooms)
- [List Digital Signage content items](/docs/api/rest/reference/zoom-rooms/ma/#operation/GETListdigitalsignagecontentitems)
- [Update Zoom Room account profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateZRAccProfile)
- [Use Zoom Room controls](/docs/api/rest/reference/zoom-rooms/ma/#operation/ZoomRoomsControls)
- [List device profiles](/docs/api/rest/reference/zoom-rooms/ma/#operation/getRoomProfiles)
- [Update Zoom Room account settings](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateZoomRoomAccSettings)
- [Update Digital Signage library playlist content items](/docs/api/rest/reference/zoom-rooms/ma/#operation/UpdateDigitalSignagelibraryplaylistcontentitems)
- [Get Zoom Room location structure](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRLocationStructure)
- [Update location settings](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateZRLocationSettings)
- [Change Zoom Rooms app version](/docs/api/rest/reference/zoom-rooms/ma/#operation/changeZoomRoomsAppVersion)
- [Delete a Digital Signage content folder](/docs/api/rest/reference/zoom-rooms/ma/#operation/Deleteadigitalsignagecontentfolder)
- [Change the assigned parent location](/docs/api/rest/reference/zoom-rooms/ma/#operation/changeParentLocation)
- [Add a location](/docs/api/rest/reference/zoom-rooms/ma/#operation/addAZRLocation)
- [Update a digital signage content folder](/docs/api/rest/reference/zoom-rooms/ma/#operation/Updateadigitalsignagecontentfolder)
- [Update E911 digital signage](/docs/api/rest/reference/zoom-rooms/ma/#operation/manageE911signage)
- [Add a digital signage content folder](/docs/api/rest/reference/zoom-rooms/ma/#operation/Addadigitalsignagecontentfolder)
- [Add a Zoom Room](/docs/api/rest/reference/zoom-rooms/ma/#operation/addARoom)
- [Add a Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/ma/#operation/AddaDigitalSignagelibraryplaylist)
- [Config Zoom Room Controller Apps](/docs/api/rest/reference/zoom-rooms/methods/#operation/ConfigZoomRoomControllerApps)
- [Delete Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/ma/#operation/DeleteDigitalSignagelibraryplaylist)
- [Delete a Digital Signage content item](/docs/api/rest/reference/zoom-rooms/ma/#operation/Deleteadigitalsignagecontentitem)
- [Delete a Zoom Room](/docs/api/rest/reference/zoom-rooms/ma/#operation/deleteAZoomRoom)
- [Update Zoom Room settings](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateZRSettings)
- [Update Zoom Rooms location structure](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateZoomRoomsLocationStructure)
- [List Zoom Room locations](/docs/api/rest/reference/zoom-rooms/ma/#operation/listZRLocations)
- [Get Zoom Room account settings](/docs/api/rest/reference/zoom-rooms/ma/#operation/getZRAccountSettings)
- [Update a device profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/updateDeviceProfile)
- [Update a Digital Signage content item attributes](/docs/api/rest/reference/zoom-rooms/ma/#operation/Updateadigitalsignagecontentitemattributes)
- [Get a device profile](/docs/api/rest/reference/zoom-rooms/ma/#operation/getRoomProfile)
- [Update a Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/ma/#operation/UpdateaDigitalSignagelibraryplaylist)
- [List Zoom Room devices](/docs/api/rest/reference/zoom-rooms/ma/#operation/listZRDevices)

### room:read:admin

View all users' Zoom Rooms information

**Associated APIs:**

- [Get Digital Signage content folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getdigitalsignagecontentfolderdetails)
- [Get device information](/docs/api/rest/reference/zoom-rooms/methods/#operation/getRoomDevices)
- [List released workspaces by timeout](/docs/api/rest/reference/zoom-rooms/methods/#operation/getWorksapceReservationReleaseInof)
- [Get Zoom Rooms virtual controller URL](/docs/api/rest/reference/zoom-rooms/methods/#operation/getWebzrcUrl)
- [List digital signage contents](/docs/api/rest/reference/zoom-rooms/methods/#operation/listDigitalSignageContent)
- [Get Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/methods/#operation/GetDigitalSignagelibraryplaylist)
- [List Digital Signage library playlists](/docs/api/rest/reference/zoom-rooms/methods/#operation/ListDigitalSignagelibraryplaylists)
- [Get Zoom Room account profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRAccountProfile)
- [Get Digital Signage content item](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getdigitalsignagecontentitem)
- [List Zoom Rooms background image library contents](/docs/api/rest/reference/zoom-rooms/methods/#operation/ListZoomRoomsbackgroundimagelibrarycontents)
- [Get Zoom Room settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRSettings)
- [Get Digital Signage library playlist content items](/docs/api/rest/reference/zoom-rooms/methods/#operation/GetDigitalSignagelibraryplaylistcontentitems)
- [List Zoom Room devices](/docs/api/rest/reference/zoom-rooms/methods/#operation/listZRDevices)
- [Get Zoom Room account settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRAccountSettings)
- [Get Zoom Room sensor data](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRSensorData)
- [Get Zoom Rooms background image library content](/docs/api/rest/reference/zoom-rooms/methods/#operation/GetZoomRoomsBackgroundImageLibraryContent)
- [Get a device profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/getRoomProfile)
- [Get a calendar resource by ID](/docs/api/rest/reference/zoom-rooms/methods/#operation/getCalendarResourceById)
- [List Digital Signage library playlist published rooms](/docs/api/rest/reference/zoom-rooms/methods/#operation/ListDigitalSignagelibraryplaylistpublishedrooms)
- [List all Zoom Room Tags](/docs/api/rest/reference/zoom-rooms/methods/#operation/listZoomRoomTags)
- [List device profiles](/docs/api/rest/reference/zoom-rooms/methods/#operation/getRoomProfiles)
- [List default Zoom Rooms background image library contents](/docs/api/rest/reference/zoom-rooms/methods/#operation/ListDefaultZoomRoomsBackgroundImageLibrarycontents)
- [Get Zoom Room profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRProfile)
- [List Zoom Room locations](/docs/api/rest/reference/zoom-rooms/methods/#operation/listZRLocations)
- [List calendar services](/docs/api/rest/reference/zoom-rooms/methods/#operation/getCalendarServices)
- [Get Zoom Rooms Background Image Library Folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/GetZoomRoomsBackgroundLibraryFolder)
- [List Zoom Rooms Background Image Library Folders](/docs/api/rest/reference/zoom-rooms/methods/#operation/ListZoomRoomsBackgroundLibraryFolders)
- [List Zoom Rooms](/docs/api/rest/reference/zoom-rooms/methods/#operation/listZoomRooms)
- [List Digital Signage content items](/docs/api/rest/reference/zoom-rooms/methods/#operation/GETListdigitalsignagecontentitems)
- [List calendar resources by calendar service](/docs/api/rest/reference/zoom-rooms/methods/#operation/getCalendarResourcesByServiceId)
- [Get Zoom Room location structure](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRLocationStructure)
- [Get Zoom Room location profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRLocationProfile)
- [Get location settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/getZRLocationSettings)

### room:write:admin

View and manage all users' Zoom Rooms information

**Associated APIs:**

- [Delete a Digital Signage content item](/docs/api/rest/reference/zoom-rooms/methods/#operation/Deleteadigitalsignagecontentitem)
- [Delete a Zoom Room](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteAZoomRoom)
- [Update Zoom Room account profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateZRAccProfile)
- [Delete a calendar service](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteACalendarService)
- [Update location settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateZRLocationSettings)
- [Change Zoom Rooms app version](/docs/api/rest/reference/zoom-rooms/methods/#operation/changeZoomRoomsAppVersion)
- [Update a Zoom Room profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateRoomProfile)
- [Add a calendar resource to a calendar service](/docs/api/rest/reference/zoom-rooms/methods/#operation/addACalendarResourceToCalendarService)
- [Update Digital Signage library playlist published rooms](/docs/api/rest/reference/zoom-rooms/methods/#operation/UpdateDigitalSignagelibraryplaylistpublishedrooms)
- [Add a digital signage content folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/Addadigitalsignagecontentfolder)
- [Add a Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/methods/#operation/AddaDigitalSignagelibraryplaylist)
- [Delete Zoom Rooms Background Image Library Content](/docs/api/rest/reference/zoom-rooms/methods/#operation/DeleteZoomRoomsBackgroundImageLibraryContent)
- [Un-assign Tags from a Zoom Room](/docs/api/rest/reference/zoom-rooms/methods/#operation/unassignZoomRoomTag)
- [Config Zoom Room Controller Apps](/docs/api/rest/reference/zoom-rooms/methods/#operation/ConfigZoomRoomControllerApps)
- [Delete Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/methods/#operation/DeleteDigitalSignagelibraryplaylist)
- [Add a digital signage URL](/docs/api/rest/reference/zoom-rooms/methods/#operation/AddadigitalsignageURL)
- [Update Zoom Room settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateZRSettings)
- [Update Zoom Rooms location structure](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateZoomRoomsLocationStructure)
- [Update Digital Signage library playlist content items](/docs/api/rest/reference/zoom-rooms/methods/#operation/UpdateDigitalSignagelibraryplaylistcontentitems)
- [Start calendar service sync process](/docs/api/rest/reference/zoom-rooms/methods/#operation/syncACalendarService)
- [Create a new Zoom Rooms Tag](/docs/api/rest/reference/zoom-rooms/methods/#operation/createZoomRoomTag)
- [Create a device profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/createRoomDeviceProfile)
- [Delete Zoom Rooms Background Image Library Folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/DeleteZoomRoomsBackgroundLibraryFolder)
- [Delete a Digital Signage content folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/Deleteadigitalsignagecontentfolder)
- [Change a Zoom Room's location](/docs/api/rest/reference/zoom-rooms/methods/#operation/changeZRLocation)
- [Update Zoom Room account settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateZoomRoomAccSettings)
- [Delete a calendar resource](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteACalendarResource)
- [Update a Digital Signage image or video file](/docs/api/rest/reference/zoom-rooms/methods/#operation/Updateadigitalsignageimageorvideofile)
- [Add a Zoom Room](/docs/api/rest/reference/zoom-rooms/methods/#operation/addARoom)
- [Add a digital signage image or video](/docs/api/rest/reference/zoom-rooms/methods/#operation/Adddigitalsignageimageorvideo)
- [Use Zoom Room controls](/docs/api/rest/reference/zoom-rooms/methods/#operation/ZoomRoomsControls)
- [Update a digital signage content folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/Updateadigitalsignagecontentfolder)
- [Update a Digital Signage content item attributes](/docs/api/rest/reference/zoom-rooms/methods/#operation/Updateadigitalsignagecontentitemattributes)
- [Add a location](/docs/api/rest/reference/zoom-rooms/methods/#operation/addAZRLocation)
- [Update E911 digital signage](/docs/api/rest/reference/zoom-rooms/methods/#operation/manageE911signage)
- [Delete a Zoom Room user device](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteDevice)
- [Assign Tags to Zoom Rooms By Location ID](/docs/api/rest/reference/zoom-rooms/methods/#operation/AssignTagsToZoomRoomsByLocationID)
- [Delete a device profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteRoomProfile)
- [Delete a location](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteAZRLocation)
- [Delete Tag](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteZoomRoomTag)
- [Update a device profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateDeviceProfile)
- [Get a device profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/getRoomProfile)
- [Update Zoom Rooms background image library content](/docs/api/rest/reference/zoom-rooms/methods/#operation/UpdateZoomRoomsBackgroundImageLibraryContent)
- [Update a Digital Signage library playlist](/docs/api/rest/reference/zoom-rooms/methods/#operation/UpdateaDigitalSignagelibraryplaylist)
- [Edit Tag](/docs/api/rest/reference/zoom-rooms/methods/#operation/editZoomRoomTag)
- [Update Zoom Room location profile](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateZRLocationProfile)
- [Add Zoom Rooms Background Image Library Folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/AddZoomRoomsBackgroundLibraryFolder)
- [Change the assigned parent location](/docs/api/rest/reference/zoom-rooms/methods/#operation/changeParentLocation)
- [Assign Tags to a Zoom Room](/docs/api/rest/reference/zoom-rooms/methods/#operation/AssignTagsToAZoomRoom)
- [Update Zoom Rooms Background Image Library Folder](/docs/api/rest/reference/zoom-rooms/methods/#operation/UpdateaZoomRoomsBackgroundLibraryFolderName)
- [Add Zoom Rooms background image library content](/docs/api/rest/reference/zoom-rooms/methods/#operation/AddZoomRoomsBackgroundImageLibraryContent)

## Rooms Web

### room:read:master

View sub account's Zoom Rooms information

**Associated APIs:**

- [List Digital Signage library playlist published rooms](/docs/api/rest/reference/zoom-rooms/ma/#operation/ListDigitalSignagelibraryplaylistpublishedrooms)

### room:write:master

Manage sub account's Zoom Rooms information

**Associated APIs:**

- [Update Digital Signage library playlist published rooms](/docs/api/rest/reference/zoom-rooms/ma/#operation/UpdateDigitalSignagelibraryplaylistpublishedrooms)
- [Add a digital signage image or video](/docs/api/rest/reference/zoom-rooms/ma/#operation/Adddigitalsignageimageorvideo)
- [Delete a Digital Signage content item](/docs/api/rest/reference/zoom-rooms/methods/#operation/Deleteadigitalsignagecontentitem)
- [Update a Digital Signage image or video file](/docs/api/rest/reference/zoom-rooms/ma/#operation/Updateadigitalsignageimageorvideofile)

## SCIM2

### scim2

Call Zoom SCIM2 API

**Associated APIs:**

- [Get a user](/docs/api/rest/reference/scim-api/methods/#operation/userSCIM2Get)
- [List users](/docs/api/rest/reference/scim-api/methods/#operation/userSCIM2List)
- [List groups](/docs/api/rest/reference/scim-api/methods/#operation/groupSCIM2List)
- [Delete a group](/docs/api/rest/reference/scim-api/methods/#operation/groupSCIM2Delete)
- [Create a group](/docs/api/rest/reference/scim-api/methods/#operation/groupScim2Create)
- [Update a group](/docs/api/rest/reference/scim-api/methods/#operation/groupSCIM2Update)
- [Deactivate a user](/docs/api/rest/reference/scim-api/methods/#operation/userADSCIM2Deactivate)
- [Get a group](/docs/api/rest/reference/scim-api/methods/#operation/groupSCIM2Get)
- [Update a user](/docs/api/rest/reference/scim-api/methods/#operation/userSCIM2Update)
- [Create a user](/docs/api/rest/reference/scim-api/methods/#operation/userScim2Create)
- [Delete a user](/docs/api/rest/reference/scim-api/methods/#operation/userSCIM2Delete)

## SIP

### sip_phone:master

View and manage sub account's SIP phone information

**Associated APIs:**

- [Delete SIP phone](/docs/api/rest/reference/zoom-api/ma/#operation/deleteSIPPhonePhones)
- [Enable SIP phone](/docs/api/rest/reference/zoom-api/ma/#operation/EnableSIPPhonePhones)
- [Update SIP phone](/docs/api/rest/reference/zoom-api/ma/#operation/UpdateSIPPhonePhones)
- [List SIP phones](/docs/api/rest/reference/zoom-api/ma/#operation/ListSIPPhonePhones)

### sip_phone:read:admin

View all users' SIP phone information

**Associated APIs:**

- [List SIP phones](/docs/api/rest/reference/zoom-api/methods/#operation/ListSIPPhonePhones)

### sip_phone:write:admin

View and manage all users' SIP phone information

**Associated APIs:**

- [Delete SIP phone](/docs/api/rest/reference/zoom-api/methods/#operation/deleteSIPPhonePhones)
- [Update SIP phone](/docs/api/rest/reference/zoom-api/methods/#operation/UpdateSIPPhonePhones)
- [Enable SIP phone](/docs/api/rest/reference/zoom-api/methods/#operation/EnableSIPPhonePhones)

### sip_trunk:master

View and manage sub account's SIP trunk information

**Associated APIs:**

- [Delete a SIP trunk](/docs/api/rest/reference/zoom-api/ma/#operation/DeleteASIPTrunk)
- [Delete all numbers](/docs/api/rest/reference/zoom-api/ma/#operation/DeleteAllNumbers)
- [Update an internal number](/docs/api/rest/reference/zoom-api/ma/#operation/UpdateAnInternalNumber)
- [Assign SIP trunk configuration](/docs/api/rest/reference/zoom-api/ma/#operation/AssignSIPTrunkConfiguration)
- [Get SIP trunk configuration](/docs/api/rest/reference/zoom-api/ma/#operation/GetSIPTrunkConfiguration)
- [Assign numbers](/docs/api/rest/reference/zoom-api/ma/#operation/AssignNumbers)
- [Delete internal call-out country](/docs/api/rest/reference/zoom-api/ma/#operation/DeleteInternalCall-outCountry)
- [Add internal numbers](/docs/api/rest/reference/zoom-api/ma/#operation/AddInternalNumbers)
- [Delete an internal number](/docs/api/rest/reference/zoom-api/ma/#operation/DeleteAnInternalNumber)
- [List SIP trunks](/docs/api/rest/reference/zoom-api/ma/#operation/ListSIPTrunks)
- [Add internal call-out countries](/docs/api/rest/reference/zoom-api/ma/#operation/AddInternalCall-outCountries)
- [Assign SIP trunks](/docs/api/rest/reference/zoom-api/ma/#operation/AssignSIPTrunks)
- [List SIP trunk numbers](/docs/api/rest/reference/zoom-api/ma/#operation/listSipTrunkNumbers)
- [List internal numbers](/docs/api/rest/reference/zoom-api/ma/#operation/ListInternalNumbers)
- [List internal call-out countries](/docs/api/rest/reference/zoom-api/ma/#operation/ListInternalCall-outCountries)

## SMS

### contact_center_sms:write:admin

send sms

**Associated APIs:**

- [Send an SMS](/docs/api/rest/reference/contact-center/methods/#operation/contactCenterSMS)

## Scheduler

### scheduler:read

View scheduler

**Associated APIs:**

- [List schedules](/docs/api/rest/reference/phone/methods/#operation/list_schedules)
- [List scheduled events](/docs/api/rest/reference/phone/methods/#operation/list_scheduled_events)
- [get routing response](/docs/api/rest/reference/phone/methods/#operation/Getroutingresponse)
- [List availability](/docs/api/rest/reference/phone/methods/#operation/list_availability)
- [Get scheduled event attendee](/docs/api/rest/reference/phone/methods/#operation/get_scheduled_event_attendee)
- [Report analytics](/docs/api/rest/reference/phone/methods/#operation/report_analytics)
- [List team](/docs/api/rest/reference/phone/methods/#operation/Listteam)
- [Get user](/docs/api/rest/reference/phone/methods/#operation/get_user)
- [Get availability](/docs/api/rest/reference/phone/methods/#operation/get_availability)
- [Get schedules](/docs/api/rest/reference/phone/methods/#operation/get_schedule)
- [Get scheduled events](/docs/api/rest/reference/phone/methods/#operation/get_scheduled_events)

### scheduler:read:admin

View scheduler

**Associated APIs:**

- [Get availability](/docs/api/rest/reference/phone/methods/#operation/get_availability)
- [Get scheduled event attendee](/docs/api/rest/reference/phone/methods/#operation/get_scheduled_event_attendee)
- [List team](/docs/api/rest/reference/phone/methods/#operation/Listteam)
- [Get schedules](/docs/api/rest/reference/phone/methods/#operation/get_schedule)
- [Get user](/docs/api/rest/reference/phone/methods/#operation/get_user)
- [Get scheduled events](/docs/api/rest/reference/phone/methods/#operation/get_scheduled_events)
- [List schedules](/docs/api/rest/reference/phone/methods/#operation/list_schedules)
- [List scheduled events](/docs/api/rest/reference/phone/methods/#operation/list_scheduled_events)
- [Report analytics](/docs/api/rest/reference/phone/methods/#operation/report_analytics)
- [get routing response](/docs/api/rest/reference/phone/methods/#operation/Getroutingresponse)
- [List availability](/docs/api/rest/reference/phone/methods/#operation/list_availability)

### scheduler:write

Manage scheduler

**Associated APIs:**

- [Create shares](/docs/api/rest/reference/phone/methods/#operation/create_shares)
- [Delete scheduled events](/docs/api/rest/reference/phone/methods/#operation/delete_scheduled_events)
- [Patch schedules](/docs/api/rest/reference/phone/methods/#operation/patch_schedule)
- [Insert schedules](/docs/api/rest/reference/phone/methods/#operation/insert_schedule)
- [Patch scheduled events](/docs/api/rest/reference/phone/methods/#operation/patch_scheduled_events)
- [Patch availability](/docs/api/rest/reference/phone/methods/#operation/patch_availability)
- [Insert availability](/docs/api/rest/reference/phone/methods/#operation/insert_availability)
- [Delete schedules](/docs/api/rest/reference/phone/methods/#operation/delete_schedules)
- [Delete availability](/docs/api/rest/reference/phone/methods/#operation/delete_availability)
- [Single use link](/docs/api/rest/reference/phone/methods/#operation/single_use_link)

### scheduler:write:admin

Manage scheduler

**Associated APIs:**

- [Insert availability](/docs/api/rest/reference/phone/methods/#operation/insert_availability)
- [Patch availability](/docs/api/rest/reference/phone/methods/#operation/patch_availability)
- [Delete availability](/docs/api/rest/reference/phone/methods/#operation/delete_availability)
- [Delete scheduled events](/docs/api/rest/reference/phone/methods/#operation/delete_scheduled_events)
- [Single use link](/docs/api/rest/reference/phone/methods/#operation/single_use_link)
- [Delete schedules](/docs/api/rest/reference/phone/methods/#operation/delete_schedules)
- [Create shares](/docs/api/rest/reference/phone/methods/#operation/create_shares)
- [Insert schedules](/docs/api/rest/reference/phone/methods/#operation/insert_schedule)
- [Patch scheduled events](/docs/api/rest/reference/phone/methods/#operation/patch_scheduled_events)
- [Patch schedules](/docs/api/rest/reference/phone/methods/#operation/patch_schedule)

## Special

### app:deeplink:write

Generate an app deeplink

**Associated APIs:**

- [Generate an app deeplink](/docs/api/rest/reference/marketplace/methods/#operation/generateAppDeeplink)

### app:deeplink:write:admin

Generate an app deeplink

**Associated APIs:**

- [Generate an app deeplink](/docs/api/rest/reference/marketplace/methods/#operation/generateAppDeeplink)

## Special&ChatBot

### app:notification:read

View chat app notification

**Associated APIs:**

- [Send app notifications](/docs/api/rest/reference/marketplace/methods/#operation/Sendappnotifications)

### app:notification:write

View and Manage chat app notification

**Associated APIs:**

- [Send app notifications](/docs/api/rest/reference/marketplace/methods/#operation/Sendappnotifications)

## Survey Management

### survey:master

View survey information

**Associated APIs:**

- [Get survey info](/docs/api/rest/reference/account/ma/#operation/getSurveyInfo)
- [Get survey answers](/docs/api/rest/reference/account/ma/#operation/getSurveyAnswers)
- [Get survey instances](/docs/api/rest/reference/account/ma/#operation/getSurveyInstancesInfo)
- [Get surveys](/docs/api/rest/reference/account/ma/#operation/getAccountSurveys)

### survey:read:admin

View survey information

**Associated APIs:**

- [Get survey answers](/docs/api/rest/reference/account/methods/#operation/getSurveyAnswers)
- [Get survey info](/docs/api/rest/reference/account/methods/#operation/getSurveyInfo)
- [Get survey instances](/docs/api/rest/reference/account/methods/#operation/getSurveyInstancesInfo)
- [Get surveys](/docs/api/rest/reference/account/methods/#operation/getAccountSurveys)

## TSP

### tsp:master

View and manage sub account's TSP account info

**Associated APIs:**

- [Set global dial-in URL for a TSP user](/docs/api/rest/reference/zoom-api/ma/#operation/tspUrlUpdate)
- [Update a TSP account](/docs/api/rest/reference/zoom-api/ma/#operation/userTSPUpdate)
- [Delete a user's TSP account](/docs/api/rest/reference/zoom-api/ma/#operation/userTSPDelete)
- [Get account's TSP information](/docs/api/rest/reference/zoom-api/ma/#operation/tsp)
- [Get a user's TSP account](/docs/api/rest/reference/zoom-api/ma/#operation/userTSP)
- [List user's TSP accounts](/docs/api/rest/reference/zoom-api/ma/#operation/userTSPs)
- [Update an account's TSP information](/docs/api/rest/reference/zoom-api/ma/#operation/tspUpdate)
- [Add a user's TSP account](/docs/api/rest/reference/zoom-api/ma/#operation/userTSPCreate)

### tsp:read

View your TSP account info

**Associated APIs:**

- [List user's TSP accounts](/docs/api/rest/reference/zoom-api/methods/#operation/userTSPs)
- [Get a user's TSP account](/docs/api/rest/reference/zoom-api/methods/#operation/userTSP)

### tsp:read:admin

View TSP info

**Associated APIs:**

- [Get a user's TSP account](/docs/api/rest/reference/zoom-api/methods/#operation/userTSP)
- [List user's TSP accounts](/docs/api/rest/reference/zoom-api/methods/#operation/userTSPs)
- [Get account's TSP information](/docs/api/rest/reference/zoom-api/methods/#operation/tsp)

### tsp:write

View and manage your TSP account info

**Associated APIs:**

- [Delete a user's TSP account](/docs/api/rest/reference/zoom-api/methods/#operation/userTSPDelete)
- [Update a TSP account](/docs/api/rest/reference/zoom-api/methods/#operation/userTSPUpdate)
- [Add a user's TSP account](/docs/api/rest/reference/zoom-api/methods/#operation/userTSPCreate)
- [Set global dial-in URL for a TSP user](/docs/api/rest/reference/zoom-api/methods/#operation/tspUrlUpdate)

### tsp:write:admin

View and manage TSP info

**Associated APIs:**

- [Set global dial-in URL for a TSP user](/docs/api/rest/reference/zoom-api/methods/#operation/tspUrlUpdate)
- [Update an account's TSP information](/docs/api/rest/reference/zoom-api/methods/#operation/tspUpdate)
- [Delete a user's TSP account](/docs/api/rest/reference/zoom-api/methods/#operation/userTSPDelete)
- [Add a user's TSP account](/docs/api/rest/reference/zoom-api/methods/#operation/userTSPCreate)
- [Update a TSP account](/docs/api/rest/reference/zoom-api/methods/#operation/userTSPUpdate)

## Tasks

### tasks:delete

Delete user's task(s)

**Associated APIs:**

- [Delete a task](/docs/api/rest/reference/Tasks/methods/#operation/deleteTask)

### tasks:delete:admin

Delete account's task(s)

**Associated APIs:**

- [Delete a task](/docs/api/rest/reference/Tasks/methods/#operation/deleteTask)

### tasks:read

Get user’s task(s)

**Associated APIs:**

- [Get task details](/docs/api/rest/reference/Tasks/methods/#operation/getTaskDetail)
- [List tasks](/docs/api/rest/reference/Tasks/methods/#operation/getMyTasks)

### tasks:read:admin

Get account's task(s)

**Associated APIs:**

- [List tasks](/docs/api/rest/reference/Tasks/methods/#operation/getMyTasks)
- [Get task details](/docs/api/rest/reference/Tasks/methods/#operation/getTaskDetail)

### tasks:write

Update or trash tasks

**Associated APIs:**

- [Create a new task](/docs/api/rest/reference/Tasks/methods/#operation/createTask)
- [Update task fields](/docs/api/rest/reference/Tasks/methods/#operation/updateTask)

### tasks:write:admin

Management the account's task

**Associated APIs:**

- [Update task fields](/docs/api/rest/reference/Tasks/methods/#operation/updateTask)

### tasks_assignee:read

View task's assignee(s)

**Associated APIs:**

- [Get assignees of a task](/docs/api/rest/reference/Tasks/methods/#operation/GetAssigneesOfATask)

### tasks_assignee:read:admin

View account's task assignees

**Associated APIs:**

- [Get assignees of a task](/docs/api/rest/reference/Tasks/methods/#operation/GetAssigneesOfATask)

### tasks_assignee:write

Add or remove task's assignee

**Associated APIs:**

- [Add assignees to a task](/docs/api/rest/reference/Tasks/methods/#operation/addTasksAssignees)
- [Remove Assignee from task](/docs/api/rest/reference/Tasks/methods/#operation/removeTaskAssignee)

### tasks_assignee:write:admin

Add or update task's assignees

**Associated APIs:**

- [Remove Assignee from task](/docs/api/rest/reference/Tasks/methods/#operation/removeTaskAssignee)
- [Add assignees to a task](/docs/api/rest/reference/Tasks/methods/#operation/addTasksAssignees)

### tasks_collaborator:read

View user's task collaborator information

**Associated APIs:**

- [Get collaborators of a task](/docs/api/rest/reference/Tasks/methods/#operation/Getcollaboratorsofatask)

### tasks_collaborator:read:admin

View account's task collaborators

**Associated APIs:**

- [Get collaborators of a task](/docs/api/rest/reference/Tasks/methods/#operation/Getcollaboratorsofatask)

### tasks_collaborator:write

Add or update task's collaborator

**Associated APIs:**

- [Remove collaborator from task](/docs/api/rest/reference/Tasks/methods/#operation/removeTaskCollaborator)
- [Add collaborators to a task](/docs/api/rest/reference/Tasks/methods/#operation/addTasksCollaborators)

### tasks_collaborator:write:admin

View and update account's task collaborator information

**Associated APIs:**

- [Remove collaborator from task](/docs/api/rest/reference/Tasks/methods/#operation/removeTaskCollaborator)
- [Add collaborators to a task](/docs/api/rest/reference/Tasks/methods/#operation/addTasksCollaborators)

### tasks_comment:read

Read user's task comment

**Associated APIs:**

- [Get a task's comments](/docs/api/rest/reference/Tasks/methods/#operation/GetAV1TasksComment)

### tasks_comment:read:admin

View account's task comment

**Associated APIs:**

- [Get a task's comments](/docs/api/rest/reference/Tasks/methods/#operation/GetAV1TasksComment)

### tasks_comment:write

Manage and view the user's task comments

**Associated APIs:**

- [Add a comment to task](/docs/api/rest/reference/Tasks/methods/#operation/addComment)
- [Delete a task's comment](/docs/api/rest/reference/Tasks/methods/#operation/DeleteTaskComment)

### tasks_comment:write:admin

View and manage account's task comment.

**Associated APIs:**

- [Delete a task's comment](/docs/api/rest/reference/Tasks/methods/#operation/DeleteTaskComment)
- [Add a comment to task](/docs/api/rest/reference/Tasks/methods/#operation/addComment)

## TrackingField

### tracking_fields:master

View and manage sub account user tracking fields

**Associated APIs:**

- [Update a tracking field](/docs/api/rest/reference/zoom-api/ma/#operation/trackingfieldUpdate)
- [Get a tracking field](/docs/api/rest/reference/zoom-api/ma/#operation/trackingfieldGet)
- [Create a tracking field](/docs/api/rest/reference/zoom-api/ma/#operation/trackingfieldCreate)
- [List tracking fields](/docs/api/rest/reference/zoom-api/ma/#operation/trackingfieldList)
- [Delete a tracking field](/docs/api/rest/reference/zoom-api/ma/#operation/trackingfieldDelete)

### tracking_fields:read:admin

View all users' tracking fields

**Associated APIs:**

- [List tracking fields](/docs/api/rest/reference/zoom-api/methods/#operation/trackingfieldList)
- [Get a tracking field](/docs/api/rest/reference/zoom-api/methods/#operation/trackingfieldGet)

### tracking_fields:write:admin

View and manage all users' tracking fields

**Associated APIs:**

- [Create a tracking field](/docs/api/rest/reference/zoom-api/methods/#operation/trackingfieldCreate)
- [Update a tracking field](/docs/api/rest/reference/zoom-api/methods/#operation/trackingfieldUpdate)
- [Delete a tracking field](/docs/api/rest/reference/zoom-api/methods/#operation/trackingfieldDelete)

## User

### user:master

View and manage sub account's user information

**Associated APIs:**

- [Update user settings](/docs/api/rest/reference/user/ma/#operation/userSettingsUpdate)
- [Delete user assistants](/docs/api/rest/reference/user/ma/#operation/userAssistantsDelete)
- [Get user permissions](/docs/api/rest/reference/user/ma/#operation/userPermission)
- [Update a user](/docs/api/rest/reference/user/ma/#operation/userUpdate)
- [Get a user](/docs/api/rest/reference/user/ma/#operation/user)
- [Revoke a user's SSO token](/docs/api/rest/reference/user/ma/#operation/userSSOTokenDelete)
- [Delete a user assistant](/docs/api/rest/reference/user/ma/#operation/userAssistantDelete)
- [Get user summary](/docs/api/rest/reference/user/ma/#operation/userSummary)
- [List users](/docs/api/rest/reference/user/ma/#operation/users)
- [Update a user's email](/docs/api/rest/reference/user/ma/#operation/userEmailUpdate)
- [Delete a user](/docs/api/rest/reference/user/ma/#operation/userDelete)
- [Delete a user's profile picture](/docs/api/rest/reference/user/ma/#operation/userPictureDelete)
- [List user schedulers](/docs/api/rest/reference/user/ma/#operation/userSchedulers)
- [Get user settings](/docs/api/rest/reference/user/ma/#operation/userSettings)
- [Delete a scheduler](/docs/api/rest/reference/user/ma/#operation/userSchedulerDelete)
- [Upload Virtual Background files](/docs/api/rest/reference/user/ma/#operation/uploadVBuser)
- [Add assistants](/docs/api/rest/reference/user/ma/#operation/userAssistantCreate)
- [Bulk update features for users](/docs/api/rest/reference/user/ma/#operation/bulkUpdateFeature)
- [Upload a user's profile picture](/docs/api/rest/reference/user/ma/#operation/userPicture)
- [Delete user schedulers](/docs/api/rest/reference/user/ma/#operation/userSchedulersDelete)
- [Get a user's token](/docs/api/rest/reference/user/ma/#operation/userToken)
- [Update user status](/docs/api/rest/reference/user/ma/#operation/userStatus)
- [Delete Virtual Background files](/docs/api/rest/reference/user/ma/#operation/delUserVB)
- [Create users](/docs/api/rest/reference/user/ma/#operation/userCreate)
- [Update a user's password](/docs/api/rest/reference/user/ma/#operation/userPassword)
- [List user assistants](/docs/api/rest/reference/user/ma/#operation/userAssistants)
- [Switch a user's account](/docs/api/rest/reference/user/ma/#operation/SwitchAUser'sAccount)

### user:read

View your user information

**Associated APIs:**

- [Check a user's PM room](/docs/api/rest/reference/user/methods/#operation/userVanityName)
- [Get user summary](/docs/api/rest/reference/user/methods/#operation/userSummary)
- [List users](/docs/api/rest/reference/user/methods/#operation/users)
- [Get a user presence status](/docs/api/rest/reference/user/methods/#operation/getUserPresenceStatus)
- [List user schedulers](/docs/api/rest/reference/user/methods/#operation/userSchedulers)
- [List a user's collaboration devices](/docs/api/rest/reference/user/methods/#operation/listCollaborationDevices)
- [Get meeting summary templates](/docs/api/rest/reference/user/methods/#operation/Getmeetingsummarytemplates)
- [Get a user](/docs/api/rest/reference/user/methods/#operation/user)
- [Check a user email](/docs/api/rest/reference/user/methods/#operation/userEmail)
- [Get user permissions](/docs/api/rest/reference/user/methods/#operation/userPermission)
- [Get user settings](/docs/api/rest/reference/user/methods/#operation/userSettings)
- [Get collaboration device detail](/docs/api/rest/reference/user/methods/#operation/getCollaborationDevice)
- [Get Meeting Template detail](/docs/api/rest/reference/user/methods/#operation/getUserMeetingTemplates)
- [List user assistants](/docs/api/rest/reference/user/methods/#operation/userAssistants)
- [Get a user's token](/docs/api/rest/reference/user/methods/#operation/userToken)

### user:read:admin

View all user information

**Associated APIs:**

- [Get a user's token](/docs/api/rest/reference/user/methods/#operation/userToken)
- [Get a user presence status](/docs/api/rest/reference/user/methods/#operation/getUserPresenceStatus)
- [List users](/docs/api/rest/reference/user/methods/#operation/users)
- [Get user settings](/docs/api/rest/reference/user/methods/#operation/userSettings)
- [Get collaboration device detail](/docs/api/rest/reference/user/methods/#operation/getCollaborationDevice)
- [Get a user](/docs/api/rest/reference/user/methods/#operation/user)
- [List a user's collaboration devices](/docs/api/rest/reference/user/methods/#operation/listCollaborationDevices)
- [List user assistants](/docs/api/rest/reference/user/methods/#operation/userAssistants)
- [List user schedulers](/docs/api/rest/reference/user/methods/#operation/userSchedulers)
- [Get user summary](/docs/api/rest/reference/user/methods/#operation/userSummary)
- [Get user permissions](/docs/api/rest/reference/user/methods/#operation/userPermission)
- [Get Meeting Template detail](/docs/api/rest/reference/user/methods/#operation/getUserMeetingTemplates)
- [Check a user's PM room](/docs/api/rest/reference/user/methods/#operation/userVanityName)
- [Get meeting summary templates](/docs/api/rest/reference/user/methods/#operation/Getmeetingsummarytemplates)
- [Check a user email](/docs/api/rest/reference/user/methods/#operation/userEmail)

### user:write

View and manage your user information

**Associated APIs:**

- [Update a user's presence status](/docs/api/rest/reference/user/methods/#operation/updatePresenceStatus)
- [List user assistants](/docs/api/rest/reference/user/methods/#operation/userAssistants)
- [Add assistants](/docs/api/rest/reference/user/methods/#operation/userAssistantCreate)
- [Get collaboration device detail](/docs/api/rest/reference/user/methods/#operation/getCollaborationDevice)
- [Delete a user assistant](/docs/api/rest/reference/user/methods/#operation/userAssistantDelete)
- [Get a user](/docs/api/rest/reference/user/methods/#operation/user)
- [Delete user assistants](/docs/api/rest/reference/user/methods/#operation/userAssistantsDelete)
- [Update a user's password](/docs/api/rest/reference/user/methods/#operation/userPassword)
- [Check a user's PM room](/docs/api/rest/reference/user/methods/#operation/userVanityName)
- [Create users](/docs/api/rest/reference/user/methods/#operation/userCreate)
- [Get a user's token](/docs/api/rest/reference/user/methods/#operation/userToken)
- [Bulk update features for users](/docs/api/rest/reference/user/methods/#operation/bulkUpdateFeature)
- [Delete Virtual Background files](/docs/api/rest/reference/user/methods/#operation/delUserVB)
- [Delete user schedulers](/docs/api/rest/reference/user/methods/#operation/userSchedulersDelete)
- [List users](/docs/api/rest/reference/user/methods/#operation/users)
- [Get user summary](/docs/api/rest/reference/user/methods/#operation/userSummary)
- [Update user status](/docs/api/rest/reference/user/methods/#operation/userStatus)
- [List a user's collaboration devices](/docs/api/rest/reference/user/methods/#operation/listCollaborationDevices)
- [Upload a user's profile picture](/docs/api/rest/reference/user/methods/#operation/userPicture)
- [Get user permissions](/docs/api/rest/reference/user/methods/#operation/userPermission)
- [List user schedulers](/docs/api/rest/reference/user/methods/#operation/userSchedulers)
- [Update user settings](/docs/api/rest/reference/user/methods/#operation/userSettingsUpdate)
- [Delete a user's profile picture](/docs/api/rest/reference/user/methods/#operation/userPictureDelete)
- [Check a user email](/docs/api/rest/reference/user/methods/#operation/userEmail)
- [Upload Virtual Background files](/docs/api/rest/reference/user/methods/#operation/uploadVBuser)
- [Delete a user](/docs/api/rest/reference/user/methods/#operation/userDelete)
- [Delete a scheduler](/docs/api/rest/reference/user/methods/#operation/userSchedulerDelete)
- [Get user settings](/docs/api/rest/reference/user/methods/#operation/userSettings)
- [Update a user](/docs/api/rest/reference/user/methods/#operation/userUpdate)
- [Revoke a user's SSO token](/docs/api/rest/reference/user/methods/#operation/userSSOTokenDelete)
- [Update a user's email](/docs/api/rest/reference/user/methods/#operation/userEmailUpdate)

### user:write:admin

View users information and manage users

**Associated APIs:**

- [List user assistants](/docs/api/rest/reference/user/methods/#operation/userAssistants)
- [Update a user's presence status](/docs/api/rest/reference/user/methods/#operation/updatePresenceStatus)
- [Delete a user's profile picture](/docs/api/rest/reference/user/methods/#operation/userPictureDelete)
- [Check a user email](/docs/api/rest/reference/user/methods/#operation/userEmail)
- [Create users](/docs/api/rest/reference/user/methods/#operation/userCreate)
- [Delete Virtual Background files](/docs/api/rest/reference/user/methods/#operation/delUserVB)
- [Get a user's token](/docs/api/rest/reference/user/methods/#operation/userToken)
- [Delete a user](/docs/api/rest/reference/user/methods/#operation/userDelete)
- [Delete a user assistant](/docs/api/rest/reference/user/methods/#operation/userAssistantDelete)
- [Check a user's PM room](/docs/api/rest/reference/user/methods/#operation/userVanityName)
- [Get user settings](/docs/api/rest/reference/user/methods/#operation/userSettings)
- [Delete user schedulers](/docs/api/rest/reference/user/methods/#operation/userSchedulersDelete)
- [Get user summary](/docs/api/rest/reference/user/methods/#operation/userSummary)
- [Update user status](/docs/api/rest/reference/user/methods/#operation/userStatus)
- [Update a user's email](/docs/api/rest/reference/user/methods/#operation/userEmailUpdate)
- [Update a user's password](/docs/api/rest/reference/user/methods/#operation/userPassword)
- [Bulk update features for users](/docs/api/rest/reference/user/methods/#operation/bulkUpdateFeature)
- [Revoke a user's SSO token](/docs/api/rest/reference/user/methods/#operation/userSSOTokenDelete)
- [Upload Virtual Background files](/docs/api/rest/reference/user/methods/#operation/uploadVBuser)
- [Get user permissions](/docs/api/rest/reference/user/methods/#operation/userPermission)
- [Update a user](/docs/api/rest/reference/user/methods/#operation/userUpdate)
- [Get collaboration device detail](/docs/api/rest/reference/user/methods/#operation/getCollaborationDevice)
- [Update user settings](/docs/api/rest/reference/user/methods/#operation/userSettingsUpdate)
- [Delete a scheduler](/docs/api/rest/reference/user/methods/#operation/userSchedulerDelete)
- [Delete user assistants](/docs/api/rest/reference/user/methods/#operation/userAssistantsDelete)
- [Add assistants](/docs/api/rest/reference/user/methods/#operation/userAssistantCreate)
- [List a user's collaboration devices](/docs/api/rest/reference/user/methods/#operation/listCollaborationDevices)
- [Get a user](/docs/api/rest/reference/user/methods/#operation/user)
- [List users](/docs/api/rest/reference/user/methods/#operation/users)
- [List user schedulers](/docs/api/rest/reference/user/methods/#operation/userSchedulers)
- [Upload a user's profile picture](/docs/api/rest/reference/user/methods/#operation/userPicture)

### user_info:read

View user info

**Associated APIs:**

- [Get a user](/docs/api/rest/reference/user/methods/#operation/user)

### user_profile

View your profile information

**Associated APIs:**

- [Get a user's token](/docs/api/rest/reference/user/methods/#operation/userToken)
- [List user schedulers](/docs/api/rest/reference/user/methods/#operation/userSchedulers)
- [Get user permissions](/docs/api/rest/reference/user/methods/#operation/userPermission)
- [Get a user](/docs/api/rest/reference/user/methods/#operation/user)
- [List user assistants](/docs/api/rest/reference/user/methods/#operation/userAssistants)

### user_zak:read

View user’s zak token

**Associated APIs:**

- [Get the user's ZAK](/docs/api/rest/reference/user/methods/#operation/userZak)

## Visitor Management

### visitor_management:read

View visitor management information

**Associated APIs:**

- [Get a list of visitors by location](/docs/api/rest/reference/zoom-rooms/methods/#operation/invitationList)
- [Invitation details by invitationID](/docs/api/rest/reference/zoom-rooms/methods/#operation/getInvitation)

### visitor_management:write

Update visitor management information

**Associated APIs:**

- [Delete an Invitation](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteInvitation)
- [Update an invitation](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateInvitation)
- [Check in a visitor](/docs/api/rest/reference/zoom-rooms/methods/#operation/checkinVisitor)

### visitor_management:write:admin

Update visitor management information

**Associated APIs:**

- [Send an invitation](/docs/api/rest/reference/zoom-rooms/methods/#operation/createInvitation)

## Webinar

### webinar:master

View and manage sub account's user webinars

**Associated APIs:**

- [Get webinar tracking sources](/docs/api/rest/reference/zoom-api/ma/#operation/getTrackingSources)
- [Delete a webinar survey](/docs/api/rest/reference/zoom-api/ma/#operation/webinarSurveyDelete)
- [List past webinar instances](/docs/api/rest/reference/zoom-api/ma/#operation/pastWebinars)
- [Remove all panelists](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPanelistsDelete)
- [Get a webinar poll](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPollGet)
- [Update a webinar's branding name tag](/docs/api/rest/reference/zoom-api/ma/#operation/updateWebinarBrandingNameTag)
- [Delete a webinar's branding wallpaper](/docs/api/rest/reference/zoom-api/ma/#operation/deleteWebinarBrandingWallpaper)
- [Set webinar's default branding virtual background](/docs/api/rest/reference/zoom-api/ma/#operation/setWebinarBrandingVB)
- [Delete a webinar registrant](/docs/api/rest/reference/zoom-api/ma/#operation/deleteWebinarRegistrant)
- [Get a webinar](/docs/api/rest/reference/zoom-api/ma/#operation/webinar)
- [List webinar templates](/docs/api/rest/reference/zoom-api/ma/#operation/listWebinarTemplates)
- [Update a webinar](/docs/api/rest/reference/zoom-api/ma/#operation/webinarUpdate)
- [Delete a webinar poll](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPollDelete)
- [Get webinar's session branding](/docs/api/rest/reference/zoom-api/ma/#operation/getWebinarBranding)
- [Upload a webinar's branding wallpaper](/docs/api/rest/reference/zoom-api/ma/#operation/uploadWebinarBrandingWallpaper)
- [Delete a webinar](/docs/api/rest/reference/zoom-api/ma/#operation/webinarDelete)
- [Get webinar's token](/docs/api/rest/reference/zoom-api/ma/#operation/webinarToken)
- [Update a webinar survey](/docs/api/rest/reference/zoom-api/ma/#operation/webinarSurveyUpdate)
- [List webinars](/docs/api/rest/reference/zoom-api/ma/#operation/webinars)
- [Add a webinar registrant](/docs/api/rest/reference/zoom-api/ma/#operation/webinarRegistrantCreate)
- [Update registrant's status](/docs/api/rest/reference/zoom-api/ma/#operation/webinarRegistrantStatus)
- [Update a live stream](/docs/api/rest/reference/zoom-api/ma/#operation/webinarLiveStreamUpdate)
- [List a webinar's polls](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPolls)
- [Delete a webinar's branding name tag](/docs/api/rest/reference/zoom-api/ma/#operation/deleteWebinarBrandingNameTag)
- [Get a webinar survey](/docs/api/rest/reference/zoom-api/ma/#operation/webinarSurveyGet)
- [Create a webinar](/docs/api/rest/reference/zoom-api/ma/#operation/webinarCreate)
- [List webinar registrants](/docs/api/rest/reference/zoom-api/ma/#operation/webinarRegistrants)
- [Upload a webinar's branding virtual background](/docs/api/rest/reference/zoom-api/ma/#operation/uploadWebinarBrandingVB)
- [Update registration questions](/docs/api/rest/reference/zoom-api/ma/#operation/webinarRegistrantQuestionUpdate)
- [Perform batch registration](/docs/api/rest/reference/zoom-api/ma/#operation/addBatchWebinarRegistrants)
- [Get a webinar registrant](/docs/api/rest/reference/zoom-api/ma/#operation/webinarRegistrantGet)
- [Add panelists](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPanelistCreate)
- [Remove a panelist](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPanelistDelete)
- [Update a webinar poll](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPollUpdate)
- [Create a webinar template](/docs/api/rest/reference/zoom-api/ma/#operation/webinarTemplateCreate)
- [List registration questions](/docs/api/rest/reference/zoom-api/ma/#operation/webinarRegistrantsQuestionsGet)
- [Create a webinar's branding name tag](/docs/api/rest/reference/zoom-api/ma/#operation/createWebinarBrandingNameTag)
- [Create webinar's invite links](/docs/api/rest/reference/zoom-api/ma/#operation/webinarInviteLinksCreate)
- [Update live stream status](/docs/api/rest/reference/zoom-api/ma/#operation/webinarLiveStreamStatusUpdate)
- [Get webinar absentees](/docs/api/rest/reference/zoom-api/ma/#operation/webinarAbsentees)
- [List panelists](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPanelists)
- [Create a webinar's poll](/docs/api/rest/reference/zoom-api/ma/#operation/webinarPollCreate)
- [Delete a webinar's branding virtual backgrounds](/docs/api/rest/reference/zoom-api/ma/#operation/deleteWebinarBrandingVB)
- [Get live stream details](/docs/api/rest/reference/zoom-api/ma/#operation/getWebinarLiveStreamDetails)
- [Update webinar status](/docs/api/rest/reference/zoom-api/ma/#operation/webinarStatus)

### webinar:read

View your webinars

**Associated APIs:**

- [Get webinar's token](/docs/api/rest/reference/zoom-api/methods/#operation/webinarToken)
- [Get a webinar registrant](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantGet)
- [List webinars](/docs/api/rest/reference/zoom-api/methods/#operation/webinars)
- [Get a webinar poll](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPollGet)
- [Get a webinar](/docs/api/rest/reference/zoom-api/methods/#operation/webinar)
- [Get webinar's session branding](/docs/api/rest/reference/zoom-api/methods/#operation/getWebinarBranding)
- [Get a webinar survey](/docs/api/rest/reference/zoom-api/methods/#operation/webinarSurveyGet)
- [Get webinar tracking sources](/docs/api/rest/reference/zoom-api/methods/#operation/getTrackingSources)
- [Get live stream details](/docs/api/rest/reference/zoom-api/methods/#operation/getWebinarLiveStreamDetails)
- [List webinar registrants](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrants)
- [List a webinar's polls](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPolls)
- [List webinar templates](/docs/api/rest/reference/zoom-api/methods/#operation/listWebinarTemplates)
- [List registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantsQuestionsGet)
- [List past webinar poll results](/docs/api/rest/reference/zoom-api/methods/#operation/listPastWebinarPollResults)
- [List webinar participants](/docs/api/rest/reference/zoom-api/methods/#operation/listWebinarParticipants)
- [List past webinar instances](/docs/api/rest/reference/zoom-api/methods/#operation/pastWebinars)
- [List panelists](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelists)
- [Get webinar absentees](/docs/api/rest/reference/zoom-api/methods/#operation/webinarAbsentees)
- [List Q&As of a past webinar](/docs/api/rest/reference/zoom-api/methods/#operation/listPastWebinarQA)

### webinar:read:admin

View all user Webinars

**Associated APIs:**

- [Get webinar's session branding](/docs/api/rest/reference/zoom-api/methods/#operation/getWebinarBranding)
- [List panelists](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelists)
- [List Q&As of a past webinar](/docs/api/rest/reference/zoom-api/methods/#operation/listPastWebinarQA)
- [Get webinar absentees](/docs/api/rest/reference/zoom-api/methods/#operation/webinarAbsentees)
- [List webinar participants](/docs/api/rest/reference/zoom-api/methods/#operation/listWebinarParticipants)
- [List registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantsQuestionsGet)
- [List webinar templates](/docs/api/rest/reference/zoom-api/methods/#operation/listWebinarTemplates)
- [List past webinar instances](/docs/api/rest/reference/zoom-api/methods/#operation/pastWebinars)
- [List a webinar's polls](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPolls)
- [Get a webinar survey](/docs/api/rest/reference/zoom-api/methods/#operation/webinarSurveyGet)
- [List webinar registrants](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrants)
- [Get a webinar poll](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPollGet)
- [Get a webinar registrant](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantGet)
- [Get a webinar](/docs/api/rest/reference/zoom-api/methods/#operation/webinar)
- [Get webinar tracking sources](/docs/api/rest/reference/zoom-api/methods/#operation/getTrackingSources)
- [List webinars](/docs/api/rest/reference/zoom-api/methods/#operation/webinars)
- [List past webinar poll results](/docs/api/rest/reference/zoom-api/methods/#operation/listPastWebinarPollResults)
- [Get live stream details](/docs/api/rest/reference/zoom-api/methods/#operation/getWebinarLiveStreamDetails)
- [Get webinar's token](/docs/api/rest/reference/zoom-api/methods/#operation/webinarToken)

### webinar:write

View and manage your webinars

**Associated APIs:**

- [Delete a webinar's branding wallpaper](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarBrandingWallpaper)
- [Update a webinar's branding name tag](/docs/api/rest/reference/zoom-api/methods/#operation/updateWebinarBrandingNameTag)
- [Set webinar's default branding virtual background](/docs/api/rest/reference/zoom-api/methods/#operation/setWebinarBrandingVB)
- [Update a webinar poll](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPollUpdate)
- [Create a webinar's branding name tag](/docs/api/rest/reference/zoom-api/methods/#operation/createWebinarBrandingNameTag)
- [Add a webinar registrant](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantCreate)
- [Upload a webinar's branding virtual background](/docs/api/rest/reference/zoom-api/methods/#operation/uploadWebinarBrandingVB)
- [Remove all panelists](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelistsDelete)
- [Delete a webinar's branding name tag](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarBrandingNameTag)
- [Create webinar's invite links](/docs/api/rest/reference/zoom-api/methods/#operation/webinarInviteLinksCreate)
- [Update a webinar](/docs/api/rest/reference/zoom-api/methods/#operation/webinarUpdate)
- [Delete a webinar poll](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPollDelete)
- [Delete a webinar survey](/docs/api/rest/reference/zoom-api/methods/#operation/webinarSurveyDelete)
- [Add panelists](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelistCreate)
- [Update registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantQuestionUpdate)
- [Delete a webinar](/docs/api/rest/reference/zoom-api/methods/#operation/webinarDelete)
- [Update a webinar survey](/docs/api/rest/reference/zoom-api/methods/#operation/webinarSurveyUpdate)
- [Update a live stream](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLiveStreamUpdate)
- [Remove a panelist](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelistDelete)
- [Create a webinar template](/docs/api/rest/reference/zoom-api/methods/#operation/webinarTemplateCreate)
- [Create a webinar's poll](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPollCreate)
- [Create a webinar](/docs/api/rest/reference/zoom-api/methods/#operation/webinarCreate)
- [Update registrant's status](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantStatus)
- [Upload a webinar's branding wallpaper](/docs/api/rest/reference/zoom-api/methods/#operation/uploadWebinarBrandingWallpaper)
- [Update webinar status](/docs/api/rest/reference/zoom-api/methods/#operation/webinarStatus)
- [Delete a webinar's branding virtual backgrounds](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarBrandingVB)
- [Delete a live webinar message](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarChatMessageById)
- [Delete a webinar registrant](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarRegistrant)
- [Update live stream status](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLiveStreamStatusUpdate)
- [Perform batch registration](/docs/api/rest/reference/zoom-api/methods/#operation/addBatchWebinarRegistrants)

### webinar:write:admin

View and manage all user Webinars

**Associated APIs:**

- [Remove all panelists](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelistsDelete)
- [Delete a webinar registrant](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarRegistrant)
- [Delete a webinar poll](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPollDelete)
- [Delete a webinar's branding wallpaper](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarBrandingWallpaper)
- [Set webinar's default branding virtual background](/docs/api/rest/reference/zoom-api/methods/#operation/setWebinarBrandingVB)
- [Update live stream status](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLiveStreamStatusUpdate)
- [Delete a webinar survey](/docs/api/rest/reference/zoom-api/methods/#operation/webinarSurveyDelete)
- [Update a webinar](/docs/api/rest/reference/zoom-api/methods/#operation/webinarUpdate)
- [Delete a webinar's branding virtual backgrounds](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarBrandingVB)
- [Create a webinar's poll](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPollCreate)
- [Update webinar status](/docs/api/rest/reference/zoom-api/methods/#operation/webinarStatus)
- [Update registrant's status](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantStatus)
- [Upload a webinar's branding virtual background](/docs/api/rest/reference/zoom-api/methods/#operation/uploadWebinarBrandingVB)
- [Delete a webinar's branding name tag](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarBrandingNameTag)
- [Create a webinar](/docs/api/rest/reference/zoom-api/methods/#operation/webinarCreate)
- [Create a webinar's branding name tag](/docs/api/rest/reference/zoom-api/methods/#operation/createWebinarBrandingNameTag)
- [Delete a live webinar message](/docs/api/rest/reference/zoom-api/methods/#operation/deleteWebinarChatMessageById)
- [Create webinar's invite links](/docs/api/rest/reference/zoom-api/methods/#operation/webinarInviteLinksCreate)
- [Update registration questions](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantQuestionUpdate)
- [Perform batch registration](/docs/api/rest/reference/zoom-api/methods/#operation/addBatchWebinarRegistrants)
- [Add panelists](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelistCreate)
- [Update a webinar poll](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPollUpdate)
- [Remove a panelist](/docs/api/rest/reference/zoom-api/methods/#operation/webinarPanelistDelete)
- [Delete a webinar](/docs/api/rest/reference/zoom-api/methods/#operation/webinarDelete)
- [Update a webinar survey](/docs/api/rest/reference/zoom-api/methods/#operation/webinarSurveyUpdate)
- [Upload a webinar's branding wallpaper](/docs/api/rest/reference/zoom-api/methods/#operation/uploadWebinarBrandingWallpaper)
- [Create a webinar template](/docs/api/rest/reference/zoom-api/methods/#operation/webinarTemplateCreate)
- [Add a webinar registrant](/docs/api/rest/reference/zoom-api/methods/#operation/webinarRegistrantCreate)
- [Update a webinar's branding name tag](/docs/api/rest/reference/zoom-api/methods/#operation/updateWebinarBrandingNameTag)
- [Update a live stream](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLiveStreamUpdate)

### webinar:write:admin:sip_dialing

Get CRC dial string with passcode

**Associated APIs:**

- [Get a webinar SIP URI with passcode](/docs/api/rest/reference/zoom-api/methods/#operation/getWebinarSipDialingWithPasscode)

### webinar:write:sip_dialing

Get CRC dial string with passcode

**Associated APIs:**

- [Get a webinar SIP URI with passcode](/docs/api/rest/reference/zoom-api/methods/#operation/getWebinarSipDialingWithPasscode)

### webinar_token:read:admin:live_streaming

View live streaming webinar token information

**Associated APIs:**

- [Get a webinar's join token for live streaming](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLiveStreamingJoinToken)

### webinar_token:read:admin:local_archiving

View local archiving webinar token information

**Associated APIs:**

- [Get a webinar's archive token for local archiving](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLocalArchivingArchiveToken)

### webinar_token:read:admin:local_recording

This scope allows an app to view an account's users' local recording webinar token information

**Associated APIs:**

- [Get a webinar's join token for local recording](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLocalRecordingJoinToken)

### webinar_token:read:live_streaming

View live streaming webinar token information

**Associated APIs:**

- [Get a webinar's join token for live streaming](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLiveStreamingJoinToken)

### webinar_token:read:local_recording

This scope allows an app to view a user's local recording webinar token information

**Associated APIs:**

- [Get a webinar's join token for local recording](/docs/api/rest/reference/zoom-api/methods/#operation/webinarLocalRecordingJoinToken)

## Whiteboard

### whiteboard:read

Get my whiteboard(s)

**Associated APIs:**

- [List all whiteboards](/docs/api/rest/reference/Whiteboard/methods/#operation/ListWhiteboards)
- [Get a whiteboard](/docs/api/rest/reference/Whiteboard/methods/#operation/GetAWhiteboard)

### whiteboard:read:admin

Get account’s whiteboard(s)

**Associated APIs:**

- [List all whiteboards](/docs/api/rest/reference/Whiteboard/methods/#operation/ListWhiteboards)
- [Get a whiteboard](/docs/api/rest/reference/Whiteboard/methods/#operation/GetAWhiteboard)

### whiteboard:write

Update or trash my whiteboard

**Associated APIs:**

- [Delete a whiteboard](/docs/api/rest/reference/Whiteboard/methods/#operation/DeleteAWhiteboard)
- [Create a new whiteboard](/docs/api/rest/reference/Whiteboard/methods/#operation/newWhiteboardCreate)

### whiteboard:write:admin

Update or trash my whiteboard

**Associated APIs:**

- [Update whiteboard basic information](/docs/api/rest/reference/Whiteboard/methods/#operation/UpdateAWhiteboardMetadata)
- [Delete a whiteboard](/docs/api/rest/reference/Whiteboard/methods/#operation/DeleteAWhiteboard)

### whiteboard_collaborator:read:admin

View account's whiteboard collaborator information

**Associated APIs:**

- [Get collaborators of a whiteboard](/docs/api/rest/reference/Whiteboard/methods/#operation/GetAWhiteboardCollaborator)

### whiteboard_collaborator:write:admin

View and manage account's whiteboard collaborator information

**Associated APIs:**

- [Update whiteboard collaborators](/docs/api/rest/reference/Whiteboard/methods/#operation/UpdateAWhiteboardCollaborator)
- [Share a whiteboard to new users or team chat channels.](/docs/api/rest/reference/Whiteboard/methods/#operation/AddAWhiteboardCollaborator)
- [Remove the collaborator from a whiteboard](/docs/api/rest/reference/Whiteboard/methods/#operation/DeleteAWhiteboardCollaborator)

### whiteboard_content:read

View and export whiteboard content

**Associated APIs:**

- [Download Whiteboards activity file](/docs/api/rest/reference/Whiteboard/methods/#operation/Downloadwhiteboardsactivityfile)
- [Get whiteboard export generation status](/docs/api/rest/reference/Whiteboard/methods/#operation/Getwhiteboardexportdatagenerationstatus)
- [List whiteboards sessions](/docs/api/rest/reference/Whiteboard/methods/#operation/Createwhiteboardsarchivefiles)
- [Download whiteboard export](/docs/api/rest/reference/Whiteboard/methods/#operation/Downloadwhiteboardexport)
- [List whiteboard sessions activities](/docs/api/rest/reference/Whiteboard/methods/#operation/Listwhiteboardsessionsarchivedfiles)

### whiteboard_content:read:admin

View and export account’s whiteboard(s) content

**Associated APIs:**

- [List whiteboards sessions](/docs/api/rest/reference/Whiteboard/methods/#operation/Createwhiteboardsarchivefiles)
- [Download Whiteboards activity file](/docs/api/rest/reference/Whiteboard/methods/#operation/Downloadwhiteboardsactivityfile)
- [Download whiteboard export](/docs/api/rest/reference/Whiteboard/methods/#operation/Downloadwhiteboardexport)
- [List whiteboard sessions activities](/docs/api/rest/reference/Whiteboard/methods/#operation/Listwhiteboardsessionsarchivedfiles)
- [Get whiteboard export generation status](/docs/api/rest/reference/Whiteboard/methods/#operation/Getwhiteboardexportdatagenerationstatus)

### whiteboard_export:write

Create my whiteboard export data

**Associated APIs:**

- [Create whiteboard export](/docs/api/rest/reference/Whiteboard/methods/#operation/Createwhiteboardsexport)

### whiteboard_export:write:admin

Create account's whiteboard export data

**Associated APIs:**

- [Create whiteboard export](/docs/api/rest/reference/Whiteboard/methods/#operation/Createwhiteboardsexport)

### whiteboard_file:read

View whiteboard file information

**Associated APIs:**

- [Download Imported Whiteboard File](/docs/api/rest/reference/Whiteboard/methods/#operation/Downloadembeddedwhiteboardfile)

### whiteboard_file:read:admin

View whiteboard file information

**Associated APIs:**

- [Download Imported Whiteboard File](/docs/api/rest/reference/Whiteboard/methods/#operation/Downloadembeddedwhiteboardfile)

### whiteboard_file:write

View and manage whiteboard file informanation

**Associated APIs:**

- [Upload file for whiteboard import](/docs/api/rest/reference/Whiteboard/methods/#operation/Uploadfileforwhiteboardimport)

### whiteboard_file:write:admin

View and manage account's whiteboard file information

**Associated APIs:**

- [Upload file for whiteboard import](/docs/api/rest/reference/Whiteboard/methods/#operation/Uploadfileforwhiteboardimport)

### whiteboard_import:read

View user's whiteboard import information

**Associated APIs:**

- [Get whiteboard import status](/docs/api/rest/reference/Whiteboard/methods/#operation/GetWhiteboardimportstatus)

### whiteboard_import:read:admin

View account's whiteboard import information

**Associated APIs:**

- [Get whiteboard import status](/docs/api/rest/reference/Whiteboard/methods/#operation/GetWhiteboardimportstatus)

### whiteboard_import:write

View and manage user's whiteboard import information

**Associated APIs:**

- [Create a new whiteboard by import](/docs/api/rest/reference/Whiteboard/methods/#operation/CreateWhiteboardImport)

### whiteboard_import:write:admin

view and manage account's whiteboard import information

**Associated APIs:**

- [Create a new whiteboard by import](/docs/api/rest/reference/Whiteboard/methods/#operation/CreateWhiteboardImport)

### whiteboard_project:read

View user's project information

**Associated APIs:**

- [Get a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Getaproject)
- [List all projects](/docs/api/rest/reference/Whiteboard/methods/#operation/Listallprojects)

### whiteboard_project:read:admin

View account's project information

**Associated APIs:**

- [List all projects](/docs/api/rest/reference/Whiteboard/methods/#operation/Listallprojects)
- [Get a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Getaproject)

### whiteboard_project:write

View and manage user's project information

**Associated APIs:**

- [Update project basic information](/docs/api/rest/reference/Whiteboard/methods/#operation/Updateproject)
- [Move whiteboards to a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Movewhiteboardstoproject)
- [Create a new project](/docs/api/rest/reference/Whiteboard/methods/#operation/Createproject)
- [Remove whiteboards from a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Removewhiteboardsfromaproject)
- [Delete a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Deleteproject)

### whiteboard_project:write:admin

View and manage account's project information

**Associated APIs:**

- [Update project basic information](/docs/api/rest/reference/Whiteboard/methods/#operation/Updateproject)
- [Remove whiteboards from a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Removewhiteboardsfromaproject)
- [Delete a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Deleteproject)
- [Create a new project](/docs/api/rest/reference/Whiteboard/methods/#operation/Createproject)
- [Move whiteboards to a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Movewhiteboardstoproject)

### whiteboard_project_collaborator:read

View user's project collaborator information

**Associated APIs:**

- [Get collaborators of a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Getcollaboratorsofaproject)

### whiteboard_project_collaborator:read:admin

View account's project collaborator information

**Associated APIs:**

- [Get collaborators of a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Getcollaboratorsofaproject)

### whiteboard_project_collaborator:write

View and update user's project collaborator information

**Associated APIs:**

- [Share a project to new users](/docs/api/rest/reference/Whiteboard/methods/#operation/Shareaprojecttonewusers)
- [Update project collaborators](/docs/api/rest/reference/Whiteboard/methods/#operation/Updateprojectcollaborators)
- [Remove the collaborator from a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Removethecollaboratorfromaproject)

### whiteboard_project_collaborator:write:admin

View and update account's project collaborator information

**Associated APIs:**

- [Share a project to new users](/docs/api/rest/reference/Whiteboard/methods/#operation/Shareaprojecttonewusers)
- [Remove the collaborator from a project](/docs/api/rest/reference/Whiteboard/methods/#operation/Removethecollaboratorfromaproject)
- [Update project collaborators](/docs/api/rest/reference/Whiteboard/methods/#operation/Updateprojectcollaborators)

### whiteboard_share_setting:write

View and manage your whiteboard sharing settings

**Associated APIs:**

- [Update whiteboard share setting](/docs/api/rest/reference/Whiteboard/methods/#operation/UpdateAWhiteboardShareSetting)

### whiteboard_share_setting:write:admin

View and manage account's whiteboard sharing settings

**Associated APIs:**

- [Update whiteboard share setting](/docs/api/rest/reference/Whiteboard/methods/#operation/UpdateAWhiteboardShareSetting)

## Workspace

### workspace:read

View workspace reservation information

**Associated APIs:**

- [Get a workspace location floor map](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getlocationfloormap)
- [Get a location's hot desk usage](/docs/api/rest/reference/zoom-rooms/methods/#operation/getHotDeskUsage)
- [Get a workspace reservation by reservationId](/docs/api/rest/reference/zoom-rooms/methods/#operation/GETGetaworkspacereservationbyreservationID)
- [List workspace additional information with time range](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getaworkspaceadditionalenhancements)
- [Get a desk assignment](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getadeskassignment)
- [Get a workspace's reservations](/docs/api/rest/reference/zoom-rooms/methods/#operation/listReservations)
- [List workspaces](/docs/api/rest/reference/zoom-rooms/methods/#operation/listWorkspaces)

### workspace:read:admin

View workspace reservation information for the account

**Associated APIs:**

- [Get a user's workspace's reservations](/docs/api/rest/reference/zoom-rooms/methods/#operation/userListReservations)
- [List workspaces](/docs/api/rest/reference/zoom-rooms/methods/#operation/listWorkspaces)
- [Get Workspace Calendar Free/Busy Event](/docs/api/rest/reference/zoom-rooms/methods/#operation/GetWorkspaceCalendarFree/BusyEvent)
- [Get a workspace](/docs/api/rest/reference/zoom-rooms/methods/#operation/getWorkspace)
- [Get a workspace QR code](/docs/api/rest/reference/zoom-rooms/methods/#operation/getWorkspaceQRCode)
- [Get a workspace asset](/docs/api/rest/reference/zoom-rooms/methods/#operation/get_workspace_asset)
- [Get a workspace reservation by reservationId](/docs/api/rest/reference/zoom-rooms/methods/#operation/GETGetaworkspacereservationbyreservationID)
- [Get a desk assignment](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getadeskassignment)
- [List workspace additional information with time range](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getaworkspaceadditionalenhancements)
- [List released workspaces by timeout](/docs/api/rest/reference/zoom-rooms/methods/#operation/getWorksapceReservationReleaseInof)
- [Get a workspace's reservations](/docs/api/rest/reference/zoom-rooms/methods/#operation/listReservations)
- [Get all workspace assets](/docs/api/rest/reference/zoom-rooms/methods/#operation/Getallworkspaceassets)
- [Get a location's hot desk usage](/docs/api/rest/reference/zoom-rooms/methods/#operation/getHotDeskUsage)
- [List workspace reservation questionnaires](/docs/api/rest/reference/zoom-rooms/methods/#operation/Listworkspacereservationquestionnaires)

### workspace:write

Edit workspace reservation information

**Associated APIs:**

- [Update workspace settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateWorkspaceSettings)
- [Delete a reservation](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteReservation)
- [Update a reservation](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateReservation)
- [Create a reservation](/docs/api/rest/reference/zoom-rooms/methods/#operation/createReservation)

### workspace:write:admin

Edit workspace reservation information for the account

**Associated APIs:**

- [Delete Workspace floor map](/docs/api/rest/reference/zoom-rooms/methods/#operation/DeleteWorkspaceFloorMap)
- [Update a workspace](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateWorkspace)
- [Update a reservation](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateReservation)
- [Create a workspace asset](/docs/api/rest/reference/zoom-rooms/methods/#operation/AddaWorkspaceasset)
- [Delete a workspace asset](/docs/api/rest/reference/zoom-rooms/methods/#operation/DeleteaWorkspaceasset)
- [Delete a reservation](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteReservation)
- [Set Workspace Calendar Free/Busy Event](/docs/api/rest/reference/zoom-rooms/methods/#operation/SetCalendarFree/BusyEvent)
- [Create a workspace](/docs/api/rest/reference/zoom-rooms/methods/#operation/createWorkspace)
- [Add or Update a Workspace floor map](/docs/api/rest/reference/zoom-rooms/methods/#operation/AddOrUpdateAWorkspaceFloorMap)
- [Edit a workspace asset](/docs/api/rest/reference/zoom-rooms/methods/#operation/PatchWorkspaceasset)
- [Delete a workspace](/docs/api/rest/reference/zoom-rooms/methods/#operation/deleteWorkspace)
- [Delete a desk assignment](/docs/api/rest/reference/zoom-rooms/methods/#operation/Deleteadeskassignment)
- [Create a reservation](/docs/api/rest/reference/zoom-rooms/methods/#operation/createReservation)
- [Check in/out of a reservation](/docs/api/rest/reference/zoom-rooms/methods/#operation/reservationEvent)
- [Update workspace settings](/docs/api/rest/reference/zoom-rooms/methods/#operation/updateWorkspaceSettings)
- [Set a desk assignment](/docs/api/rest/reference/zoom-rooms/methods/#operation/setADeskAssignment)

## Zoom AIC

### aic_archive:read:admin

View all user's AIC archive files

## Zoom Account

### data_request:read:admin

Allows viewing and downloading data request information

**Associated APIs:**

- [Get download link for data access request file](/docs/api/rest/reference/account/methods/#operation/DownloadfilesfromDataRequest)
- [List data request history](/docs/api/rest/reference/account/methods/#operation/GetDataRequestsHistory)
- [List downloadable files for export data request](/docs/api/rest/reference/account/methods/#operation/GetDownloadableFilesforDataRequest)

### data_request:write:admin

Allows creation and modification of data requests

**Associated APIs:**

- [Create data (export/deletion) request](/docs/api/rest/reference/account/methods/#operation/CreateDataAccessRequest)
- [List downloadable files for export data request](/docs/api/rest/reference/account/methods/#operation/GetDownloadableFilesforDataRequest)
- [Get download link for data access request file](/docs/api/rest/reference/account/methods/#operation/DownloadfilesfromDataRequest)
- [List data request history](/docs/api/rest/reference/account/methods/#operation/GetDataRequestsHistory)
- [Cancel data deletion request](/docs/api/rest/reference/account/methods/#operation/CancelDataRequest)

## Zoom Auto Dialer

### dialer:read:admin

View Dialer

### dialer:write:admin

Manage Dialer

## Zoom Clips

### clips:read:master

view your subAccount clips info

**Associated APIs:**

- [List all clips](/docs/api/rest/reference/clips/ma/#operation/GetUserClips)

## Zoom Docs

### docs:read

Get basic info of the file

**Associated APIs:**

- [Get metadata of a file](/docs/api/rest/reference/Docs/methods/#operation/QueryFileMetadata)
- [List all children of a file](/docs/api/rest/reference/Docs/methods/#operation/ListAllChildren)

### docs:write

Edit basic info of a file

**Associated APIs:**

- [Create a new file](/docs/api/rest/reference/Docs/methods/#operation/CreateDoc)
- [Modify metadata of a file](/docs/api/rest/reference/Docs/methods/#operation/ModifyMetadata)

## Zoom Events

### zoom_events_access_links:read

View event's Access Link

**Associated APIs:**

- [Get event access link](/docs/api/rest/reference/event/methods/#operation/GetEventAccessLink)
- [List event access links](/docs/api/rest/reference/event/methods/#operation/getEventAccessLinks)

### zoom_events_access_links:read:admin

View event's Access Link

**Associated APIs:**

- [Get event access link](/docs/api/rest/reference/event/methods/#operation/GetEventAccessLink)
- [List event access links](/docs/api/rest/reference/event/methods/#operation/getEventAccessLinks)

### zoom_events_access_links:write

View and Manage Zoom Event's access links

**Associated APIs:**

- [Create event access link](/docs/api/rest/reference/event/methods/#operation/createEventAccessLink)
- [Update event access](/docs/api/rest/reference/event/methods/#operation/updateEventAccess)
- [Delete event access link](/docs/api/rest/reference/event/methods/#operation/deleteEventAccessLink)

### zoom_events_access_links:write:admin

View and Manage Zoom Event's access links

**Associated APIs:**

- [Create event access link](/docs/api/rest/reference/event/methods/#operation/createEventAccessLink)
- [Update event access](/docs/api/rest/reference/event/methods/#operation/updateEventAccess)
- [Delete event access link](/docs/api/rest/reference/event/methods/#operation/deleteEventAccessLink)

### zoom_events_attendee_actions:read

View attendee actions performed by host for an event/session

**Associated APIs:**

- [List session attendee actions](/docs/api/rest/reference/event/methods/#operation/ListSessionAttendeeActions)
- [List event attendee actions](/docs/api/rest/reference/event/methods/#operation/ListEventAttendeeActions)

### zoom_events_attendee_actions:read:admin

View attendee actions performed by host for an event/session

**Associated APIs:**

- [List event attendee actions](/docs/api/rest/reference/event/methods/#operation/ListEventAttendeeActions)
- [List session attendee actions](/docs/api/rest/reference/event/methods/#operation/ListSessionAttendeeActions)

### zoom_events_attendee_actions:write

View and manage attendee actions performed by host for an event/session

**Associated APIs:**

- [Update event attendee actions](/docs/api/rest/reference/event/methods/#operation/UpdateEventAttendeeActions)
- [Update session attendee actions](/docs/api/rest/reference/event/methods/#operation/UpdateSessionAttendeeActions)

### zoom_events_attendee_actions:write:admin

View and manage attendee actions performed by host for an event/session

**Associated APIs:**

- [Update session attendee actions](/docs/api/rest/reference/event/methods/#operation/UpdateSessionAttendeeActions)
- [Update event attendee actions](/docs/api/rest/reference/event/methods/#operation/UpdateEventAttendeeActions)

### zoom_events_basic:read

View your Zoom events

**Associated APIs:**

- [List events](/docs/api/rest/reference/event/methods/#operation/getEvents)
- [Get an event](/docs/api/rest/reference/event/methods/#operation/getEventInfo)

### zoom_events_basic:read:admin

View all events information

**Associated APIs:**

- [Get an event](/docs/api/rest/reference/event/methods/#operation/getEventInfo)
- [List events](/docs/api/rest/reference/event/methods/#operation/getEvents)

### zoom_events_basic:write

Manage your Zoom events

**Associated APIs:**

- [Delete an event](/docs/api/rest/reference/event/methods/#operation/deleteEvent)
- [Event actions](/docs/api/rest/reference/event/methods/#operation/EventActions)
- [Update an event](/docs/api/rest/reference/event/methods/#operation/updateEvent)
- [Create an event](/docs/api/rest/reference/event/methods/#operation/createEvent)

### zoom_events_basic:write:admin

View and manage events information

**Associated APIs:**

- [Update an event](/docs/api/rest/reference/event/methods/#operation/updateEvent)
- [Create an event](/docs/api/rest/reference/event/methods/#operation/createEvent)
- [Event actions](/docs/api/rest/reference/event/methods/#operation/EventActions)
- [Delete an event](/docs/api/rest/reference/event/methods/#operation/deleteEvent)

### zoom_events_coeditor:write

View and manage coeditor information

**Associated APIs:**

- [Add or remove event co-editors](/docs/api/rest/reference/event/methods/#operation/coeditoractions)

### zoom_events_coeditor:write:admin

View and manage coeditor information

**Associated APIs:**

- [Add or remove event co-editors](/docs/api/rest/reference/event/methods/#operation/coeditoractions)

### zoom_events_coeditors:read

View Zoom event coeditors information

**Associated APIs:**

- [List coeditors](/docs/api/rest/reference/event/methods/#operation/getCoEditors)

### zoom_events_coeditors:read:admin

View Zoom events coeditor information

**Associated APIs:**

- [List coeditors](/docs/api/rest/reference/event/methods/#operation/getCoEditors)

### zoom_events_email:read

View emails for an event

**Associated APIs:**

- [List event email types](/docs/api/rest/reference/event/methods/#operation/listEmailTypes)
- [List event emails sent status](/docs/api/rest/reference/event/methods/#operation/listEmailSentStatuses)

### zoom_events_email:read:admin

View emails for an event

**Associated APIs:**

- [List event email types](/docs/api/rest/reference/event/methods/#operation/listEmailTypes)
- [List event emails sent status](/docs/api/rest/reference/event/methods/#operation/listEmailSentStatuses)

### zoom_events_exhibitors:read

View exhibitor information for an event

**Associated APIs:**

- [Get an exhibitor](/docs/api/rest/reference/event/methods/#operation/getExhibitorInfo)
- [List sponsor tiers](/docs/api/rest/reference/event/methods/#operation/ListSponsorTiers)
- [List exhibitors](/docs/api/rest/reference/event/methods/#operation/getExhibitors)

### zoom_events_exhibitors:read:admin

View exhibitor information for an event

**Associated APIs:**

- [Get an exhibitor](/docs/api/rest/reference/event/methods/#operation/getExhibitorInfo)
- [List sponsor tiers](/docs/api/rest/reference/event/methods/#operation/ListSponsorTiers)
- [List exhibitors](/docs/api/rest/reference/event/methods/#operation/getExhibitors)

### zoom_events_exhibitors:write

View and manage exhibitor information for an event

**Associated APIs:**

- [Create an exhibitor](/docs/api/rest/reference/event/methods/#operation/createExhibitor)
- [Delete an exhibitor](/docs/api/rest/reference/event/methods/#operation/deleteExhibitor)
- [Update exhibitor for an event](/docs/api/rest/reference/event/methods/#operation/updateExhibitor)

### zoom_events_exhibitors:write:admin

View and manage exhibitor information for an event

**Associated APIs:**

- [Create an exhibitor](/docs/api/rest/reference/event/methods/#operation/createExhibitor)
- [Update exhibitor for an event](/docs/api/rest/reference/event/methods/#operation/updateExhibitor)
- [Delete an exhibitor](/docs/api/rest/reference/event/methods/#operation/deleteExhibitor)

### zoom_events_file:write

zoom events file upload

**Associated APIs:**

- [Upload events file](/docs/api/rest/reference/event/methods/#operation/uploadEventFile)
- [Upload events multipart files](/docs/api/rest/reference/event/methods/#operation/uploadMultipartEventFile)
- [Initiate and complete the multipart file upload](/docs/api/rest/reference/event/methods/#operation/initiateAndCompleteAEventMultipartUpload.)

### zoom_events_file:write:admin

zoom events file upload account level

**Associated APIs:**

- [Upload events file](/docs/api/rest/reference/event/methods/#operation/uploadEventFile)
- [Upload events multipart files](/docs/api/rest/reference/event/methods/#operation/uploadMultipartEventFile)
- [Initiate and complete the multipart file upload](/docs/api/rest/reference/event/methods/#operation/initiateAndCompleteAEventMultipartUpload.)

### zoom_events_hub:write

Update Zoom Events hub configuration

**Associated APIs:**

- [Creates a new hub host](/docs/api/rest/reference/event/methods/#operation/createHubHost)
- [Remove hub host](/docs/api/rest/reference/event/methods/#operation/deleteHubHost)

### zoom_events_hub:write:admin

Update Zoom Events hub information

**Associated APIs:**

- [Remove hub host](/docs/api/rest/reference/event/methods/#operation/deleteHubHost)
- [Creates a new hub host](/docs/api/rest/reference/event/methods/#operation/createHubHost)

### zoom_events_hubs:read

View all hubs information

**Associated APIs:**

- [List hubs](/docs/api/rest/reference/event/methods/#operation/getHubList)
- [List hub Hosts](/docs/api/rest/reference/event/methods/#operation/gethubhostList)
- [List hub videos](/docs/api/rest/reference/event/methods/#operation/ListHubVideos)

### zoom_events_hubs:read:admin

View all hubs information

**Associated APIs:**

- [List hubs](/docs/api/rest/reference/event/methods/#operation/getHubList)
- [List hub videos](/docs/api/rest/reference/event/methods/#operation/ListHubVideos)
- [List hub Hosts](/docs/api/rest/reference/event/methods/#operation/gethubhostList)

### zoom_events_registrants:read

View event registrants information

**Associated APIs:**

- [List session attendees](/docs/api/rest/reference/event/methods/#operation/getSessionAttendeeList)
- [List registrants](/docs/api/rest/reference/event/methods/#operation/getRegistrants)

### zoom_events_registrants:read:admin

View event registrants information

**Associated APIs:**

- [List registrants](/docs/api/rest/reference/event/methods/#operation/getRegistrants)
- [List session attendees](/docs/api/rest/reference/event/methods/#operation/getSessionAttendeeList)

### zoom_events_reports:read

View Zoom events report

**Associated APIs:**

- [Get session attendance report](/docs/api/rest/reference/event/methods/#operation/SessionAttendanceReport)
- [Get custom report](/docs/api/rest/reference/event/methods/#operation/getCustomEventReport)
- [Get chat transcripts report](/docs/api/rest/reference/event/methods/#operation/ChatTranscriptsReport)
- [Get event survey report](/docs/api/rest/reference/event/methods/#operation/EventSurveyReportApi)
- [Get event attendance (Live or Lobby) report](/docs/api/rest/reference/event/methods/#operation/EventAttendanceReport)
- [Get event registrations report](/docs/api/rest/reference/event/methods/#operation/EventRegistrationsReport)

### zoom_events_reports:read:admin

View Zoom events reports

**Associated APIs:**

- [Get event registrations report](/docs/api/rest/reference/event/methods/#operation/EventRegistrationsReport)
- [Get chat transcripts report](/docs/api/rest/reference/event/methods/#operation/ChatTranscriptsReport)
- [Get event survey report](/docs/api/rest/reference/event/methods/#operation/EventSurveyReportApi)
- [Get custom report](/docs/api/rest/reference/event/methods/#operation/getCustomEventReport)
- [Get event attendance (Live or Lobby) report](/docs/api/rest/reference/event/methods/#operation/EventAttendanceReport)
- [Get session attendance report](/docs/api/rest/reference/event/methods/#operation/SessionAttendanceReport)

### zoom_events_sessions:read

View event session information

**Associated APIs:**

- [List session reservations](/docs/api/rest/reference/event/methods/#operation/ListSessionReservations)
- [Get ticket session join token by Event ID and Session ID](/docs/api/rest/reference/event/methods/#operation/getSessionJoinToken)
- [List session interpreters](/docs/api/rest/reference/event/methods/#operation/getSessionInterpreterList)
- [Get the session information](/docs/api/rest/reference/event/methods/#operation/getEventSessionInfo)
- [List sessions](/docs/api/rest/reference/event/methods/#operation/getEventSessionList)
- [List session polls](/docs/api/rest/reference/event/methods/#operation/getSessionPolls)
- [Get session livestream configuration](/docs/api/rest/reference/event/methods/#operation/getSessionLivestreamConfiguration)

### zoom_events_sessions:read:admin

View event session information

**Associated APIs:**

- [Get session livestream configuration](/docs/api/rest/reference/event/methods/#operation/getSessionLivestreamConfiguration)
- [Get ticket session join token by Event ID and Session ID](/docs/api/rest/reference/event/methods/#operation/getSessionJoinToken)
- [List session interpreters](/docs/api/rest/reference/event/methods/#operation/getSessionInterpreterList)
- [List session polls](/docs/api/rest/reference/event/methods/#operation/getSessionPolls)
- [Get the session information](/docs/api/rest/reference/event/methods/#operation/getEventSessionInfo)
- [List session reservations](/docs/api/rest/reference/event/methods/#operation/ListSessionReservations)
- [List sessions](/docs/api/rest/reference/event/methods/#operation/getEventSessionList)

### zoom_events_sessions:write

View and manage event session information

**Associated APIs:**

- [Create or update session polls](/docs/api/rest/reference/event/methods/#operation/updateSessionPolls)
- [Update a session](/docs/api/rest/reference/event/methods/#operation/updateEventSession)
- [Add session reservations](/docs/api/rest/reference/event/methods/#operation/AddSessionReservations)
- [Delete session reservations](/docs/api/rest/reference/event/methods/#operation/DeleteSessionReservations)
- [Update session livestream configuration](/docs/api/rest/reference/event/methods/#operation/UpdateSessionLivestreamConfiguration)
- [Delete a session](/docs/api/rest/reference/event/methods/#operation/deleteEventSession)
- [Create a session](/docs/api/rest/reference/event/methods/#operation/createEventSession)
- [Create or update session interpreters](/docs/api/rest/reference/event/methods/#operation/updateSessionInterpreters)

### zoom_events_sessions:write:admin

View and manage event session information

**Associated APIs:**

- [Create or update session polls](/docs/api/rest/reference/event/methods/#operation/updateSessionPolls)
- [Add session reservations](/docs/api/rest/reference/event/methods/#operation/AddSessionReservations)
- [Delete a session](/docs/api/rest/reference/event/methods/#operation/deleteEventSession)
- [Create a session](/docs/api/rest/reference/event/methods/#operation/createEventSession)
- [Update session livestream configuration](/docs/api/rest/reference/event/methods/#operation/UpdateSessionLivestreamConfiguration)
- [Delete session reservations](/docs/api/rest/reference/event/methods/#operation/DeleteSessionReservations)
- [Update a session](/docs/api/rest/reference/event/methods/#operation/updateEventSession)
- [Create or update session interpreters](/docs/api/rest/reference/event/methods/#operation/updateSessionInterpreters)

### zoom_events_speakers:read

View event speaker information

**Associated APIs:**

- [List speakers](/docs/api/rest/reference/event/methods/#operation/getSpeakers)
- [Get a speaker](/docs/api/rest/reference/event/methods/#operation/getSpeaker)

### zoom_events_speakers:read:admin

View event speaker information

**Associated APIs:**

- [List speakers](/docs/api/rest/reference/event/methods/#operation/getSpeakers)
- [Get a speaker](/docs/api/rest/reference/event/methods/#operation/getSpeaker)

### zoom_events_speakers:write

Manage event speaker information

**Associated APIs:**

- [Create a speaker](/docs/api/rest/reference/event/methods/#operation/createSpeaker)
- [Update a speaker](/docs/api/rest/reference/event/methods/#operation/updateSpeaker)
- [Delete a speaker](/docs/api/rest/reference/event/methods/#operation/deleteSpeaker)

### zoom_events_speakers:write:admin

Manage event speaker information

**Associated APIs:**

- [Create a speaker](/docs/api/rest/reference/event/methods/#operation/createSpeaker)
- [Delete a speaker](/docs/api/rest/reference/event/methods/#operation/deleteSpeaker)
- [Update a speaker](/docs/api/rest/reference/event/methods/#operation/updateSpeaker)

### zoom_events_ticket_types:read

View all event ticket types

**Associated APIs:**

- [List ticket types](/docs/api/rest/reference/event/methods/#operation/getEventTicketTypes)
- [List registration questions for ticket type](/docs/api/rest/reference/event/methods/#operation/getRegistrationQuestionsForTicketType)
- [List registration questions for an event](/docs/api/rest/reference/event/methods/#operation/getRegistrationQuestionsForEvent)

### zoom_events_ticket_types:read:admin

View all event ticket types

**Associated APIs:**

- [List ticket types](/docs/api/rest/reference/event/methods/#operation/getEventTicketTypes)
- [List registration questions for an event](/docs/api/rest/reference/event/methods/#operation/getRegistrationQuestionsForEvent)
- [List registration questions for ticket type](/docs/api/rest/reference/event/methods/#operation/getRegistrationQuestionsForTicketType)

### zoom_events_ticket_types:write

View and manage event ticket types

**Associated APIs:**

- [Create an event ticket type](/docs/api/rest/reference/event/methods/#operation/createTicketType)
- [Update registration questions for an event](/docs/api/rest/reference/event/methods/#operation/updateRegistrationQuestionsForEvent)
- [Update ticket type for an event](/docs/api/rest/reference/event/methods/#operation/updateTicketType)
- [Delete a ticket type](/docs/api/rest/reference/event/methods/#operation/deleteEventTicketType)
- [Update registration questions for ticket type](/docs/api/rest/reference/event/methods/#operation/updateRegistrationQuestionsForTicketType)

### zoom_events_ticket_types:write:admin

View and manage event ticket types

**Associated APIs:**

- [Update ticket type for an event](/docs/api/rest/reference/event/methods/#operation/updateTicketType)
- [Update registration questions for an event](/docs/api/rest/reference/event/methods/#operation/updateRegistrationQuestionsForEvent)
- [Create an event ticket type](/docs/api/rest/reference/event/methods/#operation/createTicketType)
- [Update registration questions for ticket type](/docs/api/rest/reference/event/methods/#operation/updateRegistrationQuestionsForTicketType)
- [Delete a ticket type](/docs/api/rest/reference/event/methods/#operation/deleteEventTicketType)

### zoom_events_tickets:read

View event tickets and event ticket details

**Associated APIs:**

- [Get a ticket](/docs/api/rest/reference/event/methods/#operation/getTicketDetails)
- [List tickets](/docs/api/rest/reference/event/methods/#operation/getTickets)

### zoom_events_tickets:read:admin

View event tickets information

**Associated APIs:**

- [Get a ticket](/docs/api/rest/reference/event/methods/#operation/getTicketDetails)
- [List tickets](/docs/api/rest/reference/event/methods/#operation/getTickets)

### zoom_events_tickets:write

Create event tickets

**Associated APIs:**

- [Create tickets](/docs/api/rest/reference/event/methods/#operation/createTickets)
- [Delete a ticket](/docs/api/rest/reference/event/methods/#operation/deleteTicket)
- [Update ticket](/docs/api/rest/reference/event/methods/#operation/Updateticket)

### zoom_events_tickets:write:admin

View and manage event tickets information

**Associated APIs:**

- [Delete a ticket](/docs/api/rest/reference/event/methods/#operation/deleteTicket)
- [Create tickets](/docs/api/rest/reference/event/methods/#operation/createTickets)
- [Update ticket](/docs/api/rest/reference/event/methods/#operation/Updateticket)

### zoom_events_vod_channels:read

View on-demand video channels

**Associated APIs:**

- [Get VOD channel details](/docs/api/rest/reference/event/methods/#operation/getVODChannelDetail)
- [List VOD channel videos](/docs/api/rest/reference/event/methods/#operation/ListVODChannelVideos)
- [List channels](/docs/api/rest/reference/event/methods/#operation/getVODChannels)

### zoom_events_vod_channels:read:admin

View on-demand video channels

**Associated APIs:**

- [List channels](/docs/api/rest/reference/event/methods/#operation/getVODChannels)
- [List VOD channel videos](/docs/api/rest/reference/event/methods/#operation/ListVODChannelVideos)
- [Get VOD channel details](/docs/api/rest/reference/event/methods/#operation/getVODChannelDetail)

### zoom_events_vod_channels:write

View and manage on-demand video channels

**Associated APIs:**

- [Add VOD channel videos](/docs/api/rest/reference/event/methods/#operation/AddVODChannelVideos)
- [Create VOD channel](/docs/api/rest/reference/event/methods/#operation/createVodChannel)
- [Delete VOD channel video](/docs/api/rest/reference/event/methods/#operation/DeleteVODChannelVideo)
- [VOD channel actions](/docs/api/rest/reference/event/methods/#operation/vodChannelActions)
- [Update VOD channel](/docs/api/rest/reference/event/methods/#operation/UpdateVideoChannel)
- [Delete VOD Channel](/docs/api/rest/reference/event/methods/#operation/DeleteVODChannel)

### zoom_events_vod_channels:write:admin

View and manage on-demand video channels

**Associated APIs:**

- [Update VOD channel](/docs/api/rest/reference/event/methods/#operation/UpdateVideoChannel)
- [Add VOD channel videos](/docs/api/rest/reference/event/methods/#operation/AddVODChannelVideos)
- [Create VOD channel](/docs/api/rest/reference/event/methods/#operation/createVodChannel)
- [Delete VOD channel video](/docs/api/rest/reference/event/methods/#operation/DeleteVODChannelVideo)
- [VOD channel actions](/docs/api/rest/reference/event/methods/#operation/vodChannelActions)
- [Delete VOD Channel](/docs/api/rest/reference/event/methods/#operation/DeleteVODChannel)

### zoom_events_vod_registration:read

Read VOD channel registrations

**Associated APIs:**

- [List VOD Registration](/docs/api/rest/reference/event/methods/#operation/ListVODRegistration)
- [Get VOD Registration Questions](/docs/api/rest/reference/event/methods/#operation/getRegistrationQuestionsForVODChannel)

### zoom_events_vod_registration:read:admin

Read VOD channel registration settings

**Associated APIs:**

- [List VOD Registration](/docs/api/rest/reference/event/methods/#operation/ListVODRegistration)
- [Get VOD Registration Questions](/docs/api/rest/reference/event/methods/#operation/getRegistrationQuestionsForVODChannel)

### zoom_events_vod_registration:write

Update VOD channel registrations

**Associated APIs:**

- [update VOD channel registration questions](/docs/api/rest/reference/event/methods/#operation/updateRegistrationQuestionsForVODchannel)
- [VOD channel registration](/docs/api/rest/reference/event/methods/#operation/VODTicketRegistration)

### zoom_events_vod_registration:write:admin

Update VOD channel registrations

**Associated APIs:**

- [update VOD channel registration questions](/docs/api/rest/reference/event/methods/#operation/updateRegistrationQuestionsForVODchannel)
- [VOD channel registration](/docs/api/rest/reference/event/methods/#operation/VODTicketRegistration)

### zoom_events_vod_reports:read

Zoom Events VOD reports

**Associated APIs:**

- [Get VOD channel registration report](/docs/api/rest/reference/event/methods/#operation/VodChannelReigistration)

### zoom_events_vod_reports:read:admin

Zoom events VOD reports

**Associated APIs:**

- [Get VOD channel registration report](/docs/api/rest/reference/event/methods/#operation/VodChannelReigistration)

## Zoom IQ

### iq_account:read:admin

View all account settings information

**Associated APIs:**

- [Get indicators settings [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/accountSettingsIndicatorsDeprecated)
- [Get indicators settings](/docs/api/rest/reference/iq/methods/#operation/accountIndicatorsSettings)

### iq_coaching:read

View your coaching information

**Associated APIs:**

- [Get conversation scorecards](/docs/api/rest/reference/iq/methods/#operation/getConversationScorecardsById)
- [Get conversation scorecards [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationScorecardsDeprecated)

### iq_coaching:read:admin

View all coaching information

**Associated APIs:**

- [Get conversation scorecards](/docs/api/rest/reference/iq/methods/#operation/getConversationScorecardsById)
- [Get conversation scorecards [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationScorecardsDeprecated)

### iq_comment:read

View your comments information

**Associated APIs:**

- [Get conversation comments](/docs/api/rest/reference/iq/methods/#operation/getConversationCommentsById)
- [Get conversation comments [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationCommentsDeprecated)

### iq_comment:read:admin

Manage all comments information

**Associated APIs:**

- [Get conversation comments](/docs/api/rest/reference/iq/methods/#operation/getConversationCommentsById)
- [Get conversation comments [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationCommentsDeprecated)

### iq_comment:write

Mangage your comments information

**Associated APIs:**

- [Get conversation comments [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationCommentsDeprecated)
- [Get conversation comments](/docs/api/rest/reference/iq/methods/#operation/getConversationCommentsById)
- [Add new comments to the conversation](/docs/api/rest/reference/iq/methods/#operation/addConversationComments)
- [Add new comments to the conversation [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/addConversationCommentDeprecated)
- [Delete conversation's comment](/docs/api/rest/reference/iq/methods/#operation/deleteConversationCommentById)
- [Edit conversation comment](/docs/api/rest/reference/iq/methods/#operation/editConversationCommentById)
- [Delete conversation's comment [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/deleteConversationCommentDeprecated)
- [Edit conversation comment [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/editConversationCommentDeprecated)

### iq_comment:write:admin

Manage all comments information

**Associated APIs:**

- [Add new comments to the conversation [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/addConversationCommentDeprecated)
- [Edit conversation comment](/docs/api/rest/reference/iq/methods/#operation/editConversationCommentById)
- [Delete conversation's comment [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/deleteConversationCommentDeprecated)
- [Delete conversation's comment](/docs/api/rest/reference/iq/methods/#operation/deleteConversationCommentById)
- [Edit conversation comment [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/editConversationCommentDeprecated)
- [Add new comments to the conversation](/docs/api/rest/reference/iq/methods/#operation/addConversationComments)
- [Get conversation comments [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationCommentsDeprecated)
- [Get conversation comments](/docs/api/rest/reference/iq/methods/#operation/getConversationCommentsById)

### iq_conversation:read

View your conversations information

**Associated APIs:**

- [Get conversation content analysis](/docs/api/rest/reference/iq/methods/#operation/getConversationContentAnalysisById)
- [Get conversation content analysis [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationContentAnalysisDeprecated)
- [Get conversation interactions [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationInteractionsDeprecated)
- [List conversations](/docs/api/rest/reference/iq/methods/#operation/listAllConversations)
- [Get conversation information [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationInfoDeprecated)
- [Get conversation interactions](/docs/api/rest/reference/iq/methods/#operation/getConversationInteraction)
- [List scheduled meetings](/docs/api/rest/reference/iq/methods/#operation/Listallscheduledmeetings)
- [Get conversation information](/docs/api/rest/reference/iq/methods/#operation/getConversationDetail)
- [List conversations [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/listConversationsDeprecated)

### iq_conversation:read:admin

View all conversations information

**Associated APIs:**

- [Get conversation content analysis](/docs/api/rest/reference/iq/methods/#operation/getConversationContentAnalysisById)
- [List conversations](/docs/api/rest/reference/iq/methods/#operation/listAllConversations)
- [Get conversation interactions [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationInteractionsDeprecated)
- [Get conversation content analysis [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationContentAnalysisDeprecated)
- [Get conversation information [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationInfoDeprecated)
- [List conversations [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/listConversationsDeprecated)
- [Get conversation interactions](/docs/api/rest/reference/iq/methods/#operation/getConversationInteraction)
- [List scheduled meetings](/docs/api/rest/reference/iq/methods/#operation/Listallscheduledmeetings)
- [Get conversation information](/docs/api/rest/reference/iq/methods/#operation/getConversationDetail)

### iq_conversation:write

Manage your conversations information

**Associated APIs:**

- [Update conversation host id to new host id by conversation id [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/UpdateconversationhostidtonewhostidbyconversationidDeprecated)
- [Get conversation information [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationInfoDeprecated)
- [Get conversation interactions [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationInteractionsDeprecated)
- [Delete conversation by conversation ID [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/deleteConversationDeprecated)
- [Add conversation by file id or download url.](/docs/api/rest/reference/iq/methods/#operation/AddConversationByFileIdOrDownloadUrl)
- [Add conversation by meeting record url or meeting UUID.](/docs/api/rest/reference/iq/methods/#operation/addConversationByRecord)
- [Upload IQ file [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/UploadIQFileDeprecated)
- [Get conversation interactions](/docs/api/rest/reference/iq/methods/#operation/getConversationInteraction)
- [List scheduled meetings](/docs/api/rest/reference/iq/methods/#operation/Listallscheduledmeetings)
- [Initiate and complete a multipart upload.](/docs/api/rest/reference/iq/methods/#operation/InitiateAndCompleteAMultipartUpload)
- [Get conversation information](/docs/api/rest/reference/iq/methods/#operation/getConversationDetail)
- [Add conversation by file id or download url. [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/AddConversationByFileIdOrDownloadUrlDeprecated)
- [Add conversation by meeting record url or meeting UUID. [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/addConversationDeprecated)
- [Upload iq multipart file.](/docs/api/rest/reference/iq/methods/#operation/UploadZraMultipartFile.)
- [Get conversation content analysis [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationContentAnalysisDeprecated)
- [Upload IQ file](/docs/api/rest/reference/iq/methods/#operation/UploadZraFile)
- [Update conversation host id to new host id by conversation id](/docs/api/rest/reference/iq/methods/#operation/UpdateConversationhostid2NewHostidByConversationId)
- [Delete conversation by conversation ID](/docs/api/rest/reference/iq/methods/#operation/deleteConversationById)
- [Get conversation content analysis](/docs/api/rest/reference/iq/methods/#operation/getConversationContentAnalysisById)
- [List conversations](/docs/api/rest/reference/iq/methods/#operation/listAllConversations)
- [List conversations [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/listConversationsDeprecated)
- [Upload iq multipart file. [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/UploadIqMultipartFileDeprecated)

### iq_conversation:write:admin

Manage all conversations information

**Associated APIs:**

- [Get conversation interactions](/docs/api/rest/reference/iq/methods/#operation/getConversationInteraction)
- [List conversations [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/listConversationsDeprecated)
- [Upload iq multipart file. [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/UploadIqMultipartFileDeprecated)
- [Delete conversation by conversation ID [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/deleteConversationDeprecated)
- [Update conversation host id to new host id by conversation id [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/UpdateconversationhostidtonewhostidbyconversationidDeprecated)
- [List conversations](/docs/api/rest/reference/iq/methods/#operation/listAllConversations)
- [Upload IQ file [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/UploadIQFileDeprecated)
- [Get conversation interactions [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationInteractionsDeprecated)
- [Upload iq multipart file.](/docs/api/rest/reference/iq/methods/#operation/UploadZraMultipartFile.)
- [Add conversation by meeting record url or meeting UUID. [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/addConversationDeprecated)
- [List scheduled meetings](/docs/api/rest/reference/iq/methods/#operation/Listallscheduledmeetings)
- [Get conversation information](/docs/api/rest/reference/iq/methods/#operation/getConversationDetail)
- [Add conversation by meeting record url or meeting UUID.](/docs/api/rest/reference/iq/methods/#operation/addConversationByRecord)
- [Update conversation host id to new host id by conversation id](/docs/api/rest/reference/iq/methods/#operation/UpdateConversationhostid2NewHostidByConversationId)
- [Get conversation content analysis](/docs/api/rest/reference/iq/methods/#operation/getConversationContentAnalysisById)
- [Add conversation by file id or download url. [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/AddConversationByFileIdOrDownloadUrlDeprecated)
- [Get conversation content analysis [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationContentAnalysisDeprecated)
- [Upload IQ file](/docs/api/rest/reference/iq/methods/#operation/UploadZraFile)
- [Initiate and complete a multipart upload.](/docs/api/rest/reference/iq/methods/#operation/InitiateAndCompleteAMultipartUpload)
- [Get conversation information [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getConversationInfoDeprecated)
- [Add conversation by file id or download url.](/docs/api/rest/reference/iq/methods/#operation/AddConversationByFileIdOrDownloadUrl)
- [Delete conversation by conversation ID](/docs/api/rest/reference/iq/methods/#operation/deleteConversationById)

### iq_deal:read

Retrieve ZoomIQ Deal information with activity

**Associated APIs:**

- [List deals [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/listDealsDeprecated)
- [Get deal information](/docs/api/rest/reference/iq/methods/#operation/getDealDetail)
- [List deals](/docs/api/rest/reference/iq/methods/#operation/listAllDeals)
- [Get deal activities](/docs/api/rest/reference/iq/methods/#operation/geAllActivitiesFromDeal)
- [Get deal information [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getDealInfoDeprecated)
- [Get deal activities [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getDealActivitiesDeprecated)

### iq_deal:read:admin

Retrieve ZoomIQ Deal information with activity

**Associated APIs:**

- [Get deal information](/docs/api/rest/reference/iq/methods/#operation/getDealDetail)
- [List deals [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/listDealsDeprecated)
- [Get deal information [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getDealInfoDeprecated)
- [Get deal activities [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getDealActivitiesDeprecated)
- [Get deal activities](/docs/api/rest/reference/iq/methods/#operation/geAllActivitiesFromDeal)
- [List deals](/docs/api/rest/reference/iq/methods/#operation/listAllDeals)

### iq_deal:write

View and manage deal activities

**Associated APIs:**

- [List deals [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/listDealsDeprecated)
- [Get deal information](/docs/api/rest/reference/iq/methods/#operation/getDealDetail)
- [Get deal activities [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getDealActivitiesDeprecated)
- [Delete activity from the deal](/docs/api/rest/reference/iq/methods/#operation/DeleteActivityFromDeal)
- [Get deal information [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getDealInfoDeprecated)
- [Get deal activities](/docs/api/rest/reference/iq/methods/#operation/geAllActivitiesFromDeal)
- [Delete activity from the deal [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/DeleteActivityFromTheDealDeprecated)
- [List deals](/docs/api/rest/reference/iq/methods/#operation/listAllDeals)

### iq_deal:write:admin

View and manage deal activities

**Associated APIs:**

- [Delete activity from the deal [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/DeleteActivityFromTheDealDeprecated)
- [Get deal activities [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getDealActivitiesDeprecated)
- [Delete activity from the deal](/docs/api/rest/reference/iq/methods/#operation/DeleteActivityFromDeal)
- [List deals [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/listDealsDeprecated)
- [Get deal information [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getDealInfoDeprecated)
- [Get deal information](/docs/api/rest/reference/iq/methods/#operation/getDealDetail)
- [List deals](/docs/api/rest/reference/iq/methods/#operation/listAllDeals)
- [Get deal activities](/docs/api/rest/reference/iq/methods/#operation/geAllActivitiesFromDeal)

### iq_playlist:read

View all playlists information

**Associated APIs:**

- [Get a user's playlist [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getUserPlaylistDeprecated)
- [Get a user's playlist](/docs/api/rest/reference/iq/methods/#operation/getUserPlaylists)

### iq_playlist:read:admin

View all playlists information

**Associated APIs:**

- [Get a user's playlist [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/getUserPlaylistDeprecated)
- [Get a user's playlist](/docs/api/rest/reference/iq/methods/#operation/getUserPlaylists)

### iq_team:read

Get team info in User level

**Associated APIs:**

- [List Account Teams](/docs/api/rest/reference/iq/methods/#operation/ListTeams)
- [List Account Teams [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/ListAccountTeamsDeprecated)

### iq_team:read:admin

Get team info

**Associated APIs:**

- [List Account Teams [Deprecated]](/docs/api/rest/reference/iq/methods/#operation/ListAccountTeamsDeprecated)
- [List Unassigned Team Users](/docs/api/rest/reference/iq/methods/#operation/ListUnassignedTeamUsers)
- [Get Team Detail](/docs/api/rest/reference/iq/methods/#operation/GetTeamDetail)
- [List Team Managers](/docs/api/rest/reference/iq/methods/#operation/ListTeamManagers)
- [List Account Teams](/docs/api/rest/reference/iq/methods/#operation/ListTeams)
- [List Team Members](/docs/api/rest/reference/iq/methods/#operation/ListTeamMembers)

### iq_team:write:admin

team resource read&edit

**Associated APIs:**

- [Remove additional access from current team](/docs/api/rest/reference/iq/methods/#operation/DeleteSharedFromTeams)
- [Assign Team Members](/docs/api/rest/reference/iq/methods/#operation/AssignTeamMembers)
- [Move team to new parent](/docs/api/rest/reference/iq/methods/#operation/MoveTeam)
- [Assign Team Managers](/docs/api/rest/reference/iq/methods/#operation/AssignTeamManagers)
- [Unassign Team Managers](/docs/api/rest/reference/iq/methods/#operation/UnassignTeamManagers)
- [Create Team](/docs/api/rest/reference/iq/methods/#operation/CreateTeam)
- [Delete Team](/docs/api/rest/reference/iq/methods/#operation/DeleteTeam)
- [Update Team name](/docs/api/rest/reference/iq/methods/#operation/UpdateTeam)
- [Remove additional access from target teams](/docs/api/rest/reference/iq/methods/#operation/DeleteSharedToTeams)
- [Grant additional access to current team](/docs/api/rest/reference/iq/methods/#operation/AddSharedFromTeams)
- [Unassign Team Members](/docs/api/rest/reference/iq/methods/#operation/UnassignTeamMembers)
- [Grant additional access to target teams](/docs/api/rest/reference/iq/methods/#operation/AddSharedToTeams)

## Zoom Meeting

### meeting_summary:write

View and manage your meeting summaries

**Associated APIs:**

- [Delete a meeting or webinar summary](/docs/api/rest/reference/zoom-api/methods/#operation/Deletemeetingorwebinarsummary)

### meeting_summary:write:admin

View and manage all user meeting summaries

**Associated APIs:**

- [Delete a meeting or webinar summary](/docs/api/rest/reference/zoom-api/methods/#operation/Deletemeetingorwebinarsummary)

## Zoom Quality Management

### qm_interactions:write

Manage the interactions.

### qm_interactions:write:admin

Manage the interactions.

## Zoom User

### division:read:admin

View divisions

**Associated APIs:**

- [List divisions](/docs/api/rest/reference/user/methods/#operation/listDivisions)
- [Get a division](/docs/api/rest/reference/user/methods/#operation/Getdivision)
- [List division members](/docs/api/rest/reference/user/methods/#operation/listDivisionMembers)

### division:wirte:admin

View and manage divisions

**Associated APIs:**

- [Create a division](/docs/api/rest/reference/user/methods/#operation/Createadivision)
- [Update a division](/docs/api/rest/reference/user/methods/#operation/Updateadivision)
- [Get a division](/docs/api/rest/reference/user/methods/#operation/Getdivision)
- [Assign a division](/docs/api/rest/reference/user/methods/#operation/assigndivisionMember)
- [Delete a division](/docs/api/rest/reference/user/methods/#operation/Deletedivision)

## Zoom Video Management

### video_mgmt_channels:read

View video channels information

**Associated APIs:**

- [List channels](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/listVideoChannels)
- [List channel permissions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/listChannelPermissions)
- [List channel videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListChannelVideos)
- [List channel playlists](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListChannelPlaylists)
- [Get channel details](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/getChannelDetail)

### video_mgmt_channels:read:admin

View video channels information

**Associated APIs:**

- [List channel permissions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/listChannelPermissions)
- [Get channel details](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/getChannelDetail)
- [List channel playlists](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListChannelPlaylists)
- [List channel videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListChannelVideos)
- [List channels](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/listVideoChannels)

### video_mgmt_channels:write

Manage video channels

**Associated APIs:**

- [Add channel playlists](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/AddChannelPlaylists)
- [Delete channel](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeleteChannel)
- [Channel actions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/channelActions)
- [Update channel](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/UpdateVideoChannel)
- [Create a channel](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/createChannel)
- [Delete channel videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeleteChannelVideos)
- [Create channel permissions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/createChannelPermissions)
- [Delete channel permissions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeleteChannelPermissions)
- [Add channel videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/AddChannelVideos)
- [Delete channel playlists](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeleteChannelPlaylists)
- [Update channel permissions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/updateChannelPermissions)

### video_mgmt_channels:write:admin

Manage video channels

**Associated APIs:**

- [Add channel playlists](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/AddChannelPlaylists)
- [Channel actions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/channelActions)
- [Update channel](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/UpdateVideoChannel)
- [Delete channel permissions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeleteChannelPermissions)
- [Add channel videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/AddChannelVideos)
- [Delete channel videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeleteChannelVideos)
- [Update channel permissions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/updateChannelPermissions)
- [Create a channel](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/createChannel)
- [Create channel permissions](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/createChannelPermissions)
- [Delete channel playlists](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeleteChannelPlaylists)
- [Delete channel](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeleteChannel)

### video_mgmt_file:write

Upload file to video management

**Associated APIs:**

- [Upload file for video management](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/uploadVODtFile)

### video_mgmt_file:write:admin

upload a file to video management

**Associated APIs:**

- [Upload file for video management](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/uploadVODtFile)

### video_mgmt_playlists:read

View playlists

**Associated APIs:**

- [List playlist videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListPlaylistVideos)
- [List playlists](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListPlaylists)

### video_mgmt_playlists:read:admin

View playlists

**Associated APIs:**

- [List playlists](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListPlaylists)
- [List playlist videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListPlaylistVideos)

### video_mgmt_playlists:write

Manage playlists

**Associated APIs:**

- [Delete playlist videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeletePlaylistVideos)
- [Delete playlist](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeletePlaylist)
- [Create a playlist](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/createPlaylist)
- [Update playlist](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/UpdatePlaylist)
- [Add playlist videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/AddPlaylistVideos)

### video_mgmt_playlists:write:admin

Manage playlists

**Associated APIs:**

- [Create a playlist](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/createPlaylist)
- [Delete playlist](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeletePlaylist)
- [Update playlist](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/UpdatePlaylist)
- [Delete playlist videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/DeletePlaylistVideos)
- [Add playlist videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/AddPlaylistVideos)

### video_mgmt_videos:read

View videos information

**Associated APIs:**

- [List all videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListAllVideos)

### video_mgmt_videos:read:admin

View videos information

**Associated APIs:**

- [List all videos](/docs/api/rest/reference/https:/developers.zoom.us/docs/api/methods/#operation/ListAllVideos)

## ZoomCommerce

### zoom_commerce:read:admin

Zoom commerce API read access for account admin

**Associated APIs:**

- [Gets all quotes for a Zoom partner](/docs/api/rest/reference/commerce/methods/#operation/getAllQuotes)
- [Gets all valid Deal Registrations for a partner](/docs/api/rest/reference/commerce/methods/#operation/getAllDealRegs)
- [Get the list of all accounts associated with a Zoom Partner/Sub-Reseller, by the account type](/docs/api/rest/reference/commerce/methods/#operation/getAllAccounts)
- [Gets details of all files associated with a quote or deal registration](/docs/api/rest/reference/commerce/methods/#operation/allFileDetails)
- [Get detailed information about a specific invoice for a distributor or a reseller](/docs/api/rest/reference/commerce/methods/#operation/getInvoiceDetail)
- [Gets the PDF document for the billing document ID](/docs/api/rest/reference/commerce/methods/#operation/downloadBillingDoc)
- [Gets details of a deal registration by the deal registration](/docs/api/rest/reference/commerce/methods/#operation/getDealRegDetails)
- [Retrieves all valid Zoom Campaigns which a deal registration can be associated with.](/docs/api/rest/reference/commerce/methods/#operation/getCampaigns)
- [Gets the details for a Zoom product or offer.](/docs/api/rest/reference/commerce/methods/#operation/getOfferDetail)
- [Gets all orders for a Zoom partner.](/docs/api/rest/reference/commerce/methods/#operation/getAllOrders)
- [Download a file associated with a quote or deal registration.](/docs/api/rest/reference/commerce/methods/#operation/downloadFile.)
- [Gets Zoom Product Catalog for a Zoom Partner](/docs/api/rest/reference/commerce/methods/#operation/getOffers)
- [Get trial details for an end customer by their Zoom account number or the trial ID](/docs/api/rest/reference/commerce/methods/#operation/getTrialDetails)
- [Gets subscription details for a given subscription number](/docs/api/rest/reference/commerce/methods/#operation/getSubscriptionDetails)
- [Gets all billing documents for a distributor or a reseller](/docs/api/rest/reference/commerce/methods/#operation/getAllBillingDocs)
- [Get order details by order reference ID](/docs/api/rest/reference/commerce/methods/#operation/getOrderDetails)
- [Get quote details by quote reference ID](/docs/api/rest/reference/commerce/methods/#operation/getQuoteDetails)
- [Gets subscription changes/versions for a given subscription number.](/docs/api/rest/reference/commerce/methods/#operation/getSubscriptionVersions)
- [Get trial subscriptions for a Zoom partner](/docs/api/rest/reference/commerce/methods/#operation/getAllTrialSubscriptions)
- [Get the account details for a Zoom Partner/Subreseller/End Customer](/docs/api/rest/reference/commerce/methods/#operation/getAccountDetails)
- [Gets the pricebook in a downloadable file](/docs/api/rest/reference/commerce/methods/#operation/downloadPricebook)
- [Gets paid subscriptions for a Zoom partner.](/docs/api/rest/reference/commerce/methods/#operation/getAllSubscriptions)

### zoom_commerce:write:admin

Zoom Commerce API write access for account admin

**Associated APIs:**

- [Create an end customer account](/docs/api/rest/reference/commerce/methods/#operation/createAccount)
- [Update a subscription quote for a Zoom partner](/docs/api/rest/reference/commerce/methods/#operation/updateQuote)
- [Preview delta order metrics and subscriptions in an order](/docs/api/rest/reference/commerce/methods/#operation/createOrderPreview)
- [Upload an attachment pdf file in context of a deal registration or quote](/docs/api/rest/reference/commerce/methods/#operation/uploadFile)
- [Updates an existing deal registration](/docs/api/rest/reference/commerce/methods/#operation/Updatesanexistingdealregistration)
- [Create a subscription order for a Zoom partner](/docs/api/rest/reference/commerce/methods/#operation/createOrder)
- [Preview delta quote metrics and subscriptions in a quote](/docs/api/rest/reference/commerce/methods/#operation/createQuotePreview)
- [Add contacts to an existing end customer or your own account.](/docs/api/rest/reference/commerce/methods/#operation/addAccountContact)
- [Creates a new deal registration for a partner](/docs/api/rest/reference/commerce/methods/#operation/createDealReg)
- [Create a subscription quote for a Zoom Partner](/docs/api/rest/reference/commerce/methods/#operation/createQuote)
- [Submits a subscription quote for provisioning](/docs/api/rest/reference/commerce/methods/#operation/provisionQuote)

## ZoomVirtualAgent

### zva:read:km_kbs

View your knowledge bases and articles

**Associated APIs:**

- [Get article](/docs/api/rest/reference/virtual-agent/methods/#operation/GetArticle)
- [Get articles](/docs/api/rest/reference/virtual-agent/methods/#operation/GetArticles)
- [Get sync](/docs/api/rest/reference/virtual-agent/methods/#operation/GetSync)

### zva:write:km_kbs

View and manage your knowledge bases and articles

**Associated APIs:**

- [Create sync request](/docs/api/rest/reference/virtual-agent/methods/#operation/CreateSyncRequest)
- [Create article](/docs/api/rest/reference/virtual-agent/methods/#operation/CreateArticle)
- [Delete article](/docs/api/rest/reference/virtual-agent/methods/#operation/DeleteArticle)
- [Update article](/docs/api/rest/reference/virtual-agent/methods/#operation/UpdateArticle)

### zva_report:read

View zva engagements

**Associated APIs:**

- [Get ZVA query details](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVAQueryDetails)
- [Get ZVA transcripts](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVATranscripts)
- [Get ZVA variable details](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVAengagementvariabledetails)
- [Get ZVA engagements](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVAEngagements)
- [Get ZVA Surveys](/docs/api/rest/reference/virtual-agent/methods/#operation/GetZVASurveys)

## workforce_management

### workforce_management:read:admin

View workforce management information

**Associated APIs:**

- [Next Migrate scopes](/docs/integrations/migrate/)
- [GitHub](https://github.com/zoom)
- [Youtube](https://www.youtube.com/@ZoomDevelopers)
- [Developer Forum](https://devforum.zoom.us/)
- [Help](/support/)
- [Terms](https://zoom.us/terms)
- [Privacy Policy](https://zoom.us/privacy)
- [API Terms of Use](https://explore.zoom.us/docs/en-us/zoom_api_license_and_tou.html)
- [Marketplace Developer Agreement](https://explore.zoom.us/en/marketplace-developer-agreement/)

