# Scalable Optimal Transport for LEDH-PFPF-OT: A Self-Contained Literature Survey

Date: 2026-06-16

Local source corpus:
`.localsource/scalable_ot_survey/MANIFEST.md`,
`.localsource/1812.05189.pdf`,
`.localsource/1812.05189.txt`,
`.localsource/1812.05189-src/`,
`.localsource/dpf_ot_audit/`.

Related prior note:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-expanded-literature-survey-result-2026-06-16.md`.

## Abstract

LEDH-PFPF-OT combines an invertible particle-flow proposal with an optimal-transport
or differentiable-resampling step.  The difficult scaling problem is not merely
computing an optimal-transport distance.  The filter needs a transport object:
a coupling, a barycentric projection, or a directly transported particle cloud
that maps a weighted empirical ensemble to an approximately equal-weight
ensemble.  Dense entropic OT and the current TensorFlow implementation can
provide this object, but they require all-pairs costs or kernels.  For `N`
particles in state dimension `D`, a squared-Euclidean cost matrix costs
`O(N^2 D)` arithmetic per full pass and `O(N^2)` storage if materialized.
Streaming implementations remove dense storage but still perform all-pairs
work.

This survey explains the OT computation problem in LEDH-PFPF-OT and reviews
the main solution families: exact online/GPU Sinkhorn, Nystrom kernel
Sinkhorn, positive-feature Sinkhorn, direct low-rank coupling OT, sparse and
screened methods, accelerated Sinkhorn variants, stochastic/minibatch OT,
sliced and subspace OT, and particle-filter-specific localization ideas.  The
recommended near-term strategy is not to choose a single paper.  Keep exact
online/streaming Sinkhorn as the semantics-preserving reference; prototype
fixed-rank Nystrom and positive-feature Sinkhorn as approximate entropic
transports; and study low-rank coupling, localized/block OT, and sliced/subspace
transports as explicit new resampling methods with downstream validation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | How can the dense/all-pairs OT step in LEDH-PFPF-OT be scaled for large particle count `N` and large state dimension `D`? |
| Baseline | Current BayesFilter `annealed_transport_resample_tf` in `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`, especially dense and streaming `filterflow`-style transport. |
| Required object | A usable particle transport: coupling, barycentric projection, or direct transported cloud. |
| Literature screen | Does the method reduce `N x N` memory or all-pairs `O(N^2 D)` arithmetic while preserving or explicitly replacing the transport object? |
| Veto | Method only returns a scalar loss; method cannot handle weighted empirical measures; method silently changes resampling semantics; method depends on a non-TensorFlow implementation as the BayesFilter default. |
| Not concluded | No method is default-ready from literature alone.  No posterior-validity, gradient-correctness, or HMC-readiness claim is made here. |

ResearchAssistant status: `/home/ubuntu/python/ResearchAssistant` is present
and the MCP adapter is read-only.  Its local index returned no stored summaries
for this query, so this survey uses direct local paper text/PDF/source
inspection.  A later arXiv download attempt for additional 2025 sliced/streaming
sources stalled; the partial file is recorded in the manifest and is not cited
as read.

## 1. The LEDH-PFPF-OT Computation Problem

### 1.1 Particle-flow context

The Li-Coates PF-PF(LEDH) construction in the local documentation is a
proposal-corrected particle-flow particle filter, not merely a deterministic
cloud motion.  For particle `i`, the source-faithful LEDH flow maintains a
zero-noise auxiliary path and an actual proposal path.  With pseudo-time
`lambda`, local observation linearization is evaluated at the moving auxiliary
state:

```math
H^i(\lambda)
=
\left.
\frac{\partial h(\eta,0)}{\partial \eta}
\right|_{\eta=\bar\eta^i_\lambda},
\qquad
e^i(\lambda)
=
h(\bar\eta^i_\lambda,0)-H^i(\lambda)\bar\eta^i_\lambda .
```

Given particle-specific predicted covariance `P^i`, the local LEDH coefficients
are

```math
A^i(\lambda)
=
-\frac{1}{2}
P^i H^i(\lambda)^\top
\bigl(\lambda H^i(\lambda)P^iH^i(\lambda)^\top+R\bigr)^{-1}
H^i(\lambda),
```

```math
b^i(\lambda)
=
\bigl(I+2\lambda A^i(\lambda)\bigr)
\left[
  \bigl(I+\lambda A^i(\lambda)\bigr)
  P^i H^i(\lambda)^\top R^{-1}\{z_k-e^i(\lambda)\}
  + A^i(\lambda)\bar\eta_0^i
\right].
```

On a pseudo-time grid
`0=lambda_0<lambda_1<...<lambda_{N_lambda}=1`, the auxiliary and actual
states are updated by the same local affine step:

```math
\bar\eta^i_{\lambda_j}
=
\bar\eta^i_{\lambda_{j-1}}
+ \epsilon_j
\left[
  A_j^i(\lambda_j)\bar\eta^i_{\lambda_{j-1}}
  + b_j^i(\lambda_j)
\right],
```

```math
\eta^i_{\lambda_j}
=
\eta^i_{\lambda_{j-1}}
+ \epsilon_j
\left[
  A_j^i(\lambda_j)\eta^i_{\lambda_{j-1}}
  + b_j^i(\lambda_j)
\right].
```

The forward determinant multiplier is also particle-specific:

```math
\theta^i
=
\prod_{j=1}^{N_\lambda}
\left|\det\{I+\epsilon_j A_j^i(\lambda_j)\}\right|.
```

After the flow, Algorithm 1 uses the PF-PF weight

```math
w_k^i
\propto
\frac{
  p(x_k^i\mid x_{k-1}^i)
  p(z_k\mid x_k^i)
  \theta^i
}{
  p(\eta_0^i\mid x_{k-1}^i)
}
w_{k-1}^i .
```

If resampling is used, the documented Algorithm 1 state to resample is the
triple

```math
\{x_k^i,P_k^i,w_k^i\}_{i=1}^{N_p}.
```

Thus OT resampling is a BayesFilter extension layered on top of a
proposal-corrected flow.  The OT survey below asks how to make that extension
scalable without confusing it with the Li-Coates source algorithm.

Local anchors:
`docs/chapters/ch19b_dpf_literature_survey.tex` and
`docs/chapters/ch19c_dpf_implementation_literature.tex`.

### 1.2 Why the OT step is harder than a scalar distance

At a filtering time step, suppose the flow and likelihood update have produced
particles `x_i in R^D` with normalized weights `a_i`.  A deterministic
OT-resampling step usually compares the weighted empirical measure

```math
\mu_N = \sum_{i=1}^N a_i \delta_{x_i}
```

to an equal-weight target ensemble.  In the simplest self-transport version,
the support points are the same cloud and the target weights are

```math
b_j = \frac{1}{N},
\qquad
\nu_N = \sum_{j=1}^N b_j \delta_{x_j}.
```

A coupling `P` says how much source mass from particle `i` is assigned to
target slot `j`.  The transport polytope is

```math
\Pi(a,b)
=
\{P\in\mathbb{R}_+^{N\times N}: P\mathbf{1}=a,\;P^\top\mathbf{1}=b\}.
```

Depending on orientation, a deterministic barycentric transform has the form

```math
z_j
=
\frac{1}{b_j}\sum_{i=1}^N P_{ij}x_i
```

or, if rows are normalized as target slots in the implementation,

```math
z_i = \sum_{j=1}^N T_{ij}x_j,
\qquad
\sum_j T_{ij}=1.
```

This is the crucial point: a fast scalar `OT(mu,nu)` is insufficient.  The
filter needs `P`, a factorization of `P`, or an operator that can apply `P` to
the particle matrix `X`.

Reich's ensemble transform particle filter makes this barycentric requirement
explicit.  After solving an OT problem for weights, it replaces random
resampling by

```math
x_j^a = \bar x_j^a = \sum_{i=1}^M p_{ij} x_i^f,
\qquad j=1,\ldots,M.
```

Corenflos et al. likewise use entropy-regularized OT to obtain a differentiable
transport matrix for resampling, with primal entries recovered from dual
potentials as

```math
p^{OT}_{\epsilon,i,j}
=
a_i b_j
\exp\{\epsilon^{-1}(f_i^\ast+g_j^\ast-c_{ij})\}.
```

Local anchors:
`.localsource/dpf_ot_audit/reich2013_nonparametric_ensemble_transform.txt`,
`.localsource/dpf_ot_audit/corenflos2021_differentiable_particle_filtering_eot.txt`.

### 1.3 Current BayesFilter bottleneck

The current TensorFlow code has two modes:

1. Dense mode materializes a transport matrix and applies
   `transported = tf.linalg.matmul(transport_matrix, x)`.
2. Streaming mode returns a `[B,0,0]` sentinel for the transport matrix and
   applies transport by row/column chunks.

Streaming mode avoids storing `N x N` transport, but the chunked loop still
computes block costs

```math
C_{ij} = \frac{1}{2}\|\tilde x_i-\tilde x_j\|_2^2
```

and block log-transport weights

```math
\log T_{ij}
=
\frac{f_i+g_j-C_{ij}}{\epsilon}
- \text{column\_log\_normalizer}_j
+ \log N
+ \log w_j .
```

Then it accumulates

```math
z_i = \sum_j T_{ij}x_j.
```

Therefore the implementation has already solved part of the memory problem,
but not the all-pairs arithmetic problem.  For each Sinkhorn update or
transport application, the pairwise cost work is still approximately
`O(N^2D)`.  If `D` and `N` are both large, merely avoiding the dense matrix is
not enough.

Local anchor:
`experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.

