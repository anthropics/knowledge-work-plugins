# Zoom Events API

Authoritative endpoint inventory for Events. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/events/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 90 |
| Path templates | 52 |
| Tags | 17 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Attendee Actions | 4 |
| Co Editors | 2 |
| Emails | 2 |
| Event Access | 5 |
| Events | 6 |
| Exhibitors | 6 |
| Files | 3 |
| Hubs | 5 |
| Registrants | 2 |
| Reports | 7 |
| Sessions | 15 |
| Speakers | 5 |
| Ticket Types | 8 |
| Tickets | 5 |
| Video On-Demand | 9 |
| Video On-Demand Registrations | 4 |
| Videos | 2 |

## Endpoints by Tag

### Attendee Actions

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/events/{eventId}/attendee_action` | List event attendee actions | `ListEventAttendeeActions` |
| PATCH | `/zoom_events/events/{eventId}/attendee_action` | Update event attendee actions | `UpdateEventAttendeeActions` |
| GET | `/zoom_events/events/{eventId}/sessions/{sessionId}/attendee_action` | List session attendee actions | `ListSessionAttendeeActions` |
| PATCH | `/zoom_events/events/{eventId}/sessions/{sessionId}/attendee_action` | Update session attendee actions | `UpdateSessionAttendeeActions` |

### Co Editors

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/events/{eventId}/coeditors` | List coeditors | `getCoEditors` |
| PATCH | `/zoom_events/events/{eventId}/coeditors` | Add or remove event co-editors | `coeditoractions` |

### Emails

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/events/{eventId}/email_types` | List event email types | `listEmailTypes` |
| GET | `/zoom_events/events/{eventId}/email_types/{emailTypeId}/send_status` | List event emails sent status | `listEmailSentStatuses` |

### Event Access

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/events/{eventId}/access_links` | List event access links | `getEventAccessLinks` |
| POST | `/zoom_events/events/{eventId}/access_links` | Create event access link | `createEventAccessLink` |
| DELETE | `/zoom_events/events/{eventId}/access_links/{accessLinkId}` | Delete event access link | `deleteEventAccessLink` |
| GET | `/zoom_events/events/{eventId}/access_links/{accessLinkId}` | Get event access link | `GetEventAccessLink` |
| PATCH | `/zoom_events/events/{eventId}/access_links/{accessLinkId}` | Update event access | `updateEventAccess` |

### Events

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/events` | List events | `getEvents` |
| POST | `/zoom_events/events` | Create an event | `createEvent` |
| DELETE | `/zoom_events/events/{eventId}` | Delete an event | `deleteEvent` |
| GET | `/zoom_events/events/{eventId}` | Get an event | `getEventInfo` |
| PATCH | `/zoom_events/events/{eventId}` | Update an event | `updateEvent` |
| POST | `/zoom_events/events/{eventId}/event_actions` | Event actions | `EventActions` |

### Exhibitors

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/events/{eventId}/exhibitors` | List exhibitors | `getExhibitors` |
| POST | `/zoom_events/events/{eventId}/exhibitors` | Create an exhibitor | `createExhibitor` |
| DELETE | `/zoom_events/events/{eventId}/exhibitors/{exhibitorId}` | Delete an exhibitor | `deleteExhibitor` |
| GET | `/zoom_events/events/{eventId}/exhibitors/{exhibitorId}` | Get an exhibitor | `getExhibitorInfo` |
| PATCH | `/zoom_events/events/{eventId}/exhibitors/{exhibitorId}` | Update exhibitor for an event | `updateExhibitor` |
| GET | `/zoom_events/events/{eventId}/sponsor_tiers` | List sponsor tiers | `ListSponsorTiers` |

### Files

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/zoom_events/files` | Upload events file | `uploadEventFile` |
| POST | `/zoom_events/files/multipart` | Upload events multipart files | `uploadMultipartEventFile` |
| POST | `/zoom_events/files/multipart/upload` | Initiate and complete the multipart file upload | `initiateAndCompleteAEventMultipartUpload.` |

### Hubs

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/hubs` | List hubs | `getHubList` |
| GET | `/zoom_events/hubs/{hubId}/hosts` | List hub Hosts | `gethubhostList` |
| POST | `/zoom_events/hubs/{hubId}/hosts` | Creates a new hub host | `createHubHost` |
| DELETE | `/zoom_events/hubs/{hubId}/hosts/{hostUserId}` | Remove hub host | `deleteHubHost` |
| GET | `/zoom_events/hubs/{hubId}/videos` | List hub videos | `ListHubVideos` |

