# P87 Phase 1 Subplan: Current Route Audit

Date: 2026-06-26

Status: `REVIEWED_READY_FOR_PHASE1_READ_ONLY_ROUTE_AUDIT`

## Phase Objective

Audit the current value/score code path and classify every derivative component
before any analytical-gradient claim or repair.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed and froze no-regression blockers.
- The current claim level remains unpromoted.
- Phase 1 is read-only except result/ledger/subplan documentation.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase1-current-route-audit-result-2026-06-26.md`
- Derivative-component classification table in the result.
- Updated execution ledger.
- Drafted or refreshed Phase 2 subplan after the route audit, even if the
  update only records that the existing Phase 2 repair scope remains valid.

## Required Checks/Tests/Reviews

Local checks:

```bash
set -euo pipefail

rg -n "ForwardAccumulator|target_derivative_backend|multistate_nonlinear_fixed_design_tt_score_path|transition_log_density_parameter_score|observation_log_density_parameter_score|transition_mean_parameter_jacobian" bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py
rg -n "multistate_nonlinear_fixed_design_tt_score_path\\(|finite_difference_table|analytic_gradient" bayesfilter/highdim/filtering.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p81_analytical_sir_score.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Review:

- Claude read-only review of the Phase 1 result is required if the result
  proposes advancing to repair or downgrading the claim level.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the current unpromoted filter score route analytical, JVP-backed diagnostic, or blocked? |
| Baseline/comparator | Current code and P81 analytical derivative route correction. |
| Primary criterion | Every derivative component is classified, and any `ForwardAccumulator` in the promoted path triggers `BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT`. |
| Veto diagnostics | Missing route component, hidden JVP, unsupported analytical wording, or FD diagnostic promoted to proof. |
| Explanatory diagnostics | Backend strings, function names, tests covering local model formulas. |
| Not concluded | No code repair, no correctness, no full-history d18 readiness. |
| Artifact | Phase 1 result. |

## Forbidden Claims/Actions

- Do not edit code in Phase 1.
- Do not call JVP-backed route analytical.
- Do not run long tests or GPU commands.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only if:

- Phase 1 result gives a concrete repair target or says repair is unnecessary;
- the derivative-component classification table is complete;
- backend provenance is resolved enough to classify the route as analytical,
  JVP-backed diagnostic, or blocked;
- Claude agrees for any material promotion/downgrade;
- Phase 2 subplan lists exact files/tests allowed for repair.

## Stop Conditions

- Route audit cannot identify derivative backend provenance.
- Proposed advancement would call current JVP path analytical.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 1 result/close record.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 2 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