## 2. Discrete OT And Entropic Sinkhorn Basics

### 2.1 Kantorovich OT

Let

```math
\mu=\sum_{i=1}^n a_i\delta_{x_i},
\qquad
\nu=\sum_{j=1}^m b_j\delta_{y_j},
```

with `a in Delta_n`, `b in Delta_m`, and cost matrix

```math
C_{ij}=c(x_i,y_j).
```

The discrete Kantorovich problem is

```math
OT(\mu,\nu)
=
\min_{P\in\Pi(a,b)} \langle C,P\rangle,
```

where

```math
\Pi(a,b)
=
\{P\in\mathbb{R}_+^{n\times m}:P\mathbf{1}_m=a,\;P^\top\mathbf{1}_n=b\}.
```

The exact linear program returns a transport plan `P`.  It is the correct
mathematical object, but dense exact solvers are too expensive for repeated
large particle-filter resampling.

### 2.2 Entropic OT

Cuturi's regularized problem replaces the linear program by a strictly convex
problem:

```math
OT_\epsilon(\mu,\nu)
=
\min_{P\in\Pi(a,b)}
\langle C,P\rangle
-\epsilon H(P),
```

with Shannon entropy convention

```math
H(P)=-\sum_{ij}P_{ij}(\log P_{ij}-1).
```

Equivalently, Corenflos et al. use a relative-entropy form

```math
W^2_{2,\epsilon}(\alpha_N,\beta_N)
=
\min_{P\in S(a,b)}
\sum_{i,j=1}^N
\left[
  p_{ij}c_{ij}
  + \epsilon p_{ij}\log\frac{p_{ij}}{a_i b_j}
\right].
```

For `epsilon>0`, the minimizer is unique and has Gibbs scaling form

```math
P_\epsilon
=
\operatorname{diag}(u)K\operatorname{diag}(v),
\qquad
K=\exp(-C/\epsilon).
```

The basic Sinkhorn updates are

```math
u \leftarrow a/(Kv),
\qquad
v \leftarrow b/(K^\top u),
```

