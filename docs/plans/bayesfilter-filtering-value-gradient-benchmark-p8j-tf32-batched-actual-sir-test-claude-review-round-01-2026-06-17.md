# Claude Review Round 01: P8j TF32 Batched Actual-SIR Test Plan

metadata_date: 2026-06-17
reviewer: Claude Opus max effort, read-only
review_target: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-test-plan-2026-06-17.md
verdict: REVISE

## Findings

1. High: the planned test gate did not force coverage of the new nonlinear
   prior-mean boundary.  The pytest expression could pass on existing
   `streaming_value_core` tests even if no `prior_mean` test existed.

2. Medium: artifact coverage was too weak for the claimed actual-SIR semantics
   tie-out.  The plan needed an executable check that the adapter uses
   `_dpf_sir_callbacks()` semantics and metadata.

3. Medium: the primary runtime gate compared ambiguously defined timing
   envelopes.  The plan needed precise fields showing that each warm timed call
   is one full batched evaluation of the five seeds at the declared shape.

## Required Repair

Patch the plan to require:

- a dedicated nonlinear-prior / actual-SIR adapter test whose absence fails the
  local check;
- JSON fields derived from `_dpf_sir_callbacks()` proving actual SIR route
  semantics;
- explicit timing fields distinguishing compile/first-call, warm-call timings,
  batch size, seed count, `T`, `N`, and scalar comparator scope.

## Verdict

VERDICT: REVISE
