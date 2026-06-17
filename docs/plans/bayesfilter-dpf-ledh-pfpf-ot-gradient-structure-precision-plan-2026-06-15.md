# BayesFilter DPF LEDH-PFPF-OT Gradient Structure/Precision Plan - 2026-06-15

## Research Intent Ledger

- Main question: For HMC-facing use, how different are gradients between dense
  OT storage and streaming OT computation, and how do FP32/TF32 precision modes
  affect those gradients relative to an FP64 dense reference?
- Candidate or mechanism under test: fixed-branch LEDH-PFPF-OT value-and-score
  on a deterministic LGSSM-shaped fixture, comparing dense tensor OT, streaming
  tensor OT, and streaming callback routes.
- Expected failure mode: streaming data structure may have non-equivalent
  gradients, FP32/TF32 may show score drift larger than value drift, or XLA
  may fail on a gradient path that the value-only path can compile.
- Promotion criterion: dense tensor and streaming tensor agree closely in FP64
  on value and score under raw TensorFlow transport gradients. FP32-no-TF32
  score drift remains small enough to justify larger gradient benchmarks.
- Promotion veto: non-finite scores, failed gradient artifact, mismatched fixed
  fixture between compared arms, or failure of the dense-vs-streaming FP64
  equivalence screen.
- Continuation veto: do not interpret precision score drift if the FP64
  data-structure equivalence check fails.
- Repair trigger: dense-vs-streaming gradient mismatch triggers localization to
  transport-only gradients before any HMC precision conclusion.
- Explanatory diagnostics: value drift, score max absolute drift, score relative
  drift, cosine similarity, norm ratio, compile/warm timing, device placement.
- What must not be concluded: no HMC convergence/readiness claim, no posterior
  validity claim, no production default change, and no statistical ranking from
  one deterministic fixture.

## Evidence Contract

- Engineering/scientific question: Does the memory-efficient streaming data
  structure preserve the gradient needed by HMC, and how much do FP32/TF32
  precision modes perturb that gradient?
- Exact baseline/comparator: FP64 dense tensor route with raw TensorFlow
  transport gradients is the reference. FP64 streaming tensor isolates the data
  structure. FP32/TF32 streaming tensor isolates precision under the same
  structure. Streaming callback is an additional route check, not the primary
  equivalence comparator if it changes the value recursion.
- Primary pass/fail criterion: finite scores and FP64 dense-vs-streaming tensor
  value/score equivalence.
- Diagnostics that can veto: non-finite score, failed child process, mismatched
  fixture/config, or FP64 dense-vs-streaming tensor score mismatch beyond the
  plan tolerance.
- Explanatory-only diagnostics: single-run timing, FP32/TF32 score drift, and
  callback-route drift.
- Artifact preserving result: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-gradient-structure-*.json`
  and result note under `docs/plans`.

## Skeptical Plan Audit

- Wrong baseline: avoided by using FP64 dense tensor as the reference.
- Proxy metrics: value drift is explanatory; score drift is the HMC-relevant
  metric.
- Missing stop conditions: stop precision interpretation if FP64
  dense-vs-streaming tensor equivalence fails.
- Unfair comparison: compare only arms with matching fixed particles,
  observations, masks, transport policy, Sinkhorn settings, chunks, dtype, and
  TF32 flag as appropriate.
- Hidden assumptions: callback pre-flow is not assumed equivalent to fixed
  pre-flow tensor unless the fixture explicitly constructs it that way.
- Environment mismatch: GPU commands must run in trusted context and record
  device placement.
- Artifact mismatch: the aggregate JSON must include both raw scores and
  compact drift summaries.

Audit status: passed for a focused gradient-structure screen.
