# Chat

Complete guide to implementing chat functionality in the Zoom Video SDK for Web.

## Getting the Chat Client

```javascript
// Get chat client after joining session
const chatClient = client.getChatClient();
```

## Sending Messages

### Send to Everyone

```javascript
// Send to all participants
await chatClient.sendToAll('Hello everyone!');
```

### Send to Specific User

```javascript
// Send private message to specific user
const userId = 12345;
await chatClient.send('Hello!', userId);
```

### Get Available Receivers

```javascript
// Get list of users you can send messages to
const receivers = chatClient.getReceivers();
receivers.forEach(user => {
  console.log(user.displayName, user.userId);
});
```

## Receiving Messages

```javascript
// Listen for incoming messages
client.on('chat-on-message', (payload) => {
  const {
    id,          // Message ID
    message,     // Message text
    sender,      // { userId, name, avatar }
    receiver,    // { userId, name } or 'everyone'
    timestamp,   // Unix timestamp
    isPrivate,   // Boolean - is this a private message
  } = payload;

  console.log(`[${sender.name}]: ${message}`);
  
  if (isPrivate) {
    console.log('(Private message)');
  }
  
  addMessageToUI(payload);
});
```

## Chat History

```javascript
// Get chat history for current session
const history = chatClient.getHistory();

history.forEach(msg => {
  console.log(`${msg.sender.name}: ${msg.message}`);
});
```

## Chat Privileges

### Check Current Privilege

```javascript
import { ChatPrivilege } from '@zoom/videosdk';

const privilege = chatClient.getPrivilege();

switch (privilege) {
  case ChatPrivilege.All:
    // Can chat to everyone and privately
    break;
  case ChatPrivilege.NoOne:
    // Cannot send chat
    break;
  case ChatPrivilege.EveryonePublicly:
    // Can only send to everyone (no private)
    break;
}
```

### Set Privilege (Host Only)

```javascript
// Host can control chat privileges
await chatClient.setPrivilege(ChatPrivilege.All);           // Allow all chat
await chatClient.setPrivilege(ChatPrivilege.NoOne);         // Disable chat
await chatClient.setPrivilege(ChatPrivilege.EveryonePublicly); // Public only
```

### Listen for Privilege Changes

```javascript
client.on('chat-privilege-change', (payload) => {
  const { chatPrivilege } = payload;
  
  if (chatPrivilege === ChatPrivilege.NoOne) {
    disableChatInput();
    showNotification('Chat has been disabled by host');
  } else {
    enableChatInput();
  }
});
```

## File Transfer

### Check if File Transfer is Enabled

```javascript
const isEnabled = chatClient.isFileTransferEnabled();

if (isEnabled) {
  // Get file transfer settings
  const settings = chatClient.getFileTransferSetting();
  console.log('Max file size:', settings.maxFileSize);
}
```

### Send File

```javascript
// Send file to specific user
const file = document.getElementById('fileInput').files[0];
const userId = 12345;

try {
  const cancelFn = await chatClient.sendFile(file, userId);
  
  // To cancel upload
  // cancelFn();
} catch (error) {
  console.error('File upload failed:', error);
}

// Track upload progress
client.on('chat-file-upload-progress', (payload) => {
  const { fileName, progress, status, fileSize } = payload;
  
  console.log(`Upload ${fileName}: ${progress}%`);
  
  if (status === 'success') {
    console.log('Upload complete');
  } else if (status === 'fail') {
    console.log('Upload failed');
  }
});
```

### Download File

```javascript
// Download file from message
const messageId = 'msg123';
const fileUrl = 'https://...';

try {
  const cancelFn = await chatClient.downloadFile(messageId, fileUrl);
  
  // Or get as blob for display
  const blob = await chatClient.downloadFile(messageId, fileUrl, true);
  const url = URL.createObjectURL(blob);
  // Display image or create download link
} catch (error) {
  console.error('Download failed:', error);
}

// Track download progress
client.on('chat-file-download-progress', (payload) => {
  const { fileName, progress, status, fileBlob } = payload;
  
  console.log(`Download ${fileName}: ${progress}%`);
  
  if (status === 'success' && fileBlob) {
    // File ready
    const url = URL.createObjectURL(fileBlob);
  }
});
```

## Complete Chat Component

