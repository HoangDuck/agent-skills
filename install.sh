#!/usr/bin/env bash
# Cài skill từ repo này vào Claude Code.
#   ./install.sh --list                     liệt kê skill
#   ./install.sh <skill...>                 cài cho mọi dự án (~/.claude/skills)
#   ./install.sh <skill...> --repo <path>   cài vào một repo (<path>/.claude/skills)
#   ./install.sh --all [--repo <path>]      cài tất cả
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
src="$here/skills"
dest="$HOME/.claude/skills"
names=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --list) for d in "$src"/*/; do n=$(basename "$d"); printf '%-24s %s\n' "$n" "$(sed -n 's/^description: //p' "$d/SKILL.md" | cut -c1-90)"; done; exit 0 ;;
    --all)  for d in "$src"/*/; do names+=("$(basename "$d")"); done ;;
    --repo) [[ -n "${2:-}" && -d "$2" ]] || { echo "--repo cần một thư mục có sẵn" >&2; exit 2; }
            dest="$(cd "$2" && pwd)/.claude/skills"; shift ;;
    -h|--help) sed -n '2,6p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)      names+=("$1") ;;
  esac
  shift
done
[[ ${#names[@]} -gt 0 ]] || { sed -n '2,6p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }

mkdir -p "$dest"
for n in "${names[@]}"; do
  [[ -f "$src/$n/SKILL.md" ]] || { echo "không có skill '$n' (xem ./install.sh --list)" >&2; exit 1; }
  if [[ -e "$dest/$n" ]]; then
    read -r -p "$dest/$n đã có. Ghi đè? [y/N] " ok
    [[ "$ok" == [yY] ]] || { echo "bỏ qua $n"; continue; }
    rm -rf "${dest:?}/$n"
  fi
  cp -R "$src/$n" "$dest/$n"
  echo "đã cài $n -> $dest/$n"
done
echo "Mở lại phiên Claude Code để nhận skill."
