# P8j Phase 2 Result: Bootstrap SIR d18 Smoke Implementation

metadata_date: 2026-06-17
status: PASS_PENDING_CLAUDE_IMPLEMENTATION_REVIEW
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Local Phase 2 gate passed; await Claude implementation/result review before Phase 3 execution. |
| Primary criterion status | Passed locally.  SIR DPF route is admitted, semantic callback tests pass, author SIR parity tests pass, and one-seed N=4 bootstrap smoke is finite. |
| Veto diagnostic status | No local veto fired.  The smoke artifact is explicitly one-seed/N=4 and not five-seed value evidence or particle-count adequacy. |
| Main uncertainty | Claude has not yet reviewed the implementation/result packet.  Bootstrap smoke does not establish LEDH/OT readiness or particle adequacy. |
| Next justified action | Claude review of implementation/result, then Phase 3 no-OT Algorithm 1 UKF LEDH SIR smoke subplan review. |
| What is not concluded | No LEDH SIR result, no OT SIR result, no five-seed value, no particle-count tuning, no leaderboard refresh, no score/Hessian/theta-gradient/HMC/NUTS readiness. |

## Implementation Summary

Changed files:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`

Code changes:

- Added `_dpf_sir_callbacks()` wrapping `highdim.zhao_cui_sir_austria_model()`.
- Added `SIR_ROW` to `_dpf_route()` with route label
  `spatial_sir_austria_j9_T20` and horizon `20`.
- Added `SIR_ROW` to `_has_dpf_route()`.
- Added SIR callback tests for required keys, model metadata, transition mean,
  observation mean, infectious-selector Jacobian, covariance callbacks,
  finite density values, clip-only-susceptible transition sample behavior, route
  label/horizon, and one-seed bootstrap smoke.

Boundary metadata:

- `transition_density_contract` is
  `gaussian_pre_projection_density_used_by_reviewed_clipped_path_adapter`.
- `ledh_observation_adapter.adapter_classification` records fixed-parameter SIR
  DPF adapter status and explicitly rejects Zhao-Cui TT/SIRT source-faithfulness
  evidence.

## Checks Run

Focused P8d route/callback tests:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "source_scope_and_route_policy or spatial_sir_value_only or sir_dpf"
```

Result:

- `5 passed, 30 deselected, 2 warnings`

Author SIR parity tests:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_p57_m1_author_sir_callback_parity.py -q
```

Result:

- `5 passed, 2 warnings`

Diff check:

```bash
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-subplan-2026-06-17.md
```

Result:

- passed

## Smoke Artifact

Command: one-seed N=4 bootstrap smoke via `_dpf_single_run()`, deliberate
CPU-only with `CUDA_VISIBLE_DEVICES=-1`.

Artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-2026-06-17.json`

Summary:

| Field | Value |
| --- | --- |
| Status | `executed_one_seed_bootstrap_sir_smoke` |
| Row | `zhao_cui_spatial_sir_austria_j9_T20` |
| Algorithm | `bootstrap_dpf_current` |
| Route label | `spatial_sir_austria_j9_T20` |
| Horizon | `20` |
| Particle count | `4` |
| Seed | `81120` |
| Log likelihood | `-889.6501906825911` |
| Minimum ESS | `1.0116020489327548` |
| Mean ESS | recorded in JSON |
| Resampling count | `3` |

Smoke nonclaims:

- one-seed N=4 smoke only;
- not five-seed DPF value evidence;
- not particle-count adequacy;
- not leaderboard completion;
- not score, Hessian, theta-gradient, HMC, or NUTS evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Recorded by later release artifacts; current worktree is dirty. |
| Dirty state | Repository had substantial pre-existing dirty/untracked work outside P8j; Phase 2 touched only the runner, P8d numeric test, and P8j artifacts. |
| Commands | Focused pytest, `git diff --check`, one-seed bootstrap smoke. |
| Environment | TensorFlow/TensorFlow Probability, deliberate CPU-only. |
| CPU/GPU status | `CUDA_VISIBLE_DEVICES=-1`; TensorFlow emitted CUDA initialization warnings but GPU was intentionally hidden. |
| Data version | Current local P8 source-scope/adapter matrix and SIR synthetic dataset generator. |
| Seeds | Smoke seed `81120`; tests use stateless callback seeds. |
| Output artifacts | This result and the Phase 2 smoke JSON. |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-subplan-2026-06-17.md` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase2-bootstrap-sir-smoke-result-2026-06-17.md` |

## Handoff

Phase 3 may not execute until Claude reviews this implementation/result packet.
If Claude agrees, Phase 3 should run a no-OT Algorithm 1 UKF LEDH SIR smoke
with the same fixed-parameter SIR boundaries and smoke-only nonclaims.
