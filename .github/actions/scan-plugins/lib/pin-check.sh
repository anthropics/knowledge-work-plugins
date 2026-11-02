#!/usr/bin/env bash
# lib/pin-check.sh — deterministic launcher pin-state classification for a
# plugin tree's declared MCP servers. Pure functions, no network, no
# module-scope side effects; bash + jq only (both already hard deps of this
# repo's CI). Sourced by scripts/static-pin-check.sh (the scan-plugins step)
# and by ../bump-plugin-shas/scripts/bump.sh (the bump gate).
#
# WHAT THIS DETECTS — the auto-exec unpinned-runtime class ONLY: an MCP server
# declared in a plugin's .mcp.json (or plugin.json mcpServers) whose `command`
# is a package-manager runner (npx/bunx/uvx/pipx) with a FLOATING package spec
# (dist-tag like @latest, a semver range, or a bare unversioned name that is
# not locally vendored). Declared servers launch at session start, so a
# floating spec means the code executed on the user's machine is resolved from
# a package registry at launch time — the marketplace entry's pinned
# source.sha does not fix it. Package invocations inside skills/commands/
# agents markdown are deliberately OUT of scope: those are agent-invoked and
# permission-gated at use time, a different (acceptable) trust shape — do NOT
# extend this scan to markdown bodies.
#
# Spec classes (per launcher spec):
#   pinned    — npm `pkg@1.2.3` (digit-led exact; prerelease/build metadata ok);
#               pip `pkg==1.2.3` (no wildcard); uvx `pkg@1.2.3` shorthand
#   floating  — dist-tag (`@latest`/`@dev`/any non-numeric tag), a range
#               (`@^1`, `pkg@1`, `pkg@1.2`, `>=`, `~=`, `==1.*`), or a bare
#               name (refined to `vendored` only by the filesystem test below)
#   bare      — npm name with no version (raw row; refine with
#               pin_check_refine_bare before judging)
#   vendored  — a bare npm name shipped at node_modules/<pkg> in the tree
#               (npx/bunx resolve the local install first → fixed by the SHA)
#   local     — `./`-style path or `${…}/`-placeholder path operand (ships in
#               the pinned tree)
#   vcsref    — `git+`/`github:`/URL/`owner/repo#ref` direct refs
#               (commit-pinnable, a different mechanism — never flagged here)
#   none      — no derivable spec (e.g. a `-c`/`--call` shell-string form) —
#               reported, never flagged
#
# Documented residual gaps (v1, carried from the source of record): `pnpm dlx`
# / `yarn dlx`, `sh -c "npx …"` wrappers, deno/bun `npm:`-specifier runs,
# uvx `--with` side-package specs.
#
# PROVENANCE / KEEP IN SYNC: this is a faithful extract of
# bryan-anthropic/mcp-local-directory `lib/plugin-launch-shape.sh`
# (launch_shape_pin_rows + the waiver helpers, as of 2026-08-12) plus the one
# filesystem-dependent step from `lib/audit-plugin-checks/p1-mcp-servers.sh`
# check P1.39 (the bare-name vendored-node_modules refinement). Those files
# remain the spec of record for the grammar; grammar changes land there first
# and are re-extracted here. `claude-plugins-community-internal` carries a
# byte-identical copy of this file under .github/scripts/ — keep the two
# copies diff-clean.
#
# Robustness contract (load-bearing — a hostile plugin-authored .mcp.json must
# never abort a `set -euo pipefail` caller): every jq index is `?`/type-
# guarded, a root-array / non-object manifest degrades to zero rows, and each
# jq call is `2>/dev/null || true`. Rows are emitted via jq `@tsv` (never
# string interpolation), so an embedded tab/newline in an attacker-controlled
# server name can neither forge nor split a row; read rows back with
# IFS=$'\t' / awk -F'\t' only.