with division elementwise.  Stabilized log-domain variants use dual potentials
`f,g` and log-sum-exp reductions instead of explicitly forming tiny kernel
entries.

Local anchors:
`.localsource/dpf_ot_audit/cuturi2013_sinkhorn_distances.txt`,
`.localsource/dpf_ot_audit/corenflos2021_differentiable_particle_filtering_eot.txt`,
`.localsource/scalable_ot_survey/2103.04737.txt`.

### 2.3 Applying the coupling to particles

If `P` is stored, the barycentric projection is one dense matrix multiply:

```math
Z
=
\operatorname{diag}(b)^{-1}P^\top X
```

for source particle matrix `X in R^{n x D}` and target slots `j=1,...,m`.
For equal target weights `b_j=1/m`,

```math
z_j = m\sum_iP_{ij}x_i.
```

If the implementation stores a row-stochastic target-to-source matrix `T`, the
same transform is

```math
Z=TX,
\qquad
T\mathbf{1}=\mathbf{1}.
```

Every scalable method must answer: can it compute this `Z` without dense
`N x N` storage and without all-pairs cost work?

## 3. Exact Online And GPU Sinkhorn

### 3.1 Online exact Sinkhorn

Online Sinkhorn keeps the exact entropic OT semantics but avoids storing the
full cost or kernel matrix.  For squared Euclidean costs,

```math
C_{ij}=\|x_i-y_j\|_2^2
=\|x_i\|_2^2+\|y_j\|_2^2-2x_i^\top y_j.
```

The stabilized update for `f` can be written schematically as

```math
f_i
\leftarrow
-\epsilon\log\sum_j
\exp\left((g_j-C_{ij})/\epsilon+\log b_j\right),
```

and similarly for `g_j`.  Online backends compute the log-sum-exp by streaming
blocks of `x_i,y_j` rather than reading a stored `C` or `K`.

This family is semantics-preserving: it gives the same entropic problem up to
numerical tolerance.  Its weakness is asymptotic.  Each iteration still touches
all `i,j` pairs.

### 3.2 FlashSinkhorn and fast CUDA log-domain Sinkhorn

FlashSinkhorn observes that for squared Euclidean costs, the log-domain update
is a row-wise log-sum-exp over biased dot-product scores, close to transformer
attention normalization.  It streams tiles through on-chip memory and writes
only the dual potentials.  The paper also states the barycentric projection
needed for transport application:

```math
T_\epsilon(x_i)
=
\frac{1}{a_i}\sum_{j=1}^m P^\ast_{ij}y_j,
```

with gradient expression

```math
\nabla_{x_i} OT_\epsilon
=
2a_i\bigl(x_i-T_\epsilon(x_i)\bigr).
```

That is directly relevant because LEDH-PFPF-OT needs `T_epsilon(x_i)`, not only
the value.  FlashSinkhorn is an engineering and systems answer to the current
BayesFilter streaming bottleneck: better tiling, fusion, and GPU memory traffic,
while preserving the all-pairs entropic OT object.

Fast Log-Domain Sinkhorn similarly argues for native CUDA log-domain kernels,
warp-level reductions, and shared-memory tiling.  It is less conceptually new
than FlashSinkhorn for our purpose, but it reinforces the same lesson: a
framework-level streaming TensorFlow implementation is a reference, not the
ceiling for exact GPU performance.

Local anchors:
`.localsource/scalable_ot_survey/2602.03067.txt`,
`.localsource/scalable_ot_survey/2605.00837.txt`,
`.localsource/scalable_ot_survey/2004.11127.txt`,
`.localsource/scalable_ot_survey/1810.08278.txt`.

### 3.3 Use for LEDH-PFPF-OT

Exact online/GPU Sinkhorn is the first reference lane.  It should remain the
comparison target because it preserves the intended entropic coupling and
barycentric transport.  It can make much larger `N` feasible on GPU, but it
does not solve cases where `N^2D` arithmetic itself is impossible.  For those,
we need low-rank, sparse, sliced, local, or minibatch approximations, each of
which changes the object or adds assumptions.

## 4. Nystrom Kernel Sinkhorn

### 4.1 What `1812.05189` does

The target paper, Altschuler et al. "Massively scalable Sinkhorn distances via
the Nystrom method", approximates the Gibbs kernel

```math
K_{ij}
=
k_\eta(x_i,x_j)
=
\exp(-\eta\|x_i-x_j\|^2)
```

by a low-rank Nystrom factorization

```math
\tilde K = V A^{-1}V^\top.
```

Given landmark points

```math
X_r=\{\tilde x_1,\ldots,\tilde x_r\}\subset X,
```

the factors are

```math
V_{ij}=k_\eta(x_i,\tilde x_j),
\qquad
A_{jj'}=k_\eta(\tilde x_j,\tilde x_{j'}).
```

If `A=LL^T`, a matrix-vector product is computed without forming
`\tilde K`:

```math
\tilde K v
=
V\left(L^{-\top}\left(L^{-1}(V^\top v)\right)\right).
```

After Cholesky, each multiply is `O(nr)` instead of `O(n^2)`.  Sinkhorn scaling
then uses

```math
\tilde P
=
D_1\tilde K D_2
=
D_1 V A^{-1}V^\top D_2.
```

For particle transport, this factorization is especially useful because

```math
\tilde P X
=
D_1V A^{-1}V^\top D_2X.
```

Thus the transported cloud can be computed in `O(nrD+r^2D)` rather than
materializing `P`.

### 4.2 Adaptive rank and effective dimension

The paper's adaptive Nystrom subroutine doubles the rank until the entrywise
kernel approximation error is below a threshold.  The diagnostic is simple for
Gaussian kernels:

```math
\|K-\tilde K\|_\infty
=
1-\min_i\tilde K_{ii}.
```

It proves that if points lie in a ball in `R^d`, the required rank can be
bounded by a quantity of the form

