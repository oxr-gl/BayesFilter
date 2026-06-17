# Phase 0 Result: Scalable OT Source Lock

Date: 2026-06-17

## Status

`PHASE_0_SOURCE_LOCK_PASSED_WITH_MINIBATCH_SOURCE_BLOCKER`

## Phase Objective

Lock the paper, note, downloaded-code, and first execution-value comparison
requirements for scalable OT candidates before implementing a master test
harness for LEDH-PFPF-OT.

This phase is a static source audit.  It does not rank algorithms empirically.
Execution value is still pending until Phase 1 fixtures and candidate runs are
recorded against the current TensorFlow dense/streaming baseline.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Do we have enough paper, note, and source-code material to design a master program that tests scalable OT schemes for LEDH-PFPF-OT? |
| Baseline/comparator | Current TensorFlow FilterFlow-style annealed transport in `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`; dense mode materializes `[B,N,N]`, streaming mode applies transport without returning a dense matrix. |
| Primary criterion | Each candidate lane has paper anchors, local survey anchors, downloaded code anchors, source status, implementation posture, and a first execution-value test. |
| Hard vetoes | Missing usable transport object; source checkout invalid for decision-grade use; paper-note-code mismatch not declared; non-TensorFlow code treated as BayesFilter default implementation; execution value inferred from GitHub validity alone. |
| Explanatory diagnostics | Backend maturity, returned object, API style, likely implementation effort, and first fixture to run. |
| Not concluded | No candidate is ranked by performance; no production default is changed; no downstream filter accuracy or HMC readiness is established. |

## Skeptical Plan Audit

The Phase 0 source-lock plan passes this audit because it does not run a proxy
benchmark or promote source availability into correctness.  The current dense
and streaming TensorFlow transport is the declared comparator, and every
candidate row below separates static evidence from future execution evidence.

Known limits:

- ResearchAssistant local paper summaries returned no matches for the OT query,
  so this artifact uses the downloaded `.localsource` paper/text/source corpus
  plus the local survey paper.
- Mini-batch/BoMb code is only partial/incomplete and is therefore blocked for
  decision-grade use until the user supplies a clean source archive or a later
  successful retry produces a clean checkout.
- Non-TensorFlow repositories are source/reference material unless a reviewed
  exception is written.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `70ab32644cedeb95d4b56e096448f3bb2c908763` |
| Timestamp | `2026-06-17T12:04:04+08:00` |
| Commands used | `sed`, `rg`, `nl`, `git rev-parse HEAD`, `date -Is`, ResearchAssistant `ra_find_paper` |
| Environment | Documentation/source audit only; no TensorFlow/GPU execution |
| CPU/GPU status | N/A |
| Seeds | N/A |
| Output artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-source-lock-result-2026-06-17.md` |
| Master program | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-code-master-program-2026-06-17.md` |
| Survey note | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` |
| Code manifest | `.localsource/scalable_ot_code_audit/MANIFEST.md` |

## Governing Source Corpus

| Corpus item | Path | Source-lock role |
| --- | --- | --- |
| Literature manifest | `.localsource/scalable_ot_survey/MANIFEST.md` | Downloaded paper corpus and missing-source ledger. |
| Self-contained survey paper | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` | Local note tying paper equations to LEDH-PFPF-OT requirements. |
| Code audit manifest | `.localsource/scalable_ot_code_audit/MANIFEST.md` | Downloaded repository status, commits, and reuse risks. |
| Current BayesFilter transport baseline | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py` | TensorFlow dense/streaming comparator for execution-value tests. |
| Current batched filter integration | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`; `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py` | Downstream value-recursion integration target. |

## Source-Lock Table

