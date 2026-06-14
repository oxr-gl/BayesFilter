# DPF4 Objective Classification Ledger

## Status

DPF4 execution artifact.  This ledger classifies every DPF scalar/objective
that may be differentiated.  It does not validate HMC, posterior correctness,
or production use.

## Scope And Boundary

- Authority inputs: DPF0-DPF3 outputs, `ch19e_dpf_hmc_target_suitability.tex`,
  `ch19f_dpf_debugging_crosswalk.tex`, and DPF monograph evidence reports.
- Student artifacts are comparison-only context.
- No production `bayesfilter/` code, vendored student code, monograph chapter,
  or high-dimensional/HMC lane artifact is edited, imported, executed, or
  copied.

## Skeptical Plan Audit

| Check | Status | Notes |
| --- | --- | --- |
| Stale context | pass | DPF3 was Claude-accepted for DPF4 start. |
| Wrong baseline | pass | Objectives are classified from DPF0-DPF3 contracts, not student HMC claims. |
| Proxy overclaim | pass | Finite gradients and smoke losses are not posterior/HMC evidence. |
| Missing stop conditions | pass | Ambiguous scalar or target status blocks HMC/posterior wording. |
| Hidden production/monograph drift | pass | DPF4 writes plan artifacts only. |
| Vendored-code contamination | pass | No student code or notebooks are used as authority. |
| High-dimensional-lane contamination | pass | External high-dimensional/HMC lanes are not used as authority. |
| Artifact fitness | pass | The ledger maps each scalar to target status, gradient meaning, and non-implications. |

## Objective Ledger

| ID | Objective/scalar | Classification | Gradient meaning | Required evidence before stronger claim | What it is not |
| --- | --- | --- | --- | --- | --- |
| DPF4-O01 | True model log likelihood / posterior | exact likelihood/posterior target | derivative of exact scalar if available | Analytic/autodiff parity and sampler diagnostics | Not supplied by classical PF realization by default. |
| DPF4-O02 | Classical PF likelihood estimator value | randomized value-side estimator | no default pathwise score through resampling | Pseudo-marginal extended-space proof if used for MCMC | Not smooth surrogate HMC and not unbiased log likelihood. |
| DPF4-O03 | Fixed-randomness classical PF log estimate | diagnostic/fixed-randomness scalar | derivative only of whatever fixed path is differentiable | Same-scalar proof and discontinuity policy | Not original likelihood score or pseudo-marginal validity. |
| DPF4-O04 | Soft-resampling filtering scalar | relaxed/surrogate target | derivative of soft map under named alpha and ancestor policy | Bias tests, posterior sensitivity, same-scalar checks | Not categorical-resampling posterior. |
| DPF4-O05 | EOT/Sinkhorn filtering scalar | relaxed transport target | derivative of EOT or finite solver object, as named | Residual, epsilon/budget sensitivity, stabilization, same-scalar checks | Not unregularized OT or categorical likelihood gradient. |
| DPF4-O06 | Learned/amortized OT scalar | learned-surrogate target | derivative through learned map and retained teacher terms | Teacher/student provenance, OOD stress, posterior-error/correction evidence | Not original or teacher posterior by default. |
| DPF4-O07 | PF-PF corrected particle scalar | proposal-corrected research candidate | derivative of corrected scalar including density and log-det terms | Jacobian/log-det audit, finite-particle variance, same-scalar checks | Not HMC-validity theorem or production target. |
| DPF4-O08 | Component training loss | component loss | derivative of training objective | Teacher/objective provenance and downstream filter evidence | Not filtering likelihood or posterior target. |
| DPF4-O09 | Transport residual | diagnostic residual | derivative of residual if optimized | Link to downstream filtering effect | Not posterior validity. |
| DPF4-O10 | Runtime or speed objective | performance diagnostic | derivative usually N/A | Correctness gates before performance ranking | Not correctness or target evidence. |

## Target-Status Labels

Allowed target-status labels:

- `exact_likelihood_target`
- `pseudo_marginal_extended_space_candidate`
- `fixed_randomness_diagnostic`
- `relaxed_target`
- `learned_surrogate`
- `component_loss`
- `transport_residual`
- `performance_diagnostic`
- `blocked_unclassified`

Any HMC-facing artifact must choose one label and record why stronger labels do
not apply.
