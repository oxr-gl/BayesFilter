# Candidate Audit: Nystrom Kernel Sinkhorn

Date: 2026-06-17

## Status

`source_locked`; semantic class: approximate kernel.  Execution value is
`execution_value_pending`.

This lane approximates the Gibbs kernel used by entropic Sinkhorn.  It can
preserve the scaling structure and expose efficient transported-particle
application, but it is only useful when the post-flow kernel has low effective
rank under the selected entropy/cost scale.

## Paper-Note-Code-Execution Matrix

| Comparison item | Original paper | Local note | Downloaded code | Execution-value test | Required resolution |
| --- | --- | --- | --- | --- | --- |
| Problem solved | Altschuler et al. approximate `K_ij = exp(-eta ||x_i-x_j||^2)` by Nystrom factors. Source TeX lines 17-27 define `V`, `A`, triangular solves, and `O(nr)` matvecs. Lines 121-172 define adaptive doubling and the diagonal error. | Survey lines 437-545 give `K`, `Ktilde = V A^{-1} V^T`, matvec, plan, transport, rank bounds, marginal residual, and transported-particle error. | POT `ot/lowrank.py` lines 530-587 implements `kernel_nystroem`; lines 590-730 implement `sinkhorn_low_rank_kernel`. POT `_empirical.py` lines 766-865 wraps empirical Nystrom Sinkhorn and returns a lazy plan. LinearSinkhorn `FastSinkhorn.py` lines 197-260 implements `Nys_Sinkhorn`/`Nys_Sinkhorn_RBF`. | Tiny fixed-landmark fixture against Phase 1 dense baseline, then high-dimensional low-rank/locality fixtures. | Implement as approximate-kernel lane; do not claim exact dense Sinkhorn equivalence unless the approximation error is measured. |
| Transport object | Approximate plan is `Ptilde = D1 V A^{-1} V^T D2`; transport is `D1 V A^{-1} V^T D2 X`. | Survey equations `eq:nystrom-plan` and `eq:nystrom-transport` make transport application explicit. | POT returns low-rank factors and a lazy plan; LinearSinkhorn source mostly returns scaling vectors and scalar traces. | Candidate result must include transported particles, scaling vectors/factors, marginal residuals, and dense-reference transported-particle error. | The BayesFilter wrapper must expose transport application, not only a Sinkhorn cost. |
| Marginals/orientation | Approximate scaling targets the same source/target histograms. Stability statement controls marginal residual in survey equation `eq:nystrom-marginal-residual`. | Local note requires row/column residuals and transported-particle error. | POT low-rank kernel code checks one marginal residual at `lowrank.py` lines 696-707 and stores lazy plan at lines 720-727. | Record row and column residuals using Phase 1 orientation. | Reconcile transposes and whether source/target samples are symmetric or rectangular. |
| Cost/kernel/epsilon | Paper uses Gaussian kernel with eta; POT uses sigma with `exp(-dist/(2 sigma^2))`; local dense baseline uses entropy epsilon/reg. | Survey equations `eq:nystrom-kernel` and `eq:nystrom-factors` define the map. | POT `_empirical.py` lines 845-847 maps `reg` to `sigma=(reg/2)**0.5`. LinearSinkhorn takes `reg`. | Candidate config must record epsilon/reg/sigma/eta mapping. | Parameter mismatch is a hard blocker for parity claims. |
| Approximation knob | Rank/anchors/landmarks; adaptive doubling uses diagonal error `1 - min_i Ktilde_ii`. | Survey equations `eq:nystrom-diag-error`, `eq:nystrom-ball-rank`, and `eq:nystrom-manifold-rank` describe failure and favorable cases. | POT uses `anchors`; LinearSinkhorn uses `rank` and seed. | Freeze landmarks/rank/seed for deterministic tests; later sensitivity over rank is explanatory. | Random landmark choices cannot decide defaults without uncertainty-aware evidence. |
| Backend and gradients | Paper method is backend independent. | BayesFilter implementation must be TensorFlow/TFP. | POT is backend-dispatched but not BayesFilter-owned TF integration; LinearSinkhorn is NumPy/PyTorch-style research code. | Phase 4 should implement a TensorFlow fixed-rank port or use sources only as reference. | Non-TF code is reference/comparator unless a reviewed exception exists. |
| Execution value | Paper complexity is favorable when `r << n`; rank bounds can be bad in high ambient dimension. | Local note states it can help only if effective rank is small and entropy is not too sharp. | Code availability shows implementability, not runtime in this repo. | First execution value requires finite transported particles and dense-reference diagnostics on Phase 1 fixtures. | No ranking, no speedup, and no execution-value claim from static source inspection. |

## Source And Semantic Classification

- Source status: `source_locked`.
- Semantic class: approximate kernel.
- BayesFilter posture: first strong candidate for a TensorFlow fixed-rank
  prototype after Phase 3 harness.
- Required transport: factored approximate plan and transported particles.

## First Execution-Value Contract

Question: can fixed-rank Nystrom Sinkhorn reproduce the dense/streaming
transport closely enough on deterministic fixtures while reducing materialized
`N x N` objects?

Baseline/comparator: Phase 1 dense TensorFlow transport and streaming parity
fixtures.

Primary criterion: finite transported particles, row/column residuals within a
declared tolerance, and dense-reference transported-particle error reported for
each rank.

Vetoes: nonpositive/NaN factors, marginal residual blow-up, wrong epsilon map,
missing transported-particle result, or treating rank-source availability as
execution value.

Not concluded: no general high-dimensional scalability, no default change, no
posterior correctness, no statistical ranking.

## Decision

Advance Nystrom to the Phase 3 harness design and Phase 4 prototype planning as
an approximate-kernel candidate.  Rank selection and landmark freezing are part
of the experimental contract, not a default policy.
