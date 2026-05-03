# Rivet Common Issues

## Webhooks never reach handlers

Symptoms:
- `client.start()` succeeds, but no event callbacks fire.

Checks:
- Marketplace endpoint URL points to correct module port.
- Endpoint includes `/zoom/events` suffix.
- `webhooksSecretToken` matches app configuration.
- Ngrok forward is active and mapped to the receiver port.

## OAuth install/callback fails

Symptoms:
- Install page redirects fail or callback errors.

Checks:
- `installerOptions.redirectUri` exactly matches Marketplace OAuth redirect.
- `stateStore` value is configured and stable.
- Receiver mode supports User OAuth (Lambda receiver caveat).

## Multi-module runtime conflicts

Symptoms:
- One module works, another silently fails.

Checks:
- Every module uses a unique port.
- Event subscriptions target the correct module endpoint.
- Env variables are not accidentally shared with wrong module.

## API-only mode confusion

Symptoms:
- OAuth expectations fail when receiver disabled.

Checks:
- `disableReceiver: true` disables OAuth flow behavior.
- For OAuth + API-only behavior, use receiver-compatible configuration and relax webhook verification as documented.

## Sample parity mismatches

Symptoms:
- Following sample exactly still fails in your environment.

Checks:
- Normalize env key names to your project standard.
- Reconcile sample README assumptions with current TypeDoc signatures.
- Verify module auth type alignment (Client Credentials vs User OAuth vs S2S).
