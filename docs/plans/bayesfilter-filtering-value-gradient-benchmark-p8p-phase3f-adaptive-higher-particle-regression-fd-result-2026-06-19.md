# P8p Phase 3f Result: Adaptive Higher-Particle Regression FD

Date: 2026-06-19

Status: `DIAGNOSTIC_BLOCKED_AD_PATH_LOCALIZATION_REQUIRED`

## Objective

Test whether the Phase 3e failures were mainly caused by low particle count
and poorly scaled finite-difference windows, while keeping TF32 enabled.

Phase 3f used the same short P8p SIR d18 diagnostic target as Phase 3e, raised
the particle count from `N=16` to `N=64`, and chose nested 9-point regression
windows per semantic-orthogonal direction from the AD directional derivative
scale.

## Artifacts

- Subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3f-adaptive-higher-particle-regression-fd-subplan-2026-06-19.md`
- JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3f-adaptive-higher-particle-regression-fd-n64-gpu-tf32-2026-06-19.json`
- Script:
  `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `9bcad31f0d9b21731b3915083d86834b43730f51` |
| TensorFlow | `2.19.1` |
| Device | trusted GPU, `/GPU:0`, RTX 4080 SUPER observed in run log |
| Precision | `float32`, TF32 enabled |
| Target | P8p parameterized SIR d18 diagnostic |
| Horizon / particles | `T=3`, `N=64` |
| Seeds | `81120,81121,81122,81123,81124` |
| Transport | `active-all`, streaming relaxed Sinkhorn OT, `10` iterations, epsilon `1.0` |
| Window policy | AD-signal-scaled nested regression windows |
| Wall time | `212.274` seconds |

## Checks

Passed before the GPU diagnostic:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3e-semantic-orthogonal-regression-fd-result-2026-06-19.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3f-adaptive-higher-particle-regression-fd-subplan-2026-06-19.md
```

Trusted GPU placement passed.  The result JSON records GPU output devices and
`tf32_execution_enabled = true`.

## Result Summary

The higher-particle run fixed the rough finite-difference-line problem.  All
three semantic-orthogonal directions had high R2 and nested slope plateaus:

| Direction | AD | Regression slopes | Adjacent relative slope changes | R2 range |
| --- | ---: | ---: | ---: | ---: |
| `rho` | `-5.644321` | `[-7.594049, -7.611427, -7.663256]` | `[0.0023, 0.0068]` | `0.99967` to `0.99999` |
| `tau_perp_given_rho` | `35.305870` | `[43.475212, 43.664730, 43.880455]` | `[0.0043, 0.0049]` | `0.99966` to `0.99996` |
| `omega_perp_given_rho_tau` | `60.824394` | `[62.685143, 63.020500, 62.555443]` | `[0.0053, 0.0074]` | `0.99968` to `0.99994` |

The finite-difference estimator is now clean enough to be informative.  The
problem is that the stable FD plateau does not equal the AD directional
derivative, especially for `rho` and `tau_perp_given_rho`.

## Interpretation

Phase 3f converts the blocker:

- Phase 3e looked like mixed FD noise plus collinearity.
- Phase 3f shows smooth value lines and stable FD slopes at higher `N`.
- Therefore the remaining discrepancy is not primarily single-pair FD noise,
  not an obvious lack of regression plateau, and not solved merely by increasing
  `N` to `64`.

The next plausible failure class is an AD-path mismatch in the full objective.
The code trace highlights transport as a strong candidate because the streaming
annealed transport path intentionally uses `tf.stop_gradient` in cost scaling
and Sinkhorn-potential initialization:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf`
  centers particles with a stopped mean and divides by a stopped scale;
- streaming Sinkhorn potentials use stopped cost keys and stopped initial
  epsilon scale;
- the active transport path is called after the LEDH flow and corrected weight
  normalization.

This is not yet proof that transport is the blocker.  It is enough to justify a
targeted `active-all` versus `no-resampling` localization diagnostic.

## Decision Table

| Decision | Primary diagnostic status | Veto status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Do not pass Phase 3 yet.  Treat the FD estimator as repaired, but localize the remaining AD/FD mismatch in the full objective. | Failed for AD agreement despite excellent slope plateaus. | No execution veto fired; diagnostic veto fired because plateaued slopes are systematically offset from AD. | Whether the missing derivative is in relaxed OT transport or upstream in LEDH flow/correction. | Run Phase 3g: same `N=64`, TF32, semantic-orthogonal adaptive regression FD, but with `transport-policy no-resampling`. | No HMC readiness, no full-horizon stability, no exact likelihood correctness, no posterior validity, no leaderboard ranking, no production/default readiness. |

## Handoff

Phase 3g should answer only this localization question:

```text
Does the AD/FD discrepancy disappear when relaxed transport is skipped?
```

If yes, the next repair should focus on the streaming annealed-transport AD
contract.  If no, the next repair should localize within LEDH flow, correction
terms, and target log-density callbacks.
