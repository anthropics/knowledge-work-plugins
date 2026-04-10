---
name: nimble-tasks-reference
description: |
  Reference for nimble tasks and batches commands. Load when polling async task status,
  tracking batch progress, or fetching results.
  Works for ALL async types: agent run-async, agent run-batch, extract-async, extract-batch,
  crawl (per-page tasks), search async, map async.
  CRITICAL: agent tasks use "success"/"error" states; crawl page tasks use "completed"/"failed".
---

# nimble tasks & batches — reference

Unified task and batch layer for ALL async Nimble operations. Every async job produces a
`task_id`, and batch jobs produce a `batch_id` containing multiple tasks. Use these
commands to check status and retrieve results.

## Table of Contents

- [Tasks](#tasks)
  - [1. Get task status](#1-get-task-status)
  - [2. Get task results](#2-get-task-results)
  - [3. List tasks](#3-list-tasks)
- [Batches](#batches)
  - [4. Get batch progress](#4-get-batch-progress)
  - [5. Get batch details](#5-get-batch-details)
  - [6. List batches](#6-list-batches)
- [Common patterns](#common-patterns)
- [Data retention](#data-retention)

---

## Tasks

### 1. Get task status

**Parameters:**

| Parameter | CLI flag | Type | Description |
|-----------|----------|------|-------------|
| `task_id` | `--task-id` | string | Task ID (required) |

**CLI:**
```bash
nimble tasks get --task-id "8e8cfde8-345b-42b8-b3e2-0c61eb11e00f"
```

**Python SDK:**
```python
from nimble_python import Nimble
nimble = Nimble(api_key=os.environ["NIMBLE_API_KEY"])

task = nimble.tasks.get(task_id)
state = task.task.state
```

**Task state values by source:**

| Source | Terminal states | Intermediate |
|--------|----------------|--------------|
| `agent run-async` | `success` / `error` | `pending` |
| `agent run-batch` (per task) | `success` / `error` | `pending` / `in_progress` |
| `extract-async` | `success` / `error` | `pending` |
| `extract-batch` (per task) | `success` / `error` | `pending` / `in_progress` |
| Crawl page task | `completed` / `failed` | `pending` / `processing` |

---

### 2. Get task results

**Parameters:**

| Parameter | CLI flag | Type | Description |
|-----------|----------|------|-------------|
| `task_id` | `--task-id` | string | Task ID (required) |

**CLI:**
```bash
nimble tasks results --task-id "8e8cfde8-345b-42b8-b3e2-0c61eb11e00f"
```

**Python SDK:**
```python
results = await nimble.tasks.results(task_id)  # returns plain dict
```

**Response shape by source:**

| Source | Shape |
|--------|-------|
| `agent run-async` / batch | `{"data": {"parsing": ...}, "status": "success", ...}` |
| Crawl page | `{"url": "...", "data": {"html": "...", "markdown": "..."}, "status_code": 200, ...}` |
| Extract async / batch | `{"data": {"html": "...", "markdown": "...", "parsing": {}}, "status": "success", ...}` |

> `tasks.results()` returns **plain dicts** — no `.model_dump()` needed.

---

### 3. List tasks

**Parameters:**

| Parameter | CLI flag | Type | Description |
|-----------|----------|------|-------------|
| `limit` | `--limit` | int | Results per page |
| `cursor` | `--cursor` | string | Pagination cursor |

**CLI:**
```bash
nimble tasks list --limit 20
```

**Python SDK:**
```python
result = nimble.tasks.list()
```

---

## Batches

Batch operations (`agent run-batch`, `extract-batch`) return a `batch_id` containing
multiple tasks. Use these commands to track overall progress and retrieve individual
task results.

### 4. Get batch progress

Lightweight progress check — returns completion percentage without fetching all task details.

**Parameters:**

| Parameter | CLI flag | Type | Description |
|-----------|----------|------|-------------|
| `batch_id` | `--batch-id` | string | Batch ID (required) |

**CLI:**
```bash
nimble batches progress --batch-id "b7e1a2f3-..."
```

**Response:**

```json
{
  "completed": false,
  "completed_count": 47,
  "progress": 0.47
}
```

| Field | Type | Description |
|-------|------|-------------|
| `completed` | bool | `true` when all tasks are done (success or error) |
| `completed_count` | int | Number of finished tasks |
| `progress` | float | 0.0 to 1.0 completion ratio |

---

### 5. Get batch details

Returns all task IDs, states, and download URLs for a batch.

**Parameters:**

| Parameter | CLI flag | Type | Description |
|-----------|----------|------|-------------|
| `batch_id` | `--batch-id` | string | Batch ID (required) |

**CLI:**
```bash
nimble batches get --batch-id "b7e1a2f3-..."
```

**Response:** Contains the full list of tasks with their IDs and states. Use
`nimble tasks results --task-id <id>` to fetch results for each successful task.

---

### 6. List batches

**Parameters:**

| Parameter | CLI flag | Type | Description |
|-----------|----------|------|-------------|
| `limit` | `--limit` | int | Results per page |
| `cursor` | `--cursor` | string | Pagination cursor |

**CLI:**
```bash
nimble batches list --limit 20
```

---

## Common patterns

### Single async task — full poll loop

```bash
# Submit
TASK_ID=$(nimble agent run-async --agent amazon_pdp --params '{"asin": "B0CHWRXH8B"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['task']['id'])")

# Poll
while true; do
  STATE=$(nimble tasks get --task-id "$TASK_ID" \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['task']['state'])")
  [ "$STATE" = "success" ] || [ "$STATE" = "error" ] && break
  sleep 3
done

nimble tasks results --task-id "$TASK_ID"
```

**Python SDK (async):**
```python
import asyncio, os
from nimble_python import AsyncNimble

async def run():
    nimble = AsyncNimble(api_key=os.environ["NIMBLE_API_KEY"])
    resp = await nimble.agent.run_async(agent="amazon_pdp", params={"asin": "B0CHWRXH8B"})
    task_id = resp.task["id"]

    while True:
        task = await nimble.tasks.get(task_id)
        if task.task.state in ("success", "error"):
            break
        await asyncio.sleep(2)

    results = await nimble.tasks.results(task_id)
    parsing = results["data"]["parsing"]
    await nimble.close()
```

### Batch — full poll loop

```bash
# Submit batch
BATCH_ID=$(nimble agent run-batch \
  --shared-inputs 'agent: amazon_serp' \
  --input '{"params": {"keyword": "iphone 15"}}' \
  --input '{"params": {"keyword": "iphone 16"}}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['batch_id'])")

# Poll progress
while true; do
  DONE=$(nimble batches progress --batch-id "$BATCH_ID" \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['completed'])")
  [ "$DONE" = "True" ] && break
  sleep 5
done

# Get all task IDs
nimble batches get --batch-id "$BATCH_ID" \
  | python3 -c "
import json, sys
batch = json.load(sys.stdin)
for task in batch['tasks']:
    if task['state'] == 'success':
        print(task['id'])
" | while read TASK_ID; do
  nimble tasks results --task-id "$TASK_ID"
done
```

**Python SDK:**
```python
import asyncio
from nimble_python import AsyncNimble

async def run_batch():
    nimble = AsyncNimble(api_key=os.environ["NIMBLE_API_KEY"])

    resp = nimble.agent.batch(
        inputs=[
            {"params": {"keyword": "iphone 15"}},
            {"params": {"keyword": "iphone 16"}},
        ],
        shared_inputs={"agent": "amazon_serp"},
    )
    batch_id = resp["batch_id"]

    # Poll until complete
    while True:
        progress = nimble.batches.progress(batch_id)
        if progress["completed"]:
            break
        await asyncio.sleep(5)

    # Fetch results
    batch = nimble.batches.get(batch_id)
    for task in batch["tasks"]:
        if task["state"] == "success":
            result = await nimble.tasks.results(task["id"])
            print(result["data"]["parsing"])

    await nimble.close()
```

---

## Data retention

| State | Retention |
|-------|-----------|
| Pending tasks (not started) | 24 hours |
| Completed results | 24-48 hours (indefinite with cloud storage) |
| Failed tasks | 24 hours |
