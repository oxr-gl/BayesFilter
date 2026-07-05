# Experiment result: Meta OT-aligned retained-Sinkhorn evaluation on the expanded heldout regime under a better evidence contract

## Plan reference
- `docs/plans/bayesfilter-neural-ot-metaot-refit-better-evidence-contract-plan-2026-06-28.md`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_teacher_data_expanded_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_low_budget_eval_expanded_tf
```

## Result summary
- The expanded donor-aligned teacher-data artifact regenerated successfully.
- The broader donor-aligned evaluation completed successfully.
- Decision: `RETAINED_TEACHER_SINKHORN_EXPANDED_HELDOUT_LOCAL_USEFULNESS_ON_DISCRIMINATING_BUDGETS`
- Local usefulness persists on the broader heldout regime at discriminating budgets.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| Initial train loss | `1.851e+01` | Donor-aligned objective starts high but finite on the expanded artifact |
| Final train loss | `-9.090e-01` | Donor-aligned objective improves strongly during training |
| Heldout log_u loss | `7.393e-01` | One-half heldout fit is finite; not itself a promotion criterion |
| Budget 5 regime | `discriminating` | Zero-init is not saturated here, so this rung supports local usefulness interpretation |
| Budget 5 student mean RMSE | `1.644e-05` | Better than zero-init on the broader discriminating low-budget rung |
| Budget 5 zero-init mean RMSE | `5.921e-05` | Baseline remains materially non-exact |
| Budget 5 better-or-equal count | `7/9` | Local usefulness persists on most broader heldout examples |
| Budget 10 regime | `discriminating` | Mid-budget rung remains informative |
| Budget 10 student mean RMSE | `3.372e-08` | Better than zero-init on the broader discriminating mid-budget rung |
| Budget 10 zero-init mean RMSE | `9.271e-08` | Baseline still not saturated |
| Budget 10 better-or-equal count | `2/9` | Mean improvement persists even though per-example wins are not universal |
| Budget 20 regime | `saturated_zero_init` | Explanatory only; not a valid algorithm-failure rung |
| Budget 20 student mean RMSE | `3.090e-09` | Student remains near-teacher but does not beat an exact/saturated baseline |
| Budget 20 zero-init mean RMSE | `0.000e+00` | Saturated zero-init baseline |

## Engineering observations
- The expanded teacher-data runner was updated to carry the same donor-aligned route metadata as the narrow artifact:
  - `meta_ot_refit_target_half = canonical_log_u`
  - `meta_ot_refit_complementary_recovery = teacher_side_sinkhorn_update`
  - `route_family = meta_ot_aligned_fixed_target_retained_sinkhorn_refit`
- The expanded evaluation runner was updated to use:
  - `prediction_head = meta_ot_log_u`
  - `loss_route = meta_ot_log_u_dual_objective_plus_teacher_log_u`
  - discriminating-versus-saturated budget labeling
- The broader artifact therefore stays semantically aligned with the donor-aligned refit rather than reusing the older pair-regression framing.

## Empirical evidence
- The donor-aligned one-half route still shows local usefulness after broadening the heldout split.
- The usefulness signal survives on both discriminating rungs (`5` and `10`).
- The saturated `20`-iteration rung still does not support promotion and should remain explanatory only.
- This strengthens the interpretation that the earlier “failure” framing was a contract/reporting problem, not a clear algorithm-failure signal.

## Mathematical claims
- None beyond the already-audited donor-aligned retained-teacher route definition. This result is empirical and contract-framed.

## Decision
- The broader better-contract run strengthens the evidence that the donor-aligned retained-Sinkhorn route has **local usefulness on discriminating budgets**.
- The route is still not justified as broadly promoted, because the evidence remains local to the deterministic LGSSM envelope and the saturated high-budget rung remains non-promoting.
- But the stronger heldout regime makes the local-usefulness conclusion more credible than the earlier tiny heldout result.

## Next step
- If stronger evidence is desired, the next justified move is no longer to ask whether the route has *any* local usefulness. It does.
- The next question should be whether that usefulness survives a broader envelope shift (e.g. different fixture family or stress slice) while keeping the same discriminating-budget framing.