```math
r^\ast(X,\eta,\epsilon')
\le
3\left(
6+\frac{53}{d}\eta R^2
+\frac{3}{d}\log\frac{2n}{\epsilon'}
\right)^d.
```

This worst-case ambient-dimensional expression is alarming for high `D`.  The
paper's more favorable result is for data on a `k`-dimensional manifold:

```math
r^\ast(X,\eta,\epsilon')
\le
c_{\Omega,\eta}
\left(\log\frac{n}{\epsilon'}\right)^{5k/2}.
```

So Nystrom Sinkhorn can help when the post-flow particles have low effective or
intrinsic dimension in the Sinkhorn kernel.  It can fail when high ambient
dimension is also high intrinsic dimension, when entropy is small, or when the
kernel length scale makes `K` effectively full rank.

### 4.3 Stability statement

The paper also gives a useful stability view.  If

```math
\|\log K-\log\tilde K\|_\infty \le \epsilon',
```

then Sinkhorn scaling the approximate kernel gives a plan

```math
\tilde P=D_1\tilde K D_2
```

with controlled marginal residual

```math
\|\tilde P\mathbf{1}-p\|_1
+\|\tilde P^\top\mathbf{1}-q\|_1
\le \epsilon',
```

and controlled objective error.  For BayesFilter, the more important
engineering diagnostic is not only objective error but transported-particle
error:

```math
\|\tilde P X-P_\epsilon X\|.
```

That must be measured directly in any prototype.

Local anchors:
`.localsource/1812.05189-src/sections/nystrom.tex`,
`.localsource/1812.05189-src/sections/sinkhorn.tex`,
`.localsource/1812.05189.txt`.

### 4.4 Use for LEDH-PFPF-OT

Nystrom Sinkhorn is a strong first approximate entropic lane because it still
resembles the current Sinkhorn object and directly supports factored transport
application.  The implementation should be deterministic at first: fixed rank,
fixed landmarks or fixed leverage-score seed, TensorFlow operations, and parity
against dense/streaming exact transport on small fixtures.

## 5. Positive-Feature Sinkhorn

Positive-feature Sinkhorn replaces the Gibbs kernel by an inner product of
positive features.  Choose a map

```math
\phi_\theta(x)\in\mathbb{R}^r_{+}
```

and define

```math
k_\theta(x,y)
=
\langle\phi_\theta(x),\phi_\theta(y)\rangle.
```

Then set the corresponding cost as

```math
c_\theta(x,y)
=
-\epsilon\log k_\theta(x,y).
```

For source and target feature matrices

```math
\xi
=
[\phi_\theta(x_1),\ldots,\phi_\theta(x_n)]
\in(\mathbb{R}_+^\ast)^{r\times n},
```

```math
\zeta
=
[\phi_\theta(y_1),\ldots,\phi_\theta(y_m)]
\in(\mathbb{R}_+^\ast)^{r\times m},
```

the sample kernel is

```math
K_\theta
=
\xi^\top\zeta.
```

Sinkhorn matrix-vector products therefore cost `O(r(n+m))`, and the dual
objective can be written as

```math
W_{\epsilon,c_\theta}(\mu,\nu)
=
\max_{\alpha\in\mathbb{R}^n,\beta\in\mathbb{R}^m}
a^\top\alpha+b^\top\beta
-\epsilon(\xi e^{\alpha/\epsilon})^\top
\zeta e^{\beta/\epsilon}
+\epsilon.
```

The paper also interprets many kernels through an integral representation

```math
k(x,y)
=
\int_U \phi(x,u)^\top\phi(y,u)\,d\rho(u),
```

then approximates this integral by finite positive features:

```math
\phi_\theta(x)
=
\frac{1}{\sqrt r}
(\phi(x,u_1),\ldots,\phi(x,u_r)).
```

For LEDH-PFPF-OT, the transport application would be

```math
P X
=
\operatorname{diag}(u)\xi^\top\zeta\operatorname{diag}(v)X.
```

As with Nystrom, this can be applied in factored form.  The main caution is
semantic: the paper is framed around Sinkhorn divergences and positive-feature
cost approximations.  Before using it as resampling, we must verify the
transported-particle quality, marginal residuals, and bias caused by the
feature approximation.

Local anchor:
`.localsource/scalable_ot_survey/2006.07057.txt`.

## 6. Direct Low-Rank Coupling OT

### 6.1 Why low-rank couplings are different from low-rank kernels

Nystrom and positive-feature methods approximate the entropic kernel `K`.
Direct low-rank OT instead constrains or parametrizes the coupling `P` itself.
This is a more radical change and potentially more useful for true
subquadratic scaling.

The nonnegative rank of a nonnegative matrix is

```math
\operatorname{rank}_+(M)
=
\min\left\{
r:\;M=\sum_{k=1}^r M_k,\;
\operatorname{rank}(M_k)=1,\;M_k\ge0
\right\}.
```

The rank-constrained coupling set is

```math
\Pi_{a,b}(r)
=
\{P\in\Pi(a,b):\operatorname{rank}_+(P)\le r\}.
```

The low-rank OT problem is

```math
\min_{P\in\Pi_{a,b}(r)}\langle C,P\rangle.
```

This returns a transport plan, but generally not the same plan as entropic
Sinkhorn at any fixed `epsilon`.

### 6.2 Factored coupling parameterization

Forrow and later Scetbon-Cuturi-Peyre use a factored coupling

```math
P
=
Q\operatorname{diag}(1/g)R^\top,
```

where

```math
Q\in\Pi(a,g),
\qquad
R\in\Pi(b,g),
\qquad
g\in\Delta_r.
```

Equivalently, define

```math
FC_{a,b}(r)
=
\{(Q,R,g): Q\in\mathbb{R}_+^{n\times r},
R\in\mathbb{R}_+^{m\times r},
g\in(\mathbb{R}_+^\ast)^r,\;
Q\in\Pi(a,g),\;R\in\Pi(b,g)\}.
```

