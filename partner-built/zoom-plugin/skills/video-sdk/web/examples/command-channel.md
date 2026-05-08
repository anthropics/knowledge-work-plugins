# Command Channel

Complete working code for custom command messaging between participants on Web.

---

## Overview

The command channel enables custom data exchange between participants within the same session. Use cases:
- Application-specific signaling
- Session transfer / waiting room coordination
- Real-time collaboration data
- Custom control messages

```
+-------------------------------------------------------------------+
|                    COMMAND CHANNEL FLOW (Web)                      |
+-------------------------------------------------------------------+
|  Setup:                                                           |
|    client.join() -> client.getCommandClient()                     |
|                                                                   |
|  Sender:                                                          |
|    cmdClient.send(message)           [broadcast to all]           |
|    cmdClient.send(message, userId)   [targeted]                   |
|                                                                   |
|  Receiver:                                                        |
|    client.on('command-channel-message', callback)                 |
|                                                                   |
|  IMPORTANT: Command channel is SESSION-SCOPED.                    |
|  It does NOT span across different sessions.                      |
+-------------------------------------------------------------------+
```

**Key difference from native SDKs**: Web uses `getCommandClient()` (NOT `getCmdChannel()` like Linux/Windows native SDKs).

---

## Limitations

| Limit | Value |
|-------|-------|
| Max message rate | 60 messages/second |
| Max message size | ~1KB recommended |
| Reliability | Best effort (not guaranteed) |
| Scope | Same session only |

**Note**: Commands are not persisted - late joiners won't receive previous commands.

---

## Setup Order (Critical)

You MUST call `getCommandClient()` and register listeners AFTER `client.join()`. The command channel subsystem is not active until after joining a session.

```javascript
// CORRECT: Everything after join
await client.join(topic, jwt, userName);
const cmdClient = client.getCommandClient();
client.on('command-channel-status', (status) => { /* ... */ });
client.on('command-channel-message', (payload) => { /* ... */ });
```

```javascript
// WRONG: Registering before join — command channel not active yet
await client.init('en-US', 'Global', { patchJsMedia: true });
client.on('command-channel-message', handler);  // WILL NOT RECEIVE MESSAGES
await client.join(topic, jwt, userName);
```

Without calling `getCommandClient()` after join, the command channel may never connect and `command-channel-status` will never fire.

---

## Complete Working Example

```javascript
import ZoomVideo from '@zoom/videosdk';

const client = ZoomVideo.createClient();

async function joinAndSetupCommandChannel(topic, jwt, userName) {
    // 1. Initialize
    await client.init('en-US', 'Global', { patchJsMedia: true });

    // 2. Join session
    await client.join(topic, jwt, userName);

    // 3. Activate command channel (MUST be after join)
    const cmdClient = client.getCommandClient();

    // 4. Listen for connection status
    client.on('command-channel-status', (status) => {
        console.log('Command channel status:', status);
        if (status === true) {
            console.log('Command channel connected - ready to send');
        }
    });

    // 5. Listen for incoming commands
    client.on('command-channel-message', (payload) => {
        try {
            const data = JSON.parse(payload.text);
            console.log('Command received:', data);
            handleCommand(data);
        } catch (e) {
            console.log('Raw command received:', payload.text);
        }
    });

    return cmdClient;
}

// Send a command (broadcast to all participants in session)
function sendCommand(cmdClient, type, data) {
    const message = JSON.stringify({ type, data });
    cmdClient.send(message);
}

// Send to a specific participant
function sendCommandToUser(cmdClient, userId, type, data) {
    const message = JSON.stringify({ type, data });
    cmdClient.send(message, userId);
}

// Handle incoming commands
function handleCommand(data) {
    switch (data.type) {
        case 'ping':
            console.log('Received ping');
            break;
        case 'transfer':
            console.log('Transfer info:', data);
            break;
        default:
            console.log('Unknown command type:', data.type);
    }
}
```

---

## Events Reference

### command-channel-status

Fires when the command channel connection status changes.

```javascript
client.on('command-channel-status', (status) => {
    // status: boolean - true when connected, false when disconnected
    if (status) {
        // Safe to send commands now
    }
});
```

### command-channel-message

Fires when a command is received from another participant.

```javascript
client.on('command-channel-message', (payload) => {
    // payload.text: string - the command message content
    // payload.senderId: number - user ID of the sender
    const message = payload.text;
    console.log('Received:', message);
});
```

---

## Cross-Platform Compatibility

When sending commands between Web and Linux/Windows native SDKs:

| Property | Web SDK | Linux SDK | Windows SDK |
|----------|---------|-----------|-------------|
| Get channel | `getCommandClient()` | `getCmdChannel()` | `getCmdChannel()` |
| Send broadcast | `cmdClient.send(msg)` | `sendCommand(nullptr, msg)` | `sendCommand(NULL, msg)` |
| Send targeted | `cmdClient.send(msg, userId)` | `sendCommand(user, msg)` | `sendCommand(user, msg)` |
| String type | JavaScript string | `const char*` (UTF-8) | `const wchar_t*` (wide) |
| Receive event | `command-channel-message` | `onCommandReceived` callback | `onCommandReceived` callback |

Use JSON strings as the message format for cross-platform compatibility.

---

## Common Issues

### Commands Not Received

**Cause**: `getCommandClient()` not called after join, or listeners registered before join

**Fix**: Ensure setup order is correct — join first, then getCommandClient(), then register listeners.

### command-channel-status Never Fires

**Cause**: `getCommandClient()` was not called

**Fix**: You must explicitly call `client.getCommandClient()` after join to activate the channel.

### Cross-SDK Messages Not Arriving

**Cause**: Version mismatch or timing issues between different SDK platforms

**Fix**: Add a server-side polling fallback:
```javascript
const pollTimer = setInterval(async () => {
    const res = await fetch(`/api/status/${sessionName}`);
    const data = await res.json();
    if (data.ready) {
        clearInterval(pollTimer);
        handleData(data);
    }
}, 3000);
```

---

## Related Documentation

- [Session Join Pattern](session-join-pattern.md) - Session setup
- [Event Handling](event-handling.md) - Event listener patterns
- [Linux Command Channel](../../linux/examples/command-channel.md) - Linux native equivalent
- [Windows Command Channel](../../windows/examples/command-channel.md) - Windows native equivalent
- [Authorization](../../references/authorization.md) - JWT roleType for host/co-host
