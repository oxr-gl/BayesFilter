# Phase 3 Result: Focused Checks And Bounded Diagnostic

Date: 2026-07-08
Status: `VALID_NON_PROMOTING_DIAGNOSTIC_RECORDED`

## Decision

Phase 3 passed as a valid non-promoting diagnostic. The required focused checks passed, the bounded CPU-hidden diagnostic wrote structured artifacts, and a small runtime-scope repair was applied after the first diagnostic exposed a loop closeout bug.

The low-rank SPD quadratic geometry attempt correctly failed closed on the minimal SSL-LSTM target because the holdout fit was poor. The harness preserved the rejection reason and fell back to the existing initial-position curvature path.

## Checks

| Check | Status |
| --- | --- |
| `py_compile` on utility, benchmark, and focused tests | passed |
| `py_compile bayesfilter/inference/hmc_kernel_tuning.py` after repair | passed |
| `pytest tests/test_quadratic_geometry.py tests/test_hmc_kernel_tuning_geometry.py tests/test_hmc_kernel_tuning_fixed_mass_step.py tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py -q` | passed: `44 passed, 27 warnings` |
| `git diff --check` | passed |

## Runtime Repair

The first bounded diagnostic wrote a structured hard-veto artifact:

- JSON: `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_cpu_hidden_2026-07-08.json`
- Public tuning status: `hard_veto`
- Repair trigger: `UnboundLocalError`

Repair applied:

- Initialized `terminal_phase6_slot_payload` before the Phase 7 loop in `bayesfilter/inference/hmc_kernel_tuning.py`.
- Repaired an indentation break in `HMCKernelTuningConfig.payload()` that blocked `py_compile`.

After repair, the rerun wrote a valid non-promoting artifact.

## Final Diagnostic Artifacts

| Artifact | Path |
| --- | --- |
| JSON diagnostic | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_rerun_cpu_hidden_2026-07-08.json` |
| Markdown diagnostic | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_rerun_cpu_hidden_2026-07-08.md` |
| Public tuning result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_rerun_public_artifacts_2026-07-08/hmc_kernel_tuning_result.json` |
| Public progress result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_rerun_public_artifacts_2026-07-08/hmc_kernel_tuning_progress.json` |
| Private tuning events | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_rerun_public_artifacts_2026-07-08/private_diagnostics/hmc_tuning_events.jsonl` |
| Initial mass artifact | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_rerun_public_artifacts_2026-07-08/private_diagnostics/mass_geometry_initial_14b2fba127e244a8.npz` |
| Windowed mass artifact | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_rerun_public_artifacts_2026-07-08/private_diagnostics/mass_windowed_attempt_0_8b267ab232523aa3.npz` |
| First-run blocker log | `/tmp/bayesfilter-low-rank-spd-quadratic-geometry-phase3-diagnostic-2026-07-08.log` |
| Rerun log | `/tmp/bayesfilter-low-rank-spd-quadratic-geometry-phase3-diagnostic-rerun-2026-07-08.log` |

## Runtime Manifest

| Field | Value |
| --- | --- |
| Git commit | `b1c97c9424907e177f8a95ab98657f07b064a081` |
| Environment | TensorFlow `2.20.0`, TFP `0.25.0` |
| CPU/GPU status | `CUDA_VISIBLE_DEVICES=-1`; CPU-hidden diagnostic |
| Seed | `[20260706, 6501]` |
| Runtime | `72.38101256400114` seconds |
| Command | `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py --initial-geometry-strategy low_rank_spd_quadratic --low-rank-quadratic-sample-count 180 --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_rerun_cpu_hidden_2026-07-08.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_rerun_cpu_hidden_2026-07-08.md --tuning-output-dir docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_rerun_public_artifacts_2026-07-08 --public-timeout-budget-s 300.0 --terminal-phase6-repair-extra-attempts 1` |

## Diagnostic Summary

| Diagnostic | Result | Role |
| --- | --- | --- |
| Wrapper status | `passed` | artifact validity |
| Phase decision | `structured_non_promoting_tuning_result_recorded` | non-promoting diagnostic |
| Low-rank geometry status | `holdout_fit_rejected` | repair/explanatory diagnostic |
| Low-rank finite samples | `180` finite; required `150` | sample-ratio gate passed |
| Low-rank holdout RMSE | `10.473452637515818` | holdout gate failed |
| Low-rank accepted | `false` | fail-closed geometry gate |
| Selected geometry after fallback | `regularized_negative_hessian_at_initial_position` | fallback geometry |
| Public tuner final status | `budget_exhausted` | non-promoting tuning blocker |
| Public tuner hard vetoes | `[]` | no runtime hard veto after repair |
| Windowed mass stage | `passed` | handoff stage |
| Fixed-mass step stage | `repair_or_retry` | active blocker |
| Frozen-step trajectory stage | not reached | blocked before trajectory handoff |
| Selected joint pair | absent | no viable `L, epsilon` pair |

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | `VALID_NON_PROMOTING_DIAGNOSTIC_RECORDED` |
| Primary criterion status | `PASSED`: checks passed and artifacts preserve low-rank rejection/fallback provenance. |
| Veto diagnostic status | No final hard vetoes; first-run runtime hard veto was repaired and rerun. |
| Main uncertainty | The minimal target is not well represented by the current local quadratic sample design; the HMC fixed-mass step still cannot find an in-window viable joint pair. |
| Next justified action | Close out this utility/integration runbook and create a separate tuning-design repair plan for the fixed-mass step/trajectory handoff, or a separate robust-MAP/quadratic sampling repair if improving the low-rank fit remains the priority. |
| What is not being concluded | No posterior correctness, HMC convergence, zero divergences, sampler superiority, default readiness, production readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness. |

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | `PASSED_ON_RERUN_NO_HARD_VETO` |
| Statistically supported ranking | `NOT_APPLICABLE` |
| Descriptive-only differences | Low-rank residuals, condition summaries, acceptance, runtime, step/tau diagnostics. |
| Default-readiness | `NOT_CHECKED` |
| Next evidence needed | A separate reviewed repair that targets either the poor low-rank holdout fit or the fixed-mass `L, epsilon` no-viable-pair blocker. |

## Post-Run Red-Team Note

| Field | Note |
| --- | --- |
| Strongest alternative explanation | The low-rank fit may be sampling too broad a trust region or using a rank/feature structure too restrictive for the minimal target's local geometry. |
| Result that would overturn this result | A rerun with reviewed sampling/fit settings showing holdout pass, SPD precision, and preserved nonclaims without runtime hard veto. |
| Weakest part of evidence | One bounded CPU-hidden diagnostic; it validates failure handling and integration, not geometry usefulness for HMC. |

## Boundary Classification

| Boundary | Status |
| --- | --- |
| CPU-hidden bounded diagnostic | `EXECUTED` |
| Trusted GPU/XLA runtime | `NOT_RUN` |
| Long HMC/convergence run | `NOT_RUN` |
| Public API/default-policy change | `NOT_INTRODUCED` |
| Source-faithful Zhao-Cui parity claim | `NOT_CLAIMED` |
| HMC convergence/posterior correctness claim | `NOT_CLAIMED` |
