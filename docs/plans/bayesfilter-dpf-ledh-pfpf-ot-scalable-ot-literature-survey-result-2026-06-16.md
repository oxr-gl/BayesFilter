# LEDH-PFPF-OT scalable OT literature survey result

Date: 2026-06-16

Plan:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-literature-survey-plan-2026-06-16.md`

## Research Question

Can Altschuler, Bach, Rudi, and Niles-Weed, "Massively scalable
Sinkhorn distances via the Nystrom method" (`arXiv:1812.05189`), or
nearby scalable optimal-transport methods, help with the dense OT
bottleneck in LEDH-PFPF-OT at large state dimension and large particle
count?

## Source And Tool Manifest

| Item | Status |
| --- | --- |
| Target paper PDF | downloaded: `.localsource/1812.05189.pdf` |
| Target paper text extraction | created: `.localsource/1812.05189.txt` |
| Target arXiv source bundle | downloaded: `.localsource/1812.05189` |
| Target arXiv source unpacked | `.localsource/1812.05189-src/` |
| ResearchAssistant location | `/home/ubuntu/python/ResearchAssistant`, not `~/ResearchAssistant` |
| ResearchAssistant MCP status | read-only; no local summaries for the target paper or LEDH/PFPF OT queries |
| ResearchAssistant PDF parser | usable via `scripts/ra-agent cli parse-pdf`; output was low-confidence metadata but good `pdftotext` body |
| ResearchAssistant discovery query | empty; Semantic Scholar returned 429, OpenAlex returned zero records for the combined query |
| Existing local OT audit sources | `.localsource/dpf_ot_audit/` already includes Corenflos 2021, Reich 2013, Schmitzer 2019, Cuturi 2013, Peyre-Cuturi 2019 |

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Yes, `arXiv:1812.05189` can help, but as an opt-in approximate low-rank entropic-transport lane, not as an automatic replacement for exact streaming FilterFlow-style OT. |
| Primary criterion status | Promising: it directly attacks the all-pairs Sinkhorn kernel using a factored low-rank kernel and returns a factored coupling. |
| Veto diagnostic status | No literature veto, but no implementation or filtering-validity evidence yet. |
| Main uncertainty | Effective rank may approach `N` for high intrinsic dimension, sharp small-entropy kernels, or poorly scaled post-flow clouds. |
| Next justified action | Prototype a fixed-rank TensorFlow Nystrom Sinkhorn transport on small LEDH-PFPF-OT fixtures and compare transported particles against dense/streaming exact transport. |
| What is not concluded | No posterior validity, no default-readiness, no HMC score readiness, no superiority over exact OT, no proof that large `D,N` filtering remains accurate. |

## Local Baseline

The current streaming LEDH-PFPF-OT path has already removed persistent dense
transport storage.  In the active transport branch, streaming mode returns an
empty `[B,0,0]` sentinel rather than the dense matrix and computes transported
particles directly.  The remaining bottleneck is all-pairs compute, not the
stored `[N,N]` object.

Local evidence:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  constructs dense `transport_matrix` for dense modes and computes
  `transported = transport_matrix @ x`, while streaming mode calls
  `_filterflow_streaming_transport`.
- `_filterflow_streaming_transport` still solves Sinkhorn potentials and then
  accumulates transported particles by row/column chunks.
- The `T=120` capacity note concluded that streaming OT still performs roughly
  `O(T N^2 D)` work, with `D=100,N=1000` and `D=100,N=2000` timing out in the
  tested active-all path.

## Target Paper Read

The paper's relevant object matches the LEDH-PFPF-OT resampling object more
closely than a mere scalar divergence method:

- It targets entropic OT with squared Euclidean cost by scaling
  `K = exp(-eta C)`.
- It approximates `K` by a Nystrom factorization
  `Ktilde = V A^{-1} V^T`, with matrix-vector products in `O(N r)` after
  Cholesky of the `r x r` landmark kernel.
- Sinkhorn scaling and rounding are written to operate through those
  matrix-vector products; the final coupling is returned in factored form, not
  materialized.
- The main theorem gives time roughly
  `Otilde(N r (r + eta R^4 / eps))` and space `O(N(r + d))`.
- The useful rank is governed by the Gaussian-kernel effective dimension.  The
  general ambient-dimension bound is still exponential in `d`, but the manifold
  bound depends on the intrinsic dimension `k`, not the ambient dimension.
- Experiments reported large speedups on point-cloud Sinkhorn distances,
  including comparisons against GeomLoss multiscale/annealing baselines.

For LEDH-PFPF-OT this means: if post-flow particles live near a low-intrinsic-rank
cloud and the entropy regularization is not too small, the method can reduce the
all-pairs Sinkhorn step to factor operations.  The transported particle cloud can
be formed from the factored coupling.  For example, ignoring the low-rank rounding
term for a moment,

```text
P X = D1 V A^{-1} V^T D2 X
```

can be evaluated without materializing `P`, at about `O(N r D + r^2 D)`.
The paper's rounding term is rank-one-like and similarly cheap to apply to
particles.  This is the key reason the paper is more useful for this repository
than methods that only approximate a scalar OT loss.

## Fit To LEDH-PFPF-OT

### Why It Fits

- The current transport is entropy-regularized and Sinkhorn-based, matching the
  target paper's algorithmic family.
- The current cost is squared-distance based after centering/scaling, matching
  the Gaussian-kernel setting up to the local `0.5 / epsilon` scaling.
- The filtering step needs a barycentric/ensemble transform, and the target
  paper returns a coupling in factored form, not only a value.
- The method is implementable in TensorFlow with fixed landmarks/rank and
  triangular solves, consistent with repository backend policy.

### Why It Is Not A Drop-In Default

- The target paper proves entropic OT approximation, not particle-filter
  posterior correctness.
- Its strongest scaling depends on low effective rank.  High ambient dimension
  alone is not fatal, but high intrinsic dimension or small entropy can destroy
  the advantage.
- The current FilterFlow-style path uses annealed/stabilized potentials,
  centering, scaling, uniform target marginals, and fixed-gradient behavior.
  A Nystrom lane must match those semantics or explicitly declare a new
  approximate transport object.
- Adaptive landmark sampling is random and data-dependent.  HMC/value-score
  use would require fixed seeds, fixed landmarks, or a reviewed stop-gradient
  policy.
- Entropic and low-rank bias must be validated downstream; dense parity of
  transported particles is necessary but not sufficient.

## Literature Survey

| Method family | Main use | Fit for LEDH-PFPF-OT | Ranking |
| --- | --- | --- | --- |
| Exact streaming Sinkhorn / online kernel chunks | Avoid dense storage while preserving exact dense Sinkhorn semantics | Already implemented; memory benefit only; compute still all-pairs | Baseline/reference |
| Nystrom Sinkhorn (`1812.05189`) | Low-rank Gaussian-kernel Sinkhorn with factored coupling | Best direct candidate for reducing all-pairs compute while retaining entropic coupling/transport | Prototype first |
| Positive-feature / random-feature Sinkhorn | Linear-time Sinkhorn divergence approximations | Potentially useful, and Corenflos explicitly mentions Scetbon-Cuturi as a DPF speedup route, but coupling/transport extraction must be checked | Prototype second or compare after Nystrom |
| Schmitzer stabilized sparse scaling | Log-domain stabilization, epsilon scaling, adaptive truncation, coarse-to-fine sparse kernels | Very useful if transport is local/sparse; less helpful if high-dimensional particle couplings are genuinely dense | Stabilization/sparse candidate |
| GeomLoss/Feydy online and multiscale Sinkhorn | GPU online/multiscale Sinkhorn without dense matrix storage | Conceptually close to current streaming path and Corenflos implementation; multiscale can help if geometry is low-dimensional/local | Engineering comparator |
| Greenkhorn / greedy coordinate Sinkhorn | Fewer updates in dense matrix scaling | Can reduce iterations but does not remove all-pairs kernel costs by itself | Lower priority |
| Screenkhorn / screening | Remove inactive rows/columns/candidates | Useful only if many couplings can be screened safely; transport bias likely needs careful validation | Lower priority |
| Stochastic/minibatch OT | Large-scale dual/value estimation | Good for training losses; poor direct fit for deterministic full-particle resampling because minibatch couplings bias the particle cloud | Diagnostic/training only |
| Sliced Wasserstein / projection OT | `O(L N log N)` projection-based distances/flows | Attractive at high dimension but changes the transport object; useful as alternative approximate resampling, not source-faithful FilterFlow OT | Research lane, not replacement |
| Reich ETPF and localized ETPF ideas | Particle-filter-specific deterministic OT resampling | Foundational; Reich explicitly notes high-dimensional OT is out of reach without localization.  Supports localization/blocking as a state-dimension strategy | Important design context |
| Low-rank/factored couplings | Approximate couplings via latent factors | Conceptually aligned, but less directly tied to current Sinkhorn resampling than Nystrom | Background candidate |
| State-space localization / block OT | Decompose transport by spatial/structural state blocks | Probably the strongest route for `D` scaling when model locality exists; it changes the filtering approximation and must be model-specific | Parallel design lane |

## Recommended Implementation Path

1. Add an experimental transport mode such as
   `transport_plan_mode="nystrom_low_rank"` under the existing experimental
   `annealed_transport_tf` surface.
2. Start with fixed-rank/fixed-landmark TensorFlow code, not adaptive random
   rank selection.  This keeps the branch deterministic for value/score work.
3. Implement only the same current object first:
   weighted source particles to uniform target particles, same centered/scaled
   cost, same epsilon convention, same returned transported cloud.
4. Apply the factored coupling to particles without materializing `P`:
   `D1 V A^{-1} V^T D2 X`, plus any declared rounding correction if used.
5. Validate in this order:
   dense-vs-Nystrom transported-particle parity on tiny fixtures;
   row/column marginal residuals;
   value parity on existing LEDH-PFPF-OT deterministic fixtures;
   gradient smoke only after value parity;
   scaling ladder at increasing `N,D`;
   downstream filtering/posterior diagnostics.

## Promotion And Veto Rules For A Prototype

| Diagnostic | Role |
| --- | --- |
| Non-finite potentials, factors, transported particles, or log likelihood | Hard veto |
| Dense-vs-Nystrom transported-particle error on tiny fixtures | Promotion criterion for continuing implementation |
| Marginal residuals against weighted-source/uniform-target constraints | Hard veto if outside tolerance |
| Runtime/memory at large `N,D` | Explanatory until correctness parity passes |
| Posterior/reference agreement | Required before any filtering-validity claim |
| Raw gradient vs finite-difference mismatch | Explanatory or veto only under a predeclared score contract; not a value-path veto by itself |

## What Not To Conclude

- Do not conclude that Nystrom Sinkhorn fixes high-dimensional filtering by
  itself.
- Do not treat low OT approximation error as proof of posterior validity.
- Do not rank stochastic candidates from one-seed timing or descriptive metrics.
- Do not replace the current exact streaming path as default without dense
  parity, posterior diagnostics, and gradient/HMC evidence.

## Bottom Line

`arXiv:1812.05189` is the most plausible direct scaling idea found in this
survey because it preserves the entropic Sinkhorn/coupling structure and can
produce the transported particle cloud from low-rank factors.  It should be the
first approximate-OT prototype for LEDH-PFPF-OT compute scaling.  The expected
failure mode is rank collapse: if the post-flow particle kernel is not
low-effective-rank at the chosen epsilon, the method falls back toward dense
cost.  In parallel, localized/block OT should be kept as the more model-aware
route for genuinely high-dimensional states.
