# Candidate Audit: Exact Online/GPU Sinkhorn

Date: 2026-06-17

## Status

`source_reference_only`; semantic class: exact semantics / reference-only.
Execution value is `execution_value_pending`.

This lane preserves the dense entropic OT problem and the same particle
transport object, but avoids materializing the full cost/kernel/plan where
possible.  It is an engineering route for memory traffic, IO, and GPU kernels,
not a subquadratic arithmetic route.

## Paper-Note-Code-Execution Matrix

| Comparison item | Original paper | Local note | Downloaded code | Execution-value test | Required resolution |
| --- | --- | --- | --- | --- | --- |
| Problem solved | GeomLoss/KeOps-style online reductions and FlashSinkhorn-style GPU kernels solve the same entropic OT scaling problem. FlashSinkhorn expresses the log-domain row update and barycentric application for squared Euclidean costs. | Survey lines 390-435 classify this as semantics-preserving online/GPU Sinkhorn and explicitly say it does not change all-pairs asymptotic work. | FlashSinkhorn `API.md` lines 397-438 exposes shifted-potential solvers and plan-application kernels. GeomLoss `_ot_result.py` lines 7-49 defines a `LinearOperator`; lines 331-357 expose dense/lazy/operator plan routes. OTT-JAX `sinkhorn.py` lines 442-469 exposes `matrix` and `apply`. | Phase 1 dense/streaming fixtures are the comparator. First test would compare TensorFlow streaming/operator application against dense transported particles for the fixed Phase 1 fixtures. | Treat as exact-semantics reference. Do not make it a BayesFilter default unless a TensorFlow/TFP operator path is implemented and reviewed. |
| Transport object | Coupling or barycentric transport is still the entropic plan: survey equation `eq:coupling-application`; FlashSinkhorn barycentric equation `eq:flash-barycentric`. | Local note requires every scalable method to compute transported particles `Z = diag(b)^{-1} P^T X` or a row-stochastic equivalent. | FlashSinkhorn applies plan to a vector or matrix at `API.md` lines 421-436. GeomLoss wraps transport as a linear operator at `_ot_result.py` lines 7-49 and plan operator at lines 352-357. OTT-JAX applies transport at `sinkhorn.py` lines 455-469. | Returned object should be transported particles and either an exact dense matrix or `streaming_no_dense_matrix`/operator reason. | Exact plan-application orientation must match Phase 1 dense baseline before any parity claim. |
| Marginals/orientation | Standard balanced entropic plan with source and target marginals; FlashSinkhorn barycentric formula divides by source mass `a_i`. | Survey lines 380-388 state the BayesFilter coupling orientation requirement. | GeomLoss marginal routines compute both marginals via the operator at `_ot_result.py` lines 387-405. OTT-JAX `apply(..., axis=0/1)` exposes orientation control. | Row and column residuals must be recorded with transported-particle shape. | Reconcile `P X` versus `P^T X` and source/target orientation before reuse. |
| Cost/kernel/epsilon | Squared Euclidean cost admits dot-product/log-sum-exp online reductions; entropy parameter is epsilon/blur/reg depending on source. | Survey equations `eq:sqeuclidean-dot` and `eq:log-domain-update` define the local parameter map. | FlashSinkhorn names `blur`, `eps`, and `cost_scale`; OTT-JAX uses potentials and geometry; GeomLoss uses regularization parameters. | Candidate config must record epsilon/blur/cost scaling and compare to dense baseline settings. | No cost-scale parity claim until settings are mapped explicitly. |
| Approximation knob | None algorithmically; chunk size, tile size, backend, and device are implementation knobs. | Local note says this is memory/IO/GPU engineering, not a mathematical approximation. | FlashSinkhorn and GeomLoss expose backend/kernel choices rather than low-rank rank/features. | If tested, use fixed chunk/tile settings and report memory proxy and runtime only after parity. | Runtime/memory are explanatory until exact transported-particle parity passes. |
| Backend and gradients | Papers and code use PyTorch/KeOps/Triton/JAX style execution. | BayesFilter governance requires TensorFlow/TFP for BayesFilter-owned algorithmic code. | FlashSinkhorn is PyTorch/Triton; GeomLoss is PyTorch/KeOps; OTT-JAX is JAX. | No external package execution in Phase 2. Any later external run needs its own reviewed environment plan. | Non-TensorFlow sources are references or comparison targets only. |
| Execution value | Paper/library benchmarks may show memory/GPU advantages but do not answer BayesFilter value by themselves. | Local note says it preserves semantics but all-pairs arithmetic remains. | Source contains usable operator patterns but has not been run locally. | First execution-value artifact must be a BayesFilter fixture result beside Phase 1 dense/streaming diagnostics. | No ranking, no speedup, and no execution-value claim from static source inspection. |

## Source And Semantic Classification

- Source status: `source_reference_only`.
- Semantic class: exact semantics and reference-only.
- BayesFilter posture: useful design source for operator application and
  memory-aware transport; not a default implementation path.
- Required transport: transported particles plus an operator or explicit
  non-materialization reason.

## First Execution-Value Contract

Question: can an exact operator implementation reduce materialization while
matching Phase 1 dense transported particles?

Baseline/comparator: Phase 1 dense and TensorFlow streaming diagnostics in
`docs/benchmarks/scalable-ot-p01-baseline-fixture-diagnostics-2026-06-17.*`.

Primary criterion: finite transported particles, dense parity at the Phase 1
tolerance scale, matching row/column orientation, and recorded
`transport_object` or `not_materialized_reason`.

Vetoes: wrong orientation, nonfinite output, missing transported particles,
runtime-only artifact, or non-TensorFlow route treated as a BayesFilter default.

Not concluded: no subquadratic scaling, no GPU performance, no production
readiness, no ranking.

## Decision

Keep exact online/GPU Sinkhorn as a reference lane.  It may inform the Phase 3
common interface and a later TensorFlow operator refactor, but it should not be
the first subquadratic prototype because it preserves all-pairs arithmetic.
