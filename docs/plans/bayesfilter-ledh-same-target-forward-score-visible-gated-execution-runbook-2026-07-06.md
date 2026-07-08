# Visible Gated Execution Runbook: LEDH Same-Target Forward Scalar And Score

Date: 2026-07-06

## Status

`COMPLETE_PHASE6_LEDGER_REBUILT_WITH_TWO_ADMITTED_LEDHD_ROWS`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch detached supervisors, nested agents, copied
workspaces, `nohup`, `setsid`, background phase runners, or interactive Claude
sessions. Execution remains visible and recoverable in the current conversation.

## Quiet Visible Execution Pattern

Large TensorFlow, CUDA, XLA, benchmark, and Claude review commands must use
bounded chat summaries and preserve full logs/artifacts when needed. The chat
gets exit status, artifact paths, pass/fail fields, and bounded failure tails,
not full streaming logs.

## Program

Master program:

- `docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-same-target-forward-score-visible-execution-ledger-2026-07-06.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-same-target-forward-score-visible-stop-handoff-2026-07-06.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Launch and invariant freeze | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase0-launch-invariant-freeze-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase0-launch-invariant-freeze-result-2026-07-06.md` |
| 1 | Row target and theta freeze | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-freeze-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-freeze-result-2026-07-06.md` |
| 2 | Common forward likelihood API | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase2-common-forward-api-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase2-common-forward-api-result-2026-07-06.md` |
| 3 | Model forward scalar admission | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-model-forward-admission-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase3-model-forward-admission-result-2026-07-06.md` |
| 4 | Manual no-tape score implementation | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase4-manual-score-implementation-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase4-manual-score-implementation-result-2026-07-06.md` |
| 5 | Per-model score and memory tests | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase5-per-model-score-tests-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase5-per-model-score-tests-result-2026-07-06.md` |
| 6 | Integration and leaderboard rebuild | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase6-integration-leaderboard-subplan-2026-07-06.md` | `docs/plans/bayesfilter-ledh-same-target-forward-score-phase6-integration-leaderboard-result-2026-07-06.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter produce LEDH scores for all highdim model rows by building the same-target observed-data likelihood estimator first and the no-tape score second? |
| Baseline/comparator | July 3 LEDH-inclusive leaderboard, July 5 score-memory suite, prior row-score admission closeout, and row target contracts. |
| Primary pass criterion | Every promoted row has same-target value admission, no-tape score implementation, tiny correctness, `N=10000` correctness/memory, and all-model integration evidence. |
| Veto diagnostics | Score before scalar; proposal scalar treated as likelihood; scoped row promoted; callback existence promoted; autodiff promoted; memory/runtime success promoted; leaderboard rebuild before row gates. |
| Explanatory diagnostics | Runtime, compile time, memory, old callback traces, and diagnostic finite differences. |
| Not concluded | No HMC readiness, posterior correctness, scientific superiority, or fair runtime ranking unless separately gated. |
| Artifacts | Master program, subplans, ledger, stop handoff, review bundles, phase results, logs, tests, code diffs, and leaderboard artifacts. |

## Skeptical Plan Audit

Before each phase, Codex must check:

- wrong baselines;
- proxy metrics promoted to pass criteria;
- score work before same-target scalar admission;
- proposal or transformed diagnostic scalar mistaken for likelihood;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`: read the subplan, confirm prerequisites, restate the evidence
   contract, and append a ledger entry.
2. `EXECUTE_MINIMAL`: perform only visible actions needed for the phase.
3. `ASSESS_GATE`: compare outputs against primary criterion and veto
   diagnostics.
4. `PASS_REVIEW`: send material phase results or diffs to Claude read-only
   review.
5. `REPAIR_LOOP`: patch fixable blockers, rerun checks, and retry review up to
   five rounds for the same blocker.
6. `ADVANCE_OR_STOP`: continue after passed gates; stop only on explicit stop
   conditions or human-required boundaries.

## Plain-Language Gate

Before accepting any phase result, Codex must verify that the artifact:

- states the claimed target and computed quantity separately;
- labels mismatches as `wrong relative to the stated target`;
- labels unsupported bridges as `unsupported` or `not checked`;
- uses `surrogate` only for proposal mechanisms unless the row target itself
  is a surrogate likelihood;
- states what remains unproved or unevaluated.

## Human-Required Stop Conditions

Stop if continuing would require:

- changing row target definitions after seeing results;
- package installation or data fetch;
- destructive git/filesystem action;
- changing pass/fail criteria after seeing results;
- changing default backend or product policy;
- modifying unrelated dirty user work;
- claiming GPU results without trusted-context evidence;
- continuing after five non-convergent review rounds.

## Final Visible Handoff

On completion or stop, write a result or handoff artifact with:

- current phase and status;
- commands run and checks passed/failed;
- artifacts written;
- admitted rows and blocked rows;
- next action and explicit stop reason if any.
