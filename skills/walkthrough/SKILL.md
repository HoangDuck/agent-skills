---
name: walkthrough
description: Use when the user wants to understand how code works without reading it all - especially a large AI-written change (branch, PR, commit range, uncommitted diff) or an existing feature or module - explained as business flow, implementation flow and usage flow, with the few places worth reading by hand. Vietnamese triggers - "walkthrough", "giải thích luồng", "code này chạy thế nào", "AI vừa viết gì", "nhánh này làm gì", "PR này thay đổi gì", "luồng nghiệp vụ", "flow của tính năng", "đọc hộ code".
argument-hint: "<hỏi bằng lời, ví dụ: nhánh này | PR 12 | luồng checkout | thay đổi chưa commit>"
---

# Walkthrough

Request: $ARGUMENTS

**Explain only what you opened.** Every step you describe points to code you read; anything guessed is marked "suy ra, chưa kiểm". Read-only on source. Reply in the user's language, per [output.md](references/output.md). `<skill>` means this skill's base directory.

The user asks in plain words. Never ask about modes or flags; work them out.

## 1. What to walk through

| The request names | Target | Read |
|---|---|---|
| "nhánh này", a branch, PR, commit or range, "AI vừa viết", "chưa commit" | a **change** | [change.md](references/change.md), [flows.md](references/flows.md) |
| a feature, screen, API, module or file | a **feature** | flows.md |
| nothing | the current branch's change against the default branch; if it has no commits ahead, uncommitted changes; if none, ask what to explain | change.md, flows.md |

Ask only when you cannot tell the target: one plain question listing the candidates. Open with one sentence saying what you will walk through and on which `branch@SHA`.

Words that change depth: "nhanh", "tổng quan" → map and the three flows in short form, no failure walk. "chi tiết" → every flow, every branch of it. "lưu file" → write the report file. Default: complete on the main flows, short on the rest.

## 2. Method

1. **Map** — list the files in scope, grouped by layer (UI, state, API client, handler, service, data, jobs, config, tests). For a change use `bash <skill>/scripts/diffmap.sh <range>`. Collapse generated and lock files to a count.
2. **Entry points** — find what starts each flow: screen, button, route, endpoint, job, webhook, event. A flow without a nameable trigger is reported as "chưa thấy chỗ gọi", not explained as if it runs.
3. **Trace** — follow each entry point to its outcome, opening every file on the path, per flows.md.
4. **Write the three flows** — business, implementation, usage — per flows.md, with diagrams.
5. **Checks** — for a change, the AI-code checklist in change.md. For a feature, the failure walk in flows.md.
6. **Read-by-hand list** — at most 5 places where a human should read the code, each with why (business rule, money or data written, security, concurrency, surprising logic).

## 3. Always

- Follow the chain until it reaches a real trigger. Registered is not used: a route nobody navigates to, a provider nobody reads, an endpoint no client calls is "code exists, not reached".
- Name things as the user sees them in the business and usage flows; identifiers belong in the implementation flow and appendix.
- Long results (more than about one and a half screens, or when asked) go to `docs/walkthrough/<target>-<YYYY-MM-DD>.md`; chat gets the short version and the link.
- Static reading unless you ran something. Say what you ran.
