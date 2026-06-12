#!/usr/bin/env bash
# validate-all.sh
# Runs validate-plugin.sh against every plugin directory in the repository.
#
# Usage:
#   ./scripts/validate-all.sh [repo-root]
#
# If repo-root is omitted, the parent directory of this script is used.
#
# Exit codes:
#   0  All plugins passed validation
#   1  One or more plugins failed validation

set -euo pipefail

# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
RESET='\033[0m'

# ---------------------------------------------------------------------------
# Locate paths
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${1:-"$(dirname "$SCRIPT_DIR")"}"
VALIDATE_SCRIPT="$SCRIPT_DIR/validate-plugin.sh"

if [[ ! -x "$VALIDATE_SCRIPT" ]]; then
  printf "${RED}ERROR:${RESET} validate-plugin.sh not found or not executable at:\n" >&2
  echo "  $VALIDATE_SCRIPT" >&2
  exit 1
fi

if [[ ! -d "$REPO_ROOT" ]]; then
  printf "${RED}ERROR:${RESET} Repo root '%s' is not a directory.\n" "$REPO_ROOT" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Discover plugin directories
# A directory is considered a plugin if it contains .claude-plugin/plugin.json
# We skip the repo root itself.
# ---------------------------------------------------------------------------
PLUGIN_DIRS=()
while IFS= read -r -d '' plugin_json; do
  plugin_dir="$(dirname "$(dirname "$plugin_json")")"
  # Skip the repo root
  if [[ "$plugin_dir" == "$REPO_ROOT" ]]; then
    continue
  fi
  PLUGIN_DIRS+=("$plugin_dir")
done < <(find "$REPO_ROOT" -name "plugin.json" -path "*/.claude-plugin/plugin.json" -print0 2>/dev/null)

if [[ ${#PLUGIN_DIRS[@]} -eq 0 ]]; then
  printf "${YELLOW}No plugins found in '%s'.${RESET}\n" "$REPO_ROOT"
  exit 0
fi

# Sort for consistent output
IFS=$'\n' PLUGIN_DIRS=($(sort <<<"${PLUGIN_DIRS[*]}")); unset IFS

echo ""
printf "${BOLD}Plugin Validation — $(date '+%Y-%m-%d %H:%M:%S')${RESET}\n"
printf "Repository: %s\n" "$REPO_ROOT"
printf "Plugins found: %d\n" "${#PLUGIN_DIRS[@]}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ---------------------------------------------------------------------------
# Run validate-plugin.sh for each plugin, capture pass/fail
# ---------------------------------------------------------------------------
PASSED=()
FAILED=()
WARNED=()

for plugin_dir in "${PLUGIN_DIRS[@]}"; do
  plugin_name="$(basename "$plugin_dir")"

  # Run the validator; capture exit code without aborting the loop
  if output="$("$VALIDATE_SCRIPT" "$plugin_dir" 2>&1)"; then
    echo "$output"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Distinguish clean pass vs pass-with-warnings
    if echo "$output" | grep -q "\[WARN\]"; then
      WARNED+=("$plugin_name")
    else
      PASSED+=("$plugin_name")
    fi
  else
    echo "$output"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    FAILED+=("$plugin_name")
  fi
done

# ---------------------------------------------------------------------------
# Final summary table
# ---------------------------------------------------------------------------
TOTAL=${#PLUGIN_DIRS[@]}
NUM_PASSED=$(( ${#PASSED[@]} + ${#WARNED[@]} ))
NUM_FAILED=${#FAILED[@]}

echo ""
printf "${BOLD}Overall Results${RESET}\n"
echo ""
printf "  Total plugins validated : %d\n" "$TOTAL"
printf "  ${GREEN}Passed${RESET}                  : %d\n" "$NUM_PASSED"
printf "  ${RED}Failed${RESET}                  : %d\n" "$NUM_FAILED"
echo ""

if [[ ${#PASSED[@]} -gt 0 ]]; then
  printf "  ${GREEN}Clean passes:${RESET}\n"
  for p in "${PASSED[@]}"; do
    printf "    ${GREEN}✓${RESET} %s\n" "$p"
  done
  echo ""
fi

if [[ ${#WARNED[@]} -gt 0 ]]; then
  printf "  ${YELLOW}Passed with warnings:${RESET}\n"
  for p in "${WARNED[@]}"; do
    printf "    ${YELLOW}~${RESET} %s\n" "$p"
  done
  echo ""
fi

if [[ ${#FAILED[@]} -gt 0 ]]; then
  printf "  ${RED}Failed:${RESET}\n"
  for p in "${FAILED[@]}"; do
    printf "    ${RED}✗${RESET} %s\n" "$p"
  done
  echo ""
  printf "${RED}Validation failed for %d plugin(s). See output above for details.${RESET}\n" "$NUM_FAILED"
  echo ""
  exit 1
fi

printf "${GREEN}All plugins passed validation.${RESET}\n"
echo ""
exit 0
