# Message Issues

## Messages Not Sending

- Confirm you're using the correct API:
  - Team Chat API uses user OAuth token
  - Chatbot API uses bot token + `robot_jid`

## Card Not Rendering

- Validate the card JSON payload against known-good examples.
- Simplify to a minimal card and add components incrementally.

