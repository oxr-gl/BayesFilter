# P0 Subplan: Target-Route Registry and Claim Classes

metadata_date: 2026-06-08
phase: P0
status: REVIEWED_READY_FOR_PHASE_EXECUTION

## Question

Which model targets can support DPF value and gradient comparison against
Kalman, UKF, SVD/sigma-point, CUT4, and Zhao-Cui/fixed-design TT routes, and
what claim class is allowed for each route?

## Evidence Contract

Primary criterion:

- create a registry with one row per `target_id x route_id`;
- include target identity, state law, observation law, parameter vector,
  transform/Jacobian terms, route implementation path, value support, gradient
  support, claim class, promotion tolerance, certification band, blockers, and
  nonclaims;
- include `primary_gradient_statistic` for any row where P5 may compare
  gradients;
- classify each route as `EXACT_ORACLE`, `CERTIFIED_APPROXIMATION`,
  `SURROGATE_USEFULNESS`, `DIAGNOSTIC_ONLY`, or `BLOCKED`;
- identify which rows are eligible for P1-P5 execution.

Baseline/comparator:

- P42 validation classes;
- existing P45 target registry as a schema donor and blocker-pattern example
  only; P45 does not already cover LGSSM, tiny nonlinear dense-oracle rows, or
  simple transformed/KSC rows required by this program;
- existing code/test inventory under `bayesfilter/`, `experiments/`, and
  `tests/highdim/`.

Veto diagnostics:

- missing target identity;
- missing parameterization;
- missing `promotion_tolerance` or `certification_band`;
- missing `primary_gradient_statistic` for a gradient-eligible row;
- approximate route labeled exact without proof;
- route omitted because it is blocked;
- DPF route declared comparable without seed/evaluator-variance plan;
- gradient support declared without same-parameterization contract.

Explanatory-only diagnostics:

- current test coverage, implementation path availability, fixture size, and
  expected resource cost.

What will not be concluded:

- no numerical value or gradient agreement;
- no HMC readiness;
- no production readiness.

## Required Initial Target Rows

At minimum P0 must classify:

- LGSSM with exact Kalman value and analytic gradient;
- tiny scalar/2D nonlinear additive-Gaussian closures with dense quadrature
  potential;
- simple transformed SV and KSC-style mixture approximation rows;
- generalized SV native and transformed diagnostics;
- spatial SIR additive-Gaussian closure and native/non-Gaussian blocked row;
- predator-prey additive-Gaussian closure and native/non-Gaussian blocked row.

## Required Route IDs

- `kalman_exact`
- `dense_refined_quadrature`
- `ukf`
- `svd_sigma_point`
- `cut4`
- `zhao_cui_fixed_design_tt`
- `dpf_bootstrap_ot`
- `dpf_ledh_pfpf_ot`

## Tasks

1. Build the registry artifact under `docs/plans/`.
2. Add a test or script-level validator if the registry is machine-readable.
3. Record row-level tolerances before numerical execution.
4. Record blocked rows explicitly.
5. Record P1-P5 eligibility lists.
6. Run Claude read-only governance review.

## Planned Artifacts And Review Gate

Runner status:
planned validator; P0 `PRECHECK` must implement this validator, select an
existing validator by reviewed amendment, or write a blocker/manual-audit
justification before any execution claim.

- Planned validation commands:

```bash
python -m json.tool docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p0_registry_tf --validate-only
```

The P0 phase must create or explicitly waive the validator module before
claiming execution.  If no validator is created, the phase result must record a
reviewed blocker or a reviewed reason that `json.tool` plus manual ledger audit
is sufficient for P0 only.

- Registry:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-target-route-registry-2026-06-08.json`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p0-target-route-registry-result-2026-06-08.md`
- Phase Claude review ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p0-claude-review-ledger-2026-06-08.md`

Claude review follows the master max-five read-only loop.  If material registry
or claim-class findings remain after five iterations, P0 exits
`BLOCKED_FOR_HUMAN_REVIEW`.

## Exit Criteria

P0 exits with `PASS_P0_TARGET_ROUTE_REGISTRY_READY_FOR_P1` only if the registry
is complete, blocked rows are explicit, and Claude review returns
`VERDICT: AGREE`.

## Stop Conditions

- a target cannot be described in the same mathematical notation across routes;
- a route's value or gradient surface is unknown and cannot be classified from
  local code/docs;
- Claude and Codex do not converge on claim classes after five review rounds.