Then

```math
\min_{P\in\Pi_{a,b}(r)}\langle C,P\rangle
=
\min_{(Q,R,g)\in FC_{a,b}(r)}
\left\langle C,Q\operatorname{diag}(1/g)R^\top\right\rangle.
```

Transport application is efficient:

```math
PX
=
Q\operatorname{diag}(1/g)R^\top X.
```

If `r << N`, this is attractive for particles: compute `R^T X` first, then
multiply through the latent rank.

### 6.3 Latent-coupling factorization

Halmos et al. introduce a latent-coupling factorization with an additional
`r x r` latent plan:

```math
LC_{a,b}(r)
=
\{(Q,R,T):
Q\in\mathbb{R}_+^{n\times r},
R\in\mathbb{R}_+^{m\times r},
T\in\mathbb{R}_+^{r\times r},
Q\in\Pi(a,\cdot),
R\in\Pi(b,\cdot),
T\in\Pi(g_Q,g_R)
\}.
```

The induced coupling is schematically

```math
P
=
Q\operatorname{diag}(1/g_Q)
T
\operatorname{diag}(1/g_R)R^\top.
```

This generalizes the diagonal latent connection in the older factorization.
For LEDH-PFPF-OT, it means the transport can route mass through a small latent
transport problem, not merely through matched latent components.

### 6.4 Riemannian low-rank OT and rank diagnostics

The 2026 Riemannian low-rank paper uses positive factors and manifold
optimization.  For balanced linear OT it represents

```math
\Gamma
=
U\operatorname{diag}(U^\top\mathbf{1})^{-1}V^\top,
```

and optimizes

```math
f(U,V)=\langle C,\Gamma\rangle.
```

It also gives a rank-sufficiency diagnostic for convex full-coupling objectives.
Let `Gamma_r` be the rank-`r` solution and define a reduced gradient/slack
matrix

```math
R
=
\nabla_\Gamma f(\Gamma_r)
-\alpha^\ast\mathbf{1}^\top
-\mathbf{1}(\beta^\ast)^\top.
```

Then

```math
\delta_r=\min_{ij}R_{ij}.
```

If `delta_r >= 0`, the rank-`r` solution is globally optimal for the full
problem under the theorem's assumptions.  If `delta_r < 0`, the most negative
entry suggests a rank-increase direction.  Even when the exact certificate is
hard to satisfy numerically, this is useful as a diagnostic: it tells us whether
the chosen rank is clearly too small.

Local anchors:
`.localsource/scalable_ot_survey/1806.07348.txt`,
`.localsource/scalable_ot_survey/2103.04737.txt`,
`.localsource/scalable_ot_survey/2205.12365.txt`,
`.localsource/scalable_ot_survey/2305.19727.txt`,
`.localsource/scalable_ot_survey/2411.10555.txt`,
`.localsource/scalable_ot_survey/2503.03025.txt`,
`.localsource/scalable_ot_survey/2603.03578.txt`,
`.localsource/scalable_ot_survey/2606.12120.txt`.

### 6.5 Use for LEDH-PFPF-OT

Direct low-rank coupling is the most promising long-term subquadratic route
because it can reduce both storage and transport application.  But it is not a
silent acceleration of dense Sinkhorn.  It imposes a low-rank structure on the
resampling plan.  That may be beneficial in high dimension, but it changes the
filter approximation and requires downstream posterior validation.

## 7. Sparse, Screened, And Stabilized OT

### 7.1 Sparse multiscale OT

Schmitzer's sparse multiscale algorithm starts from the exact discrete problem

```math
\Pi(\mu,\nu)
=
\{\pi\in P(X\times Y):
\pi(\{x\}\times Y)=\mu(x),
\pi(X\times\{y\})=\nu(y)\},
```

```math
\min_{\pi\in\Pi(\mu,\nu)}
C(\pi),
\qquad
C(\pi)=\sum_{(x,y)\in X\times Y}c(x,y)\pi(x,y).
```

The dense problem considers the full product `X x Y`.  The sparse algorithm
tries to solve a sequence of sparse subproblems while verifying global
optimality locally through shielding neighborhoods.  This is highly relevant
when the true transport is geometrically local.

For LEDH-PFPF-OT, locality is plausible after LEDH flow if the flow has already
moved particles close to posterior structure.  But high-dimensional
concentration can make nearest-neighbor locality brittle.  A locality audit of
post-flow particles should precede this lane.

### 7.2 Screenkhorn

Screenkhorn accelerates regularized OT by screening dual variables.  The
regularized primal is

```math
S_\eta(\mu,\nu)
=
\min_{P\in\Pi(\mu,\nu)}
\{\langle C,P\rangle-\eta H(P)\}.
```

With Gibbs kernel

```math
K=\exp(-C/\eta),
```

the dual can be written in variables `u,v` as

```math
\min_{u\in\mathbb{R}^n,v\in\mathbb{R}^m}
\Psi(u,v)
=
\mathbf{1}_n^\top B(u,v)\mathbf{1}_m
-\langle u,\mu\rangle
-\langle v,\nu\rangle,
```

where

```math
B(u,v)
=
\Delta(e^u)K\Delta(e^v).
```

The idea is to identify negligible components and solve a smaller constrained
dual problem.  This can reduce work when many rows/columns or interactions are
inactive, but it still has to yield a transport object with acceptable marginal
residuals.

### 7.3 Stabilization and epsilon scaling

Schmitzer's stabilized sparse scaling work and the broader computational OT
literature emphasize log-domain stabilization, epsilon scaling, truncation, and
coarse-to-fine methods.  These are not a separate approximation family for our
purposes; they are a toolbox that should be combined with exact, sparse, or
low-rank methods.  Small `epsilon` is exactly where standard-domain
`K=exp(-C/epsilon)` underflows and where kernel low-rank approximations can
degrade.

