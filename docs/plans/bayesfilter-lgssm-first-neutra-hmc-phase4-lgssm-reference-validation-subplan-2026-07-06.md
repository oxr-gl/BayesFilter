# BayesFilter LGSSM-First NeuTra/HMC Phase 4 Subplan

Date: 2026-07-06

## Phase Objective

Use LGSSM reference structure to validate the Phase 2 generic adapter target
against deterministic exact-QR and grid references before any longer or
decision-making sampler validation.

## Entry Conditions Inherited From Previous Phase

- Phase 3 tiny smoke completed without runtime/mechanics failure.
- Phase 3 did not claim convergence or posterior correctness.
- Phase 3 review passed or a fixable blocker was visibly repaired.
- Longer or decision-making HMC posterior validation has not been approved.

## Required Artifacts

- Deterministic reference JSON artifact:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-2026-07-06.json`
- Bounded reference log artifact:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-2026-07-06.log`
- Phase 4 result:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-result-2026-07-06.md`
- Phase 4 review bundle.
- Refreshed Phase 5 subplan.

## Required Checks/Tests/Reviews

- CPU-only deterministic target/reference command with `CUDA_VISIBLE_DEVICES=-1`
  before TensorFlow import.
- Evaluate the Phase 2 generic adapter on a fixed two-dimensional grid around
  the initial point.
- Compare adapter log posterior to the source rank-1
  `QRStaticLGSSMTarget.target_log_prob` across the grid.
- Compare adapter score to finite-difference score at selected grid/initial
  points.
- Compute deterministic grid normalization/moments as reference artifacts only.
- Review before transport/NeuTra phases.
- Do not interpret stochastic sampler diagnostics in this phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the Phase 2 generic LGSSM target agree with deterministic source-fixture and grid references under stated tolerances? |
| Baseline/comparator | `QRStaticLGSSMTarget.target_log_prob`, exact QR Kalman value/score checks, and deterministic fixed grid over the two unconstrained coordinates. |
| Primary criterion | Adapter-source value residual and finite-difference score residual stay below predeclared tolerances with all grid values finite. |
| Veto diagnostics | Nonfinite grid value/score, value residual above `1e-9`, finite-difference score residual above `1e-4`, hidden HMC sampling, GPU use, or posterior claims beyond deterministic target validation. |
| Explanatory diagnostics | Grid log normalizer, grid posterior mean/covariance, maximum/minimum log posterior, runtime. |
| Not concluded | HMC convergence, stochastic posterior validation, generic nonlinear SSM validity, NeuTra readiness, production readiness. |
| Artifact | Phase 4 result, logs, and reference manifest. |

## Forbidden Claims/Actions

- Do not rank samplers without uncertainty evidence.
- Do not use training or GPU without approval.
- Do not proceed to NeuTra if the reference gate fails.
- Do not run HMC sampling in Phase 4 without a separately approved amendment.
- Do not treat deterministic grid moments as exact continuous posterior moments.
- Do not use DSGE/c603 material.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if deterministic LGSSM target/reference validation
passes and Phase 5 is refreshed as fixed-transport mechanics handling with
explicit nonclaims. If the reference gate fails, Phase 5 must be refreshed as
blocker handling.

## Stop Conditions

Stop if reference comparator is unclear, if validation fails with no reviewed
repair path, if HMC sampling becomes necessary without approval, or if review
does not converge after five rounds.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 4 result;
3. draft or refresh Phase 5 subplan;
4. review Phase 5 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
