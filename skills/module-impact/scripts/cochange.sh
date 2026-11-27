#!/usr/bin/env bash
# Files that historically change together with a module. Run from the repo root.
#   cochange.sh [MAX_FILES_PER_COMMIT] -- <module paths...>
# Commits touching more than MAX files (default 40) are skipped as noise.
set -euo pipefail
max=40
if [[ "${1:-}" =~ ^[0-9]+$ ]]; then max=$1; shift; fi
[[ "${1:-}" == "--" ]] && shift
[[ $# -gt 0 ]] || { echo "usage: $0 [max] -- <module paths...>" >&2; exit 2; }

git log --no-merges --full-diff --name-only --format='@@%h' -- "$@" | awk -v max="$max" '
  function flush(  i) {
    if (n > 0) { if (n <= max) { used++; for (i = 1; i <= n; i++) count[files[i]]++ } else skipped++ }
    n = 0
  }
  /^@@/ { flush(); next }
  NF    { files[++n] = $0 }
  END {
    flush()
    for (f in count) printf "%6d %s\n", count[f], f | "sort -rn | head -40"
    close("sort -rn | head -40")
    printf "commits used: %d, skipped (> %d files): %d\n", used, max, skipped
  }'
