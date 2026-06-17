# Candidate Audit: Sliced And Subspace OT

Date: 2026-06-17

## Status

`source_locked`; semantic class: semantic replacement / exploratory surrogate.
Execution value is `execution_value_pending`.

This lane projects high-dimensional measures to one-dimensional or low
dimensional problems.  It is relevant when dimension dominates the dense OT
bottleneck, but it does not automatically produce a full-state BayesFilter
coupling unless a reconstruction or resampling rule is explicitly designed.

## Paper-Note-Code-Execution Matrix

| Comparison item | Original paper | Local note | Downloaded code | Execution-value test | Required resolution |
| --- | --- | --- | --- | --- | --- |
| Problem solved | Paty-Cuturi subspace robust Wasserstein, Kolouri generalized sliced, Deshpande max-sliced, and the sliced OT survey define projection-based distances/maps. Local text files `1901.08949.txt`, `1902.00434.txt`, and `1904.05877.txt` are present. | Survey lines 892-973 define monotone 1D transport, sliced Wasserstein, empirical projection average, sorting, max-sliced objective, and the full-state warning. | POT `ot/sliced/_sliced_plans.py` lines 21-184 returns sparse per-projection plans; lines 187-260 defines min-sliced transport plan and warns about dense return under TensorFlow/JAX. | Fixed-projection diagnostic comparing projected transport consistency and downstream value, not exact dense parity. | Treat as semantic replacement unless a full-state reconstruction is designed and validated. |
| Transport object | One-dimensional monotone maps or per-projection matching plans; subspace objectives optimize over projections/subspaces. | Survey equations `eq:monotone-map`, `eq:sliced-wasserstein`, `eq:empirical-sliced`, `eq:max-sliced` define the projection objects. | POT returns per-projection plan tuples with rows/cols/data at lines 143-151 and COO-like plans at lines 152-184. | Candidate output must clearly say whether it is projected particles, averaged projection plans, a reconstructed full-state transform, or only a distance. | A distance-only output blocks BayesFilter resampling claims. |
| Marginals/orientation | Per-projection 1D OT has its own monotone matching; full high-dimensional marginal coupling is not automatic. | Local note says projected maps are not the same object as dense coupling in `R^D`. | POT `sliced_plans` handles uniform permutation plans or general 1D plans depending on weights. | Record projected residuals and any full-state reconstruction residual separately. | Do not report dense row/column residual unless a full coupling is constructed. |
| Cost/kernel/epsilon | Usually unregularized or projection-specific Wasserstein; not the same as entropic dense Sinkhorn. | Survey lines 914-965 define projection distances rather than the original Gibbs kernel. | POT sliced routines use metrics/projections, not entropic epsilon. | Candidate config must record projections, seed, metric, and reconstruction rule. | Dense Sinkhorn epsilon cannot be silently reused. |
| Approximation knob | Number and choice of projections, learned/max projection, subspace dimension, reconstruction rule. | Local expected failure mode is loss of full-state information. | POT exposes `projections`, `n_projections`, `seed`, `dense`, and metric choices. | Freeze directions for deterministic tests; later projection sensitivity is explanatory. | Random projections cannot justify ranking without replication. |
| Backend and gradients | Projection sorting can be nondifferentiable or piecewise differentiable depending on implementation. | BayesFilter default implementation must be TensorFlow/TFP. | POT is generic Python/backend-dispatched but not a BayesFilter implementation. | Phase 9 should be an exploratory TensorFlow diagnostic only after semantic replacement criteria are explicit. | No gradient or HMC-readiness claim in this phase. |
| Execution value | Literature supports scalable sliced distances, but BayesFilter needs a transport/resampling map. | Local note says it should be studied as new resampling approximation. | Source exposes per-projection plans, not a validated full-state LEDH map. | First execution-value artifact must preserve projected/full-state distinction and downstream diagnostics. | No ranking, no speedup, and no execution-value claim from static source inspection. |

## Source And Semantic Classification

- Source status: `source_locked`.
- Semantic class: semantic replacement / exploratory surrogate.
- BayesFilter posture: later exploratory lane, after exact/approximate-kernel
  candidates and common interface.
- Required transport: projected transport object or explicitly designed
  full-state reconstruction.

## First Execution-Value Contract

Question: can projection-based transport produce a meaningful, finite
resampling surrogate for high-dimensional LEDH-PFPF-OT without pretending to be
the dense entropic plan?

Baseline/comparator: Phase 1 dense/streaming baseline for descriptive semantic
delta and downstream value diagnostics, not for exact parity.

Primary criterion: fixed projection directions, finite projected transport,
explicit output semantics, and downstream diagnostic artifact.

Vetoes: distance-only result treated as transported particles, missing
reconstruction rule, silent dense-Sinkhorn parity claim, or non-TensorFlow
default route.

Not concluded: no dense OT equivalence, no posterior correctness, no default
change, no statistically supported ranking.

## Decision

Keep as a source-grounded exploratory semantic-replacement lane.  It should be
scheduled after the common interface and after the first coupling-like
prototypes because its BayesFilter transport semantics require additional
design.
