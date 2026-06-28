# Low-Rank Residual Posterior-Gradient Calibration Visible Stop Handoff

Date: 2026-06-25

Status: `STOPPED_P02B_FULL_ARTIFACT_NOT_PRODUCED`

## Current State

P00 governance passed. P01 instrumentation passed local checks and Claude
review. P02 trusted GPU/XLA reproduction ran and stopped with
`LOW_RANK_GRADIENT_REPAIR_REQUIRED`: streaming rows passed hard vetoes, but
low-rank rows for `91002:qr_plus` and
`91003:center,q_plus,q_minus,r_plus,r_minus,qr_plus` failed gradient validity.

P02A then ran the focused trusted GPU/XLA repair diagnostic.  It localized the
failure to disconnected/nonfinite low-rank route likelihood and final-particle
gradients on all P02 failing probes.  Route outputs, factors, particles, and
`g` were finite/valid; prior gradients were finite/connected.  The finite value
gradients in P02A are prior-only on the failing probes and do not repair P02.

P02B then planned a route-internal gradient-connectivity diagnostic to test the
candidate hypotheses, including a same-harness A/B tape control, component/block
checkpoint gradients, and mandatory H5 cross-time probes.  Claude reviewed the
revised P02B subplan and returned `VERDICT: AGREE`.  The implementation passed
local syntax and CPU-hidden schema checks, but the full trusted GPU/XLA P02B
artifact was not produced: all-checkpoint instrumentation hit XLA/TensorArray
or compile-scaling limits at P02 shape.  The final run logged a very slow XLA
compile and one compiled cluster but wrote no JSON/Markdown artifact before it
was stopped.  Claude execution review R1 returned `VERDICT: AGREE` that this
is correctly classified as an artifact blocker.  Therefore P02B did not confirm
or reject H1-H5.

Reset memo:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-reset-memo-2026-06-25.md`

Latest P02A result:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02a-gradient-repair-diagnostic-result-2026-06-25.md`

Latest P02B result/blocker:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02b-route-internal-gradient-connectivity-result-2026-06-25.md`

## Stop Summary

The runbook is stopped before P03.  The next safe action is a revised staged
P02B diagnostic plan that avoids an all-checkpoint mega-graph.  A reasonable
next shape is a cheaper A/B tape-control artifact first, then staged
checkpoint groups or a narrower first-break search.  Review that revised shape
before another trusted GPU/XLA run.  Do not patch the solver, run P03, or claim
H1-H5 until the required P02B-style artifact exists.

The runbook's Claude review step for P02A was initially blocked as an external
export of local plan/result artifacts.  After explicit user approval, Claude R1
returned `VERDICT: REVISE`; the docs were patched to quarantine stale P02 raw
artifact phase/title metadata and to frame the `tf.stop_gradient` source hint as
hypothesis-only.  Claude R2 returned `VERDICT: AGREE`.

P02B plan review converged with Claude R2 `VERDICT: AGREE`.  P02B execution
review R1 also returned `VERDICT: AGREE`: the missing JSON/Markdown artifact is
an artifact blocker, not H1-H5 evidence; the CPU-hidden checks are only
harness/schema checks; the physical GPU0 deviation is adequately recorded; and
the next action should be a reviewed P02B-R staged diagnostic with an explicit
runtime stop condition.

## Non-Claims

- No calibrated threshold yet.
- No posterior correctness claim.
- No HMC readiness claim.
- No package default readiness claim.
- No public API readiness claim.
- No statistical superiority claim.
