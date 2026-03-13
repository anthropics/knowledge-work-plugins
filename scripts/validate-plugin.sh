#!/usr/bin/env bash
# validate-plugin.sh
# Validates a single plugin directory against the expected structure and content rules.
#
# Usage:
#   ./scripts/validate-plugin.sh <plugin-dir>
#
# Exit codes:
#   0  All checks passed (or only warnings)
#   1  One or more checks failed

set -euo pipefail

# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
RESET='\033[0m'

pass()  { printf "  ${GREEN}[PASS]${RESET} %s\n" "$*"; }
fail()  { printf "  ${RED}[FAIL]${RESET} %s\n" "$*"; FAIL_COUNT=$((FAIL_COUNT + 1)); }
warn()  { printf "  ${YELLOW}[WARN]${RESET} %s\n" "$*"; WARN_COUNT=$((WARN_COUNT + 1)); }
info()  { printf "        %s\n" "$*"; }

FAIL_COUNT=0
WARN_COUNT=0

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <plugin-dir>" >&2
  exit 1
fi

PLUGIN_DIR="${1%/}"   # strip trailing slash

if [[ ! -d "$PLUGIN_DIR" ]]; then
  printf "${RED}ERROR:${RESET} '%s' is not a directory.\n" "$PLUGIN_DIR" >&2
  exit 1
fi

PLUGIN_NAME="$(basename "$PLUGIN_DIR")"

echo ""
printf "${BOLD}Validating plugin: %s${RESET}\n" "$PLUGIN_NAME"
printf "  Path: %s\n" "$PLUGIN_DIR"
echo ""

# ---------------------------------------------------------------------------
# Helper: check YAML frontmatter contains a required field
#   Usage: has_frontmatter_field <file> <field>
#   Returns 0 if found, 1 if not
# ---------------------------------------------------------------------------
has_frontmatter_field() {
  local file="$1"
  local field="$2"
  # frontmatter is between the first and second '---' lines
  awk -v f="$field" '/^---/{c++; if(c==2) exit} c==1 && $0 ~ "^"f"[[:space:]]*:"' "$file" | grep -q .
}

# ---------------------------------------------------------------------------
# 1. .claude-plugin/plugin.json — required
# ---------------------------------------------------------------------------
printf "${BOLD}[1] .claude-plugin/plugin.json${RESET}\n"

PLUGIN_JSON="$PLUGIN_DIR/.claude-plugin/plugin.json"

if [[ ! -f "$PLUGIN_JSON" ]]; then
  fail ".claude-plugin/plugin.json not found (required)"
else
  pass ".claude-plugin/plugin.json exists"

  # Must be valid JSON
  if ! python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$PLUGIN_JSON" 2>/dev/null; then
    fail ".claude-plugin/plugin.json is not valid JSON"
  else
    pass ".claude-plugin/plugin.json is valid JSON"

    # Required fields: name, version, description
    for field in name version description; do
      value="$(python3 -c "
import json,sys
d=json.load(open(sys.argv[1]))
print(d.get(sys.argv[2], ''))
" "$PLUGIN_JSON" "$field" 2>/dev/null)"

      if [[ -z "$value" ]]; then
        fail "plugin.json missing required field: '$field'"
      else
        pass "plugin.json has '$field': $value"
      fi
    done
  fi
fi

echo ""

# ---------------------------------------------------------------------------
# 2. commands/*.md — YAML frontmatter with 'description'
# ---------------------------------------------------------------------------
printf "${BOLD}[2] commands/*.md — YAML frontmatter${RESET}\n"

COMMANDS_DIR="$PLUGIN_DIR/commands"

if [[ ! -d "$COMMANDS_DIR" ]]; then
  info "No commands/ directory (optional — skipping)"
