# 1D LGSSM T4 Residual Solver Ladder Plan

## Question

After the proposal log-probability autodiff topology fix, the 1D LGSSM horizon
ladder shows BayesFilter and FilterFlow agreement at `T=4`, but both
implementations exceed the strict row-residual gate. This plan tests whether
that shared residual veto is explained by the annealed transport solver
settings `convergence_threshold` and `max_iterations`.

## Evidence Contract

- Comparator: current local patched `.localsource/filterflow` executable branch.
- Baseline fixture: existing `T4_extension` scalar-state LGSSM fixture from the
  horizon ladder.
- Primary criterion: BayesFilter and FilterFlow must match each other in trigger
  pattern, scalar, step ledger, and AD gradient under the existing tolerances.
- Residual veto: max row/column residual must be below the existing `1e-4`
  tolerance for a residual-resolved decision.
- Explanatory diagnostics: finite-difference gradients, FilterFlow-vs-BayesFilter
  finite-difference deltas, and BayesFilter iteration counts.
- Not concluded: mathematical correctness of either implementation, posterior
  correctness, production readiness, or general nonlinear-SSM validity.
- Artifact: JSON/report from
  `experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_t4_residual_solver_ladder_tf`.

## Skeptical Audit

This is a narrow solver-setting ladder, not a new correctness baseline. It does
not treat finite-difference agreement as the comparator promotion criterion.
It keeps the baseline fixed to the same T4 numeric fixture and changes only
`convergence_threshold` and `max_iterations`. If the residual remains above the
gate under tighter settings while BayesFilter and FilterFlow continue to match,
the next question is residual-definition/algorithmic semantics, not a
cross-implementation bug.

## Configurations

| Config | convergence threshold | max iterations |
| --- | ---: | ---: |
| `baseline_1e-6_iter200` | `1e-6` | `200` |
| `threshold_1e-7_iter200` | `1e-7` | `200` |
| `threshold_1e-6_iter500` | `1e-6` | `500` |
| `threshold_1e-8_iter500` | `1e-8` | `500` |

