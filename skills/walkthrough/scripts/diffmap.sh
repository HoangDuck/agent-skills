#!/usr/bin/env bash
# Map of a change, grouped by folder (most churn first); generated, lock and asset files collapsed.
# Run from the repo root.
#   diffmap.sh                 current branch vs merge-base with the default branch
#   diffmap.sh <range>         e.g. main..feature, abc123^..abc123
#   diffmap.sh --worktree      uncommitted changes (staged + unstaged + untracked) vs HEAD
set -euo pipefail

default_branch() {
  local b c
  b=$(git symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##') || true
  for c in "$b" main master develop; do
    if [[ -n "$c" ]] && git rev-parse -q --verify "$c^{commit}" >/dev/null; then echo "$c"; return; fi
  done
  echo "không tìm thấy nhánh mặc định; truyền range, ví dụ main..HEAD" >&2; exit 2
}

mode=range
if [[ "${1:-}" == "--worktree" ]]; then
  mode=worktree; rev=HEAD; label="uncommitted vs HEAD"
elif [[ -n "${1:-}" ]]; then
  rev=$1; label=$1
else
  base=$(default_branch); rev="$(git merge-base "$base" HEAD)..HEAD"; label="$base...HEAD"
fi

echo "range: $label  @ $(git rev-parse --abbrev-ref HEAD)@$(git rev-parse --short HEAD)"
[[ $mode == range ]] && echo "commits: $(git rev-list --count "$rev" 2>/dev/null || echo '?')"

{
  git diff --numstat -M "$rev"
  [[ $mode == worktree ]] && git ls-files --others --exclude-standard | awk '{print "new\t-\t" $0}'
  true
} | awk -F'\t' '
  function newpath(p,   pre, post, mid) {
    if (match(p, /\{[^}]* => [^}]*\}/)) {
      pre = substr(p, 1, RSTART - 1); post = substr(p, RSTART + RLENGTH)
      mid = substr(p, RSTART + 1, RLENGTH - 2); sub(/.* => /, "", mid)
      p = pre mid post; gsub(/\/\//, "/", p); return p
    }
    if (p ~ / => /) sub(/.* => /, "", p)
    return p
  }
  function gen(p) {
    return p ~ /(^|\/)(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|pubspec\.lock|Podfile\.lock|go\.sum|composer\.lock|poetry\.lock|Cargo\.lock|Gemfile\.lock)$/ \
        || p ~ /\.(g|freezed|gr|config|mocks)\.dart$/ || p ~ /\.pb(\.gw)?\.go$/ || p ~ /_generated\./ \
        || p ~ /(^|\/)(dist|build|vendor|node_modules|\.dart_tool|Pods)\// || p ~ /\.min\.(js|css)$/ \
        || p ~ /\.(snap|svg|png|jpe?g|gif|webp|ico|ttf|otf|woff2?|pdf)$/
  }
  {
    a = $1; d = $2; p = newpath($3)
    if (gen(p)) { gc++; next }
    n = split(p, s, "/"); dir = (n > 2 ? s[1] "/" s[2] : (n == 2 ? s[1] : "."))
    tag = (a == "new" ? "   new" : (a == "-" ? "   bin" : sprintf("%+6d", a)))
    if ($3 ~ / => / && a == "0" && d == "0") tag = " moved"
    rm  = (d ~ /^[0-9]+$/ ? sprintf("-%d", d) : "")
    rows[dir] = rows[dir] sprintf("    %s %6s  %s\001", tag, rm, p)
    cnt[dir]++; tf++
    if (a ~ /^[0-9]+$/) { add[dir] += a; ta += a }
    if (d ~ /^[0-9]+$/) { del[dir] += d; td += d }
  }
  END {
    for (k in cnt) printf "%d\t%s\001%s  (%d files, +%d -%d)\001%s\n", add[k] + del[k], k, k, cnt[k], add[k], del[k], rows[k]
    printf "-1\t~\001total: %d files, +%d -%d%s\n", tf, ta, td, (gc ? sprintf("; %d generated/lock/asset files not listed", gc) : "")
  }' | sort -t"$(printf '\t')" -k1,1nr | cut -f2- | sed 's/^[^\x01]*\x01//' | tr '\001' '\n'
