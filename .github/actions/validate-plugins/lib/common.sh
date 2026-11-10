#!/usr/bin/env bash
# Shared helpers for validate-plugins action scripts.
# Source this at the top of every script: source "$ACTION_PATH/lib/common.sh"

set -euo pipefail

# ---- logging ---------------------------------------------------------------

log()   { printf '%s\n' "$*"; }
info()  { printf '::notice::%s\n' "$*"; }
warn()  { printf '::warning::%s\n' "$*"; }
error() { printf '::error::%s\n' "$*"; }
die()   { error "$*"; record_result "fatal" "fail" "die" "$*"; exit 1; }

group_start() { printf '::group::%s\n' "$*"; }
group_end()   { printf '::endgroup::\n'; }

# ---- result tracking -------------------------------------------------------
# Scripts append findings here; 90-report.sh reads it.

RESULTS_FILE="${VALIDATE_TMP:-./.validate-tmp}/results.jsonl"

record_result() {
  local step="$1" status="$2" subject="$3" detail="${4:-}"
  mkdir -p "$(dirname "$RESULTS_FILE")"
  jq -cn \
    --arg step "$step" \
    --arg status "$status" \
    --arg subject "$subject" \
    --arg detail "$detail" \
    '{step:$step, status:$status, subject:$subject, detail:$detail}' \
    >> "$RESULTS_FILE"
}

# ---- safety predicates / assertions ---------------------------------------

# Returns 0 if the value contains shell metacharacters or whitespace.
has_unsafe_chars() {
  case "$1" in
    *'$'*|*'`'*|*';'*|*'&'*|*'|'*|*'('*|*')'*|*'<'*|*'>'*|*' '*|*'	'*|*'"'*|*"'"*|*'\'*)
      return 0 ;;
  esac
  return 1
}

assert_safe_string() {
  local label="$1" value="$2"
  if has_unsafe_chars "$value"; then
    die "$label contains unsafe characters: $value"
  fi
}

# URL must be https://<allowed-host>/<safe-chars> only.
# Host must be in ALLOWED_HOSTS (space-separated) and must not be a bare IP.
# SSRF guard: prevents cloning from metadata endpoints / internal ranges.
assert_safe_url() {
  local url="$1"
  assert_safe_string "url" "$url"
  if [[ ! "$url" =~ ^https://[A-Za-z0-9./_-]+$ ]]; then
    die "url does not match ^https://[A-Za-z0-9./_-]+\$ : $url"
  fi
  local host="${url#https://}"
  host="${host%%/*}"
  if [[ "$host" =~ ^[0-9.]+$ ]] || [[ "$host" =~ : ]]; then
    die "url host is a bare IP address (not permitted): $host"
  fi
  : "${ALLOWED_HOSTS:?ALLOWED_HOSTS must be set (action.yml provides the default)}"
  local allowed="$ALLOWED_HOSTS"
  local ok=""
  for h in $allowed; do
    if [[ "$host" == "$h" ]] || [[ "$host" == *".$h" ]]; then
      ok=1; break
    fi
  done
  if [[ -z "$ok" ]]; then
    die "url host '$host' is not in the allowlist ($allowed)"
  fi
}

# SHA must be exactly 40 lowercase hex.
assert_safe_sha() {
  local sha="$1"
  if [[ ! "$sha" =~ ^[0-9a-f]{40}$ ]]; then
    die "sha is not a 40-char lowercase hex string: $sha"
  fi
}

# Path must be relative, no .., safe chars only.
assert_safe_path() {
  local p="$1"
  assert_safe_string "path" "$p"
  if [[ "$p" == /* ]] || [[ "$p" == *".."* ]]; then
    die "path is absolute or contains '..': $p"
  fi
}

# ---- CLI validation helper -------------------------------------------------
# Runs `claude plugin validate <path>`, classifies pass/warn/fail, honours
# FAIL_ON_WARNINGS, records the result. Returns 0 on pass/warn, 1 on fail.
cli_validate() {
  local step="$1" subject="$2" path="$3"
  local out
  if out="$(claude plugin validate "$path" 2>&1)"; then
    log "$out"
    if grep -qE '^⚠|passed with warnings' <<<"$out"; then
      if [[ "${FAIL_ON_WARNINGS:-false}" == "true" ]]; then
        error "$subject: warnings (fail-on-warnings is set)"
        record_result "$step" "fail" "$subject" "$out"
        return 1
      fi
      warn "$subject: warnings"
      record_result "$step" "warn" "$subject" "$out"
    else
      record_result "$step" "pass" "$subject" ""
    fi
    return 0
  fi
  error "$subject: claude plugin validate failed"
  log "$out"
  record_result "$step" "fail" "$subject" "$out"
  return 1
}

# ---- external manifest resolution ------------------------------------------
# Resolve the plugin manifest to validate for an external (cloned) plugin.
# Echoes the manifest path on success (rc 0); rc 1 = no manifest found and the
# entry is NOT strict:false.
#
# Why the strict:false branch exists: a strict:false (skills-only) plugin
# legitimately ships NO plugin.json — the marketplace SYNTHESIZES a manifest from
# the entry's inline fields plus auto-discovered skills/commands/agents, and the
# plugin loads fine. But `claude plugin validate` operates on a manifest file, so
# without this branch step 30 hard-fails every strict:false external plugin for
# "no plugin manifest" — a false positive. We mirror the marketplace by
# synthesizing a minimal manifest ({name}) into the cloned target and validating
# that. (The clone/SHA/subdir checks in step 30 still run first; the marketplace-
# level schema check in step 20 still validates the entry holistically.)
#
# Synthesis writes ONLY into the throwaway clone dir (removed after validation),
# never the source repo. Args: $1=target dir, $2=entry name, $3=strict ("false"
# relaxes; any other value, incl. unset/true, requires a real manifest).
#
# Exit codes (so the caller need not re-derive what happened):
#   0 = an existing manifest was found and is echoed
#   2 = no manifest existed; a minimal one was synthesized (strict:false) + echoed
#   1 = no manifest and not strict:false, OR synthesis failed (fail-closed: the
#       caller treats this as a hard "no manifest" failure rather than validating
#       a path that may not exist — see the set -e/subshell note below).
# NOTE: when called as `m="$(resolve_external_manifest …)"`, set -e is suppressed
# inside the command-substitution subshell, so the mkdir/jq guards below MUST
# return explicitly rather than relying on errexit to abort on failure.
resolve_external_manifest() {
  local target="$1" name="$2" strict="${3:-true}"
  if [[ -f "$target/.claude-plugin/plugin.json" ]]; then
    printf '%s' "$target/.claude-plugin/plugin.json"; return 0
  fi
  if [[ -f "$target/plugin.json" ]]; then
    printf '%s' "$target/plugin.json"; return 0
  fi
  if [[ "$strict" == "false" ]]; then
    mkdir -p "$target/.claude-plugin" || return 1
    jq -n --arg name "$name" '{name: $name}' > "$target/.claude-plugin/plugin.json" || return 1
    printf '%s' "$target/.claude-plugin/plugin.json"; return 2
  fi
  return 1
}

