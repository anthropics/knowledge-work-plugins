#!/usr/bin/env bash
# Claude policy scan of changed external marketplace entries.
# Non-blocking by default; set FAIL_ON_FINDINGS=true to hard-fail on a policy
# failure and FAIL_ON_UNSCANNED=true to hard-fail on a target with no verdict.

source "$VALIDATE_LIB"

# Auth: either a static API key, or the WIF env-var set (the action's mint
# step exports ANTHROPIC_FEDERATION_RULE_ID + _IDENTITY_TOKEN_FILE etc.; the
# claude CLI reads those and exchanges the JWT itself). Unset an empty
# ANTHROPIC_API_KEY so the CLI doesn't see a blank X-Api-Key header.
if [[ -z "${ANTHROPIC_API_KEY:-}" && -z "${ANTHROPIC_FEDERATION_RULE_ID:-}" ]]; then
  die "no Anthropic auth: need ANTHROPIC_API_KEY or ANTHROPIC_FEDERATION_RULE_ID"
fi
[[ -z "${ANTHROPIC_API_KEY:-}" ]] && unset ANTHROPIC_API_KEY
: "${MARKETPLACE_PATH:?}"
: "${BASE_REF:?}"
: "${ALLOWED_HOSTS:?}"
: "${SCAN_TIMEOUT_SECS:?}"
[[ "$SCAN_TIMEOUT_SECS" =~ ^[0-9]+$ ]] || die "scan-timeout-secs must be an integer"

PROMPT_FILE="${POLICY_PROMPT:-$ACTION_PATH/policy/prompt.md}"
SCHEMA_FILE="$ACTION_PATH/policy/schema.json"
[[ -f "$PROMPT_FILE" ]] || die "policy prompt not found at $PROMPT_FILE"

workroot="$(mktemp -d)"
trap 'rm -rf "$workroot"' EXIT

# ---- determine targets ----------------------------------------------------

# Shared with static-pin-check.sh (lib/targets.sh) so the AI review and the
# static pin check resolve the identical target set.
source "$ACTION_PATH/lib/targets.sh"

group_start "Determine scan targets"

resolve_scan_targets "$MARKETPLACE_PATH" "$BASE_REF" "${SCAN_ALL_EXTERNAL:-false}" "$workroot/targets.json"

count="$(jq 'length' -- "$workroot/targets.json")"
log "Scan targets: $count"
group_end

# Verdicts are reported by entry name, so two targets sharing a name could
# pass one off as the other.
if [[ "$(jq '[.[].name] | length - (unique | length)' -- "$workroot/targets.json")" -ne 0 ]]; then
  die "duplicate entry names among the scan targets"
fi

if [[ "$count" -eq 0 ]]; then
  log "No external entries to scan."
  echo "scanned=[]" >> "${GITHUB_OUTPUT:-/dev/stdout}"
  echo "failed=[]" >> "${GITHUB_OUTPUT:-/dev/stdout}"
  echo "unscanned=[]" >> "${GITHUB_OUTPUT:-/dev/stdout}"
  echo "result=pass" >> "${GITHUB_OUTPUT:-/dev/stdout}"
  exit 0
fi

# ---- scan each target -----------------------------------------------------

scanned='[]'
failed='[]'
idx=0

entry_line() {
  grep -n "\"name\": \"$1\"" -- "$MARKETPLACE_PATH" 2>/dev/null | head -1 | cut -d: -f1 || true
}

# Model and CLI output is shaped by the scanned repository. Print it with
# workflow-command processing paused so it cannot emit commands of its own.
log_untrusted() {
  local tok
  tok="$(head -c 16 /dev/urandom | od -An -tx1 | tr -d ' \n')"
  printf '::stop-commands::%s\n%s\n::%s::\n' "$tok" "$1" "$tok"
}

# Same text inside an annotation: one line, bounded.
oneline() { printf '%s' "$1" | tr '\r\n' '  ' | cut -c1-500; }

