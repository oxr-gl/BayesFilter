# Claude Read-Only Review Bundle

Date: 2026-07-08
Review name: `bayesfilter-quadratic-map-covariance-initializer-phase0`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review whether the Phase 0 planning bundle is sufficient and safe to start
implementation of a reusable BayesFilter quadratic MAP-covariance initializer.

The intended design is: use BFGS/L-BFGS only as a finite local neighborhood
locator; use constrained SPD quadratic geometry as covariance/precision
authority; validate and report diagnostics without making MAP, posterior, or
HMC-readiness claims.

## Artifacts To Inspect

- `docs/plans/bayesfilter-quadratic-map-covariance-initializer-master-program-2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-map-covariance-initializer-phase0-governance-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-map-covariance-initializer-visible-gated-execution-runbook-2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-map-covariance-initializer-visible-execution-ledger-2026-07-08.md`
- `bayesfilter/inference/quadratic_geometry.py`
- `bayesfilter/inference/mass_matrix.py`
- `tests/test_quadratic_geometry.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the Phase 0 artifacts define a correct, bounded implementation path for the reusable initializer? |
| Baseline/comparator | Existing reusable `fit_low_rank_spd_quadratic_geometry`, mass-matrix helpers, and benchmark-local MAP helper pattern. |
| Primary criterion | The plan must encode BFGS as locator only, SPD quadratic fit as covariance source, sample-budget guard, fail-closed behavior, focused tests, and explicit nonclaims. |
| Veto diagnostics | Missing stop condition, unsupported MAP/HMC claim, BFGS inverse Hessian used as covariance authority, artifact mismatch, insufficient review/repair loop, or implementation scope that bypasses local checks. |
| Explanatory diagnostics | Suggestions about API names, tests, diagnostics, and clearer boundaries. |
| Numeric provenance | `5 * n_regression_parameters` is user-directed; condition caps/tolerances are inherited from existing geometry helpers or hypotheses until tested; no numeric value may be treated as scientific truth. |
| Not concluded | No implementation correctness, global MAP, posterior covariance correctness, HMC readiness, sampler convergence, statistical superiority, default readiness, or Zhao-Cui source faithfulness. |

## Review Questions

1. Is there a material correctness or boundary issue in the master program,
   Phase 0 subplan, or runbook?
2. Is the evidence contract internally consistent?
3. Are required artifacts and checks sufficient for Phase 0 and for entering
   implementation?
4. Are there unsupported claims or hidden authority transfers?
5. Are there unsupported numeric defaults that were invented, inherited, or
   overcommitted without provenance?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
