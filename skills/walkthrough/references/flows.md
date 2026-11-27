# The three flows

Build them from the same trace; each answers a different reader.

## Business flow — "what does this do for whom?"

For someone who knows the product, not the code.

- Actor and goal: who starts it and what they want done.
- Steps as the business sees them, including decisions ("if stock is short, the order is held").
- Rules found in code: limits, validations, permissions, statuses and their transitions, money and date handling. Quote the rule in plain words; put `file:line` in the appendix.
- Outcomes: what changes in the world (record created, email sent, balance moved) for success and for each failure.
- Diagram: `flowchart TD` with decisions as diamonds.

## Implementation flow — "how does the code carry it out?"

For a developer who has not read it. The goal is that they could explain the code without opening it.

1. **Hop table** per entry point: `trigger → UI or route → state or handler → service → data / external → response → UI update`. One row per hop: component (with `MỚI`/`ĐỔI` for a change), the function it runs, what it reads and writes.
2. **Diagram:** `sequenceDiagram` across the real components (4–7 participants; group the rest).
3. **Code walk:** for each hop that holds logic, a short excerpt copied from the file, then what the important lines do:
   - Keep 5–20 lines: the signature and the lines that decide something (validation, branching, calculation, query, write, error handling). Replace the rest with `// ...` (or the language's comment). Never invent or "clean up" code; copy it.
   - Header: `` `path/to/file.ext:start-end` — what this does ``.
   - Under it, a short list keyed by line number or symbol: what the line does and why it matters ("dòng 42: kiểm mã trước khi khoá dòng, nên hai request song song có thể cùng qua"). Point out surprising behaviour, implicit defaults, and what is *not* done.
   - For a change, show the diff instead (` ```diff `), trimmed the same way, so removed and added lines are visible.
   - Skip hops that only pass data along; say so in the table ("chỉ chuyển tiếp").
4. **Data shapes:** the request and response bodies, the main model or table fields touched, and the in-app state, each as a small example (JSON or the model's fields), noting which field each hop writes.
5. **Side effects:** jobs queued, events emitted, caches touched, external calls, files written — each with where it happens.
6. **Error path:** for each hop, what an error becomes (thrown, converted, retried, shown, swallowed), with the line.

Default depth: the main flow gets full code walks. Other flows get the hop table only, unless the user says "chi tiết". "Nhanh" drops the code walk.

## Usage flow — "how do I use or call it?"

For a user, tester or developer consuming it.

- End user: where to find it (menu, screen, button), what to enter, what they see on success and on each error.
- API or code consumer: endpoint or function, inputs and outputs with one realistic example, auth needed.
- Setup: config, flags, permissions, seed data, migrations required before it works.
- How to try it by hand: the shortest path to exercise the main flow, and which tests cover it.

## Failure walk (features, and "chi tiết" for changes)

Per main step: fails, times out, retried, double-submitted, back or cancel, app killed, out of order, partly done. What state is left and does the next attempt get past it? "No handling found" is a finding; cite where you looked.

## Tracing rules

- Search from the repo root with `git grep -n -w`; search every naming form (`snake_case`, `camelCase`, wire name, label text).
- Walk up until a trigger: `URL → API function → state → view → whoever builds the view → menu / route / button`, and `route → handler → service → model`, plus jobs, signals, admin, imports.
- Registered is not used: DI registration, route tables, `lazyPut`, providers and handlers count only when something reaches them.
- An empty search counts only if the same pattern finds the definition.
- Docs and comments are claims; code wins. Report mismatches.
