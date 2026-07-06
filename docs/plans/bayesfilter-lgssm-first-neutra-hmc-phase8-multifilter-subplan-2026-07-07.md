# Phase 8 Subplan: Multi-Filter Nonlinear Target Gate

Date: 2026-07-07

## Phase Objective

Extend the LGSSM-first NeuTra/HMC program from one simple nonlinear non-DSGE
target adapter to a reviewed multi-filter target gate.

This phase is a target/filter semantics phase. It must not run NeuTra training,
HMC sampling, sampler tuning, or GPU jobs without a new reviewed execution
subplan.

## Entry Conditions Inherited From Previous Phase

- Phase 7 selected `model_b_nonlinear_accumulation` as the first simple
  nonlinear non-DSGE target.
- Phase 7 produced a stable `SSMTargetContract` and generic posterior adapter.
- Phase 7 local checks passed:
  - `tests/test_simple_nonlinear_generic_target_adapter_tf.py`: `8 passed`;
  - `tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py`:
    `9 passed`;
  - py_compile passed.
- Phase 7 made no NeuTra training, HMC, posterior correctness, production, or
  scientific validity claim.
- Serious future NeuTra training remains GPU-only by owner directive; external
  sample generation remains multicore CPU by policy.

## Required Artifacts

- Phase 8 result:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase8-multifilter-result-2026-07-07.md`
- Multi-filter target semantics note naming the admissible filters and their
  approximation semantics.
- Focused tests showing each admitted filter produces finite value/score or is
  explicitly blocked with a reason.
- Refreshed next-phase subplan.

## Required Checks/Tests/Reviews

- Re-run Phase 7 target-adapter tests.
- Add or run focused multi-filter tests for any newly admitted filter route.
- Run `git diff --check` on Phase 8 code/docs.
- Review the Phase 8 result and next subplan before crossing into training,
  HMC, GPU, or sample-generation work.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which deterministic nonlinear filter routes can be safely exposed through the generic target adapter boundary for Model B or another simple non-DSGE fixture? |
| Baseline/comparator | Phase 7 deterministic SVD-UKF Model B adapter. |
| Primary criterion | Each admitted route has explicit approximation semantics, stable target/adapter metadata, and finite batch-native value/score checks. |
| Veto diagnostics | Hidden training/HMC/GPU work, unstable signatures, nonfinite values/scores, unclear filter semantics, or using one filter's evidence to promote another. |
| Explanatory diagnostics | Runtime, branch diagnostics, finite-difference residuals, deterministic residuals, and route-specific warnings. |
| Not concluded | Learned NeuTra quality, HMC convergence, posterior correctness, sampler superiority, production readiness, default-policy change, or scientific validity. |
| Artifact | Phase 8 result, tests, and next subplan. |

## Forbidden Claims/Actions

- Do not run NeuTra training in this phase.
- Do not run HMC sampling or sampler tuning in this phase.
- Do not use DSGE/c603.
- Do not claim exactness for deterministic sigma-point approximations.
- Do not treat finite value/score as posterior correctness.
- Do not run GPU work without a new reviewed GPU execution subplan.

## Exact Next-Phase Handoff Conditions

The next phase may begin only if:

- Phase 8 records which filter routes are admitted, blocked, or deferred;
- every admitted route has finite value/score checks;
- blocked routes have explicit blockers rather than silent omission;
- review agrees the next subplan preserves training/HMC/GPU boundaries.

## Stop Conditions

Stop if:

- any route has unclear target/filter semantics;
- any admitted route emits nonfinite values or scores;
- a route requires training, HMC, GPU execution, or sample generation;
- review does not converge after five rounds.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 8 result;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
