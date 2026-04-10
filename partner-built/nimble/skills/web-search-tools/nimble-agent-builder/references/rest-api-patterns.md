# REST API Patterns

Reference for running Nimble agents from TypeScript/Node, Go, Ruby, curl, and other non-Python languages. For Python, use `references/sdk-patterns.md`.

**Official SDK client libraries available:**
- **TypeScript/Node** — `npm install @nimble-way/sdk`. See [Node SDK docs](https://docs.nimbleway.com/nimble-sdk/sdks/node).
- **Go** — `go get github.com/Nimbleway/nimble-go@latest`. See [Go SDK docs](https://docs.nimbleway.com/nimble-sdk/sdks/go).
- **Ruby, curl, others** — use the raw REST patterns below. The API is standard JSON + Bearer auth.

## Table of Contents

- [Authentication](#authentication)
- [Sync endpoint](#sync-endpoint)
- [Async endpoint](#async-endpoint)
- [TypeScript/Node examples](#typescriptnode-examples)
- [Go examples](#go-examples)
- [Ruby examples](#ruby-examples)
- [curl examples](#curl-examples)
- [Response handling](#response-handling)
- [Error handling](#error-handling)
- [Retry logic](#retry-logic)

---

## Authentication

All requests require a Bearer token:

```
Base URL: https://api.nimbleway.com
Header:  Authorization: Bearer <NIMBLE_API_KEY>
Content-Type: application/json
```

---

## Sync endpoint

`POST /v1/agent` — submit and wait for results in a single request.

**Request:**

```json
{
  "agent": "<agent-name>",
  "params": { "keyword": "wireless headphones" }
}
```

**Response:**

```json
{
  "data": {
    "parsing": [
      { "product_name": "...", "price": 29.99, "rating": 4.5 }
    ]
  },
  "url": "https://...",
  "agent_name": "<agent-name>"
}
```

`parsing` is a **list** for ecommerce SERP agents, a **dict** with nested `entities` for non-ecommerce SERP agents (e.g., `google_search`), and a flat **dict** for PDP agents. See "Response handling" below for all three shapes.

---

## Async endpoint

For 4+ concurrent jobs, use the async flow for higher throughput. Three steps:

### 1. Submit

`POST /v1/agent/async` — same body as sync. Returns immediately.

```json
{
  "task": { "id": "uuid-string", "state": "pending" }
}
```

### 2. Poll

`GET /v1/tasks/{task_id}` — repeat until terminal state.

| State | Meaning |
|-------|---------|
| `pending` | Queued |
| `success` | Done — fetch results |
| `failed` | Error |

**IMPORTANT:** The terminal success state is `"success"`, NOT `"completed"`.

### 3. Retrieve

`GET /v1/tasks/{task_id}/results` — only after state is `"success"`.

Response has the same shape as the sync endpoint (`data.parsing`).

---

## TypeScript/Node examples

> **SDK available:** Prefer `@nimble-way/sdk` over raw `fetch` for a first-class API with typed responses.
> ```typescript
> import Nimble from "@nimble-way/nimble-js";
> const nimble = new Nimble({ apiKey: process.env.NIMBLE_API_KEY });
> const result = await nimble.agent.run({ agent: "amazon_pdp", params: { asin: "B08N5WRWNW" } });
> ```
> See [Node SDK docs](https://docs.nimbleway.com/nimble-sdk/sdks/node). Raw `fetch` patterns below are useful for environments without npm (Cloudflare Workers raw mode, Deno without npm compat, etc.).

### Single agent (sync)

```typescript
const BASE = "https://api.nimbleway.com";
const KEY = process.env.NIMBLE_API_KEY!;

async function runAgent(agent: string, params: Record<string, unknown>) {
  const res = await fetch(`${BASE}/v1/agent`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ agent, params }),
  });
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  return res.json();
}

// Usage
const data = await runAgent("amazon_serp", { keyword: "keyboard" });
const records = data.data.parsing; // array for SERP agents
```

### Batch (sync with Promise.all)

For 2–3 concurrent jobs:

```typescript
const jobs = [
  runAgent("amazon_serp", { keyword: "keyboard" }),
  runAgent("walmart_serp", { keyword: "keyboard" }),
];
const results = await Promise.all(jobs);
const allRecords = results.flatMap((r) => r.data.parsing ?? []);
```

### Async batch pipeline

For 4+ jobs, submit all via async endpoint, then poll concurrently:

```typescript
async function submitAsync(agent: string, params: Record<string, unknown>) {
  const res = await fetch(`${BASE}/v1/agent/async`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ agent, params }),
  });
  if (!res.ok) throw new Error(`submitAsync ${res.status}: ${await res.text()}`);
  const data = await res.json();
  return data.task.id as string;
}

async function pollUntilDone(taskId: string, intervalMs = 3000, maxAttempts = 60) {
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const res = await fetch(`${BASE}/v1/tasks/${taskId}`, {
      headers: { Authorization: `Bearer ${KEY}` },
    });
    if (!res.ok) throw new Error(`poll ${res.status}: ${await res.text()}`);
    const data = await res.json();
    const state = data.task?.state;
    if (state === "success" || state === "failed") return state;
    await new Promise((r) => setTimeout(r, intervalMs));
  }
  throw new Error(`Task ${taskId} did not complete after ${maxAttempts} attempts`);
}

async function fetchResults(taskId: string) {
  const res = await fetch(`${BASE}/v1/tasks/${taskId}/results`, {
    headers: { Authorization: `Bearer ${KEY}` },
  });
  if (!res.ok) throw new Error(`fetchResults ${res.status}: ${await res.text()}`);
  return res.json();
}

// Pipeline: submit all → poll → collect
const taskIds = await Promise.all(
  jobs.map(([agent, params]) => submitAsync(agent, params))
);
const states = await Promise.all(taskIds.map((id) => pollUntilDone(id)));
const rows = [];
for (let i = 0; i < taskIds.length; i++) {
  if (states[i] === "success") {
    const result = await fetchResults(taskIds[i]);
    const parsing = result.data?.parsing ?? [];
    rows.push(...(Array.isArray(parsing) ? parsing : [parsing]));
  }
}
```

---

## Go examples

> **SDK available:** Prefer `github.com/Nimbleway/nimble-go` over raw `net/http` for a first-class API.
> ```go
> client := nimble.NewClient(option.WithAPIKey(os.Getenv("NIMBLE_API_KEY")))
> result, err := client.Agent.Run(context.TODO(), nimble.AgentRunParams{
>     Agent: "amazon_pdp",
>     Params: map[string]interface{}{"asin": "B08N5WRWNW"},
> })
> ```
> See [Go SDK docs](https://docs.nimbleway.com/nimble-sdk/sdks/go). Raw `net/http` patterns below are useful when you can't add dependencies.

### Single agent (sync)

```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

const base = "https://api.nimbleway.com"

func runAgent(agent string, params map[string]any) (map[string]any, error) {
	body, _ := json.Marshal(map[string]any{"agent": agent, "params": params})
	req, _ := http.NewRequest("POST", base+"/v1/agent", bytes.NewReader(body))
	req.Header.Set("Authorization", "Bearer "+os.Getenv("NIMBLE_API_KEY"))
	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		b, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("HTTP %d: %s", resp.StatusCode, b)
	}

	var result map[string]any
	json.NewDecoder(resp.Body).Decode(&result)
	return result, nil
}
```

### Response handling

`data.parsing` has three shapes — see the "Response handling" section below for full details with all three patterns. Quick two-way check for ecommerce agents:

```go
data := result["data"].(map[string]any)
switch parsing := data["parsing"].(type) {
case []any:
	// Ecommerce SERP — iterate records
	for _, rec := range parsing {
		row := rec.(map[string]any)
		fmt.Println(row["product_name"], row["price"])
	}
case map[string]any:
	// PDP — single record (or nested entities for non-ecommerce SERP)
	fmt.Println(parsing["product_title"], parsing["web_price"])
}
```

### Async batch (goroutines)

These functions extend the sync example above. Add `"time"` to the import block.

```go
func submitAsync(agent string, params map[string]any) (string, error) {
	body, _ := json.Marshal(map[string]any{"agent": agent, "params": params})
	req, _ := http.NewRequest("POST", base+"/v1/agent/async", bytes.NewReader(body))
	req.Header.Set("Authorization", "Bearer "+os.Getenv("NIMBLE_API_KEY"))
	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	var result map[string]any
	json.NewDecoder(resp.Body).Decode(&result)
	task := result["task"].(map[string]any)
	return task["id"].(string), nil
}

func pollUntilDone(taskID string) (string, error) {
	for attempt := 0; attempt < 60; attempt++ {
		req, _ := http.NewRequest("GET", base+"/v1/tasks/"+taskID, nil)
		req.Header.Set("Authorization", "Bearer "+os.Getenv("NIMBLE_API_KEY"))
		resp, err := http.DefaultClient.Do(req)
		if err != nil {
			return "", err
		}
		var result map[string]any
		json.NewDecoder(resp.Body).Decode(&result)
		resp.Body.Close()

		state := result["task"].(map[string]any)["state"].(string)
		if state == "success" || state == "failed" {
			return state, nil
		}
		time.Sleep(3 * time.Second)
	}
	return "", fmt.Errorf("task %s did not complete", taskID)
}
```

---

## Ruby examples

### Single agent (sync)

```ruby
require "net/http"
require "json"

BASE = "https://api.nimbleway.com"
KEY  = ENV.fetch("NIMBLE_API_KEY")

def run_agent(agent, params)
  uri = URI("#{BASE}/v1/agent")
  req = Net::HTTP::Post.new(uri)
  req["Authorization"] = "Bearer #{KEY}"
  req["Content-Type"]  = "application/json"
  req.body = { agent: agent, params: params }.to_json

  res = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) { |http| http.request(req) }
  raise "HTTP #{res.code}: #{res.body}" unless res.is_a?(Net::HTTPSuccess)

  JSON.parse(res.body)
end

# Usage
data = run_agent("amazon_serp", { keyword: "keyboard" })
parsing = data.dig("data", "parsing")
# parsing is Array for SERP, Hash for PDP
```

### Async batch

```ruby
def submit_async(agent, params)
  uri = URI("#{BASE}/v1/agent/async")
  req = Net::HTTP::Post.new(uri)
  req["Authorization"] = "Bearer #{KEY}"
  req["Content-Type"]  = "application/json"
  req.body = { agent: agent, params: params }.to_json

  res = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) { |http| http.request(req) }
  JSON.parse(res.body).dig("task", "id")
end

def poll_until_done(task_id, max_attempts: 60)
  max_attempts.times do
    uri = URI("#{BASE}/v1/tasks/#{task_id}")
    req = Net::HTTP::Get.new(uri)
    req["Authorization"] = "Bearer #{KEY}"
    res = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) { |http| http.request(req) }
    state = JSON.parse(res.body).dig("task", "state")
    return state if %w[success failed].include?(state)
    sleep 3
  end
  raise "Task #{task_id} did not complete"
end

def fetch_results(task_id)
  uri = URI("#{BASE}/v1/tasks/#{task_id}/results")
  req = Net::HTTP::Get.new(uri)
  req["Authorization"] = "Bearer #{KEY}"
  res = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) { |http| http.request(req) }
  JSON.parse(res.body)
end
```

---

## curl examples

### Sync call

```bash
curl -X POST https://api.nimbleway.com/v1/agent \
  -H "Authorization: Bearer $NIMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agent": "amazon_serp", "params": {"keyword": "keyboard"}}'
```

### Async submit + poll + retrieve

```bash
# Submit
TASK_ID=$(curl -s -X POST https://api.nimbleway.com/v1/agent/async \
  -H "Authorization: Bearer $NIMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agent": "amazon_serp", "params": {"keyword": "keyboard"}}' \
  | jq -r '.task.id')

# Poll (repeat until state is "success")
curl -s https://api.nimbleway.com/v1/tasks/$TASK_ID \
  -H "Authorization: Bearer $NIMBLE_API_KEY" \
  | jq '.task.state'

# Retrieve results
curl -s https://api.nimbleway.com/v1/tasks/$TASK_ID/results \
  -H "Authorization: Bearer $NIMBLE_API_KEY" \
  | jq '.data.parsing'
```

---

## Response handling

Both sync and async endpoints return the same data structure. There are **three** response shapes:

| Agent type | `data.parsing` shape | Examples |
|-----------|---------------------|----------|
| Detail/PDP | `object` (flat fields) | `amazon_pdp`, `walmart_pdp` |
| Ecommerce SERP | `array` (list of records) | `amazon_serp`, `walmart_serp` |
| Non-ecommerce SERP | `object` with nested `entities.{EntityType}` arrays | `google_search`, `google_maps_search` |

**Note:** The REST API (`POST /v1/agent`) returns results at `data.parsing`. The CLI `nimble agent run` also returns `data.parsing` (same format). This document covers the REST API layer, used for script/codegen. For interactive use, the CLI is preferred.

**Before generating code**, check the `skills` output from `nimble agent get --template-name <name>` (CLI) to determine which shape applies. See `agent-api-reference.md` > "Response shape inference" for the full mapping table.

### Non-ecommerce SERP response shape

Agents like `google_search` and `google_maps_search` return a nested structure:

```json
{
  "data": {
    "parsing": {
      "entities": {
        "OrganicResult": [
          { "title": "...", "url": "...", "snippet": "...", "position": 1 }
        ],
        "Ad": [ ... ],
        "PeopleAlsoAsk": [ ... ]
      },
      "total_entities_count": 12,
      "entities_count": { "OrganicResult": 10, "Ad": 2 }
    }
  }
}
```

### Handling all three response types

#### TypeScript

```typescript
const parsing = data.data?.parsing;
if (Array.isArray(parsing)) {
  // Ecommerce SERP — flat list of records
  records = parsing;
} else if (parsing && typeof parsing === "object") {
  const entities = parsing.entities;
  if (entities) {
    // Non-ecommerce SERP — extract specific entity type
    records = entities.OrganicResult ?? [];
  } else {
    // Detail/PDP — single record as flat object
    records = [parsing];
  }
}
```

#### Go

```go
data := result["data"].(map[string]any)
switch parsing := data["parsing"].(type) {
case []any:
	// Ecommerce SERP — iterate records
	for _, rec := range parsing {
		row := rec.(map[string]any)
		fmt.Println(row["product_name"], row["price"])
	}
case map[string]any:
	if entities, ok := parsing["entities"].(map[string]any); ok {
		// Non-ecommerce SERP — extract entity type
		if organic, ok := entities["OrganicResult"].([]any); ok {
			for _, rec := range organic {
				row := rec.(map[string]any)
				fmt.Println(row["title"], row["url"])
			}
		}
	} else {
		// PDP — single record
		fmt.Println(parsing["product_title"], parsing["web_price"])
	}
}
```

#### Ruby

```ruby
parsing = data.dig("data", "parsing")
case parsing
when Array
  # Ecommerce SERP — iterate records
  records = parsing
when Hash
  if (entities = parsing["entities"])
    # Non-ecommerce SERP — extract entity type
    records = entities["OrganicResult"] || []
  else
    # PDP — single record
    records = [parsing]
  end
end
```

#### curl + jq

```bash
# Ecommerce SERP (array)
curl -s ... | jq '.data.parsing[]'

# Non-ecommerce SERP (nested entities)
curl -s ... | jq '.data.parsing.entities.OrganicResult[]'

# PDP (single object)
curl -s ... | jq '.data.parsing'
```

---

## Error handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401/403 | Invalid or expired API key | Check `NIMBLE_API_KEY` |
| 404 | Agent not found | Verify agent name via `nimble agent list --limit 100` (CLI) |
| 429 | Rate limited | Back off and retry after delay |
| 500-504 | Server error | Retry with exponential backoff |

For async tasks, a `"failed"` state means server-side failure. Resubmit the job or fall back to the sync endpoint.

---

## Retry logic

The Python SDK handles retries automatically (`max_retries`). For other languages, implement exponential backoff for 429 and 5xx errors.

**Note:** Only retry idempotent failures (rate limits, server errors). Do not retry 4xx client errors (except 429).

### TypeScript

```typescript
async function fetchWithRetry(
  url: string,
  init: RequestInit,
  maxRetries = 3,
  baseDelayMs = 1000,
): Promise<Response> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    const res = await fetch(url, init);
    if (res.ok) return res;
    if (attempt === maxRetries || (res.status < 429 && res.status >= 400)) {
      throw new Error(`${res.status}: ${await res.text()}`);
    }
    if (res.status === 429 || res.status >= 500) {
      const delay = baseDelayMs * 2 ** attempt;
      await new Promise((r) => setTimeout(r, delay));
    } else {
      throw new Error(`${res.status}: ${await res.text()}`);
    }
  }
  throw new Error("Unreachable");
}
```

### Go

```go
func fetchWithRetry(req *http.Request, maxRetries int) (*http.Response, error) {
	for attempt := 0; attempt <= maxRetries; attempt++ {
		resp, err := http.DefaultClient.Do(req)
		if err != nil {
			if attempt == maxRetries {
				return nil, err
			}
			time.Sleep(time.Duration(1<<attempt) * time.Second)
			continue
		}
		if resp.StatusCode < 400 {
			return resp, nil
		}
		if resp.StatusCode == 429 || resp.StatusCode >= 500 {
			resp.Body.Close()
			if attempt == maxRetries {
				return nil, fmt.Errorf("HTTP %d after %d retries", resp.StatusCode, maxRetries)
			}
			time.Sleep(time.Duration(1<<attempt) * time.Second)
			continue
		}
		b, _ := io.ReadAll(resp.Body)
		resp.Body.Close()
		return nil, fmt.Errorf("HTTP %d: %s", resp.StatusCode, b)
	}
	return nil, fmt.Errorf("max retries exceeded")
}
```