### Registrants

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/events/{eventId}/registrants` | List registrants | `getRegistrants` |
| GET | `/zoom_events/events/{eventId}/sessions/{sessionId}/attendees` | List session attendees | `getSessionAttendeeList` |

### Reports

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/events/{eventId}/reports/chat_transcripts` | Get chat transcripts report | `ChatTranscriptsReport` |
| GET | `/zoom_events/events/{eventId}/reports/custom_reports/{customReportId}` | Get custom report | `getCustomEventReport` |
| GET | `/zoom_events/events/{eventId}/reports/event_attendance` | Get event attendance (Live or Lobby) report | `EventAttendanceReport` |
| GET | `/zoom_events/events/{eventId}/reports/sessions/{sessionId}/attendance` | Get session attendance report | `SessionAttendanceReport` |
| GET | `/zoom_events/events/{eventId}/reports/survey` | Get event survey report | `EventSurveyReportApi` |
| GET | `/zoom_events/events/{eventId}/reports/ticket_registration` | Get event registrations report | `EventRegistrationsReport` |
| GET | `/zoom_events/hubs/{hubId}/vod_channels/{channelId}/reports/registrations` | Get VOD channel registration report | `VodChannelReigistration` |

### Sessions

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/events/{eventId}/sessions` | List sessions | `getEventSessionList` |
| POST | `/zoom_events/events/{eventId}/sessions` | Create a session | `createEventSession` |
| DELETE | `/zoom_events/events/{eventId}/sessions/{sessionId}` | Delete a session | `deleteEventSession` |
| GET | `/zoom_events/events/{eventId}/sessions/{sessionId}` | Get the session information | `getEventSessionInfo` |
| PATCH | `/zoom_events/events/{eventId}/sessions/{sessionId}` | Update a session | `updateEventSession` |
| GET | `/zoom_events/events/{eventId}/sessions/{sessionId}/interpreters` | List session interpreters | `getSessionInterpreterList` |
| PUT | `/zoom_events/events/{eventId}/sessions/{sessionId}/interpreters` | Create or update session interpreters | `updateSessionInterpreters` |
| GET | `/zoom_events/events/{eventId}/sessions/{sessionId}/join_token` | Get ticket session join token by Event ID and Session ID | `getSessionJoinToken` |
| GET | `/zoom_events/events/{eventId}/sessions/{sessionId}/livestream` | Get session livestream configuration | `getSessionLivestreamConfiguration` |
| PATCH | `/zoom_events/events/{eventId}/sessions/{sessionId}/livestream` | Update session livestream configuration | `UpdateSessionLivestreamConfiguration` |
| GET | `/zoom_events/events/{eventId}/sessions/{sessionId}/polls` | List session polls | `getSessionPolls` |
| PUT | `/zoom_events/events/{eventId}/sessions/{sessionId}/polls` | Create or update session polls | `updateSessionPolls` |
| DELETE | `/zoom_events/events/{eventId}/sessions/{sessionId}/reservations` | Delete session reservations | `DeleteSessionReservations` |
| GET | `/zoom_events/events/{eventId}/sessions/{sessionId}/reservations` | List session reservations | `ListSessionReservations` |
| POST | `/zoom_events/events/{eventId}/sessions/{sessionId}/reservations` | Add session reservations | `AddSessionReservations` |

### Speakers

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/events/{eventId}/speakers` | List speakers | `getSpeakers` |
| POST | `/zoom_events/events/{eventId}/speakers` | Create a speaker | `createSpeaker` |
| DELETE | `/zoom_events/events/{eventId}/speakers/{speakerId}` | Delete a speaker | `deleteSpeaker` |
| GET | `/zoom_events/events/{eventId}/speakers/{speakerId}` | Get a speaker | `getSpeaker` |
| PATCH | `/zoom_events/events/{eventId}/speakers/{speakerId}` | Update a speaker | `updateSpeaker` |

