# Flow: impact inside one module

The module-level questions (who reads, who writes, what is shared, what is at risk), asked between **steps** and **flows**.

**Boundary:** the module's own files. A call leaving the module is an `exit: <where>` line. In `flow` mode list it and offer `cross`; in `full` (or scope both) follow it there.

## 1. List the flows

A flow runs from one trigger to its outcomes. Find triggers: routes, buttons, endpoints, webhooks, lifecycle hooks, timers, jobs. List each flow with a one-line trigger and rough step count **before** reading step bodies.

Cover all of them unless the question names one, or the user asked for a quick answer (then cover the flow the question points at and list the rest).

## 2. Steps

| # | Step | Trigger | Code `file:line` | Reads | Writes | Next on success / failure | Status |
|---|---|---|---|---|---|---|---|

State covers controller or component state, params passed between steps, local storage, DB columns, request attributes, timers and flags. Split a step where the user or system can stop, fail or branch. A small flow needs one table; do not pad it.

## 3. Coupling

- **Step → step:** for each piece of state, which step writes it and which later steps read it. Changing a step affects the readers of its writes.
- **Flow → flow:** state, methods, models or rules that several flows touch.
- **Unmatched state:** read but never written here (comes from outside), or written but never read here (used outside, or dead). Find out which.

## 4. Failure walk

For each step, open the code and answer: fails, times out, retried, double-tapped, back or cancel, leave and return, app killed, runs out of order, only partly done. Which state is left behind, and does the next attempt get past it? "No handling found" is a finding; cite where you looked.

## 5. Deliver

Per [output.md](output.md): the body says in plain words which steps and features are affected. The step table, coupling and risks (`Level | Risk | Step | Trigger | Consequence | Evidence or "inferred"`) go in the appendix. When files are written, add step and state rows per [relations.md](relations.md); `render` builds the step coupling matrix and the flow map.
