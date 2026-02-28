#!/usr/bin/env bash
# BetterCallClaude Privacy Check Hook
# Scans tool input for Anwaltsgeheimnis (attorney-client privilege) patterns
# per Art. 321 StGB and Art. 13 BGFA across DE/FR/IT
#
# This script reads the tool input JSON from stdin and checks for
# privileged content patterns. Returns hookSpecificOutput JSON on stdout
# when a match is found, or exits silently (exit 0) to allow.

set -euo pipefail

# Read tool input from stdin
INPUT=$(cat)

# Extract content fields from the JSON input
# Check: file content (Write), new_string (Edit), command (Bash)
CONTENT=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    parts = []
    # Write tool
    if 'content' in data:
        parts.append(data['content'])
    # Edit tool
    if 'new_string' in data:
        parts.append(data['new_string'])
    # Bash tool
    if 'command' in data:
        parts.append(data['command'])
    print(' '.join(parts))
except:
    print('')
" 2>/dev/null || echo "")

# If no content extracted, allow the operation
if [ -z "$CONTENT" ]; then
    exit 0
fi

# Anwaltsgeheimnis patterns across DE/FR/IT
# Source: BetterCallClaude privacy_mode.py
PATTERNS=(
    # German (DE)
    "anwalt.*geheimnis"
    "mandatsgeheimnis"
    "berufsgeheimnis"
    "geschäftsgeheimnis"
    "vertraulich"
    "streng[[:space:]]+vertraulich"
    # French (FR)
    "secret[[:space:]]+professionnel"
    "confidentiel"
    "strictement[[:space:]]+confidentiel"
    # Italian (IT)
    "segreto[[:space:]]+professionale"
    "riservato"
    "strettamente[[:space:]]+riservato"
    # Legal references (all languages)
    "Art\.[[:space:]]*321[[:space:]]*StGB"
    "Art\.[[:space:]]*13[[:space:]]*BGFA"
)

# Check content against each pattern (case-insensitive)
for pattern in "${PATTERNS[@]}"; do
    if echo "$CONTENT" | grep -iqE "$pattern"; then
        MATCHED_PATTERN="$pattern"
        echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"Potential attorney-client privileged content detected (Anwaltsgeheimnis, Art. 321 StGB). Pattern matched: ${MATCHED_PATTERN}. Please confirm this content should be written/sent.\"}}"
        exit 0
    fi
done

# No privileged content detected — silent exit allows the operation
exit 0
