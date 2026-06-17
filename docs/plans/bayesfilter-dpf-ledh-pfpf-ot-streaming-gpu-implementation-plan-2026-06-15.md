# BayesFilter DPF LEDH-PFPF-OT Streaming GPU Implementation Plan

Date: 2026-06-15

## Research Intent Ledger

- Question: can a streaming `tf.while_loop` LEDH-PFPF-OT value path preserve
  fixed-branch correctness against the current experimental baseline while
  reducing XLA graph blow-up and dense OT materialization pressure?
- Candidate mechanism: a new opt-in TensorFlow implementation in
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`.
- Baseline/comparator: current fixed-branch
  `experimental_batched_ledh_pfpf_ot_tf.batched_ledh_pfpf_ot_value_core_tf`.
- Primary correctness criterion: tiny deterministic fixture parity for log
  likelihood, filtered means, variances, and ESS against the baseline.
- Performance diagnostic: JIT compile and warm-call timings on synthetic LGSSM
  shapes, recorded as descriptive only.
- Promotion vetoes: failed parity, non-finite output, failed `tf.function`
  `jit_compile=True` smoke, source uses a Python `for` time loop in the new
  value core, or the streaming path materializes a `[B,N,N]` transport matrix.
- Explanatory diagnostics: compile time, warm-call time, GPU memory information,
  and output device placement.
- What must not be concluded: no production default readiness, no CPU/GPU
  superiority claim, no active-transport finite-difference score equivalence,
  and no claim that this solves all high-dimensional filtering research
  questions.

## Skeptical Plan Audit

- Wrong baseline risk: the comparator is explicitly the existing experimental
  fixed-branch core, not HMC, NeuTra, or a different particle-flow paper.
- Proxy metric risk: timing and memory are explanatory; they do not promote the
  algorithm without parity and finite-output checks.
- Stop condition: stop implementation if parity or JIT smoke fails until the
  mismatch is diagnosed.
- Fair comparison: keep fixture, transport parameters, and deterministic
  pre-flow inputs fixed between baseline and streaming.
- Hidden assumption: the initial streaming path still accepts full
  `pre_flow_particles`; replacing that with a per-step proposal callback is a
  later interface improvement, not required for this parity-preserving pass.
- Environment mismatch: trusted GPU checks are separate from CPU tests; sandbox
  GPU failures are not interpreted as machine failures.
- Artifact adequacy: tests preserve correctness; benchmark JSON/Markdown
  preserve performance diagnostics.

Audit status: pass for a focused opt-in implementation and smoke benchmark.

## Implementation Checklist

- Add a streaming result contract and `tf.while_loop` value core.
- Default to streaming OT with `transport_plan_mode="streaming"` and no returned
  `[B,N,N]` matrix.
- Support `return_history=False` for likelihood-only GPU/HMC use.
- Add tests for parity, JIT smoke, source-shape constraints, and no dense
  transport output in the streaming default.
- Add or adapt a benchmark harness entry point for the streaming GPU path.
