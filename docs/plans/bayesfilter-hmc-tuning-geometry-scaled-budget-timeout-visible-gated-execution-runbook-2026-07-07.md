# BayesFilter HMC Tuning Geometry-Scaled Budget And Timeout Visible Runbook

Date: 2026-07-07

Status: `DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is supervisor and executor.

Claude is read-only reviewer only.

This runbook is visible and recoverable in the current conversation.  It must
not launch detached supervisors, `codex exec`, `overnight_gated_launch.sh`,
`setsid`, `nohup`, background phase runners, or copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-master-program-2026-07-07.md`

Execution ledger:

- `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-visible-execution-ledger-2026-07-07.md`

Stop handoff:

- `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-visible-stop-handoff-2026-07-07.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, Inventory, And Baseline Lock | `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-p00-inventory-subplan-2026-07-07.md` | `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-p00-inventory-result-2026-07-07.md` |
| 1 | Central Policy Design | To be drafted after Phase 0 | Phase 1 result |
| 2 | BayesFilter Implementation | To be drafted after Phase 1 | Phase 2 result |
| 3 | CCMA Integration | To be drafted after Phase 2 | Phase 3 result |
| 4 | Test And Audit Gate | To be drafted after Phase 3 | Phase 4 result |
| 5 | LaTeX Documentation And Closeout | To be drafted after Phase 4 | Phase 5 result/reset memo |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the active BayesFilter/CCMA HMC tuning path be repaired so sample and timeout behavior is centrally derived from model geometry, stage role, observed throughput, and meaningful progress? |
| Baseline/comparator | Current active BayesFilter tuner and CCMA launcher/supervisor before this program's edits. |
| Primary pass criterion | One promoted BayesFilter policy controls HMC tuning samples, attempts, progress/stall behavior, and emergency cap; CCMA uses it by default; active defaults contain no unexplained magic timeout/sample constants. |
| Veto diagnostics | NUTS introduced; MacroFinance-local HMC mechanics introduced; public artifact leaks private mechanics; progress-aware watcher still kills slow-but-progressing tuning; no-progress tuning lacks diagnostic closeout; tests fail. |
| Explanatory diagnostics | Dimension, condition number, effective dimension, regularization pressure, chosen sample counts, timing rationale, emergency cap, and review status. |
| Not concluded | No posterior convergence, sampler superiority, empirical validity, scientific validity, GPU readiness, or production readiness. |
| Artifacts | Phase docs, review bundles, code/test diffs, logs, LaTeX doc update, result note, reset memo. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Fixed-trajectory HMC, not NUTS | User directive and BayesFilter chapters | TFP NUTS is not viable/default for CCMA TensorFlow path | NUTS sneaks back as repair | `rg NUTS NoUTurn nuts` in active files | Baseline |
| BayesFilter owns tuning | MacroFinance AGENTS and user directive | Generic HMC policy belongs in BayesFilter | MacroFinance duplicates tuner | import/wrapper audit | Baseline |
| Sample budget derived from geometry | User directive | Counts should reflect dimension and geometry | arbitrary small samples support false decisions | policy tests with low/high dimension and condition number | Hypothesis |
| Timing derived from progress and throughput | User directive | Slow progress should continue; no progress should stop | hard timeout kills useful run or infinite hang | watcher/policy tests | Hypothesis |
| Emergency cap remains | Safety requirement | Machine protection, not tuning evidence | cap becomes hidden tuning failure criterion | startup payload explains cap role | Reviewed default |

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands in this conversation; preserve
   unrelated dirty work.
3. `ASSESS_GATE`: compare output to criterion and vetoes; write phase result.
4. `PASS_REVIEW`: send material result/subplan/diff to Claude read-only review
   when available, or record Codex substitute review.
5. `REPAIR_LOOP`: patch fixable problems visibly; rerun focused checks; stop
   after five review rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after gate passes.

## Quiet Execution Pattern

Long commands must predeclare log paths, preserve full logs as artifacts, and
print only bounded summaries in chat.  Do not stream large TensorFlow/test
output into the session.

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch,
credentials, destructive git/filesystem action, changing pass/fail criteria
after seeing results, modifying unrelated dirty work, or changing scientific
claims/default boundaries beyond this reviewed program.
