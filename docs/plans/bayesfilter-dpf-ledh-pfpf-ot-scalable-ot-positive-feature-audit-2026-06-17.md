# Candidate Audit: Positive-Feature Sinkhorn

Date: 2026-06-17

## Status

`source_locked`; semantic class: approximate kernel / semantic kernel
replacement.  Execution value is `execution_value_pending`.

This lane replaces the Gibbs kernel by an inner product of positive features.
It may produce linear-time Sinkhorn matvecs, but the feature kernel changes the
cost/kernel unless an approximation error contract is written and checked.

## Paper-Note-Code-Execution Matrix

| Comparison item | Original paper | Local note | Downloaded code | Execution-value test | Required resolution |
| --- | --- | --- | --- | --- | --- |
| Problem solved | Scetbon-Cuturi positive features replace the kernel by `k_theta(x,y)=<phi_theta(x),phi_theta(y)>`; paper text is locally extracted in `.localsource/scalable_ot_survey/2006.07057.txt`. | Survey lines 546-624 define positive features, kernel/cost replacement, dual objective, finite features, and transport application, with semantic warning. | LinearSinkhorn `FastSinkhorn.py` lines 77-99 implements scaling for factored positive matrices; lines 102-135 implements `Lin_Sinkhorn_RBF`; lines 138-161 implements the Gaussian feature map. `EXP_GAN/torch_lin_sinkhorn.py` is an additional scalar-cost script. | Fixed-feature tiny fixture against Phase 1 dense baseline and Nystrom reference. | Declare whether the lane is approximating dense Gibbs kernel or intentionally replacing the kernel. |
| Transport object | With feature matrices `xi,zeta`, transport can be applied as `diag(u) xi^T zeta diag(v) X`. | Survey equation `eq:positive-feature-transport` explicitly gives the transported-particle route. | LinearSinkhorn source returns scalings/cost traces; it does not expose a reusable BayesFilter transport API. | Candidate wrapper must return transported particles and feature/scaling diagnostics, not only scalar Sinkhorn cost. | Scalar loss routines are not sufficient for resampling. |
| Marginals/orientation | Scaling vectors should satisfy source/target marginals under the feature kernel. | Local note requires marginal residual and transported-particle comparison to exact entropic reference. | `Lin_Sinkhorn` computes residuals against `a` and `b` at `FastSinkhorn.py` lines 83-98; `Lin_Sinkhorn_RBF` updates `u,v` at lines 120-125. | Record row/column residuals under the feature-induced plan. | Orientation and matrix shapes must be audited because code uses `A`, `B`, and `B.T` conventions. |
| Cost/kernel/epsilon | Cost is `c_theta = -epsilon log k_theta`; finite features approximate an integral representation. | Survey equations `eq:positive-feature-kernel`, `eq:positive-feature-cost`, and `eq:positive-feature-finite` define the local math. | `Feature_Map_Gaussian` uses `reg`, radius `R`, seed, and `num_samples` at lines 138-161. | Candidate config must record feature count, seed, radius rule, and epsilon/reg. | A feature-kernel success does not establish exact dense-Sinkhorn equivalence. |
| Approximation knob | Number of positive features, random feature seed, feature distribution, and radius. | Local note flags changed cost/kernel as the main expected failure mode. | LinearSinkhorn uses `num_samples` and fixed seed. | Freeze features for deterministic tests; later vary feature count as explanatory. | Random-feature luck cannot be a promotion criterion without replication. |
| Backend and gradients | Method is differentiable in principle under suitable feature maps. | BayesFilter-owned implementation must be TensorFlow/TFP. | Inspected source is NumPy/PyTorch research code. | Phase 5 should implement TensorFlow feature factors and a transported-particle application. | Do not promote PyTorch/NumPy source to default code. |
| Execution value | Linear-time claims depend on feature quality and stable positive factors. | Local note requires comparison against dense reference and explicit semantic warning. | Source availability demonstrates a research route, not local execution value. | First execution-value artifact must include dense-reference particle error, residuals, feature count, finite checks, and runtime. | No ranking, no speedup, and no execution-value claim from static source inspection. |

## Source And Semantic Classification

- Source status: `source_locked`.
- Semantic class: approximate kernel when features approximate the Gibbs
  kernel; semantic replacement when the feature kernel is treated as the new
  cost.
- BayesFilter posture: viable TensorFlow prototype only with explicit feature
  and kernel-error diagnostics.
- Required transport: feature factors, scaling vectors, and transported
  particles.
- Boundary guard: `source_locked` plus `execution_value_pending` must not be
  read as transport correctness, dense-Gibbs equivalence, default-readiness, or
  ranking evidence, even if the feature kernel is descriptively close to the
  dense Gibbs kernel on a small fixture.

## First Execution-Value Contract

Question: can fixed positive features produce finite, diagnostically valid
transported particles on Phase 1 fixtures and quantify the semantic delta from
dense entropic OT?

Baseline/comparator: Phase 1 dense/streaming TensorFlow baseline and, where
available, Nystrom candidate diagnostics.

Primary criterion: finite transported particles, valid residuals under the
feature plan, and dense-reference transported-particle error reported as
promotion criterion only for the approximation-to-dense interpretation.

Vetoes: scalar loss only, nonpositive/zero feature kernel causing invalid
scalings, wrong cost/epsilon map, non-TensorFlow default path, or silent
semantic replacement.

Not concluded: no exact dense equivalence, no posterior correctness, no
production default, no statistically supported ranking.

## Decision

Advance as a later approximate-kernel/semantic-replacement candidate.  It
should not outrank Nystrom from static evidence alone because the inspected code
is more script-oriented and the semantic change is stronger.
