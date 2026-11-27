# Walking through a change

## Find the range

| User says | Range |
|---|---|
| "nhánh này", nothing | `$(git merge-base <default> HEAD)..HEAD` (default branch from `origin/HEAD`, else `main`, else `master`) |
| a branch name | `$(git merge-base <default> <branch>)..<branch>` |
| "PR 12" | the PR's head branch if fetched; else ask for the branch name |
| a commit or `a..b` | as given (one commit → `<sha>^..<sha>`) |
| "chưa commit" | working tree vs `HEAD` (`diffmap.sh --worktree`) |

Read the range without switching branches: `git show <ref>:<path>` for files not checked out. State the range and `branch@SHA` in the first line.

## What to say about a change

- **Before vs after** for each affected flow: which steps are new, changed or removed. Mark them in the diagrams (`:::new`, `:::changed`, or a note) and in tables (`MỚI`, `ĐỔI`, `BỎ`).
- **Wiring:** does every new piece connect? New screen reachable from a menu or route, new endpoint called by a client, new job scheduled, new config read, migration present for new fields.
- **Callers of changed code:** for each changed public function, endpoint, model field or contract, who else uses it and whether they still fit.
- **Tests:** what the added tests actually assert; flows with no test.

## AI-code checklist

Check each; report only what you found, with `file:line`.

| Look for | Why it matters |
|---|---|
| Code written but never reached (unused functions, screens, endpoints, params) | looks done, does nothing |
| Duplicates of helpers, models or constants that already exist | two sources of truth |
| Hard-coded values, sample data, fake IDs, `TODO`, stubbed returns, mock left in place | works in demo only |
| Swallowed errors (`catch` that logs or ignores), missing error states in UI | silent failure |
| Contract drift: client field names, types or enums not matching the server | breaks at runtime |
| Changes outside the asked scope (renames, reformatting, unrelated files) | hidden risk in review |
| Missing permission, tenant or ownership checks on new endpoints or queries | data leak |
| Money, dates and timezones handled ad hoc | wrong numbers |
| New dependencies, config keys, env vars or migrations not documented | breaks on deploy |
| Tests that only assert mocks or happy path | false confidence |