| Candidate | Original paper anchor | Local note anchor | Downloaded code anchor | Source status | Implementability | First execution-value test | Non-claims |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Dense/streaming exact baseline | Cuturi Sinkhorn; Corenflos differentiable OT resampling; Reich ensemble transform. Entropic plan has `P = diag(u) K diag(v)` and transport application `Z = diag(b)^{-1} P^T X`. | Survey lines 360-388 define Gibbs scaling, Sinkhorn updates, and particle transport requirement. | `annealed_transport_tf.py` lines 16-38 define `AnnealedTransportTFResult` and public wrapper; lines 94-101 distinguish dense vs streaming sentinel; lines 229-245 select streaming transport; lines 682-852 implement streaming transport application. FilterFlow code at `.localsource/.../filterflow/.../plan.py` lines 13-43 returns dense matrix. | `source_locked` | Already TensorFlow/TFP. It is the oracle/baseline, not a scaling solution. | Phase 1 tiny deterministic, LGSSM-style, and high-dimensional synthetic fixtures in dense and streaming modes; record row/column residuals, finite checks, transported particles, runtime, and memory proxy. | Does not solve all-pairs arithmetic; streaming avoids dense matrix storage but still computes pairwise reductions. |
| Exact online/GPU Sinkhorn | GeomLoss/KeOps and FlashSinkhorn preserve exact entropic Sinkhorn semantics while streaming reductions; FlashSinkhorn also states barycentric application `T_epsilon(x_i) = a_i^{-1} sum_j P^*_{ij} y_j`. | Survey lines 390-435 classify this as semantics-preserving memory/IO/GPU engineering that does not change all-pairs asymptotic work. | GeomLoss `src/geomloss/ot/_ot_result.py` lines 7-49 define a linear operator; lines 243-259 cache `plan`, `lazy_plan`, `plan_operator`; lines 329-357 expose plan/operator route. FlashSinkhorn `API.md` lines 421-436 documents `apply_plan_vec_flashstyle` and `apply_plan_mat_flashstyle`. OTT-JAX `sinkhorn.py` lines 442-469 exposes `matrix` and `apply`. | `source_reference_only` | TensorFlow port/operator refactor possible; PyTorch/KeOps/Triton/JAX code is reference/comparison only. | Compare local streaming TensorFlow plan application against dense baseline for fixed `N,D`; then optionally run external reference only if environment/dependency plan is approved. | Not subquadratic in pairwise arithmetic; source validity is not evidence of BayesFilter speedup. |
| Nystrom kernel Sinkhorn | Altschuler et al. 1812.05189. Kernel approximation `K_ij = exp(-eta ||x_i-x_j||^2)`, `Ktilde = V A^{-1} V^T`; transport application `Ptilde X = D1 V A^{-1} V^T D2 X`; rank bounds depend on intrinsic structure. | Survey lines 437-545 give equations for Nystrom kernel, factors, matvec, plan, transport, diagonal approximation error, marginal residual, and transported-particle error. | `.localsource/1812.05189-src/sections/nystrom.tex`; `.localsource/1812.05189-src/sections/sinkhorn.tex`; LinearSinkhorn `FastSinkhorn.py` lines 197-260 implement `Nys_Sinkhorn` and `Nys_Sinkhorn_RBF`; POT `ot/lowrank.py` lines 530-587 implements `kernel_nystroem`, lines 590-729 implements `sinkhorn_low_rank_kernel`; POT `_empirical.py` lines 766-971 exposes empirical Nystrom Sinkhorn wrappers. | `source_locked` | TensorFlow fixed-rank port is feasible and should freeze landmarks/rank for deterministic tests. POT/LinearSinkhorn are reference implementations. | Tiny dense parity with fixed landmarks and rank; compare transported particles, marginal residuals, and low-rank matvec against dense baseline. Then scale rank/features across high-dimensional synthetic rank/locality fixtures. | A favorable Nystrom result would show viability under tested rank/epsilon only; it would not prove high-dimensional scalability in general. |
| Positive-feature Sinkhorn | Scetbon and Cuturi positive-feature Sinkhorn. Kernel is replaced by `k_theta(x,y)=<phi_theta(x),phi_theta(y)>`; transport uses `P X = diag(u) xi^T zeta diag(v) X`. | Survey lines 546-624 define positive features, kernel/cost replacement, dual objective, finite features, and transport application, with semantic warning. | LinearSinkhorn `FastSinkhorn.py` lines 77-135 implement low-rank feature Sinkhorn scaling/cost traces; lines 139-161 implement Gaussian positive feature map; `EXP_GAN/torch_lin_sinkhorn.py` is an additional PyTorch scalar-cost source. | `source_locked` | TensorFlow port feasible for a deterministic fixed-feature comparator. Source API is research-script style and must be adapted. | Fixed-feature tiny parity against dense reference and Nystrom; report marginal residuals, transported-particle error, feature count, finite checks, and runtime. | Positive features change the cost/kernel; success is not exact dense-Sinkhorn equivalence unless approximation error is separately controlled. |
| Direct low-rank coupling OT | Forrow factored couplings; Scetbon low-rank Sinkhorn factorization. Coupling is constrained as `P = Q diag(1/g) R^T` with transport `P X = Q diag(1/g) R^T X`. | Survey lines 628-760 define nonnegative-rank, low-rank coupling set, factored coupling constraints, objective, transport application, latent coupling extension, and rank diagnostics. | POT `ot/lowrank.py` lines 322-527 implements `lowrank_sinkhorn`, returning `Q,R,g` and `lazy_plan`; OTT-JAX `sinkhorn_lr.py` lines 153-248 exposes `LRSinkhornOutput.matrix`, `apply`, marginals, and mass; POT `ot/factored.py` lines 17-157 implements factored OT and returns low-rank lazy plan. | `source_locked` | TensorFlow port/prototype feasible as a declared semantic replacement, not as a dense-Sinkhorn approximation. | Tiny factorized-coupling fixture with `rank < N`; verify finite `Q,R,g`, marginal residuals, transported particles, and compare to dense as descriptive semantic delta. | Dense-reference error is explanatory, not a hard veto, because this lane solves a different constrained problem. |
| Sparse/screened/multiscale OT | Schmitzer sparse/multiscale and Screenkhorn reduce active support or variables when locality/screening holds. | Survey lines 762-826 define sparse OT, Screenkhorn primal/dual/B matrix, and stabilization/sparse-scaling caveats. | Schmitzer MultiScaleOT `src/Sinkhorn/TSinkhornSolver.cpp`, `src/ShortCutSolver/TShortCutSolver.cpp`, `src/ShortCutSolver/MultiScaleSolver.cpp`; POT `ot/bregman/_screenkhorn.py`; manifest records valid C++/Python inspected checkout. | `source_reference_only` | Locality diagnostic first; TensorFlow sparse prototype only if post-flow coupling is actually local or screenable. C++ code is algorithmic reference. | Measure dense baseline plan locality/sparsity on LEDH-PFPF-OT fixtures before coding. If no locality, block sparse prototype. | Sparse source code does not imply high-dimensional LEDH particles have exploitable local support. |
| Sliced/subspace OT | Paty-Cuturi subspace OT; Kolouri generalized sliced; Deshpande max-sliced; recent sliced OT survey. These project to 1D/subspace transports and generally change the object. | Survey lines 892-973 define monotone 1D transport, sliced Wasserstein, empirical projection average, sorting, max-sliced objective, and warning about mapping back to full state. | POT `ot/sliced/_sliced_plans.py` lines 21-184 returns sparse COO-like plans per projection; lines 187 onward define min-sliced transport plan. | `source_locked` | TensorFlow projection diagnostic feasible; full BayesFilter resampling route is exploratory semantic replacement. | Projection fixture with fixed directions; compare projected transport consistency and downstream LGSSM value as exploratory diagnostics, not dense parity. | Does not provide a full-state dense coupling unless an explicit reconstruction is designed and validated. |
| Mini-batch / BoMb OT | Nguyen BoMb-OT and partial mini-batch OT solve minibatch/hierarchical or unbalanced local problems; object differs from a single full deterministic coupling. | Survey lines 847-890 define stochastic/minibatch caveat, BoMb objective, finite minibatch cost construction, unbalanced local objective, and replacement warning. | `.localsource/scalable_ot_code_audit/Mini-batch-OT-sparse/ABC/utils.py` lines 11-36 implement `mOT`; lines 39-65 implement `BoMbOT`; checkout recorded partial/incomplete in manifest. | `source_partial_user_needed` | Blocked for decision-grade implementation until clean source/archive. Concept-only diagnostic possible with explicit user approval. | No decision-grade execution test yet. If source is fixed, first run should inspect whether minibatch code can construct a reproducible full-particle transport or only a scalar/hierarchical cost. | Do not infer viability from partial source; do not treat minibatch scalar costs as a resampling map. |

