# Phase 3 Result: Trusted GPU/XLA Runtime Smoke

Date: 2026-07-06

Status: `COMPLETE`

## Phase Objective

Run the smallest trusted GPU/XLA runtime-path smoke through the reusable
internal minimal scalar target, recording device provenance and preserving the
scope as runtime smoke only.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the extracted minimal scalar target launch through the trusted GPU/XLA HMC runtime path without hard-veto failure? |
| Baseline/comparator | Phase 2 CPU-hidden regression and predecessor CPU-hidden ladder. |
| Primary pass criterion | Trusted GPU/XLA command writes valid artifact with device provenance, `use_xla=True`, `jit_compile=True`, explicit approval flag recorded, no runtime exception, finite samples, and no hard vetoes. |
| Veto diagnostics | Missing explicit approval, CPU-hidden or missing GPU device context, missing provenance, CUDA/XLA runtime exception, nonfinite target/sample, invalid artifact, unsupported convergence/default-readiness claim, or artifact not recording `use_xla=True`/`jit_compile=True`. |
| Explanatory diagnostics | Runtime, acceptance, device names, XLA compile metadata when available, TF32 setting, and TensorFlow warnings. |
| Not concluded | HMC convergence, posterior correctness, ranking, default readiness, production readiness, source-faithful parity, or LEDH result. |

## Review And Approval

- External Claude review remained denied for private-context transfer risk.
- Fresh visible Codex substitute boundary review returned `VERDICT: AGREE`.
- Trusted GPU provenance command `nvidia-smi` was approved and run.
- Reviewed GPU/XLA smoke command was approved and run.

## Checks

| Check | Status | Evidence |
| --- | --- | --- |
| GPU provenance | `PASSED` | `nvidia-smi` showed GPU 0 and GPU 1 available; GPU 0 used by the smoke command. |
| Explicit approval flag | `PASSED` | Artifact records `trusted_gpu_xla_approval: true`. |
| Device provenance | `PASSED` | Artifact records `CUDA_VISIBLE_DEVICES=0`, physical GPU `/physical_device:GPU:0`, and trust basis `explicit_user_approved_trusted_gpu_xla_hmc_runtime`. |
| XLA/JIT path | `PASSED` | Artifact records `use_xla: true`, `jit_compile: true`; log records XLA cluster compilation. |
| HMC runtime | `PASSED` | No runtime exception; sample shape `[2, 24]`; samples all finite `True`. |
| Hard veto screen | `PASSED` | `hard_vetoes: []`. |
| `git diff --check` | `PASSED` | Repository diff check returned exit status 0 after the run. |

## Runtime Artifact Summary

| Field | Value |
| --- | --- |
| JSON artifact | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase3_gpu_xla_smoke_2026-07-06.json` |
| Markdown artifact | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase3_gpu_xla_smoke_2026-07-06.md` |
| Quiet log | `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/phase3_gpu_xla_smoke_2026-07-06.log` |
| Status | `passed` |
| Hard vetoes | `[]` |
| Seed | `[20260706, 3301]` |
| Sample shape | `[2, 24]` |
| Samples all finite | `True` |
| Acceptance rate | `1.0` explanatory only |
| Native divergence status | `not_exposed_by_kernel`; not interpreted as zero divergences |
| Runtime | `tfp.mcmc.sample_chain` |
| XLA first call | compile plus execute, explanatory only |

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | `PASSED_FOR_LAUNCH_SMOKE` |
| Statistically supported ranking | `NOT_CLAIMED` |
| Descriptive-only differences | Runtime and acceptance are explanatory only. |
| Default-readiness | `NOT_CHECKED` |
| Next evidence needed | Reviewed longer diagnostics before any convergence, posterior, ranking, or default-readiness claim. |

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `PASS_PHASE3_ADVANCE_TO_PHASE4_DESIGN` |
| Primary criterion status | `PASSED_LAUNCH_SMOKE_ONLY` |
| Veto diagnostic status | `NO_PHASE3_HARD_VETO_OBSERVED` |
| Main uncertainty | Tiny GPU/XLA smoke does not assess convergence, posterior correctness, ranking, production readiness, or default readiness. |
| Next justified action | Design a longer sampler-diagnostics ladder with predeclared evidence roles and approval boundaries. |
| What is not being concluded | HMC convergence, posterior correctness, ranking, source-faithful parity, public API/package readiness, default readiness, GPU/XLA production readiness, or LEDH result. |
