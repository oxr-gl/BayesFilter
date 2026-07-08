# Phase 2 Subplan: CPU Regression Through Internal Surface

Date: 2026-07-06

Status: `COMPLETE`

## Phase Objective

Rerun the minimal scalar CPU-hidden debug/reference adapter/canary checks
through the extracted internal module and record whether extraction preserved
the predecessor ladder behavior.

## Entry Conditions Inherited From Previous Phase

- Phase 1 passed and the benchmark harness consumes the internal module.
- Phase 1 result records no behavior/schema drift or explains any drift.
- Phase 1 semantic predecessor comparator passed for schema, fixture, target
  values, shapes, capability metadata, nonclaims, and adapter signature.
- No GPU/XLA or long-run boundary is open.

## Required Artifacts

- Adapter CPU regression JSON:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_adapter_cpu_hidden_2026-07-06.json`
- Adapter CPU regression Markdown:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_adapter_cpu_hidden_2026-07-06.md`
- Canary CPU regression JSON:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_canary_cpu_hidden_2026-07-06.json`
- Canary CPU regression Markdown:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_canary_cpu_hidden_2026-07-06.md`
- Short-ladder CPU regression JSON:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_short_ladder_cpu_hidden_2026-07-06.json`
- Short-ladder CPU regression Markdown:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_short_ladder_cpu_hidden_2026-07-06.md`
- Quiet log under
  `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/`.
- Phase 2 result file.
- Refreshed Phase 3 GPU/XLA smoke subplan.

## Required Checks, Tests, Reviews

- Compile:
  `python -m compileall -q bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py tests/test_ssl_lstm_zhaocui_hmc_minimal.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`
- Focused tests:
  `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 pytest -q tests/test_ssl_lstm_zhaocui_hmc_minimal.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`
- Adapter regression command:
  `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py --mode phase1-adapter --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_adapter_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_adapter_cpu_hidden_2026-07-06.md`
- Tiny canary regression command:
  `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py --mode phase2-canary --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_canary_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_canary_cpu_hidden_2026-07-06.md --num-results 2 --num-burnin-steps 1 --step-size 1e-5 --num-leapfrog-steps 1 --seed 20260706 2201`
- Short-ladder regression command:
  `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py --mode phase4-short-ladder --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_short_ladder_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_short_ladder_cpu_hidden_2026-07-06.md`
- Forbidden-token scan:
  `rg -n "GradientTape|tf\\.py_function|import numpy|np\\." bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py`
- `git diff --check`
- Material result/handoff review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the extracted internal module preserve CPU-hidden minimal HMC mechanics behavior? |
| Baseline/comparator | Predecessor Phase 1/2/4 CPU-hidden artifacts and Phase 1 extraction result. |
| Primary pass criterion | Compile/tests pass, all three CPU-hidden regression commands write valid artifacts with no hard vetoes, adapter regression preserves the immutable predecessor comparator fields, and no debug evidence is mislabeled as GPU/default/convergence evidence. |
| Veto diagnostics | Nonfinite value/score, runtime exception, nonfinite samples, invalid artifact, schema drift, unsupported claim, or debug evidence mislabeled as default/GPU evidence. |
| Explanatory diagnostics | Runtime, score norm, log probability, acceptance, finite counts, and artifact diff summary. |
| Not concluded | GPU/XLA behavior, convergence, posterior correctness, ranking, source-faithful parity, default readiness, or LEDH result. |

## Forbidden Claims And Actions

Do not run GPU/CUDA/XLA or long sampler diagnostics. Do not claim convergence,
posterior correctness, ranking, source-faithful parity, default readiness, or
GPU/XLA production readiness.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 only after CPU regression passes and Phase 3 has explicit
trusted GPU/XLA approval or a result deferring the boundary.

## Stop Conditions

Stop if CPU regression fails in a way that invalidates the extracted target,
artifacts are corrupted, or continuing requires unapproved GPU/long-run
boundary.
