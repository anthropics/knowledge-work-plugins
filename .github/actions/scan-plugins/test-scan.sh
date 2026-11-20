#!/usr/bin/env bash
# Test suite for scripts/scan.sh — how the policy scan stages a target, invokes
# the claude CLI, and turns its output into verdicts. Network-free and
# model-free: `git`, `timeout` and `claude` are stubs on PATH. The claude stub
# records its argv, working directory and environment, then prints a canned
# result chosen by the plugin's own name.
#
# Runs identically on macOS bash 3.2 and Linux bash 5.x.

set -euo pipefail
cd "$(dirname "$0")"
ACTION_DIR="$PWD"
TMP="$(cd -P -- "$(mktemp -d)" && pwd -P)"; trap 'rm -rf "$TMP"' EXIT
failures=0; total=0

pass() { total=$((total+1)); printf 'ok %d - %s\n' "$total" "$1"; }
fail() { total=$((total+1)); failures=$((failures+1)); printf 'NOT OK %d - %s\n    got: %s\n' "$total" "$1" "${2:-}"; }
check() { if eval "$2"; then pass "$1"; else fail "$1" "${3:-}"; fi; }

SHA=0123456789abcdef0123456789abcdef01234567
BADSHA=ffffffffffffffffffffffffffffffffffffffff

# ---- fixtures: one "upstream repository" per directory ---------------------

mkplugin() { mkdir -p "$1/.claude-plugin"; jq -n --arg n "$2" '{name:$n}' > "$1/.claude-plugin/plugin.json"; }
FIX="$TMP/upstreams"
for n in ok noisy autherror errored stringpass failing inject; do mkplugin "$FIX/$n" "$n"; done
# Configuration a hostile repository could ship at its root.
mkdir -p "$FIX/ok/.claude"; echo '{}' > "$FIX/ok/.claude/settings.json"; echo '{}' > "$FIX/ok/.mcp.json"; echo x > "$FIX/ok/CLAUDE.md"
# Monorepo: the plugin is a subdirectory with a sibling that must stay out of view.
mkplugin "$FIX/mono/plugins/sub" ok; mkdir -p "$FIX/mono/plugins/sibling"; echo s > "$FIX/mono/plugins/sibling/file"
# Plugin directory swapped for a symlink that leaves the clone.
mkdir -p "$FIX/linked/plugins" "$TMP/outside"; echo secret > "$TMP/outside/secret"; ln -s "$TMP/outside" "$FIX/linked/plugins/sub"

# ---- stubs -----------------------------------------------------------------

STUBS="$TMP/stubs"; mkdir -p "$STUBS"
cat > "$STUBS/git" <<EOF
#!/usr/bin/env bash
# clone --quiet --depth 1 -- URL DEST | -C DEST fetch ... -- SHA | -C DEST ... checkout | cat-file
case " \$* " in
  *" clone "*) url="\${@: -2:1}"; dest="\${@: -1}"; src="$FIX/\$(basename "\$url" .git)"
               [ -d "\$src" ] || exit 128
               cp -R "\$src/." "\$dest/"; mkdir -p "\$dest/.git"; echo '[core]' > "\$dest/.git/config" ;;
  *" fetch "*) [ "\${@: -1}" = "$BADSHA" ] && exit 128; exit 0 ;;
  *" checkout "*) exit 0 ;;
  *) exit 1 ;;
