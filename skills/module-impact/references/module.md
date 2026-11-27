# Full: whole-module impact

Run [flow.md](flow.md) first, then this. Use any extra analysis tool the project profile names.

## 1. Handles

- Backend: module or app, data models, tables, URL paths, serializers or DTOs, error codes, jobs.
- Mobile: URL constants, API / repository / controller / page / model classes, route names.
- Web: API functions, slices or hooks, pages, route URLs.
- If the profile names a relation store, `grep` the module there. Old rows are claims: run `relations.py check` on them and report stale ones.

## 2. Readers, writers, anchors

Trace every read and write per [trace.md](trace.md). Then walk the anchors below in **both directions** — what the module uses, and what others use of it — and finish with the discovery sweep. For every field the module leaves missing or empty, follow [field.md](field.md); this is required.

| Group | `anchor`: look at (typical `key`) |
|---|---|
| Code | `variable`: globals, statics, shared reactive state, constants (`var:`) · `function`: helpers, utils, extensions (`func:`) · `method`: public methods called across modules, mixins, base classes (`method:`) · `model`: server models, serializers, enums ↔ client models, duplicate class names (`model:`) · `library`: shared internal packages; third-party only if behaviour matters (`lib:`) · `ui`: shared widgets, dialogs, theme tokens (`ui:`) · `i18n`: translation keys, error texts (`i18n:`) |
| Contract | `interface`: request/response shape, server fields vs client parsing keys, abstract classes, callbacks (`http:POST /api/x/`) · `route`: route names, menu entries, deep links (`route:`) · `event`: signals, sockets, push, event bus (`event:`) · `external`: third-party APIs, webhooks, payment or accounting sync (`external:`) · `hardware`: printer, terminal, scanner, sensors (`hardware:`) |
| Data | `database`: tables, FKs both ways, cascade, constraints, indexes, soft delete, raw SQL (`db:`) · `storage`: uploaded files, object-storage paths, generated documents (`storage:`) · `cache`: server cache, local storage keys, offline copies, singletons (`cache:`) · `seed`: code referenced from stored data — permission and view names, menu rows, error-code tables, fixtures (`seed:`) · `compat`: existing rows, data migrations, older app builds against a newer API (`compat:`) |
| Behaviour | `rule`: validation, uniqueness, business limits, error codes ↔ client mapping (`rule:`) · `permission`: permission classes, auth middleware, permission and menu-visibility keys (`permission:`) · `tenant`: organization scoping, org headers, plan gating (`tenant:`) · `format`: timezone, date strings, money units, rounding, enum strings (`format:`) · `timing`: init order, lifecycle, refresh after write (`timing:`) · `flow`: steps of one flow (`flow:`) · `concurrency`: transactions, locks, double submit, retries, idempotency (`concurrency:`) |
| Runtime and delivery | `config`: settings, env, feature flags (`config:`) · `middleware`: framework defaults, exception handlers, HTTP interceptors (`middleware:`) · `job`: cron, queues, management commands (`job:`) · `output`: reports, exports, receipts, emails, notifications (`output:`) · `audit`: activity log, author fields, analytics (`audit:`) · `release`: deploy order, migrations, unmerged branches touching the same files (`release:`) · `test`: tests, seeds and mocks encoding current behaviour (`test:`) · `docs`: specs and feature docs (`docs:`) · `client`: other repos or tools using the API or database directly (`client:`) · `other`: anything else, with a `note` (`other:`) |

### Discovery sweep (finds what the list misses)

1. **Co-change**, from each repo root: `bash <skill>/scripts/cochange.sh -- <module paths>`. Explain every high-count file you have not already listed. Nothing surviving means history told you nothing, not that there is no coupling.
2. **Literals:** grep every repo for the module's strings (paths, keys, codes, class and URL names used as text). Reflection and database-driven lookups do not show up as imports.
3. **Second hop:** for each live reader, who consumes *its* output (report → export → accounting)?
4. **Failure walk:** if this write failed, ran twice, arrived late or carried the wrong date, who notices?

## 3. Files

Write relation rows per [relations.md](relations.md) first, then `report.md`. It opens with sections 1–6 of [output.md](output.md); its appendix has these sections, every one present:

1. **Verdict** — one sentence on readers, one on writers; `branch@SHA` per repo.
2. **Readers** and **Writers** — `Where | What it does | Entry point | Status | Evidence`.
3. **Anchor checklist** — `Anchor | Uses | Used by | Shared with | Search done`. One row per anchor with a finding; one "none found" line naming the empty anchors; skipped ones with the reason. Then the discovery sweep result.
4. **Risk warnings** — `Level (HIGH/MEDIUM/LOW) | Risk | Trigger | Consequence | Evidence or "inferred"`. Consider: dead path mistaken for live, data written but never shown, date or timezone, missing permission, missing uniqueness, no edit or delete, no author recorded, contract mismatch, unmapped error codes, shared anchor with other owners, unmerged branch, older app builds.
5. **Missing fields** — the field.md table per field, or "none found".
6. **Change impact matrix** — `If this changes | Affected | Propagation (LIVE / ON_NEXT_LOAD / SNAPSHOT / RECOMPUTE) | Required action | Test to run`.
7. **Flow, access and anchor matrices, relation map** — pasted from `render`.
8. **Not checked** — repos out of scope, other tools reading the database, direct database access, older builds, anything not run.

In chat give the readable body, the HIGH and MEDIUM warnings in plain words, and links to both files.
