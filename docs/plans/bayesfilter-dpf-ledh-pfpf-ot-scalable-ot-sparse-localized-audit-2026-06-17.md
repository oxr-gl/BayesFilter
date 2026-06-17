# Candidate Audit: Sparse, Screened, And Localized OT

Date: 2026-06-17

## Status

`source_reference_only`; semantic class: exact semantics when certified sparse
support preserves the full OT object, approximate support restriction when
screening/truncation is used, and reference-only until locality is demonstrated.
Execution value is `execution_value_pending`.

This lane can preserve the OT object only when the active support is small or
screenable.  Its first BayesFilter question is therefore diagnostic: do the
post-flow particles have exploitable locality under the actual transport
kernel?

## Paper-Note-Code-Execution Matrix

| Comparison item | Original paper | Local note | Downloaded code | Execution-value test | Required resolution |
| --- | --- | --- | --- | --- | --- |
| Problem solved | Schmitzer sparse/multiscale OT solves exact discrete OT through sparse subproblems and shielding; Screenkhorn solves a screened approximate dual for regularized OT. | Survey lines 762-826 define sparse OT, Screenkhorn primal/dual/B matrix, and stabilization/truncation caveats. | POT `_screenkhorn.py` lines 20-120 defines Screenkhorn and returns a screened matrix; lines 405-426 builds `gamma`. Schmitzer MultiScaleOT `TSinkhornSolver.cpp` lines 321-352 generates sparse/truncated kernels and iterates Sinkhorn. MultiScaleOT source exposes sparse coupling handlers and sparse containers in search anchors. | Phase 8 should first measure dense baseline plan locality/sparsity on Phase 1/LEDH fixtures before coding a sparse prototype. | Block sparse implementation if the plan/support is not local or screenable. |
| Transport object | Sparse/multiscale methods still seek a coupling on a restricted or certified active support; Screenkhorn returns a screened transport matrix. | Local note says sparse methods are useful only if post-flow LEDH particles have genuinely local couplings. | POT returns `gamma`; Schmitzer code exposes sparse kernels/coupling containers and sparse iteration routes. | Locality diagnostic should inspect dense plan mass concentration, nearest-neighbor mass, support threshold curves, and transport error from truncation. | A sparse source implementation is not enough; the BayesFilter particle geometry must justify support restriction. |
| Marginals/orientation | Exact sparse solvers maintain marginals when support is valid; Screenkhorn approximates a constrained dual and normalizes `gamma`. | Survey lines 786-820 state screened plan must still give acceptable transport and marginal residuals. | POT `_screenkhorn.py` lines 420-426 normalizes `gamma`; Schmitzer solver updates `u` and `v` with sparse kernel products at lines 345-352. | Record residuals for any truncated/screened plan and dense-reference transported-particle error if a sparse plan is built. | Sparse truncation cannot silently drop mass. |
| Cost/kernel/epsilon | Sparse methods depend strongly on geometry, cost metric, and epsilon/truncation threshold. | Survey lines 822-826 flag stabilization and truncation for small epsilon. | Schmitzer code uses `truncation_thresh` to generate sparse kernels at lines 321-330. POT Screenkhorn takes `M`, `reg`, and budgets. | Candidate config must record threshold/budget/epsilon and dense cost settings. | Wrong threshold can produce misleading speed with invalid transport. |
| Approximation knob | Active set, shielding neighborhood, budget, truncation threshold, epsilon schedule. | Local expected failure mode is lack of locality in high-dimensional post-flow particles. | POT exposes `ns_budget`, `nt_budget`; Schmitzer exposes sparse kernel generation and refinement. | First knob diagnostic is support/mass curve, not runtime. | Runtime is irrelevant until locality and residuals pass. |
| Backend and gradients | Sparse C++/POT routes are implementation references. | BayesFilter default remains TensorFlow/TFP. | Schmitzer MultiScaleOT is C++/Python; POT is generic Python/backend-dispatched. | Any TensorFlow sparse prototype needs a later reviewed subplan. | C++/POT code is not a BayesFilter default implementation. |
| Execution value | Literature/code can be strong in low-dimensional geometry. | Local note says this lane is conditional. | Source is valid but not run locally. | First execution-value artifact is a locality diagnostic, not a sparse solver benchmark. | No ranking, no speedup, and no execution-value claim from static source inspection. |

## Source And Semantic Classification

- Source status: `source_reference_only`.
- Semantic class: exact sparse/support-restricted or screened approximation,
  conditional on locality.
- BayesFilter posture: diagnostic-first lane.
- Required transport: sparse/truncated coupling or explicit block due to lack
  of locality.

## First Execution-Value Contract

Question: do the current LEDH-PFPF-OT post-flow dense plans have enough local
support concentration to justify sparse/screened transport?

Baseline/comparator: Phase 1 dense baseline fixtures plus later LEDH-specific
fixtures.

Primary criterion: locality/support diagnostics show that a small active set
captures declared mass while preserving transported-particle output and
marginals on a tiny truncation check.

Vetoes: diffuse dense plan, invalid marginal residuals after truncation, no
transported particles, runtime-only artifact, or C++/POT source treated as
default implementation.

Not concluded: no sparse speedup, no production readiness, no default change,
no statistical ranking.

## Decision

Keep as a reference and diagnostic lane.  Do not implement sparse TensorFlow
code until a Phase 8 locality diagnostic shows the support structure exists in
the actual BayesFilter fixtures.
