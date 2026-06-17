# BayesFilter DPF LEDH-PFPF-OT GPU Efficient Implementation Plan

Date: 2026-06-15

## Question

Can the current two-source LEDH-PFPF-OT route be made more GPU-memory efficient
without changing the research target to a different OT method?

## Source Split

- Li-Coates supplies the LEDH/PF-PF filtering proposal and corrected-weight
  accounting.
- Corenflos/FilterFlow supplies the entropy-regularized differentiable OT
  resampling route needed for gradients.
- This plan does not replace Corenflos with sliced OT, low-rank OT, learned OT,
  or another research program.

## Evidence Contract

- Engineering question: can we preserve dense FilterFlow-style behavior on small
  fixtures while adding an exact streaming transport operator that avoids
  storing the full `[B,N,N]` transport matrix when requested?
- Baseline/comparator: existing dense FilterFlow-style annealed transport and
  existing batched value recursion on deterministic small fixtures.
- Primary pass/fail criterion: streaming transported particles and value outputs
  match dense outputs within existing tiny-fixture tolerances.
- Veto diagnostics: non-finite outputs, failed dense/streaming parity, failure
  under `tf.function`, accidental use of NumPy/RNG in implementation paths, or
  benchmark/correctness scripts failing to record transport mode.
- Explanatory-only diagnostics: timing, compile time, memory readings, and large
  synthetic LGSSM runs.
- What will not be concluded: no production readiness, no HMC readiness, no
  superiority over dense OT, no validity of large-scale approximate OT, and no
  replacement of the Corenflos route.
- Artifact: this plan plus targeted pytest and benchmark/correctness JSON
  outputs.

## Skeptical Plan Audit

- Wrong baseline: dense FilterFlow-style OT remains the correctness baseline for
  small `N`; streaming is not compared only against timing.
- Proxy metrics: timing and memory do not promote correctness.
- Missing stop condition: any dense/streaming parity failure blocks the change.
- Unfair comparison: benchmark artifacts record dense versus streaming plan mode
  and chunk sizes.
- Hidden assumption: streaming exact OT removes persistent `[N,N]` storage but
  does not remove all-pairs computation; reports must not claim `O(N)` or
  `O(N log N)` scaling.
- Stale context: Li-Coates and Corenflos roles are kept separate.
- Environment mismatch: GPU use remains opt-in/trusted; CPU smoke can validate
  code shape without making GPU claims.
- Artifact relevance: tests and scripts answer implementation correctness and
  memory-shape questions, not scientific performance.

Status: pass for scoped implementation.

## Implementation Scope

1. Preserve dense transport mode as default/reference.
2. Add `transport_plan_mode="streaming"` that computes Sinkhorn softmins and
   transported particles in row/column chunks.
3. Return an empty `[B,0,0]` sentinel instead of materializing `[B,N,N]` in
   streaming mode.
4. Wire mode and chunk sizes through value, correctness, and benchmark scripts.
5. Add dense-versus-streaming correctness tests.
