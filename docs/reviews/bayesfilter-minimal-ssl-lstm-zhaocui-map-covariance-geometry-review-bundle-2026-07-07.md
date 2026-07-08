# Claude Read-Only Review Bundle

Date: 2026-07-07
Review name: `bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-review-2026-07-07`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve boundary crossings, or act as execution authority.

## Objective

Review the planned repair for the minimal scalar SSL-LSTM `zhaocui_fixed` HMC tuning harness: add a bounded MAP-candidate Hessian initial covariance path and repair joint `L, epsilon` candidate viability so out-of-window trajectory lengths cannot be selected.

## Artifacts To Inspect

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-map-covariance-geometry-plan-2026-07-07.md`
- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py`
- `bayesfilter/inference/hmc_kernel_tuning.py`
- `bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py`
- `bayesfilter/inference/mass_matrix.py`
- `tests/test_hmc_kernel_tuning_fixed_mass_step.py`
- `tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py`

## Key Existing Anchors

- Current harness uses `initial_covariance = initial_covariance_scale^2 * I` in `initial_covariance()`.
- `tune_hmc_kernel()` already accepts `negative_hessian`, `initial_covariance`, and `parameter_scales`; geometry hint precedence is negative Hessian, then covariance, then scales.
- Current `_joint_l_epsilon_ladder_candidate_payload()` records `trajectory_length` but marks viability from ladder pass/acceptance/veto state without requiring the trajectory window.
- Existing trajectory helpers include `_trajectory_window_payload()` and direction-specific repair trigger vocabulary used by Phase 6.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the planned repair conceptually safe and sufficient for a bounded diagnostic geometry/selector fix? |
| Baseline/comparator | Current minimal Phase 5 harness with `0.01^2 I` initial covariance and current joint-grid viability semantics. |
| Primary criterion | Plan preserves nonclaims, uses MAP-candidate wording, records provenance, enforces trajectory-window viability, and has focused tests/checks. |
| Veto diagnostics | True MAP or sampler-readiness overclaim; candidate outside trajectory window still viable; hidden default-policy change; missing finite/SPD/provenance gate; insufficient tests. |
| Explanatory diagnostics | Optimizer iterations, Hessian eigenvalues/condition number, acceptance, runtime, descriptive `L * epsilon` distance. |
| Numeric provenance | Target trajectory and window multipliers are existing HMC geometry/tuning config values; new optimizer iteration limits are bounded diagnostic settings, not scientific thresholds. |
| Not concluded | No posterior correctness, convergence, zero divergences, source-faithful Zhao-Cui parity, superiority, default readiness, production readiness, or GPU/XLA readiness. |

## Review Questions

1. Is there a material correctness or boundary issue in using a local `map_candidate` Hessian as a diagnostic initial covariance for this minimal harness?
2. Should joint `L, epsilon` viability require the declared trajectory window, and are the proposed repair triggers appropriate?
3. Are required artifacts and checks sufficient for the stated phase?
4. Are there unsupported claims or hidden authority transfers?
5. Are there unsupported numeric defaults that were invented, inherited, or overcommitted without provenance?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
