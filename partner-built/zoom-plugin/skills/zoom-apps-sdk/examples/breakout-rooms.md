# Breakout Room Integration

Detect breakout rooms, track room changes, and sync state across rooms.

## Overview

When a meeting uses breakout rooms, each room gets its own meeting UUID. Your app needs to handle room transitions and optionally sync state between rooms.

## Key Concepts

| Property | Description |
|----------|-------------|
| `meetingUUID` | Unique per room (changes when moving to breakout) |
| `parentUUID` | Original meeting UUID (available in breakout rooms) |
| `onBreakoutRoomChange` | Event fired when user moves between rooms |

## Detecting Room Changes

```javascript
import zoomSdk from '@zoom/appssdk';

await zoomSdk.config({
  capabilities: [
    'getMeetingUUID', 'getMeetingContext',
    'onBreakoutRoomChange'
  ],
  version: '0.16'
});

// Get current room info
const { meetingUUID } = await zoomSdk.getMeetingUUID();
console.log('Current room UUID:', meetingUUID);

// Listen for room changes
zoomSdk.addEventListener('onBreakoutRoomChange', async (event) => {
  console.log('Room changed:', event);

  // Get new room UUID
  const { meetingUUID: newUUID } = await zoomSdk.getMeetingUUID();
  console.log('Now in room:', newUUID);

  // Re-initialize room-specific state
  await loadRoomState(newUUID);
});
```

## Cross-Room State Sync

Use your backend to sync state across rooms. The `parentUUID` links all breakout rooms to the main meeting.

```javascript
// Frontend: Register with backend on room entry
async function registerRoom() {
  const { meetingUUID } = await zoomSdk.getMeetingUUID();
  const context = await zoomSdk.getMeetingContext();

  await fetch('/api/room/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      roomUUID: meetingUUID,
      parentUUID: context.parentUUID || meetingUUID,
      // parentUUID is null in main room, set in breakout rooms
    })
  });
}

// Backend: Aggregate state across all rooms
app.get('/api/meeting/:parentUUID/state', async (req, res) => {
  const rooms = await db.find({ parentUUID: req.params.parentUUID });
  const aggregated = rooms.reduce((acc, room) => {
    // Merge state from all rooms
    return { ...acc, ...room.state };
  }, {});
  res.json(aggregated);
});
```

## Managing Breakout Rooms via REST API

Create and manage breakout rooms from your backend using the Zoom REST API:

```javascript
// Create breakout rooms (requires meeting:write scope)
const response = await axios.post(
  `https://api.zoom.us/v2/meetings/${meetingId}/batch_registrants`,
  {
    rooms: [
      { name: 'Room 1', participants: ['user1@example.com'] },
      { name: 'Room 2', participants: ['user2@example.com'] }
    ]
  },
  { headers: { 'Authorization': `Bearer ${accessToken}` } }
);
```

## Pattern: Room-Specific vs Global State

```javascript
const { meetingUUID } = await zoomSdk.getMeetingUUID();
const context = await zoomSdk.getMeetingContext();
const parentUUID = context.parentUUID || meetingUUID;

// Room-specific state (e.g., room discussion notes)
const roomState = await loadState(`room:${meetingUUID}`);

// Global state (e.g., meeting agenda visible in all rooms)
const globalState = await loadState(`meeting:${parentUUID}`);
```

## Resources

- **Breakout rooms docs**: https://developers.zoom.us/docs/zoom-apps/guides/breakout-rooms/
