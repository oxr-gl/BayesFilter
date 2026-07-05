# Phase 0 Subplan: Launch Boundary And Score Meaning Freeze

Date: 2026-07-03

Status: `DRAFT_PENDING_REVIEW`

## Phase Objective

Freeze the launch boundary and the mathematical meaning of `score` before any
implementation or benchmark work starts.

## Entry Conditions Inherited From Previous Phase

This is the first phase.  It inherits:

- current LEDH-inclusive leaderboard closeout says no LEDH score row is
  admitted;
- user direction says score means total derivative, not a stopped partial
  derivative;
- Claude may be used only as a read-only reviewer;
- GPU/CUDA/TensorFlow/XLA commands require trusted or escalated execution.

## Required Artifacts

- This subplan.
- Phase result:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase0-launch-boundary-score-meaning-result-2026-07-03.md`
- Execution ledger:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-visible-execution-ledger-2026-07-03.md`
- Review bundle:
  `docs/reviews/bayesfilter-ledh-leaderboard-score-repair-plan-review-bundle-2026-07-03.md`

## Required Checks, Tests, And Reviews

- Local path check for all master/runbook/subplan artifacts.
- Local text check that the master/runbook distinguish total derivative from
  partial derivative.
- Claude read-only plan review gate after local checks pass.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the runbook ready to launch without ambiguity about score meaning or authority boundaries? |
| Baseline/comparator | Existing LEDH-inclusive leaderboard closeout and July 1 total-VJP repair result. |
| Primary criterion | Phase 0 passes if the artifacts state that score means total derivative and that no LEDH score row is currently admitted. |
| Veto diagnostics | Contract E reused as leaderboard score; partial derivative allowed as score; Claude given execution authority; GPU runs planned without trusted context. |
| Explanatory diagnostics | File inventory, review status, dirty worktree note. |
| Not concluded | No code correctness, no score row admission, no HMC readiness. |

## Forbidden Claims And Actions

- Do not claim any LEDH leaderboard score row is fixed.
- Do not use Contract E as same-target leaderboard score evidence.
- Do not run GPU score benchmarks in Phase 0.
- Do not allow Claude to edit files or launch commands.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- local path/text checks pass;
- Claude plan review returns `VERDICT: AGREE` or a documented human-accepted
  fallback is recorded;
- Phase 0 result records the launch boundary and nonclaims plainly.

## Stop Conditions

Stop if:

- the score meaning cannot be stated without ambiguity;
- Claude review returns a material blocker that is not fixed within five
  rounds;
- local checks show missing required artifacts;
- continuing would require a new human boundary decision.

## Phase-End Duties

At the end of Phase 0:

1. run the required local checks;
2. write the Phase 0 result;
3. draft or refresh the Phase 1 subplan;
4. review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
