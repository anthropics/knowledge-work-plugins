# DocuSign: fetching contracts for review

Use the DocuSign MCP connector to pull envelopes awaiting signature.

## Fetch pending envelopes

Use `getEnvelopes` to list envelopes in `sent` or `delivered` status (awaiting recipient action):

```
Tool: getEnvelopes
Params: { status: "sent" }  // or "delivered"
```

Returns a list of envelopes with: `envelopeId`, `emailSubject`, `createdDateTime`, `status`, `recipients`.

## Download document from envelope

Use `getEnvelope` with the `envelopeId` to get the full envelope details, then download the document for reading.

## What NOT to do

- Never call `triggerWorkflow` or any action that moves the envelope forward in the signing process.
- Never call `updateEnvelope` to modify the document.
- Never call `createEnvelope` — this skill is review-only.

## Fallback

If DocuSign is not connected or the envelope is not found:

```
"DocuSign isn't connected — paste the contract text or attach the file directly."
```
