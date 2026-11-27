# Relation rows

Matrices and maps are generated from these rows: `relations.jsonl` in the report folder, one JSON object per line.

## Fields

| Field | Rule |
|---|---|
| `project` | repo folder name |
| `module` | `<project>/<module>` |
| `anchor` | an anchor from [module.md](module.md) |
| `type` | `import call http db event cache config cron external step impact` |
| `key` | `<anchor prefix>:<name>`, e.g. `http:POST /api/orders/` |
| `role` | `provides` (defines it) or `consumes` |
| `evidence` | `path:line`, relative to the repo |
| `symbol` | text that is on that exact line |
| `confidence` | `code` (you read it) or `inferred` |
| `access`, `status`, `entry` | data-flow rows: `read`/`write`, a status from trace.md, the trigger (`"none"` if there is none, and then not `LIVE`) |
| `ref` | only when you read a ref other than the working tree |
| `note` | required for `anchor: "other"` |

```json
{"project": "shop-web", "module": "shop-web/checkout", "anchor": "interface", "type": "http", "key": "http:POST /api/orders/", "role": "consumes", "access": "write", "status": "LIVE", "entry": "Cart page, Pay button", "evidence": "src/api/orders.ts:14", "symbol": "createOrder", "confidence": "code"}
```

## Flow rows

A **step** row: `type: "step"`, `anchor: "flow"`, `key: "flow:<name>"`, plus `step` (number), `name`, and `next` (names of following steps, or `"exit: <where>"`). Mark an extra entry step with `"start": true`, an unreachable one with `"status": "DEAD"`.

```json
{"project": "shop-web", "module": "shop-web/checkout", "anchor": "flow", "type": "step", "key": "flow:checkout", "role": "provides", "step": 1, "name": "Review cart", "next": ["exit: payment"], "evidence": "src/checkout/Cart.tsx:20", "symbol": "CartPage", "confidence": "code"}
```

A **state** row is a data-flow row with `flow` and `step` pointing at an existing step:

```json
{"project": "shop-web", "module": "shop-web/checkout", "anchor": "variable", "type": "cache", "key": "var:cartId", "role": "provides", "flow": "flow:checkout", "step": 1, "access": "write", "status": "LIVE", "entry": "Review cart", "evidence": "src/checkout/Cart.tsx:31", "symbol": "setCartId", "confidence": "code"}
```

## Script

`--root` is the folder that contains the repo folders (`..` from a repo root).

```bash
S=<skill>/scripts/relations.py
D=<report folder>
python3 $S check  $D/relations.jsonl --root ..     # must print OK; fix rows until it does
python3 $S render $D/relations.jsonl               # paste into the report, never hand-write
python3 $S ingest $D/relations.jsonl --root .. --into <store>   # only when asked
```

`check` proves the symbol is on the line, not that the status is right. `ingest` updates rows whose line moved instead of duplicating them, and holds back `DEAD`, `NO_ROUTE`, `UNVERIFIED` and `inferred` rows (`--keep-inferred` to include those).
