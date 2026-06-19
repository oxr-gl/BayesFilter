# P8p Phase 3c Result: Observation-Noise Gradient Diagnostics

Date: 2026-06-19

Status: `DIAGNOSTIC_PASS_PHASE3_REPAIR_NEEDED`

## Objective

Diagnose whether the suspicious `log_obs_noise_scale` AD/finite-difference
mismatch is caused by:

- a direct observation-covariance gradient bug;
- finite-difference step or TF32 precision sensitivity;
- non-orthogonal or collinear parameter geometry.

## Artifacts

- Subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3c-observation-noise-diagnostic-subplan-2026-06-19.md`
- GPU TF32 JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3c-observation-noise-diagnostic-gpu-tf32-2026-06-19.json`
- GPU TF32-disabled JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3c-observation-noise-diagnostic-gpu-no-tf32-2026-06-19.json`

## Checks

Passed:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3c-observation-noise-diagnostic-subplan-2026-06-19.md
```

Trusted GPU diagnostics passed route guarantees in both runs:

- finite values, AD gradients, and finite differences;
- all theta components connected;
- trusted GPU placement;
- theta-zero P8j parity max absolute delta `0.0`;
- fixed random streams and fixed resampling mask;
- relaxed Sinkhorn OT used;
- categorical resampling not used.

## Isolated Observation-Noise Path

The isolated check evaluates only the Gaussian observation log-density on the
initial particles.  It excludes LEDH flow, target correction, and transport.

| Mode | AD | FD step `1e-2` | FD step `5e-3` | FD step `1e-3` | FD step `5e-4` | FD step `1e-4` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| TF32 enabled | `22.727247` | `22.728920` | `22.726822` | `22.726057` | `22.731779` | `22.754669` |
| TF32 disabled | `22.726557` | `22.728920` | `22.726822` | `22.726057` | `22.731779` | `22.754669` |

Conclusion:

- The direct covariance parameterization
  `R(theta) = R0 * exp(2 * log_obs_noise_scale)` is differentiating correctly
  in the isolated observation likelihood.
- The suspicious Phase 3 mismatch is not explained by a simple factor-of-two,
  sign, log-determinant, or direct Gaussian covariance wiring bug.

## Full LEDH-PFPF-OT Route: Observation Noise FD Ladder

| Mode | AD | MC SE | FD `1e-2` | FD `5e-3` | FD `1e-3` | FD `5e-4` | FD `1e-4` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TF32 enabled | `49.012104` | `4.282451` | `42.485428` | `40.205383` | `40.714260` | `63.171383` | `33.950806` |
| TF32 disabled | `46.826401` | `2.023461` | `45.104980` | `45.111084` | `45.249935` | `45.288082` | `43.754578` |

Residual divided by MC SE:

| Mode | FD `1e-2` | FD `5e-3` | FD `1e-3` | FD `5e-4` | FD `1e-4` |
| --- | ---: | ---: | ---: | ---: | ---: |
| TF32 enabled | `1.52` | `2.06` | `1.94` | `-3.31` | `3.52` |
| TF32 disabled | `0.85` | `0.85` | `0.78` | `0.76` | `1.52` |

Conclusion:

- With TF32 enabled, small-step finite differences are unstable in the full
  LEDH-PFPF-OT route.
- With TF32 disabled, the full-route observation-noise finite-difference ladder
  is stable and agrees with AD within about `0.76` to `1.52` estimated MC
  standard errors.
- The earlier Phase 3 observation-noise failure is best explained by TF32 and
  finite-difference sensitivity in the full route, not by a direct
  observation-noise gradient bug.

## Parameter Geometry

Seed-gradient correlations were very high in both runs:

| Mode | corr(kappa, nu) | corr(kappa, obs-noise) | corr(nu, obs-noise) |
| --- | ---: | ---: | ---: |
| TF32 enabled | `-0.997760` | `0.985979` | `-0.990533` |
| TF32 disabled | `-0.994299` | `0.955142` | `-0.956583` |

Conclusion:

- The tiny `T=3, N=16` diagnostic target has strongly non-orthogonal
  parameter geometry.
- This supports the user's collinearity concern.  It can explain high gradient
  variance and fragile scalar finite-difference tests.
- It does not by itself prove HMC difficulty at full horizon, but it is a
  warning that HMC diagnostics should use mass-matrix/adaptation checks and not
  rely on marginal scalar gradient tests alone.

## Decision Table

| Decision | Primary diagnostic status | Veto status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Reclassify the `log_obs_noise_scale` issue as FD/TF32 sensitivity plus strong parameter geometry, not a direct isolated covariance-gradient bug. | Passed.  Isolated observation-noise AD/FD agrees; TF32-disabled full-route ladder agrees within MC-SE scale. | No route veto fired in Phase 3c. | Full-route float64 CPU/GPU was not run; full-horizon behavior remains untested. | Patch Phase 3 validation protocol: disable TF32 for gradient FD validation, use a step ladder, and interpret residuals against per-seed MC SE. | No Phase 3 pass yet, no full-horizon stability, no HMC/NUTS readiness, no posterior validity, no production/default readiness. |

## Handoff

The next safe action is a Phase 3d repair rerun with a revised predeclared
gradient validation rule:

- trusted GPU;
- `tf32-mode disabled`;
- five fixed seeds;
- FD ladder including `1e-2`, `5e-3`, `1e-3`, `5e-4`, `1e-4`;
- per-seed Jacobian and MC-SE reporting;
- pass/fail rule based on stable FD plateau and residual relative to MC SE,
  rather than a single scalar 20 percent tolerance;
- no HMC or full-horizon claims until that repaired gate is reviewed and passes.
