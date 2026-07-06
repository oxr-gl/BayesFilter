# LEDH Compact Sensitivity Phase 1 Review Bundle

## Role

Claude is a read-only reviewer.  Codex remains supervisor and executor.  Do not
edit files, run commands, or authorize boundaries.

## Objective

Review the Phase 1 mathematical documentation and master plan for a new
memory-light LEDH-PFPF-OT score route.  The route should compute the total
derivative of the same finite scalar value executed by the fixed-randomness
LEDH + finite Sinkhorn computation, while avoiding the old full-history reverse
scan as the admitted production score.

## Files And Ranges

Review only these fixed paths/ranges:

- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`, section
  `Compact Sensitivity Score For Finite LEDH--PFPF--OT`, currently around
  lines 780-1057.
- `docs/plans/bayesfilter-ledh-compact-sensitivity-score-master-program-2026-07-05.md`.

## Evidence Already Run

- Local label/reference search found the new labels.
- MathDevMCP audit on
  `prop:bf-hd-ledh-compact-sensitivity-score` returned `status=unverified` with
  no contradiction/mismatch; it asked for domain assumptions around inverse,
  Cholesky, and log determinant.  Codex patched the section to state positive
  definiteness, jitter/projection semantics, and branch-boundary assumptions.
- A second MathDevMCP summary remained formally unverified, with remaining
  items requiring human/formal review and solve-conditioning diagnostics.

## Review Questions

Please answer these specific questions:

1. Does the LaTeX section correctly distinguish the exact likelihood score from
   the total derivative of the executed finite LEDH-PFPF-OT scalar?
2. Is the forward sensitivity/JVP route mathematically plausible as a
   memory-light replacement for full-history reverse mode, under the stated
   branch and positive-definite assumptions?
3. Does the plan require the right gates before demoting the old route:
   no-tape source/runtime checks, same-scalar finite differences, tiny parity
   with the old diagnostic route, and value/score same-route metadata?
4. Is there a material mathematical or planning blocker that must be fixed
   before implementation starts?

## Forbidden Claims

Do not approve claims of exact Kalman correctness, HMC readiness, posterior
correctness, nonlinear-row support, or runtime ranking against frozen
non-LEDH rows.

## Required Verdict Format

End with exactly one of:

`VERDICT: AGREE`

or

`VERDICT: REVISE`

If `REVISE`, list only blocking fixes required before implementation.
