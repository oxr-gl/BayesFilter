# Phase 7 Target Selection Note: Simple Nonlinear Non-DSGE SSM

Date: 2026-07-07

## Scope

This note launches Phase 7 of the LGSSM-first NeuTra/HMC program.  It selects
the first BayesFilter-owned simple nonlinear non-DSGE SSM target for the
generic adapter gate.

This is a target-adapter gate only.  It is not NeuTra training, HMC sampling,
sampler tuning, posterior convergence validation, production readiness, or a
scientific validity claim.

## Selected Target

Selected model:

- `model_b_nonlinear_accumulation`
- source fixture:
  `bayesfilter.testing.nonlinear_models_tf.make_nonlinear_accumulation_model_tf`
- observations:
  `bayesfilter.testing.nonlinear_models_tf.model_b_observations_tf`

Parameter coordinate:

- `theta = (rho, sigma, beta)`
- identity unconstrained chart for this adapter fixture
- fixed non-estimated constants:
  - `alpha = 0.55`
  - `observation_sigma = 0.30`

Filter/likelihood semantics:

- deterministic SVD-UKF sigma-point approximation
- source:
  `bayesfilter.nonlinear.experimental_batched_svd_sigma_point_tf`
- approximation semantics:
  `deterministic_approximation`
- deterministic target policy:
  `deterministic`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generic target adapter handle a BayesFilter-owned simple nonlinear non-DSGE SSM? |
| Baseline/comparator | Phase 6 LGSSM generic adapter foundation and the existing Model B SVD sigma-point value/score kernel. |
| Primary criterion | A stable `SSMTargetContract` and batch-native posterior adapter emit finite value/score for Model B under the deterministic SVD-UKF approximation. |
| Veto diagnostics | DSGE/c603 dependency, nonfinite values/scores, unstable target or adapter signature, missing target manifest, hidden NeuTra training, hidden HMC, GPU work, or posterior-correctness overclaim. |
| Explanatory diagnostics | Deterministic residual, finite-difference score residual, target signature, adapter signature, and CPU-hidden smoke runtime. |
| Not concluded | Learned NeuTra quality, HMC convergence, posterior correctness, sampler ranking, broad nonlinear SSM validity, production readiness, default-policy change, or scientific validity. |
| Artifact | Phase 7 result and focused tests. |

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Phase 7 does not use DSGE/c603 or LGSSM evidence to claim nonlinear validity; it uses the existing Model B nonlinear fixture. |
| Proxy metric promoted | Finite value/score and finite-difference checks are adapter gates only, not posterior correctness. |
| Missing stop conditions | Stop for nonfinite values/scores, unstable signatures, unclear model/filter semantics, hidden training/HMC/GPU work, or test failure. |
| Hidden assumptions | The identity chart treats `sigma` as an unconstrained innovation loading in this fixture; this is recorded in the transform manifest. |
| Artifact mismatch | Required output is a target-selection note, adapter/test code, and Phase 7 result, not a trained transport or sampler artifact. |

Audit status: passed for Phase 7 target-adapter execution.

## Stop Conditions

Stop if:

- the generic `SSMTargetContract` cannot be materialized without process-local
  identity;
- target or adapter signatures are unstable;
- value or score is nonfinite;
- finite-difference diagnostics fail at the adapter gate;
- implementation requires NeuTra training, HMC sampling, DSGE/c603 import, or
  GPU execution.
