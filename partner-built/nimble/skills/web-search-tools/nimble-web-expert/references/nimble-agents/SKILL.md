---
name: nimble-agents-reference
description: |
  Reference for nimble agent commands. Load for Step 0 agent lookup.
  Contains: full agent table (50+ sites across e-commerce, food, real estate, jobs, social, travel),
  discover/list/schema/run commands, response shapes (PDP=dict, SERP=list, google=entities), agent memory.
---

# nimble agent — reference

Pre-built agents for specific sites. Always faster and more reliable than manual extraction — use them whenever a matching agent exists (see Step 0 in SKILL.md).

## Table of Contents

- [1. List agents](#1-list-agents)
- [2. Get agent details (schema)](#2-get-agent-details-schema)
- [3. Run agent (sync)](#3-run-agent-sync)
- [4. Run agent (async)](#4-run-agent-async)
- [5. Run agent (batch)](#5-run-agent-batch)
- [Response shapes](#response-shapes)
- [Known agents — baked-in table](#known-agents--baked-in-table)
- [Agent gallery](#agent-gallery)
- [Agent memory — save new agents](#agent-memory--save-new-agents)

---

## 1. List agents

**Parameters:**

| Parameter    | CLI flag       | Type   | Default | Description                                              |
| ------------ | -------------- | ------ | ------- | -------------------------------------------------------- |
| `limit`      | `--limit`      | int    | —       | Results per page                                         |
| `offset`     | `--offset`     | int    | —       | Pagination offset                                        |
| `search`     | `--search`     | string | —       | Search agents by domain, vertical, or name keyword       |
| `managed_by` | `--managed-by` | string | —       | Filter by attribution (e.g. `nimble`)                    |
| `privacy`    | `--privacy`    | string | —       | Filter by privacy level                                  |

**CLI:**

```bash
# All agents (broad lookup)
nimble agent list --limit 100

# Targeted search by domain or vertical (preferred when domain is known)
nimble agent list --limit 100 --search "amazon"
nimble agent list --limit 100 --search "ecommerce"
nimble agent list --limit 100 --search "jobs"
```

**Python SDK:**

```python
from nimble_python import Nimble
nimble = Nimble(api_key=os.environ["NIMBLE_API_KEY"])

agents = nimble.agent.list()
```

**Response fields per agent:** `name`, `display_name`, `description`, `vertical`, `entity_type`, `domain`, `is_public`, `managed_by`

---

## 2. Get agent details (schema)

**Parameters:**

| Parameter       | CLI flag          | Type   | Description           |
| --------------- | ----------------- | ------ | --------------------- |
| `template_name` | `--template-name` | string | Agent name (required) |

**CLI:**

```bash
nimble agent get --template-name amazon_pdp
```

**Python SDK:**

```python
agent = nimble.agent.get(template_name="amazon_pdp")
```

**Response:** same as list item + `output_schema` — JSON schema mapping field names to `{type, description}`.

---

## 3. Run agent (sync)

**Parameters:**

| Parameter      | CLI flag         | Type   | Default  | Description                                             |
| -------------- | ---------------- | ------ | -------- | ------------------------------------------------------- |
| `agent`        | `--agent`        | string | required | Agent name                                              |
| `params`       | `--params`       | JSON   | required | Agent input parameters                                  |
| `localization` | `--localization` | bool   | `false`  | Enable zip_code/store_id localization (agent-dependent) |

**CLI:**

```bash
nimble agent run --agent amazon_pdp --params '{"asin": "B0CHWRXH8B"}'
```

**Python SDK:**

```python
resp = nimble.agent.run(agent="amazon_pdp", params={"asin": "B0CHWRXH8B"})
parsing = resp.data.parsing  # dict for PDP agents, list for SERP agents
```

**Response fields:** `task_id`, `status` (`success`/`failed`), `status_code`, `data.parsing`, `data.html`, `metadata.query_duration`, `metadata.agent`

> SERP `parsing` items are typed Pydantic objects — call `.model_dump()` before `json.dumps()` or `**` spread. PDP `parsing` is a plain dict.

---

## 4. Run agent (async)

**Parameters:**

| Parameter      | CLI flag                | Type   | Default  | Description                        |
| -------------- | ----------------------- | ------ | -------- | ---------------------------------- |
| `agent`        | `--agent`               | string | required | Agent name                         |
| `params`       | `--params`              | JSON   | required | Agent input parameters             |
| `localization` | `--localization`        | bool   | `false`  | Enable localization                |
| `callback_url` | `--callback-url`        | string | —        | POST callback when task completes  |
| `storage_type` | `--storage-type`        | string | —        | `s3` or `gs`                       |
| `storage_url`  | `--storage-url`         | string | —        | Destination: `s3://bucket/prefix/` |
| `compress`     | `--storage-compress`    | bool   | `false`  | Gzip the stored output             |
| `custom_name`  | `--storage-object-name` | string | —        | Custom filename instead of task_id |

**CLI:**

```bash
nimble agent run-async --agent amazon_pdp --params '{"asin": "B0CHWRXH8B"}' \
  --callback-url "https://your.server/callback"
```

**Python SDK:**

```python
resp = await nimble.agent.run_async(agent="amazon_pdp", params={"asin": "B0CHWRXH8B"})
task_id = resp.task["id"]   # resp.task is a plain dict
```

**Task states:** `pending` → `success` or `error` — poll and fetch results via `nimble-tasks` reference.

---

## 5. Run agent (batch)

Submit up to 1,000 agent requests in a single call. Uses an `inputs` + `shared_inputs`
pattern — shared config applies to all items, per-item params override.

**Parameters:**

| Parameter       | CLI flag          | Type  | Default  | Description                                           |
| --------------- | ----------------- | ----- | -------- | ----------------------------------------------------- |
| `inputs`        | `--input`         | array | required | Array of per-item inputs (up to 1,000)                |
| `shared_inputs` | `--shared-inputs` | JSON  | required | Shared config: `agent` (required) + default `params`  |

Each item in `inputs` contains a `params` object with agent-specific inputs (e.g. `asin`,
`keyword`). Per-item `params` are merged with `shared_inputs.params` — per-item values
take priority.

**CLI:**

```bash
nimble agent run-batch \
  --shared-inputs 'agent: amazon_serp' \
  --input '{"params": {"keyword": "iphone 15"}}' \
  --input '{"params": {"keyword": "iphone 16"}}' \
  --input '{"params": {"keyword": "iphone 16 pro"}}'
```

**Python SDK:**

```python
resp = nimble.agent.batch(
    inputs=[
        {"params": {"keyword": "iphone 15"}},
        {"params": {"keyword": "iphone 16"}},
        {"params": {"keyword": "iphone 16 pro"}},
    ],
    shared_inputs={"agent": "amazon_serp"},
)
batch_id = resp["batch_id"]
```

**Node SDK:**

```javascript
const resp = await nimble.agent.batch({
  inputs: [
    { params: { keyword: "iphone 15" } },
    { params: { keyword: "iphone 16" } },
    { params: { keyword: "iphone 16 pro" } },
  ],
  sharedInputs: { agent: "amazon_serp" },
});
const batchId = resp.batch_id;
```

**Response:**

```json
{
  "batch_id": "b7e1a2f3-...",
  "batch_size": 3,
  "tasks": [
    { "id": "task-001-uuid", "state": "pending", "batch_id": "b7e1a2f3-..." }
  ]
}
```

**Polling:** Use `nimble batches progress --batch-id <batch_id>` to check completion,
then `nimble batches get --batch-id <batch_id>` to get all task IDs, then
`nimble tasks results --task-id <id>` for each successful task.
See `nimble-tasks` reference for the full polling flow.

**Delivery options:**
- **Polling** — check status with batch/task IDs (default)
- **Webhooks** — pass `callback_url` in `shared_inputs`; Nimble POSTs on completion
- **Cloud storage** — set `storage_type` + `storage_url` in `shared_inputs`

---

## Response shapes

| Agent type                   | `data.parsing` shape                          | Notes                                      |
| ---------------------------- | --------------------------------------------- | ------------------------------------------ |
| PDP (product/profile/detail) | flat dict                                     | Access with `.get("field")`                |
| SERP / list                  | array of objects                              | Iterate items; call `.model_dump()` in SDK |
| Google Search                | `{"entities": {"OrganicResult": [...], ...}}` | Nested entities dict                       |

---

## Known agents — baked-in table

> **Note:** Agent names containing date and random suffixes (e.g. `indeed_search_2026_02_23_vlgtrsgu`) are Nimble-managed and may be updated. Always run `nimble agent list --limit 100` to confirm current names before use.

### E-commerce — US

| Site                 | Agent                             | Key param      |
| -------------------- | --------------------------------- | -------------- |
| Amazon product page  | `amazon_pdp`                      | `asin`         |
| Amazon search        | `amazon_serp`                     | `keyword`      |
| Amazon best sellers  | `amazon_best_sellers`             | —              |
| Amazon category      | `amazon_plp`                      | _(see schema)_ |
| Walmart product      | `walmart_pdp`                     | `product_id`   |
| Walmart search       | `walmart_serp`                    | `keyword`      |
| Target product       | `target_pdp`                      | `tcin`         |
| Target search        | `target_serp`                     | `query`        |
| Best Buy product     | `best_buy_pdp`                    | `product_id`   |
| Home Depot product   | `homedepot_pdp`                   | _(see schema)_ |
| Home Depot search    | `homedepot_serp`                  | _(see schema)_ |
| Sam's Club product   | `sams_club_pdp`                   | _(see schema)_ |
| Sam's Club search    | `sams_club_plp`                   | _(see schema)_ |
| eBay search          | `ebay_search_2026_02_23_pbgj8oft` | _(see schema)_ |
| ASOS product         | `asos_pdp`                        | _(see schema)_ |
| ASOS search          | `asos_serp`                       | _(see schema)_ |
| Kroger product       | `kroger_pdp`                      | _(see schema)_ |
| Kroger search        | `kroger_serp`                     | _(see schema)_ |
| Foot Locker product  | `footlocker_pdp`                  | _(see schema)_ |
| Staples product      | `staples_pdp`                     | _(see schema)_ |
| Staples search       | `staples_serp`                    | _(see schema)_ |
| Office Depot product | `office_depot_pdp`                | _(see schema)_ |
| B&H search           | `b_and_h_serp`                    | _(see schema)_ |
| Slickdeals           | `slickdeals_pdp`                  | _(see schema)_ |

### Food delivery

| Site                 | Agent            |
| -------------------- | ---------------- |
| DoorDash restaurant  | `doordash_pdp`   |
| DoorDash search      | `doordash_serp`  |
| Uber Eats restaurant | `uber_eats_pdp`  |
| Uber Eats search     | `uber_eats_serp` |

### Real estate

| Site             | Agent                                  | Key params                                      |
| ---------------- | -------------------------------------- | ----------------------------------------------- |
| Zillow listings  | `zillow_plp`                           | `zip_code`, `listing_type` (sales/rentals/sold) |
| Zillow property  | `zillow_pdp`                           | _(see schema)_                                  |
| Rightmove search | `rightmove_search_2026_02_23_pxo1ccrm` | _(see schema)_                                  |

### Jobs

| Site          | Agent                                     | Key params                |
| ------------- | ----------------------------------------- | ------------------------- |
| Indeed search | `indeed_search_2026_02_23_vlgtrsgu`       | `location`, `search_term` |
| ZipRecruiter  | `ziprecruiter_search_2026_02_23_8rtda7lg` | _(see schema)_            |

### Search & maps

| Site                | Agent                 | Key param                             |
| ------------------- | --------------------- | ------------------------------------- |
| Google search       | `google_search`       | `query`                               |
| Google Maps search  | `google_maps_search`  | `query`                               |
| Google Maps reviews | `google_maps_reviews` | `place_id`                            |
| Yelp search         | `yelp_serp`           | `search_query`, `location` (optional) |

### News & finance

| Site                | Agent                                            |
| ------------------- | ------------------------------------------------ |
| BBC article         | `bbc_info_2026_02_23_wexv71ke`                   |
| BBC search          | `bbc_search_2026_02_23_t0gj94t2`                 |
| The Guardian search | `guardian_search_2026_02_23_nair7e5i`            |
| NYTimes search      | `nytimes_search_2026_02_23_4zleml8l`             |
| Bloomberg search    | `bloomberg_search_2026_02_23_a9u4p1tv`           |
| Yahoo Finance       | `yahoo_finance_info_2026_02_23_fl3ij8ps`         |
| MarketWatch         | `marketwatch_info_2026_02_23_zpwkys0h`           |
| Morningstar         | `morningstar_search_2026_02_23_zicq0zdj`         |
| Polymarket          | `polymarket_prediction_data_2026_02_24_9zhwkle8` |

### Social media

| Site                | Agent                                  |
| ------------------- | -------------------------------------- |
| Instagram post      | `instagram_post`                       |
| Instagram profile   | `instagram_profile_by_account`         |
| Instagram reel      | `instagram_reel`                       |
| TikTok account      | `tiktok_account`                       |
| TikTok video        | `tiktok_video_page`                    |
| TikTok Shop product | `tiktok_shop_pdp`                      |
| Facebook page       | `facebook_page`                        |
| Facebook profile    | `facebook_profile_about_section`       |
| YouTube Shorts      | `youtube_shorts`                       |
| Pinterest search    | `pinterest_search_2026_02_23_kxzd5awh` |
| Quora topic         | `quora_info_2026_02_23_99baxvhr`       |

### Travel & LLM platforms

| Site               | Agent                |
| ------------------ | -------------------- |
| Skyscanner flights | `skyscanner_flights` |
| ChatGPT            | `chatgpt`            |
| Gemini             | `gemini`             |
| Grok               | `grok`               |
| Perplexity         | `perplexity`         |

---

## Agent gallery

```bash
open -a "Google Chrome" "https://online.nimbleway.com/pipeline-gallery"
open -a "Google Chrome" "https://online.nimbleway.com/pipeline-gallery/amazon_pdp/overview"
```

---

## Agent memory — save new agents

After a successful run, save to `learned/examples.json` so Step 0 matches faster next time:

```bash
python3 -c "
import json, pathlib, datetime
p = pathlib.Path.home() / '.claude/skills/nimble-web-expert/learned/examples.json'
data = json.loads(p.read_text()) if p.exists() else {'good': [], 'bad': [], 'agents': []}
data.setdefault('agents', [])
new_entry = {
    'agent_name': 'amazon_pdp',
    'tags': ['amazon', 'product', 'ecommerce', 'price', 'asin'],
    'params_example': {'asin': 'B0CHWRXH8B'},
    'last_used': str(datetime.date.today()),
    'notes': 'Returns price, title, rating, availability.'
}
if not any(a['agent_name'] == new_entry['agent_name'] for a in data['agents']):
    data['agents'].append(new_entry)
    p.write_text(json.dumps(data, indent=2))
    print('Saved.')
"
```
