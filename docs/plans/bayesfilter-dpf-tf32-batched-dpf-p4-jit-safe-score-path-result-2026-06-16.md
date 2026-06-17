# Phase 4 Result - JIT-Safe Score Path - 2026-06-16

## Status

`PHASE_4_BLOCKED_FIXABLE_SCORE_JIT`

## Objective

Test whether the streaming relaxed-objective value+score path is currently
JIT-safe on a tiny no-resampling fixture before HMC-facing diagnostics.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the streaming relaxed-objective value+score path run under `tf.function(jit_compile=True)` on a tiny fixture? |
| Baseline/comparator | Current streaming score diagnostic script and no-resampling tiny fixture. |
| Primary pass criterion | Failed. The tiny FP64 no-resampling score/JIT diagnostic exited nonzero during XLA compilation. |
| Veto diagnostics | JIT compile failure fired. No HMC-facing diagnostics may proceed. |
| Explanatory diagnostics | XLA reports an unfixed TensorArray/tensor-list size in the gradient through a `tf.while_loop`. |
| Not concluded | No HMC readiness, no score correctness, no posterior validity, no production/public API readiness. |

## Command Artifact

Command output was redirected per the quiet execution pattern.

Log:

- `docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-2026-06-16.log`

Expected JSON/Markdown artifacts were not produced because the command failed
during XLA compilation.

## Failure Summary

The log tail reports:

```text
XLA compilation requires a fixed tensor list size. Set the max number of
elements. This could also happen if you're using a TensorArray in a while loop
that does not have its maximum_iteration set.
```

The failing node is in the gradient path:

```text
gradient_tape/while/while/Any_0/accumulator
```

Interpretation: the streaming value path can JIT for value-only execution, but
the score path through `GradientTape` and the current `tf.while_loop` /
`TensorArray` structure is not XLA-safe yet.

## Decision

Phase 4 is blocked by a fixable engineering issue. The next repair should focus
on the streaming value core's `tf.while_loop` history/accumulator structure and
any TensorArray created inside gradient-bearing control flow.

Candidate repair directions to evaluate in a new Phase 4 repair subplan:

- add `maximum_iterations` to relevant `tf.while_loop` calls where static
  `time_steps` or block counts are known;
- avoid creating zero-size TensorArrays on the gradient-bearing
  `return_history=False` path if they still become gradient accumulators;
- split a score-specific likelihood-only core that carries only tensors needed
  for the scalar objective;
- test no-resampling score JIT before active transport score behavior.

## Required Next Action

Create a focused Phase 4 repair subplan before editing code. The repair
subplan must preserve:

- value-path semantics;
- FP64 and FP32-no-TF32 reference lanes;
- the distinction between relaxed-objective score and categorical PF score;
- the prohibition on HMC readiness claims before score JIT and HMC diagnostics
  pass.
