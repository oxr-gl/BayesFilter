# Phase 0 Subplan: Launch And Invariant Freeze

metadata_date: 2026-07-06
status: DRAFT
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 0

## Phase Objective

Freeze the corrected construction runbook: same-target observed-data
log-likelihood scalar first, no-tape score second, leaderboard rebuild last.

## Entry Conditions Inherited From Previous Phase

- The prior row-score admission runbook closed as blocker triage.
- The user approved replacing the inventory-first plan with a construction
  plan.
- Claude review and GPU/XLA trusted runs are approved within bounded repo
  scope.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md`
- Visible runbook:
  `docs/plans/bayesfilter-ledh-same-target-forward-score-visible-gated-execution-runbook-2026-07-06.md`
- Execution ledger:
  `docs/plans/bayesfilter-ledh-same-target-forward-score-visible-execution-ledger-2026-07-06.md`
- Stop handoff:
  `docs/plans/bayesfilter-ledh-same-target-forward-score-visible-stop-handoff-2026-07-06.md`
- Launch review bundle:
  `docs/reviews/ledh-same-target-forward-score-launch-review-bundle-2026-07-06.md`
- Phase 0 result:
  `docs/plans/bayesfilter-ledh-same-target-forward-score-phase0-launch-invariant-freeze-result-2026-07-06.md`

## Required Checks/Tests/Reviews

- `git diff --check` on the new planning and review artifacts.
- Focused `rg` checks that the master/runbook/subplans contain:
  - `log p_theta(y_1:T)`;
  - `No LEDH score work may begin`;
  - `wrong relative to the stated target`;
  - `proposal`;
  - `leaderboard rebuild last`.
- Claude read-only launch review of the master, runbook, Phase 0/1 subplans,
  and review bundle.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the new program force same-target likelihood scalar construction before score work? |
| Baseline/comparator | Prior row-score admission closeout, July 5 score-memory result, and corrected user instruction. |
| Primary criterion | The launch artifacts make same-target forward likelihood admission a hard prerequisite for every row score. |
| Veto diagnostics | Another inventory-only plan; score before scalar; proposal scalar treated as likelihood; unsupported row promotion. |
| Explanatory diagnostics | Existing blocker artifacts and prior review logs. |
| Not concluded | No code repair, row admission, score correctness, HMC readiness, or leaderboard promotion. |

## Forbidden Claims/Actions

- Do not edit algorithm code in Phase 0.
- Do not run GPU/XLA benchmarks in Phase 0.
- Do not claim any new row is admitted.
- Do not ask Claude to approve execution boundaries.

## Allowed Operations

- Edit planning, review, and ledger artifacts.
- Run local text/diff checks.
- Run bounded Claude read-only review.
- Use fresh Codex review only if Claude is unavailable or policy-blocked.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- local checks pass;
- read-only review returns `VERDICT: AGREE` or an explicitly recorded fallback
  review agrees;
- Phase 0 result states that Phase 1 must freeze row targets and theta before
  any implementation.

## Stop Conditions

Stop if the launch artifacts do not enforce same-target likelihood first, if
Claude/Codex review finds a non-fixable plan flaw, or if continuing would
require changing row definitions without human direction.
