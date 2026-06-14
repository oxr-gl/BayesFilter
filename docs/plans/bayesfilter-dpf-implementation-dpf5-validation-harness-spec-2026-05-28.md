# DPF5 Validation Harness Specification

## Status

DPF5 execution artifact.  This specification defines the validation harness and
benchmark ladder needed before any BayesFilter-owned DPF implementation can be
ranked, promoted, or considered for production-boundary review.

## Scope And Boundary

- Authority inputs: DPF0-DPF4 outputs, DPF monograph evidence reports,
  controlled-baseline reports, student reports as comparison-only context, and
  the production checklist.
- DPF5 defines harness requirements only; it does not implement benchmark code.
- No production `bayesfilter/` code, vendored student code, monograph chapter,
  or high-dimensional lane artifact is edited, imported, executed, or copied.

## Skeptical Plan Audit

| Check | Status | Notes |
| --- | --- | --- |
| Stale context | pass | DPF4 was Claude-accepted for DPF5 start. |
| Wrong baseline | pass | Independent references and DPF1-DPF4 contracts precede student/controlled comparison rows. |
| Proxy overclaim | pass | Proxy RMSE, ESS, runtime, finite gradients, and student agreement cannot promote correctness. |
| Missing stop conditions | pass | Failed veto diagnostics block rankings and downstream promotion. |
| Hidden production/monograph drift | pass | DPF5 writes plan artifacts only. |
| Vendored-code contamination | pass | Student code is not copied, executed, edited, or imported. |
| High-dimensional-lane contamination | pass | No separate high-dimensional lane artifact is used. |
| Artifact fitness | pass | The harness separates correctness, numerical, gradient, proxy, performance, and production ledgers. |

## Harness Tiers

| Tier | Name | Purpose | Primary criterion | Veto first? |
| --- | --- | --- | --- | --- |
| H0 | Import and boundary scan | Ensure production/tests do not import student baselines. | No student-baseline imports in `bayesfilter` or `tests`. | yes |
| H1 | Classical LGSSM recovery | Check DPF1 classical PF against analytic Kalman reference. | Finite estimates and declared residual/MCSE contract. | yes |
| H2 | Affine PF-PF parity | Check DPF3 density-ratio, log-det, and corrected-weight algebra. | Residuals within deterministic tolerance. | yes |
| H3 | Resampling component residuals | Check DPF2 soft/Sinkhorn object-level contracts. | Bias/proxy labels and marginal residual tolerances pass. | yes |
| H4 | Same-scalar gradient checks | Check DPF4 value/gradient semantics on named scalars. | Finite and parity-checked gradients for same scalar. | yes |
| H5 | Controlled nonlinear range-bearing fixture | Exercise integrated filtering on bounded nonlinear fixture. | Finite rows with proxy labels and reference/proxy comparator ids. | yes |
| H6 | Student/controlled qualitative comparison | Compare against frozen student/controlled aggregate evidence. | Same-regime labels only, never promotion. | no, explanatory |
| H7 | Performance/runtime envelope | Measure runtime/memory after correctness vetoes pass. | Runtime and memory rows with CPU/GPU policy. | no, after vetoes |

## Veto Ordering

The harness must evaluate in this order:

1. source/import boundary;
2. finite values and structured failures;
3. independent reference residuals;
4. proposal/Jacobian/weight parity;
5. component residual and bias labels;
6. same-scalar value/gradient checks;
7. Monte Carlo uncertainty and seed policy;
8. only then proxy comparison and runtime ranking.

If any veto tier fails, speed, ESS, proxy RMSE, and student same-regime
comparison must not be ranked as if the method were valid.

## Required Artifact Ledgers

- mathematical claim ledger;
- engineering correctness ledger;
- numerical validity ledger;
- gradient validity ledger;
- proxy comparison ledger;
- performance ledger;
- production readiness ledger.

No ledger may promote into another without an explicit criterion in the result
note.