esac
EOF
cat > "$STUBS/timeout" <<'EOF'
#!/usr/bin/env bash
[ "$1" = "-k" ] && shift 2
shift
exec "$@"
EOF
cat > "$STUBS/claude" <<EOF
#!/usr/bin/env bash
n="\$(jq -r .name plugin/.claude-plugin/plugin.json 2>/dev/null || echo unknown)"
rec="$TMP/rec/\$n"; mkdir -p "\$rec"
printf '%s\n' "\$@" > "\$rec/argv"; pwd -P > "\$rec/cwd"; env > "\$rec/env"; find . | sort > "\$rec/tree"
v() { jq -nc --argjson p "\$1" --arg s "\$2" --arg x "\$3" '{passes:\$p,summary:\$s,violations:\$x,may_make_external_network_calls:false,may_download_additional_software:false}'; }
out() { jq -nc --argjson e "\$1" --argjson so "\$2" '{type:"result",is_error:\$e,num_turns:7,duration_ms:1234,total_cost_usd:0.12,usage:{input_tokens:10,cache_creation_input_tokens:20,cache_read_input_tokens:30,output_tokens:40},result:"text"} + (if \$so == null then {} else {structured_output:\$so} end)'; }
case "\$n" in
  ok)          out false "\$(v true fine '')" ;;
  noisy)       echo "warning: something on stderr" >&2; out false "\$(v true fine '')" ;;
  autherror) jq -nc '{type:"result",is_error:true,result:"Authentication failed",num_turns:1,usage:{input_tokens:0,output_tokens:0}}'; exit 1 ;;
  errored)     out true "\$(v true fine '')" ;;
  stringpass)  out false '{"passes":"true","summary":"s","violations":""}' ;;
  failing)     out false "\$(v false bad 'hooks/x.sh phones home')" ;;
  inject)      out false "\$(v false \$'line1\n::error::forged' \$'first\n::set-output name=failed::[]\n##[error]forged')" ;;
