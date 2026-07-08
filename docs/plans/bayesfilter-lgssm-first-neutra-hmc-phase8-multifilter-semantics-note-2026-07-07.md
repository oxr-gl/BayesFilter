# Phase 8 Semantics Note: Simple Nonlinear Multi-Filter Gate

Date: 2026-07-07

## Scope

This note records the Phase 8 filter-route semantics for the LGSSM-first
NeuTra/HMC program.  It applies only to the BayesFilter-owned simple nonlinear
non-DSGE Model B target fixture introduced in Phase 7.

This is a generic target/filter interface gate.  It is not NeuTra training,
HMC sampling, sampler tuning, posterior convergence validation, production
readiness, or a scientific validity claim.

## Target

- Model: `model_b_nonlinear_accumulation`
- Parameter order: `(rho, sigma, beta)`
- Parameter coordinate: identity unconstrained fixture chart
- Fixed constants:
  - `alpha = 0.55`
  - `observation_sigma = 0.30`
- Generic target boundary:
  `bayesfilter.testing.simple_nonlinear_generic_target_adapter_tf`

## Route Status

| Filter id | Backend | Status | Semantics |
| --- | --- | --- | --- |
| `model-b-svd-ukf-deterministic-loglikelihood` | `tf_svd_ukf` | admitted | Deterministic sigma-point approximation admitted in Phase 7 and preserved as the default route. |
| `model-b-svd-cubature-deterministic-loglikelihood` | `tf_svd_cubature` | admitted | Deterministic sigma-point approximation admitted in Phase 8 through the same generic adapter boundary. |
| `model-b-svd-cut4-deterministic-loglikelihood` | `tf_svd_cut4` | deferred | Deferred until a dedicated generic-adapter finite-difference and branch-diagnostic gate is reviewed. |
| `model-b-principal-sqrt-ukf-deterministic-loglikelihood` | `tf_principal_sqrt_ukf` | deferred | Deferred until principal-square-root/custom-op availability and provenance are gated for this target. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which deterministic nonlinear filter routes can be safely exposed through the generic target adapter boundary for Model B? |
| Baseline/comparator | Phase 7 deterministic SVD-UKF Model B adapter. |
| Primary criterion | Each admitted route has explicit approximation semantics, stable target/adapter metadata, and finite batch-native value/score checks. |
| Veto diagnostics | Hidden training/HMC/GPU work, unstable signatures, nonfinite values/scores, unclear filter semantics, or using one filter's evidence to promote another. |
| Explanatory diagnostics | Deterministic residual, finite-difference score residual, target signature, adapter signature, and CPU-hidden smoke runtime. |
| Not concluded | Learned NeuTra quality, HMC convergence, posterior correctness, sampler superiority, production readiness, default-policy change, or scientific validity. |

## Nonclaims

- No NeuTra training was run.
- No HMC sampling or tuning was run.
- No GPU work was run.
- No filter route is claimed exact for this nonlinear target.
- No admitted route is ranked over another route.
- No posterior correctness, convergence, production readiness, default-policy
  change, or scientific validity is claimed.
