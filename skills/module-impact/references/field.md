# Field: missing, empty, renamed or changed

A value that one module fails to set breaks code far away, often under another name. Finish every step.

1. **Define it:** model and column (or param, config key, enum). Which state matters: null, empty, default, unknown enum value, renamed, retyped, new unit or format.
2. **Writers:** every create and update path — API, forms, admin, imports and sync, jobs, migrations and column defaults, older app builds. Which set it, which do not?
3. **Aliases:** every name it travels under — request attributes set by middleware, serializer `source=` and context, helper params, response keys, JSON tags and `CodingKeys` / `@JsonKey`, tokens, local storage, client model fields, report column labels. Search each alias.
4. **Readers:** search all aliases in every repo in scope. Keep the complete list and count it.
5. **Open each reader** and classify what that state does there:

| Behaviour | Note |
|---|---|
| excluded | the record disappears from results |
| matches only empty | an equality filter on an empty value matches other empty rows (Django `filter(x=None)` is `IS NULL`) |
| error | crash, exception or 4xx / 5xx |
| wrong value | wrong total, date, currency or label without an error |
| fallback | a default replaces it |
| guarded | the code handles it on purpose |
| unaffected | read, but not used in this case |

6. **Impact per role, both directions:** for each role (profile, else the roles in code) say what the affected record's owner can no longer see or do, **and who can no longer see or reach that record**.
7. **Escape paths:** what still works (explicit join, admin override), how to repair existing data, and whether a fix needs a data migration or a client release.

Deliver per [output.md](output.md). Features and roles go in the body in plain words; this table is the appendix:

| Reader `file:line` | API or screen | Behaviour | Affected role | Status |
|---|---|---|---|---|

Under "Checked / not checked": "N readers found, N opened". Unopened readers are `UNVERIFIED`. Whether bad rows exist in real data is unchecked unless you queried it.
