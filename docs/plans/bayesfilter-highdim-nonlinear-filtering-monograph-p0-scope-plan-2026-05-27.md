# P0 Scope, Evidence Contract, and Reviewer Criteria Plan

## Question

What claim boundary is defensible for a monograph-quality high-dimensional
nonlinear filtering program before any chapter or benchmark work begins?

## Evidence Contract

Baseline:

- BayesFilter V1 master execution summary.
- V1 nonlinear performance final summary.
- Model B/C HMC ladder result.
- Existing nonlinear chapters and NAWM-scale design target.

Primary criterion:

- A reviewer can tell exactly which claims are allowed, which are forbidden,
  what evidence would promote a result, and which stop rules protect the
  program from overclaiming.

Veto diagnostics:

- Any phase plan treats a smoke test as production evidence.
- Any plan merges engineering correctness, numerical validity, sampler validity,
  and scientific interpretation.
- Any plan treats HMC, tensor networks, GPU, XLA, or NAWM as solved.

Explanatory diagnostics:

- Existing V1 benchmark timings and HMC finite-sample rows.

Non-implications:

- Passing P0 does not validate any algorithm or chapter claim.

Artifact:

- Master program and this subplan.

## Tasks

1. Inspect current V1 summaries and relevant chapters.
2. Record allowed/forbidden claims in the master program.
3. Define review-loop and stop-rule mechanics.
4. Prepare P0 result entry in the consolidated execution result.

## Exit Label

`P0_SCOPE_ACCEPTED` if the master program has explicit claim boundaries and no
scope leak.
