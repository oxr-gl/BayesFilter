# BayesFilter DPF TF32 Batched DPF Visible Stop Handoff - 2026-06-16

## Status

`PHASE_6_CLOSEOUT_GUARDRAILS_PASSED`

## Current State

The visible TF32 batched DPF master program is closed through Phase 6.

Clean visible execution was restarted from:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-reset-memo-2026-06-16.md`

The final closeout result is:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p6-closeout-guardrails-result-2026-06-17.md`

## Final Phase Summary

Phase 0 passed and created the master program, visible runbook, ledger, stop
handoff, Phase 0 result, Claude review trail, and Phase 1 subplan.

Phase 1 passed and inventoried the streaming value path, precision lanes,
score/JIT boundary, and dirty-worktree constraints.

Phase 2 passed. It verified a tiny streaming correctness/JIT guardrail, a
bounded single-GPU TF32 JIT value artifact on GPU 0, and a tiny FP32-no-TF32
reference-lane artifact.

Phase 3 passed. It verified two trusted GPUs and produced per-GPU independent
row-split TF32 value artifacts for rows `[0, 1]` and `[2, 3]`.

Phase 4 passed after staged repair:

- no-resampling score/JIT repair passed;
- active-transport score/JIT compile repair passed up to JSON serialization;
- streaming active transport score NaNs were localized to the padded
  streaming column log normalizer backward path;
- finite log-zero padding and loop-variable structure repairs made the active
  streaming raw-gradient score path finite on the tiny active-odd fixture.

Phase 5 passed with an explicit GPU TF32 full-chain HMC limitation:

- CPU FP64 active-odd score/JIT guardrail passed;
- CPU and trusted GPU0 JIT PF MC-vs-precision diagnostics passed on the tiny
  active-odd fixture;
- CPU FP64 HMC mechanics smoke passed with finite samples, target log
  probabilities, log accept ratios, and MH trace;
- direct GPU TF32 full-chain HMC mechanics was not completed because the
  generic HMC runner hard-casts `initial_state` to `tf.float64`.

Phase 6 passed and recorded final guardrails, artifact pointers, nonclaims, and
next actions.

Post-closeout mixed-precision HMC smoke passed:

- HMC state, step size, leapfrog bookkeeping, and MH diagnostics stayed FP64;
- DPF target computation ran internally in FP32/TF32 on trusted GPU0;
- value/score tensors were cast back to FP64 for TFP HMC;
- tiny active-odd GPU0 mechanics smoke passed hard-veto checks.

This does not test full FP32 HMC mechanics and does not establish HMC readiness.

## Key Current Artifacts

- Ledger:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-visible-execution-ledger-2026-06-16.md`
- Master program:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-master-program-2026-06-16.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-visible-gated-execution-runbook-2026-06-16.md`
- Phase 4 streaming-gradient repair result:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-streaming-gradient-nan-repair-result-2026-06-17.md`
- Phase 5 HMC-facing diagnostics result:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p5-hmc-facing-diagnostics-result-2026-06-17.md`
- Phase 6 closeout result:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p6-closeout-guardrails-result-2026-06-17.md`
- Mixed-precision HMC smoke result:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-mixed-precision-hmc-smoke-result-2026-06-17.md`
- Active-odd score/JIT artifact:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-nan-repair-rerun-2026-06-17.json`
- Phase 5 GPU0 precision-vs-MC artifact:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p5-pf-mc-error-vs-precision-gpu0-jit-b1-t3-np8-d2-m2-seeds3-active-odd-2026-06-17.json`
- CPU FP64 HMC mechanics smoke artifact:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p5-hmc-mechanics-smoke-fp64-cpu-b1-t3-np8-d2-m2-active-odd-rerun-2026-06-17.json`
- Trusted GPU0 mixed-precision HMC smoke artifact:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-mixed-precision-hmc-smoke-fp32-tf32-gpu0-b1-t3-np8-d2-m2-active-odd-2026-06-17.json`

## Latest Checks

- Phase 4 status grep: passed,
  `PHASE_4_STREAMING_GRADIENT_NAN_REPAIR_PASSED`.
- Phase 5 status grep: passed,
  `PHASE_5_HMC_FACING_DIAGNOSTICS_PASSED_WITH_GPU_HMC_TF32_LIMITATION`.
- Required Phase 5 artifacts: present.
- Phase 5 final `py_compile`: passed, log at
  `docs/benchmarks/logs/p5-final-pycompile-2026-06-17.log`.
- `git diff --check`: passed before Phase 6 closeout writes.
- Mixed-precision focused dtype tests: passed, `2 passed`.
- CPU FP32-no-TF32 mixed-precision HMC smoke: passed.
- Trusted GPU0 FP32/TF32 mixed-precision HMC smoke: passed.

## If Continuing In A New Session

Start from the Phase 6 result:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p6-closeout-guardrails-result-2026-06-17.md`

Then choose a new, separate subplan. The safest next engineering subplan is a
larger replicated mixed-precision HMC-facing diagnostic ladder. A full FP32 HMC
runtime dtype subplan is separate and should not be required for the current
preferred FP64-HMC/TF32-target architecture.

## Nonclaims

This clean run did not establish HMC readiness, posterior correctness, chain
convergence, production readiness, public API readiness, scientific
correctness, TF32 superiority, broad GPU speedup, 100k-particle score
scalability, or single-filter particle-cloud sharding across GPUs.
