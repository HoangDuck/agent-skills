# Output: readable first, evidence last

Write for someone who knows the product but has not read this code.

## Order

Headings in the user's language; drop one that has nothing to say.

1. **Short answer** — one to three sentences. No file names or identifiers except the one asked about.
2. **Affected features** — `Feature | What happens`, one row per thing a user can notice.
3. **Who is affected** — per role: what they can no longer do, and who can no longer see or reach them.
4. **Why** — the cause chain in plain steps.
5. **Workaround and fix** — what still works, how to repair data, the recommended next action.
6. **Checked / not checked** — repos and `branch@SHA`, what was run, what is only reasoned from code, what was left out.
7. **Appendix** — files, line numbers, statuses, matrices. Long ones go to a file; link it.

When both scopes were checked, split sections 2 and 3 into **Inside the module** (which flow and step) and **Between modules** (which other feature or role), then add one table `Step in this module | Reaches | Effect outside`. A single scope needs no split; say which was checked.

## Example

Not `products/views.py:120 excluded, buyer, LIVE` in the body, but:

> | Browse products | The seller's products disappear |

with `products/views.py:120` in the appendix.

## Rules

- Name features as the user sees them (screen, button, report), not endpoints, classes or paths.
- Translate statuses in the body: `LIVE` → in use · `DEAD` → code exists but cannot be reached · `API_ONLY` → backend only, no app uses it · `NO_ROUTE` → the app calls something the backend does not have · `UNVERIFIED` → not checked.
- Explain a technical term the first time, or replace it.
- One idea per table cell; at most three columns before the appendix.
- Sections 1–6 fit in about one and a half screens. Completeness belongs in the appendix, not in longer sentences.
- Mark consequences reasoned but not run, in the user's language (Vietnamese: "suy ra từ code, chưa chạy").
- End with at most one decision for the user, with your recommendation.
