# Phase 1 Subplan: Initializer Artifact Smoke

Date: 2026-07-08

## Status

`DRAFT_SUBPLAN`

## Phase Objective

Run the repaired reusable quadratic MAP-covariance initializer on the minimal
scalar SSL-LSTM `zhaocui_fixed` target and write a structured CPU-hidden
diagnostic artifact proving only that the initializer produced a finite SPD
theta-coordinate mass candidate.

This phase must not initialize HMC geometry and must not run HMC.

## Entry Conditions

- Phase 0 coordinate audit result exists and identifies the required transform
  from whitened `z` precision to original theta precision.
- `estimate_quadratic_map_covariance` has been patched so accepted
  `precision`/`covariance` are in original theta coordinates when `scale` is
  supplied.
- Focused tests passed after the patch:
  - `pytest tests/test_quadratic_map_covariance.py tests/test_identifiable_ssl_lstm_oracle_geometry.py tests/test_v1_public_api.py -q`
  - `python -m py_compile bayesfilter/inference/quadratic_map_covariance.py bayesfilter/inference/hmc_kernel_tuning.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py`
  - `git diff --check`

## Required Artifacts

- Script:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_quadratic_initializer_artifact_2026_07_08.py`
- JSON artifact:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_artifact_cpu_hidden_2026-07-08.json`
- Markdown artifact:
  `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_artifact_cpu_hidden_2026-07-08.md`
- Phase 1 result note:
  `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase1-initializer-artifact-result-2026-07-08.md`
- Draft Phase 2 subplan if Phase 1 passes.

## Required Checks And Reviews

- Local Codex self-review of the subplan and script for:
  coordinate consistency, artifact coverage, HMC boundary safety, and unsupported
  claims.
- Local checks:
  - `python -m py_compile docs/benchmarks/benchmark_minimal_ssl_lstm_quadratic_initializer_artifact_2026_07_08.py`
  - `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_minimal_ssl_lstm_quadratic_initializer_artifact_2026_07_08.py`
  - `pytest tests/test_quadratic_map_covariance.py tests/test_identifiable_ssl_lstm_oracle_geometry.py tests/test_v1_public_api.py -q`
  - `git diff --check`
- Claude review is not used in this phase unless the user separately approves
  external transfer after the prior approval rejection.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the repaired reusable initializer produce a finite SPD theta-coordinate mass artifact on the minimal scalar SSL-LSTM target? |
| Baseline/comparator | Phase 0 coordinate audit plus the old Phase 5 manual transform convention. |
| Primary pass criterion | JSON artifact exists and records `accepted=true`, finite positive precision/covariance eigen summaries, `mass_precision_coordinate_system=theta`, `mass_covariance_coordinate_system=theta`, and no HMC runtime. |
| Veto diagnostics | Initial target value/score nonfinite; initializer rejected; missing theta-coordinate diagnostics; non-SPD returned precision/covariance; CPU-hidden status missing; HMC geometry/runtime invoked; unsupported HMC readiness or posterior claim. |
| Explanatory diagnostics | Locator status, geometry status, sample counts, condition number, map-candidate role, scale summary, covariance source, and nonclaims. |
| What will not be concluded | HMC geometry readiness, HMC runtime readiness, posterior correctness, convergence, sampler superiority, default readiness, or Zhao-Cui source-faithfulness. |
| Artifact preserving result | Phase 1 JSON/Markdown artifacts and result note listed above. |

## Forbidden Claims And Actions

- Do not call `initialize_hmc_kernel_geometry`.
- Do not call `tune_hmc_kernel` or any HMC runtime.
- Do not use GPU/default-policy evidence.
- Do not claim MAP quality beyond `map_candidate_role` recorded by the
  initializer.
- Do not claim HMC readiness, posterior correctness, convergence, default
  readiness, or source-faithful Zhao-Cui behavior.
- Do not change pass/fail criteria after seeing the Phase 1 result.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- Phase 1 artifact has `decision.initializer_artifact_passed = true`;
- `decision.vetoes` is empty;
- artifact records theta-coordinate mass semantics;
- artifact records CPU-hidden debug/reference status;
- result note says Phase 1 did not run HMC geometry or HMC runtime.

Phase 2 must use the Phase 1 `map_candidate` or `locator_position` only in its
recorded role and must initialize HMC geometry only, still without HMC runtime.

## Stop Conditions

- The initializer is rejected or produces nonfinite/non-SPD mass.
- Coordinate diagnostics are absent or contradict Phase 0.
- The artifact would not answer the Phase 1 question.
- A required local check fails without an obvious in-scope repair.
- Continuing would require HMC runtime, GPU/default-policy evidence, external
  Claude review, package installation, or network access.

## Skeptical Plan Audit

| Risk | Phase 1 audit |
| --- | --- |
| Wrong baseline | Uses Phase 0 coordinate rule and old Phase 5 transform convention only, not sampler success. |
| Proxy metric promoted | Fit acceptance and eigen summaries are initializer-artifact gates only. |
| Missing stop conditions | Stop conditions block HMC geometry/runtime and non-SPD artifacts. |
| Unfair comparison | No ranking or method comparison. |
| Hidden assumptions | `scale=prior_scale` is a coordinate transform for local quadratic fitting; returned mass must be theta-coordinate. |
| Stale context | Uses current repaired `estimate_quadratic_map_covariance` source in this worktree. |
| Environment mismatch | CPU-hidden debug/reference exception is required and must be recorded. |
| Artifact mismatch | JSON/Markdown artifact directly records initializer status, coordinate semantics, and nonclaims. |

Audit status: `PASSED_FOR_PHASE_1_INITIALIZER_ARTIFACT_SMOKE`.

