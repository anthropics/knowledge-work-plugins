# LLM Integration

Use an LLM to interpret user intent from Team Chat messages, then call Zoom APIs or respond with rich message cards.

Recommended flow:

1. Receive `bot_notification` event.
2. Extract user text and channel context.
3. Classify intent with your LLM (meeting actions, help, status).
4. Execute safe backend actions (for example, create/list meetings).
5. Send structured response back to Team Chat.

Implementation references:

- [Chatbot Setup](chatbot-setup.md)
- [Sample Repositories](../references/samples.md)
