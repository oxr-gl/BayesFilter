# P8p Phase 3g Result: No-Resampling AD/FD Localization

Date: 2026-06-19

Status: `LOCALIZED_PRIMARY_MISMATCH_TO_ACTIVE_TRANSPORT`

## Objective

Rerun the repaired Phase 3f regression-FD diagnostic with relaxed transport
skipped.  The goal was to localize whether the Phase 3f AD/FD discrepancy was
introduced by active streaming annealed transport or already present upstream
in LEDH flow, correction terms, or target log-density callbacks.

## Artifacts

- Subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3g-no-resampling-localization-subplan-2026-06-19.md`
- JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3g-no-resampling-localization-n64-gpu-tf32-2026-06-19.json`
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
| Transport policy | `no-resampling` |
| Window policy | AD-signal-scaled nested regression windows |
| Wall time | `97.768` seconds |

## Checks

Passed before the GPU diagnostic:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3f-adaptive-higher-particle-regression-fd-result-2026-06-19.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3g-no-resampling-localization-subplan-2026-06-19.md
```

Trusted GPU placement passed.  The JSON records GPU output devices and
`tf32_execution_enabled = true`.

## Result Summary

With transport skipped, the large Phase 3f AD/FD mismatch mostly disappears.

| Direction | AD | Regression slopes | AD - slope range | Residual / slope SE | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| `rho` | `-19.804478` | `[-19.803806, -19.800312, -19.804747]` | `-0.004166` to `0.000269` | `-0.50` to `0.03` | Pass |
| `tau_perp_given_rho` | `-8.857559` | `[-8.813468, -8.839838, -8.843623]` | `-0.044091` to `-0.013936` | `-0.13` to `-0.08` | Pass |
| `omega_perp_given_rho_tau` | `-102.297981` | `[-101.485245, -101.543678]` | `-0.812737` to `-0.754303` | `-16.09` to `-9.90` | Small sharp mismatch |

The slope plateaus are excellent in all directions.  `rho` and `tau_perp`
agree with AD under the repaired protocol.  `omega_perp` still has a small
absolute mismatch, but it is much smaller than the active-transport mismatches
from Phase 3f.

## Comparison To Phase 3f

Phase 3f active-all transport produced plateaued FD slopes far from AD:

| Direction | Phase 3f AD | Phase 3f plateau slopes | Phase 3g no-resampling status |
| --- | ---: | ---: | --- |
| `rho` | `-5.644321` | about `-7.6` | AD/FD agrees after skipping transport |
| `tau_perp_given_rho` | `35.305870` | about `43.7` | AD/FD agrees after skipping transport |
| `omega_perp_given_rho_tau` | `60.824394` | about `62.8` | remaining small mismatch, much reduced |

This localizes the primary mismatch to the active relaxed transport path rather
than the generic regression-FD estimator, raw semantic basis, or the upstream
no-resampling LEDH/correction route.

## Interpretation

The active streaming annealed transport path is now the main repair surface for
the P8p gradient gate.

The code trace is consistent with this result.  The streaming annealed
transport implementation uses stopped centering/scale and stopped Sinkhorn
potential keys.  Those choices are defensible for numerical stabilization, but
they mean the value computed by the forward route and the derivative exposed by
TensorFlow can differ from a full finite-difference derivative of the same
forward value.

The small no-resampling `omega_perp` mismatch should not be ignored, but it is
not the dominant blocker.  It may reflect remaining observation-noise/flow
curvature, TF32 rounding, or a local metric-basis artifact.  It is small enough
to handle after the transport AD contract is made explicit.

## Decision Table

| Decision | Primary diagnostic status | Veto status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Treat active streaming annealed transport as the primary Phase 3 AD/FD repair surface. | Localization passed: skipping transport removes the large mismatches in two directions and sharply reduces the third. | Phase 3 still not passed because active-all transport remains mismatched and no-resampling is not the intended DPF route. | Whether dense transport shows the same mismatch, and which stopped/scaled part of the streaming transport AD contract accounts for it. | Run a transport AD-contract repair phase: dense-vs-streaming comparison, stop-gradient ablation, and a documented custom-gradient/default policy decision. | No HMC readiness, no full-horizon stability, no exact likelihood correctness, no posterior validity, no leaderboard ranking, no production/default readiness. |

## Handoff

The next phase should not tune particles or FD windows further until the
transport AD contract is resolved.  Recommended next steps:

1. Add a plan for transport AD contract repair.
2. Compare active-all dense transport versus active-all streaming transport at
   the same `T=3`, `N=64`, TF32, semantic-orthogonal adaptive FD settings.
3. Add an opt-in diagnostic ablation for stopped centering/scale and stopped
   Sinkhorn keys in the transport core.
4. Decide whether the default gradient should be a full forward-value gradient,
   a deliberate stabilized surrogate gradient, or a custom-gradient contract.
5. Rerun the active-all Phase 3 gradient gate only after that decision is
   implemented and documented.

Until then, the DPF/SIR d18 gradient lane remains blocked before HMC.