```javascript
class ChatManager {
  constructor(client) {
    this.client = client;
    this.chatClient = null;
    this.messages = [];
  }

  init() {
    this.chatClient = this.client.getChatClient();
    this.setupEventListeners();
    this.loadHistory();
  }

  setupEventListeners() {
    // Incoming messages
    this.client.on('chat-on-message', (payload) => {
      this.messages.push(payload);
      this.onMessageReceived(payload);
    });

    // Privilege changes
    this.client.on('chat-privilege-change', (payload) => {
      this.onPrivilegeChange(payload.chatPrivilege);
    });

    // File upload progress
    this.client.on('chat-file-upload-progress', (payload) => {
      this.onUploadProgress(payload);
    });

    // File download progress
    this.client.on('chat-file-download-progress', (payload) => {
      this.onDownloadProgress(payload);
    });
  }

  loadHistory() {
    this.messages = this.chatClient.getHistory();
    this.renderMessages();
  }

  async sendMessage(text, receiverId = null) {
    const privilege = this.chatClient.getPrivilege();
    
    if (privilege === ChatPrivilege.NoOne) {
      throw new Error('Chat is disabled');
    }

    try {
      if (receiverId) {
        await this.chatClient.send(text, receiverId);
      } else {
        await this.chatClient.sendToAll(text);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      throw error;
    }
  }

  async sendFile(file, receiverId) {
    if (!this.chatClient.isFileTransferEnabled()) {
      throw new Error('File transfer is disabled');
    }

    const settings = this.chatClient.getFileTransferSetting();
    if (file.size > settings.maxFileSize) {
      throw new Error(`File too large. Max: ${settings.maxFileSize} bytes`);
    }

    return await this.chatClient.sendFile(file, receiverId);
  }

  getReceivers() {
    return this.chatClient.getReceivers();
  }

  getPrivilege() {
    return this.chatClient.getPrivilege();
  }

  // Override these in your implementation
  onMessageReceived(message) {
    console.log('New message:', message);
    this.renderMessages();
  }

  onPrivilegeChange(privilege) {
    console.log('Privilege changed:', privilege);
  }

  onUploadProgress(progress) {
    console.log('Upload:', progress);
  }

  onDownloadProgress(progress) {
    console.log('Download:', progress);
  }

  renderMessages() {
    // Implement your UI rendering
  }
}

// Usage
const chatManager = new ChatManager(client);
chatManager.init();

// Send message
document.getElementById('send-btn').onclick = async () => {
  const input = document.getElementById('chat-input');
  await chatManager.sendMessage(input.value);
  input.value = '';
};
```

## React Component

```typescript
import React, { useState, useEffect, useRef } from 'react';
import { VideoClient, ChatPrivilege } from '@zoom/videosdk';

interface ChatMessage {
  id: string;
  message: string;
  sender: { userId: number; name: string };
  timestamp: number;
  isPrivate: boolean;
}

interface ChatProps {
  client: typeof VideoClient;
}

export const Chat: React.FC<ChatProps> = ({ client }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [privilege, setPrivilege] = useState<ChatPrivilege>(ChatPrivilege.All);
  const [receivers, setReceivers] = useState<any[]>([]);
  const [selectedReceiver, setSelectedReceiver] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const chatClient = client.getChatClient();

  useEffect(() => {
    // Load history
    setMessages(chatClient.getHistory());
    setReceivers(chatClient.getReceivers());
    setPrivilege(chatClient.getPrivilege());

    // Listen for new messages
    const handleMessage = (payload: ChatMessage) => {
      setMessages(prev => [...prev, payload]);
    };

    // Listen for privilege changes
    const handlePrivilege = (payload: { chatPrivilege: ChatPrivilege }) => {
      setPrivilege(payload.chatPrivilege);
    };

    // Listen for user changes (update receivers)
    const handleUserChange = () => {
      setReceivers(chatClient.getReceivers());
    };

    client.on('chat-on-message', handleMessage);
    client.on('chat-privilege-change', handlePrivilege);
    client.on('user-added', handleUserChange);
    client.on('user-removed', handleUserChange);

    return () => {
      client.off('chat-on-message', handleMessage);
      client.off('chat-privilege-change', handlePrivilege);
      client.off('user-added', handleUserChange);
      client.off('user-removed', handleUserChange);
    };
  }, [client, chatClient]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim()) return;
    if (privilege === ChatPrivilege.NoOne) return;

    try {
      if (selectedReceiver) {
        await chatClient.send(inputValue, selectedReceiver);
      } else {
        await chatClient.sendToAll(inputValue);
      }
      setInputValue('');
    } catch (error) {
      console.error('Send failed:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const isDisabled = privilege === ChatPrivilege.NoOne;

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.isPrivate ? 'private' : ''}`}>
            <span className="sender">{msg.sender.name}</span>
            {msg.isPrivate && <span className="private-badge">(private)</span>}
            <p className="text">{msg.message}</p>
            <span className="time">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </span>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <select
          value={selectedReceiver || ''}
          onChange={(e) => setSelectedReceiver(e.target.value ? Number(e.target.value) : null)}
          disabled={isDisabled || privilege === ChatPrivilege.EveryonePublicly}
        >
          <option value="">Everyone</option>
          {receivers.map((r) => (
            <option key={r.userId} value={r.userId}>
              {r.displayName}
            </option>
          ))}
        </select>

        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={isDisabled ? 'Chat disabled' : 'Type a message...'}
          disabled={isDisabled}
        />

        <button onClick={sendMessage} disabled={isDisabled || !inputValue.trim()}>
          Send
        </button>
      </div>

      {isDisabled && (
        <div className="chat-disabled-notice">
          Chat has been disabled by the host
        </div>
      )}
    </div>
  );
};
```

## Key Points

1. **Get ChatClient after joining** - `client.getChatClient()` only works after `join()`
2. **Check privileges** - Host can disable chat or limit to public only
3. **Handle private messages** - Check `isPrivate` flag in message payload
4. **File transfer** - Check `isFileTransferEnabled()` before sending files
5. **Update receivers list** - Refresh when participants join/leave

## Error Handling

```javascript
try {
  await chatClient.sendToAll('Hello');
} catch (error) {
  switch (error.type) {
    case 'IMPROPER_MEETING_STATE':
      // Not in a session
      break;
    case 'INSUFFICIENT_PRIVILEGES':
      // Chat disabled or no permission
      break;
    case 'INVALID_PARAMETERS':
      // Invalid message or receiver
      break;
  }
}
```

## Related Documentation

- [Event Handling](event-handling.md) - Chat events
- [API Reference](../references/web-reference.md) - Full ChatClient API
