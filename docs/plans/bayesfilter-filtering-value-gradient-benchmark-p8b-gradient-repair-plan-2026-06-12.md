# P8b Gradient Repair Plan

Date: 2026-06-12

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the P8b benchmark repair its gradient holes by filling only gradient cells whose coordinate system, derivative path, and branch validity are explicit? |
| Baseline | Current P8b artifact `bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-results-2026-06-12.json`, where LGSSM Kalman has value/score/curvature and LGSSM UKF/SVD/CUT4 are value-only. |
| Primary criterion | Every newly promoted score cell must contain a finite score vector, score norm, min/max components, coordinate system, derivative provenance, and reason code; cells that cannot certify a derivative branch remain explicit blocked/pending cells. |
| Comparators | LGSSM Kalman exact score for the same synthetic dataset and physical theta `[phi1, phi2, phi3, q_scale, r_scale]`; existing sigma-point value cells must continue to match the Kalman value. |
| Veto diagnostics | Missing score provenance; silent `None` score in an executed-score cell; sigma-point value no longer matching Kalman on LGSSM; weak eigensystem branch reported as a real score; DPF gradient ranked before seed ladder and Monte Carlo standard error. |
| Explanatory diagnostics | Sigma-point branch metadata, finite score norms, value gaps to Kalman, current pending status for non-LGSSM rows. |
| Artifact | Updated P8b JSON/CSV/Markdown artifacts plus this plan and a result note under `docs/plans`. |
| Not concluded | Full Phase 8 closeout, nonlinear model gradient correctness, DPF gradient validity, Bayesian-estimation readiness, or a filter ranking. |

## Skeptical Plan Audit

Status: `PASS_WITH_NARROW_FIRST_SLICE`.

The first executable repair is intentionally narrow. The current missing-gradient table is not one problem:

- LGSSM UKF/SVD/CUT4 have deterministic TensorFlow value paths and existing sigma-point derivative APIs.
- KSC mixture SV has a value surrogate but no fast score adapter in the current P8b runner.
- DPF cells require fixed stochastic branches, seed ladders, and Monte Carlo standard errors before score interpretation.
- Nonlinear rows need target-specific score adapters and coordinate provenance before promotion.

The plan therefore does not use gradient norm alone as proof of correctness, does not treat finite autodiff as a certified DPF gradient, and does not convert all holes into numeric cells at once.

## Phase G1: LGSSM Deterministic Sigma-Point Scores

Goal: fill the LGSSM UKF/SVD/CUT4 score cells if the derivative branch is certifiable, while preserving exact value agreement with Kalman.

Implementation tasks:

1. Add a physical-theta first-derivative adapter for the current LGSSM structural model:
   - theta coordinates: `[phi1, phi2, phi3, q_scale, r_scale]`;
   - initial covariance derivative for stationary AR(1) variances;
   - transition derivative for diagonal `phi` and innovation scale `q_scale`;
   - observation covariance derivative for `r_scale`;
   - zero observation-map parameter derivative because the observation matrix is fixed.
2. Call the existing derivative APIs:
   - `tf_svd_ukf_score`;
   - `tf_svd_cubature_score`;
   - `tf_svd_cut4_score`.
3. Preserve branch guardrails:
   - if the analytic branch blocks on repeated eigenvalues or another guardrail, emit an explicit branch-blocked diagnostic cell;
   - do not report the blocked analytic score.
4. For LGSSM only, allow an affine-equivalence score fallback after a value tieout:
   - the fallback score is the Kalman autodiff score in the same physical theta coordinates;
   - it is allowed only when the sigma-point value matches Kalman to tolerance on the same data/theta;
   - provenance must say `lgssm_affine_equivalence`, not raw sigma-point autodiff.
5. Fill score fields only after successful execution or certified LGSSM affine-equivalence fallback:
   - `score`;
   - `score_l2_norm`;
   - `score_max_component`;
   - `score_min_component`;
   - `score_coordinate_system=physical_theta`;
   - `score_derivative_provenance=<backend>_analytic_first_order_<branch>`.
6. Keep Hessian status deferred unless a Hessian backend is actually run.

Pass criteria:

- P8b runner regenerates artifacts.
- LGSSM Kalman value/score remains present.
- LGSSM UKF/SVD/CUT4 either have real finite analytic score vectors, certified affine-equivalence score vectors, or explicit branch-block statuses.
- No test permits an `executed_numeric` score cell with missing provenance.
- Existing no-silent-holes and DPF seed-ladder guardrails still pass.

## Phase G2: KSC Mixture SV Score Adapter

Goal: decide whether the KSC mixture surrogate can expose a fast score in the same coordinate system as the value route.

Required before execution:

- confirm the surrogate theta coordinate contract;
- avoid labeling the surrogate score as native SV truth;
- add a separate result row or reason code if the score is for transformed synthetic theta only.

This phase is not part of the first executable slice unless G1 passes and the adapter is already available.

## Phase G3: Nonlinear Deterministic Filter Scores

Goal: add target-specific score adapters for deterministic filters on nonlinear rows.

Required before execution:

- model-specific derivative adapters;
- coordinate-system contract;
- branch diagnostics for SVD/CUT4 eigensystem paths;
- a reference or diagnostic interpretation rule that does not rank against a nonexistent exact oracle.

## Phase G4: DPF Gradient Diagnostics

Goal: run DPF score diagnostics only under a stochastic evidence contract.

Required before promotion:

- fixed seed and fixed branch definitions;
- particle-count ladder;
- seed ladder;
- Monte Carlo standard errors for value and score summaries;
- explicit separation between fixed-branch diagnostic gradients and resampling-invalid gradients.

DPF gradients remain blocked for ranking until these are present.

## Claude Review Loop

Claude is a read-only critical reviewer. The review asks whether the plan:

- promotes only certifiable gradients;
- preserves branch-blocked outcomes as blockers rather than failures to hide;
- keeps DPF and nonlinear score claims out of the first slice;
- includes enough tests and artifacts to prevent silent holes.

Convergence rule: accept if Claude reports no material blockers. Otherwise patch this plan and loop up to five reviews.

## Execution Commands

CPU-only commands:

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8_numeric.py
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8b_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_closure.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_fix_gates.py
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_run_p8_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8b_numeric.py
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8b_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-results-2026-06-12.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-value-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-score-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-curvature-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-status-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-stochastic-uncertainty-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-summary-2026-06-12.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-gradient-repair-plan-2026-06-12.md
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-results-2026-06-12.json
```

Claude review commands must use the trusted Claude worker wrapper with escalated permissions.
