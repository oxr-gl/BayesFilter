# Phase 3 Subplan: Trusted GPU/XLA Runtime Smoke

Date: 2026-07-06

Status: `COMPLETE`

## Phase Objective

Run the smallest trusted GPU/XLA runtime-path smoke through the reusable
internal minimal scalar target, recording device provenance and preserving the
scope as runtime smoke only.

## Entry Conditions Inherited From Previous Phase

- Phase 2 CPU regression passed.
- The user has explicitly approved the trusted GPU/CUDA/XLA HMC command, or the
  phase must write a deferral result and stop/advance according to the master
  program.

## Required Artifacts

- GPU/XLA smoke JSON artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase3_gpu_xla_smoke_2026-07-06.json`
- GPU/XLA smoke Markdown artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase3_gpu_xla_smoke_2026-07-06.md`
- Quiet log:
  `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/phase3_gpu_xla_smoke_2026-07-06.log`
- Phase 3 result file.
- Refreshed Phase 4 longer-diagnostics design subplan.

## Required Checks, Tests, Reviews

- Trusted GPU provenance check:
  `nvidia-smi`
- Compile/test precheck:
  `python -m compileall -q bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py tests/test_ssl_lstm_zhaocui_hmc_minimal.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`
- Smallest approved HMC runtime command with XLA enabled:
  `CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py --mode phase3-gpu-xla-smoke --trusted-gpu-xla-approval --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase3_gpu_xla_smoke_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase3_gpu_xla_smoke_2026-07-06.md --num-results 2 --num-burnin-steps 1 --step-size 1e-5 --num-leapfrog-steps 1 --seed 20260706 3301 > docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/phase3_gpu_xla_smoke_2026-07-06.log 2>&1`
- Artifact validation and material result review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the extracted minimal scalar target launch through the trusted GPU/XLA HMC runtime path without hard-veto failure? |
| Baseline/comparator | Phase 2 CPU-hidden regression and predecessor CPU-hidden ladder. |
| Primary pass criterion | Trusted GPU/XLA command writes valid artifact with device provenance, `use_xla=True`, `jit_compile=True`, explicit approval flag recorded, no runtime exception, finite samples, and no hard vetoes. |
| Veto diagnostics | Missing explicit approval, CPU-hidden or missing GPU device context, missing provenance, CUDA/XLA runtime exception, nonfinite target/sample, invalid artifact, unsupported convergence/default-readiness claim, or artifact not recording `use_xla=True`/`jit_compile=True`. |
| Explanatory diagnostics | Runtime, acceptance, device names, XLA compile metadata when available, TF32 setting, and TensorFlow warnings. |
| Not concluded | HMC convergence, posterior correctness, ranking, default readiness, production readiness, source-faithful parity, or LEDH result. |

## Forbidden Claims And Actions

Do not treat a launch smoke as convergence, correctness, ranking, or default
readiness. Do not run this phase without explicit GPU/XLA approval.

Do not run a CPU-hidden substitute for Phase 3. If the approved GPU/XLA command
cannot run, write a deferral or blocker result; do not relabel CPU evidence as
GPU/XLA evidence.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 only if GPU/XLA smoke passes or is explicitly deferred with
a result that states why longer diagnostics may or may not proceed.

## Stop Conditions

Stop if approval is absent, the trusted runtime fails in a way that invalidates
the target artifact, provenance is missing, or review does not converge.
