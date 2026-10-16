#!/usr/bin/env bash
# lib/targets.sh — shared scan-target resolution for the scan-plugins action.
# Factored out of scripts/scan.sh so the AI policy scan and the static
# pin-check resolve the IDENTICAL target set (changed-external diff vs the
# full external corpus). Pure jq + git; no network.

# resolve_scan_targets <marketplace_path> <base_ref> <scan_all> <out_file>
# Writes a JSON array of {name, source} to <out_file>:
#   scan_all=true  → every external (object-source) entry
#   otherwise      → external entries added or changed vs <base_ref>'s copy of
#                    the marketplace (a missing base ref = empty base, i.e.
#                    everything external is a target)
resolve_scan_targets() {
  local marketplace_path="$1" base_ref="$2" scan_all="$3" out_file="$4" workdir
  if [[ "$scan_all" == "true" ]]; then
    jq -c '[.plugins[] | select(.source|type=="object") | {name, source}]' -- "$marketplace_path" > "$out_file"
    return 0
  fi
  workdir="$(dirname "$out_file")"
  if git cat-file -e "$base_ref:$marketplace_path" 2>/dev/null; then
    git show "$base_ref:$marketplace_path" > "$workdir/base.json"
  else
    echo '{"plugins":[]}' > "$workdir/base.json"
  fi
  jq -c -s \
    '(.[0].plugins | map({(.name): .}) | add // {}) as $b
     | [.[1].plugins[]
        | select(.source|type=="object")
        | select(($b[.name] // null) != .)
        | {name, source}]' \
    "$workdir/base.json" "$marketplace_path" > "$out_file"
}
