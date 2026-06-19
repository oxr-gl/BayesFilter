# P8p Phase 3e Subplan: Semantic Orthogonal Nested Regression FD

Date: 2026-06-19

Status: `DRAFT_EXECUTABLE`

## Phase Objective

Keep TF32 enabled and test a more disciplined parameterization for gradient
validation:

1. start from semantic SIR coordinates;
2. orthogonalize them under the local seed-gradient covariance metric;
3. use nested 9-point regression finite differences to check slope plateaus.

This phase is a diagnostic repair candidate for Phase 3 only.  It does not
authorize HMC or full-horizon claims.

## Parameter Coordinates

Let:

```text
a = log_kappa_scale
b = log_nu_scale
c = log_obs_noise_scale
```

Start with:

```text
rho   = (a - b) / sqrt(2)
tau   = (a + b) / sqrt(2)
omega = c
```

Then apply Gram-Schmidt to the coordinate directions under the local
seed-gradient covariance metric:

```text
rho
tau_perp   = tau residualized against rho
omega_perp = omega residualized against rho and tau_perp
```

## Required Artifacts

- Script:
  `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`
- JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3e-semantic-orthogonal-regression-fd-gpu-tf32-2026-06-19.json`
- Result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3e-semantic-orthogonal-regression-fd-result-2026-06-19.md`

## Required Checks

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3e-*
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
  --phase-label "P8p Phase 3e semantic orthogonal regression FD GPU TF32" \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --row-chunk-size 16 \
  --col-chunk-size 16 \
  --particle-chunk-size 16 \
  --dtype float32 \
  --tf32-mode enabled \
  --base-step 0.001 \
  --base-step-ladder 0.001,0.0005,0.00025 \
  --regression-offsets=-4,-3,-2,-1,0,1,2,3,4 \
  --basis-set semantic-orthogonal \
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3e-semantic-orthogonal-regression-fd-gpu-tf32-2026-06-19.json
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do semantically meaningful, locally orthogonal directions produce stable nested regression-FD slopes that agree with AD under TF32? |
| Baseline/comparator | Phase 3d raw, physics, and whitened regression-FD diagnostics. |
| Primary diagnostics | AD directional derivative; regression slope for base steps `1e-3`, `5e-4`, `2.5e-4`; adjacent slope plateau; regression R2 and max residual. |
| Veto diagnostics | Nonfinite value/gradient/slope; missing GPU placement; regression line too nonlinear; no slope plateau; target or TF32 disabled. |
| Explanatory diagnostics | Direction vectors in original theta coordinates, seed-gradient covariance, per-seed gradient noise. |
| Not concluded | HMC readiness, full-horizon gradient stability, global orthogonality, exact likelihood correctness, production/default readiness. |

## Handoff Conditions

If all semantic-orthogonal directions show slope plateaus and AD agreement
within the regression uncertainty scale, use this protocol as the candidate
Phase 3 repair.  Otherwise, continue with smaller windows or higher particle
counts before any HMC work.
