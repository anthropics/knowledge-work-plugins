# Rivet Reference Map

## Canonical Documentation

- Product docs: https://developers.zoom.us/docs/rivet/
- JavaScript docs: https://developers.zoom.us/docs/rivet/javascript/
- TypeDoc reference: https://zoom.github.io/rivet-javascript/modules.html

## Modules (TypeDoc)

From `@zoom/rivet` TypeDoc module index:
- Accounts
- Chatbot
- Meetings
- Phone
- Team Chat
- Users
- Video SDK

Each module generally exposes:
- `*Client` class(es)
- `*Endpoints` wrapper class
- `*EventProcessor`
- `HttpReceiver` and `AwsLambdaReceiver`
- Shared option/types/error surfaces

## Key API Shapes

- Event subscription:
- `client.webEventConsumer.event(eventName, handler)`
- Event shortcut examples:
- `onSlashCommand`, `onButtonClick`, `onChannelMessagePosted`
- Endpoint wrappers:
- `client.endpoints.<group>.<operation>({ path, query, body })`

## Important Links for Validation

- Rivet sample app: https://github.com/zoom/rivet-javascript-sample
- ISV starter sample: https://github.com/zoom/isv-rivet-starter
- Rivet server sample: https://github.com/zoom/Rivet-Server-Sample
- Rivet package source: https://github.com/zoom/rivet-javascript