# pin_check_rows <manifest_json> -> one TSV row per (server, spec):
# "<name>\t<launcher>\t<class>\t<spec>" for every npx/bunx/uvx/pipx-launched
# server. `bare` rows are raw — refine with pin_check_refine_bare.
pin_check_rows() {
  printf '%s' "$1" | jq -r '
    def npmclass($s):
      if   ($s | test("://") or ($s | test("^git[+]")) or ($s | test("^github:"))) then "vcsref"
      elif ($s | test("^[.]{0,2}/")) then "local"
      # An env-var placeholder PATH (${CLAUDE_PLUGIN_ROOT}/…) resolves inside the
      # installed plugin at runtime — SHA-fixed like a ./-path. The contains("/")
      # half is LOAD-BEARING: a pathless placeholder like `${UNSET:-evil@latest}`
      # is a registry-spec evasion, NOT a path — it falls through to
      # classification (→ floating, fail-toward-flagging).
      elif (($s | startswith("$")) and ($s | contains("/"))) then "local"
      # An unscoped owner/repo#<committish> operand is npx GitHub shorthand —
      # treated commit-pinnable ONLY when it carries a #ref: a REF-LESS
      # `npx user/repo` resolves the default-branch HEAD at session start — the
      # same source.sha defeat, and a one-token evasion if excluded. Ref-less
      # slash forms classify floating (fail toward flagging). Scoped @scope/name
      # never matches (leading @).
      elif (($s | startswith("@") | not) and ($s | contains("/")) and ($s | contains("#"))) then "vcsref"
      elif (($s | startswith("@") | not) and ($s | contains("/"))) then "floating"
      else
        (if ($s | startswith("@")) then ($s | ltrimstr("@") | split("@")) else ($s | split("@")) end) as $parts
        # Exact = a FULL 3-component semver (prerelease and/or build metadata ok —
        # both optional groups). `pkg@1` / `pkg@1.2` are npm RANGES (newest 1.x /
        # 1.2.x at install — the same source.sha defeat), not pins.
        | if ($parts | length) <= 1 then "bare"
          elif (($parts | last) | test("^[0-9]+[.][0-9]+[.][0-9]+(-[0-9A-Za-z.-]+)?([+][0-9A-Za-z.-]+)?$")) then "pinned"
          else "floating" end
      end;
    def pipclass($s):
      if   ($s | test("://") or ($s | test("^git[+]")) or ($s | test("^github:"))) then "vcsref"
      elif ($s | test("^[.]{0,2}/")) then "local"
      elif (($s | startswith("$")) and ($s | contains("/"))) then "local"
      # `==` must not carry a pip wildcard (`pkg==1.*` is a range).
      elif (($s | test("==[0-9]")) and (($s | contains("*")) | not)) then "pinned"
      # uv accepts the npm-style `pkg@<version-or-tag>` shorthand too
      # (`uvx ruff@0.3.0` is an exact pin; `uvx pkg@latest` floats). Reuse the
      # npm split; a non-pinned @-result is floating for pip launchers.
      elif ($s | contains("@")) then (npmclass($s) | if . == "pinned" then "pinned" else "floating" end)
      else "floating" end;
    def npmspecs($args):
      ["-p","--package"] as $pkgflags
      | ["--loglevel","--cache","--userconfig","--registry","--shell","--shell-auto-fallback","--node-arg","-n","-c","--call","--env-file"] as $vflags
      | (reduce $args[] as $a ({mode:"scan", specs:[], pos:null};
          if .pos != null then .
          elif .mode == "pkgval"  then (.specs += [$a] | .mode = "scan")
          elif .mode == "skipval" then (.mode = "scan")
          elif ($a | startswith("--package=")) then (.specs += [$a | sub("^--package=";"")])
          elif (($pkgflags | index($a)) != null) then (.mode = "pkgval")
          elif (($vflags   | index($a)) != null) then (.mode = "skipval")
          elif ($a | startswith("-")) then .
          else (.pos = $a) end))
      # npx semantics: with -p/--package the positional is the COMMAND to run
      # from the selected package(s), NOT a package spec — classifying it would
      # false-fire on `npx -p pkg@1.2.3 bin` (bin reads as a bare floating
      # name). Package flags win; the positional is a spec only when no package
      # flag selected one.
      | (if (.specs | length) > 0 then .specs
         elif .pos != null then [.pos]
         else [] end);
    def uvxspecs($args):
      ["--python","-p","--with","--with-requirements","--index","--index-url","--extra-index-url","-i","--constraint","-c","--exclude-newer","--cache-dir","--refresh-package","--env-file"] as $vflags
      | (reduce $args[] as $a ({mode:"scan", from:null, pos:null};
          if .mode == "fromval"  then (.from = $a | .mode = "scan")
          elif .mode == "skipval" then (.mode = "scan")
          elif ($a | startswith("--from=")) then (.from = ($a | sub("^--from=";"")))
          elif ($a == "--from") then (.mode = "fromval")
          elif (($vflags | index($a)) != null) then (.mode = "skipval")
          elif ($a | startswith("-")) then .
          elif (.pos == null) then (.pos = $a)
          else . end))
      | (if .from != null then [.from] elif .pos != null then [.pos] else [] end);
    def pipxspecs($args):
      ["--python","--pip-args","--index-url"] as $vflags
      | (reduce $args[] as $a ({mode:"scan", spec:null, pos:null, first:true};
          if .mode == "specval"  then (.spec = $a | .mode = "scan")
          elif .mode == "skipval" then (.mode = "scan")
          elif ($a | startswith("--spec=")) then (.spec = ($a | sub("^--spec=";"")))
          elif ($a == "--spec") then (.mode = "specval")
          elif (($vflags | index($a)) != null) then (.mode = "skipval")
          elif ($a | startswith("-")) then .
          elif (.first and ($a == "run" or $a == "install")) then (.first = false)
          elif (.pos == null) then (.pos = $a)
          else . end))
      | (if .spec != null then [.spec] elif .pos != null then [.pos] else [] end);
    (if (.mcpServers? // null) != null then .mcpServers else . end)
    | (if type == "object" then . else {} end)
    | to_entries[]
    | select((.value | type) == "object")
    | select((.value.command? // null | type) == "string")
    | .key as $name
    | ((.value.command | split("/") | last | ascii_downcase)) as $base
    | ((.value.args? // []) | (if type == "array" then . else [] end) | map(select(type == "string"))) as $args
    | (if   ($base | test("^npx([.](cmd|exe))?$"))  then {l:"npx",  kind:"npm"}
       elif ($base | test("^bunx([.](cmd|exe))?$")) then {l:"bunx", kind:"npm"}
       elif ($base | test("^uvx([.](cmd|exe))?$"))  then {l:"uvx",  kind:"pip"}
       elif ($base | test("^pipx([.](cmd|exe))?$")) then {l:"pipx", kind:"pip"}
       else null end) as $lk
    | select($lk != null)
    | (if $lk.kind == "npm" then npmspecs($args)
       elif $lk.l == "uvx"  then uvxspecs($args)
       else pipxspecs($args) end) as $specs
    | (if ($specs | length) == 0
         then [[$name, $lk.l, "none", ""]]
         else ($specs | map([$name, $lk.l, (if $lk.kind == "npm" then npmclass(.) else pipclass(.) end), .]))
       end)
    | .[] | @tsv
  ' 2>/dev/null || true
}

# pin_check_refine_bare <rows-TSV> <tree_root> — refine `bare` rows to
# `vendored` (a REAL local install: a non-symlink package dir carrying its
# package.json — a bare `mkdir node_modules/<pkg>` or a symlink out of tree
# must NOT buy the exemption) or `floating`. The spec is UNTRUSTED — a
# `..`-containing or empty spec is never path-tested: it classifies floating
# (fail toward flagging). npm launchers only; uvx/pipx have no bare class.
pin_check_refine_bare() {
  local rows="$1" root="$2" n l c s
  [ -n "$rows" ] || return 0
  while IFS=$'\t' read -r n l c s; do
    [ -z "$c" ] && continue
    if [ "$c" = "bare" ]; then
      case "$s" in
        ''|*..*) c="floating" ;;
        *) if [ ! -L "$root/node_modules/$s" ] && [ -f "$root/node_modules/$s/package.json" ]; then
             c="vendored"
           else
             c="floating"
           fi ;;
      esac
    fi
    printf '%s\t%s\t%s\t%s\n' "$n" "$l" "$c" "$s"
  done <<EOF
$rows
EOF
}

# pin_check_tree <tree_root> — classify every declared MCP server in the tree.
# Reads, in order: .mcp.json (root), .claude-plugin/.mcp.json, and the
# `mcpServers` object of .claude-plugin/plugin.json / plugin.json (extracted
# explicitly — a plugin.json's OTHER top-level objects must not be misread as
# servers). Emits refined TSV rows (bare already resolved to
# vendored/floating). Sources are concatenated; a server declared in two
# files yields two rows (both real declarations). node_modules resolution is
# rooted at <tree_root> (the plugin root — the runtime cwd for a declared
# server, whichever file declares it).
pin_check_tree() {
  local root="$1" rows="" r f
  for f in "$root/.mcp.json" "$root/.claude-plugin/.mcp.json"; do
    [ -f "$f" ] || continue
    r="$(pin_check_rows "$(cat "$f" 2>/dev/null || true)")"
    [ -n "$r" ] && rows="${rows:+$rows
}$r"
  done
  for f in "$root/.claude-plugin/plugin.json" "$root/plugin.json"; do
    [ -f "$f" ] || continue
    r="$(pin_check_rows "$(jq -c '.mcpServers? // {}' "$f" 2>/dev/null || true)")"
    [ -n "$r" ] && rows="${rows:+$rows
}$r"
  done
  [ -n "$rows" ] || return 0
  pin_check_refine_bare "$rows" "$root"
}

# pin_check_floating_specs <refined-rows-TSV> — print each floating spec, one
# per line (the set a waiver must fully cover).
pin_check_floating_specs() {
  printf '%s\n' "$1" | awk -F'\t' '$3=="floating" && $4 != "" {print $4}'
}

# pin_check_waiver_prefixes <slug> <waiver_file> -> rc 0 + prints the entry's
# space-separated package prefixes, iff the slug holds an entry WITH >=1
# prefix. Entry format: `<slug> <prefix> [<prefix>…]  # rationale + date +
# adjudicator`. Inline `#` comments and CRLF are stripped; slug match is exact
# and case-sensitive. Missing/unreadable file, unlisted slug, or a prefix-less
# entry -> rc 1 (no waiver; fails toward enforcement, never a silent waive).
pin_check_waiver_prefixes() {
  local slug="$1" waiver_file="$2" out
  [ -n "$slug" ] || return 1
  [ -f "$waiver_file" ] && [ -r "$waiver_file" ] || return 1
  out="$(awk -v s="$slug" '
    { sub(/\r$/, ""); sub(/#.*/, "") }
    NF >= 2 && $1 == s { o=$2; for (i = 3; i <= NF; i++) o = o " " $i; print o; f=1; exit }
    END { exit(f ? 0 : 1) }
  ' "$waiver_file" 2>/dev/null)" || return 1
  [ -n "$out" ] || return 1
  printf '%s\n' "$out"
}

# pin_check_specs_all_waived <specs (newline-sep)> <prefixes (space-sep)>
# -> rc 0 iff there is >=1 spec AND EVERY spec's package name matches an
# adjudicated prefix. A prefix ending in "/" is a scope prefix (package must
# START with it); any other prefix must EQUAL the package name. The package
# name = the spec minus a leading `--package=`, a trailing npm
# `@<version-or-tag>` (scope-aware — only an `@` after the first char
# strips), any pip version-operator tail, and a pip extras `[...]` suffix.
# Zero specs, or any unmatched spec -> rc 1 (fail toward enforcement).
pin_check_specs_all_waived() {
  local specs="$1" prefixes="$2" spec pkg p ok n=0
  [ -n "$specs" ] || return 1
  [ -n "$prefixes" ] || return 1
  while IFS= read -r spec; do
    [ -z "$spec" ] && continue
    n=$((n + 1))
    pkg="${spec#--package=}"
    # ORDER matters: strip the npm @-tail FIRST (a no-op when there is none —
    # the tail match excludes /), THEN any pip operator tail, THEN pip extras.
    pkg="$(printf '%s' "$pkg" | sed -E 's/(.)@[^@/]*$/\1/')"
    pkg="$(printf '%s' "$pkg" | sed -E 's/[=<>~!].*$//')"
    pkg="${pkg%%\[*}"
    ok=1
    for p in $prefixes; do
      case "$p" in
        */) case "$pkg" in "$p"*) ok=0 ;; esac ;;
        *)  [ "$pkg" = "$p" ] && ok=0 ;;
      esac
      [ "$ok" = 0 ] && break
    done
    [ "$ok" = 0 ] || return 1
  done <<EOF
$specs
EOF
  [ "$n" -ge 1 ]
}

# pin_check_entry_waived <slug> <floating_specs (newline-sep)> <waiver_file>
# -> rc 0 iff the slug holds a package-grained waiver entry AND every floating
# spec matches an adjudicated prefix. Missing slug/specs/file -> rc 1.
pin_check_entry_waived() {
  local slug="$1" specs="$2" waiver_file="${3:-}"
  [ -n "$waiver_file" ] || return 1
  local prefixes
  prefixes="$(pin_check_waiver_prefixes "$slug" "$waiver_file")" || return 1
  pin_check_specs_all_waived "$specs" "$prefixes"
}
