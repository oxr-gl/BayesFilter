# LEDH-PFPF-OT Total-VJP GPU/XLA Validation Master Program

Date: 2026-07-01

Status: `COMPLETE`

## Objective

Validate whether the corrected LEDH-PFPF-OT `transport_ad_mode="full"` manual
total-derivative route can run in the repository default GPU/XLA/TF32 lane, and
then decide the next implementation action from evidence.

The mathematical target is the total derivative of the finite fixed-Sinkhorn
scalar.  The stopped route computes a partial derivative and is wrong relative
to any claim that it is the score of the executed active-transport scalar.

## Role Contract

Codex is supervisor and executor.

Claude is a read-only reviewer only.  Claude may identify blockers in plans,
results, diffs, and claim wording, but cannot authorize crossing human,
runtime, model-file, funding, product-capability, or scientific-claim
boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the corrected total-derivative finite-Sinkhorn manual route run under trusted GPU/XLA/TF32, and does it remain viable as particle count increases? |
| Baseline/comparator | Phase 0 CPU float64 same-finite-scalar repair artifact `bayesfilter-ledh-pfpf-ot-manual-total-vjp-score-repair-result-2026-07-01.md`; Phase 1 same route on GPU/XLA; later phases compare particle-count ladder behavior within the same route. |
| Primary pass criterion | The reviewed phase gate passes: exact GPU-visible execution, XLA JIT for the manual-reverse unit, `transport_ad_mode="full"`, finite objective, finite gradient, finite seed MCSE, and recorded artifacts. |
| Veto diagnostics | CPU fallback; missing GPU tensors; XLA not used when the phase asks for XLA; nonfinite objective or gradient; route reports `transport_ad_mode!="full"`; stopped partial route used as the score; OOM; unsupported dtype/global-state drift; result artifact absent or internally inconsistent. |
| Explanatory diagnostics | Runtime, compile time, GPU memory, per-seed gradient variance, gradient norm, MCSE, row residuals when emitted, comparison to historical stopped-route artifacts. |
| Not concluded | No HMC readiness, no posterior correctness, no exact nonlinear likelihood score, no production default promotion, no no-autodiff production VJP claim. |
| Artifacts | This master program, phase subplans/results, visible runbook, execution ledger, stop handoff, JSON/markdown run outputs under `docs/plans`. |

## Skeptical Plan Audit

Wrong-baseline risk:
The stopped partial derivative cannot be used as a correctness baseline.  The
correct baseline for the mathematical repair is the same finite scalar, already
checked in CPU float64.  GPU phases check viability of that route, not exact
likelihood correctness.

Proxy-metric risk:
Finite GPU gradients, runtime, and memory are viability metrics.  They do not
prove HMC readiness or statistical correctness.

Environment risk:
All GPU/CUDA/NVIDIA commands must run with trusted/escalated permissions.  A
non-escalated GPU failure is sandbox evidence only.

Route risk:
The existing GPU/XLA runner must be verified to record `transport_ad_mode="full"`
and the manual-reverse XLA compiler.  If it silently runs `stabilized`, Phase 1
fails.
Phase 0 must also prove from code anchors that the legacy manual streaming
gradient-mode selector paired with `transport_ad_mode="full"` dispatches to the
total-derivative helper, not merely that the output metadata echoes the flag.

Implementation risk:
The current total route uses local TensorFlow tape inside the finite transport
helper.  It may fail under XLA or at material particle counts.  If so, that is
an implementation viability failure, not evidence that the total derivative is
mathematically unnecessary.

Plan status after audit:
Proceed only after Claude review of this program, the runbook, and the Phase 0
subplan converges or reaches five rounds for the same blocker.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Route And Artifact Inventory | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase0-route-inventory-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase0-route-inventory-result-2026-07-01.md` |
| 1 | Tiny GPU/XLA Full-Route Smoke | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-result-2026-07-01.md` |
| 2 | Harness Repair If Needed | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase2-harness-repair-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase2-harness-repair-result-2026-07-01.md` |
| 3 | Material Particle Ladder | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-particle-ladder-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-particle-ladder-result-2026-07-01.md` |
| 4 | HMC-Direction Diagnostic Gate | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-result-2026-07-01.md` |
| 5 | Final Decision And Next Implementation | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase5-final-decision-subplan-2026-07-01.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase5-final-decision-result-2026-07-01.md` |

## Phase Summary

### Phase 0: Route And Artifact Inventory

Freeze the target, inventory the repaired code paths, verify local artifact
presence, prove the Phase 1 selector pair reaches the total-derivative helper,
run non-GPU compile/tests, probe GPU availability in trusted context, and draft
or refresh Phase 1.

### Phase 1: Tiny GPU/XLA Full-Route Smoke

Run the smallest GPU-visible XLA manual-reverse diagnostic that uses
`transport_ad_mode="full"`.  This phase answers only whether the corrected
route can compile/run and produce finite value/gradient on the GPU.

### Phase 2: Harness Repair If Needed

If Phase 1 fails because no existing runner cleanly exercises the corrected
route, implement the smallest runner or wrapper repair.  If Phase 1 passes,
write a no-op result and skip to Phase 3.

### Phase 3: Material Particle Ladder

Run an ordered particle-count ladder, starting from `N=16` and advancing only if
the previous rung passes memory/runtime/finite-gradient gates.  Candidate rungs:
`N=16`, `N=64`, `N=256`, `N=1000` if earlier rungs are sane.

### Phase 4: HMC-Direction Diagnostic Gate

Run the SIR direction diagnostic only after Phase 3 shows the corrected route is
GPU/XLA viable.  Apply the agreed rule: pass if at least one holds:
`2 MCSE`, or `4 MCSE` with MCSE decreasing as `N` increases, or relative error
below `1%`.

### Phase 5: Final Decision And Next Implementation

Classify the route plainly:

- `GPU_XLA_VIABLE_TOTAL_DERIVATIVE_EXPERIMENTAL_ROUTE`;
- `BLOCKED_BY_XLA_OR_MEMORY`;
- `NEEDS_HAND_CODED_TOTAL_VJP`;
- `NOT_HMC_READY`;
- or another direct label supported by artifacts.

## Required Review Loop

For every material subplan and result:

1. Codex performs a skeptical audit.
2. Codex runs required local checks.
3. Codex writes a result or blocker record.
4. Codex drafts or refreshes the next subplan.
5. Claude performs bounded read-only review.
6. Fixable issues are patched visibly and rereviewed, up to five rounds for the
   same blocker.

## Forbidden Claims And Actions

- Do not call the stopped route a score for active transport.
- Do not use CPU-only evidence as GPU evidence.
- Do not treat finite gradients as HMC readiness.
- Do not change pass/fail criteria after seeing run results.
- Do not use detached supervisors, backgrounded phase runners, or copied
  workspaces in this visible runbook.
- Do not stage, commit, revert, or delete unrelated dirty worktree changes.
