#!/bin/bash
# Validates an AI-Firstify assessment report follows the expected format.
# Usage: validate-report.sh <report-file>

FILE="$1"
if [ -z "$FILE" ]; then
  echo "Usage: validate-report.sh <report-file>"
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "FAIL: File not found: $FILE"
  exit 1
fi

ERRORS=0

# Check required sections
for section in "AI-Firstify Assessment Report" "Overall Score" "Priority Recommendations" "Detailed Findings" "Recommended Next Steps"; do
  if ! grep -q "$section" "$FILE"; then
    echo "FAIL: Missing section: $section"
    ERRORS=$((ERRORS + 1))
  fi
done

# Check all 7 dimensions are scored
for dim in "Project Structure" "Agent Architecture" "Skill Usage" "Scope & Complexity" "Context Hygiene" "Safety" "Workflow Design"; do
  if ! grep -q "$dim" "$FILE"; then
    echo "FAIL: Missing dimension: $dim"
    ERRORS=$((ERRORS + 1))
  fi
done

# Check scores use valid values
SCORE_COUNT=$(grep -oE 'GREEN|YELLOW|RED' "$FILE" | wc -l | tr -d ' ')
if [ "$SCORE_COUNT" -lt 7 ]; then
  echo "FAIL: Found $SCORE_COUNT scores, expected at least 7 (one per dimension)"
  ERRORS=$((ERRORS + 1))
fi

# Check priority levels exist
if ! grep -qE '\*\*\[(HIGH|MEDIUM|LOW)\]\*\*' "$FILE"; then
  echo "FAIL: No priority-tagged recommendations found (expected [HIGH], [MEDIUM], or [LOW])"
  ERRORS=$((ERRORS + 1))
fi

# Check metadata
if ! grep -q "Project:" "$FILE"; then
  echo "FAIL: Missing project name metadata"
  ERRORS=$((ERRORS + 1))
fi
if ! grep -q "Date:" "$FILE"; then
  echo "FAIL: Missing date metadata"
  ERRORS=$((ERRORS + 1))
fi

if [ "$ERRORS" -eq 0 ]; then
  echo "PASS: Report format is valid ($SCORE_COUNT scores found)"
else
  echo "FAIL: $ERRORS format issues found"
  exit 1
fi