## Paper-Note-Code-Execution Gate Outcomes

| Candidate | Problem solved | Transport object in source | BayesFilter execution-value gate | Phase 0 decision |
| --- | --- | --- | --- | --- |
| Dense/streaming baseline | Same FilterFlow-style annealed regularized transport used locally. | Dense matrix in dense mode; streamed transported particles in streaming mode. | Required Phase 1 comparator. | `source_locked`, keep as oracle. |
| Exact online/GPU | Same entropic OT semantics, optimized implementation. | Lazy/operator/plan-application routes in GeomLoss, FlashSinkhorn, OTT-JAX. | Useful if we need memory/IO improvement without semantic change. | `source_reference_only`, not first subquadratic lane. |
| Nystrom Sinkhorn | Approximate Gibbs kernel Sinkhorn. | Low-rank kernel factors, scaling vectors, lazy plan routes. | Candidate lane worth baseline-gated testing as an approximate-kernel prototype. | `source_locked`, not yet ranked. |
| Positive-feature Sinkhorn | Feature-approximated cost/kernel Sinkhorn. | Feature factors and scaling routines, mostly scalar-cost scripts. | Candidate feature-kernel lane worth baseline-gated testing; must declare changed kernel. | `source_locked`, not yet ranked. |
| Direct low-rank coupling | Rank-constrained/factored coupling OT. | `Q,R,g`, lazy plan, `apply` in OTT-JAX. | Candidate semantic-replacement lane worth baseline-gated testing. | `source_locked`, not yet ranked. |
| Sparse/localized | Sparse/screened exact or regularized OT if active support is small. | Sparse C++ solvers and Screenkhorn reference. | Requires locality diagnostic before implementation. | `source_reference_only`, conditional. |
| Sliced/subspace | Projection-based OT/surrogate. | Per-projection sparse plans. | Exploratory downstream-value diagnostic only. | `source_locked`, semantic-replacement lane. |
| Mini-batch/BoMb | Hierarchical/minibatch OT cost, not necessarily a full plan. | Partial local source only; visible functions return scalar costs. | Blocked until clean source and transport-object audit. | `source_partial_user_needed`. |

