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

For a developer who has not read it: enough to explain the code without opening it, in as few lines as possible.

1. **Hop table**, one row per hop of the main flow: `# | Component (MỚI/ĐỔI) | Function | Writes | On error`. "Writes" names the state, field or side effect (job, event, external call); "On error" says what an error becomes (thrown, returned code, retried, shown, swallowed). Hops that only pass data along say "chuyển tiếp".
2. **Diagram:** `sequenceDiagram`, only when there are 4 or more participants.
3. **Code** for at most 4 hops, those that decide something (validation, branching, calculation, query, write, error handling):
   - Header `` `file:start-end` — what it does ``, then up to 10 lines copied from the file (a ` ```diff ` for a change). Trim the rest with `// ...`; never rewrite code.
   - At most 3 notes under it, keyed by line: what the line does that matters, especially surprises, implicit defaults and what is missing.
4. **Request / response:** one small example, only if the flow crosses an API.

"Chi tiết" lifts the 4-hop limit and adds the other flows. "Nhanh" keeps only the hop table.

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