Local anchors:
`.localsource/scalable_ot_survey/1510.05466.txt`,
`.localsource/scalable_ot_survey/1906.08540.txt`,
`.localsource/dpf_ot_audit/schmitzer2019_stabilized_sparse_scaling.txt`.

## 8. Accelerated, Greedy, And Stochastic Sinkhorn Iterations

This family improves iteration complexity or coordinate-update efficiency but
does not by itself remove dense all-pairs kernel access.

Greenkhorn updates the most violating row or column instead of all rows and
columns.  The standard Sinkhorn projection is

```math
P=\operatorname{diag}(u)K\operatorname{diag}(v),
```

and Greenkhorn changes the schedule for updating components of `u,v`.  It can
be faster when many marginal constraints are already nearly satisfied or when
mass is sparse.

Accelerated primal-dual, accelerated mirror-descent, and related methods
improve theoretical dependence on accuracy or regularization.  They are useful
secondary tools, especially if we keep a dense/online backend.  But if each
iteration still requires `Kv` and `K^T u` with dense `K`, the large `N,D`
bottleneck remains.

Local anchors:
`.localsource/scalable_ot_survey/1705.09634.txt`,
`.localsource/scalable_ot_survey/1802.04367.txt`,
`.localsource/scalable_ot_survey/1803.01347.txt`,
`.localsource/scalable_ot_survey/1901.06482.txt`,
`.localsource/scalable_ot_survey/2605.30267.txt`.

## 9. Stochastic And Minibatch OT

### 9.1 Stochastic dual OT

Genevay et al. develop stochastic optimization for large-scale regularized OT.
This is important for learning losses and settings where measures are sampled
from distributions.  For particle filtering, however, the resampling step acts
on a finite ensemble at a specific time.  Replacing the full coupling by
stochastic dual estimates is not automatically a valid resampling transform.

### 9.2 BoMb-OT and hierarchical minibatches

Minibatch OT methods reduce computation by solving smaller OT problems and an
outer problem over minibatches.  The entropic population BoMb-OT has the form

```math
ED^m_d(\mu,\nu)
=
\min_{\gamma\in\Pi(\mu^{\otimes m},\nu^{\otimes m})}
\mathbb{E}_{(X^m,Y^m)\sim\gamma}
\left[
  d(P_{X^m},P_{Y^m})
\right]
+\lambda\,KL(\gamma\mid \mu^{\otimes m}\otimes\nu^{\otimes m}).
```

For finite `k` minibatches of size `m`, an outer `k x k` OT problem couples
minibatches.  If the inner discrepancy is Sinkhorn with complexity `O(m^2)`,
the cost matrix construction is roughly `O(m^2k^2)`.  If the inner discrepancy
is sliced Wasserstein, it can be closer to `O(m log m k^2)`.

For an unbalanced minibatch variant, the local unbalanced OT problem is

```math
UOT^\phi_\tau(\mu_n,\nu_n)
=
\min_{\pi\in\mathbb{R}_+^{n\times n}}
\langle C,\pi\rangle
+\tau D_\phi(\pi\mathbf{1},\mu_n)
+\tau D_\phi(\pi^\top\mathbf{1},\nu_n).
```

The minibatch transportation plan is then assembled from outer minibatch
couplings and inner minibatch plans.

### 9.3 Use for LEDH-PFPF-OT

Minibatch OT is tempting for large `N`, but it is the most dangerous drop-in
candidate.  A minibatch plan can be optimal inside small batches and wrong for
the full ensemble.  It may be useful for diagnostics, training losses, or a
new randomized resampling method, but it should not replace full-ensemble
transport without a filtering-theory argument and posterior validation.

Local anchors:
`.localsource/scalable_ot_survey/1605.08527.txt`,
`.localsource/scalable_ot_survey/2102.05912.txt`,
`.localsource/scalable_ot_survey/2108.09645.txt`.

## 10. Sliced, Max-Sliced, Generalized Sliced, And Subspace OT

### 10.1 One-dimensional OT by sorting

Sliced methods attack high dimension by projecting measures to one-dimensional
distributions.  For one-dimensional measures, the monotone transport map is

```math
T(x)=F_\nu^{-1}(F_\mu(x)),
```

and

```math
W_p^p(\mu,\nu)
=
\int_0^1
\left|
F_\mu^{-1}(z)-F_\nu^{-1}(z)
\right|^p dz.
```

For empirical distributions, this is computed by sorting projected samples.
The cost is `O(N log N)` per projection rather than `O(N^2)`.

### 10.2 Sliced Wasserstein

For direction `theta in S^{d-1}`, let `theta#mu` be the pushforward of `mu`
under projection `x -> <theta,x>`.  The sliced Wasserstein distance is

```math
SW_p^p(\mu,\nu)
=
\int_{S^{d-1}}
W_p^p(\theta_\#\mu,\theta_\#\nu)\,d\theta.
```

The empirical approximation uses directions
`theta_1,...,theta_L`:

```math
\widehat{SW}_p^p(\mu,\nu)
=
\frac{1}{L}\sum_{\ell=1}^L
W_p^p((\theta_\ell)_\#\mu,(\theta_\ell)_\#\nu).
```

Deshpande et al. write the same idea as

```math
\widetilde W_p(P_d,P_g)
=
\left[
\int_{\omega\in\Omega}
W_p^p(P_d^\omega,P_g^\omega)\,d\omega
\right]^{1/p}.
```

For samples `D,F`, a finite set of directions `\hat\Omega` gives

```math
\frac{1}{|\hat\Omega|}
\sum_{\omega\in\hat\Omega}
W_2^2(D^\omega,F^\omega),
```

and each one-dimensional term is computed by sorting:

