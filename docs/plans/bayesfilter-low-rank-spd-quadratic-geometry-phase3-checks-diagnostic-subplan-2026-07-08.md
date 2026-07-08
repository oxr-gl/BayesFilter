# Phase 3 Subplan: Focused Checks And Bounded Diagnostic

Date: 2026-07-08
Status: `DRAFT_READY_FOR_EXECUTION`
Master program: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-master-program-2026-07-08.md`

## Phase Objective

Run the required focused checks and one bounded CPU-hidden minimal SSL-LSTM diagnostic using the optional `low_rank_spd_quadratic` geometry strategy.

## Entry Conditions Inherited From Phase 2

- Phase 2 focused integration checks passed.
- The strategy is optional and non-default.
- No unresolved review or implementation blocker remains.

## Required Artifacts

- Diagnostic JSON: `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_cpu_hidden_2026-07-08.json`
- Diagnostic Markdown: `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_cpu_hidden_2026-07-08.md`
- Tuning output directory: `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_public_artifacts_2026-07-08/`
- Diagnostic log: `/tmp/bayesfilter-low-rank-spd-quadratic-geometry-phase3-diagnostic-2026-07-08.log`
- Phase 3 result: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase3-checks-diagnostic-result-2026-07-08.md`

## Required Checks, Tests, Reviews

Run:

```bash
PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile bayesfilter/inference/quadratic_geometry.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py tests/test_quadratic_geometry.py tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py
```

```bash
PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest tests/test_quadratic_geometry.py tests/test_hmc_kernel_tuning_geometry.py tests/test_hmc_kernel_tuning_fixed_mass_step.py tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py -q
```

```bash
git diff --check
```

Then run the bounded diagnostic:

```bash
PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py --initial-geometry-strategy low_rank_spd_quadratic --low-rank-quadratic-sample-count 180 --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_cpu_hidden_2026-07-08.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_cpu_hidden_2026-07-08.md --tuning-output-dir docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_low_rank_spd_quadratic_geometry_public_artifacts_2026-07-08 --public-timeout-budget-s 300.0 --terminal-phase6-repair-extra-attempts 1
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the optional low-rank SPD geometry path produce a structured minimal-target diagnostic artifact or honest fallback without breaking focused HMC checks? |
| Baseline/comparator | Existing Phase 5 diagnostic and 2026-07-07 geometry/tau-gate result. |
| Primary criterion | Focused tests pass and diagnostic JSON/Markdown artifacts are written with CPU-hidden provenance and low-rank geometry diagnostics. |
| Veto diagnostics | Test failure, runtime exception, missing JSON/Markdown artifact, missing low-rank geometry payload/fallback reason, non-SPD accepted precision, unsupported convergence/default/source-faithfulness claim. |
| Explanatory only | Whether low-rank fit accepts, residuals, condition number, center refinement, acceptance, runtime, step, `L`, `L * step`. |
| Not concluded | No posterior correctness, HMC convergence, zero divergences, default readiness, GPU/XLA readiness, source-faithful Zhao-Cui parity, or sampler superiority. |

## Forbidden Claims And Actions

- Do not treat the bounded CPU-hidden diagnostic as GPU/XLA evidence.
- Do not rank low-rank geometry against prior geometry from one run.
- Do not change default policy based on this diagnostic.
- Do not continue to long HMC validation in Phase 3.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 if:

- Required checks pass.
- Diagnostic command exits successfully and writes the required artifacts, or a result note records a true continuation veto.
- Phase 3 result separates candidate rejection from research-direction rejection.

## Stop Conditions

- Focused checks fail after local repair.
- Diagnostic fails before writing structured artifacts.
- Artifact lacks CPU-hidden provenance or low-rank geometry diagnostics.
- Continuing would require changing pass/fail criteria after seeing results.
