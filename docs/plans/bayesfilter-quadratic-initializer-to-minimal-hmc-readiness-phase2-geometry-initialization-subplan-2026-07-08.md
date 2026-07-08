# Phase 2 Subplan: HMC Geometry Initialization Smoke

Date: 2026-07-08

## Status

`DRAFT_SUBPLAN`

## Phase Objective

Feed the Phase 1 theta-coordinate quadratic initializer artifact into
`initialize_hmc_kernel_geometry` and write a structured geometry-only artifact
with formula-derived step size, leapfrog count, target trajectory, and
`L * step_size` diagnostics.

This phase must not run HMC or tune an HMC kernel.

## Entry Conditions

- Phase 0 coordinate audit passed with the theta-coordinate mass rule recorded.
- Phase 1 accepted artifact exists:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_artifact_cpu_hidden_2026-07-08.json`
- Phase 1 decision has `initializer_artifact_passed=true` and empty vetoes.
- Phase 1 artifact records:
  - `mass_precision_coordinate_system=theta`;
  - `mass_covariance_coordinate_system=theta`;
  - finite positive precision/covariance eigen summaries;
  - `hmc_geometry_invoked=false`;
  - `hmc_runtime_invoked=false`.

## Required Artifacts

- Script:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_quadratic_initializer_geometry_2026_07_08.py`
- JSON artifact:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_geometry_cpu_hidden_2026-07-08.json`
- Markdown artifact:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_geometry_cpu_hidden_2026-07-08.md`
- Phase 2 result note:
  `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase2-geometry-initialization-result-2026-07-08.md`
- Draft Phase 3 bounded mechanics subplan if Phase 2 passes.

## Required Checks And Reviews

- Local Codex self-review for coordinate consistency, no HMC runtime, artifact
  completeness, and unsupported claims.
- Local checks:
  - `python -m py_compile docs/benchmarks/benchmark_minimal_ssl_lstm_quadratic_initializer_geometry_2026_07_08.py`
  - `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_minimal_ssl_lstm_quadratic_initializer_geometry_2026_07_08.py`
  - `pytest tests/test_quadratic_map_covariance.py tests/test_hmc_kernel_tuning_geometry.py tests/test_identifiable_ssl_lstm_oracle_geometry.py tests/test_v1_public_api.py -q`
  - `git diff --check`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the Phase 1 theta-coordinate mass artifact be consumed by `initialize_hmc_kernel_geometry` without coordinate or SPD failures? |
| Baseline/comparator | Phase 1 artifact plus `initialize_hmc_kernel_geometry` negative-Hessian contract. |
| Primary pass criterion | Geometry artifact exists and records finite positive `initial_step_size`, positive `initial_num_leapfrog_steps`, finite positive `target_trajectory_length`, `selected_hint=negative_hessian`, no geometry fallback, matching theta-coordinate covariance source, and no HMC runtime. |
| Veto diagnostics | Missing/failed Phase 1 artifact, non-SPD mass, geometry initialization exception, fallback to identity/other hint, nonfinite or nonpositive formula outputs, HMC runtime invoked, unsupported HMC readiness/posterior claim. |
| Explanatory diagnostics | `target_trajectory_length`, `initial_step_size`, `initial_num_leapfrog_steps`, `L * step_size`, difference from `pi/2`, curvature frequency summary, and mass artifact signature. |
| What will not be concluded | HMC runtime readiness, tuning success, posterior correctness, convergence, sampler superiority, default readiness, or Zhao-Cui source-faithfulness. |
| Artifact preserving result | Phase 2 JSON/Markdown artifacts and result note listed above. |

## Forbidden Claims And Actions

- Do not call `tune_hmc_kernel`.
- Do not run a chain, bootstrap screen, acceptance telemetry, or HMC runtime.
- Do not treat `L * step_size` close to or far from `1.57` as a pass/fail
  criterion unless the result violates a predeclared formula finite/positive
  gate.
- Do not claim HMC readiness, posterior correctness, sampler convergence,
  default readiness, or source-faithful Zhao-Cui behavior.

## Exact Next-Phase Handoff Conditions

Phase 3 bounded mechanics may be drafted only if:

- Phase 2 artifact has `decision.geometry_initialization_passed=true`;
- no vetoes fired;
- `selected_hint=negative_hessian`;
- `hmc_runtime_invoked=false`;
- formula outputs are finite and positive;
- result note explicitly states `L * step_size` is explanatory only.

## Stop Conditions

- Phase 1 artifact is absent, rejected, or not theta-coordinate.
- Geometry initialization fails or falls back.
- Required local checks fail without an obvious in-scope repair.
- Continuing would require HMC runtime, GPU/default-policy evidence, external
  Claude review, package installation, or network access.

## Skeptical Plan Audit

| Risk | Phase 2 audit |
| --- | --- |
| Wrong baseline | Uses Phase 1 artifact and HMC geometry initializer contract only. |
| Proxy metric promoted | `L * step_size` and the `1.57` heuristic are explanatory, not pass criteria. |
| Missing stop conditions | Stop conditions block HMC runtime and fallback geometry. |
| Unfair comparison | No ranking or comparison. |
| Hidden assumptions | Negative Hessian is Phase 1 theta-coordinate precision; script must verify this before calling geometry initializer. |
| Stale context | Uses current repaired initializer artifact from Phase 1. |
| Environment mismatch | CPU-hidden debug/reference status must be recorded. |
| Artifact mismatch | JSON/Markdown artifact directly records formula outputs, selected hint, and runtime boundary. |

Audit status: `PASSED_FOR_PHASE_2_GEOMETRY_INITIALIZATION_SMOKE`.

