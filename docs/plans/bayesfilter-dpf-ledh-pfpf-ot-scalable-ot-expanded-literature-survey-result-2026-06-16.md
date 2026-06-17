# LEDH-PFPF-OT scalable OT expanded literature survey result

Date: 2026-06-16

Prior focused note:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-literature-survey-result-2026-06-16.md`

Expanded corpus manifest:
`.localsource/scalable_ot_survey/MANIFEST.md`

## Research Question

The dense or all-pairs optimal-transport step in LEDH-PFPF-OT is difficult to
scale when both state dimension `D` and particle count `N` are large.  Which
methods in the recent OT literature are useful for this computation, and which
combination should be studied before changing the algorithm?

The key repository-specific requirement is stronger than "compute a fast OT
distance."  LEDH-PFPF-OT needs a particle transport object: a coupling,
barycentric projection, or directly transported particle cloud that moves a
weighted empirical measure toward an equal-weight ensemble.  A paper that only
accelerates a scalar Sinkhorn divergence is useful as a diagnostic or training
loss, but is not by itself a resampling replacement.

## Evidence Contract And Skeptical Audit

| Field | Contract |
| --- | --- |
| Baseline | Current BayesFilter exact dense/streaming FilterFlow-style Sinkhorn transport in `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`. |
| Primary literature screen | Does the method reduce dense `N x N` storage or all-pairs `O(N^2 D)` work while still producing a usable transport of particles? |
| Veto diagnostics | Method returns only a scalar value; method cannot handle weighted empirical measures; method changes the filtering approximation without a declared validation ladder; method depends on a non-TensorFlow backend as an implementation default. |
| Explanatory diagnostics | Paper benchmark speedups, library maturity, GPU friendliness, differentiability, statistical sample-complexity claims. |
| What will not be concluded | No method is default-ready from literature alone; no posterior validity claim; no HMC/value-score readiness; no ranking of stochastic candidates from paper benchmarks. |
| Artifact | This result note plus `.localsource/scalable_ot_survey/MANIFEST.md`. |

Skeptical audit passed.  The expanded search corrects the main weakness of the
first pass: `1812.05189` is not the only relevant scalable-OT paper.  The
remaining risk is that recent 2025-2026 arXiv methods may evolve quickly, so
their implementation details should be rechecked against source code before
engineering work.

## Corpus Summary

Downloaded into `.localsource/scalable_ot_survey/`: 33 PDFs and 33 `pdftotext`
extractions.  The earlier target paper `1812.05189` remains in
`.localsource/1812.05189.*` with source unpacked under
`.localsource/1812.05189-src/`.

ResearchAssistant status: the local MCP adapter is read-only and returned no
stored summaries for the expanded query.  The local RA command-line tooling was
available, but this expanded pass primarily used direct downloads plus local
text extraction because the RA MCP index had no relevant local records.

## Local Baseline Diagnosis

The existing BayesFilter streaming transport already avoids materializing the
dense transport matrix in streaming mode.  It returns a `[B,0,0]` sentinel for
the transport matrix and computes transported particles by chunks.  The core
remaining bottleneck is therefore all-pairs kernel/cost computation, not only
stored `N x N` memory.

This matters because several papers solve only the storage problem or improve
iteration complexity while retaining all-pairs interactions.  Those are useful,
but they do not by themselves solve the observed large-`D`, large-`N` timeout
route.

## Method Family Classification

| Family | Representative local sources | Transport object? | Scaling help | Fit |
| --- | --- | --- | --- | --- |
| Exact online/streaming Sinkhorn | Feydy et al. 2018/GeomLoss, KeOps 2021, FlashSinkhorn 2026, FastSinkhorn 2026 | Yes | Avoids dense storage and improves GPU IO; still all-pairs per iteration | Best semantics-preserving baseline and near-term engineering lane |
| Nystrom kernel Sinkhorn | Altschuler et al. 2018/2019 target `1812.05189` | Yes, factored coupling | Replaces kernel matvec by low-rank factors if effective rank is small | Strong first approximate-kernel prototype |
| Positive-feature Sinkhorn | Scetbon and Cuturi 2020 | Mostly divergence/factored kernel; coupling extraction requires care | Linear-time kernel operations with positive features | Useful comparator; transport-map details must be verified |
| Low-rank/factored coupling OT | Forrow et al. 2018; Scetbon et al. 2021/2022/2023; Halmos et al. 2024/2025; 2026 low-rank papers | Yes, explicitly factored coupling | True subquadratic/linear memory in rank | Strongest long-term subquadratic lane, but changes feasible coupling class |
| Sparse/stabilized/screened Sinkhorn | Schmitzer 2015/2019; Screenkhorn 2019 | Yes, if retained support is valid | Reduces active pairs when geometry is local/screenable | Useful if post-flow clouds have locality; high-dimensional concentration may weaken it |
| Accelerated/greedy Sinkhorn | Greenkhorn; APDAGD/APDAMD; Acc-Sinkhorn 2026 | Yes, but dense unless combined with online/low-rank backend | Improves iterations or accuracy dependence | Secondary; combine with backend after object is chosen |
| Stochastic/minibatch OT | Genevay 2016; BoMb-OT; partial minibatch OT | Sometimes local plans, not full deterministic plan | Reduces memory/compute by sampling | Not direct resampling replacement without new filtering theory |
| Sliced/projection/subspace OT | generalized/max-sliced, Paty-Cuturi subspace robust, 2025 sliced survey | Usually projected transports or distances | `O(L N log N)` style alternatives; better high-dimensional statistics | Research lane; changes transport object |
| Particle-filter-specific OT/localization | Reich ETPF, Corenflos differentiable OT resampling | Yes | Mostly context; high-dimensional route often needs localization | Important design constraint, not enough alone |

## Paper-Level Findings

### Exact or near-exact all-pairs semantics

FlashSinkhorn (`2602.03067`) is important because it attacks the exact bottleneck
from the systems side.  It rewrites stabilized log-domain Sinkhorn updates for
squared Euclidean costs as attention-like log-sum-exp reductions, streams tiles
through GPU SRAM, avoids `N x N` intermediates, and includes streaming transport
application.  This is probably the closest paper to our current streaming code,
but with much stronger GPU kernel engineering.  It is semantics-preserving for
entropic OT, but still all-pairs work per iteration.

Fast Log-Domain Sinkhorn (`2605.00837`) is similar in spirit: a native CUDA
log-domain implementation with warp-level reductions and shared-memory tiling.
It supports the view that our current TensorFlow streaming implementation is an
algorithmic baseline, not an optimized GPU kernel.

KeOps (`2004.11127`) and GeomLoss/Feydy (`1810.08278`) are mature references
for online kernel reductions with autodiff and memory efficiency.  They are not
TensorFlow-native defaults for this repo, but they are useful for algorithmic
and benchmark design.

Conclusion for this family: this is the correctness-preserving engineering
lane.  It should remain the reference path and a strong benchmark.  It will not
give true subquadratic asymptotics unless combined with sparsity, low-rank
factors, or locality.

### Low-rank kernel Sinkhorn

The original target paper, `1812.05189`, remains a strong candidate because it
approximates the Gaussian Gibbs kernel by a Nystrom factorization
`K ~= V A^{-1} V^T`, runs Sinkhorn through low-rank matvecs, and returns a
factored coupling.  The transported cloud can be computed without materializing
`P`; schematically, `P X = D1 V A^{-1} V^T D2 X`, plus any rounding correction.

The main caveat is unchanged: low-rank kernel Sinkhorn is only useful if the
effective kernel rank stays much smaller than `N`.  High intrinsic dimension,
small entropy, or badly scaled post-flow particles can collapse the advantage.

Positive-feature Sinkhorn (`2006.07057`) attacks the same matvec bottleneck
from a different angle: choose a positive feature map so the Sinkhorn kernel is
an inner product in `R^r_+`, giving `O(Nr)` iterations.  This may be more stable
than arbitrary low-rank approximations because positivity is built in.  However,
the paper is framed around Sinkhorn divergences and learned/kernel features;
before using it for resampling, we must verify how to apply the resulting
factored kernel/coupling to particles and how feature approximation bias affects
the ensemble transform.

Conclusion for this family: best first approximate-kernel experiment after an
exact online baseline.  Start deterministic, fixed-rank, fixed-landmark/feature,
and compare transported particles against dense exact OT.

### Low-rank coupling OT

The low-rank coupling literature is now much broader than the original Nystrom
paper:

- Forrow et al. (`1806.07348`) introduce factored couplings and argue that low
  transport rank improves high-dimensional statistical behavior.
- Scetbon-Cuturi-Peyre (`2103.04737`) solve OT over couplings constrained by
  nonnegative rank, rather than only approximating the Sinkhorn kernel.
- Scetbon-Cuturi (`2205.12365`) study approximation, statistics, and debiasing
  for low-rank OT.
- Scetbon et al. (`2305.19727`) extend low-rank solvers to unbalanced OT.
- Halmos et al. (`2411.10555`) propose factor relaxation with latent coupling,
  with linear space complexity and support for several OT variants.
- Halmos et al. (`2503.03025`) combine low-rank OT with hierarchical
  refinement to recover high-resolution assignments.
- 2026 papers (`2603.03578`, `2606.12120`) improve optimization routes through
  transport clustering and Riemannian low-rank geometry.

This family is highly relevant because it returns couplings and attacks the
quadratic coupling itself, not only storage.  It is also a more radical
algorithmic change than Nystrom Sinkhorn: the feasible set is now low-rank
couplings, so the filter is no longer solving the same entropic transport
problem.  That may be a virtue in high dimension, but it must be declared as a
new approximate resampling method and validated downstream.

Conclusion for this family: strongest long-term scaling lane.  It should be
studied in parallel with Nystrom/Flash-style Sinkhorn, not treated as a silent
replacement for FilterFlow-style OT.

### Sparse, screened, and multiscale OT

Schmitzer's sparse multiscale (`1510.05466`) and stabilized sparse scaling
(`1610.06519`) papers are directly relevant if the true coupling is local.
They combine log-domain stabilization, epsilon scaling, adaptive truncation,
and coarse-to-fine sparsification.  Screenkhorn (`1906.08540`) screens dual
components to reduce the Sinkhorn problem.

This route is attractive when LEDH has already moved particles close enough
that transport should be local.  It may fail in high dimension if nearest
neighbor structure is unstable or if the coupling remains diffuse due to
entropy.

Conclusion for this family: useful as an exact/near-exact sparse candidate and
as a stabilization toolbox.  It should be benchmarked after we inspect
post-flow coupling locality.

### Acceleration without removing all-pairs work

Greenkhorn (`1705.09634`), greedy stochastic Sinkhorn (`1803.01347`),
accelerated gradient / mirror descent (`1802.04367`, `1901.06482`), and
Acc-Sinkhorn (`2605.30267`) improve iteration complexity or convergence
behavior.  They are valuable, especially for smaller epsilon, but they do not
remove the dense kernel/cost bottleneck unless paired with an online, sparse,
or low-rank backend.

Conclusion for this family: not first-line for our observed scaling problem.
Use these only after deciding the backend representation.

### Stochastic and minibatch OT

Genevay et al. (`1605.08527`) and the minibatch/BoMb/POT papers
(`2102.05912`, `2108.09645`) are important for large-scale ML losses and
training.  They reduce memory by solving many smaller problems or optimizing
dual objectives from samples.  For particle resampling, that is dangerous:
mini-batch couplings can create mappings that are optimal inside small batches
but wrong for the full ensemble.  The papers themselves discuss misspecified
mappings and corrections.

Conclusion for this family: useful for diagnostics, training losses, or
possible randomized resampling research.  Not a direct LEDH-PFPF-OT replacement
without a new filtering argument and posterior validation.

### Sliced, projection, and subspace robust OT

Generalized/max-sliced Wasserstein (`1902.00434`, `1904.05877`), Paty-Cuturi
subspace robust Wasserstein (`1901.08949`), and the 2025 sliced OT survey
(`2508.12519`) address the high-dimensional curse by projecting to lower
dimensional problems.  These methods can be much cheaper and statistically
better behaved.  The 2025 survey is useful because it now covers sliced
transport plans, barycenters, gradient flows, unbalanced/partial variants, and
extensions beyond simple random one-dimensional projections.

For LEDH-PFPF-OT, this is not the same transport object.  A sliced or subspace
transport could be an excellent new resampling method if we accept an
approximation inspired by high-dimensional geometry.  It should not be sold as
faithful dense Sinkhorn acceleration.

Conclusion for this family: important research lane, especially when state
dimension is the dominant issue.  It needs its own filtering validation plan.

### Particle-filter-specific context

Reich's ensemble transform particle filter and Corenflos et al.'s
differentiable OT resampling confirm that OT-based resampling is a reasonable
particle-filter object, but also reinforce the high-dimensional warning.
Reich-style localization/blocking is likely complementary to all numerical OT
accelerations.  If the state has spatial or structural locality, block/local OT
may be the most robust `D`-scaling idea.

Conclusion for this family: keep localization/block transport as a parallel
model-aware design lane.  It is probably the most principled answer to truly
high-dimensional state spaces when model locality exists.

## Recommended Strategy Before Implementation

Do not choose a single paper yet.  Use a three-lane plan:

1. Exact online/GPU semantics-preserving lane.
   Study FlashSinkhorn/KeOps-style tiling against our current streaming
   TensorFlow path.  This is the correctness reference and near-term scaling
   benchmark.  It preserves the current entropic OT object but remains all-pairs.

2. Approximate low-rank entropic lane.
   Prototype deterministic fixed-rank Nystrom Sinkhorn first, then compare
   positive-feature Sinkhorn.  These preserve Sinkhorn-style scaling and can
   apply a factored coupling to particles.  Key diagnostics are effective rank,
   marginal residuals, and transported-particle parity.

3. Structural approximate coupling lane.
   Study low-rank coupling OT and possibly sliced/subspace/localized OT as new
   resampling methods.  These may be the only route to genuine large-`N,D`
   scaling, but they change the transport approximation and require posterior
   validation, not only dense OT parity.

## Prototype Priority

| Priority | Candidate | Why |
| --- | --- | --- |
| 0 | Keep exact streaming/dense as reference | Needed for parity and vetoes |
| 1 | Flash/online exact Sinkhorn benchmark or design note | Preserves semantics; reveals how much is engineering vs algorithm |
| 2 | Fixed-rank Nystrom Sinkhorn transport | Directly applies factored entropic coupling to particles |
| 3 | Positive-feature Sinkhorn transport check | Potentially stable linear-time kernel route |
| 4 | Sparse/stabilized truncation after locality audit | Good if LEDH post-flow clouds are local |
| 5 | Low-rank coupling OT experimental resampler | Strong scaling, but changes feasible coupling class |
| 6 | Sliced/subspace/localized transport | High-dimensional research lane, not drop-in |
| 7 | Minibatch/stochastic OT | Diagnostics/training only unless new filtering theory is written |

## Validation Ladder For Any Candidate

1. Small deterministic dense parity: transported particles, not only OT value.
2. Marginal residuals: weighted source and uniform target constraints.
3. Non-finite and positivity checks.
4. Effective rank, sparsity, or projection diagnostics, depending on method.
5. LEDH-PFPF-OT value parity on existing fixtures.
6. Gradient smoke only after value parity.
7. Runtime and memory ladder over `N,D`.
8. Downstream posterior/reference diagnostics.
9. Multi-seed or uncertainty-aware comparison before any ranking claim.

## Decision Table

| Field | Decision |
| --- | --- |
| Can `1812.05189` help? | Yes, but it is one member of a broader low-rank kernel family. |
| Most semantics-preserving path | Flash/online exact Sinkhorn style, plus current streaming reference. |
| Most plausible subquadratic path | Low-rank kernel Sinkhorn first; low-rank coupling OT second as a structural approximation. |
| Best high-dimensional state strategy | Combine numerical OT acceleration with localization/blocking or subspace/sliced ideas when model structure supports it. |
| Main risk | Replacing full-particle resampling by a fast scalar or minibatch approximation that does not transport the ensemble correctly. |
| Default-readiness | No candidate is default-ready from literature alone. |

## What To Ask The User For

No blocking papers remain for this first expanded survey.  For a deeper
second-pass survey or implementation plan, useful user-provided sources would
be:

- the Lin et al. 2021 latent-coupling / k-Wasserstein barycenter paper cited by
  Halmos et al. 2024, if the user wants the FRLC antecedent fully traced;
- any author code or benchmark scripts for FlashSinkhorn, low-rank OT, or FRLC
  that the user wants treated as implementation anchors;
- any LEDH-PFPF-OT paper/source-specific constraints that require preserving a
  particular resampling semantics beyond generic entropic OT.

## Bottom Line

The useful literature is now clearly broader than Nystrom Sinkhorn.  The best
engineering posture is to keep exact online Sinkhorn as the reference, prototype
Nystrom/positive-feature factored Sinkhorn as the first approximate entropic
transport lane, and study low-rank coupling or sliced/localized transport as
explicit new resampling methods rather than silent accelerations.  For large
`D,N`, a combination is likely needed: GPU-online exact transport for reference
and moderate sizes; low-rank factors when the post-flow kernel has small
effective rank; localization or low-rank coupling when the state/particle
geometry has real structure.
