# BayesFilter LGSSM-First NeuTra/HMC Phase 2 Subplan

Date: 2026-07-06

## Phase Objective

Materialize a reviewed LGSSM target adapter using BayesFilter's generic
`SSMTargetContract` and batch-native value/score adapter surfaces. The target is
the deterministic static QR LGSSM fixture already used for CPU HMC-readiness
smoke tests, recast as a generic BayesFilter SSM posterior target.

## Entry Conditions Inherited From Previous Phase

- Phase 1 inventory has identified the exact implementation boundary:
  construct a generic LGSSM adapter and focused tests only.
- DSGE/c603 remains deferred.
- No HMC/GPU/training/package/git boundary has been crossed.
- Phase 1 review has passed or recorded a repaired fixable blocker.

## Required Artifacts

- Focused code/test changes implementing the smallest LGSSM generic adapter
  boundary. Preferred initial shape:
  - a test/support helper for a static QR LGSSM `SSMTargetContract`;
  - rank-2 Gaussian prior value/score;
  - rank-2 QR Kalman likelihood value/score;
  - a `GenericSSMPosteriorAdapter` construction helper.
- Focused tests, likely in a new test module such as
  `tests/test_lgssm_generic_target_adapter_tf.py` unless local patterns suggest
  a better name.
- Phase 2 result:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase2-lgssm-target-adapter-result-2026-07-06.md`
- Phase 2 review bundle if code or public target semantics change.
- Refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase3-plain-hmc-smoke-subplan-2026-07-06.md`

## Required Checks/Tests/Reviews

- CPU-only focused tests with `CUDA_VISIBLE_DEVICES=-1` before TensorFlow
  import.
- Checks for:
  - stable target signature and adapter signature;
  - stable manifest fields without process-local identity;
  - finite rank-2 `[B]` value and `[B, D]` score;
  - batch-of-one accepted and rank-1 rejected;
  - direct posterior equals prior plus QR Kalman likelihood;
  - likelihood or posterior score agrees with finite-difference and/or existing
    analytic QR diagnostic at the initial point.
- Review if code or public target semantics change.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter expose a real exact LGSSM posterior target through the generic batch-native SSM adapter? |
| Baseline/comparator | Phase 1 inventory, `QRStaticLGSSMTarget`, exact QR Kalman likelihood code, and existing QR derivative diagnostics. |
| Primary criterion | Adapter emits finite rank-2 posterior value/score, stable target signature, and focused gradient/reference checks pass. |
| Veto diagnostics | Process-local signature, shape ambiguity, nonfinite value/score, gradient/reference mismatch, hidden HMC/training/GPU, or DSGE dependency. |
| Explanatory diagnostics | Target signature, adapter signature, finite probes, gradient residuals. |
| Not concluded | HMC convergence, posterior validation, NeuTra readiness, production readiness. |
| Artifact | Phase 2 result and tests/logs. |

## Forbidden Claims/Actions

- Do not run HMC or NeuTra training.
- Do not use GPU.
- Do not claim posterior convergence or production readiness.
- Do not use DSGE/c603 material.
- Do not add package dependencies or mutate the environment.
- Do not change BayesFilter default backend or public product policy.
- Do not promote finite value/score or finite-difference agreement into HMC
  readiness.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if Phase 2 target adapter passes focused checks and
records nonclaims. The Phase 3 subplan must then be refreshed so plain HMC
smoke uses this generic adapter rather than the older rank-1 fixture directly.
Otherwise Phase 3 must be refreshed as blocker handling.

## Stop Conditions

Stop if finite value/score or target-signature checks fail, if exact QR Kalman
reference cannot be tied to the adapter, or if review does not converge after
five rounds.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 2 result;
3. draft or refresh Phase 3 subplan;
4. review Phase 3 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
