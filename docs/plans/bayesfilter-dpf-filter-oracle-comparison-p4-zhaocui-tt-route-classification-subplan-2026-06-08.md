# P4 Subplan: Zhao-Cui and Fixed-Design TT Route Classification

metadata_date: 2026-06-08
phase: P4
status: REVIEWED_READY_AFTER_P3_PASS

## Question

For which targets can Zhao-Cui or BayesFilter fixed-design TT-style routes act
as master-schema claim classes for DPF value and gradient comparisons, with
Kalman-tied sanity checks recorded only as auxiliary diagnostic notes?

## Evidence Contract

Baseline/comparator:

- exact Kalman for LGSSM;
- dense/refined quadrature for small nonlinear targets;
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase1-lgssm-exact-reference-result-2026-06-05.md`;
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase7-integration-closeout-result-2026-06-05.md`;
- `docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json`;
- `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase5-cross-model-error-calibration-result-2026-06-08.md`.

Primary criteria:

- classify every Zhao-Cui/fixed-design TT route using exactly the master claim
  classes: `EXACT_ORACLE`, `CERTIFIED_APPROXIMATION`,
  `SURROGATE_USEFULNESS`, `DIAGNOSTIC_ONLY`, or `BLOCKED`;
- record Kalman-tied sanity checks only as auxiliary diagnostics within one of
  those classes, normally `DIAGNOSTIC_ONLY` unless an exact or certified
  approximation criterion is separately satisfied;
- require same-target value evidence before any gradient comparison;
- record branch/fixed-design hashes and basis/rank settings for runnable rows;
- preserve blocked multistate rows rather than forcing comparisons.

Veto diagnostics:

- scalar-only route applied to multistate target without reviewed adapter;
- adaptive TT fit or branch mutation hidden inside a fixed-branch gradient
  claim;
- fit residual promoted to likelihood correctness;
- Zhao-Cui route treated as oracle where only dense/Kalman can be exact.

Explanatory-only diagnostics:

- TT rank, basis size, fit residual, holdout residual, retained mass residual,
  wall time, and branch hashes.

What will not be concluded:

- no paper-scale Zhao-Cui reproduction;
- no adaptive MATLAB behavior reproduction;
- no coupled multivariate TT claim without an implemented route.

## Tasks

1. Inventory current Zhao-Cui/highdim code paths.
2. Map each P0 target row to available or blocked TT routes.
3. Add or update route classification artifacts.
4. For runnable rows, require value evidence against exact/dense reference.
5. For gradient rows, require fixed-branch score contract and P42 diagnostics.
6. Run Claude review.

## Planned Commands And Artifacts

Runner status:
planned module; P4 `PRECHECK` must implement this runner, select an existing
runner by reviewed amendment, or write a blocker before any execution claim.

Planned command template:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p4_zhaocui_tt_route_classification_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p4_zhaocui_tt_route_classification_tf --validate-only
```

If P4 remains classification-only and does not need TensorFlow execution, the
phase may replace this with a pure Python registry validator through a reviewed
amendment before execution.

Required artifacts:

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p4_zhaocui_tt_route_classification_2026-06-08.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p4-zhaocui-tt-route-classification-2026-06-08.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p4-zhaocui-tt-route-classification-result-2026-06-08.md`
- Phase Claude review ledger:
  `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p4-claude-review-ledger-2026-06-08.md`

Claude result or blocker review follows the master max-five read-only loop.

## Exit Criteria

P4 exits with `PASS_P4_ZHAOCUI_ROUTE_CLASSIFICATION_READY_FOR_P5` when all
target rows have explicit Zhao-Cui route classifications and P5 eligibility is
known.

## Stop Conditions

- route cannot be classified without a scientific target decision;
- exact/dense reference disagrees with the fixed-design route beyond reviewed
  tolerance;
- Claude and Codex disagree on whether a route is oracle-grade after five
  rounds.
