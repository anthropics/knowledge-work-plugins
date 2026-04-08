# Zoom Video Management API

Authoritative endpoint inventory for Video Management. This file mirrors the official Zoom API Hub OpenAPI document for this product area.

## Canonical Source

- OpenAPI JSON: https://developers.zoom.us/api-hub/video-management/methods/endpoints.json
- Base URL: `https://api.zoom.us/v2`
- Authentication details: [authentication.md](authentication.md)

## Notes

- Endpoint methods and paths below are generated from the official Zoom API Hub `paths` object.
- Scope names are defined per operation and frequently use granular scope names. Check the API Hub operation page for the exact scopes before implementation.
- Use this file for endpoint discovery and inventory. Use `../examples/` for orchestration patterns, not as the canonical source of path names.

## Coverage

| Metric | Value |
|--------|-------|
| Endpoint operations | 25 |
| Path templates | 11 |
| Tags | 5 |

## Tag Index

| Tag | Operations |
|-----|------------|
| Channels | 6 |
| files | 1 |
| Permissions | 4 |
| Playlists | 7 |
| Videos | 7 |

## Endpoints by Tag

### Channels

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| GET | `/video_management/channels` | List channels | `listVideoChannels` |
| POST | `/video_management/channels` | Create a channel | `createChannel` |
| DELETE | `/video_management/channels/{channelId}` | Delete channel | `DeleteChannel` |
| GET | `/video_management/channels/{channelId}` | Get channel details | `getChannelDetail` |
| PATCH | `/video_management/channels/{channelId}` | Update channel | `UpdateVideoChannel` |
| PATCH | `/video_management/channels/{channelId}/actions` | Channel actions | `channelActions` |

### files

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| POST | `/video_management/files` | Upload file for video management | `uploadVODtFile` |

### Permissions

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/video_management/channels/{channelId}/permissions` | Delete channel permissions | `DeleteChannelPermissions` |
| GET | `/video_management/channels/{channelId}/permissions` | List channel permissions | `listChannelPermissions` |
| PATCH | `/video_management/channels/{channelId}/permissions` | Update channel permissions | `updateChannelPermissions` |
| POST | `/video_management/channels/{channelId}/permissions` | Create channel permissions | `createChannelPermissions` |

### Playlists

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/video_management/channels/{channelId}/playlists` | Delete channel playlists | `DeleteChannelPlaylists` |
| GET | `/video_management/channels/{channelId}/playlists` | List channel playlists | `ListChannelPlaylists` |
| POST | `/video_management/channels/{channelId}/playlists` | Add channel playlists | `AddChannelPlaylists` |
| GET | `/video_management/playlists` | List playlists | `ListPlaylists` |
| POST | `/video_management/playlists` | Create a playlist | `createPlaylist` |
| DELETE | `/video_management/playlists/{playlistId}` | Delete playlist | `DeletePlaylist` |
| PATCH | `/video_management/playlists/{playlistId}` | Update playlist | `UpdatePlaylist` |

### Videos

| Method | Endpoint | Summary | Operation ID |
|--------|----------|---------|-------------|
| DELETE | `/video_management/channels/{channelId}/videos` | Delete channel videos | `DeleteChannelVideos` |
| GET | `/video_management/channels/{channelId}/videos` | List channel videos | `ListChannelVideos` |
| POST | `/video_management/channels/{channelId}/videos` | Add channel videos | `AddChannelVideos` |
| DELETE | `/video_management/playlists/{playlistId}/videos` | Delete playlist videos | `DeletePlaylistVideos` |
| GET | `/video_management/playlists/{playlistId}/videos` | List playlist videos | `ListPlaylistVideos` |
| POST | `/video_management/playlists/{playlistId}/videos` | Add playlist videos | `AddPlaylistVideos` |
| GET | `/video_management/videos` | List all videos | `ListAllVideos` |
