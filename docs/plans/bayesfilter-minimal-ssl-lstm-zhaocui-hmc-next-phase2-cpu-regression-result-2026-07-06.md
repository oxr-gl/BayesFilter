# Phase 2 Result: CPU Regression Through Internal Surface

Date: 2026-07-06

Status: `COMPLETE`

## Phase Objective

Rerun the minimal scalar CPU-hidden debug/reference adapter/canary checks
through the extracted internal module and record whether extraction preserved
the predecessor ladder behavior.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the extracted internal module preserve CPU-hidden minimal HMC mechanics behavior? |
| Baseline/comparator | Predecessor Phase 1/2/4 CPU-hidden artifacts and Phase 1 extraction result. |
| Primary pass criterion | Compile/tests pass, all three CPU-hidden regression commands write valid artifacts with no hard vetoes, adapter regression preserves the immutable predecessor comparator fields, and no debug evidence is mislabeled as GPU/default/convergence evidence. |
| Veto diagnostics | Nonfinite value/score, runtime exception, nonfinite samples, invalid artifact, schema drift, unsupported claim, or debug evidence mislabeled as default/GPU evidence. |
| Explanatory diagnostics | Runtime, score norm, log probability, acceptance, finite counts, and artifact diff summary. |
| Not concluded | GPU/XLA behavior, convergence, posterior correctness, ranking, source-faithful parity, default readiness, or LEDH result. |

## Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Compile | `PASSED` | Internal module, harness, new tests, and existing ladder tests compiled. |
| Focused pytest | `PASSED` | Quiet log reports `12 passed`. |
| Adapter regression | `PASSED` | Artifact status `passed`, hard vetoes `[]`, log prob `-1.3985848756201187`, score shape `[24]`, signature `85095a36eaf605d1d84c539d5d912896b63c4028ae0aa8e63c5d63d183c85508`. |
| Tiny canary regression | `PASSED` | Artifact status `passed`, hard vetoes `[]`, sample shape `[2, 24]`, samples all finite `True`, seed `[20260706, 2201]`. |
| Short ladder regression | `PASSED` | Artifact status `passed`, hard vetoes `[]`, all predeclared seeds passed `True`, row count `3`. |
| Forbidden-token scan | `PASSED` | No `GradientTape`, `tf.py_function`, `import numpy`, or `np.` hits in the internal module or harness target path. |
| `git diff --check` | `PASSED` | Repository diff check returned exit status 0. |

## Runtime Artifacts

- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_adapter_cpu_hidden_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_adapter_cpu_hidden_2026-07-06.md`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_canary_cpu_hidden_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_canary_cpu_hidden_2026-07-06.md`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_short_ladder_cpu_hidden_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase2_short_ladder_cpu_hidden_2026-07-06.md`
- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/phase2_adapter_cpu_hidden_2026-07-06.log`
- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/phase2_canary_cpu_hidden_2026-07-06.log`
- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/phase2_short_ladder_cpu_hidden_2026-07-06.log`
- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/phase2_pytest_cpu_hidden_2026-07-06.log`

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `PASS_PHASE2_ADVANCE_TO_PHASE3_BOUNDARY_REVIEW` |
| Primary criterion status | `PASSED` |
| Veto diagnostic status | `NO_PHASE2_HARD_VETO_OBSERVED` |
| Main uncertainty | CPU-hidden non-JIT regression does not answer GPU/XLA behavior, convergence, posterior correctness, ranking, or default-readiness questions. |
| Next justified action | Review Phase 3 trusted GPU/XLA smoke boundary and request explicit approval if the boundary-safe subplan remains justified. |
| What is not being concluded | GPU/XLA behavior, HMC convergence, posterior correctness, ranking, source-faithful parity, public API/package readiness, default readiness, or LEDH result. |
