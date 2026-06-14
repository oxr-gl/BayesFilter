# P49-M2 Subplan: Retained TT/SIRT Object Skeleton

metadata_date: 2026-06-09
phase: P49-M2
status: PLAN_REVIEW_CONVERGED

## Objective

Repair R2 by replacing the paper-scale all-grid retention concept with a
clean-room retained object design: density/transport object, affine map,
normalizer metadata, sample diagnostics, and replay identity.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter represent the retained filtering object without retaining all axes as a tensor-product grid? |
| Baseline/comparator | Source `SIRTs`, `L`, `mu`, `samples`, `weight`, `logmarginal_likelihood`; BayesFilter retained-grid objects. |
| Primary pass criterion | A minimal retained-object skeleton or design artifact passes shape, metadata, branch, and no-all-grid checks. |
| Veto diagnostics | Pairwise-grid propagation remains the only retained interface; retained object lacks normalizer or coordinate metadata. |
| Not concluded | No adaptive TT-cross production quality. |

## Planned Work

1. Define clean-room retained object fields and invariants.
2. Add tests or contracts that reject all-grid retention for source-faithful
   high-dimensional phases.
3. If code is implemented, keep it minimal and TF/TFP-backed.
4. Preserve fixed-branch retained grid for the gradient lane under a different
   label.

## Repair Loop

If implementation is too large for one phase, write a blocker split plan and
complete only the invariant/test skeleton first.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p49-m2-retained-transport-object-result-2026-06-09.md`