else
  CMD_FILES=()
  while IFS= read -r -d '' f; do
    CMD_FILES+=("$f")
  done < <(find "$COMMANDS_DIR" -maxdepth 1 -name "*.md" -print0 2>/dev/null)

  if [[ ${#CMD_FILES[@]} -eq 0 ]]; then
    info "commands/ directory is empty (optional)"
  else
    for cmd_file in "${CMD_FILES[@]}"; do
      rel="${cmd_file#"$PLUGIN_DIR/"}"

      # Check file starts with --- (has frontmatter at all)
      first_line="$(head -1 "$cmd_file")"
      if [[ "$first_line" != "---" ]]; then
        fail "$rel: missing YAML frontmatter (file should start with ---)"
        continue
      fi

      if has_frontmatter_field "$cmd_file" "description"; then
        pass "$rel: has 'description' in frontmatter"
      else
        fail "$rel: frontmatter missing required 'description' field"
      fi
    done
  fi
fi

echo ""

# ---------------------------------------------------------------------------
# 3. skills/*/SKILL.md — YAML frontmatter with 'name' and 'description'
# ---------------------------------------------------------------------------
printf "${BOLD}[3] skills/*/SKILL.md — YAML frontmatter${RESET}\n"

SKILLS_DIR="$PLUGIN_DIR/skills"

if [[ ! -d "$SKILLS_DIR" ]]; then
  info "No skills/ directory (optional — skipping)"
else
  SKILL_FILES=()
  while IFS= read -r -d '' f; do
    SKILL_FILES+=("$f")
  done < <(find "$SKILLS_DIR" -name "SKILL.md" -print0 2>/dev/null)

  if [[ ${#SKILL_FILES[@]} -eq 0 ]]; then
    info "skills/ directory has no SKILL.md files (optional)"
  else
    for skill_file in "${SKILL_FILES[@]}"; do
      rel="${skill_file#"$PLUGIN_DIR/"}"

      first_line="$(head -1 "$skill_file")"
      if [[ "$first_line" != "---" ]]; then
        fail "$rel: missing YAML frontmatter (file should start with ---)"
        continue
      fi

      for field in name description; do
        if has_frontmatter_field "$skill_file" "$field"; then
          pass "$rel: has '$field' in frontmatter"
        else
          fail "$rel: frontmatter missing required '$field' field"
        fi
      done
    done
  fi
fi

echo ""

# ---------------------------------------------------------------------------
# 4. .mcp.json — valid JSON if present
# ---------------------------------------------------------------------------
printf "${BOLD}[4] .mcp.json (optional)${RESET}\n"

MCP_JSON="$PLUGIN_DIR/.mcp.json"

if [[ ! -f "$MCP_JSON" ]]; then
  info ".mcp.json not found (optional — skipping)"
else
  if ! python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$MCP_JSON" 2>/dev/null; then
    fail ".mcp.json is not valid JSON"
  else
    pass ".mcp.json is valid JSON"

    # Warn if mcpServers key is missing (expected structure)
    has_mcp_servers="$(python3 -c "
import json,sys
d=json.load(open(sys.argv[1]))
print('yes' if 'mcpServers' in d else 'no')
" "$MCP_JSON" 2>/dev/null)"

    if [[ "$has_mcp_servers" != "yes" ]]; then
      warn ".mcp.json does not contain a top-level 'mcpServers' key (expected)"
    else
      pass ".mcp.json has 'mcpServers' key"
    fi
  fi
fi

echo ""

# ---------------------------------------------------------------------------
# 5. ~~ placeholder check
#    Files that contain ~~ placeholders should have a CONNECTORS.md nearby
# ---------------------------------------------------------------------------
printf "${BOLD}[5] ~~ placeholder consistency${RESET}\n"

# Collect all .md files in the plugin (excluding CONNECTORS.md itself)
ALL_MD_FILES=()
while IFS= read -r -d '' f; do
  ALL_MD_FILES+=("$f")
done < <(find "$PLUGIN_DIR" -name "*.md" ! -name "CONNECTORS.md" -print0 2>/dev/null)

PLACEHOLDER_FILES=()
for md_file in "${ALL_MD_FILES[@]}"; do
  if grep -q "~~" "$md_file" 2>/dev/null; then
    PLACEHOLDER_FILES+=("$md_file")
  fi
done

if [[ ${#PLACEHOLDER_FILES[@]} -eq 0 ]]; then
  info "No ~~ placeholders found in .md files"
else
  CONNECTORS_MD="$PLUGIN_DIR/CONNECTORS.md"
  if [[ ! -f "$CONNECTORS_MD" ]]; then
    for pf in "${PLACEHOLDER_FILES[@]}"; do
      rel="${pf#"$PLUGIN_DIR/"}"
      warn "$rel: contains ~~ placeholders but CONNECTORS.md is missing"
    done
  else
    for pf in "${PLACEHOLDER_FILES[@]}"; do
      rel="${pf#"$PLUGIN_DIR/"}"
      pass "$rel: contains ~~ placeholders and CONNECTORS.md exists"
    done
  fi
fi

echo ""

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
printf "${BOLD}Summary for %s${RESET}\n" "$PLUGIN_NAME"

if [[ $FAIL_COUNT -eq 0 && $WARN_COUNT -eq 0 ]]; then
  printf "  ${GREEN}All checks passed.${RESET}\n"
elif [[ $FAIL_COUNT -eq 0 ]]; then
  printf "  ${GREEN}All checks passed${RESET} with ${YELLOW}%d warning(s)${RESET}.\n" "$WARN_COUNT"
else
  printf "  ${RED}%d check(s) failed${RESET}, ${YELLOW}%d warning(s)${RESET}.\n" "$FAIL_COUNT" "$WARN_COUNT"
fi

echo ""

if [[ $FAIL_COUNT -gt 0 ]]; then
  exit 1
fi

exit 0
