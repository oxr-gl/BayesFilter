# Phase 2 Result: HMC Geometry Initialization Smoke

Date: 2026-07-08

## Status

`PASSED_GEOMETRY_ONLY`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the Phase 1 theta-coordinate mass artifact be consumed by `initialize_hmc_kernel_geometry` without coordinate or SPD failures? |
| Primary criterion | Passed: geometry artifact records finite positive step size, positive leapfrog count, finite target trajectory, `selected_hint=negative_hessian`, no fallback, theta-coordinate covariance source, and no HMC runtime. |
| Veto diagnostics | No vetoes. |
| Explanatory diagnostics | `target_trajectory_length=1.570796326794897`, `initial_step_size=0.22590050090246147`, `initial_num_leapfrog_steps=7`, `L * step_size=1.5813035063172303`. |
| Not concluded | No HMC runtime readiness, tuning success, posterior correctness, convergence, sampler superiority, default readiness, or Zhao-Cui source-faithfulness claim. |

## Artifact

- JSON:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_geometry_cpu_hidden_2026-07-08.json`
- Markdown:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_geometry_cpu_hidden_2026-07-08.md`
- Script:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_quadratic_initializer_geometry_2026_07_08.py`

## Key Diagnostics

| Diagnostic | Value |
| --- | --- |
| Geometry decision | `geometry_initialization_passed=true` |
| Vetoes | `[]` |
| Selected hint | `negative_hessian` |
| Fallback used | `false` |
| Position role | `locator_position_geometry_covariance_only` |
| Covariance source | `low_rank_spd_quadratic_geometry_precision_theta_coordinates` |
| Initial step size | `0.22590050090246147` |
| Initial leapfrog steps | `7` |
| Unclamped leapfrog steps | `7` |
| Target trajectory length | `1.570796326794897` |
| `L * step_size` | `1.5813035063172303` |
| `L * step_size - pi/2` | `0.01050717952233371` |
| `target_trajectory_length - pi/2` | `4.440892098500626e-16` |
| Omega min/median/max | `0.9999999999999788` / `0.9999999999999998` / `1.000000000000004` |
| HMC geometry invoked | `true` |
| HMC runtime invoked | `false` |

## Interpretation

The Phase 1 mass artifact is internally consistent with the Phase 2 geometry
initializer. In the mass-scaled coordinates used by the initializer, curvature
frequencies are essentially one, so the formula target trajectory is `pi/2`.
The product `L * step_size` is slightly above `pi/2` because `L` is computed by
ceiling `target_trajectory_length / step_size`.

This is a geometry-only result. It does not show that HMC will have acceptable
energy behavior, acceptance, divergence status, ESS, posterior correctness, or
runtime feasibility.

## Decision Table

| Decision | Status |
| --- | --- |
| Phase 2 geometry initialization | Passed. |
| Primary criterion status | Satisfied: finite formula outputs and no fallback. |
| Veto diagnostic status | No vetoes. |
| Main uncertainty | Whether a bounded fixed-kernel mechanics smoke has acceptable finite target/acceptance/energy diagnostics. |
| Next justified action | Draft Phase 3 bounded mechanics smoke subplan with strict runtime vetoes. |
| What is not being concluded | HMC readiness, posterior correctness, sampler convergence, default readiness, or source-faithful Zhao-Cui behavior. |

