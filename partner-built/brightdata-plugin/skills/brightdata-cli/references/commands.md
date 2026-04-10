# Bright Data CLI — Full Command Reference

**Package:** `@brightdata/cli` | **Commands:** `brightdata` / `bdata` (shorthand) | **Requires:** Node.js >= 20

## Installation

```bash
# macOS / Linux
curl -fsSL https://cli.brightdata.com/install.sh | bash

# Any platform
npm install -g @brightdata/cli

# Without installing
npx --yes --package @brightdata/cli brightdata <command>
```

---

## Global Options

These flags work with any command:

| Flag | Description |
|------|-------------|
| `-k, --api-key <key>` | Override API key for this request |
| `--timing` | Show request timing info |
| `-v, --version` | Show CLI version |

---

## `bdata login`

Authenticate with Bright Data. Opens the browser for OAuth by default.

| Flag | Description |
|------|-------------|
| `-k, --api-key <key>` | Use API key directly (skips browser) |
| `-c, --customer-id <id>` | Bright Data account ID (optional) |
| `-d, --device` | Use device flow for SSH/headless environments |

**What happens on login:**
1. Opens browser for OAuth (or uses device flow / direct API key)
2. Validates the API key
3. Saves credentials locally (`~/.config/brightdata-cli/credentials.json`)
4. Checks for required zones (`cli_unlocker`, `cli_browser`)
5. Creates missing zones automatically
6. Sets `cli_unlocker` as default zone if none configured

```bash
bdata login                        # Browser OAuth (recommended)
bdata login --device               # Headless/SSH environments
bdata login --api-key <key>        # Direct API key
```

---

## `bdata logout`

Clear stored credentials.

```bash
bdata logout
```

---

## `bdata scrape <url>`

Scrape any URL using Bright Data's Web Unlocker. Handles CAPTCHAs, JavaScript rendering, and anti-bot protections automatically.

| Flag | Description |
|------|-------------|
| `-f, --format <fmt>` | `markdown` (default), `html`, `screenshot`, `json` |
| `--country <code>` | ISO country code for geo-targeting (e.g. `us`, `de`, `jp`) |
| `--zone <name>` | Web Unlocker zone name |
| `--mobile` | Use a mobile user agent |
| `--async` | Submit async, return a snapshot ID |
| `-o, --output <path>` | Write output to file |
| `--json` | Force JSON output |
| `--pretty` | Pretty-print JSON output |

```bash
bdata scrape https://news.ycombinator.com
bdata scrape https://example.com -f html
bdata scrape https://amazon.com -f json --country us -o product.json
bdata scrape https://example.com -f screenshot -o page.png
bdata scrape https://example.com --async
bdata scrape https://docs.github.com | glow -
```

---

## `bdata search <query>`

Search Google, Bing, or Yandex via Bright Data's SERP API.

Google returns structured JSON with: organic results, ads, People Also Ask, related searches.
Bing/Yandex return markdown by default.

| Flag | Description |
|------|-------------|
| `--engine <name>` | `google` (default), `bing`, `yandex` |
| `--country <code>` | Localized results (e.g. `us`, `de`) |
| `--language <code>` | Language code (e.g. `en`, `fr`) |
| `--page <n>` | Page number, 0-indexed (default: `0`) |
| `--type <type>` | `web` (default), `news`, `images`, `shopping` |
| `--device <type>` | `desktop`, `mobile` |
| `--zone <name>` | SERP zone name |
| `-o, --output <path>` | Write output to file |
| `--json` | Force JSON output |
| `--pretty` | Pretty-print JSON output |

```bash
bdata search "typescript best practices"
bdata search "restaurants berlin" --country de --language de
bdata search "AI regulation" --type news
bdata search "web scraping" --page 1
bdata search "open source scraping" --json | jq -r '.organic[].link'
bdata search "bright data pricing" --engine bing
```

---

## `bdata pipelines <type> [params...] [options]`

Extract structured data from 40+ platforms. Triggers an async collection job, polls until ready, returns results.

