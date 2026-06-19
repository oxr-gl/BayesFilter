# P8p Phase 3d Result: Regression FD Reparameterization Diagnostic

Date: 2026-06-19

Status: `DIAGNOSTIC_MIXED_REPARAMETERIZATION_NOT_YET_SUFFICIENT`

## Objective

Keep TF32 enabled and test whether a better parameterization plus 9-point
regression finite differences resolves the P8p Phase 3 gradient-check fragility.

This is diagnostic only.  It does not establish HMC readiness or full-horizon
gradient stability.

## Artifacts

- Subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3d-regression-fd-reparameterization-subplan-2026-06-19.md`
- Script:
  `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
- JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3d-regression-fd-reparameterization-gpu-tf32-2026-06-19.json`

## Checks

Passed:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3d-regression-fd-reparameterization-subplan-2026-06-19.md
```

Trusted GPU command used TF32 enabled, `T=3`, `N=16`, five fixed seeds, and
9-point symmetric regression offsets `[-4,-3,-2,-1,0,1,2,3,4]` with base step
`0.001`.

## Regression FD Summary

Regression model:

```text
f(theta0 + x * direction) = intercept + slope * x
```

The table compares AD directional derivatives with regression slopes.

| Basis | Direction | AD | Regression slope | AD - slope | Residual / slope SE | R2 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| raw | `log_kappa_scale` | `-99.171295` | `-191.133102` | `91.961807` | `6.29` | `0.9607` |
| raw | `log_nu_scale` | `59.660671` | `79.057816` | `-19.397144` | `-2.64` | `0.9430` |
| raw | `log_obs_noise_scale` | `49.012104` | `38.130695` | `10.881409` | `5.62` | `0.9823` |
| physics | `rho=(a-b)/sqrt2` | `-112.311157` | `-182.727158` | `70.416000` | `9.55` | `0.9887` |
| physics | `tau=(a+b)/sqrt2` | `-27.938229` | `-50.917686` | `22.979458` | `1.80` | `0.6937` |
| physics | `omega=c` | `49.012104` | `38.130695` | `10.881409` | `5.62` | `0.9823` |
| whitened | `whitened_0` | `-55.156452` | `-57.894127` | `2.737675` | `0.77` | `0.9741` |
| whitened | `whitened_1` | `26.268478` | `47.871651` | `-21.603172` | `-3.94` | `0.9158` |
| whitened | `whitened_2` | `-109.837433` | `-204.231125` | `94.393692` | `6.73` | `0.9680` |

## Interpretation

The user's diagnosis is partly supported:

- The raw parameterization is highly non-orthogonal.
- A seed-gradient whitened direction can make one diagnostic direction behave
  well under TF32: `whitened_0` has AD/regression residual only `0.77` slope
  standard errors.
- The simple physics transform `rho/tau/omega` is not enough.  It does not
  resolve the main FD/AD mismatch, and the `tau` line has poor local linearity
  (`R2 = 0.6937`).

The result is mixed:

- Regression FD is better evidence than a single central difference.
- Reparameterization helps only when it uses the empirical local covariance
  structure.
- The 9-point window with base step `0.001` is still too broad or too
  TF32-sensitive for several directions.  High R2 does not guarantee the slope
  is local enough for an AD check when the function has numerical roughness.

## Recommended Reparameterization

For diagnostics, use a local linear transform based on seed-gradient geometry:

```text
theta = theta0 + B z
```

where columns of `B` are normalized eigenvector/inverse-square-root directions
of the seed-gradient covariance.  In this run:

```text
whitened_0 = [-0.012159, -0.130261, -0.991405]
whitened_1 = [ 0.248756,  0.959914, -0.129174]
whitened_2 = [ 0.968490, -0.248189,  0.020731]
```

Do not yet adopt this as the model parameterization.  It is a local diagnostic
basis estimated from a tiny `T=3, N=16` target.

For semantic parameterization, keep the physics transform as an interpretable
candidate:

```text
rho   = (log_kappa_scale - log_nu_scale) / sqrt(2)
tau   = (log_kappa_scale + log_nu_scale) / sqrt(2)
omega = log_obs_noise_scale
```

but it needs further orthogonalization against `omega` using local covariance
or observed-information estimates before it is useful for gradient validation.

## Decision Table

| Decision | Primary diagnostic status | Veto status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Do not repair Phase 3 solely with `rho/tau/omega`.  Continue with regression-FD, but use smaller local windows and local covariance/whitened directions. | Mixed.  One whitened direction passed; raw and simple physics directions remain mismatched. | No execution veto fired; several regression lines are not adequate local derivative checks. | Whether smaller regression windows or lower-noise particle counts make all whitened directions agree under TF32. | Run Phase 3e with nested regression windows, e.g. base steps `1e-3`, `5e-4`, `2.5e-4`, and focus on whitened/orthogonalized directions. | No HMC readiness, no full-horizon stability, no global orthogonality, no exact likelihood correctness. |

## Handoff

Next diagnostic should keep TF32 enabled and avoid single-pair FD.  It should
use:

- local covariance/whitened directions;
- nested 7- or 9-point regression windows;
- plateau criteria across window sizes;
- five fixed seeds and per-seed gradient covariance;
- no Phase 4 or HMC claim until the repaired Phase 3 gate passes.
