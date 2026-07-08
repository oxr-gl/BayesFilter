# Phase 1 Result: Initializer Artifact Smoke

Date: 2026-07-08

## Status

`PASSED_WITH_LOCAL_NEIGHBORHOOD_REPAIR`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the repaired reusable initializer produce a finite SPD theta-coordinate mass artifact on the minimal scalar SSL-LSTM target? |
| Primary criterion | Passed after repair: JSON artifact records `initializer_artifact_passed=true`, no vetoes, finite positive precision/covariance eigen summaries, and theta-coordinate mass diagnostics. |
| Veto diagnostics | No vetoes in the accepted rerun. Initial attempt rejected with `geometry_holdout_fit_rejected`; repair narrowed the local fit radius and disabled the locator jump. |
| Explanatory diagnostics | Geometry fit accepted with holdout RMSE `0.003825993934031596` below threshold `0.25`; finite sample count `220`, required finite samples `150`; precision condition number `55.004100411471235`. |
| Not concluded | No HMC geometry readiness, HMC runtime readiness, posterior correctness, convergence, sampler superiority, default readiness, or Zhao-Cui source-faithfulness claim. |

## Artifact

- JSON:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_artifact_cpu_hidden_2026-07-08.json`
- Markdown:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_artifact_cpu_hidden_2026-07-08.md`
- Script:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_quadratic_initializer_artifact_2026_07_08.py`

## Key Diagnostics From Accepted Rerun

| Diagnostic | Value |
| --- | --- |
| Accepted/status | `true` / `usable` |
| Locator status | `disabled_initial_position` |
| Map candidate role | `locator_position_geometry_covariance_only` |
| Geometry coordinate system | `z` |
| Mass precision coordinate system | `theta` |
| Mass covariance coordinate system | `theta` |
| Covariance source | `low_rank_spd_quadratic_geometry_precision_theta_coordinates` |
| Precision eigen min/max | `0.06034566533142975` / `3.3192590352870006` |
| Precision condition number | `55.004100411471235` |
| Covariance eigen min/max | `0.3012720578204372` / `16.57119851952585` |
| Geometry holdout passed | `true` |
| HMC geometry invoked | `false` |
| HMC runtime invoked | `false` |
| CPU-hidden status | `true` |

## Repair Loop Note

The first Phase 1 run used the Phase 5-era wider geometry settings and an
enabled locator. It rejected with `geometry_holdout_fit_rejected`. The
diagnostics showed that a `scale=5.0` transform with trust radius `1.0` sampled
a large nonlinear neighborhood, and the locator moved to a high-curvature point
with large score norm.

The repair kept the same pass/fail contract but changed the artifact-builder
defaults to:

- `locator_enabled=false`;
- `low_rank_trust_radius=0.05`;
- `low_rank_pilot_radius=0.02`.

This repair narrows the diagnostic to a local mass artifact around the minimal
fixture center. It does not certify the center as a global MAP or certify HMC
performance.

## Decision Table

| Decision | Status |
| --- | --- |
| Phase 1 initializer artifact | Passed after repair. |
| Primary criterion status | Satisfied: finite SPD theta-coordinate mass artifact exists. |
| Veto diagnostic status | No accepted-rerun vetoes. |
| Main uncertainty | Whether HMC geometry initialization with this mass produces formula-derived `epsilon`/`L` diagnostics that are internally coherent. |
| Next justified action | Draft and execute Phase 2 HMC geometry-initialization-only subplan. |
| What is not being concluded | HMC readiness, posterior correctness, sampler convergence, default readiness, or source-faithful Zhao-Cui behavior. |