# The CLI gets an explicit environment: its own settings, auth, proxy and
# locale variables. Everything else the runner exports to a step (the OIDC
# request token, runtime and cache tokens, ...) stays out of the process.
scan_env=(DISABLE_AUTOUPDATER=1)
for k in $(compgen -e); do
  case "$k" in
    PATH|HOME|TMPDIR|LANG|LC_ALL|NODE_EXTRA_CA_CERTS|SSL_CERT_FILE|\
    HTTP_PROXY|HTTPS_PROXY|NO_PROXY|http_proxy|https_proxy|no_proxy|\
    ANTHROPIC_*|CLAUDE_CODE_*)
      scan_env+=("$k=${!k}") ;;
  esac
done

while IFS= read -r ext; do
  idx=$((idx+1))
  name="$(jq -r '.name' <<<"$ext")"
  url="$(jq -r '.source.url // .source.repo // empty' <<<"$ext")"
  sha="$(jq -r '.source.sha // empty' <<<"$ext")"
  subdir="$(jq -r '.source.path // ""' <<<"$ext")"
  if [[ ! "$name" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]]; then
    printf '::warning file=%s::scan-plugins: target #%s has an unsafe name; skipping\n' "$MARKETPLACE_PATH" "$idx"
    continue
  fi
  line="$(entry_line "$name")"
  loc="file=$MARKETPLACE_PATH${line:+,line=$line}"

  group_start "Scan: $name"

  if [[ -z "$url" || -z "$sha" ]]; then
    printf '::warning %s::scan-plugins: %s has no url or sha; skipping\n' "$loc" "$name"
    group_end; continue
  fi
  if [[ "$url" =~ ^[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*$ ]]; then
    url="https://github.com/$url"
  fi
  if has_unsafe_chars "$url" || [[ ! "$url" =~ ^https://[A-Za-z0-9./_-]+$ ]]; then
    printf '::warning %s::scan-plugins: %s url unsafe; skipping\n' "$loc" "$name"
    group_end; continue
  fi
  host="${url#https://}"; host="${host%%/*}"
  ok=""; for h in $ALLOWED_HOSTS; do [[ "$host" == "$h" || "$host" == *".$h" ]] && { ok=1; break; }; done
  if [[ -z "$ok" ]]; then
    printf '::warning %s::scan-plugins: %s host not in allowlist; skipping\n' "$loc" "$name"
    group_end; continue
  fi
  if [[ ! "$sha" =~ ^[0-9a-f]{40}$ ]]; then
    printf '::warning %s::scan-plugins: %s sha malformed; skipping\n' "$loc" "$name"
    group_end; continue
  fi
  if [[ -n "$subdir" ]] && { has_unsafe_chars "$subdir" || [[ "$subdir" == *".."* ]]; }; then
    printf '::warning %s::scan-plugins: %s subdir unsafe; skipping\n' "$loc" "$name"
    group_end; continue
  fi

  dest="$workroot/ext-$idx"
  mkdir -p -- "$dest"
  if ! timeout 120 git clone --quiet --depth 1 -- "$url" "$dest" 2>&1 \
     || ! git -C "$dest" fetch --quiet --depth 1 origin -- "$sha" 2>&1 \
     || ! git -C "$dest" -c advice.detachedHead=false checkout --quiet "$sha" -- 2>&1; then
    printf '::warning %s::scan-plugins: %s clone/fetch/checkout failed; skipping\n' "$loc" "$name"
    rm -rf -- "$dest"; group_end; continue
  fi
  target="$dest${subdir:+/$subdir}"
  if [[ ! -d "$target" ]]; then
    printf '::warning %s::scan-plugins: %s subdir not found at sha; skipping\n' "$loc" "$name"
    rm -rf -- "$dest"; group_end; continue
  fi

  # `-d` follows symlinks, and the directory staged below is what the scan can
  # read, so it must physically live inside the clone.
  dest_real="$(cd -P -- "$dest" 2>/dev/null && pwd -P || true)"
  target_real="$(cd -P -- "$target" 2>/dev/null && pwd -P || true)"
  if [[ -z "$dest_real" || -z "$target_real" ]] \
     || [[ "$target_real" != "$dest_real" && "$target_real" != "$dest_real"/* ]]; then
    printf '::warning %s::scan-plugins: %s plugin directory resolves outside the clone; skipping\n' "$loc" "$name"
    rm -rf -- "$dest"; group_end; continue
  fi

  # Isolation from the scanned repository, in two independent layers.
  #
  # 1. Layout. The CLI looks for project configuration (.claude/ settings and
  #    hooks, .mcp.json, CLAUDE.md, the git repository) in its working
  #    directory and that directory's parents. So the working directory is a
  #    fresh, otherwise empty one, and the plugin sits below it in plugin/,
  #    without the clone's .git.
  # 2. Flags. --restricted ignores user, project and local settings files,
  #    removes the tools that run code or fetch URLs, and confines the file
  #    tools to the working directory. --safe-mode turns off CLAUDE.md, skills,
  #    plugins, hooks, MCP servers and custom agents. --tools leaves only the
  #    three read-only file tools. No tool is pre-approved: reads inside the
  #    working directory need no approval, and --permission-prompts none denies
  #    anything that would ask.
  #
  # Not --bare: bare mode accepts only ANTHROPIC_API_KEY or an apiKeyHelper, so
  # the Workload Identity Federation variables are never read.
  # Needs claude-code 2.1.295 or later.
  stage="$workroot/stage-$idx"
  mkdir -p -- "$stage"
  rm -rf -- "$dest_real/.git"
  mv -- "$target_real" "$stage/plugin"

  prompt="$(cat "$PROMPT_FILE")"$'\n\n'"The plugin files are in the \`plugin/\` subdirectory of the current working directory, and the paths named here are relative to it. Read every relevant file (\`.claude-plugin/plugin.json\`, \`.mcp.json\`, \`skills/\`, \`agents/\`, \`commands/\`, \`hooks/\`, and any source) before deciding. If you cannot read the plugin's files, set \`passes\` to false and say so in \`violations\`."

  schema="$(cat "$SCHEMA_FILE")"
  errfile="$workroot/stderr-$idx"
  # </dev/null: claude -p reads stdin if available, which would consume the
  # remaining lines of the targets pipe and silently truncate the loop.
  # stderr is kept apart so a CLI warning cannot make the JSON unparseable.
  raw="$(cd "$stage" && env -i "${scan_env[@]}" \
           timeout -k 10 "$SCAN_TIMEOUT_SECS" \
           claude -p "$prompt" \
             --restricted \
             --safe-mode \
             --strict-mcp-config \
             --disable-slash-commands \
             --tools "Read,Glob,Grep" \
             --permission-prompts none \
             --no-session-persistence \
             --output-format json \
             --json-schema "$schema" \
           </dev/null 2>"$errfile" || true)"

  # --json-schema places the validated object at .structured_output;
  # .result is the text result. Only `passes` is gated. A run the CLI itself
  # reports as failed (auth, API, schema retries) is not a verdict.
  verdict="$(jq -c 'select(.is_error != true) | .structured_output // empty' <<<"$raw" 2>/dev/null || true)"
  if [[ -z "$verdict" ]] || ! jq -e '.passes | type == "boolean"' <<<"$verdict" >/dev/null 2>&1; then
    printf '::warning %s::scan-plugins: %s — no usable verdict; CLI output in step log\n' "$loc" "$name"
    log_untrusted "stdout: $raw"$'\n'"stderr: $(cat -- "$errfile" 2>/dev/null || true)"
    rm -rf -- "$dest" "$stage"; group_end; continue
  fi

  log "  usage: $(jq -c '{num_turns, duration_ms, total_cost_usd,
                          input_tokens: .usage.input_tokens,
                          cache_creation_input_tokens: .usage.cache_creation_input_tokens,
                          cache_read_input_tokens: .usage.cache_read_input_tokens,
                          output_tokens: .usage.output_tokens}' <<<"$raw" 2>/dev/null || echo '{}')"

  passes="$(jq -r '.passes' <<<"$verdict")"
  violations="$(oneline "$(jq -r '(.violations // "") | tostring' <<<"$verdict")")"

  # Join the static pin check's action-emitted fields (never model-produced —
  # the model's verdict cannot set them). PIN_RESULTS_FILE is exported by the
  # static-pin-check step; absent (e.g. standalone scan.sh use) → false/[].
  pin_extra='{"unpinned_autoexec_runtime":false,"unpinned_autoexec_specs":[]}'
  if [[ -n "${PIN_RESULTS_FILE:-}" && -f "${PIN_RESULTS_FILE:-}" ]]; then
    pin_extra="$(jq -c --arg n "$name" \
      '[.[] | select(.name==$n)][0] // {}
       | {unpinned_autoexec_runtime: (.unpinned_autoexec_runtime // false),
          unpinned_autoexec_specs:   (.unpinned_autoexec_specs   // [])}' \
      -- "$PIN_RESULTS_FILE" 2>/dev/null || echo '{"unpinned_autoexec_runtime":false,"unpinned_autoexec_specs":[]}')"
  fi

  scanned="$(jq -c --arg n "$name" --argjson v "$verdict" --argjson p "$pin_extra" '. + [($v + $p + {name:$n})]' <<<"$scanned")"

  log "  verdict:"
  log_untrusted "$(jq '.' <<<"$verdict" | sed 's/^/    /')"

  if [[ "$passes" == "true" ]]; then
    log "  ✓ $name passes"
  else
    failed="$(jq -c --arg n "$name" '. + [$n]' <<<"$failed")"
    if [[ "${FAIL_ON_FINDINGS:-false}" == "true" ]]; then
      printf '::error %s::scan-plugins: %s FAILS policy — %s\n' "$loc" "$name" "$violations"
    else
      printf '::warning %s::scan-plugins: %s fails policy (non-blocking) — %s\n' "$loc" "$name" "$violations"
    fi
  fi

  rm -rf -- "$dest" "$stage"
  group_end
done < <(jq -c '.[]' -- "$workroot/targets.json")

# Targets that ended without a verdict, whatever the reason (skipped by a
# guard, clone failure, timeout, auth or API error). Callers that need the
# scan to be complete gate on this being empty.
unscanned="$(jq -c --argjson s "$scanned" '[.[].name] - [$s[].name]' -- "$workroot/targets.json")"
ucount="$(jq 'length' <<<"$unscanned")"

# ---- summary --------------------------------------------------------------

fcount="$(jq 'length' <<<"$failed")"
{
  echo "## Policy scan"
  echo
  echo "Scanned $(jq 'length' <<<"$scanned") plugin(s). Policy failures: $fcount. No verdict: $ucount."
  echo
  if [[ "$(jq 'length' <<<"$scanned")" -gt 0 ]]; then
    echo "| Plugin | Passes | Unpinned auto-exec | Net calls | Installs sw | Summary |"
    echo "|---|---|---|---|---|---|"
    jq -r 'def neutralize: gsub("[|\n\r\\[\\]<>`]"; " ");
      .[] | "| \(.name) | \(if .passes then "✅" else "❌" end) | \(if .unpinned_autoexec_runtime then "⚠️ yes" else "no" end) | \(if .may_make_external_network_calls then "yes" else "no" end) | \(if .may_download_additional_software then "yes" else "no" end) | `\((.summary // "") | tostring | neutralize | .[0:120])` |"' <<<"$scanned"
  fi
  if [[ "$fcount" -gt 0 ]]; then
    echo
    echo "### Violations"
    jq -r --argjson s "$scanned" 'def neutralize: gsub("[|\n\r\\[\\]<>`]"; " ");
      $s[] | select(.passes==false) | "- **\(.name)** — `\((.violations // "") | tostring | neutralize | .[0:500])`"' <<<'null'
  fi
} >> "${GITHUB_STEP_SUMMARY:-/dev/stdout}"

{
  echo "scanned=$scanned"
  echo "failed=$failed"
  echo "unscanned=$unscanned"
} >> "${GITHUB_OUTPUT:-/dev/stdout}"

if [[ "$fcount" -gt 0 && "${FAIL_ON_FINDINGS:-false}" == "true" ]]; then
  echo "result=fail" >> "${GITHUB_OUTPUT:-/dev/stdout}"
  exit 1
fi
if [[ "$ucount" -gt 0 ]]; then
  echo "result=incomplete" >> "${GITHUB_OUTPUT:-/dev/stdout}"
  if [[ "${FAIL_ON_UNSCANNED:-false}" == "true" ]]; then
    printf '::error::scan-plugins: %s of %s target(s) ended without a verdict\n' "$ucount" "$count"
    exit 1
  fi
  printf '::warning::scan-plugins: %s of %s target(s) ended without a verdict (non-blocking)\n' "$ucount" "$count"
  exit 0
fi
echo "result=pass" >> "${GITHUB_OUTPUT:-/dev/stdout}"
