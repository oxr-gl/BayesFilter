# Claude Read-Only Review Bundle

Date: 2026-07-06
Review name: `ledh-same-target-forward-score-launch`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run commands, launch agents, approve boundary
crossings, or act as execution authority.

## Objective

Review the launch artifacts for the LEDH same-target forward scalar and score
construction program. Decide whether the plan fixes the prior planning error by
requiring same-target observed-data likelihood scalar admission before score
work.

## Artifacts To Inspect

- `docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-visible-gated-execution-runbook-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase0-launch-invariant-freeze-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-freeze-subplan-2026-07-06.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the launch artifacts force `log p_theta(y_1:T)` or its finite-`N` LEDH likelihood estimator to be built and admitted before any row score work? |
| Baseline/comparator | Prior row-score admission closeout, July 5 score-memory suite, and corrected user instruction. |
| Primary criterion | The plan must be construction-oriented, not another inventory-only run, and must sequence target/theta freeze, forward likelihood API, model forward admission, score implementation, tests, then leaderboard rebuild. |
| Veto diagnostics | Score before scalar; proposal or diagnostic scalar treated as likelihood; scoped SIR promoted; callback existence promoted; autodiff promoted; leaderboard rebuild before row gates; hidden authority transfer. |
| Explanatory diagnostics | Existing blocker artifacts and previous LEDH runbooks. |
| Not concluded | This review does not admit a row, approve code, or authorize scientific claims. |

## Review Questions

1. Does the master program make same-target likelihood scalar construction the
   first repair target?
2. Are the phase order and stop conditions sufficient to prevent another
   inventory-only closeout?
3. Does Phase 1 correctly force row target and theta freeze before code edits?
4. Are there unsupported claims, hidden assumptions, or boundary mistakes?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
