---
name: module-impact
description: Use when asked about impact or dependencies of a module, field, API, screen or flow, inside one module or across a project's repos - who reads or writes some data, whether an API, screen or button is really reachable, how the steps of a flow affect each other, what a missing, empty, renamed or changed field breaks, or when an impact report, matrix, relation map or risk list is wanted. Vietnamese triggers - "check impact", "module nào depend số liệu", "view nào post/nhập số liệu vào", "api này có được gọi không", "màn này còn dùng không", "impact trong module", "flow nào bị ảnh hưởng", "đổi/thiếu field này ảnh hưởng gì", "ma trận impact", "bản đồ quan hệ".
argument-hint: "<hỏi bằng lời, ví dụ: checkout | thiếu currency thì báo cáo bị gì | api /api/orders/ còn dùng không>"
---

# Module Impact

Request: $ARGUMENTS (empty: ask what to check).

**A search hit is not an impact.** Count a path only when you can name what triggers it, and describe behaviour only for code you opened.

Read-only on source: write only into the report folder. Reply in the user's language and shape every answer per [output.md](references/output.md). `<skill>` means this skill's base directory.

The user asks in plain words. Never ask them about modes, scopes, flags, branches or repos; work those out yourself.

## 1. Setup

- Read `.claude/module-impact.project.md` in the current repo: repos, stacks, default branch, roles, report folder, relation store, conventions, known traps.
- No profile: current repo only, stack from its manifest files. Repos you see referenced (API base URLs, package names, sibling folders) but did not search go under "not checked". Offer once, at the end, to write a profile from [project.template.md](project.template.md).
- Per repo, record `branch@shortSHA` and whether the tree is dirty (`git -C <repo> status --porcelain`).
- **Read the checked-out working tree.** If its branch is not the default branch, say so in one line under "Checked". If the user names another branch ("trên nhánh dev"), read that ref without switching: `git grep -n -e <pat> <ref> -- <paths>` and `git show <ref>:<path>` (no `--untracked` with a ref), and add `"ref": "<ref>"` to every relation row.

## 2. Pick the mode from the question

| The question | Mode | Read |
|---|---|---|
| yes/no: is X used, called, reachable | `quick` | [trace](references/trace.md) |
| who reads or who writes X | `data` | trace |
| a field, param, config or enum value missing, empty, renamed or changed | `field` | [field](references/field.md), trace |
| steps or flows inside one module | `flow` | [flow](references/flow.md), trace |
| a module name alone, or "impact của module X" | `full` (both scopes) | flow, [module](references/module.md), field, trace, [relations](references/relations.md) |

Several may apply; combine them. Open with one plain sentence saying what you will check.

**Default: wide and complete.** Every repo in the profile, both directions, every affected place opened, all flows covered. More tokens for completeness is accepted. Stay on the question: no dependency catalogue for a yes/no or field question.

**Limits in words narrow it**, and then do exactly that, naming in one line what you left out:

| User says | Do |
|---|---|
| "nhanh", "trả lời nhanh" | smallest mode that answers; give counts instead of opening every reader |
| "trong module", "chỉ flow" | `flow` only; list exits, do not follow them |
| "liên module", "ai dùng" | cross only; no step tables |
| "chỉ backend", "chỉ app", a repo name | only those repos |
| "trên nhánh <b>" | read that ref (see Setup) |
| "lưu file", "xuất báo cáo" | write files (see below) |
| "lưu vào store", "ingest" | ingest validated rows, if the profile names a store |

**Ask only when you cannot tell what the target is:** one plain question listing the candidates, prepared from file names and hit counts. If you cannot ask, take the most likely target and say so.

## 3. Always

- Search each repo from its own root and follow "Search hygiene" in trace.md.
- Never state what happens elsewhere from a hit. A field left missing or empty that has readers: follow field.md for every reader, unless the user asked for a quick answer (then give the count and offer it).
- A follow-up reuses what you verified; read only the missing part.
- **Files:** write them in `full`, when asked, or when the appendix passes about 15 rows. Folder: the profile's report folder, else `docs/impact/<target>-<YYYY-MM-DD>/`. Matrices and maps come only from `<skill>/scripts/relations.py render` after `check` passes.
- Ingest only when asked and the profile names a store; otherwise never touch shared files.
- Static analysis unless you ran something. Anything unopened is `UNVERIFIED`.
