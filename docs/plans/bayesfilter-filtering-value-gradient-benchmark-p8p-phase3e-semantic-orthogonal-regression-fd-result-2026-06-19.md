# P8p Phase 3e Result: Semantic Orthogonal Regression FD

Date: 2026-06-19

Status: `DIAGNOSTIC_MIXED_HIGHER_PARTICLE_RERUN_REQUIRED`

## Objective

Keep TF32 enabled and test whether semantic SIR coordinates, orthogonalized
under the local seed-gradient covariance metric, make nested 9-point
regression finite differences agree with AD on the P8p SIR d18 gradient
diagnostic.

This phase is diagnostic only.  It does not establish HMC readiness,
full-horizon gradient stability, or exact likelihood correctness.

## Artifacts

- Subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3e-semantic-orthogonal-regression-fd-subplan-2026-06-19.md`
- JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3e-semantic-orthogonal-regression-fd-gpu-tf32-2026-06-19.json`
- Script:
  `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `9bcad31f0d9b21731b3915083d86834b43730f51` |
| TensorFlow | `2.19.1` |
| Device | trusted GPU, `/GPU:0` |
| Precision | `float32`, TF32 enabled |
| Target | P8p parameterized SIR d18 diagnostic |
| Horizon / particles | `T=3`, `N=16` |
| Seeds | `81120,81121,81122,81123,81124` |
| Transport | `active-all`, streaming relaxed Sinkhorn OT, `10` iterations, epsilon `1.0` |
| Wall time | `159.738` seconds |

## Direction Construction

The semantic coordinates start from:

```text
rho   = (log_kappa_scale - log_nu_scale) / sqrt(2)
tau   = (log_kappa_scale + log_nu_scale) / sqrt(2)
omega = log_obs_noise_scale
```

Phase 3e then applies Gram-Schmidt under the seed-gradient covariance metric.
The resulting directions in original theta coordinates were:

| Direction | Original-theta vector |
| --- | --- |
| `rho` | `[0.00180385, -0.00180385, 0.0]` |
| `tau_perp_given_rho` | `[0.03382879, 0.13192342, 0.0]` |
| `omega_perp_given_rho_tau` | `[0.00890956, 0.10047209, 0.78660822]` |

The seed-gradient correlations remained very high:

```text
corr(kappa, nu)        = -0.997760
corr(kappa, obs_noise) =  0.985979
corr(nu, obs_noise)    = -0.990533
```

This supports the parameter-collinearity diagnosis.

## Nested Regression FD Summary

Regression model:

```text
f(theta0 + x * direction) = intercept + slope * x
```

| Direction | AD | Slope at `1e-3` | Slope at `5e-4` | Slope at `2.5e-4` | Plateau status |
| --- | ---: | ---: | ---: | ---: | --- |
| `rho` | `-0.286509` | `-0.347264` | `-1.530965` | `-4.436239` | Failed; slopes drift and R2 is near zero |
| `tau_perp_given_rho` | `4.515794` | `7.078425` | `7.655589` | `-0.052389` | Failed; smaller window collapses |
| `omega_perp_given_rho_tau` | `43.663986` | `41.946152` | `31.010942` | `31.890869` | Mixed; large window agrees, smaller windows plateau away from AD |

The `omega_perp` large window is promising, but the full diagnostic did not
converge.  The `rho` direction is especially vulnerable because its AD
directional derivative is very small relative to the objective roughness seen
in the full TF32 route.

## Interpretation

Phase 3e confirms that semantic orthogonalization is a useful discipline, but
it does not by itself close the gradient-validation gate at `N=16`.

The strongest explanation is not a direct observation-covariance gradient bug.
Phase 3c already isolated that path and found the direct covariance derivative
correct.  Phase 3e instead points to a combination of:

- high parameter collinearity;
- too-small directional signal in some metric-normalized directions;
- finite-difference windows that are not scaled to each direction;
- particle/noise roughness at `N=16`;
- TF32 numerical roughness in the full LEDH-PFPF-OT route.

The next diagnostic should therefore increase the particle count and choose
finite-difference windows by directional signal scale, while keeping TF32
enabled.

## Decision Table

| Decision | Primary diagnostic status | Veto status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Do not promote Phase 3e as a passing gradient protocol.  Keep semantic orthogonalization, but rerun with higher `N` and adaptive direction-specific regression windows. | Mixed/failing.  No all-direction slope plateau and AD agreement. | No execution veto fired; diagnostic veto fired for missing plateau and unstable slopes. | Whether `N=16` noise/window scale is the dominant cause, or whether the full TF32 route remains too rough even at higher `N`. | Run Phase 3f with TF32 enabled, `N=64`, semantic-orthogonal directions, and AD-signal-scaled nested regression windows. | No HMC readiness, no full-horizon stability, no exact likelihood correctness, no posterior validity, no production/default readiness. |

## Handoff

Phase 3f should be a focused repaired-gradient diagnostic, not a leaderboard
run.  Its pass condition is stable nested regression-FD slopes agreeing with AD
across the semantic-orthogonal directions on the short fixed-randomness target.
If Phase 3f remains mixed, the next smallest discriminating action is either a
higher-particle rerun (`N=128`) or a narrower investigation of the rough
direction values, not HMC.
