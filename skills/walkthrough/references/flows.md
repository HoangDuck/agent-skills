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

For a developer who will maintain it: they should understand in detail what runs underneath, in far less time than reading the code. **Detail lives in plain-word explanation, not in the amount of code shown.**

1. **Hop table**, one row per hop of the main flow: `# | Component (MỚI/ĐỔI) | Logic chính | Writes | On error`.
   - "Logic chính": in plain words, what this hop decides or computes, with the real values (limits, conditions, formulas, statuses), e.g. "từ chối nếu `used >= max_uses`; giảm = % × tổng, không trần". "chuyển tiếp" when it only passes data along.
   - "Writes": state, field or side effect (job, event, external call). "On error": what an error becomes (thrown, returned code, retried, shown, swallowed).
2. **Diagram:** `sequenceDiagram`, only when there are 4 or more participants.
3. **Code, only where the code itself is the point:** a bug or risk, money or data written, concurrency, security, or behaviour the table cannot convey in a sentence. At most 4 excerpts:
   - Header `` `file:start-end` — what it does ``, then up to 8 lines copied from the file (a ` ```diff ` for a change), trimmed with `// ...`. Never rewrite code.
   - At most 3 notes, keyed by line.
4. **Underneath (ẩn bên dưới):** what the framework or libraries do on this path that the code does not show: middleware and interceptors, DI and lifecycle (created, reused, disposed), ORM behaviour (lazy loading, transactions, hooks, soft delete), serialization and naming conversion, caching, retries, background isolates or goroutines. One line each, with where it is configured; only what is verified to apply.
5. **Request / response:** one small example, only if the flow crosses an API.

Depth: main flow gets all of the above; other flows get the hop table only. "Nhanh": hop table without the underneath section. "Chi tiết": every flow gets the full treatment and the excerpt limit rises to 8.

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
