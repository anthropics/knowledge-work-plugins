# Sample Comparison

Use this quick matrix to choose the right Team Chat or chatbot sample shape before building your own integration.

| Sample shape | Best when | Strengths | Watch-outs |
|--------------|-----------|-----------|------------|
| Minimal webhook bot | You want to validate event flow quickly | Fastest setup, easy signature verification review | Usually in-memory state only |
| Full chatbot sample | You need slash commands, cards, and bot responses together | Shows end-to-end chat lifecycle | More moving parts than a simple receiver |
| LLM-enhanced bot | You want summarization or assistant behavior | Good reference for prompt assembly and response shaping | Requires stricter latency and fallback design |
| Multi-language sample | You need parity across runtimes | Useful for comparing auth and verification patterns | Feature coverage often drifts between languages |

## What to Compare

- OAuth flow type and token handling
- Webhook signature verification approach
- Message card rendering support
- Persistence model: in-memory, file, or database
- Local development strategy: tunnel, mock events, replay fixtures
