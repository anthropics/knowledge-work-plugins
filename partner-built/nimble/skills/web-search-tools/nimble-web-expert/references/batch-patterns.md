# Batch Patterns

Patterns for running `nimble agent`, `nimble extract`, and `nimble search` in parallel across multiple inputs — instead of one at a time.

## Table of Contents

- [When to use batch patterns](#when-to-use-batch-patterns)
- [Parallel agent runs](#parallel-agent-runs)
- [Parallel URL extraction](#parallel-url-extraction)
- [Parallel search queries](#parallel-search-queries)
- [Large-scale batches — generate a script](#large-scale-batches--generate-a-script)
- [Aggregating and displaying results](#aggregating-and-displaying-results)

---

## When to use batch patterns

| Scenario                                 | Inputs | Method                                         |
| ---------------------------------------- | ------ | ---------------------------------------------- |
| Run same agent with different params     | 2–5    | Parallel bash: `&` + `wait`                    |
| Extract multiple URLs                    | 2–5    | Parallel bash: `&` + `wait`                    |
| Run multiple search queries              | 2–5    | Parallel bash: `&` + `wait`                    |
| Any of the above                         | 6–20   | `xargs -P` or bash array with `&` + `wait`     |
| Any of the above                         | 20+    | Generate a Python script with `asyncio`        |
| Multi-site comparison with normalization | any    | Parallel bash (small) or Python script (large) |

**Default:** whenever the user provides or implies multiple inputs (list of ASINs, list of keywords, list of URLs, list of queries), use the parallel path — never loop one-by-one.

---

## Parallel agent runs

### 2–5 inputs — parallel bash

```bash
mkdir -p .nimble

nimble --transform "data.parsing" agent run --agent amazon_serp --params '{"keyword": "trackpad"}' > .nimble/trackpad.json &
nimble --transform "data.parsing" agent run --agent amazon_serp --params '{"keyword": "mouse"}' > .nimble/mouse.json &
nimble --transform "data.parsing" agent run --agent amazon_serp --params '{"keyword": "keyboard"}' > .nimble/keyboard.json &
wait

echo "All done"
```

All three requests fly out simultaneously. `wait` blocks until all finish. Each result lands in its own file.

### 2–5 inputs — from a bash array

```bash
mkdir -p .nimble
keywords=("trackpad" "mouse" "keyboard")

for kw in "${keywords[@]}"; do
  nimble --transform "data.parsing" agent run \
    --agent amazon_serp \
    --params "{\"keyword\": \"$kw\"}" \
    > ".nimble/amazon-${kw// /-}.json" &
done
wait
echo "All ${#keywords[@]} searches complete"
```

### 6–20 inputs — xargs parallel

```bash
mkdir -p .nimble
# One keyword per line in keywords.txt
cat keywords.txt | xargs -P 8 -I{} sh -c \
  'nimble --transform "data.parsing" agent run --agent amazon_serp --params "{\"keyword\": \"{}\"}" > ".nimble/amazon-{}.json" && echo "✓ {}"'
```

`-P 8` = up to 8 concurrent requests. Adjust based on your rate limit.

---

## Parallel URL extraction

### 2–5 URLs

```bash
mkdir -p .nimble

nimble --transform "data.markdown" extract --url "https://example.com/page1" --format markdown > .nimble/page1.md &
nimble --transform "data.markdown" extract --url "https://example.com/page2" --format markdown > .nimble/page2.md &
nimble --transform "data.markdown" extract --url "https://example.com/page3" --format markdown > .nimble/page3.md &
wait
```

### From a list of URLs

```bash
mkdir -p .nimble
urls=(
  "https://example.com/page1"
  "https://example.com/page2"
  "https://example.com/page3"
)

for url in "${urls[@]}"; do
  slug=$(echo "$url" | sed 's|https\?://||; s|/|-|g')
  nimble --transform "data.markdown" extract \
    --url "$url" --format markdown \
    > ".nimble/${slug}.md" &
done
wait
```

### Render flag — apply to all in parallel

```bash
for url in "${urls[@]}"; do
  nimble --transform "data.markdown" extract \
    --url "$url" --render --driver vx10-pro --format markdown \
    > ".nimble/$(basename $url).md" &
done
wait
```

---

## Parallel search queries

```bash
mkdir -p .nimble

nimble search "best trackpad 2025" > .nimble/search-trackpad.json &
nimble search "trackpad vs mouse productivity" > .nimble/search-comparison.json &
nimble search "apple magic trackpad review" > .nimble/search-review.json &
wait
```

Or from an array:

```bash
queries=("best trackpad 2025" "trackpad review" "trackpad vs mouse")

for q in "${queries[@]}"; do
  slug=$(echo "$q" | tr ' ' '-')
  nimble search "$q" > ".nimble/search-${slug}.json" &
done
wait
```

---

## Large-scale batches — generate a script

For 20+ inputs, generate a Python script and run it with `uv run`.

**Which template to use:**

| Command            | Template                     | Why                                                                         |
| ------------------ | ---------------------------- | --------------------------------------------------------------------------- |
| `nimble agent run` | Python SDK (`nimble_python`) | Direct SDK call — no subprocess overhead, built-in retries, typed responses |
| `nimble extract`   | CLI subprocess               | No Python SDK equivalent for `extract`                                      |
| `nimble search`    | CLI subprocess               | No Python SDK equivalent for `search`                                       |

### Template — parallel agent runs (Python SDK)

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["nimble_python"]
# ///
"""Run nimble agent in parallel across multiple inputs."""
import asyncio, json, os, pathlib
from nimble_python import AsyncNimble

AGENT = "amazon_serp"
INPUTS = [
    {"keyword": "trackpad"},
    {"keyword": "mouse"},
    {"keyword": "keyboard"},
    # add more...
]
CONCURRENCY = 8
OUT_DIR = pathlib.Path(".nimble")
OUT_DIR.mkdir(exist_ok=True)

nimble = AsyncNimble(api_key=os.environ["NIMBLE_API_KEY"], max_retries=4, timeout=120.0)
SEM = asyncio.Semaphore(CONCURRENCY)


async def run_one(params: dict) -> dict:
    key = next(iter(params.values()))
    slug = str(key).replace(" ", "-")
    out_file = OUT_DIR / f"{AGENT}-{slug}.json"

    async with SEM:
        try:
            resp = await nimble.agent.run(agent=AGENT, params=params)
            parsing = resp.data.parsing
        except Exception as e:
            print(f"  ✗ {key}: {e}")
            return {"input": params, "error": str(e)}

    # SERP items are typed Pydantic objects — must call .model_dump() to serialize to JSON
    serializable = [item.model_dump() for item in parsing] if isinstance(parsing, list) else parsing
    out_file.write_text(json.dumps(serializable, ensure_ascii=False, indent=2))
    print(f"  ✓ {key} → {out_file}")
    return {"input": params, "file": str(out_file), "count": len(parsing) if isinstance(parsing, list) else 1}


async def main():
    print(f"Running {len(INPUTS)} inputs (concurrency={CONCURRENCY})...")
    results = await asyncio.gather(*[run_one(p) for p in INPUTS], return_exceptions=True)

    ok = [r for r in results if isinstance(r, dict) and "error" not in r]
    fail = [r for r in results if isinstance(r, dict) and "error" in r]
    print(f"\nDone: {len(ok)} succeeded, {len(fail)} failed")
    if fail:
        for f in fail:
            print(f"  ✗ {f['input']}: {f['error'][:80]}")

    await nimble.close()

asyncio.run(main())
```

Run with:

```bash
uv run batch.py
```

### Template — parallel URL extraction

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Extract multiple URLs in parallel via nimble CLI."""
import asyncio, os, pathlib, re

URLS = [
    "https://example.com/page1",
    "https://example.com/page2",
    # add more...
]
CONCURRENCY = 6
OUT_DIR = pathlib.Path(".nimble")
OUT_DIR.mkdir(exist_ok=True)


def url_to_slug(url: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", url.lower()).strip("-")[:60]


async def extract_one(url: str) -> dict:
    slug = url_to_slug(url)
    out_file = OUT_DIR / f"extract-{slug}.md"

    proc = await asyncio.create_subprocess_exec(
        "nimble", "--transform", "data.markdown",
        "extract", "--url", url, "--format", "markdown",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**os.environ},
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        print(f"  ✗ {url}: {stderr.decode().strip()[:80]}")
        return {"url": url, "error": stderr.decode().strip()}

    out_file.write_text(stdout.decode())
    print(f"  ✓ {url} → {out_file}")
    return {"url": url, "file": str(out_file), "chars": len(stdout)}


async def main():
    sem = asyncio.Semaphore(CONCURRENCY)

    async def bounded(u):
        async with sem:
            return await extract_one(u)

    print(f"Extracting {len(URLS)} URLs...")
    results = await asyncio.gather(*[bounded(u) for u in URLS], return_exceptions=True)

    ok = [r for r in results if isinstance(r, dict) and "error" not in r]
    fail = [r for r in results if isinstance(r, dict) and "error" in r]
    print(f"\nDone: {len(ok)} succeeded, {len(fail)} failed")

asyncio.run(main())
```

---

## Aggregating and displaying results

After parallel runs, read and merge the output files:

```bash
# Combine all JSON arrays into one
python3 -c "
import json, pathlib, sys

files = list(pathlib.Path('.nimble').glob('amazon-*.json'))
all_results = []
for f in files:
    data = json.loads(f.read_text())
    if isinstance(data, list):
        all_results.extend(data)
    elif isinstance(data, dict):
        all_results.append(data)

print(json.dumps(all_results, indent=2))
print(f'Total: {len(all_results)} records from {len(files)} files', file=sys.stderr)
"
```

### Present results immediately

After the `wait` (or script completion), display a summary table — don't ask the user to wait further:

```
| # | Keyword  | Results | Top Item                     | Price  |
|---|----------|---------|------------------------------|--------|
| 1 | trackpad |      22 | Apple Magic Trackpad (White) | $119   |
| 2 | mouse    |      24 | Logitech MX Master 3S        | $99    |
| 3 | keyboard |      24 | Keychron K2 Pro              | $89    |
```

Full data saved to `.nimble/` (one file per input). Offer to drill into any row.

---

## Key rules

- **Never run inputs one-by-one** if there are 2+. Always use `&` + `wait` or `xargs -P`.
- **Save each result to its own file** in `.nimble/` with a descriptive name.
- **Handle failures per-item** — if one fails, continue the rest. Report failures at the end.
- **20+ inputs → generate a script.** Don't run 20 background bash jobs; use the Python asyncio template.
- **Concurrency limit:** default to 8 concurrent requests. Reduce if you hit rate limits.
