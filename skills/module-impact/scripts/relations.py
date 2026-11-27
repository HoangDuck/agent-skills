#!/usr/bin/env python3
"""Validate, render and ingest module-impact relation rows (JSONL).

  check  ROWS --root DIR                       every row valid, symbol really on its evidence line
  render ROWS                                  flow, access and anchor matrices, relation map
  ingest ROWS --root DIR --into STORE          check, then upsert into a shared store
         [--keep-inferred]

--root is the folder that contains the repo folders. Rows with "ref" are read from that
git ref (git show) instead of the working tree.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REQUIRED = ("project", "module", "anchor", "type", "key", "role", "evidence", "symbol", "confidence")
TYPES = set("import call http db event cache config cron external step impact".split())
ANCHORS = set("""
    variable function method model library ui i18n
    interface route event external hardware
    database storage cache seed compat
    rule permission tenant format timing flow concurrency
    config middleware job output audit release test docs client other
""".split())
STATUSES = {"LIVE", "DEAD", "API_ONLY", "NO_ROUTE", "UNVERIFIED"}
HELD = {"DEAD", "NO_ROUTE", "UNVERIFIED"}
# Identity ignores the line number, so a row whose code moved is updated, not duplicated.
IDENTITY = ("project", "module", "type", "key", "role", "access", "flow", "step", "ref", "file", "symbol")


def load(path):
    rows = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as error:
                sys.exit(f"{path}:{number}: invalid JSON: {error}")
    return rows


def is_int(value):
    return type(value) is int


def is_step(row):
    return row.get("type") == "step"


def inside(path, parent):
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def source_lines(root, row, file):
    base = Path(root).resolve()
    repo = (base / row["project"]).resolve()
    if not inside(repo, base) or not repo.is_dir():
        return None
    ref = row.get("ref")
    if ref:
        if str(ref).startswith("-") or os.path.isabs(file) or ".." in Path(file).parts:
            return None
        out = subprocess.run(["git", "-C", str(repo), "show", f"{ref}:{file}"], capture_output=True)
        return out.stdout.decode("utf-8", "replace").splitlines() if out.returncode == 0 else None
    target = (repo / file).resolve()
    if not inside(target, repo) or not target.is_file():
        return None
    return target.read_text(encoding="utf-8", errors="replace").splitlines()


def problems(row, root):
    found = [f"missing '{f}'" for f in REQUIRED if row.get(f) in (None, "")]
    if found:
        return found
    if row["anchor"] not in ANCHORS:
        found.append(f"unknown anchor '{row['anchor']}'")
    if row["anchor"] == "other" and not row.get("note"):
        found.append("anchor 'other' needs a 'note'")
    if row["type"] not in TYPES:
        found.append(f"unknown type '{row['type']}'")
    if row["role"] not in ("provides", "consumes"):
        found.append("role must be provides or consumes")
    if row["confidence"] not in ("code", "inferred"):
        found.append("confidence must be code or inferred")
    if "status" in row and row["status"] not in STATUSES:
        found.append(f"status must be one of {sorted(STATUSES)}")
    if "access" in row:
        if row["access"] not in ("read", "write"):
            found.append("access must be read or write")
        if "status" not in row:
            found.append("access row needs 'status'")
        if not row.get("entry"):
            found.append("access row needs 'entry' ('none' if there is no trigger)")
        elif row.get("status") == "LIVE" and str(row["entry"]).strip().lower().startswith("none"):
            found.append("LIVE row cannot have entry 'none'")
    if is_step(row) or row["anchor"] == "flow":
        if not (is_step(row) and row["anchor"] == "flow" and str(row["key"]).startswith("flow:")):
            found.append("step rows need type 'step', anchor 'flow' and key 'flow:<name>' together")
        if not is_int(row.get("step")) or not row.get("name") or not isinstance(row.get("next"), list):
            found.append("step row needs a number 'step', a 'name' and a list 'next'")
    if "flow" in row:
        if is_step(row):
            found.append("a step row must not have 'flow'; that field marks state rows")
        if not str(row["flow"]).startswith("flow:") or not is_int(row.get("step")) or "access" not in row:
            found.append("state row needs 'flow: flow:<name>', a number 'step' and 'access'")
    file, _, number = str(row["evidence"]).rpartition(":")
    lines = source_lines(root, row, file) if file and number.isdigit() else None
    if lines is None:
        where = f" at ref {row['ref']}" if row.get("ref") else ""
        found.append(f"evidence must be an existing path:line{where}, got '{row['evidence']}'")
    else:
        index = int(number) - 1
        if not 0 <= index < len(lines) or str(row["symbol"]) not in lines[index]:
            found.append(f"'{row['symbol']}' is not on {row['evidence']}")
    return found


def flows_of(rows):
    flows = {}
    for r in rows:
        if is_step(r) and is_int(r.get("step")) and r.get("name") and isinstance(r.get("next"), list):
            flows.setdefault(r["key"], []).append(r)
    return {key: sorted(steps, key=lambda r: r["step"]) for key, steps in flows.items()}


def flow_problems(rows):
    found, flows = [], flows_of(rows)
    for key, steps in flows.items():
        numbers, names = [r["step"] for r in steps], [r["name"] for r in steps]
        if len(set(numbers)) != len(numbers) or len(set(names)) != len(names):
            found.append(f"{key}: step numbers and names must be unique")
        by_name = {r["name"]: r for r in steps}
        for r in steps:
            for target in r["next"]:
                if target not in by_name and not str(target).startswith("exit:"):
                    found.append(f"{key} step {r['step']}: next '{target}' is not a step name or 'exit: ...'")
        queue = [steps[0]["name"]] + [r["name"] for r in steps if r.get("start")]
        seen = set()
        while queue:
            name = queue.pop()
            if name in by_name and name not in seen:
                seen.add(name)
                queue.extend(by_name[name]["next"])
        for r in steps:
            if r["name"] not in seen and r.get("status") != "DEAD":
                found.append(f"{key} step {r['step']} '{r['name']}' is unreachable: link it, mark 'start' or 'DEAD'")
    for r in rows:
        if "flow" in r and not is_step(r) and r.get("step") not in [x["step"] for x in flows.get(r["flow"], [])]:
            found.append(f"state '{r.get('key')}' points at undefined step {r.get('flow')} #{r.get('step')}")
    return found


def check(rows, root):
    bad = 0
    for number, row in enumerate(rows, 1):
        for problem in problems(row, root):
            print(f"row {number}: {problem}", file=sys.stderr)
            bad += 1
    for problem in flow_problems(rows):
        print(problem, file=sys.stderr)
        bad += 1
    if bad or not rows:
        sys.exit(f"FAILED: {bad} problem(s) in {len(rows)} row(s)")
    print(f"OK: {len(rows)} row(s)")


def quote(text):
    return str(text).replace('"', "'")


def render_flows(rows):
    flows = flows_of(rows)
    states = [r for r in rows if "flow" in r and not is_step(r)]
    for key, steps in flows.items():
        print(f"## {key}\n\n| # | Step | Next | Evidence |\n|---|---|---|---|")
        for r in steps:
            mark = " (DEAD)" if r.get("status") == "DEAD" else ""
            print(f"| {r['step']} | {r['name']}{mark} | {', '.join(map(str, r['next'])) or '-'} | `{r['evidence']}` |")
        ids = {r["name"]: f"s{r['step']}" for r in steps}
        dead = {r["name"] for r in steps if r.get("status") == "DEAD"}
        print("\n```mermaid\nflowchart TD")
        for r in steps:
            print(f'  s{r["step"]}["{r["step"]}. {quote(r["name"])}"]')
        exits = 0
        for r in steps:
            for target in r["next"]:
                if target not in ids:
                    ids[target] = f"x{exits}"
                    exits += 1
                    print(f'  {ids[target]}(["{quote(target)}"])')
                arrow = "-.->" if r["name"] in dead or target in dead else "-->"
                print(f"  s{r['step']} {arrow} {ids[target]}")
        print("```\n")
        own = [r for r in states if r["flow"] == key]
        if own:
            numbers = [r["step"] for r in steps]
            print("### State by step (R = reads, W = writes)\n")
            print("| State | " + " | ".join(f"#{n}" for n in numbers) + " |")
            print("|---|" + "---|" * len(numbers))
            for state in sorted({r["key"] for r in own}):
                cells = ["".join(sorted({r["access"][0].upper() for r in own if r["key"] == state and r["step"] == n})) or "-"
                         for n in numbers]
                print(f"| `{state}` | " + " | ".join(cells) + " |")
            print()
    if not states:
        return
    short = lambda r: f"{r['flow'][5:]} #{r['step']}"
    listing = lambda found: ", ".join(sorted({short(r) for r in found})) or "-"
    print("## Step coupling (changing a writer affects its readers)\n")
    print("| State | Written by | Read by | Crosses flows |\n|---|---|---|---|")
    only_read, only_written = [], []
    for state in sorted({r["key"] for r in states}):
        own = [r for r in states if r["key"] == state]
        writes = [r for r in own if r["access"] == "write"]
        reads = [r for r in own if r["access"] == "read"]
        if not writes:
            only_read.append(state)
        if not reads:
            only_written.append(state)
        shared = "YES" if len({r["flow"] for r in own}) > 1 else "-"
        print(f"| `{state}` | {listing(writes)} | {listing(reads)} | {shared} |")
    print("\n### Unmatched state (check: outside source, outside use, dead, or missing row)\n")
    print(f"- read, never written in these flows: {', '.join(f'`{s}`' for s in only_read) or 'none'}")
    print(f"- written, never read in these flows: {', '.join(f'`{s}`' for s in only_written) or 'none'}\n")


def render(rows):
    render_flows(rows)
    rows = [r for r in rows if not (is_step(r) or "flow" in r)]
    if not rows:
        return
    access = [r for r in rows if "access" in r]
    if access:
        # keys are rows: a module touches many keys, so keys-as-columns grows unreadably wide
        modules = sorted({r["module"] for r in access})
        print("## Access matrix (R = reads, W = writes)\n")
        print("| Data | " + " | ".join(modules) + " |")
        print("|---|" + "---|" * len(modules))
        for key in sorted({r["key"] for r in access}):
            cells = ["<br>".join(sorted({f"{r['access'][0].upper()} {r['status']}" for r in access
                                         if r["module"] == module and r["key"] == key})) or "-"
                     for module in modules]
            print(f"| `{key}` | " + " | ".join(cells) + " |")
        print()

    # group by key: one key reached through two anchors (interface and client) is still shared
    users, anchors = {}, {}
    for r in rows:
        users.setdefault(r["key"], set()).add(r["module"])
        anchors.setdefault(r["key"], set()).add(r["anchor"])
    print("## Anchor matrix (shared = used by 2 or more modules)\n")
    print("| Anchor | Key | Modules | Shared |\n|---|---|---|---|")
    for key in sorted(users, key=lambda k: (len(users[k]) < 2, sorted(anchors[k]), k)):
        found = users[key]
        print(f"| {', '.join(sorted(anchors[key]))} | `{key}` | {', '.join(sorted(found))} | {'YES' if len(found) > 1 else '-'} |")

    edges = []
    for r in rows:
        if "access" in r:
            source, target = (r["module"], r["key"]) if r["access"] == "write" else (r["key"], r["module"])
            edge = (source, target, f"{r['access']} {r['status']}", r["status"] == "LIVE")
        elif r["type"] == "http" and r["role"] == "provides":
            edge = (r["key"], r["module"], "served by", True)
        elif len(users[r["key"]]) > 1:
            edge = (r["module"], r["key"], f"{r['role']} {r['anchor']}", True)
        else:
            continue
        if edge not in edges:
            edges.append(edge)
    if not edges:
        return
    names = sorted({n for e in edges for n in e[:2]})
    ids = {name: f"n{i}" for i, name in enumerate(names)}
    print("\n## Relation map\n\n```mermaid\nflowchart LR")
    for name in names:
        shape = '[("{}")]' if name.startswith("db:") else ('(["{}"])' if name.startswith("http:") else '["{}"]')
        print(f"  {ids[name]}{shape.format(quote(name))}")
    for source, target, label, solid in edges:
        print(f"  {ids[source]} {'-->' if solid else '-.->'}|{label}| {ids[target]}")
    print("```\n\n```text")
    for source, target, label, solid in sorted(edges):
        print(f"{source} {'──' if solid else '┄┄'}[{label}]──> {target}")
    print("```")


def identity(row):
    file = str(row.get("evidence", "")).rpartition(":")[0]
    return tuple(file if f == "file" else row.get(f) for f in IDENTITY)


def ingest(rows, store, keep_inferred):
    # Graph tools may ignore status, so broken or guessed paths would read as real dependencies.
    held = [r for r in rows if r.get("status") in HELD or (r.get("confidence") == "inferred" and not keep_inferred)]
    rows = [r for r in rows if not any(r is h for h in held)]
    path = Path(store)
    existing = load(path) if path.exists() else []
    index = {identity(r): i for i, r in enumerate(existing)}
    added = updated = same = 0
    for row in rows:
        i = index.get(identity(row))
        if i is None:
            index[identity(row)] = len(existing)
            existing.append(row)
            added += 1
        elif existing[i] != row:
            existing[i] = row
            updated += 1
        else:
            same += 1
    if added or updated:
        tmp = path.with_name(path.name + ".tmp")
        tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in existing), encoding="utf-8")
        tmp.replace(path)
    print(f"added {added}, updated {updated}, unchanged {same}, held back {len(held)} "
          f"(DEAD / NO_ROUTE / UNVERIFIED{'' if keep_inferred else ' / inferred'}) -> {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["check", "render", "ingest"])
    parser.add_argument("rows")
    parser.add_argument("--root", default=".", help="folder that contains the repo folders")
    parser.add_argument("--into", help="relation store to update (ingest)")
    parser.add_argument("--keep-inferred", action="store_true", help="ingest 'inferred' rows too")
    args = parser.parse_args()
    if args.command == "ingest" and not args.into:
        parser.error("ingest needs --into")
    rows = load(args.rows)
    if args.command == "render":
        render(rows)
        return
    check(rows, args.root)
    if args.command == "ingest":
        ingest(rows, args.into, args.keep_inferred)


if __name__ == "__main__":
    main()