esac
EOF
chmod +x "$STUBS"/*

# ---- runner ----------------------------------------------------------------

# run_scan LABEL ENTRIES_JSON [VAR=VALUE...] — sets RC, OUT (stdout+stderr),
# and the parsed step outputs SCANNED / FAILED / UNSCANNED / RESULT.
run_scan() {
  local label="$1" entries="$2"; shift 2
  local d="$TMP/run-$label"; rm -rf "$d" "$TMP/rec"; mkdir -p "$d"
  jq -n --argjson p "$entries" '{plugins:$p}' > "$d/marketplace.json"
  echo "policy text" > "$d/prompt.md"; : > "$d/output"; : > "$d/summary"
  set +e
  OUT="$(cd "$d" && env PATH="$STUBS:$PATH" \
      VALIDATE_LIB="$ACTION_DIR/../validate-plugins/lib/common.sh" VALIDATE_TMP="$d/vt" ACTION_PATH="$ACTION_DIR" \
      MARKETPLACE_PATH=marketplace.json BASE_REF=none ALLOWED_HOSTS="github.com" SCAN_TIMEOUT_SECS=5 \
      POLICY_PROMPT="$d/prompt.md" GITHUB_OUTPUT="$d/output" GITHUB_STEP_SUMMARY="$d/summary" \
      ANTHROPIC_API_KEY="" ANTHROPIC_FEDERATION_RULE_ID=fdrl_test ANTHROPIC_ORGANIZATION_ID=org \
      ANTHROPIC_SERVICE_ACCOUNT_ID=svac_test ANTHROPIC_IDENTITY_TOKEN_FILE="$d/jwt" \
      ACTIONS_ID_TOKEN_REQUEST_TOKEN=runner-secret ACTIONS_ID_TOKEN_REQUEST_URL=https://example.invalid \
      ACTIONS_RUNTIME_TOKEN=runner-secret GITHUB_TOKEN=runner-secret \
      "$@" bash "$ACTION_DIR/scripts/scan.sh" 2>&1)"
  RC=$?
  set -e
  SCANNED="$(sed -n 's/^scanned=//p' "$d/output")"; FAILED="$(sed -n 's/^failed=//p' "$d/output")"
  UNSCANNED="$(sed -n 's/^unscanned=//p' "$d/output")"; RESULT="$(sed -n 's/^result=//p' "$d/output")"
  SUMMARY="$(cat "$d/summary")"
}
entry() { jq -nc --arg n "$1" --arg r "${2:-$1}" --arg s "${3:-$SHA}" --arg p "${4:-}" \
  '{name:$n, source:({source:"url", url:("https://github.com/acme/"+$r+".git"), sha:$s} + (if $p=="" then {} else {path:$p} end))}'; }
names() { jq -c '[.[].name]' <<<"${1:-[]}"; }

# ---- a clean pass ----------------------------------------------------------

run_scan pass "[$(entry ok)]"
check "pass: exit 0, result=pass"            '[[ $RC -eq 0 && "$RESULT" == pass ]]'            "rc=$RC result=$RESULT"
check "pass: verdict recorded under the entry name" '[[ "$(names "$SCANNED")" == "[\"ok\"]" && "$(jq ".[0].passes" <<<"$SCANNED")" == true ]]' "$SCANNED"
check "pass: nothing failed or unscanned"    '[[ "$FAILED" == "[]" && "$UNSCANNED" == "[]" ]]' "failed=$FAILED unscanned=$UNSCANNED"
check "pass: usage line logged"              'grep -q "usage: {\"num_turns\":7,.*\"total_cost_usd\":0.12" <<<"$OUT"' "$OUT"

A="$TMP/rec/ok/argv"
for f in --restricted --safe-mode --strict-mcp-config --disable-slash-commands --no-session-persistence; do
  check "flags: $f is passed" 'grep -qx -- "$f" "$A"'
done
check "flags: --tools is exactly the three read-only file tools" '[[ "$(grep -x -A1 -- --tools "$A" | tail -1)" == "Read,Glob,Grep" ]]'
check "flags: --permission-prompts none"     '[[ "$(grep -x -A1 -- --permission-prompts "$A" | tail -1)" == "none" ]]'
check "flags: --bare is not passed"          '! grep -qx -- --bare "$A"'
check "flags: no tool is pre-approved"       '! grep -qxE -- "--allowed-tools|--allowedTools" "$A"'
check "flags: no extra directory is granted" '! grep -qx -- --add-dir "$A"'
check "prompt: policy text first, then where the files are" '[[ "$(sed -n 2p "$A")" == "policy text" ]] && grep -q "plugin/. subdirectory of the current working directory" "$A"'

T="$TMP/rec/ok/tree"
check "layout: working directory holds only plugin/"  '[[ "$(grep -c "^\./[^/]*$" "$T")" -eq 1 ]] && grep -qx "./plugin" "$T"' "$(cat "$T")"
check "layout: plugin manifest is under plugin/"      'grep -qx "./plugin/.claude-plugin/plugin.json" "$T"'
check "layout: repository config is below, never at, the working directory" '! grep -qxE "\./(\.claude|\.mcp\.json|CLAUDE\.md)" "$T" && grep -qx "./plugin/.mcp.json" "$T"'
check "layout: the clone's .git is gone"              '! grep -q "\.git" "$T"'

E="$TMP/rec/ok/env"
check "env: federation variables reach the CLI"       'grep -qx "ANTHROPIC_FEDERATION_RULE_ID=fdrl_test" "$E" && grep -q "^ANTHROPIC_IDENTITY_TOKEN_FILE=" "$E"'
check "env: an empty ANTHROPIC_API_KEY is not passed" '! grep -q "^ANTHROPIC_API_KEY=" "$E"'
check "env: runner tokens do not reach the CLI"       '! grep -qE "^(ACTIONS_|GITHUB_)|runner-secret" "$E"' "$(grep -E '^(ACTIONS_|GITHUB_)' "$E" || true)"

# ---- subdirectory plugins --------------------------------------------------

run_scan subdir "[$(entry ok mono "$SHA" plugins/sub)]"
check "subdir: scanned"                               '[[ "$(names "$SCANNED")" == "[\"ok\"]" ]]' "$SCANNED"
check "subdir: only the plugin directory is staged"   '! grep -q sibling "$TMP/rec/ok/tree"' "$(cat "$TMP/rec/ok/tree")"

run_scan symlink "[$(entry linked linked "$SHA" plugins/sub)]"
check "symlinked plugin directory: no verdict"        '[[ "$SCANNED" == "[]" && "$UNSCANNED" == "[\"linked\"]" ]]' "scanned=$SCANNED unscanned=$UNSCANNED"
check "symlinked plugin directory: CLI never started" '[[ ! -d "$TMP/rec" ]]'
check "symlinked plugin directory: target left intact" '[[ -f "$TMP/outside/secret" ]]'

# ---- output that is not a verdict ------------------------------------------

run_scan noisy "[$(entry noisy)]"
check "stderr noise does not break parsing"           '[[ "$(names "$SCANNED")" == "[\"noisy\"]" ]]' "$SCANNED"

for n in autherror errored stringpass; do
  run_scan "$n" "[$(entry "$n")]"
  check "$n: no verdict, reported as unscanned"       '[[ "$SCANNED" == "[]" && "$UNSCANNED" == "[\"$n\"]" ]]' "scanned=$SCANNED unscanned=$UNSCANNED"
done
check "no verdict: summary counts it"                 'grep -q "No verdict: 1" <<<"$SUMMARY"' "$SUMMARY"
check "no verdict: default only warns, result=incomplete" '[[ $RC -eq 0 && "$RESULT" == incomplete ]] && grep -q "^::warning::.*1 of 1 target(s) ended without a verdict" <<<"$OUT"' "rc=$RC result=$RESULT"

run_scan closed "[$(entry autherror),$(entry ok)]" FAIL_ON_UNSCANNED=true
check "fail-on-unscanned: exit 1, result=incomplete"  '[[ $RC -eq 1 && "$RESULT" == incomplete ]] && grep -q "^::error::.*1 of 2 target(s) ended without a verdict" <<<"$OUT"' "rc=$RC result=$RESULT"
check "fail-on-unscanned: the verdicts that exist are still reported" '[[ "$(names "$SCANNED")" == "[\"ok\"]" && "$UNSCANNED" == "[\"autherror\"]" ]]' "scanned=$SCANNED unscanned=$UNSCANNED"
run_scan closed-ok "[$(entry ok)]" FAIL_ON_UNSCANNED=true
check "fail-on-unscanned: a complete scan passes"     '[[ $RC -eq 0 && "$RESULT" == pass ]]' "rc=$RC result=$RESULT"

run_scan badsha "[$(entry ok ok "$BADSHA"),$(entry noisy)]"
check "fetch failure: unscanned, the loop carries on" '[[ "$UNSCANNED" == "[\"ok\"]" && "$(names "$SCANNED")" == "[\"noisy\"]" ]]' "scanned=$SCANNED unscanned=$UNSCANNED"

run_scan badname "[$(entry 'a b::x' ok)]"
check "unsafe entry name: unscanned, never echoed"    '[[ "$SCANNED" == "[]" && "$(jq length <<<"$UNSCANNED")" -eq 1 ]] && ! grep -q "a b::x" <<<"$OUT"' "$OUT"

run_scan dupes "[$(entry ok),$(entry ok noisy)]"
check "duplicate target names: hard error"            '[[ $RC -ne 0 && -z "$SCANNED" ]]' "rc=$RC scanned=$SCANNED"

# ---- policy failures -------------------------------------------------------

run_scan failing "[$(entry failing)]" FAIL_ON_FINDINGS=true
check "fail-on-findings: exit 1, result=fail"         '[[ $RC -eq 1 && "$RESULT" == fail && "$FAILED" == "[\"failing\"]" ]]' "rc=$RC result=$RESULT failed=$FAILED"
run_scan failing-soft "[$(entry failing)]"
check "default: a policy failure only warns"          '[[ $RC -eq 0 && "$FAILED" == "[\"failing\"]" ]] && grep -q "^::warning .*fails policy" <<<"$OUT"' "rc=$RC"

# ---- model text cannot drive the runner ------------------------------------

run_scan inject "[$(entry inject)]" FAIL_ON_FINDINGS=true
# Drop everything printed while command processing is paused, then look for
# commands the model text tried to smuggle in.
live="$(awk '/^::stop-commands::/{tok=substr($0,18); skip=1; next} skip && $0=="::" tok "::"{skip=0; next} !skip' <<<"$OUT")"
check "inject: no forged command outside a paused block" '! grep -qE "^::error::forged|^::set-output|^##\[error\]" <<<"$live"' "$live"
check "inject: the annotation is a single line"          '[[ "$(grep -c "^::error .*FAILS policy" <<<"$live")" -eq 1 ]] && grep -q "FAILS policy — first  *::set-output" <<<"$live"' "$live"
check "inject: summary table text sits in a code span"   'grep -q "| \`line1 ::error::forged\` |" <<<"$SUMMARY"' "$SUMMARY"

# ---- summary ----------------------------------------------------------------

echo
echo "test-scan: $((total-failures))/$total passed"
[[ "$failures" -eq 0 ]] || { echo "FAILURES: $failures"; exit 1; }