```math
W_2^2(D^\omega,F^\omega)
=
\frac{1}{|D|}\sum_i
\left\|
D^\omega_{\pi_D^\omega(i)}
-F^\omega_{\pi_F^\omega(i)}
\right\|_2^2.
```

### 10.3 Max-sliced and generalized sliced

Max-sliced Wasserstein replaces random averaging by the best projection:

```math
MSW_p^p(\mu,\nu)
=
\max_{\theta\in S^{d-1}}
W_p^p(\theta_\#\mu,\theta_\#\nu).
```

Generalized sliced Wasserstein replaces linear projections by a richer family
of slicing functions.  This can reduce projection complexity when linear
one-dimensional projections miss relevant nonlinear structure.

### 10.4 Subspace robust Wasserstein

Subspace robust Wasserstein searches over lower-dimensional projections rather
than all of `R^D`.  In a representative form, it optimizes Wasserstein distance
after projecting onto a `k`-dimensional subspace.  This addresses the statistical
curse of dimensionality by focusing transport on informative subspaces.

### 10.5 Use for LEDH-PFPF-OT

Sliced and subspace methods are highly relevant when `D` is the dominant
problem.  They can also generate transport maps in projected coordinates, but a
full particle resampling transform in `R^D` is not the same object as a dense
coupling.  A sliced transport plan may be a good new resampler if we define how
multiple one-dimensional couplings are composed or averaged into a particle
update.  It should not be called a faithful acceleration of dense Sinkhorn.

Local anchors:
`.localsource/scalable_ot_survey/1901.08949.txt`,
`.localsource/scalable_ot_survey/1902.00434.txt`,
`.localsource/scalable_ot_survey/1904.05877.txt`,
`.localsource/scalable_ot_survey/2508.12519.txt`.

## 11. Localization And Particle-Filter-Specific Structure

The numerical OT literature does not know the state-space model.  LEDH-PFPF-OT
does.  If the state has spatial, block, factor, or conditional-independence
structure, the most principled large-`D` answer may be localization rather than
a generic global OT approximation.

A localized OT resampler would partition the state or particle features and
solve smaller transport problems:

```math
x_i=(x_i^{(1)},\ldots,x_i^{(B)}),
```

then compute block transports

```math
P^{(b)}\in\Pi(a^{(b)},b^{(b)})
```

or shared particle-level couplings restricted by local costs

```math
C_{ij}
=
\sum_{b=1}^B C_{ij}^{(b)}
```

with screening/locality.  This is not covered by a single surveyed paper above,
but it is a recurring lesson from ensemble transform particle filters and
high-dimensional filtering: a global transport in the full state can be
statistically and computationally fragile.

For BayesFilter, localization should be studied alongside low-rank methods,
not after them.  It is especially important if LEDH state vectors come from
spatial fields, macro panels, or structured latent blocks.

Local anchors:
`.localsource/dpf_ot_audit/reich2013_nonparametric_ensemble_transform.txt`,
`docs/chapters/ch19b_dpf_literature_survey.tex`,
`docs/chapters/ch19c_dpf_implementation_literature.tex`.

## 12. Method Taxonomy For LEDH-PFPF-OT

| Family | Representative local sources | Transport object? | What it fixes | Main risk |
| --- | --- | --- | --- | --- |
| Exact online/GPU Sinkhorn | GeomLoss/KeOps, FlashSinkhorn, Fast Log-Domain Sinkhorn | Yes | Dense storage and GPU IO | Still all-pairs `O(N^2D)` work |
| Nystrom Sinkhorn | Altschuler et al. `1812.05189` | Yes, factored entropic coupling | Kernel matvecs when effective rank is small | Rank may grow badly with dimension/small epsilon |
| Positive-feature Sinkhorn | Scetbon-Cuturi `2006.07057` | Yes if coupling application is implemented | Linear-time positive kernel matvecs | Feature approximation changes cost/kernel |
| Low-rank coupling OT | Forrow; Scetbon; Halmos; Jawanpuria-Mishra | Yes, factored coupling | Coupling storage and transport application | Changes feasible plan class |
| Sparse/multiscale/screened | Schmitzer; Screenkhorn | Yes | Active pair count when coupling is local/screenable | Locality may fail in high dimension |
| Accelerated/greedy Sinkhorn | Greenkhorn, APDAGD/APDAMD, Acc-Sinkhorn | Yes | Iteration count/convergence | Dense kernel access remains |
| Stochastic/minibatch OT | Genevay, BoMb-OT, partial minibatch OT | Sometimes partial/local plans | Training-scale memory and compute | Not a full deterministic resampling plan |
| Sliced/subspace OT | GSW, max-sliced, subspace robust, sliced survey | Projected plans/maps | High-dimensional statistics and speed | Different transport object |
| Localization/block OT | Reich-style filtering context, model structure | Yes if designed | Large `D` with state locality | Requires model-specific validation |

## 13. Recommended Research Program

### Lane A: semantics-preserving exact reference

Keep the current dense/streaming TensorFlow path as the correctness reference.
Study FlashSinkhorn/KeOps-style online GPU design as an implementation
benchmark.  This lane answers: how far can exact entropic OT scale if we fix
engineering and memory traffic?

Required diagnostics:

```math
\|P\mathbf{1}-a\|_1,
\qquad
\|P^\top\mathbf{1}-b\|_1,
\qquad
\|Z_{\text{candidate}}-Z_{\text{dense}}\|.
```

### Lane B: approximate entropic factored kernels

Prototype fixed-rank Nystrom Sinkhorn first.  Then compare positive-feature
Sinkhorn.  Both should expose a factored transport application:

```math
Z
=
\operatorname{diag}(b)^{-1}
\tilde P^\top X
```

without dense `P`.

Primary diagnostics:

```math
\text{effective rank},
\qquad
\|\log K-\log\tilde K\|_\infty,
\qquad
\|Z_{\text{factored}}-Z_{\text{exact}}\|.
```