| Flag | Description |
|------|-------------|
| `--format <fmt>` | `json` (default), `csv`, `ndjson`, `jsonl` |
| `--timeout <seconds>` | Polling timeout (default: `600`) |
| `-o, --output <path>` | Write output to file |
| `--json` | Force JSON output |
| `--pretty` | Pretty-print JSON output |

```bash
bdata pipelines list                                           # List all types
bdata pipelines linkedin_person_profile "https://linkedin.com/in/username"
bdata pipelines amazon_product "https://amazon.com/dp/B09V3KXJPB" --format csv -o product.csv
bdata pipelines instagram_profiles "https://instagram.com/username"
bdata pipelines amazon_product_search "laptop" "https://amazon.com"
bdata pipelines google_maps_reviews "https://maps.google.com/..." 7
bdata pipelines youtube_comments "https://youtube.com/watch?v=..." 50
```

See [pipelines.md](pipelines.md) for the full list of types and their parameters.

---

## `bdata status <job-id>`

Check status of an async snapshot job.

| Flag | Description |
|------|-------------|
| `--wait` | Poll until the job completes |
| `--timeout <seconds>` | Polling timeout (default: `600`) |
| `-o, --output <path>` | Write output to file |
| `--json` / `--pretty` | JSON output |

```bash
bdata status s_abc123xyz
bdata status s_abc123xyz --wait --pretty
bdata status s_abc123xyz --wait --timeout 300
```

---

## `bdata zones`

List and inspect Bright Data proxy zones.

```bash
bdata zones                        # List all active zones
bdata zones info <name>            # Full details for a zone
bdata zones --json -o zones.json   # Export as JSON
bdata zones info my_zone --pretty  # Pretty-print zone info
```

---

## `bdata budget`

View account balance and per-zone cost/bandwidth. Read-only.

| Subcommand | Description |
|------------|-------------|
| *(none)* | Quick account balance |
| `balance` | Balance + pending charges |
| `zones` | Cost & bandwidth table for all zones |
| `zone <name>` | Detailed cost & bandwidth for one zone |

| Flag | Description |
|------|-------------|
| `--from <datetime>` | Start of date range (e.g. `2024-01-01T00:00:00`) |
| `--to <datetime>` | End of date range |
| `--json` / `--pretty` | JSON output |

```bash
bdata budget
bdata budget balance
bdata budget zones
bdata budget zone my_zone
bdata budget zones --from 2024-01-01T00:00:00 --to 2024-02-01T00:00:00
```

---

## `bdata config`

View and manage CLI configuration.

| Subcommand | Description |
|------------|-------------|
| *(none)* | Show all config |
| `get <key>` | Get a single value |
| `set <key> <value>` | Set a value |

| Config Key | Description |
|------------|-------------|
| `default_zone_unlocker` | Default zone for `scrape` and `search` |
| `default_zone_serp` | Override zone for `search` only |
| `default_format` | Default output format: `markdown` or `json` |
| `api_url` | Override API base URL |

```bash
bdata config
bdata config set default_zone_unlocker my_zone
bdata config set default_format json
bdata config get default_zone_unlocker
```

---

## `bdata init`

Interactive setup wizard. Walks through authentication, zone selection, and default configuration.

| Flag | Description |
|------|-------------|
| `--skip-auth` | Skip the authentication step |
| `-k, --api-key <key>` | Provide API key directly |

```bash
bdata init
```

---

## `bdata skill`

Install Bright Data AI agent skills into coding agents (Claude Code, Cursor, Copilot, etc.).

| Subcommand | Description |
|------------|-------------|
| `add` | Interactive picker — choose skills + target agents |
| `add <name>` | Install a specific skill directly |
| `list` | List all available skills |

Available skills: `search`, `scrape`, `data-feeds`, `bright-data-mcp`, `bright-data-best-practices`

```bash
bdata skill add              # Interactive
bdata skill add scrape       # Direct install
bdata skill list             # See what's available
```

---

## Configuration Storage

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/brightdata-cli/` |
| Linux | `~/.config/brightdata-cli/` |
| Windows | `%APPDATA%\brightdata-cli\` |

Two files:
- `credentials.json` — API key (mode 0o600)
- `config.json` — Zones, output format, preferences

Priority order: CLI flags > Environment variables > config.json > Defaults
