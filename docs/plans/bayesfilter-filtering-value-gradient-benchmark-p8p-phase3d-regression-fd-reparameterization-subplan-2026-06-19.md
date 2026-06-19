# P8p Phase 3d Subplan: Regression FD Reparameterization Diagnostic

Date: 2026-06-19

Status: `DRAFT_EXECUTABLE`

## Phase Objective

Test whether the remaining Phase 3 gradient-check fragility is caused by
non-orthogonal parameterization and brittle single-pair finite differences.

This phase keeps TF32 enabled and replaces scalar central finite differences
with symmetric 9-point local linear regression finite differences along:

- raw theta directions;
- physics-informed SIR directions:
  - `rho = (log_kappa_scale - log_nu_scale) / sqrt(2)`;
  - `tau = (log_kappa_scale + log_nu_scale) / sqrt(2)`;
  - `omega = log_obs_noise_scale`;
- local seed-gradient whitened directions from the measured seed-gradient
  covariance.

## Entry Conditions

- Phase 3c isolated observation-noise path passed.
- Phase 3c showed strong seed-gradient collinearity.
- User explicitly requested reparameterization and regression-FD diagnostics
  while keeping TF32 enabled.

## Required Artifacts

- Companion script:
  `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
- JSON result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3d-regression-fd-reparameterization-gpu-tf32-2026-06-19.json`
- Result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3d-regression-fd-reparameterization-result-2026-06-19.md`

## Required Checks

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3d-*
```

Trusted GPU diagnostic:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --time-steps 3 \
  --num-particles 16 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P8p Phase 3d regression FD reparameterization GPU TF32" \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --row-chunk-size 16 \
  --col-chunk-size 16 \
  --particle-chunk-size 16 \
  --dtype float32 \
  --tf32-mode enabled \
  --base-step 0.001 \
  --regression-offsets=-4,-3,-2,-1,0,1,2,3,4 \
  --basis-set raw-physics-whitened \
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3d-regression-fd-reparameterization-gpu-tf32-2026-06-19.json
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do AD directional derivatives match 9-point regression-FD slopes better in physics-informed or locally whitened coordinates while keeping TF32 enabled? |
| Baseline/comparator | Phase 3c single-coordinate FD ladder and seed-gradient geometry. |
| Primary diagnostics | AD directional derivative, regression slope, slope standard error, residual / slope SE, regression residual size, and R-squared for each direction. |
| Veto diagnostics | Nonfinite objective/gradient/slope; missing trusted GPU placement; regression fit too curved to interpret; changing target or disabling TF32. |
| Explanatory diagnostics | Seed-gradient covariance/correlation, basis construction, objective values along each line. |
| Not concluded | HMC readiness, global orthogonality, exact likelihood correctness, stochastic PF marginal-gradient correctness, full-horizon stability, or production readiness. |

## Stop Conditions

Stop before Phase 4 if:

- regression FD slopes disagree with AD across all bases;
- regression residuals show high curvature or nonlocality;
- basis construction is numerically unstable;
- interpreting success would require scientific claims beyond this diagnostic.

## Handoff Conditions

If physics or whitened coordinates materially reduce AD/FD residuals with
valid linear fits, the next Phase 3 repair should use regression FD in those
coordinates, not single-pair FD in raw coordinates.
