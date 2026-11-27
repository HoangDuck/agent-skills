# Output

Write for someone who knows the product and will maintain this code, but has not read it. Headings in the user's language; drop one that has nothing to say.

1. **Tóm tắt** — two or three sentences: what this does (or what the change does), for whom, and the one thing to watch.
2. **Business flow** — steps in plain words, then the flowchart.
3. **Implementation flow** — hop table with the logic in plain words, diagram if needed, up to 4 code excerpts where the code itself matters, what runs underneath, per flows.md.
4. **Usage flow** — where to find it or how to call it, setup, how to try it by hand.
5. **Cần chú ý** — findings from the AI-code checklist or the failure walk, most serious first: `Mức | Vấn đề | Hậu quả`.
6. **Nên tự đọc** — at most 5 places: `Chỗ | Vì sao`.
7. **Đã đọc / chưa đọc** — range or files, `branch@SHA`, what was opened, what was only listed, what was run.
8. **Phụ lục** — file map from diffmap, `file:line` for every claim, before/after tables.

## Rules

- Target: the chat answer reads in about 5 minutes, far less than reading the code. Put depth into precise sentences and tables, not into more code. When it would run longer, write the full version to the report file and keep the summary, flows, findings and read-by-hand list in chat.
- Code excerpts are copied, never rewritten; trimmed parts are marked with a comment.
- Business and usage flows use names a user sees (screen, button, report), not classes or paths.
- Mermaid diagrams: quote labels with spaces (`A["Tạo đơn"]`), keep each to about 12 nodes; split rather than cram.
- Mark anything not traced to code: "suy ra, chưa kiểm".
- End with at most one recommendation.
