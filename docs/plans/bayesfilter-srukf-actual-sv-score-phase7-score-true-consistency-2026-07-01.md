# Phase 7 Actual-SV SR-UKF Score-At-True Consistency

Status: PASSED

## Evidence Contract

- Question: is the average analytical SR-UKF score at the true parameter
  compatible with zero across 10 independently simulated datasets?
- Primary criterion: every coordinate mean lies within two standard errors
  of zero, with a tiny-standard-error absolute fallback of `1e-10`.
- Not concluded: exact likelihood correctness, HMC readiness, GPU/XLA
  readiness, or leaderboard admission.
- Warning: the cubature SR-UKF actual-SV route can make the gamma score
  nearly zero structurally; this passes the consistency gate but is weak
  evidence about gamma information in the surrogate.

## Manifest

- Git commit: `ef119f8`
- CPU/GPU status: `CPU-only; CUDA_VISIBLE_DEVICES=-1 set before TensorFlow import by caller`
- Command: `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_actual_sv_srukf_phase7_ladder.py`

## Results

| Case | Param | Mean | SE | z | Pass |
| --- | --- | ---: | ---: | ---: | --- |
| actual_sv_moderate_persistence | theta_gamma | -2.23315e-18 | 2.5587e-18 | -0.872766 | True |
| actual_sv_moderate_persistence | theta_beta | 0.761734 | 1.55086 | 0.491168 | True |
| actual_sv_higher_persistence | theta_gamma | 8.23893e-18 | 8.13905e-18 | 1.01227 | True |
| actual_sv_higher_persistence | theta_beta | 5.09469 | 2.94338 | 1.7309 | True |

## Route Boundary

- Admitted score route: `factor_propagating_srukf_manual_score`.
- Forbidden families remain excluded: `GradientTape`,
  `tf_svd_sigma_point_filter`, historical SVD/eigenderivative
  derivatives, and strict-SPD principal-root derivative helpers.
