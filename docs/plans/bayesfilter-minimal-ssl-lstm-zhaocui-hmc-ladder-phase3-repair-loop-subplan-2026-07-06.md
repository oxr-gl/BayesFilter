# Phase 3 Subplan: Repair Loop And Retest Gate

Date: 2026-07-06

Status: `DRAFT_PENDING_PHASE2_RESULT`

## Phase Objective

Classify any Phase 2 canary hard veto and apply the smallest focused repair
within the scalar HMC mechanics scope, or record that no repair is needed.

## Entry Conditions Inherited From Previous Phase

- Phase 2 result exists and classifies the CPU-hidden canary outcome.
- Any failure is already labeled as implementation, initialization, tuning,
  numerical, artifact, or boundary failure.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase3-repair-loop-result-2026-07-06.md`
- If a repair is applied, updated harness/test/artifact/log paths from Phases 1
  or 2.
- Draft/refreshed Phase 4 subplan.

## Required Checks, Tests, And Reviews

- If no repair is needed: verify Phase 2 pass evidence and write a no-op
  repair result.
- If repair is needed: patch visibly, rerun focused failing checks, rerun
  canary only if required by the repair.
- `git diff --check`.
- Review repair result/Phase 4 subplan if external review is available; else
  local Codex substitute review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does Phase 2 require a focused repair before any short replicated debug ladder? |
| Baseline/comparator | Phase 2 hard-veto classification. |
| Primary pass criterion | Either no repair is required, or a focused repair is applied and the failed hard-veto check is rerun successfully. |
| Veto diagnostics | Unclassified failure, pass/fail criterion change after seeing results, broad semantic change, public API/model/default-policy change, or unsupported claim. |
| Explanatory diagnostics | Repair class, commands rerun, before/after hard-veto status, and residual uncertainty. |
| Not concluded | HMC convergence, posterior correctness, ranking, GPU/XLA readiness, default readiness, source-faithful parity, or LEDH result. |

## Forbidden Claims And Actions

- Do not treat a tuning failure as evidence against the scientific idea unless
  the plan explicitly says so.
- Do not silently broaden repair scope.
- Do not change criteria after seeing results.
- Do not run long/GPU/detached work without approval.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only when:

- Phase 3 result exists;
- any Phase 2 hard veto is either repaired, classified as non-fixable within
  scope, or explicitly absent;
- Phase 4 short replicated ladder subplan exists and states its evidence class.

## Stop Conditions

Stop if failure cannot be classified, if repair requires scope expansion, if
review does not converge after five rounds for the same blocker, or if broader
runtime approval is required and not granted.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write Phase 3 result/close record.
3. Draft or refresh Phase 4 subplan.
4. Review Phase 4 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