### Lane C: structural approximate couplings

Study low-rank coupling OT, localized OT, and sliced/subspace transports as new
resampling methods.  These should not be judged only by dense Sinkhorn parity:
some may intentionally bias the transport to improve high-dimensional behavior.
They require downstream filtering diagnostics.

For low-rank coupling:

```math
P=Q\operatorname{diag}(1/g)R^\top
```

or

```math
P
=
Q\operatorname{diag}(1/g_Q)T
\operatorname{diag}(1/g_R)R^\top.
```

For sliced/subspace methods:

```math
\widehat{SW}_p^p
=
\frac{1}{L}\sum_{\ell=1}^L
W_p^p((\theta_\ell)_\#\mu,(\theta_\ell)_\#\nu).
```

The validation question is not "does this match dense Sinkhorn exactly?" but
"does this produce a stable, posterior-valid, differentiable resampling
approximation under the filtering target?"

## 14. Validation Ladder Before Any Default Change

1. Small deterministic dense parity: compare transported particles, not only OT
   values.
2. Marginal checks: source and target constraints with weighted inputs.
3. Positivity and non-finite checks.
4. Representation diagnostics: rank, feature dimension, sparsity, projection
   count, or block locality.
5. LEDH-PFPF-OT value parity on existing fixtures.
6. Gradient smoke tests after value parity.
7. Runtime and memory ladder over `N,D`.
8. Posterior/reference diagnostics for filtering.
9. Multi-seed uncertainty-aware comparisons before ranking stochastic methods.
10. Default-readiness review only after downstream evidence, not from paper
    benchmarks alone.

## 15. Conclusions

The answer to whether `1812.05189` can help is yes, but it should not be the
only method considered.  Nystrom Sinkhorn is a strong first approximate
entropic transport because it yields a factored coupling and can apply the
transport to particles.  Its success depends on the effective rank of the
post-flow Gibbs kernel.

For near-term engineering, exact online/GPU Sinkhorn is the reference lane.  It
preserves the current entropic OT semantics and directly supports barycentric
transport, but it remains all-pairs.  For true large-`N,D` scaling, the most
promising methods are structural: low-rank coupling OT, localization/block OT,
and possibly sliced/subspace transports.  These are not mere accelerations;
they are new resampling approximations and must be validated as such.

The safest research posture is a three-lane program: exact online Sinkhorn for
reference and moderate scaling, low-rank kernel Sinkhorn for the first
factored entropic approximation, and low-rank/localized/sliced transports as
explicit new filtering methods.  No candidate should become a BayesFilter
default until it passes transported-particle parity or a declared replacement
criterion, marginal diagnostics, numerical stability checks, and downstream
filtering validation.

## References And Local Source Map

| Topic | Local source |
| --- | --- |
| Corpus manifest | `.localsource/scalable_ot_survey/MANIFEST.md` |
| Current TensorFlow annealed transport | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py` |
| LEDH/PF-PF source-form documentation | `docs/chapters/ch19b_dpf_literature_survey.tex`; `docs/chapters/ch19c_dpf_implementation_literature.tex` |
| Cuturi Sinkhorn distances | `.localsource/dpf_ot_audit/cuturi2013_sinkhorn_distances.txt` |
| Reich ensemble transform PF | `.localsource/dpf_ot_audit/reich2013_nonparametric_ensemble_transform.txt` |
| Corenflos differentiable OT resampling | `.localsource/dpf_ot_audit/corenflos2021_differentiable_particle_filtering_eot.txt` |
| Nystrom Sinkhorn target paper | `.localsource/1812.05189-src/sections/nystrom.tex`; `.localsource/1812.05189-src/sections/sinkhorn.tex`; `.localsource/1812.05189.txt` |
| Positive-feature Sinkhorn | `.localsource/scalable_ot_survey/2006.07057.txt` |
| Exact online/GPU Sinkhorn | `.localsource/scalable_ot_survey/1810.08278.txt`; `.localsource/scalable_ot_survey/2004.11127.txt`; `.localsource/scalable_ot_survey/2602.03067.txt`; `.localsource/scalable_ot_survey/2605.00837.txt` |
| Low-rank coupling OT | `.localsource/scalable_ot_survey/1806.07348.txt`; `.localsource/scalable_ot_survey/2103.04737.txt`; `.localsource/scalable_ot_survey/2205.12365.txt`; `.localsource/scalable_ot_survey/2305.19727.txt`; `.localsource/scalable_ot_survey/2411.10555.txt`; `.localsource/scalable_ot_survey/2503.03025.txt`; `.localsource/scalable_ot_survey/2603.03578.txt`; `.localsource/scalable_ot_survey/2606.12120.txt` |
| Sparse/screened/stabilized OT | `.localsource/scalable_ot_survey/1510.05466.txt`; `.localsource/scalable_ot_survey/1906.08540.txt`; `.localsource/dpf_ot_audit/schmitzer2019_stabilized_sparse_scaling.txt` |
| Accelerated/greedy Sinkhorn | `.localsource/scalable_ot_survey/1705.09634.txt`; `.localsource/scalable_ot_survey/1802.04367.txt`; `.localsource/scalable_ot_survey/1803.01347.txt`; `.localsource/scalable_ot_survey/1901.06482.txt`; `.localsource/scalable_ot_survey/2605.30267.txt` |
| Stochastic/minibatch OT | `.localsource/scalable_ot_survey/1605.08527.txt`; `.localsource/scalable_ot_survey/2102.05912.txt`; `.localsource/scalable_ot_survey/2108.09645.txt` |
| Sliced/subspace OT | `.localsource/scalable_ot_survey/1901.08949.txt`; `.localsource/scalable_ot_survey/1902.00434.txt`; `.localsource/scalable_ot_survey/1904.05877.txt`; `.localsource/scalable_ot_survey/2508.12519.txt` |
