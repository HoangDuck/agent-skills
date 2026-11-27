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

For a developer who has not read it.

- The path per entry point: `trigger → UI or route → state or handler → service → data / external → response → UI update`. One line per hop: component, what it does, what it reads and writes.
- Data: the main models and fields touched, where each is written and read, what is persisted vs in memory.
- Side effects: jobs queued, events emitted, caches touched, external calls, files written.
- Error path: where errors are caught, converted, shown or swallowed.
- Diagram: `sequenceDiagram` across the real components (keep to 4–7 participants; group the rest).

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
