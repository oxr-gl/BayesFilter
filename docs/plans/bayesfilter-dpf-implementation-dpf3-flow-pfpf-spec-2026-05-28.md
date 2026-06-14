# DPF3 Particle-Flow / PF-PF Specification

## Status

DPF3 execution artifact.  This specification defines the BayesFilter-owned
particle-flow / PF-PF proposal-correction contract.  It does not implement code
or validate nonlinear filtering correctness.

## Scope And Boundary

- Authority inputs: DPF0-DPF2 outputs, `ch19c_dpf_implementation_literature.tex`,
  IE4 affine-flow PF-PF evidence, and controlled range-bearing proxy reports.
- Student EDH/PFPF artifacts are comparison-only context.
- No production `bayesfilter/` code, vendored student code, monograph chapter,
  or high-dimensional lane artifact is edited, imported, executed, or copied.

## Skeptical Plan Audit

| Check | Status | Notes |
| --- | --- | --- |
| Stale context | pass | DPF2 was Claude-accepted for DPF3 start on iteration 3. |
| Wrong baseline | pass | DPF3 baseline is DPF1 classical PF plus monograph PF-PF proposal correction, not student EDH/PFPF output. |
| Proxy overclaim | pass | Student and controlled RMSE/ESS/runtime rows remain comparison-only. |
| Missing stop conditions | pass | Missing Jacobian/proposal/target binding blocks movement. |
| Hidden production/monograph drift | pass | DPF3 writes plan artifacts only. |
| Vendored-code contamination | pass | No student code is copied, edited, executed, or imported. |
| High-dimensional-lane contamination | pass | No separate high-dimensional lane artifact is used. |
| Artifact fitness | pass | The spec states proposal density, Jacobian correction, corrected weights, tests, and exclusions. |

## PF-PF Object Contract

| Object | Requirement |
| --- | --- |
| Ancestor state | State after previous filtering/resampling decision; artifact must record ancestor policy. |
| Pre-flow proposal | Density `q_{t,0}(x_{t,0}|x_{t-1}, y_t)` or bootstrap prior proposal. |
| Flow map | Differentiable map `x_{t,1} = Phi_t(x_{t,0})` on the proposal support used. |
| Invertibility | Local inverse/pre-image and nonsingular forward Jacobian on weighted paths, or structured blocker. |
| Forward log determinant | `log |det D Phi_t(x_{t,0})|`, with sign convention explicitly recorded. |
| Post-flow proposal | `q_{t,1}(x_{t,1}) = q_{t,0}(x_{t,0}) |det D Phi_t(x_{t,0})|^{-1}`. |
| Target density | One-step target factor proportional to observation density times transition density at post-flow state. |
| Corrected log weight | `log p(y_t|x_{t,1}) + log p(x_{t,1}|x_{t-1}) - log q_{t,0}(x_{t,0}) + log |det D Phi_t(x_{t,0})|`. |
| Normalization | Stable log-sum-exp with unnormalized and normalized residual checks. |

## Flow Family Classification

| Family | Status | Required evidence |
| --- | --- | --- |
| Affine EDH special case | first-rung analytic/parity reference | Closed-form pushforward density, log-det sign, corrected-weight parity. |
| LEDH/local flow | candidate after path-specific Jacobian contract | Per-particle map and log-det contract; no EDH determinant reuse unless maps match. |
| Nonlinear range-bearing PF-PF | controlled-fixture diagnostic | Finite outputs, finite weights, reference/proxy labels, ESS/resampling/runtime rows. |
| Stochastic flow | deferred clean-room spec | Target/proposal, covariance/noise semantics, Jacobian or density correction, validation fixture. |
| Kernel PFF | excluded pending debug | Separate convergence/debug gate before routine panels. |

## Required Artifact Fields

Future PF-PF artifacts must record:

- model/fixture id, time horizon, particle count, flow steps, flow family;
- target density id and proposal density id;
- pre-flow and post-flow state binding;
- forward-log-det convention and residual checks;
- unnormalized corrected log weights and normalized weights;
- finite checks for states, densities, log determinants, and weights;
- affine parity or controlled-fixture comparator id;
- seed/dtype/device/CPU-GPU status;
- non-implications for nonlinear correctness, posterior, HMC, production, and
  student agreement.

## DPF3 Decision

Proposal-corrected affine/EDH-style PF-PF can be specified as a BayesFilter
experimental path after DPF1.  Nonlinear and local-flow variants require
controlled diagnostics.  Stochastic flow is deferred and kernel PFF remains
excluded.