### Ticket Types

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/events/{eventId}/questions` | List registration questions for an event | `getRegistrationQuestionsForEvent` |
| PUT | `/zoom_events/events/{eventId}/questions` | Update registration questions for an event | `updateRegistrationQuestionsForEvent` |
| GET | `/zoom_events/events/{eventId}/ticket_types` | List ticket types | `getEventTicketTypes` |
| POST | `/zoom_events/events/{eventId}/ticket_types` | Create an event ticket type | `createTicketType` |
| DELETE | `/zoom_events/events/{eventId}/ticket_types/{ticketTypeId}` | Delete a ticket type | `deleteEventTicketType` |
| PATCH | `/zoom_events/events/{eventId}/ticket_types/{ticketTypeId}` | Update ticket type for an event | `updateTicketType` |
| GET | `/zoom_events/events/{eventId}/ticket_types/{ticketTypeId}/questions` | List registration questions for ticket type | `getRegistrationQuestionsForTicketType` |
| PUT | `/zoom_events/events/{eventId}/ticket_types/{ticketTypeId}/questions` | Update registration questions for ticket type | `updateRegistrationQuestionsForTicketType` |

### Tickets

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/events/{eventId}/tickets` | List tickets | `getTickets` |
| POST | `/zoom_events/events/{eventId}/tickets` | Create tickets | `createTickets` |
| DELETE | `/zoom_events/events/{eventId}/tickets/{ticketId}` | Delete a ticket | `deleteTicket` |
| GET | `/zoom_events/events/{eventId}/tickets/{ticketId}` | Get a ticket | `getTicketDetails` |
| PATCH | `/zoom_events/events/{eventId}/tickets/{ticketId}` | Update ticket | `Updateticket` |

### Video On-Demand

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/hubs/{hubId}/vod_channels` | List channels | `getVODChannels` |
| POST | `/zoom_events/hubs/{hubId}/vod_channels` | Create VOD channel | `createVodChannel` |
| DELETE | `/zoom_events/hubs/{hubId}/vod_channels/{channelId}` | Delete VOD Channel | `DeleteVODChannel` |
| GET | `/zoom_events/hubs/{hubId}/vod_channels/{channelId}` | Get VOD channel details | `getVODChannelDetail` |
| PATCH | `/zoom_events/hubs/{hubId}/vod_channels/{channelId}` | Update VOD channel | `UpdateVideoChannel` |
| POST | `/zoom_events/hubs/{hubId}/vod_channels/{channelId}/actions` | VOD channel actions | `vodChannelActions` |
| GET | `/zoom_events/hubs/{hubId}/vod_channels/{channelId}/videos` | List VOD channel videos | `ListVODChannelVideos` |
| POST | `/zoom_events/hubs/{hubId}/vod_channels/{channelId}/videos` | Add VOD channel videos | `AddVODChannelVideos` |
| DELETE | `/zoom_events/hubs/{hubId}/vod_channels/{channelId}/videos/{videoId}` | Delete VOD channel video | `DeleteVODChannelVideo` |

### Video On-Demand Registrations

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/hubs/{hubId}/vod_channels/{channelId}/registration_questions` | Get VOD Registration Questions | `getRegistrationQuestionsForVODChannel` |
| PUT | `/zoom_events/hubs/{hubId}/vod_channels/{channelId}/registration_questions` | update VOD channel registration questions | `updateRegistrationQuestionsForVODchannel` |
| GET | `/zoom_events/hubs/{hubId}/vod_channels/{channelId}/registrations` | List VOD Registration | `ListVODRegistration` |
| POST | `/zoom_events/hubs/{hubId}/vod_channels/{channelId}/registrations` | VOD channel registration | `VODTicketRegistration` |

### Videos

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/zoom_events/videos/{videoId}/metadata` | Get metadata for a specific video | `getVideoMetadata` |
| PATCH | `/zoom_events/videos/{videoId}/metadata` | Update metadata for a specific video. | `updateVideoMetadata` |
