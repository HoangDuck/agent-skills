#!/usr/bin/env bash
# Kiểm mọi skill trong skills/: có SKILL.md, frontmatter có name trùng tên thư mục và description,
# description không quá 1024 ký tự, link .md tương đối không gãy.
set -uo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
bad=0
for d in "$root"/skills/*/; do
  n=$(basename "$d"); f="$d/SKILL.md"
  [[ -f "$f" ]] || { echo "$n: thiếu SKILL.md"; bad=1; continue; }
  [[ "$(head -1 "$f")" == "---" ]] || { echo "$n: SKILL.md phải mở bằng frontmatter ---"; bad=1; }
  name=$(sed -n 's/^name: //p' "$f" | head -1)
  desc=$(sed -n 's/^description: //p' "$f" | head -1)
  [[ "$name" == "$n" ]] || { echo "$n: name '$name' phải trùng tên thư mục"; bad=1; }
  [[ -n "$desc" ]] || { echo "$n: thiếu description"; bad=1; }
  (( ${#desc} <= 1024 )) || { echo "$n: description dài ${#desc} > 1024"; bad=1; }
  while IFS= read -r md; do
    dir=$(dirname "$md")
    while IFS= read -r link; do
      [[ -e "$dir/$link" ]] || { echo "$n: link gãy ${md#$d} -> $link"; bad=1; }
    done < <(grep -o '](\([^)#: ]*\.md\))' "$md" | sed 's/](\(.*\))/\1/')
  done < <(find "$d" -name '*.md')
done
(( bad )) && exit 1
echo "OK: $(ls -d "$root"/skills/*/ | wc -l | tr -d ' ') skill"
