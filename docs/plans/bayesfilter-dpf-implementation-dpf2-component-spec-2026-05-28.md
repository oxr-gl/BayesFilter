# DPF2 Differentiable Resampling Component Specification

## Status

DPF2 execution artifact.  This specification defines optional differentiable
resampling components for a future BayesFilter-owned DPF.  It does not
authorize code implementation, production defaults, or HMC/posterior claims.

## Scope And Boundary

- Authority inputs: DPF0 obligations, DPF1 classical resampling semantics,
  `ch32_diff_resampling_neural_ot.tex`, IE5/IE6 DPF monograph evidence, and
  DPF0-A patch recommendations.
- Student artifacts are comparison-only usability context.
- No production `bayesfilter/` code, vendored student code, monograph chapter,
  or high-dimensional lane artifact is edited, imported, executed, or copied.

## Skeptical Plan Audit

| Check | Status | Notes |
| --- | --- | --- |
| Stale context | pass | DPF1 was Claude-accepted for DPF2 start. |
| Wrong baseline | pass | Hard categorical resampling from DPF1 remains the classical baseline. |
| Proxy overclaim | pass | Finite output/gradient and residual smokes are component diagnostics only. |
| Missing stop conditions | pass | Missing bias label, teacher provenance, or gradient-object label blocks promotion. |
| Hidden production/monograph drift | pass | DPF2 writes plan artifacts only. |
| Vendored-code contamination | pass | Student implementations are not copied, edited, executed, or imported. |
| High-dimensional-lane contamination | pass | Learned/neural paths do not use the separate high-dimensional lane. |
| Artifact fitness | pass | The spec states component inputs, outputs, gradients, bias/proxy semantics, tests, and non-implications. |

## Component Families

| Component | Mathematical object | Inputs | Outputs | Gradient route | Status |
| --- | --- | --- | --- | --- | --- |
| Hard categorical resampling | Ancestor draw from `Categorical(w)` | particles `X`, normalized weights `w`, seed/key | equal-weight cloud selected from ancestors | none pathwise through ancestor draw | baseline only |
| Soft resampling | Interpolation between sampled ancestor and weighted mean | `X`, `w`, `alpha`, seed/key, optional ancestor policy | equal-weight surrogate cloud | branchwise through mean/interpolation if ancestor fixed; further relaxation must be named | optional relaxed component |
| Unregularized OT projection | Coupling solving unregularized OT | `X`, `w`, target marginal `u`, cost `C` | coupling or barycentric cloud | not first implementation target | reference/deferred |
| Entropic OT optimizer | `Pi_epsilon*` solving EOT | `X`, `w`, `u`, `C`, `epsilon` | EOT coupling and barycentric cloud | implicit/KKT under regularity | optional relaxed component after residual contract |
| Finite Sinkhorn | `Pi_{epsilon,K}` computed by declared solver | `X`, `w`, `u`, `C`, `epsilon`, `K`, stabilization, tolerance | numerical coupling and barycentric cloud | unrolled autodiff or implicit fixed point, explicitly named | optional numerical component |
| Learned/amortized OT | Parametric student map imitating a named teacher | weighted cloud, teacher id, architecture, checkpoint/provenance | cloud, coupling, or summary | autodiff through student map | deferred |
| Neural/transformer resampling | Learned map with neural resampling semantics | architecture and training inputs | resampled cloud/proposal | autodiff through model | deferred/debug gate |

## Required Component Fields

Each future component implementation must record:

- component id and object class;
- particle shape, weight shape, dtype, and device;
- seed/key policy and whether ancestor randomness is sampled, fixed, relaxed, or
  marginalized;
- parameters such as `alpha`, `epsilon`, Sinkhorn iteration budget, tolerance,
  stabilization, cost function, target marginal, and gradient path;
- finite output and finite gradient checks where a gradient path exists;
- bias/proxy label;
- downstream non-implications;
- artifact provenance, especially for learned/neural components.

## Promotion Boundaries

| Evidence | Allowed conclusion | Forbidden conclusion |
| --- | --- | --- |
| Soft-resampling affine/mean preservation | The selected affine/mean summary is preserved in conditional expectation under stated assumptions. | Full categorical-law preservation or nonlinear unbiasedness. |
| Soft-resampling finite gradient | The chosen surrogate path has finite derivative on the tested branch. | Original likelihood-score validity or posterior preservation. |
| Sinkhorn residual pass | The finite numerical plan has bounded marginal residuals under stated epsilon/budget/stabilization. | Exact unregularized OT, categorical equivalence, or HMC target validity. |
| Learned map MSE/residual | Student approximates a declared teacher on a declared distribution if provenance exists. | Out-of-distribution correctness, posterior preservation, or production readiness. |

## DPF2 Decision

Soft and finite Sinkhorn/EOT-style resampling can be specified as optional
relaxed components.  Learned/amortized OT and neural resampling remain deferred
until provenance-bearing component specs exist.
