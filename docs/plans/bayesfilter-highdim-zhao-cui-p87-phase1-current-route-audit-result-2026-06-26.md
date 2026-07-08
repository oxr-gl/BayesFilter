# P87 Phase 1 Result: Current Route Audit

Date: 2026-06-26

Status: `P87_PHASE1_CURRENT_ROUTE_AUDIT_BLOCKS_ANALYTICAL_PROMOTION_REVIEWED`

## Decision

Phase 1 classifies the current unpromoted SIR d18 filter-score route as
blocked for analytical-gradient promotion.

The current route has local analytical SIR score/Jacobian helpers, but the
filter-level target derivative backend still uses
`tensorflow_forward_accumulator_for_model_log_density` and the implementation
contains `tf.autodiff.ForwardAccumulator`. Therefore
`BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT` remains active until Phase 2 repairs
the promoted route or explicitly preserves the downgrade.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the current unpromoted filter score route analytical, JVP-backed diagnostic, or blocked? |
| Baseline/comparator | Current code and P81 analytical derivative route correction. |
| Primary criterion | Met for audit: derivative components were classified; any `ForwardAccumulator` in the promoted path triggers `BLOCK_ANALYTICAL_ROUTE_HAS_JVP_COMPONENT`. |
| Veto diagnostics | Active: the filter-level target derivative backend is JVP-backed. |
| Explanatory diagnostics | Backend strings, function names, tests covering local model formulas. |
| Not concluded | No code repair, no analytical-gradient correctness, no full-history d18 readiness, no source-route correctness, no HMC/production readiness. |
| Artifact | This Phase 1 result and the refreshed Phase 2 subplan. |

## Derivative Component Classification

| Component | Evidence | Classification | Consequence |
| --- | --- | --- | --- |
| SIR transition mean parameter Jacobian | `bayesfilter/highdim/models.py:727` defines `transition_mean_parameter_jacobian`; `tests/highdim/test_p81_analytical_sir_score.py:202` compares it with `GradientTape`. | Local analytical formula with diagnostic autodiff test. | Eligible for Phase 3 local algebra certification; not sufficient for filter-level promotion. |
| SIR transition log-density parameter score | `bayesfilter/highdim/models.py:754` calls the analytical transition mean Jacobian; `tests/highdim/test_p81_analytical_sir_score.py:227` compares with `GradientTape`. | Local analytical formula with diagnostic autodiff test. | Eligible for Phase 3 local algebra certification; not sufficient for filter-level promotion. |
| SIR observation log-density parameter score | `bayesfilter/highdim/models.py:775` defines an analytical observation score; `tests/highdim/test_p81_analytical_sir_score.py:227` compares with `GradientTape`. | Local analytical formula with diagnostic autodiff test. | Eligible for Phase 3 local algebra certification; not sufficient for filter-level promotion. |
| Infectious-components VJP scatter | `tests/highdim/test_p81_analytical_sir_score.py:270` verifies scatter of observation cotangent to full state. | Local analytical mapping helper with diagnostic test. | Supports local algebra coverage only. |
| Scalar fixed-design filter score path | `bayesfilter/highdim/filtering.py:1130` and `:1369` report `tensorflow_forward_accumulator_for_model_log_density`. | JVP-backed diagnostic route. | Cannot be called analytical. |
| Multistate fixed-design filter score path, multi-parameter wrapper | `bayesfilter/highdim/filtering.py:1466` reports `tensorflow_forward_accumulator_for_model_log_density`. | JVP-backed diagnostic route. | Cannot be called analytical. |
| Multistate fixed-design filter score path, single-parameter route | `bayesfilter/highdim/filtering.py:1703` reports `tensorflow_forward_accumulator_for_model_log_density`. | JVP-backed diagnostic route. | Cannot be called analytical. |
| Forward-mode target log derivative primitive | `bayesfilter/highdim/filtering.py:4316` defines `_scalar_target_log_derivative_by_forward_accumulator`; `:4327` enters `tf.autodiff.ForwardAccumulator`. | Autodiff/JVP implementation primitive. | This is the active blocker for analytical-gradient promotion. |
| Horizon-0 SIR d18 smoke | `tests/highdim/test_p81_analytical_sir_score.py:132` runs horizon-0 and checks finite score/FD rows; `:166` asserts `horizon == 0`. | Diagnostic horizon-0 smoke only. | `BLOCK_HORIZON0_OVERCLAIM` remains active for full-history claims. |
| Two-row SIR d18 all-grid transition | `tests/highdim/test_p81_analytical_sir_score.py:169` expects `COMPLEXITY_GATE`. | Explicit d18 all-pairs/all-grid blocker evidence. | `BLOCK_D18_ALL_PAIRS_DRIFT` remains active for full-history route claims. |

## Checks Run

Fail-closed Phase 1 local checks:

```bash
set -euo pipefail
rg -n "ForwardAccumulator|target_derivative_backend|multistate_nonlinear_fixed_design_tt_score_path|transition_log_density_parameter_score|observation_log_density_parameter_score|transition_mean_parameter_jacobian" bayesfilter/highdim/filtering.py bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py
rg -n "multistate_nonlinear_fixed_design_tt_score_path\\(|finite_difference_table|analytic_gradient" bayesfilter/highdim/filtering.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p81_analytical_sir_score.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

All checks completed successfully.

## Phase 2 Handoff

Phase 2 should execute the analytical-route repair/block decision. The concrete
repair target is the filter-level target derivative backend:

- remove or bypass `tf.autodiff.ForwardAccumulator` from any route that will be
  promoted as analytical; or
- explicitly record that analytical-gradient promotion remains blocked and
  keep the current route diagnostic-only.

The Phase 2 subplan remains valid after refresh because it already targets the
JVP-backed backend and requires either a JVP-free promoted route or a blocker
record.

## What Is Not Concluded

This Phase 1 audit does not establish analytical-gradient correctness,
full-history d18 feasibility, source-route correctness, HMC readiness,
production readiness, LEDH comparison, GPU performance, d50/d100 scaling, or
any default-policy change.