## Do We Have Enough Material For A Master Test Program?

Yes, for a staged master program that begins with baseline-gated tests:

1. Phase 1 baseline fixture contract for dense and streaming TensorFlow
   transport.
2. Candidate audit notes for Nystrom, positive-feature, low-rank coupling,
   exact online/GPU, sparse/localized, sliced/subspace, and Mini-batch/BoMb.
3. Common transport-result schema requiring particles, transport object or
   explicit non-materialization reason, diagnostics, source route, and run
   manifest.
4. TensorFlow test candidates for fixed-rank Nystrom and positive-feature
   Sinkhorn after the baseline fixture gate passes.
5. A declared semantic-replacement prototype for direct low-rank coupling.

Not yet, for a decision-grade Mini-batch/BoMb implementation.  The visible code
is insufficiently clean and appears oriented toward scalar/hierarchical costs in
the inspected files.  The user should provide a clean archive/source if this
lane is to influence algorithm selection.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PHASE_0_SOURCE_LOCK_PASSED_WITH_MINIBATCH_SOURCE_BLOCKER` | Paper, note, and downloaded-code anchors are sufficient for all lanes except decision-grade Mini-batch/BoMb. | No veto for baseline, exact online/GPU reference, Nystrom, positive features, low-rank coupling, sparse reference, or sliced/subspace. Mini-batch/BoMb has a source blocker. | Execution value remains unmeasured; external libraries have not been installed or run; code anchors are source-read evidence only. | Begin Phase 1 baseline fixture contract and candidate audit notes; ask user for clean Mini-batch/BoMb source if that lane should remain active. | No empirical ranking, no production default, no posterior correctness, no statistically supported comparison. |

## Post-Run Red Team

Strongest alternative explanation: Nystrom and positive-feature lanes may look
attractive in source form but fail when the LEDH post-flow Gibbs kernel has high
effective rank, small entropy, or poor feature approximation in high dimension.

What would overturn this phase decision: Phase 1 discovers that the current
dense/streaming TensorFlow baseline is not deterministic or cannot provide the
diagnostics needed for candidate comparison.

Weakest evidence link: static source inspection does not prove any external
repository runs in the current environment or that its API behavior matches the
documentation.  That must be tested only after a reviewed execution plan.

## Next Phase

Write and execute the Phase 1 baseline fixture contract.  The first fixture
artifact must record dense and streaming TensorFlow outputs before any candidate
is compared or ranked.
