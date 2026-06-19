# P8p Phase 3b Result: Per-Seed AD Gradient Noise Diagnostic

Date: 2026-06-18

Status: `DIAGNOSTIC_PASS_PHASE3_STILL_BLOCKED`

## Objective

Estimate the Monte Carlo seed-to-seed variability of the P8p AD gradient on the
same tiny SIR d18 diagnostic target used by Phase 3, using per-seed Jacobian
contributions from the same batched objective route.

This diagnostic does not replace the Phase 3 AD/finite-difference gate and does
not establish HMC readiness.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the Phase 3 AD/finite-difference residuals large relative to per-seed AD gradient Monte Carlo noise on the tiny fixed-randomness SIR d18 target? |
| Comparator | Phase 3 central finite-difference residual table. |
| Primary diagnostic | Per-seed Jacobian contributions, seed sample SD, and standard error of the five-seed batch mean. |
| Veto diagnostics | Nonfinite value/gradient/FD; disconnected gradient component; missing trusted GPU placement; broken theta-zero P8j parity; categorical resampling. |
| Not concluded | Stochastic PF marginal-gradient correctness, exact nonlinear likelihood correctness, Phase 3 pass, full-horizon stability, HMC/NUTS readiness, posterior convergence, or production/default readiness. |

## Code Change

Patched `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py` to report:

- `per_seed_gradient_contributions`, computed as the jacobian of the
  log-likelihood vector with respect to each theta component;
- `monte_carlo_gradient_noise`, with seed mean, seed sample SD, standard error
  of the batch mean, min, max, and batch size.

## Checks

Passed:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
```

Trusted GPU command:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --time-steps 3 \
  --num-particles 16 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P8p Phase 3b MC gradient noise diagnostic" \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --row-chunk-size 16 \
  --col-chunk-size 16 \
  --particle-chunk-size 16 \
  --dtype float32 \
  --tf32-mode enabled \
  --fd-step 0.0005 \
  --repeat-evaluations 1 \
  --check-theta-zero-p8j-parity \
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3b-mc-gradient-noise-2026-06-18.json
```

Artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3b-mc-gradient-noise-2026-06-18.json`

## Result Summary

Route guarantees passed:

- trusted GPU placement;
- finite value, AD gradient, and finite differences;
- all theta components connected;
- theta-zero P8j parity max absolute delta `0.0`;
- fixed random streams and fixed resampling mask;
- relaxed Sinkhorn OT used;
- categorical resampling not used.

Per-seed AD gradient contributions:

| Seed | `log_kappa_scale` | `log_nu_scale` | `log_obs_noise_scale` |
| ---: | ---: | ---: | ---: |
| 81120 | `-349.321899` | `118.568481` | `45.711838` |
| 81121 | `-259.637817` | `110.061600` | `45.402195` |
| 81122 | `-191.306839` | `89.631958` | `44.629162` |
| 81123 | `-373.369598` | `121.412910` | `43.260429` |
| 81124 | `679.848450` | `-141.904922` | `66.058289` |

Monte Carlo gradient noise estimate:

| Parameter | Five-seed mean | Seed sample SD | SE of five-seed mean |
| --- | ---: | ---: | ---: |
| `log_kappa_scale` | `-98.757530` | `441.267883` | `197.341019` |
| `log_nu_scale` | `59.554005` | `113.303391` | `50.670822` |
| `log_obs_noise_scale` | `49.012383` | `9.575850` | `4.282451` |

Same five-seed finite differences:

| Parameter | AD mean | FD | Abs residual | Residual / SE |
| --- | ---: | ---: | ---: | ---: |
| `log_kappa_scale` | `-99.171295` | `-133.346558` | `34.175262` | `0.17` |
| `log_nu_scale` | `59.660671` | `102.615349` | `42.954678` | `0.85` |
| `log_obs_noise_scale` | `49.012104` | `63.171383` | `14.159279` | `3.31` |

## Interpretation

The five-seed diagnostic materially changes the interpretation of Phase 3:

- `log_kappa_scale` is extremely noisy at `T=3, N=16`; an AD/FD residual of the
  Phase 3 size is plausible at this small particle count.
- `log_nu_scale` is also noisy; the five-seed residual is within one estimated
  standard error of the batch mean.
- `log_obs_noise_scale` remains suspicious: its seed-to-seed AD gradient noise is
  much smaller, and even the five-seed residual is about `3.31` estimated
  standard errors.

This does not prove an observation-noise gradient bug, because finite
differences through relaxed OT can still be step-size and precision sensitive.
It does show that a scalar 20 percent FD tolerance is not an adequate diagnostic
by itself for the kappa and nu components at the tiny `N=16` rung.

## Decision Table

| Decision | Primary diagnostic status | Veto status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Keep Phase 3 blocked, but reclassify the failure as partly MC-noise dominated. | Passed; per-seed AD Jacobian noise was measured and preserved route guarantees. | No diagnostic veto fired in Phase 3b. | The observation-noise component still has AD/FD mismatch beyond estimated seed noise; finite-difference step/precision sensitivity remains untested. | Run a focused Phase 3c ladder: FD step sizes and TF32 disabled/float64 where feasible, using five seeds and MC-noise-aware interpretation. | No Phase 3 pass, no HMC readiness, no exact score correctness, no full-horizon gradient stability. |

## Handoff

Do not advance to full-horizon Phase 4 from this result alone.

The next safe subplan should:

- keep the five-seed per-seed Jacobian diagnostic;
- run a finite-difference step ladder, at least `1e-2`, `5e-3`, `1e-3`,
  `5e-4`, `1e-4`;
- compare TF32 enabled versus disabled;
- focus especially on `log_obs_noise_scale`;
- avoid changing scientific target, particle count adequacy claims, or HMC
  readiness claims.
